---
name: hubspot-cta
version: 1.1.0
description: "Implement CTA buttons in HubSpot email and landing page templates. Use when the user wants to add, fix, or style CTA buttons in HubSpot templates. Also use when the user mentions 'HubSpot CTA,' 'email CTA,' 'call to action button,' 'CTA module,' or 'email_cta.' Works alongside hubspot-email and hubspot-landing-page skills."
---

# HubSpot CTA Buttons

You are an expert at implementing CTA (call-to-action) buttons across HubSpot email templates and landing page templates. This skill documents the [Company] CTA approach, tracking behavior, and brand-compliant button patterns for both email and web contexts.

**This skill works alongside:**
- **hubspot-email** — email template constraints, table-based layout, 600px max
- **hubspot-landing-page** — landing page template constraints, full CSS support
- **web-design** — hover/focus/active states, motion, accessibility, and polish/audit workflows for any CTA that ships on a live landing page

## Before Building

**Always read these first:**
1. `/brain/brand-guide/brand-guide.md` — colors, typography, button styles
2. This skill file — CTA approach and patterns
3. The relevant template skill (`hubspot-email` or `hubspot-landing-page`) for context-specific constraints

---

## CTA Approach by Template Type

**IMPORTANT: Email and landing page templates use different CTA approaches.** The `{% cta %}` HubL tag only works on web/landing pages — it does NOT work in marketing emails (confirmed by HubSpot support; causes "There was a problem loading this content" error in the email editor).

### Email Templates: `@hubspot/email_cta` Module

Email templates use the native `email_cta` module. Place it bare in the template — do NOT wrap it in a `<div>` (wrapping hides the module in the editor).

```jinja
{% module "cta" path="@hubspot/email_cta", label="CTA Button" %}
```

**Centering:** Target the module's auto-generated wrapper ID in the **non-inlined** style block (the one WITHOUT `id="hs-inline-css"`). Do NOT use the `hs-inline-css` block — those styles get inlined before the wrapper exists.

```html
<style type="text/css">
  #hs_cos_wrapper_cta { text-align: center; padding: 16px 24px 0 24px; }
  #hs_cos_wrapper_cta table { margin: 0 auto; }
</style>
```

**Brand colors:** Marketer sets the brand guide's CTA background, text color, and button radius in the CTA editor's Styles tab. Email CTAs and landing-page CTAs may need different colors — some accents render inconsistently across email clients, and an accent competing with nearby accents loses its call-to-action weight. The brand guide (`brain/brand-guide/brand-guide.md`) should name the approved CTA color per context.

**What does NOT work for email CTAs:**
- ~~Styled `<a>` + `{% text %}`~~ — HubSpot Remix editor auto-converts to a broken module
- ~~`{% cta %}` tag~~ — page-only, causes "There was a problem loading this content"
- ~~Wrapping `{% module %}` in a `<div>`~~ — hides the module entirely in the editor
- ~~CSS in `hs-inline-css` targeting `#hs_cos_wrapper_cta`~~ — styles inlined before wrapper exists

### Landing Page Templates: Embedded HTML CTAs with `{% cta %}`

Landing page templates use **`{% cta %}` HubL tags** that reference **Embedded HTML CTAs** created in HubSpot. The Embedded HTML type gives full design control via custom CSS while plugging into HubSpot's CTA tracking pipeline (views, clicks, conversions).

1. **Create** an Embedded HTML CTA in HubSpot (Marketing > Lead Capture > CTAs) with the button text, destination URL, and brand CSS
2. **Reference** it in templates with `{% cta "main_cta" label="CTA Button" %}`
3. **Pick** which CTA to use from the sidebar when building each page

### Blog Posts (Sanity CMS): Embedded CTA in Card Wrapper

Blog posts use a **self-contained HTML card** with a HubSpot-tracked button inside. Keep the card HTML in a template file in your instance (e.g., `templates/blog-cta.html`) and paste it into Sanity's **Custom HTML Embed** field.

**How it works:**
- The card wrapper (border, pill label, heading, subtext) is static inline-styled HTML
- The button inside is a HubSpot Embedded CTA with click tracking (create one, note its CTA ID)
- The CTA styles are scoped to the embed's auto-generated CTA class (it ends in the CTA ID) to prevent CSS bleed into the blog page

**IMPORTANT: The HubSpot embed code's default `<style>` uses bare `a` selectors that will restyle every link on the page.** Fix this in the template file by scoping to the CTA class. If updating the embed code, always scope the styles.

**Usage:** Copy the card template contents into Sanity's Custom HTML Embed field. No modifications needed per-post (the HubSpot tracking link is the same CTA across all posts).

### Comparison

