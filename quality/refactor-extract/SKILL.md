---
name: refactor-extract
description: Extract a function, method, class, or constant from inline code into its own named definition (and optionally its own module) — without changing behavior. The smallest-scope refactor skill — sibling to refactor-split (whole module) and refactor-architecture (package). Loads when the operator says "extract this into a function" / "pull X out" / "give this a name" / "duplicate logic should be one function".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# refactor-extract

The smallest-scope refactor skill. Extract one logical unit (function /
method / class / constant / type alias) from inline code into its own named
definition. Optionally relocate the new definition to its own module if
that's where it logically belongs.

This is the everyday refactor skill — most refactor work is extraction, not
package restructuring. Use this when: a function is too long, the same
logic appears in 2+ places, an inline expression is hard to read, a magic
constant would benefit from a name, an inline class would be cleaner as
its own definition.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "extract this into a function", "pull X out", "give this a name", "duplicate logic should be one function", "this expression is too dense", "factor out the common code"
- **Code review feedback**: a reviewer flags duplicated logic, an overly long function, or an unnamed magic value
- **Quality-coverage finding**: a coverage gap is in a long function whose individual paths can't be tested in isolation — extracting the paths makes them testable
- **Quality-lint finding**: a complexity rule (e.g., function too long, cyclomatic complexity too high) — extraction usually fixes it
- **From quality-debt review**: a TODO marker says "// TODO: extract this when we have time"

Do NOT load when:

- A whole module needs splitting (load `refactor-split` — sibling skill)
- Package boundaries need restructuring (load `refactor-architecture` — larger sibling)
- A symbol just needs renaming (load `refactor-rename` — different operation)
- Behavior needs to change (load `feature-implement` — refactor preserves behavior)
- A pattern needs applying (load `refactor-patterns`)

## Operations

This skill has 4 named operations.

### Operation 1: Identify the extraction + behavior contract

**Trigger**: skill loaded; extraction candidate identified.

**Process**:

1. Read the source location. Capture: the file, line range, what the inline code does (in your own words), what inputs it consumes, what outputs it produces, what side effects it has.
2. Identify the BEHAVIOR PRESERVATION contract. The extracted unit must produce IDENTICAL outputs + side effects for ALL valid inputs as the inline code did.
3. Choose the extraction shape:
   - **Function**: most common. Pure or nearly-pure logic. Inputs become parameters; output becomes return value; side effects stay explicit.
   - **Method**: when the extracted logic naturally belongs on an existing class (operates on its state).
   - **Class**: when the extracted logic carries state across multiple calls OR represents a coherent domain concept worth naming.
   - **Constant / type alias**: when extracting a magic value or repeated type signature.
4. Choose the destination:
   - **Same module**: default. Extracted unit lives next to its caller.
   - **New module**: when the extracted unit will be imported by 2+ files OR represents a cross-cutting concern (e.g., a utility used by `aicp/core/` AND `aicp/backends/`).
   - **Existing utility module**: when there's already a natural home (`aicp/core/<topic>.py`).
5. Verify destination doesn't already have a function with the same name (avoid silent shadowing). `grep -n "def <name>\|class <name>" <destination_file>`.
6. Document the plan in chat for operator approval before any code change.

**Quality bar (Operation 1 done when)**:

- [ ] Source location identified (file:line range)
- [ ] Inline code's behavior described in own words (inputs / outputs / side effects)
- [ ] Extraction shape chosen (function / method / class / constant) with reason
- [ ] Destination chosen (same module / new module / existing module) with reason
- [ ] No name collision at destination
- [ ] Operator approved the plan

### Operation 2: Verify test coverage exists for the source

**Trigger**: Operation 1 plan approved.

**Process**:

1. Find tests that exercise the source code path:

   ```bash
   # If extracting from aicp/core/router.py L100-150
   grep -rn "from aicp.core.router import\|aicp.core.router\." tests/ 2>/dev/null
   ```

2. Run the relevant tests; capture pass count + coverage of the source lines:

   ```bash
   pytest tests/test_router.py --cov=aicp.core.router --cov-report=term-missing 2>&1 | tail -20
   ```

