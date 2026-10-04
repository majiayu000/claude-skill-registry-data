---
name: knowledge-tree-builder
description: Use when building, extending, validating, or operating a source-grounded research knowledge tree for a field, including learning-first trees, research-incubation trees, frontier tracking, branch trunks, cards, protocols, and long-term maintenance.
---

# Knowledge Tree Builder

Build and operate source-grounded research knowledge trees. This is an
orchestrator skill: it coordinates purpose alignment, branch design, artifact
routing, sub-skill use, maturity gates, and validation. It should not duplicate
the full methods of specialized paper, search, review, or experiment skills.

## Core Rules

- Keep `learning` enabled by default.
- Align the operation profile before research, frontier, project, or high-frequency maintenance behavior.
- Use mode flags, priority, and cadence instead of a single fixed operating mode.
- Treat v0-v7 as capability milestones, not mandatory releases.
- Build only to the next acceptance gate; ask before crossing a gate that changes scope, cost, cadence, evidence burden, or project commitment.
- If the user asks to "go as far as appropriate," interpret that as next-gate planning unless they explicitly approve implementation, high cadence, or frontier/project expansion.
- Do not propose `frontier/`, `frontier_overlay`, frontier radar, watchlists, opportunity ledgers, `protocols/`, weekly scans, or project-facing artifacts as in-scope current work unless the current gate allows them or the user explicitly confirms that gate.
- If `frontier-tracking` is requested but v7 or frontier implementation is not confirmed, keep frontier content out of the current trunk, artifact layout, templates, opportunity ledgers, and research hooks. Put it only under "future confirmation needed."
- Give every new artifact one primary branch owner; link from secondary branches.
- Preserve `source-stated` or `paper-stated`, `Codex-inferred`, `needs-check`, and `not-reported` boundaries.
- Write human-facing knowledge-tree content in Chinese by default. Keep code, file names, directory names, commands, YAML/JSON keys, evidence labels, source IDs, paper titles, venue names, URLs, and quoted source titles in their original language unless the user asks otherwise.

## Workflow

1. Inspect the target directory or source material first.
2. If purpose, scope, non-goals, operation profile, or acceptance criteria are unclear, use `codex-deep-interview`.
3. If branch structure, maturity target, or multi-phase expansion is needed, use `codex-consensus-plan`.
4. Record or propose the operation profile: mode flags, priority, update cadence, source-refresh cadence, promotion path, and confirmation gates.
5. Select the next maturity gate from the operation profile and current tree state.
6. Route work through the artifact contract and sub-skill routing below.
7. Validate language, source grounding, and gate boundaries before claiming completion.

## Sub-skill Routing

Use skill names, not local file paths. Do not force-load sub-skill files through
path links. Load or invoke a sub-skill only when its phase is reached.

- **REQUIRED SUB-SKILL:** Use `codex-deep-interview` when purpose, scope, non-goals, operation profile, or acceptance criteria are materially unclear.
- **REQUIRED SUB-SKILL:** Use `codex-consensus-plan` before committing to branch trunk, maturity target, or multi-phase expansion.
- Use `anysearch`, `research-lit`, `semantic-scholar`, `arxiv`, or `paper-review-source-intel` when current external sources or academic source refresh are needed.
- Use `paper-to-research-card` when converting a paper into a source-grounded research card, if that skill is available.
- Use `research-idea-to-experiment-matrix` when promoting a research hook into an experiment matrix, if that skill is available.
- Use `research-experiment-design-reviewer` before treating a matrix or protocol as implementation-ready.
- Use `codex-completion-loop` when the user asks to carry edits through implementation, verification, and final evidence.

If a named sub-skill is not available, continue with the closest local method and say what fallback was used.

## Reference Routing

Read only the reference file needed for the current phase:

- Operation profile, mode flags, cadence, promotion paths: `references/operation-modes.md`
- Directory layout, file responsibilities, artifact ownership: `references/artifact-contract.md`
- v0-v7 capability milestones and gate rules: `references/maturity-gates.md`
- Sub-skill inputs, outputs, and integration rules: `references/subskill-routing.md`
- Reusable prompts: `references/prompts.md`
- Quality gates and validation checks: `references/validation.md`

## Output Contract

For planning or design answers, include:

- operation profile;
- target maturity gate;
- in-scope and out-of-scope work;
- artifacts to create or update;
- sub-skills to use;
- confirmation gates;
- validation plan.

For implementation work, update or create only the files required by the chosen
gate, then report changed artifacts and verification evidence.

For knowledge-tree artifacts, the readable prose should be Chinese unless the
user explicitly requests another language. Do not translate stable machine
tokens such as `source-stated`, `Codex-inferred`, file paths, source IDs, or
paper titles.

## Human Confirmation Gates

Ask the user before:

- changing primary mode, priority order, update cadence, or source-refresh cadence;
- increasing maintenance above the default monthly update plus quarterly review;
- changing the branch trunk;
- adding a `frontier/` overlay;
- running a large source refresh;
- promoting a research hook into a protocol draft;
- connecting the tree to a private project, codebase, dataset, manuscript, or expensive experiment.

## Common Mistakes

- Do not turn a learning tree into a research or frontier tree silently.
- Do not auto-run from v0 to v7 because a mode flag was selected.
- Do not label `frontier/`, `frontier_overlay`, radar, watchlist, or opportunity-ledger artifacts as v1-v4 work; before v7, mention them only as future options unless explicitly confirmed.
- Do not create a "frontier radar" branch inside the stable trunk before the v7 gate; use stable problem, method, dataset, evaluation, and learning branches first.
- Do not make `frontier/` replace `branches/`; frontier is an overlay.
- Do not copy all sub-skill content into this skill.
- Do not put local absolute paths, credentials, private endpoints, or unpublished materials in public tree files.
- Do not leave user-facing explanations, learning routes, glossary entries, comparison notes, or build summaries in English when the user has not requested English.
