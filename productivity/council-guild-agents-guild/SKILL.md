---
name: council
description: "Convenes multiple agents to debate an important decision"
user-invocable: true
workflow:
  version: 1
  steps:
    - id: identify-type
      role: system
      intent: "Analyze the question and determine council type: architecture, feature-scope, or tech-debt."
      requires: [user-question]
      produces: [council-type, participant-roles]
      gate: true
    - id: agent-1
      role: dynamic
      intent: "Analyze the question from specialized perspective. State position with concrete arguments. Spawn via Agent tool IN PARALLEL with agent-2 and agent-3."
      requires: [user-question, council-type]
      produces: [perspective-1]
      model-tier: reasoning
    - id: agent-2
      role: dynamic
      intent: "Analyze the question from specialized perspective. State position with concrete arguments."
      requires: [user-question, council-type]
      produces: [perspective-2]
      model-tier: reasoning
    - id: agent-3
      role: dynamic
      intent: "Analyze the question from specialized perspective. State position with concrete arguments."
      requires: [user-question, council-type]
      produces: [perspective-3]
      model-tier: reasoning
    - id: synthesize
      role: system
      intent: "Synthesize debate: points of agreement, disagreement, risks. Present options to user."
      requires: [perspective-1, perspective-2, perspective-3]
      produces: [synthesis, options]
      gate: true
    - id: write-spec
      role: system
      intent: "After user decides, write spec document to docs/specs/."
      requires: [synthesis, user-decision]
      produces: [spec-document]
      gate: true
---

# Council

Convenes a council of specialized agents to debate an important decision. Each agent contributes their independent perspective and the result is a synthesis of the debate.

Agents are invoked IN PARALLEL using the `Task` tool to obtain independent perspectives without bias.

## When to use

- Before making an important architectural decision
- To evaluate the scope of a feature with multiple perspectives
- To decide whether to address technical debt and how to prioritize it
- When you need multiple viewpoints on a complex problem

## Usage

`/council [question or decision to debate]`

Optionally you can specify the type: `/council architecture [question]`

## Council Types

### 1. Council Architecture

**Participants:** Tech Lead + Advisor + Developer
**When it applies:** Decisions about architecture, patterns, large refactors, new technologies

Invokes all 3 agents IN PARALLEL using Task tool:

- Task 1: Reads `.claude/agents/tech-lead.md` — architecture and technical coherence perspective
- Task 2: Reads `.claude/agents/advisor.md` — feasibility and business risk perspective
- Task 3: Reads `.claude/agents/developer.md` — implementability and pragmatism perspective

### 2. Council Feature-Scope

**Participants:** Advisor + Developer + Tech Lead
**When it applies:** Defining feature scope, prioritizing functionality, evaluating product proposals

Invokes all 3 agents IN PARALLEL using Task tool:

- Task 1: Reads `.claude/agents/advisor.md` — domain and strategic vision perspective
- Task 2: Reads `.claude/agents/developer.md` — implementability and pragmatism perspective
- Task 3: Reads `.claude/agents/tech-lead.md` — technical feasibility and effort perspective

### 3. Council Tech-Debt

**Participants:** Tech Lead + Developer + Code Reviewer
**When it applies:** Deciding whether to address technical debt, planning refactors, evaluating codebase quality

Invokes all 3 agents IN PARALLEL using Task tool:

- Task 1: Reads `.claude/agents/tech-lead.md` — architectural impact perspective
- Task 2: Reads `.claude/agents/developer.md` — implementation cost perspective
- Task 3: Reads `.claude/agents/code-reviewer.md` — quality and risk perspective

## Process

### Step 1 — Identify council type

Analyze the user's question and determine which council type applies:

- If it mentions architecture, patterns, technologies -> **architecture**
- If it mentions features, priorities, scope, users -> **feature-scope**
- If it mentions technical debt, refactor, quality, maintainability -> **tech-debt**
- If unclear, ask the user

### Step 2 — Convene agents

**Workspace detection:** Before invoking agents, check if the project is inside a workspace:

1. Look for a `guild-workspace.json` file by searching upward from the project root
2. If found, load the workspace config and identify which member this project is
3. Read CLAUDE.md and PROJECT.md from each sibling member repo
4. Build a workspace context block with:
   - Workspace name
   - Each sibling's stack, structure summary, and current task
   - Absolute paths so the agent can read any sibling file for deeper analysis

