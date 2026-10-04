---
name: agent-creator
description: Create new specialist agents, modify and improve existing agents, and validate agent behavior. Use when users want to create a custom agent from scratch, edit or optimize an existing agent, test an agent against realistic prompts, or improve an agent's description and instructions. Triggers on phrases like "create an agent for X", "make a specialist agent that does Y", "build me an agent for Z", "improve this agent", "update agent instructions", "add a new agent", or whenever a new autonomous specialist role needs to be defined. Always use this skill when the work involves writing or editing .agent.md files, even if the user just says "I need something that specializes in X".
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Agent Creator

A skill for designing, writing, and iteratively improving specialist agents.

At a high level, the process goes like this:

- Understand what role the agent should play and what it should do autonomously
- Draft the agent persona, instructions, and workflow
- Test it with realistic prompts that simulate how users will actually invoke it
- Evaluate both the agent's behavior and the quality of outputs it produces
- Refine the instructions based on what worked and what didn't
- Repeat until the agent behaves reliably and produces excellent results

Your job is to figure out **where the user is in this process** and jump in to help them progress. If they say "I want an agent for X", start from scratch. If they already have a draft, go straight to evaluation and iteration.

---

## Key Concepts

### Skills vs. Agents

Understanding the distinction helps design better agents:

| Concept  | Skill                                      | Agent                                              |
| -------- | ------------------------------------------ | -------------------------------------------------- |
| File     | `SKILL.md`                                 | `<name>.agent.md`                                  |
| Trigger  | Opportunistic (based on description match) | Explicit invocation                                |
| Scope    | Provides instructions to current Claude    | Autonomous specialist running with its own context |
| Identity | No persona — just a workflow guide         | Has a clear persona, expertise, and role           |
| Autonomy | Guides Claude step-by-step                 | Iterates independently until task is resolved      |

Agents are **autonomous specialists**. They should be self-sufficient, persistent, and iterate until the task is truly done — not hand things back to the user prematurely.

---

## Creating an Agent

### Step 1: Capture Intent

Start by understanding what the user wants this agent to do. Extract answers from the conversation if available:

1. What **domain or specialty** should this agent cover? (e.g., security, database, documentation)
2. What **tasks** will it be asked to perform autonomously?
3. What are the **expected outputs**? (code, documents, reports, decisions)
4. What **tools** should it use or have awareness of? (file search, terminal, MCPs, etc.)
5. What **behavioral expectations** exist? (e.g., always document evidence, always test, ask before destructive actions)
6. Are there **existing agents** it should complement or differ from?

If this is being derived from a conversation history, extract context before asking further questions.

### Step 2: Research Existing Agents

Before drafting, always check the `agents/` directory:

```bash
ls agents/
```

Look for:

- Agents with overlapping domain — to avoid duplication and identify gaps
- Patterns and conventions already established in this workspace
- Descriptions that can serve as inspiration or contrast

Read 2-3 existing `.agent.md` files relevant to the domain to absorb the established voice and structure.

### Step 3: Interview for Depth

Ask targeted questions to fill in gaps:

- What should the agent do if it hits an obstacle? (retry, escalate, document?)
- How much autonomy should it have before asking for confirmation? (especially for destructive actions)
- What documentation sources should it consult on startup? (docs/, README, ADRs, etc.)
- Should it interact with other agents? Which ones?
- What defines "done" for this agent? (success criteria)

### Step 4: Write the Agent File

Create the file at `agents/<name>.agent.md` following the anatomy in the next section.

Save it alongside the other agents so it integrates naturally into the workspace.

---

## Agent Anatomy

Every agent file follows this exact structure:

```
agents/
└── <name>.agent.md
    ├── YAML frontmatter  (name + description)
    └── <instructions> block
        ├── Identity & expertise
        ├── Behavioral requirements
        ├── Documentation sources
        ├── Phased workflow
        ├── Testing/validation requirements
        └── Communication & interruption handling
```

### YAML Frontmatter

```yaml
---
name: <lowercase-hyphenated-name>
description: <rich description — see below>
---
```

