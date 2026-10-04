---
name: create-subagent
description: Generates single-purpose Claude Code sub-agents for use via the Task tool. Use when creating dedicated sub-agents, scaffolding agent definitions, or generating agents with diagnostics and permissions setup.
user-invocable: true
argument-hint: "<description-or-name> [--doc <requirements-path>]"
skills:
  - subagent-prompting
  - anthropic-validator
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Skill
  - Task
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Create Sub-Agent

Generates a complete single-purpose Claude Code sub-agent from a description or requirements document. Conducts an adaptive interview to understand the agent's identity and mission, determines tool permissions and supporting configuration, spawns a Sonnet sub-agent to generate the agent file, validates with anthropic-validator, and presents the scaffold with architectural decisions.

Sub-agents are invoked via `Task(subagent_type=...)` and run in a forked context. They perform a single focused task and return results. They **cannot** spawn other sub-agents — pipeline orchestration belongs in skills, not agents.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Sub-agent creation | "Create a sub-agent for X", "Make an agent for X" |
| Agent scaffolding | "Scaffold an agent", "Set up a new agent" |
| Agent generation | "Generate an agent that does X" |
| Dedicated worker | "Create a dedicated agent for this sub-agent role" |
| Task tool agent | "I need an agent I can invoke via Task tool" |

**DO NOT use for:**
- Creating pipeline orchestration (use `create-skill` — it generates the orchestrating skill + sub-agent files)
- Creating Agent Teams leads (use `create-skill` with the research template)
- Creating skills (use `create-skill`)
- Editing existing agents (edit directly)
- Debugging agent issues (use `issue-debugging`)
- Validating existing agents (use `anthropic-validator`)

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Decision framework** | `references/decision-framework.md` | **REQUIRED** | Load at Stage 0 for interview + classification |
| **Agent conventions** | `references/agent-conventions.md` | **REQUIRED** | Include in Stage 2 generator prompt |
| **Content guidance** | `references/content-guidance.md` | **REQUIRED** | Include in Stage 2 generator prompt |
| **Agent template** | `references/template-single-agent.md` | **REQUIRED** | Load at Stage 2 |
| **Diagnostic template** | `templates/diagnostic-output.yaml` | **REQUIRED** | Use at Stage 6 |
| **Subagent prompting** | `subagent-prompting` skill | **REQUIRED** | Load at Stage 0 for 4-part prompt template |

**Fallback behavior:**
- If content-guidance is missing: Proceed without it, note in diagnostics (output quality will be lower)

---

## Usage

```
/create-subagent <description-or-name>
/create-subagent --doc <requirements-document>
```

**Arguments:**
- `<description-or-name>` — Free-text description of the desired agent, or an agent name to start from
- `--doc <path>` — Path to a requirements document. Extracts interview answers from it instead of asking fresh.

**Examples:**
- `/create-subagent a code security reviewer that checks for OWASP vulnerabilities` — Start from description
- `/create-subagent --doc plans/task-briefs/P4.4-implementer.md` — Start from requirements doc
- `/create-subagent market-analyst` — Start from a name

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping.**

This skill uses a 6-stage pipeline. You are the orchestrator. Follow every item in order. Do NOT return to the user until all applicable items are checked.

- [ ] **Stage 0 — Pre-Flight**: Arguments parsed (description, name, or --doc)
- [ ] **Stage 0 — Pre-Flight**: Decision framework, agent conventions, and content guidance loaded
- [ ] **Stage 0 — Pre-Flight**: Adaptive interview conducted (1-2 rounds via AskUserQuestion)
- [ ] **Stage 0 — Pre-Flight**: Routing check completed (pipeline/teams → redirect to create-skill and STOP, OR single → proceed)
- [ ] **Stage 1 — Classify**: Two decisions made (tool permissions, supporting configuration)
- [ ] **Stage 1 — Classify**: Classification presented to user and confirmed via AskUserQuestion
- [ ] **Stage 2 — Generate**: Sonnet sub-agent spawned via Task tool (you do NOT generate the file yourself)
- [ ] **Stage 2 — Generate**: Generated agent file verified to exist in working directory
- [ ] **Stage 2 — Generate**: Agent uses system-prompt register (identity statement, not task steps)
- [ ] **Stage 3 — Validate**: `/anthropic-validator` invoked via Skill tool (manual review is NOT a substitute)
- [ ] **Stage 3 — Validate**: Validator output read and findings counted
- [ ] **Stage 3 — Validate**: Manual checks completed (single-line description, system-prompt register, permissions section)
- [ ] **Stage 4 — Refine**: If validation found critical/high issues, Sonnet sub-agent spawned to fix (max 2 retries)
- [ ] **Stage 5 — Deploy**: Agent file deployed from working directory to `.claude/agents/`
- [ ] **Stage 5 — Deploy**: Working directory cleaned up
- [ ] **Stage 5 — Present**: Post-generation summary presented with architectural decisions
- [ ] **Stage 5 — Present**: Permissions setup steps communicated
- [ ] **Stage 5 — Present**: Next steps communicated (this is a scaffold, not production-ready output)
- [ ] **Stage 6 — Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

