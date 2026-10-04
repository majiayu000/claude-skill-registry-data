---
name: continuous-feedback
description: Identifies improvement targets from accumulated session learnings and proposes concrete skill/agent modifications. General-purpose pipeline for any Claude Code project.
user-invocable: true
argument-hint: "<target-skill-or-path> [--sources <paths>] [--since <session-N>]"
skills:
  - subagent-prompting
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - Skill
  - Task
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Continuous Feedback

Analyzes accumulated session handoffs, memory files, and other learning sources to identify concrete improvement opportunities for skills and agents. Spawns a Collector, 1-3 specialized Analyzers (parallel), and a Proposer — then validates and annotates proposals for user review.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Skill improvement | "What improvements can we make to test-audit?", "Evolve code-review" |
| Session learning harvest | "What have we learned across sessions?", "Harvest learnings" |
| Feedback loop | "Run continuous feedback on X", "Analyze our session learnings" |
| Retrospective | "What patterns have emerged?", "Review accumulated experience" |

**DO NOT use for:**
- Initial topic research (use `bulwark-research`)
- Brainstorming new features (use `bulwark-brainstorm`)
- Code review (use `code-review`)
- Debugging (use `issue-debugging`)

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Collect instructions** | `references/collect-instructions.md` | **REQUIRED** | Include in Collector prompt |
| **Specialization references** | `references/specialize-*.md` | **REQUIRED** | Load matching specializations for Analyzers |
| **Collect output template** | `templates/collect-output.md` | **REQUIRED** | Include in Collector prompt |
| **Proposal output template** | `templates/proposal-output.md` | **REQUIRED** | Include in Proposer prompt |
| **Diagnostic template** | `templates/diagnostic-output.yaml` | **REQUIRED** | Use when writing diagnostics |
| **Subagent prompting** | `subagent-prompting` skill | **REQUIRED** | Load at Stage 0 for 4-part prompt template |

**Fallback behavior:**
- If a specialization reference is missing: Skip that specialization, always run general Analyzer, note in diagnostics
- If output template is missing: Use the schemas from this SKILL.md directly

---

## Usage

```
/continuous-feedback <target-skill-or-path> [--sources <paths>] [--since <session-N>]
```

**Arguments:**
- `<target-skill-or-path>` — Target skill name (e.g., `test-audit`) or path to a skill directory. If a directory containing multiple skills, analyze all detected skill types.
- `--sources <paths>` — Custom input source paths (files or directories). Overrides default input sources.
- `--since <session-N>` — Only collect learnings from session N onwards. Default: last 10 sessions.

**Examples:**
- `/continuous-feedback test-audit` — Analyze learnings for the test-audit skill
- `/continuous-feedback test-audit --since session-50` — Only learnings from session 50 onwards
- `/continuous-feedback skills/code-review/ --sources logs/research/` — Custom input sources
- `/continuous-feedback .claude/skills/` — Analyze all skills in the directory

---

## Stages

### Stage 0: Pre-Flight (Orchestrator)

```
Stage 0: Pre-Flight
├── Parse arguments (target, --sources, --since)
├── Resolve target: skill name → skill directory path
│   ├── Check skills/{name}/ first
│   ├── Then .claude/skills/{name}/
│   └── If raw path provided, use directly
├── Verify Pre-Flight Gate (see below)
├── Resolve input sources (default or custom)
├── Determine specializations: read target's SKILL.md to detect skill type
├── Slugify target for output directory
├── Create output directory: logs/continuous-feedback/{run-slug}/
├── Load subagent-prompting skill
├── Load references/collect-instructions.md
├── Load matching references/specialize-*.md files
├── AskUserQuestion if target is ambiguous or inputs are unclear
└── Token budget check (warn if >30% consumed)
```

#### Pre-Flight Gate

**MANDATORY** — These checks MUST pass before proceeding. Do NOT skip.

| Check | Condition | Failure Action |
|-------|-----------|----------------|
| Session handoff threshold | ≥5 session handoffs exist in the input scope | STOP: "Insufficient input data. Need at least 5 session handoffs. Found {N}." |
| Target path exists | Target path exists and contains readable files | STOP: "Target path does not exist: {path}" |
| Target is identifiable | Can determine what kind of skill/asset the target is | AskUserQuestion: "Could not determine target type. What kind of skill is {target}?" |

#### Default Input Sources

When `--sources` is NOT provided, use these defaults:

1. `sessions/*.md` — Session handoff files (windowed by `--since`, default: last 10)
2. Project MEMORY.md — Always read in full (curated summary, not windowed)
3. `.claude/agent-memory/*/MEMORY.md` — Agent memory files when available

### Stage 1: Collect (Sonnet sub-agent, sequential)

