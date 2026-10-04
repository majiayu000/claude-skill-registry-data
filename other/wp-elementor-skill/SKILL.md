---
name: wordpress-elementor-dev
description: >
  Expert WordPress and Elementor Pro development skill. Use this whenever the user
  asks about WordPress theme development, Elementor Pro customization, plugin architecture,
  custom post types, hooks/filters, Loop Grids, Dynamic Tags, Theme Builder templates,
  off-canvas UIs, custom CSS/JS injection, performance optimization, or any PHP/JS/CSS
  code targeting a WordPress or Elementor environment. Trigger even for general questions
  like "how do I add a custom field in Elementor", "what hook should I use for X in
  WordPress", "how do I override a WooCommerce template", or "how do I register a
  custom widget" — do not wait for the user to explicitly say "use the skill."
  Also trigger for ACF integration, REST API endpoints, child theme setup, WooCommerce
  customization, WPML/multilingual setups, and any debugging of WordPress/Elementor issues.
---

# WordPress & Elementor Pro — Skill Router

A complete procedural guide for producing production-grade WordPress and Elementor Pro
code. This file is the **router** — read it first, then load the relevant sub-file(s)
for the task at hand.

---

## Sub-file Map — Read the Right File for Each Task

| Task type | Read this file |
|---|---|
| Plugin scaffold, child theme, code placement, CPT, AJAX handler | **scaffolding.md** |
| PHP standards, sanitization, escaping, nonces, WP_Error, transients, password hashing | **php-standards.md** |
| JavaScript standards, enqueue API, defer/async, wp_add_inline_script | **js-css-standards.md** |
| CSS standards, BEM, design tokens, Elementor CSS selectors | **js-css-standards.md** |
| Elementor custom widget, Dynamic Tags, Loop Grid, Form actions, Theme Builder conditions | **elementor-patterns.md** |
| Elementor extension points — custom **form fields**, **theme locations**, injecting controls into native widgets, **adding a TAB to the editor's Elements panel**, Finder/context-menu, hooks reference, deprecations | **elementor-extending.md** |
| WooCommerce HPOS, order API, template overrides, Loop Grid for products | **woocommerce.md** |
| REST API endpoints, schema, permission callbacks | **rest-api.md** |
| Off-canvas UI, off-canvas accessibility, focus trap | **offcanvas-ui.md** |
| Performance checklists (frontend + backend), speculative loading, IE conditional comments | **performance.md** |
| Accessibility checklist, WCAG 2.2 AA, ARIA patterns | **performance.md** |
| **Hard-won production gotchas** — widget lifecycle fatals, `content_template()` escaping, CSS-in-Elementor footguns, transactional email, wp.org review/packaging, embedding apps, AJAX/loop re-rendering, dynamic CSS in loops, Swiper on optimised sites, holding a login without counting it as failed | **field-notes.md** |
| **wordpress.org submission** — the 18 Directory Guidelines, Plugin Check 2.1.0 categories/usage, review process, required headers/readme | **wp-org-guidelines.md** |
| **Subversion (SVN)** — deploying/tagging a release on the wordpress.org plugin/theme SVN (trunk/tags/assets), the daily work cycle, branching/merging, properties, repo admin | **svn/svn.md** (self-contained sub-bundle; `svn/references/` goes deeper) |
| **Debugging & static analysis** — PHPCS+WPCS, PHPStan, Plugin Check, `WP_DEBUG`/Query Monitor, Elementor Safe Mode/cache, symptom→cause table | **debugging.md** |
| **Common WordPress APIs** — admin settings page (Settings + Options API), `register_meta`, roles/capabilities, WP-Cron, internationalization (i18n) | **wordpress-apis.md** |
| **Database layer (MariaDB/MySQL)** — custom tables + `dbDelta()`, charsets & the `varchar(191)` index rule, indexes, `EXPLAIN`, MariaDB↔MySQL portability, `sql_mode`, full-text | **mariadb.md** |

### Widget Boilerplates — Load when building a widget of that type

