---
name: product-ideation
description: Evaluates product ideas through a six-agent research pipeline producing BUY/HOLD/SELL recommendations backed by market analysis, competitive intelligence, and segment targeting. Use when assessing product viability, researching markets for new ideas, or deciding whether to pursue a product concept.
user-invocable: true
argument-hint: "<idea-description> | --doc <path-to-idea-file>"
skills:
  - subagent-prompting
allowed-tools:
  - AskUserQuestion
  - Read
  - Skill
  - Task
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Product Ideation

Evaluates a product idea through a structured six-agent research pipeline and delivers a BUY/HOLD/SELL recommendation. The orchestrator interviews the user to clarify the idea, then spawns dedicated sub-agents for validation, market research, competitive analysis, pattern documentation, segment analysis, and final strategy. All analysis is grounded in web research and structured frameworks.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|----------------------|
| Idea evaluation | "Is this product idea worth pursuing?", "Evaluate my idea: X" |
| Market analysis | "Research the market for X", "Should I build X?" |
| Investment-style assessment | "Give me a BUY/HOLD/SELL on this idea", "Validate my product concept" |
| Pre-build research | "Before I start building X, help me understand the landscape" |

**DO NOT use for:**
- Evaluating existing live products or companies (use a financial analysis skill instead)
- Technical architecture decisions for an already-committed product (the idea stage has passed)
- Competitive analysis in isolation without a product idea as the anchor

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Analysis frameworks** | `references/analysis-frameworks.md` | **REQUIRED** | Include in sub-agent prompts at Stage 1+ |
| **Final report template** | `templates/final-report.md` | **REQUIRED** | Include in strategist sub-agent prompt |
| **Diagnostics schema** | `templates/diagnostic-output.yaml` | **REQUIRED** | Write at pipeline completion |
| **Prompting** | `subagent-prompting` skill | **REQUIRED** | Load before spawning any sub-agent |
| **Idea validator** | `.claude/agents/product-ideation-idea-validator.md` | **REQUIRED** | Spawned at Stage 1 (parallel) |
| **Market researcher** | `.claude/agents/product-ideation-market-researcher.md` | **REQUIRED** | Spawned at Stage 1 (parallel) |
| **Competitive analyzer** | `.claude/agents/product-ideation-competitive-analyzer.md` | **REQUIRED** | Spawned at Stage 2 (sequential) |
| **Pattern documenter** | `.claude/agents/product-ideation-pattern-documenter.md` | **REQUIRED** | Spawned at Stage 3 (parallel) |
| **Segment analyzer** | `.claude/agents/product-ideation-segment-analyzer.md` | **REQUIRED** | Spawned at Stage 3 (parallel) |
| **Strategist** | `.claude/agents/product-ideation-strategist.md` | **REQUIRED** | Spawned at Stage 4 (sequential) |

---

## Usage

```
/product-ideation <idea-description>
/product-ideation --doc <path-to-idea-file>
```

**Arguments:**
- `<idea-description>` — Free-text description of the product idea
- `--doc <path>` — Path to a file containing the idea description

**Examples:**
- `/product-ideation a mobile app that lets freelancers track client payments with automated invoice reminders`
- `/product-ideation --doc plans/ideas/saas-invoicing-tool.md`

---

## Pre-Flight Gate (BLOCKING)

**STOP. Before ANY work, you MUST acknowledge what this skill requires.**

This skill uses a **six-agent pipeline with parallel and sequential stages**. You are the orchestrator. You coordinate, read outputs, and spawn agents — you do NOT perform their analysis yourself.

### What You MUST Do

1. Parse input and conduct a focused interview (Stage 0) — at most 2 AskUserQuestion rounds
2. Read `references/analysis-frameworks.md` and `templates/final-report.md` before spawning agents
3. Spawn Stage 1 agents (idea-validator AND market-researcher) in the same message as parallel Tasks
4. Wait for both Stage 1 agents to complete before spawning Stage 2
5. Spawn Stage 3 agents (pattern-documenter AND segment-analyzer) in the same message as parallel Tasks
6. Wait for all prior outputs before spawning the strategist
7. Read the final strategy report from `$PROJECT_DIR/logs/` and present its contents to the user
8. Write diagnostic YAML at completion

### What You MUST NOT Do

