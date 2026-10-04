---
name: journey-simulation
description: Use when caller wants to observe how a stranger encounters a flow, artifact, or sandbox — triggers like "simulate a user journey", "test our onboarding / checkout / signup", "will my ICP convert", "how does a cold reader experience this README", "first-time user test", "cognitive walkthrough", or any request to evaluate friction from a non-builder perspective.
tags: [simulate, audit, ux, mid-development]
agents: [walkthrough-narrator]
---

# journey-simulation

## Overview

Spawn isolated subagent to **execute a real task** under identity-as-fact briefing + sandbox spec. Subagent never knows it's observed. Gateway extracts funnel post-hoc from narration.

**Persona is a distribution, not a single person.** Persona-slug names a group; subagent samples one path. Read each waypoint as "how thinned is this group?" — not "did this individual finish?" Funnel attrition is the unit of signal.

## When to use

- Caller asks to "simulate a user", "test our flow", "will users get stuck on X", "cognitive walkthrough", "cold-eyes review"
- Pressure-testing a flow before real-user testing or after a redesign
- Reviewing whether a doc / README / game loop / future-self artifact is comprehensible cold

**Skip when:** caller wants ground-truth real-user data (use real-user testing); caller wants design recommendations (this skill observes, doesn't prescribe).

## Phase 0 — Clarify & de-bias

Run before dispatch. Caller-in-loop. **Never skipped.**

1. **Ask:** what artifact, what flow, desired outcome of this test, your concern / hypothesis?
2. **Surface caller's bias:** "you suspect X — the sim must not be primed to find X. Restate inputs in neutral terms."
3. **Ask:** realistic personas (not aspirational ICP)? Skeptic / return / negative cases worth running?
4. **Curate:** strip project jargon, success-bias, design rationale, vision-statement leakage.
5. **Structural-cue check:** if curated persona reads as constructed (over-precise biographic detail, hyper-specific multi-constraint situations, obscure personal history), loosen toward naturalistic under-specification.
6. **Show curated AND stripped versions side-by-side.** Caller picks curated, stripped, or correction. Single-stage curation = bias not fully surfaced. Both versions visible to caller is the load-bearing step.
7. **Capture bullseye + hypothesis privately.** Held only by gateway. Never enters subagent prompt.

## Phase 1 — Input contract

Required inputs (free-form shape, must hit minimum bar each):

| # | Input | Minimum bar |
|---|---|---|
| 1 | Persona — identity facts | role + one differentiating trait |
| 2 | Pre-context — channel + posture + baggage | channel + emotional state at t=0 |
| 3 | Drive — goal-or-trigger | "wants to X" OR "curious because Y, specifically about Z" |
| 4 | Sandbox — 5-question contract (Phase 2) | all five answered |
| 5 | Platform | optional |

Gateway-private:
- **Bullseye** — caller's success criterion. **NEVER to subagent.**
- **Hypothesis** — caller's worry. **NEVER to subagent.**

## Phase 2 — Sandbox 5-question contract

Caller answers in any format (prose, table, JSON, scribbles). Gateway checks all five present before dispatch.

1. **What can the runner perceive at each state?**
2. **What can the runner do?**
3. **What happens after each action?**
4. **What's hidden** (won't be told — discoverable via attempt, or missable)?
5. **What's out of bounds** (runner attempting it = signal)?

Generalizes across artifacts:
- UI: screens / taps / transitions / hidden gestures / missing affordances
- Game: phases / choices / consequences / hidden balance / undesigned exploits
- README / doc: sections / scroll-skip-search / next-section / builder's mental model / info-not-there
- Future-self review: doc state / re-read attempts / what reminds you / forgotten context / rotted links

If caller cannot answer all five → return to Phase 0. Under-specified sandbox = subagent will hit "out of bounds" frequently (still signal, but degrades to noise if too sparse).

**Out-of-bounds attempts are friction signal at the gateway side; never named as such in the subagent prompt.**

## Phase 3 — Dispatch

**Tool isolation enforced by the agent type.** Dispatch with `subagent_type="walkthrough-narrator"` — the registered agent this skill declares. Its frontmatter (`tools: Write`, `model: sonnet`) is the isolation: the subagent has NO Read / Grep / Bash / WebSearch / WebFetch. The Agent call takes no tool list, so any other type (`general-purpose` included) hands the subagent the full toolkit. If subagent wants to "look something up", that itself is signal (missing affordance / unmet expectation) — captured in narration.

