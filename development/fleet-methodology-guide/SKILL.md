---
name: fleet-methodology-guide
description: Stage awareness — what's expected at each methodology stage, what to do, what NOT to do, which tools and skills are available
user-invocable: false
---

# Fleet Methodology Guide

## Your Current Stage

Your stage is determined by `task_readiness` in your task context:
- **conversation** (0-20%) — understand requirements with PO
- **analysis** (20-50%) — examine what exists in the codebase
- **investigation** (50-80%) — research options, explore approaches
- **reasoning** (80-99%) — plan approach, reference verbatim requirement
- **work** (99-100%) — execute the confirmed plan

Source of truth: `config/methodology.yaml`

## Stage Quick Reference

### conversation (readiness 0-20%)
**Job:** UNDERSTAND, not BUILD.

| DO | DON'T |
|----|-------|
| Ask specific questions about unclear requirements | Write code |
| Propose your understanding, accept correction | Commit changes |
| Extract knowledge from PO | Create PRs |
| Post draft proposals for PO review | Produce finished deliverables |

**Tools available:** fleet_read_context, fleet_chat, fleet_task_progress, fleet_artifact_create (drafts only)
**Tools BLOCKED:** fleet_commit, fleet_task_complete, fleet_task_accept
**Skills to use:** /brainstorming (mandatory before creative work), fleet-communicate

**Advance when:** PO confirms understanding. Readiness increases. Verbatim requirement populated. No open questions.

---

### analysis (readiness 20-50%)
**Job:** UNDERSTAND WHAT EXISTS, not solve the problem.

| DO | DON'T |
|----|-------|
| Read and examine the codebase | Produce solutions (that's reasoning) |
| Reference SPECIFIC files and line numbers | Write implementation code |
| Produce analysis_document artifact progressively | Skip to planning |
| Present findings to PO via task comments | |

**Tools available:** fleet_read_context, fleet_commit (analysis docs only), fleet_artifact_create/update, fleet_task_progress
**Tools BLOCKED:** fleet_task_complete
**Skills to use:** fleet-gap, fleet-urls, /systematic-debugging, fleet-comment

**Advance when:** Analysis document covers relevant areas. PO reviewed findings. Implications for task are clear.

---

### investigation (readiness 50-80%)
**Job:** EXPLORE OPTIONS, not decide.

| DO | DON'T |
|----|-------|
| Research solutions, explore options | Decide on an approach (that's reasoning) |
| Explore MULTIPLE options — not just the first one | Write implementation code |
| Cite sources, compare tradeoffs | Commit to a solution |
| Present findings to PO | |

**Tools available:** fleet_read_context, fleet_commit (investigation docs only), fleet_artifact_create/update, fleet_task_progress
**Tools BLOCKED:** fleet_task_complete
**Skills to use:** /brainstorming, /dispatching-parallel-agents, /adversarial-spec (architect), fleet-report

**Advance when:** Research document has multiple options. PO reviewed findings. Enough info to decide in reasoning.

---

### reasoning (readiness 80-99%)
**Job:** PLAN, not execute.

| DO | DON'T |
|----|-------|
| Decide approach based on requirements + analysis + investigation | Start implementing |
| Produce plan that references verbatim requirement EXPLICITLY | Skip contribution check |
| Specify target files and components | |
| Map acceptance criteria to implementation steps | |
| Present plan to PO for confirmation | |

**Tools available:** fleet_read_context, fleet_task_accept, fleet_task_create, fleet_commit (planning docs), fleet_artifact_create/update
**Tools BLOCKED:** fleet_task_complete
**Skills to use:** /writing-plans, fleet-plan, fleet-task-create, fleet-contribution (check inputs)

**Before advancing:** Verify required contributions received (use eng_contribution_check or pm_contribution_check). Missing contributions → fleet_request_input. Do NOT advance to work without required inputs.

**Advance when:** Plan exists and references verbatim. Plan specifies target files. PO confirmed. Readiness reaches 99-100%.

---

### work (readiness 99-100%)
**Job:** EXECUTE THE PLAN, not redesign.

| DO | DON'T |
|----|-------|
| Execute the confirmed plan exactly | Deviate from the plan |
| Follow conventions: conventional commits, tests | Add unrequested scope |
| Use pre-embedded task data (or fleet_read_context if injection:none) | Modify files outside plan targets |
| Call fleet_task_accept with plan | Skip tests |
| Call fleet_commit for each logical change | |
| Call fleet_task_complete when done | |

**Tools available:** ALL tools
**Tools BLOCKED:** none
**Skills to use:** /test-driven-development, /verification-before-completion, fleet-commit, fleet-pr, fleet-contribution (consume inputs)

**Required tool sequence:**
1. `fleet_read_context` — load task + methodology state
2. `fleet_task_accept(plan)` — confirm plan (verbatim reference checked)
3. `fleet_commit(files, msg)` — one or more, conventional format
4. `fleet_task_complete(summary)` — push, PR, review chain fires

## Readiness Is Not a Gate

Readiness defines your methodology stage. It does NOT block dispatch.
The PO sets readiness to control what stage you operate in.

- Readiness 10 → conversation stage → ask questions
- Readiness 30 → analysis stage → examine codebase
- Readiness 50 → investigation stage → research options
- Readiness 80 → reasoning stage → plan approach
- Readiness 99 → work stage → execute plan

## Task Types and Required Stages

| Type | Required Stages |
|------|----------------|
| epic | conversation → analysis → investigation → reasoning → work |
| story | conversation → reasoning → work |
| task | reasoning → work |
| subtask | reasoning → work |
| bug | analysis → reasoning → work |
| spike | conversation → investigation → reasoning (no work) |
| blocker | conversation → reasoning → work |

## Checkpoints

- At **50% readiness** → PO gets checkpoint notification (informational)
- At **90% readiness** → PO gate request (BLOCKING — only PO can approve)
- At **phase advancement** → PO gate request (ALWAYS)
