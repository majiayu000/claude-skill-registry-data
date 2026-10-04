---
name: snaap-brand
description: >
  Use when writing or reviewing any customer-facing copy or UI for Snaap Connections — product
  text, page copy, CTAs, emails, error and empty states. Enforces tone, KES formatting and the
  forbidden-claims list.
---
# Snaap brand & copy rules

**Who we are:** an online smartphone and accessories retailer with a physical shop on Digo Rd,
Opp Baroda Mall, Mombasa. We sell nationwide within five counties. WhatsApp is the only checkout.

**Tone:** clear, honest, practical. Kenyan English. No hype, no pressure.

**Money:** always format via `formatKES` from `src/constants/business` → `KSh 12,999`. No decimals,
ever. Never `Intl.NumberFormat` with `style:"currency"` — it produces `Ksh 25,500.00`. The product
page has shipped this bug; watch for it.

**Language:** English primary, Swahili secondary. Never machine-translate customer copy without
flagging it for human review.

**Forbidden — never ship any of these (this codebase has shipped all of them):**
- Fake or fallback ratings and review counts (e.g. `rating || 4.5`, a literal `"4.5 (24 reviews)"`).
  Show ratings only from real approved reviews; otherwise show nothing.
- Fake urgency or countdowns not tied to a real end time; fake or invented stock numbers.
- A "free delivery over KES X" threshold — none exists at any order value.
- Any global Lipa Mdogo Mdogo deposit or instalment figure — terms vary per phone and live in each
  product's own description.
- Any WhatsApp number other than `254117000900`.
- Invented Kenyan market facts, Safaricom terms, prices or delivery times. Ask, or mark UNVERIFIED.

**Unapproved copy** is wrapped in `PLACEHOLDER COPY — NOT APPROVED — DO NOT PUBLISH`, kept
`noindex`, and listed in the repo-root `CONTENT-VERIFY.md`.
