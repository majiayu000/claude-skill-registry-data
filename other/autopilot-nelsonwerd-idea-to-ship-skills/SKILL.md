---
name: autopilot
description: >-
  Run the idea-to-ship pipeline AUTONOMOUSLY, in character as a grounded
  founder-persona — composing ideate → deep-dive → prompt-pack → build-loop to
  take a real, grounded niche to a near-finish-line-AIMED first-draft product
  plus an honest ledger of what only a human or the market can finish. ALWAYS
  invoke when the user says any of "run autopilot", "build this idea→ship
  autonomously", "spin up a grounded founder and build it", "fly the whole
  pipeline end to end", or "autonomous first-draft from a concept". It composes
  the existing skills, never reimplementing them, and states its honest bounds —
  a near-finish-line first draft, NOT a finished or market-validated product
  (~80% craft ceiling; grounding firewall; its go/kill calls are a signal). Do
  NOT use to drive each phase by hand (use the skills directly), when there's no
  real grounding (you'd be inventing demand), or when you need market validation
  (the human handoff).
---

# Autopilot — autonomous idea→ship orchestrator

`autopilot` flies the **idea-to-ship pipeline end to end, autonomously**, in character as a *grounded* founder-persona — productizing the "paste one kickoff and the pipeline runs itself" pattern. It takes a real, grounded niche and hands back a **near-finish-line-AIMED first-draft product + an honest validation ledger**.

It is an **orchestrator: it composes the existing skills and never reimplements them.** It invokes `ideate`, `deep-dive`, `prompt-pack`, and `build-loop`, carries each one's file output into the next, and adds only the connective tissue — the autonomy contract, the corrected gate, the kill-ledger, and an honest hand-off. If you find yourself pasting a sub-skill's procedure into this run, stop: invoke the skill instead.

It states its limits in its own text (below) because the whole point is an honest first draft, not an oversold "finished product."

## When to use this

**Strong triggers — invoke without asking:**
- "Run autopilot" / "fly the whole pipeline" / "take this idea→ship autonomously"
- "Spin up a grounded founder-persona and build it" / "autonomous first-draft from this concept/niche"

**Softer triggers:**
- You have a *grounded* niche (real lived pain or real data) and want a first-draft product + an honest validation ledger without hand-running each phase.

**Do NOT use this for:**
- Driving each phase yourself — use `ideate` / `deep-dive` / `prompt-pack` / `build-loop` directly.
- A concept with **no real grounding** — autopilot will not invent demand to fill the gap (see the firewall in Bounds).
- **Market validation** — out of scope; that is the human/market handoff.
- A settled code change (`prompt-pack`) or a soundness audit (`deep-dive`).

**Routing tie-breaker:** autopilot *automates the manual tier*. Reach for it to fly the pipeline end-to-end with eyes open on the bounds — not to replace human taste, finish, or market judgment.

## What it produces — and its honest bounds (read this before you trust it)

Load-bearing, stated up front so no one reads an autonomous run as more than it is.

**Produces:** a grounded `CONCEPT_BRIEF`, a validated + sequenced build pack, a **near-finish-line-AIMED first-draft product** (designed + machine-validated as far as machines can check), and an honest ledger of what's checked vs. what only a human/market can verify.

**The 3 eyes-open limits it does NOT escape:**
1. **~80% craft ceiling + a last-mile tail.** "Near-finish-line" is the *aim, not a guarantee*; a correctness/security/taste tail remains for the **human to finish**.
2. **The grounding firewall.** Real data to *discover the problem* and *seed the build* = yes. A synthetic persona's *reaction to the proposed solution* **never** counts as validation. autopilot injects real signal at the front; it does not manufacture demand.
3. **Judgment quality isn't cleanly measurable.** Its go / iterate / kill calls are a **signal a human weighs**, never proof. "The system's judgment matches an expert" is **non-gating** (it's circular — it needs the market truth the system exists to replace).

**Market validation is explicitly the human handoff.** "Works + looks good + well-judged" ≠ "people want it." autopilot is a force-multiplier toward a finishable first draft — not a finished-product factory and not a market validator.

## The pipeline it flies (compose, never copy)

Hard rule: **invoke** each skill and carry its file forward; never inline its content.

1. **`ideate`** → a grounded `CONCEPT_BRIEF.md` — forced success-metric + kill-criterion, and (via its conditional-design forcing-function) a **substantive design direction** when feel is load-bearing.
2. **`deep-dive`** → validates the brief's load-bearing claims with honest confidence + a ground-truth tally; its hand-back is folded into the brief (verdict, what's verified vs. still-a-bet).
3. **`prompt-pack`** → sequences the *validated/gated* scope into self-contained build prompts; carries **execute-discipline**.
4. **Gate-impact pass** → before each unit's build opens, enumerate the gates, frozen constraints, and conventions that unit's **planned surface** will trip, and clear them all in **one pass**. The mechanism lives in `prompt-pack`; autopilot's job is that the pass *happens*. **Not optional** — it is the phase gate between planning and building.
5. **`build-loop`** → drives each shippable unit to near-finish-line craft on **two co-equal tracks** — the objective machine facts AND, when feel is load-bearing, the **mandatory multi-pass visual design loop**.

