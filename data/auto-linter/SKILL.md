---
name: auto-linter
description: Run linters/formatters on changed files and apply safe, mechanical fixes. Use in Flow 3 and Flow 4.
allowed-tools: Bash, Read, Write
---

# Auto Linter Skill

You are a helper for running formatters and linters in this repository. Your job is to apply safe, mechanical fixes that improve code hygiene without changing behavior.

## Purpose

The auto-linter skill provides automated code formatting and linting across the codebase. It:

1. **Formats code** to match project style conventions (safe to auto-apply)
2. **Lints code** to detect issues, style violations, and potential bugs (reports findings)
3. **Auto-fixes safe issues** that are mechanical/non-semantic
4. **Reports issues** that require human judgment to resolve

The goal is polish, not behavior change. Formatting is deterministic and safe. Lint fixes vary by confidence level.

## When to Use

| Flow                | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| **Flow 3 (Build)**  | Called by `standards-enforcer` after implementation to polish the diff |
| **Flow 4 (Review)** | Called to verify code meets standards before merge decision            |
| **Ad-hoc**          | When code hygiene sweep is needed before commit                        |

Typical invocation chain:

```
code-implementer (writes code)
  -> test-executor (verifies behavior)
    -> standards-enforcer (calls auto-linter)
      -> repo-operator (commits polished code)
```

## Supported Tools

### Rust (Primary)

| Tool           | Purpose                   | Auto-fix                           |
| -------------- | ------------------------- | ---------------------------------- |
| `cargo fmt`    | Code formatting           | Yes - always safe                  |
| `cargo clippy` | Linting + static analysis | Report only (some `--fix` allowed) |

**Commands:**

```bash
# Format (modifies files)
cargo fmt --all

# Format check only (no changes)
cargo fmt --all -- --check

# Lint (report findings)
cargo clippy --all-targets --all-features -- -D warnings

# Lint with auto-fix (machine-applicable only)
cargo clippy --all-targets --all-features --fix --allow-dirty --allow-staged -- -D warnings
```

### JavaScript / TypeScript

| Tool       | Purpose         | Auto-fix                     |
| ---------- | --------------- | ---------------------------- |
| `prettier` | Code formatting | Yes - always safe            |
| `eslint`   | Linting         | Yes for `--fix`, some manual |
| `biome`    | Format + lint   | Yes for format, lint varies  |

**Commands:**

```bash
# Prettier format
npx prettier --write "src/**/*.{js,ts,jsx,tsx}"

# Prettier check
npx prettier --check "src/**/*.{js,ts,jsx,tsx}"

# ESLint with auto-fix
npx eslint --fix "src/**/*.{js,ts,jsx,tsx}"

# ESLint report only
npx eslint "src/**/*.{js,ts,jsx,tsx}"

# Biome (combined)
npx biome check --apply src/
```

### Python

| Tool    | Purpose                   | Auto-fix           |
| ------- | ------------------------- | ------------------ |
| `black` | Code formatting           | Yes - always safe  |
| `ruff`  | Fast linting + formatting | Yes for many rules |
| `isort` | Import sorting            | Yes - always safe  |
| `mypy`  | Type checking             | Report only        |

**Commands:**

```bash
# Black format
black src/ tests/

# Black check
black --check src/ tests/

# Ruff lint with auto-fix
ruff check --fix src/ tests/

# Ruff format
ruff format src/ tests/

# isort
isort src/ tests/

# mypy (no auto-fix)
mypy src/
```

### Go

| Tool                  | Purpose         | Auto-fix           |
| --------------------- | --------------- | ------------------ |
| `gofmt` / `goimports` | Code formatting | Yes - always safe  |
| `golangci-lint`       | Meta-linter     | Some rules fixable |
| `staticcheck`         | Static analysis | Report only        |

**Commands:**

```bash
# Format
gofmt -w .
goimports -w .

# golangci-lint
golangci-lint run --fix ./...

# golangci-lint report only
golangci-lint run ./...
```

