---
name: hubspot-email
version: 1.1.0
description: "Build HTML email templates for HubSpot. Use when the user wants to create, edit, or troubleshoot HubSpot email templates. Also use when the user mentions 'HubSpot email,' 'email template,' 'HubL email,' or 'email HTML.' For email sequences and drip campaigns, see email-sequence. For CTA buttons, see hubspot-cta."
---

# HubSpot Email Templates

You are an expert email developer creating HTML email templates for upload to HubSpot. Every template must follow HubSpot's technical constraints, email client compatibility rules, and the brand system.

**Scope boundary — pull two `web-design` reference files for email.** Email HTML has different constraints than web (table-based layout, 600px max, no JS, limited CSS, no hover on many clients), so don't load all of `web-design`. But two of its reference files apply directly and should be loaded alongside this skill for any email build or review:

- `.claude/skills/web-design/references/accessibility.md` — semantic HTML, alt text, contrast (brand palette), reading order, reduced-motion. Email a11y matters and this covers the gaps brand-guide doesn't.
- `.claude/skills/web-design/references/anti-patterns.md` — brand-specific bans (banned shapes, gradient usage rules, copy patterns, email CTA color rules). All apply to email.

Skip `web-design`'s motion/responsive/composition/state files — those assume a live web environment. Switch fully to `web-design` only when the CTA destination or thank-you page needs craft review.

## Before Building

**Always read these first:**
1. `/brain/brand-guide/brand-guide.md` — colors, typography, spacing, brand system
2. This skill file — HubSpot constraints and email HTML rules

**If the email includes product claims or copy:**
Read `/brain/truth.md` and `/brain/positioning-and-messaging.md` to ensure accuracy. Never invent product facts.

Gather this context (ask if not provided):

### 1. Email Type
- What kind of email? (webinar promotion, product announcement, newsletter, event invite, nurture, other)
- Is this a one-off or a reusable template with editable placeholders?

### 2. Content
- What is the primary message?
- Any supporting content (bullets, speaker bios, dates, CTAs)?
- How many CTAs? What action(s)?

### 3. Upload Method
- **AI Upload** (paste HTML, HubSpot recreates in drag-and-drop) — more limitations
- **Coded Template** (Design Manager, full HubL support) — more control
- Default to AI Upload constraints (strictest) unless told otherwise

---

## HubSpot AI Upload Limitations

When creating templates for HubSpot's "Upload external email template" feature, these elements **will not transfer**:

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| **Max width 600px** | Container must be 600px or narrower | Always use 600px container |
| **No background gradients** | CSS `linear-gradient` on backgrounds is stripped | Use solid background colors. Apply gradients only as accent images or via the gradient bar as an `<img>` if needed |
| **No rounded corners on modules** | `border-radius` on outer module wrappers won't transfer via AI Upload | Remove radius from large containers (cards, banner wrappers). Small inline elements like **buttons and tags can keep `border-radius`** — these work fine. For full radius support, use a **coded template** via Content > Design Manager (HTML + HubL, type Email) instead of AI Upload |
| **No overlapping elements** | Text over images, absolute positioning stripped | Use stacked layout — image block, then text block. No layered compositions |
| **No custom fonts** | Custom `@import` or `@font-face` ignored | Use system-safe font stacks. The brand font won't render — fall back to `Arial, Helvetica, sans-serif` |
| **No custom modules** | HubSpot-specific modules won't transfer | Use standard HTML tables and content blocks |
| **Images must be publicly hosted** | Local or private image URLs won't load | Use publicly accessible URLs (e.g., from your website, CDN, or HubSpot File Manager) |
| **No JavaScript** | All `<script>` tags stripped | Never include JS — it's stripped by all email clients anyway |
| **No CSS positioning** | `position: absolute/fixed/relative` not supported | Use table-based layout exclusively |
| **No CSS floats** | `float` property unreliable in email | Use table cells for side-by-side layouts |
| **No external stylesheets** | `<link rel="stylesheet">` won't load | All CSS must be inline or in `<style>` in `<head>` |
| **`filter` CSS property** | Not supported in most email clients | Don't use `filter: invert()` etc. — use pre-made white icon assets instead |
| **Social module icons** | Platform-specific social icons for some niche networks not supported | Use simple image icons with links |

### What DOES Transfer Well
- Table-based layouts
- Inline styles
- Solid background colors
- Standard images (publicly hosted)
- Text formatting (bold, italic, size, color)
- Links and buttons (with inline styles)
- Basic `<style>` block in `<head>` (HubSpot inlines it)
- Media queries in a **separate** `<style>` block (for responsive)

---

## HubSpot Coded Template Requirements

When building templates for upload via Design Manager (coded templates), follow these requirements.

### Template Annotations (Design Manager)

Every coded email template file must start with template annotations as an HTML comment before the DOCTYPE:

```html
<!--
  templateType: email
  isAvailableForNewContent: true
  label: [Company] Email - [Template Name]
-->
<!DOCTYPE html>
```

- `templateType: email` — tells Design Manager this is an email template
- `isAvailableForNewContent: true` — makes it selectable when creating new emails
- `label` — display name in the template picker

### HubL Editable Fields

Use these HubL tags to create editable fields that appear in the email editor sidebar:

```jinja
{# Editable text — use for short fields (titles, names, dates, URLs) #}
{% text "field_id" label="Field Label", value="Default value", no_wrapper=True %}

{# Editable rich text — use for paragraphs, formatted content #}
{% rich_text "field_id" label="Field Label", html="<p>Default content</p>", no_wrapper=True %}

{# Boolean toggle — use to show/hide sections #}
{% boolean "field_id" label="Show Section", value=True, export_to_template_context=True %}

{# Module — use for HubSpot-managed email modules #}
{% module "module_id" path="@hubspot/email_cta" %}
```

