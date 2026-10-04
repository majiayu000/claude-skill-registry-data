---
name: plan-creation
description: Create structured implementation plans via a 4-role scrum team (Product Owner, Architect, Eng/Delivery Lead, QA/Critic) with optional Agent Teams peer debate mode.
when_to_use: Use when the user asks to design, plan, scope, or break down an implementation, feature, refactor, or system change. Also invoked by orchestrator pipelines (e.g., new-feature) that need a structured plan before execution.
user-invocable: true
argument-hint: "<topic, filepath, or directory> [--doc <path>] [--research <synthesis-file>]"
skills:
  - subagent-prompting
allowed-tools:
  - AskUserQuestion
  - Bash
  - Edit
  - Glob
  - Grep
  - Read
  - Skill
  - Task
  - Write
version: 1.0.2
author: "Ashay Kubal @ Qball Inc."
---

# Plan Creation

Create structured implementation plans through a 4-role collaborative scrum team: Product Owner, Technical Architect, Engineering & Delivery Lead, and QA/Critic. The Product Owner explores the codebase first, then Architect and Eng Lead analyze in parallel, and the QA/Critic challenges everything last. The orchestrator synthesizes all outputs into a hybrid Markdown + YAML plan.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Implementation planning | "Create an implementation plan for X" |
| Feature planning | "Plan how we'd build X" |
| Project scoping | "Break down X into phases and workpackages" |
| Post-research planning | "We've researched X, now create a plan" |
| Task brief creation | "Create a task brief for X" |

**DO NOT use for:**
- Initial topic research (use `bulwark-research` first)
- Feasibility brainstorming (use `bulwark-brainstorm`)
- Quick technical questions (ask directly)
- Code review or debugging (use `code-review` or `issue-debugging`)

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Plan output template** | `templates/plan-output.md` | **REQUIRED** | Load at Stage 5 for plan structure |
| **Critic output template** | `templates/critic-output.md` | **REQUIRED** | Include in QA/Critic agent prompt |
| **Synthesis template** | `templates/synthesis-output.md` | **REQUIRED** | Use when writing synthesis |
| **Diagnostic template** | `templates/diagnostic-output.yaml` | **REQUIRED** | Use at Stage 6 |
| **Role output reference** | `templates/role-output.md` | OPTIONAL | Reference for parsing agent outputs |
| **Subagent prompting** | `subagent-prompting` skill | **REQUIRED** | Load at Stage 1 for 4-part prompt template |
| **Research synthesis** | `--research <file>` | OPTIONAL | If provided, include in all agent prompts |

**Fallback behavior:**
- If an agent fails to spawn: Re-spawn once. If still fails, skip that role and document in synthesis under "Incomplete Coverage"
- If PO fails: STOP — all downstream agents depend on PO output. Inform user.
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
- [ ] **Stage 1 — Mode Detection**: If env var is SET, user offered choice via AskUserQuestion (Agent Teams vs Task tool) — you MUST NOT default silently
- [ ] **Stage 1 — Mode Detection**: If user selects Agent Teams, AT Confirmation Flow executed (RED banner + model class choice)
- [ ] **Stage 2 — Product Owner**: PO spawned via Task tool (`plan-creation-po`, Opus) and output read
- [ ] **Stage 3A or 3B**: Correct mode executed based on user's Stage 1 choice
- [ ] **Stage 3A (Task tool)**: Architect + Eng Lead spawned in parallel via Task tool with all prior outputs
- [ ] **Stage 3B (Agent Teams)**: Agent files read, delegate mode entered, 3 teammates spawned with correct model class
- [ ] **Stage 3B (Agent Teams)**: Lead enforces Work-Complete Confirmation Gate, Re-Entry Gate, and Shutdown Gate (rendezvous before synthesis) — synthesis MUST NOT begin until all teammates have explicit YES confirmation AND 30s quiet period has elapsed
- [ ] **Stage 4 — QA / Critic**: (Task tool mode 3A only — in 3B mode the critic is embedded in the team) QA/Critic spawned with all 3 prior outputs and output read
- [ ] **Stage 5 — Synthesis**: ALL role outputs read, synthesis written, plan drafted using template
- [ ] **Stage 5 — Consistency**: Before writing the plan, verify `executive_summary.workpackage_count == sum(phase.workpackages.length for phase in phases)`. If counts disagree, re-derive the executive summary count from the structured phase blocks and emit a `process_notes` entry in the Stage 6 diagnostic flagging the drift.
- [ ] **Stage 5 — Approval**: Plan presented to user via AskUserQuestion — you MUST NOT write the final plan without user approval
- [ ] **Stage 5 — Plan Written**: Final plan written to `plans/{slug}/plan_v{N}.md`
- [ ] **Stage 6 — Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

