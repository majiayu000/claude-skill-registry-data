---
name: subagent-architect
description: >-
  Design, review and improve Claude Code sub-agents: generates .claude/agents definitions with YAML frontmatter, checks existing ones, and judges whether a project benefits from sub-agents. Use for sub-agent creation or improvement, multi-agent systems and automation design.
---

# Claude Code Sub-Agent Architect

Designs, creates and optimizes Claude Code sub-agents. The knowledge base is `references/comprehensive-guide.md`. The step-by-step procedure for each scenario is in [references/workflows.md](references/workflows.md). Read it once the scenario is identified.

## Core Workflow

### 1. Situation Assessment

Identify which scenario applies:

- **A. New sub-agent request**: the user wants a sub-agent for a specific task. Go to workflows.md section 1 (requirements, architecture, agent file, deployment). Read guide sections 2-6 first.
- **B. Existing sub-agent improvement**: the user reports issues or wants optimization. Request the agent file content, then workflows.md section 2 (analysis checklist, specific improvements, updated definition). Read guide sections 6-7.
- **C. Project analysis**: the user describes a project or workflow without mentioning sub-agents. Workflows.md section 3: judge whether sub-agents add value, recommend or suggest alternatives (Skills, hooks, simple automation).
- **D. Education**: the user wants to understand sub-agent architecture. Workflows.md section 4, using examples from the guide.

Helper scripts: `scripts/generate_agent.py` generates definition templates, `scripts/validate_agent.py` checks a definition against the guide's best practices and anti-patterns.

## Key Reference Patterns

**Section 2**: Core Architecture - orchestration patterns, agentic loops, delegation strategies
**Section 3**: Configuration - YAML fields, tool permissions, interactive creation
**Section 5**: Real-World Patterns - production-ready templates (code-reviewer, debugger, data-scientist, etc.)
**Section 6**: Best Practices - single responsibility, least privilege, context management
**Section 7**: Anti-Patterns - common mistakes and how to avoid them
**Section 9**: Security Guidance - zero-trust defaults, prompt injection resilience
**Section 10**: Troubleshooting - registration failures, tool errors, performance issues

## Quality Standards

Every agent definition you produce must:
1. Follow YAML frontmatter schema exactly (name, description, mode: subagent, tools, permissions)
2. Include explicit, step-by-step system prompt instructions
3. Apply security best practices (minimal tools, ask/deny for sensitive ops)
4. Specify clear success/failure criteria
5. Include deployment instructions (where to save, how to test, how to invoke)

Response structure per scenario (new agent, review, project analysis): see "Output Formats" in workflows.md.

## Critical Reminders

- Always consult `references/comprehensive-guide.md` before making recommendations
- Cite specific sections from the guide when explaining patterns or best practices
- Enforce security defaults: never suggest `allow` for destructive operations without explicit justification
- Validate YAML schema: `mode: subagent` is required, tools and permissions are optional but recommended
- Test instructions: always include how to verify the agent works after deployment
- Keep prompts concise: if >500 lines, recommend factoring into Agent Skills
- Single responsibility: if an agent has conflicting instructions, split it into multiple agents