**Important:** Always use `no_wrapper=True` when placing `{% text %}` or `{% rich_text %}` inside styled containers. Without it, HubSpot adds wrapper `<div>` or `<span>` elements that break inline styling.

**Important:** For `{% boolean %}` tags, use `export_to_template_context=True` instead of `no_wrapper=True`. Without it, the boolean renders "true" or "false" as visible text in the email body. `export_to_template_context=True` stores the value silently and makes it available via `widget_data.field_id.value`.

**Conditional sections with boolean:**
```jinja
{% boolean "show_section" label="Show Section", value=True, export_to_template_context=True %}
{% if widget_data.show_section.value %}
  <!-- HTML for the conditional section -->
{% endif %}
```

### Email Template Validator — Rejected Patterns

HubSpot's email template validator rejects several patterns. Common ones:

- `{% dnd_area %}` with any name other than `"main"`
- a `class` attribute on `{% dnd_area %}`
- `{% text %}` tags used as editable fields inside email module markup
- module field names `body` (use `body_text`) and `name` (use something descriptive like `event_name`)

When HubSpot blocks a tag type for editable fields, wrap those fields in a micro custom module and include it via `{% module "label" path="./modules/foo" %}`.

### Personalization Token — Greeting Pattern

When using a personalization token for greetings (e.g., "Hi {{first_name}},"), always set the **fallback value to "there"** in HubSpot's token picker UI. This produces:

- **With name:** "Hi Rita,"
- **Without name:** "Hi there,"

**Do NOT leave the fallback blank or use a space.** HubSpot's UI requires a fallback value — an empty field or a space creates awkward rendering ("Hi ," or "Hi  ,"). The word "there" is the established pattern for all [Company] emails.

When inserting via the HubSpot rich text editor: type "Hi ", click Insert > Personalization, select Contact > First Name, set fallback to "there", then type "," after the token.

For the coded template equivalent:
```jinja
Hi {% personalization_token "contact.firstname", "there" %},
```

### Default Email Modules Reference

Email modules are **different from web page modules**. Use `@hubspot/email_cta` not `@hubspot/cta`, `@hubspot/email_text` not `@hubspot/text`, etc.

| Module | Path | Use For |
|--------|------|---------|
| Call-to-Action | `@hubspot/email_cta` | HubSpot-managed CTA (renders its own markup) |
| Main Email Body | `@hubspot/email_body` | Primary email content (rich text) |
| Logo | `@hubspot/email_logo` | Company logo (pulls from account settings) |
| Image | `@hubspot/image_email` | Standalone image |
| Linked Image | `@hubspot/email_linked_image` | Image with link |
| Header | `@hubspot/email_header` | Heading (h1-h6) |
| Text | `@hubspot/email_text` | Single line of text |
| Section Header | `@hubspot/email_section_header` | Header + subheader |
| CAN-SPAM Footer | `@hubspot/email_can_spam` | Auto-populated business address + unsubscribe |
| Social Sharing | `@hubspot/email_social_sharing` | Social share buttons |
| Raw HTML | `@hubspot/raw_html_email` | Custom HTML block |
| Video | `@hubspot/video_email` | Video embed with thumbnail |
| Blog Post Filter | `@hubspot/email_post_filter` | Blog post filter by tag/author/month |
| Blog Post Listing | `@hubspot/email_post_listing` | Recent/popular blog posts |
| Subscriptions | `@hubspot/email_subscriptions` | Subscription preferences page |
| Subscription Confirmation | `@hubspot/email_subscriptions_confirmation` | Subscription change confirmation |
| Unsubscribe (Backup) | `@hubspot/email_simple_subscription` | Simple unsubscribe form |

**IMPORTANT: `@hubspot/rich_text_email` does NOT exist.** There is no email-specific rich text module. For rich text / HTML content in email templates, use `@hubspot/email_body` (accepts `html` parameter for default content). The web module `@hubspot/rich_text` is NOT in HubSpot's "replace for email" list, so it *may* also work, but `@hubspot/email_body` is the confirmed email-native option.

### CTA Buttons in Email Templates

**IMPORTANT: `{% cta %}` does NOT work in HubSpot marketing emails.** The `{% cta %}` HubL tag is for **web/landing pages only**. Using it in an email template causes a "There was a problem loading this content" error in the email editor sidebar. This was confirmed by HubSpot support.

#### Recommended Approach: `@hubspot/email_cta` Module

Use the native CTA module. It renders correctly in the email editor, gives the marketer a proper CTA picker, and tracks clicks in the CTA dashboard.

```jinja
{% module "cta" path="@hubspot/email_cta", label="CTA Button" %}
```

**Do NOT wrap this in a `<div>`.** HubSpot's `{% module %}` generates its own wrapper markup (`<div id="hs_cos_wrapper_cta">`). Adding a parent div hides the module entirely in the email editor.

**Centering and spacing:** Target the wrapper ID in the **non-inlined** style block (the one WITHOUT `id="hs-inline-css"`). Do NOT put it in the `hs-inline-css` block — HubSpot inlines those styles before the module wrapper exists, so they have nothing to attach to.

```html
<!-- Non-inlined styles — HubSpot keeps these as <style> in <head> -->
<style type="text/css">
  /* Center the CTA module wrapper and its inner table */
  #hs_cos_wrapper_cta { text-align: center; padding: 16px 24px 0 24px; }
  #hs_cos_wrapper_cta table { margin: 0 auto; }
</style>
```

