# PhotoSwipe (vendored)

Third-party lightbox used by the photo strip. Shipped from this folder because the site's
Content Security Policy only allows same-origin scripts.

- Package:  photoswipe 5.4.4 (MIT, see LICENSE)
- Source:   https://registry.npmjs.org/photoswipe/-/photoswipe-5.4.4.tgz  (upstream: https://github.com/dimsemenov/Photoswipe)
- Tarball integrity (npm registry, verified on download):
  sha512-WNFHoKrkZNnvFFhbHL93WDkW3ifwVOXSW3w1UuZZelSmgXpIGiZSNlZJq37rR8YejqME2rHs9EhH9ZvlvFH2NA==
- Files are the unmodified `dist/` builds. SHA-256 of each:
  2c223af0b21d32240087ee189eb70fd315907b6ade8b561e24265baccd6a98e7  LICENSE
  b82c385604f90cc77082d8e1bd4f5ef7c9d3da62d95dcc3ff1691a4eb0dddd12  photoswipe-lightbox.esm.min.js
  b0eaaae0b9de064d25e2f18517b9011a526d9b2142376e1c0febd096cebab9f3  photoswipe.css
  542069771beb34dc461cdb9374da8af643c591ebf65d8ec36331dd9a0681ebd4  photoswipe.esm.min.js

Reviewed at vendoring time: no network calls, eval/new Function, storage, workers, source-map
references or runtime dependencies in the shipped files.

To update: `npm pack photoswipe@<version>`, verify the tarball against `npm view photoswipe@<version>
dist.integrity`, review the files the same way, replace them here, update this file, and run the
site checks and a browser test of the lightbox.