```
Stage 1: Collect
├── Construct prompt using 4-part template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT)
│   ├── GOAL: Parse input sources and extract learning items with source
│   │   attribution and LLM-classified skill_relevance tags
│   ├── CONSTRAINTS:
│   │   ├── Use Grep to locate section headers, Read with offsets for targeted extraction
│   │   ├── Preserve full learning content (pass-through, no lossy compression)
│   │   ├── Assign skill_relevance via LLM classification (NOT keyword matching)
│   │   ├── Each item MUST have: id, source, section, category, skill_relevance, content
│   │   └── Target 1000-2000 words depending on input volume
│   ├── CONTEXT:
│   │   ├── Input file paths (resolved session handoffs, memory files, custom paths)
│   │   ├── Parsing rules from references/collect-instructions.md
│   │   └── Collect output template from templates/collect-output.md
│   └── OUTPUT: logs/continuous-feedback/{run-slug}/01-collect.md
├── Spawn general-purpose Sonnet agent
├── Read Collector output
├── Verify output is non-empty (see Error Handling)
├── Extract skill_types_detected from Collector YAML header
└── Token budget check
```

**Pass-through schema**: The Collector groups and tags learning items but preserves near-raw content. Each item includes:

```yaml
- id: L001
  source: "session_45_20260208.md"
  section: "Learnings"
  category: "defect-pattern"  # defect-pattern | architecture-decision | framework-observation | workflow-improvement | tool-behavior
  skill_relevance: ["test-audit", "code-review"]  # LLM-classified
  content: |
    Full learning text preserved with surrounding context.
    No lossy compression — Analyzers handle interpretation.
```

### Stage 2: Analyze (1-3 Sonnet sub-agents, parallel)

```
Stage 2: Analyze
├── Read Collector output (01-collect.md)
├── Determine Analyzer count from skill_types_detected:
│   ├── If "test-audit" in detected types → load specialize-test-audit.md
│   ├── If "code-review" in detected types → load specialize-code-review.md
│   └── ALWAYS spawn general Analyzer with specialize-general.md
├── For each Analyzer, construct prompt using 4-part template:
│   ├── GOAL: Analyze collected learnings through {specialization} lens and
│   │   identify concrete improvements for the target skill
│   ├── CONSTRAINTS:
│   │   ├── Only analyze items matching your specialization (filtered by skill_relevance)
│   │   ├── General Analyzer: also process items not fully covered by other Analyzers
│   │   ├── Read the target skill's current files to avoid proposing existing content
│   │   ├── For each improvement: what was learned, what it affects, proposed change, priority, evidence
│   │   └── Target 800-1200 words
│   ├── CONTEXT:
│   │   ├── Collector output (01-collect.md)
│   │   ├── Specialization reference (references/specialize-{type}.md)
│   │   └── Target skill path for autonomous exploration
│   └── OUTPUT: logs/continuous-feedback/{run-slug}/02-analyze-{specialization}.md
├── Spawn all Analyzers in parallel (single message, multiple Task calls)
├── Read all Analyzer outputs
└── Token budget check (checkpoint if >55%)
```

**CRITICAL**: Spawn all Analyzers in a single message with N Task tool calls. Do NOT spawn sequentially.

**Dynamic spawning**: The number of Analyzers is data-driven (1-3). If collected learnings only match test-audit and general, only 2 Analyzers spawn. The general Analyzer ALWAYS runs.

### Stage 3: Act/Propose (Sonnet sub-agent, sequential)

```
Stage 3: Act
├── Construct prompt using 4-part template:
│   ├── GOAL: Synthesize all analyses into concrete, copy-paste-ready change
│   │   proposals for the target skill
│   ├── CONSTRAINTS:
│   │   ├── Every proposal MUST have all mandatory fields (see proposal template)
│   │   ├── Proposed content MUST be copy-paste ready — specific enough to apply
│   │   │   without interpretation
│   │   ├── "Improve X" is a FAILURE. "Add the following pattern to {file} under
│   │   │   {section}: [specific content]" is SUCCESS
│   │   ├── Read target skill's current files to avoid stale proposals
│   │   ├── Skip proposals for content that already exists in the target
│   │   ├── Deduplicate across analyses — merge overlapping improvements
│   │   └── Target 1500-2500 words
│   ├── CONTEXT:
│   │   ├── All Analyzer outputs (02-analyze-*.md files)
│   │   ├── Proposal output template from templates/proposal-output.md
│   │   └── Target skill path for autonomous exploration
│   └── OUTPUT: logs/continuous-feedback/{run-slug}/03-proposal.md
├── Spawn general-purpose Sonnet agent
├── Read Proposer output
├── Verify proposals have mandatory fields (see Error Handling)
└── Token budget check
```

**Proposal mandatory fields** (each proposed change):

| Field | Required | Description |
|-------|----------|-------------|
| Target | YES | Exact file path |
| Change type | YES | Add / Modify / Remove |
| Section | YES | Target section within file, or "New section" |
| Priority | YES | High / Medium / Low |
| Source learnings | YES | L-IDs and session/memory references |
| Proposed content | YES | Copy-paste ready text |
| Rationale | YES | Why this improves the skill, traced to learning items |
| Validation | YES | How to verify the change works |

### Stage 4: Validate (Orchestrator, no sub-agent)

