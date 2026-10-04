---
name: harness
description: "Configures a harness. A meta-skill that defines specialized agents and creates the skills those agents will use. Use when (1) asked to 'configure a harness' or 'build a harness,' (2) asked for 'harness design' or 'harness engineering,' (3) building a harness-based automation system for a new domain/project, (4) reconfiguring or extending a harness, or (5) handling operations/maintenance requests for an existing harness, such as 'inspect the harness,' 'audit the harness,' 'harness status,' or 'synchronize agents/skills.'"
version: 1.0.0
license: MIT
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: imported
  upstream: C:\Users\Admin\.agents\skills\harness\SKILL.md
---

> Bundled with Unleash skills pack. Source: C:\Users\Admin\.agents\skills\harness\SKILL.md

# Harness — Agent Team & Skill Architect

A meta-skill that configures a harness for a domain/project, defines the role of each agent, and creates the skills those agents will use.

**Core principles:**
1. Create agent definitions (`.claude/agents/`) and skills (`.claude/skills/`).
2. **Use an agent team as the default execution mode.**
3. **Register a harness pointer in CLAUDE.md.** — Record only the minimum pointer information required to trigger the orchestrator skill in a new session: trigger rules and change history.
4. **A harness is not static; it is an evolving system.** — Incorporate feedback after every run and continuously update agents, skills, and CLAUDE.md.

## Workflow

### Phase 0: Current-State Audit

When the harness skill is triggered, first inspect the current state of the existing harness.

1. Read `project/.claude/agents/`, `project/.claude/skills/`, and `project/CLAUDE.md`
2. Branch into an execution mode based on the current state:
   - **New build**: The agent/skill directories do not exist or are empty → Run all phases starting from Phase 1
   - **Existing harness extension**: An existing harness is present and new agents/skills have been requested → Run only the necessary phases according to the Phase selection matrix below
   - **Operations/maintenance**: An audit, modification, or synchronization of the existing harness has been requested → Proceed to the Phase 7-5 operations/maintenance workflow

   **Phase selection matrix for extending an existing harness:**
   | Change type | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
   |----------|---------|---------|---------|---------|---------|---------|
   | Add an agent | Skip (use Phase 0 results) | Determine placement only | Required (including 3-0) | If a dedicated skill is needed (including 4-0) | Modify the orchestrator | Required |
   | Add/modify a skill | Skip | Skip | Skip | Required (including 4-0) | If connections change | Required |
   | Architecture change | Skip | Required | Affected agents only (including 3-0) | Affected skills only (including 4-0) | Required | Required |
3. Compare the existing agent/skill inventory against the CLAUDE.md records to detect inconsistencies (drift)
4. Summarize the audit results for the user and obtain confirmation of the execution plan

### Phase 1: Domain Analysis
1. Identify the domain/project from the user's request
2. Identify core task types (creation, validation, editing, analysis, etc.)
3. Analyze conflicts/duplication with existing agents and skills based on the Phase 0 audit results
4. Explore the project codebase — identify the technology stack, data models, and major modules
5. **Detect user proficiency** — Infer the user's technical level from contextual clues in the conversation, such as terminology and question depth, and adjust the communication tone accordingly. Do not use terms such as "assertion" or "JSON schema" without explanation when speaking to users with limited coding experience.

### Phase 2: Team Architecture Design

#### 2-1. Select an Execution Mode

**An agent team is the highest-priority default.** Whenever two or more agents collaborate, always evaluate an agent team first. Team members coordinate among themselves through direct communication (`SendMessage`) and a shared task list (`TaskCreate`); sharing discoveries, discussing conflicts, and filling gaps improves output quality.

| Mode | When to use | Characteristics |
|------|----------|------|
| **Agent team** (default) | Two or more agents collaborate, real-time coordination and feedback exchange are needed, or intermediate artifacts must be cross-referenced | Self-coordination through `TeamCreate` + `SendMessage` + `TaskCreate` |
| **Subagents** (alternative) | A single-agent task, returning only the result to the main agent is sufficient, or team communication overhead is excessive | Directly invoke the `Agent` tool; parallelize with `run_in_background` |
| **Hybrid** | Phases have different characteristics — for example, parallel collection (subagents) → consensus-based integration (team) | Combine team/subagent modes by Phase |

