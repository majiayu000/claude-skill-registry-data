---
name: qa-pulse
description: Run periodic codebase quality assurance pulse checks — test suite sweeps, CI health, divergence tracking, coverage baselines, and formatted reporting
version: 1.0.0
author: Sentry
metadata:
  hermes:
    tags: [cron, qa, testing, ci, pulse, quality]
    triggers: [qa-pulse, test-sweep, qa-lead-pulse, quality-check, ci-health, test-suite]
    related_skills: [discord-report-format, recurring-status-checks]
---

# QA Pulse

Periodic codebase quality assurance pulse checks. Run scheduled test suite sweeps, track test counts across cycles, monitor divergence, and surface regressions. Designed for cron-based Sentry-like roles that validate codebase health at regular intervals.

## Overview

A QA pulse is a bounded investigation cycle (typically 4h or daily) that:
1. Discovers current test structure dynamically (paths drift between rebases)
2. Runs targeted test suites for speed
3. Detects regressions vs. pre-existing failures
4. Tracks divergence from upstream
5. Maintains a running pulse log
6. Piggy-backs the daily digest
7. Delivers a compact formatted report

## Phase 1: Quiet Hours Gate

Always start with a quiet-hours check before doing any work:

```bash
TZ='America/New_York' date +%H
```

If hour is 00-06 (midnight to 6:59 AM ET): output `[SILENT]` — nothing else. Do not run any tests or logs.

If hour is 07+ (7 AM or later): proceed with the full pulse.

## Phase 2: Read Pulse History