**Name rules:**

- Lowercase, hyphen-separated
- End with `-specialist` if it's a domain expert (consistent with existing patterns)
- Descriptive of the role, not the technology alone

**Good names:**

```
security-hardening-specialist
api-design-specialist
data-pipeline-specialist
frontend-accessibility-specialist
```

**Bad names:**

```
my-agent
helper
code-agent
python
```

### Description (Critical for Discoverability)

The description is the primary mechanism by which Claude selects agents. A weak description means the agent never gets invoked.

**Proven template:**

```
This custom agent is a <ROLE> responsible for <PRIMARY RESPONSIBILITY>.
Use this agent when <USE CASES AND TRIGGER CONTEXTS>.
The agent will autonomously <BEHAVIOR STYLE> with thorough and iterative
reasoning, documenting all actions and evidence until <COMPLETION CRITERIA>.
```

**Key principles:**

- **Be specific about when to use it** — include concrete trigger contexts, not just abstract role names
- **Name the outputs** — what does the agent deliver? (reports, fixes, plans, documents)
- **State the completion contract** — when does the agent consider itself done?
- **Be slightly "pushy"** — agents tend to be underselected; a description that's assertive about its use cases gets invoked more reliably

**Example (good):**

```
This custom agent is a database specialist responsible for designing, optimizing,
and maintaining databases and data pipelines. Use this agent when you need to
ensure the performance, integrity, and reliability of your data systems
throughout the system lifecycle, from design to production and incident response.
The agent will autonomously conduct data assessments, implement optimizations,
and respond to data-related incidents with thorough and iterative reasoning,
documenting all actions and evidence until the data task is resolved.
```

**Example (weak — avoid):**

```
An agent that helps with databases.
```

### Instructions Block

Wrap all content in `<instructions>...</instructions>` tags:

```markdown
<instructions>

...content...

</instructions>
```

#### 1. Identity & Expertise

Open with a clear role declaration and list of core competency areas:

```markdown
You are a specialist in <DOMAIN> responsible for <MISSION STATEMENT>.

Your primary expertise is in:

1. **<Capability 1>** - <brief description>
2. **<Capability 2>** - <brief description>
3. **<Capability 3>** - <brief description>
```

The capability list anchors the agent's identity and helps it prioritize when tasks overlap multiple domains.

#### 2. Behavioral Requirements

Define the non-negotiables — how the agent should behave regardless of the task:

```markdown
## Behavioral Requirements

- Work **autonomously** until the task is fully resolved. Do not return control to the user mid-task unless confirmation is genuinely required.
- Always **document evidence, changes, and justifications** (logs, diffs, scan results, decisions).
- When you state you will execute a tool or command, **actually execute it** — never just mention it.
- Prefer **current, well-supported solutions** — use recent stable versions unless explicitly constrained.
- Plan before acting. **Reflect after each action** to validate results and update your plan.
```

Adjust these to the specific agent's domain (e.g., a docs agent emphasizes clarity over tool execution; a security agent emphasizes evidence logging).

#### 3. Documentation Sources

Tell the agent where to look for context at startup:

```markdown
## Documentation Sources

On any new task:

- Check `docs/`, `README.md`, `SUMMARY.md`, and relevant ADRs
- Look for `.instructions.md` files under `.github/instructions/`
- Review any existing style guides, linters, or config files relevant to the task
```

#### 4. Phased Workflow

This is the heart of the agent. Define a numbered, phase-based workflow that takes the agent from "receive task" to "task complete":

```markdown
## Workflow

### Phase 1: Understanding the Task

1. Read the task or request carefully
2. Identify ambiguities and resolve them with targeted questions (one at a time)
3. Define success criteria — what does "done" look like?

### Phase 2: Research & Context Gathering

1. Review relevant documentation
2. Explore the codebase or existing artifacts
3. Identify constraints, dependencies, and risks

### Phase 3: Planning

1. Create an action plan with numbered, verifiable steps
2. Identify tools needed
3. Estimate effort and flag risks

### Phase 4: Execution

1. Execute the plan incrementally
2. Validate each step before proceeding
3. Document decisions and evidence as you go

### Phase 5: Validation & Completion

1. Run tests or checks relevant to the domain
2. Verify all success criteria are met
3. Produce a summary of what was done and any follow-up recommendations
```