---

## Pipeline

```fsharp
// create-subagent pipeline
PreFlight(args)                              // Stage 0: Orchestrator — parse input, interview, routing check
|> Classify(interview_answers)               // Stage 1: Orchestrator — two independent decisions
|> Generate(classification, template, conventions) // Stage 2: Sonnet sub-agent — produce agent file
|> Validate(generated_output)                // Stage 3: Orchestrator — run anthropic-validator
|> Refine(validator_findings)                // Stage 4: Sonnet sub-agent (conditional, max 2 retries)
|> DeployAndPresent(working_dir, target_dir)  // Stage 5: Orchestrator — deploy to target + post-generation summary
|> Diagnostics()                             // Stage 6: Orchestrator — write YAML
```

---

## Stage Definitions

### Stage 0: Pre-Flight (Orchestrator)

```
Stage 0: Pre-Flight
├── Parse arguments (description, name, or --doc path)
├── Load references/decision-framework.md
├── Load references/agent-conventions.md
├── Load references/content-guidance.md
├── Load subagent-prompting skill
├── If --doc provided:
│   ├── Read the requirements document
│   ├── Extract answers to Q1-Q5 from the document
│   └── Present extracted answers to user for confirmation via AskUserQuestion
├── If no --doc:
│   └── AskUserQuestion: Present all 5 core questions from decision-framework.md
│       ├── Q1: What is this agent's identity and mission? (2-3 invocation examples)
│       ├── Q2: What tools does it need access to?
│       ├── Q3: Single focused task, or multiple stages/operations?
│       ├── Q4: Does it need structured diagnostic output?
│       └── Q5: Restricted permissions or full access?
├── If complexity detected in answers (Q3 = "multiple stages"):
│   └── AskUserQuestion: Follow-up questions per decision-framework.md
│       ├── Q6: Do stages depend on each other's output?
│       ├── Q7: Do workers need direct communication?
│       └── Q8-Q10: Additional context-specific follow-ups
├── ROUTING CHECK (after all interview answers received):
│   ├── If Q3 = "multiple stages" AND (Q6 = "dependent" OR Q7 = "direct comms"):
│   │   └── STOP PIPELINE. Present redirect message to user:
│   │       "This use case requires a pipeline skill that orchestrates multiple sub-agents.
│   │        Sub-agents are single-purpose — they can't spawn other sub-agents.
│   │
│   │        Use /create-skill instead. It will generate:
│   │        - An orchestrating skill (SKILL.md) with pipeline stages
│   │        - Dedicated sub-agent files (.claude/agents/*.md) for each stage
│   │
│   │        The generated sub-agents will have deterministic behavior locked into their
│   │        system prompts, and the orchestrating skill handles sequencing, error handling,
│   │        and synthesis."
│   │       Do NOT proceed to Stage 1. Return to user.
│   └── Otherwise: Continue to Stage 1
├── Determine agent name (from input or derived from description)
│   └── Target: .claude/agents/{agent-name}.md
├── Set working directory: tmp/create-subagent/{agent-name}/
│   └── All generation and refinement happens here to avoid .claude/ edit approval storms
│       Files are deployed to the target directory only after validation passes (Stage 5)
└── Token budget check (warn if >30% consumed)
```

**Interview behavior**: Maximum 2 AskUserQuestion rounds. Present Q1-Q5 together in round 1. Follow-ups (if needed) in round 2. Do NOT ask questions one at a time.

### Stage 1: Classify (Orchestrator)

Apply the two-decision classification from `references/decision-framework.md`:

```
Stage 1: Classify
├── Decision A: Tool Permissions
│   ├── Full access → no tools: list in frontmatter (inherits all)
│   ├── Restricted → tools: [specific list] in frontmatter
│   ├── If Write/Edit needed → include quality gate guidance in protocol
│   └── If Bash needed → include allowed/forbidden command lists in protocol
├── Decision B: Supporting Configuration
│   ├── Always: Permissions Setup section
│   ├── If diagnostics needed (Q4 = yes): diagnostic output section + schema
│   └── If diagnostics needed: subagent-output-templating in skills: dependency
└── Present classification to user via AskUserQuestion:
    ├── "Tool permissions: {full/restricted: [list]} — {reason}"
    ├── "Configuration: {list} — {reason}"
    └── "Proceed with generation? [Yes / Adjust]"
```

**MANDATORY**: Wait for user confirmation before proceeding to Stage 2. If user selects "Adjust", re-classify with their feedback.

### Stage 2: Generate (Sonnet sub-agent)

```
Stage 2: Generate
├── Read references/template-single-agent.md
├── Construct prompt using 4-part template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT):
│   ├── GOAL: Generate a complete, structurally correct single-purpose sub-agent
│   │   definition. The agent must use system-prompt register and include all
│   │   required sections (Pre-Flight, Mission, Protocol, Output, Permissions).
│   ├── CONSTRAINTS:
│   │   ├── Write in SYSTEM-PROMPT REGISTER — WHO the agent IS, not WHAT to do
│   │   ├── Open with identity statement: "You are a..."
│   │   ├── Use present tense for behavioral descriptions
│   │   ├── Description MUST be a single line (multi-line breaks discovery)
│   │   ├── Description MUST use role-based trigger framing
│   │   ├── Include Pre-Flight Gate with MUST/MUST NOT (binding language)
│   │   ├── Include DO/DO NOT mission section
│   │   ├── Include Tool Usage Constraints for every tool in frontmatter
│   │   ├── Include Permissions Setup section (tool permissions unsolved per #10093)
│   │   ├── Do NOT add unnecessary files (no README, CHANGELOG, LICENSE)
│   │   ├── Do NOT use emojis in generated content
│   │   └── Keep agent under 250 lines
│   ├── CONTEXT:
│   │   ├── Classification from Stage 1 (both decisions)
│   │   ├── User's interview answers (identity, mission, tools from Q1-Q5)
│   │   ├── Template: references/template-single-agent.md
│   │   ├── Agent conventions: references/agent-conventions.md
│   │   ├── Content guidance: references/content-guidance.md
│   │   ├── Instruction: "Read 1-2 existing agents from the codebase for structural
│   │   │   reference (use Glob to find .claude/agents/*.md)"
│   │   ├── Target output path: .claude/agents/{agent-name}.md (final deployment location)
│   │   └── Working directory: tmp/create-subagent/{agent-name}/
│   └── OUTPUT:
│       ├── Write agent file to {working-directory}/{agent-name}.md
│       └── Return summary: file path with line count
├── Spawn: Task(description="Generate agent file", subagent_type="general-purpose",
│          model="sonnet", prompt=...)
├── Read generator output (file path + summary)
└── Verify file was created (Read {working-directory}/{agent-name}.md)
```

### Stage 3: Validate (Orchestrator)

```
Stage 3: Validate
├── FIRST: Invoke /anthropic-validator (this is the PRIMARY validation — NOT optional)
│   ├── Use the Skill tool: Skill(skill="anthropic-validator", args="{working-directory}/{agent-name}.md")
│   ├── Do NOT substitute manual review for this step
│   └── Do NOT proceed past this node until the Skill tool has been invoked
├── Read validator output
├── Check for critical/high findings:
│   ├── 0 critical AND 0 high → proceed to Stage 5 (skip Stage 4)
│   └── Any critical or high → proceed to Stage 4 (refine)
├── THEN: Manual checks (these supplement the validator, they do NOT replace it)
│   ├── Check description is single-line (read agent file, verify no multiline description)
│   ├── Check system-prompt register (body opens with identity, not task steps)
│   └── Check Permissions Setup section exists
└── Stage 3 exit gate:
    ├── [ ] /anthropic-validator was invoked via the Skill tool (not manual review)
    ├── [ ] Validator output was read and findings counted
    └── If either is unchecked, Stage 3 is NOT complete — go back and invoke the validator
```

### Stage 4: Refine (Sonnet sub-agent, conditional, max 2 retries)

This stage only runs if Stage 3 found critical or high issues.