---

## Usage

```
/plan-creation <topic-or-prompt> [--research <synthesis-file>]
/plan-creation --doc <path-to-document> [--research <synthesis-file>]
```

**Arguments:**
- `<topic-or-prompt>` - Free-text topic description or problem statement
- `--doc <path>` - Use a document as the topic source
- `--research <synthesis-file>` - Path to research synthesis (from bulwark-research or bulwark-brainstorm). Strongly recommended.

**Examples:**
- `/plan-creation "add user authentication" --research logs/research/auth/synthesis.md`
- `/plan-creation --doc plans/proposal.md`
- `/plan-creation "migrate database to PostgreSQL"`

**Plan Versioning:**

Plans are written to `plans/{slug}/plan_v{N}.md` with automatic version detection:

| Scenario | Version | Example |
|----------|---------|---------|
| First plan for a topic | `v1` | `plans/add-auth/plan_v1.md` |
| Minor revision (user iterates on current plan) | `v1.1`, `v1.2` | Approval gate feedback → revision |
| Major version (full re-run or pivot) | `v2`, `v3` | New invocation for same slug |

The skill checks for existing `plans/{slug}/plan_v*.md` files before writing. When ambiguous (re-run vs revision), it asks the user.

---

## Stages

### Stage 1: Pre-Flight

```
Stage 1: Pre-Flight
├── Read problem statement / document
├── Load research synthesis if --research provided
├── AskUserQuestion if ambiguous (iterative, 2-3 questions per round)
├── Slugify topic for output directory
├── Create output directory: $PROJECT_DIR/logs/plan-creation/{slug}/
├── Load subagent-prompting skill
├── Detect mode: Task tool (default) or Agent Teams (opt-in)
└── Token budget check (warn if >30% consumed)
```

**AskUserQuestion Protocol (Pre-Spawn):**

If the problem statement is ambiguous, under-specified, or could benefit from scope boundaries:

1. Ask 2-3 clarifying questions using AskUserQuestion
2. Assess whether the answers provide sufficient clarity to construct high-quality prompts
3. If not, ask up to 3 more questions in a follow-up round
4. Repeat until clarity is achieved (no hard cap on rounds, but each round is 2-3 questions max)
5. If the problem statement is clear and well-scoped from the start, skip this step and note in diagnostics: `pre_flight_interview: skipped (problem statement sufficient)`

If `--research` was not provided, warn the user: "No research synthesis provided. Plan quality is significantly higher when preceded by `/bulwark-research` or `/bulwark-brainstorm`. Proceed without research?"

**Mode Detection:**