- Do NOT perform market research, validation, or competitive analysis yourself — spawn the agents
- Do NOT skip the interview — the idea must be clear before spawning agents
- Do NOT spawn agents with `run_in_background: true`
- Do NOT proceed past Stage 1 without confirming both parallel agents completed
- Do NOT return to user before the strategist has written its output to `$PROJECT_DIR/logs/`

**Anti-thought traps:**
- "I already know this market, I can skip the research agents" — STOP. Spawn the agents.
- "The idea is simple, I don't need to interview" — STOP. Conduct at least one AskUserQuestion round.
- "I can summarize the recommendation without reading the strategist output" — STOP. Read the log file.

---

## Pipeline

```fsharp
// product-ideation pipeline
Stage0_Interview(args)
|> [Stage1_IdeaValidator(idea),         // product-ideation-idea-validator — feasibility + timing
    Stage1_MarketResearcher(idea)]       // product-ideation-market-researcher — market size + trends
|> Stage2_CompetitiveAnalyzer(market_research_output)  // product-ideation-competitive-analyzer
|> [Stage3_PatternDocumenter(competitive_output),       // product-ideation-pattern-documenter
    Stage3_SegmentAnalyzer(competitive_output)]         // product-ideation-segment-analyzer
|> Stage4_Strategist(all_outputs)       // product-ideation-strategist — BUY/HOLD/SELL
|> Stage5_Diagnostics(pipeline_results)
```

---

## Stage Definitions

### Stage 0: Interview (Orchestrator)

```
Stage 0: Interview
├── Parse arguments:
│   ├── If --doc <path>: Read the file, extract idea description
│   └── If free-text: Use as idea description directly
├── Load references/analysis-frameworks.md
├── Load templates/final-report.md
├── AskUserQuestion (Round 1 — REQUIRED):
│   ├── Q1: What problem does this product solve, and for whom?
│   ├── Q2: What is your rough idea of the business model (subscription, one-time, marketplace, etc.)?
│   ├── Q3: Are there any specific markets or geographies to focus on?
│   └── Q4: Do you have any known competitors in mind, or is this a blank slate?
├── If answers are ambiguous or incomplete:
│   └── AskUserQuestion (Round 2 — CONDITIONAL, max 1 additional round):
│       └── Ask 1-2 targeted follow-ups based on gaps in Round 1 answers
├── Synthesize: Combine original idea + interview answers into a complete idea brief
└── Token budget check (warn if >20% consumed before agents start)
```

**Interview behavior**: Maximum 2 AskUserQuestion rounds. Present all Round 1 questions together. Do NOT ask questions one at a time.

### Stage 1: Parallel Batch 1 — Idea Validator + Market Researcher

Spawn both agents in the same message. Do NOT wait for one before spawning the other.

**Idea Validator prompt structure:**

```
GOAL: Assess whether the product idea has sufficient merit to warrant deep market research.
Evaluate technical feasibility, market timing, problem-solution fit, and uniqueness.

CONSTRAINTS:
- Use WebSearch to check for prior art and existing solutions
- Produce a clear PASS/CONDITIONAL/FAIL verdict with reasoning
- Write output to $PROJECT_DIR/logs/product-ideation-idea-validation-{YYYYMMDD-HHMMSS}.md
- Do not exceed 500 words in the main report

CONTEXT:
Idea brief: {synthesized idea brief from Stage 0}
Frameworks reference: {path to references/analysis-frameworks.md}

OUTPUT:
Write report to $PROJECT_DIR/logs/product-ideation-idea-validation-{YYYYMMDD-HHMMSS}.md
Return summary to orchestrator: verdict, top 3 strengths, top 3 concerns, report path
```

Spawn: `Task(subagent_type="product-ideation-idea-validator", prompt=...)`

**Market Researcher prompt structure:**

```
GOAL: Research the market landscape for this product idea. Produce an evidence-based
assessment of market size, growth trajectory, key players, regulatory context, and
technology trends. Ground all claims in web research.

CONSTRAINTS:
- Use WebSearch and WebFetch extensively — minimum 5 distinct sources
- Quantify market size where possible (TAM, growth rate, CAGR)
- Note recency of data — prefer sources from 2023 or later
- Write output to $PROJECT_DIR/logs/product-ideation-market-research-{YYYYMMDD-HHMMSS}.md

CONTEXT:
Idea brief: {synthesized idea brief from Stage 0}
Frameworks reference: {path to references/analysis-frameworks.md} — use PESTLE and TAM/SAM/SOM

OUTPUT:
Write report to $PROJECT_DIR/logs/product-ideation-market-research-{YYYYMMDD-HHMMSS}.md
Return summary to orchestrator: market size estimate, growth trend, top 3 key players, report path
```