Customize phases to the domain. A security agent has reconnaissance and threat modeling phases. A docs agent has usability review phases. Don't use generic phases if specialized ones make more sense.

#### 5. Communication & Interruption Handling

Every agent should handle user interruptions gracefully:

```markdown
## Communication

- If the user interrupts with a new instruction, integrate it into your current plan and continue without losing momentum.
- If the user asks a question mid-task, answer it clearly and then ask whether to resume.
- Think out loud when facing ambiguous decisions — explain your reasoning before acting.
- Never conclude your turn with "I'll do this next" — actually do it.
```

---

## Testing the Agent

After writing the agent draft, design **2-3 realistic test prompts** that simulate how users will actually invoke it. These should be:

- Concrete, not abstract — include domain-specific details
- Non-trivial — something that requires multi-step autonomous work
- Varied — cover different aspects of the agent's scope

**Good test prompt:**

```
Our PostgreSQL database is hitting 90% CPU during peak hours. It hosts a
multi-tenant SaaS application with ~500 tables. I've attached the slow query
log. Identify the root causes and propose optimizations with implementation steps.
```

**Weak test prompt (too simple):**

```
Help with the database.
```

### How to Run Tests

Since agents are autonomous specialists, the best way to test them is to:

1. Spawn a subagent using `runSubagent` with the agent's name (if already registered)
2. OR manually follow the agent's own instructions yourself to simulate a run
3. Evaluate the output against the success criteria

For each test run, assess:

| Dimension              | Questions                                      |
| ---------------------- | ---------------------------------------------- |
| **Role alignment**     | Did it stay in character as the specialist?    |
| **Autonomy**           | Did it work without unnecessary hand-holding?  |
| **Output quality**     | Was the output accurate, complete, and useful? |
| **Workflow adherence** | Did it follow the phased workflow?             |
| **Documentation**      | Did it document decisions and evidence?        |
| **Completion**         | Did it deliver a clear, actionable result?     |

---

## Improving the Agent

After evaluating test runs, identify the most impactful change to make. Common issues and their fixes:

| Issue                                          | Fix                                                                  |
| ---------------------------------------------- | -------------------------------------------------------------------- |
| Agent stops and asks too many questions        | Strengthen autonomy language in Behavioral Requirements              |
| Agent misses its specialty scope               | Sharpen the identity section and capability list                     |
| Agent never gets selected                      | Rewrite the description with stronger use cases and trigger contexts |
| Output is generic or shallow                   | Add domain-specific validation steps to the workflow                 |
| Agent doesn't document its work                | Add explicit documentation requirements to each workflow phase       |
| Agent is too rigid / struggles with edge cases | Add an "Unexpected Situations" section with escalation guidance      |
| Instructions are vague                         | Replace vague directives with concrete examples                      |

### Iteration Principles

1. **Change one thing at a time.** Small, targeted changes are easier to evaluate.
2. **Explain the why.** Instead of writing `ALWAYS do X`, explain _why X matters_ — agents reason better when given context.
3. **Don't over-specify.** Too many rigid rules create brittle agents. Give the agent enough context to reason well, not a rigid script.
4. **Read the transcript, not just the output.** If the agent wasted 5 steps on something unnecessary, that's a signal to remove the instruction that caused it.
5. **Generalize from examples.** Don't add a rule just to fix one test case — think about what general principle would prevent the whole class of error.

---

## Description Optimization

Once the agent is working well, optimize its description for discoverability.

Generate 10-15 eval queries — a mix of should-trigger and should-not-trigger. Focus on near-misses: queries that share keywords with the agent's domain but should actually be handled by a different specialist.

**Good should-trigger example:**

