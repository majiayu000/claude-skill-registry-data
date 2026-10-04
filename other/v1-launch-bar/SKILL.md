---
name: v1-launch-bar
description: Gate a built v1 to go / no-go on two recorded tests — a true stranger reaches first correct value in ≤60 seconds unaided, AND the learn-from-corrections mechanism is wired and proven to compound (the thing 95% of enterprise pilots never deliver). Output is a recorded-evidence go / no-go checklist. Fires on "are we ready to launch", "is v1 good enough", "launch bar", "go/no-go on v1", "should we ship this pilot". Not the ongoing post-launch loop or cadence (use refine-flywheel), not pilot price / terms / commercial success metric (use pilot-six-term-sheet), not defining what "working" means or the golden-set + cost spec before code (use eval-first-spec).
type: generator
supersedes: none
---

## What it does

Turns "I think we're ready" into a go / no-go decision made on recorded evidence, not opinion. It runs a built v1 against exactly two gates and passes only if both are green on tape. Gate A: a person with zero context reaches the one correct outcome in ≤60 seconds with no rescue. Gate B: the product has a wired mechanism that captures the customer's corrections and turns them into better output — proven to close at least once before launch, with a numeric week-1 → week-4 delta committed as the pilot's exit proof. The artefact is the filled `template.md`: a checklist where every row carries a recorded-evidence citation and an evidence-ladder tier. A v1 that is polished, feature-complete, and loved by everyone who has seen it still fails if a true stranger stalls or the corrections loop is not wired. Feature-completeness is not a gate here. The two tests are.

## The Icarus reframe

95% of enterprise pilots ship a static tool: it does the same thing in week 4 as in week 1, and every edit the customer makes vanishes into a log nobody reads. That is the death shape, and it passes most launch reviews because the review scores polish and demos, not learning. This skill absorbs `evidence-driven-testing` — proof over prose, one recorded assertion per state change, show the old failure beside the new success — and points it at the launch decision itself, not at a single UI test. The 60-second test is a recorded session with a real stranger (behaviour observed, 0.7 on the ladder), never the fellow's "it's obvious" (opinion, 0.1). The corrections test reuses that skill's strongest move — the before/after that shows the old wrong output next to the new corrected one — and applies it to the whole product's ability to learn: seed one real correction, show the same input now yields the corrected output, on tape. A launch decision made on the fellow's confidence has measured nothing.

## When to use / When NOT

Use when a v1 is built, real users are lined up, and its eval pass rate at the chosen autonomy level (from `eval-first-spec`) is already met — and the fellow needs to decide go or no-go on the pilot. Trigger phrases: "are we ready to launch", "is v1 good enough", "launch bar", "go/no-go on v1", "should we ship this pilot".

Do not use when:

| Request | Belongs to |
|---|---|
| "How do we keep improving the product / what's the monthly cadence / run the loop / what happens after launch" | `refine-flywheel` (08). This skill is the one-time gate and wires the mechanism; that skill runs it forever and measures the delta this skill commits to. Hand the pilot over once it is GO. |
| "How do we price the pilot / what are the terms / set the commercial success metric" | `pilot-six-term-sheet` (07, sibling). Its success metric is the business KPI the customer buys; the two launch tests here are the product bar underneath it. |
| "Define what working means / write the golden set / what's the cost-per-outcome" | `eval-first-spec` (07, sibling). That is the pre-build spec. This skill assumes its pass rate is already an input, and does not re-derive it. |
| "How should we run the user observation / who watches / how do we avoid leading" | `usability-test-protocol` (05). Route the *how* of the stranger observation there; this skill owns the *gate*, not the protocol. |

Do not invent readiness. If there is no built v1, or no real users to show it to, this is not a launch question yet. Say so and name the earlier step. Never fabricate a stranger session, a correction, or a delta.

## Method

Fill in `template.md`. Two gates, then the decision and the handoff. Every row needs a recorded-evidence citation; a row backed only by opinion scores 0.1 and counts as RED.

### Step 0 — Confirm you have something to gate

Three preconditions, all `[Fact]` or this stops:

