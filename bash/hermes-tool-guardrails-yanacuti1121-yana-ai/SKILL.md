---
name: hermes-tool-guardrails
description: Yana AI-native (not hermes-agent-derived — see Provenance correction below) command allowlist + approval-gate pattern for safe tool execution. Block dangerous commands by default, prompt for approval on risky ones, auto-deny in non-interactive subagents. Complements YAMTAM's safe-run.sh at the agent decision level. Distinct from [[hermes-tool-loop-guard]], which detects within-turn tool-call failure loops.
---

## Provenance correction (2026-06-20)

This skill was originally tagged `license: MIT` / `source: https://github.com/NousResearch/hermes-agent`
when imported (commit `98f1d51b`). After the real upstream source was vendored
and read (`vendor/hermes-agent/_upstream/`), a full grep for this skill's
content (`allowlist`, `auto_approve`, `require_approval`, `always_block`,
"Approval needed") found **zero matches anywhere in the actual hermes-agent
source**. The real `agent/tool_guardrails.py` is loop-detection logic only —
ported verbatim as `core/lib/hermes_adapted/tool_guardrails.py` and documented
correctly in [[hermes-tool-loop-guard]]. The attribution on this file was
false provenance, not a real hermes-agent pattern. Source/license header
removed; content below is Yana AI-native guidance, kept because it doesn't
duplicate the cited rule files below — not because it came from hermes-agent.

# Hermes Tool Guardrails

Defense-in-depth for shell command execution. Works alongside YAMTAM's hook layer — hooks block at the OS level, this skill enforces at the agent decision level before the call is even made.

**Trigger phrases:** "command approval", "allowlist", "safe commands", "guardrails", "restrict tools", "auto-deny subagent", "command safety"

---

## Three Execution Modes

| Mode | Context | Behavior |
|------|---------|----------|
| **Interactive** | CLI session with human present | Prompt for approval on risky commands |
| **Non-interactive subagent** | Spawned worker agent | Auto-deny anything not in allowlist |
| **Cron/batch** | Scheduled, unattended | Allow only explicitly approved patterns |

**Default for subagents: non-interactive (safe).** Never pass `--allow-all` when spawning a worker.

---

## Allowlist Config

```yaml
# .yana/tool-guardrails.yaml
approval:
  auto_approve:
    - "git status"
    - "git diff *"
    - "git log *"
    - "npm test *"
    - "cargo test *"
    - "cat *"
    - "ls *"

  require_approval:
    - "git push *"
    - "npm publish *"
    - "cargo publish *"
    - "gh release *"
    - "kubectl apply *"
    - "terraform apply *"

  always_block:
    - "rm -rf *"
    - "git push --force *"
    - "chmod 777 *"
    - "curl * | bash"
    - "eval *"
```

---

## Approval Gate Logic

```python
def check_command(cmd: str, interactive: bool) -> bool:
    if matches_always_block(cmd):
        print(f"[BLOCKED] {cmd}")
        return False

    if matches_auto_approve(cmd):
        return True

    if not interactive:
        # Subagent: deny anything not pre-approved
        print(f"[DENIED — non-interactive] {cmd}")
        return False

    # Interactive session: ask human
    print(f"\n⚠ Approval needed:\n  {cmd}\n")
    answer = input("Allow? [y/N] ").strip().lower()
    return answer == 'y'
```

---

## Subagent Tool Restriction

Give subagents only what they need:

```python
delegate_task(
    goal="Run the test suite and report failures",
    toolsets=["terminal"],
    disabled_tools=[
        "write_file",    # cannot modify files
        "delegate_task", # no further delegation
        "web_search"     # no internet
    ]
)
```

**Minimum toolset by role:**

| Role | Needs | Does NOT need |
|------|-------|--------------|
| Reviewer | Read, Grep | Write, Bash |
| Tester | Read, Write, Bash | Web, Delegate |
| Documenter | Read, Write | Bash, Web |

---

## Dangerous Pattern Detection

Beyond the allowlist — always suspicious:

```python
DANGEROUS_PATTERNS = [
    r"rm\s+-[rf]{1,2}\s",       # destructive delete
    r"\|\s*(ba)?sh",             # pipe to shell interpreter
    r"eval\s+['\"`$]",          # eval with dynamic content
    r"base64\s+-d.*\|",          # decode and pipe
    r"curl.*\|\s*(ba)?sh",       # remote script execution
    r"sudo\s+",                  # privilege escalation
    r"chmod\s+[0-7]*7[0-7]*\s+",# world-writable permission
]
```

---

## Mutation Verification

After write operations, confirm the change happened:

```bash
before=$(sha256sum src/auth.ts | cut -d' ' -f1)
# ... write operation ...
after=$(sha256sum src/auth.ts | cut -d' ' -f1)
[ "$before" != "$after" ] && echo "VERIFIED" || echo "WARNING: no change"
```

---

## YAMTAM Defense Layers

| Layer | Enforces |
|-------|---------|
| `safe-run.sh` (hook) | Hard-blocks dangerous shell patterns |
| `guard-destructive.sh` (hook) | PreToolUse hook for Bash tool |
| This skill (agent level) | Decision before tool is called |
| Subagent toolset restriction | Structural prevention at spawn time |

---

## Anti-Fake-Pass

```
❌ Config defined but not checked before execution
❌ Interactive mode in cron job — hangs forever
❌ Same allowlist for orchestrator and workers — workers need tighter restrictions
❌ "Approve everything in dev" — bad habit that leaks to prod
❌ Skipping mutation verification on critical writes
```

## See Also
- `core/rules/02-terminal-validator.md` — YAMTAM hard-block patterns
- `core/scripts/safe-run.sh` — shell-level enforcement
- `core/hooks/guard-destructive.sh` — PreToolUse hook
