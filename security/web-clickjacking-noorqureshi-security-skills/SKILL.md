---
name: web-clickjacking
description: >
  Clickjacking / UI redress — frame a target so a victim's clicks hit hidden actions. Load when a
  page allows framing (no X-Frame-Options / frame-ancestors), on state-changing one-click actions,
  or "clickjacking". Signals: missing framebusting headers, sensitive buttons, OAuth consent, account settings.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: low
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-1021]
tools: [burp]
schema_version: 1
---

# Clickjacking (UI redress)

## When it applies
A sensitive, state-changing page can be embedded in an `<iframe>` on an attacker site, and the
action needs only clicks (no CSRF token / re-auth). The attacker overlays their own UI so the
victim clicks the framed action unknowingly.

## Why it works
Without `X-Frame-Options: DENY/SAMEORIGIN` or CSP `frame-ancestors`, the browser lets any site
frame the page. Making the frame transparent and positioning it under a decoy button turns the
victim's clicks into actions on the target in their authenticated session.

## Method
1. **Check framability**: load the target in `<iframe src="https://target/…">`; if it renders (no
   framebusting), it's frameable. Inspect for missing `X-Frame-Options` / `frame-ancestors`.
2. **Find a worthwhile action**: one-click state change — delete account, change email, authorize
   OAuth, transfer, enable a setting.
3. **Build the PoC**: transparent iframe (`opacity:0`) over a decoy ("Click to win"), aligned so
   the victim's click lands on the target's button. Multi-step → chain frames/drag (classic UI redress).
4. **Assess impact** honestly — clickjacking on a trivial action is low; on ATO/authorization it matters.

## Gotchas
- `SameSite=Lax/Strict` cookies can break framed authenticated actions — verify the action still fires framed.
- Modern browsers + CSP `frame-ancestors` usually block it; the finding is the *missing* protection + a real action.
- Don't over-claim: needs victim interaction and a meaningful action to be more than informational.

## Verify success
A working PoC page where a normal-looking click performs the sensitive action on the target in the
victim's session (screen-record the overlay).

## References
PortSwigger clickjacking labs; OWASP clickjacking defense cheat sheet.
