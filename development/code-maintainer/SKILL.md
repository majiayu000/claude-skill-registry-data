---
name: code-maintainer
description: Fix bugs, optimize performance, and maintain code quality in CClean-Killer. Use when asked to fix detection issues, false positives, false negatives, optimize scan speed, improve performance, refactor code, or do quick maintenance tasks like version bumps or linting.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Code Maintainer

Fix bugs, optimize performance, and maintain code quality in the CClean-Killer codebase.

## Purpose

Handle day-to-day development tasks:
- Fix detection issues (false positives/negatives)
- Optimize script performance
- Quick maintenance tasks

## Modes

### Mode: fix

Debug and fix detection issues including false positives and false negatives.

**When to use:** User says "fix detection", "false positive", "false negative", "not detecting", "wrongly detecting"

**Workflow:**

1. **Diagnose Phase**
   - Identify the specific issue (FP or FN)
   - Run detection with verbose output:
     ```bash
     ./scripts/macos/find-parasites.sh --verbose 2>&1 | grep -i "[pattern]"
     ./scripts/macos/find-orphans.sh --verbose 2>&1 | grep -i "[pattern]"
     ```
   - Check pattern matching logic in script

2. **Trace Phase**
   - Read the detection function in `scripts/macos/find-parasites.sh`
   - Check `is_known_parasite()` function
   - Verify bundle ID extraction from plist
   - Check skip patterns in `scripts/macos/lib/common.sh`

3. **Fix Phase**
   - For false positive: Add to skip patterns or refine match
   - For false negative: Add/fix pattern in KNOWN_PARASITES array
   - Update `knowledge/parasite-fingerprints.json` if needed

4. **Verify Phase**
   - Run tests:
     ```bash
     npm run test:unit
     ```
   - Verify fix works on real data

**Files Modified:**
- `scripts/macos/find-parasites.sh`
- `scripts/macos/find-orphans.sh`
- `scripts/macos/lib/common.sh` (SKIP_PATTERNS)
- `knowledge/parasite-fingerprints.json`
- `tests/unit/test-parasite-patterns.sh`

**Common Issues:**

| Issue | Location | Fix |
|-------|----------|-----|
| Pattern too broad | `KNOWN_PARASITES` array | Make pattern more specific |
| Pattern too narrow | `KNOWN_PARASITES` array | Use broader glob pattern |
| Wrong bundle ID extraction | `get_bundle_id_from_plist()` | Fix plist parsing |
| App check failing | `app_exists_for_agent()` | Fix mdfind or /Applications check |
| Safe item flagged | `SKIP_PATTERNS` | Add to skip list |

---

### Mode: optimize

Improve performance of scanning and detection scripts.

**When to use:** User says "optimize", "slow scan", "improve performance", "speed up", "benchmark"

**Workflow:**

1. **Profile Phase**
   - Run benchmark:
     ```bash
     time ./scripts/macos/scan.sh --dry-run
     time ./scripts/macos/find-parasites.sh --dry-run
     ```
   - Identify slow operations

2. **Analyze Phase**
   - Check for:
     - Repeated file system operations
     - Inefficient loops
     - Missing caching
     - Sequential operations that could be parallel
   - Reference `scripts/macos/lib/optimized-patterns.sh` for existing optimizations

3. **Implement Phase**
   - Apply optimization techniques:
     ```bash
     # Cache app list instead of repeated mdfind
     declare -A APP_CACHE

     # Use find with -prune for skipping
     find "$dir" -name ".git" -prune -o -type f -print

     # Parallel processing
     find ... | xargs -P 4 ...
     ```

4. **Benchmark Phase**
   - Compare before/after:
     ```bash
     ./scripts/benchmark.sh --compare
     ```
   - Document improvement in `docs/OPTIMIZATION-REPORT.md`

**Files Modified:**
- `scripts/macos/*.sh`
- `scripts/macos/lib/common.sh`
- `scripts/macos/lib/optimized-patterns.sh`
- `docs/OPTIMIZATION-REPORT.md`

**Optimization Techniques:**

| Technique | When to Use | Example |
|-----------|-------------|---------|
| Associative arrays | Repeated lookups | `declare -A cache` |
| Find with -prune | Skip directories | `-name ".git" -prune` |
| Parallel xargs | Independent operations | `xargs -P 4` |
| Early termination | First match sufficient | `return` after match |
| Caching | Expensive repeated calls | Cache mdfind results |

---

### Mode: maintain

Quick maintenance tasks: version bumps, linting, syncing, cleanup.

**When to use:** User says "bump version", "lint", "sync json", "cleanup", "maintenance"

**Quick Tasks:**

1. **Version Bump**
   ```bash
   # Update version in package.json
   npm version patch  # or minor/major
   ```

2. **Lint Scripts**
   ```bash
   # Check shell scripts
   shellcheck scripts/macos/*.sh scripts/macos/lib/*.sh
   ```

3. **Sync JSON Database**
   - Ensure `parasite-fingerprints.json` matches `common-parasites.md`
   - Update `totalParasites` count
   - Update `lastUpdated` date

4. **Validate Configs**
   ```bash
   # Check JSON syntax
   jq . knowledge/parasite-fingerprints.json > /dev/null

   # Check all scripts are executable
   find scripts -name "*.sh" ! -executable
   ```

5. **Clean Temp Files**
   ```bash
   rm -f scripts/**/*.bak
   rm -f **/*.tmp
   ```

**Files Modified:**
- `package.json` (version)
- `knowledge/parasite-fingerprints.json` (metadata)
- Various (linting fixes)

---

## Safety Rules

1. **ALWAYS** run tests after fixes
2. **NEVER** remove safety checks during optimization
3. **PRESERVE** backward compatibility in function signatures
4. **VERIFY** optimizations don't change output
5. **DOCUMENT** non-obvious optimizations with comments

## Debugging Commands

```bash
# Verbose detection output
./scripts/macos/find-parasites.sh --verbose

# Dry run (no changes)
./scripts/macos/clean.sh --dry-run --all

# JSON output for parsing
./scripts/macos/scan.sh --json | jq .

# Test specific pattern
grep -r "com.example" knowledge/

# Check if pattern matches
[[ "com.google.keystone.agent" == com.google.* ]] && echo "matches"
```

## Examples

### Example 1: Fix false positive

```
User: "Google Chrome is being flagged as a parasite but it's installed"

1. Check detection: ./scripts/macos/find-parasites.sh --verbose | grep google
2. Find: com.google.keystone.agent flagged as zombie
3. Trace: app_exists_for_agent() not finding Chrome.app
4. Fix: Update app detection to check "Google Chrome.app"
5. Verify: Run detection again, no longer flagged
```

### Example 2: Optimize slow scan

```
User: "Scanning takes 30 seconds, can we speed it up?"

1. Profile: time ./scripts/macos/scan.sh shows 25s in du calls
2. Analyze: Repeated du on same directories
3. Implement: Cache directory sizes in associative array
4. Benchmark: New time is 8 seconds
5. Document in OPTIMIZATION-REPORT.md
```

## Related Skills

- **knowledge-manager**: For adding new parasites after fixing detection
- **quality-assurance**: For adding regression tests after fixes
