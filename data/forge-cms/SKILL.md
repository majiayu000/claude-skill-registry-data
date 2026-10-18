---
name: forge-cms
description: "Forge: CMS work — WordPress and headless CMS: CMS, WordPress, theme, plugin, custom post type, WP-CLI, Contentful, Sanity, Strapi, Payload, content model."
---

# Forge playbook — CMS (WordPress · headless)

A CMS is a **content-model + editor-safety + migration domain** sitting on top of a live database and uploads. The rendered front-end defers to `forge-website` (real content, responsive, a11y, SEO, performance); the API/secret/webhook plumbing defers to `forge-integration`; this file governs the content model, the CMS-specific attack surface, and migration/backup safety. The single most important rule is **back up before you change anything** — CMS mistakes hit live content and are often irreversible without a backup. **Honest limit:** Forge cannot run a live WordPress/MySQL install or take a real DB/uploads backup unless the environment provides PHP + MySQL + WP-CLI (opt-in, owner-side) — mark those steps not-run when the runtime is absent.

## Hard rules (non-negotiable)
- **Content model first.** Define post types / fields / taxonomies (WordPress custom post types + ACF/meta) or the headless schema (Contentful/Sanity/Strapi/Payload content types) before templating. Editors must be able to change content **without touching code** — no business copy hardcoded in the theme.
- **No secrets in the theme or repo.** DB credentials, salts, API tokens, and SMTP creds live in env / `wp-config.php` (via env constants), never committed. `wp-config.php` with real values is **never** in git; headless API tokens are server-side only.
- **WordPress output/input safety.** Escape on output (`esc_html` / `esc_attr` / `esc_url` / `wp_kses`), sanitize on input (`sanitize_text_field` etc.), and use `$wpdb->prepare` for every query — WP is a large XSS/SQLi surface. **Nonces** (`wp_verify_nonce`) **+ capability checks** (`current_user_can`) on every state-changing action. Never edit WordPress core; extend via a **child theme** and properly enqueued scripts/styles (`wp_enqueue_*`). Vet third-party plugins (source, active maintenance, known CVEs) and pin versions.
- **Headless token + webhook hygiene.** Read/write API tokens stay server-side and are never shipped to the browser; preview/draft tokens are scoped and short-lived; CORS is locked to known origins; **CMS→build webhooks verify their signature** before triggering a rebuild (defer to `forge-integration`).
- **Backup before change; reversible, staged migrations.** Take a full DB + uploads backup before any plugin/theme/core update or content migration. Migrations run on **staging** first and are reversible. Serialized data (WP `wp_options`, meta) must be changed with a **serialization-safe** tool — `wp search-replace` (WP-CLI), never a raw SQL find/replace, which corrupts serialized PHP and silently breaks the site.
- **Keep it patched; least privilege.** Core, themes, and plugins stay on security-patched versions; user roles follow least privilege (no gratuitous Administrators).
- **Performance + accessibility are gates, not extras.** Page/object caching, image optimization, minimal plugin bloat, lazy-loading; and a11y on rendered output (semantic markup, alt text, heading order, contrast) — the CMS must emit accessible, fast HTML.

## Team (conditional)
Lead: `build-boss` (theme/plugin build) or `integration-boss` (headless integration + webhooks). Rendered front-end: the `forge-website` team (`ui-boss`, `seo-boss`). Support: `security-boss` (escaping/sanitization/nonces/capabilities, secrets in `wp-config`, plugin vetting), `database-reviewer` (migrations, serialized-data safety, schema), `php-reviewer` (WordPress theme/plugin PHP) or `typescript-reviewer` (headless front-end), `test-boss` (editor flows, template rendering, migration dry-run), `seo-boss` (metadata/schema/CWV). Optional advisors: `security-reviewer`, `codex-reviewer` on theme/plugin PHP or the headless token path.

## Skills / commands / MCP
`forge-website` for the rendered site (real content, responsive, a11y, SEO, performance — the CMS front-end IS a website). `forge-integration` for API-token hygiene + signed CMS→build webhooks. Exact API/config from WordPress + WP-CLI + ACF, or the headless vendor (Contentful/Sanity/Strapi/Payload), docs via Context7. `forge-n8n` if content automation runs through n8n. `systematic-debugging` for white-screen/plugin-conflict issues. **Opt-in dependency:** a local WordPress/PHP runtime (LocalWP / Docker / `wp-env`) and WP-CLI are owner-side — Forge does not provision them; without them, live migration/backup/verification are advisory + marked not-run.

## Fan-out & flow
L2 for a single theme or headless integration; L3 for a full site with custom post types + migration + multiple templates.
**Serial:** content model → **backup** → theme/plugin or headless integration → migration (reversible, on staging) → performance + a11y pass → SEO.
**Parallel:** independent templates/components ∥ content-type definitions ∥ SEO / a11y / performance audits on rendered output (independent once the content model is fixed).

## Domain gates
- Content model defined (post types / fields / taxonomies or headless schema); editors can edit content without code.
- No secrets in the theme/repo; `wp-config` values + API tokens in env; `wp-config.php` not committed.
- WordPress: output escaped, input sanitized, `$wpdb->prepare` used; nonces + capability checks on state-changing actions; child theme (no core edits); third-party plugins vetted + version-pinned.
- Headless: server-side tokens not exposed to the client; CMS→build webhooks signature-verified; CORS locked to known origins.
- Backup taken before any migration/update; migrations reversible + tested on staging; serialized data changed with a serialization-safe tool (`wp search-replace`).
- Performance (caching, image optimization, CWV budget — see `~/.claude/rules/ecc/web/performance.md`) and a11y (semantic, alt text, heading order, contrast) verified on rendered output.
- Core/themes/plugins on patched versions; user roles least-privilege.

## Ship-readiness (unique)
Content model in place and editor-tested (an editor can change copy without code); secrets in env with `wp-config`/tokens uncommitted; WP escaping/sanitization/nonces/capabilities verified (or headless client-side token exposure ruled out + webhooks verified); **backup taken and migration reversibility proven on staging** before touching production; performance + a11y evidence on the rendered site; core/plugin versions current. If no PHP/WP runtime was available, mark backup/migration/live-verify as not-run (owner-side) rather than implying they passed. Advisory checklist; optionally run `security-reviewer` / `codex-reviewer` on theme/plugin PHP or the headless token path — not a blocker.
