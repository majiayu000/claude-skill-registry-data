---
name: padosoft-email-html-builder
description: >-
  Use this skill whenever the user creates, fixes, converts or reviews an HTML email (welcome, transactional, newsletter, DEM, ESP template) or asks to test it on Mailtrap or MailUp, even when they do not explicitly say "HTML", "template" or "deliverability": it produces table-based emails with minimal inline CSS, an aligned text/plain part, one-click List-Unsubscribe, and validates them with the included linter down to 0 errors, targeting SpamAssassin spam <= 0.1 and HTML Check with no warnings outside the baseline. Do not use it for copywriting without code, for configuring DNS/SPF/DKIM or for managing lists and bulk sends.
license: MIT
compatibility: >-
  Requires Python 3.10+ for the included scripts (standard library only). Optional: a headless browser
  (Playwright/Chromium) for the verification screenshots and a Mailtrap account for HTML Check and spam reports.
metadata:
  version: 1.1.0
  author: Padosoft
  summary: HTML email that passes the deliverability checks on the first send.
  profiles: email
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: email, html email, mailtrap, mailup, deliverability, spamassassin, outlook, responsive, accessibility
---

# Email HTML Builder

Produces HTML emails that are **production ready on the first try**: table layout with HTML attributes, inline CSS reduced to typography alone, a minimal `<style>`, an aligned text/plain part, one-click unsubscribe headers. The expected result on Mailtrap is **spam ≤ 0.1** and an **HTML Check with only the allowed warnings** (§5). On MailUp Check-up: **zero problems**.

The complete normative rules with `R-xxx` IDs are in `references/rules.md`. The linter is `scripts/lint_email.py` and the reference template is `templates/reference-welcome-dark.html`. **If those files are not available, the essential rules below are enough and are binding.**

---

## 0. Included scripts

| Script | Use |
|---|---|
| `scripts/lint_email.py` | Rule validator. `python3 scripts/lint_email.py email.html --text email.txt --subject "Subject" [--production] [--transactional] [--json]`. Exit 1 if any MUST is violated, 0 when clean. |
| `scripts/build_payload.py` | Generates the Mailtrap JSON payload with `List-Unsubscribe` and One-Click. `--help` for the options. |
| `scripts/send_mailtrap_sandbox.sh` / `.ps1` | Sandbox send. Variables: `MAILTRAP_TOKEN`, `MAILTRAP_INBOX_ID`. |
| `scripts/screenshot_email.py` | Screenshots at 600px and 375px, with and without `<style>` (requires Playwright; if it is missing, skip gate G2 and say so in the report). |
| `templates/reference-welcome-dark.html` | Compliant template to start from (0 MUST violated). |
| `references/rules.md` | Complete `R-xxx` rules. Read it when a warning is not in the §5 baseline, or when you need the rationale behind a rule. |


---

## 1. Mandatory workflow

Run the phases **in order**. Do not deliver before G1–G2 are green. If you have access to Mailtrap, run G3–G6 as well.

1. **Brief.** Work out or ask (once, in a single batch) what is missing:
   - type of email, brand, language and light/dark theme;
   - a palette of 2–3 colors, content, CTA and URLs;
   - sending platform (MailUp, Mailtrap Sending, SES…) and the syntax of the dynamic fields;
   - legal details for the footer.

   If the brief is incomplete do not stall: use explicit placeholders and list them in the report.
2. **Content design.** Before writing code, settle:
   - subject: 35–50 characters;
   - preheader: 40–100 characters, complementary to the subject;
   - a single primary CTA;
   - text/image ratio ≥ 80/20;
   - which blocks to use (header, hero, card, benefits, social, footer).
3. **Code.** Start from the skeleton in §3 (or from `templates/`). Apply **every** MUST rule in §4.
4. **Text/plain.** Write the text-only version with the same content and the same links in clear text.
5. **G1 Lint.** Run `python3 scripts/lint_email.py email.html --text email.txt --subject "…"` and bring the violated MUSTs to **0**. If the script is not there, work through the §6 checklist by hand.
6. **G2 Render.** Take screenshots with Playwright/Chromium at **600px** and **375px**, then repeat them without `<style>` and with images blocked. No breakage allowed.
7. **Payload and test send.**
   - `scripts/build_payload.py` generates the JSON payload (List-Unsubscribe included);
   - the send starts with `scripts/send_mailtrap_sandbox.{ps1,sh}` or with the Mailtrap connector (`send-sandbox-email`);
   - on Windows use **PowerShell**: `$env:VAR="…"` and not the `VAR=… cmd` syntax.
