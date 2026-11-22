---
name: plan
description: Create an implementation plan for a nontrivial task and persist it to .agentic/specs/ for execution by /execute-plan.
user-invocable: true
disable-model-invocation: false
argument-hint: "<task>"
model: opus
---

# Plan a nontrivial change

If the session already runs a stronger model, delete the model pin.

## Step 1 — Sync & understand

- Fresh context first: if this session already carries a long unrelated
  conversation, suggest the user `/clear` (or open a new session) and re-invoke
  `/plan` before any investigation — plans inherit stale assumptions and debate
  residue from long sessions. No mechanism can do this automatically; say it,
  then stop and wait.
- Start from the right base: check `git branch --show-current`. If the session
  sits on a feature branch, offer to switch to the repo's default branch first. Then offer
  `git pull`. Deliberately
  planning on top of an in-flight branch (stacked work) is allowed — but it's
  the user's explicit call, and the spec header must record that base.
- Read `.agentic/gotchas.md` entries and the exemplars for the affected area.
- Grep `.agentic/decisions/` for active ADRs touching this area — a plan that
  contradicts an ADR needs `/decide` (supersession) as an explicit plan step.
- Investigate the code itself; use parallel `scout` subagents
  (`.claude/agents/scout.md` ) for breadth, and keep the
  design thinking in the main session. Native plan mode is welcome — this skill
  governs the *artifact*, not how you think.

## Step 2 — Interview (only if ambiguous)

Max 2 rounds, 3–7 questions total via AskUserQuestion. Ask about intent, scope
boundaries, and acceptance criteria — never about things the code can answer.

## Step 3 — Write the plan

Write `.agentic/specs/plan-<slug>.md`. The spec is a **cold handoff**: `/execute-plan`
runs it in a fresh session that saw none of this conversation — anything not in the
file is lost.

- **Header** — one line: `planned-against: <branch> @ <git rev-parse --short HEAD>`
  — the base branch and commit the plan was investigated on — so the executor
  branches from the same base and can detect drift if the code moves before
  execution.
- **Overview** — goal + why now (2–5 lines).
- **Affected areas** — files/modules, verified against the actual tree, never from memory.
- **Context & constraints** — what the executor can't re-derive cheaply: key
  investigation findings (each with an evidence path), decisions the user made in
  the interview (scope calls, rejected alternatives), and pointers to the governing
  ADRs/gotchas by path. Judgment and rationale only — never restate code facts the
  executor can re-read (a spec that paraphrases code becomes a drift source; hard
  rule 2).
- **Steps** — discrete, ordered; each names the files it touches and how to verify it
  (which test/command proves the step works). Mark independent steps as parallelizable.
- **Acceptance criteria → test mapping** — a table: each AC, the test that will prove
  it, and the test file it lives in.
- **Quality gate checklist** — copy the thresholds FROM `.agentic/quality-gates.yaml`
  at plan time; never write numbers from memory.
- **Out of scope** — what this plan deliberately does not do.

## Step 4 — Adversarial review, then approval

- Dispatch a `critic` subagent (`.claude/agents/critic.md`. Fix legitimate findings in the
  plan; record rejected findings in a **Review** section of the spec itself, each
  with the rejection reason.
- Present the plan — including the critic's verdict and how findings were
  handled — and get explicit user approval before any execution. On approval,
  hand off to `/execute-plan` — and suggest running it in a fresh session
  (`/clear` first). Do not start implementing inside this skill.
