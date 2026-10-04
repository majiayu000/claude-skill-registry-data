---
name: ai-engineering-maturity
description: >
  Framework for the 8 stages of AI engineering maturity (team and organization view). Based on the Upsun article by Fabien Potencier (https://upsun.com/blog/8-stages-ai-engineering-maturity/), which adapts Steve Yegge's individual "AI-assisted development" trust gradient into an organizational SDLC model. Use to assess adoption of AI tooling (Grok skills/agents/prompts, MCP, shared context, guardrails), diagnose drift or islands, plan advancement without skipping stages, and ensure AI amplifies good foundational practices rather than bad ones. Always reference alongside copilot-instructions, git-workflow-guardrails, and load-project-cache-first.
user-invocable: true
disable-model-invocation: false
---

# AI Engineering Maturity — 8 Stages Framework (ndestates-io .grok)

**Primary source (full article + visuals)**: https://upsun.com/blog/8-stages-ai-engineering-maturity/

This skill makes the framework native and actionable inside Grok sessions for this project. It shifts focus from *individual developer* (Yegge levels: autocomplete → parallel agents) to *team + organization*. "Team" here includes humans + our AI tooling (Grok + .github/skills/agents/prompts/MCP servers + shared context). "Organization" includes leadership, budgets, governance, delivery cadence, and cross-team coordination.

**Core vocabulary (from the article)**:
- **Team**: Group working toward the same outcome (engineers + product + design + QA + the AI "agent slots" and shared tooling they use).
- **Organization**: All teams + leadership + governance + budgets above them.
- AI is an **amplifier**: It accelerates whatever practices already exist (good or bad). The "10x" rarely appears at org level until the whole distribution moves together.
- **Shared context engineering** (AGENTS.md equivalents, curated skills/prompt libraries in-repo, project memory) is explicit work.
- **Security & governance before scale**.
- **Eval becomes the product** at higher stages.
- Do **not skip stages**. The pain/friction of the current stage is the evidence and motivation for the next. Governance, testing, and shared context are prerequisites for autonomous agents.
- No org is uniform: the number is a "center of gravity", not a label for every individual/team.

## The 8 Stages (condensed from the source for quick reference + project mapping)

### Stage 1: The vacuum
Leadership has taken no real position (or just bought licenses and stopped). Developers form ad-hoc habits: pasting code into any chat, no shared context files, no agent setup, no managed keys or guardrails. This is a necessary learning/intuition-building phase. "Don’t mistake silence for inaction. Your developers have already decided for themselves."

**Project mapping**: Pre-.grok era or when individuals ignore the shared tooling.

### Stage 2: The drift
Individuals have decided on their own. One engineer has sophisticated local agents, personal prompts, custom skills, a private AGENTS.md. The person next to them is unchanged for years. Variation looks "normal". "This is the last stage where inaction is free." Once visible on delivery, it becomes a team problem.

**Project mapping**: Some sessions use full .github/prompts/daily-standup-with-cache.prompt.md + spawn_subagent + our .grok/ ; others bypass for ad-hoc prompts.

### Stage 3: The islands
Gaps move from individuals to teams and become visible on the delivery calendar. One team has shared AGENTS.md, MCP servers, reusable skills → throughput jumps. The neighboring team still works like it's 2024. Tooling gap hardens into resentment.

**Project mapping**: Different sub-teams or contributors (or human vs "AI-augmented" flow) advancing at different rates.

### Stage 4: The standardization bet (first stage requiring real leadership commitment)
AI becomes a deliberate organizational capability.
- Context engineering is explicit: shared AGENTS.md + curated skill/prompt library in the repos (encode knowledge once).
- Security & governance *before* scale: SSO/SCIM, secret scanning, PR gates on agent output, audit logs, approved models/tools behind a gateway.
- Training is ongoing (built around early champions from Stage 2).

**Project mapping (strong alignment)**: This .github/ + .grok/ structure (native full-content skills/prompts/agents in-repo, no thin links), dual .github/ for Copilot parity, mandatory MCP/agent/prompt threat scans in security checklist, git-workflow-guardrails + ddev-local-runtime as governance gates, cache-first discipline.

### Stage 5: The workflow redesign
Stage 4 upgraded tools; Stage 5 redesigns the factory floor.
- Spec-first is default (the spec lives in the repo as the agent's primary entry point; agents can't work well from vague tickets).
- Code review becomes risk-based: "Does this match the spec? Do the tests prove it? Blast radius if wrong?"
- CI gates treat agent-opened PRs identically to human ones.
- Evals run right next to unit tests.
- Expect a productivity dip (role shifts from "writing code" to "reviewing + orchestrating"). Watch *quality*, not just velocity.

**Project mapping**: Our load-project-cache-first + daily-standup-with-cache + structured TODOs + branch-context-agent + guardrails already push spec/context-first. Agent PRs (if any) must follow full gates.

### Stage 6: The operating system
Changes what a "team" is composed of and how teams coordinate.
- Sprints can contain "three engineers and five agent slots".
- Humans look more like product managers: writing specs, debating the AI, verifying tests/outcomes.
- TDD becomes non-negotiable (agents optimize for passing tests; weak suites get gamed).
- Parallel agents in sandboxes have real cost (token budgets + per-run observability required).
- Shared context (project memory, skills, prompt libraries, MCP servers) is treated as real infrastructure — maintained as team assets and coordinated across teams.

**Project mapping**: spawn_subagent usage, our memories/INDEX + docs/codebase cache as "project memory", skills as reusable "slots", guardrails enforcing budgets/hygiene indirectly.

### Stage 7: The bright factory
Agents write and ship whole units of work with minimal human authorship; the human role is supervisor. Most organizations are still "babysitting" — agents kicked off from a personal laptop terminal, looping locally, opening PRs from a dev machine, with no shared runtime and no central record of what ran or why. The local-machine detail is the differentiator.

**Project mapping**: Current state for many advanced users of Grok (local sessions).

### Stage 8: The autonomous factory
Agents move off individual laptops onto shared infrastructure: scheduled runs in sandboxed environments, centralized logs and traces. A migration or recurring task that used to need babysitting now runs overnight and reports results in the morning.
- Recurring jobs are first-class citizens (dependency updates, security patches, test expansion, etc.) with defined success criteria and automatic escalation on failure.
- **Eval becomes the product**: Knowledge that used to live only in people's heads now lives in agent configs, skills, and eval suites that gate every merge. "Your standards no longer live in someone's head. They live in the system."

**Project mapping (aspirational target for .grok evolution)**: Our shared .grok/ + docs/codebase/ + TODO carry + security/MCP scans + guardrails + cache discipline are the foundation. Future: more automated evals, scheduled "agent" maintenance jobs, stronger in-repo eval suites that our skills reference.

## Honest Caveats (verbatim spirit from source)
- No organization sits cleanly on a single stage. You will have teams (or tool usages) at Stage 6 next to others still in Stage 1. The number is a center of gravity.
- You should not skip stages. Going straight to autonomous agents without the governance, testing, and shared context is how projects get canceled. The friction/pain of the current stage is the lesson that justifies the next.
- Stay skeptical. Hype is loud; evidence is quieter. Treat every promise (including this one) with care.
- The autonomous factory is the direction. The hardest part is not the agents — it is trusting them enough to move them off laptops onto shared, observable infrastructure. Build with evidence: one eval, one recurring verified task, one deployment at a time.

## Application & Principles for ndestates-io + Grok

This project already has strong Stage 4+ artifacts precisely because of the deliberate .grok investment (caching, skills, agents, guardrails, dual native + Copilot paths). AI tooling here is meant to **amplify** our existing strong practices (strict DDEV runtime, test DB safety, recovery-first, security checklist on every form/MCP/agent change, cache-first token efficiency, TODO discipline, branch guardrails) rather than paper over weak ones.

**Mandatory principles when using or extending Grok on this project**:
- **Shared context over individual drift** (Stage 2/3 prevention): Always start sessions with `.github/prompts/load-project-cache-first.prompt.md` or `.github/prompts/daily-standup-with-cache.prompt.md`. Prefer spawning subagents and using the curated .github/skills/ + prompts/ + memories/ over personal one-off prompts. Update the shared assets (not local copies).
- **Security & governance before any scaling of AI/agent/MCP usage** (Stage 4): Any change to skills, agents, prompts, or MCP-related behavior triggers the full security checklist (including `mcp-threat-*.txt` scan). See copilot-instructions §3 and git-workflow-guardrails.
- **Spec / context first** (Stage 5): Tasks should be well-specified in TODO, branch context, or clear prompts backed by cache/docs. Vague requests are poor inputs for agents.
- **Risk-based review + evals as gates** (Stage 5/8): Treat AI-generated output (code, plans, analyses) with the same (or higher) scrutiny as human work. Use existing agents (security-audit, test-safety, branch-context, etc.) as automated "evals".
- **Don't skip stages**: When tempted to go straight to "autonomous" heavy agent usage, first ensure the foundations (this skill + guardrails + cache + tests + DDEV) are solid.
- **AI is an amplifier**: Our disciplined processes (DDEV-only, test DB only, MCP threat scans on every relevant change, cache + TODO as "standards living in the system") will be amplified. Sloppy habits will also be amplified faster.
- **Center of gravity view**: When planning or reviewing, surface where the project/team currently sits for AI-augmented work and what the next concrete step is (e.g. "improve shared skill library", "add more eval gates in guardrails").
- **Cost & observability** (Stage 6): Be mindful of parallel agent runs and token spend. Use monitoring (errors.log etc.) for agentic flows.

**Assessment questions (use when this skill is invoked or at standup)**:
- Where is the center of gravity for AI-assisted work on this project right now (individual habits vs. shared .grok/ usage)?
- Are we seeing islands (different contributors/flows at very different stages)?
- Have we encoded our standards in the system (.grok/, docs/codebase/, TODO carry, security scans) or do they still live only in heads?
- For any new capability (new skill, new MCP server, heavier agent usage): have we done the Stage 4 security/governance work first?
- Are we treating evals/tests/guardrails as first-class and running them on AI output?
- Is the current workflow still "babysitting on laptop" or moving toward shared infrastructure/scheduled/audited runs?

**When to invoke this skill**:
- At the start of sessions that involve extending Grok (new skills/agents/prompts).
- When diagnosing slow org-level productivity gains despite individual wins.
- As part of planning or branch context reviews.
- Periodically in daily-standup synthesis to track advancement.

Full original article (including the big maturity diagram) should be read for depth: https://upsun.com/blog/8-stages-ai-engineering-maturity/

Always cross-reference with:
- `.github/skills/copilot-instructions/SKILL.md` (especially MCP/agent/prompt security rules and DDEV/guardrails)
- `.github/skills.github/skills/git-workflow-guardrails/SKILL.md/SKILL.md`
- `.github/skills.github/prompts/load-project-cache-first.prompt.md` and `daily-standup-with-cache`
- `docs/codebase/CONCERNS.md` and TODOs

This skill is self-contained and native to .grok (GitHub Copilot compatible). A parallel may exist under .github/ for Copilot users.

**Grok execution note**: When this skill is active or referenced, surface the current assessed stage + one concrete recommended advancement step in briefings. Cite the source URL.