```
Stage 4: Validate
├── Read proposal document (03-proposal.md)
├── For each proposed change:
│   ├── If targeting a skill asset (.md in skills/ or .claude/skills/):
│   │   └── Annotate: "Run /anthropic-validator on {target} after applying"
│   ├── If targeting a code file (.ts, .js, .sh, etc.):
│   │   └── Annotate: "Run just typecheck && just lint && just test after applying"
│   └── If targeting configuration:
│       └── Annotate: "Verify configuration is valid and reload"
├── Write validation notes to logs/continuous-feedback/{run-slug}/04-validation.md
└── Present proposals to user with validation annotations
```

**Design note**: Stage 4 does NOT run validators on proposals (proposals are not applied yet). It annotates each proposal with the appropriate validation steps the user should run after applying.

### Stage 5: Diagnostics (REQUIRED)

```
Stage 5: Diagnostics
├── Write diagnostic YAML to logs/diagnostics/continuous-feedback-{YYYYMMDD-HHMMSS}.yaml
│   └── Use templates/diagnostic-output.yaml schema
└── Verify completion checklist
```

---

## Execution Flow (F# Pipeline)

```fsharp
// continuous-feedback pipeline
PreFlight(args, inputs)                    // Stage 0: Orchestrator
|> Collector(sessions, memory, custom)     // Stage 1: Sonnet, sequential
|> [Analyzer(test-audit), Analyzer(code-review), Analyzer(general)]  // Stage 2: Sonnet, parallel (dynamic 1-3)
|> Proposer(all_analyses, target_skills)   // Stage 3: Sonnet, sequential
|> Validate(proposal)                      // Stage 4: Orchestrator, no sub-agent
```

---

## Token Budget Management

| Checkpoint | Threshold | Action |
|------------|-----------|--------|
| After Pre-Flight | >30% consumed | Warn user: "Pipeline agents will consume significant context" |
| After Collector output read | Running tally | If approaching 45%, checkpoint with user |
| After all Analyzers complete | Running tally | If approaching 55%, checkpoint with user |
| After Proposer output read | Must be <65% | Leave room for validation + diagnostics |
| Pipeline complete at >65% | Immediate | Write diagnostics, do not start additional work |

If token budget is insufficient to complete the full pipeline, inform the user and suggest: "Collector + Analyzers this session, Proposer + validation next session."

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Collector returns empty output | Re-spawn once with reinforced extraction instructions. If still empty, STOP — cannot proceed without collected learnings. |
| Collector returns truncated output | Accept as-is, note in diagnostics. |
| Analyzer returns empty output | Re-spawn once. If still empty, skip that specialization, document gap. |
| Proposer returns empty/vague output | Re-spawn once with reinforced specificity instructions. If still vague, document in diagnostics. |
| Proposer proposals missing mandatory fields | Re-spawn once with explicit field checklist. If still incomplete, document in diagnostics. |
| Token budget exceeded mid-pipeline | Stop spawning, write partial results, note incomplete in diagnostics. |
| No learnings match a specialization | Do not spawn that Analyzer. Document in diagnostics. |
| Fewer than 5 session handoffs | Pre-Flight Gate blocks. Inform user. |
| Target path does not exist | Pre-Flight Gate blocks. Inform user. |

---

## Diagnostic Output (REQUIRED)

**MANDATORY**: You MUST write diagnostic output after every invocation. This is Stage 5 and cannot be skipped.

Write to: `logs/diagnostics/continuous-feedback-{YYYYMMDD-HHMMSS}.yaml`

**Template**: Use `templates/diagnostic-output.yaml` for the schema. Fill in actual values from the session.

---

## Completion Checklist

**IMPORTANT**: Before returning to the user, verify ALL items are complete:

- [ ] Stage 0: Pre-Flight Gate passed (≥5 session handoffs, target exists)
- [ ] Stage 0: Arguments parsed (target, --since, --sources)
- [ ] Stage 0: Output directory created at `logs/continuous-feedback/{run-slug}/`
- [ ] Stage 0: subagent-prompting skill loaded
- [ ] Stage 0: AskUserQuestion used if target was ambiguous
- [ ] Stage 1: Collector spawned (Sonnet) and output read
- [ ] Stage 1: Collector output is non-empty with learning items
- [ ] Stage 2: Correct number of Analyzers spawned (1-3, based on detected skill types)
- [ ] Stage 2: All Analyzers spawned in parallel (single message)
- [ ] Stage 2: General Analyzer always included
- [ ] Stage 2: All Analyzer outputs read
- [ ] Stage 3: Proposer spawned (Sonnet) and output read
- [ ] Stage 3: All proposals have mandatory fields (target, change_type, section, proposed_content, rationale, validation)
- [ ] Stage 3: Proposals are copy-paste ready (not vague recommendations)
- [ ] Stage 4: Validation annotations written to `logs/continuous-feedback/{run-slug}/04-validation.md`
- [ ] Stage 4: Proposals presented to user with validation steps
- [ ] Stage 5: Diagnostic YAML written to `logs/diagnostics/`

**Do NOT return to user until all checkboxes can be marked complete.**
