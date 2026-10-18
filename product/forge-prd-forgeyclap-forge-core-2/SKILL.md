---
name: forge-prd
description: Generates a structured PRD + ticket per acceptance criterion. Use before a non-trivial feature/build, after Deep Learn Mode — write a PRD, scope this feature, spec this out.
---

# Forge PRD generator (WP3)

A **Forge PRD** is a structured product-requirements document the Lead writes before a non-trivial build — it forces the scope, acceptance criteria, and test plan to be explicit before agents start touching files. It is rendered to markdown by `.claude/forge-bin/forge-prd.cjs`, a zero-dependency writer that stores both the markdown and its structured JSON meta under `.claude/forge-prd/`.

## When the Lead generates one
- Before a non-trivial feature/build (new module, new integration, anything touching 3+ files) — not for a 1-2 line fix.
- Typically right after **Deep Learn Mode** (`forge-deeplearn` skill) so the PRD's risks/architecture sections are grounded in the real codebase, not guesswork.
- Not needed when the task is a small, well-understood change or a PRD for this exact scope already exists — check `.claude/forge-prd/index.jsonl` first.

## How
1. The Lead produces the PRD content itself — real analysis, not filler — as a JSON object:
   ```json
   {
     "prd_id": "prd-<short-slug>",
     "title": "…", "project": "…",
     "sections": {
       "goal": "…", "users": ["…"], "problem": "…", "solution": "…", "modules": ["…"],
       "user_stories": ["…"], "mvp_scope": "…", "non_goals": "…", "architecture": "…",
       "risks": ["…"], "test_plan": "…", "roadmap": "…",
       "acceptance_criteria": [
         { "id": "ac-1", "text": "…", "owner": "coder", "required_tests": ["…"] }
       ]
     }
   }
   ```
   Each section value may be a plain string or an array of strings (rendered as bullets). A section the Lead genuinely has nothing for is simply omitted — it renders honestly as `_(not specified)_`, never invented.
2. Write it:
   ```
   node .claude/forge-bin/forge-prd.cjs write '<prd-json>' --run <run_id> --tickets
   ```
   - `--tickets` auto-creates one ticket per `acceptance_criteria` entry (`.claude/forge-tickets/tk-<prd_id>-<n>`, `status: "open"`) — these feed the Ticket Board and the review gates the same as any other ticket.
   - `--run <run_id>` logs `prd_generated` (and one `ticket_created` per ticket) to that run's dashboard events.
   - Dry-run a preview without writing anything: `node .claude/forge-bin/forge-prd.cjs render '<prd-json>'`.

## What it produces
`.claude/forge-prd/<prd_id>.md` (the rendered PRD, fixed section order: Goal, Users, Problem, Solution, Modules, User Stories, MVP Scope, Non-Goals, Architecture, Risks, Acceptance Criteria, Test Plan, Roadmap), `.claude/forge-prd/<prd_id>.meta.json` (the structured PRD + `_generated` timestamp), and an appended row in `.claude/forge-prd/index.jsonl`. The dashboard's **PRD** dock tab reads these read-only — it lists every generated PRD (title, project, created, acceptance-criteria count) and lets you expand one to see which sections are present.

## Honesty rule (non-negotiable)
- **Real content only.** Every section reflects an actual decision the Lead made — no placeholder/lorem sections, no invented acceptance criteria just to pad the count.
- **Secrets are auto-redacted.** Every string in the PRD is redacted (`forge-store.cjs`'s `redactValue`) before it is rendered to markdown or written to disk — never write a raw secret into a PRD.
- **The PRD viewer is read-only.** There is no write endpoint on the dashboard for PRDs; the only way to create or change one is `forge-prd.cjs write` (or hand-editing the store files, which the dashboard will simply reflect on next read).
