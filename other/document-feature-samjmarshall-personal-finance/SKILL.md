---
name: document-feature
description: Interview a developer to produce a living feature doc at docs/feature/{slug}.md, capturing user value, architecture (with ADR links), and data/user flow with at least one Mermaid diagram. Use when the user says "document this feature", "write a feature doc", "create docs/feature/X", "explain feature X for new devs", or asks to onboard future engineers onto a shipped feature. Different from /write-plan (forward-looking design) and Epics (scope/sprint planning) — this is the present-tense "what does this thing do today" doc for engineers reading the codebase cold.
disable-model-invocation: true
model: sonnet
effort: high
---

# document-feature

## What this is, what this isn't

`docs/feature/{slug}.md` is the **living, present-tense** doc for a shipped feature. Adjacent doc types serve different purposes:

- `thoughts/designs/` — forward-looking proposals (past-tense once shipped)
- `thoughts/epics/` — scope and milestone planning
- `thoughts/plans/` — the build roadmap for an epic
- `docs/adr/` — point-in-time decisions

A feature doc tells a future engineer (human or LLM agent) what the feature does **today** and where to look. It is not a design history.

## Quick start

```
User: /document-feature lead-conversation-history
→ Recon → Interview (3 pillars) → Draft → Plain-language pass → Update index
```

Output: `docs/feature/lead-conversation-history.md` + an entry in `docs/feature/README.md`.

## Workflow

### 1. Recon (read code first, ask less)

- Resolve `{slug}` from user input.
- Check `docs/feature/{slug}.md` — if it exists, ask: update or replace?
- Grep code for the feature; identify file paths and route segments.
- List ADRs in `docs/adr/` that may relate.
- Find GitHub issues/PRs: `gh issue list --search "{slug}"`, `gh pr list --search "{slug}"`, and `git log --oneline --grep="{slug}"` to surface PRs that shipped the feature. Capture issue numbers for the frontmatter `related-issues:` field.
- **Fast-path**: if `thoughts/designs/*-{slug}.md` exists, read it first and pre-fill draft answers — the interview then verifies and updates rather than gathering from scratch.
- Surface findings to the user before starting the interview.

### 2. Interview (3 pillars, one Q at a time)

Methodology: one question at a time, propose a recommended answer when the codebase suggests one, explore code instead of asking when answerable. Full bank in [INTERVIEW.md](INTERVIEW.md).

- **P1 — User value**: who is the user, what problem does this solve, what's out of scope, how do we know it works?
- **P2 — Design + ADRs + ops**: where does this live in code, what was the design choice (and what was rejected), which ADRs apply, what logs/alerts/flags signal health, what are the failure modes?
- **P3 — Flow**: what triggers it (UI, cron, webhook — list all), what data path does it follow, what state changes happen, what are the edges?

### 3. Draft

- Load [TEMPLATE.md](TEMPLATE.md); write to `docs/feature/{slug}.md`.
- Embed at least one Mermaid diagram in the Flow section. Pick by content:
  - `sequenceDiagram` — ≥2 actors with ordered messages
  - `flowchart LR` — single-actor branching logic
  - `stateDiagram-v2` — explicit state transitions
  - `graph TD` / `graph LR` — feature spans ≥3 services/modules
- Mirror the diagram styles already proven in `docs/README.md` so they render in the existing stack.
- Cross-link ADRs/designs/epics via relative paths (see `docs/adr/adr001-imessage-integration-for-sales-automation.md` Links section).

### 4. Plain-language pass

- Apply rules from [PLAIN-LANGUAGE.md](PLAIN-LANGUAGE.md) — two zones: **explain-mode** (~grade 6) for user-value sections, **tech-mode** (~grade 9-10) for architecture/flow.
- Invoke the `writing-clearly-and-concisely` skill on the draft for the final pass.

### 5. Update index

- Append/update `docs/feature/README.md`: one line per slug, sorted alphabetically. Format: `- [Feature Name](slug.md) — one-line description from doc's intro.`
- Bootstrap on first run with a brief explainer paragraph framing what `docs/feature/` is.

## Behavioural rules

- **Do not create ADRs.** If a hard-to-reverse decision surfaces without one, flag inline with `> [!NOTE] Missing ADR: <decision>. Recommend /domain-model.` Defer creation to the `domain-model` skill.
- Frontmatter required fields: `status: living`, `last-updated: YYYY-MM-DD`, `related-adrs:`, `related-design:`, `related-epic:`, `related-issues:` (GitHub issue/PR numbers — `gh issue list` and `git log` for the slug surface candidates).
- Bootstrap `docs/feature/` if it does not exist; the first feature doc creates the directory.

## See also

- [INTERVIEW.md](INTERVIEW.md) — full question bank with skip-if conditions.
- [PLAIN-LANGUAGE.md](PLAIN-LANGUAGE.md) — Strunk rules, compression principles, replaceable-pattern checklist.
- [TEMPLATE.md](TEMPLATE.md) — output skeleton with frontmatter and Mermaid placeholders.
