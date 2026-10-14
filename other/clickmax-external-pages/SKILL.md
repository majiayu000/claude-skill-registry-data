---
name: clickmax-external-pages
description: Use when the user wants to connect an external page/site to Clickmax tracking or forms using Clickmax page scripts.
---

## When this applies

Use this skill for external pages: a page hosted outside the Clickmax builder that needs Clickmax tracking, capture/forms, or script installation guidance.

DOES NOT APPLY inside a Max Design (AI Builder) session bound to a repository: pages built there get the Clickmax script injected and are registered as external pages AUTOMATICALLY on publish — never call `pages_create_external` for them, and "criar uma página" in that session means a new route file in the project (`sandbox.*`), governed by the session playbook.

CLASSIFICATION RULE (external vs builder): a page is EXTERNAL whenever it already lives at a URL on a domain the user has NOT connected in Clickmax (Framer, Webflow, their own site, any third-party host). Register it with `pages_create_external` (real URL) — NEVER `pages_create`. Creating a builder page for a URL you did not build yields an empty Clickmax-hosted page and breaks the capture-script setup (the app opens the visual editor instead of the script/redirect flow). If you have the live URL and still call `pages_create`, pass it as `sourceUrl`: the server rejects non-Clickmax hosts and tells you to switch to `pages_create_external`.

An external page has THREE setup steps the user does in their own HTML. Only step 1 is tool-generated (it embeds a minified per-page loader); steps 2 and 3 are STATIC snippets kept in this skill's references. Page metadata (`projectSlug`, `path`, `externalUrl`) comes from `pages_get`.

|Step|What it does|Snippet source|Docs|
|-|-|-|-|
|1. Install script (`Instalar script`)|boots the Browser SDK (tracking + page_view)|`pages_get_external_script` -> `headScript` (per-page string)|https://docs.clickmax.io/sdk|
|2. Lead capture (`Configurar captura`)|a Clickmax-bound form/widget that ingests leads|[lead capture](references/lead-capture.md) — static|https://docs.clickmax.io/sdk/forms/|
|3. Redirect (`Redirecionamento`)|annotate buttons/links/forms so the SDK advances the visitor to the next funnel step|[redirect](references/redirect.md) — static|https://docs.clickmax.io/sdk/tracking/|

Surface each in a copyable code block with its doc link. Steps 2 and 3 only work once step 1's head script is installed. An external MCP client (Claude/Codex) with the skill installed gets steps 2/3 from these references; either way the head comes from the tool.

Not this skill:

- designing/editing builder page content -> use the visual builder workflow
- funnel graph routing -> `clickmax-funnels`

## Key assumptions

- External pages are not builder pages; do not promise builder-only editing, publish, path, or domain controls.
- The external script goes in the external site's `<head>` so tracking/form bindings initialize reliably.
- Clickmax can provide script/bootstrap guidance, but the external site's HTML/CMS must be edited outside Clickmax.
- Redirect behavior and form attributes must be kept consistent with the user's external page flow.

## Thought process

1. Confirm the page is external and resolve/create its Clickmax page record.
2. Retrieve the external script for the exact page.
3. Explain the install location and the minimum form attributes needed.
4. Keep the answer to one concrete install example unless the user asks for variants.

## Execute guide

- External page that belongs to a FUNNEL step (most common: "vincular a página externa ao funil") = compose the granular tools in order: `mcp__plugin_clickmax_clickmax__pages_create_external` (get `pageId`) -> `mcp__plugin_clickmax_clickmax__funnels_node_create` (`type: "page"` + `slug` + `triggers`) -> `mcp__plugin_clickmax_clickmax__funnels_node_connect_page` (linking an external page auto-wires `node.config.externalUrl`) -> `mcp__plugin_clickmax_clickmax__funnels_triggers_connect` (route to the next node) -> `mcp__plugin_clickmax_clickmax__pages_get_external_script` (surface the snippets). Full graph guidance -> `clickmax-funnels` (external-page common flow).
- Use `mcp__plugin_clickmax_clickmax__pages_list` / `mcp__plugin_clickmax_clickmax__pages_get` to identify existing external page records.
- Use `mcp__plugin_clickmax_clickmax__pages_create_external` for a standalone external page NOT tied to a funnel node (to plug it into a funnel later, follow the granular sequence above).
- Use `mcp__plugin_clickmax_clickmax__pages_update` for external page metadata or URL changes.
- Use `mcp__plugin_clickmax_clickmax__pages_get_external_script` (by `pageId`) to get step 1 — it returns `headScript` (a string); tell the user to paste it before `</head>`. For steps 2/3 hand them the snippets from [lead capture](references/lead-capture.md) / [redirect](references/redirect.md) + the docs links (no tool call — static).
- Use `mcp__plugin_clickmax_clickmax__pages_delete` only when the user explicitly wants to remove the Clickmax page record.

## References

- [lead capture](references/lead-capture.md) — form + widget snippets for step 2 (`/sdk/forms/`)
- [redirect](references/redirect.md) — button/link/form annotation snippets for step 3 (`/sdk/tracking/`)

## Report

- State that this is an external page setup, not a Clickmax builder page.
- Return page URL/identity, script install location, and one concise form/tracking instruction.
- If the user needs implementation help, provide the smallest HTML example that matches the returned script guidance.

## Warnings

- Do not tell the user Clickmax can visually edit external site content.
- Do not use builder-page publish/config language for external pages.
- Do not dump multiple script/form variants when one exact install path is enough.

## Anti-patterns

- Treating a funnel node that references a page as proof the external script is installed.
- Returning a generic web-tracking answer without using the page-specific script tool.

---

Clickmax skill revision: `b8294822a4d6`
