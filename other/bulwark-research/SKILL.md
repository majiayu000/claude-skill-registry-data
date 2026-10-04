---
name: bulwark-research
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Read
  - Skill
  - Task
  - Write
version: 1.0.1
description: Structured multi-viewpoint research using 5 parallel Sonnet sub-agents. Use when deep research is needed on a complex topic before implementation planning.
user-invocable: true
argument-hint: "<topic, filepath, or directory>"
skills:
  - subagent-prompting
author: "Ashay Kubal @ Qball Inc."
---

# Bulwark Research

Structured multi-viewpoint research on a given topic. Spawns 5 Sonnet sub-agents in parallel, each analyzing from a distinct analytical viewpoint, then synthesizes into a single research document.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Deep research | "Research agent teams", "Investigate loop detection" |
| Topic exploration | "What do we know about X?", "Explore approaches to Y" |
| Pre-planning research | "Before we build X, research the landscape" |
| Multi-viewpoint analysis | "Analyze X from multiple angles" |

**DO NOT use for:**
- Evaluating implementation feasibility (use `bulwark-brainstorm`)
- Quick fact lookup (use web search or codebase exploration)
- Code review (use `code-review`)
- Debugging (use `issue-debugging`)

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Viewpoint definitions** | `references/viewpoint-*.md` | **REQUIRED** | Always load all 5 before spawning agents |
| **Output templates** | `templates/viewpoint-output.md` | **REQUIRED** | Include in every agent prompt |
| **Synthesis template** | `templates/synthesis-output.md` | **REQUIRED** | Use when writing synthesis |
| **Subagent prompting** | `subagent-prompting` skill | **REQUIRED** | Load at Stage 1 for 4-part prompt template |

**Fallback behavior:**
- If a viewpoint reference file is missing: Note in diagnostic log, reduce to 4 agents, continue
- If output template is missing: Use the schema from this SKILL.md directly

---

## Usage

```
/bulwark-research <topic-or-prompt> [--context <file>]
/bulwark-research --doc <path-to-document>
```

**Arguments:**
- `<topic-or-prompt>` - Free-text topic description or problem statement
- `--context <file>` - Additional context file to provide to all agents
- `--doc <path>` - Use a document as the topic source instead of free text

**Examples:**
- `/bulwark-research "agent teams and multi-agent orchestration"` - Research a topic
- `/bulwark-research --doc plans/proposal.md` - Research from a document
- `/bulwark-research "loop detection" --context docs/architecture.md` - Research with context

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping. Skipping items violates SC1-SC3 (Skill Compliance Rules in Rules.md).**

This skill uses a 4-stage pipeline with 5 parallel Sonnet sub-agents. You are the orchestrator, NOT the analyst. Follow every item in order. Do NOT return to the user until all applicable items are checked.

- [ ] **Stage 1 — Pre-Flight**: Topic defined, output directories created, subagent-prompting + all 5 viewpoint references loaded
- [ ] **Stage 1 — Pre-Flight**: AskUserQuestion used if topic was ambiguous (2-3 questions per round)
- [ ] **Stage 2 — Agents**: All 5 viewpoint agents spawned in parallel (single message, 5 Task tool calls)
- [ ] **Stage 2 — Agents**: Sub-agents NOT spawned with `run_in_background: true` (SA5)
- [ ] **Stage 2 — Outputs**: All agent outputs written to `$PROJECT_DIR/logs/research/{topic-slug}/`
- [ ] **Stage 3 — Synthesis**: ALL 5 agent outputs read before writing synthesis (MANDATORY — no skipping)
- [ ] **Stage 3 — Synthesis**: Written using `templates/synthesis-output.md` to `$PROJECT_DIR/artifacts/research/{topic-slug}/synthesis.md` (artifact, not log)
- [ ] **Stage 3 — Review**: AskUserQuestion used for post-synthesis review
- [ ] **Stage 3 — Critical Evaluation Gate**: Applied to every user response — classified as Factual / Opinion / Speculative
- [ ] **Stage 3 — Follow-up**: Spawned for Speculative responses (or user declined with caveat added to synthesis)
- [ ] **Stage 4 — Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

---

## Stages

### Stage 1: Pre-Flight

