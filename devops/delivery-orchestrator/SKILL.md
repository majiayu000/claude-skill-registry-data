---
name: delivery-orchestrator
description: Decompose an epic into atomic parallelizable tasks, route each to the right skill, and keep the four delivery records straight — issues, STATUS, ROADMAP, CHANGELOG. Use as a meta-router when several skills could apply, and as the baseline for how delivery state is recorded. Trigger at the start of any multi-track epic, when the skill count exceeds ~12, or when the records have drifted from reality.
---

# Delivery Orchestrator

> **A skill for choosing skills.** Once your harness grows past a handful of skills, the agent needs a way to select the right one. This is that skill.

The orchestrator has three jobs: decompose work into the smallest independently executable units,
route each unit to the skill that owns it, and **keep the delivery records honest** — because a
plan nobody can trust is worse than no plan, and it takes longer to discover.

## When to use

- Starting a new epic or multi-track piece of work
- When an agent is about to attempt everything in one context window
- When parallel execution across multiple agents is needed
- When you need to decide which skill applies to an incoming task
- **When the records have drifted** — a status file that stops before today's work, a roadmap
  asking for a decision already made, a tracker claiming `gated` with nothing that walks it

## The delivery records — the baseline

**One fact, one owner.** Four artefacts carry delivery state, and each answers exactly one
question. Full doctrine, including the issue template and the audit: `docs/DELIVERY-RECORDS.md`.

| Record | The one question it answers | Written when |
|---|---|---|
| **GitHub issues** | *What exactly is this work, and how will we know it is done?* | Before the first line of code |
| **`STATUS.md`** | *What is happening now, and what waits on whom?* | One entry per working session |
| **`ROADMAP.md`** | *What are we building toward, in what order?* | When a milestone or the plan changes |
| **`CHANGELOG.md`** | *What shipped — proven, tested?* | When user-visible work merges |

The four rules that keep them from drifting:

1. **`ROADMAP` owns build order.** Where another document disagrees about what is next, the
   roadmap wins.
2. **`CHANGELOG` records the proven, not the intended.** A changelog of intentions reads as
   evidence, which makes it worse than none.
3. **An issue not filed is not started.** The tracker is current *before* the code, because the
   failure this prevents is work that accretes from a small fix and is reconciled afterwards,
   if at all.
4. **`gated` means a test proves a user can reach it; `shipped` means a person used it.** These
   two are the ones routinely overclaimed. Code existing is `built`, and deployment is not
   shipping.

## Procedure

### Part 1 — Decomposition

1. **Read the spec or brief** — confirm a feature spec or HLD exists. If not, invoke `spec-first-delivery` first.
2. **Identify tracks** — group work into independent tracks (e.g. backend API, frontend, infrastructure, testing). Tracks can run in parallel. Dependencies between tracks must be explicit.
3. **Break each track into atomic tasks** — an atomic task is one that:
   - Can be assigned to a single agent
   - Has a clear input and a clear output
   - Does not require coordination with another concurrent task to complete
   - Can be validated independently
4. **Sequence dependencies** — where task B requires output from task A, mark the dependency. Everything else is parallel.
5. **Assign context boundaries** — each agent gets only the context it needs. Avoid stuffing all specs into every agent's context.

### Part 2 — Skill routing

1. **Map each task to a skill** using the routing table below. If no skill matches exactly, use the closest and note the gap.
2. **Validate integration after parallel work** — run the full regression suite (`make check` or the project's equivalent convergence command) after all parallel tracks complete. Parallel work that skips integration validation is not done.

## Skill routing table

| Task type | Route to skill |
|---|---|
| New feature / epic planning | `spec-first-delivery` |
| Architecture decision or trade-off | `the-architect` |
| High-stakes design review | `adversarial-gate` |
| Pre-deployment go/no-go | `release-readiness` |
| Release process governance, SemVer, ADR, changelog | `release-manager` |
| Enterprise policy, compliance, or governance alignment | `governance-guardrail` |
| GitHub repo operations: CI triggers, billing, issues, labels, branch protection | `github-manager` |
| Google ADK agent patterns | `adk-expert` |
| Cloud infrastructure guardrails (GCP, AWS, Azure, Alibaba Cloud) | `cloud-expert` |
| MCP server design or governance | `mcp-server-scaffold` |
| Agent output validation | `domain-validator` |
| PR or code review | `pr-reviewer` |
| LLM cost or model selection | `cost-guardrail` |
| Status or standup synthesis | `sitrep` |
| Plugin-directory, marketplace, or curated-list submission | `plugin-submission` |
| New repo or operating model install / repair | `operating-model-bootstrap` |
| Delivery controls: source of truth, issue/PR conventions, DoD, escalation | `delivery-orchestrator` (own it here) |
| An agreed goal to pursue autonomously to a merged outcome | `get-it-done` |
| Developer-machine contention, orphaned automation browsers, cloud-sync stalls | `system-performance-guardrail` |
| Read-only SRE checkup of a GCP project: probes, status table, one `OVERALL:` line | `cloud-checkup` |
| Frontend performance measurement: Core Web Vitals, traces, Lighthouse, heap growth | `frontend-performance-audit` |
| Routing this list | `delivery-orchestrator` (you are here) |

## Outputs

- Task breakdown: tracks, atomic tasks, dependencies
- Skill routing: task → skill mapping
- Parallel execution plan with integration validation step
- A brief orchestration summary for the human lead

## Guardrails

- **Atomic means independently validatable.** If you cannot describe how to verify a task in isolation, it is not atomic — split it further or merge it with its dependency.
- **Parallel agents must not share mutable state without a coordination strategy.** If two tracks write to the same file or schema, they are not independent. Use worktrees or serialise them.
- **Integration validation is not optional.** Parallel work that skips the post-merge regression check is not complete.
- **Keep agent context lean.** Each agent gets its task spec and relevant ADRs, not the entire repo.
