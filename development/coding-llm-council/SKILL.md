---
name: llm-council
description: Convene an internal "council" of distinct senior-engineer personas to analyze a problem, stress-test an approach, and produce an implementation plan before writing code — grounding the decision in up-to-date online research (current library/API versions, vendor pricing and limits, regulatory rules) rather than stale training data. Use this whenever the user is analyzing a system, weighing architectural or design trade-offs, planning a non-trivial feature or refactor, evaluating a library/tool/vendor choice, debugging something whose root cause is unclear, or asks to "think through", "plan", "analyze", "research", "review the approach for", or "figure out how to build" something — even if they don't say the word "council". Trigger it especially for decisions that are expensive to reverse (data models, API contracts, infra, auth, migrations) or that depend on external facts that may have changed. Do NOT trigger for trivial one-liners, straightforward lookups, or when the user just wants code written for an already-decided approach.
---

# LLM Council

Convene a small council of opinionated senior engineers inside a single response. Each has a distinct mandate and is allowed — expected — to disagree. The goal is to surface the strongest objection _before_ code is written, not to manufacture consensus. This is for analysis and planning, not for rubber-stamping.

## When to run this

Scale the effort to the stakes — this is the most important rule in the skill. A **full council** is for decisions that are expensive to reverse or genuinely uncertain: data models, API/contract design, auth, migrations, infra topology, build-vs-buy, vendor/library selection, or any "how should I implement X" where more than one credible approach exists. Most questions don't need that. Default to a **light council** — 2–3 relevant lenses, a few lines each, straight to a verdict, skipping the adversarial pass — and reserve the full ceremony for calls that actually warrant it. Skip the council entirely for trivial or already-decided work. When unsure, start light; you can always escalate mid-flow if the problem turns out to have teeth.

If the request is under-specified in a way that changes the answer (unknown scale, unknown constraints, unclear success criteria), ask **one** sharp clarifying question first, then proceed. Don't stall the council waiting for perfect information — state assumptions explicitly and move.

## The council

Convene the members whose mandate is relevant. Not every problem needs all of them; pick 3–5. Each member is a lens, not a costume — keep them terse and technical.

- **The Architect** — owns structure and boundaries. Cares about coupling, data flow, where state lives, contract stability, and whether this fits the existing codebase cleanly. Asks: what's the smallest design that survives the next three requirements?
- **The Pragmatist** — owns shipping. Cares about scope, time-to-working, and the boring path. Actively resents complexity that isn't paying rent. Asks: what's the 20% that gets 80%, and what can we defer or delete?
- **The Skeptic** — owns failure modes. Cares about edge cases, race conditions, partial failures, idempotency, data integrity, security, and the claim you didn't verify. Asks: how does this break in production, and what's the blast radius?
- **The Operator** — owns life after deploy. Cares about observability, migrations, rollback, cost, rate limits, cold starts, and on-call pain. Asks: how does whoever is on call debug this at 2am?
- **The Domain Specialist** — convened when the problem has real domain weight (payments, auth/identity, compliance/tax, ORM and migration semantics, concurrency, LLM/agent orchestration, or whatever the specific domain of the task is). Brings the specific constraint the generalists would miss.
- **The Researcher** — owns "what does reality actually say?". Refuses to let the council reason from stale training data on anything that changes: current library/API versions and their breaking changes, framework defaults, vendor or platform pricing/limits/behavior, regulatory rules, and whether a "known" fact is still true. Their job is to name the load-bearing claims that need verifying and to go verify them (web_search / web_fetch of primary sources — official docs, changelogs, vendor pages, regulator sites) before the verdict rests on them. Convene the Researcher whenever the decision depends on any external fact that could have drifted since the knowledge cutoff.

You may add a bespoke member for a specific problem (e.g. "The Cost Modeler" for unit-economics questions). Name it and give it a one-line mandate.

## Process

