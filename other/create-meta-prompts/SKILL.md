---
name: create-meta-prompts
description: "Creates optimized prompts for Claude-to-Claude pipelines with research, planning, and execution stages. Activates when building prompts that produce outputs for other prompts to consume, or running multi-stage workflows (research → plan → implement). Triggers on: meta-prompt, prompt chain, Claude pipeline, multi-stage workflow, Do/Plan/Research/Refine prompt, prompt orchestration, chained prompts, prompt dependency, sequential prompts. Does NOT activate for single one-shot prompts — use the relevant task skill directly instead."
metadata:
  version: "1.0.0"
allowed-tools: "Read, Write, Bash"
---

# Create Meta-Prompts

Builds structured prompts for multi-stage Claude-to-Claude workflows. Every
execution produces a `SUMMARY.md` for human scanning. Each prompt gets its own
folder in `.prompts/` with clear provenance and chain detection.

---

## Workflow (7 Steps)

1. **Intake** — Determine purpose (Do/Plan/Research/Refine), gather requirements
2. **Chain detection** — Check `.prompts/*/` for existing research/plan files to reference
3. **Generate** — Create prompt using purpose-specific patterns
4. **Save** — Create folder in `.prompts/{number}-{topic}-{purpose}/`
5. **Present** — Show decision tree for running
6. **Execute** — Run prompt(s) with dependency-aware execution engine
7. **Summarize** — Create `SUMMARY.md` for human scanning

---

## Folder Structure

```
.prompts/
├── 001-auth-research/
│   ├── completed/001-auth-research.md   ← archived after run
│   ├── auth-research.md                 ← full output (XML for Claude)
│   └── SUMMARY.md                       ← executive summary (human-readable)
├── 002-auth-plan/
│   ├── completed/002-auth-plan.md
│   ├── auth-plan.md
│   └── SUMMARY.md
└── 003-auth-implement/
    ├── completed/003-auth-implement.md
    └── SUMMARY.md
```

---

## Purpose Routing

| Purpose | Load pattern file | Use when |
|---|---|---|
| **Do** | `references/do-patterns.md` | Build/implement/fix/create |
| **Plan** | `references/plan-patterns.md` | Roadmap/approach/strategy |
| **Research** | `references/research-patterns.md` | Gather/analyze/explore |
| **Refine** | `references/refine-patterns.md` | Improve existing output |

---

## Intake

See `references/intake-gate.md` for the full intake flow.
Questions by purpose: `references/question-bank.md`.

---

## Prompt Structure (All Outputs)

Every generated prompt includes:
1. **Objective** — What to accomplish, why it matters
2. **Context** — Referenced files (`@`), dynamic context (`!`)
3. **Requirements** — Specific instructions
4. **Output specification** — Where to save, what structure
5. **Metadata** (research/plan only) — `<confidence>`, `<dependencies>`, `<open_questions>`, `<assumptions>`
6. **SUMMARY.md requirement** — Mandatory in every prompt
7. **Success criteria**

---

## Execution Engine

See `references/execution-engine.md` for full details on:
- Single / Sequential / Parallel / Mixed-DAG execution modes
- Dependency detection from `@` references
- Output validation rules
- Failure handling and recovery options
- Archiving behavior
- Result presentation format

---

## Reference Index

| File | Purpose |
|---|---|
| `references/intake-gate.md` | Intake flow, purpose detection, chain detection |
| `references/execution-engine.md` | Full execution engine specification |
| `references/do-patterns.md` | Do prompt patterns |
| `references/plan-patterns.md` | Plan prompt patterns |
| `references/research-patterns.md` | Research prompt patterns |
| `references/refine-patterns.md` | Refine/iteration patterns |
| `references/summary-template.md` | SUMMARY.md structure |
| `references/metadata-guidelines.md` | Confidence/dependencies/assumptions fields |
| `references/question-bank.md` | Intake questions by purpose |
| `references/intelligence-rules.md` | Extended thinking, parallel tools, depth |

---

## Success Criteria

**Prompt creation:** Intake complete → chain detection done → prompt generated with correct structure → folder created → SUMMARY.md requirement included → decision tree presented.

**Execution:** Dependencies detected and ordered → prompts run in correct mode → output validated → SUMMARY.md displayed inline → failed prompts handled with recovery options → successful prompts archived.
