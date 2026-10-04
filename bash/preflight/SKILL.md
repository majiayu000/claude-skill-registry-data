---
name: preflight
description: Pre-work safety check at the start of a session. Inspects git state for unexpected staged files or parallel-session commits, confirms the main daemon (:9000) and dogfood daemon (:9001) are reachable, and surfaces anomalies before any code work begins. Use when the user says "preflight", "/preflight", "check state", or whenever you suspect another Claude/user session may have been editing in parallel. NOT a shell/dependency probe (use env-check) and NOT a code audit (use eos-architecture-review / eos-bug-audit).
---

# Preflight

Pre-work safety check. Catches the recurring friction modes documented in `MEMORY.md` — parallel-session auto-staging, daemon drift, and environment quirks — *before* they compound into a wasted hour.

## When to use

- First turn after `/clear` or a fresh `/eos-session-resume`
- When `git status` shows files you didn't touch
- Before any release work (`/eos-release-public`, version bumps)
- When the user says "preflight" or invokes `/preflight`

## Process

### 1. Git state

```bash
git status --short
git log --oneline -5
```

Flag anything surprising:
- **Staged files Claude didn't touch this session** → ask before staging more. Another session may be active.
- **Commits with timestamps inside the last 30 min that you didn't make** → parallel session evidence; warn explicitly.
- **Detached HEAD or unexpected branch** → halt, ask.

### 2. Daemon health

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:9000/api/health
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:9001/api/health   # dogfood, may be disabled
```

- `:9000` not responding → the user's main daemon is down. Surface; do NOT try to restart it (`.claude/rules/daemon-handling.md`).
- `:9001` connection refused with `dogfood-demo` plugin enabled → note it, but don't act.

### 3. Context Bus integrity (only if `.agent-bus/` exists)

```bash
python scripts/agent_bus.py ripple --dry-run
```

- **Workspace not initialized** (`[-] Context Bus not initialized…`) → skip; the bus is opt-in, fresh clones don't have one.
- **No changes detected** → bus in sync.
- **Changes detected** → surface to the user. Don't auto-ripple — they may have intentionally edited a native file and need to pull it back into `.agent-bus/` first. Ripple is one-way (canonical → native); blind sync would clobber.

### 4. Environment quick-probe

Two stable Windows quirks documented in `.claude/rules/environment.md`:

- Console default cp1252 — handled by the `PYTHONIOENCODING=utf-8` hook in `.claude/settings.json`. If a recent session crashed on non-ASCII output, mention it.
- Python 3.13 wheels missing for `g2p_en` / `espeak-ng` — surfaces only if the user touches pronounce/voice work.

### 5. Static self-audit suite (scope-gated — only the scopes the session touches)

The graduated `check-*.py` / `*_audit.py` family runs through one runner,
`scripts/preflight.py` (the runtime home in `.claude/rules/self-audit-loops.md`).
Pick the scope(s) for what this session actually touches — don't run everything
(the `audits.md` false-positive trap). Pure file I/O, no daemon.

```bash
python scripts/preflight.py --list            # see the registry (check → scope → gate)
python scripts/preflight.py --scope ui        # touching themes / shared frontend / app pages
python scripts/preflight.py --scope kb        # touching KB / engineering notes
python scripts/preflight.py --scope vault     # touching vault data
python scripts/preflight.py --scope ui,kb     # combine
```

- **exit non-zero (a `✗ FAIL` row)** → a hard-gate check failed (personal-data /
  branding leak, WCAG AA contrast). Fix before proceeding — see
  `.claude/rules/self-audit-loops.md` + `audits.md`.
- **`· warn` rows** → advisory. Triage, don't reflex-fix. Notably: `kb_link_audit`
  flags `[[slug]]`-in-`related:` and "(to be created)" links that are *intentional*
  (the kb app strips `[]`); only unmarked dangling body wikilinks are real.
- Heavy/live checks (`check-clickable`, `ui_walk_audit` — need the daemon/browser)
  are deliberately NOT in the static runner; run them at release time.

### 6. Report

Write one short paragraph back. Format:

```
Preflight:
  git: <clean | N staged files Claude didn't touch | parallel commits detected>
  bus: <in sync | OUT OF SYNC — ripple needed>
  :9000: <ok | DOWN — user needs to run restart.bat>
  :9001: <ok | refused — dogfood plugin off>
  audits: <not run | scope=<...> clean | N FAIL / M warn>
  anomalies: <none | bullet list>
```

If everything is clean, one line is enough: `Preflight: clean. Ready.`

## What this skill is NOT

- Not a daemon restart. The user owns :9000 — see `.claude/rules/daemon-handling.md`.
- Not a test runner. Tests are downstream of preflight, run via `pytest` after work starts.
- Not a CLAUDE.md audit. Run `/claude-md-management:claude-md-improver` for that.