| Widget type | Read this file |
|---|---|
| Button / CTA with icon and link | **widget-button.md** |
| Container / layout wrapper / section / card shell | **widget-container.md** |
| Image with caption, link, lightbox | **widget-image.md** |
| Heading / title / HTML tag selector | **widget-heading.md** |
| Rich text / WYSIWYG body content | **widget-text-editor.md** |
| Video embed (YouTube, Vimeo, self-hosted) | **widget-video.md** |
| Widget that renders a saved Elementor template by ID | **widget-elementor-template.md** (SELECT2, `get_builder_content_for_display()`, Dynamic Tags context, CSS timing) |
| Widget whose markup lives in a separate PHP template file | **widget-php-template.md** (Strategies A/B/C, `load_template()`, `ob_start`, path-traversal safety) |
| Divider / horizontal rule with optional text or icon | **widget-divider.md** |
| Spacer / vertical gap | **widget-spacer.md** |
| Single standalone icon with optional link | **widget-icon.md** |
| Icon + title + description box | **widget-icon-box.md** |
| Image + title + description box | **widget-image-box.md** |
| Image grid / gallery | **widget-image-gallery.md** |
| Image slider / carousel | **widget-image-carousel.md** |
| Bullet list with icons per item | **widget-icon-list.md** |
| Animated number counter | **widget-counter.md** |
| Percentage progress bar | **widget-progress.md** |
| Customer quote / testimonial | **widget-testimonial.md** |
| Tabbed content panels | **widget-tabs.md** |
| Accordion — one panel open at a time | **widget-accordion.md** |
| Toggle — multiple panels open simultaneously | **widget-toggle.md** |
| Social media icon links row | **widget-social-icons.md** |
| Colored alert / notice box | **widget-alert.md** |
| Audio player (SoundCloud / self-hosted) | **widget-audio.md** |
| WordPress shortcode output | **widget-shortcode.md** |
| Raw custom HTML / JS / CSS embed | **widget-html.md** |
| Named anchor for in-page navigation | **widget-menu-anchor.md** |
| WordPress registered sidebar output | **widget-sidebar.md** |
| WordPress <!--more--> read more tag | **widget-read-more.md** |
| Google Maps embed | **widget-google-maps.md** |
| Decorative star rating display | **widget-star-rating.md** |
| Schema-ready structured rating | **widget-rating.md** |
| Text following a curved / custom SVG path | **widget-text-path.md** |
| Nested Tabs / Nested Accordion (each panel is a Container holding any widgets) | **widget-nested.md** |

**Always read the relevant sub-file before writing code.** For tasks that span multiple
areas (e.g. a WooCommerce widget with custom REST endpoint), read all relevant sub-files.
For a widget task, read BOTH the widget boilerplate file AND **elementor-patterns.md**.
For **any custom widget, plugin, or wp.org-bound work, also skim `field-notes.md`** — it
catches the lint-passing, review-failing, site-down mistakes the topic files don't dwell on.

---

## 0. Golden Rules (Never Violate)

These override everything in all sub-files:

1. **Native APIs first** — WordPress core hook before plugin; Elementor API before template override.
2. **Sanitize in, escape out** — Every input sanitized. Every output escaped. No exceptions.
3. **Prefix everything** — All functions, classes, constants, hooks, and CSS classes use a project-specific prefix.
4. **State your placement** — Every code response must declare exactly where the code lives.
5. **No over-clarifying** — Only ask a clarification question if the missing info would materially change the code output. Otherwise, state your assumption and proceed.
6. **NEVER hardcode visual settings in widgets** — Every visual property (colors, fonts, sizes,
   spacing, backgrounds, borders, shadows, alignment) MUST be exposed as a standard Elementor
   control in the editor panel. Users control appearance via the toolbar — not by editing code.
   See §5 "Mandatory Widget Controls" below for the required controls checklist.
