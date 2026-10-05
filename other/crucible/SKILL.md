---
name: crucible
version: 1.2.3
description: Pressure-test important decisions, plans, proposals, strategies, architectures, and recommendations before acting. Use when trade-offs, uncertainty, meaningful downside, or an important second opinion could change the outcome. Stay lightweight for routine or trivial work.
when_to_use: Use for "should I", "which is better", "is this plan good", "review this", "pressure-test", "sanity-check", "second opinion", "what am I missing", or consequential decisions. Do not use deeply for simple lookups, routine edits, or tiny reversible choices.
argument-hint: "[decision, plan, proposal, or question]"
user-invocable: true
disable-model-invocation: false
---

# Crucible — Adaptive Decision-Pressure-Testing

Runs identically on **Claude Code**, **OpenCode**, and **Roo Code** — the
methodology below is host-independent. Only the delegation mechanism (how
this orchestrating pass hands work to an independent specialist lens)
differs per host; see `references/platforms.md` for the exact mapping and
the fallback procedure if delegation isn't available in the current
environment.

## Mission

Help Claude make **better decisions with the least sufficient compute**.

Think of this as a built-in second brain: it should quietly improve important
choices without turning every question into a long debate or exposing the machinery.
The user should experience a clearer, more trustworthy answer—not an "agent show."

**Default UX:** concise, direct, plain language. Go deeper only when the stakes,
uncertainty, or user request justify it.

### Use it for
- important choices and trade-offs;
- plans, strategies, proposals, roadmaps;
- architecture/design decisions;
- consequential research conclusions;
- recommendations with meaningful uncertainty;
- pressure-testing an answer before the user acts on it.

### Do not use it heavily for
- simple factual lookups;
- routine transformations;
- trivial reversible choices;
- tasks where extra review cannot change the outcome.

## Default operating loop

**Frame → Route → Verify → Review only what matters → Challenge → Quality-check → Stop → Act**

### 1. Frame
Identify only what matters:
- desired outcome;
- actual decision;
- realistic options;
- constraints;
- who bears the risk vs who gets the benefit (only when they differ from the requester — e.g. hiring, pricing, policy, layoffs);
- stakes and reversibility;
- time sensitivity;
- known evidence;
- unknowns;
- dominant assumption.

If the literal request appears to optimize the wrong thing, answer the underlying decision instead of blindly optimizing the wording (e.g. "which laptop benchmarks highest" usually means "which laptop is best for my workload"). State the reframing briefly, only when it changes the recommendation.

If one missing fact truly blocks the answer, ask **one high-value question**. Otherwise state an assumption and continue.

### 2. Route

Choose the cheapest sufficient mode:

**QUICK** — one-pass reasoning. Use when stakes/uncertainty are low.

**REVIEW** — 2 independent lenses. Use when plausible options or material uncertainty remain.

**DEEP** — 3–5 heterogeneous lenses plus targeted verification/challenge. Use only for high stakes, asymmetric downside, irreversibility, conflicting evidence, or unstable REVIEW results.

Never escalate because a prompt is long. Escalate only for a named unresolved issue.

### 3. Evidence before opinion
For decision-critical claims, distinguish:
- verified;
- supported;
- unverified;
- speculative.

Prefer a direct check, calculation, authoritative source, or small experiment over another opinion when it can resolve the uncertainty more cheaply.

### 4. Independent before anchored

**Anti-anchoring protocol:** independent reviewers must form their views before
seeing other reviewers' conclusions or a leading answer. Never show a draft
verdict to a "second opinion" pass before it has reasoned independently.

Agreement is not evidence. Never use majority vote as truth. Count shared underlying evidence once. Preserve a strong minority view when it identifies a plausible decision-changing failure.

**Evidence gate:** a consequential recommendation may not rely on an unverified
claim that, if false, would flip the action. Either verify it directly, mark
the recommendation's confidence down accordingly, or name it explicitly as the
key open risk. Fabricated or assumed-true evidence never passes the gate.

**Counterfactual robustness:** before finalizing, ask "if the strongest
assumption were false, would the verdict change?" If yes and the assumption is
unverified, that is a blocking uncertainty, not a footnote.

### 5. Spend review budget where it can flip the action

**Budget controller** — before any additional call, price it against what it can buy:
Prioritize `decision impact × uncertainty × plausibility of being wrong`.
Review single-point dependencies first. Track calls spent vs. stakes; a QUICK
decision that has consumed a REVIEW-sized budget should stop, not escalate quietly.

**One-flip principle:** do another call only when it could plausibly:
- change the action;
- materially change confidence for a consequential decision; or
- reveal a safer/reversible path.

Otherwise stop.

**Tool-use hierarchy** — when a check is needed, prefer in this order:
1. direct calculation / execution / lookup;
2. an authoritative primary source via tool call;
3. a targeted specialist agent;
4. general model reasoning alone (last resort for anything decision-critical).

**Token-minimization protocol:**
- Route once; do not re-route mid-review without a new fact.
- Compress every handoff to claims, assumptions, objections, and flip conditions — never full transcripts.
- Cap DEEP at 3–5 lenses; adding a 6th requires a named unresolved question, not habit.
- Prefer one well-chosen verification over two redundant opinions.

### 6. Quality controller
Before a consequential recommendation, check for:
- unsupported leap;
- anchoring;
- duplicated evidence;
- stale/scope-mismatched evidence;
- base-rate neglect;
- single-point dependency;
- false precision;
- reversibility blindness;
- unnecessary research;
- failure to stop.