Spawn: `Task(subagent_type="product-ideation-market-researcher", prompt=...)`

After both agents return: verify both log files exist. If either is missing, re-spawn that agent once.

### Stage 2: Sequential — Competitive Analyzer

Read the market research log file path from Stage 1 output before constructing this prompt.

```
GOAL: Perform competitive intelligence analysis. Identify direct competitors, indirect
competitors, and failed competitors. Assess their positioning, pricing, strengths,
weaknesses, and the reasons for failure in failed cases.

CONSTRAINTS:
- Read market research output from: {market_research_log_path}
- Use WebSearch to discover competitors not mentioned in market research
- Include at least 3 direct competitors and 2 failed competitors
- Write output to $PROJECT_DIR/logs/product-ideation-competitive-analysis-{YYYYMMDD-HHMMSS}.md

CONTEXT:
Idea brief: {synthesized idea brief from Stage 0}
Market research: {market_research_log_path}
Frameworks reference: {path to references/analysis-frameworks.md} — use Porter's Five Forces

OUTPUT:
Write report to $PROJECT_DIR/logs/product-ideation-competitive-analysis-{YYYYMMDD-HHMMSS}.md
Return summary to orchestrator: top 3 competitors, market gap identified (yes/no), report path
```

Spawn: `Task(subagent_type="product-ideation-competitive-analyzer", prompt=...)`

### Stage 3: Parallel Batch 2 — Pattern Documenter + Segment Analyzer

Read the competitive analysis log file path from Stage 2 output before spawning. Spawn both agents in the same message.

**Pattern Documenter prompt structure:**

```
GOAL: Document success patterns and failure patterns from the competitive landscape.
Produce competitor profiles, identify opportunity gaps, and extract repeatable lessons.

CONSTRAINTS:
- Read competitive analysis from: {competitive_analysis_log_path}
- May use WebSearch to deepen understanding of specific competitor trajectories
- Document at least 3 success patterns and 3 failure patterns
- Write output to $PROJECT_DIR/logs/product-ideation-patterns-{YYYYMMDD-HHMMSS}.md

CONTEXT:
Idea brief: {synthesized idea brief from Stage 0}
Competitive analysis: {competitive_analysis_log_path}
Frameworks reference: {path to references/analysis-frameworks.md}

OUTPUT:
Write report to $PROJECT_DIR/logs/product-ideation-patterns-{YYYYMMDD-HHMMSS}.md
Return summary to orchestrator: top success pattern, top failure risk, biggest opportunity gap, report path
```

Spawn: `Task(subagent_type="product-ideation-pattern-documenter", prompt=...)`

**Segment Analyzer prompt structure:**

```
GOAL: Identify and profile target user segments for this product idea. Determine who
will buy it, why, at what price, and in what volume. Produce TAM/SAM/SOM estimates
and at least 2 detailed user personas.

CONSTRAINTS:
- Read competitive analysis from: {competitive_analysis_log_path}
- Use WebSearch to validate segment size claims
- Produce at least 2 distinct user personas with willingness-to-pay estimates
- Write output to $PROJECT_DIR/logs/product-ideation-segments-{YYYYMMDD-HHMMSS}.md

CONTEXT:
Idea brief: {synthesized idea brief from Stage 0}
Competitive analysis: {competitive_analysis_log_path}
Frameworks reference: {path to references/analysis-frameworks.md} — use Jobs-to-be-Done + TAM/SAM/SOM

OUTPUT:
Write report to $PROJECT_DIR/logs/product-ideation-segments-{YYYYMMDD-HHMMSS}.md
Return summary to orchestrator: primary segment, estimated TAM, top persona name, report path
```

Spawn: `Task(subagent_type="product-ideation-segment-analyzer", prompt=...)`

After both agents return: verify both log files exist.

### Stage 4: Sequential — Strategist

Read all four prior log file paths before constructing this prompt.