**Decision sequence:**
1. First determine whether the work can be designed around an agent team — this is the default for two or more agents
2. Choose subagents only when team communication is structurally unnecessary because only results need to be delivered, and team overhead exceeds its benefits
3. If the characteristics of each Phase differ substantially, consider a hybrid approach — explicitly state each Phase's execution mode in the orchestrator

> For a detailed comparison table and a decision tree by pattern, see "Execution Modes" in `references/agent-design-patterns.md`.

#### 2-2. Select an Architecture Pattern

1. Decompose the work into specialized domains
2. Determine the agent team structure (see `references/agent-design-patterns.md` for architecture patterns)
   - **Pipeline**: Sequentially dependent tasks
   - **Fan-out/fan-in**: Parallel independent tasks
   - **Expert pool**: Selective invocation based on the situation
   - **Generate-validate**: Quality review after generation
   - **Supervisor**: A central agent manages state and dynamically distributes work
   - **Hierarchical delegation**: A higher-level agent recursively delegates to lower-level agents

#### 2-3. Agent Separation Criteria

Evaluate agents across four dimensions: specialization, parallelism, context, and reusability. For the detailed criteria table, see "Agent Separation Criteria" in `references/agent-design-patterns.md`. Duplication and reuse analysis involving existing agents is covered in Phase 3-0.

### Phase 3: Create Agent Definitions

#### 3-0. Review Existing Agents for Duplication

Before creating a new agent, check for duplication with existing agents in `project/.claude/agents/`. Repeatedly building a harness can easily result in agents with overlapping roles accumulating under different names.

> For duplication classification criteria and reuse design, see "Agent Reuse Design" in `references/agent-design-patterns.md`.

**Every agent must be defined in a `project/.claude/agents/{name}.md` file.** Do not place the role directly in the `Agent` tool's prompt without an agent definition file. Reasons:
- The agent definition must exist as a file to be reusable in the next session
- The team communication protocol must be explicit to ensure collaboration quality among agents
- The core value of the harness is the separation between agents (who) and skills (how)

Even when using built-in types (`general-purpose`, `Explore`, `Plan`), create an agent definition file. Specify the built-in type through the `Agent` tool's `subagent_type` parameter, and put the role, principles, and protocols in the agent definition file.

**Model configuration:** Use `model: "opus"` for every agent. When invoking the `Agent` tool, always specify the `model: "opus"` parameter. Harness quality directly depends on agent reasoning ability, and opus ensures the highest quality.

**Team reconfiguration:** Only one agent team can be active per session, but a team can be disbanded and a new team created between Phases. If each Phase requires a different combination of specialists, as in a pipeline pattern, save the previous team's artifacts to files, clean up the team, and create a new team.

Define each agent in `project/.claude/agents/{name}.md`. Required sections: core role, operating principles, input/output protocol, error handling, and collaboration. In agent team mode, add a `## Team Communication Protocol` section that specifies the message senders/recipients and the scope of work requests.

> For the definition template and complete real-world files, see "Agent Definition Structure" in `references/agent-design-patterns.md` and `references/team-examples.md`.

**Requirements when including a QA agent:**
- Use the `general-purpose` type for the QA agent (`Explore` is read-only and therefore cannot run validation scripts)
- The core of QA is not "existence checking" but **"cross-boundary comparison"** — read both the API response and the frontend hook and compare their shapes
- Run QA **incrementally immediately after each module is completed**, not once after everything is complete
- Detailed guide: See `references/qa-agent-guide.md`

### Phase 4: Create Skills

Create each agent's skills in `project/.claude/skills/{name}/SKILL.md`. For detailed authoring guidance, see `references/skill-writing-guide.md`.

#### 4-0. Review Existing Skills for Duplication

Before creating a new skill, check for duplication with existing skills in `project/.claude/skills/`. Repeatedly building a harness can easily result in skills with overlapping functionality accumulating under different names.

> For duplication classification criteria and generalization patterns, see "Skill Reuse Design" in `references/skill-writing-guide.md`.

#### 4-1. Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name and description required)
│   └── Markdown body
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for repetitive/deterministic tasks
    ├── references/ - Reference documents loaded conditionally
    └── assets/     - Files used in outputs (templates, images, etc.)
