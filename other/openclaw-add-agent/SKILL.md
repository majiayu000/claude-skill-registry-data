---
name: openclaw-add-agent
description: Add a new specialized agent to an OpenClaw deployment — create the agent directory, agent.yaml manifest, CLAUDE.md/SOUL.md/AGENTS.md trio, register with OpenClaw, copy auth profiles, verify visibility. Loads when an OpenClaw deployment exists and the operator says "add a new agent", "create agent X", "spin up another agent", "I need a Y agent in the fleet".
argument-hint: <agent-name> [workspace-path]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# openclaw-add-agent

The fleet-extension skill that adds a new specialized AI agent to an existing OpenClaw deployment. Each agent is a Claude Code instance with a scoped role (e.g., `architect`, `implementer`, `qa`, `pm`) running in its own workspace, registered with the OpenClaw orchestrator. AICP exposes the inference + skills these agents consume; OpenFleet runs the agents.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **OpenClaw exists**: project (typically `openfleet`) has an OpenClaw deployment running; operator wants to grow the agent count.
- **Direct verb**: operator says "add a new agent", "create agent X", "spin up another agent", "register a Y agent in the fleet", "I need a new role".
- **Fleet capacity gap**: an existing role is overloaded and the operator wants to specialize a sub-role into its own agent.

Do NOT load when:

- No OpenClaw deployment exists — load `openclaw-setup` first.
- The agent isn't an OpenClaw agent (e.g., it's a Plane integration, a one-off script) — different concern.
- An agent with the same name already exists — load `feature-iterate` (refine existing) or rename the new one.
- The "agent" is conceptual/methodological (a methodology model) — that's a `wiki/config/methodology.yaml` change, not an OpenClaw agent.

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Pick role and confirm slot

**Trigger**: skill loaded; operator confirmed OpenClaw exists.

**Process**:

1. Read existing agents from `openfleet/agents/` (or operator-named workspace root). List names and one-line roles. Cross-reference with `openfleet/config/agent-tooling.yaml` to see which roles are already specialized.
2. Confirm the new agent's role is **distinct** from existing roles — no overlap, clear boundary. State the proposed role + boundary back to the operator: *"Adding `<name>` whose responsibility is X. This is distinct from `<existing>` which does Y because Z."* Wait for confirmation.
3. Validate the agent name: **lowercase with hyphens** (`architect`, `qa-runner`, `pm-coordinator`). Reject CamelCase, underscores, or numbers-as-prefix.
4. Decide workspace path. Default: `openfleet/agents/<name>/`. Operator can override via `$ARGUMENTS` second arg.
5. Read [openfleet/config/agent-tooling.yaml](../../../../openfleet/config/agent-tooling.yaml) to determine which AICP skills the role typically loads. The agent's `agent.yaml` will reference this list.

**Quality bar (Operation 1 done when)**:

- [ ] Existing agents listed; new role's distinctness confirmed.
- [ ] Agent name is lowercase-hyphen-only.
- [ ] Workspace path decided.
- [ ] Skills the agent will load identified from agent-tooling.yaml.
- [ ] Operator approved the role + boundary statement.

### Operation 2: Author the agent files

**Trigger**: Operation 1 confirmed.

**Process**:

1. Create the agent directory: `mkdir -p openfleet/agents/<name>`.
2. Author `agent.yaml` (the manifest OpenClaw consumes):
   ```yaml
   name: <name>
   type: claude-code  # or claude-mem, depending on deployment
   description: One-line role description.
   mission: |
     Multi-line mission statement — what this agent does in the fleet.
     Why it's distinct from sibling agents.
   capabilities:
     - skill1
     - skill2
   mode: think  # or edit, act — per agent's authority level
   workspace: openfleet/agents/<name>
   ```
3. Author `CLAUDE.md` with agent-specific instructions:
   - Role + boundary (verbatim from Operation 1).
   - How this agent receives work (from PM agent? from Plane? from board?).
   - Hard rules specific to this role (e.g., "never modify test files" for an `implementer` agent).
   - Reference to AICP skills it loads.