Phase-by-phase orchestration (what each invocation gets, what carries forward, where the gates are): `references/pipeline-playbook.md` — the gate-impact pass sits between its Phase 3 and Phase 4.

## The autonomy contract

- Run **in character** as the grounded persona. Answer every phase gate the founder can answer — the brain-dump, the selection rubric, the divergence ranking, the pressure-test verdict, the convergence locks — **in-character, without stopping for a human.**
- **But never fake a human-only gate.** A gate that genuinely needs a human or real-world signal (real use, a taste sign-off, a market/paste-into-prod test) is **emitted honestly**, not auto-passed in-character. (Execute-discipline, below — the experiment's sharpest failure was a run that narrated a gate it had actually abandoned.)
- **Narrate the phases.** Say which skill is running and what file it produced, so the run is legible and resumable.

## Execute-discipline (inherited from `prompt-pack`) — never fake a gate

Build **only the validated/gated scope** — never extra breadth to look complete. If a phase's gate needs a human or real-world signal you don't have, **STOP and emit the gate** (name what's unverified and who must clear it); never fake it, render a "passed"/inert gate, or build past it. autopilot inherits this from `prompt-pack` and enforces it across the *whole* run — the autonomy makes it easy to rationalize past a gate, so this is the rule that keeps an autonomous run honest.

## The corrected gate (proceed / park)

- **Gate on real-use + checkable craft:** does it build, run, pass its flows and (when load-bearing) its design bar via `build-loop`? Is the output a *finish-the-last-mile takeover*, not a from-scratch rebuild?
- **Non-gating signal:** "the system's judgment matches an expert." Report it as a signal, **never as the gate** (it's circular). An expert backtest is agreement-by-construction.
- **Parking is a valid, honest outcome.** Say so and stop — then log it (kill-ledger, below).

## Design, carried through (per `ideate` conditional-design + `build-loop`'s visual loop)

- When the brief marks feel **load-bearing**, autopilot carries the brief's **substantive design direction** (target vibe, references, principles, the intended feel, design acceptance criteria) **into the `build-loop` invocation**, and expects `build-loop` to run its **mandatory, multi-pass visual design loop** — render → critique → fix → re-render, every iteration, never a unit-test substitute, never one-and-done.
- In the hand-off, **surface the design residual + the human taste spot-check** — the loop drives design hard toward the bar, but "looks good to two models" ≠ "a designer signed off." Never imply the loop reached finished/elite design on its own.
- When feel is **not** load-bearing (a plain utility), plain-but-clear is correct; the visual loop stays light.

## The kill-ledger (LOCKED)

Parked or killed concepts are **never silently dropped.** Each is surfaced with its **steelman** (the strongest honest case for it) + the **specific evidence that would flip it to *go*** — a reviewable parking lot, so a kernel autopilot parked can be rescued. (Maps onto `ideate`'s steelman-before-kill / park-with-a-revisit-trigger.)

## The kickoff (emitted each run)

autopilot opens each run by emitting a **kickoff** that locks the run's frame, then executes it. The full fill-in template is `references/kickoff-skeleton.md`; it captures: the **grounded persona** (real lived pain / real data — not invented demand), the **forced success-metric + kill-criterion**, the **autonomy contract**, the **pipeline order**, **execute-discipline**, the **substantive design direction when feel is load-bearing**, a **narrate-the-phases** instruction, and the **context/handoff safety-net**.

## Context / handoff safety-net

A full autonomous run is long and may outlive one chat. **Files are the durable memory** — the `CONCEPT_BRIEF`, the pack, `build-loop`'s per-iteration ledger, any proof notes — never chat memory. Each phase's output is a file the next phase (or a future session) reads. If the run risks a context limit, emit a **`prompt-pack` Mode C handoff** so a fresh chat resumes cleanly with no amnesia.

## Model tiering (spend reasoning where judgment lives)

A long run accumulates **paperwork** — ledger and receipt copying, status/doc reconciliation, formatting gates, mechanical restatement of a contract already locked in a file. That work does not need frontier-tier reasoning; route it to a cheaper tier (or a script) and keep the strong tier where the run's quality actually comes from.

- **Strong tier:** the brief's decisions, the design direction, `deep-dive`'s red-team, `build-loop`'s critique passes, and any debugging where the cause is still unknown.
- **Cheap tier:** transcription, reformatting, filling a settled template, restating a locked decision, mechanical doc sync.
- **The hard line:** anything making a **judgment call about correctness or honesty** stays on the strong tier — grading a gate, splitting verified vs. still-a-bet, writing the kill-ledger or the hand-off. Cheap-tiering a judgment call is how a run starts quietly overclaiming.

## Pitfalls to avoid

- **Re-implementing a sub-skill** instead of invoking it. Compose, don't copy. (If you're pasting a funnel or a loop procedure, stop.)
- **Faking or auto-passing a human-only gate in-character** — the experiment's sharpest failure. Emit it; never narrate a gate you abandoned.
- **Treating a synthetic persona's reaction to the solution as validation** — a firewall breach. Real data discovers + seeds; it never validates the solution.
- **Claiming the output is finished / elite / validated.** It's a first draft; the market is the handoff; design has a human taste residual.
- **Silently dropping a parked concept** — the kill-ledger forbids it.
- **Opening a unit's build before its gate-impact pass** — discovering constraints one at a time turns one unit into a chain of stop-fix-resume detours, and each partial fix breeds the next.
- **Letting the build phase go one-and-done or unit-test-substitute** — `build-loop`'s own rules require a genuine multi-pass loop and (when load-bearing) the visual design loop; surface the iteration count + design residual, don't paper over them.

## Scale heuristics

| Situation | What autopilot runs |
|---|---|
| A narrow, single-purpose app, design **not** the wedge | Full pipeline; `build-loop` plain-but-clear, N≈3–5; market handoff stated. |
| A narrow app where **feel is the wedge** | Full pipeline carrying the substantive design direction; `build-loop`'s mandatory multi-pass visual loop + different-model critic + a flagged human taste spot-check. |
| A grounded niche, optional real-data seeding | Compose `ground` if installed (it's optional); the run works with or without it — the firewall holds either way. |
| No real grounding available | Don't run autopilot — it would invent demand. Hand back: ground the concept first. |

autopilot is the autonomous tier of the idea-to-ship suite: it flies the manual tier's pipeline to a near-finish-line-aimed first draft + an honest ledger — eyes open on the 3 limits, never overselling the result.