```
GOAL: Synthesize all research outputs into a definitive BUY/HOLD/SELL recommendation.
Produce the final report using the provided template. Support the recommendation with
confidence level, strategic rationale, risk factors, and next steps.

CONSTRAINTS:
- Read ALL of the following before writing:
    {idea_validation_log_path}
    {market_research_log_path}
    {competitive_analysis_log_path}
    {patterns_log_path}
    {segments_log_path}
- Use the final-report template at: {path to templates/final-report.md}
- Recommendation MUST be exactly one of: BUY, HOLD, or SELL
- Confidence MUST be exactly one of: High, Medium, or Low
- Write output to $PROJECT_DIR/logs/product-ideation-strategy-{YYYYMMDD-HHMMSS}.md

CONTEXT:
Idea brief: {synthesized idea brief from Stage 0}
All prior outputs: see CONSTRAINTS for paths
BUY/HOLD/SELL criteria: {path to references/analysis-frameworks.md} — see Recommendation Thresholds section
Final report template: {path to templates/final-report.md}

OUTPUT:
Write final report to $PROJECT_DIR/logs/product-ideation-strategy-{YYYYMMDD-HHMMSS}.md
Return summary to orchestrator: recommendation, confidence level, one-sentence rationale, report path
```

Spawn: `Task(subagent_type="product-ideation-strategist", prompt=...)`

After agent returns: read the full strategy report from the log path. Present its contents to the user verbatim (do not summarize — this is the deliverable).

### Stage 5: Diagnostics (REQUIRED)

**MANDATORY**: Write diagnostic YAML after every invocation. Cannot be skipped.

```
Write to: $PROJECT_DIR/logs/diagnostics/product-ideation-{YYYYMMDD-HHMMSS}.yaml
Use schema from: templates/diagnostic-output.yaml

Include:
- Input type and value
- Interview rounds conducted
- Each pipeline stage: success | failed | skipped
- Final recommendation and confidence
- All log file paths
- Outcome: success | partial | failure
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Agent returns empty output | Re-spawn once with reinforced instructions. If still empty, mark stage as failed in diagnostics, skip to next stage. |
| Idea validation returns FAIL | Present the FAIL verdict to user. AskUserQuestion: "The idea validator flagged significant concerns. Proceed anyway, or refine the idea?" |
| Market researcher finds no data | Note data gap in final report. Strategist must lower confidence to Low if market size cannot be estimated. |
| Both Stage 1 agents fail | STOP. Inform user: "Research pipeline failed at Stage 1. Please retry with a more specific idea description." |
| Log file missing after agent completes | Glob for similar filenames in `$PROJECT_DIR/logs/`. If found, use it. If not, re-spawn agent. |
| Token budget >60% at Stage 3 | Warn user. Spawn agents sequentially instead of in parallel to conserve context. |
| Token budget >80% at any point | Stop at current stage. Present partial output with explanation. Write diagnostics noting partial completion. |

---

## Token Budget Management

| Checkpoint | Threshold | Action |
|------------|-----------|--------|
| After Stage 0 interview | >20% consumed | Warn: "Significant context used in interview. Pipeline will consume more." |
| After Stage 1 (parallel) | >45% consumed | Warn: "Approaching mid-budget. Consider running Stage 3 sequentially." |
| After Stage 2 | >60% consumed | Warn: "Context budget constrained. Spawning Stage 3 sequentially." |
| After Stage 3 | >75% consumed | Warn: "Low budget. Strategist prompt will be minimal." |

---

## Completion Checklist

**IMPORTANT**: Before returning to user, verify ALL items are complete:

- [ ] Stage 0: Arguments parsed (description or --doc)
- [ ] Stage 0: references/analysis-frameworks.md loaded
- [ ] Stage 0: templates/final-report.md loaded
- [ ] Stage 0: AskUserQuestion interview conducted (1-2 rounds)
- [ ] Stage 0: Synthesized idea brief produced
- [ ] Stage 1: idea-validator spawned and output verified in `$PROJECT_DIR/logs/`
- [ ] Stage 1: market-researcher spawned and output verified in `$PROJECT_DIR/logs/`
- [ ] Stage 2: competitive-analyzer spawned and output verified in `$PROJECT_DIR/logs/`
- [ ] Stage 3: pattern-documenter spawned and output verified in `$PROJECT_DIR/logs/`
- [ ] Stage 3: segment-analyzer spawned and output verified in `$PROJECT_DIR/logs/`
- [ ] Stage 4: strategist spawned and output verified in `$PROJECT_DIR/logs/`
- [ ] Stage 4: Final report contents read from `$PROJECT_DIR/logs/` and presented to user
- [ ] Stage 5: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`
