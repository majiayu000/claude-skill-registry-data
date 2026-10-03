---
name: stitch
description: Operate Google Stitch through an already configured Stitch MCP server. Use when the user explicitly mentions Stitch or asks to generate, edit, vary, import, export, synchronize, or convert Stitch screens; manage a Stitch design system; run a resumable multi-page Stitch loop; or turn Stitch screens into React. Do not trigger for generic UI design requests that do not require Stitch.
---

# Stitch

Treat Stitch as a design execution backend. Keep product structure, visual direction, and design policy in Aphrodite; use this skill to translate those decisions into Stitch operations and code artifacts.

## Boundary

- Let `design-plan` (`/aphrodite`) own discovery, IA, layout blueprints, and the root `DESIGN.md`.
- Let Stitch own remote project/screen operations and `.stitch/` runtime state.
- Let the existing application architecture own routing, state, data, and component conventions.
- Use standalone Stitch mode only when the user explicitly wants direct Stitch work without Aphrodite.

Never invent a visual direction inside this skill when `DESIGN.md` or `docs/design-refs/` exists. Compile those artifacts into Stitch inputs.

## Preflight

1. Inspect the available tools and identify the Stitch MCP namespace by capability, not by a hard-coded prefix.
2. Stop and report the missing dependency if no Stitch MCP tools are available. Never fabricate project IDs, screen IDs, URLs, or tool results.
3. Read [references/mcp-contract.md](references/mcp-contract.md) completely before any Stitch MCP call.
4. Read the project root `DESIGN.md` and relevant `docs/design-refs/` artifacts before generating or editing a screen.
5. Check `.stitch/metadata.json` before remote lookup. Validate it with:

```bash
python <STITCH_SKILL_DIR>/scripts/validate_stitch_state.py .stitch/metadata.json
```

Resolve `<STITCH_SKILL_DIR>` to the directory containing this `SKILL.md`; do not assume the skill is installed inside the target project.

6. Classify the action:
   - Read-only: list/get projects, retrieve screens, download artifacts, compare state.
   - Remote mutation: create/edit/vary/apply a design system.
   - Sensitive upload: send a local image, HTML file, or `DESIGN.md` to Stitch.
7. Treat the user's explicit request to create/edit/vary as authorization for that scoped remote mutation. Before a sensitive upload, still show the exact project, files, types, and sizes and obtain confirmation.

## Route the Request

The first column is a semantic route key. In the default source-only install, a parent harness or the current
LLM selects the route after reading this file; it does not issue a slash command. The `/stitch ...` text in
parentheses is only a compatibility alias when source-only skills were explicitly activated with
`--include-source-only-skills`.

| Route key (full-install compatibility alias) | Route | Required reference |
|---|---|---|
| `generate` (`/stitch generate`) | Generate a screen from text or an uploaded image | [generate-and-design-system.md](references/generate-and-design-system.md) |
| `edit` (`/stitch edit`) | Modify selected existing screens | [generate-and-design-system.md](references/generate-and-design-system.md) |
| `variants` (`/stitch variants`) | Produce controlled alternatives from a selected screen | [generate-and-design-system.md](references/generate-and-design-system.md) |
| `design-system pull` (`/stitch design-system pull`) | Reverse-extract remote visual language into a proposed `DESIGN.md` update | [generate-and-design-system.md](references/generate-and-design-system.md) |
| `design-system push` (`/stitch design-system push`) | Synchronize the root `DESIGN.md` into Stitch | [generate-and-design-system.md](references/generate-and-design-system.md) |
| `design-system apply` (`/stitch design-system apply`) | Apply a Stitch design-system asset to selected screens | [generate-and-design-system.md](references/generate-and-design-system.md) |
| `loop` (`/stitch loop`) | Generate a resumable multi-page set | [loop-state.md](references/loop-state.md) |
| `react` (`/stitch react`) | Convert or synchronize Stitch screens with a React app | [react-handoff.md](references/react-handoff.md) |
| `import` (`/stitch import`) | Capture local UI and upload it into Stitch | [import-export.md](references/import-export.md) |
| `sync` (`/stitch sync`) | Refresh remote metadata and local staged artifacts | [loop-state.md](references/loop-state.md) |
| `status` (`/stitch status`) | Compare local runtime state with the remote project | [loop-state.md](references/loop-state.md) |

When the full-install compatibility aliases are active, preserve these mappings:

- `/stitch design` means `/stitch design-system pull`.
- `/stitch prompt` means compile an Aphrodite brief into the `generate` route without calling Stitch unless generation was requested.

If the request is ambiguous, infer the least-mutating route from the available artifacts. Ask only when two routes would materially change different remote state.

## Artifact Authority

Use this order when artifacts disagree:

1. Root `DESIGN.md`: design-system source of truth.
2. Latest `docs/design-refs/` brief, sitemap, direction, and layout blueprint: page structure and content contract.
3. Existing application code: functional and architectural contract.
4. `.stitch/` files: transport, cache, and resumable execution state.
5. Remote Stitch screen: generated implementation candidate.

Use `.stitch/DESIGN.md` only as a synchronized transport copy of root `DESIGN.md`. Do not let it become a second independently edited design system. See [references/loop-state.md](references/loop-state.md) for the full artifact contract.

## Core Execution Protocol

1. Retrieve the current project and selected screens before mutation.
2. Resolve the intended device type, target screen instances, and design-system asset.
3. Compile only the requested change:
   - Generate for a new structure.
   - Edit for a localized change.
   - Create variants for exploration around a good base.
   - Avoid rerolling a screen whose structure is already correct.
4. Perform the smallest sufficient Stitch operation.
5. Retrieve the resulting project and screen metadata again; do not trust a mutation response alone.
6. Download the resulting HTML and full-width screenshot into `.stitch/designs/` without overwriting existing files unless refresh was requested.
7. View the screenshot and compare it with `DESIGN.md`, the layout blueprint, and the requested delta.
8. Update `.stitch/metadata.json` only from observed remote state, then run the state validator.
9. Run code-level and visual verification required by the selected route.
10. Report project ID, affected screen IDs, local artifacts, verification evidence, and any residual drift.

## Non-Negotiable Rules

- Never assume legacy tools such as `get_screen_html`, `get_screen_metadata`, or `download_screen_asset` exist. Discover the live contract and prefer `get_screen` download URLs when available.
- Never repeat colors, fonts, and theme instructions in every generation prompt when a project-level Stitch design system is applied. This creates two competing theme sources.
- Never send position or dimension fields to `apply_design_system`; pass only `id` and `sourceScreen` for real screen instances.
- Never expose an API key in a prompt, command transcript, committed file, or report. Use the `STITCH_API_KEY` environment variable for direct uploads.
- Never overwrite an existing root `DESIGN.md`, staged screen, or application file without first comparing the old and new state.
- Never keep an autonomous loop alive by inventing unnecessary pages. Finish when the declared roadmap is complete.
- Never impose a new React architecture merely because Stitch emitted static HTML. Adapt to the repository's stack and conventions.
- Never declare visual fidelity from HTML inspection alone. Inspect the downloaded screenshot or a rendered local page.

## Deterministic Helpers

Use the bundled scripts instead of re-emitting binary/base64 payloads or writing ad hoc state checks:

```bash
# Validate resumable state
python <STITCH_SKILL_DIR>/scripts/validate_stitch_state.py .stitch/metadata.json

# Download a screen artifact without accidental overwrite
python <STITCH_SKILL_DIR>/scripts/fetch_stitch_asset.py \
  --url "<download-url>" --output .stitch/designs/home.html

# Preview an upload without network mutation
python <STITCH_SKILL_DIR>/scripts/upload_to_stitch.py \
  --project-id "<project-id>" --file DESIGN.md --dry-run
```

Read [references/import-export.md](references/import-export.md) before using the uploader. An actual upload requires `STITCH_API_KEY` and `--confirm-upload` after user confirmation.

## Completion Evidence

Do not report completion until all applicable evidence exists:

- Stitch MCP capability and target project confirmed.
- Resulting screen or design-system IDs retrieved after mutation.
- `.stitch/metadata.json` updated and validator passed.
- Generated screenshot visually inspected.
- React route: typecheck/lint and rendered comparison completed when the project supports them.
- Loop route: sitemap and baton agree; baton is explicitly complete when no declared page remains.

## Provenance

This local adapter selectively incorporates operational patterns from `google-labs-code/stitch-skills` as reviewed at commit `535b0889a46868c9b08f8a7f7084db3c1958a2b6` on 2026-08-09. The upstream project is a useful implementation reference, not the local design-policy authority and not an officially supported Google product.
