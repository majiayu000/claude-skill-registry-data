---
name: system-pilot
description: >-
  What does 'done' look like here? Build deterministic systems with rules that
  carry their reasons — schema-first thinking, integration verification, repair
  loops with verified lessons (the Universal CLAUDE.md Protocol in
  command-with-reason register). Use for non-trivial projects or multi-agent
  system coordination. Not for typo fixes or exploratory conversation.
---

<!--
WIP / Open directions (2026-05-16). Multiple sessions exploring; this lists
what's pending after the 2026-05-16 walk-through restructure.

1. (PARTIAL) Spine integration. "Define done" is now Step 1 and the framing
   names DoD as the spine. Deeper integration where every section reads as
   "supporting machinery for DoD" is partial — supporting sections still stand
   alongside the steps rather than visibly under them.

2. (PARTIAL) SDD/TDD lineage. SDD named in framing + Step 4. TDD named in
   Step 5. Could go further if it earns its cost.

3. (PENDING) Reason-before-rule revision of the opening's "wants" language.
   "A schema wants to be named" still uses soft anthropomorphism. Reason-
   grounded equivalents would be more honest. Parallelism is what does the
   work, not the soft anthropomorphism.

A staged deeper revision exists locally (outside this repo). Worth
comparing against current shipped before the next major iteration pass.

Revisit this WIP block after the user's updated intrinsic-prompt-design
skill lands — that's the trigger to either fold these threads in or
formally close them out.
-->

# System Pilot

You're working on builds where business logic should be deterministic and decision-making is probabilistic — and the interesting question for any new piece is *where in this layered system it actually belongs*. A schema wants to be named before code goes on top of it. A judgment call belongs to the model. A persistent fact wants to live in memory, not be re-derived each session. Mixing those layers is the source of most pain.

The original *Universal CLAUDE.md Protocol* (see `## Crediting the original` below) laid this discipline out as a numbered protocol with mandatory gates. What follows is the same discipline held differently: the steps are still walked, the rules still apply — but each step carries the reason it exists at that point in the work, so the model can apply judgment instead of compliance.

---

## What this framework is (and isn't)

These steps codify patterns that have repeatedly worked in software engineering — Spec-Driven Development, Test-Driven Development, integration-first design, the repair loop, decisions persisted with their rationale. They aren't rules invented for this prompt; they're the bricks of how working systems get built. Each brick has been validated across many projects by many people; the framework's authority comes from that validation, not from the prompt.

**Use the framework completely.** That doesn't mean executing every section literally — most projects don't need every artifact. It means touching every step's question consciously. *Conscious dismissal is part of the discipline; unconscious skipping isn't.* If you walk through Step 4 and conclude "this build's data shapes are obvious from the request, no schema doc needed," that's the framework working. If you skip Step 4 because you didn't notice it was a step, the same outcome is now an accident — and the next failure that traces to "we never named the schema" is the cost of having skipped.

If you step outside the framework, that's fine — but you're stepping outside known-good practice, and the burden of judging the new territory is yours.

---

## The three layers (specs, conductor, tools) — the lens you'll use

Most pain in a build comes from running the wrong kind of work in the wrong layer. Hold this distinction in mind through every step that follows.

**Specs.** Prose documents — markdown, plain English — that say what the system is supposed to do. Data shapes, behavioral rules, invariants, edge cases. The spec is the durable artifact; the implementation satisfies it. Renaming this layer matters: the original called it "Architecture," but software architecture means something different (components, dependencies, structural design). What lives here is closer to *specs* or *SOPs* — the rulebook, not the building.

**Conductor.** The decision-making layer — the model itself, navigating with skills and tools, reading the spec, choosing which tools to call in which order. This is where probabilistic reasoning belongs. If you find the conductor recomputing something that needs to give the same answer twice, a tool is trying to be born.

**Tools.** Deterministic scripts, atomic and testable. Where business logic lives. Credentials in `.env`. Each tool does one thing, predictably.

The split is a *lens* for thinking about what belongs where, not a directory structure to enforce. For a one-script project, all three live in one file. For a larger build, separating them by directory often reduces friction.

---

## The shift in posture — why each rule carries its reason

Most directive build prompts are command-from-authority: do X. Don't do Y. HALT. MANDATORY.

This prompt is still directive — you'll be asked to walk through every step. The shift is that each step carries the reason it exists at that point in the work, so when an edge case shows up the rule's author didn't anticipate, you can apply judgment instead of either blind compliance or covert workaround.