```

#### 4-2. Writing the Description — Encourage Aggressive Triggering

The description is the skill's only trigger mechanism. Because Claude tends to evaluate triggers conservatively, write the description **aggressively ("pushy")**.

**Bad example:** `"A skill for processing PDF documents"`
**Good example:** `"Performs all PDF operations, including reading PDF files, extracting text/tables, merging, splitting, rotating, watermarking, encryption, and OCR. Always use this skill whenever a .pdf file is mentioned or a PDF output is requested."`

The key is to describe both what the skill does and the specific situations that should trigger it, while distinguishing similar cases in which it should not trigger.

#### 4-3. Principles for Writing the Body

| Principle | Description |
|------|------|
| **Explain why** | Instead of coercive instructions such as "ALWAYS/NEVER," explain why the action is necessary. When an LLM understands the reason, it can make correct decisions even in edge cases. |
| **Keep it lean** | The context window is a shared resource. Aim to keep the SKILL.md body under 500 lines; remove content that does not justify its weight or move it to references/. |
| **Generalize** | Explain principles so the skill can handle diverse inputs rather than using narrow rules tailored only to specific examples. Do not overfit. |
| **Bundle repeated code** | If test runs reveal scripts that agents repeatedly write in common, bundle them in `scripts/` in advance. |
| **Use the imperative mood** | Write in an imperative/directive tone such as "Do X" or "Perform Y." |

#### 4-4. Progressive Disclosure

Skills manage context through a three-level loading system:

| Level | When loaded | Size target |
|------|----------|----------|
| **Metadata** (name + description) | Always present in context | ~100 words |
| **SKILL.md body** | When the skill is triggered | <500 lines |
| **references/** | Only when needed | Unlimited (scripts can run without being loaded) |

**Size management rules:**
- When SKILL.md approaches 500 lines, separate details into references/ and leave a pointer in the body explaining when to read the file
- Include a **table of contents (ToC)** at the top of reference files with 300 or more lines
- If domain/framework-specific variants exist, separate them by domain under references/ and load only the relevant files

```
cloud-deploy/
├── SKILL.md (workflow + selection guide)
└── references/
    ├── aws.md    ← Load only when AWS is selected
    ├── gcp.md
    └── azure.md
```

#### 4-5. Skill-Agent Connection Principles

- One agent ↔ one to N skills (1:1 or 1:many)
- A skill may also be shared by multiple agents
- A skill describes "how it is done," while an agent describes "who does it"

> For detailed authoring patterns, examples, and data schema standards, see `references/skill-writing-guide.md`.

### Phase 5: Integration and Orchestration

The orchestrator is a special form of skill that coordinates the entire team by connecting individual agents and skills into a single workflow. While the individual skills created in Phase 4 define "what and how each agent does," the orchestrator defines "who collaborates, when, and in what order." For a concrete template, see `references/orchestrator-template.md`.

**Modifying the orchestrator when extending an existing harness:** When extending an existing harness rather than creating a new one, modify the existing orchestrator instead of creating a new orchestrator. When adding an agent, incorporate the new agent into the team composition, task assignments, and data flow, and add trigger keywords related to the new agent to the description.

The orchestrator pattern varies according to the execution mode selected in Phase 2-1:

#### 5-0. Orchestrator Patterns by Mode

**Agent team pattern (default):**
The orchestrator creates a team with `TeamCreate` and assigns work with `TaskCreate`. Team members communicate directly through `SendMessage` and coordinate among themselves. The leader (orchestrator) monitors progress and synthesizes the results.

```
[Orchestrator/Leader]
    ├── TeamCreate(team_name, members)
    ├── TaskCreate(tasks with dependencies)
    ├── Team members coordinate among themselves (SendMessage)
    ├── Collect and synthesize results
    └── Clean up the team
```

**Subagent pattern (alternative):**
The orchestrator directly invokes subagents with the `Agent` tool. Use `run_in_background: true` for parallel execution; results are returned only to the main agent. Use this when team communication is unnecessary and reducing overhead is desirable.

```
[Orchestrator]
    ├── Agent(agent-1, run_in_background=true)
    ├── Agent(agent-2, run_in_background=true)
    ├── Wait for and collect results
    └── Create the integrated artifact
