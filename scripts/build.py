#!/usr/bin/env python3
"""Build the site into dist/. Standard library only.

    python3 scripts/build.py            # build
    python3 scripts/build.py --serve    # build, then preview at http://localhost:8000

What it does
  1. renders every src/pages/*.html, filling in shared partials from src/partials/
  2. copies public/ (css, js, images, icons, robots.txt, ...) into dist/ unchanged
  3. appends a content fingerprint (?v=<hash>) to the css/js/vendor URLs the pages reference

Template syntax (deliberately tiny; an unknown name or missing partial fails the build)
  {{ name }}                 value from the page's front matter, HTML-escaped
  {% include "file.html" %}  insert src/partials/file.html (it may use {{ }} and nest includes)

A page may start with a front-matter block of `key: value` lines between `---` markers.
Built-in values: `year` (current year). `base` should be "" on the home page and "/" on any
other page, so shared navigation links resolve from anywhere.
"""
from __future__ import annotations

import argparse
import datetime
import functools
import hashlib
import html
import http.server
import re
import shutil
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
PARTIALS = ROOT / "src" / "partials"
PUBLIC = ROOT / "public"

INCLUDE = re.compile(r'\{%\s*include\s+"([\w./-]+)"\s*%\}')
VARIABLE = re.compile(r"\{\{\s*(\w+)\s*\}\}")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# Stylesheets and scripts that pages reference get a content fingerprint (?v=<hash>), so a
# browser that cached an old copy can never be paired with newer HTML (GitHub Pages lets
# browsers cache for 10 minutes under an unchanged URL).
ASSET_REF = re.compile(r'((?:href|src)=")(/assets/(?:css|js|vendor)/[^"?#]+)(")')


def parse_page(text: str, name: str) -> tuple[dict[str, str], str]:
    """Split a page into (front-matter variables, template body)."""
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text
    variables: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            sys.exit(f"{name}: bad front-matter line: {line!r}")
        key, value = line.split(":", 1)
        variables[key.strip()] = value.strip()
    return variables, text[match.end():]


def render(template: str, variables: dict[str, str], where: str, depth: int = 0) -> str:
    if depth > 5:
        sys.exit(f"{where}: includes nested too deeply (loop?)")

    def include(match: re.Match) -> str:
        partial = PARTIALS / match.group(1)
        if not partial.is_file():
            sys.exit(f'{where}: partial "{match.group(1)}" not found in src/partials/')
        return render(partial.read_text(encoding="utf-8"), variables, partial.name, depth + 1)

    def variable(match: re.Match) -> str:
        key = match.group(1)
        if key not in variables:
            sys.exit(f'{where}: unknown variable "{{{{ {key} }}}}" (set it in the page front matter)')
        return html.escape(variables[key], quote=True)

    return VARIABLE.sub(variable, INCLUDE.sub(include, template))


def fingerprint(page_html: str, where: str) -> str:
    def stamp(match: re.Match) -> str:
        asset = PUBLIC / match.group(2).lstrip("/")
        if not asset.is_file():
            sys.exit(f"{where}: references {match.group(2)} but public/{match.group(2).lstrip('/')} does not exist")
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
        return f"{match.group(1)}{match.group(2)}?v={digest}{match.group(3)}"

    return ASSET_REF.sub(stamp, page_html)


def build(out: Path) -> None:
    if out.resolve() in (ROOT, ROOT.parent) or ROOT not in out.resolve().parents:
        sys.exit(f"refusing to build into {out}: output must be a folder inside the repo")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(PUBLIC, out)

    pages = sorted(PAGES.glob("*.html"))
    if not pages:
        sys.exit("no pages found in src/pages/")
    for page in pages:
        variables, body = parse_page(page.read_text(encoding="utf-8"), page.name)
        variables.setdefault("base", "")
        variables.setdefault("year", str(datetime.date.today().year))
        rendered = fingerprint(render(body, variables, page.name), page.name)
        (out / page.name).write_text(rendered, encoding="utf-8")
    print(f"built {len(pages)} page(s) + {sum(1 for p in PUBLIC.rglob('*') if p.is_file())} static file(s) -> {out.relative_to(ROOT)}/")


def serve(out: Path, port: int) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as server:
        print(f"serving {out.relative_to(ROOT)}/ at http://localhost:{port} (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--out", default="dist", help="output folder inside the repo (default: dist)")
    parser.add_argument("--serve", nargs="?", const=8000, type=int, metavar="PORT",
                        help="after building, serve the result (default port 8000)")
    args = parser.parse_args()
    out = (ROOT / args.out).resolve()
    build(out)
    if args.serve:
        serve(out, args.serve)


if __name__ == "__main__":
    main()
