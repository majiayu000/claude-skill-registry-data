---
name: bulwark-brainstorm
description: "Role-based brainstorming with dual modes: --scoped (sequential Task tool, 5 roles) and --exploratory (Agent Teams peer debate, 4 roles). Use for feasibility assessment and idea validation."
user-invocable: true
argument-hint: "<topic, filepath, or directory> [--research <synthesis-file>] [--scoped | --exploratory]"
skills:
  - subagent-prompting
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Read
  - Skill
  - Task
  - Write
version: 1.0.1
author: "Ashay Kubal @ Qball Inc."
---

# Bulwark Brainstorm

Role-based brainstorming on a given topic with two execution modes:

- **`--scoped`** (default): Sequential Task tool pipeline — Project SME first, 3 role agents in parallel, Critical Analyst last. Best when the problem statement is well understood and you need focused implementation brainstorming.
- **`--exploratory`**: Agent Teams peer debate — Project SME first, then 3 AT teammates (Product & Delivery Lead, Architect, Critical Analyst) debating collaboratively. Best when validating whether an idea has merit and the problem framing is uncertain.

Both modes synthesize into a single brainstorm document with actionable recommendations.

**Invocation arguments:** $ARGUMENTS

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Implementation evaluation | "Should we build X?", "Evaluate this approach" |
| Feasibility assessment | "Is this feasible?", "How would we implement X?" |
| Architecture brainstorm | "Design the approach for X", "How should X fit into our system?" |
| Post-research planning | "We've researched X, now plan the implementation" |
| Role-based analysis | "Get PM/architect/dev perspectives on X" |

**DO NOT use for:**
- Initial topic research (use `bulwark-research` first)
- Quick technical questions (ask directly)
- Code review (use `code-review`)
- Debugging (use `issue-debugging`)

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Role definitions** | `references/role-*.md` | **REQUIRED** | Load each before spawning its agent |
| **Role output template** | `templates/role-output.md` | **REQUIRED** | Include in PM, Architect, Dev Lead prompts |
| **Critic output template** | `templates/critic-output.md` | **REQUIRED** | Include in Critical Analyst prompt |
| **Synthesis template** | `templates/synthesis-output.md` | **REQUIRED** | Use when writing synthesis |
| **Subagent prompting** | `subagent-prompting` skill | **REQUIRED** | Load at Stage 1 for 4-part prompt template |
| **AT teammate prompts** | `references/at-teammate-prompts.md` | **REQUIRED** (--exploratory only) | Load at Stage 3B for AT prompt structure |
| **Research synthesis** | `--research <file>` | OPTIONAL | If provided, include in all agent prompts |

**Fallback behavior:**
- If a role reference file is missing: Note in diagnostic log, skip that role, continue with remaining agents
- If output template is missing: Use the schema from this SKILL.md directly
- If research synthesis not provided: Agents work from problem statement alone (warn user that quality may be lower)

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping.**

This skill uses a multi-stage pipeline. You are the orchestrator. Follow every item in order. Do NOT return to the user until all applicable items are checked.

