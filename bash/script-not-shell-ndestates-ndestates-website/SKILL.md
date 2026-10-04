---
name: script-not-shell
description: >
  Avoid inline shell escaping failures by writing script files first. Use when running
  multi-line Python/bash, heredocs, nested quotes, YAML/JSON in shell, audit logic, or
  after heredoc/syntax errors. Creates temp scripts (/tmp) or permanent scripts (scripts/).
  Invoke with .github/skills/script-not-shell/SKILL.md. Reduces retry loops and token waste.
argument-hint: "Optional: temp | permanent | audit — and what the script should do"
user-invocable: true
disable-model-invocation: false
---

# Script-Not-Shell (avoid escaping failures)

**Default rule:** If a terminal command is not a single simple invocation, **write a file and run it** — do not inline complex logic in the shell tool.

## When to use (mandatory)

Use this skill **before** running the shell when any of these are true:

| Trigger | Example failure mode |
|---------|---------------------|
| Multi-line Python/bash | `python3 << 'PY'` heredoc delimiter errors |
| Nested quotes | `"$(echo 'foo')"` inside JSON or SQL |
| Backticks / `$()` chains | Audit one-liners with 3+ substitutions |
| Regex in shell | `sed`/`grep` with unescaped `/` or `\` |
| YAML/JSON embedded in shell | Passing structured data via `-c` |
| Prior attempt failed | `syntax error`, `unexpected end of file`, `warning: here-document` |
| Reusable check | Alignment audits, registry validators, report generators |

## Decision: temp vs permanent

| Kind | Path | When |
|------|------|------|
| **Temp** | `/tmp/agent-<task>-<timestamp>.sh` or `.py` | One-off probe, debug, single session |
| **Permanent** | `scripts/<kebab-name>.sh` or `.py` | Will run again, CI gate, audit, or chain step |

**Permanent scripts must:**
- Use `#!/usr/bin/env bash` or `python3` shebang
- Exit non-zero on failure (`set -euo pipefail` for bash)
- Print a one-line `PASS` / `FAIL` summary
- Be referenced from `docs/codebase/TESTING.md` if they are validation gates

## Workflow (agent)

1. **Stop** — do not retry the same escaped one-liner.
2. **Choose** temp vs permanent (table above).
3. **Write** the full script with the Write tool (not echo/heredoc in shell).
4. **Run** only: `bash scripts/foo.sh` or `python3 scripts/foo.py` (or `chmod +x` once for permanent).
5. **On FAIL** — fix the script file; never escalate escaping in the shell.
6. **Temp cleanup** — delete `/tmp/agent-*` when done unless user wants to keep for debug.
7. **Permanent** — add to `scripts/`, document in TESTING.md if a gate; run `check_name_alignment.py` / `chain-audit.sh` only if registry-related.

## Anti-patterns (never)

- `python3 -c '...50 lines...'`
- `bash -c "curl ... | jq ... | while read..."`
- Heredocs inside chained shell commands passed to the Shell tool
- "Fixing" a failed one-liner by adding more backslashes
- Re-running the same failed command hoping for a different result (wastes tokens)

## Host vs DDEV

- **Orchestrator template / host-only tasks:** run scripts on host (`git`, `gh`, `python3 scripts/*`).
- **Application repos (ndestates-io):** run project scripts via `ddev exec python3 scripts/...` or `ddev exec bash scripts/...` per `ddev-local-runtime`.

## Cache citation (required in standup/triage when relevant)

When this skill was needed in a session, cite:

- `docs/codebase/CONCERNS.md` §6 (shell escaping)
- `docs/codebase/CONVENTIONS.md` — Script-first execution
- This skill: `.github/skills.github/skills/script-not-shell/SKILL.md/SKILL.md`

## Related gates

- `scripts/check_name_alignment.py` — example permanent audit script (born from heredoc failure)
- `scripts.github/skills/chain/SKILL.md-audit.sh`, `scripts/loop-audit.sh` — permanent bash audits