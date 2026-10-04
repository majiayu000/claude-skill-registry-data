---
name: refactor-rename
description: Rename a symbol (function, class, variable, constant, file, directory) consistently across the AICP codebase — call sites, imports, tests, docs, configs. Behavior-preserving, fully traced. Smaller-scope sibling to refactor-extract (extract a definition) and refactor-split (split a module). Loads when the operator says "rename X to Y" / "this name is wrong" / "consistent rename across codebase" / "I changed X's name in module A but missed call sites".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# refactor-rename

Rename a symbol (function, class, variable, constant, file, directory)
across the AICP codebase consistently — every call site, import, test,
doc, and config that references the old name updates to the new name.
Behavior-preserving by definition; the goal is name change with zero
semantic drift.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "rename X to Y", "this name is wrong",
  "the function is misnamed", "I want to rename this variable across
  the codebase", "consistent rename"
- **Drift detection**: operator notices that a symbol was renamed in one
  place but call sites still use the old name (silent breakage or shadowing)
- **Naming alignment**: bringing a symbol's name in line with project
  conventions (e.g., snake_case enforcement, removing legacy prefixes)
- **Pre-merge cleanup**: a feature branch named things one way and the
  merge target uses different naming — reconcile before merge

Do NOT load when:

- The intent is to extract a function/class (load `refactor-extract` —
  rename is just one side effect of extraction)
- The intent is to split a module (load `refactor-split` — rename may
  happen as part of move)
- The intent is architectural restructuring (load `refactor-architecture`)
- The intent is changing BEHAVIOR, not just NAME (this skill is strictly
  rename; behavior changes load `feature-implement` instead)

## Operations

### Operation 1 — Find all references to the symbol being renamed

**When**: before any rename, enumerate every call site so the operator
sees the full scope.

**Process**:

1. Identify the symbol's current name AND scope (e.g., is it
   `aicp.core.router.score_complexity` or just any function named
   `score_complexity`?)
2. Use `Grep` for the symbol name (not Bash `grep`):
   - Function/method: `Grep "<name>\b"` with `type: py` to filter
   - Class: same — class names are uppercase by convention
   - Variable: same, but be wary of shadowing in different scopes
   - Constant: typically ALL_CAPS — easier to disambiguate
3. Filter results: distinguish DEFINITION sites vs CALL sites vs IMPORT
   sites vs DOC mentions
4. Report counts per category to the operator before proceeding

**Quality bar**: never proceed to Operation 2 without the operator confirming
the enumeration is complete. False negatives (missed call sites) cause
silent breakage; false positives (renaming an unrelated same-named symbol)
cause introduced bugs.

### Operation 2 — Apply the rename consistently

**When**: enumeration is verified, operator approved the new name.

**Process**:

1. Rename the DEFINITION first (function/class declaration line)
2. Rename CALL SITES — use `Edit` with `replace_all: true` IF the
   symbol name is unambiguous in the file; otherwise per-occurrence
3. Rename IMPORTS — `from aicp.X import old_name` → `from aicp.X import new_name`,
   plus any `import aicp.X.old_name` aliases
4. Rename DOC MENTIONS — CLAUDE.md, AGENTS.md, README, wiki/ pages,
   other SKILL.md files that reference the symbol
5. Rename TEST FIXTURES — test file names if symbol-specific; test
   function names if they reference the renamed symbol
6. Rename CONFIG REFERENCES — `config/*.yaml` keys/values that name the
   symbol (uncommon but possible for plugin/skill systems)

**Quality bar**: after all renames, run `Grep "<old-name>\b"` again — should
return zero hits. ANY remaining hit means a missed reference.

### Operation 3 — Verify behavior preservation

**When**: rename complete, before declaring done.

**Process**:

1. Run AICP's test suite: `pytest` — if any test fails that previously
   passed, the rename was NOT behavior-preserving (likely a missed call
   site or a renamed-but-still-used import alias)
2. Run linter: `ruff check aicp/ tests/` — catches reference errors
   that pytest may not exercise
