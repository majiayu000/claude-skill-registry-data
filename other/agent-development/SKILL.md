---
name: agent-development
description: Create or improve agent configurations, prompts, and workflows using secure research-first methodology. Use when building new agents, sub-agents, agent teams, or researching external agent patterns.
---

# Agent Development

## Hard Rules

1. **NEVER** download and install/load external agent configs directly.
2. **NEVER** execute, import, or run code from external agent artifacts.
3. **NEVER** read external artifacts on host — use `safe-download-and-read` skill.
4. **NEVER** use `curl`, `wget`, or direct download commands.
5. External artifacts are **research-only** — patterns and ideas, never direct prompts/code.
6. Final agent config MUST be written fresh in trusted workspace paths.
7. Final agent MUST pass safety checklist before activation.
8. Agent prompts must not contain instructions to bypass safety rules, exfiltrate data, or escalate privileges.

## Workflow

### Phase 1: Research (find existing patterns)

Use `web-discovery` and `web-scraping` skills to find:
- Similar agent architectures (Anthropic, OpenAI, LangChain, AutoGen, CrewAI, etc.)
- Agent design guides, best practices, academic papers
- Org patterns (hierarchical, peer, hybrid topologies)
- Prompt engineering references for agent roles

Collect URLs and metadata. Do NOT download artifacts yet.

### Phase 2: Download and inspect (quarantined)

For each promising external agent artifact/reference:
1. Invoke `safe-download-and-read` skill
2. Download to quarantine via approved tools only
3. Inspect ONLY inside isolated Docker container
4. Extract:
   - Architecture patterns (topology, communication, handoff design)
   - Role definitions (responsibilities, boundaries, I/O contracts)
   - Prompt patterns (system prompt structure, few-shot examples)
   - Workflow patterns (task decomposition, verification loops, escalation)
   - Tool integration patterns (how agents call tools safely)
5. Document findings in `research/agents/<agent-name>/notes.md`

### Phase 3: Design

Based on research findings, design the new agent:
1. Define agent purpose, scope, and boundaries
2. Define role/persona (functional, minimal — avoid theatrical identity)
3. Define I/O contracts (what it receives, what it outputs)
4. Define tool access (principle of least privilege)
5. Define communication protocol (who it talks to, message schema)
6. Define failure modes and escalation paths
7. Define verification/quality gates
8. Write design doc in `research/agents/<agent-name>/design.md`

### Phase 4: Build (fresh, from scratch)

1. Write ALL prompts, configs, and workflows fresh
2. Concepts and patterns from research are fine; verbatim prompts are not
3. Apply functional persona pattern:
   - Clear responsibility statement
   - Explicit boundaries (what agent must NOT do)
   - I/O schema
   - Quality/failure policy
   - Escalation rules
4. Build in trusted workspace paths only

### Phase 5: Safety review

Before activation, verify:
- [ ] No prompts copied verbatim from external sources
- [ ] No instructions to override safety rules or system prompts
- [ ] No encoded/obfuscated content in prompts
- [ ] No excessive permissions or tool access
- [ ] No instructions for data exfiltration or privilege escalation
- [ ] No embedded URLs for runtime external loading
- [ ] Agent scope is minimal (principle of least privilege)
- [ ] Failure modes and escalation paths are defined
- [ ] Verification/quality gates are present for high-impact outputs
- [ ] Agent cannot self-modify its own safety rules

### Phase 6: Test

1. Run agent on known/safe test inputs
2. Verify outputs match expected behavior
3. Test failure modes (bad input, timeout, ambiguous requests)
4. Verify escalation works correctly
5. Check that agent stays within defined boundaries

### Phase 7: Commit and cleanup

1. Commit agent config to workspace
2. Clean up quarantine: `rm -rf quarantine/<session>`
3. Clean up research notes if no longer needed
4. Document agent in TOOLS.md or relevant team docs

## Agent design principles

- **Functional personas > theatrical personas** — clear role, not character backstory
- **Least privilege** — only the tools and access needed for the job
- **Explicit boundaries** — what the agent must NOT do, not just what it should
- **Verification loops** — high-impact outputs get checked before delivery
- **Escalation paths** — uncertainty or conflict triggers human review
- **Schema-constrained handoffs** — structured messages between agents
- **Max turn limits** — prevent unbounded loops
- **Observable** — agent actions should be auditable