```

**Hybrid pattern:**
Combine different modes across Phases. Common combinations:
- **Parallel collection (subagents) → consensus-based integration (team)**: In Phase 2, use subagents to collect independent material in parallel → In Phase 3, create a team for discussion and consensus-based integration
- **Team generation (team) → validation (subagent)**: In Phase 2, the team generates a draft → In Phase 3, a single subagent independently validates it
- **Team reconfiguration between Phases**: Run `TeamDelete` followed by a new `TeamCreate` for each Phase, inserting subagent invocations between them

When selecting a hybrid approach, state the execution mode for each Phase at the top of the corresponding Phase section in the orchestrator (for example, `**Execution mode:** Agent team`).

#### 5-1. Data Transfer Protocol

Specify how data is transferred among agents within the orchestrator:

| Strategy | Method | Applicable mode | Suitable cases |
|------|------|----------|-----------|
| **Message-based** | Direct communication among team members through `SendMessage` | Team | Real-time coordination, feedback exchange, lightweight status updates |
| **Task-based** | Share work status through `TaskCreate`/`TaskUpdate` | Team | Progress tracking, dependency management, requesting the work itself |
| **File-based** | Write and read files at agreed paths | Team + subagents | Large data, structured artifacts, audit trails required |
| **Return-value-based** | Return message from the `Agent` tool | Subagents | The main agent directly collects subagent results |

**Recommended combination (team mode):** Task-based (coordination) + file-based (artifacts) + message-based (real-time communication)
**Recommended combination (subagent mode):** Return-value-based (result collection) + file-based (large artifacts)
**Hybrid:** Apply the appropriate combination for each Phase's execution mode

Rules for file-based transfer:
- Create a `_workspace/` folder under the working directory to store intermediate artifacts
- File naming convention: `{phase}_{agent}_{artifact}.{ext}` (for example, `01_analyst_requirements.md`)
- Output only final artifacts to the user-specified path; preserve intermediate files (`_workspace/`) for post-validation and audit trails

#### 5-2. Error Handling

Include an error-handling policy in the orchestrator. Core principle: retry once; if the retry also fails, continue without that result and explicitly report the omission. Do not delete conflicting data; include its source.

> For a strategy table by error type and implementation details, see "Error Handling" in `references/orchestrator-template.md`.

#### 5-3. Team Size Guidelines

| Work scale | Recommended team size | Tasks per team member |
|----------|------------|--------------|
| Small (5–10 tasks) | 2–3 members | 3–5 tasks |
| Medium (10–20 tasks) | 3–5 members | 4–6 tasks |
| Large (20+ tasks) | 5–7 members | 4–5 tasks |

> Coordination overhead increases with team size. Three focused team members are better than five unfocused team members.

#### 5-4. Register the Harness Pointer in CLAUDE.md

After configuring the harness, register a minimal pointer in the project's `CLAUDE.md`. Because CLAUDE.md is loaded in every new session, recording only the harness's existence and trigger rules is sufficient; the orchestrator skill handles the rest.

**CLAUDE.md template:**

````markdown
## Harness: {domain name}

**Goal:** {One-line core goal of the harness}

**Trigger:** For requests involving {domain}, use the `{orchestrator-skill-name}` skill. Simple questions may be answered directly.

**Change history:**
| Date | Change | Target | Reason |
|------|----------|------|------|
| {YYYY-MM-DD} | Initial configuration | All | - |
````

**Do not include the following in CLAUDE.md:** agent list, skill list, directory structure, or detailed execution rules. Reason: agent/skill lists are managed by the orchestrator skill and `.claude/agents/`, `.claude/skills/`, so duplicating them is unnecessary. The directory structure can be inspected directly in the file system. CLAUDE.md should contain only the **pointer (trigger rules) + change history**.

#### 5-5. Support Follow-Up Work

The orchestrator must handle follow-up work as well as initial execution. Ensure the following three items:

**1. Include follow-up keywords in the orchestrator description:**
Follow-up requests will not trigger if only initial-creation keywords are present. The description must include the following follow-up expressions:
- "run again," "rerun," "update," "modify," "improve"
- "redo only {subtask} of {domain}"
- "based on the previous results," "improve the results"

**2. Add a context-check step to orchestrator Phase 1:**
At the start of the workflow, check whether existing artifacts are present and determine the execution mode:
- `_workspace/` exists + the user requests a partial modification → **Partial rerun** (reinvoke only the relevant agent)
- `_workspace/` exists + the user provides new input → **New run** (move the existing _workspace to `_workspace_prev/`)
- `_workspace/` does not exist → **Initial run**

**3. Include reinvocation guidance in agent definitions:**
In each agent `.md` file, specify "behavior when previous artifacts exist":
- If a previous result file exists, read it and incorporate improvements
- If user feedback is provided, modify only the relevant part

> See the "Phase 0: Context Check" section of the orchestrator template: `references/orchestrator-template.md`

### Phase 6: Validation and Testing

Validate the generated harness. For detailed testing methodology, see `references/skill-testing-guide.md`.

#### 6-1. Structural Validation

- Verify that all agent files are in the correct locations
- Validate skill frontmatter (name, description)
- Check consistency of references among agents
- Verify that no commands were created

#### 6-2. Validation by Execution Mode

- **Agent team**: Verify communication paths among team members, task dependencies, and appropriate team size
- **Subagents**: Verify each agent's input/output connections, `run_in_background` settings, and return-value collection logic
- **Hybrid**: Verify that each Phase's execution mode is specified in the orchestrator and that data transfer remains intact at Phase boundaries (when switching from team → subagents, verify that the team's artifacts are connected to the subagents' inputs)

#### 6-3. Skill Execution Testing

Perform actual execution tests for each generated skill:

1. **Write test prompts** — Write 2–3 realistic test prompts for each skill. Use concrete, natural sentences that a real user would plausibly enter.

2. **Run with-skill vs without-skill comparisons** — When possible, run executions with and without the skill in parallel to verify the skill's added value. Spawn agents in pairs:
   - **With-skill**: Read the skill and perform the task
   - **Without-skill (baseline)**: Perform the same prompt without the skill

3. **Evaluate results** — Evaluate output quality qualitatively (user review) and quantitatively (assertion-based). When the artifact is objectively verifiable, such as file creation or data extraction, define assertions. For subjective outputs, such as writing style or design, rely on user feedback.

4. **Iterative improvement loop** — If testing reveals problems:
   - **Generalize** the feedback and modify the skill accordingly (do not make narrow changes tailored only to a specific example)
   - Retest after the modification
   - Repeat until the user is satisfied or no further meaningful improvement is possible

5. **Bundle recurring patterns** — If test runs reveal code that agents repeatedly write in common, such as generating the same helper script in every test, bundle that code in `scripts/` in advance.

#### 6-4. Trigger Validation

Validate whether each skill's description triggers correctly:

1. **Should-trigger queries** (8–10) — Diverse expressions that should trigger the skill (formal/casual, explicit/implicit)
2. **Should-NOT-trigger queries** (8–10) — "Near-miss" queries with similar keywords for which another tool/skill, rather than this skill, is appropriate

**Key principle for writing near-misses:** Obviously unrelated queries such as "Write a Fibonacci function" have no testing value. A query with an **ambiguous boundary**, such as "Extract the chart from this Excel file as a PNG" (xlsx skill vs image conversion), is a good test case.

Also check for trigger conflicts with existing skills at this stage.

#### 6-5. Dry-Run Testing

- Review whether the orchestrator skill's Phase sequence is logical
- Verify that the data transfer path contains no gaps (dead links)
- Verify that every agent's input matches the previous Phase's output
- Verify that fallback paths for each error scenario are executable

#### 6-6. Write Test Scenarios

- Add a `## Test Scenarios` section to the orchestrator skill
- Describe at least one normal flow and one error flow

