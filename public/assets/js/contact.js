/*
  Contact form behaviour (Web3Forms). Plain ES5-style JS, no dependencies.

  - Live site, no valid access key set -> the form, nav pill and footer link stay hidden.
  - Valid access key set               -> they appear and the form submits over fetch().
  - localhost preview, no valid key    -> they appear with a notice, and sending is disabled,
                                          so the layout can be previewed before going live.

  The access key is public by design (it can only send mail to the address it was issued
  for); the receiving address never appears in this repo. See the comment in index.html.
*/
(function () {
  'use strict';

  var form = document.getElementById('contact-form');
  if (!form) { return; }

  // Web3Forms access keys are UUIDs; anything else (placeholder, typo) counts as "not set".
  var key = form.elements.access_key.value.trim();
  var configured = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(key);
  var isLocalPreview = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);

  if (!configured && !isLocalPreview) { return; }   // live site: stay hidden until configured

  document.querySelectorAll('[data-contact]').forEach(function (el) { el.hidden = false; });

  var status = document.getElementById('contact-status');
  var button = form.querySelector('button[type="submit"]');

  if (!configured) {
    button.disabled = true;
    status.textContent = 'Preview only: set a valid Web3Forms access key in index.html to enable sending.';
    console.info('[contact] Form shown for local preview. Set a valid Web3Forms access key (a UUID) in index.html to enable it.');
    return;
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    button.disabled = true;
    status.textContent = 'Sending…';

    fetch(form.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(form)))
    })
      .then(function (response) {
        return response.json().then(function (data) { return { ok: response.ok, data: data }; });
      })
      .then(function (result) {
        if (!(result.ok && result.data && result.data.success)) { throw new Error('rejected'); }
        form.reset();
        status.textContent = 'Thanks — your message has been sent.';
      })
      .catch(function () {
        // Deliberately generic: never reveal the destination address or service details.
        status.textContent = 'Sorry, that did not go through. Please try again later.';
      })
      .then(function () { button.disabled = false; });
  });
}());