**Why this works:** The non-inlined `<style>` block stays in the `<head>` as a CSS rule. At render time, the module wrapper exists and the rules apply. `text-align: center` centers inline content; `margin: 0 auto` on the inner table centers block-level content. Works in Gmail, Apple Mail, iOS, and most modern clients. Outlook may ignore the `<style>` block (button still renders, just left-aligned).

**Brand colors:** Marketer sets the CTA background, text color, and corner radius from `brain/brand-guide/brand-guide.md` in the CTA editor's Styles tab. Some brand accents render inconsistently across email clients — Outlook, dark-mode Gmail, and forwarded chains can shift saturated colors. The brand guide should name an email-safe CTA color; verify it in major clients before standardizing. Web-safe accents can stay the default on landing pages where contrast is reliable.

**What you get:** CTA dashboard tracking (views, clicks, conversions), native "Link to: CTA" picker, marketer controls styling via editor UI.
**What you don't get:** Pixel-perfect brand CSS from the template — marketer sets brand colors manually per-email.

**CTA card copy:** headlines work better as imperatives that pair with the button ("See X in action" + "Book a demo") than as noun phrases ("X in action"). Flow: kicker poses the problem → imperative headline points to the solution → body proves it → button takes action. Avoid echo between the kicker, headline, and body opener — a headline that repeats the kicker's opening words is a dead giveaway.

#### Comparison

| Approach | Brand Control | CTA Dashboard | Editor UX |
|----------|--------------|---------------|-----------|
| **`@hubspot/email_cta` module** (recommended) | Marketer sets in Styles tab | Yes — views, clicks, conversions | Native CTA picker + style editor |
| ~~Styled `<a>` + `{% text %}`~~ | ~~Full inline CSS~~ | ~~Per-email only~~ | **Breaks in Remix editor — HubSpot auto-converts to broken module** |
| ~~`{% cta %}` tag~~ | ~~N/A~~ | ~~N/A~~ | **Does not work in emails — page-only tag** |

---

## Drag-and-Drop (dnd_area) Email Templates

HubSpot's email editor (Remix) always uses a drag-and-drop editor. Even coded templates get auto-converted to dnd modules — and the conversion often breaks (producing "Unknown Module" or uneditable modules). The fix: use `{% dnd_area %}` tags to **control** how HubSpot builds the module tree.

### When to Use dnd_area

**Choose between classic HubL and dnd_area based on who controls the layout.**

- **Classic HubL** (`{% text %}`, `{% rich_text %}`, `{% boolean %}`): template author locks the structure, marketers only fill in labelled fields. Use this for brand-critical recurring templates (newsletters, promos, announcements) where design consistency matters more than layout flexibility. Classic HubL templates render correctly in the Remix email editor.
- **dnd_area**: template author provides a starter layout, marketers drag/drop/reorder modules per send. Use when different issues need different structures, or when multiple non-technical marketers need layout flexibility without touching code.

For a single-marketer workflow with tight design control ([Company] today), classic HubL is usually the right default. Reach for dnd_area when layout flexibility per send is more valuable than brand-lockdown consistency.

### Required `<head>` Includes

```html
{{ dnd_area_stylesheet }}   <!-- REQUIRED for dnd_area rendering -->
{{ email_header_includes }}  <!-- Cross-client rendering -->
{{ reset_css_stylesheet }}   <!-- Cross-client CSS reset -->
```

### Constraints

- **Only ONE `dnd_area` per email template** (HubSpot limit)
- **`dnd_row` is NOT supported in email** — use `dnd_section` > `dnd_column` > `dnd_module`
- **Minimum width: 624px**
- Static HTML (logo, footer) goes OUTSIDE the `dnd_area` — locked, not editable per-email
- Module defaults are passed as parameters in the `dnd_module` tag

### Architecture Pattern

```
Static HTML (not editable)
├── Logo header
├── Gradient accent bar

{% dnd_area "main", full_width=False %}
├── dnd_section → dnd_column → dnd_module (content)
├── dnd_section → dnd_column → dnd_module (more content)
├── dnd_section → dnd_column → dnd_module @hubspot/email_cta
{% end_dnd_area %}

Static HTML (not editable)
├── Footer (logo, social, CAN-SPAM, unsubscribe)
```

**Pre-place a starter layout.** For recurring `dnd_area` newsletter templates, pre-place default `{% dnd_module %}` tags inside the `dnd_area` with realistic starter content (e.g. Featured + 2 Blog Posts + 1 Event + Dev Corner). This gives the marketer a working starting layout instead of an empty canvas.

**Section markers on repeatable modules.** For repeatable dnd custom modules (blog post, event, industry item), add a `show_section_marker` boolean field. Turn it ON for the first item in a group and OFF for the rest, so they stack cleanly under one marker and one leading divider. This prevents duplicate 'LATEST POSTS'-style headers when the marketer drops multiple instances.

### Static-vs-dnd Horizontal Alignment Gotcha

**The bug:** In a template mixing a static masthead/footer with a `dnd_area`, the dnd module content renders **~10px to the right** of the static sections — even when both use the same inner padding (e.g. `padding: 0 40px`). Visible as a misaligned divider/separator line or an off-axis share-row box.

**Why it happens:** HubSpot's `dnd_area_stylesheet` (injected via `{{ dnd_area_stylesheet }}`) adds default horizontal padding to the `.dnd-section` / `.dnd-column` / `.dnd-module` wrappers it generates. Those wrappers sit between your email-container `<td>` and your module's HTML, so the effective left offset of module content is `(module inner padding) + (wrapper padding)`, while static masthead/footer content is just `(td padding)`.

