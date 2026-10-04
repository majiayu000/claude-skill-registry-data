---
name: ds-figma
description: 'Generate or refresh a clean Figma design system FROM the code (the code is the source of truth). Use when a project has (or you''re building) its design system in code and you want the Figma side clean and in sync — "make a clean Figma DS from the code", "sync Figma with the code", "the Figma is messy, rebuild it from the code". Variables = token names, library mirrors the real components, Code Connect, auto-layout. For an existing/legacy Figma DS: generate fresh and re-link the screens, do NOT merge. Uses the Figma MCP.'
---

# ds-figma — a clean Figma DS, generated from the code

The code is the source of truth; this produces the **Figma reflection** of it. Run it once the
project's code design system is clean (`/ds-audit` first; no code DS yet → build it, or
`/ds-bootstrap` for greenfield).

## Approach — generate fresh, don't merge

Building a clean library *into* an existing, drifted Figma page works badly (duplicate
components, broken instance links). So:

1. **Generate a fresh, clean Figma library from the code** (Figma MCP — `figma-generate-library`):
   - **Variables = token names exactly** (light + dark).
   - **Components mirror the real code components 1:1** (shadcn + `@efounders` bespoke).
   - **Auto-layout everywhere**; clean layer names.
   - **Code Connect**: link each Figma component to its real code component.
   - A component not in the code → **don't fake it**; flag it as a gap to add to the DS.
2. **If a legacy Figma DS exists, don't merge into it.** Generate the fresh library, **re-link
   the screens** to the new components (instance swap), then **retire / kill the legacy DS page.**
   Clean break — never two competing sources.
   - *Optional, upstream only:* if the old Figma holds a genuinely-better decision not yet in
     the code, fold it **into the code first** — it then flows into the fresh Figma. Then kill the legacy.
3. Prefix any exploration / WIP frames with `_wip/` so the MCP skips them later.

## Deliver

The Figma link + a short summary: what was generated, which screens got re-linked, what legacy
was retired, and any component gaps flagged (to add in code — never faked in Figma).

## Rules
- **Code = source of truth.** Figma reflects it; never the reverse.
- **Fresh + re-link beats merge** whenever a legacy Figma DS exists.
- Variables = token names · real components · auto-layout · Code Connect.
