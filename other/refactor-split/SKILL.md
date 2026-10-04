---
name: refactor-split
description: Split a single overlarge module into multiple focused modules — without changing behavior. Sibling to refactor-extract (function-level) and refactor-architecture (package-level). Loads when the operator says "this file is too big" / "split aicp/core/X.py" / "router.py is doing 5 things".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# refactor-split

Splits a single overlarge module into multiple focused modules. Sits between
`refactor-extract` (function/class-level — extract one thing within a file)
and `refactor-architecture` (package-level — restructure many packages).
This skill operates at the FILE level: one module becomes 2+ modules,
typically with a shared package directory.

Triggered when a single `.py` file accumulates multiple responsibilities and
becomes hard to navigate. AICP convention (CLAUDE.md): "Keep modules small
and focused. One responsibility per file." Splits enforce that.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "this file is too big", "split aicp/core/X.py", "router.py is doing 5 things", "break this module up", "factor this into multiple files"
- **Quality-audit / quality-lint finding**: a single file is hot in multiple metrics (line count high + cyclomatic complexity high + responsibility unclear) — the file needs splitting, not just internal extraction
- **Quality-coverage finding**: coverage gaps cluster in one file because its responsibilities are too tangled to test in isolation — split first, then test
- **From quality-debt**: a TODO or HACK marker says "// TODO: split this file when we figure out the right boundaries"
- **From refactor-architecture**: package-level refactor identified that one of the destination packages should be a multi-file package, not one giant module — load this skill to split

Do NOT load when:

- Function-level extraction within ONE file is enough (load `refactor-extract`)
- Package-level restructuring is needed (load `refactor-architecture`)
- Behavior needs to change (load `feature-implement`)
- Lexical rename only (load `refactor-rename`)

## Operations

This skill has 4 named operations.

### Operation 1: Identify the responsibilities to split + the destination layout

**Trigger**: skill loaded; oversized module identified.

**Process**:

1. Read the source module. Capture: total line count, top-level definitions (classes, functions, constants), implicit dependencies between them.
2. Identify the SEAMS — where natural responsibility boundaries lie:
   - Group definitions by what data they operate on (cohesion: same data ⇒ same module)
   - Group by who calls them (callers from one package suggest the definition belongs near that package)
   - Group by lifecycle (initialization-only vs runtime-only vs shutdown-only suggest different modules)
   - Group by conceptual layer (low-level utilities vs high-level orchestration)
3. Choose the destination layout:
   - **In-place split**: `router.py` becomes `router/__init__.py` + `router/scoring.py` + `router/dispatch.py` + `router/circuit.py`. The package is created at the OLD module's path. Importers see the same `from aicp.core.router import X` if `__init__.py` re-exports.
   - **Sibling split**: `router.py` stays but slimmer; new `router_scoring.py` and `router_circuit.py` siblings created. Less disruption to imports.
   - **Submodule split**: `router.py` stays as the public entrypoint; new module `aicp/core/_router/scoring.py` etc. holds internals (underscore-prefix package signals private).
4. For EACH new module, name what it contains in 1 sentence:
   - `router/scoring.py` — pure scoring logic, no I/O
   - `router/dispatch.py` — backend dispatch + failover chain traversal
   - `router/circuit.py` — circuit breaker state machine
5. Verify the split makes IMPORTS cleaner, not harder. If `router/dispatch.py` ends up importing `router/scoring.py` AND `router/circuit.py` AND being imported by `router/__init__.py` — fine, layered. If the new modules form circular imports, the split is wrong — re-think the seams.
6. Document the plan in chat for operator approval.

**Quality bar (Operation 1 done when)**:

- [ ] Source module enumerated (definitions, line counts, dependencies)
- [ ] Seams identified with reasoning (cohesion / callers / lifecycle / layer)
- [ ] Destination layout chosen (in-place / sibling / submodule)
- [ ] Each new module has a 1-sentence purpose
- [ ] No circular imports in the proposed layout
- [ ] Operator approved the plan

### Operation 2: Verify test coverage exists

**Trigger**: Operation 1 plan approved.

**Process**:

1. Find tests that exercise the source module:

   ```bash
   grep -rn "from aicp.core.router\|aicp.core.router\." tests/ 2>/dev/null
   pytest tests/ --collect-only -q 2>/dev/null | grep router
   ```