1. Check `$CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var
2. If env var is SET: offer user choice via AskUserQuestion — "Agent Teams enhanced mode is available. Use Agent Teams or Task tool?" Default to Task tool if user doesn't specify.
3. If env var is NOT SET: use Task tool mode. If user explicitly requested Agent Teams, notify: "Agent Teams requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Using Task tool mode."

**AT Confirmation Flow (if user selects Agent Teams):**

Execute this confirmation flow BEFORE spawning any teammates:

**Step 1 — Display RED warning banner** using ANSI color `\033[38;2;255;154;150m` (#FF9A96):

```
⚠️  NOTICE: Claude Code's Agent Teams is an experimental feature. Unexpected
issues like teammates being stuck or unresponsive may occur. Agent Teams mode
is also significantly more token-expensive than Task tool mode (4 concurrent
agents vs sequential sub-agents).

If you run into issues, start a new session and re-run /plan-creation.
If the final output does not match expectations, re-run with Task tool mode.
```

**Step 2 — AskUserQuestion: model class + mode confirmation**

Present a single question with 3 options:

| Option | Label | Description |
|--------|-------|-------------|
| 1 | Opus agents (Recommended) | Higher quality analysis, highest token cost. Opus-class agents for all roles. |
| 2 | Sonnet agents | Good quality, lower token cost. Sonnet-class agents for all roles. |
| 3 | Switch to Task tool mode | Cancel Agent Teams and use sequential sub-agents instead. |

- Option 1: proceed with Opus agents in AT mode (Stage 3B)
- Option 2: proceed with Sonnet agents in AT mode (Stage 3B)
- Option 3: fall back to Task tool mode (Stage 3A), skip AT entirely

### Stage 2: Product Owner (Opus, Sequential — First)

```
Stage 2: Product Owner
├── Construct prompt using 4-part template
│   ├── GOAL: Explore codebase and produce requirements analysis for {topic}
│   ├── CONSTRAINTS: Do not make architectural decisions or estimate effort
│   ├── CONTEXT: Problem statement + research synthesis (if available)
│   └── OUTPUT: $PROJECT_DIR/logs/plan-creation/{slug}/01-product-owner.md
├── Spawn plan-creation-po agent via Task tool
│   ├── subagent_type: plan-creation-po
│   ├── model: opus (specified in agent frontmatter)
│   ├── Agent autonomously explores codebase (Glob, Grep, Read)
│   └── NO hardcoded document paths — agent discovers what's relevant
├── Read PO output from logs/plan-creation/{slug}/01-product-owner.md
└── Token budget check
```

**CRITICAL — PO Autonomy**: The PO agent MUST NOT receive hardcoded project document paths. Instead:

- PO receives the problem statement and (optionally) research synthesis
- PO is spawned as `plan-creation-po` subagent type
- PO autonomously explores the codebase using Glob, Grep, Read
- PO output documents which files it read and why

This makes the skill portable across any project.

### Stage 3A: Scrum Team — Task Tool Mode

```
Stage 3A: Scrum Team (Task Tool Mode)
├── Read PO output in full
├── Construct 2 prompts using 4-part template:
│   ├── Technical Architect:
│   │   ├── GOAL: Analyze system design, components, integration, trade-offs for {topic}
│   │   ├── CONSTRAINTS: Do not estimate effort or sequence work
│   │   ├── CONTEXT: Problem statement + research synthesis + PO output (full text)
│   │   └── OUTPUT: $PROJECT_DIR/logs/plan-creation/{slug}/02-technical-architect.md
│   └── Engineering & Delivery Lead:
│       ├── GOAL: Produce WBS, estimates, dependencies, milestones, risk register for {topic}
│       ├── CONSTRAINTS: Do not redesign architecture — work with Architect's design
│       ├── CONTEXT: Problem statement + research synthesis + PO output (full text)
│       └── OUTPUT: $PROJECT_DIR/logs/plan-creation/{slug}/03-eng-delivery-lead.md
├── Spawn BOTH agents in parallel via Task tool (single message, 2 Task tool calls)
│   ├── subagent_type: plan-creation-architect (opus)
│   └── subagent_type: plan-creation-eng-lead (sonnet)
├── Read both outputs
└── Token budget check (checkpoint if >55%)
```

**CRITICAL**: Spawn both agents in a single message with 2 Task tool calls. Do NOT spawn sequentially.

**Note**: Both Architect and Eng Lead receive the PO output directly in their prompt CONTEXT. They do NOT read each other's output — they work independently in parallel. The QA/Critic cross-references their outputs in Stage 4.

### Stage 3B: Scrum Team — Agent Teams Mode (Enhanced, Opt-In)

**Pre-condition**: User selected Agent Teams in Pre-Flight AND confirmed model class in AT Confirmation Flow.

```
Stage 3B: Scrum Team (Agent Teams Mode)
├── Read PO output in full (from Stage 2)
├── Read agent definition files from .claude/agents/:
│   ├── .claude/agents/plan-creation-architect.md
│   ├── .claude/agents/plan-creation-eng-lead.md
│   └── .claude/agents/plan-creation-qa-critic.md
├── YOU (the orchestrator) become the delegate-mode Scrum Lead
│   └── Your role: coordination ONLY — do not perform analysis yourself
├── Enter delegate mode with 3 teammates
├── Create shared task list with initial tasks:
│   ├── "[Architect] Analyze system design for {topic}"
│   ├── "[Eng Lead] Produce WBS and delivery plan for {topic}"
│   └── "[QA/Critic] Adversarially review all analyses for {topic}"
├── Spawn 3 teammates using agent file content as system prompts:
│   ├── Technical Architect (model: user's choice from AT Confirmation)
│   ├── Engineering & Delivery Lead (model: user's choice from AT Confirmation)
│   └── QA / Critic (model: user's choice from AT Confirmation)
├── Each teammate prompt MUST include (in addition to agent file content):
│   ├── Problem statement + research synthesis (if available)
│   ├── PO output (full text)
│   ├── Dual-output contract (see below)
│   ├── CC-ALL instruction (see below)
│   ├── Task list coordination instruction (see below)
│   └── Rendezvous instruction (see below)
├── Use in-process display mode (WSL2 safe — no tmux)
├── Shutdown gate: see below
└── Token budget check
```

**Dual-Output Contract** (include in EVERY teammate prompt):

> You MUST produce two outputs:
> 1. **Full analysis** → Write to `$PROJECT_DIR/logs/plan-creation/{slug}/{NN}-{role-name}.md` using the Write tool. This is your SA2-compliant artifact. Include all analysis, tables, and findings.
> 2. **Coordination summary** → Send a 3-5 sentence summary of your key findings and conclusions to the Scrum Lead via mailbox. This is for coordination only — the full analysis is in the log file.

**CC-ALL Instruction** (include in EVERY teammate prompt):

> When sending peer DMs with work instructions, challenges, or significant findings, you MUST CC every other teammate (including the Scrum Lead). Peer DMs without full-team CC are invisible to non-recipients and will be treated as stalled work. Format: include `CC: <Teammate-A>, <Teammate-B>, Scrum-Lead` at the top of the message. The CC-ALL convention replaces the prior CC-to-Lead pattern — every participant sees every cross-cutting peer message in real time.

**Task List Coordination Instruction** (include in EVERY teammate prompt):

> When you receive work from a peer via DM (e.g., "review this section", "stress-test this estimate"), create a new task in the shared task list describing the peer-dispatched work before starting it. Mark it in_progress immediately. This gives the Scrum Lead visibility into peer-coordinated work.

**Rendezvous Instruction** (include in EVERY teammate prompt):

> Your FINAL action before going idle is to send the Scrum Lead: "WORK COMPLETE — all tasks done, log written to {path}". Do NOT go idle without sending this message.

**Work-Complete Confirmation Gate (MANDATORY)** — Scrum Lead logic — YOU enforce this:

When a teammate sends `WORK COMPLETE`, do NOT mark them terminal. Instead:

1. Send the following DM to that teammate, CC all other teammates:
   > "Confirm: have you incorporated ALL inbound debate feedback from this round? Reply YES when fully complete, NO if still iterating."
2. Await explicit `YES` response.
3. Only after receiving `YES` mark the teammate as terminal.
4. If the teammate replies `NO` or does not respond within the timeout, treat them as active — do NOT begin synthesis.

**Reason**: teammates often send `WORK COMPLETE` at initial draft, then iterate on peer feedback. Without this gate, synthesis excludes post-debate outcomes.

**Re-Entry Gate (MANDATORY)** — extends the Confirmation Gate:

If a teammate who previously confirmed `YES` sends any new peer DM, new WORK COMPLETE signal, or new content, mark them as **re-active** and require a fresh confirmation handshake (repeat the Confirmation Gate procedure). The previous confirmation is **invalidated**.

**Reason**: a teammate may confirm done, then re-engage after receiving a late peer DM. Without re-entry handling, the late iteration is missed.

**Shutdown Gate** (rendezvous before synthesis):

The Scrum Lead (you, the orchestrator) MUST NOT call `requestShutdown` for ANY teammate AND MUST NOT begin Stage 5 synthesis until ALL of the following are true:

1. All shared task list tasks are in terminal state (completed or blocked)
2. WORK COMPLETE + explicit `YES` confirmation received from ALL 3 teammates (per Confirmation Gate above)
3. All 3 log files exist and are non-empty:
   - `logs/plan-creation/{slug}/02-technical-architect.md`
   - `logs/plan-creation/{slug}/03-eng-delivery-lead.md`
   - `logs/plan-creation/{slug}/04-qa-critic.md`
4. **Quiet period of 30 seconds** with NO new peer DM activity AND NO re-active teammates (per Re-Entry Gate). If any new activity lands during the quiet period, reset the 30s timer and re-evaluate the Confirmation Gate for any re-active teammate.

If a teammate appears idle but has NOT sent WORK COMPLETE:
- Check the shared task list for in-progress tasks assigned to that teammate
- Send a status check message: "Status update? Are you still working on [task]?"
- Do NOT send `requestShutdown` — they may be executing a long tool call

**AT Completion Banner** (display after ALL teammates shut down):

After Agent Teams execution completes successfully, display an AMBER banner using ANSI color `\033[38;2;255;244;176m` (#FFF4B0):

```
ℹ️  Agent Teams is an experimental feature. If the final plan does not match
your expectations, try re-running /plan-creation with Task tool mode
(sequential sub-agents). Individual role outputs are preserved in
logs/plan-creation/{slug}/ for inspection.
```

Then proceed to Stage 5 (Synthesis) — Stage 4 is skipped in AT mode.

**CRITICAL — Agent File Reuse**: The 3 agent files in `.claude/agents/` contain the role expertise (system prompts, output formats, tool constraints). For AT mode, read each file's content and use it as the teammate's system prompt. This keeps a single source of truth per role — the agent files serve both Task tool mode (via `subagent_type`) and AT mode (content embedded in teammate prompts).

**Note**: In AT mode, the QA/Critic participates throughout — it can challenge the Architect and Eng Lead via peer DMs during their analysis, not just after. This is the primary quality advantage over Task tool mode.

---

### Stage 4: QA / Critic (Sonnet, Sequential — Last, Task Tool Mode ONLY)

```
Stage 4: QA / Critic
├── Load templates/critic-output.md
├── Read ALL 3 prior output files:
│   ├── 01-product-owner.md
│   ├── 02-technical-architect.md
│   └── 03-eng-delivery-lead.md
├── Construct prompt using 4-part template
│   ├── GOAL: Adversarially review all prior analyses — challenge assumptions, identify gaps, stress-test estimates, produce APPROVE/MODIFY/REJECT verdict
│   ├── CONSTRAINTS: Do not redesign or re-plan — only challenge and validate
│   ├── CONTEXT: Problem statement + research synthesis + ALL 3 prior outputs (full text) + critic-output.md template
│   └── OUTPUT: $PROJECT_DIR/logs/plan-creation/{slug}/04-qa-critic.md
├── Spawn plan-creation-qa-critic agent via Task tool
│   ├── subagent_type: plan-creation-qa-critic
│   └── model: sonnet (specified in agent frontmatter)
├── Read Critic output
└── Token budget check
```

**CRITICAL**: The QA/Critic MUST receive ALL 3 prior outputs in full. This is the entire point — the Critic cross-references PO requirements against Architect components against Eng Lead workpackages to find gaps.

**Skip condition**: If Agent Teams mode was used (Stage 3B), skip Stage 4 entirely — the QA/Critic already participated throughout Stage 3B via peer debate. Proceed directly to Stage 5.

### Stage 5: Synthesis & Plan Output (SHARED — Mode-Aware)

```
Stage 5: Synthesis
├── Read ALL 4 agent output files (MANDATORY — do not skip any):
│   ├── logs/plan-creation/{slug}/01-product-owner.md
│   ├── logs/plan-creation/{slug}/02-technical-architect.md
│   ├── logs/plan-creation/{slug}/03-eng-delivery-lead.md
│   └── logs/plan-creation/{slug}/04-qa-critic.md
├── If Agent Teams mode: also review lead coordination notes from the AT session
├── If any output is missing or empty → re-spawn that agent once (max 1 retry)
│   └── In AT mode: re-spawning is NOT possible — document gap in "Incomplete Coverage"
├── If retry fails → document gap in synthesis under "Incomplete Coverage"
├── Load templates/synthesis-output.md
├── Load templates/plan-output.md
├── Write synthesis to $PROJECT_DIR/logs/plan-creation/{slug}/synthesis.md
├── Compose plan draft:
│   ├── Executive Summary from synthesis consensus + PO problem statement
│   ├── YAML body from:
│   │   ├── Phases and workpackages: Eng Lead's WBS + Architect's component structure
│   │   ├── Milestones: Eng Lead's milestones
│   │   ├── Dependency graph: Eng Lead's dependency analysis + Architect's integration order
│   │   ├── Risks: Consolidated from all roles, prioritized by Critic
│   │   └── Kill criteria: From Critic's verdict
│   └── Apply Critic's MODIFY requirements (if verdict was MODIFY)
├── Present draft plan to user via AskUserQuestion approval gate
├── Critical Evaluation Gate (see below)
├── Determine plan version:
│   ├── Glob for existing plans/{slug}/plan_v*.md
│   ├── If none found: version = v1 (first plan)
│   ├── If user is iterating on the current plan (minor revision): bump minor (v1 → v1.1, v1.1 → v1.2)
│   ├── If user is starting fresh or pivoting: bump major (v1 → v2, v2 → v3)
│   └── When ambiguous, ask user: "This is a revision of the existing plan (v1.1) or a new plan (v2)?"
├── On approval: write final plan to plans/{slug}/plan_v{N}.md
├── Emit Stage 5 opt-in hint (see below) — discoverability for plan-to-tasks
└── Token budget check (must be <65% after synthesis)
```

**Enforcement**: Do NOT begin writing synthesis until ALL available agent outputs have been read. The orchestrator must reference every agent's output at least once in the synthesis.

**Stage 5 opt-in hint** (P10.5) — after writing the plan, emit this 3-line hint to the user:

> **Next step (optional)**: To generate executable task structure from this plan, run:
>
>     /plan-to-tasks plans/{slug}/plan_v{N}.md
>
> The skill will produce a structured `tasks.yaml` (workpackage index) and per-workpackage YAML files for execution-ready task tracking. No-op cost when ignored; discoverable when needed.

#### Critical Evaluation Gate (Post-User Q&A)

After each AskUserQuestion round, do NOT blindly incorporate user responses. Instead:

**Step 1 — Classify each user response:**

| Classification | Definition | Action |
|---------------|------------|--------|
| **Preference** | Scope, priority, or UX choice (e.g., "I'd prefer v1 to focus on X", "Let's defer Y") | Incorporate directly. These are user decisions — no validation needed. |
| **Technical Claim** | Assertion about a technology, library, or API (e.g., "Library X supports this", "That API has rate limits") | **Do NOT incorporate.** Trigger Step 2. |
| **Architectural Suggestion** | Proposed structural approach (e.g., "What if we structure it as a plugin?", "We could use event sourcing") | **Do NOT incorporate.** Trigger Step 2. |

**Step 2 — For Technical Claims and Architectural Suggestions, present to user:**

> "Your suggestion about [X] involves a technical claim / architectural approach that hasn't been validated against the codebase and research. I recommend a targeted follow-up with 2 focused agents (Technical Architect + QA/Critic) to verify feasibility and stress-test the approach.
>
> This will spawn 2 agents and consume additional token budget.
>
> [Run follow-up validation / Incorporate as-is with LOW confidence caveat]"

**Step 3 — If follow-up validation approved:**

1. Spawn 2 agents in parallel (single message, 2 Task tool calls):
   - **Technical Architect** (`plan-creation-architect`) — validates the suggestion against the codebase and research
   - **QA/Critic** (`plan-creation-qa-critic`) — stress-tests the suggestion
2. Use the same 4-part prompt template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT)
3. Provide both agents with: original research synthesis, PO output, and the specific user suggestion
4. Output to: `$PROJECT_DIR/logs/plan-creation/{slug}/followup-{NN}-architect.md` and `followup-{NN}-critic.md`
5. Read both outputs, then update plan with validated findings
6. Tag follow-up findings in plan with: `[Follow-up: validated]` or `[Follow-up: refuted]` or `[Follow-up: mixed — see details]`

**Step 4 — If user declines follow-up:**

Incorporate the user's suggestion into the plan with an explicit caveat:
> **[Unvalidated — user suggestion, not verified against codebase or research]**: {suggestion}

**Repeat**: After updating the plan, ask if user has additional input. Apply the same classification gate to each round. Each round with Technical Claim / Architectural Suggestion input that triggers validation consumes ~10-15% token budget (2 agents) — warn user if approaching 55%.

### Stage 6: Diagnostics (REQUIRED)

```
Stage 6: Diagnostics
├── Write diagnostic YAML to $PROJECT_DIR/logs/diagnostics/plan-creation-{YYYYMMDD-HHMMSS}.yaml
└── Verify Mandatory Execution Checklist (top of skill)
```

---

## Execution Flow (F# Pipeline)

```fsharp
// Task tool mode (default)
ProductOwner(topic, research?)                          // Stage 2: Opus, solo
|> [Architect, EngDeliveryLead](po_output)              // Stage 3A: parallel Task tool
|> QACritic(all_prior_outputs)                          // Stage 4: sequential Task tool
|> Synthesis |> ApprovalGate |> PlanOutput(plan_v{N})   // Stage 5: versioned output

// Agent Teams mode (enhanced, opt-in)
ProductOwner(topic, research?)                          // Stage 2: Opus, Task tool (solo)
|> AgentTeam[Architect, EngDeliveryLead, QACritic](po_output)  // Stage 3B: peer debate
|> Synthesis |> ApprovalGate |> PlanOutput(plan_v{N})   // Stage 5: versioned output
// Note: Stage 4 skipped in AT mode — QA/Critic participates throughout Stage 3B
```

---

## Token Budget Management

| Checkpoint | Threshold | Action |
|------------|-----------|--------|
| After constructing PO prompt | >30% consumed | Warn user: "4 agents will consume significant context" |
| After reading Stage 3A outputs | Running tally | If approaching 55%, checkpoint with user |
| After synthesis | Must be <65% | Leave room for plan approval + session closing |
| Synthesis complete at >65% | Immediate | Write plan as-is, create handoff, do not start additional work |

If token budget is insufficient to complete all 4 agents + synthesis, inform the user and suggest splitting (e.g., "PO + Architect/Eng Lead this session, Critic + synthesis next session").

---

## Error Handling

**Both modes:**

| Scenario | Action |
|----------|--------|
| Agent returns empty output | Re-spawn once. If still empty, document gap in synthesis. |
| Agent returns truncated output | Accept as-is, note in diagnostics. |
| Agent fails to spawn | Re-spawn once. If still fails, skip role, document. |
| PO fails | STOP — subsequent agents depend on PO. Inform user. |
| Token budget exceeded mid-session | Stop spawning, synthesize from available outputs, note incomplete. |
| Research synthesis not provided | Warn user, proceed with lower quality. |
| User rejects plan draft | Ask what needs to change, re-enter Critical Evaluation Gate. |

**Agent Teams mode only:**

| Scenario | Action |
|----------|--------|
| Teammate appears stuck (no WORK COMPLETE, no task updates) | Send status check via mailbox. Wait for response before any shutdown attempt. |
| Teammate never sends WORK COMPLETE | After status check + 1 follow-up, check if log file was written. If log exists and is non-empty, treat as implicit completion. Document in diagnostics. |
| Peer DM traffic invisible to non-recipients | Mitigated by CC-ALL convention — every peer DM must CC all teammates including the Scrum Lead. Rely on CC-ALL message stream and task list state. |
| One teammate fails, others succeed | Document gap. Do NOT shut down working teammates — let them complete. Synthesize from available outputs. |
| AT env var absent but user requested AT | Notify user, fall back to Task tool mode (Stage 3A). |
| User selects "Switch to Task tool" in AT Confirmation | Execute Stage 3A instead. No AT infrastructure spawned. |

---

## Diagnostic Output (REQUIRED)

**MANDATORY**: You MUST write diagnostic output after every invocation. This is Stage 6 and cannot be skipped.

Write to: `$PROJECT_DIR/logs/diagnostics/plan-creation-{YYYYMMDD-HHMMSS}.yaml`

**Template**: Use `templates/diagnostic-output.yaml` for the schema. Fill in actual values from the session.

---


**Do NOT return to user until all applicable checkboxes can be marked complete.**