```
Stage 4: Refine (attempt {N} of 2)
├── Construct prompt using 4-part template:
│   ├── GOAL: Fix all critical and high findings from anthropic-validator
│   ├── CONSTRAINTS:
│   │   ├── Only fix the specific issues identified — do not restructure
│   │   ├── Preserve the existing agent content and identity
│   │   ├── Description must remain single-line
│   │   └── Must remain in system-prompt register
│   ├── CONTEXT:
│   │   ├── Validator findings (critical and high items with descriptions)
│   │   ├── Current generated file (read from {working-directory}/{agent-name}.md)
│   │   └── Agent conventions: references/agent-conventions.md
│   └── OUTPUT: Edit file at {working-directory}/{agent-name}.md to fix findings
├── Spawn: Task(description="Fix validator findings", subagent_type="general-purpose",
│          model="sonnet", prompt=...)
├── Re-run Stage 3 (validate)
├── If still failing after 2 retries:
│   └── Proceed to Stage 5 with caveats noted
└── Token budget check
```

### Stage 5: Deploy & Present (Orchestrator)

```
Stage 5: Deploy & Present
├── Deploy: Move {working-directory}/{agent-name}.md to .claude/agents/{agent-name}.md
│   ├── This is the ONLY point where the file is written to .claude/
│   └── Clean up: Remove {working-directory}/ after successful copy
├── Read generated agent file from .claude/agents/{agent-name}.md for summary
├── Present to user:
│   ├── "Generated agent at: .claude/agents/{agent-name}.md"
│   ├── "Lines: {count}"
│   ├── "Architectural decisions:"
│   │   ├── "Tool permissions: {full/restricted: [list]} — {reason}"
│   │   └── "Configuration: {list} — {reason}"
│   ├── "Validation: {pass/fail with details}"
│   ├── If caveats: "Unresolved issues: {list}"
│   ├── "Permissions to configure:"
│   │   └── {List tool permissions that must be added to settings.json}
│   └── "Next steps:"
│       ├── "1. Review and customize the identity and expertise sections"
│       ├── "2. Adjust tool permissions in .claude/settings.json"
│       ├── "3. Test by invoking via Task tool: Task(subagent_type=\"{name}\", prompt=\"...\")"
│       ├── "4. Add project-specific protocol steps as needed"
│       └── "5. Configure Stop hook if diagnostic output is needed"
└── Note: This is a scaffold, not production-ready output (generate-and-customize contract)
```

### Stage 6: Diagnostics (REQUIRED)

**MANDATORY**: Write diagnostic output after every invocation. This cannot be skipped.

```
Stage 6: Diagnostics
├── Write to: $PROJECT_DIR/logs/diagnostics/create-subagent-{YYYYMMDD-HHMMSS}.yaml
│   └── Use templates/diagnostic-output.yaml schema
└── Include:
    ├── Input: description/name/doc path
    ├── Interview: questions asked, rounds completed
    ├── Routing: redirected (true/false), reason if redirected
    ├── Classification: both decisions
    ├── Generation: file created, line count, model used
    ├── Validation: pass/fail, findings count, retry count
    └── Outcome: success/partial/failure/redirected
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Generator sub-agent returns empty output | Re-spawn once with reinforced instructions. If still empty, STOP: "Generation failed. Please try with a more detailed description." |
| anthropic-validator finds critical issues | Stage 4 retry (max 2). After 2 retries, present with caveats. |
| anthropic-validator unavailable | Skip validation, note in diagnostics, warn user: "Validation skipped — run /anthropic-validator manually." |
| Interview answers are ambiguous | Ask 1-2 follow-up questions (max 2 AskUserQuestion rounds total). |
| Pipeline/teams detected in interview | STOP pipeline. Redirect to `/create-skill` with guidance message. Write diagnostic with outcome: redirected. |
| Token budget exceeded | Stop at current stage, present partial output with explanation. |
| Agent file already exists at target path | AskUserQuestion: "Agent {name} already exists at .claude/agents/{name}.md. Overwrite / Choose different name / Cancel?" |
| Working directory already exists | Silently remove and recreate tmp/create-subagent/{agent-name}/ (working dirs are ephemeral) |
| User rejects classification | Re-classify with user's feedback. Max 2 classification rounds. |
| Generated agent uses task-instruction register | Stage 4 refine with specific instruction to rewrite in system-prompt register. |

---

## Token Budget Management

| Checkpoint | Threshold | Action |
|------------|-----------|--------|
| After Pre-Flight | >30% consumed | Warn: "Remaining budget may limit validation and refinement." |
| After Generate | >55% consumed | Warn: "Approaching budget. Validation + refinement may be limited." |
| After Validate | >65% consumed | Skip refinement if needed, present as-is with caveats. |