### Other Languages

| Language | Format Tool             | Lint Tool                |
| -------- | ----------------------- | ------------------------ |
| Java     | `google-java-format`    | `checkstyle`, `spotbugs` |
| C/C++    | `clang-format`          | `clang-tidy`             |
| Ruby     | `rubocop --autocorrect` | `rubocop`                |
| Shell    | `shfmt`                 | `shellcheck`             |

## Safe vs Manual Fixes

### Safe to Auto-Apply

These changes are mechanical and do not alter behavior:

- **Whitespace:** Indentation, trailing spaces, blank lines
- **Formatting:** Line length, brace placement, quote style
- **Import sorting:** Alphabetization, grouping
- **Trailing commas:** Adding/removing per style
- **Semicolons:** (in languages where optional)
- **Simple lint fixes:** Unused imports, redundant type annotations

### Requires Manual Review

These may change behavior or require judgment:

- **Logic changes:** Even "equivalent" refactors
- **Error handling:** Adding/changing catch blocks
- **Type narrowing:** Changing type signatures
- **Dead code removal:** May be intentional (feature flags)
- **Security-related:** Never auto-fix security warnings

### Decision Rule

If the tool marks the fix as "machine-applicable" or "safe", apply it. If marked as "suggestion" or "manual", report it for human review.

## Behavior

### 1. Detect Changed Files

Prefer scoped runs on changed files:

```bash
# Get changed Rust files
git diff --name-only origin/main...HEAD | grep '\.rs$'

# Get changed JS/TS files
git diff --name-only origin/main...HEAD | grep -E '\.(js|ts|jsx|tsx)$'
```

If no changed-files info is available, run on the entire project.

### 2. Run Formatting (Always Safe)

Format first, as it may resolve some lint issues:

```bash
# Rust
cargo fmt --all

# JS/TS
npx prettier --write "src/**/*.{js,ts,jsx,tsx}"

# Python
black src/ tests/ && isort src/ tests/
```

### 3. Run Linting

After formatting, run linters:

```bash
# Rust
cargo clippy --all-targets --all-features -- -D warnings 2>&1 | tee lint_output.log

# JS/TS
npx eslint "src/**/*.{js,ts,jsx,tsx}" 2>&1 | tee lint_output.log

# Python
ruff check src/ tests/ 2>&1 | tee lint_output.log
```

### 4. Capture Output

Save all output to artifacts:

- `lint_output.log` - Raw tool output (overwrite per run)
- `lint_summary.md` - Parsed summary with counts and categories

### 5. Report Results

Report back with:

- Files modified by formatting
- Warning/error counts from linting
- Issues requiring manual attention

## Configuration

### Detecting Project Stack

Check for configuration files to determine which tools to use:

| File             | Stack    | Tools                   |
| ---------------- | -------- | ----------------------- |
| `Cargo.toml`     | Rust     | cargo fmt, clippy       |
| `package.json`   | JS/TS    | prettier, eslint, biome |
| `pyproject.toml` | Python   | black, ruff, mypy       |
| `go.mod`         | Go       | gofmt, golangci-lint    |
| `.tool-versions` | Multiple | Use specified versions  |

### Project-Specific Config

Respect project configuration:

- `.prettierrc`, `.prettierignore`
- `.eslintrc.*`, `.eslintignore`
- `pyproject.toml` (black, ruff sections)
- `rustfmt.toml`, `clippy.toml`
- `.golangci.yml`

### Custom Commands

If a project defines custom lint commands (in `package.json` scripts, Makefile, etc.), prefer those:

```bash
# If defined in package.json
npm run lint
npm run format

# If defined in Makefile
make lint
make fmt
```

## Examples

### Rust Project (Default)

```bash
# Step 1: Format
cargo fmt --all

# Step 2: Lint
cargo clippy --all-targets --all-features -- -D warnings 2>&1 | tee lint_output.log

# Step 3: Report
# Files formatted: src/lib.rs, src/main.rs
# Clippy: 0 errors, 2 warnings
```

