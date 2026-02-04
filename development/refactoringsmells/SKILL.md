---
name: refactoring/smells
description: Code Smells refactoring skill
---

# Code Smells

Checklist of code smells to identify during refactoring. Both generic C issues and ikigai-specific violations.

## Generic C Code Smells

### Function-Level

| Smell | Signal | Action |
|-------|--------|--------|
| Long function | >50 lines | Extract functions by responsibility |
| Deep nesting | >3 levels | Extract inner logic, use early returns |
| Long parameter list | >4 params | Introduce parameter object (struct) |
| Magic numbers | Literal values in logic | Define named constants |
| Duplicate code | Copy-pasted blocks | Extract shared function |
| Comments explaining what | `// increment counter` | Rename to be self-documenting |
| Dead code | Unreachable branches | Delete it |
| Complex conditionals | `if (a && b \|\| c && !d)` | Extract to named boolean or function |

### Structural

| Smell | Signal | Action |
|-------|--------|--------|
| God struct | Struct with 10+ fields | Split by responsibility |
| Feature envy | Function uses another module's data extensively | Move function to that module |
| Primitive obsession | Passing raw `char*`, `int` everywhere | Introduce domain types |
| Shotgun surgery | One change requires editing many files | Consolidate related code |
| Divergent change | One file changes for unrelated reasons | Split by responsibility |

## ikigai-Specific Violations

### Naming

| Violation | Example | Fix |
|-----------|---------|-----|
| Missing `ik_` prefix | `config_load()` | `ik_cfg_load()` |
| Wrong abbreviation | `ik_configuration_load()` | `ik_cfg_load()` (use approved abbrev) |
| Inconsistent module prefix | `ik_config_load()` vs `ik_cfg_parse()` | Pick one, use consistently |
| Missing `_ptr` suffix | `bool *visible;` (raw pointer) | `bool *visible_ptr;` |
| Missing `g_` prefix | `volatile sig_atomic_t shutdown;` | `g_shutdown` |

### Error Handling

| Violation | Example | Fix |
|-----------|---------|-----|
| Unchecked res_t | `ik_cfg_load(...); use(cfg);` | `TRY(ik_cfg_load(...))` or check `is_err()` |
| Wrong mechanism | `if (!ptr) return ERR(...)` for OOM | OOM → `PANIC()`, not res_t |
| assert for runtime | `assert(file_exists(path))` | External input → res_t, not assert |
| Missing LCOV marker | `if (!ptr) PANIC("OOM");` | Add `// LCOV_EXCL_BR_LINE` |
| Error on wrong context | `ERR(tmp, ...)` before `talloc_free(tmp)` | Use parent context for errors |

### Memory (talloc)

| Violation | Example | Fix |
|-----------|---------|-----|
| malloc instead of talloc | `char *buf = malloc(size);` | `talloc_array(ctx, char, size)` |
| Missing parent | `talloc_new(NULL)` in non-main | Pass parent context from caller |
| Orphaned allocation | `talloc(ctx, ...)` never freed/stolen | Attach to proper parent or free |
| Hidden allocation | Function mallocs internally | Accept `TALLOC_CTX*` parameter |

### Dependency Injection

| Violation | Example | Fix |
|-----------|---------|-----|
| Global state | `static config_t *g_config;` | Pass config as parameter |
| Hidden I/O | `load_from_disk()` inside init | Load externally, pass data in |
| Service locator | `get_service("db")` | Pass `db_t*` parameter |
| Constructor does work | `init()` opens files, connects | Accept opened resources as params |

### Style

| Violation | Example | Fix |
|-----------|---------|-----|
| Block comment | `/* comment */` | `// comment` |
| Primitive type | `int count;` | `int32_t count;` |
| Wrong include order | System before project headers | Project headers first |
| static helper function | `static void helper() {...}` | Inline at call site |

## Investigation Workflow

1. **Scan for patterns** - Use grep/search for smell signals
2. **Triage by impact** - Fix high-frequency smells first
3. **Verify with tests** - Ensure refactoring doesn't break behavior
4. **One smell at a time** - Don't mix refactoring types in one commit
