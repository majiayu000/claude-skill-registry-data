---
name: scaffold-subagent
description: Scaffold a new sub-agent inside an EXISTING fleet project — create the agent directory (`openfleet/agents/<name>/`), the agent.yaml manifest, the CLAUDE.md/SOUL.md/AGENTS.md trio (per AICP fleet convention), source/test stubs, register in fleet's `agent-tooling.yaml` + `agent-identities.yaml`, and verify the agent registration is visible. Distinct from `scaffold` (whole new top-level project) and `scaffold-monorepo` (multi-package). Sister to `openclaw-add-agent` which REGISTERS the agent with a running OpenClaw deployment — this skill scaffolds the AGENT FILES; openclaw-add-agent activates them. Loads when the operator says "scaffold a new agent", "add a new sub-agent", "create the X agent in the fleet", "stand up a new agent role".
argument-hint: <agent-name> [fleet-project-path]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# scaffold-subagent

The sub-agent skeleton skill. Reads the fleet project's conventions, creates the agent directory + the AICP context trio (CLAUDE.md/SOUL.md/AGENTS.md) + agent.yaml manifest + source/test stubs, registers in fleet manifests. Sister to `openclaw-add-agent` which then activates the scaffolded agent in a running OpenClaw deployment.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "scaffold an agent", "create a new sub-agent", "add the X agent", "stand up a new fleet agent role".
- **Mission-bound**: a fleet project has identified a gap (no architect agent, no QA agent, no integrator) — operator wants the structure created.
- **Sister-project agent**: openfleet adding a new agent class; sister projects (dspd, nnrt) following the same trio convention.

Do NOT load when:

- Whole new top-level project — load `scaffold`.
- Multi-package monorepo — load `scaffold-monorepo`.
- Adding a NEW MCP tool to an existing agent — that's an `evolve-plugin-system` concern.
- Deployment-time registration (gateway register, MC visibility) of an already-scaffolded agent — load `openclaw-add-agent`.
- Bootstrap an OpenClaw deployment from scratch — load `openclaw-setup` first.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read fleet conventions + check preconditions

**Trigger**: skill loaded; operator named agent + (optional) fleet path.

**Process**:

1. Resolve inputs:
   - Agent name: from `$0` arg. Convention: kebab-case, role-descriptive (e.g., `architect`, `qa-runner`, `migration-specialist`).
   - Fleet project path: from `$1` arg, default current directory.
2. Verify fleet project exists and is structured:
   ```bash
   ls <fleet>/agents/ <fleet>/config/agent-tooling.yaml <fleet>/config/agent-identities.yaml 2>/dev/null
   ```
   If any are missing: stop, point operator to `openclaw-setup` first.