| Approach | Works In | Design Control | CTA Dashboard | Tradeoff |
|----------|----------|---------------|---------------|----------|
| **`@hubspot/email_cta` module** (recommended for email) | Emails | Marketer sets in Styles tab | Yes — views, clicks, conversions | Brand colors set manually per-email |
| **Embedded HTML CTA + `{% cta %}`** | Landing pages only | Full — brand CSS on each CTA | Yes — views, clicks, conversions | Create one CTA per unique URL |
| **Embedded CTA in card wrapper** | Blog (Sanity CMS) | Full — inline styles + HubSpot button | Yes — views, clicks | Same CTA across posts; card HTML pasted per-post |
| ~~Styled `<a>` + `{% text %}`~~ | ~~Emails~~ | ~~Full inline CSS~~ | ~~Per-email only~~ | **Breaks in Remix editor** |
| ~~`{% cta %}` in emails~~ | ~~Emails~~ | ~~N/A~~ | ~~N/A~~ | **Does not work — page-only tag** |

### Per-Campaign Workflow

For each new campaign (webinar, event, announcement):

1. Go to **Marketing > Lead Capture > CTAs** (or **Marketing > CTAs**)
2. Click **Create CTA**
3. Select **Embeds and Buttons** tab > **Embedded HTML**
4. Set the **Link URL** (e.g., the webinar registration page URL)
5. Set the **Button Content** (e.g., "Register Now →")
6. Go to **Advanced > Custom CSS**
7. Paste the appropriate brand CSS (see sections below)
8. Save the CTA
9. When building the email or page, pick this CTA from the sidebar dropdown

---

## Brand CSS for Embedded HTML CTAs

### Email CTA CSS

Paste this into the CTA's **Advanced > Custom CSS** when creating CTAs for email use:

```css
a {
  display: inline-block;
  padding: 14px 36px;
  background-color: #111111; /* placeholder — email CTA background from brand-guide */
  font-family: Arial, Helvetica, sans-serif; /* prepend the brand font (see brand-guide) */
  font-size: 17px;
  font-weight: 500;
  color: #FFFFFF !important; /* placeholder — CTA text color from brand-guide */
  text-decoration: none;
  border-radius: 12px; /* placeholder — button radius from brand-guide */
  line-height: 1.2;
}
a:hover {
  background-color: #333333; /* placeholder — hover color from brand-guide */
}
```

