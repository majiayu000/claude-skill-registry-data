---
name: auto-duplicate-fixer
description: Automate detection and removal of duplicate files/functions in TypeScript, JavaScript, and Python projects. Safely refactor imports, validate with tests, and deploy changes with zero risk of breaking the system.
---

# Skill: Auto Duplicate File Fixer (TS/JS + Python)

## Purpose
Automate detection and removal of duplicate files/functions in TypeScript, JavaScript, and Python projects. Safely refactor imports, validate with tests, and deploy changes with zero risk of breaking the system.

Designed for **daily incremental fixes** that keep architecture clean without chaos.

## Inputs
- `project_root`: Path to project
- `mode`: 'daily' | 'aggressive' | 'analysis' (default: 'daily')
- `--dry-run`: Preview only, don't modify

## Outputs
- `.duplicate-report.json`: Detection results
- `.keep-remove-map.json`: Decision mapping (keep/remove)
- `.refactor-log.json`: Files changed, imports updated
- `.validation-log.json`: Test/lint/build results
- `.deploy-log.json`: Commit/PR status
- `.pipeline-log.json`: Full execution log

## Pattern Standards (TS/JS)
- Named exports preferred over default exports
- Imports: absolute paths or aliases (no relative > 2 levels)
- 1 file = 1 responsibility
- Utility functions: centralize in `src/utils` or `src/services`
- No duplicate functions across `src/helpers`, `src/utils`, `src/services`

Naming convention:
```
src/
  utils/        # General utilities (helper.ts, formatter.ts)
  helpers/      # (DEPRECATED: merge to utils)
  services/     # Business logic (userService.ts, authService.ts)
  hooks/        # React hooks
  components/   # UI components
  constants/    # Constants
```

## Pattern Standards (Python)
- PEP8 compliance
- All functions/classes: must have docstring
- No duplicate logic across modules
- Centralize utils in `/common` or `/core` package

Example structure:
```
src/
  common/       # Shared utilities (helpers.py, validators.py)
  core/         # Core business logic
  services/     # Service classes
  models/       # Data models
```

## Procedure

### Phase 1: Detect Duplicates
**Command**: `npm run check <project> -- --format=json --min-tokens=50`

**Alternative (direct)**: `node scripts/detect.js <project> --format=json --min-tokens=50`

Process:
- Scan all `.ts`, `.tsx`, `.js`, `.jsx`, `.py` files
- Compute MD5 hashes → find identical files
- Use jscpd → find structural duplicates (80%+ similarity)
- Use AST → find function/class duplicates (Python)
- Output: `.duplicate-report.json`

Tools:
- `jscpd`: Copy-paste detection
- `ts-morph` / `babel`: AST parsing
- `python ast`: Python structural analysis

### Phase 2: Decide (Keep/Remove)
**Command**: `npm run decide <project> -- --report=.duplicate-report.json --strategy=test-coverage-first`

**Alternative (direct)**: `node scripts/decide.js <project> --report=.duplicate-report.json --strategy=test-coverage-first`

Decision ranking (highest score wins):
1. **Test Coverage** (×3): # of test cases / describe blocks
2. **Import Count** (×2): How many files depend on this
3. **Type Definitions** (+5 if present): Has interface/type annotations (TS only)
4. **Naming Convention** (+3): Follows src/ conventions

Example:
```
File A (helper.ts):
  - 5 test cases → 15 points
  - imported by 3 files → 6 points
  - has types → 5 points
  - follows convention → 3 points
  Total: 29 points

File B (helpers/util.ts):
  - 0 tests → 0 points
  - imported by 1 file → 2 points
  - no types → 0 points
  - doesn't follow convention → 0 points
  Total: 2 points

Decision: KEEP A, REMOVE B
```

Output: `.keep-remove-map.json`

### Phase 3: Refactor Imports & Delete
**Command**: `npm run refactor <project>`

**Alternative (direct)**: `node scripts/refactor.js <project>`

Process:
1. Find all files importing removed files
2. **TS/JS**: Update import paths (handle variants: relative, absolute, index files)
3. **Python**: Update `import x` and `from x import y` statements
4. Delete removed files
5. Update barrel files (`index.ts`, `__init__.py`)
6. Output: `.refactor-log.json`

Safety checks:
- Dry-run all import replacements first
- Preserve import semantics (named vs default)
- Handle circular dependencies

### Phase 4: Validate
**Command**: `npm run validate <project>`

**Alternative (direct)**: `bash scripts/validate.sh <project>`