**What does NOT fix it** (tried and failed on a real newsletter build):
- `padding={'top':0,'bottom':0,'left':0,'right':0}` on `dnd_section` / `dnd_column`
- `hs_wrapper_css={'padding':'0'}` on every `dnd_module`
- `full_width=False` on `dnd_area` and `dnd_section` (still a good idea for other reasons, but doesn't fix the offset)
- A `<style>` block in the template `<head>` with `!important` overrides on `.dnd-section` / `.dnd-column` / `.dnd-module` — HubSpot's stylesheet injection wins the specificity war somehow.

**What DOES fix it — adjust the static sections, not the dnd wrappers.** Measure the offset live in devtools (in the company's case: ~10px), then bump the left (and usually right) padding on every static `<td>` by that amount so it aligns with the module content. The dnd wrapper's offset is fixed — you match it from the static side.

Concrete pattern that worked (modules use 40px inner L/R padding, wrapper adds ~10px each side):
```html
<!-- Masthead: left 50 (not 40) to match dnd module content -->
<td style="padding: 48px 40px 32px 50px;">...masthead...</td>

<!-- Share row: 50 L and R so the box aligns with module content both sides -->
<td style="padding: 48px 50px 0 50px;"><div>...share box...</div></td>

<!-- Footer divider: 50 L and R so the line matches module dividers -->
<td style="padding: 32px 50px 0 50px;"><div style="border-top: 1px solid #E5E7EB;">&nbsp;</div></td>
```

**Rule of thumb:** don't fight HubSpot's dnd wrapper. Measure the offset once, then pad the static sections to match. This keeps all the module padding logic untouched and doesn't rely on CSS override tricks that don't actually work.

**Diagnose 'shifted' or 'off' before fixing.** When a user flags an email as 'shifted' or 'off,' identify the specific element first. 'Shifted right' can mean viewport-level centering (usually a client or editor-preview quirk, not a bug) or element-level misalignment between static and dnd sections (the real bug, above). Ask which — don't guess. The wrong assumption burns test-send round-trips.

### Pre-placed vs. Dragged Module Width

Pre-placed `{% dnd_module %}` content is wrapped by HubSpot's editor with different default styles than modules the marketer drags in at runtime. If pre-placed content renders at a different width than dragged content, try `hs_wrapper_css={'padding':'0'}` on the `{% dnd_module %}`, or check whether the `{% dnd_area %}` needs `full_width=False` to stay inside its parent container's `max-width`.

### Module Paths for dnd Email

Only use modules confirmed to work in dnd email context:

| Module | Path | Works in dnd email |
|--------|------|--------------------|
| CTA Button | `@hubspot/email_cta` | **Confirmed** |
| Image | `@hubspot/image_email` | **Confirmed** (in official docs) |
| Email Body (rich text) | `@hubspot/email_body` | Testing |
| Raw HTML | `@hubspot/raw_html_email` | Testing |
| One line of text | `@hubspot/email_text` | Testing |

**Do NOT use `@hubspot/rich_text_email`** — this path does not exist and produces "Unknown Module" errors.

**Module folder convention.** Place custom modules for a `dnd_area` template in a `modules/` subfolder next to the template and reference them as `dnd_module path="./modules/name"`. This mirrors the repo layout to the Design Manager folder structure and makes uploads predictable.

### Syntax Examples

**Rich text content with default HTML:**
```jinja
{# Example values — use the email background and body text colors from /brain/brand-guide/brand-guide.md #}
{% dnd_section
    background_color={'color':'#111111'},
    padding={'top':'0','bottom':'0','left':'24','right':'24'}
%}
  {% dnd_column width=12 %}
    {% dnd_module
        path='@hubspot/email_body',
        html='<div style="font-size: 16px; color: #FFFFFF;">Default content here</div>'
    %}
    {% end_dnd_module %}
  {% end_dnd_column %}
{% end_dnd_section %}
```

**CTA button (native editor):**
```jinja
{# Example background — use the email background color from /brain/brand-guide/brand-guide.md #}
{% dnd_section
    background_color={'color':'#111111'},
    padding={'top':'36','bottom':'0','left':'24','right':'24'}
%}
  {% dnd_column width=12, horizontal_alignment='CENTER' %}
    {% dnd_module path='@hubspot/email_cta' %}
    {% end_dnd_module %}
  {% end_dnd_column %}
{% end_dnd_section %}
```
Marketer sets brand colors manually in Button module style tab: the brand guide's email CTA background, button text color, and corner radius.

**Image module:**
```jinja
{% dnd_module path='@hubspot/image_email',
    img={'alt':'Logo', 'height':32, 'src':'https://example.com/logo.svg', 'width':143},
    alignment='center'
%}
{% end_dnd_module %}
```

### dnd_section Parameters

```jinja
{# Example background — use the card/surface color from /brain/brand-guide/brand-guide.md #}
{% dnd_section
    background_color={'color':'#111111'},
    padding={'top':'0','bottom':'0','left':'24','right':'24'},
    max_width=600
%}
```

---

### Required CAN-SPAM Footer Variables
```html
{{ site_settings.company_name }}
{{ site_settings.company_street_address_1 }}
{{ site_settings.company_street_address_2 }}
{{ site_settings.company_city }}
{{ site_settings.company_state }}
{{ site_settings.company_zip }}
{{ site_settings.company_country }}
```

### Required Links
```html
<!-- Unsubscribe -->
<a data-unsubscribe="true" href="{{ unsubscribe_link }}">Unsubscribe</a>

<!-- Unsubscribe from all -->
<a data-unsubscribe="true" href="{{ unsubscribe_link_all }}">Unsubscribe from all</a>

<!-- View as webpage -->
<a data-viewaswebpage="true" href="{{ view_as_page_url }}">View as web page</a>
```

### Preview Text
```html
<div id="preview_text" style="display:none!important;">
  {% text "preview_text" label="Preview Text" value="Preview text here" %}
</div>
```

### CSS Inlining
Use `id="hs-inline-css"` on style blocks that should be compiled to inline CSS:
```html
<style type="text/css" id="hs-inline-css">
  /* These styles will be inlined on target elements */
  td { font-family: Arial, sans-serif; }
</style>
```

Keep media queries in a **separate** `<style>` block (without the inline ID) so they aren't inlined:
```html
<style type="text/css">
  @media only screen and (max-width: 620px) {
    .mobile-full { width: 100% !important; }
  }
</style>
```

---

## Email HTML Best Practices

### Layout
- **Always use tables for layout.** `<table role="presentation">` with `cellspacing="0" cellpadding="0" border="0"`
- **600px max width** for the email container
- **Single-column layouts** are most reliable across clients
- **Stack on mobile:** Multi-column desktop layouts should collapse to single column via media queries
- Use `align="center"` on wrapper `<td>` to center the email container

### CSS
- **Inline all critical styles.** Email clients strip `<style>` blocks unpredictably
- Keep a `<style>` block in `<head>` as progressive enhancement, but don't rely on it
- Media queries go in their own `<style>` block
- Never use: `position`, `float`, `flexbox`, `grid`, `filter`, `clip-path`, `calc()`, `CSS variables`
- `border-radius` works in most clients except Outlook (degrades gracefully to square)
- `background-image` unreliable in Outlook — always have a solid `background-color` fallback

### Typography
- Use system-safe font stacks: `Arial, Helvetica, sans-serif` or `Georgia, serif`
- `@import` Google Fonts as progressive enhancement — they render in Apple Mail, iOS, some Android — but **always** include fallback
- For AI Upload: don't rely on custom fonts at all
- Minimum body text: 14px. Recommended: 16px for readability on mobile
- **Link colors on light backgrounds must pass WCAG AA (4.5:1).** Many brand accents fail on white — define a darker, accessible variant of the accent for links on light backgrounds, and record it in the brand guide

### Images
- All images must be **publicly accessible URLs**
- Always include `alt` text, `width`, `height`, and `style="display: block; border: 0;"`
- Use `width` attribute (not just CSS) for Outlook compatibility
- Don't use CSS `filter` on images — use pre-made assets in the correct color
- Compress images for fast load times
- **60/40 rule:** Approximately 60% text, 40% images for deliverability
- **Hugging the left edge:** wrap an image inside a `<td>` in a zero-whitespace table (`<td style="padding:0; line-height:0; font-size:0;">`) when it must sit flush-left with other siblings. A plain `<a><img></a>` inside a `<td>` picks up a leading space from surrounding HTML whitespace in some clients, offsetting the image to the right of other left-aligned elements.

### Icons

For newsletter and digest-style emails, use line icons (e.g. Lucide) paired with uppercase section labels rather than emoji. Emoji looks dated and can't match brand voice; line icons give a clean, modern, TLDR-like feel.

**Icon workflow:** download the Lucide SVG from `unpkg.com/lucide-static@latest/icons/{name}.svg`, bake the brand accent hex in place of `currentColor` with `sed 's/stroke="currentColor"/stroke="#RRGGBB"/'` (use the accent hex from the brand guide), then rasterize to a 40×40 PNG with `rsvg-convert -w 40 -h 40`. Store both the SVG and PNG side by side in `marketing/icons/{category}/`, and reference the PNG in email (SVG support is unreliable across clients).

### Buttons
- Use the **bulletproof button** pattern (table-based) for Outlook compatibility:
```html
<!-- Placeholder colors — use the email CTA background and button text colors from the brand guide -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0">
  <tr>
    <td style="background-color: #333333; border-radius: 12px; text-align: center;">
      <a href="[URL]" target="_blank"
         style="display: inline-block; padding: 14px 36px; font-family: Arial, Helvetica, sans-serif; font-size: 17px; font-weight: 500; color: #FFFFFF; text-decoration: none;">
        Button Text
      </a>
    </td>
  </tr>
</table>
```

### Dark Mode — Gmail iOS (Critical)

Gmail App on iOS is a massive platform and the hardest dark mode problem in email. **Read this before building any dark-themed email template.**

**How Gmail iOS dark mode works:**
- Gmail applies a proprietary color inversion algorithm to emails — it modifies BOTH backgrounds AND text colors
- It targets: `background-color` CSS, `bgcolor` HTML attributes, `color` CSS, and `<font color="">` tags
- There is **no opt-out**. No meta tag, CSS property, or HTML attribute reliably prevents Gmail iOS from modifying colors
- `@media (prefers-color-scheme: dark)` is **ignored** by Gmail iOS (works in Gmail Web only)
- `color-scheme` / `supported-color-schemes` meta tags have **no effect** on Gmail iOS

**What Gmail iOS does NOT touch:**
- `background-image` (including `linear-gradient()`) — this is the only known way to preserve a background color
- Actual images (`<img>` tags) — these render as-is

**Techniques we tested and their results:**

| Technique | Fixes Backgrounds? | Fixes Text? | Verdict |
|-----------|-------------------|-------------|---------|
| `color-scheme` meta tags | No | No | Useless for Gmail iOS |
| `bgcolor` on `<table>`/`<td>` | No | N/A | Gmail inverts these too |
| `background-image: linear-gradient(#color, #color)` | **Yes** | No | Only reliable background fix |
| `<font color="">` tags | N/A | No | Gmail overrides them |
| `@media (prefers-color-scheme: dark)` | N/A | N/A | Gmail iOS ignores entirely |

**The core problem for dark-themed emails:** You can preserve dark backgrounds with the gradient hack, but Gmail will still mute/shift all text colors. The result is dark background + washed-out text — which can look worse than letting Gmail do its full inversion (where at least backgrounds and text have consistent contrast).

**Recommendation:**
- **Do not build dark-themed email templates expecting pixel-perfect rendering in Gmail iOS dark mode.** It will not happen.
- If you build a dark email, accept that Gmail iOS users will see a color-shifted version. Test in HubSpot's "Preview in email client" → Gmail App Dark (iOS 18) to verify it's at least readable.
- Consider whether a light-themed template would serve better if Gmail iOS is a priority audience.
- Do NOT add `background-image` gradient hacks, `<font>` tags, or `color-scheme` meta tags to "fix" Gmail dark mode — we tested all of these and none produce an acceptable result for dark emails. They create partial fixes that look worse than Gmail's native full inversion.

### Dark Mode — Other Clients

- **Apple Mail:** Respects `@media (prefers-color-scheme: dark)` and `color-scheme` meta — progressive enhancement works here
- **Outlook.com / Outlook mobile:** Uses `[data-ogsc]` (text color) and `[data-ogsb]` (background color) attributes when forcing dark mode. These are Outlook-specific, not Gmail.
- **Transparent PNGs** may become invisible on inverted backgrounds — use solid-background versions or test carefully
- For clients that support it, `color-scheme: light dark;` in CSS is fine as progressive enhancement — just know it does nothing for Gmail iOS

### Outlook Specific
- Outlook uses Word as its rendering engine — most CSS is ignored
- Use `<!--[if mso]>` conditional comments for Outlook-specific fixes
- MSO properties (`mso-table-lspace`, `mso-padding-alt`, etc.) are valid for Outlook only
- `border-radius` does not work in Outlook — buttons degrade to rectangular
- Background images don't work in Outlook without VML (Vector Markup Language) hacks

---

## [Company] Brand Adaptation for Email

Since email clients have limited CSS support, adapt the brand system. Pull every color value from `/brain/brand-guide/brand-guide.md` — never hardcode them into the skill or reuse values from a previous build:

| Brand Element | Website | Email Adaptation |
|--------------|---------|-----------------|
| Background | Brand background color | Solid hex from the brand guide — works in email |
| Font | The brand font (see brand-guide) | `Arial, Helvetica, sans-serif` or another web-safe fallback stack (with `@import` of the brand font as progressive enhancement) |
| Gradient accent bar | CSS `linear-gradient` | Use a **pre-made gradient image** (hosted PNG/SVG) or a thin `<img>` element |
| Gradient text | `background-clip: text` | Not supported — use a solid text color from the brand guide instead |
| CTA button | Brand CTA color, solid | Styled `<a>` with `{% text %}` fields for URL and copy (see CTA section above) |
| Accent tag | Solid accent bg + contrasting text | Works with inline styles — solid `background-color` and `color` on the tag element are reliable across clients |
| Card surfaces | Card surface color with `border-radius` | Use the brand guide's card color as a solid bg. Radius works except Outlook (graceful degradation) |
| Border | `1px solid` brand border color | Works inline on `<td>` |
| Social icons | CSS `filter: invert()` | **Don't use filter.** Host icon PNGs in the correct color and reference directly |

### CTA Card Blocks

Only simple card-style CTA blocks from the brand guide translate to email. Variants that rely on CSS gradient backgrounds and ambient glows get stripped by email clients — adapt the brand's card CTA pattern with solid background colors and a bulletproof button (see Buttons above).

### Gradient Bar as Image
Since CSS gradients don't work in email backgrounds, create the signature gradient as a hosted image:
- Create a 600x4px PNG with the brand gradient (colors from the brand guide)
- Host it publicly (website or HubSpot File Manager)
- Reference as `<img src="[gradient-bar-url]" width="600" height="4" style="display: block;" />`

---

## Base Template + Variants

All [Company] HubSpot email templates use a **base template** pattern. The shared foundation (header, gradient bar, CTA, footer) lives in one file, and each email type is a variant that customizes the content area.

### Existing Templates

```
marketing/templates/email-templates/
├── email-base-hubspot.html              ← Base (DO NOT upload — starting point only)
├── [variant]-email.html                 ← One file per email type (classic coded, HubL fields)
└── _previews/                           ← Static HTML previews (not for upload)
    └── [variant]-preview.html
```

**Iterate locally against `_previews/*.html` before pushing to HubSpot.** HubSpot round-trips are slow and obscure layout cause-and-effect. Keep the preview faithful to HubSpot's dnd_area wrapping (`<td class="dnd-section">` → `<td class="dnd-column">` → `<td class="dnd-module">`); if a preview doesn't mirror that nesting, fix the preview before debugging layout issues in HubSpot.

### Creating a New Email Variant

1. Duplicate `email-base-hubspot.html`
2. Rename it (e.g., `product-announcement-hubspot.html`)
3. Update the template annotations:
   - Set `isAvailableForNewContent: true`
   - Update `label` (e.g., `[Company] - Product Announcement`)
4. Replace the content between `CONTENT START` and `CONTENT END` with your email-specific sections
5. Add any extra responsive CSS classes in the media query `<style>` block if needed
6. Upload to Design Manager (see Upload Instructions below)

### What's Shared (don't modify unless updating brand)
- Logo header
- Gradient accent bar
- CTA button section (styled `<a>` with `{% text %}` fields for URL and button copy — marketer edits from sidebar)
- Footer (social icons, CAN-SPAM address, unsubscribe, view-as-webpage)
- Base styles (`id="hs-inline-css"`) and responsive media queries
- Preview text module

### What Changes Per Variant
- The content area between the gradient bar and CTA
- Any variant-specific responsive CSS classes (e.g., `.date-col` for a two-column date layout)
- The preview text default value

---

## Template Structure

Every email template should follow this structure:

```
1. DOCTYPE + HTML wrapper
2. <head>
   - Meta tags (charset, viewport, X-UA-Compatible)
   - Outlook conditional comments (PixelsPerInch)
   - <style> block with inline-css ID (base styles)
   - <style> block for media queries (responsive)
3. <body> (background color on body + wrapper table)
4. Full-width wrapper table (100% width, centered)
5. Email container table (600px, centered)
   a. Logo header (linked to website)
   b. Content sections
   c. CTA button(s)
   d. Footer (social icons, copyright, unsubscribe)
6. Closing tags
```

---

## Output Format

**Output location:** `marketing/email/templates/[template-slug]/` — confirm the project slug with the user before creating files.

### For Each Template, Provide:

**1. Complete HTML file**
- Production-ready, tested against the constraints above
- All styles inlined on elements
- Progressive `<style>` block in head
- Responsive media queries in separate `<style>` block
- `<!-- EDITABLE: -->` comments marking content the user should replace
- Placeholder brackets `[like this]` for variable content

**2. Upload instructions**
- Brief notes on which upload method to use (AI Upload vs. coded template)
- Any post-upload adjustments needed in HubSpot's editor
- Image hosting requirements (list any images that need public URLs)

**For Design Manager (coded templates):**
1. Go to **Content > Design Manager** (or **Marketing > Files and Templates > Design Tools**)
2. Click **File > New file**
3. Select **HTML + HubL** as the file type
4. In "What are you building?" select **Template**
5. Click **Template type** and select **Email**
6. Enter a file name and click **Create**
7. Paste the complete template code
8. Click **Publish** (top right)
9. The template will appear in the template picker when creating new marketing emails
10. All HubL editable fields (`{% text %}`, `{% rich_text %}`, `{% boolean %}`) will appear in the right sidebar when editing an email

**3. Testing checklist**
- [ ] Preview in HubSpot
- [ ] Send test email to yourself
- [ ] Check rendering in Gmail (web + mobile) — including Gmail App Dark (iOS 18) preview
- [ ] Check rendering in Outlook (if audience uses it)
- [ ] Check rendering in Apple Mail
- [ ] Verify all links work
- [ ] Verify images load
- [ ] Check mobile responsive behavior

---

## Checklist Before Delivering

- [ ] Read `/brain/brand-guide/brand-guide.md`
- [ ] Template annotations present (for coded templates: `templateType: email`, `isAvailableForNewContent: true`, `label`)
- [ ] Max width 600px
- [ ] Table-based layout only (no flexbox, grid, floats, positioning)
- [ ] All critical styles inlined
- [ ] No CSS gradients on backgrounds (use images or solid colors)
- [ ] No overlapping elements
- [ ] No JavaScript
- [ ] No `filter` CSS property
- [ ] Font stack includes system-safe fallbacks
- [ ] All images use publicly accessible URLs
- [ ] All images have `alt`, `width`, `height`, `display: block`, `border: 0`
- [ ] Bulletproof button pattern used for CTAs
- [ ] Social icons are pre-made white PNGs (not filtered)
- [ ] Gmail App Dark (iOS 18) preview checked — email is readable (colors will shift, that's expected)
- [ ] No transparent PNGs that become invisible on inverted backgrounds
- [ ] CAN-SPAM compliant footer (unsubscribe link present)
- [ ] Responsive media queries in separate `<style>` block
- [ ] Outlook conditional comments included
- [ ] Tested at 600px and mobile widths
- [ ] No AI slop patterns in copy (see CLAUDE.md)
- [ ] Product claims verified against `/brain/truth.md`

---

## Subscription Types & List Filtering (Sending)

These rules govern who actually receives an email — separate from how the template is built.

- **Set the email's Subscription type correctly.** HubSpot's send engine auto-filters recipients by the Subscription type field on the email itself, so list-level opt-in filters are redundant: the list defines the candidate pool, the Subscription type field is the actual gate. The type also determines which unsubscribe link the recipient sees and which subscription gets decremented on unsubscribe. Wrong type = unsubscribes hit the wrong list, a compliance and trust risk.
- **Active-list 'subscriber' filters must account for the tri-state model.** HubSpot's `Opted out of email: [subscription name]` property is null by default (Subscribed / Unsubscribed / Not Specified). A filter for 'subscribers' must use `is none of Yes` AND check the 'Include records where property is empty' box — otherwise never-unsubscribed contacts are excluded from the list.

---

## MCP Tools: HubSpot Dev, Figma & agent-browser

### HubSpot Dev MCP (Documentation & CMS)

Use these tools to look up HubSpot documentation and manage CMS assets:

1. **Search docs** — Use `mcp__HubSpotDev__search-docs` to find HubSpot developer documentation on email modules, template markup, HubL syntax, or any email-related API. Always search before guessing at module paths or field syntax.
2. **Fetch doc page** — Use `mcp__HubSpotDev__fetch-doc` immediately after searching to read the full documentation page. Never skip this step — search results are summaries, not complete docs.
3. **Create a CMS template** — Use `mcp__HubSpotDev__create-cms-template` to scaffold a new email template file. Set `templateType` to `email-template`.
4. **List remote contents** — Use `mcp__HubSpotDev__list-cms-remote-contents` to see what templates and assets are already deployed in the HubSpot Design Manager.
5. **Create a CMS module** — Use `mcp__HubSpotDev__create-cms-module` to scaffold a custom email module if needed.

**When to use:** Before building any email template, search docs to verify module paths (e.g., confirm `@hubspot/email_body` vs `@hubspot/email_text` behavior). After building, use `list-cms-remote-contents` to check for naming conflicts before manual upload.

---

### Figma MCP (Design Input)

When the user provides a Figma URL or references an email design mockup:

1. **Pull design context** — Use `mcp__figma-remote-mcp__get_design_context` to extract layout, colors, typography, and spacing from the Figma mockup. Translate these into email-safe HTML (table-based, inline styles, system fonts).
2. **Take a screenshot** — Use `mcp__figma-remote-mcp__get_screenshot` to see the visual design before building the template.
3. **Get metadata** — Use `mcp__figma-remote-mcp__get_metadata` to understand the section structure and layer hierarchy.

**When to use:** When the user has an email design in Figma that needs to be converted to a HubSpot-compatible HTML template. Remember: the Figma design will use features email doesn't support (gradients, custom fonts, border-radius) — adapt per the constraints in this skill.

### agent-browser (Email Rendering Validation)

After building an email template, use agent-browser to validate rendering:

1. **Open the template** — Run `agent-browser open <file>` to open the HTML email file in the browser.
2. **Test at email width** — Run `agent-browser set viewport 600 900` to set the viewport to 600px wide (email container width), then run `agent-browser screenshot` to capture the result.
3. **Test mobile rendering** — Run `agent-browser set viewport 375 812` and run `agent-browser screenshot` again to verify responsive behavior.
4. **Full-page capture** — Run `agent-browser screenshot` to capture the entire email template for review.
5. **Check accessibility** — Run `agent-browser snapshot -i` to verify heading structure, link text, and alt text on images.
6. **Console errors** — Run `agent-browser console` to catch any broken image references or CSS issues.

**When to use:** After building any email template — always use agent-browser to validate in the browser before delivering. This catches layout issues, broken images, and responsive problems before the template reaches HubSpot.

---

## HubSpot Documentation References

- [Email template markup](https://developers.hubspot.com/docs/cms/building-blocks/templates/email-template-markup) — CSS handling, responsive structures, required HubL variables
- [Specify drag and drop areas in a custom email template](https://developers.hubspot.com/docs/cms/guides/specify-drag-and-drop-areas-in-a-custom-email-template) — `dnd_area`, `dnd_section`, `dnd_column`, `dnd_module` tags for email
- [Using modules in templates](https://developers.hubspot.com/docs/cms/building-blocks/modules/using-modules-in-templates) — module snippets, paths, default modules
- [Create and edit modules in the design manager](https://knowledge.hubspot.com/design-manager/create-and-edit-modules) — custom module creation, field types, editor options
- [Build a custom coded template](https://knowledge.hubspot.com/design-manager/build-a-custom-coded-template) — Design Manager upload workflow
- [HubSpot's default modules](https://knowledge.hubspot.com/design-manager/use-default-modules-in-your-template) — default module paths and usage
- [Templates overview](https://developers.hubspot.com/docs/cms/building-blocks/templates) — template types, annotations, structure
- [Using HubL tags to change href](https://community.hubspot.com/t5/CMS-Development/Using-HubL-tags-to-change-href/m-p/528716) — community discussion on HubL in href attributes
- [Custom coded email](https://community.hubspot.com/t5/CMS-Development/Custom-coded-email/m-p/393616) — community discussion on coded email template patterns
- [Adding button module with CTA to custom HTML email](https://community.hubspot.com/t5/CMS-Development/Adding-button-module-with-cta-module-to-a-custom-HTML-email/m-p/538887) — community discussion on button/CTA in coded emails
- [How to code custom drag & drop email templates](https://community.hubspot.com/t5/CMS-Development/How-to-code-custom-drag-amp-drop-email-templates-in-HubSpot/td-p/427327) — community discussion on dnd email templates

---

## Analytics

Use the `analytics` skill to pull real email performance data when reviewing or optimizing email templates:

- **`hubspot-emails.ts`** — Open rates, click rates, CTOR, bounce rates, and top-performing emails. Benchmark new templates against historical performance or identify which formats work best.

Example: Before building a new email template, run `npx tsx .claude/skills/analytics/scripts/hubspot-emails.ts 90d` to see which existing emails had the highest open/click rates, then apply those patterns to the new template.

---

## Mandatory Skill Delegation

**Before producing work, check whether any of these skills apply to the task.** If they do, load the skill before writing that portion. Do not replicate a skill's logic from memory — load it and apply it.

| When the task involves... | Skill to Load | Mandatory? |
|--------------------------|---------------|-----------|
| CTA buttons (placement, centering, tracking, brand CSS) | `hubspot-cta` | Yes — load before adding any CTA to a template |
| Writing or reviewing email copy/messaging | `copywriting` or `copy-editing` | Yes — load before writing or editing copy |
| Email sequence strategy, drip campaign logic | `email-sequence` | Yes — load when the email is part of a sequence |
| Visual design decisions beyond what's in the brand guide | `brand-design` | Yes — load for custom visual asset work |
| Landing page templates (different constraints) | `hubspot-landing-page` | Load if the user asks about landing pages to avoid applying email constraints |

---

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
