---
name: cm-how-it-work
description: "Complete guide to vibe coding with CodyMaster — from idea to deploy. Read this first if you are new."
disable-model-invocation: true
---

# CodyMaster Kit — The Ultimate Vibe Coding Guide

## Overview

The **CodyMaster (CM)** kit transforms ideas into production code through 13 specialized, optimized skills. This workflow ensures the highest quality, absolute security, and maximum execution speed.

```
💡 Idea → 🔍 Analysis → 📐 Design → 🧪 Test-first (TDD) → 💻 Code → ✅ Verify → 🚀 Deploy → 🔄 Iterate
```

---

## Workflow

### Phase 0: Identity & Safety 🔒
> **Rule #1:** Always verify identity before performing any action that could change the project state.

- **Skill:** `cm-identity-guard`
- **When:** At the start of a work session, before git push, deploy, or database operations.
- **Action:** Run `node check-identity.js` (or similar script) to verify GitHub/Cloudflare/Supabase accounts.

---

### Phase 0.3: Knowledge Infrastructure Setup 🧠
> **For large codebases, establish the memory foundation before planning.**

- **Skills:** `cm-codeintell` + `cm-dockit` + `cm-deep-search` + `cm-notebooklm`
- **When:** When onboarding to a new codebase or starting a massive refactoring initiative.
- **Action:**
    1. Scan structure with `cm-codeintell` to build the Skeleton Index.
    2. Generate missing architectural docs with `cm-dockit`.
    3. Index the docs for fast local retrieval with `cm-deep-search` (qmd).
    4. Sync high-value patterns to the Cloud Brain with `cm-notebooklm`.
- **Output:** A fully indexed 5-tier memory ecosystem ready for precise, low-token AI problem solving.

---

### Phase 0.5: Strategic Analysis 🔍
> **For complex initiatives and enhancements on existing products.**

- **Skills:** `cm-brainstorm-idea` + `cm-codeintell`
- **When:** When the task is complex and requires multi-dimensional analysis (tech, product, design, business) before planning.
- **Action:**
    1. Scan codebase with **code intelligence** (AST graph + architecture diagram via `cm-codeintell`).
    2. Interview user and analyze with 9 Windows (TRIZ).
    3. Propose 2-3 options, evaluate multi-dimensionally, recommend the best option.
- **Output:** OpenSpec `openspec/changes/[initiative]/proposal.md` — qualified problem + recommended option → passes to `cm-planning`.

---

### Phase 1: Planning & Design 📐
> **Understand the 'Job to be Done' (JTBD) and architecture before writing code.**

- **Skill:** `cm-planning` (Combines brainstorming + writing-plans)
- **Action:**
    1. Brainstorm requirements and analyze i18n.
    2. Propose architecture and tech stack.
    3. Write detailed OpenSpec docs (`openspec/changes/[init]/design.md` and `tasks.md`).
- **Output:** Design docs and execution plan (OpenSpec tasks) approved by user.

---

### Phase 2: Implementation (TDD & Execution) 💻
> **Turn the plan into actual source code safely.**

- **Skills:**
    - `cm-tdd`: Red-Green-Refactor cycle. No production code without a failing test first.
    - `cm-execution`: Execute plans intelligently (Manual, Parallel, or Subagent mode).
    - `cm-project-bootstrap`: For new projects — setup repo, i18n, SEO, and deploy pipeline from Day 0.
    - `cm-execution`: Isolate different work items to avoid state mixing.

---

### Phase 3: Quality Control & Verification ✅
> **Prove with evidence, not words.**

- **Skills:**
    - `cm-quality-gate`: Setup test infrastructure (`test:gate`) and verify output before claiming "done".
    - `cm-debugging`: When tests fail, use systematic investigation framework to find root cause.
    - `cm-code-review`: Professional request and feedback review process.

---

### Phase 4: Safe Deployment 🚀
> **Ship code without fear of incidents.**

- **Skills:**
    - `cm-safe-deploy`: Run 8-gate pipeline (Secret → Syntax → Test → Build → Deploy → Smoke).
    - `cm-safe-i18n`: Translate and synchronize languages consistently across the entire project.
    - `cm-terminal`: Monitor all terminal commands to detect errors immediately.

---

## CodyMaster Kit — 34 Skills Summary

### 🔧 Engineering
| Skill | Primary Function |
|-------|-----------------|
| `cm-tdd` | Strict Red-Green-Refactor TDD — no code without failing test first. |
| `cm-debugging` | Systematic 5-phase error investigation (root cause first). |
| `cm-quality-gate` | 6-gate verification: static analysis → blind review → ship. |
| `cm-quality-gate` | Setup and enforce the verification gate before claiming "done". |
| `cm-code-review` | Manage PR lifecycle: request → receive feedback → complete branch. |
| `cm-codeintell` | AST knowledge graph + architecture diagrams + smart context (30% fewer tokens). |

### ⚙️ Operations
| Skill | Primary Function |
|-------|-----------------|
| `cm-safe-deploy` | Multi-gate deploy pipeline with rollback strategy. |
| `cm-identity-guard` | Verify account before push/deploy to prevent wrong-project incidents. |
| `cm-execution` | Isolate feature work in separate workspaces/batches — no state mixing. |
| `cm-terminal` | Safe terminal execution with progress logging and error capture. |
| `cm-safe-deploy` | Defense-in-depth: pre-commit hooks, repo scanning, token lifecycle. |
| `cm-safe-i18n` | Safe multi-language management with multi-pass batching and 8-gate audit. |