3. Read existing agent conventions to copy (don't reinvent):
   ```bash
   ls <fleet>/agents/   # what other agents exist
   ls <fleet>/agents/<one-existing>/   # the trio shape: CLAUDE.md / SOUL.md / AGENTS.md / agent.yaml / src / tests
   ```
   Capture the exact directory structure used by existing agents. Match it.
4. Check for name collision:
   ```bash
   ls <fleet>/agents/<agent-name>/ 2>/dev/null && echo "AGENT EXISTS"
   grep -r "^\s*-\s*name:\s*<agent-name>" <fleet>/config/ 2>/dev/null
   ```
   If existing: stop and ask operator if this is a re-scaffold (rare; usually means abort and rename).
5. Identify the agent's MISSION + CAPABILITIES from operator. If unclear, surface specific questions:
   - What problem does this agent uniquely solve? (the mission, one sentence)
   - What 3-5 capabilities define its competence?
   - What stage(s) of work does it own (per fleet's stage map)?
   - What permission mode is its default — Think / Edit / Act?
   - What backend preference fits its work (cost-sensitive, audit-safe, fast)?

**Quality bar (Operation 1 done when)**:

- [ ] Agent name + fleet path resolved.
- [ ] Fleet structure verified (agents dir + config files exist).
- [ ] Existing agent conventions captured (directory shape + file set).
- [ ] No name collision (or operator-authorized re-scaffold).
- [ ] Mission + capabilities + stages + mode + backend identified explicitly.

### Operation 2: Create agent directory + the AICP trio

**Trigger**: Operation 1 inputs validated.

**Process**:

1. Create agent directory matching fleet convention:
   ```
   <fleet>/agents/<agent-name>/
   ├── agent.yaml          # manifest
   ├── CLAUDE.md           # Claude Code context for this agent
   ├── SOUL.md             # agent identity / personality / values
   ├── AGENTS.md           # cross-tool context (mission + rules + commands)
   ├── README.md           # human-facing — what this agent is, how to invoke
   ├── src/                # any agent-specific code
   │   └── __init__.py
   ├── tests/
   │   └── test_smoke.py
   └── prompts/            # if the agent has reusable prompt templates
       └── README.md
   ```
2. Author **agent.yaml** — the canonical manifest:
   ```yaml
   name: <agent-name>
   mission: <one-sentence mission>
   stage: <stage(s) the agent owns, per fleet stage map>
   capabilities:
     - <capability-1>: <one-line>
     - <capability-2>: <one-line>
     - ...
   default_mode: think | edit | act
   backend_preference: <local | k2_6_openrouter | ollama_cloud | openrouter | claude>
   budget:
     max_cost_cad: <number>
     max_duration_seconds: <number>
   skills:               # which AICP skills this agent reaches for
     - <skill-name>
     - ...
   tools:                # which MCP / system tools needed
     - <tool>
   visibility:
     mission_control: true
     standing_orders: true
   ```
3. Author **CLAUDE.md** — Claude Code-specific:
   - Agent identity profile (name, mission, stage ownership).
   - Project context (this is part of `<fleet>` — pointer to fleet's CLAUDE.md).
   - Architecture summary (the agent's own internals + how it interacts with siblings).
   - Tech stack (matches fleet's stack — no agent-specific divergence unless explicitly justified).
   - Key principles (3-5 bullets, agent-specific).
   - Pointers (link to `SOUL.md` for values, `AGENTS.md` for cross-tool, fleet's CLAUDE.md for cross-agent).
4. Author **SOUL.md** — agent's identity, personality, values:
   - "I am the <name> agent. My job is <mission>."
   - 3-5 values that shape how the agent makes judgment calls (e.g., "I prefer fewer-but-clearer commits over many-but-fuzzy", "I always verify before acting").
   - 1-2 explicit anti-patterns (what this agent never does).
5. Author **AGENTS.md** — universal cross-tool context for the agent:
   - Hard rules (5-7 bullets the agent never violates).
   - Stage gates if applicable.
   - Quality gates (mode-bound: Think mode never edits, Edit mode never runs commands, etc.).
   - Common commands the agent reaches for.
   - Conventions specific to this agent (commit format, file layout, etc.).

**Quality bar (Operation 2 done when)**:

- [ ] Agent directory matches fleet's existing-agent shape exactly.
- [ ] agent.yaml has all required fields populated.
- [ ] CLAUDE.md/SOUL.md/AGENTS.md trio authored with REAL agent-specific content (not boilerplate).
- [ ] Source + tests stubs exist.
- [ ] Mission, capabilities, mode, backend each appear consistently across the trio + agent.yaml.

### Operation 3: Register in fleet manifests

**Trigger**: Operation 2 agent directory authored.

**Process**:

1. Update `<fleet>/config/agent-tooling.yaml` — add this agent's tooling section. Mirror the format used by existing agents:
   ```yaml
   <agent-name>:
     skills:
       - <skill-1>
       - <skill-2>
     mcp_tools:
       - <tool-1>
     hooks: []
   ```
2. Update `<fleet>/config/agent-identities.yaml` — register the agent's identity:
   ```yaml
   - name: <agent-name>
     mission: <copy from agent.yaml>
     workspace: agents/<agent-name>/
     enabled: true
   ```
3. Update `<fleet>/config/skill-assignments.yaml` (if it exists) — assign the agent to its stage(s).
4. If fleet uses Mission Control: add the agent to MC's known-agents config OR ensure MC's auto-discovery will pick it up on next reload.
5. If fleet uses standing-orders.yaml: add an introduction line so cross-agent communication includes the new agent.
6. Verify YAML validity:
   ```bash
   for f in <fleet>/config/*.yaml; do
     python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "INVALID: $f"
   done
   ```

**Quality bar (Operation 3 done when)**:

- [ ] agent-tooling.yaml registers the agent's skills + MCP tools + hooks.
- [ ] agent-identities.yaml has the new identity entry.
- [ ] skill-assignments.yaml updated if applicable (or noted as "no skill-assignments tracking in this fleet").
- [ ] MC / standing-orders updated for visibility.
- [ ] All modified config YAMLs validate cleanly.

### Operation 4: Smoke + commit + announce

**Trigger**: Operation 3 manifests updated.

**Process**:

1. Smoke the agent's basic existence:
   ```bash
   ls <fleet>/agents/<agent-name>/   # all files present
   cat <fleet>/agents/<agent-name>/agent.yaml | python3 -c "import yaml,sys; yaml.safe_load(sys.stdin)"
   pytest <fleet>/agents/<agent-name>/tests/ 2>&1 | tail -5   # smoke test passes
   ```
2. Verify cross-fleet consistency:
   ```bash
   grep -l "<agent-name>" <fleet>/config/*.yaml | wc -l   # at least 2 (tooling + identities)
   ```
3. Commit as a single, scoped commit:
   ```bash
   cd <fleet>
   git add agents/<agent-name>/ config/agent-tooling.yaml config/agent-identities.yaml [config/skill-assignments.yaml]
   git commit -m "scaffold(agent): add <agent-name> — <mission summary>"
   ```
4. Announce + suggest the next skill:
   - "Agent `<agent-name>` scaffolded at `<fleet>/agents/<agent-name>/`."
   - "Registered in: agent-tooling.yaml, agent-identities.yaml, [skill-assignments.yaml]."
   - "Next: load `openclaw-add-agent` to ACTIVATE this scaffolded agent in the running OpenClaw deployment (gateway registration + MC visibility verification)."
5. If the agent has a stage assignment that overlaps with existing agents: surface the overlap. The fleet may want resolution before activation.

**Quality bar (Operation 4 done when)**:

- [ ] Agent directory present + agent.yaml validates + smoke test passes.
- [ ] Cross-fleet consistency verified (agent name appears in ≥2 config files).
- [ ] Single commit made naming the agent + mission.
- [ ] Operator told the next skill is `openclaw-add-agent` (activation, not scaffold).
- [ ] Stage overlaps with existing agents flagged (or "no overlap" stated).

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Trio mismatch — different mission across CLAUDE.md / SOUL.md / agent.yaml

CLAUDE.md says "this agent reviews architectures". SOUL.md says "I author tests". agent.yaml says mission is "build foundation pieces". Three documents, three missions, none of them aligned. The agent is launched and acts inconsistently because its own context disagrees about what it is.

**The rule**: Operation 2 step 5 — mission appears LITERALLY THE SAME across CLAUDE.md, SOUL.md, AGENTS.md, agent.yaml, and README.md. Same sentence, same words. The trio is a multi-perspective view of ONE identity; if perspectives disagree, the identity is undefined. Always verify with `grep "<mission-phrase>" <fleet>/agents/<agent-name>/*.md` after authoring.

### Gotcha 2: Copying another agent's content verbatim

Operator says "make a new agent like the architect agent". Skill copies architect's files, find-replaces the name, calls it done. New agent has architect's mission language, architect's skill list, architect's anti-patterns. It's not a new agent — it's a renamed clone.

**The rule**: Operation 2 — using existing agents as STRUCTURAL templates is correct (directory shape, file set, format). Copying CONTENT is wrong. Each agent's mission / capabilities / values / hard rules must be authored fresh from Operation 1's specification. Treat existing agents as "what shape goes where", not "what words go in it".

### Gotcha 3: Forgetting fleet manifest registration

Skill creates the agent directory beautifully — agent.yaml, trio, src, tests, all there. Doesn't update agent-tooling.yaml or agent-identities.yaml. The agent EXISTS on disk but is INVISIBLE to the fleet — `openclaw agents list` doesn't show it, MC doesn't know about it, skill discovery skips it.

**The rule**: Operation 3 is non-negotiable. Without manifest registration, the agent is dead code. Operation 4's quality bar verifies the agent name appears in ≥2 config files; if it doesn't, the scaffold is incomplete.

### Gotcha 4: Stage overlap with existing agents undocumented

New agent's stage assignment is "test" — but the fleet already has an existing test-runner agent. Two agents both claim the test stage; OpenClaw routes ambiguously, work doubles up or falls between them. The overlap was never surfaced.

**The rule**: Operation 1 step 5 captures stages explicitly; Operation 4 step 5 flags overlap with existing agents. If two agents claim the same stage, surface to operator BEFORE the commit — they may want one of: split scope, replace existing, or designate the new agent as primary with the existing as fallback.

### Gotcha 5: Backend / mode default that contradicts the mission

Mission is "real-time fleet orchestration with sub-second decisions". Default mode is `think` and backend preference is `claude` (high-quality but high-latency cloud). The defaults guarantee the agent will fail at its mission — every invocation pays cloud-round-trip time, decisions are slow, orchestration falls behind.

**The rule**: Operation 1 step 5 — mode + backend defaults must serve the mission. A latency-sensitive agent gets `local` backend + `act` mode (no human checkpoint between decisions). An audit-sensitive agent gets `k2_6_openrouter` (pinned provider) + `edit` mode (human approves before act). Don't default to "safest" if "safest" is incompatible with the mission.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning. For sub-agent ARTIFACTS specifically, openfleet's existing 10 agents are the live exemplar of the AICP trio convention; their `agent-identities.yaml` is the registration target.

## Domain context

This skill operates in the **backend-ai-platform-python** domain, but its primary target is the **openfleet** sister project where the OpenClaw fleet of 10 agents lives. AICP itself uses skills, not agents-with-trio-files — the skill assumption is "this skill is being invoked from openfleet (or a similar fleet-class project)". The AICP CLAUDE.md/SOUL.md/AGENTS.md trio convention is documented per CLAUDE.md and is the canonical agent-context shape across the AICP fleet ecosystem. Sister projects (dspd, nnrt) follow the same trio for their own agents. The MCP tool surface and skill library this skill registers FROM is AICP's; the deployment that activates the scaffolded agent is OpenClaw's gateway + Mission Control.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| openclaw-add-agent | ACTIVATE a scaffolded agent in OpenClaw | Activation; this skill is scaffold-only |
| openclaw-setup | Bootstrap OpenClaw fleet from scratch | Fleet bootstrap; this skill assumes fleet exists |
| scaffold | New top-level project | Top-level; this skill is sub-agent within fleet |
| scaffold-monorepo | Multi-package monorepo from day 1 | Multi-package; this skill is one agent |
| openclaw-fleet-status | Snapshot of fleet operational state | Read-only state; this skill modifies fleet state |
| openclaw-health | System audit of fleet | Audit; this skill creates an addition to audit |
| evolve-plugin-system | Add NEW skill / MCP-tool / hook surface | Plugin system; this skill is a fleet-internal agent |
