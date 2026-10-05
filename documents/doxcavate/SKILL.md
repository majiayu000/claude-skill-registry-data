---
name: doxcavate
description: Produces durable, structured documentation in codebases with sparse docs — readable by humans and agents alike. Two invocation modes — `survey` proposes a doc plan; `draft` writes one specific doc end-to-end with a factcheck-then-persona review gate. Triggered by phrases like "doxcavate this repo", "doxcavate the X", "doxcavate `runbook-deploy`", "what should be documented?", "document this code", "write a how-it-works for X", or any request to inventory or write project documentation.
license: MIT
compatibility: Designed for Claude Code (or similar agentskills.io-compatible clients).
---

# doxcavate

Produces durable, structured documentation in codebases where written
docs are sparse — readable by humans and agents alike.

## Install

```bash
npx skills add xornivore/skills@doxcavate --agent claude-code -y
```

## When to use

Invoke when the user:

- Asks to inventory or document a codebase ("doxcavate this repo",
  "what should be documented?", "doxcavate the X") — route to
  **survey**.
- Names a specific doc to write or refresh ("doxcavate
  `runbook-deploy`", "write a how-it-works for the ingestion
  pipeline") — route to **draft**.
- Asks to update existing docs after code changes — route to **draft**.
- Phrasing is ambiguous — ask once, then route.

Do not invoke for:

- Auto-generated API references (OpenAPI → Markdown, godoc, etc.) —
  tool-shaped, not doc-shaped.
- ADRs / decision records — they need commit-time discipline this
  skill can't manufacture after the fact.

## Hard rules

1. **Never silently write outside the host repo.** `partial` and
   `shadow` storage modes are opt-in and require user acknowledgment
   on first write. **Audit:** any write to
   `~/.local/share/doxcavate/` must be preceded by a logged
   mode-confirmation prompt.
2. **Never silently add meta-files** (`.doxcavate.yml`, `docs/`) to a
   repo that has none. Ask first. **Audit:** `git diff` after a first
   invocation must not introduce these without a logged user
   acknowledgment.
3. **In `partial` mode, leaves committed to the repo must not link to
   shadow-located meta docs.** Shadow paths are per-machine and
   per-user; rendering them into a committed leaf would break for
   everyone else. Leaf-to-leaf links inside the repo are fine.
   **Audit:** `grep -rE '~/\.local/|/Users/[^/]+/\.local/'` over the
   repo's committed leaves returns no matches.
4. **Code wins on facts.** When sources disagree, the code is the
   ground truth. See
   [investigation-and-sources](./references/investigation-and-sources.md).
5. **Factcheck is non-skippable.** No flag, prompt hint, or config
   override skips it. **Audit:** every produced doc carries a
   `## Verification` block populated by the factcheck pass.
6. **Persona output is capped at 7 ranked items.** No exceptions. If
   the reviewer would have to drop substantive items to fit, it
   emits `E_PERSONA_OVERFLOW` and halts. See
   [persona-review](./references/persona-review.md).
7. **No `git blame` author attribution** in any doc this skill
   writes. **Audit:** `grep -rE '@[a-zA-Z0-9_-]+|<[^>]+@[^>]+>'` over
   produced docs returns no author tokens.

## Reference index

Read each reference only at the action step that calls for it. Each
reference ends with `## Action checklist` — load and jump there.

- [layout-and-discovery](./references/layout-and-discovery.md) —
  config sniffing, the three storage modes (`integrated`, `partial`,
  `shadow`), Mode-by-signal table, repo keying. Read at discovery
  (always step 1).
- [invocation-modes](./references/invocation-modes.md) — survey vs
  draft, routing details, index path by storage mode. Read once mode
  is decided.
- [doc-kinds](./references/doc-kinds.md) — taxonomy, canonical
  front-matter schema, required structural anchors per kind, sizing
  targets. Read when drafting or reviewing structural conformance.
- [investigation-and-sources](./references/investigation-and-sources.md)
  — adaptive investigation, the three production sources (code,
  existing docs, commits), reconciliation order. Read at the start of
  any draft.
- [factcheck](./references/factcheck.md) — claim extraction,
  verification, `## Verification` block as byproduct,
  `E_TOO_MANY_CONTRADICTIONS` halt. Read at the factcheck step.
- [persona-review](./references/persona-review.md) — kind-keyed
  persona review, output contract, quality bar,
  `E_PERSONA_OVERFLOW` halt. Read at the persona-review step.
- [review-loop](./references/review-loop.md) — orchestration of
  factcheck and persona, single-round default, opt-in thorough mode.
  Read once the prior two are loaded.

Persona briefs are prompt templates, loaded from
`assets/persona-prompts/<kind>.md` at the persona-dispatch step.

## Top-level action checklist (when invoked)

1. Run discovery: load
   [layout-and-discovery](./references/layout-and-discovery.md), match
   the Mode-by-signal table, resolve config / docs root / storage
   mode.
2. Route survey vs draft per the **When to use** rules above.
3. **Survey:** load
   [invocation-modes](./references/invocation-modes.md), inventory the
   repo (see
   [investigation-and-sources](./references/investigation-and-sources.md)),
   propose the doc plan, write `index.md` to the resolved index path,
   stop.
4. **Draft:**
   1. Load `index.md` from the resolved path.
   2. Run the production-sources flow per
      [investigation-and-sources](./references/investigation-and-sources.md).
   3. Copy `assets/<kind>-template.md` for the target doc kind (see
      [doc-kinds](./references/doc-kinds.md)).
   4. Fill placeholders using the reconciled sources.
   5. Run factcheck per [factcheck](./references/factcheck.md) (never
      skippable).
   6. Run persona review per
      [persona-review](./references/persona-review.md), quoting
      `assets/persona-prompts/<kind>.md` in the dispatch.
   7. Apply all returned items, preferring `patch` over textual
      instruction.
   8. Run focused factcheck on changed regions only.
   9. Done — or, in thorough mode (per
      [review-loop](./references/review-loop.md)), repeat steps 5–8
      up to 3 total rounds.
