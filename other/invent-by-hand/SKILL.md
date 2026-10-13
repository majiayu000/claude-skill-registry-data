---
name: invent-by-hand
description: Invent an original product concept before the machine hands you the generic one — onion the stated idea to its invariant core need, diverge and keep the strange child, anchor every concept to your proprietary YODA corpus, then run the generic-prompt test (if the one-line prompt a competitor would type reaches your concept, it isn't yours yet). Returns an invented concept + rationale. Fires on "what should we actually build", "invent the solution", "make it non-obvious", "give me a concept a competitor couldn't just prompt for", "what's the product idea here". Not for carving and adoption-testing the first slice (use wedge-five-questions, run it next), not for finding the proprietary data the concept stands on (use yoda-data-sourcing, run it first), not for designing a cheap experiment to validate an already-chosen idea (use concierge-probe / probe-matrix, section 04).
type: interactive
supersedes: none
---

## What it does

Takes a fellow's stated idea and forces an original product concept out of it — one a frontier model would not hand to every competitor who typed the obvious prompt. It peels the idea to the single invariant need underneath, generates a divergent set of concepts instead of the first safe one, ties each to a specific row of the fellow's proprietary corpus, and then runs the test that gates the whole skill: the generic-prompt test. Write the one-line prompt a competitor with no proprietary data would type into a model. If the model's default answer lands on your concept, the concept is a commodity — the machine already gives it to everyone — and it dies. What survives is unreachable by that prompt for a nameable reason: your trapped corpus, a tacit judgment the model cannot see, or a non-obvious inversion. The output is an invented concept plus the rationale for why a generic prompt could not produce it, ready to hand to `wedge-five-questions`.

## The Icarus reframe

In the age of the machine, the danger is not that you cannot generate ideas; it is that you generate the same idea as everyone else. Ask a model "what should we build in factory operations?" and it returns the average of everything ever built there — a copilot, a dashboard, a chatbot — the one concept no one can defend, because the model will hand it to your competitor on the same afternoon. So this skill inverts the usual brainstorm: it invents *by hand first*, grounded in the fellow's own corpus, and then uses the machine only as an adversary. The rule is one line — **if a generic prompt could produce it, it isn't yours yet** — and it is enforced literally: every candidate is run against the prompt a competitor would type, and only the concepts that prompt cannot reach, for a reason you can name, are allowed to survive. The concept that survives is still a hypothesis; the test proves no competitor can prompt their way to it, not that a customer wants it.

## When to use / When NOT

Use when a fellow has a stated idea (or a validated core need and a proprietary corpus) and needs the actual thing to build — the concept — and wants it to be non-obvious rather than the default the machine gives everyone. Trigger phrases: "what should we actually build", "invent the solution", "make it non-obvious", "give me a concept a competitor couldn't just prompt for", "what's the product idea here".

Do not use when:

| Request | Belongs to |
|---|---|
| "Is this the smallest thing to build first / will it get adopted / is my wedge sharp" | `wedge-five-questions` (sibling, section 06). It carves the invented concept into the first adopted slice and tests it 5/5. Run this to invent the concept, that to test the first build. |
| "Where's our proprietary data / what data can't a competitor get" | `yoda-data-sourcing` (section 03). It finds the corpus this skill stands on. Run it first — a concept with no band-P corpus to anchor to is invention on sand, and this skill routes back there. |
| "Design a cheap experiment to validate this idea / build a pretotype" | `concierge-probe` / `probe-matrix` (section 04). That is where a chosen concept meets behaviour cheaply. This skill produces the concept worth probing; it does not design the probe. |

Also do not use it to invent a concept from a bare domain. If the fellow can only name an industry ("logistics", "safety") with no observed decision and no corpus, the input is not ready. Say so and ask the one unblocking question (Method step 1). Invent no specifics to fill the gap.

## Method

Fill in `template.md`. Six steps. The concept is a `[Hypothesis]` at every step; what carries evidence is the need it serves and the corpus it exploits.

### Step 1 — Onion to the invariant core need

Peel the stated idea until the need underneath would survive a 10x change in the underlying technology. If the "need" you land on still contains a tool, a model, or a UI word ("copilot", "dashboard", "app", "chatbot"), you have not peeled far enough — that is a solution wearing a need's clothes. Borrow the discipline of `job-in-primitives` (section 01): strip every tool, vendor, and role name until only the raw need remains.

| Layer | Statement | Tool/model/UI word in it? | Survives a 10x tech change? |
|---|---|---|---|
| 0 As stated | _[the idea in the fellow's words]_ | _[y/n]_ | _[y/n]_ |
| 1 The job | _[what work it does]_ | _[y/n]_ | _[y/n]_ |
| 2 The decision | _[the choice the user makes]_ | _[y/n]_ | _[y/n]_ |
| 3 Core need (invariant) | _[the need that does not move]_ | no | yes |

The bottom row is the launchpad. If the fellow cannot name a real decision a real person makes, stop — this is a domain, not an idea. Ask: *what recurring decision, made by whom, do you want to change?*

### Step 2 — Diverge: generate at least six, keep the strange child

Against the core need, generate at least six concepts spanning obvious → adjacent → strange. Do not converge yet. Carry at least two forward, and at least one of them must be a **strange child**: a concept that inverts the obvious (fewer alerts not more; subtract not add; say-no not answer). The strange child is kept not because weird is good, but because weird is far from the generic prompt's output — which is exactly where a defensible concept can live.

| # | Concept (one line) | Obvious / adjacent / strange | Carry forward? |
|---|---|---|---|
| 1 | _[the first thing everyone thinks of]_ | obvious | _[y/n]_ |
| … | _[…]_ | _[…]_ | _[…]_ |

If your strange child also turns out reachable in Step 4, you did not diverge far enough — go back and push harder.

### Step 3 — Anchor each survivor to the YODA corpus

Every carried concept must exploit one specific row of the fellow's proprietary corpus (a band-P source from `yoda-data-sourcing`). Name the row. A concept with no corpus anchor is not eligible — flag it, do not invent a corpus to save it.

| Concept | Corpus row it exploits (from `yoda-data-sourcing`) | Band | Evidence the corpus is real (ladder + [Fact]/[Assumption]) |
|---|---|---|---|
| _[…]_ | _[e.g. shadow-thread corrections; incident ledger; exception history]_ | P | _[≥0.5 to count — a held sample or observed flow]_ |

A corpus anchor scored at `[Assumption]` / 0.1 ("I'm sure that data exists somewhere") is not an anchor; it is a sourcing task to run first via `yoda-data-sourcing`.

### Step 4 — Run the generic-prompt test

For each survivor, write the actual one-line prompt a competitor with no proprietary data would type, state the model's default answer, and score the distance. Only D2 survives.

| Band | Test | Verdict |
|---|---|---|
| **D0 — reachable** | The generic prompt's default answer *is* this concept (a chatbot, a dashboard, an OCR tool, "an AI copilot for X"). | Commodity. The machine hands it to every competitor. Kill it. |
| **D1 — variant** | The prompt reaches a near-neighbour; your concept is a tweak (nicer UI, one extra feature) the model would also suggest if pushed. | Not yours yet. Push further, or anchor harder to the corpus. |
| **D2 — unreachable** | No generic prompt reaches it, and you can name *why*: it depends on your band-P corpus, a tacit judgment the model cannot see, a non-obvious inversion, or a structural aggregation position (a cross-party vantage no single competitor holds — e.g. a cross-operator delta no one operator can see). | Yours. Proceed — but it is still a `[Hypothesis]`. |

The "why" must be specific: the corpus row from Step 3, the inversion from Step 2, or the aggregation position named above. "It's unreachable because we're more creative" is not a why — that is a D1 in disguise. If every survivor is D0 or D1, the honest output is *this isn't yours yet*; return to Step 2 with the corpus in hand.

**Second-prompt guard (against reflexivity).** The test runs on the same model that just helped invent the concept, so a motivated pass can under-estimate what a competitor's prompt reaches in order to bless its own strange child. Before scoring anything D2, write a *second, stronger* competitor prompt — steelman the incumbent's default: hand it the obvious adjacent data, the sharper framing, and the follow-up a real competitor would type next — and confirm it still misses. A concept is D2 only if BOTH the naive and the steelmanned prompt fail to reach it; if the stronger prompt lands on it, it was D1 all along.

### Step 5 — Sketch the chosen concept by hand

Render the surviving concept as one concrete artefact — one screen, one interaction, or the thing the user physically holds — by hand, no code. React to a concrete thing, not an abstraction. This sketch is the minimum needed to close the invention loop and feed the wedge test. It is not a prototype: when the fellow wants a clickable one, route to `first-mocks` (section 05); do not build it here.

### Step 6 — State the invented concept, rationale, and kill line

Fill the final block in `template.md`: the concept in one sentence, the invariant need it serves, the corpus row it exploits, the specific reason a generic prompt cannot produce it, its status (`[Hypothesis]`), and the one observation that would change the view (the cheapest probe that would kill the direction).

**Kill line.** The output is auto-failed if the chosen concept is D0 or D1 (a generic prompt could produce it), if it has no band-P corpus anchor, or if it is simply the first obvious concept with no divergence and no strange child tested. When the kill line fires, name what is missing and route: back to Step 2 for divergence, or to `yoda-data-sourcing` for the corpus. Do not bless the obvious concept because it is tidy.

## Evidence standard

Every Icarus skill weights behaviour and money over opinion. Here is the honest part: an invented concept has moved no money and produced no behaviour yet, so the concept itself is a `[Hypothesis]` by construction — never score it as validated. What must clear the bar is not the concept but its two anchors.

| Signal | Score |
|---|---|
| Money moved | 1.0 |
| Behaviour observed | 0.7 |
| Artefact shown | 0.5 |
| Verbal commitment | 0.3 |
| Opinion | 0.1 |

The bar this skill enforces: **the core need must be observed and the corpus anchor must be a real band-P source, each ≥ 0.5.** A concept invented on an assumed need (0.1) and an imaginary dataset (0.1) is invention on sand, however non-obvious it looks. Tag every empirical claim `[Fact]`, `[Assumption]`, or `[Hypothesis]`. The generic-prompt test proves that no competitor can prompt their way to the concept; it does not prove a customer wants it. That proof is the wedge and the probe — do not let a clever D2 concept skip the adoption test.

## Gotchas

Regression to the median. Asking the machine (or a committee) "what should we build in X" returns the average of everything ever built in X, and the average is the one concept no one can defend, because the model will hand the same average to your competitor. The strange child, corpus-anchored, is where a defensible concept lives — not because weird is good, but because weird is far from the generic prompt.

Strange is not the same as good. A strange child that serves no core need or exploits no corpus is noise, not invention. Keep only the strange child that is both far from the generic prompt (D2) and anchored to a band-P row. Novelty alone fails the corpus anchor and should die in Step 3.

The corpus you do not have yet. Anchoring a concept to a proprietary source you have only assumed is inventing on sand. If the anchor is not a real band-P row with evidence ≥ 0.5 from `yoda-data-sourcing`, the concept is not grounded — go get the data first. A clever concept over imaginary data is the most seductive failure this skill catches.

Unreachable today, reachable tomorrow. Today's D2 can be tomorrow's D0 as models improve. A concept unreachable only because the current model is weak — not because of your corpus — is a D1 with a short shelf life. Anchor on the corpus the model still cannot see, not on the model's temporary blind spot.

Invention mistaken for validation. A D2 concept is unreachable, not proven. It remains a `[Hypothesis]`. Passing the generic-prompt test earns the right to run the wedge test, nothing more. The most common misread is treating "no competitor can prompt this" as "customers will adopt this."

## Examples

`examples/sample.md` — a full worked invention for Mentix's "AI copilot for factory managers": onions it to the shift-start triage decision, diverges to a strange child (a shift-start *walk order* that encodes the senior lead's ignore-list from shadow WhatsApp corrections), anchors it to that band-P corpus, and shows the generic prompt returning a Q&A chatbot (D0) while the walk-order concept sits at D2 — unreachable without the shadow-thread corpus.

## Related skills

`yoda-data-sourcing` (section 03) — supplies the proprietary corpus every concept must anchor to in Step 3. Run it first. A concept with no band-P corpus row is invention on sand, and this skill routes back there rather than inventing a dataset.

`wedge-five-questions` (sibling, section 06) — takes the invented concept and carves the smallest adopted slice, then tests it 5/5 on behaviour. The concept this skill returns is a `[Hypothesis]`; the wedge test is where it first meets behaviour. Run this to invent, that to test the first build.

`moat-design-canvas` (sibling, section 06) — the corpus row this skill requires as an anchor is the seed of the canvas's data-advantage gate. Invention grounds the moat in a real corpus before the canvas sequences it into dated gates.

`unserved-needs-finder` (section 02) — owns the full Kano-sorted need map. This skill's onion is a single-thread peel to the one invariant need to invent against, not a needs-prioritisation exercise. If the fellow wants the wide need map, send them there.

`job-in-primitives` (section 01) — strips tool/vendor/role names from the job; this skill borrows the same discipline to strip them from the *need* while peeling the onion. Reference, do not restate.

`first-mocks` (sibling, section 05) — renders a chosen concept as a clickable prototype (Crazy 8s → paper → digital → clickable). This skill's hand sketch is the minimum concrete artefact to close the invention loop; when the fellow wants a real clickable prototype, route there.

`concierge-probe` / `probe-matrix` (section 04) — the Icarus home for "now test it cheaply." This is where the experiment-design job of the absorbed `brainstorm-experiments-new` lives; this skill keeps only the invention job.

Supersedes: none. Absorbs `discovery/brainstorm-experiments-new`'s useful bones — YODA (your own data beats others' data), skin-in-the-game, behaviour over opinion — but reframes from experiment-design to invention. Brainstorm-experiments designs pretotypes for an already-chosen idea; this produces the idea worth pretotyping and refuses the generic one. For pretotype design itself, route to section 04 probes.
