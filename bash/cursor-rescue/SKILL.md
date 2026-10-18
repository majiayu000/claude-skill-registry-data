---
name: cursor-rescue
description: "Diagnose and recover Cursor backend failures for Harness workflows. Use when user invokes cursor:rescue, Cursor delegation fails, cursor-agent is missing, setup-cursor fails, or backend resolution unexpectedly falls back to claude."
description-en: "Diagnose and recover Cursor backend failures for Harness workflows. Use when user invokes cursor:rescue, Cursor delegation fails, cursor-agent is missing, setup-cursor fails, or backend resolution unexpectedly falls back to claude."
description-ja: "Harness の Cursor backend 失敗を診断・復旧するスキル。cursor:rescue、Cursor 委譲が失敗した、cursor-agent が見つからない、setup-cursor が失敗した、backend が想定外に claude fallback した時に使う。"
allowed-tools: ["Read", "Bash", "Grep"]
argument-hint: "[failure summary]"
user-invocable: true
---

# cursor:rescue - Cursor Backend Recovery

Cursor backend の failure path を短く切り分ける skill。変更は最小限にし、破壊的操作はしない。

## Quick Reference

```bash
cursor:rescue "breezing fell back to claude"
cursor:rescue "cursor-agent not found"
```

## Diagnosis Order

Run one compact diagnostic block:

```bash
set +e
HARNESS_PLUGIN_ROOT="${HARNESS_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}"
if [ -z "$HARNESS_PLUGIN_ROOT" ] && [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  probe="$(cd "${CLAUDE_SKILL_DIR}" && pwd)"
  while [ "$probe" != "/" ] && [ ! -d "$probe/scripts" ]; do
    probe="$(cd "$probe/.." && pwd)"
  done
  [ -d "$probe/scripts" ] && HARNESS_PLUGIN_ROOT="$probe"
fi
if [ -z "$HARNESS_PLUGIN_ROOT" ]; then
  echo "ERROR: HARNESS_PLUGIN_ROOT is not set and could not be derived from CLAUDE_PLUGIN_ROOT or CLAUDE_SKILL_DIR" >&2
  exit 2
fi
echo "==RESOLVED_BACKEND=="
bash "${HARNESS_PLUGIN_ROOT}/scripts/resolve-impl-backend.sh" --role worker
echo "==USER_OR_PROJECT_DEFAULT=="
bash "${HARNESS_PLUGIN_ROOT}/scripts/set-impl-backend.sh" --show
echo "==CURSOR_MODEL=="
bash "${HARNESS_PLUGIN_ROOT}/scripts/model-routing.sh" --host cursor --role worker --field model
echo "==CURSOR_AGENT=="
CURSOR_AGENT_BIN="${CURSOR_AGENT_BIN:-}"
if [ -z "$CURSOR_AGENT_BIN" ]; then
  if command -v cursor-agent >/dev/null 2>&1; then
    CURSOR_AGENT_BIN="$(command -v cursor-agent)"
  elif [ -x "$HOME/.local/bin/cursor-agent" ]; then
    CURSOR_AGENT_BIN="$HOME/.local/bin/cursor-agent"
  fi
fi
if [ -z "$CURSOR_AGENT_BIN" ]; then
  echo "NOT_INSTALLED: cursor-agent not found in PATH or $HOME/.local/bin"
else
  "$CURSOR_AGENT_BIN" --version
fi
echo "==CURSOR_PACKAGE_CHECK=="
bash "${HARNESS_PLUGIN_ROOT}/scripts/setup-cursor.sh" --check
```

## Common Fixes

| Symptom | Fix |
|---|---|
| `cursor-agent` missing | Install / sign in to Cursor CLI, then rerun `cursor:setup --check`. |
| backend resolves to `claude` unexpectedly | Run `bash scripts/set-impl-backend.sh --show`; set user default with `cursor:setup --user-default` or project default with `cursor:setup --project-default`. |
| `setup-cursor.sh --check` fails | Report the first failing `[ERR]` line and the missing file path. |
| companion exits 2 | Workspace guard or forbidden path. Recreate an isolated worktree and retry. |
| companion exits 3 | `cursor-agent` not found in PATH or `$HOME/.local/bin`. |

## Output

Return:

- root cause candidate
- exact failing command
- minimal fix command
- whether retrying the original workflow is safe