Validation stack:
- **Tests**: `npm run test:ci` / `pytest`
- **TypeCheck**: `tsc --noEmit`
- **Lint**: `eslint` / `flake8`
- **Build**: `npm run build`

If ANY fails:
- Rollback via `git checkout -- .`
- Log errors in `.validation-log.json`
- Exit with status 1

Output: `.validation-log.json`

### Phase 5: Deploy
**Command**: `npm run deploy <project> -- --auto-merge`

**Alternative (direct)**: `node scripts/deploy.js <project> --auto-merge`

Process:
1. Check `git status` for changes
2. Stage all changes (`git add -A`)
3. Commit with message including file counts
4. If GitHub Actions: create PR via API
5. Output: `.deploy-log.json`

Commit message:
```
Auto-fix: Remove duplicates and refactor imports

Files deleted: 5
Imports updated: 12

Automated by auto-duplicate-fixer skill
```

## Error Handling Protocol

**On Test Failure**:
```bash
git checkout -- .
# Log failure to validation log
echo '{"status": "failed", "reason": "tests-failed", "timestamp": "'$(date -Iseconds)'"}' >> .validation-log.json
```

**On TypeScript Errors**:
```bash
npx tsc --noEmit --pretty
```

**On Build Failure**:
- Log full error
- Rollback
- Report to stderr

**On Conflict**:
- Skip this group
- Continue with next
- Document in log

## Usage

### Daily Mode (Safe)
```bash
npm run daily /path/to/project
```
- Fixes 1-3 files per day
- Always runs full validation
- Safe for CI/CD

### Aggressive Mode
```bash
npm run aggressive /path/to/project
```
- Fixes larger batches
- Use when you know codebase is stable

### Analysis Only (Dry-Run)
```bash
npm run dry-run /path/to/project
```
- No files modified
- Preview what would be fixed
- Generate reports only

### Manual Phases
```bash
# Detect only
npm run check /path/to/project

# View decisions
cat /path/to/project/.keep-remove-map.json

# Refactor
npm run refactor /path/to/project

# Validate
npm run validate /path/to/project

# Deploy
npm run deploy /path/to/project
```

## Automation (Cron/Scheduled)

Schedule daily at 2 AM (requires git access):
```bash
# Add to crontab
0 2 * * * cd /path/to/project && npm run daily

# Or in GitHub Actions
name: Daily Duplicate Fix
on:
  schedule:
    - cron: '0 2 * * *'
jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run daily
      - uses: peter-evans/create-pull-request@v4
```

## Supported Languages

| Language | Detection | Refactor | Validate |
|----------|-----------|----------|----------|
| TypeScript | ✅ AST + jscpd | ✅ Import rewrite | ✅ tsc + test |
| JavaScript | ✅ AST + jscpd | ✅ Import rewrite | ✅ eslint + test |
| Python | ✅ AST | ✅ import rewrite | ✅ pytest + flake8 |

## Examples

### Example 1: Duplicate Utilities
```
Before:
src/utils/format.ts (15 tests, imported 5 places)
src/helpers/formatter.ts (0 tests, imported 1 place)

Decision: KEEP src/utils/format.ts, REMOVE src/helpers/formatter.ts

Action:
- Update: src/services/user.ts
  import { format } from '../utils/format';

- Delete: src/helpers/formatter.ts
- Delete: src/helpers/index.ts (if becomes empty)
```

### Example 2: Python Duplicates
```
Before:
core/validators.py (validate_email, validate_phone)
utils/helpers.py (validate_email, validate_phone)

Decision: KEEP core/validators.py, REMOVE utils/helpers.py

Action:
- Update: services/user.py
  from core.validators import validate_email

- Delete: utils/helpers.py
```

## Logs & Debugging

Check any phase's logs:
```bash
cat .duplicate-report.json     # What was found
cat .keep-remove-map.json      # What will be kept/removed
cat .refactor-log.json         # What was changed
cat .validation-log.json       # Test results
cat .deploy-log.json           # PR/commit status
cat .pipeline-log.json         # Full execution timeline
```

## Caveats

- **Circular imports**: Will be detected pre-refactor
- **Dynamic imports**: May not be rewritten (manual check needed)
- **Large projects**: Consider `aggressive` mode for speed
- **Python type hints**: Optional, but recommended for better decisions

## Requirements

- Node.js >= 16
- npm
- git
- jscpd (auto-installed)
- pytest / tox (Python projects)
- TypeScript compiler (TS projects)

Install script:
```bash
npm install
```