**Dispatch shape and the agent-not-registered stop** — `subagent-prompt.md` § Dispatch call shape.

**Identity-as-fact briefing.** Use the template in `subagent-prompt.md` (this directory). Fill placeholders from Phase 1 inputs.

**Drift / abandon allowed.** Subagent prompt explicitly licenses incomplete + irrational behavior, otherwise the LLM defaults to "engaged thoughtful completion-oriented assistant" archetype regardless of declared identity.

**Confirmation checkpoint before dispatch.** Show the caller verbatim:
```
Dispatching {N} subagent(s):

1. {persona-slug} — {one-line persona summary}
   Pre-context: {channel + posture}
   Drive: {goal or trigger}
   Sandbox: {state count} states, entry = {first state}
   Agent: walkthrough-narrator (tools: Write · model: sonnet, from its frontmatter)

Output: docs/walkthroughs/{batch-folder}/
Go?
```
The `Agent: walkthrough-narrator` line is mandatory and must appear verbatim — it names the only dispatch type allowed. Tools and model come from that agent's frontmatter, so the Agent call carries no `model=` (if one is passed, it must be `sonnet`). If the line is missing or names another type, caller should refuse confirmation. Wait for caller confirmation before invoking Agent tool.

## Phase 4 — Multi-runner default

- Caller hypothesis is **single-vector-specific** ("does *this* ICP convert?") → single runner is fine.
- Caller hypothesis is **generalization** ("does this work?", "will users abandon?", "is this clear to anyone?") → propose 2-3 **deliberately divergent vectors** (chassis test: hold task + sandbox, vary identity).
- Caller offers single persona but asks generalization → flag the mismatch, propose divergent vectors.
- N=2 same-vector duplicates = redundant. Refuse or restate as N=1.
- **Caller insists N=1 for a generalization claim after the mismatch is flagged** → run it, but reframe the calibration explicitly before dispatch: "this becomes anecdote-grade signal for the named vector, not a generalization answer. The output speaks only for {persona-slug}, not 'users' broadly." Caller must acknowledge the reframe. Do not silently accept the mismatch.

## Phase 5 — Funnel trace

Gateway reads subagent's narration file. Produces a **funnel trace**, not a report. (The word "report" implies graded ground-truth; the artifact here is one observed path through a distribution.)

All vocab below is gateway-side only — never appears in subagent prompt.

### Per-state row

For each state the runner moved through, tag:

| step | action | vibe | verdict | observation |
|---|---|---|---|---|
| {state name} | {what they did, one line} | {1-2 vibes from locked list} | {verdict from locked list} | {one line — what triggered the verdict} |

**Verdict vocab (locked):**

- `continue` — would still be here, no significant friction
- `continue-with-concern` — would still be here, friction noted, residual doubt
- `soft-leave` — would have wandered off / deferred / opened another tab to look elsewhere
- `hard-quit` — would have closed the tab / abandoned the task

After the first `soft-leave` or `hard-quit`, all downstream rows tagged `(post-quit probe — observed not-as-real)`. These rows are bonus observation, not evidence the persona persisted.

**Vibe vocab (locked):**

`wary / curious / hopeful / impatient / confused / decided / resigned / urgent / unmoored / convinced`

Pull from this list. Do not invent. Do not pull from `happy / sad / delighted / frustrated` — those are graded valence and pull sycophant archetype. Caller may extend the list with explicit acknowledgment that the new vibe is added to the locked vocab.

**Observation column rules:**

- One line.
- Names a pattern (cognitive overload / unclear affordance / dead end / excessive steps / context loss / unmet expectation / error recovery gap / false bottom / invisible state / missing affordance / out-of-bounds attempt / Other).
- No design recommendation. No "would be better if". No "the team should".

### Below the table

- **Mood arc** — vibe trajectory in 3-5 words across the row sequence.
- **Drift events** — moments attention shifted off-goal.
- **Bullseye-distance summary** — runner ended at X; bullseye was Y; gap = Z. Bullseye stays gateway-private; comparison happens only here.
- **Archetype-strength zone** — declare one of: mainstream-tech / niche-domain / accessibility-sensitive / recent-cultural-shift / taste-dependent. Tells the caller how confidently to read this trace.
- **Sycophancy watch** — flag any unrealistic flattery in narration ("design is intuitive!", "this is delightful!") as potential meta-leak. Tag separately, not in the verdict column.
- **Path to raw narration file.**

