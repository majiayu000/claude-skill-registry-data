---
name: mk:stitch
description: Generate novel UI from a text prompt via Stitch AI. Exports Tailwind/HTML, produces DESIGN.md for mk:frontend-design handoff. NOT for implementing existing designs — use mk:figma or mk:frontend-design for that.
user-invocable: true
when_to_use: Generate a new UI design from a text description (text-prompt → novel design). NOT for implementing an existing design source — use mk:figma for Figma URLs or mk:frontend-design for an existing spec/mockup/DESIGN.md. Stitch generates novel designs from scratch; it does not interpret existing visual sources.
category: frontend
phase: on-demand
keywords:
  - stitch
  - ui-generation
  - text-to-ui
  - prototyping
  - design-generation
  - tailwind
  - html-export
  - design-to-code
  - design-handoff
  - ai-design
  - rapid-prototyping
  - mock-ui
  - screen-design
requires_external_service:
  - stitch
default_enabled: false
requires_env:
  - name: STITCH_API_KEY
    required: true
    description: Stitch API key (sk_...) for design generation
    setup: Get from https://stitch.withgoogle.com/settings/api
    fallback: Skill is disabled without this key. Use mk:frontend-design for text-based design instead.
trust_level: kit-authored
injection_risk: high
stable_output_contract: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
argument-hint: '[generate|export|quota] [args]'
metadata:
  author: meowkit
  version: 1.0.0
owner: utility
criticality: medium
status: active
runtime: claude-code
---

# Stitch — AI Design Generation

Generate high-fidelity UI designs from text prompts. Export Tailwind/HTML, PNG screenshot,
and DESIGN.md for handoff to `mk:frontend-design`.

Use only for a novel, text-prompt design. Existing design sources belong to `mk:figma` or
`mk:frontend-design`.

## Setup and guard

Set `STITCH_API_KEY` in the project env file, then install the scripts once:

```bash
cd .claude/skills/stitch/scripts && npm install
```

Run the prerequisite check before any API command; it fails before a network request if the key
or `tsx` is unavailable. Full setup, optional variables, and MCP setup: [references/stitch-setup.md](references/stitch-setup.md).

## Fail-Closed Gate

Before any script runs, verify both prerequisites:

```bash
# Key gate
[ -z "$STITCH_API_KEY" ] && { echo "[X] STITCH_API_KEY not set — add it to the project env file"; exit 1; }

# tsx gate
npx tsx --version 2>/dev/null || { echo "[X] tsx not found — run: cd .claude/skills/stitch/scripts && npm install"; exit 1; }
```

`stitch-api-call.ts` also checks `STITCH_API_KEY` as its first action before any Stitch SDK
call. If the key is unset the script exits 1 immediately — no network request is made.

## Quick Start

```bash
# 1. Check quota
npx tsx .claude/skills/stitch/scripts/stitch-quota.ts check

# 2. Generate (API call only — returns JSON with screenId + imageUrl)
npx tsx .claude/skills/stitch/scripts/stitch-api-call.ts \
  generate "A checkout page with cart summary and payment form"

# 3. Export + write files (pipe: API call → schema-validate → write to disk)
npx tsx .claude/skills/stitch/scripts/stitch-api-call.ts export <screen-id> | \
  npx tsx .claude/skills/stitch/scripts/stitch-write-output.ts
```

## Commands

| Task | Command / contract |
|---|---|
| Check quota | `npx tsx .claude/skills/stitch/scripts/stitch-quota.ts check` |
| Generate | `npx tsx .claude/skills/stitch/scripts/stitch-api-call.ts generate "<prompt>"` — returns `screenId`, `projectId`, `imageUrl`, and quota data |
| Export | `npx tsx .claude/skills/stitch/scripts/stitch-api-call.ts export <screen-id> \| npx tsx .claude/skills/stitch/scripts/stitch-write-output.ts` |

Show `imageUrl` and obtain user approval before exporting. Detailed flags, quota operations, and
the API/write security boundary: [references/stitch-operations.md](references/stitch-operations.md).

## Workflow

1. Check quota; if exhausted (exit 2), route to `mk:frontend-design`.
2. Generate, review the returned screenshot with the user, then export and write.
3. Handoff `DESIGN.md` to `mk:frontend-design` for implementation.

Load [references/design-to-code-pipeline.md](references/design-to-code-pipeline.md) for variants,
iteration patterns, and detailed handoff guidance.

The writer outputs the HTML, image, and `DESIGN.md` handoff under `tasks/designs/`; exact paths
and the handoff contract are in [references/stitch-operations.md](references/stitch-operations.md).

## Limitations

- **HTML/Tailwind only** — no React/Vue/Svelte export; use `mk:frontend-design` to convert
- **Non-responsive layouts** — add breakpoints during implementation
- **Static only** — no animations; add micro-interactions in code
- **Local quota tracking** — actual usage may diverge if designs are generated outside this skill

## Gotchas

- `STITCH_API_KEY` must be set in the project env file — the skill fails closed (exit 1) if unset; no network call is attempted
- `tsx` must be installed (`npm install` in `scripts/`) — scripts will not run without it; install once per machine
- Local quota can drift from real Stitch usage (e.g., designs made via the Stitch web UI); if you hit `RATE_LIMITED` despite the tracker showing credits, run `stitch-quota.ts reset`
- Quota limits and paid-tier availability are volatile; load [quota-management.md](references/quota-management.md) before making a quota-based decision.
- Screen IDs returned by `generate` are stable (Tool Contract Rule 2); project name auto-detection uses git remote then CWD basename
- The optional MCP integration stores the API key in `.claude/.mcp.json` — never commit that file; the kit's `.gitignore` covers it
- `stitch-write-output.ts` validates CDN URLs against a Google-domain allowlist; if Stitch changes CDN domains, update `ALLOWED_CDN_SUFFIXES` in that script

## References

| Topic | File |
|-------|------|
| SDK API | `references/stitch-sdk-api.md` |
| MCP Setup | `references/stitch-mcp-setup.md` |
| Pipeline Patterns | `references/design-to-code-pipeline.md` |
| Quota Strategy | `references/quota-management.md` |
