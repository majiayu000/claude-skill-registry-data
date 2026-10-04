---
name: snaap-whatsapp
description: >
  Use for any WhatsApp CTA, deep link or order handoff. WhatsApp is the only checkout. Enforces the
  single number and the message-from-validated-state rule.
---
# WhatsApp CTAs

**254117000900 is the only number.** Two older numbers are retired (their exact values are kept out of the repo on purpose) — if
either reappears in the repo, treat it as a build-failing error. Always build links with `waLink()`
from `@/constants/business`, never a hardcoded `wa.me/...`.

**WhatsApp is the checkout.** There is no cart gateway, no Daraja, no card processor — don't build
one. Treat WhatsApp CTAs as first-class conversion surfaces.

**Message contents are built from server-validated state** — product name, SKU, price, delivery
charge — so totals can't be tampered with client-side. For a Lipa Mdogo Mdogo–eligible product,
prefill a message naming the device and asking about Lipa Mdogo Mdogo specifically. Never put an
invented figure in the message.

**Mechanics:** `https://wa.me/254117000900?text=<url-encoded message>`. Handle "WhatsApp not
installed" gracefully. Fire the agreed GA4 conversion event on click.
