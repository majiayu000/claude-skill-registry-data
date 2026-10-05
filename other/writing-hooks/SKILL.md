---
name: writing-hooks
description: "Guide for writing, configuring, and debugging Claude Code hooks. Use when adding, writing, or debugging hooks — including silent failures and permission errors."
when_to_use: "write hook, create hook, hook not running, debug hook, hook silent failure, hooks.json, pre-tool hook, post-tool hook"
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# Writing Hooks

Guide for adding hooks to `harness/hooks/hooks.json` and writing the scripts they invoke.

## Hook Types

| Type | When to use | Cost |
|------|-------------|------|
| `command` | Deterministic checks, fast guards, file ops | Low |
| `prompt` | Single LLM judgment with `{"ok": true/false}` response | Medium |
| `agent` | Multi-step LLM reasoning with file tools | High |
| `http` | POST to external service | Varies |

Prefer `command` whenever the logic can be expressed in any executable script or the Go binary. Reserve `agent`/`prompt` for cases that genuinely need judgment — they are slower and cost tokens on every invocation.

> **Note**: `agent` hooks do NOT work on `PreCompact`. Use `command` instead.

## Adding a command Hook

### 1. Write the script

Place scripts in `harness/scripts/`. Use whichever language fits the task — bash, Python, and Node.js are all fine. The only requirement is that the script is executable and produces the correct exit code and stdout.

**Exit codes control the hook outcome:**

| Exit code | Meaning |
|-----------|---------|
| `0` | Allow / pass |
| `2` + JSON to stdout | Block (PreToolUse / Stop) |
| `0` + JSON to stdout | Inject context (PostToolUse, PreCompact) |

**Bash example — blocking Stop hook:**
```bash
#!/usr/bin/env bash
if [[ some_condition ]]; then
  echo '{"decision":"block","reason":"Explain why"}'
  exit 2
fi
exit 0
```

**Python example — blocking Stop hook:**
```python
#!/usr/bin/env python3
import sys, json
if some_condition:
    print(json.dumps({"decision": "block", "reason": "Explain why"}))
    sys.exit(2)
sys.exit(0)
```

**Node.js example — warning injection (PreCompact):**
```js
#!/usr/bin/env node
if (someCondition) {
  console.log(JSON.stringify({ systemMessage: "Warning: something needs attention" }));
}
process.exit(0);  // never block compaction
```

### 2. Set execution permission

Scripts without `chmod +x` fail silently or with `permission denied`, regardless of language:

```bash
chmod +x harness/scripts/your-script.py   # or .sh, .js, etc.
```

Alternatively, invoke the interpreter explicitly in the hook command (step 3) — then `chmod +x` is not required.

### 3. Register in hooks.json

Edit `harness/hooks/hooks.json` (SSOT). Reference the script via `${CLAUDE_PLUGIN_ROOT}` and invoke with the appropriate interpreter:

```json
{ "type": "command", "command": "bash \"${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh\"", "timeout": 5 }
{ "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/your-script.py\"", "timeout": 5 }
{ "type": "command", "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/your-script.js\"", "timeout": 5 }
```

For `bin/harness` subcommands, use `timeout: 3`. For scripts, use `timeout: 5`.

### 4. Validate

```bash
make validate   # runs tests/validate-plugin.sh
```

---

## Checklist for New Hooks

- [ ] Script has the correct shebang for its language (`#!/usr/bin/env bash`, `#!/usr/bin/env python3`, `#!/usr/bin/env node`)
- [ ] Script is executable (`chmod +x`) **or** interpreter is explicit in the hook command (`python3 "..."`, `node "..."`)
- [ ] Script path uses `${CLAUDE_PLUGIN_ROOT}/scripts/` — never absolute paths
- [ ] Timeout matches type: `3` for `bin/harness`, `5` for scripts, `30` for agents
- [ ] Tested locally by running the script directly with its interpreter
- [ ] `make validate` passes after editing `hooks.json`

---

## Common Issues

### Hook not running (silent failure)

Three likely causes:

1. **Not executable** — check with `ls -la harness/scripts/your-script.*`. Either `chmod +x` the file or prefix the command with the interpreter (`python3 "..."`, `node "..."`, `bash "..."`)
2. **Wrong path** — verify the path resolves correctly; run the script directly to confirm
3. **Syntax error** — run the script manually (`python3 script.py`, `node script.js`, `bash -n script.sh`) to surface errors before the hook fires

### Permission denied

```bash
chmod +x harness/scripts/your-script.py   # or .sh, .js
# OR use explicit interpreter in hooks.json — no chmod needed
```

### Hook fires but doesn't block

For blocking hooks (PreToolUse / Stop), you must **both** print JSON to stdout **and** `exit 2`. Printing alone or exiting alone won't block.

### agent hook not firing on PreCompact

Agent hooks silently do nothing on `PreCompact`. Convert to a `command` script — see `harness/scripts/check-wip-precompact.sh` as a reference.

---

## Event Reference

Key events and their typical use:

| Event | Use for |
|-------|---------|
| `PreToolUse` | Guard writes, validate inputs before execution |
| `PostToolUse` | Cleanup, logging, tracking after tool runs |
| `Stop` | Block session end if work is incomplete |
| `PreCompact` | Warn (don't block) before context compaction |
| `UserPromptSubmit` | Inject policy context, track commands |
| `SessionStart` | One-time session initialization (`once: true`) |

Full event list and response schemas: `.claude/rules/hooks-editing.md`

---

## Related

- `harness/hooks/hooks.json` — SSOT for all hook configuration
- `harness/scripts/` — All command hook scripts
- `.claude/rules/hooks-editing.md` — Complete event reference and timeout guidelines
- `update-config` skill — For adding automated behaviors via settings.json