3. If AICP CLI was affected: live-test the relevant CLI command (e.g.,
   if router was renamed, run `aicp --check`)
4. If tests pass and linter is clean: rename is behavior-preserving

**Quality bar**: NEVER skip the test+lint verification. A rename that
"looks" complete can have residual references in execution paths the
unit tests don't cover.

### Operation 4 — Rename a file or directory

**When**: the rename target is a file/directory, not a symbol within a file.

**Process**:

1. Use `git mv` (not Bash `mv`) to preserve git history:
   `git mv aicp/old_path/old_file.py aicp/new_path/new_file.py`
2. Update ALL imports of the renamed module:
   `Grep "from aicp.old_path"` → fix each occurrence
3. Update __init__.py exports if applicable
4. Update CLAUDE.md / AGENTS.md / wiki/ references to the file path
5. Verify with pytest + ruff per Operation 3

**Quality bar**: file renames break more places than symbol renames
because the import path changes. Always run the verification step.

## Gotchas

- **Detection**: agent uses Bash `grep` instead of the Grep tool.
  **Rule**: NEVER use Bash `grep`/`rg` — use the Grep tool.
  **Reasoning**: per CLAUDE.md, Grep is permission-managed and ripgrep-backed;
  Bash variants miss permissions and are slower.

- **Detection**: agent uses `Edit` with `replace_all: true` on a generic name (e.g., `result`, `data`, `cfg`).
  **Rule**: only use `replace_all` when the symbol name is unambiguous in
  the file. Generic names need per-occurrence Edit calls with sufficient context.
  **Reasoning**: replace_all on `result` would rename every `result` variable,
  not just the one you wanted. The Edit tool's `replace_all` is for unique
  symbols.

- **Detection**: agent renames the definition but skips imports.
  **Rule**: imports are part of the rename — `from aicp.X import old_name`
  fails after `old_name` is renamed.
  **Reasoning**: Python doesn't auto-update imports. Missing the import
  rename causes ImportError at runtime, not at edit time.

- **Detection**: agent skips the test+lint verification.
  **Rule**: every rename runs through pytest + ruff before declaring done.
  **Reasoning**: a "looks complete" rename can have residual references in
  execution paths unit tests don't exercise. The verification gate catches them.

- **Detection**: agent uses Bash `mv` for file renames instead of `git mv`.
  **Rule**: file renames use `git mv` to preserve history.
  **Reasoning**: `git mv` records the rename in git history; `mv` followed
  by `git add` records as delete+create, losing the connection between
  old and new for blame/log.

- **Detection**: agent renames a symbol that has multiple definitions across packages (e.g., two functions both named `validate`).
  **Rule**: scope-disambiguate FIRST. Either `aicp.X.validate` vs `aicp.Y.validate`
  is the answer (they're distinct), or one of them needs renaming separately.
  **Reasoning**: Python's namespace allows multiple `validate` functions;
  the rename must be scope-specific or it breaks unrelated callers.

## Reference exemplars

- AICP's CLI dispatcher pattern in `aicp/cli/main.py` — large surface
  area of named handlers, common rename target as the API evolves
- `aicp/core/skills.py` skill name resolution — naming conventions
  for skills (`aicp-ops-*`, `feature-*`, `quality-*`)
- `wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md`
  — example of a rename motivated by alignment with second-brain naming

## Domain context

AICP is a 61-module Python codebase (~94 test files, 1,758 tests) with
strong naming conventions: snake_case functions/variables, PascalCase
classes, ALL_CAPS constants, kebab-case skills. Renames must respect
those conventions or they violate `quality-lint` (ruff config). The
test suite is the verification floor — all renames must keep `pytest`
green.

## Related skills

| Skill | When to use |
|-------|-------------|
| `refactor-extract` | When extracting a NEW definition from inline code (rename + extract is a different op) |
| `refactor-split` | When splitting a module (file moves are involved, often with renames) |
| `refactor-architecture` | When the rename is part of a larger package-level restructuring |
| `quality-lint` | When verifying ruff catches naming issues post-rename |
| `feature-test` | When the rename touches a feature in active development |
