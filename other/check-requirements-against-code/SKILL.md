---
name: check-requirements-against-code
description: Check requirements docs against implementation and report discrepancies
allowed-tools: Read, Grep, Glob, Bash, Agent, Edit, Write
---

Comprehensively compare the requirements documents in `docs/` against the actual
implementation (`src/` and `apple-fm-helper/main.swift`), then bring the
derived docs back in sync. Generate a report with recommendations and questions.

## Steps

1. **Read all requirements documents** in `docs/`: `1-overview.md`,
   `2-architecture.md`, `3-requirements.md`, `4-protocol.md`. If new numbered
   docs have been added, include them. Also read `README.md` and `CLAUDE.md` —
   both enumerate the API and module layout and drift the same way.

2. **For each FR/NFR in `3-requirements.md`**, verify against the code:
   - Find the implementing symbol in `src/` (or the Swift helper).
   - Check the behavior matches, and that the **status marker** is honest —
     remember **Partial** is the correct marker for code that is written but not
     yet verified on an Apple Intelligence device (AF-2). Don't upgrade a Swift
     path to **Shipped** without on-device evidence.
   - Note missing, different, undocumented, or stale items.

3. **Verify the wire protocol three ways agree**: `docs/4-protocol.md`, the Node
   side (`src/protocol.ts` + `src/helper.ts`), and the Swift helper
   (`apple-fm-helper/main.swift`). The event vocabulary (`delta`/`result`/`error`),
   the probe line shape, and the error codes must match across all three. The
   reference stub `tests/fixtures/stub-helper.js` must also still match.

4. **Check `CLAUDE.md` completeness**:
   - Every doc under `docs/` appears in the docs list.
   - The architecture/source list names every file under `src/`.
   - The public API block matches the exports of `src/index.ts`.
   - The "Commands" section lists every `npm run *` script in `package.json`.
   - The coverage-thresholds sentence matches `vitest.config.ts`.

5. **Synchronize `docs/ai/code-summary.md`**: confirm the directory tree matches
   `src/` (use Glob), the Public API list matches `src/index.ts`, the coverage
   thresholds match `vitest.config.ts`, and the "where do I look" entries still
   resolve. Make the edits in place.

6. **Synchronize `docs/ai/requirements-summary.md`**: confirm each FR/NFR line
   matches its row in `3-requirements.md` (same status). Make the edits in place.

7. **Final consistency pass**: `CLAUDE.md`, `README.md`, and the two AI summaries
   must agree with the source docs and code. Resolve any disagreement in favor of
   the code / `src/index.ts` (API) / `3-requirements.md` (behavior) /
   `vitest.config.ts` (thresholds). **The most common drift here is a new public
   export or a new `src/*.ts` file landing without the AI summaries and CLAUDE.md
   being updated** — look for that explicitly.

## Report Format

### Discrepancies Found
For each: **Requirement** (doc + ID), **Implementation** (file:line), **Type**
(`missing` | `different` | `undocumented` | `stale` | `status-wrong`),
**Recommendation** (fix doc or fix code).

### CLAUDE.md / Summary Coverage Audit
List docs, source files, exports, scripts, or thresholds that are present in code
but missing from CLAUDE.md / the AI summaries (or vice versa).

### Files Edited
The summary/doc files you updated and why (or "no changes needed").

### Questions
Ambiguous requirements where the implementation made a judgment call.