- [ ] **Stage 1 — Pre-Flight**: Topic parsed (from argument, --doc, or AskUserQuestion)
- [ ] **Stage 1 — Pre-Flight**: subagent-prompting skill loaded
- [ ] **Stage 1 — Pre-Flight**: If topic is ambiguous or under-specified, AskUserQuestion interview conducted (2-3 questions per round)
- [ ] **Stage 1 — Pre-Flight**: If --research not provided, user warned via displayed message AND asked to confirm proceeding
- [ ] **Stage 1 — Mode Detection**: `$CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var checked — you MUST check this, no exceptions
- [ ] **Stage 1 — Mode Detection**: If `--exploratory` requested AND env var NOT SET: notify user ("Agent Teams requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Using --scoped mode.") and fall back to `--scoped`
- [ ] **Stage 1 — Mode Detection**: If env var IS SET AND user requests `--exploratory`: AT Confirmation Flow executed (token cost warning + model class choice)
- [ ] **Stage 1 — Mode Detection**: If no mode flag provided: default to `--scoped` (do NOT auto-select AT even if env var is set)
- [ ] **Stage 2 — Project SME**: SME spawned via Task tool (general-purpose, Opus) and output read
- [ ] **Stage 3A (--scoped)**: PM + Architect + Dev Lead spawned in parallel (3 Task tool calls), all outputs read
- [ ] **Stage 3B (--exploratory)**: 3 AT teammates spawned in delegate mode with correct model class, all outputs read
- [ ] **Stage 4 (--scoped only)**: Critical Analyst spawned with ALL prior outputs, output read
- [ ] **Stage 5 — Synthesis**: ALL role outputs read, synthesis written using template, AskUserQuestion for post-synthesis review
- [ ] **Stage 5 — Evaluation Gate**: Critical Evaluation Gate applied to all user responses
- [ ] **Stage 6 — Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

---

## Usage

```
/bulwark-brainstorm <topic-or-prompt> [--research <synthesis-file>] [--scoped | --exploratory]
/bulwark-brainstorm --doc <path-to-document> [--research <synthesis-file>] [--scoped | --exploratory]
```

**Arguments:**
- `<topic-or-prompt>` - Free-text topic description or problem statement
- `--doc <path>` - Use a document as the topic source
- `--research <synthesis-file>` - Path to Phase 1 research synthesis (from bulwark-research). Strongly recommended.
- `--scoped` - (default) Sequential Task tool mode with 5 roles. Use when the problem statement is well understood.
- `--exploratory` - Agent Teams peer debate with 4 roles. Use when validating whether an idea has merit. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

**Examples:**
- `/bulwark-brainstorm "agent teams" --research artifacts/research/agent-teams/synthesis.md` - Scoped brainstorm with research (default mode)
- `/bulwark-brainstorm --scoped "loop detection"` - Explicit scoped mode
- `/bulwark-brainstorm --exploratory "new plugin architecture"` - Exploratory mode with AT peer debate
- `/bulwark-brainstorm --doc plans/proposal.md --exploratory` - Exploratory from a document

---

## Stages

### Stage 1: Pre-Flight

```
Stage 1: Pre-Flight
├── Read problem statement / document
├── Load research synthesis if --research provided
├── Parse mode flag: --scoped (default) or --exploratory
├── Mode detection (see below)
├── AskUserQuestion if ambiguous (iterative, 2-3 questions per round)
├── Slugify topic for output directory
├── Create output directories: $PROJECT_DIR/logs/brainstorm/{topic-slug}/ and $PROJECT_DIR/artifacts/brainstorm/{topic-slug}/
├── Load subagent-prompting skill
├── Load references/role-project-sme.md (needed for Stage 2)
└── Token budget check (warn if >30% for --scoped, >25% for --exploratory)
```

**Mode Detection (MANDATORY — do NOT skip):**

1. Check `$CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var
2. Apply this decision matrix:

| Env Var | User Flag | Action |
|---------|-----------|--------|
| NOT SET | No flag | `--scoped` (default) |
| NOT SET | `--scoped` | `--scoped` |
| NOT SET | `--exploratory` | Notify user: "Agent Teams requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Using --scoped mode." Fall back to `--scoped`. |
| SET | No flag | `--scoped` (do NOT auto-select AT) |
| SET | `--scoped` | `--scoped` |
| SET | `--exploratory` | Execute AT Confirmation Flow (see below) |

**AT Confirmation Flow (when --exploratory is selected and env var is set):**

Display to user:

> **Exploratory mode uses Agent Teams peer debate and consumes ~2x tokens compared to --scoped mode.**
>
> 3 AT teammates will debate collaboratively after the SME phase.
>
> **Model class for AT teammates:**
> - **Opus** — highest quality, higher token cost
> - **Sonnet** — high quality, lower token cost (empirically validated)
>
> [Proceed with Opus / Proceed with Sonnet / Switch to --scoped]

Record the user's model choice for Stage 3B teammate spawning.

**AskUserQuestion Protocol (Pre-Spawn):**

If the problem statement is ambiguous, under-specified, or could benefit from scope boundaries:

1. Ask 2-3 clarifying questions using AskUserQuestion
2. Assess whether the answers provide sufficient clarity to construct high-quality prompts
3. If not, ask up to 3 more questions in a follow-up round
4. Repeat until clarity is achieved (no hard cap on rounds, but each round is 2-3 questions max)
5. If the problem statement is clear and well-scoped from the start, skip this step and note in diagnostics: `pre_flight_interview: skipped (problem statement sufficient)`

If `--research` was not provided, warn the user: "No research synthesis provided. Brainstorm quality is significantly higher when preceded by `/bulwark-research`. Proceed without research?"

### Stage 2: Project SME (Opus, Sequential — First)

```
Stage 2: Project SME
├── Load references/role-project-sme.md
├── Construct prompt using 4-part template
│   ├── GOAL: Establish project context relevant to the topic
│   ├── CONTEXT: Problem statement + research synthesis (if available)
│   └── OUTPUT: $PROJECT_DIR/logs/brainstorm/{topic-slug}/01-project-sme.md
├── Spawn general-purpose Opus agent
│   ├── Agent autonomously explores codebase (Glob, Grep, Read)
│   ├── NO hardcoded document paths — agent discovers what's relevant
│   └── Output documents which files were read and why
├── Read SME output
└── Token budget check
```

**CRITICAL — SME Autonomy**: The SME agent MUST NOT receive hardcoded project document paths. Instead:

- SME receives the problem statement and (optionally) research synthesis
- SME is spawned as `general-purpose` subagent type with Opus model
- SME autonomously explores the codebase using Glob, Grep, Read
- Instruct the SME: "Identify the MINIMUM files needed to answer: What exists relevant to this topic? Where are the integration points? What constraints apply? What must not be disrupted? Do NOT attempt to read the entire codebase."
- SME output documents which files it read and why

This makes the skill portable across any project.

### Stage 3A: Role Analysis — Task Tool Mode (`--scoped`)

**Execute this stage ONLY in `--scoped` mode. Skip entirely in `--exploratory` mode.**

```
Stage 3A: Role Analysis (--scoped)
├── Load references/role-product-manager.md
├── Load references/role-technical-architect.md
├── Load references/role-development-lead.md
├── Load templates/role-output.md
├── Construct 3 prompts using 4-part template
│   ├── Each receives: problem statement + research synthesis + SME output
│   └── Each writes to: $PROJECT_DIR/logs/brainstorm/{topic-slug}/{NN}-{role-slug}.md
├── Spawn all 3 agents in parallel via Task tool
│   ├── subagent_type: general-purpose
│   ├── model: opus
│   └── All 3 in a single message (parallel)
├── Read all 3 outputs
└── Token budget check (checkpoint if >55%)
```

**Output files (--scoped):** `02-product-manager.md`, `03-technical-architect.md`, `04-development-lead.md`

**CRITICAL**: Spawn all 3 agents in a single message with 3 Task tool calls. Do NOT spawn sequentially.

### Stage 3B: Role Analysis — Agent Teams Mode (`--exploratory`)

**Execute this stage ONLY in `--exploratory` mode. Skip entirely in `--scoped` mode.**

In `--exploratory` mode, 5 roles collapse to 4. The PM and Dev Lead merge into a Product & Delivery Lead. The Critical Analyst joins as an active AT teammate (not a sequential gatekeeper), challenging positions in real time throughout the debate.

```
Stage 3B: Role Analysis (--exploratory)
├── Load references/role-product-delivery-lead.md
├── Load references/role-technical-architect.md
├── Load references/role-critical-analyst.md
├── Load templates/role-output.md
├── Load templates/critic-output.md
├── Enter delegate mode as lead
├── Spawn 3 AT teammates with user's chosen model class (Opus or Sonnet)
│   ├── Product & Delivery Lead
│   ├── Technical Architect
│   └── Critical Analyst
├── Each teammate prompt includes:
│   ├── Role reference content
│   ├── SME output (from Stage 2)
│   ├── Problem statement + research synthesis
│   ├── Dual-output contract (SA2)
│   ├── Peer debate directives
│   └── AT mitigation patterns (4 mandatory: CC-ALL, task list, completion signal, confirmation handshake)
├── Wait for all teammates to complete
├── Read all 3 output files from logs/
└── Token budget check (checkpoint if >45%)
```

