---
name: env-check
description: Probe the dev environment for the recurring Windows quirks documented in `.claude/rules/environment.md` — Python version + 3.13 dep gaps, stdout encoding (cp1252 trap, tested by actually writing a non-ASCII char), and daemon reachability on :9000 + :9001. Use when the shell is behaving oddly, when a non-ASCII print just crashed, or when the user says "env-check" / "/env-check". NOT a git/daemon state check at session start (use preflight) and NOT a diagnosis of why the daemon died (use eos-wedge-postmortem).
---

# Env Check

Codifies the environment friction surfaced across 4+ recent sessions so we stop re-discovering it. Read-only — never installs, never restarts. Run anomalies past the user before continuing whatever work is queued.

## When to use

- A non-ASCII `print()` just crashed with `UnicodeEncodeError`
- A `pip install` succeeded but the import still fails
- A daemon call returned an unexpected error
- Beginning of a session that will touch pronounce/voice/non-ASCII work
- User says "env-check"

## Probes (in order)

### 1. Python version + 3.13 dep gaps

```bash
python --version
```

If `3.13.x`, flag the known wheel gaps before they bite:

```bash
python -c "import g2p_en" 2>&1 | head -1
python -c "import phonemizer" 2>&1 | head -1
where espeak-ng 2>&1 | head -1
```

Known: `g2p_en` has no Python 3.13 wheel as of recent sessions; `espeak-ng` needs a separate Windows install. Apps depending on these (`apps/pronounce`, `apps/public/standard/voice-assistant` listen path) gate imports behind try/except. Surface gaps; do NOT install.

### 2. Encoding — actively write a non-ASCII char

Reading `sys.stdout.encoding` is the indirect test. The direct test is to *write* a non-ASCII char and see if the subprocess crashes:

```bash
python -c "import sys; print('encoding:', sys.stdout.encoding); print('é α 中 ✓')"
```

Expected with the `.claude/settings.json` `env.PYTHONIOENCODING=utf-8` hook active: `encoding: utf-8` followed by the four chars rendering cleanly. If you see `UnicodeEncodeError` or `cp1252` in the first line, the hook isn't taking effect — flag it and tell the user to write non-ASCII via `open(path, "w", encoding="utf-8")` rather than `print()` until the hook is fixed.

### 3. Daemons

```bash
curl -s -o /dev/null -w "main :9000 = %{http_code}\n" http://localhost:9000/api/health
curl -s -o /dev/null -w "dogfood :9001 = %{http_code}\n" http://localhost:9001/api/health
```

Anything other than 200 → report, don't act (`.claude/rules/daemon-handling.md`). Connection refused on :9001 is fine if `dogfood-demo` is disabled in `emptyos.toml`.

### 4. Sandbox pool (only if test-fix work is queued)

```bash
curl -s http://localhost:9000/sandbox/api/status
```

Look for at least one `idle` member. If `pool_full` or every member is `dead`, surface so the user can restart the main daemon (which re-seeds the pool).

## Report shape

Two or three lines is fine — skip rows that aren't relevant to the current task. Surface anomalies *before* starting work, not after.

```
Env check:
  python: 3.13.x · stdout=utf-8 · non-ASCII print ok
  pronounce stack: g2p_en MISSING (3.13 wheel gap) · espeak-ng ok
  :9000: 200 · :9001: refused (dogfood off)
  sandbox: 2 idle / 0 leased
```

If any row is anomalous, lead with it and ask the user how to proceed:

```
Env check anomaly:
  stdout=cp1252 — PYTHONIOENCODING hook not active
  Any non-ASCII print() from a Bash tool will crash.
  Proceed with file-only I/O, or stop and fix the hook?
```

## What this skill is NOT

- Not a fixer. It surfaces; the user (or a separate skill) acts.
- Not a daemon manager — never restart anything.
- Not a replacement for `/preflight` — preflight is broader (git + daemon + env); env-check is the deep-dive when the env is the suspected cause.