Invoke the 3 corresponding agents IN PARALLEL using Task tool with `model: "opus"` (all council agents use reasoning tier). Each agent:

1. Reads their `.claude/agents/[name].md` file to assume their role
2. Reads `CLAUDE.md` for project context
3. **If in a workspace:** receives the workspace context block and considers cross-repo impact as part of their analysis. They may read files from sibling repos using the provided paths.
4. Analyzes the question from their specialized perspective
5. States their position with concrete arguments

### Step 3 — Present debate

Present the perspectives of all 3 agents in a structured format:

```text
## Council: [type]
Question: [the user's question]

### [Agent 1] — [position]
[main arguments]

### [Agent 2] — [position]
[main arguments]

### [Agent 3] — [position]
[main arguments]

### Synthesis
- Points of agreement: [...]
- Points of disagreement: [...]
- Identified risks: [...]
```

### Step 4 — Request decision

Present clear options to the user based on the debate:

- Option A: [summary of one position]
- Option B: [summary of another position]
- Option C: [compromise or alternative]

Ask the user to decide.

### Step 5 — Write Spec Document

After the user makes their decision in Step 4, offer to write a spec document to `docs/specs/`.

1. **Suggest filename**: Derive a kebab-case filename (3-5 words) from the council question. Present the suggested filename to the user for confirmation. Example: `docs/specs/graphql-migration-strategy.md`
2. **Create directory**: Create `docs/specs/` if it does not already exist.
3. **Read the spec template**: Read `src/templates/specs/SPEC_TEMPLATE.md` (or the project's local copy) to use as the structural guide.
4. **Assemble spec content**: Map the council debate to the template format:
   - **Title**: From the council question
   - **spec-id**: Matches the filename (without `.md`)
   - **status**: Always `draft`
   - **date**: Current date in `YYYY-MM-DD` format
   - **council-type**: From Step 1 (architecture, feature-scope, or tech-debt)
   - **Context**: From the council question and background provided by the user
   - **Decision**: The user's chosen option from Step 4
   - **Constraints**: Extracted from agent arguments during the debate
   - **Acceptance Criteria**: Derived from the decision, as checkboxes (`- [ ]`)
   - **Technical Approach**: Synthesis of implementation details from agents
   - **Trade-offs Considered**: Options A/B/C from Step 4 with their pros and cons
   - **Unresolved Questions**: Open risks and unknowns identified during debate
   - **Test Strategy**: How to verify the implementation meets the acceptance criteria
   - **Council Perspectives**: Summary of each agent's independent position
   - **Points of Dissent**: Where agents disagreed and how it was resolved, or "None — consensus reached"
5. **Write the file**: Use the Write tool to create the spec at `docs/specs/<filename>.md`.
6. **Report**: Tell the user the file path of the written spec.
7. **Trivial decisions**: For trivial or low-impact decisions, skip the full spec document and just summarize the decision in the chat.

## Subagent Configuration

When spawning council agents via the Task tool, always use `subagent_type: "general-purpose"`. Guild agent role names (advisor, developer, tech-lead, etc.) are NOT valid Claude Code subagent_types.

Example:

```text
Task tool with:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: "Read .claude/agents/tech-lead.md and assume that role. Then: [debate question]

[If in workspace, append:]
## Workspace context
[workspace context block from Step 2]"
```

The `model` parameter is resolved from the step's `model-tier`: all council agents use reasoning→`"opus"`.

## Example Session

```text
User: /council Should we migrate from REST to GraphQL?

Council: Architecture

Tech Lead (opus) — Recommends GraphQL for complex queries, keep REST for simple CRUD.
Advisor (opus) — Risk is high mid-project. Suggests incremental adoption.
Developer (opus) — Prefers REST simplicity. GraphQL adds tooling overhead.

Consensus: Incremental adoption. New endpoints in GraphQL, existing stay REST.
```

## Notes

- Agents must be invoked in parallel to prevent one from influencing another
- Each perspective must be independent — not "responding" to another agent
- The synthesis is done by you (the skill), not by the agents
- If all 3 agents agree, indicate consensus and suggest taking action
- After the user decides, always offer to write the spec to `docs/specs/`
- The spec document is the primary output of `/council` — it captures the debate, decision, and rationale
- If the user declines the spec, summarize the decision in chat
- In v1.x, `parallel` execution is best-effort — the orchestrator may run parallel steps sequentially if concurrent agent execution is unavailable