7. **Name for the directory from day one** — Naming is decided first and is effectively
   irreversible, so get it right before writing code. The plugin **slug/name must NOT start with
   a trademark you don't own** — `"CRM for WooCommerce"`, never `"WooCommerce CRM"` (Directory
   Guideline 17). The **text domain must exactly equal the plugin slug**. The wp.org slug is
   **permanent**, and a widget's `get_name()` is **sticky** (stored in every page's
   `_elementor_data` — renaming it breaks placed widgets). Choose the public name, slug, text
   domain, and code prefix (Rule #3) **together, once**. This is distinct from Rule #3: that
   governs internal code symbols; this governs the public identity. See **wp-org-guidelines.md**
   (Guidelines 12/16/17) and **field-notes.md** §1 (sticky `get_name()`).

---

## 1. Default Assumptions

Quickly assess — **only ask if the answer would change the code**:

| Info needed | Ask only if... |
|---|---|
| Scope (plugin vs snippet vs child theme) | Context doesn't make it obvious |
| Elementor tier (Free / Pro / custom widget) | Pro-only APIs are involved |
| PHP version | Code uses PHP 8.3+ features like typed class constants, or 8.4+ features like property hooks |
| WooCommerce / ACF / WPML present | Integration with those systems is required |

**Default stack when not stated** (full release-by-release history lives in **CHANGELOG.md** — keep volatile version-tracking out of this router):

| Component | Version | Notes |
|---|---|---|
| **WordPress** | **7.1** | **"Mary Lou", released Aug 19, 2026** (7.0 "Armstrong" was May 20; the 7.0 branch ended at 7.0.4, Aug 12). Minimum PHP **7.4** (7.2/7.3 dropped — sites still on them stay pinned to 6.9.x). No multisite assumed. **7.1 makes the post editor iframe unconditional — see below.** |
| **PHP** | **8.3** recommended | 7.4 = minimum. 8.4 / 8.5 = "beta support" (possible deprecation notices). 8.2 fully compatible but no longer the recommended default. |
| **Elementor (free + Pro)** | **4.2+** | Separate plugins with **independent version numbers** — currently **free 4.2.3 / Pro 4.2.2** (both Aug 19, 2026). 4.0.0 (Mar 30, 2026) made the Atomic Editor stable + default for new installs; 4.2.0 (Jul 20) added Atomic Grid (free) and Atomic Loop (Pro). ⚠️ Elementor's header still reads **"Tested up to: 7.0.4"** — it has **not** declared WP 7.1 support. **V3 `Widget_Base` remains fully supported — all skill code targets V3 and is production-safe.** |
| **WooCommerce** | **11.0+** | **11.0 (Aug 4, 2026) REMOVED the product editor beta** and bumped to **Action Scheduler 4.0.0** (breaking dedup change). HPOS default-on since 8.2; 10.7 disabled HPOS "sync on read"; 10.9 defers Store API draft-order creation — see woocommerce.md. |

**Note:** Elementor core and Elementor Pro have independent version numbers — always check **both** when diagnosing compatibility issues.

### WordPress 7.1 — what changed for plugin / Elementor devs

WP 7.1 **"Mary Lou"** shipped **August 19, 2026** (WordCamp US). Unlike 7.0, this release
contains **four changes that can break a shipped plugin** — they are listed first. No PHP or
WordPress minimum changed.

**🔴 Breaking — audit your plugin for these:**

1. **The post editor is now ALWAYS in an iframe** — including on sites registering legacy meta
   boxes, which was the last remaining escape hatch. Editor JavaScript that reaches for the
   global `document` / `window` now targets the **wrong document**. Use the canvas element's
   **`ownerDocument`** and **`defaultView`** instead:
   ```js
   // ❌ breaks in 7.1 — this is the OUTER document, not the editor canvas
   document.querySelector( '.my-block' ).classList.add( 'ready' );

   // ✅ resolve the document from a node you already own inside the canvas
   const doc  = myCanvasNode.ownerDocument;
   const view = doc.defaultView;                   // the iframe's `window`
   doc.querySelector( '.my-block' )?.classList.add( 'ready' );
   view.requestAnimationFrame( … );
   ```
   Injected `<style>`/`<link>` must go into the **canvas** document too, or it styles nothing.
   **Elementor's own editor is unaffected** (it is not the block editor) — this hits block
   registrations, meta boxes, and any block-editor integration your plugin ships.
2. **`__next40pxDefaultSize` is now a no-op** on `@wordpress/components` — **remove the prop**
   entirely; there is no replacement. Form controls render at 40px unconditionally.
3. **List-table markup changed:** the row header moved from the checkbox column to the **title**
   column. Any CSS/JS selector keyed on `th.check-column` (or assuming the row header's position)
   breaks — audit custom admin list tables and column callbacks.
4. **jQuery UI updated to 1.14.2.** Test anything depending on jQuery UI behaviour or styling.

**🟢 New and useful:**

- **SVG Icon API** (public in 7.1) — register icons and whole collections, render server-side,
  read over REST: `wp_register_icon_collection()`, `wp_register_icon()`, `wp_get_icon()`.
  ⚠️ SVGs pass through a **conservative allowlist — only `<svg>`, `<path>` and `<polygon>` survive**.
  A `<g>`, `<circle>`, `<rect>` or `<use>` in your icon is stripped silently, so convert shapes to
  paths before registering. (This is a *core* API — Elementor widgets still ship their own SVGs;
  see `elementor-extending.md` §8 and the "don't `wp_kses()` inline SVG" rule in `field-notes.md` §6.)
- **Abilities API matured:** `wp_get_abilities()` filtering, **execution-lifecycle hooks**, custom
  validation, a unified `public` exposure flag, and client-compatible JSON-Schema preparation.
  Registration timing rules from 7.0 are unchanged (see the 7.0 section below).
- **Global Styles / `theme.json`:** responsive style variations with **configurable breakpoints**,
  pseudo-state styling (`:hover` / `:focus` / `:active`), and `text-shadow` support.
- **Media:** client-side image processing in the browser via **WebAssembly** (compression/resizing
  no longer hit the server), infinite scroll in the Media Library, and registration of multiple
  image sizes at once. Multisite now enforces upload limits on **media sideloading**.
- **Persistent admin bar** across editor screens — review any custom toolbar nodes for behaviour
  in the editor context.
- **Design System:** semantic design tokens for theming admin UI (relevant if you build admin or
  editor panels — compare the Elementor panel tokens in `elementor-extending.md` §5).
- **DataViews / DataForm** APIs matured for data-driven admin interfaces.
- **React stays on 18.3** — React 19 was deferred again. Don't bundle `react/jsx-runtime`
  yourself, and avoid string refs / `defaultProps`, which fail under the experimental React 19 flag.
- Conditional block-CSS loading can affect **remote content pulls** — verify if you render blocks
  outside a normal page request.

_Sources: wordpress.org/news/2026/08/mary-lou/ · make.wordpress.org/core/2026/08/05/wordpress-7-1-field-guide/ ·
developer.wordpress.org/news/2026/08/whats-new-for-developers-august-2026/_

### WordPress 7.0 — what changed for plugin / Elementor devs

WP 7.0 "Armstrong" shipped **May 20, 2026** (delayed from the original April 9 target while
the RTC storage layer was redesigned — see below). Everything below is **opt-in and
non-breaking**; most plugin/Elementor work is unaffected. It remains relevant because 7.1
changed none of it.

- **Minimum PHP is now 7.4** (7.2/7.3 dropped). The skill's recommended baseline stays
  **PHP 8.3**. Bump your plugin's `Requires PHP` header to 7.4 only once you target WP 7.0+
  exclusively. No new DB minimum is enforced; `wordpress.org/about/requirements/` recommends
  **MariaDB 10.11+ or MySQL 8.0+** (the MariaDB floor was raised from 10.6; re-verified Aug 2026).
- **Real-Time Collaboration (RTC):** simultaneous multi-author block editing (CRDT-based, via
  an HTTP-polling sync provider — not WebRTC). Data is stored in a **dedicated core database
  table**; an earlier `wp_post_meta` / `wp_sync_storage` design was rejected, and building the
  table is what pushed the release from April to May. **Plugin impact:** scope every
  `WP_Query` / `get_posts()` with an explicit `post_type` so internal core post types never
  leak into your results — do **not** hardcode any internal RTC type name. The
  `WP_ALLOW_COLLABORATION` constant lets hosts swap the sync transport.
- **WP AI Client:** provider-agnostic PHP + JS AI API — `wp_ai_client_prompt( $prompt )->generate_text()`.
  Guard with `function_exists( 'wp_ai_client_prompt' )`.
- **Abilities API:** `wp_register_ability()` (PHP, since WP 6.9) plus a JS counterpart in 7.0.
  Use `'meta' => ['show_in_rest' => true]` to expose via REST. Register ONLY inside the
  **`wp_abilities_api_init`** hook (core renamed the feature plugin's `abilities_api_init`;
  categories go on `wp_abilities_api_categories_init`) or you get `_doing_it_wrong`; a
  `category` is required and must already be registered. Calling it also sets your real
  `Requires at least` floor to **6.9** — Plugin Check errors on the header and
  `function_exists()` guards don't count (see `debugging.md` §1).
- **Connectors UI** (Settings → Connectors) for managing AI provider credentials, and a
  **Command Palette** in wp-admin.
- **Iframed editor** was still conditional in 7.0 — **7.1 makes it unconditional.** See the 7.1
  section above; `"apiVersion": 3` in `block.json` is now table stakes, not preparation.

_Sources: make.wordpress.org/core/2026/01/09/dropping-support-for-php-7-2-and-7-3/ ·
make.wordpress.org/core/2026/04/22/wordpress-7-0-release-party-updated-schedule/ ·
wordpress.org/about/requirements/_

> 📌 **PHP support labels (unchanged in WP 7.1):** PHP 7.4–8.3 fully compatible; **8.3 recommended**;
> 8.4 (WP 6.7+) and 8.5 (WP 6.9+) carry a "beta support" label (possible deprecation notices).
> Source: make.wordpress.org/core/handbook/references/php-compatibility-and-wordpress-versions/

> ✅ **Elementor 4.x status (current: free 4.2.3 / Pro 4.2.2, both Aug 19, 2026):** Elementor
> 4.0.0 (Mar 30, 2026, free + Pro) made the **Atomic Editor stable and the default for new
> installs** and added Atomic Forms, Pro Interactions, and Component creation. Updating to 4.x
> leaves **existing sites untouched** — V3 widgets and V4 Atomic Elements coexist on the same
> page; Atomic features are toggled at WP Admin → Elementor → Editor → Settings.
>
> **There is still NO third-party API for building Atomic Elements, and Elementor has said so
> explicitly** — they will not release one soon and *advise against* integrating with Atomic
> internals until they announce it (elementor/elementor GitHub Discussion #32950). Atomic
> Elements are documented only as a **data structure**
> (developers.elementor.com/docs/data-structure/atomic-elements). So **continue using V3
> `Widget_Base`** for all third-party widgets — it is the correct, production-safe API and all
> skill code targets it. *(Re-verified Aug 23, 2026 — unchanged since the July check.)*
>
> ⚠️ **Elementor has not declared WP 7.1 compatibility yet.** As of free 4.2.3 / Pro 4.2.2 the
> `Tested up to` header reads **7.0.4**, three days after WP 7.1 shipped. That is normal lag,
> not a known incompatibility — but when a client reports editor breakage on a fresh 7.1 site,
> check Elementor's current `Tested up to` before debugging your own code.
>
> **V4 Atomic Elements that now ship by default (awareness only — not third-party-buildable yet):**
> Div Block & Flexbox Container (layout); **Atomic Grid** — advanced row/column layouts (free
> 4.2.0, Jul 20, 2026); Atomic Heading, Paragraph, Image, Button, Video, SVG;
> **Atomic Tabs**; **Atomic Forms** (Pro) with composable fields — Label, Input, Textarea,
> Checkbox, Submit, plus Radio, Select, Date Picker, Time Picker, and File Upload (added in
> Pro 4.1.0, May 26, 2026); and **Atomic Loop** — dynamic content layouts, the V4 counterpart
> of the Pro Loop Grid (Pro 4.2.0, Jul 20, 2026). These are end-user elements; building
> **custom** atomic elements still awaits the finalized V4 extension docs — keep targeting V3
> `Widget_Base` until then.
> Source: elementor.com/products/website-builder/v4-faq/ ·
> developers.elementor.com/elementor-editor-4-0-developers-update/ ·
> elementor.com/pro/changelog/ · github.com/elementor/elementor/releases

> 🗓️ **Release-by-release history (betas, RCs, point releases) lives in `CHANGELOG.md`.**
> Keep this router focused on durable guidance; update version facts in the table above
> and in `CHANGELOG.md`, not scattered across the sub-files.
---

## 2. Architecture Decision Tree

Run through this mentally before writing a single line:

```
Does a WordPress core hook (add_action/add_filter) solve it?
  YES → Use the hook. No plugin needed. Place in child theme functions.php
        or Elementor Custom Code.
  NO  → Does Elementor's PHP/JS API solve it?
          YES → Extend via Elementor hooks, Dynamic Tags, or Widget_Base.
                Register via elementor/widgets/register or elementor/dynamic_tags/register.
          NO  → Is this logic reusable across themes or sites?
                  YES → Scaffold a dedicated plugin (see scaffolding.md).
                  NO  → Child theme functions.php or Elementor Custom Code block.

Is a WooCommerce override needed?
  → Use Elementor Loop Grid + custom query filter BEFORE touching template files.
  → Only override woocommerce/ templates as an absolute last resort.

Is this a REST API endpoint?
  → Always register via register_rest_route() inside a plugin, never in functions.php.
```

---

## 3. Mandatory Output Format

**Every single code response must follow this structure — no exceptions:**

```
📍 PLACEMENT
Exact file path or Elementor hook location.
e.g. /wp-content/plugins/myplugin/includes/class-myplugin-hooks.php
     Elementor → Site Settings → Custom Code → wp_footer

⚙️ REQUIRES
WordPress X.X+ | PHP X.X+ | Elementor Pro X.X+ | ACF X.X+ | WooCommerce X.X+
(list only what the code actually depends on)

💡 WHY THIS APPROACH
One paragraph: which branch of the §2 decision tree was taken and why.

📋 CODE
Complete, commented, deployment-ready code block — no truncation, no omissions.

🔧 INTEGRATION NOTES (include when relevant)
Any manual steps required: flush rewrite rules, set Query ID in Elementor editor,
activate plugin, clear Elementor cache, etc.
```

---

## 4. Quick Reference — Pattern Index

| Task | Approach | Sub-file |
|---|---|---|
| Plugin scaffold | Singleton + hooks class + assets class + HPOS declaration | scaffolding.md |
| Child theme setup | `wp_enqueue_style` parent + child in functions.php | scaffolding.md |
| Custom Post Type + Taxonomy | `register_post_type()` + `register_taxonomy()` in plugin | scaffolding.md |
| Secure AJAX handler | `wp_ajax_` hooks + nonce verify + `wp_send_json_*` | scaffolding.md |
| PHP sanitization / escaping | `wp_unslash()` + `sanitize_*` + `esc_*` patterns | php-standards.md |
| Transient caching | `get_transient` / `set_transient` | php-standards.md |
| External API call + WP_Error | `wp_remote_get()` + `WP_Error` pattern | php-standards.md |
| Admin settings page | Settings API + `register_setting` + `sanitize_callback` + `settings_fields` | wordpress-apis.md |
| Store plugin options | Options API + explicit boolean `autoload` (WP 6.6+) | wordpress-apis.md |
| Custom field exposed to REST / Elementor | `register_post_meta` + `show_in_rest` | wordpress-apis.md |
| Scheduled / background task | WP-Cron (`wp_schedule_event`) + Action Scheduler for heavy jobs | wordpress-apis.md |
| Create a custom DB table | `dbDelta()` + `$wpdb->prefix` + `get_charset_collate()`; strict formatting rules | mariadb.md |
| "Specified key was too long" / emoji not saving | `utf8mb4` + index string columns at **`varchar(191)`** | mariadb.md |
| Slow query / missing index | `EXPLAIN` (`type: ALL`, `key: NULL`, `Using filesort`) + leftmost-prefix rule | mariadb.md |
| SQL that must run on MariaDB **and** MySQL | Plain standard SQL; JSON is stored/compared differently — don't query inside it | mariadb.md |
| Make a plugin translatable | i18n functions + text-domain = slug + WP 6.7 `init`-timing rule | wordpress-apis.md |
| Ship a translation for a wp.org-hosted plugin | `.pot` only in the zip; translate.wordpress.org → language packs (90% gate). **Never** bundle `.mo` / call `load_plugin_textdomain()` | wordpress-apis.md |
| Style UI text for non-Latin locales | Caseless scripts + `text-transform`/`letter-spacing`; don't size to English string length | js-css-standards.md |
| Test that translations actually load | Set the site locale before bootstrap; `unload_textdomain()` in WP-CLI; validate placeholders | debugging.md |
| Deploy / tag a plugin release on wp.org SVN | `svn co` → copy to `trunk/` → `svn cp trunk tags/X.Y.Z` → `svn ci` (assets/ is a sibling) | svn/svn.md |
| Any SVN task (checkout, commit, branch, merge, conflicts, repo admin) | Subversion sub-bundle | svn/svn.md |
| WP 6.8 password hashing | `wp_check_password()` + `wp_password_needs_rehash()` | php-standards.md |
| WP 6.8 app password / key hashing | `wp_fast_hash()` + `wp_verify_fast_hash()` (BLAKE2b) | php-standards.md |
| JS standards + enqueue defer/async | IIFE + WP 6.3+ enqueue API | js-css-standards.md |
| PHP → JS data passing | `wp_add_inline_script()` with `wp_json_encode()` | js-css-standards.md |
| CSS BEM + design tokens | Scoped tokens, 8pt spacing, fluid type | js-css-standards.md |
| Custom Elementor widget | `Widget_Base` + all required methods | elementor-patterns.md |
| Elementor Dynamic Tag | `Tag` class + `elementor/dynamic_tags/register` | elementor-patterns.md |
| Elementor Loop Grid query | `elementor/query/` filter | elementor-patterns.md |
| ACF field in Elementor | Dynamic Tag extending `\Elementor\Core\DynamicTags\Tag` | elementor-patterns.md |
| Elementor Pro Form action | `Action_Base` + field iteration | elementor-patterns.md |
| Theme Builder custom condition | `Condition_Base` + `elementor/theme/register_conditions` | elementor-patterns.md |
| Elementor Pro custom form field | `Field_Base` + `elementor_pro/forms/fields/register` | elementor-extending.md |
| Theme Builder custom location | `register_location` + `elementor_theme_do_location()` | elementor-extending.md |
| Add a control to a NATIVE Elementor widget | `elementor/element/{el}/{section}/before_section_end` | elementor-extending.md |
| Filter a native widget's output | `elementor/widget/render_content` filter | elementor-extending.md |
| Add a TAB to the editor panel (like an SEO plugin) | `elementorV2.editorElementsPanel.injectTab()` + `elementor/editor/before_enqueue_scripts` | elementor-extending.md |
| WooCommerce HPOS compatibility | `FeaturesUtil::declare_compatibility()` + `wc_get_order()` | woocommerce.md |
| WooCommerce loop | Loop Grid + `elementor/query/` filter | woocommerce.md |
| Custom REST endpoint | `register_rest_route()` + schema callback in plugin | rest-api.md |
| Off-canvas filter panel | BEM CSS + ARIA JS + Custom Code block | offcanvas-ui.md |
| Performance checklist | Frontend + backend checklists | performance.md |
| Accessibility checklist | WCAG 2.2 AA patterns | performance.md |
| Elementor dependency check | `Requires Plugins: elementor` header + `did_action` fallback | scaffolding.md |
| Widget with button/CTA | Controls + render matching native Button widget | widget-button.md |
| Widget with container/layout | Controls + render matching native Container | widget-container.md |
| Widget with image | `Group_Control_Image_Size` + `get_attachment_image_html()` | widget-image.md |
| Widget with heading | TEXTAREA + header_size tag selector | widget-heading.md |
| Widget with rich text | WYSIWYG + wp_kses_post output | widget-text-editor.md |
| Widget with video embed | Source SELECT + overlay + aspect ratio | widget-video.md |
| Widget rendering saved Elementor template | get_builder_content_for_display() + SELECT2 | widget-elementor-template.md |
| Widget with PHP template file | load_template() + locate_template() strategies A/B/C | widget-php-template.md |
| Widget with divider line | Style + width + optional text/icon element | widget-divider.md |
| Widget with spacer gap | Single responsive SLIDER | widget-spacer.md |
| Widget with single icon | ICONS control + size + color tabs | widget-icon.md |
| Widget with icon + text box | Icon + title + description pattern | widget-icon-box.md |
| Widget with image + text box | Image + title + description pattern | widget-image-box.md |
| Widget with image grid | GALLERY control + Group_Control_Image_Size | widget-image-gallery.md |
| Widget with image slider | GALLERY + Swiper + navigation controls | widget-image-carousel.md |
| Widget with icon bullet list | REPEATER + icon + text + optional link | widget-icon-list.md |
| Widget with animated counter | Number + prefix/suffix + duration | widget-counter.md |
| Widget with progress bar | Percentage SLIDER + bar styling | widget-progress.md |
| Widget with testimonial quote | Content + image + name + job title | widget-testimonial.md |
| Widget with tabbed panels | REPEATER tabs + horizontal/vertical type | widget-tabs.md |
| Widget with accordion | REPEATER + single-open collapse pattern | widget-accordion.md |
| Widget with toggle panels | REPEATER + multi-open toggle pattern | widget-toggle.md |
| Widget with social icons | REPEATER + brand icons + links | widget-social-icons.md |
| Widget with alert/notice box | Type SELECT + title + description + dismiss | widget-alert.md |
| Widget with audio player | SoundCloud URL + autoplay options | widget-audio.md |
| Widget outputting shortcode | TEXTAREA + do_shortcode() | widget-shortcode.md |
| Widget with raw HTML embed | CODE control + unescaped output | widget-html.md |
| Widget as named anchor | TEXT ID + sanitize_html_class() | widget-menu-anchor.md |
| Widget outputting sidebar | Registered sidebar SELECT + dynamic_sidebar() | widget-sidebar.md |
| Widget with read more tag | No controls — WordPress $more global | widget-read-more.md |
| Widget with Google Maps | Address TEXT + zoom SLIDER + iframe | widget-google-maps.md |
| Widget with star rating display | Scale + rating number + icon style | widget-star-rating.md |
| Widget with schema rating | Icon count + fractional rating + gap | widget-rating.md |
| Widget with curved/path text | `<svg>` + `<textPath>` + unique path id | widget-text-path.md |
| Nested Tabs / Accordion widget | `Widget_Nested_Base` + `print_child()` + container panels | widget-nested.md |

---

## 5. Mandatory Widget Controls — No Hardcoded Visuals (NEVER VIOLATE)

> **This section is MANDATORY for every custom Elementor widget.** Whenever you build a widget,
> every visual property must be an Elementor control — NEVER a hardcoded CSS value. Users
> control appearance from the editor panel/toolbar, not by editing source code.

### The Rule

**NEVER hardcode** any of the following in PHP `render()`, in static CSS, or in
`content_template()` output:

- Colors (text, background, border, shadow)
- Typography (font family, size, weight, line-height, letter-spacing, transform)
- Spacing (padding, margin, gap)
- Sizing (width, height, min/max values)
- Borders (style, width, color, radius)
- Shadows (box-shadow, text-shadow)
- Backgrounds (color, gradient, image)
- Alignment / positioning
- Opacity, transitions, hover effects

**ALL** of the above must use Elementor controls with `selectors` that inject CSS dynamically.
The only exceptions are structural CSS (display, position, overflow) required for the widget
layout to function at all — and even these should use controls when there is a user-facing
choice (e.g. flex-direction toggle).

> ⚠️ **"No hardcoded visuals" does NOT mean "put a `default` on every control."**
> Elementor emits a `default` exactly like a user-set value, so a colour default paints on every
> install and clearing the swatch only restores it — the user cannot turn it off. **Elementor core
> carries no `default` on colour controls at all** (`includes/widgets/heading.php`: `title_color`
> uses a `'global'` reference; `title_hover_color` is entirely empty). Follow that split:
> - **Sizes, spacing, alignment, toggles, tags, labels** → give a real `'default'`.
> - **Colours** → leave empty. Put the resting look in your stylesheet's `var(--token, fallback)`
>   and let the control override it. For **state** colours (hover / active / selected / current)
>   also write a **direct CSS property**, never a custom property, and keep that state
>   **colour-free in your CSS** — otherwise "empty" still paints the fallback.
>
> See `field-notes.md` §4 for the full trap, plus the theme-specificity and `accent-color` cases.

### Required Controls Checklist — Apply to Every Widget

When building a widget, include ALL controls that apply to its visual elements.
Use this checklist as a mandatory gate:

| Visual property | Required Elementor control | Tab |
|---|---|---|
| **Text content** | `TEXT`, `TEXTAREA`, or `WYSIWYG` + `'dynamic' => ['active' => true]` | TAB_CONTENT |
| **Typography** (any text element) | `add_group_control( Group_Control_Typography::get_type() )` | TAB_STYLE |
| **Text color** | `COLOR` control with `selectors` | TAB_STYLE |
| **Text alignment** | `add_responsive_control()` with `CHOOSE` (left/center/right/justify) | TAB_STYLE or TAB_CONTENT |
| **Background** | `add_group_control( Group_Control_Background::get_type() )` | TAB_STYLE |
| **Border** | `add_group_control( Group_Control_Border::get_type() )` | TAB_STYLE |
| **Border radius** | `add_responsive_control()` with `DIMENSIONS` + `'selectors'` | TAB_STYLE |
| **Box shadow** | `add_group_control( Group_Control_Box_Shadow::get_type() )` | TAB_STYLE |
| **Text shadow** | `add_group_control( Group_Control_Text_Shadow::get_type() )` | TAB_STYLE |
| **Padding** | `add_responsive_control()` with `DIMENSIONS` | TAB_STYLE |
| **Margin** | `add_responsive_control()` with `DIMENSIONS` | TAB_STYLE |
| **Width / Height** | `add_responsive_control()` with `SLIDER` | TAB_STYLE |
| **Spacing / Gap** | `add_responsive_control()` with `SLIDER` | TAB_STYLE |
| **Image** | `MEDIA` + `add_group_control( Group_Control_Image_Size::get_type() )` | TAB_CONTENT |
| **CSS Filters** (if image/element) | `add_group_control( Group_Control_Css_Filter::get_type() )` | TAB_STYLE |
| **Hover state** | Duplicate color/background/shadow controls inside `'section_style_hover'` with `selectors` targeting `:hover` | TAB_STYLE |
| **Transition duration** | `SLIDER` (seconds) with `selectors => ['transition-duration']` | TAB_STYLE |
| **Link** | `URL` control with `'dynamic' => ['active' => true]` | TAB_CONTENT |
| **Icon** | `ICONS` control with `fa4compatibility` | TAB_CONTENT |
| **HTML tag** | `SELECT` (h1–h6, div, span, p) | TAB_CONTENT |

### Example — Correct vs Incorrect

```php
// ❌ WRONG — hardcoded color and font-size
protected function render(): void {
    $settings = $this->get_settings_for_display();
    echo '<h2 style="color: #e94560; font-size: 24px;">'
        . esc_html( $settings['title'] ) . '</h2>';
}

// ✅ CORRECT — all visuals controlled from the panel via selectors
protected function register_controls(): void {
    // ... Content section with title TEXT control ...

    $this->start_controls_section( 'section_title_style', [
        'label' => esc_html__( 'Title Style', 'myplugin' ),
        'tab'   => \Elementor\Controls_Manager::TAB_STYLE,
    ] );

    $this->add_control( 'title_color', [
        'label'     => esc_html__( 'Color', 'myplugin' ),
        'type'      => \Elementor\Controls_Manager::COLOR,
        'selectors' => [
            '{{WRAPPER}} .myplugin-widget__title' => 'color: {{VALUE}};',
        ],
    ] );

    $this->add_group_control(
        \Elementor\Group_Control_Typography::get_type(),
        [
            'name'     => 'title_typography',
            'selector' => '{{WRAPPER}} .myplugin-widget__title',
        ]
    );

    $this->add_responsive_control( 'title_align', [
        'label'   => esc_html__( 'Alignment', 'myplugin' ),
        'type'    => \Elementor\Controls_Manager::CHOOSE,
        'options' => [
            'left'   => [ 'title' => esc_html__( 'Left',   'myplugin' ), 'icon' => 'eicon-text-align-left' ],
            'center' => [ 'title' => esc_html__( 'Center', 'myplugin' ), 'icon' => 'eicon-text-align-center' ],
            'right'  => [ 'title' => esc_html__( 'Right',  'myplugin' ), 'icon' => 'eicon-text-align-right' ],
        ],
        'selectors' => [
            '{{WRAPPER}} .myplugin-widget__title' => 'text-align: {{VALUE}};',
        ],
    ] );

    $this->add_responsive_control( 'title_spacing', [
        'label'      => esc_html__( 'Bottom Spacing', 'myplugin' ),
        'type'       => \Elementor\Controls_Manager::SLIDER,
        'size_units' => [ 'px', 'em', 'rem' ],
        'range'      => [ 'px' => [ 'min' => 0, 'max' => 100 ] ],
        'selectors'  => [
            '{{WRAPPER}} .myplugin-widget__title' => 'margin-bottom: {{SIZE}}{{UNIT}};',
        ],
    ] );

    $this->end_controls_section();
}

protected function render(): void {
    $settings = $this->get_settings_for_display();
    // ✅ No inline styles — all visuals come from Elementor's selectors
    $this->add_render_attribute( 'title', 'class', 'myplugin-widget__title' );
    $this->add_inline_editing_attributes( 'title' );
    echo '<h2 ' . $this->get_render_attribute_string( 'title' ) . '>'
        . esc_html( $settings['title'] ) . '</h2>';
}
```

### `add_render_attribute()` and `add_inline_editing_attributes()` — Always Use

The official Elementor API for building HTML attributes is `$this->add_render_attribute()`.
**Always use it** instead of manually concatenating class/id/aria attributes in `render()`.
Pair with `$this->add_inline_editing_attributes()` for any text field that supports live
editing in the Elementor editor panel.

**Outputting the built attributes — pick by context:** use
`get_render_attribute_string( 'key' )` when you are concatenating into a string (as in the
`echo '<h2 ' . ... . '>'` example above), and `print_render_attribute_string( 'key' )` when
you are echoing directly inside a `?> … <?php` HTML block (e.g.
`<h2 <?php $this->print_render_attribute_string( 'title' ); ?>>`). Both are correct Elementor
APIs — `print_*` simply echoes what `get_*` returns. The widget sub-files use the `print_*`
form inside their HTML templates.

Source: developers.elementor.com/docs/widgets/rendering-html-attribute/
Source: developers.elementor.com/docs/widgets/rendering-inline-editing/
