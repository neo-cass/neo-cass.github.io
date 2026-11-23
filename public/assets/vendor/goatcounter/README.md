# GoatCounter count.js (vendored)

Page-view counter for https://neocass.goatcounter.com. Shipped from this folder because the
site's Content Security Policy only allows same-origin scripts; the only third-party permission
it needs is `connect-src https://neocass.goatcounter.com` for the count beacon.

- File:     count.v4.js, unmodified (ISC licence, stated in the file header)
- Source:   https://gc.zgo.at/count.v4.js  (upstream: https://github.com/arp242/goatcounter)
- Integrity published by GoatCounter (https://www.goatcounter.com/help/countjs-versions),
  verified on download:
  sha384-nRw6qfbWyJha9LhsOtSb2YJDyZdKvvCFh0fJYlkquSFjUxp9FVNugbfy8q1jdxI+
- SHA-256:
  b9f5c4c04edb8802d7b73f479a2f532f52367b633b56a09a224fc659fde86c03  count.v4.js

Reviewed at vendoring time: no cookies, eval/new Function, extra script loads or runtime
dependencies. Its only network call is one `navigator.sendBeacon` to the endpoint in the
`data-goatcounter` attribute. It uses `localStorage` only for the `#toggle-goatcounter`
opt-out, and does not count localhost, file:// or framed pages.

To update: download the newer `count.vN.js` from https://gc.zgo.at, verify its sha384 against
the versions page above, review it the same way, replace it here, update the script path in
`src/partials/analytics.html` and this file, and run the site checks.