**Output files (--exploratory):** `02-product-delivery-lead.md`, `03-technical-architect.md`, `04-critical-analyst.md`

#### AT Teammate Prompt Structure, Configuration, and Failure Recovery

**MANDATORY**: Load `references/at-teammate-prompts.md` before constructing Stage 3B teammate prompts. It contains the full prompt structure (6 sections including dual-output contract, peer debate directives, 4 AT mitigation patterns, Critic deferred-verdict directive, and Lead Coordination Gates), AT configuration (hardcoded settings), and failure recovery procedures.

### Stage 4: Critical Analyst — `--scoped` Mode ONLY (Opus, Sequential — Last)

**Execute this stage ONLY in `--scoped` mode. In `--exploratory` mode, the Critical Analyst is a Stage 3B teammate — skip Stage 4 entirely.**

```
Stage 4: Critical Analyst (--scoped only)
├── Load references/role-critical-analyst.md
├── Load templates/critic-output.md
├── Construct prompt using 4-part template
│   ├── CONTEXT includes ALL prior outputs:
│   │   ├── Problem statement + research synthesis
│   │   ├── SME output (01-project-sme.md)
│   │   ├── PM output (02-product-manager.md)
│   │   ├── Architect output (03-technical-architect.md)
│   │   └── Dev Lead output (04-development-lead.md)
│   └── OUTPUT: $PROJECT_DIR/logs/brainstorm/{topic-slug}/05-critical-analyst.md
├── Spawn general-purpose Opus agent
├── Read Critical Analyst output
└── Token budget check
```

**CRITICAL**: The Critical Analyst MUST receive ALL 4 prior outputs. This is the whole point — the Critic synthesizes and challenges everything.

### Stage 5: Synthesis (SHARED — mode-aware)

```
Stage 5: Synthesis
├── Read ALL agent output files from logs/brainstorm/{topic-slug}/
│   ├── --scoped: expect 5 files (01-project-sme, 02-product-manager, 03-technical-architect, 04-development-lead, 05-critical-analyst)
│   └── --exploratory: expect 4 files (01-project-sme, 02-product-delivery-lead, 03-technical-architect, 04-critical-analyst)
├── Verify expected file count matches mode (5 for --scoped, 4 for --exploratory)
├── If any output is missing or empty → re-spawn that agent once (max 1 retry)
├── If retry fails → document gap in synthesis under "Incomplete Coverage"
├── Load templates/synthesis-output.md
├── Write synthesis to $PROJECT_DIR/artifacts/brainstorm/{topic-slug}/synthesis.md
│   └── Include mode field in YAML header (mode: scoped | exploratory)
├── AskUserQuestion for user on open questions (iterative, 2-3 per round)
├── Critical Evaluation Gate (see below)
└── Token budget check (must be <65% after synthesis)
```

**Enforcement**: Do NOT begin writing synthesis until ALL available agent outputs have been read. The orchestrator must reference every agent's output at least once in the synthesis.

**Mode-specific synthesis notes:**
- In `--exploratory` mode, the synthesis should capture debate dynamics — where teammates disagreed, what challenges were raised, and how positions evolved. Check for "Post-Debate Update" sections in agent outputs.
- In `--scoped` mode, synthesis follows the existing pattern (consensus areas, divergence areas, implementation outline).

#### Critical Evaluation Gate (Post-User Q&A)

After each AskUserQuestion round, do NOT blindly incorporate user responses. Instead:

**Step 1 — Classify each user response:**

| Classification | Definition | Action |
|---------------|------------|--------|
| **Preference** | Scope, priority, or UX choice (e.g., "I'd prefer v1 to focus on X", "Let's defer Y") | Incorporate directly. These are user decisions — no validation needed. |
| **Technical Claim** | Assertion about a technology, library, or API (e.g., "Library X supports this", "That API has rate limits") | **Do NOT incorporate.** Trigger Step 2. |
| **Architectural Suggestion** | Proposed structural approach (e.g., "What if we structure it as a plugin?", "We could use event sourcing") | **Do NOT incorporate.** Trigger Step 2. |

