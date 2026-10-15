---
name: agent
description: Initialize any agent by name -- looks up the dispatch table and runs the right primitive (skill, daemon, integration, external).
version: 0.1.0
execution-mode: side_effecting
meta-skill: dispatch
meta-skill-mode: invocation-time
meta-skill-topology: decision-tree
argument-hint: "<agent-name> [action] (e.g., \"arbiter\", \"lead-doctor status\", \"codex delegate security audit\")"
category: fleet-ops
status: candidate
---
# Agent Dispatch

Initialize, query, or interact with any named agent in the fleet. Resolves the agent name to its execution primitive and runs the appropriate action.

## Usage

```
[agent] <name>                  # Default action (status for daemons, run for integrations)
[agent] <name> status           # Check agent status (process, bus, health)
[agent] <name> run [args]       # Execute the agent's primary function
[agent] <name> logs             # Tail recent logs or bus messages from this agent
[agent] <name> delegate <task>  # Prepare a delegation packet for external agents
```

## Dispatch Table

The dispatch table lives in `playbooks/AGENT_REGISTRY.md` under
the **Dispatch Table** section. It maps every agent name to:
- **Primitive**: skill, agent-def, daemon, integration, ci-workflow, external, entry-script
- **Invocation**: the actual command or action to take
- **Default action**: what happens when no action is specified

## Execution

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=agent] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 1. Parse arguments

Extract `$ARGUMENTS` into:
- `AGENT_NAME`: first word (required)
- `ACTION`: second word (default: per dispatch table)
- `ARGS`: remaining words

### 2. Resolve agent identity

```bash
# Check canonical agents, autonomous services, and aliases
python3 -c "
from hummbl_governance.services.agent_identity import canonicalize, get_status, get_trust_tier, AUTONOMOUS_SERVICES, CANONICAL_AGENTS
name = '$AGENT_NAME'
canonical = canonicalize(name)
print(f'canonical={canonical}')
print(f'status={get_status(name)}')
print(f'trust={get_trust_tier(name)}')
print(f'is_service={name in AUTONOMOUS_SERVICES or canonical in AUTONOMOUS_SERVICES}')
print(f'is_agent={canonical in CANONICAL_AGENTS}')
"
```

If not found in identity registry, check the dispatch table in AGENT_REGISTRY.md.

### 3. Look up dispatch table

Read `playbooks/AGENT_REGISTRY.md` and find the row matching `AGENT_NAME` in the dispatch table.

### 4. Execute by primitive type

#### Daemon (launchd)
Default action: **status**
```bash
# Check process
launchctl list | grep -i "$AGENT_NAME"
# Recent bus messages from this agent
grep "$AGENT_NAME" _state/coordination/messages.tsv | tail -10
# Logs (if available)
cat ~/Library/Logs/hummbl/$AGENT_NAME.log 2>/dev/null | tail -20
```

If action is `run`: warn that daemons are managed by launchd. Suggest `launchctl kickstart` if they want to force a run.

#### Integration (Python adapter)
Default action: **run**
Execute the invocation command from the dispatch table and interpret the output.

#### External agent (codex, gemini)
Default action: **delegate**
Chain to `[delegate]` skill with the agent name and any provided task description.
Apply guardrails from `~/.agents/rules/` (gemini-guardrails.md, _archived/kimi-guardrails.md).

#### CI Workflow (GitHub Actions)
Default action: **status**
```bash
gh run list --workflow="$WORKFLOW_FILE" --limit 3
```

#### Entry Script (bin/)
Default action: **run**
Execute the script from the dispatch table.

#### Agent Def (Claude Code session persona)
Default action: **info**
Read the agent definition file and summarize capabilities.
Note: Agent defs can only be initialized at session start, via your runtime's agent-init mechanism (see the runtime binding table in `rules/skill-provider-neutrality.md`).

#### Skill (existing skill)
Default action: **run**
Chain to the skill: invoke `[skill-name]` directly.

### 5. Output format

```
## Agent: <display_name>
**Canonical ID**: <id> | **Primitive**: <type> | **Trust**: <tier> | **Status**: <status>

### Result
<action output, interpreted>

### Recent Bus Activity
<last 5 bus messages from this agent, if any>
```

## Error Handling

- **Unknown agent**: List similar names from the registry. Suggest `[agent-roster]` for full list.
- **Retired agent**: Show retirement reason from registry. Do not execute.
- **Deprecated identity**: Reject. Show canonical name if one exists.
- **Probation agent**: Warn about guardrails before executing.

## Examples

```
[agent] arbiter              → runs arbiter score, shows quality digest
[agent] lead-doctor          → shows daemon status + recent health transitions
[agent] lead-doctor logs     → tails lead-doctor bus messages and log files
[agent] codex delegate "run security audit on services/"
                            → prepares delegation packet with context
[agent] gemini status        → shows probation status, recent bus activity, guardrail summary
[agent] config-drift         → shows daemon status + last drift check result
[agent] quality-arbiter      → shows last CI run status for quality-arbiter.yml
```

## Skill Chains

### Mandatory

None — meta-skill; the dispatched skill carries its own mandatory chains. This skill only resolves the dispatch table and delegates.

### Advisory

- After `[agent] <name> status` → `[agent-roster]` for fleet-wide context
- After `[agent] <name> delegate` → `[delegate]` to complete the delegation packet
- After `[agent] <name> logs` → `[debug-test]` if logs reveal errors worth investigating
- For Devin→opencode delegation → `[cross-runtime-bridge]` (`python ~/bin/cross_runtime_bridge.py delegate "<task>" --workdir <dir> --auto`)

## Authority

- **T1 (TRUSTED)**: May run freely
- **T2 (Active/High)**: May run freely
- **T3 (Medium)**: Operator approval required for side_effecting targets; read-only actions (status, logs) permitted
- **T4 (Probationary)**: May run advisory targets only (status, info, logs); side_effecting targets BLOCKED
- **Operator**: Override any restriction
