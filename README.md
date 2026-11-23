# neocass.com

Personal site for Neo Cass, published with GitHub Pages at <https://neocass.com>.
Plain HTML, CSS and a little JavaScript. A tiny build step fills shared partials (head,
navigation, footer) into each page; there is no framework, no cookies, and no third-party
requests except the optional contact form.

```
src/
  pages/              index.html, 404.html (front matter + page-specific markup)
  partials/           head, nav, footer, social tags, structured data, analytics
public/               copied to the site unchanged
  assets/
    css/style.css     all styles, driven by design tokens (see its header)
    js/contact.js     contact-form behaviour
    js/gallery.js     photo lightbox setup
    vendor/photoswipe/  vendored lightbox library (see its README)
    images/           profile, social card, CV preview; gallery/ and gallery/thumbs/
    icons/, presentations/
  favicon.ico, apple-touch-icon.png, robots.txt, sitemap.xml, CNAME
scripts/
  build.py            renders src/ + copies public/ into dist/
  check_site.py       static checks on dist/ (also run in CI)
  build_images.py     regenerates every derived image from the originals
.github/workflows/site.yml   build, check, deploy
dist/                 build output (git-ignored)
```

The CV at `/cv/cv.pdf` is built and published by the separate
[`cv`](https://github.com/neo-cass/cv) repository (a GitHub Pages project site on the same domain).

## Develop

```bash
python3 scripts/build.py --serve      # build, then http://localhost:8000
python3 scripts/build.py && python3 scripts/check_site.py
```

The build also appends a content fingerprint (`?v=<hash>`) to every stylesheet and script URL,
so a browser holding an old cached CSS can never be paired with newer HTML.

Templates are deliberately tiny: `{{ name }}` fills a value from the page's front matter and
`{% include "file.html" %}` inserts a partial. An unknown name or missing partial fails the
build. Shared markup (head, nav, footer) lives once in `src/partials/`; `base` is `""` on
the home page and `/` elsewhere so nav links work from any URL.

## Deploy

Pushing to `main` runs `.github/workflows/site.yml`: build, **check**, then deploy `dist/` to
GitHub Pages. The deploy job depends on the build job, so a failing check blocks publishing.
Pull requests build and check but do not deploy. Settings -> Pages -> Source must be
"GitHub Actions".

## Checks

`scripts/check_site.py` verifies the built output: no leftover template tokens, unique ids,
working anchors, every local link/image exists, alt text and dimensions on all images, the
strict Content Security Policy (no inline scripts, styles or handlers), `rel=noopener` on
new-tab links, valid JSON-LD, robots/sitemap, size budgets, and **that no email address or
phone number appears in any published file**.

## Images

Camera originals (HEIC/JPEG with EXIF, GPS, colour profiles) are **never committed**; keep
them outside the repo or in the git-ignored `originals/` folder. Everything published is
generated, metadata-free, by:

```bash
uv run --with pillow --with pillow-heif --with pymupdf \
    python scripts/build_images.py --originals /path/to/originals --cv-pdf /path/to/cv.pdf
```

Crop boxes live at the top of that script, and it fails if any metadata survives. The CV
preview (`cv-preview.webp`) is a **snapshot of the CV's first page**; the current design does
not show it, but re-run with `--cv-pdf` whenever the CV changes if you bring it back. To add a
photo: add it to `GALLERY`, run the script, add a link (with `data-pswp-width`/`-height`)
wrapping its thumbnail inside `.photo-strip` in `index.html`, then run the checks. Thumbnails
are cropped to 3:4 by CSS, so no per-photo rule is needed.

## Photo lightbox

Clicking a gallery thumbnail opens [PhotoSwipe](https://photoswipe.com) (MIT): arrows,
keyboard, swipe and zoom, with no captions (alt text stays in the page for screen readers). It is vendored in
`public/assets/vendor/photoswipe/` (the CSP only allows same-origin scripts) with its version,
source and checksums recorded in that folder's README. Without JavaScript the thumbnails are
plain links to the full image.

## Contact form

Uses [Web3Forms](https://web3forms.com) and is **live**: the access key is set in
`src/pages/index.html` (the hidden `access_key` field). The key is public by design and can
only send mail to the address it was issued for; that address is never in the repo.

To change the receiving address, get a new key at web3forms.com and replace the old one. If
the field ever holds something that is not a valid key (a UUID), the form and the `[Contact]`
link hide themselves on the live site; on `localhost` they show with a "preview only" notice.

## Design

Plain, text-first and monospace, written up in [`DESIGN.md`](DESIGN.md): one narrow column,
one self-hosted monospace font (Inconsolata), greyscale text with full-colour photos, no rounded corners,
shadows or gradients. Entries are rows with the year on the left; profile links sit in
`[brackets]`. Light and dark themes follow the visitor's system setting. The header of
`public/assets/css/style.css` has the short version.

## Analytics

GoatCounter (no cookies, no personal data, no consent banner), dashboard at
https://neocass.goatcounter.com. The snippet is `src/partials/analytics.html`, included on the
home page and the 404 page (so broken incoming links show up as 404 paths). The script itself
is vendored in `public/assets/vendor/goatcounter/` so the CSP keeps `script-src 'self'`; only
the count endpoint is allowed in `connect-src`. Visits from localhost are never counted. To
exclude your own visits, open https://neocass.com/#toggle-goatcounter once in each browser.

## Notes

- Do not add contact details (email, phone, home town) to this repo or to the public CV:
  they are what the checks above guard against.