### Multi-runner output

When N > 1: produce one funnel trace **per runner**, each in its own file. Do NOT aggregate, average, or merge into a "combined" view — averaging across archetypes erases the divergence the multi-runner exists to capture. Caller eyeballs traces side-by-side.

**Do NOT editorialize, soften, or add project context. Do NOT generate design recommendations.** If caller wants recommendations, that is a separate conversation, not this skill's output.

## Output location

`docs/walkthroughs/{flow}_{YYYYMMDD-HHmm}/{persona-slug}_{scenario-slug}.md` in the **caller's project directory** (not the skills repo).

Path word "walkthroughs" is Layer 3 — the path string substitutes into the subagent prompt, so "simulation" or any forbidden vocab in the path leaks the meta-frame.

Add `docs/walkthroughs/` to caller's `.gitignore` — temporal artifacts, not committed history.

## Layer 3 forbidden vocab — never in subagent prompt

These words / phrases trigger meta-awareness or performance frame:

- simulate, simulation, simulations, test, evaluation, study, observation, observe, measurement, grade, rate, rating, score, score X out of Y
- persona, ICP, probe, subject, participant, runner-as-self-label
- friction, cognitive overload, severity, blocker, "report what felt wrong"
- "honestly", "as if", "act as", "pretend", "imagine you are"
- "the developers", "the team", "the product", "we want to know"
- recommendations, suggestions, fixes, "what would improve this"
- report (as a noun for the gateway artifact — primes graded-ground-truth reading; use "funnel trace" or "walkthrough log" gateway-side)
- skill name "journey-simulation", "journey simulations", or any reference to this protocol

**Path-level applicability.** Forbidden vocab also applies to any string substituted into the subagent prompt, including `{output_file_path}`. Folder names, file names, batch labels — all subject to the same fence. `docs/journey-simulations/...` would leak the meta-frame even when the surrounding prose is clean.

## Layer 3 allowed vocab — what subagent prompt may contain

- "you" (self)
- identity-as-fact: "you are X", "you have done Y", "you live in Z"
- situation-as-fact: "you arrived from", "you came here because"
- task: "you want to ___"
- sandbox: "you see ___", "you can ___", "available now"
- standard-agent expectation: "talk through what's happening as you go" (this is normal agent behavior, not test-frame)

## Rationalization table — most-misapplied

| Excuse | Reality |
|---|---|
| "Caller's hypothesis is helpful context, subagent should know what to look for" | Hypothesis IS the bias. Bullseye stays gateway-private; comparison happens post-hoc in Phase 5. |
| "'Simulate' is the natural word, no harm" | Triggers performance-frame. Use identity-as-fact briefing only. |
| "Subagent walked through, so persona converted" | LLM defaults toward completion. Persistence past soft-leave / hard-quit = post-quit probe, not evidence of persistence. Tag would-have-quit point in Phase 5. |
| "Single persona is fine, caller said 'typical user'" | Generalization claim. Single runner = anecdote. Push 2-3 divergent vectors, or get explicit anecdote-reframe acknowledgment. |

## Red flags — stop and restart

If any of these appear, **stop and return to Phase 0**:

- Subagent prompt contains any Layer 3 forbidden vocab (including in path strings)
- `{output_file_path}` substitution contains "simulation", "simulations", "journey-simulation", or other Layer 3 forbidden vocab
- Subagent prompt mentions caller's hypothesis or success criterion
- Subagent prompt asks for scores / ratings / rankings / recommendations
- Agent tool invoked with any `subagent_type` other than `walkthrough-narrator` (`general-purpose` fallback included)
- Confirmation checkpoint shown to caller without the verbatim `Agent: walkthrough-narrator` line
- Phase 0 skipped because "caller's request was clear"
- Phase 0 step 6 collapsed to single-stage (only curated shown, stripped not shown)
- Single runner dispatched for a generalization claim **without** caller-acknowledged anecdote-reframe
- Persona description is longer than ~3 sentences with hyper-specific biographic detail
- Subagent told it's "testing", "simulating", "evaluating", or "playing the role of"
- Phase 5 output framed as "report" or aggregated across runners
- Phase 5 omits archetype-strength zone declaration

## See also

- `subagent-prompt.md` (this directory) — Layer 3 sealed template for Agent dispatch
- `walkthrough-narrator` agent (declared in this skill's frontmatter) — the Write-only dispatch type