### Phase 7: Harness Evolution

A harness is not a static artifact that is built once and then abandoned. It is a system that continuously evolves based on user feedback.

#### 7-1. Collect Feedback After Execution

After every harness execution, ask the user for feedback:
- "Is there anything in the results that could be improved?"
- "Would you like to change anything about the agent team composition or workflow?"

If there is no feedback, move on. Do not pressure the user, but always provide the opportunity.

#### 7-2. Feedback Incorporation Paths

The modification target depends on the feedback type:

| Feedback type | Modification target | Example |
|-----------|----------|------|
| Output quality | The relevant agent's skill | "The analysis is too superficial" → Add depth criteria to the skill |
| Agent role | Agent definition `.md` | "A security review is also needed" → Add a new agent |
| Workflow order | Orchestrator skill | "Validation should happen first" → Change the Phase order |
| Team composition | Orchestrator + agents | "These two could probably be combined" → Merge the agents |
| Missing trigger | Skill description | "It does not work when phrased this way" → Expand the description |

#### 7-3. Change History

Record every change in the **Change history** table in CLAUDE.md (the same table as the "Change history" section in the Phase 5-4 template):

```markdown
**Change history:**
| Date | Change | Target | Reason |
|------|----------|------|------|
| 2026-04-05 | Initial configuration | All | - |
| 2026-04-07 | Added QA agent | agents/qa.md | Feedback indicated insufficient artifact quality validation |
| 2026-04-10 | Added tone guide | skills/content-creator | Feedback: "It is too formal" |
```