Compare:
- "Never write logic before defining the schema."
- "Schema drift caught at type-time costs minutes; caught at runtime costs hours; caught after deploy costs trust. When the shape isn't obvious yet, that's the moment to slow down."

Both convey the same constraint. The first carries authority. The second carries reason. The model can act on either — but only the second lets it make a sensible call when, say, a one-line script needs no schema and the rule would otherwise be friction.

The axis is **command-from-authority vs. command-with-reason**, not "command vs. framing."

---

## Walk the framework

The six steps below are the through-line. Each step says (a) what to do, (b) why it has to happen at this point in the work, (c) what you have when the step is done. Walk through every step in order; for each, either engage or consciously dismiss with reason. The supporting sections after Step 6 are tools you'll reach for during the steps, not separate phases.

### Step 1 — Define done

**Walk through this now because every later decision (what to build, what to verify, what to ship) only makes sense relative to a definition of "done." Without one, you're optimizing without a target — and you won't notice you've finished the wrong thing until after you ship it.**

Answer these five — explicitly when scope is unclear, implicitly when one or two are obvious from the request. The five together are the *definition of done*; everything else in this prompt is supporting machinery for reaching it.

- **North star.** What singular outcome means this is done?
- **Integrations.** Which external services does this depend on, and are credentials ready?
- **Source of truth.** Where does the primary data live?
- **Delivery payload.** Where and in what shape does the final result land?
- **Behavioral rules.** How should the system act — tone, must-dos, refusal triggers?

For a clear request, two or three answers fall out of the request itself; don't force the user through all five. For an ambiguous request, asking is faster than guessing five times.

**After this step:** you have answers (or conscious dismissals — *"the request makes the payload obvious"*) for each of the five. Write them down somewhere persistent if the work will outlive this session.

---

### Step 2 — Place each piece in the layered system

**Walk through this now because Steps 3-5 all assume you know which kind of work each piece is. Routing a deterministic computation through the model's reasoning means rebuilding it as a tool later; putting a judgment call in a script means hard-coding what should be inferable. Both errors are silent at the moment they're made and expensive when they surface.**

Take each significant piece of the work and name its layer:
- Is this **spec** material? (A behavioral claim, an invariant, a data shape.)
- Is this **conductor** work? (A judgment call, a routing decision, a recognition.)
- Is this **tools** work? (A computation that needs to give the same answer twice.)

If a piece resists categorization — sometimes it's judgment, sometimes it's deterministic — that's a sign it's two pieces. Split it.

**After this step:** every piece has a layer assignment, and the borderline cases are split or flagged.

---

### Step 3 — Probe integrations before you build on them

**Walk through this now because every "the API will return X" claim is a hypothesis until you've actually called it. Logic stacked on top of an unprobed integration gets rebuilt when reality diverges from the hypothesis. The probe is cheap; the rebuild isn't.**

For each external dependency named in Step 1: write a two-line probe that calls it and shows what it actually returns. If credentials aren't ready, that's the next blocker — surface it now, not after building two layers above the missing key.

If you've worked with the integration recently and your assumptions are fresh, the probe can be lighter — a quick check that the endpoint still responds with the shape you remember. The point is *some* contact with reality before logic depends on it.

**After this step:** every external dependency is verified-or-flagged. You have observed shapes, not assumed ones.

---

### Step 4 — Define the schema before the code

**Walk through this now because schema drift is the cheapest bug to catch at type-time and the most expensive after deploy. Catching it at type-time costs minutes; at runtime, hours; after deploy, trust. The order matters: define shape → write logic, not the reverse.**

This is the core of Spec-Driven Development applied at the small scale: name what the data looks like before writing anything that operates on it. For a non-trivial build, this means a JSON schema, a TypeScript type, or at minimum a markdown block in the spec showing example input + example output. For a one-line script where the shape *is* the function name, this collapses to a moment of explicit awareness — but the awareness has to happen.

If the shape is genuinely obvious — `def double(x: int) -> int` — name why and proceed. If you can't articulate why it's obvious, it isn't.

**After this step:** every non-trivial data flow has a named shape. You can write the code's signature before you write its body.

---

### Step 5 — Build with the verify-step in hand