### JavaScript/TypeScript Project

```bash
# Step 1: Format
npx prettier --write "src/**/*.{js,ts,jsx,tsx}"

# Step 2: Lint with auto-fix
npx eslint --fix "src/**/*.{js,ts,jsx,tsx}" 2>&1 | tee lint_output.log

# Step 3: Report
# Files formatted: 12 files
# ESLint: 0 errors, 5 warnings (3 auto-fixed)
```

### Python Project

```bash
# Step 1: Format
black src/ tests/
isort src/ tests/

# Step 2: Lint
ruff check src/ tests/ 2>&1 | tee lint_output.log

# Step 3: Type check (optional)
mypy src/ 2>&1 | tee -a lint_output.log

# Step 4: Report
# Files formatted: 8 files
# Ruff: 0 errors, 3 warnings
# Mypy: 0 errors
```

## Output Artifacts

### lint_output.log

Raw output from all tools run. Include command and exit code:

```
=== cargo fmt ===
(no output - all files formatted)
Exit code: 0

=== cargo clippy ===
warning: unused variable: `x`
  --> src/lib.rs:42:9
   |
42 |     let x = 5;
   |         ^ help: if this is intentional, prefix it with an underscore: `_x`
   |
   = note: `#[warn(unused_variables)]` on by default

Exit code: 0
```

### lint_summary.md

```markdown
# Lint Summary

## Tools Run

- cargo fmt: PASS (0 files modified)
- cargo clippy: PASS (0 errors, 2 warnings)

## Warnings

| File       | Line | Code                    | Message                     |
| ---------- | ---- | ----------------------- | --------------------------- |
| src/lib.rs | 42   | unused_variables        | unused variable: `x`        |
| src/lib.rs | 87   | clippy::needless_return | unneeded `return` statement |

## Files Modified by Formatting

- (none)

## Manual Fixes Required

- (none)
```

## Troubleshooting

### Tool Not Found

```
error: cargo fmt not found
```

**Solution:** Ensure the tool is installed and in PATH. For Rust: `rustup component add rustfmt clippy`

### Configuration Conflicts

```
error: conflicting configuration in .prettierrc and .editorconfig
```

**Solution:** Remove conflicting settings or ensure consistency across config files.

### Permission Errors

```
error: EACCES: permission denied, open 'src/file.ts'
```

**Solution:** Check file permissions. May indicate file is locked by another process.

### Lint Fails with Exit Code 1

This is expected when there are errors. Check `lint_output.log` for details:

- If all issues are warnings: proceed with warnings noted
- If errors exist: report errors for manual resolution

### Formatter Changes Staged Files

This is normal behavior. After formatting:

1. Inspect changes with `git diff`
2. If changes are correct, proceed to commit
3. If changes are unexpected, check formatter configuration

## Integration with standards-enforcer

The `standards-enforcer` agent calls this skill as part of its hygiene sweep:

1. standards-enforcer loads the diff
2. Performs suspicious deletion check
3. Runs hygiene sweep (debug artifacts)
4. **Calls auto-linter** for format/lint
5. Writes report with combined results

When called by standards-enforcer:

- Focus on changed files in the current diff
- Report format exit code and files touched
- Report lint exit code and remaining errors
- Do not duplicate hygiene work (debug print removal, etc.)

## Invariants

- **No semantic changes:** Formatting only, no behavior modifications
- **No test removal:** Never delete or modify test assertions
- **Respect .gitignore:** Do not format ignored files
- **Preserve intent:** If a lint fix would change behavior, report instead of fix
- **Idempotent:** Running twice produces the same result

## Philosophy

The diff should look like it came from a professional engineer. Consistent formatting, no obvious style violations, clean imports. Auto-linting is the mechanical polish that lets reviewers focus on logic and design, not whitespace and semicolons.

Machine time is cheap. Human attention is expensive. Let the tools handle the mechanical parts.
