---
name: ak-stitch
description: "Generate AI UI designs from text prompts with Google Stitch and export Tailwind, HTML or DESIGN.md for design-to-code."
when_to_use: "Invoke for rapid prototyping or design exploration."
category: design
keywords: [Stitch, UI-generation, prototyping, Tailwind]
license: Proprietary
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
argument-hint: "[design prompt or action]"
metadata:
  author: agentkit
  version: "1.0.1"
---

# Google Stitch — AI Design Generation

Generate high-fidelity UI designs from text prompts via Google Stitch. Export Tailwind/HTML, orchestrate design-to-code pipelines with existing UI skills.

Resolve service limits and available models from current account/service evidence when needed. Bundled quota counters are local estimates, not live account entitlement.

## Setup only when needed

First inspect installed dependencies and check whether `STITCH_API_KEY` is present
without displaying its value. Use an existing authorized environment/secret store.
If missing, report the required setup and pause provider calls; do not write
placeholders or credentials into a global Claude home automatically.

Install missing SDK dependencies only in the selected skill/project environment.
For requested MCP setup, read `references/stitch-mcp-setup.md` and adapt to the
actual runtime's supported configuration. Resolve SDK models/methods from the
installed version/help or service; examples do not establish live capabilities.

## Quick Start

```bash
# Check quota
npx tsx scripts/stitch-quota.ts check

# Generate design
npx tsx scripts/stitch-generate.ts "A checkout page with payment form and cart summary"

# Export as HTML + DESIGN.md
npx tsx scripts/stitch-export.ts <screen-id> --format all --output ./stitch-exports/
```

## Actions

### generate

Generate UI design from text prompt.

```bash
npx tsx scripts/stitch-generate.ts "<prompt>" [--project <id>] [--project-name <title>] [--device MOBILE|DESKTOP|TABLET] [--variants <count>]
```

Returns: screen ID, preview image URL. With `--variants`: additional design alternatives.

### export

Export generated design as HTML/Tailwind, screenshot, or DESIGN.md.

```bash
npx tsx scripts/stitch-export.ts <screen-id> [--format html|image|all] [--output <dir>]
```

Outputs:
- `design.html` — Semantic HTML with Tailwind CSS classes
- `design.png` — Screenshot of the design
- `DESIGN.md` — Agent-readable design spec (colors, typography, spacing, components)

### quota

Check and manage daily quota.

```bash
npx tsx scripts/stitch-quota.ts check       # Show remaining credits
npx tsx scripts/stitch-quota.ts increment   # Bump after generation
npx tsx scripts/stitch-quota.ts reset       # Force reset (auto-resets daily)
```

### edit

Refine an existing design.

```typescript
const editedScreen = await screen.edit("Make the header darker and add a search bar");
```

### Project Isolation

Stitch auto-isolates designs per git repo. Each repo gets its own Stitch project automatically.

**Resolution priority:**
1. `--project <id>` — direct Stitch project ID
2. `--project-name <title>` — title-based lookup-or-create
3. `STITCH_PROJECT_ID` env — user's global override
4. Auto-detect from git repo name
5. `"claudekit-default"` fallback

When an active plan exists, pass `--project-name "{repo}/{plan-slug}"` to group designs by plan:
```bash
npx tsx scripts/stitch-generate.ts "checkout page" --project-name "my-saas/auth-system"
```

If no plan is active, omit `--project-name` — the script auto-detects from the git repo name.

## Orchestration Pipeline

### Design-to-Code Flow

1. **Check quota** — Read available account evidence and optionally the local tracker. Treat tracker output as an estimate; on rate limiting use service reset/retry guidance, not blind retries.
2. **Generate** — Run `stitch-generate.ts` with user's design prompt. If a plan is active, pass `--project-name "{repo}/{plan-slug}"` for isolation.
3. **Review** — Show generated design image to user for feedback
4. **Variants** (optional) — Generate alternatives if user wants exploration
5. **Export** — Run `stitch-export.ts --format all` to get HTML + DESIGN.md
6. **Implement** — Hand off exported artifacts to implementation skill:
   - `ak-frontend-design` — React/Vue/Svelte components from Tailwind export
   - `ak-ui-ux-pro-max` — Full page layouts with style guide integration
   - `ak-ui-styling` — Design token extraction from DESIGN.md
7. **Track quota** — Record completed generation usage once; inspect whether the generation script already increments before changing the local counter.

### Handoff Protocol

- Export creates `DESIGN.md` in project root or plan directory
- Implementation skills detect `DESIGN.md` and use it as design spec
- Compare DESIGN.md with the latest accepted brief; user instructions take precedence
- If no DESIGN.md exists, skills fall back to normal text-based design flow

See `references/design-to-code-pipeline.md` for detailed patterns and examples.

## Quota Management

- Consult current service/account limits; local defaults are not a live quota reading
- Local tracking via `~/.claudekit/.stitch-quota.json`
- Warns when remaining credits < 20%
- **Fallback:** When exhausted, use `ak-ui-ux-pro-max` for text-based design generation

See `references/quota-management.md` for strategies.

## Limitations

- **No React export** — HTML/Tailwind only; Claude converts to React/Vue components
- **Responsive verification** — Inspect exported layouts at target viewports and add missing breakpoints
- **No animations** — Static designs only; add micro-interactions in code
- **Single-user** — No multiplayer/collaboration features
- **Quota uncertainty** — Service limits/tier support require current account evidence
- **Generic output risk** — Combine with style guides for differentiation

## References

| Topic | File |
|-------|------|
| SDK API | `references/stitch-sdk-api.md` |
| MCP Setup | `references/stitch-mcp-setup.md` |
| Pipeline Patterns | `references/design-to-code-pipeline.md` |
| Quota Strategy | `references/quota-management.md` |
