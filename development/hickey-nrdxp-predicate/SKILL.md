---
name: hickey
description: |
  Structural simplicity review based on Rich Hickey's "Simple Made Easy" framework.
  Trigger when:
  - Reviewing code for complected concerns, analyzing coupling, or simplifying code architecture.
  - Prompt contains: /hickey, simple made easy, complect, decouple, compose.
---

# Structural Simplicity Review

Evaluate code for **structural simplicity** using Rich Hickey's "Simple Made Easy" framework. Designed for a world where AI generates code faster than humans can read it — where functional tests pass but accidental complexity accumulates silently.

The core premise: **tests tell you code works; they tell you nothing about whether it's simple.** Hickey: _"What's true of every bug found in the field? It passed the type checker... it passed all the tests."_ Complected code can be perfectly correct today. The damage surfaces when you try to change it, reason about it, or extend it.

> [!NOTE]
> This workflow is the **spatial** half of the code-spacetime review pair. It reads code as a static snapshot — what's tangled right now? For the **temporal** half — what will pull apart, and when? — see `/lowy`. Run both for full coverage. See `engineering.md` §8.1.

**Attribution:** Adapted from Rich Hickey's [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) (Strange Loop, 2011) and [Srid Ratnakumar's implementation](https://github.com/srid/agency/blob/master/.apm/skills/hickey/SKILL.md). Full talk transcript: [matthiasn/talk-transcripts](https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md).

---

## Key Definitions

**Simple** (sim-plex, "one fold/braid"): One concern, one role, one concept. Simplicity is _objective_ — count the interleaved concerns. Hickey: _"What matters for simplicity is that there is no interleaving, not that there's only one thing."_

**Easy** (adjacens, "nearby"): Familiar, at hand, within our skillset. Easy is _relative_. Hickey: _"If you want everything to be familiar, you will never learn anything new."_

**Complect** (com-plectere, "to braid together"): Interleave independent concerns so they cannot be reasoned about in isolation. Hickey: _"Every time I think I pull out a new part of the software I need to comprehend, and it's attached to another thing, I had to pull that other thing into my mind because I can't think about the one without the other."_

**Compose** (com-ponere, "to place together"): Combine independent things side by side, preserving isolation. Hickey: _"I'd rather have more things hanging nice, straight down, not twisted together, than just a couple of things tied in a knot."_

---

## The Evaluation Process

Work through these layers in order. **Every finding must survive self-verification** — after completing all layers, run the Self-Verification Checklist (§ below) on your own evaluation to catch wishful justifications and bogus dismissals.

### Layer 1: Identify the Concerns

Name the independent concerns the code addresses. Write them out explicitly. If you can't cleanly name distinct concerns, that is itself a finding.

### Layer 2: Fragmentation Check

Hickey's "don't complect" has a dual the rest of this workflow doesn't cover: **don't fragment what belongs together**. When one domain concept is split across multiple fields, state locations, signals, modules, or call sites, and their coherence depends on an unenforced rule, you have the same structural bug as complecting — you just arrived at it from the opposite direction. The fix for complecting is separation. The fix for fragmentation is **reunification** at whatever layer the one thing naturally lives: one type, one signal, one module, one function, one file.

For every group of related fields, state locations, or entities in the changed code, ask: **does the domain model this as one thing?**

If yes, is the code representing it as one thing, or has it been shattered into parts whose coherence depends on an unenforced rule? The rule can live anywhere — type shape, code convention, doc comment, "we remember to update both", runtime ordering, a reactive pipeline that rebuilds the unity at read time.

1. **Enumerate invariants.** Write out every rule coupling the parts, in plain language: "if A then B", "all Xs agree on Y", "when kind=X then field F is present", "at most one of A/B/C is set", "every update of P must update Q".
2. **Check consumption sites, not just definitions.** Fragmentation is most visible at the reader. If every consumer projects the same value out of a per-entity structure, the per-entity part is lying — the projection is the fingerprint. If multiple modules derive the same value from different sources, the derivation is the fingerprint.
3. **Watch for reconciliation machinery.** A memo that lifts one value out of a collection; a callback that writes back into the collection; an effect that copies one entity's state onto others; a config loader that cross-validates two files; a convention comment that says "keep X in sync with Y". All are the shape of *the state is fragmented and we're rebuilding the unity somewhere downstream*. The machinery is the bug, not the fix.
4. **Collapse at the natural layer.** Pick the representation layer where the one thing naturally lives. Sometimes that's a discriminated union in a type; sometimes it's a module-level signal; sometimes it's moving two files into one. The layer is wherever the unity stops needing a rule to hold.
5. **Silence is the bug.** A review that skips this layer because "no invariants came to mind" is the same review that misses the fragmentation. When the review genuinely finds nothing, writing "no invariants found" explicitly is the required cheap output. The enumeration is what forces the check, not the outcome.

### Layer 3: Check for Concept Multiplication

Hickey: _"Be particularly careful not to be fooled by code organization. There are tons of libraries that look — oh, look, there's different classes; there's separate classes. They call each other in these nice ways."_

For each new abstraction (component, module, signal, type) the code introduces:

1. **Name what it represents at the domain level**, not the implementation level.
2. **Search for existing abstractions serving the same domain concept.** If one exists, extending it is the default — not creating a parallel one.
3. **"Mirror existing pattern" is an easiness judgment, not a simplicity judgment.** Creating ComponentB because ComponentA exists and looks similar adds a concept. Extending ComponentA keeps concept count flat.

Two abstractions serving one user-level concern = accidental concept multiplication, even if each is internally clean. The structural layers below won't catch this — they check _within_ abstractions, not _across_ them.

**Concept Multiplication vs. Fragmentation**: these are close cousins but distinct bugs. Concept Multiplication is about *duplicated wholes* (two classes for one domain concept → delete one). Fragmentation (Layer 2) is about *split wholes* (one domain concept shattered across multiple locations → collapse to one). A single finding can trigger both layers from different angles; that's redundancy, not muddling.

### Layer 4: Structural Pattern Scan

Scan for known structural patterns **and any additional patterns from project instructions**. The catalog has two halves: complecting (things braided together that should be separate) and fragmentation (things split apart that should be one). Both directions are "interleaved vs. not-interleaved" — Hickey's principle is bidirectional.

**Complecting patterns (things-that-should-be-separate braided together)**

| Construct | What it complects | Simpler alternative |
|---|---|---|
| Mutable state | Value + time + identity | Immutable values, controlled state containers |
| Objects | State + identity + value + namespace | Plain functions + data + namespaces |
| Methods | Function + state; function + namespace | Free functions, interfaces |
| Inheritance | Types with types | Composition, interfaces, traits |
| Switch/case on type | Who + what | Dynamic dispatch, visitor pattern |
| Mutable variables | Value + time | `const`/`final`/`let` bindings, immutable data |
| Imperative loops | What + how + when | `map`/`filter`/`reduce`, declarative transforms |
| Actors | What + who | Queues + stateless handlers |
| ORM | Object identity + relational model + query | Plain data + declarative queries |
| Conditionals scattered across code | One decision braided across many sites | Rules, declarative policies, lookup tables |
| Callbacks/closures over mutable state | Control flow + state + time | Streams, queues, immutable values |
| Hand-rolled utility when a focused library solves the exact problem | *Scope decision* with *implementation choice* | Use the library. Hand-roll only when the library adds surface area you actively don't want. "Zero deps" is an easiness judgment dressed as a simplicity judgment — code you don't own is genuinely simpler than code you do own. |

**Fragmentation patterns (things-that-belong-together split apart)**

| Construct | What it fragments | Simpler alternative |
|---|---|---|
| Parallel optional/nullable fields with coupled presence | "Thing exists + its shape" into independent slots whose combinations include illegal states | Discriminated union / single container encoding the coupling |
| Per-entity state the domain says must agree across entities | One value into N copies indexed by identity, with an unenforced "all agree" rule | Single source-of-truth at the containing scope |
| Reactive pipeline projecting one value out of a per-entity structure | Sharedness reconstituted at read time | Make the underlying state shared; delete the pipeline |
| Callback-down + value-up across module boundaries | One state location into a cycle across N modules | Lift the state to the layer all consumers share |
| Sum type modeled as parallel optional fields per variant | A discriminator scattered into its projections | Actual sum type with the discriminator as the key |
| Booleans whose combinations encode a state machine | One state into several independent flags | Enum / union naming each reachable state |
| "Convention: update X when Y changes" maintained by memory | A rule into documentation or code review discipline | Structure so the coupling is mechanical, not memorized |
| Duplicated derivations (same value computed in N places) | One computation into N copies | Compute once, read N times |
| Config or data split across files/modules by accident of history | A concept into shards held together by cross-reference | Collapse into the one file or module that owns the concept |

When you find a catalog match in either half, **do not dismiss it**. Design the concrete alternative first (Layer 7), then evaluate whether the current approach is actually justified. The proof burden is on the current code, not on you to prove it's wrong. Hickey: _"what matters are the artifacts not the authoring."_

### Layer 5: Structural Entanglement Analysis

For each file or module touched:

1. **Concern count per module.** Multiple distinct concerns in one module = braiding. Flag it.
2. **Mutable binding count per function.** Count `let` bindings + reassignments. 3+ in a single scope = scrutinize.
3. **Closure depth.** Closures over mutable state braid the inner function with the outer function's timeline.
4. **Data flow topology.** Pipeline or DAG = good. Cycles (handler emits onto its own channel) = complected.
5. **Lifecycle nesting.** New lifecycle scopes (AbortControllers, watchers, timers) inside a handler that already has its own lifecycle = braiding "when" concerns.
6. **Temporal coupling.** Correctness depending on execution order beyond what types enforce = invisible braid.

### Layer 6: Assess Severity

For every finding, assess — but **severity does not grant dismissal**. A low-severity finding is still a finding. Report it. The user decides what to act on, not you.

- **Blast radius.** How much of the system must be understood to diagnose a bug from this entanglement?
- **Change friction.** Can the complected concerns be modified independently?
- **Reasoning load.** Can you explain the code without "and then" or "but only if"?

### Layer 7: Suggest Simplifications

For **every** finding — not just "significant" ones — propose a concrete structural alternative. Write out what it would look like, even as pseudocode. This is mandatory.

**Never label a finding "essential complexity" without first designing the simplified version.** Hickey: _"Simplicity is a choice. It's your fault if you don't have a simple system."_ Assume the existing code came from someone who didn't know better. Design the simpler version. Only after you have it in hand can you evaluate whether the current approach is justified — and if so, explain exactly what makes the simplified version non-viable.

Follow Hickey's design questions:

- **What**: Cleaner abstraction boundary?
- **Who**: Subcomponents as arguments instead of hardwired?
- **How**: Implementation isolated so changes don't ripple?
- **When/Where**: Queue or channel instead of direct calls?
- **Why**: Declarative policies instead of scattered conditionals?

---

## Self-Verification Checklist

After completing all layers, **audit your own output** against this checklist. If any item fires, revise before presenting to the user.

### Dismissed Findings

- Findings you talked yourself out of ("However..." / "acceptable tradeoff" / "justified")
- "Low severity" used as a synonym for "ignore"
- Bogus "essential complexity" labels without a concrete simplified alternative
- Claims about code behavior that you didn't verify by reading the code

### Scope-Based Dismissals

"Out of scope for this PR", "pre-existing issue", "appropriate scope for a bug fix", "orthogonal", and "follow-up refactor" are not simplicity judgments — they are process judgments that let findings evaporate. If you find yourself writing one, either fix the finding in this PR or defer it with a tracked issue. The Actions section enforces this — if you can't fill it in, you're dismissing the finding.

Any finding described as "pre-existing" or "orthogonal" that does not appear in the Actions section with a **Defer** disposition and an issue reference is a dismissal, not a deferral.

### Premature Closure Phrases

These phrase shapes mean you stopped reasoning one step early. If any appear in your evaluation, re-open the question they're dismissing:

- _"X and Y share Z but are separate concerns"_ — verified at the *domain* level, or just at the current implementation layout?
- _"different consumers read different fields/signals/modules"_ — is the split justified by domain difference, or by how today's UI happens to be organized?
- _"technically could diverge, but in practice doesn't"_ — if it's technical, the representation can fix it; "in practice" is a promise that won't hold across refactors.
- _"each X could theoretically have its own Y"_ — theoretical divergence is the classic fragmentation cover story.
- _"this is a convention, not a constraint"_ — conventions are fragmentation dressed as discipline.
- _"we agree to update both"_ / _"we remember to clear X when Y changes"_ — discipline is not a type system.
- _"lift X to be shared"_ — if you're lifting X to make it shared, X wants to *be* shared at its home, not projected from elsewhere.

---

## Output Format

1. **Concerns identified** — Name the distinct concerns.
2. **Fragmentation findings** — Layer 2 findings. If none, write "no invariants found" explicitly.
3. **Concept multiplication** — Layer 3 findings.
4. **Structural pattern matches** — Layers 4–5 findings (both complecting and fragmentation halves of the catalog), with line references.
5. **Severity** — For each finding: blast radius, change friction, reasoning load.
6. **Simplifications** — Concrete alternative for every finding.
7. **Self-verification result** — Output of the Self-Verification Checklist on this evaluation, including the premature closure phrase check.
8. **Actions** — One entry per finding, formatted for downstream consumption. **Every finding from every layer must appear here** — including findings labeled "pre-existing", "orthogonal", or "not introduced by this PR". A finding that never reaches this section has been dismissed, not deferred.

   Each entry **starts with a short bolded finding label (≤8 words)** that names *what* is wrong, then dispositions it as exactly one of:
   - **Fix in this PR**: one-line description of what the implementation step must do. This is the default — prefer it.
   - **Defer**: create a tracked issue for the finding first, then reference it here. "Out of scope" without an issue link is a dismissal, not a deferral.

   Example: `**viewportDimensions complects current+default roles** — Fix in this PR: delete the signal, replace with per-tile FitAddon measurement.`

   "No findings" → "No actions." But if findings exist and the actions list is empty, the evaluation is incomplete.

Do NOT include a "What's simple" section. Praise biases toward positive framing and makes findings feel like minor quibbles. Report what you found. The absence of findings is its own praise.

---

## Caveats

- **Simple ≠ easy, simple ≠ short.** Hickey: _"This whole notion of programmer convenience... we are infatuated with it, not to our benefit."_
- **Simple ≠ familiar.** Hickey: _"If you want everything to be familiar, you will never learn anything new because it can't be significantly different from what you already know."_
- **Tests are necessary but not sufficient.** Hickey: _"I'm glad I've got these guardrails... do the guardrails help you get to where you want to go? No."_
- **This is not a replacement for functional review.** Simplicity analysis complements correctness review. A perfectly simple program that does the wrong thing is useless.
- **Do NOT run tests, builds, or any shell commands.** This workflow is purely analytical — read code, reason about structure, report findings.
- **For volatility-based decomposition** (do boundaries encapsulate axes of change?), see `/lowy`.