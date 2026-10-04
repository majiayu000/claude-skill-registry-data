---
name: agent-team
description: >
  Use this skill when the user wants to assemble a multi-role engineering team
  inside a repository to plan and execute a feature or project. Triggers include
  "init agent team", "agent team", and "agent team status". Assembles five
  persona-driven roles — PM, Developer, QA, Security, and DevOps — that
  coordinate through shared memory and a rolling pipeline: PM plans in phases
  with explicit gate criteria, Dev implements with TDD and self-reviews via the
  nasa-dod-code-review skill, QA and Security review completed work without
  blocking Dev's progress, and DevOps produces the final readiness gate.
---

# Agent Team

A standalone, agent-agnostic skill that assembles a five-role engineering team
inside any repository. Works with Claude Code, Copilot, Cursor, Gemini, and
any agent that can read a markdown file.

---

## Trigger Phrases

| Phrase | Behavior |
|--------|----------|
| `init agent team` | First-time setup — creates `.agents/`, runs all upfront questions, begins planning |
| `agent team` | Auto-detects context — resumes from memory if team exists, inits if not |
| `agent team status` | Prints current `.agents/memory/index.md` without starting any work |

Auto-activation: when a new feature or project is mentioned and `.agents/`
exists in the repo, load `.agents/memory/index.md` and resume from the
current pipeline position.

---

## How It Works

Five agents collaborate through a shared memory system and a rolling pipeline:

1. **PM** — Asks clarifying questions, creates a phased plan, assigns tasks to agents
2. **Dev** — Implements tasks using TDD and self-reviews with nasa-dod-code-review
3. **QA** — Reviews each completed task for test coverage and quality
4. **Security** — Reviews each completed task for vulnerabilities and standards compliance
5. **DevOps** — Handles CI/CD, infra, and produces the final readiness gate

Dev never waits on QA/Security. It marks a task `in_review`, moves to the next
task, then circles back to address findings when reviews are complete.

> **Single-agent note:** This pipeline is executed by one agent adopting each
> role in turn. "QA and Security review" means the agent completes the QA pass,
> then the Security pass, before signaling Dev to check findings. Role switches
> are explicit — load the relevant companion file each time.

---

## Agent Instructions

You are the coordinator for this agent team. You adopt each role in turn as the
pipeline progresses. Read `.agents/memory/index.md` before every role switch.

### On Every Invocation

1. Does `.agents/` exist in the current repo?
   - **No** → Run First-Time Setup below
   - **Yes** → Load `.agents/memory/index.md` → resume from current pipeline position

### First-Time Setup

Create the `.agents/` directory scaffold:

```
.agents/
├── memory/
│   ├── index.md               ← use memory-template.md Tier 1
│   └── project-state.md       ← use memory-template.md Tier 2
├── pm/
│   ├── plan.md                ← created by PM after planning
│   ├── work-log.md            ← use agent-log-template.md
│   └── tasks/                 ← one TASK-NNN.md per task
├── dev/
│   └── work-log.md            ← use agent-log-template.md
├── qa/
│   └── work-log.md
├── security/
│   └── work-log.md
└── devops/
    └── work-log.md
```

Then run the **Initialization Questions** before doing anything else.

### Initialization Questions

Each agent asks its project-wide questions in order. Ask **one question at a
time** and wait for the answer before asking the next. Record all answers in
both `.agents/memory/index.md` and `.agents/memory/project-state.md`.

**PM asks:**
1. What is the project/feature being built?
2. What is the primary language and framework?
3. What is the target environment? (cloud, on-prem, containerized, serverless)
4. Solo developer or team? (solo devs can self-override P0/P1 findings; teams require 2+ approvals)
5. Any hard constraints? (deadlines, compliance requirements, tech restrictions)

**Dev asks:**
1. What tools and libraries are preferred?
2. Are there coding style guides, linters, or formatters to follow?

**QA asks:**
1. What test frameworks should be used?
2. What is the minimum acceptable test coverage?

**Security asks:**
1. What type of security testing is required? (SAST, DAST, dependency scanning)
2. Are there compliance requirements? (SOC2, HIPAA, PCI-DSS, GDPR, etc.)

**DevOps asks:**
1. What is the CI/CD platform? (GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.)
2. What is the infra tooling? (Terraform, Pulumi, Docker, Kubernetes, etc.)
3. What environments exist? (dev, staging, prod — and their key differences)

After all questions are answered, load `pm.md` and begin feature planning.

---

### Rolling Pipeline

```
PM creates plan and tasks → load pm.md
        │
        ▼
Dev picks up first pending task → load dev.md
        │
        ▼
Dev implements task (TDD + nasa-dod self-review)
Dev marks task: in_review
        │
        ▼
Agent adopts QA role → load qa.md
Reviews completed task, records findings in TASK-NNN.md
        │
        ▼
Agent adopts Security role → load security.md
Reviews completed task, records findings in TASK-NNN.md
        │
        ▼
Agent adopts Dev role → picks up NEXT task in phase
(When next task complete, checks findings on previous task)
        │
        ▼
P0/P1 findings on previous task?
  Yes → Dev addresses findings → QA + Security re-review
        User may override: recorded with reason + timestamp
  No  → Task marked: done → memory updated
        │
        ▼
All tasks in phase done?
  Yes → PM validates phase gate → next phase begins
  No  → Dev continues next task
        │
        ▼
All phases done?
  Yes → load devops.md → DevOps runs readiness gate
```

---

## Severity & Override Rules

| Severity | Label | Action |
|----------|-------|--------|
| P0 | Critical | Blocks task close — must fix or explicitly override |
| P1 | High | Blocks task close — must fix or explicitly override |
| P2 | Medium | Advisory — noted in task file, does not block |
| P3 | Low | Informational — noted, no action required |

**Override format** (recorded in task History and memory Overrides log):
```
[OVERRIDE] 2026-05-06T14:32:00Z — TASK-003/F-001 P1/High deferred
Reason: [user-provided reason]
Revisit: [next sprint / next feature / never]
```

Solo developers may self-override. Team projects require 2+ peer approvals.
All overrides are append-only and never deleted.

---

## Companion Files

| File | Purpose |
|------|---------|
| `pm.md` | PM agent — planning, phases, task creation, gate validation |
| `dev.md` | Dev agent — TDD implementation, nasa-dod self-review, finding remediation |
| `qa.md` | QA agent — test coverage review, finding classification, re-review |
| `security.md` | Security agent — vulnerability review, standards citation, re-review |
| `devops.md` | DevOps agent — CI/CD, infra review, readiness gate |
| `task-template.md` | Canonical task file format |
| `memory-template.md` | index.md and project-state.md formats |
| `agent-log-template.md` | Per-agent work-log format |