3. If coverage on the lines being extracted is INSUFFICIENT (lines not exercised by any test), STOP. Refactoring uncovered code means there's no signal if the refactor breaks behavior. Either:
   - **Pause the extraction**, load `quality-coverage` or `feature-test` to add tests covering the source lines, then resume here.
   - **Accept the risk**, document explicitly in the commit message ("refactor without coverage — risk accepted because <reason>"), and verify behavior manually.

   The DEFAULT is pause + add tests. Only accept the risk if the operator explicitly chooses.
4. Capture the BASELINE: test count + which tests exercise the source. The same tests must pass after extraction.

**Quality bar (Operation 2 done when)**:

- [ ] Tests exercising the source lines identified
- [ ] Coverage on extracted lines confirmed (or risk explicitly accepted)
- [ ] Baseline test count captured

### Operation 3: Apply the extraction in 3 sub-steps

**Trigger**: Operation 2 baseline confirmed.

**Process** (3 sub-steps, each in its own commit):

**Sub-step A: Add the new definition** (without removing the inline code)

1. Add the extracted function/method/class/constant at the destination. Give it a clear name (per AICP conventions: snake_case for functions, PascalCase for classes, UPPER_SNAKE_CASE for constants).
2. Add a one-line docstring explaining WHY (not what — the code shows what). For utility functions, often the name + signature is self-explanatory; skip the docstring rather than add filler.
3. Ensure the new definition is INDEPENDENTLY callable: type hints on parameters, type hint on return, no implicit dependencies on caller-local state.
4. Run lint: `ruff check + ruff format --check` on the modified files.
5. Commit: `refactor(<scope>): add <name> for upcoming extraction`. Note: tests still passing because nothing yet calls the new definition (or nothing calls it externally — caller still has inline code).

**Sub-step B: Replace the inline code with a call**

1. At the source location, replace the inline code with a call to the new definition. Pass the right inputs; receive the right outputs.
2. Run the previously-identified tests: `pytest <those tests> --tb=short`. ALL MUST PASS. If any fail, the extraction has a behavior change — either fix the new definition OR fix the call site OR rollback (revert this sub-step) if you can't reconcile.
3. Run the FULL test suite (`pytest tests/ --tb=short`) for safety — extraction sometimes affects other code paths through import side effects.
4. Run lint again.
5. Commit: `refactor(<scope>): use <name> in place of inline code`.

**Sub-step C: Remove duplicate inline code from other call sites (if any)**

1. If the original motivation was deduplication, find OTHER inline copies of the same logic and replace them with calls to the new definition too. One commit per replacement keeps reviewable diffs.
2. After each replacement: relevant tests + full suite. Same gate as Sub-step B.

**Quality bar (Operation 3 done when)**:

- [ ] Sub-step A: new definition added; tests still pass; commit landed
- [ ] Sub-step B: inline code replaced; relevant + full suite pass; commit landed
- [ ] Sub-step C (if applicable): all duplicate sites replaced; tests pass after each
- [ ] Lint clean throughout
- [ ] Test count unchanged from Operation 2 baseline

### Operation 4: Verify behavior preservation + close out

**Trigger**: Operation 3 sub-steps complete.

**Process**:

1. Final verification:
   - Full test suite: `pytest tests/ --tb=short` — exit 0, count unchanged
   - Lint: `ruff check + ruff format --check` — exit 0
   - For hot paths: run a representative request through the changed code (e.g., `aicp --route "test"` if router was touched). Confirm output structure unchanged.
2. Update any callers' docstrings or comments that referenced the inline code. Stale references ("see the function above for details" when "above" is now `from .X import Y`) confuse future readers.
3. If the extraction surfaced a SYSTEMIC pattern (e.g., "this duplication came from copy-paste-then-tweak across 5 backends — should standardize backend interface"), file as a follow-up task or contribute as a lesson.
4. No standalone wiki page needed for routine extractions — the commit messages capture the refactor. EXCEPTION: if the extraction creates a new utility module that other modules will import, add a brief docstring at module top explaining the module's purpose.

**Quality bar (Operation 4 done when)**:

