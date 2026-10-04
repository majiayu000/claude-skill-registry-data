---
name: email-design
description: Email look and structure for this API's transactional mail. Use when adding a notification that sends mail, editing any template under resources/views/emails/ or resources/views/vendor/mail/, or changing email colors, logo, layout, or copy.
---

# Email design

Every email is a Laravel markdown mail rendered through the `mail::` components published in `resources/views/vendor/mail/`, following the device/client color scheme (see Tokens). `config/mail.php` `markdown.paths` points there, so package mails built from `MailMessage` lines (Horizon, spatie/laravel-backup, via `resources/views/vendor/notifications/email.blade.php`) get the same look with no extra code. The upstream spec is `../matches_dashboard/DESIGN.md` (sibling repo, may be absent); this skill carries the parts of it this codebase needs, and the components already encode them. Build from the components first and write raw markup only for a block no component covers.

## Adding an email

1. **Notification** (`app/Notifications/`, `ShouldQueue`): pin the dispatch locale in the constructor with `$this->locale(app()->getLocale())`. The queue worker runs on `APP_LOCALE=en`, so without it every queued mail renders in English. In `toMail()` compute `$subject = __('emails.<name>.subject')`, then `->subject($subject)->markdown('emails.<area>.<name>', [...])`.
2. **View** (`resources/views/emails/<area>/<name>.blade.php`): wrap the body in `<x-mail::message :preheader="..." :reason="...">`, open with one `# heading` (the single H1), write copy as markdown paragraphs, compose with the components below, and close with `{{ __('emails.common.thanks') }}<br>` + `{{ config('app.name') }}` when the mail is signed.
3. **Copy**: every string goes through `__('emails.<name>.<key>')`, added to both `lang/it.json` and `lang/en.json` (flat JSON, append before the closing `}`). Reuse the `emails.common.*` keys. Each email carries its own `reason` key: why the recipient gets it.
4. **Preview**: send it to Mailpit once per locale (`notifyNow` skips the queue):
   `vendor/bin/sail artisan tinker --execute 'app()->setLocale("it"); (new App\Models\User)->forceFill(["username" => "mario.rossi", "email" => "mario.rossi@example.com"])->notifyNow(new App\Notifications\<Name>(<fake args>));'`
5. **Test**: add a row to the `notifications()` data provider in `tests/Feature/EmailNotificationsTest.php` (factory closure + one string the HTML must contain). Run `vendor/bin/sail artisan test --compact tests/Feature/EmailNotificationsTest.php`.

Done when the test is green and both locales render in Mailpit (dashboard port is `FORWARD_MAILPIT_DASHBOARD_PORT` in `.env`; open `/view/latest.html` or `/view/<id>.html`): no raw `emails.` keys, logo centered, one H1, footer reason present.

## Components

`resources/views/vendor/mail/html/` (plus a `text/` twin for every custom component, used for the plain-text part). Styles come from `html/themes/default.css`, which `CssToInlineStyles` inlines at send time; an inline `style` in a component wins over the theme.

| Component | Props | Use |
|---|---|---|
| `x-mail::message` | `preheader`, `reason` (footer line) | Document skeleton via `layout`: MSO wrappers, 600px card, logo `header`, `footer` (reason + `emails.common.automatic`) |
| `x-mail::button` | `url`, `color` (`primary`/`success`/`error`); slot = label | The one CTA: bulletproof VML button plus the plain-text fallback link beneath it |
| `x-mail::subcopy` | slot = markdown | Secondary lines, 14/22 `text-muted` (expiry notes, "ignore this email") |
| `x-mail::info-box` | `rows` (label ⇒ value), `monospace` (bool) | Structured data: uppercase dimmed label over the value on `bg-elevated` |
| `x-mail::code` | `label`; slot = code | Large centered monospace code on `bg-elevated` (verification codes) |
| `x-mail::panel` / `x-mail::table` | slot = markdown | Elevated box / markdown table, themed |

Status badge: `<span class="badge badge-error">label</span>` on its own markdown line (`badge-success` / `badge-warning` / `badge-error`).

The logo is resolved in `html/header.blade.php` via `App\Support\AppLogo::emailUrl()`: PNG/JPG only (SVG and WebP render in no mail client), an absolute URL to the public `api/public/settings/logo` route with a `?v=<mtime>` buster for email-proxy image caches, centered, 140px wide, `border-radius:16px`. With no email-safe logo the header falls back to the app name in `primary`. That route skips the group `throttle:10,1`, because email image proxies share a few IPs across many recipients.

## Tokens

