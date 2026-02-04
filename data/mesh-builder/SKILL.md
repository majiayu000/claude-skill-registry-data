---
name: mesh-builder
description: Build TX V4 meshes - agent configs, prompts, routing. Use for new meshes, agent roles, or multi-agent workflows. Triggers - mesh, routing, agents, multi-agent, config.yaml
---

# Mesh Builder

Build meshes (agent workflows) for TX V4.

## Quick Start

```bash
# Test prompt output before deploying
tx prompt <mesh> <agent>              # View built prompt with injected protocol
tx prompt narrative-engine narrator   # Example
tx prompt dev --raw                   # Raw output, no metadata
```

## Documentation

| Topic | Location |
|-------|----------|
| Config fields | `docs/mesh-config.md` |
| FSM (state tracking) | `.ai/docs/mesh-fsm-config.md` |
| Available meshes | `docs/meshes.md` |
| Message format | `docs/message-format.md` |

## Minimal Config

```yaml
mesh: example
description: "What this mesh does"

agents:
  - name: worker
    model: sonnet       # opus | sonnet | haiku
    prompt: prompt.md

entry_point: worker
```

## Writing Prompts

Focus on **workflow only**.

### System Auto-Injects (DO NOT WRITE IN PROMPTS):
- ❌ Message protocol (frontmatter schema, message types, paths format)
- ❌ Routing instructions (how to write messages to other agents)
- ❌ Rearmatter format (success_signal, grade, confidence fields)
- ❌ Workspace structure and paths (auto-injected from config.yaml)
- ❌ Message file naming conventions
- ❌ Tool availability and usage instructions (system provides)

### Write ONLY:
- ✅ Agent role and mandate
- ✅ Workflow steps (what to do, when)
- ✅ Decision trees and logic
- ✅ Domain-specific guidance
- ✅ Quality gates and success criteria

```markdown
# {Agent Name}

You are the {role} agent.

## Workflow
1. Read incoming task
2. {Work steps}
3. Signal completion when finished
```

## Multi-Agent Routing

```yaml
routing:
  agent-a:
    complete:
      agent-b: "Handoff reason"
    blocked:
      core: "Need intervention"
```

See `docs/mesh-config.md` for full routing reference.

## Common Patterns

**Automatic Session persistence**: `continuation: true` or `continuation: [agent1, agent2]`

**MCP tools only**: `toolRestriction: mcp-only`

**Quality evaluation**: `graded: true` or `graded: [checklist, rubric]`

**FSM state tracking**: `fsm:` block for system-managed state variables and logic. Only use if needed, linear workflows generally don't need fsm.

**Parallel execution**: `ensemble: { type: parallel }` for FSM states - See `docs/mesh-fsm-config.md` "Ensemble States" section

**CRITICAL - FSM Entry Routing**: Entry agents in FSM ensemble meshes MUST fan out to ALL ensemble workers. FSM observes these messages to track state, but explicit routing triggers the workers.
```yaml
routing:
  entry:
    complete:
      worker-1: "Spawn worker 1"  # ✅ CORRECT - Fan out to all workers
      worker-2: "Spawn worker 2"
      worker-3: "Spawn worker 3"
      # core: "..."                # ❌ WRONG - Workers never spawn!
```

**Original task injection**: `injectOriginalMessage: true` - Injects original task into downstream agents

**Design documentation**: `playbook_notes:` - Embed architectural rationale in config (replaces separate READMEs)

**Self-assessment metadata**: `rearmatter:` - Agent outputs self-assessment fields (grade, confidence, status) for FSM routing decisions

**Lifecycle hooks**: Auto-commit, brain insights, quality gates

```yaml
lifecycle:
  post:
    - commit:auto    # Auto-commit changes
    - brain-update   # Document insights
```

Available hooks: `worktree:create`, `commit:auto`, `brain-update`, `quality:*`. See `docs/mesh-config.md`.

## FSM (State Tracking)

Add `fsm:` block to track state and provide context to agents.

**IMPORTANT**: If you use FSM, you must also define `routing:` configuration. Routes can exist without FSM, but FSM cannot exist without routes.

**Sequential workflow:**
```yaml
fsm:
  initial: init

  context:
    turn: 0
    workspace: null

  states:
    init:
      agents: [coordinator]
      entry:
        set:
          turn: "$((turn + 1))"
          workspace: "/path/to/turn-$turn"
      exit:
        default: awaiting_work

    awaiting_work:
      agents: [worker]
      exit:
        when:
          - condition: signal == "PASS"
            target: complete
        default: awaiting_work

  scripts: {}
```

**Parallel workflow (ensemble):**
```yaml
routing:
  # Ensemble agents need explicit routing
  rev-1:
    complete:
      synthesizer: "Review 1 complete"
  rev-2:
    complete:
      synthesizer: "Review 2 complete"
  rev-3:
    complete:
      synthesizer: "Review 3 complete"

fsm:
  initial: parallel_review

  states:
    parallel_review:
      ensemble:
        type: parallel          # Required: type inside ensemble block
        agents: [rev-1, rev-2, rev-3]
        aggregation: concat
      exit:
        set:
          results: "$ENSEMBLE_OUTPUT"
        default: synthesize

  scripts: {}
```

**Agents receive injected context:**
```markdown
## FSM Context
state: awaiting_work
turn: 5
workspace: /path/to/turn-5
```

See `docs/mesh-fsm-config.md` for:
- Exit-based routing (when/run/default)
- Ensemble states (parallel execution)
- Self-loops and iteration tracking
- Gates and validation

## Documentation

**`playbook_notes` in config.yaml** (for maintainers)
- Design rationale and architectural decisions
- WHY the mesh is built this way
- Alignment with methodologies/patterns
- Not injected into prompts

**Example:**
```yaml
playbook_notes: |
  This mesh implements the Ralph pattern from ClaytonFarr/ralph-playbook.
  Uses layered quality refinement: haiku drafts, sonnet reviews, opus finalizes.
```

## Debugging

```bash
tx status    # Workers, queue
tx msg       # Message viewer
tx spy       # Real-time activity
tx logs      # System logs
```