2. Run them with coverage:

   ```bash
   pytest tests/test_router*.py --cov=aicp.core.router --cov-report=term-missing 2>&1 | tail -20
   ```

3. If coverage is insufficient (lines being moved aren't exercised), STOP and load `quality-coverage` or `feature-test` to add coverage first. Refactoring uncovered code is silent regression risk.
4. Capture BASELINE: test count, pass rate, coverage % per file.

**Quality bar (Operation 2 done when)**:

- [ ] Tests exercising the source module identified
- [ ] Coverage on lines-to-move confirmed
- [ ] Baseline test count + coverage captured

### Operation 3: Apply the split in 4 sub-steps

**Trigger**: Operation 2 baseline confirmed.

**Process** (4 sub-steps, each in its own commit):

**Sub-step A: Create the new module(s) — empty shells**

1. For in-place split: `mkdir aicp/core/router/` then create `__init__.py` (initially re-exports everything from a temporary `_legacy.py`) + the planned new files (initially empty).
2. For sibling/submodule splits: just create the new files, empty.
3. The OLD module still works. New shells are dead code at this point.
4. Run tests — must still pass (the change is purely structural).
5. Lint passes.
6. Commit: `refactor(<scope>): scaffold split of <module> into <new layout>`.

**Sub-step B: Move the actual code** — one logical group per commit

1. Pick ONE responsibility group from Operation 1 (e.g., the scoring functions). Cut them from the source module, paste into the new module.
2. Update internal imports within the source module + new module. Use `from .X import Y` (relative imports for intra-package).
3. Update the `__init__.py` to re-export from the new module so external imports keep working: `from .scoring import compute_score`.
4. Run tests — must still pass.
5. Lint passes.
6. Commit: `refactor(<scope>): move <group> into <new module>`.
7. Repeat for each responsibility group. ONE commit per group, not one giant commit.

**Sub-step C: Update external imports (optional, can be separate task)**

1. Decide: do external callers update their imports now (`from aicp.core.router.scoring import compute_score` directly), OR keep using the old path (`from aicp.core.router import compute_score`) which works via `__init__.py` re-exports?
2. Recommendation: leave re-exports in place. Updating ALL external imports is high-churn for low value (the re-exports are stable). Update only when you're touching the caller for other reasons.
3. If you DO update some imports, run the tests after each batch.

**Sub-step D: Cleanup the temporary `_legacy.py` (if used)**

1. If Sub-step A used a `_legacy.py` shim, now that all responsibilities have moved, the shim is empty (or has only re-exports). Delete it.
2. Run tests.
3. Commit: `refactor(<scope>): remove legacy shim from split`.

**Quality bar (Operation 3 done when)**:

- [ ] Each sub-step committed independently with passing tests
- [ ] Each new module has its responsibility group + only that group
- [ ] `__init__.py` re-exports the public surface (external imports unchanged unless explicitly updated)
- [ ] No circular imports
- [ ] Test count unchanged from Operation 2 baseline
- [ ] Lint clean throughout

### Operation 4: Verify behavior preservation + close out

**Trigger**: Operation 3 sub-steps complete.

**Process**:

1. Final verification:
   - Full test suite: `pytest tests/ --tb=short` — exit 0, count unchanged
   - Lint: `ruff check + ruff format --check` — exit 0
   - Wiki lint (if AGENTS.md or CLAUDE.md mentioned the old structure, update):

     ```bash
     grep -rn "aicp/core/<old_module>\.py" AGENTS.md CLAUDE.md wiki/ 2>/dev/null
     ```

     For each match, update to reflect the new layout.
2. Update `wiki/config/domain-profiles/backend-ai-platform-python.yaml` if path patterns referenced the old module specifically (usually patterns are glob-based and unaffected).
3. If the split surfaced a SYSTEMIC pattern (e.g., "every backend file in `aicp/backends/` is starting to look like router did — they all need internal splits"), file as a follow-up task.
4. No standalone wiki page needed for routine splits — commit messages capture the refactor. EXCEPTION: if the split creates a new public package (with `__init__.py` exposing API), add a brief module-level docstring in `__init__.py` explaining the package's purpose and public surface.

**Quality bar (Operation 4 done when)**:

- [ ] Full suite + lint final-check pass
- [ ] AGENTS.md / CLAUDE.md / wiki references to old structure updated
- [ ] Domain profile path patterns confirmed still applicable
- [ ] Lesson contributed if systemic
- [ ] New package (if created) has docstring at `__init__.py` top

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Splitting along arbitrary lines (random groupings)

The temptation: file is 1200 lines, split into 4 modules of ~300 lines each. NO — splits should follow RESPONSIBILITY seams, not line counts. A 600-line module focused on one responsibility is fine; a 200-line module mixing 3 responsibilities is bad.

**Detection**: did Operation 1 step 2 identify seams BY RESPONSIBILITY (cohesion / callers / lifecycle / layer)? Or did you just chunk the file?

**The rule**: split where responsibilities diverge, not where line counts cross thresholds. A "too long" module that has only one responsibility is a candidate for `refactor-extract` (extract a few helpers), not `refactor-split`.

### Gotcha 2: Breaking external imports without re-exports (consumer breakage)

The temptation: split the module, update internal imports, ship it. External callers (other AICP modules, fleet's agent-tooling.yaml referencing skills, tests) suddenly fail with ImportError. You broke the public surface.

**Detection**: `grep -rn "from aicp.core.<old_module> import" aicp/ tools/ tests/ ../openfleet/ 2>/dev/null` — any matches?

**The rule**: `__init__.py` re-exports preserve the public surface. External imports keep working. Only update external imports as a SEPARATE pass with its own commits (Operation 3 Sub-step C).

### Gotcha 3: Circular imports between split modules (dead-on-arrival)

The temptation: cut the module along seams that LOOK clean, but the actual imports form a cycle: `scoring.py` imports `dispatch.py`, `dispatch.py` imports `circuit.py`, `circuit.py` imports `scoring.py`. Python detects circular imports at import time; the package doesn't load.

**Detection**: did Operation 1 step 5 verify the import graph is a DAG (no cycles)?

**The rule**: layer the new modules. Lower-level modules (scoring is data-driven, no I/O) at the bottom; higher-level modules (dispatch orchestrates) at the top. If you find a cycle, restructure the seams (often the seam itself is wrong).

### Gotcha 4: Splitting before testing (regression risk)

Same as `refactor-extract` Gotcha 1, applied at module scale. If the source module's lines aren't covered by tests, splitting can introduce silent regressions (different import order = different module-level state, different error wrapping, etc.).

**Detection**: Operation 2 confirmed coverage on lines being moved?

**The rule**: tests first, split second. The cost of pausing to add coverage is small; the cost of a silent split regression in production is large.

### Gotcha 5: One giant commit (un-revertable)

The temptation: do all 4 sub-steps in one commit because "they're all related." But if Sub-step C broke something, you can only revert THE WHOLE thing, losing Sub-steps A and B's work.

**Detection**: more than 5-10 files changed in a single commit on a refactor branch?

**The rule**: per Operation 3 — each sub-step is independently revertable. Each ends in a buildable + testable state.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Sibling skills**: [refactor-architecture](../refactor-architecture/SKILL.md) (package-level — multi-package restructure) and [refactor-extract](../refactor-extract/SKILL.md) (function-level — pull out one thing)
- **Real example**: this repo's CLAUDE.md slim (646→265 lines) was a hybrid — content extraction (move sections to AGENTS.md) + structural reduction. See git history for the multi-step pattern this skill formalizes.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP convention (CLAUDE.md): "Keep modules small and focused. One responsibility per file." Splits enforce this. Common AICP split candidates: `aicp/core/router.py` (scoring + dispatch + circuit + escalation), `aicp/core/controller.py` (mode enforcement + dispatch + events).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| refactor-extract | extract a function/class within a file | Function-level; this skill is module-level |
| refactor-architecture | restructure packages | Package-level; this skill is module-level |
| refactor-rename | lexical rename | Mechanical; this skill is structural |
| refactor-patterns | apply a design pattern | Pattern-level |
| refactor-dependencies | dep hygiene | Different scope |
| feature-implement | new behavior | Refactor preserves behavior |
| quality-audit | umbrella that surfaces split candidates | Sibling — audit identifies need; this skill executes |