**Step 2 — For Technical Claims and Architectural Suggestions, present to user:**

> "Your suggestion about [X] involves a technical claim / architectural approach that hasn't been validated against the codebase and research. I recommend a targeted follow-up with 2 focused agents (Technical Architect + Critical Analyst) to verify feasibility and stress-test the approach.
>
> This will spawn 2 Opus agents and consume additional token budget.
>
> [Run follow-up validation / Incorporate as-is with LOW confidence caveat]"

**Step 3 — If follow-up validation approved:**

1. Spawn 2 Opus agents in parallel (single message, 2 Task tool calls):
   - **Technical Architect** — validates the suggestion against the codebase and research:
     GOAL: Validate whether [{user_suggestion}] is technically feasible for this project.
     Include the Propose-Challenge-Refine reasoning depth instructions.
     Agent has access to Glob, Grep, Read for codebase exploration.
   - **Critical Analyst** — stress-tests the suggestion:
     GOAL: Challenge [{user_suggestion}]. Is this the simplest approach? What assumptions does it introduce? What would change the verdict?
     Include the Highest-Risk Assumption Focus reasoning depth instructions.
2. Use the same 4-part prompt template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT)
3. Provide both agents with: original research synthesis, SME output, and the specific user suggestion
4. Output to: `$PROJECT_DIR/logs/brainstorm/{topic-slug}/followup-{NN}-architect.md` and `followup-{NN}-critic.md`
5. Read both outputs, then update synthesis with validated findings
6. Tag follow-up findings in synthesis with: `[Follow-up: validated]` or `[Follow-up: refuted]` or `[Follow-up: mixed — see details]`

**Step 4 — If user declines follow-up:**

Incorporate the user's suggestion into synthesis with an explicit caveat:
> **[Unvalidated — user suggestion, not verified against codebase or research]**: {suggestion}

**Repeat**: After updating synthesis, ask if user has additional questions or input. Apply the same classification gate to each round. There is no limit on follow-up rounds, but each round with Technical Claim / Architectural Suggestion input that triggers validation consumes ~15-20% token budget (2 Opus agents) — warn user if approaching 55%.

### Stage 6: Diagnostics (REQUIRED)

```
Stage 6: Diagnostics
├── Write diagnostic YAML to $PROJECT_DIR/logs/diagnostics/bulwark-brainstorm-{YYYYMMDD-HHMMSS}.yaml
└── Verify completion checklist
```

---

## Roles (Sections)

Each role brings a distinct professional perspective. Role availability depends on the execution mode.

### Role Mapping by Mode

| Role | `--scoped` | `--exploratory` |
|------|-----------|----------------|
| **Project SME** | Stage 2: Solo first (Task tool) | Stage 2: Solo first (Task tool) — identical |
| **Senior Product Manager** | Stage 3A: Parallel (Task tool) | Merged into Product & Delivery Lead |
| **Senior Technical Architect** | Stage 3A: Parallel (Task tool) | Stage 3B: AT teammate |
| **Senior Development Lead** | Stage 3A: Parallel (Task tool) | Merged into Product & Delivery Lead |
| **Product & Delivery Lead** | N/A | Stage 3B: AT teammate (combined PM + Dev Lead) |
| **Critical Analyst** | Stage 4: Sequential last (Task tool) | Stage 3B: AT teammate — active from start |

### Role 1: Project SME (Both Modes — Sequential First)

**Purpose**: Establish what exists, what has been built, and where the topic fits in the current architecture.

**Focus Areas**:
- Current project architecture relevant to the topic
- Existing assets that relate to or would be affected
- Integration points — where does this connect?
- Constraints imposed by current design decisions
- What the project already does well that must not be disrupted

**Execution**: Solo, first. Output feeds all subsequent agents. Identical in both modes.

**Reference**: `references/role-project-sme.md`

### Role 2: Senior Product Manager (`--scoped` only)

**Purpose**: Evaluate user value, prioritization, and scope boundaries.