These phases are a checklist to draw from proportionally, not a rigid march — a light council might be Frame → one-line deliberation → Verdict in four sentences, while an irreversible migration earns every phase. Research in particular isn't a fixed step: pull a fact the moment a claim becomes load-bearing, wherever in the flow that happens. Keep the whole thing tight — this is a thinking tool, not a performance.

### 1. Frame (scan context first)

Before framing, spend a moment grounding the council in the _actual_ codebase rather than generic best-practice — this is where an engineering council beats a strategy one, because the context is verifiable ground truth, not vibes. Quickly pull the few things that would change an advisor's answer:

- Project docs (a `CLAUDE.md`, `README`, or `docs/` note if present) and the specific schema, module, endpoint, or config the decision actually touches — read the real code, don't reason about an imagined version of it.
- Adjacent code that constrains the design: existing patterns, migration history, and how similar problems were already solved in this codebase.
- Any prior decision record on the same question (see phase 8), so you build on it instead of re-litigating settled ground.

Use whatever's available — the filesystem, a codebase-memory/search MCP if one is connected, or the user's attachments. Timebox it; grab the 2–3 files that matter, not everything. Adapt to whatever stack, language, and conventions the project uses rather than assuming any particular one.

Then state the problem in one or two sentences in your own words, list the assumptions you're making, and name the decision that actually has to be made. If you're inferring context (stack, scale, constraints), say so explicitly so the user can correct you.

### 2. Candidate approaches

Lay out 2–4 genuinely distinct approaches, not one approach and two strawmen. For each: a one-line summary and its core trade-off. If there's an obvious default, still articulate at least one real alternative — the point is to make the choice visible.

### 3. Research the load-bearing unknowns

Before deliberating, identify the facts the decision actually rests on that could be wrong or stale, and verify them online rather than reasoning from memory. This is not optional whenever an external fact is doing real work in the decision.

- **What to verify:** current versions and breaking changes of any library/framework in play; a tool's actual current API, defaults, or config; vendor pricing, rate limits, quotas, and documented behavior; regulatory/tax/compliance rules; whether a "well-known" fact is still current; prior-art and whether the thing already exists as an off-the-shelf solution (build-vs-buy).
- **How:** prefer primary sources — official docs, GitHub releases/changelogs, vendor pages, regulator/government sites, RFCs, the source repo itself — over blog aggregators and forum lore. Use `web_search` to find them and `web_fetch` to read the actual page; a snippet is not verification. Use the current year in queries, not a remembered one.
- **Scope the effort to stakes:** a reversible internal helper may need zero or one lookup; a payments, migration, or vendor-selection decision may warrant several. Don't boil the ocean — verify what changes the answer, skip timeless fundamentals you already know.
- **Report it:** briefly note what you checked and what you found (with the source), and flag anything you _couldn't_ confirm so the council treats it as an assumption rather than a fact. If a search contradicts what the plan assumed, that finding feeds straight into deliberation.

