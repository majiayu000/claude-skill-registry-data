---
name: ux-gift-sweep
description: Run a "free UX test" outreach sweep — find small businesses likely to pay for web work, test THEIR OWN website on real phone engines, and draft a short email with 1-3 real, developer-checkable findings (with screenshots) plus an optional paid follow-on. Use when you say "run the UX sweep", "find businesses to UX test", "test their website and email them", "free website audit campaign", or ask who replied. Uses mobile-ui-audit as the test engine and a findings table of true causes and fixes.
---

# UX gift sweep

**Goal:** a business owner opens an email about a real bug on their own site. Their developer
checks it, finds it's real, and the owner trusts you enough to ask about paid work. The gift is
the pitch, and it opens on their own record (their own website).

Composes:
- **Testing engine:** `mobile-ui-audit` (phone checks, money-path checks, `--hop` one click deep).
- **Wording of findings:** `findings.md` here — each bug with its true cause and fix.
- **Channel and sending discipline:** `distribution-channel`; replies: `business-inbox`.

## The email

Keep it short and identical except for the findings. A template:

```
Subject: I ran UX testing on your website

#1) <what a visitor sees, where>. <why, in one line>. Recommend to your developer that they <fix>.

#2) ...

Forward this to whoever runs your website to have them fix the above.

This was free, no catch. If useful, we also do more thorough testing and redesigns — just ask.

<your name>
```

Use 1-3 findings and drop unused numbers. Write the template once in your own voice and then
never vary anything but the findings.

## Rules, each with its why

1. **Every finding is real for that site and was seen on a real engine run.** The email asks them
   to forward it to a developer; a developer who can't reproduce one bug writes off the whole
   email. Keep the screenshot and raw JSON for every finding in `evidence/<slug>/`.
2. **The cause must be technically correct** — take it from `findings.md`, not a guess. (Autofill
   reads `autocomplete` attributes; "cookies keyed wrong" is the kind of plausible wrong cause any
   developer spots.) A wrong cause is worse than no cause.
3. **Big, or it doesn't go in.** Qualifies only if anyone who can use a website would see it on
   their phone and agree it's broken: can't order, book or pay; can't reach the menu or button;
   the page slides sideways or comes up blank; a dead link on the order path; a popup that won't
   close. Lead with what the visitor sees, in plain words; the technical cause goes only in the
   "recommend to your developer" line. Never include small tap targets, a pinch-zoom cap, small
   text, invisible console errors, or anything flagged only by an automated check. Autofill counts
   only on a real checkout, and never alone.
4. **Attach a screenshot per finding where a still image shows the bug**: phone-sized PNG, red box
   around the broken thing, named for the finding, under ~150KB, at most 3 per email. Look at it
   first: if a stranger wouldn't see the breakage, drop the picture (keep the finding). Skip images
   for things a still can't show (scroll lock, dead link).
5. **No real finding means no email.** Filler findings are the cheap help the email pretends not
   to be.
6. **A bug on the money path ranks first** (checkout, ordering, booking, gift cards, the scroll to
   the menu). "This cost you sales" is what turns into paid work.
7. **Pick businesses that would pay**: independent, own domain, real traffic (~50+ reviews), takes
   money or bookings on the site. Skip chains and franchises (corporate web teams).
8. **Run phone checks headless.** No visible browser windows on the operator's screen.
9. **Write drafts; a human reads and sends.** Respect sender limits: bulk providers cap requests
   (e.g. 100 per rolling 24h on some plans, and refused sends don't show in stats), and Gmail and
   Outlook block on bounce and complaint rates, not count — one complaint in 100 is 1%, triple
   Google's 0.3% line. MX-check every address, prefer the address on their own site, check
   suppression lists before each batch.
10. **Check for earlier contact** in your outreach ledgers; prefer businesses you haven't emailed,
    and flag the rest.

## Procedure

1. **Pool**: businesses with a website and a findable email; rank by rule 7.
2. **Test the top ~150** concurrently with `mobile-ui-audit --devices iphone,android --hop`.
3. **Write findings** in the shape: what the visitor runs into and where -> why -> "Recommend to
   your developer that they ...", worded from `findings.md`.
4. **Draft** each as `drafts/<slug>.txt` with `To:`, `Subject:`, `Attach:` header lines and the
   body; images in `drafts/<slug>/`; rank best-first in a README.
5. **Send** after review; log date, business, to, findings and reply kind in a ledger.
6. **Read replies after 7 days**: "fixed it, thanks", a price request, or a payment. Silence isn't
   a no, and a small batch is a probe, not a verdict.