### 🎨 Product
| Skill | Primary Function |
|-------|-----------------|
| `cm-project-bootstrap` | Full project setup: design system → CI → staging → deploy from Day 0. |
| `cm-brainstorm-idea` | Strategic analysis gate: 9 Windows + Double Diamond → 2-3 qualified options. |
| `cm-planning` | Brainstorm intent → write implementation plan → coordinate execution. |
| `cm-ux-master` | 48 UX Laws + 37 Design Tests + Figma/Stitch + BM25 semantic design search. |
| `cm-design-system` | Live UI concept generation via design-token and Stitch/Open Design workflows. |
| `cm-dockit` | Generate complete knowledge bases, SOPs, and API docs from codebase. |
| `cm-readit` | Web audio engine: TTS reader, MP3 audio player, Voice CRO trigger system. |
| `cm-jtbd` | JTBD customer discovery: Switch Interview → Canvas → Opportunity Scoring. |

### 📈 Growth
| Skill | Primary Function |
|-------|-----------------|
| `cm-content-factory` | Self-learning content engine: research → generate → audit → deploy. |
| `cm-ads-tracker` | Conversion tracking setup: GTM, Meta CAPI, TikTok, Google Ads. |
| `cm-cro-methodology` | CRO audit: funnel mapping → persuasion assets → A/B test design. |

### 🎯 Orchestration
| Skill | Primary Function |
|-------|-----------------|
| `cm-execution` | Execute plans: Manual / Parallel / Subagent / RARV batch modes. |
| `cm-continuity` | Working memory protocol: read at session start, update at session end. |
| `cm-skill-index` | Meta-skill: when to invoke which skill and how to discover the right one. |
| `cm-skill-chain` | Compose skills into automated multi-step pipelines (5 built-in chains). |
| `cm-skill-index` | Progressive disclosure index — 90% token savings on skill discovery. |
| `cm-deep-search` | Semantic search via qmd for large codebases (>200 src / >50 docs files). |
| `cm-notebooklm` | Cloud Brain sync — cross-machine knowledge persistence via NotebookLM. |
| `cm-how-it-work` | Full vibe coding guide — phases, skills per phase, use cases. |

### 🖥️ Workflow Commands
| Skill | Primary Function |
|-------|-----------------|
| `cm-start` | Orchestrate full workflow from objective to production code. |
| `cm-status` | Ultra-concise 1-2 sentence progress summary; pair with `cm dashboard` for visuals. |

## 🚀 Autonomous Workflow System

The kit supports autonomous mode by applying the **Reason → Act → Reflect → Verify (RARV)** loop.

### How to Use the Workflow:
1. **`/cm-start [objective]`**: Start work. The system will automatically initialize the OpenSpec structure (`openspec/changes/[objective]/`), break down tasks into `tasks.md` and sync with `cm-tasks.json`, launch the tracking interface, and autonomously use CM skills to complete them.
2. **`/cm-dashboard`**: Open the visual tracking Dashboard in browser (shows Kanban board, reasoning log, and progress).
3. **`/cm-status`**: View quick progress summary in Terminal.

---

## 💡 Activation Guide by Use Cases

There are 2 ways to use CodyMaster: **Fully autonomous (Via Workflows)** or **Manual skill activation (Via Prompting)**.

### 1. Build New Feature / New Project (Autonomous)
> Best way to delegate complete work packages.
- **Command:** `/cm-start "Build user management feature with list screen and CRUD form"`
- **Implicit flow:** Planning → create Task JSON → sub-agents continuously run `cm-tdd` and `cm-quality-gate` for each task until done.

### 2. Fix Production Bug (Manual)
> Bugs need close supervision and AI should not blindly change too much code.
- **Step 1:** Activate `cm-debugging` to find Root Cause.
- **Step 2:** Activate `cm-tdd` to write test reproducing the bug and fix it.
- **Step 3:** Activate `cm-safe-deploy` to ship code safely.

### 3. Setup New Project From Scratch
> Establish a solid foundation to avoid technical debt later.
- **Command:** "Use `cm-identity-guard` to ensure correct account, then run `cm-project-bootstrap` to setup a new Next.js project."

### 4. Batch Multi-Language Translation
> Tedious work that's error-prone if AI loses focus.
- **Command:** "Use `cm-safe-i18n` to extract all hardcoded text in `/components` directory to `vi.json` and `en.json` files."

---

## 9 Golden Rules

1. **Identity First:** Verify account (`cm-identity-guard`) before push/deploy.
2. **Design Before Code:** Always have an approved plan before typing.
3. **i18n Day 0:** Always consider multi-language from the brainstorm step.
4. **Test Before Code:** RED → GREEN → REFACTOR. No exceptions (`cm-tdd`).
5. **Evidence Over Claims:** Only trust terminal/test results output, not AI "saying" it's done.
6. **Deploy via Gates:** 8 gates must pass sequentially. Any gate fails = STOP (`cm-safe-deploy`).
7. **Safe Secrets:** Never commit secrets. Pre-commit hooks protect every push (`cm-safe-deploy`).
8. **Parallel Power:** Use parallel execution for i18n or multi-bug fixes (`cm-execution`).
9. **Working Memory:** Read CONTINUITY.md at session start, update at session end (`cm-continuity`).
