---
name: work-prep
description: "Orchestrates the full preparation workflow for a ticket. Calls /flagrare:intake (which gathers context from Jira/Notion/Figma, grounds the brief in the codebase via /flagrare:codebase-explore, then asks codebase-informed clarifying questions), then hands the codebase-grounded brief to /flagrare:atdd-plan for a TDD-first implementation plan. Use when the user shares a ticket key (e.g. SKU-123), says 'start work on', 'pick up ticket', 'plan this feature', 'work prep', or provides a Jira URL."
---

# Work Prep

Full preparation workflow: ticket context gathering followed by implementation planning.

This skill orchestrates two existing skills in sequence. It does not duplicate their logic.

---

## When to Use

- User shares a ticket key (e.g. `SKU-123`, `ST-456`, `CORE-789`)
- User provides a Jira/Atlassian URL
- User says "start work on", "pick up ticket", "plan this feature", "work prep", "let's work on [ticket]"
- User pastes a ticket key with no other context

---

## Workflow

### Step 0: Lock the goal (anti-stall)

**Hard requirement.** Before invoking any sub-skill, you (the executing model) MUST call `/goal` yourself. work-prep is a multi-skill chain (`intake → atdd-plan → confirm`) that emits a large context brief and a large plan mid-flow, both are points where the model tends to read "turn complete" and stop. A `/goal` is a session-scoped Stop-hook: after every turn a fast evaluator checks your condition against the conversation and makes you continue if it is unmet. Set it here, once, spanning the whole chain. (Grounded in [`docs/research/2026-06-11-claude-code-goal-anti-stall.md`](../../../../docs/research/2026-06-11-claude-code-goal-anti-stall.md).)

Phrase the condition as something your own output demonstrates, the evaluator cannot run tools or read files, only judge what you have surfaced:

> A codebase-grounded context brief has been produced; the most blocking clarifying questions have been asked via the `AskUserQuestion` tool and answered (or none were blocking); `/flagrare:atdd-plan` has produced an implementation plan with acceptance tests; and the closing next-step `AskUserQuestion` (Start implementation / Adjust the plan / Stop here) has been presented and answered. Stop after 20 turns if not met.

**One goal per session.** Because work-prep sets this spanning goal, `/flagrare:intake` must NOT set its own, the `[work-prep]` prefix in Step 1 signals it to skip (a second goal would silently replace this one). Likewise do not re-set the goal between steps.

**If `/goal` is unavailable** (untrusted workspace, or `disableAllHooks` / `allowManagedHooksOnly` set): proceed without it and rely on the same-turn handoffs and the sub-skills' own no-yield notes.

Also create a Todo list (TodoWrite) with one item per stage of the chain.

### Step 1: Invoke `/flagrare:intake`

Call `/flagrare:intake` with the ticket reference prefixed by `[work-prep] ` (e.g., args: `[work-prep] SKU-123`). This prefix tells intake two things: (1) skip setting its own `/goal`, work-prep's Step 0 goal already spans the chain, and (2) skip its Step 6 next-step prompt and hand off directly. This skill will:

1. Parse the ticket ID/URL and identify the platform
2. Read the full ticket via MCP (Jira, Linear, etc.)
3. Follow all referenced links in parallel (Notion, Figma, Confluence, GitHub, etc.)
4. Synthesise a context brief (without questions yet)
5. **Ground the brief in the codebase** via `/flagrare:codebase-explore`, finding the files, utilities, and prior attempts the plan will touch
6. Ask **codebase-informed** clarifying questions (specific: "extend `src/x.ts` or fork it?", not abstract: "where should this live?")
7. Resolve open questions with the user
8. Set the bet with `/flagrare:measure-impact` (quick), or record a skip for a small fix, and pass it to `/flagrare:atdd-plan`. Intake does this in its `[work-prep]` hand-off, right before invoking atdd-plan.

**Wait for `/flagrare:intake` to complete before proceeding.** The context brief must be finalized, codebase findings populated, and open questions resolved.

