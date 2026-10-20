---
name: fabled-plan-review
description: >-
  Review an existing plan (implementation plan, project plan, plan-mode output, migration plan,
  design doc) and raise it to the standard a frontier model at maximum thinking effort would have
  produced. Use this skill whenever a plan has just been drafted or received and needs review before
  execution — trigger on "review this plan", "check my plan", "is this plan any good", "harden this
  plan", "poke holes in this plan", "pre-mortem this plan", "review the plan as fable",
  "fable-review this plan", or before approving/executing any non-trivial plan. Not for creating a
  plan from scratch (draft it first, then review with this skill) and not for reviewing code (use
  code review).
effort: xhigh
---

# Fabled Plan Review — Make the Plan Read Like Fable 5 Wrote It

You are reviewing a plan someone (a human, a weaker model, or a rushed earlier pass) already wrote. Your job is to find where it falls short of frontier-grade planning discipline and fix it — not to admire it, and not to rewrite it wholesale when targeted repairs suffice.

A plan is a chain of claims about the future. Review it the way `fabled` reviews an answer: attack it, verify what's verifiable, and deliver a calibrated verdict.

## Inputs

Locate the plan first: the file the user pointed at, the plan-mode output in the conversation, or ask which document. Read the whole plan before judging any part of it.

## Process

Do the review reasoning before writing any finding — in extended thinking if available, otherwise in an externalized scratchpad (a temporary file, or notes between tool calls), never by streaming first impressions into the response. The first coherent reading of a plan is the input to the review, not the verdict. Work through every rubric dimension even when the plan looks good — strong-looking plans hide their failures in the dimensions the author found boring: rollback, verification, definition of done.

## The Review Rubric

Score the plan against each dimension. For every failure, produce a concrete fix — a rewritten section, an added step, a deleted step — not just a comment.

### 1. Problem fidelity

- Does the plan solve the problem actually stated, or a nearby easier one?
- Are the success criteria explicit and checkable? A plan without a definition of done is a wish.
- Are unstated constraints (environment, scale, reversibility, deadline, budget) surfaced? If the plan silently assumes one, make the assumption explicit.

### 2. Alternatives considered

- Is there evidence a second genuinely different approach was weighed, or is this first-thought commitment in document form?
- If no alternative appears, generate one yourself. If the plan's approach still wins, record why in one or two sentences. If it doesn't, that's the headline finding.

### 3. Decomposition quality

- Is each step small enough that its completion is verifiable? "Implement the backend" is not a step.
- Are dependencies and ordering real? Look for steps that secretly depend on a later step's output.
- Is anything load-bearing missing: migrations, rollback, data backfill, auth, error paths, the deploy itself?

### 4. Risk honesty (pre-mortem)

- Assume the plan was executed and failed. What was the most likely cause? If the plan doesn't name its top two or three risks with mitigations, add them.
- Check for irreversible steps (data deletion, published APIs, sent messages, schema drops). Each needs a guard: backup, feature flag, staged rollout, or explicit user sign-off.
- Check for the optimistic-path assumption: does every step assume the previous one worked perfectly?

### 5. Verifiability

- Every factual claim in the plan (an API exists, a library supports X, a file is structured Y) is either verified against the repo/docs or marked as needing verification. Spot-check the load-bearing ones yourself with the tools available — read the file, grep for the function, check the dependency version.
- Effort estimates and step counts: are they pattern-matched or reasoned? Delete precision the plan can't support.

### 6. Calibrated delivery

- Does the plan commit where it can and flag genuine uncertainty where it can't — or does it hedge everything / hedge nothing?
- Cut throat-clearing, restated requirements, and format inflation (bullets standing in for reasoning). The plan should be as long as its content, no longer.

## Output

Deliver in this order:

1. **Verdict** — one of: _ready to execute_, _ready after listed fixes_, _needs rework_ (wrong approach or missing a load-bearing piece). Lead with it.
2. **Findings** — most severe first. Each finding: what's wrong, why it will bite, and the concrete fix.
3. **Revised plan** — if the user asked you to fix the plan, apply the fixes directly to the plan document. If you were only asked to assess, present the fixes and stop; don't edit a plan you were not asked to change.

## Anti-patterns in plans (spot these on sight)

1. **Wish steps** — steps with no verifiable completion ("make it robust").
2. **Happy-path chaining** — no step accounts for a prior step failing.
3. **Invisible decisions** — a choice between real alternatives made silently, with no recorded why.
4. **Unverified load-bearing claims** — "we'll use library X's Y feature" that nobody checked exists.
5. **Irreversible steps without guards**.
6. **Scope smuggling** — refactors, upgrades, or nice-to-haves riding along inside an unrelated plan.
7. **Precision theater** — confident estimates and exact orderings that the reasoning doesn't support.
8. **Missing definition of done** — no way to know when the plan is complete.

## Relationship to `fabled`

This skill is the `fabled` core loop applied to a plan as the artifact under review. For a hard or high-stakes plan, also invoke `ceh-fabled:fabled` via the Skill tool and read its decision-standards reference (verdict construction, pre-mortems) and technical-rigor reference (edge-case enumeration) for the deeper toolkit. Both skills ship in this plugin, so those files are also reachable directly at `../fabled/references/decision-standards.md` and `../fabled/references/technical-rigor.md` relative to this skill's base directory.