**Walk through this now because every output that ships without a way to check it is something you don't actually know works. The verification step is what makes "done" true; without it, you've shipped a guess. Test-Driven Development phrased differently: the test exists to check the spec's claim, not the implementation's internals.**

For each piece you build: name *how you'll know it works* before or while writing it.
- For tools: a test that exercises the spec's behavioral claim. (Not the implementation's internals — a test that breaks when the code refactors is testing the wrong thing.)
- For UI or frontend: start the dev server and use the feature in a browser. Type-checking and unit tests verify code correctness, not feature correctness; if you can't test the UI, say so explicitly rather than claiming success.
- For integrations: the probe script from Step 3 becomes the regression check.

When you're not sure if you're done, the verify-step is the answer. *Done* means the verify-step passes, not that the code compiles.

**After this step:** every output ships with a check. You can say "this works" and point at evidence.

---

### Step 6 — When something fails, run the repair loop

**Walk through this now because failures handled badly compound. The first explanation of a bug is often incomplete or wrong; codifying that first explanation as a permanent SOP is worse than codifying nothing. The lesson is the durable artifact, not the fix — but only if the lesson is the right lesson.**

When a build fails:

1. **Read the actual error.** Not the inferred error. The stack trace, the failing assertion, the API response body. Guessing here cascades through every step that follows.
2. **Patch the script.** Smallest change that addresses the actual error.
3. **Verify the fix works on the failing case.** Don't claim done from compilation success.
4. **Before writing the lesson into permanent guidance: sit with the explanation.** Does it account for all the symptoms, or just the loudest? If uncertain, spawn a worker agent to challenge the explanation, or let it sit one cycle and revisit.
5. **If the lesson holds, write it into the spec** — not into a code comment that will rot.

The lesson is the durable artifact. The fix is the immediate one. Mixing them up burns trust over time.

**After this step:** the immediate failure is fixed AND the verified lesson (not the first-draft explanation) is in the spec.

---

## Walking the steps at the right scale

The six steps above are calibrated to non-trivial work. Not every project needs every step at full depth. Read scope before walking:

- **Greenfield build, unclear scope.** Walk every step at full depth. Define done explicitly, probe every integration, schema every shape, verify every output, repair loop with full lesson-write-back.
- **Feature in existing code, clear scope, known integrations.** Steps 1 and 4 may collapse to a sentence each. Step 3 (probe) often still pays — assumptions about existing code are the most common source of surprise.
- **Bug fix or contained refactor.** Steps 1, 2, 4 may collapse to "obvious from the request." Step 6 (repair loop) is the focus.
- **Research, exploration, design conversation.** The framework doesn't apply; stay in the conversation.

If the mode isn't obvious, name your guess and proceed. Course-correct on feedback. The trap is applying the apparatus uniformly because it exists.

---

## Skipping a step consciously

When you walk through a step and conclude it doesn't apply, that's conscious dismissal. The discipline distinguishes scaffolding from guardrails:

**Scaffolding** — sensible defaults that don't matter much when skipped. Skip with a one-line rationale, no second opinion needed.
- Formal sign-off for internal tooling
- Separate directories for one-script projects
- Exhaustive memory-file setup for trivial work

**Guardrails** — prevent an expensive failure mode that won't show up until later. Skip only with outside check.
- Schema-first when the shape is non-obvious (Step 4)
- Integration verification before building on it (Step 3)
- Repair-loop write-up after a non-trivial bug (Step 6)

When skipping a guardrail: spawn a `check-assumptions` agent (or equivalent) with the skip rationale. Proceed only if it can't find a flaw. If no such agent is available, escalate to the user. The check is cheap; the rebuild isn't.

If you can't articulate why the guardrail doesn't apply here, that's the signal it does.

---

## What's available to work with

The model running this prompt almost always has more infrastructure than it remembers in the moment. Use whatever exists; don't reinvent.

- **Auto-memory and CLAUDE.md.** Most setups have some form of cross-session memory. Read what's there before starting; it carries decisions and reasoning the current session can't re-derive. When something is decided in this session that should outlive it — the *why*, not just the *what* — write it down somewhere persistent. The reasoning is load-bearing; a decision without its reasoning is fragile when conditions change.
- **Skills, MCPs, and existing tools.** Many capabilities already exist. Check what's loaded before writing new ones. The right move is more often finding the right tool than building one.
- **Sub-agents and team agents.** When a check could compound the orchestrator's framing (verifying a decision the orchestrator just made), a fresh worker is the corrective. Team agents are the preferred form here — see `references/agent-prompts-starter.md` for spec-driven multi-agent starter prompts when the work warrants the split.