Both palettes are `../matches_dashboard/DESIGN.md` §2 verbatim; mail clients have no reliable CSS variables, so the hex values are fixed. **Light is the default**, the inverse of DESIGN.md's dark-first §1 (a deliberate choice for this API): the light palette lives in `html/themes/default.css` and is inlined, so every client without `prefers-color-scheme` (Gmail web, Outlook Windows) shows light; the `@media (prefers-color-scheme: dark)` block in `html/layout.blade.php` switches to dark in Apple Mail, iOS Mail, Outlook macOS/iOS and Thunderbird, with `!important` only because it has to beat the inlined styles. Gmail apps and Outlook.com run their own dark conversion on the light base.

| Token | Light (inline) | Dark (media query) | Use |
|---|---|---|---|
| `bg-canvas` | `#f5f5f5` | `#0f0f0f` | Outer body / wrapper table |
| `bg-card` | `#ffffff` | `#171717` | 600px card |
| `bg-elevated` | `#fafafa` | `#262626` | Info boxes, code block |
| `border` | `#e5e5e5` | `#2e2e2e` | Separators, box borders |
| `text` | `#0a0a0a` | `#f5f5f5` | Primary text, H1 |
| `text-toned` | `#1a1a1a` | `#dddddd` | H2 |
| `text-muted` | `#333333` | `#bbbbbb` | Secondary body |
| `text-dimmed` | `#555555` | `#999999` | Labels, footer, fallback link text |
| `primary` | `#0369a1` | `#38bdf8` | Links, wordmark |
| `primary-strong` | `#0369a1` | `#0ea5e9` | CTA background (also the VML `fillcolor`) |
| `on-primary` | `#ffffff` | `#0b1a24` | CTA label |
| `success` / `success-bg` | `#15803d` / `#dcfce7` | `#4ade80` / `#16301f` | Positive status; badge text / background, success CTA |
| `warning` / `warning-bg` | `#b45309` / `#fef3c7` | `#fbbf24` / `#33290f` | Warning status |
| `error` / `error-bg` | `#b91c1c` / `#fee2e2` | `#f87171` / `#361b1b` | Error status, error CTA |

A color change is a two-place edit: the light value in `themes/default.css` plus any matching `bgcolor` attribute (layout, panel, info-box, code, button `$fill`), the dark value in the layout's media query. A new token goes in both columns. Outlook Windows reads neither `<style>` nor the media query, so it always renders the light inline values, VML button included.

Type scale, font stack `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`: H1 24/32 700, H2 18/26 600, body 16/24, secondary 14/22, label 13/20 uppercase `letter-spacing:0.04em`, footer 12/18. Monospace (codes, class names, paths): `'SFMono-Regular', Menlo, Consolas, 'Courier New', monospace`.

## Component markup rules

When adding or editing a `mail::` component:

- The body slot goes through CommonMark: component HTML must start at column 0 and contain no blank lines (an indented line becomes a code block, a blank line ends the HTML block). Leave indentation only in the `text/` twins.
- New classes get their light styles in `themes/default.css` and, when they carry color, a dark rule in the layout's media query (selectors specific enough to beat `.content-cell p`); colored `<td>`s still carry a `bgcolor` attribute, because the inliner writes only `style`.
- Layout is `<table role="presentation" cellpadding="0" cellspacing="0" border="0">`; padding sits on `<td>`; every `h1`/`h2`/`p` carries an explicit `margin` (`0 0 16px 0`).
- Every text element ends up with inline `font-family`, `font-size`, `line-height`, `color` (from the theme or the component); every colored `<td>` carries both `bgcolor` and `background-color`. Anything only in the layout's `<style>` (responsive rules, dark mode) is progressive: Gmail strips it.
- Spacing on the 8-grid: 8 / 16 / 24 / 32 / 48.
- Colors come from the token table. `#000000` never appears; `#ffffff` only as the light `bg-card` and `on-primary`.
- Status is always color plus a text label.
- Images: absolute URL, PNG/JPG, `width` attribute, `height:auto`, `display:block`, meaningful `alt`; the message must still read with images blocked.
- One CTA per email, via `x-mail::button`.
- Keep the rendered HTML under 100 KB (Gmail truncates beyond it); current emails are ~7 KB.
- Outlook desktop ignores `border-radius`; the design must hold with square corners.

## Package mails

Horizon `LongWaitDetected` and the six spatie/laravel-backup notifications build their mail from `MailMessage` lines, rendered by the published `vendor/notifications/email.blade.php` (upstream copy minus its subcopy, since `x-mail::button` already prints the fallback link). They inherit layout, logo and theme; their copy stays the packages' own English strings.