4. Create `SOUL.md` as an identical copy of `CLAUDE.md`. Per the existing OpenClaw convention, `SOUL.md` is the loader-side filename; `CLAUDE.md` is the developer-side. They MUST stay in sync (use a symlink if the deployment supports it, otherwise commit them as duplicates with a comment noting the sync requirement).
5. Author `AGENTS.md` (universal cross-tool layer per the brain's three-layer pattern):
   - Identity profile (type / domain / scale).
   - Hard rules.
   - Where to find things (skill paths, AICP CLI, fleet registry).
   - Reading order for a new agent (this file → CLAUDE.md → skills).

**Quality bar (Operation 2 done when)**:

- [ ] `agent.yaml` valid YAML; loads via `python3 -c "import yaml; yaml.safe_load(open('agent.yaml'))"` exits 0.
- [ ] CLAUDE.md exists with role + boundary + hard rules + skill list.
- [ ] SOUL.md is byte-identical to CLAUDE.md (verify with `diff CLAUDE.md SOUL.md` returning empty).
- [ ] AGENTS.md authored per the brain's 3-layer agent context pattern.
- [ ] No skills referenced that don't exist in `~/devops-expert-local-ai/.claude/skills/`.

### Operation 3: Register, verify, hand off

**Trigger**: Operation 2 files written.

**Process**:

1. Register the agent with OpenClaw:
   ```bash
   openclaw agents add <name> --workspace openfleet/agents/<name>
   ```
   If the operator's deployment uses a different orchestrator command, use that. Verify exit 0.
2. Copy auth profiles from a sibling agent if available (Claude credentials, ntfy tokens, Plane API key as needed). Check: `openfleet/agents/<sibling>/.credentials/` → `openfleet/agents/<name>/.credentials/`. Don't commit credential files.
3. Verify the agent is visible:
   ```bash
   openclaw agents list   # should include <name>
   openclaw agents status <name>  # should show "registered, not running" or "running"
   ```
4. Update fleet-level docs:
   - `openfleet/config/agent-tooling.yaml`: add the new agent's `skills:` list.
   - `openfleet/README.md` (or fleet's CLAUDE.md): add the agent to the role roster.
5. Suggest the next skill: `openclaw-fleet-status` (verify the agent boots), `openclaw-health` (broader health check after the addition).

**Quality bar (Operation 3 done when)**:

- [ ] `openclaw agents add` exits 0.
- [ ] `openclaw agents list` shows the new agent.
- [ ] Auth profiles in place (or explicitly noted as deferred if creds aren't ready).
- [ ] Fleet-level config + docs updated.
- [ ] Operator told what's next (boot the agent, watch logs, verify it picks up work).

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Role overlap with existing agent

You add `qa-runner` whose mission is "verify code quality" — but the existing `qa` agent already does that. Two agents now compete for the same work; PM agent gets confused which to dispatch to; tasks land in both queues; one agent's work invalidates the other's.

**The rule**: Operation 1 step 2 — explicitly state the boundary against EVERY existing agent, not just the most-similar one. If a sibling can do this work, the new agent isn't justified. Add capability to the existing agent instead, or split via a clearly different scope (e.g., `qa-coverage` vs `qa-correctness` if both axes need their own agent).

### Gotcha 2: SOUL.md and CLAUDE.md drift

Operator (or a future skill) edits `CLAUDE.md` to add a new rule. Forgets to update `SOUL.md`. OpenClaw loads `SOUL.md`; the new rule never reaches the agent at runtime.

**The rule**: keep them byte-identical. Either symlink (`ln -s CLAUDE.md SOUL.md` if deployment allows it) OR add a pre-commit hook that fails if they diverge. Verify with `diff CLAUDE.md SOUL.md` returning empty after every change. If symlinks aren't supported, document the sync rule prominently in BOTH files at the top.

### Gotcha 3: Referencing skills that don't exist

`agent.yaml` lists `skills: [my-cool-skill]` but `.claude/skills/my-cool-skill/SKILL.md` doesn't exist. Agent boots OK, but at first attempt to load the skill it errors silently and falls back to no-skill behavior. Operator sees "agent doesn't seem to know what it's doing" and can't trace why.

**The rule**: validate every skill name in `agent.yaml` against `~/devops-expert-local-ai/.claude/skills/`. Reject capabilities that aren't authored. Add a CI check (or `tools/lint.py` rule) that fails if `agent-tooling.yaml` references a non-existent skill.

### Gotcha 4: Credentials committed by accident

Copying auth profiles, you `cp -r .credentials/` and forget the file is auto-staged. Commit lands with API keys in git history. Standard secret-leak failure mode.

**The rule**: `.credentials/` and similar paths in `.gitignore` BEFORE you copy. Verify with `git status` after the copy — if any credential file appears as a tracked change, abort and add to gitignore. After commit, `git log -p | grep -E "(api_key|secret|token)\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}"` returns nothing.

### Gotcha 5: Agent-tooling.yaml drift

You add the agent's directory and files but forget to update `openfleet/config/agent-tooling.yaml`. The PM agent's dispatcher doesn't know the new agent exists — work never routes to it. The agent sits idle; operator wonders why nothing happens.

**The rule**: Operation 3 step 4 isn't optional. The new agent is invisible to the dispatcher until it's in `agent-tooling.yaml`. Verify by re-reading `agent-tooling.yaml` after the edit; the new agent's name + skills MUST appear.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

The canonical OpenClaw agent layout: `openfleet/agents/<name>/` with the four-file pattern (`agent.yaml`, `CLAUDE.md`, `SOUL.md`, `AGENTS.md`).

## Domain context

This skill operates **across** the AICP and OpenFleet projects. AICP provides the skill library + LocalAI inference; OpenFleet runs the OpenClaw deployment that orchestrates agents. The skill itself lives in AICP because AICP is the canonical home of skills (per the brain's "skill library is one project" principle), but the artifacts it produces live in OpenFleet.

For the fleet topology context, see [docs/architecture/fleet-integration.md](../../../docs/architecture/fleet-integration.md).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| openclaw-setup | No OpenClaw deployment exists | Bootstrap the orchestrator; this skill adds to an existing one |
| openclaw-fleet-status | Check what agents are running + queue health | Read-only check; this skill writes a new agent |
| openclaw-health | Audit OpenClaw + Mission Control + agents | Audit; this skill is creation |
| scaffold-subagent | Create a sub-agent inside a single project | Scoped to one project; openclaw-add-agent is fleet-scoped |
| mvp-agent | New agent in a fleet from zero to operational | Bigger workflow that includes idea→architecture→agent; this skill is just the "register the agent" step |
