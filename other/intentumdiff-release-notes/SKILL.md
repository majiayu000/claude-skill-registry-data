---
name: intentumdiff-release-notes
description: >-
  How IntentumDiff turns a semantic diff into human intent — the deterministic "what/why/risk"
  explainer, the release-notes buckets, and the opt-in BYOK LLM narrative. Use this whenever
  you work on release notes, intent explanations, the "why" text shown in CodeLens/hover/Peek,
  risk categorisation, or the LLM narrative — files `plugins/vscode/src/releaseNotes.ts`,
  `intentExplain.ts`, `intentLlmPrompt.ts`, `intentLlmExplainer.ts`. It covers the bucket
  model, how risk is derived, the anti-redundancy rules for "what — why", NodeFacts-driven
  wording, and the privacy-safe LLM path. Read intentumdiff-vscode and intentumdiff-engine first;
  the LLM path must obey the BYOK/privacy invariants.
---

# IntentumDiff — Intent explanations & release notes

Two layers: a **deterministic explainer** (always on, offline) that turns each change into a
readable `{ what, why, risk }`, and **release notes** that bucket those by derived risk. An
**opt-in BYOK LLM** can add a narrative — grounded only in locally-derived facts, never raw
source by default.

## Deterministic explainer (`intentExplain.ts`)

`explainChange(change, group?, contentClass?)` and `explainGroup(group, changes, contentClass?)`
→ `IntentExplanation = { what, why, risk }`. Composed from parts (so i18n stays feasible):

- **what** — verb + subject (+ location from `scope_trail`): "Added function `ccc`", "Renamed
  `total` → `subtotal`", "Modified `calculate_tax`", "Moved `validate`", "Removed `foo`".
  Prefer `refactoring_kind`/labels/`node_type`; fall back to `description` then the change type.
- **why** — a *specific* impact clause, built from the strongest available signal and **never
  restating the what**. Sources, in priority order: value change parsed from `text_diff`
  (`[-old][+new]`), node-type role (return→"changes the returned value", condition→"changes
  control flow", import→"changes a dependency", …), `NodeFacts` (no params / returns nothing /
  stub body / async / generator), visibility, size. Guarantees a short honest baseline when no
  strong signal exists — never the platitude "may change runtime behavior" alone.
- **risk** — `riskForContent(kind, contentClass)`: code → `behavior` (MEANINGFUL) /
  `internal` (REFACTORING, MOVED); non-code → `content`; style/noise → unrisked.

**NodeFacts are the honest source.** Prefer `node.facts` (engine-emitted: `param_count`,
`returns`, `body`, `is_async`, `is_generator`) over reverse-engineering the tree. A
`def ccc(): pass` must read "no parameters; returns nothing; empty no-op body", not "takes a
parameter" or "now available to callers." See `intentumdiff-engine` for NodeFacts.

**Content-awareness:** gate all code framing on `contentClass === "code"`. On docs/config/data/
text, drop "New public API", function nouns, and behavior claims (see `intentumdiff-vscode` →
`contentClass.ts`).

## Release notes (`releaseNotes.ts`)

`buildReleaseNotes(diff)` → `ReleaseNotes { behavior, internal, other, guardrails }`:

- **behavior** — `risk === "behavior"` (meaningful code changes).
- **internal** — `risk === "internal"` (refactors, moves).
- **other** — `risk === "content"` (docs/config/data/text edits — "Docs & chores").
- **guardrails** — guardrail violations with severity + scope.

Each line is `noteLine(explanation)` = `what — why`, where the `why` is dropped if it merely
restates the `what`. Style/noise groups earn no note (`categoryForKind` returns undefined,
matching CodeLens suppression). `releaseNotesSummary` gives "N behavior · M internal · K
docs/chore · G guardrail". `releaseNotesToMarkdown` (Copy-as-Markdown) and `releaseNotesToJson`
(Export-JSON) always emit all sections for a stable shape.

**Ungrouped-change coverage (index-space contract):** notes must cover changes owned by no
group. `buildReleaseNotes` uses `coveredChangeIndices(groups, changes.length)` and classifies
any uncovered change via `kindForChange` — not only when the engine emits zero groups. Skip
out-of-range indices everywhere. (See `intentumdiff-engine` → `references/index-space-contract.md`.)

## Opt-in LLM narrative (BYOK — obey privacy invariants)

`IntentLlmExplainer` + prompt builders in `intentLlmPrompt.ts`
(`buildExplainPrompt`, `buildReleaseNarrativePrompt`, `renderFactSheet`):

- Gated on `intentumdiff.intent.explainer === "llm"`; deterministic is the fallback on any
  error/refusal/no-model/offline. Never blocks the UI (hover/CodeLens show deterministic
  immediately, upgrade when the LLM resolves; results cached by content hash).
- Providers: `vscode-lm` (Copilot, no key, VS Code's own consent), `anthropic` (BYOK), and
  `openai-compatible` (BYOK cloud **or** local Ollama/LM Studio/vLLM via `baseUrl`).
- **Privacy:** the narrative sends only locally-derived notes/facts. Per-change prompts respect
  `codeSharing` — `signatures`/`facts` send no bodies/literals; `full` (verbatim source) only
  to a **local** endpoint. The prompt explicitly forbids review-process meta-advice ("reviewers
  must verify…") and instructs the model to explain what the code *does*; stubs/no-ops must be
  called out as such.
- Keys in SecretStorage only. **Unit tests do no network** — the prompt/parse logic is pure and
  tested; the network call lives in a thin vscode wrapper.

## Tests

`test/releaseNotes.test.ts` (buckets, summary, ungrouped coverage, out-of-range),
`test/intentExplain.test.ts` (what/why/risk, NodeFacts wording, no-redundancy, content-class),
`test/intentLlmPrompt.test.ts` (prompt framing, no "code element" on non-code, no network).