**Focus Areas**:
- User value proposition — who benefits and how?
- Prioritization — what delivers the most value soonest?
- Scope boundaries — what is v1 vs. deferred?
- Success criteria — how do we know this works?
- Risk to user experience if implemented poorly

**Execution**: Parallel with Architect and Dev Lead (Stage 3A). Receives SME output.

**Reference**: `references/role-product-manager.md`

### Role 3: Senior Technical Architect (Both Modes)

**Purpose**: Define system design, patterns, and technical trade-offs.

**Focus Areas**:
- Architectural approach — how should this be structured?
- Design patterns that apply (and which to avoid)
- Technical trade-offs and their implications
- Integration architecture — how it connects to existing systems
- Extensibility and future-proofing considerations

**Execution**:
- `--scoped`: Parallel with PM and Dev Lead (Stage 3A). Receives SME output.
- `--exploratory`: AT teammate (Stage 3B). Receives SME output + peer debate.

**Reference**: `references/role-technical-architect.md`

### Role 4: Senior Development Lead (`--scoped` only)

**Purpose**: Assess implementation feasibility, effort, and practical risks.

**Focus Areas**:
- Implementation feasibility — can this be built with available tools?
- Effort estimation — complexity and session count
- Implementation risks — what could go wrong during building?
- Testing strategy — how do we verify this works?
- Dependencies and ordering — what must be built first?

**Execution**: Parallel with PM and Architect (Stage 3A). Receives SME output.

**Reference**: `references/role-development-lead.md`

### Role 5: Product & Delivery Lead (`--exploratory` only)

**Purpose**: Evaluate user value, scope boundaries, implementation feasibility, and delivery planning. Combines PM's value/prioritization lens with Dev Lead's feasibility/effort lens.

**Focus Areas**:
- User value proposition and prioritization
- Scope boundaries — v1 vs. deferred
- Implementation feasibility and effort estimation
- Build order, dependencies, testing strategy
- Value-effort trade-offs — which features have the best ROI?

**Execution**: AT teammate (Stage 3B). Receives SME output + peer debate.

**Reference**: `references/role-product-delivery-lead.md`

### Role 6: Critical Analyst (Both Modes — Different Execution)

**Purpose**: Perform cost-benefit analysis, challenge assumptions, validate the problem itself, poke holes.

**Focus Areas**:
- Problem validation — should this problem be solved at all?
- Cost-benefit analysis — is the investment justified?
- Assumption challenges — what might be wrong?
- Gaps in the proposals — what has been overlooked?
- Simpler alternatives — could a less ambitious approach work?
- Kill criteria — under what conditions should this be abandoned?
- Final verdict: proceed / modify / defer / kill

**Execution**:
- `--scoped`: Solo, last (Stage 4). Receives ALL prior outputs. Maximum information, zero influence on the analysis process.
- `--exploratory`: AT teammate (Stage 3B). Active from start. Challenges in real time. Partial information early, maximum influence on debate. Deferred verdict.

**Reference**: `references/role-critical-analyst.md`
**Output template**: `templates/critic-output.md` (has verdict + problem validation sections)

---

## Execution Flow (F# Pipeline)

```fsharp
// --scoped mode (default, unchanged)
ProjectSME(topic, research?)           // Stage 2: Opus, solo
|> [ProductManager, TechArchitect, DevLead](sme_output)  // Stage 3A: 3 Opus, parallel
|> CriticalAnalyst(all_prior_outputs)  // Stage 4: Opus, solo
|> Synthesis                           // Stage 5: Orchestrator

// --exploratory mode (new)
ProjectSME(topic, research?)           // Stage 2: Opus, solo (Task tool)
|> AgentTeam[ProductDeliveryLead, TechArchitect, CriticalAnalyst](sme_output)  // Stage 3B: AT peer debate
|> Synthesis                           // Stage 5: Orchestrator
```

---

## Token Budget Management

| Checkpoint | `--scoped` Threshold | `--exploratory` Threshold | Action |
|------------|---------------------|--------------------------|--------|
| After constructing SME prompt | >30% consumed | >25% consumed | Warn user about agent token cost |
| After reading Stage 3A/3B outputs | >55% | >45% | Checkpoint with user |
| After synthesis | Must be <65% | Must be <65% | Leave room for session closing |
| Synthesis complete at >65% | Immediate | Immediate | Create handoff, do not start additional work |