If no external fact is load-bearing (pure local reasoning over the user's own code), say so in one line and skip to deliberation.

### 4. Council deliberation

Give each convened member a short, pointed take. They should reference each other and disagree where they genuinely would. Format as:

> **Architect:** <take>
> **Skeptic:** <objection, ideally to the Architect's take>
> ...

Rules that make this useful rather than theater:

- Every member must say something that could change the decision. If a member has nothing load-bearing to add, drop them.
- Don't manufacture disagreement. If a plan is genuinely robust, say _why_ it holds — that's a useful signal in its own right. But treat a total absence of objections with suspicion: it usually means the failure modes weren't probed hard enough, not that none exist. Send the Skeptic back in before concluding there's nothing to worry about.
- No vague hedging ("it depends", "consider the trade-offs"). Name the actual condition, the actual failure, the actual cost.
- Cite specifics from the actual codebase and constraints when relevant rather than generic best-practice.
- Ground claims in research. A member asserting a version behavior, a vendor limit, or a rule that wasn't verified should be challenged and sent to check rather than waved through.

### 5. Adversarial pass (full council only)

This is what turns a set of labeled opinions into an actual decision — inspired by Karpathy's peer-review round, but honest about the adaptation. In his setup, genuinely separate models review each other blind. Here a single reasoner ran every lens and now reviews them, so this is self-critique, not independent review — and it can't pretend otherwise. Its value isn't simulated objectivity; it's forcing a real second look that attacks the leading answer instead of defending it.

Do it deliberately: set aside which lens said what, and judge the _positions_ on merit. Answer three questions:

1. Which position's reasoning is actually strongest — on the merits, not because of which lens carried the most authority?
2. Which has the biggest hidden flaw or unstated assumption, and what is it?
3. What did _every_ position miss that still matters?

Question 3 earns its keep — it surfaces the blind spot no single lens produced. Whatever it turns up feeds straight into the verdict. If the pass exposes that the strongest-sounding position rests on an unverified external fact, stop and verify it before deciding. Skip this on a light council; with two lenses there's nothing to pit against each other.

### 6. Verdict

Synthesize into a single recommendation. State: the chosen approach, _why it won_ over the alternatives (including what the adversarial pass changed, if anything), the top 1–3 risks that remain (and how to mitigate or detect them), and what you're explicitly choosing NOT to do (deferred scope). Cite the sources that settled any contested external fact. The verdict may side against the loudest lens if its reasoning turned out weakest. If the council genuinely couldn't converge, say so and name the one piece of information that would break the tie — and if that's externally knowable, go look it up rather than punting.

On an expensive or irreversible decision, stop here and let the user weigh in before you plan or build. Present the verdict, note that you can proceed to a plan on request, and wait — the point of the council is to inform _their_ call, not to commit the codebase in one uninterrupted response. On lighter calls where the path is now obvious, flowing straight into the plan is fine.

### 7. Implementation plan (when the task calls for building)

Produce an ordered, checkable plan:

- Break work into small, independently verifiable steps in dependency order.
- For each step: what changes, which files/modules/tables, and the **check** that proves it worked — an observable verification (a test that passes, a command whose output you can read, a concrete behavior you can see), never a rubber-stamp like "confirm it works." If a step can't be verified, that's a design smell worth calling out.
- Call out migrations, contract changes, and anything irreversible with a ⚠️ and a rollback note.
- Flag the riskiest step and suggest doing a thin end-to-end slice first if the risk is integration-level.
- Note where a spike or a quick verification search is warranted before committing (e.g. confirming a library's current API, a vendor's actual behavior, a tricky edge case) rather than assuming.

Keep the plan a plan — don't start writing the implementation unless the user asks. End by offering to start on step 1 or to adjust the plan.

### 8. Persist the decision (optional, for consequential calls)

For decisions worth revisiting — architecture, migrations, vendor/build-vs-buy, anything you'll want to reconstruct later — offer to save a short record so a future session builds on it instead of re-litigating. Keep it terse: the framed problem, the candidate approaches considered, the verdict and _why_, the risks accepted, and what was deferred. A dozen lines, not a transcript dump.

Write it where the project already keeps such notes (e.g. `docs/decisions/` or an ADR file if the repo uses them, or wherever the user's convention points). This doubles as a lightweight ADR and as retrievable memory for the next council on the same ground — so when the same decision resurfaces after a change, phase 1 can pick it up and pick up where this left off. Only do this when asked or when the stakes clearly warrant it; skip it for routine calls.

## How to present it

The visible output mirrors the phases, minus the internal mechanics (don't narrate context-scanning or show raw search steps — fold findings in where they matter). Use this as a default skeleton, not a rigid template — drop sections that didn't earn their place:

- **Frame** — the problem restated, assumptions, the decision to be made.
- **Approaches** — the 2–4 candidates with their core trade-offs.
- **Deliberation** — the sharp, load-bearing exchange between lenses (the distilled version, not every thought). Format as `> **Lens:** take`.
- **Adversarial pass** — strongest position, biggest hidden flaw, what everyone missed. Full council only.
- **Verdict** — the recommendation, why it won, residual risks, deferred scope, sources for any contested fact.
- **Plan** — the ordered, checkable steps, when building.

A light council collapses this to a few sentences: a one-line frame, the call, and why. Match the format's weight to the decision's weight — a heavy scaffold on a small question is its own kind of failure.

## Style

- Prose and tight sub-points over heavy formatting. The deliberation block is the one place structure earns its keep.
- Be direct and technical; assume a capable engineer reading. No filler reassurance.
- Verify, don't assert. If a claim about a tool, version, API, vendor behavior, or regulation is load-bearing and could have changed, _search for it_ rather than stating it with false confidence — this matters most for anything touching money, security, auth, or data integrity. Reasoning confidently from stale training data is the failure mode this skill exists to prevent.
- Match depth to stakes: a reversible internal helper gets a light council; a payments or migration decision gets the full treatment.
- The council serves the decision. If partway through it's clear the real answer is "don't build this yet" or "the premise is wrong", say that plainly — a good council is willing to kill the idea.

## Worked example (abridged)

A compact full-council run, to show the target shape. Real ones go deeper; this is the skeleton in motion.

**Prompt:** "We call a third-party enrichment API on every profile view — it's slow and we're near the rate limit. Should we cache it, and where?"

**Frame:** Decision is whether to add a cache and at which layer, given an external dependency that's both latency- and quota-constrained. Assuming reads vastly outnumber writes and slightly-stale data is tolerable (needs confirming with the user).

**Approaches:** (1) In-process memory cache — trivial, but per-instance and lost on deploy. (2) Shared cache (Redis/equivalent) — survives deploys, coordinates across instances, adds an operational dependency. (3) Persist enriched data in the primary DB, refresh on a schedule — most durable, decouples reads from the API entirely, but staleness is now a product decision.

> **Architect:** Approach 3 changes the data model — enrichment becomes owned state, not a passthrough. That's the cleanest boundary if the data has a natural refresh cadence, but it's the biggest commitment.
> **Pragmatist:** Approach 2 gets 80% of the win for a fraction of the cost. Don't restructure the data model to dodge a rate limit you could solve with a shared cache and a TTL this afternoon.
> **Skeptic:** All three hand-wave the invalidation. What's the staleness tolerance in _hours_? If enrichment drives anything user-visible or billable, a silent stale read is a correctness bug, not a cache miss. And what's the failure behavior when the cache is cold _and_ the API is rate-limited — do reads block, error, or serve stale?
> **Operator:** Approach 2 adds a dependency I now have to monitor and that becomes a new outage mode. Fine if it already exists in the stack; a real cost if I'm standing Redis up solely for this.

**Adversarial pass:** Strongest is the Pragmatist's — a shared cache with a TTL matches the actual constraint without over-committing. Biggest hidden flaw, surfaced by the Skeptic: every approach dodged the staleness _number_, which is the load-bearing unknown — without it the choice is unanchored. What all missed: the rate limit means the _cold-cache stampede_ is the real risk (many simultaneous misses all hitting a throttled API); the fix (single-flight / request coalescing) is orthogonal to which cache layer wins.

**Verdict:** Shared cache with a TTL derived from the staleness tolerance, plus request coalescing so concurrent misses collapse to one upstream call — _if_ a shared cache already exists in the stack; otherwise start with in-process caching + coalescing and revisit. Chosen over the DB-persistence approach because nothing yet justifies making enrichment owned state; revisit that if the API becomes a permanent source of record. **Residual risk:** stale reads — mitigated by setting the TTL from a real tolerance, not a guess. **Deferred:** DB persistence, cache warming. _This is an expensive-enough call to stop here and confirm the staleness tolerance and whether a shared cache exists before planning._