### Step 2: Invoke `/flagrare:atdd-plan`

Once `/flagrare:intake` has produced a complete, codebase-grounded context brief, invoke `/flagrare:atdd-plan`. Pass the brief as opening context. This skill will:

1. Run its own `/flagrare:codebase-explore` pass (atdd-plan stays self-sufficient, intake's findings in the brief are additional input, not a substitute)
2. Produce an ATDD-first implementation plan with acceptance tests, named design patterns, SOLID audit, and gap review
3. Present the plan for user review

### Step 3: Confirm readiness: use the AskUserQuestion tool

After the plan is presented, issue an `AskUserQuestion` tool call, same interaction shape as intake's next-step prompt and plan-mode's accept tool. Do NOT phrase this as prose; that lets the turn end ambiguously.

Options:

- **Start implementation** (Recommended): proceed to write code against the plan.
- **Adjust the plan**: collect specific changes from the user, re-run the relevant atdd-plan steps, then re-present.
- **Stop here**: return control with the plan saved/printed for later.

---

## Anti-patterns

- **Don't skip the Step 0 `/goal`.** It's the forcing function that carries the model across the brief and the plan without stopping. The `[work-prep]` prefix on intake assumes this goal exists.
- **Don't let a sub-skill set its own goal.** Only one goal is active per session; a second silently replaces work-prep's spanning goal and the chain loses its anti-stall guarantee mid-flow.
- Don't skip `/flagrare:intake` and jump to planning. Context gaps turn into rework.
- Don't invoke `/flagrare:atdd-plan` before clarifying questions are resolved.
- Don't start implementation before the plan is reviewed and approved.
- Don't re-fetch context that `/flagrare:intake` already gathered. Pass the brief forward.
- Don't ask clarifying questions before codebase grounding. Questions asked without knowing what exists are abstract and frequently miss the real ambiguity. intake handles this by calling `/flagrare:codebase-explore` before Step 5.
- Don't be surprised that `/flagrare:codebase-explore` runs twice in this flow, once in intake (scoped to inform questions) and once in atdd-plan (scoped to anchor the plan). atdd-plan stays standalone-callable; that requires it to do its own pass.
- **Don't end work-prep with a prose "what next?" question.** After the plan is presented, close with a tool-driven `AskUserQuestion` prompt, same UX contract as plan-mode's accept tool. A button, not a typing prompt.

---

## Critical: The handoff mechanism

The `[work-prep]` prefix in intake's args is the signal. When intake sees it, intake skips its next-step prompt and immediately invokes `/flagrare:atdd-plan` itself. This means:

- Work-prep invokes intake (with prefix) → intake runs its full workflow → intake invokes atdd-plan → atdd-plan produces plan → work-prep resumes at Step 3.
- Work-prep does NOT need to invoke atdd-plan itself. Intake handles the handoff when it sees the `[work-prep]` prefix.

If you are executing work-prep and intake finishes WITHOUT invoking atdd-plan (e.g., it returned with just the brief), you MUST invoke `/flagrare:atdd-plan` yourself before proceeding to Step 3.

---

## Flow position

```
/flagrare:work-prep [ticket ID or URL]
     |
     v
[Step 0: /goal locked, spans the whole chain, anti-stall]
     |
     v
/flagrare:intake [work-prep] <- 0. skip own /goal (work-prep owns it)
                                1. read ticket + follow references in parallel
                                2. synthesise brief (no questions yet)
                                3. /flagrare:codebase-explore  <- ground brief in code
                                4. ask codebase-informed clarifying questions
                                5. resolve, finalize brief
                                6. detect [work-prep] prefix → invoke atdd-plan directly
     |
     v
/flagrare:atdd-plan       <- runs its own /flagrare:codebase-explore pass
                             (stays self-sufficient for standalone use),
                             then produces ATDD-first plan
     |
     v
[user reviews plan]
     |
     v
[implementation begins]
```