**`--exploratory` costs ~2x tokens** due to AT peer debate overhead. The lower thresholds account for this.

If token budget is insufficient to complete all agents + synthesis, inform the user and suggest splitting (e.g., "SME + role analysis this session, synthesis next session").

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Agent returns empty output | Re-spawn once. If still empty, document gap in synthesis. |
| Agent returns truncated output | Accept as-is, note in diagnostics. |
| Agent fails to spawn | Re-spawn once. If still fails, skip role, document. |
| SME fails | STOP — subsequent agents depend on SME. Inform user. |
| Token budget exceeded mid-session | Stop spawning, synthesize from available outputs, note incomplete. |
| Research synthesis not provided | Warn user, proceed with lower quality. |
| AT teammate fails mid-debate (`--exploratory`) | Fall back to Stage 3A for failed role only. Partial AT output from successful teammates feeds into fallback as additional context. |
| All AT teammates fail (`--exploratory`) | Fall back to full Stage 3A (--scoped pipeline). Document in diagnostics. |
| AT lead context compaction (`--exploratory`) | Known platform limitation. SME running before AT is the structural mitigation. Document in diagnostics if observed. |
| `--exploratory` requested, env var not set | Notify user, fall back to `--scoped`. Not an error — graceful degradation. |

---

## Diagnostic Output (REQUIRED)

**MANDATORY**: You MUST write diagnostic output after every invocation. This is Stage 6 and cannot be skipped.

Write to: `$PROJECT_DIR/logs/diagnostics/bulwark-brainstorm-{YYYYMMDD-HHMMSS}.yaml`

**Template**: Use `templates/diagnostic-output.yaml` for the schema. Fill in actual values from the session.

---

## Completion Checklist

**IMPORTANT**: Before returning to the user, verify ALL applicable items are complete:

### Shared (both modes)

- [ ] Stage 1: Pre-flight complete (topic defined, directories created, skills loaded)
- [ ] Stage 1: Mode detection performed (env var checked, mode selected)
- [ ] Stage 1: AskUserQuestion used if topic was ambiguous
- [ ] Stage 1: User warned if --research not provided
- [ ] Stage 2: Project SME spawned (Opus) and output read
- [ ] Stage 2: SME explored codebase autonomously (no hardcoded paths)
- [ ] Stage 5: ALL outputs read before writing synthesis
- [ ] Stage 5: Synthesis written using `templates/synthesis-output.md` with mode field in YAML header
- [ ] Stage 5: AskUserQuestion used for post-synthesis review
- [ ] Stage 5: Critical Evaluation Gate applied to all user responses
- [ ] Stage 5: Synthesis written to `$PROJECT_DIR/artifacts/brainstorm/{topic-slug}/synthesis.md`
- [ ] Stage 6: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

### `--scoped` mode only

- [ ] Stage 3A: All 3 role agents spawned in parallel (Opus)
- [ ] Stage 3A: All role outputs written to `$PROJECT_DIR/logs/brainstorm/{topic-slug}/`
- [ ] Stage 4: Critical Analyst spawned with ALL prior outputs
- [ ] Stage 4: Critic output read

### `--exploratory` mode only

- [ ] Stage 1: AT Confirmation Flow completed (token warning + model class choice)
- [ ] Stage 3B: Delegate mode entered, 3 AT teammates spawned with correct model class
- [ ] Stage 3B: All teammate outputs written to `$PROJECT_DIR/logs/brainstorm/{topic-slug}/`
- [ ] Stage 3B: AT mitigation patterns included in all teammate prompts (CC-ALL, task list, completion signal, confirmation handshake)
- [ ] Stage 3B: Lead enforces Work-Complete Confirmation Gate, Re-Entry Gate, and Rendezvous Gate before synthesis
- [ ] Stage 6: AT-specific metrics captured in diagnostic YAML

**Do NOT return to user until all applicable checkboxes can be marked complete.**
