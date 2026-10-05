---
name: propagate
description: >
  Walk an upstream documentation change downstream — when a PRD, SRS, tech-design,
  or feature spec is edited, find every dependent document, identify which sections
  are now stale, and interactively update them to keep the entire doc chain
  consistent. Use after editing any spec-forge document, or run periodically with
  --since to catch accumulated drift.
---

# Spec Forge — Propagate

## ⚡ Execution Entry Point (READ THIS FIRST)

**Begin executing Step 1 immediately; never fall back to a manual workflow or stop to ask what to do.**

---

Walk a doc change downstream and keep the whole chain consistent.

## Iron Law

**EVERY UPSTREAM CHANGE PROPAGATES OR FAILS LOUDLY. Partial propagation is worse than no propagation — it creates the illusion of consistency where there is none.**

## When to Use

- After editing a PRD / SRS / tech-design / feature-spec — find and update every doc that references the changed concepts
- After running `/spec-forge:prd` or another generator that modified an existing doc in place
- Periodically, with `--since {git-ref}`, to catch accumulated drift across recent commits
- Before a release, to make sure no doc is silently stale relative to its upstream
- When `spec-forge:analyze` or `spec-forge:audit` flags inconsistencies between upstream and downstream docs

This skill is the symmetric counterpart to `code-forge:fix --review` (which propagates code review findings into code changes). Where `code-forge:fix` walks *up* from a bug to the spec, `spec-forge:propagate` walks *down* from a spec change to the docs and code that depend on it.

## Command Format

```
/spec-forge:propagate [@source-doc.md] [--since git-ref] [--scope all|docs|code] [--dry-run] [--save]
```

| Argument / Flag | Default | Description |
|-----------------|---------|-------------|
| `@source-doc.md` | — | The upstream doc whose changes should propagate. If omitted, auto-detect from `git diff HEAD` (uncommitted changes) or `git diff HEAD~1 HEAD` (last commit). |
| `--since {git-ref}` | — | Compute the diff between `{git-ref}` and `HEAD` instead of using uncommitted changes. Useful for catching drift across multiple commits. |
| `--scope` | `docs` | What to propagate into. `docs` = downstream documentation only. `code` = also flag code that references changed requirement IDs. `all` = both. |
| `--dry-run` | off | Generate the impact report and per-downstream proposed changes, but do NOT apply any edits. The user reviews the report and re-runs without `--dry-run` to apply. |
| `--save` | off | Save the propagation report to `docs/propagate-report-{timestamp}.md` in addition to displaying it. |

## Workflow

```
Step 1 (Determine Source) → Step 2 (Extract Changed Concepts) → Step 3 (Discover Downstream Refs)
  → Step 4 (Per-Downstream Impact Analysis) → Step 5 (Interactive Review) → Step 6 (Apply)
  → Step 7 (Verify) → Step 8 (Report)
```

## Detailed Steps

### Step 1: Determine Source Document and Change Scope

#### 1.1 Resolve the Source

Parse `$ARGUMENTS`:

- **If `@source-doc.md` is provided:** use it as the source. Verify the file exists.
- **If `--since {ref}` is provided:** the source is the set of all `.md` files in `docs/` that changed between `{ref}` and `HEAD`. Use `git diff --name-only {ref}...HEAD -- 'docs/**/*.md' '*.md'` to enumerate.
- **If neither is provided:**
  1. Run `git status --porcelain -- 'docs/**/*.md' '*.md'` to find uncommitted doc changes.
  2. If non-empty: those files are the source.
  3. If empty: run `git diff --name-only HEAD~1 HEAD -- 'docs/**/*.md' '*.md'` (the last commit's doc changes).
  4. If still empty: display `No doc changes detected. Provide an explicit @source-doc.md or use --since {ref}.` and stop.

If the source is auto-detected, display the resolved file list and use `AskUserQuestion`:
- "Propagate from these {N} files" → continue to 1.2
- "Pick a different source" → re-prompt with `AskUserQuestion` listing nearby docs

#### 1.2 Compute Change Scope

For each source file, compute the diff:

- **Uncommitted source:** `git diff HEAD -- {file}`
- **`--since` source:** `git diff {ref}...HEAD -- {file}`
- **Last-commit source:** `git diff HEAD~1 HEAD -- {file}`

Display the diff summary:

```
Source documents:
  docs/core/prd.md     +24 -8
  docs/core/srs.md     +12 -3
Total: 2 files, +36 -11 lines
```

Store the per-file diffs in memory for Step 2.

---

### Step 2: Extract Changed Concepts (Sub-agent)

**Offload to a sub-agent** so the diff content stays out of the main context.

Spawn an `Agent` tool call:
- `subagent_type`: `"general-purpose"`
- `description`: `"Extract changed concepts from doc diff"`

**Sub-agent prompt must include:**
- The source file paths
- The full diff for each (paste verbatim)
- The instruction: **"Extract every concept the diff introduces, modifies, or removes. A concept is anything a downstream document might reference: requirement ID (FR-XXX-NNN, NFR-XXX-NNN, REQ-NNN), defined term, component name, module name, API endpoint, data field, success metric, decision, dependency, persona, or numeric threshold. For each concept, classify it as ADDED, MODIFIED, REMOVED, or RENAMED. For RENAMED, provide both the old and new name."**
- The required structured return format below

**Sub-agent must return:**

```
CONCEPTS_REPORT

ADDED:
- type: {requirement_id|term|component|api|metric|decision|threshold|other}
  name: {concept name}
  defined_at: {source_file:line}
  summary: {one-sentence description}

MODIFIED:
- type: {...}
  name: {...}
  defined_at: {source_file:line}
  what_changed: {one-sentence description of the change}

REMOVED:
- type: {...}
  name: {...}
  was_defined_at: {source_file:line in the OLD version}
  reason: {one-sentence why it was removed, if inferrable}

RENAMED:
- type: {...}
  old_name: {...}
  new_name: {...}
  defined_at: {source_file:line}

SEARCH_TERMS:
- {keyword 1}
- {keyword 2}
- {... grep-friendly strings to find downstream references — include literal IDs, exact term names, and at least one variant for each rename}
```

**Main context retains:** Only this report (~3-5KB).

---

### Step 3: Discover Downstream References (Sub-agent)

**Offload to a sub-agent** so the grep output stays out of the main context.

**Deterministic assist:** the ID-shaped SEARCH_TERMs (FR-XXX-NNN, NFR-XXX-NNN, REQ-NNN) can be extracted and located mechanically — `python3 "<sf_scripts>/sf-trace.py" ids <file...>` (resolve `<sf_scripts>` via `@../shared/scripts.md`) pulls the exact IDs each doc declares, and `python3 "<sf_scripts>/sf-scan.py" --root "<root>" --docs-only` gives the doc inventory those terms are located across. Feed those to the sub-agent as the deterministic starting point; the STALE vs STILL_VALID vs AMBIGUOUS judgement (Step 4) stays with the model. Fall back to grep by hand if the scripts are unavailable.

Spawn an `Agent` tool call:
- `subagent_type`: `"general-purpose"`
- `description`: `"Discover downstream references"`

**Sub-agent prompt must include:**
- The `CONCEPTS_REPORT` from Step 2 (paste verbatim)
- The project root path
- The scope flag (`docs`, `code`, or `all`)
- The instruction: **"For every entry in SEARCH_TERMS, grep the project for references and produce a list of downstream files and locations that mention any of these concepts. Exclude the source files themselves (they are upstream). For docs scope, search `**/*.md` excluding the source files. For code scope, also search source files (`**/*.{py,ts,js,tsx,jsx,go,rs,java,rb,php}`). Group results by downstream file."**
- The instruction: **"For each downstream file, list which concepts it references, with line numbers. Distinguish RENAMED concepts: a downstream file that mentions only the OLD name is now stale; one that mentions only the NEW name is current; one that mentions both is in the middle of an update."**
- The required structured return format below

**Sub-agent must return:**

```
DOWNSTREAM_REPORT

DOC_REFERENCES:
- file: {downstream_file_path}
  type: {prd|srs|tech-design|feature-spec|test-cases|test-plan|readme|adr|other}
  references:
    - concept: {concept name}
      kind: {ADDED|MODIFIED|REMOVED|RENAMED}
      lines: [{line numbers where mentioned}]
      uses_old_name: {true|false}  # only for RENAMED
      uses_new_name: {true|false}  # only for RENAMED

CODE_REFERENCES:  # only if scope = code or all
- file: {code_file_path}
  language: {python|typescript|...}
  references:
    - concept: {concept name}
      kind: {...}
      lines: [{...}]

ORPHANED:
- {concepts marked REMOVED in CONCEPTS_REPORT that are still referenced somewhere — these are the most urgent fixes}

SUMMARY:
  total_downstream_docs: {N}
  total_downstream_code_files: {N}
  most_referenced_concept: {name and ref count}
```

**Main context retains:** Only this report (~5-10KB depending on project size).

---

### Step 4: Per-Downstream Impact Analysis (Parallel Sub-agents)

For each entry in `DOWNSTREAM_REPORT.DOC_REFERENCES` (and optionally `CODE_REFERENCES`), spawn a sub-agent to determine **what specific changes the downstream needs**. Fan out per-downstream in parallel — one `Agent` tool call per downstream file — batching to stay within your tool-call budget.

**Each sub-agent receives:**
- The downstream file path
- The relevant slice of `CONCEPTS_REPORT` (only the concepts this downstream references)
- The relevant slice of `DOWNSTREAM_REPORT` (only this file's references)
- The instruction below

**Sub-agent prompt:**

```
You are analyzing whether {downstream_file} needs to be updated in response to upstream
spec changes.

Read {downstream_file} from disk. For each referenced concept, decide whether and how
the downstream needs to change.

Decision rules:
- ADDED concept: usually no change needed unless the downstream is the natural place
  to consume the new concept (e.g., a new requirement should be referenced from the
  test-cases doc). If the downstream should reference the new concept, propose where.
- MODIFIED concept: the downstream's mention of this concept may now be stale. Read
  the surrounding context, compare against the new upstream definition, and decide:
  STALE (needs update), STILL_VALID (the change doesn't affect this mention), or
  AMBIGUOUS (human judgment needed).
- REMOVED concept: the downstream still references something that no longer exists.
  Either the reference must be deleted, or replaced with a pointer to the replacement
  (if there is one — check the surrounding context for hints).
- RENAMED concept: any mention of the old name is stale. Replace with the new name.

For each needed change, produce a unified-diff-style proposed edit that the orchestrator
can apply directly. Be precise about the line range and the exact replacement text.
Do NOT make subjective improvements unrelated to the propagation — only address the
upstream changes.

Return structured output:

DOWNSTREAM_IMPACT for {downstream_file}

CHANGES_NEEDED:
- concept: {concept name}
  decision: STALE | STILL_VALID | AMBIGUOUS | REMOVE_REFERENCE | ADD_REFERENCE
  current_text:
    line {N}: {current line content}
  proposed_text:
    line {N}: {proposed replacement}
  rationale: {one sentence why this change is needed}
  confidence: HIGH | MEDIUM | LOW  # HIGH = mechanical replacement, LOW = needs human review

NO_CHANGE_NEEDED:
- concept: {concept name}
  reason: {one sentence}

AMBIGUOUS:
- concept: {concept name}
  question: {what the human needs to decide}
```

After all sub-agents complete, aggregate into a single `IMPACT_REPORT` keyed by downstream file.

---

### Step 5: Interactive Review

Walk the `IMPACT_REPORT` with the user. For each downstream file with `CHANGES_NEEDED`, display the proposed changes and use `AskUserQuestion` to choose:

```
Downstream: docs/core/srs.md
Proposed changes (3):

  [1] FR-AUTH-005 (RENAMED → FR-USER-005)
      Current  L42:  - The system shall enforce FR-AUTH-005 (password complexity)
      Proposed L42:  - The system shall enforce FR-USER-005 (password complexity)
      Confidence: HIGH

  [2] threshold "5 attempts" (MODIFIED → "3 attempts")
      Current  L88:  - Account locks after 5 failed attempts
      Proposed L88:  - Account locks after 3 failed attempts
      Confidence: HIGH

  [3] component "AuthService" (REMOVED, replaced by "UserAuthFlow" + "SessionManager")
      Current  L120: - AuthService validates credentials and issues tokens
      Proposed L120: <AMBIGUOUS — needs human decision>
      Confidence: LOW
      Question: How should this sentence be split between UserAuthFlow and SessionManager?

How would you like to proceed?
  - Apply all HIGH-confidence changes, ask me about LOW/AMBIGUOUS
  - Apply all proposed changes (including AMBIGUOUS — I'll review the diff after)
  - Show me the full diff for this file before deciding
  - Skip this file entirely
  - Stop and let me handle this manually
```

For each AMBIGUOUS change, follow up with a focused `AskUserQuestion` per concept.

If `--dry-run` was set: skip the interactive choices, collect everything as "would apply" / "would skip", and jump to Step 8 (Report).

---

### Step 6: Apply Changes

For each accepted change from Step 5:

1. Read the current content of the downstream file
2. Apply the proposed edit using `Edit` (specific line range, exact text replacement)
3. After all changes for a file are applied, run `git diff -- {file}` and store the diff

**Hard rule:** Use `Edit` for surgical changes. Never rewrite the entire file. Never use `Write` to overwrite. The downstream file may have content unrelated to the propagation — that content must not be touched.

**Hard rule:** Apply changes file by file, not concept by concept. This keeps each file's edits atomic and easy to revert.

---

### Step 7: Verify

After all changes are applied:

1. **Re-run the discovery (Step 3) on the updated downstreams.** This is a mechanical re-grep, not hand work — re-run the same search (the discovery sub-agent, or `python3 "<sf_scripts>/sf-scan.py"` / `sf-trace.py ids` for ID-shaped terms) and compare before/after hit counts. Any concept marked REMOVED or RENAMED in `CONCEPTS_REPORT` that still appears in any downstream file is a propagation gap — display it as `STILL_STALE` and ask the user to address it manually.

2. **If scope includes `code`:** run the project's test suite (auto-detect from build config). If tests fail, surface the failures. The propagation may have broken something — the user must decide whether to fix forward or revert.

3. **Optional: invoke `spec-forge:audit` on the affected docs** to confirm internal consistency post-propagation. Spawn as a sub-agent.

---

### Step 8: Report

Display the propagation report:

```
Propagate Complete

Source documents: {N}
  - docs/core/prd.md (+24 -8)
  - docs/core/srs.md (+12 -3)

Concepts changed:
  ADDED: {N}    MODIFIED: {N}    REMOVED: {N}    RENAMED: {N}

Downstream files analyzed: {N}
  Updated:    {N}
  Skipped:    {N}
  Ambiguous:  {N} (left for manual)

Code references: {N} (scope = {scope})

Verification:
  Stale references remaining: {N}
  {if any: list them}
  Tests after propagation: {pass/fail/skipped}

Files modified:
  docs/core/srs.md       3 changes
  docs/core/tech-design.md  5 changes
  docs/features/auth.md  2 changes
  README.md              1 change

Next steps:
  Review changes:  git diff
  Commit:          git add <files> && git commit -m "docs: propagate changes from prd.md"
  Re-run audit:    /spec-forge:audit

{if --save was used:}
Report saved: docs/propagate-report-{timestamp}.md
```

If `--dry-run` was set: prefix the entire report with `DRY RUN — no changes were applied.` and append:

```
To apply the proposed changes, re-run without --dry-run:
  /spec-forge:propagate {original args minus --dry-run}
```

---

## Common Mistakes

- **Skipping Step 2 (concept extraction).** Without an explicit list of changed concepts, the discovery sub-agent has nothing to grep for and the propagation collapses to a manual review.
- **Touching code in `--scope docs` mode.** When the user specified `docs`, the skill must not modify any code files even if they reference stale concepts. Code-side updates are out of scope.
- **Treating AMBIGUOUS as HIGH-confidence and silently applying.** When the impact analyzer says LOW / AMBIGUOUS, the user must decide. Auto-applying these defeats the safety of the workflow.
- **Forgetting Step 7 verification.** After applying, the same grep that found the references should now find zero. If it doesn't, the propagation is incomplete.
- **Running propagate on a dirty source.** If the source doc itself is in the middle of being edited (multiple unrelated changes pending), the concept extraction will be polluted. Either stage the unrelated changes elsewhere first or use `--since` against a clean ref.

## Coordination With Other Skills

- **`spec-forge:analyze`** is the broader landscape tool — it surfaces *all* drift across the doc collection. Use `analyze` periodically; use `propagate` after each upstream change.
- **`spec-forge:audit`** verifies docs against code and against quality criteria. After a `propagate` run, an `audit` confirms the propagation didn't break anything.
- **`code-forge:fix --review`** is the symmetric tool on the code side — it walks code review findings back into the code. `propagate` walks doc changes forward into downstream docs.
- **`apcore-skills:sync`** is the cross-language version — it verifies that the same spec is consistent across multiple language implementations. `propagate` is the within-doc-chain version.