8. **Without Mailtrap** (no account or connector): declare G3–G6 as *not run* in the report, do not estimate them, and in exchange work through the manual checklist in §6 on top of the linter. Deliver anyway.
9. **G3–G6 Mailtrap verification.** Use `get-sandbox-message-html-analysis`, `get-sandbox-message-spam-score` and the blacklist and text reports. Compare against the §5 baseline: every entry outside the baseline is a defect to fix and resend. **Do not declare a removable warning a "false positive".**
10. **G7 MailUp** (if that is the sending platform): Check-up with no errors on blacklisted links, tracking enabled, unsubscribe present, weight, dynamic fields with defaults, summary, analytics, custom tracking domain, spam and code.
11. **Delivery.**
    - `.html`, `.txt` and `payload.json` files;
    - a **report** with the outcome of the gates, remaining warnings with their rationale, placeholders still to be replaced and SHOULD exceptions with their rationale;
    - a version number (`v1`, `v2`…) in the test subject.

---

## 2. Key principle (the cause of the historical mistakes)

The Mailtrap checker uses caniemail.com data and **reports every CSS property present, even when there is a fallback**. `bgcolor` next to `background-color` does **not** remove the warning: the CSS property has to be **deleted**.
→ **Layout with HTML attributes. Inline CSS for typography only. `<style>` only for rounded corners and media queries.**

---

