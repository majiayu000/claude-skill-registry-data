---
name: specification-capture
description: "Capture the four specification elements (non-goals, failure modes, interface contracts, risk map) for an issue and persist them to the decision journal under a ## Specification heading. Use when starting work on an issue (Phase 1 of /flow:start), entering a design discussion (/flow:design), or starting a brainstorm (/flow:brainstorm). This skill MUST be consulted because acceptance criteria alone do not say what the implementation is NOT, how it fails, what schemas it honors, or where its logic is most likely to be subtly wrong — without those, PLAN cannot fence the implementation and VERIFY cannot tell a right implementation from a plausible wrong one."
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
agent: general-purpose
---

# Specification Capture

## Contract

Iron law: **every issue gets the four elements (non-goals, failure modes, interface contracts, risk map) in the journal before PLAN.** Invoked with issue context, journal path, and invocation reason (Per-invoker scope below). Returns the `## Captured Specification` payload from [`references/specification-journal-format.md`](../../references/specification-journal-format.md) after writing and re-reading `.decisions/issue-{N}.md`. Permitted skips: elements outside the invoker's scope row; the risk map when `specFirst.riskMap` is `false` (written as `disabled — specFirst.riskMap=false`); elements the journal already holds for an unchanged issue.

## Inputs

Issue context, journal path (`<journal dir>/issue-{N}.md`, the journal dir being what `bin/journal-dir.sh` prints; never a hand-built `.decisions/`), invocation reason (`start` | `design` | `brainstorm`). Any missing: halt with `SPEC_CAPTURE_BLOCK: missing input <name>`. Toggle: `"${CLAUDE_PLUGIN_ROOT:-plugins/flow}/bin/cascade-resolve.sh" --default true '.specFirst.riskMap'`.

## Process

### Step 1: Read the journal first

Run `bin/journal-read-section.sh --file "$JOURNAL" --heading '## Specification'` and record which of `### Non-goals`, `### Failure modes`, `### Interface contracts`, `### Risk map` exist. All four present and the issue not newer than the journal (staleness rule in the reference): return verbatim. Otherwise fill only the gaps.

### Step 2: Extract from the issue body

Cues. Non-goals: `## Non-goals`, `## Out of scope`, "Does NOT". Failure modes: `## Failure modes`, `## Error cases`, "timeout", "fallback". Interface contracts: `## API`, `## Schema`, `## Contract`, type definitions, signatures. Risk map: `## Risks`, `## Tricky parts`, "edge", "subtle", "off-by-one".

Verbatim matches are `extracted-from-issue`; never prompt for what the issue states.

### Step 3: Prompt for missing elements

Draft each missing element, then surface one blocking six-field escalation per element (never bundled) via `AskUserQuestion` per [`references/escalation-format.md`](../../references/escalation-format.md). Options: (1) accept draft, (2) edit, (3) reject (update the issue first). Recommend (1).

Risk map draft: 2-6 rows from the issue and the touched files. Each: where the logic is likeliest subtly wrong; what the plausible wrong version does (reversed order, off-by-one, wrong precedence, wrong empty case); one input where right and wrong differ.

### Step 4: Write the journal

Write `## Specification` per the reference shape (replace if present, append otherwise). All four failure-mode categories are required; a non-applicable one is `none — {reason}`, never blank.

Persist it with `bin/journal-append.sh --file "$JOURNAL" --replace-heading '## Specification' -` (on stdin), never `Write`: an unlocked body write can be published over by the manifest writer's rename. Non-zero exit → `SPEC_CAPTURE_BLOCK: journal write failed (exit {code})`. Re-read with the Step 1 command; absent → `SPEC_CAPTURE_BLOCK: journal write verification failed`.

### Step 5: Return the captured specification

Return the `## Captured Specification` payload; consumers cite subsections as `Non-goals touched`, `Failure modes covered`, `Interface contract`, `Risk areas`.

## Per-invoker scope

- `commands/start.md` Phase 1: all four (risk map exempt when `specFirst.riskMap` is `false`); partial = BLOCK.
- `commands/design.md` Phase 1: non-goals + interface contracts; risk map recommended.
- `commands/brainstorm.md` Phase 1: non-goals only, captured before generating approaches.
- `commands/debug.md` Phase 3 (via `goal-contract-capture`): outcome + acceptance criterion (the reproducing test) + root-cause constraints; full specification skipped.

## Anti-patterns

- "The acceptance criteria are enough": criteria scope WHAT; the elements scope IS NOT, FAILS HOW, WHICH SCHEMAS, WRONG WHERE.
- "I'll capture during PLAN": PLAN's fence is built from the specification; the Stranger Test fails.
- "The failure-mode categories cover risk": no. Timeouts, partial failures, invalid input, missing context are infrastructure error paths agents already over-test. The risk map is about the core logic being subtly wrong.

## Verification gates

The invoker MUST verify (any failure: halt, re-invoke):

1. The journal contains `## Specification`.
2. `### Non-goals`, `### Failure modes`, `### Interface contracts` present and non-empty (`none — {reason}` allowed per failure-mode category).
3. `### Risk map` is a 2-6 row table, or exactly `disabled — specFirst.riskMap=false`.
4. The return payload matches the journal.