| Precondition | If missing |
|---|---|
| A built, running v1 a stranger can touch | Not a launch question. Go back to build. |
| The one **outcome unit** the v1 promises (borrow it from `eval-first-spec`'s job line) | No target for the stranger to reach. Get the job line first. |
| Eval pass rate at the chosen autonomy level already met | The eval gate is upstream; do not launch under it. Route to `eval-first-spec`. |

On a vague or underspecified request, do not dump all three preconditions at once. Lead with the single unblocking ask — *point me at the running v1 and name the one outcome a stranger must reach* — and pull the rest only once that lands.

### Step 1 — Gate A: the 60-second stranger test

A stranger reaches first correct value in ≤60 seconds, unaided, and can restate the job in one sentence.

Rules that make it real, not a friendly demo:

- **Who counts as a stranger.** Matches the real user role; has never seen the product, the deck, or a description of it. Disqualified: the fellow, anyone on the build/design team, the champion, anyone briefed. A friendly who already knows the answer is not a stranger, and their success is opinion (0.1), not behaviour.
- **The clock.** Start at first contact with the artefact. Stop at first *correct* outcome — the outcome unit from Step 0, not "clicked around" — or at 60 seconds, whichever comes first. Record the session.
- **No rescue.** The fellow may not explain, hint, or drive. If the stranger needs narration to proceed, the run is a fail, recorded as such. Route the observation discipline (no leading, observe the artefact not the person) to `usability-test-protocol`; do not restate it here.
- **Two separate checks per stranger:** (1) *comprehension* — one correct sentence on what it does; (2) *first value* — reached the correct outcome in time. A stranger can stumble into value without understanding, or understand without valuing; both must be true.

| Metric | Bar |
|---|---|
| Strangers run | ≥ 3 (one success is luck; a pattern needs a few) |
| Reached correct first value ≤ 60 s, no rescue | ≥ 2 of 3 |
| Restated the job in one correct sentence | ≥ 2 of 3 |
| Evidence | Recorded session per stranger, cited [Fact] |

Gate A is GREEN only on recorded strangers. "Everyone who's seen it gets it instantly" is disqualified input — those people are not strangers, and the claim is opinion.

### Step 2 — Gate B: the learn-from-corrections test

The product must visibly improve from the customer's corrections. At the gate you cannot yet have week-4 data, so score readiness now and commit the delta to week 4. Five rows; every one must be present.

| # | Row | What green looks like | Gate-time evidence |
|---|---|---|---|
| B1 | **Capture wired** | A code path logs every correction as a `(system_output → human_final)` diff — the edit the customer made before using the output. | Cite the path / event. Not "we can query the DB later." [Fact] |
| B2 | **Feedback path named** | A named route by which a captured correction changes future output: into the golden set, a `lessons.md`, retrieval, or a re-prompt — with the trigger that fires it. | Name the path and trigger. "We'll look at the logs" is RED. [Fact] |
| B3 | **Proven once** | Seed one real correction, then show the same input now produces the corrected output. Recorded before/after — old wrong beside new right. | Recorded diff, cited [Fact]. Behaviour observed, 0.7. |
| B4 | **Tweak-time instrumented** | The metric "how much the customer edits before accepting" is captured from day 1 (tweak-distance / tweak-time). This is the instrument `refine-flywheel` will read. | Cite the instrument. [Fact] |
| B5 | **Delta committed** | A specific, checkable week-1 → week-4 promise on a named metric, e.g. "median tweak-distance on the top-5 recurring input types drops ≥ 30%". | The number and metric, stated now. [Hypothesis] until week 4. |

Kill rule for Gate B: if B1–B4 are not all present and B5 is not a specific number, the mechanism is not wired and the launch bar is **NO-GO**, however good the output looks. "We'll add the feedback loop after launch" is exactly the static-tool trap; a promise to build the mechanism later is not the mechanism.

### Step 3 — The decision

| Gate | State | Basis |
|---|---|---|
| A — stranger | GREEN / RED | Recorded strangers only |
| B — corrections | GREEN / RED | B1–B5 all present |

Both GREEN on recorded evidence → **GO**. Either RED → **NO-GO**, and name the single smallest fix that turns it green (e.g. "run 3 true strangers", "wire B1 capture", "seed one correction and record the before/after"). A gate that is "green" on opinion (0.1) rather than recorded behaviour (0.7) is RED. Do not average the two gates into a score; both are hard.

### Step 4 — Handoff

On GO, the mechanism wired in Gate B is now run continuously by `refine-flywheel` (08): it reads the tweak-time instrument (B4), re-runs the whole eval set on every model release, and promotes autonomy by eval result. The week-1 → week-4 delta committed in B5 is that skill's first checkpoint. This skill's job ends at the gate; do not run the ongoing loop here.

## Evidence standard

Every Icarus skill weights behaviour and money over opinion. The ladder:

| Signal | Score |
|---|---|
| Money moved | 1.0 |
| Behaviour observed | 0.7 |
| Artefact shown | 0.5 |
| Verbal commitment | 0.3 |
| Opinion | 0.1 |

The launch bar refuses to pass a gate on anything below behaviour observed (0.7). A recorded stranger reaching the outcome is behaviour (0.7) and clears Gate A; "users tell us it's intuitive" is verbal commitment or opinion (0.1–0.3) and does not. A recorded before/after showing a correction was learned is behaviour (0.7) and clears B3; "the model will pick it up over time" is a hypothesis, not a proof, and does not. The committed delta (B5) is tagged `[Hypothesis]` until week 4 makes it `[Fact]` — that is honest, because the gate cannot yet observe the future; what it can and does require is that everything gate-time (B1–B4, both Gate A checks) is `[Fact]` on tape. Tag every readiness claim. A launch decision is the last place to let an opinion wear the costume of a fact.

## Gotchas

The friendly stranger. The most common cheat is running the "stranger" test on a colleague, an advisor, or the champion — someone already carrying context. Their instant success is worthless as evidence and disqualified as input. If the fellow cannot name three people who have genuinely never seen it, Gate A has not been run.

The static tool that demos beautifully. A v1 can pass every polish check, win the room, and still be the 95% death shape — because nothing in it learns from a correction. Gate B is the only defence, and it is the gate fellows most want to skip because it is invisible in a demo. No B1–B4 wired, no launch, regardless of Gate A.

Delta that cannot be judged. "It'll get better over the pilot" is not a B5 commitment. Without a named metric and a number, week 4 cannot tell success from drift, and `refine-flywheel` inherits a promise it cannot check. Force the number now.

Comprehension smuggled in as value. A stranger who says "oh I see, it's a risk list" has passed comprehension, not value — they have not yet reached the outcome. Scoring the two as one lets a clear-but-useless v1 pass. Keep them separate.

Corrections that quietly raise autonomy. The Gate B loop learns from corrections to improve *output quality* at the current autonomy level — it must never silently promote autonomy (loosen a gate, drop a sign-off, widen a threshold) because the corrections looked good. A correction that implies more autonomy is a decision for `guardrail-design` (re-size the guard) or `refine-flywheel` (promote on a scored eval), never an automatic effect of the week-1 → week-4 loop. Wiring the loop to auto-tighten thresholds is exactly the trap on an L0 safety product: the mechanism that earns trust must not also spend it.

Launching under the eval gate. This skill sits on top of `eval-first-spec`'s pass rate; it does not replace it. A v1 that is charming to strangers but fails its own golden set is not ready — Gate A does not buy back a failing eval. Confirm the precondition in Step 0.

## Examples

`examples/sample.md` — a full worked launch bar for Azraq's data-centre risk product: Gate A run on three operations engineers who had never seen it (2 of 3 reached the correct top-risk read in ≤60 s), and Gate B initially RED because the monthly report was a static PDF with no correction capture — the classic 95% trap — forcing a NO-GO, the one wired fix (log the client's markups as diffs and feed them to the golden set + retrieval), a seeded before/after proving the loop closed, and a committed week-1 → week-4 delta before the decision flipped to GO.