## 3. Reference skeleton

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
<meta name="color-scheme" content="dark">
<meta name="supported-color-schemes" content="dark">
<title>Title</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<style>
.r10{border-radius:10px}.r9{border-radius:9px}.r9t{border-radius:9px 9px 0 0}
@media (max-width:620px){.wrap{width:100%!important}.col{display:block!important;width:100%!important}.vgap{display:block!important;width:100%!important;height:16px!important}.gut{width:20px!important}.h1m{font-size:26px!important;line-height:32px!important}.txtm{font-size:16px!important;line-height:24px!important}.imgm{width:100%!important;height:auto!important}}
</style>
</head>
<body bgcolor="#04050a" text="#aab3c5" link="#2ff5d6" vlink="#2ff5d6" alink="#2ff5d6" marginwidth="0" marginheight="0" topmargin="0" leftmargin="0">
<!--[if !mso]><!--><div aria-hidden="true" style="display:none; mso-hide:all;">Preheader of 40-100 characters, no invisible filler.</div><!--<![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#04050a">
 <tr><td height="32" style="font-size:1px; line-height:32px;">&nbsp;</td></tr>
 <tr><td align="center" valign="top">
  <table role="presentation" width="632" class="wrap" align="center" cellpadding="0" cellspacing="0" border="0"><tr>
   <td width="16" style="font-size:1px; line-height:1px;">&nbsp;</td>
   <td align="center" valign="top">
    <table role="presentation" class="wrap" width="600" align="center" cellpadding="0" cellspacing="0" border="0">
     <!-- blocks -->
    </table>
   </td>
   <td width="16" style="font-size:1px; line-height:1px;">&nbsp;</td>
  </tr></table>
 </td></tr>
 <tr><td height="32" style="font-size:1px; line-height:32px;">&nbsp;</td></tr>
</table>
</body>
</html>
```

### Block patterns (copy them, do not reinvent them)

**Vertical and horizontal spacing** (instead of padding):
```html
<tr><td height="24" style="font-size:1px; line-height:24px;">&nbsp;</td></tr>
<td class="gut" width="24" style="font-size:1px; line-height:1px;">&nbsp;</td>
```

**Card with border and corners** (instead of border and background-color):
```html
<table role="presentation" class="r10" width="100%" cellpadding="1" cellspacing="0" border="0" bgcolor="#1c2333"><tr><td>
  <table role="presentation" class="r9" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#0d1018">
    <tr><td colspan="3" height="24" style="font-size:1px; line-height:24px;">&nbsp;</td></tr>
    <tr><td width="20" style="font-size:1px; line-height:1px;">&nbsp;</td><td><!-- content --></td><td width="20" style="font-size:1px; line-height:1px;">&nbsp;</td></tr>
    <tr><td colspan="3" height="24" style="font-size:1px; line-height:24px;">&nbsp;</td></tr>
  </table>
</td></tr></table>
```

**Accessible H1 heading** (no `<h1>`):
```html
<td align="center" class="h1m" role="heading" aria-level="1" style="font-family:Arial, Helvetica, sans-serif; font-size:30px; line-height:38px; font-weight:700; color:#f2f4f8;">Title</td>
```

**Bulletproof CTA** (VML and HTML with **identical** dimensions):
```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://…" style="height:48px; v-text-anchor:middle; width:220px;" arcsize="21%" fillcolor="#2ff5d6" stroke="f"><w:anchorlock/><center style="color:#04050a; font-family:Arial, Helvetica, sans-serif; font-size:15px; font-weight:bold;">Browse the products</center></v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" class="r10" width="220" cellpadding="0" cellspacing="0" border="0" bgcolor="#2ff5d6"><tr>
<td align="center" height="48" style="font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:48px; font-weight:700;"><a href="https://…" target="_blank" style="color:#04050a; text-decoration:none;">Browse the products</a></td>
</tr></table>
<!--<![endif]-->
```

**Image in a card** (the cell carries height and bgcolor, so it stays intact when images are blocked):
```html
<td align="center" valign="middle" height="120" class="r9t" bgcolor="#161b27" style="font-size:0; line-height:0;"><a href="https://…" target="_blank"><img src="https://cdn.example.com/img/x@2x.jpg" width="174" height="120" border="0" alt="Short description" class="imgm"></a></td>
```

**Columns that stack on mobile** (whole px, sum = container):
```html
<tr><td class="col" width="176" valign="top">…</td><td class="vgap" width="12" style="font-size:1px; line-height:1px;">&nbsp;</td><td class="col" width="176" valign="top">…</td><td class="vgap" width="12" style="font-size:1px; line-height:1px;">&nbsp;</td><td class="col" width="176" valign="top">…</td></tr>
```

**Divider:**
```html
<tr><td height="1" bgcolor="#1c2333" style="font-size:1px; line-height:1px;">&nbsp;</td></tr>
```

---

## 4. Essential MUST rules (IDs in `references/rules.md`)

**Structure and weight**
- Tables only, `role="presentation" cellpadding="0" cellspacing="0" border="0"`, a 600px container, a 16px outer gutter built with cells (R-004/005/006).
- Forbidden: `<h1>`, `<script>`, `<form>`, `<iframe>`, `<video>`, `<svg>`, `<link>`, `@import`, the `on*` handlers, empty tags and superfluous comments (R-007/008/009/011).
- HTML under 100 KB (target 40 KB). Images ≤ 50 KB, GIFs ≤ 100 KB with a complete first frame (R-050/052/604).

**CSS**
- Inline, **only** `font-family`, `font-size`, `line-height`, `font-weight`, `font-style`, `letter-spacing`, `color`, `text-decoration`, `text-align` and `mso-*` are allowed (R-100).
- **Forbidden inline:** padding, margin, background, border, border-radius, width, height, max/min-*, display, opacity, overflow, visibility, outline, box-shadow, position, float, text-transform, table-layout (R-101). The only exception is the preheader (`display:none; mso-hide:all`).
- Mandatory substitutions (R-200…210):

  | Instead of | Use |
  |---|---|
  | `background` | `bgcolor` |
  | padding | empty cells with `height`/`width` |
  | border | outer table with `bgcolor` + `cellpadding="1"` |
  | CSS width/height | `width`/`height` attributes |
  | body margins | `marginwidth`/`marginheight` |
  | default color | `text`/`link` on `<body>` |
  | gap under images | `font-size:0; line-height:0` on the cell |
  | background images | a solid color |

- A single `<style>`, with **one line** of `border-radius` and **one line** of `@media (max-width:620px){…}`, without `only screen and`. No reset, no preheader classes, no `prefers-color-scheme` or `:root` (R-300…303).
- No comment containing the string `<style`. The email must stay readable even without the style block (R-304/305).

**Antispam and deliverability**
- **Marketing vs transactional.** The unsubscribe rules (`R-405` `List-Unsubscribe` header, `R-454` footer link) apply to **commercial and bulk** email. For a purely transactional one (order confirmation, password reset, shipping) they are not required: use `--transactional` in the linter, still keep an "Email preferences" link, and state it in the report. All the other rules apply to both.
- HTML **100% ASCII**: accented characters as numeric entities (`&#232;`) (R-402).
- **Never use invisible filler** in the preheader (`&#847;`, `&zwnj;`, repeated `&nbsp;`): it costs +2.4 SpamAssassin points (R-401).
- Preheader without `color`. No text in a color equal or close to the background, separators included (R-400/403).
- Text/plain aligned with the HTML. `List-Unsubscribe` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers (R-404/405).
- Subject 35–50 characters (60 max): no ALL CAPS, no `!!!`, no trigger words or more than one emoji (R-406).
- Spam target ≤ 0.1, blacklist 0, no shorteners or bare IPs. Text/images ≥ 80/20. Sender domain with SPF+DKIM+DMARC, a monitored `Reply-To` (R-407…412).

**Links (MailUp Check-up)**
- Absolute, working HTTPS links. Tracking enabled with a **custom tracking domain** (R-450/451).
- UTM `utm_source`, `utm_medium=email`, `utm_campaign`, without spaces (R-452).
- Dynamic fields in the platform syntax (MailUp `[field]`) with a default value. In links the protocol must be explicit (`https://[field]`) (R-453).
- Unsubscribe in the footer, two clicks at most (R-454). `tel:` without spaces, asset paths without spaces (R-457/458).

**Design and accessibility**
- `color-scheme` = `dark` **or** `light`, never `light dark` without a complete dark theme (R-500).
- **Calculated** contrast ≥ 4.5:1 for every normal text, footer included (R-501).
- Fonts: headings ≥ 22px, body ≥ 16px on mobile (`.txtm` class), legal ≥ 12px, CTA ≥ 15px. A palette of 2–3 colors (R-502/503).
- `aria-hidden` on glyphs and separators. `lang` and `<title>` filled in. DOM order = visual order (R-504/505).
- `<img>` with `width`, `height`, `border="0"`, a short `alt`, HTTPS src from the brand CDN (no placeholders). The cell carries `height` and `bgcolor`. Never put essential text inside an image only (R-600…603).
- CTA VML + HTML with identical dimensions, area ≥ 46×46px, a single primary CTA (R-700…703).
- Columns in whole px (no `33.33%`), no spacing asymmetry when they stack (R-800…802).

**Footer:** reason for receiving, legal entity, address, VAT number, contacts, Unsubscribe, Preferences, Privacy, copyright and social. In production, **zero placeholders** (R-900/901).

---

## 5. Mailtrap baseline (the only allowed warnings)

| Rule | Reason |
|---|---|
| `style` | The style block is needed for responsive and corners |
| `@media`, `@media max-width` | Mobile media queries |
| `width`/`display`/`height`/`font-size`/`line-height` inside the media query | Stacked columns and mobile typography |
| `border-radius` (1 line) | On Outlook the corners stay square |
| `display` on the preheader | It is the only way to hide it |

SpamAssassin in testing: `MISSING_MID` 0.1 (the production MTA adds the Message-ID) and `HTML_MESSAGE` 0.0. **Any other entry has to be fixed.**

Mailtrap Market Support ≥ 95% (for Mailtrap ≥ 90% is acceptable, below 85% it has to be redone).

---

## 6. Manual checklist (when the linter is not there)

- [ ] No `style=""` in the body with properties outside the whitelist, preheader aside
- [ ] Every background color is `bgcolor`, every spacing is a cell, every border is a table with `cellpadding="1"`
- [ ] `<style>` = 1 radius line + 1 `@media (max-width:620px)` line
- [ ] `grep -P '[^\x00-\x7F]'` over the HTML finds nothing
- [ ] No `&#847;`/`&zwnj;` in the source
- [ ] `<body>` with `bgcolor`, `text`, `link`, `marginwidth`, `marginheight`
- [ ] Contrasts ≥ 4.5:1 calculated (script or tool), footer and separators included
- [ ] Every `<img>` has width, height, border="0", alt, HTTPS src; the cell has height and bgcolor
- [ ] CTA VML and HTML with the same width and height
- [ ] Columns in whole px with the correct sum
- [ ] Subject 35–50 characters, preheader 40–100
- [ ] Text/plain aligned, List-Unsubscribe and One-Click in the payload
- [ ] HTTPS links with UTM and unsubscribe present
- [ ] No placeholders if it is going to production

---

## 7. Delivery report format

```
Version: vN  |  HTML weight: xx KB  |  Subject: "…" (nn chars)  |  Preheader: nn chars
G1 Lint: PASS (0 MUST, n SHOULD)      G2 Render: PASS (600/375/no-style/img-off)
G3 HTML Check: xx% — warnings: [baseline only | list of extras + fix]
G4 Spam: 0.1 (MISSING_MID)            G5 Blacklist: 0      G6 HTML/Text: aligned
G7 MailUp Check-up: [outcome | not run]
SHOULD exceptions with rationale: …
Placeholders to replace: …
Next step: …
```

Always flag the uncertainties explicitly, for example the syntax of the platform's unsubscribe placeholder that still has to be verified on the account.