```
Stage 1: Pre-Flight
├── Read problem statement / document
├── AskUserQuestion if ambiguous (iterative, 2-3 questions per round)
├── Slugify topic for output directory
├── Create output directories: $PROJECT_DIR/logs/research/{topic-slug}/ and $PROJECT_DIR/artifacts/research/{topic-slug}/
├── Load subagent-prompting skill
├── Load all 5 references/viewpoint-*.md
├── Load templates/viewpoint-output.md
└── Token budget check (warn if >30% consumed)
```

**AskUserQuestion Protocol (Pre-Spawn):**

If the problem statement is ambiguous, under-specified, or could benefit from scope boundaries:

1. Ask 2-3 clarifying questions using AskUserQuestion
2. Assess whether the answers provide sufficient clarity to construct high-quality prompts
3. If not, ask up to 3 more questions in a follow-up round
4. Repeat until clarity is achieved (no hard cap on rounds, but each round is 2-3 questions max)
5. If the problem statement is clear and well-scoped from the start, skip this step and note in diagnostics: `pre_flight_interview: skipped (problem statement sufficient)`

### Stage 2: Viewpoint Analysis (5 Sonnet, Parallel)

```
Stage 2: Viewpoint Analysis
├── Construct 5 prompts using 4-part template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT)
├── Each prompt includes:
│   ├── Viewpoint definition from references/viewpoint-{name}.md
│   ├── Output template from templates/viewpoint-output.md
│   ├── Topic description + any user-provided context
│   └── Output path: $PROJECT_DIR/logs/research/{topic-slug}/{NN}-{viewpoint-slug}.md
├── Spawn all 5 agents in parallel via Task tool
│   ├── subagent_type: general-purpose
│   ├── model: sonnet
│   └── All 5 in a single message (parallel)
└── Token budget check after all 5 complete (checkpoint if >55%)
```

**CRITICAL**: Spawn all 5 agents in a single message with 5 Task tool calls. Do NOT spawn sequentially.

### Stage 3: Synthesis

```
Stage 3: Synthesis
├── Read ALL 5 agent output files (MANDATORY — do not skip any)
├── If any output is missing or empty → re-spawn that agent once (max 1 retry)
├── If retry fails → document gap in synthesis under "Incomplete Coverage"
├── Load templates/synthesis-output.md
├── Write synthesis to $PROJECT_DIR/artifacts/research/{topic-slug}/synthesis.md
├── AskUserQuestion for user on open questions (iterative, 2-3 per round)
├── Critical Evaluation Gate (see below)
└── Token budget check (must be <65% after synthesis)
```

**Enforcement**: Do NOT begin writing synthesis until ALL available agent outputs have been read. The orchestrator must reference every agent's output at least once in the synthesis.

#### Critical Evaluation Gate (Post-User Q&A)

After each AskUserQuestion round, do NOT blindly incorporate user responses. Instead:

**Step 1 — Classify each user response:**

| Classification | Definition | Action |
|---------------|------------|--------|
| **Factual** | Known, verifiable information (e.g., "We use PostgreSQL") | Incorporate directly into synthesis |
| **Opinion** | Preference or priority (e.g., "I'd prefer approach A") | Incorporate directly with attribution: "User preference: ..." |
| **Speculative** | Unvalidated claim or proposed solution (e.g., "I think library X can do this", "What if we used approach Y?") | **Do NOT incorporate.** Trigger Step 2. |

**Step 2 — For Speculative responses, present to user:**

> "Your suggestion about [X] is unvalidated. I recommend a targeted follow-up research phase with 2 focused agents (Direct Investigation + Contrarian) to verify feasibility and surface risks before incorporating this into the synthesis.
>
> This will spawn 2 Sonnet agents and consume additional token budget.
>
> [Run follow-up research / Incorporate as-is with LOW confidence caveat]"

**Step 3 — If follow-up research approved:**

1. Spawn 2 Sonnet agents in parallel (single message, 2 Task tool calls):
   - **Direct Investigation** — focused on validating the specific claim/solution
   - **Contrarian** — focused on finding failure modes and alternatives for the specific claim/solution
2. Use the same 4-part prompt template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT)
3. Include the REASONING DEPTH instructions from the viewpoint reference docs
4. Output to: `$PROJECT_DIR/logs/research/{topic-slug}/followup-{NN}-direct-investigation.md` and `followup-{NN}-contrarian.md`
5. Read both outputs, then update synthesis with validated findings
6. Tag follow-up findings in synthesis with: `[Follow-up: validated]` or `[Follow-up: refuted]` or `[Follow-up: mixed — see details]`

