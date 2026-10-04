---
name: pressure-test
version: 0.1.0
license: MIT
description: Use when an idea, plan, design, or scope needs to be stress-tested before anyone builds it, when the user says "pressure test this", "poke holes in this", or wants the fuzzy parts made concrete. Also use in sous mode when the user hands off and says to answer the open questions yourself, figure it out, or that they are going AFK.
---

# pressure-test

The gate between "I have an idea" and "here is a plan." A plan only earns the build when its load-bearing decisions are explicit and its unresolved branches are closed. This skill drives toward that, one decision at a time, and refuses to let a vague idea coast into implementation on momentum.

Two modes, one job. In **interactive mode** the user answers. In **sous mode** the user has stepped away and the agent answers in their place, on the record. Either way the deliverable is the same: a set of decisions someone can build from, each one traceable to why it was made.

## The mechanic that makes this work

Every decision gets pinned to its basis. That pin is the whole point, it is what separates a real decision from a guess wearing a confident voice.

- In interactive mode, the basis is the user's answer. You propose, they confirm or redirect, you record what they chose.
- In sous mode, you supply the basis and you label it honestly, one of: `evidence` (something you inspected this session: the repo, docs, a tool's `--help`, an upstream project), `stated-constraint` (the user's own prior decisions or stated limits), or `judgment` (your best call, nothing verifiable behind it). A decision built on more than one gets split labels naming the unverified part, like: `evidence+judgment (the endpoints are from the load report; the 300ms target is mine)`.

A raw limit the user stated is `stated-constraint`; a conclusion you drew from it is `judgment`. "The ADR forbids new datastores" is stated-constraint; "so reusing the existing Redis is fine" is judgment built on it. Recalled knowledge you could not re-confirm this session is `judgment`, not `evidence`. Collapsing these distinctions is the one dishonest move this skill exists to prevent.

## How to run it

Work the decisions in dependency order, never as a questionnaire dump. Resolve the upstream decision before the ones that hang off it. Before asking anything, check whether the repo, docs, or files already answer it, an answer you can read is not a question you should ask.

A workable spine, when nothing more specific suggests itself. Treat it as a dependency tree, not a checklist to march through: 1 and 2 gate everything, 3 and 4 fall out of them, and 5, 7, and 8 are outputs you derive last, not parallel questions to ask first.

1. The actual problem, stripped of the proposed solution.
2. Who has it, and who decides whether it is solved.
3. What "done" looks like, concrete enough to test.
4. Which constraints are real versus assumed.
5. The explicit non-goals.
6. The decisions most likely to be wrong or expensive to reverse.
7. What can be deferred without blocking the first move.
8. The smallest credible thing to build first.

Push back on anything vague, self-contradictory, or driven by vanity rather than the problem. Stop the moment the remaining uncertainty no longer changes what gets built. Pressing a plan that is already settled is its own failure.

## Sous mode (the handoff)

Triggered when the user says some form of "answer your own questions", "figure it out", "I'm going AFK", or goes quiet after authorizing autonomous work. The sous chef now makes the calls the user would have, and leaves a record they can audit on return.

1. Generate the same decisions you would have surfaced interactively, in the same dependency order.
2. Resolve each yourself, preferring in this order: evidence, then the user's stated constraints and past decisions, then conservative judgment. Inspect before you assume.
3. Record every decision with its basis label. This Q&A transcript is part of the deliverable, not scratch work.
4. Float the one to three calls most likely to be overturned if the user disagrees to the top, so those are the first things they review.
5. **Stay in bounds.** A decision that commits to something destructive, public-facing, paid, breaking, brand-defining, or otherwise hard to reverse is not yours to make. Adding a library to a prototype is in bounds; provisioning a paid managed service is not. Park the out-of-bounds ones as open questions and pick the path that keeps them open. The handoff buys autonomy on reversible calls, not on the ones that cost real money or cannot be taken back.

"Build it" is not the only valid conclusion. If the evidence says the premise is wrong, the problem does not exist, or the idea is not worth it, say so. Recommending against the build is a legitimate sous-mode outcome, not a failure to decide.

Sous mode produces decisions the user can see and challenge, never decisions made silently in their name. Save the transcript alongside the work, for example `docs/decisions/<date>-pressure-test.md`.

## Rules

- One decision at a time. No wall-of-questions, no wall-of-assumptions.
- Never ask what the repo or conversation already answers. Inspect first.
- Never let `judgment` masquerade as `evidence`. The label is the honesty mechanism.
- Stop when the answer is clear enough to act. Theater is not rigor.
- In sous mode, when in doubt about whether a call is in bounds, it is not. Park it.

## Output shape

Both modes end with:

- **Decisions** (in sous mode, each tagged `evidence` / `stated-constraint` / `judgment`)
- **Open questions** (in sous mode, everything parked as out of bounds, with the riskiest calls flagged at the top)
- **Recommended next step**

Blunt, useful, short.

## Common mistakes

- Running it as an interview script instead of following the dependency tree, asking question 4 before question 1's answer reshapes it.
- Asking the user what a `grep` would have told you.
- In sous mode, quietly upgrading a guess to a fact by dropping the `judgment` label.
- Making a destructive or public-facing call in sous mode because it "seemed obvious", the threshold for parking is reversibility, not confidence.
- Pressing past the point of decision, turning a sharp plan into a stalled one.