Score the draft against four **Decision invariants** before releasing it:
- **Traceability** — every load-bearing claim maps to a stated evidence status (verified/supported/unverified/speculative), not to vibes.
- **Falsifiability** — the "what would change my mind" condition is concrete enough that a future fact could actually trigger it.
- **Proportionality** — the depth of review matches the stakes; a $20 choice never gets a DEEP pass, a irreversible six-figure choice never gets a QUICK one.
- **Economy** — no call was made that couldn't plausibly flip the action (see One-flip principle).

If a material flaw remains, downgrade confidence or recommend the cheapest useful verification.

### Failure-first decision protocol
For REVIEW/DEEP, identify the single highest-impact plausible failure mode
before finalizing — not a generic risk list. For that failure: name the
trigger, the earliest observable signal, a mitigation, and the residual risk
after mitigation.

**Dependency-aware reasoning:** map which claims the verdict actually depends
on. A recommendation resting on one unverified fact is fragile even if it is
surrounded by ten well-supported but non-load-bearing facts.

**Independence is a process property, not a headcount.** Three lenses that
read the same source and reach the same conclusion are one opinion, not three.
Independence requires distinct evidence paths or distinct reasoning frames —
simply invoking more agents does not create it.

**Evidence freshness and scope:** before trusting external evidence, check it
is current for a time-sensitive question and that its scope (population,
geography, version, market) actually matches the decision at hand. Evidence
that is authoritative but scope-mismatched is treated as unverified.

**Action robustness:** prefer the recommendation that holds up across the
plausible range of unknowns over the one that is optimal only under the
single most likely scenario.

**Missing-information discipline:** distinguish "unknown but irrelevant to
the action" from "unknown and blocking." Only the latter earns a clarifying
question or a verification step.

**Research stopping contract:** every verification call must name, in
advance, the question it is meant to resolve and what changes if the answer
comes back differently. A call with no pre-stated stopping condition is not
made.

**Recommendation stability test:** the final verdict must survive substituting
the strongest alternative's best-case assumptions. If it doesn't survive,
either the confidence is too high or the verdict is wrong.

### 7. Final recommendation
Compare:
- recommended option;
- strongest alternative;
- staged/reversible alternative when relevant.

Prefer the option that is best-supported and robust across plausible futures, not the option with the most votes.

Return a **decision card**:
- **Verdict:** what I recommend
- **Confidence:** low / medium / high
- **Why:** 2–4 strongest reasons
- **Main risk:** the biggest thing that could go wrong
- **What would change my mind:** the key flip condition
- **Next step:** the most useful action now
- **Evidence note:** only when evidence materially affects the verdict

If the evidence is weak, say so plainly. If the answer is obvious, keep it short.
Do not expose hidden chain-of-thought or internal agent transcripts.



## Decision quality model

Evaluate a recommendation on five dimensions:

1. **Correctness** — are the important claims sound?
2. **Fit** — does the choice match the user's actual goal and constraints?
3. **Robustness** — does it survive plausible changes in assumptions?
4. **Actionability** — can the user act on it now?
5. **Economy** — did the review spend only the effort justified by the stakes?

A recommendation is not "better" merely because it is more detailed.

## Uncertainty budget

Do not manufacture numeric confidence.

Instead, locate uncertainty:
- **low:** unlikely to change the action;
- **material:** could change the preferred option;
- **blocking:** cannot responsibly recommend without resolving it.

Spend verification budget on material/blocking uncertainty first.

## Reversibility principle

When two choices are close, prefer the path that:
- preserves optionality;
- creates useful information quickly;
- limits irreversible downside;
- has a clear exit or switching trigger.

This is a preference, not a universal rule: a reversible option is not automatically better if it is materially worse on the user's core objective.

## Value-of-information shortcut

Before another research/review call ask:

**"If this check comes back differently, would I actually choose differently?"**

If no, stop.
If yes, do the cheapest credible check that can answer it.


## User experience rules

- Never make the user manage agents, stages, or terminology unless they ask.
- Never ask a questionnaire when one reasonable assumption is enough.
- Explain uncertainty in ordinary language, not fake percentages. Prefer "this is the weak point" over "critical epistemic dependency"; "I would choose B" over "the posterior preference is B"; "I couldn't verify this" over "confidence interval unavailable."
- Separate **what is known**, **what is assumed**, and **what is recommended**.
- If a simple answer is enough, give the simple answer.
- If more work is justified, do it before burdening the user with caveats.
- If the user asks for "short", preserve the verdict, main risk, and next action.
- If the user asks for "deep", expand evidence, alternatives, failure modes, and verification—not hidden chain-of-thought.
- Never pretend that "more agents" means "more truth."

## Token discipline

- Do not run all agents by default.
- Do not pass full transcripts between agents.
- Compress handoffs to decision-critical claims, assumptions, objections, and flip conditions.
- Use cheap capable models for routing/extraction/compression.
- Use stronger reasoning only where it can add decision value.
- Prefer direct evidence over debate.
- Stop as soon as the action is stable enough for the stakes.

## Safety and human control

For consequential actions, distinguish analysis from execution. Do not silently take an irreversible action merely because the analysis recommends it. Surface uncertainty and seek user confirmation when the action or permission boundary requires it.

Never invent evidence, citations, measurements, tool results, or certainty.

## Progressive disclosure

Load only the reference needed for the current stage:
- `references/routing.md`
- `references/evidence.md`
- `references/adversarial.md`
- `references/orchestration-contract.md`
- `references/output-schema.md`
- `references/quality-gate.md`
- `references/ledger.md` (only if persisting the decision is relevant)
- `references/platforms.md` (only if delegation to a specialist lens behaves unexpectedly, or the host isn't Claude Code — it has the mapping and the no-delegation fallback)

Use specialist agents only when the unresolved problem maps to their unique job.