**Step 4 — If user declines follow-up:**

Incorporate the user's suggestion into synthesis with an explicit caveat:
> **[Unvalidated — user suggestion, not research-backed]**: {suggestion}

**Repeat**: After updating synthesis, ask if user has additional questions or input. Apply the same classification gate to each round. There is no limit on follow-up rounds, but each round with Speculative input that triggers research consumes ~10-15% token budget — warn user if approaching 60%.

### Stage 4: Diagnostics (REQUIRED)

```
Stage 4: Diagnostics
├── Write diagnostic YAML to $PROJECT_DIR/logs/diagnostics/bulwark-research-{YYYYMMDD-HHMMSS}.yaml
└── Verify completion checklist
```

---

## Viewpoints (Sections)

Each viewpoint is a distinct analytical lens. All 5 run in parallel — they do not see each other's output.

### Viewpoint 1: Direct Investigation

**Core Question**: What is this? How does it work? State of the art?

**Focus Areas**:
- Precise definition — what it is and what it is not
- Mechanical operation (architecture, data flow, lifecycle)
- Current state of the art — tooling, adoption, standards
- Key terminology and taxonomy

**Reference**: `references/viewpoint-direct-investigation.md`

### Viewpoint 2: Practitioner Perspective

**Core Question**: How do teams use this in production? What works?

**Focus Areas**:
- Real-world adoption patterns
- Common implementation approaches and trade-offs
- Practical gotchas documentation doesn't cover
- Operational concerns (debugging, monitoring, maintenance)
- Team skill requirements and learning curves

**Reference**: `references/viewpoint-practitioner.md`

### Viewpoint 3: Contrarian Angle

**Core Question**: What failure modes do most people overlook?

**Focus Areas**:
- Failure modes advocates rarely mention
- Scenarios where this is the wrong choice
- Hidden costs (complexity, maintenance burden, cognitive load)
- Alternatives that might be simpler
- When NOT to use this

**Reference**: `references/viewpoint-contrarian.md`

### Viewpoint 4: First Principles

**Core Question**: What core problem does this solve? Minimal viable version?

**Focus Areas**:
- Fundamental problem being addressed (stripped of buzzwords)
- Why existing approaches are insufficient
- Minimal set of capabilities for value
- Essential vs. deferrable
- Decomposition into independent sub-problems

**Reference**: `references/viewpoint-first-principles.md`

### Viewpoint 5: Prior Art / Historical

**Core Question**: What similar patterns exist? Lessons from predecessors?

**Focus Areas**:
- Historical predecessors and analogous patterns
- Evolution trajectories — what succeeded, what failed, why
- Hype vs. foundational patterns
- Lessons applicable to current topic

**Reference**: `references/viewpoint-prior-art.md`

---

## Token Budget Management

| Checkpoint | Threshold | Action |
|------------|-----------|--------|
| After constructing all prompts | >30% consumed | Warn user: "5 agents will consume significant context" |
| After reading 3 of 5 outputs | Running tally | If approaching 55%, checkpoint with user |
| After synthesis | Must be <65% | Leave room for session closing |
| Synthesis complete at >65% | Immediate | Create handoff, do not start additional work |

If token budget is insufficient to complete all 5 agents + synthesis, inform the user and suggest splitting (e.g., "3 agents this session, 2 + synthesis next session").

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Agent returns empty output | Re-spawn once. If still empty, document gap in synthesis. |
| Agent returns truncated output | Accept as-is, note in diagnostics. |
| Agent fails to spawn | Re-spawn once. If still fails, reduce to 4 agents, document. |
| Token budget exceeded mid-session | Stop spawning, synthesize from available outputs, note incomplete. |
| User-provided document unreadable | AskUserQuestion for alternative source. |

---

## Diagnostic Output (REQUIRED)

**MANDATORY**: You MUST write diagnostic output after every invocation. This is Stage 4 and cannot be skipped.

Write to: `$PROJECT_DIR/logs/diagnostics/bulwark-research-{YYYYMMDD-HHMMSS}.yaml`

**Template**: Use `templates/diagnostic-output.yaml` for the schema. Fill in actual values from the session.
