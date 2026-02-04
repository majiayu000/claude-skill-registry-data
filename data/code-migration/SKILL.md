---
name: code-migration
description: Use when moving logic between layers, deprecating patterns, refactoring responsibilities, or enforcing canonical owners. Ensures migrations are complete with no legacy coexistence.
---

# Code Migration

**Core principle:** When you move responsibility from A to B, delete A.

Half-migrations are technical debt. If `files_helper.py` and `path_comp.py` both construct paths, every developer must learn *which one to use*. That ambiguity is the bug.

---

## Migration Checklist

When moving logic from one location to another:

- [ ] **Move the code** to its canonical location
- [ ] **Update all call sites** (use grep, not hope)
- [ ] **Update skills** that reference the old location
- [ ] **Add ruff rules** to ban imports from the old location
- [ ] **Delete the old code** (not deprecate - delete)
- [ ] **Run validate_skills.py** to catch stale references
- [ ] **Run tests** to confirm nothing broke

If you can't check all boxes, the migration isn't done.

---

## Canonical Owners

Every responsibility has exactly ONE canonical owner:

| Responsibility | Canonical Owner | NOT |
|---------------|-----------------|-----|
| Library path construction | `path_comp.py` | `files_helper.py` |
| Wall-clock timestamps | `time_helper.now_ms()` | `time.time()` |
| Monotonic intervals | `time_helper.internal_ms()` | `time.monotonic()` |
| Essentia calls | `ml_backend_essentia_comp.py` | anywhere else |
| Logging setup | `logging_helper.get_logger()` | `logging.getLogger()` |
| Config access | Injected `AppConfig` | `os.environ`, `config.yaml` |

**If two places can do the same thing, one of them is wrong.**

---

## Enforcement Stack

Migrations are enforced at every layer:

### 1. Ruff Rules (Syntax-Level)

Ban dangerous imports before code runs:

```toml
# ruff.toml
[lint.flake8-tidy-imports.banned-api]
"time.time".msg = "Use nomarr.helpers.time_helper.now_ms() for timestamps"
"builtins.print".msg = "Use logging via get_logger()"
```

### 2. Import-Linter (Architecture-Level)

Prevent layer violations:

```
helpers cannot import from services
workflows cannot import from interfaces
only ml_backend_essentia_comp.py may import essentia
```

### 3. Skills (Documentation-Level)

Every skill documents what IS canonical, not what WAS.

### 4. validate_skills.py (Tooling-Level)

Catches stale references in skills:

```bash
python scripts/validate_skills.py --check-refs
```

---

## Anti-Patterns

### Deprecation Warnings

```python
# ❌ Wrong - deprecation is procrastination
import warnings
warnings.warn("Use path_comp instead", DeprecationWarning)
```

If it's deprecated, delete it. Pre-alpha means no backwards compatibility.

### Keeping It Around Just In Case

```python
# ❌ Wrong - dead code that looks alive
def old_path_builder(path: str) -> str:
    """DEPRECATED: Use path_comp.build_library_path_from_input()"""
    ...
```

Delete it. Git remembers.

### TODO: Remove After Migration

```python
# ❌ Wrong - TODOs are lies
# TODO: Remove this once all callers use the new API
def legacy_function():
    ...
```

Remove it now. The migration isn't done until it's gone.

### Wrapper For Compatibility

```python
# ❌ Wrong - shims become permanent
def get_path(path: str) -> str:
    """Compatibility wrapper."""
    return path_comp.build_library_path_from_input(path).absolute
```

Update the callers directly.

---

## Migration Workflow

### Step 1: Identify the Migration

```bash
# Find all usages of the old pattern
python scripts/discover_import_chains.py nomarr.helpers.files_helper

# Or grep for specific functions
grep -r "build_path" nomarr/
```

### Step 2: Create the Canonical Location

Move the logic to its proper layer (components for business logic, helpers for pure utilities).

### Step 3: Update All Call Sites

```bash
# Find all files that import the old module
grep -r "from nomarr.helpers.files_helper import" nomarr/
```

### Step 4: Ban the Old Pattern (If Still Exists)

If old code still exists and has callers, add a temporary ruff ban to prevent new usages:

```toml
# Add to ruff.toml during migration
[lint.flake8-tidy-imports.banned-api]
"nomarr.helpers.files_helper.build_path".msg = "Use path_comp.build_library_path_from_input()"
```

**Remove the ban after deleting the old code.** Bans for deleted patterns are garbage.

### Step 5: Delete the Old Code

```bash
git rm nomarr/helpers/old_module.py
```

### Step 6: Update Skills

```bash
python scripts/validate_skills.py --check-refs
```

### Step 7: Verify Migration Complete

```bash
# Check that all traces are gone
python scripts/check_migration.py nomarr.helpers.old_module

# If migration plan included a ruff ban, verify it exists
python scripts/check_migration.py nomarr.helpers.old_module --expect-ban

# Full QC
python scripts/run_qc.py
pytest
```

---

## Decision Framework

When you find duplicate responsibilities:

```
Q: Is there a clear canonical owner?
├─ No  → Decide which location should own it
└─ Yes → Q: Does the old location still exist?
         ├─ Yes → Delete it. Update callers first if needed.
         └─ No  → Good. Verify skills and rules match reality.
```

When someone proposes keeping both:

```
"Can we keep the old one for compatibility?"
→ No. Pre-alpha. Delete it.

"What if something still uses it?"
→ Find it and update it. That's the migration.

"What if we need it later?"
→ Git remembers. Delete it.
```

---

## Validation

Before considering a migration complete, run:

```bash
python scripts/check_migration.py nomarr.old.pattern
```

The script validates:
- [ ] Old code is **deleted**, not deprecated
- [ ] No imports of the old module remain
- [ ] No skill references to old pattern
- [ ] No `# TODO: remove` comments remain
- [ ] (With `--expect-ban`) Ruff ban exists

Manual checks:
- [ ] No wrapper/shim functions exist
- [ ] Tests pass

**The migration is done when there's no trace of the old pattern.**