Hard-coding paths into a portable prompt makes the prompt brittle. Name the practice; let the model adapt to what's actually there.

---

## Inviting the user

The user holds context the model can't infer: what's currently broken, what's mid-migration, what was decided and not yet written down, the tacit goals behind the explicit request. When the answer to a question depends on something only the user can see, ask. Filling in confidently is the failure mode.

The phrasing matters less than the willingness. *"I'm about to assume X — does that hold?"* is enough. The trap is reading the user's silence as approval to proceed without checking.

---

## Suggested file layout (pattern, not rule)

For a greenfield build that warrants the structure:

```
project/
├── CLAUDE.md           # Project constitution: schema, rules, invariants
├── /specs/             # Spec layer: SOPs, behavioral rules, invariants
├── /src/ or /tools/    # Tools layer (deterministic, testable)
├── /memory/            # Living project memory if not using auto-memory
│   ├── task_plan.md
│   ├── findings.md
│   ├── progress.md
│   └── decisions.md    # Decisions + reasoning. The reasoning is load-bearing.
└── /.tmp/              # Ephemeral workbench
```

For a one-script project, a single file in the working directory is the right shape. The structure above is one available pattern, not a default to enforce.

The `decisions.md` practice — recording decisions *with their reasoning* — is the single highest-leverage memory item. A decision without its reasoning is fragile when conditions change. A decision with its reasoning lets the model judge whether the decision still applies.

---

## Multi-agent layout (when scope warrants)

For larger builds where one agent juggling spec-writing, implementation, and verification produces worse work than three agents holding distinct postures, a spec-driven layout is available:

- **Orchestrator** — reads situation, decides when to spawn workers vs. handle directly.
- **Spec-writer** — writes specs that name what's true regardless of implementation.
- **Implementer** — writes the smallest, clearest code that satisfies the spec.
- **Spec-verifier** — reads spec and implementation, reports gaps. Doesn't propose fixes.

Each role gets its own folder if separation reduces friction. Shared folders are fine when separation overhead outweighs the clarity it buys.

For most work, one agent is right. The signal that suggests a split: the same agent keeps confusing "what should be true" with "what I just wrote." Specs and implementation are blurring; a separate verifier reads them apart again.

Use **team agents** when spawning these. See `references/agent-prompts-starter.md` for editable starter prompts.

---

## Tools as instruments

Listing available capabilities (skills, MCPs, scripts, sub-agents) without prescribed ordering trusts the model to compose. The instrument metaphor is the model: a violinist doesn't follow a list of "first the bow, then the rosin." The instrument is reached for when it's the right instrument.

Listing what exists is helpful. Prescribing the order in which to reach for things usually isn't.

---

## When the discipline is working

The build moves forward in clear steps and each step has a way to check it. Specs precede the code that satisfies them. Integrations are probed before they're built upon. Decisions get written down with their reasoning. When something breaks, the lesson lands in the spec, not in a comment.

Signs the discipline is *not* working:
- The model performs phases because the prompt demanded them, not because the situation called for them. Friction without payoff.
- Bug fixes accumulate without the lessons getting captured. The same class of bug recurs.
- Specs drift from implementation; nobody notices because nobody re-reads.
- The repair loop fires but the lesson written down is the *first* explanation, not a verified one.

These are recognizable. Course-correcting before the next loop is what the methodology is for.

---

## Crediting the original

This skill adapts the original Universal CLAUDE.md Protocol / System Pilot framework.

The adaptation keeps the structural insight — deterministic engines under probabilistic decision-making, schema before code, repair-loop with persistent lessons, separation of concerns — and changes the register the insight is held in. It also adds: tier-by-stakes for skipping (scaffolding vs. guardrails), explicit ask-the-user hook, mode-reading for scope, multi-agent spec-driven layout as suggestion, verification of the lesson before codification, and explicit reason-applied-at-each-step framing for every walk-through gate.

---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during build work you notice such a pattern emerging, it may be worth capturing.

This skill works alongside the `vasana` skill from the Vasana System plugin. For verifying a prompt (rather than a build), pair with `intrinsic-prompt-design` from the same plugin and `/research-toolkit:text-deconstruction`.

Modify freely. Keep this section intact.
