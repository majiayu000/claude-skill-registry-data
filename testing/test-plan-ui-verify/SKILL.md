---
name: test-plan-ui-verify
description: Browser-based UI test execution against live ODH/RHOAI clusters. Loads TCs from a GitHub PR or repo folder via ui_prepare.py, executes each via a persistent Playwright browser, and produces a visual HTML report with PASS/FAIL/BLOCKED/INCOMPLETE verdicts and screenshots. Use for verifying UI test cases against live clusters with visual evidence and screenshot capture.
argument-hint: "(run after ui_prepare.py - no arguments)"
user-invocable: true
model: claude-opus-4-6
allowedTools:
  # Security note: ui_assert.py accepts --js with arbitrary JavaScript that
  # executes in the authenticated browser session. This is intentional — TC
  # assertions require evaluating DOM state. Mitigations: the CDP port is
  # bound to 127.0.0.1 only; TC sources must come from a trusted repository.
  - Bash(python3 *scripts/ui_read_ctx.py*)
  - Bash(python3 *scripts/ui_interact.py *)
  - Bash(python3 *scripts/ui_assert.py *)
  - Bash(python3 *scripts/ui_block.py *)
  - Bash(python3 *scripts/ui_stop_browser.py*)
  - Bash(python3 *scripts/ui_cleanup.py*)
  - Bash(python3 *scripts/ui_collect.py*)
  - Bash(python3 *scripts/ui_report.py*)
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# test-plan.ui-verify

Verifies UI test cases against a live ODH/RHOAI cluster. Reads TC-*.md files from a GitHub PR or repository folder, runs browser interactions via the Playwright Python API (persistent CDP browser), and produces a PASS/FAIL/BLOCKED report with highlighted screenshots. Test cases with no UI steps are automatically marked BLOCKED.

## Two-step flow

```
# Step 1 — terminal (deterministic setup):
python3 skills/test-plan-ui-verify/scripts/ui_prepare.py \
  --test-plan-pr <url> [--tc <filter>] [--priority <P>]

# Step 2 — Claude Code (launched automatically, or type manually):
/test-plan-ui-verify
```

## ui_prepare.py flags

| Flag | Description |
|---|---|
| `--test-plan-pr <url>` | Load TCs from any open GitHub PR |
| `--test-plan <path>` | Load TCs from a folder in main (e.g. `org/repo/feature_folder`) |
| `--tc <filter>` | Exact ID (`TC-FILTER-001`) or category prefix (`TC-FILTER`, `TC-E2E,TC-CARD`) |
| `--priority <P>` | `P0`, `P1`, or `P2` — default: all priorities |
| `--target-url <url>` | Skip route auto-detection, use this URL |
| `--refresh-map <path>` | Regenerate element-map.yaml from odh-dashboard source |
| `--setup` | One-time credential setup wizard |
| `--upgrade-phase <pre\|post>` | Upgrade testing: `pre` saves baseline on old cluster; `post` compares against baseline on new cluster |
| `--baseline <session-dir>` | Explicit baseline for `--upgrade-phase post` — pin comparison to a specific prior session (e.g. the original working state when verifying a fix after a broken intermediate run) |

## Supporting files

| File | Purpose |
|---|---|
| `test-variables.yml` | Cluster credentials (gitignored — copy from `.example`) |
| `element-map.yaml` | 1300+ data-testid selectors from dashboard source |
| `component-registry.yaml` | ODH component → URL/auth configuration and known routes |
| [`scripts/ui_prepare.py`](scripts/ui_prepare.py) | Deterministic setup: loads TCs, resolves creds/URL, launches browser, writes context |
| [`scripts/ui_interact.py`](scripts/ui_interact.py) | Element interaction: click, fill, goto, scroll, expand (auto-relogins on session expiry) |
| [`scripts/ui_assert.py`](scripts/ui_assert.py) | Assertion runner: banner, screenshot, log, exit code; `--inspect` for diagnostic-only calls; `--click-before` to open ephemeral UI (dropdowns, menus) before asserting |
| [`scripts/ui_block.py`](scripts/ui_block.py) | Logs BLOCKED/INCOMPLETE verdict entries to the TC log |
| [`scripts/ui_report.py`](scripts/ui_report.py) | Generates `report.html` + `report.md` per run; for upgrade post-runs also generates `upgrade-report.html` (FIXED/REGRESSION/STABLE comparison) with a `pre-session/` symlink to the baseline |
| [`scripts/github_utils.py`](scripts/github_utils.py) | GitHub API helpers: fetch TC files and metadata via `gh` |
| [`scripts/build_element_map.py`](scripts/build_element_map.py) | Regenerates element-map.yaml from odh-dashboard source |

## Output

All results land in `skills/test-plan-ui-verify/results/<session>/`:
- `report.html` — visual report: color-coded verdicts, per-TC assertion tables with screenshot thumbnails; open in browser
- `report.md` — plain-text Markdown summary (same content, for GitHub / terminal)
- `TC-*-verify-*.png` — highlighted verification screenshots (one per assertion)
- `tc_log.json` — raw assertion data (verdict priority: FAIL > INCOMPLETE > BLOCKED > PASS)

**Upgrade post-runs additionally produce:**
- `upgrade-report.html` — side-by-side comparison: FIXED / REGRESSION / STABLE / STILL FAILING / POST-ONLY per TC; links to pre and post individual reports
- `upgrade-report.md` — plain-text version of the comparison
- `pre-session/` — symlink to the baseline session directory for easy navigation

---

> **Execution constraints:** Never retry the *same* action more than twice. For route discovery, look up `ctx["known_routes"]` first, then try alternatives freely — URL attempts are unlimited. If 3 consecutive tool calls produce no progress, mark the TC INCOMPLETE and move on. Use `ui_assert.py --inspect` for read-only DOM investigation (never logs to TC log, never mutates DOM). Only call `ui_assert.py` without `--inspect` for official Expected Results.

**Before executing, read the full implementation guide:**

Use the `Read` tool to read `instructions.md` in this skill's directory, then follow the phases exactly.