No transitions (email clients don't support them). System font fallback included.

### Landing Page CTA CSS

Paste this into the CTA's **Advanced > Custom CSS** when creating CTAs for landing page use:

```css
a {
  display: inline-block;
  padding: 12px 32px;
  background-color: #111111; /* placeholder — landing page CTA background from brand-guide */
  font-family: Arial, Helvetica, sans-serif; /* prepend the brand font (see brand-guide) */
  font-size: 18px;
  font-weight: 500;
  color: #FFFFFF !important; /* placeholder — CTA text color from brand-guide */
  text-decoration: none;
  border-radius: 12px; /* placeholder — button radius from brand-guide */
  line-height: 150%;
  transition: background-color 0.3s;
}
a:hover {
  background-color: #333333; /* placeholder — hover color from brand-guide */
}
```

### Legacy CTA Caveat

Custom CSS on CTAs is available through the **legacy CTA tool**. Accounts created after March 17, 2025 do not have access to the legacy tool. The new CTA tool has a visual style editor (colors, fonts, spacing) but no raw CSS input. If using the new tool, set:
- Background color: the brand guide's CTA background
- Text color: the brand guide's CTA text color
- Font: the brand font (see brand-guide), or Arial as fallback
- Border radius: the brand guide's button radius
- Padding: match values above

---

## Using CTAs in Templates

### In Email Templates (coded, Design Manager)

**`{% cta %}` does not work in email templates** — it's a page-only HubL tag. Use the `@hubspot/email_cta` module:

```jinja
{% module "cta" path="@hubspot/email_cta", label="CTA Button" %}
```

**Do NOT wrap in a `<div>`** — it hides the module in the editor. Center via non-inlined CSS:

```html
<!-- In the non-inlined <style> block (no id="hs-inline-css") -->
<style type="text/css">
  #hs_cos_wrapper_cta { text-align: center; padding: 16px 24px 0 24px; }
  #hs_cos_wrapper_cta table { margin: 0 auto; }
</style>
```

The marketer selects a CTA from the sidebar and sets brand colors in the Styles tab.

### In Landing Page Templates (fixed layout)

```html
<!-- Tracked CTA — marketer picks from sidebar -->
<div style="text-align: center; padding: 36px 0;">
  {% cta "main_cta" label="CTA Button" %}
</div>
```

### Anchor Link CTAs (Landing Pages Only)

For bottom-of-page CTAs that scroll to a form section, use a styled `<a>` tag with the `.btn-primary` class. These don't need CTA tracking — the conversion is the form submission:

```html
<a href="#registration_form" class="btn-primary">Register for the Webinar</a>
```

---

## Landing Page Button CSS Reference

For non-tracked buttons (anchor links, in-page navigation), use the `.btn-primary` and `.btn-secondary` classes from the base landing page template:

```css
.btn-primary {
  display: inline-block;
  padding: 12px 32px;
  background-color: var(--btn-primary-bg);    /* primary button color from brand-guide */
  color: var(--btn-text);                     /* button text color from brand-guide */
  font-family: var(--brand-font);             /* the brand font (see brand-guide) */
  font-size: 18px;
  font-weight: 500;
  line-height: 150%;
  border: none;
  border-radius: 12px; /* placeholder — button radius from brand-guide */
  text-decoration: none;
  transition: background-color 0.3s;
}
.btn-primary:hover { background-color: var(--btn-primary-hover); /* hover color from brand-guide */ }

.btn-secondary {
  display: inline-block;
  padding: 12px 32px;
  background-color: var(--btn-secondary-bg);  /* secondary button color from brand-guide */
  color: var(--btn-text);                     /* button text color from brand-guide */
  font-family: var(--brand-font);
  font-size: 18px;
  font-weight: 500;
  line-height: 150%;
  border: 1px solid var(--btn-border);        /* button border color from brand-guide */
  border-radius: 12px; /* placeholder — button radius from brand-guide */
  text-decoration: none;
  transition: all 0.3s;
}
.btn-secondary:hover { background-color: var(--btn-secondary-hover); /* hover color from brand-guide */ }
```

---

## Custom CTA Module (Design Manager)

For drag-and-drop landing page templates, build a custom module in Design Manager so the CTA button appears as a draggable component with a built-in CTA picker.

### Module Structure

A custom module in HubSpot Design Manager consists of:
- **Fields** (the editor UI) — defined in the module's field configuration
- **HTML + HubL** (the rendering template) — how the module renders on the page
- **CSS** (optional) — module-specific styles

### Field Configuration

| Field | Type | Label | Default |
|-------|------|-------|---------|
| `cta_button` | CTA | CTA Button | (none — marketer picks from CTA library) |
| `alignment` | Choice (dropdown) | Button Alignment | `center` (options: `left`, `center`, `right`) |

The **CTA field type** embeds a CTA picker directly in the module, so the marketer selects from existing HubSpot CTAs — getting full tracking.

### Module HTML + HubL

```html
<div style="text-align: {{ module.alignment }};">
  {% cta "cta_button" %}
</div>
```

### Creating the Module in Design Manager

1. Go to **Content > Design Manager**
2. Click **File > New file**
3. Select **Module** as the file type
4. Name it `[Company] CTA Button`
5. Add the fields listed above using the field editor
6. Paste the HTML + HubL into the module template
7. Click **Publish**
8. The module will appear in the module picker when editing drag-and-drop pages

**Note:** This module is for **web/landing pages only**. Email templates use `{% module "cta" path="@hubspot/email_cta" %}` (see above).

---

## HubSpot CTA Tracking

### What CTA Dashboard Tracking Provides

When using `{% cta %}` with a HubSpot CTA object, you get:
- **Views** — how many times the CTA was displayed
- **Clicks** — how many times the CTA was clicked
- **Click rate** — clicks / views
- **Submissions** — form submissions attributed to the CTA
- **Conversion rate** — submissions / clicks
- **Aggregate data** — performance across all placements of the same CTA

### Email Link Tracking (Also Automatic)

In addition to CTA dashboard tracking, HubSpot automatically tracks **every link click** in marketing emails. This provides per-email click metrics (total clicks, unique clicks, click rate) in the email performance dashboard.

### Landing Page Tracking

On landing pages with the HubSpot tracking code:
- CTA views and clicks tracked in CTA dashboard
- Page views, time on page tracked in page analytics
- Form submissions tracked as conversions

---

## HubSpot CTA Types Reference

HubSpot's CTA tool (Marketing > CTAs) offers these types:

| Type | Behavior | Use Case |
|------|----------|----------|
| **Embedded** (button) | Inline button element on page | CTA buttons in content — **this is what we use** |
| **Embedded** (image) | Inline image CTA | Banner-style CTAs |
| **Pop-up Box** | Modal triggered by scroll %, time, exit intent, or inactivity | Lead capture overlays |
| **Sticky Banner** | Fixed bar at top or bottom of page | Persistent promotions |
| **Slide-in** | Corner slide-in triggered by scroll %, time, exit intent, or inactivity | Non-intrusive lead capture |

Pop-up, sticky banner, and slide-in CTAs require the **HubSpot tracking code** installed on the page.

### Available Module Field Types (for Custom Modules)

When building custom modules in Design Manager, these field types are available:

Alignment, Background Image, Blog, Boolean, Border, Choice, Color, CRM Object, CRM Object Property, **CTA**, Date, Date and Time, Email Address, Embed, File, Followup Email, Font, Form, Gradient, HubDB Row, HubDB Table, Icon, Image, Rich Text, Text, and more.

The **CTA field type** embeds a CTA picker in a custom module — the marketer selects from existing HubSpot CTAs for full tracking.

---

## Checklist Before Delivering

### Email CTAs
- [ ] Using `{% module "cta" path="@hubspot/email_cta" %}` (NOT `{% cta %}` — page-only tag)
- [ ] Module is NOT wrapped in a `<div>` (wrapping hides it in the editor)
- [ ] Centering CSS in non-inlined style block: `#hs_cos_wrapper_cta { text-align: center; }` + `table { margin: 0 auto; }`
- [ ] Brand colors documented for marketer: CTA background, text color, and button radius per `brain/brand-guide/brand-guide.md` (set in Styles tab)
- [ ] Tested CTA renders and is clickable in editor preview

### Landing Page CTAs
- [ ] Using `{% cta %}` for tracked CTA buttons
- [ ] Embedded HTML CTA created with landing page brand CSS
- [ ] Anchor link CTAs (non-tracked) use `.btn-primary` / `.btn-secondary` class
- [ ] Hover state works (primary and secondary hover colors per the brand guide)
- [ ] Responsive — buttons remain tappable on mobile (min 44px touch target)

### CTA Creation (in HubSpot)
- [ ] Created at Marketing > Lead Capture > CTAs
- [ ] Type: Embeds and Buttons > Embedded HTML
- [ ] Link URL set correctly
- [ ] Button content text set
- [ ] brand CSS pasted into Advanced > Custom CSS
- [ ] CTA saved and available in picker

---

## MCP Tools: HubSpot Dev & agent-browser

### HubSpot Dev MCP (Documentation)

Use these tools to look up HubSpot documentation on CTA behavior, module fields, and tracking:

1. **Search docs** — Use `mcp__HubSpotDev__search-docs` to find HubSpot developer documentation on CTA modules, CTA field types, tracking behavior, or the CTA API. Always search before guessing at module behavior or field options.
2. **Fetch doc page** — Use `mcp__HubSpotDev__fetch-doc` immediately after searching to read the full documentation page.
3. **Get feature config schema** — Use `mcp__HubSpotDev__get-feature-config-schema` when building custom CTA modules to verify available field types and configuration options.

**When to use:** When uncertain about CTA module behavior, field types for custom modules, or tracking API details. Always verify against docs rather than guessing.

---

### CTA Rendering Validation

After building templates with CTA buttons, use agent-browser to validate:

1. **Open the template** — Use `agent-browser open <file-path>` to open the email or landing page HTML file.
2. **Screenshot the CTA** — Use `agent-browser screenshot` to capture how the button renders. Verify: the brand guide's CTA background and text colors, button radius, and correct padding.
3. **Test hover state** — Use `agent-browser hover` on the CTA element, then screenshot to verify the hover color changes to the brand guide's hover color.
4. **Test mobile rendering** — Use `agent-browser set viewport 375 812` to mobile width and verify the CTA remains tappable (minimum 44px touch target) and properly sized.
5. **Accessibility check** — Use `agent-browser snapshot -i` to verify the CTA has proper link text (not just "Click here") and is keyboard-accessible.

**When to use:** After building any template with CTA buttons. Validates that brand CSS is applied correctly and the button works at all viewport sizes.

---

## Output Location

Output co-locates with the parent email or landing page template.

---

## Mandatory Skill Delegation

**Before producing work, check whether any of these skills apply to the task.** If they do, load the skill before writing that portion. Do not replicate a skill's logic from memory — load it and apply it.

| When the task involves... | Skill to Load | Mandatory? |
|--------------------------|---------------|-----------|
| Building an email template that contains CTAs | `hubspot-email` | Yes — load for email-specific constraints (table layout, 600px, CAN-SPAM) |
| Building a landing page template that contains CTAs | `hubspot-landing-page` | Yes — load for landing page constraints (full CSS, dnd architecture) |
| CTA button copy (action verbs, urgency, clarity) | `copywriting` | Yes — load before writing CTA copy |
| Visual design decisions beyond what's in the brand guide | `brand-design` | Yes — load for custom visual asset work |