Use this history to track how the harness has evolved and prevent regression.

#### 7-4. Evolution Triggers

Propose harness evolution not only when the user explicitly says "modify the harness," but also in the following situations:
- The same type of feedback is repeated two or more times
- A pattern of repeated agent failures is discovered
- The user is observed bypassing the orchestrator and performing work manually

#### 7-5. Operations/Maintenance Workflow

Systematically inspect, modify, and synchronize an existing harness. Follow this workflow when entering the "operations/maintenance" branch from Phase 0.

**Step 1: Current-state audit**
- Compare the `.claude/agents/` file list against the orchestrator skill's agent composition → Generate a list of inconsistencies
- Compare the `.claude/skills/` directory list against the orchestrator skill's skill composition → Generate a list of inconsistencies
- Report the audit results to the user

**Step 2: Incremental additions/modifications**
- Add/modify/delete agents and add/modify/delete skills according to the user's request
- Make one change at a time and immediately run Step 3 (synchronization) after each change

**Step 3: Update the CLAUDE.md change history**
- Record the date, change, target, and reason in the change history table

**Step 4: Validate changes**
- Validate the structure of modified agents/skills according to Phase 6-1
- If the modification scope affects triggers, perform trigger validation according to Phase 6-4
- For large-scale changes, such as architecture changes or adding/deleting three or more agents, also perform Phase 6-3 (execution testing) and 6-5 (dry run)
- Perform a final consistency check between CLAUDE.md and the actual files

## Artifact Checklist

Verify after generation is complete:

- [ ] `project/.claude/agents/` — **Agent definition files must be created** (a file is required even for built-in types)
- [ ] `project/.claude/skills/` — Skill files (SKILL.md + references/)
- [ ] One orchestrator skill (including data flow + error handling + test scenarios)
- [ ] Execution mode specified (select agent team / subagents / hybrid; for hybrid, specify the mode for each Phase)
- [ ] `model: "opus"` parameter specified for every Agent invocation
- [ ] Existing agents reviewed for duplication before creating new agents (Phase 3-0)
- [ ] Existing skills reviewed for duplication before creating new skills (Phase 4-0)
- [ ] `.claude/commands/` — Nothing created
- [ ] No conflicts with existing agents/skills
- [ ] Skill descriptions are written aggressively ("pushy") — **including follow-up work keywords**
- [ ] SKILL.md body is within 500 lines; if exceeded, content is separated into references/
- [ ] Execution validation completed with 2–3 test prompts
- [ ] Trigger validation (should-trigger + should-NOT-trigger) completed
- [ ] **Harness pointer registered in CLAUDE.md** (trigger rules + change history)
- [ ] **Agent/skill additions/deletions/modifications recorded in the CLAUDE.md change history**
- [ ] **Context-check step included in orchestrator Phase 1** (determine initial/follow-up/partial rerun)

## References

- Harness patterns: `references/agent-design-patterns.md`
- Existing harness examples (including complete real-world files): `references/team-examples.md`
- Orchestrator template: `references/orchestrator-template.md`
- **Skill authoring guide**: `references/skill-writing-guide.md` — Authoring patterns, examples, and data schema standards
- **Skill testing guide**: `references/skill-testing-guide.md` — Testing, evaluation, and iterative improvement methodology
- **QA agent guide**: `references/qa-agent-guide.md` — Consult when including a QA agent in a build harness. Includes integration consistency validation methodology, boundary bug patterns, and a QA agent definition template. Based on seven bug cases discovered in real projects.