- [ ] Full suite + lint final-check pass
- [ ] Hot path manually verified (if applicable)
- [ ] Stale references in comments/docstrings updated
- [ ] Lesson contributed if systemic
- [ ] New module (if created) has top-of-file docstring

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Extracting without tests (silent regression)

The temptation: the inline code "looks simple," extracting it "obviously preserves behavior." NO — extraction often subtly changes behavior (different default for a kwarg, different ordering, different exception type wrapped in a different way). Without tests, the regression ships.

**Detection**: Operation 2 step 3 — did you confirm tests cover the extracted lines?

**The rule**: extract WITH coverage. If coverage is missing, either pause to add tests or explicitly document the risk in the commit message. Default is "pause and add tests."

### Gotcha 2: Extracting too eagerly (one-call-site noise)

The temptation: extract every function that's >20 lines because "long is bad." But extraction has a cost: every extracted function adds an indirection that future readers must follow. A 30-line function called from one place is often clearer than a 10-line caller + 20-line helper.

**Detection**: did the extracted function get called from MORE than one place? Or only from one?

**The rule**: extract for ONE of these reasons: (a) deduplication (called from 2+ places), (b) testability (the inline code can't be tested in isolation), (c) clarity (the inline expression is hard to understand and a name helps). Length alone isn't a reason.

### Gotcha 3: Mixing extraction with other changes (scope creep)

The temptation: while extracting, you spot a bug in the logic. Tempting to fix it. NO — the extraction commit must preserve behavior. Bug fix is a separate commit (separate task) so reviewers can see what changed where.

**Detection**: the diff for the extraction commit includes any logic change beyond mechanical move + parameter passing.

**The rule**: extraction commits are pure structural change. Spotted bugs become follow-up tasks.

### Gotcha 4: Naming the extracted function poorly (worse than inline)

The temptation: extracting `if x > 5 and y < 10` into `def check_x_y(x, y)`. The function name doesn't say what the check MEANS — it just describes the parameters. The original inline code was at least specific about the comparison.

**Detection**: would a future reader understand the extracted function's PURPOSE from its name + signature alone? If not, the name is generic.

**The rule**: extracted names describe MEANING, not mechanism. `is_within_threshold(x, y)` or `passes_validation(x, y)` is better than `check_x_y`. If you can't think of a meaningful name, the extraction may not be ready (or the underlying concept isn't crisp enough yet).

### Gotcha 5: Extracting to a wrong-layer module (architecture drift)

The temptation: the extracted utility "could go anywhere." Pick the closest existing file. But that file is in `aicp/cli/` and the utility is now used by `aicp/core/router.py` — meaning core depends on cli. Layering violation.

**Detection**: did the new dependency direction make sense (lower layer to upper layer)? Or did extraction create a higher-layer-imports-from-lower-layer reverse dependency?

**The rule**: extracted utilities go in the LOWEST layer that needs them. If `core/` and `cli/` both need it, the utility goes in a shared lower-layer module (`aicp/core/utils.py` or a new `aicp/common/`). Never in `cli/` if `core/` will import it.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Real extraction example** (this repo): see git log for any commit prefixed `refactor:` — most are extractions
- **Sibling skill**: [refactor-architecture](../refactor-architecture/SKILL.md) for package-level structural refactor (this skill's larger scope sibling)
- **Sibling skill**: [refactor-split](../refactor-split/SKILL.md) for module-level split (this skill's same-scope sibling)

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP-specific concerns: prefer composition over inheritance (CLAUDE.md convention); maintain Python type hints on extracted public signatures; keep modules small (one responsibility).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| refactor-split | split a whole module that's too big | Module-level; this skill is function/class-level |
| refactor-architecture | restructure packages | Package-level; this skill is finest grain |
| refactor-rename | lexical rename | Mechanical; this skill is structural extraction |
| refactor-patterns | apply a design pattern | Pattern-level; this skill is mechanical extraction |
| refactor-dependencies | dep hygiene | Different scope (deps vs code structure) |
| feature-implement | new behavior | Refactor preserves behavior; feature adds |
| quality-coverage | testing gaps surfaced this extraction | Sibling — coverage often motivates extraction |
| quality-lint | complexity rule fired | Sibling — lint often motivates extraction |
