#!/usr/bin/env python3
"""Static checks for the BUILT site. Standard library only.

    python3 scripts/build.py && python3 scripts/check_site.py

Checks dist/ (the output of build.py), i.e. exactly what gets deployed. Exits non-zero if anything fails, so it also runs in CI (.github/workflows/site.yml).

What it guards
  templates   no unrendered {{ }} / {% %} tokens left in any page
  structure   unique ids, working #anchors, every local href/src/srcset target exists
  images      alt text, width and height on every <img> (no layout shift)
  security    strict CSP present, no inline scripts/styles/handlers (the CSP forbids them),
              target=_blank links carry rel=noopener
  privacy     no email addresses or phone numbers anywhere in published files
  contact     every [data-contact] element ships hidden (form is never shown half-configured)
  analytics   the GoatCounter endpoint is allowed by the CSP's connect-src (else nothing is counted)
  seo         title, description, canonical, Open Graph image, valid JSON-LD, robots + sitemap
  weight      per-file size budgets
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_args = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
_args.add_argument("--dist", default="dist", help="built site folder (default: dist)")
DIST = (ROOT / _args.parse_args().dist).resolve()
if not DIST.is_dir():
    sys.exit(f"{DIST.name}/ not found. Run `python3 scripts/build.py` first.")

PAGES = ["index.html", "404.html"]
HOST = "https://neocass.com"

# Everything in dist/ is published. Third-party code under assets/vendor/ is reviewed when it is
# vendored (see its README) and is exempt from the privacy scan and the first-party size budgets.
VENDOR = "assets/vendor/"
PUBLISHED = [p for p in DIST.rglob("*") if p.is_file() and p.suffix in {".html", ".css", ".js", ".xml", ".txt"}
             and not p.relative_to(DIST).as_posix().startswith(VENDOR)]
VENDOR_BUDGET_KB = 80

BUDGET_KB = {".css": 30, ".js": 10, ".webp": 600, ".jpg": 400, ".png": 100, ".ico": 50}
# cv/ is published by the separate cv repository, so it is not in dist/.
EXTERNAL_PATHS = ("cv/",)

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+")
PHONE = re.compile(r"(?:tel:|\+\d)[\d\s().-]{7,}\d")

failures: list[str] = []
notes: list[str] = []


def fail(page: str, msg: str) -> None:
    failures.append(f"{page}: {msg}")


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.refs: list[tuple[str, str]] = []      # (attribute, value)
        self.imgs: list[dict] = []
        self.metas: list[dict] = []
        self.links: list[dict] = []
        self.inline_style = 0
        self.handlers = 0
        self.inline_scripts = 0
        self.jsonld: list[str] = []
        self.data_contact: list[dict] = []
        self.beacons: list[str] = []            # data-goatcounter endpoints
        self.title = ""
        self._in_title = False
        self._script: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if "style" in a:
            self.inline_style += 1
        self.handlers += sum(1 for k in a if k.startswith("on"))
        if "data-contact" in a:
            self.data_contact.append({"tag": tag, "hidden": "hidden" in a})
        if tag == "img":
            self.imgs.append(a)
        if tag == "meta":
            self.metas.append(a)
        if tag == "link":
            self.links.append(a)
        if tag == "title":
            self._in_title = True
        if tag == "script":
            if "data-goatcounter" in a:
                self.beacons.append(a["data-goatcounter"])
            if "src" in a:
                self.refs.append(("src", a["src"]))
            elif a.get("type") == "application/ld+json":
                self._script = "ld"
            else:
                self.inline_scripts += 1
        for attr in ("href", "src"):
            if attr in a and tag != "script":
                self.refs.append((attr, a[attr]))
        if "srcset" in a:
            for cand in a["srcset"].split(","):
                self.refs.append(("srcset", cand.strip().split()[0]))
        if tag == "a" and a.get("target") == "_blank" and "noopener" not in a.get("rel", ""):
            fail("html", f'target=_blank link without rel=noopener: {a.get("href")}')

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._script = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._script == "ld":
            self.jsonld.append(data)


def local_target(ref: str) -> Path | None:
    if re.match(r"(?:[a-z]+:)?//|mailto:|tel:|#", ref):
        return None
    path = ref.split("#")[0].split("?")[0]
    if not path or path == "/":
        return DIST / "index.html"
    if path.lstrip("/").startswith(EXTERNAL_PATHS):
        return None
    return DIST / path.lstrip("/")


parsed: dict[str, Page] = {}
for name in PAGES:
    p = Page()
    text = (DIST / name).read_text(encoding="utf-8")
    if re.search(r"\{\{|\{%", text):
        fail(name, "unrendered template token ({{ }} or {% %}) left in output")
    p.feed(text)
    parsed[name] = p

index_ids = set(parsed["index.html"].ids)

for name, p in parsed.items():
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup:
        fail(name, f"duplicate ids {sorted(dup)}")
    if not p.title.strip():
        fail(name, "missing <title>")
    if not any(m.get("name") == "viewport" for m in p.metas):
        fail(name, "missing viewport meta")

    csp = next((m["content"] for m in p.metas if m.get("http-equiv") == "Content-Security-Policy"), "")
    if "default-src 'none'" not in csp or "script-src 'self'" not in csp:
        fail(name, "strict Content-Security-Policy meta missing")
    if p.inline_style:
        fail(name, f"{p.inline_style} inline style attribute(s) (blocked by CSP)")
    if p.inline_scripts:
        fail(name, f"{p.inline_scripts} inline <script> (blocked by CSP)")
    if p.handlers:
        fail(name, f"{p.handlers} inline event handler(s) (blocked by CSP)")

    connect = re.search(r"connect-src([^;]*)", csp)
    allowed = connect.group(1).split() if connect else []
    for endpoint in p.beacons:
        origin = re.match(r"https://[^/]+", endpoint)
        if not origin or origin.group(0) not in allowed:
            fail(name, f"analytics endpoint {endpoint} is not https or not in the CSP connect-src")

    for img in p.imgs:
        src = img.get("src", "?")
        for need in ("alt", "width", "height"):
            if need not in img:
                fail(name, f"<img src={src}> missing {need}")

    for attr, ref in p.refs:
        target = local_target(ref)
        if target is not None and not target.exists():
            fail(name, f"{attr}={ref} does not exist")
        if ref.startswith("#") and ref != "#" and ref[1:] not in p.ids:
            fail(name, f"anchor {ref} has no matching id")
        if ref.startswith("/#") and ref[2:] not in index_ids:
            fail(name, f"anchor {ref} has no matching id on index.html")

    for el in p.data_contact:
        if not el["hidden"]:
            fail(name, f"<{el['tag']} data-contact> must ship with the hidden attribute")

# Index-only SEO requirements
idx = parsed["index.html"]
names = {m.get("name") for m in idx.metas} | {m.get("property") for m in idx.metas}
for need in ("description", "og:title", "og:description", "og:image", "og:url", "twitter:card"):
    if need not in names:
        fail("index.html", f"missing meta {need}")
if not any(l.get("rel") == "canonical" for l in idx.links):
    fail("index.html", "missing canonical link")
try:
    ld = json.loads("".join(idx.jsonld))
    if ld.get("@type") != "Person" or len(ld.get("sameAs", [])) < 3:
        fail("index.html", "JSON-LD Person needs at least three sameAs links")
except (ValueError, TypeError):
    fail("index.html", "JSON-LD is missing or not valid JSON")
og_image = next((m["content"] for m in idx.metas if m.get("property") == "og:image"), "")
if og_image and not (DIST / og_image.replace(HOST + "/", "")).exists():
    fail("index.html", f"og:image {og_image} does not exist on disk")

# robots + sitemap
robots = (DIST / "robots.txt").read_text(encoding="utf-8")
if f"Sitemap: {HOST}/sitemap.xml" not in robots:
    fail("robots.txt", "does not point at the sitemap")
for loc in re.findall(r"<loc>(.*?)</loc>", (DIST / "sitemap.xml").read_text(encoding="utf-8")):
    if not loc.startswith(HOST + "/"):
        fail("sitemap.xml", f"{loc} is not on {HOST}")

# Privacy: nothing personal in published files
for path in PUBLISHED:
    text = path.read_text(encoding="utf-8", errors="ignore")
    rel = path.relative_to(DIST)
    for m in EMAIL.findall(text):
        fail(str(rel), f"email address found: {m[:3]}…")
    for m in PHONE.findall(text):
        fail(str(rel), "phone-number-like string found")

# Size budgets
for path in DIST.rglob("*"):
    if path.is_file() and path.suffix in BUDGET_KB:
        kb = path.stat().st_size / 1024
        limit = VENDOR_BUDGET_KB if path.relative_to(DIST).as_posix().startswith(VENDOR) else BUDGET_KB[path.suffix]
        if kb > limit:
            fail(str(path.relative_to(DIST)), f"{kb:.0f} KB exceeds the {limit} KB budget")

# Informational
if "YOUR_WEB3FORMS_ACCESS_KEY" in (DIST / "index.html").read_text(encoding="utf-8"):
    notes.append("contact form: access key not set yet, so the form stays hidden on the live site")

for n in notes:
    print(f"note: {n}")
if failures:
    print(f"\n{len(failures)} problem(s):")
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print(f"OK: {len(PAGES)} pages, {len(PUBLISHED)} published text files checked.")