```
Our API starts returning 503s when traffic spikes above 200 RPS. I've checked
the load balancer logs and there's no obvious bottleneck there. Can you
investigate the backend service layer and propose a scaling strategy?
```

**Good should-not-trigger example (adjacent but different specialist):**

```
I need to document our microservices API endpoints so the frontend team
can integrate. Can you generate OpenAPI specs from our existing route handlers?
```

(This belongs to documentation-specialist, not developer-specialist)

Review the eval queries before running them — bad queries give false signal.

---

## Agent Registration

Once the agent is finalized:

1. Save to `agents/<name>.agent.md` (relative to workspace root)
2. The agent will appear in the agents list available to `runSubagent`
3. Update any documentation that enumerates available agents (e.g., `task-orchestration-specialist` references)
4. If this agent replaces or supersedes an existing one, note the overlap explicitly

### File Naming Convention

Follow the pattern established by all existing agents:

```
<domain>-<qualifier>-specialist.agent.md
```

Examples:

```
database-specialist.agent.md
cybersecurity-specialist.agent.md
frontend-accessibility-specialist.agent.md
api-design-specialist.agent.md
```

---

## Quality Checklist

Before considering an agent complete, verify:

- [ ] Name is lowercase-hyphenated and ends with `-specialist` (if domain expert)
- [ ] Description follows the 3-sentence template (role, use cases, completion contract)
- [ ] Description is specific enough to distinguish this agent from similar ones
- [ ] Instructions are wrapped in `<instructions>...</instructions>`
- [ ] Identity/expertise section is clear and specific
- [ ] Behavioral requirements explicitly state autonomy expectations
- [ ] Workflow has at least 3 named phases with numbered steps
- [ ] Agent cites where it should look for documentation (`docs/`, `README.md`, etc.)
- [ ] Instructions explain the _why_ behind key requirements (not just MUST/NEVER rules)
- [ ] Agent has been tested with at least 2 realistic prompts
- [ ] Communication/interruption handling is defined

---

## Reference Patterns

### Minimal viable agent (new domain)

```markdown
---
name: <name>-specialist
description: This custom agent is a <role> responsible for <responsibility>.
Use this agent when <use cases>. The agent will autonomously <behavior>
with thorough and iterative reasoning, documenting all actions and evidence
until <completion criteria>.
---

<instructions>

You are a specialist in <domain> responsible for <mission>.

Your primary expertise is in:

1. **<Area 1>** - <description>
2. **<Area 2>** - <description>
3. **<Area 3>** - <description>

## Behavioral Requirements

- Work autonomously until the task is fully resolved.
- Document all decisions, changes, and evidence as you work.
- When you state you will execute something, actually execute it.
- Use the latest stable versions of any tools or libraries unless constrained.
- Plan before acting; verify results after each step.

## Documentation Sources

At the start of any task:

- Review `docs/`, `README.md`, `SUMMARY.md`
- Check `.github/instructions/` for project conventions
- Identify any relevant configuration files

## Workflow

### Phase 1: Understanding the Task

1. Parse the request and identify ambiguities
2. Define success criteria
3. Identify required tools and dependencies

### Phase 2: Research & Analysis

1. Gather context from documentation
2. Explore relevant artifacts
3. Identify risks and constraints

### Phase 3: Planning

1. Create a numbered action plan
2. Flag risks and dependencies

### Phase 4: Execution

1. Implement incrementally
2. Validate each step
3. Document evidence

### Phase 5: Validation & Handoff

1. Verify all success criteria are met
2. Run domain-specific checks
3. Summarize results and next steps

## Communication

- If interrupted by new instructions, incorporate them and continue without losing momentum.
- If asked a question mid-task, answer clearly, then ask if you should resume.
- Never end a turn with "I will do X next" without actually doing it.

</instructions>
```

### When updating an existing agent

Before editing, always read the current file in full. Make targeted edits — never rewrite the entire file unless the structure is fundamentally broken. Preserve working sections and modify only what needs improvement. After editing, re-test with the same prompts used before to confirm the change made things better.