Read the existing pulse log before running anything. This gives you:
- What was tested last cycle and what passed/failed
- Which regressions are pre-existing (don't re-flag them as new)
- Divergence trend
- Fix categories that need re-verification

The pulse log is typically at `$PROFILE_DIR/PULSE.md` (e.g. `~/AppData/Local/hermes/profiles/qa-lead/PULSE.md`).

Focus on the last 2-3 entries to understand the current state. Note:
- **Pre-existing failures** — don't report these as new regressions
- **Fix categories** — the set of Windows compat fixes that must be re-verified each cycle
- **Divergence trend** — is it growing or shrinking?
- **Last cycle's Next Action** — was it acted on?

## Phase 3: Dynamic Test Path Discovery

**Do NOT hardcode test paths.** Test files are frequently relocated during upstream rebases — approval tests move from `tests/approval/` to `tests/tools/test_approval.py`, hindsight moves from `tests/plugins/` to `tests/plugins/memory/`, Docker/mempalace get stripped entirely. Hardcoded paths cause `file or directory not found` errors and waste cycles.

Use `find` to discover current paths:

```bash
# Find all test files matching a suite
find tests -name "*.py" -path "*approval*"
find tests -name "*.py" -path "*tirith*"
find tests -name "*.py" -path "*hindsight*"
find tests -name "*.py" -path "*mempalace*"

# Broader: find specific test files
find tests -name "test_tirith_security.py"
find tests -name "test_context_references.py"
```

Key paths to check (may drift):
- Approval: `tests/acp/`, `tests/tools/test_approval.py`, `tests/tools/test_approval_*.py`
- Security: `tests/tools/test_tirith_security.py`
- Hindsight: `tests/plugins/memory/test_hindsight_*.py`
- Context refs: `tests/agent/test_context_refs*.py`
- Skills: `tests/skills/`
- Scripts: `tests/scripts/`
- Docker: `tests/docker/`
- MemPalace: may be missing if stripped upstream (check `tests/memory/`)

## Phase 4: Run Targeted Suites

**Do NOT run the full test collection.** Full collection may be 43K+ tests and takes 40+ seconds just to collect. Instead, run specific suite directories:

```bash
# Targeted suite runs (preferred — one pytest per suite)
pytest tests/acp/ --tb=short -q                  # ACP: 311-312 tests, ~60s
pytest tests/tools/test_tirith_security.py --tb=short -q  # Tirith: 95 tests, ~5s
pytest tests/tools/test_approval.py tests/tools/test_approval_*.py --tb=short -q  # Approval
pytest tests/agent/test_context_references.py tests/plugins/memory/test_hindsight* --tb=short -q
```

**Concurrent batch** is acceptable (separate terminal calls, they run in parallel server-side), but each suite must report clearly.

Focus on these metrics from each suite:
- **Pass/fail count** — track against last cycle (e.g., approval 311/312 vs 310/312)
- **Pre-existing failures** — flag with "unchanged" not "new regression"
- **Timing** — useful for performance regression detection (e.g., "was 9s, now 16s")
- **New regressions** — these are 🔴 attention items

## Phase 5: Divergence Tracking

Track how far behind upstream the local branch has drifted:

```bash
# Absolute counts
git rev-list --left-right --count HEAD...origin/main
# Output: "ahead   behind"

# Recent commits
git log --oneline -5
git log --oneline origin/main..HEAD | head -5

# Conflict check
git merge-tree HEAD origin/main 2>/dev/null | grep -c "^+<<<<<<<"  # 0 = clean
```

Divergence severity:
- 0-50 behind: 🟢 low risk
- 50-200 behind: 🟡 moderate — monitor
- 200-500 behind: 🟡 attention — rebase window narrowing
- 500+ behind: 🔴 high risk — merge conflicts likely

Check for file overlap with fix paths: `git diff --stat HEAD...origin/main -- <fix-paths>` should be empty.

## Phase 6: Working Tree Audit

Check for uncommitted changes, stale stashes, and artifacts:

```bash
git status --short              # Modified/untracked files
git stash list                  # Stale stash count
```

Clean state: 0 modified tracked, 0 stash entries. Harmless untracked artifacts (`.coverage`, `.playwright-mcp/`, `NUL`, temp files) can be noted as "harmless" but not flagged as issues.

## Phase 7: Pulse Log Append

Append a structured entry to `PULSE.md`. Format:

```markdown
## Pulse @ YYYY-MM-DD HH:MM UTC (Nth Cycle — Brief Title)

- **Status**: 🟢 Nominal / 🟡 Attention / 🔴 Issue
- **Focus**: [what you investigated this cycle]
- **Findings**:
  - ✅ Suite: count/expected (notes about pre-existing failures)
  - ✅ Suite: count/expected
  - 🟡 Divergence: N ahead, M behind (delta since last pulse)
  - 🟢 Working tree: CLEAN / N modified / N stash
  - 🟢/🟡/🔴 Fix categories summarizing all applicable categories
- **Next Action**: [one concrete thing]
```

Append via shell heredoc or `cat >>`:

```bash
cat >> $PROFILE_DIR/PULSE.md << 'EOF'

## Pulse @ ...
...
EOF
```

**IMPORTANT:** Do NOT use `write_file` with a partial `read_file` view. `read_file` returns line-number-prefixed content that `write_file` rejects. Use `cat >>` for appending, or read the full file first and construct the complete replacement.

## Phase 8: Daily Digest Cross-Post

After appending to PULSE.md, also append a brief entry to the daily digest:

```bash
python /path/to/append-digest.py "Role Pulse" "- findings line 1\n- findings line 2"
```

**⚠️ Path resolution pitfall on MSYS2/Windows:** When calling Python scripts from git-bash, MSYS2 resolves `/e/` to `C:\e\` (the system drive), not `E:\`. Do NOT use MSYS2-style paths like `${MY_REPOS}/...`. Use one of:
- Forward-slash Windows path: `${USER_HOME}/AppData/Local/hermes/profiles/docs-lead/append-digest.py`
- Fully escaped Windows path: `E:\\yourdata\\...`
- Or find the script first: `find ${USER_HOME} -name "append-digest.py"`

## Phase 9: Report Delivery

Format the report using `discord-report-format` conventions:
- **🔵 SENTRY PULSE** | Wed Jul 22 · 11:00 AM ET
- **📊 RECAP** — key results, one line per suite
- **⏳ PENDING** — pre-existing failures, push status, divergence
- **🎯 RECOMMENDED ACTIONS** — 2-4 concrete next steps
- **🔍 Checked:** — timestamp

Compact format: one line per finding, no blank lines between items, bold for key names, backticks for paths/commands.

## Common Fix Categories (Sentry on Windows)

When running pulses on Windows, these fix categories need re-verification each cycle:

| Category | Tests | Fix | Pre-existing Failures |
|----------|-------|-----|-----------------------|
| Tirith autouse fixture | `test_tirith_security.py` (95 tests) | `is_platform_supported=True` mock + unsupported_platform marker | 0 once applied |
| Approval pipeline | `tools/approval.py` (225-311 tests) | Path-separator skip in `_rewrite_resolved_hermes_home` | 1 symlink-on-Windows |
| USERPROFILE monkeypatch | hindsight, context_refs (132 tests) | `monkeypatch.setenv("USERPROFILE", tmp_path)` across 5+ refs | 0 once applied |
| ACP CRLF path translation | `test_acp_acp_adapter/` (19 tests) | Platform-aware `_parse_file_path` + CRLF normalization | 1 ProactorEventLoop |
| Skills path-sep assertions | openclaw, unbroker (302 tests) | `endswith(os.sep)` instead of `endswith("/")` | 1 mode==0o600 on Windows |

## Pitfalls

- **Don't hardcode test paths.** They drift between rebases. Always `find` first.
- **Don't run the full 43K+ test collection.** Use targeted suites for speed.
- **Don't flag pre-existing failures as new regressions.** Track them across cycles.
- **Don't use `write_file` to append to PULSE.md** after reading with offset/limit — the tool warns and refuses. Use `cat >>` shell heredoc.
- **Don't use MSYS2-style paths (`/e/`, `/c/`) for Python scripts.** Use forward-slash Windows paths (`C:/Users/...`).
- **Don't report "no commits" without checking working tree.** Developers often stage work without committing.
- **Don't run during quiet hours (00-06 ET).** Output `[SILENT]` and stop.
- **Don't omit the divergence check.** Without it, the report lacks context for whether failures are local or upstream-introduced.
- **Don't defer commits on reappearing changes.** During pulse checks on forks that get force-reset to origin/main, quality work from prior sessions can survive in the working tree as unstaged changes even after its commits are orphaned. If you find changes that look correct and complete, commit them *before* investigating their source — the next git operation (rebase, reset, stash drop) may destroy them permanently.

## Related Skills

- `discord-report-format` — Discord formatting rules for delivery and pulse report structure
- `recurring-status-checks` — stakeholder-focused status checks (different from codebase QA)
- `test-driven-development` — TDD workflow (when writing new tests during a pulse)
- `codebase-inspection` — codebase structure analysis
