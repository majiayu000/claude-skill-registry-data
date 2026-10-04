---
name: linting
description: Code formatting and linting context for the Megahub project. Use when writing or reviewing code in C++ or JavaScript, or when running format/lint checks. Describes tool commands, style conventions, and when to apply them.
---

# Linting & Formatting — Megahub

## Tools

| Layer | Tool | Config file | Purpose |
|-------|------|-------------|---------|
| C++ | `clang-format` | `/.clang-format` | Code formatting |
| C++ | `cppcheck` | — (run manually) | Static analysis |
| JS/CSS | Prettier | `/frontend/prettier.config.js` | Code formatting |
| JS | ESLint v9 | `/frontend/eslint.config.js` | Bug detection |
| Pre-commit | lefthook | `/lefthook.yml` | Runs all checks on staged files |

---

## Running Tools

### JavaScript (run from `frontend/`)

```sh
npm run lint           # ESLint check (errors and warnings)
npm run lint:fix       # ESLint auto-fix where possible
npm run format         # Prettier — write formatted output
npm run format:check   # Prettier — check only (no writes)
```

### C++ (run from project root)

```sh
# Format a single file in-place
clang-format -i lib/megahub/src/megahub.cpp

# Check all lib and src files without modifying
find lib src -name "*.cpp" -o -name "*.h" | xargs clang-format --dry-run --Werror

# Static analysis
cppcheck --enable=warning,performance,portability \
         --suppress=missingInclude \
         --suppress=unusedFunction \
         --suppress=ctuOneDefinitionRuleViolation \
         --inline-suppr \
         --error-exitcode=1 \
         --quiet \
         lib/btremote lib/commands lib/configuration lib/hubwebserver \
         lib/i2csync lib/imu lib/inputdevices lib/logging lib/lpfuart \
         lib/megahub lib/portstatus lib/statusmonitor \
         src/
```

---

## When to Apply

- **After writing any JS code**: run `npm run format` then `npm run lint` from `frontend/`
- **After writing any C++ code**: run `clang-format -i` on the modified files
- **The pre-commit hook runs automatically** on staged files if lefthook is installed

---

## Pre-commit Hook Setup (one-time)

```sh
brew install lefthook   # macOS
lefthook install        # registers the git hooks
```

After this, every `git commit` automatically checks:
- C++ staged files → clang-format (fails if unformatted)
- JS staged files → ESLint (fails on errors)
- JS/CSS staged files → Prettier (fails if unformatted)
