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

The résumé at `/cv/cv.pdf` is built and published by the separate
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
preview (`cv-preview.webp`) is a **snapshot of the CV's first page**: re-run with `--cv-pdf`
whenever the CV changes. To add a photo: add it to `GALLERY`, run the script, add a `<figure>`
(with `data-pswp-width`/`-height` on its link) to `index.html` and an aspect rule
`.photo--<name>` in `style.css`, then run the checks.

## Photo lightbox

Clicking a gallery thumbnail opens [PhotoSwipe](https://photoswipe.com) (MIT): arrows,
keyboard, swipe and zoom, with no captions (alt text stays in the page for screen readers). It is vendored in
`public/assets/vendor/photoswipe/` (the CSP only allows same-origin scripts) with its version,
source and checksums recorded in that folder's README. Without JavaScript the thumbnails are
plain links to the full image.

## Contact form

Uses [Web3Forms](https://web3forms.com). The form, the hero "Contact" pill and the footer
link are **hidden on the live site until a valid access key is set**:

1. Get a key at web3forms.com for the address that should receive messages.
2. Replace `YOUR_WEB3FORMS_ACCESS_KEY` in `src/pages/index.html` with it (a UUID; anything
   else counts as "not set"). The key is public by design and can only send mail to that
   address; the address itself is never in the repo.

On `localhost` the form is shown with a "preview only" notice so layout can be checked first.

## Design

Follows the "Apple design analysis" `DESIGN.md` from
[awesome-design-md](https://github.com/VoltAgent/awesome-design-md): Action Blue as the only
accent, 17px body, tight display type, 44px touch targets, spec breakpoints. Light and dark
themes follow the visitor's system setting; dark uses the spec's dark surfaces. The header of
`public/assets/css/style.css` lists the few deliberate deviations (no dark tiles or black nav
in the light theme; slightly darker small-text greys and form borders for accessibility
contrast).

## Analytics (optional)

A disabled GoatCounter snippet (no cookies, no personal data) is in
`src/partials/analytics.html`. To enable it, follow the comments there and in `head.html`,
including the matching change to the Content Security Policy.

## Notes

- Do not add contact details (email, phone, home town) to this repo or to the public CV:
  they are what the checks above guard against.
