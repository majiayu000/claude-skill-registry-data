---
name: code-cleanup
description: Find and fix surface hygiene (typos, naming, comment hygiene, editing artifacts, debug statements) and redundancies, non-idiomatic code, dead code, and unnecessary complexity. Identifies comments that violate the project commenting policy and strips them. Use when asked to clean up, simplify, fix typos or comment hygiene, remove dead code, or address code-quality findings directly.
---

Apply small, behavior-preserving fixes — surface hygiene and complexity/redundancy — until further changes would have diminishing returns.

## Operating Principles

- Assume cleanup is requested; focus on safe, behavior-preserving improvements within scope.
- Prefer applying validated fixes over merely generating review findings.
- If analysis is requested without edits, report findings and proposed fixes instead of modifying files.
- Keep changesets easy to review: small, targeted changes with clear verification.
- For larger structural refactors (extraction/rename/movement across modules), use `code-plan-refactor`; this skill applies only small in-place fixes.
- For runtime/production errors, use `code-debug`; this skill addresses code quality, not failures.

## Modes

- **Focused** (default): Clean the requested files, diff, or subsystem.
- **Diff**: Clean only current working-copy changes.
- **Opportunistic**: Clean nearby low-risk issues within the scope.
- **Conservative**: Remove only obvious dead or redundant code and simple non-idioms.

## Process

### Step 1 - Identify Scope

- For code changes: `jj diff -s` to see changed files, then `jj diff -- path` to narrow scope.
- Focus on user-specified files or paths.
- Determine the cleanup mode from the request, defaulting to **Focused**.

### Step 2 - Map Cleanup Opportunities

Apply a scout lens to map cleanup opportunities in the following scope: {scope}:

- Map relevant files, conventions, and call paths.
- Cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs.
- Stay read-only.
- Keep it concise and task-relevant.

Read the `martin-fowler-code-smells` reference and flag relevant Fowler smells (Duplicated Code, Lazy Elements, Speculative Generality, Middle Man, Long Function, etc.); treat smells as heuristics and skip what the linter/formatter already enforces.

#### Redundancies

- Redundant defensive checks that restate the obvious (e.g. `if arr is not None and len(arr) > 0:` when context guarantees a non-empty list).
- Single-use intermediate variables that just rename (e.g. `is_valid = check(x); if is_valid:` -> `if check(x):`).
- Duplicate logic that could share a single source (e.g. near-identical blocks differing only by a constant).

#### Non-idiomatic code

- Verbose manual equivalents of established idioms (e.g. index-based loop where a comprehension or `for...in` is idiomatic).
- Reinventing stdlib functionality (e.g. custom `unique()` instead of a built-in set/dedup primitive).

#### Dead code

- Unreachable code after early returns/raises.
- Unused imports, variables, functions, or fields.
- Commented-out code left after a change.

#### Simplification opportunities

- Overly complex conditionals that collapse (e.g. `if x == True:` -> `if x:`; nested `if` chains that combine).
- Unnecessary abstraction for a single use case (e.g. a generic wrapper with one caller and one implementation).

#### Unnecessary complexity

- Premature generalization (e.g. configurable hooks/strategies with only one strategy ever passed).
- Deep nesting that flattens with early returns or guards.

#### Reimplemented functionality

- Reimplemented logic duplicating a well-known library or stdlib utility (e.g. custom date parsing, retry/backoff loop, custom argument parser).
- Reinventing functionality a popular, trusted dependency already provides (e.g. custom HTTP client reimplementing timeout/retry/redirect handling; custom JSON schema validation).
- Exceptions: the user asked for a reimplementation/dependency-free approach, or no existing library fits constraints (license, size, platform) with a note explaining why.

#### Hygiene and artifacts

- Spelling typos, grammatical errors, naming/formatting convention violations.
- Whitespace/newline noise, missing final newline, merge artifacts.
- Ad-hoc debug statements (`print()`, `console.log()`).
- Out-of-scope changes and inconsistent coding conventions.

#### Comment hygiene

Per the project commenting policy, comments exist only to capture _why not_ — the non-obvious decision rationale, rejected alternative, or constraint. Identify and strip every violating comment.

Report each violation with file:line, the comment text, and its category:

- **Describes what/how**: restates code, function name, type signature, list size/count, or obvious mechanics (e.g. `// Returns the user` on `function getUser()`).
- **Narrative or changelog**: step-by-step narration, work history, "replaced x with y", "previously we...", "As discussed above"; changelog-style blocks are forbidden.
- **Decorated**: inline borders/emphasis like `// --- Title ---`, `# ==== Title ====`, `/* ===== */`. Reduce to `// Title`, or strip when obvious.
- **Filler and boilerplate**: "Note:/Important:/NB:" prefixes adding nothing; filler words (simply/just/basically); over-detailed docstrings on trivial functions; built-in/stdlib explanations.
- **Stale**: commented-out code, orphaned TODOs, references to deleted constructs or removed behavior, transitional/legacy markers.

Action:

- **Strip** the comment entirely when it carries no _why not_ rationale.
- **Trim to the rationale** when a why-not reason is buried inside a violating comment.
- **Keep** comments that encode a genuine constraint or rejected alternative, even when terse.

Do not strip license/copyright headers, shebangs and editor modelines, language/tooling pragmas and region markers, i18n message comments, or config-file comments conveying settings meaning.

Report file paths, line numbers, and evidence for each.

Once mapping is complete:

- Consult the `code-check` skill for project test and lint commands.
- Run targeted tests or checks on the current diff to establish a safety baseline.

### Step 3 - Synthesize Findings

- Filter to safe, behavior-preserving improvements; discard speculative items lacking evidence.
- Align with existing project patterns rather than external preferences.

### Step 4 - Apply Fixes

Apply a worker lens to apply these cleanup fixes in the files {files} based on the {prioritized findings list}:

- Read files before editing; keep diffs minimal and idiomatic; preserve public behavior; verify with the narrowest meaningful command.
- If a fix fails twice, stop and report.

Specifically:

- Apply one logical cleanup per step.
- Strip policy-violating comments per findings: remove or trim to why-not rationale. Never strip license headers, shebangs/modelines, tooling pragmas, or config-file settings comments.
- Preserve public behavior, API signatures, and test expectations.

### Step 5 - Stop at Diminishing Returns

Halt cleanup when:

- Remaining issues are speculative or lack clear evidence.
- Fixes require risky, cross-cutting refactors.
- Changes require product or API decisions beyond the request.
- Edits produce churn without maintainability value.

### Step 6 - Verify

- Re-run baseline safety checks.
- Apply the project formatter if applicable.

### Step 7 - Report

Report to the user:

- **Scope**: Files and mode targeted.
- **Cleanup Applied**: Each modification with a before/after summary.
- **Verification**: Test and check results confirming behavior was preserved.
- **Deferred/Remaining Items**: Identified issues left unfixed, with rationale.

## Guardrails

- Avoid broad rewrites or behavioral/API changes unless explicitly requested.
- Do not fix unrelated issues outside the defined scope.
- Do not delete code unless usage analysis and build evidence support removal, or the user explicitly asked.
- Always preserve public behavior and test outcomes.
- Strip only policy-violating comments; keep genuine why-not rationale, license/copyright headers, shebangs/modelines, tooling pragmas, and config-file settings comments.
- Do not invoke other skills directly; only reading `code-check` for command detection is permitted.
