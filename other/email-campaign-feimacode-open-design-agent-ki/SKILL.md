---
name: email-campaign
zh_name: "邮件营销"
en_name: "Email Campaign"
emoji: "✉️"
description: "An HTML email that survives real inboxes — Gmail, Outlook desktop and web, Apple Mail, phones: table layout, inline-ready styles, a bulletproof button, dark-mode aware, one clear call to action."
zh_description: "可在 Gmail、Outlook、Apple Mail 和手机上正常显示的 HTML 邮件: 表格布局、行内样式、防失效按钮、适配深色模式、一个明确的行动号召"
en_description: "An HTML email that survives real inboxes — Gmail, Outlook desktop and web, Apple Mail, phones: table layout, inline-ready styles, a bulletproof button, dark-mode aware, one clear call to action."
category: email
scenario: marketing
tags: ["email", "newsletter", "html email", "edm", "launch email", "邮件", "邮件营销"]
triggers:
  - "email"
  - "html email"
  - "newsletter"
  - "email campaign"
  - "launch email"
  - "product update email"
  - "edm"
  - "邮件"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - color
      - accessibility-baseline
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, components]
  example_prompt: "A launch email for our new reporting dashboard: one headline, three short benefits, one button to try it, and a footer with unsubscribe and view-in-browser links."
---

# Email Campaign

**Intent.** One email with one job, built so it looks the same in Gmail, Outlook (desktop and web), Apple Mail and on phones. Email clients are not browsers: no flexbox or grid, no positioning, no transforms, no SVG, no external CSS, no scripts. The export inlines your styles; your job is to only use what survives.

## Content first

- **Subject line and preheader:** write both. The preheader is the first sentence of the email (35–90 characters) and must add to the subject, not repeat it. Put it in a hidden `<div data-od-preheader>` as the first thing inside the column, or make it the first paragraph.
- **One message, one call to action.** Headline (≤ 8 words), 1–3 short paragraphs or 2–4 benefit rows, one primary button. A secondary text link at most.
- Real content from the brief. No lorem ipsum, no "Click here".

## Structure (required)

```html
<body style="margin:0;padding:0;background-color:#f4f2ee">
  <table data-od-email role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
         style="width:100%;max-width:600px;margin:0 auto;background-color:#ffffff">
    <tr><td style="padding:32px 32px 8px"> <!-- logo / wordmark as text --> </td></tr>
    <tr><td style="padding:8px 32px"> <!-- headline, body --> </td></tr>
    <tr><td style="padding:16px 32px 32px"> <!-- button --> </td></tr>
    <tr><td style="padding:24px 32px;background-color:#f4f2ee"> <!-- footer --> </td></tr>
  </table>
</body>
```

- The single column is the `<table data-od-email>`, `width="100%"` with `max-width:600px`, so it fills phones and stops at 600px elsewhere. Every layout is rows of that table; side-by-side items are a nested `role="presentation"` table with `<td>` cells (two columns at most), never flexbox or grid.
- Every `<table>` used for layout has `role="presentation" cellpadding="0" cellspacing="0" border="0"`.
- Spacing with `padding` on `<td>`, not `margin` (Outlook ignores margins on many elements).

## Type and color

- Font stack: the design system's font first, then web-safe fallbacks (`Helvetica, Arial, sans-serif` or `Georgia, 'Times New Roman', serif`). Web fonts load in Apple Mail only; everything else uses the fallback, so pick a fallback that keeps the feel.
- Sizes: body 16px (never under 14px), line-height 1.5; headline 28–36px.
- Colors from the design system as hex values. **Every background gradient needs a solid `background-color` fallback** on the same element. Text contrast at least 4.5:1.
- Dark mode: add `<meta name="color-scheme" content="light dark">` (export adds it) and avoid pure white logos on transparent backgrounds; keep text on solid backgrounds.

## The button (bulletproof)

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
  <td align="center" bgcolor="#1f4cff" style="border-radius:8px;background-color:#1f4cff">
    <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="https://example.com/try" style="height:48px;v-text-anchor:middle;width:220px" arcsize="17%" stroke="f" fillcolor="#1f4cff"><center style="color:#ffffff;font-family:Arial,sans-serif;font-size:16px;font-weight:bold">Try the dashboard</center></v:roundrect><![endif]-->
    <!--[if !mso]><!--><a href="https://example.com/try" style="display:inline-block;padding:14px 28px;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:700;color:#ffffff;text-decoration:none;border-radius:8px">Try the dashboard</a><!--<![endif]-->
  </td>
</tr></table>
```

## Images

- PNG or JPEG only (no SVG, no `data:` URIs). Every image has `alt` (or `alt=""` if decorative) and explicit `width`; set `style="display:block;max-width:100%;height:auto"`.
- Images live under the artifact's `assets/`. Recipients can only load hosted images: tell the user to upload `assets/` and export with `baseUrl` set to that address, which rewrites every image URL.
- The email must still make sense with images off: never put the headline or the button text inside an image.

## Footer (required)

Sender name and postal address line, an unsubscribe link and a view-in-browser link (use the placeholders `{{unsubscribe_url}}` and `{{view_in_browser_url}}` if the user didn't give real ones, and say so).

## Check and export

1. Register the artifact (kind `html`), then call `check_open_design_artifact`. Fix every `email-*` error (layout, SVG, unsupported CSS); local images show as notes until export.
2. Export with `export_open_design_artifact` and `format: "email"` (plus `baseUrl` once images are hosted). It writes `exports/<name>.email.html` and a plain-text version, `.email.txt`. Fix any remaining errors and export again.
3. Tell the user how to send a test: open the `.email.html` in a browser, select all, copy, and paste into their email tool's HTML or rich-text editor (or import the file), then send a test to Gmail and Outlook before sending to the list.