## Related skills

`eval-first-spec` (07, sibling) — defines what "working" means before code (job line, 20 golden cases, cost-per-outcome). Its pass rate is a precondition to this gate, not something this gate re-derives. Run it first, upstream.

`pilot-six-term-sheet` (07, sibling) — carries the commercial terms and the business success metric of the pilot. The two launch tests here are the product-readiness bar beneath that metric. Keep the boundary: price and terms there, go/no-go here.

`usability-test-protocol` (05) — the discipline for running the stranger observation (Product runs, Design notes, no leading, observe the artefact not the person). Route the *how* there; this skill owns the *gate* and the 60-second binary.

`refine-flywheel` (08) — the ongoing loop this skill hands off to on GO. It reads the tweak-time instrument (B4), re-runs evals on model release, and measures the week-1 → week-4 delta (B5). This skill wires and proves the mechanism once; that skill runs it forever. They compose; neither restates the other.

Absorbs and reframes `skills/product-verification/evidence-driven-testing`. It lifts that skill's bones — proof over prose, one recorded assertion per state change, show the old failure beside the new success, always cite the exact version tested — and points them at the launch decision: the stranger session and the correction before/after are the recordings, and the go/no-go is the annotated result. Use this at the launch gate; use the original when recording proof of a single UI change on a PR.

Supersedes: none. New skill; no prior launch-bar exists in the pack.
