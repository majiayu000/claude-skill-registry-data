---
name: build-loop
description: >-
  Drive a build to actually-works, near-finish-line craft by looping build → see
  → exercise → check → critique → rebuild over the agent's existing tools (bash
  build/test, headless screenshot + vision, Playwright, axe/Lighthouse) until
  acceptance criteria pass or an explicit stop-condition fires — no infinite
  thrash. ALWAYS invoke when the user says any of "tighten this build", "iterate
  until it passes", "self-verify the UI", "make it actually work, not just
  compile", "loop until the core flows pass", or "drive this to near-finish-line".
  Also invoke proactively after a scaffold or feature lands and before handing a
  draft to a human. Composition-first over existing tools, not a new program; it
  states its own honest bounds — objective craft only, taste self-graded, ~80%
  ceiling, market validation out of scope. Do NOT use to decide WHAT to build
  (that's ideate) or whether a design/strategy is sound (deep-dive).
---

# Build-Loop — see-and-exercise iteration until a build actually works

`build-loop` takes a build that compiles-but-isn't-done and drives it toward **near-finish-line craft** by repeating one disciplined cycle — **build → see → exercise → check → critique → rebuild** — until its acceptance criteria pass or a stop-condition fires. It doesn't just re-read its own plan; it *runs, sees, and exercises what it built*, then feeds those observations back into the next rebuild.

It is **composition-first**: it orchestrates tools the agent already has — `bash` (build/test), a headless screenshot + vision to *see*, Playwright/headless to *exercise* the flows, `axe`/Lighthouse to *check* — via prose. It is **not** a new program, and not a reinvention of the see-and-exercise agents vendors already ship; it's the discipline that wraps them: a target, a loop, a stop-condition, and an honest ledger of what was actually checked.

This skill is the downstream partner to `prompt-pack` (which sequences *what* to build) and `ideate` (which decides *whether* to build it). It carries `prompt-pack`'s execute-discipline (**never fake a signal you didn't run**) and `ideate`'s conditional-design (**a design bar only when feel is load-bearing**).

## When to use this

**Strong triggers — invoke without asking:**
- "Tighten this build" / "drive it to near-finish-line" / "make it actually work, not just compile"
- "Iterate until it passes" / "loop until the core flows pass"
- "Self-verify the UI" / "see whether what I built actually renders and works"

**Softer triggers — invoke proactively:**
- A scaffold or feature just landed and you want it driven from "compiles" to "works + holds a craft bar."
- You're about to hand a draft to a human and want the machine-checkable defects gone first.

**Do NOT use this for:**
- Deciding **what** to build or whether it's worth building → that's `ideate`.
- Judging whether a design/strategy/codebase is **sound or safe** → that's `deep-dive`.
- A one-line fix you can make and eyeball in ten seconds → just do it.
- **Validating that people want it** → out of scope (see bounds below); that's the human/market handoff.

**Routing tie-breaker:** `build-loop` answers *"does this build actually work and meet its craft bar?"* — not *"is it the right thing to build?"* (`ideate`) or *"is it sound?"* (`deep-dive`).

## What it can and cannot do (read this before you trust it)

The honest bounds are load-bearing — they're stated here, up front, so no one reads a green loop as more than it is.

- **Catches (objective, trustworthy ground truth):** broken builds, failing tests, dead/half-wired flows, console errors, a control that doesn't actually change its output, missing-asset/404s, contrast and other `axe`-checkable a11y violations, blown performance budgets. These are *machine-checkable* — this is the part that moves a rudimentary scaffold toward near-finish-line craft.
- **Soft on (self-graded taste):** a model screenshotting its own UI and calling it "tasteful" is the monoculture, at the visual layer. The loop drives design *hard* toward a stated bar and reliably flags *ugly/broken/missing*; it stays unreliable on *genuinely good*. The different-model critic (default when design is load-bearing) blunts this, but two correlated models still aren't a user — **a human spot-check is the final taste gate** ("looks good to two models" ≠ "a designer signed off").
- **Cannot see (the last-mile tail — plan for a human to finish it):**
  - **Content wrong against a source of truth it doesn't hold** — e.g. a value marked "invalid" that is actually valid in the target dictionary. The build is green, the flow works, the screenshot looks fine, and the content is still wrong. Without the external oracle, the loop has no way to know.
  - **Subtle correctness/security defects with no failing check** — a race, an auth edge, an off-by-one that no test exercises.
  - **Whether anyone wants it** — "works + looks good" ≠ "people want it."
- **Ceiling: ~80% of the craft, not 100%.** "Near-finish-line" is the **aim, not a guarantee**; the last-mile correctness/security/taste tail is the human's. **Market validation is explicitly out of scope.**

If a defect lands in "cannot see," the loop's job is to **name it and hand it off** — never to paper over it with a passing-looking screenshot.

## Prerequisite — lock the acceptance criteria first

You cannot loop without a target; a loop with no criteria either thrashes forever or stops arbitrarily. **Before iterating, lock:**
1. **Acceptance criteria** — binary, checkable statements of "done" (a machine or a scripted flow can settle each). Detail + examples in `references/acceptance-criteria.md`.
2. **The design bar — conditionally.** If experience/feel is load-bearing to this product (cf. `ideate`'s conditional-design forcing-function), carry a **substantive** design direction from the brief — target aesthetic/vibe, 1–2 reference points, key design principles, the intended "feel" — plus concrete design acceptance criteria, and compose `frontend-design` for the direction + craft. When it's load-bearing the **visual design loop is mandatory and runs every iteration** (step 2) — a passing unit test never substitutes for it. If it's a plain utility, the bar is **plain-but-clear** — say so and don't gold-plate it.
3. **Every criterion countable or observable.** "Award-winning", "beautiful", "production-grade" are unfalsifiable — nothing can close them, so the loop thrashes until the budget runs out. Translate each stated goal into criteria a machine or a scripted flow can settle (states present, contrast ratio, flows completing end-to-end, budgets met), and say plainly which part is **self-graded taste**. A goal that won't translate isn't an acceptance criterion — it's a human gate; name it as one.

If these don't exist yet, write them first (or pull them from the `CONCEPT_BRIEF.md` / pack). No criteria → no loop.

## The loop

Run this cycle each iteration. The detailed per-step playbook — exact invocations, what to look for, how to score — is in `references/loop-procedure.md`.

1. **Build & test** — run the project's own build, type-check, and unit/integration tests via `bash`. Capture exit codes and pass counts as ground truth. **A red build is iteration 0's only job** — get it green before anything else; you can't see or exercise what won't run.
2. **See — the design-critique pass.** Render the *running* UI and critique it. **When design is load-bearing this is mandatory and runs every iteration — a unit/coupling test never substitutes for it.** Prefer an **interactive renderer** you can click and play with (Preview MCP: `preview_start`/`preview_screenshot`/`preview_click`/`preview_fill`/`preview_console_logs`; or Claude-in-Chrome; or computer-use); the always-available fallback is a **Playwright** script that launches the app and screenshots it. Capture the **key states** (empty/loading/error/hover/focus/filled) across **≥2 viewports** (mobile + desktop); critique against (a) the brief's design direction and (b) general craft — hierarchy, spacing/rhythm, typography, color + contrast, motion/interaction feel, state coverage, responsiveness, polish — and emit **design defects with severity**, like machine defects. Compose `frontend-design` for *how to make it good*, not just to flag bad. Capture console errors too. **No renderer? Report the visual loop NOT RUN** (the design bar is unmet for a load-bearing build) — never fake it. Full checklist + exact tool invocations: `references/design-critique.md`.
3. **Exercise** — drive the core flows headless (Playwright or equivalent): click, fill, navigate; assert each flow completes end-to-end. Critically, assert **control→output coupling** — drive each input and confirm the output it claims to govern actually changes (this is how you catch a slider wired to nothing).
4. **Check** — `axe` for a11y (contrast/focus/roles), Lighthouse for performance budgets, and a scan for broken assets/links.
5. **Critique** — turn the above into a **defect list with severity** (Blocker / High / Medium / Low) and the acceptance criterion each one blocks. Every entry points at a checkable signal or a named criterion — **no vibes.** (Optionally, fold in the different-model critic's findings — below.)
6. **Rebuild — then loop again; don't stop because something got fixed.** Fix the **top** defects only, drawn from **both tracks** (machine AND design); don't refactor adjacent code or gold-plate. Then **re-enter at step 1** and re-ask the improvement questions every pass — *what's still broken? what's still below the bar? what would make this better?* **Keep iterating while ANY Blocker/High/Medium defect (either track) is open and BUDGET isn't hit.** Fixing one defect is the *start* of the next pass, not the end of the loop.

**Every iteration advances two co-equal tracks** — (i) the objective machine facts (build/test/flows/console/a11y) and (ii), when design is load-bearing, the design bar. Neither substitutes for the other: green machine facts never excuse a skipped design loop, and a pretty screenshot never excuses a red test. Keep a **per-iteration ledger** carrying both — the objective signals (build exit, test pass count, flows passing, console-error count, a11y-violation count) **and** a design column (design-bar criteria met / design defects open). The objective signals are ground truth; the design column mixes checkable items (states present, contrast, responsiveness) with self-graded taste — keep the soft part labeled. That ledger *is* the craft-delta evidence you report — not "it looks better."

## The stop-condition (no infinite thrash)

Stop and report the moment **any** of these fires:

- **PASS** — **no open Blocker/High/Medium defect on either track**: all acceptance criteria met, build/tests green, and (when design is load-bearing) the design bar met via the visual loop. A green build/test alone is **not** PASS — and neither is "fixed a couple of things" while the ledger or the critic still lists open Medium+ defects. (Success — hand off; any Low/Note residue goes in the report.)
- **PLATEAU** — **2 consecutive iterations with genuinely no progress** (no acceptance criterion newly passed AND no defect of severity ≥ Medium closed). A re-critique or the different-model critic **surfacing new Medium+ defects is progress to act on next pass, not a plateau.** (True diminishing returns — hand off what's left.)
- **BUDGET** — the rebuild cap for this surface is reached (**default 4 rebuild passes per surface, plus at most one different-model critic pass; never set below 3 for a design-load-bearing build; caller-settable**). This is the finite hard backstop. When it fires, **ship the strongest version you have** and record what you'd do next — the open queue is the hand-off, not a reason to keep swinging.
- **BLOCKED** — the next defect needs a human or real-world signal the loop can't get (a taste call, an external-oracle/content check, a paste-into-production test). **STOP and emit it** as a human gate — carrying `prompt-pack`'s execute-discipline: never fake it, render a passed-looking result, or build past it to look complete.

**Why this can't infinite-loop:** BUDGET is an unconditional counter — even if PASS, PLATEAU, and BLOCKED never trigger, the loop halts at N iterations. The other three only ever stop it *sooner*. Every run terminates.

Always report the **iteration count** (how many full passes ran), the **per-iteration ledger** (both tracks), **which condition fired**, and the **open-defect queue at stop** — so a one-pass run on a non-trivial build is visibly incomplete and a premature stop is obvious. The craft-delta is the ledger, not a vibe. (More passes close *checkable* defects — they don't reach the last-mile tail the loop can't see; don't read "more iterations" as "perfect.")

## Scope the battery to the change (claim-narrowing, never gate-weakening)

Re-running the entire battery for every change is quadratic — the battery grows, each pass costs more, and eventually verification is the whole run. Scope each pass by what the change can actually reach.

- **Full battery** — any change that can affect product behaviour. This is the default; when in doubt, you're here.
- **Scoped battery** — changes that *provably cannot* touch product behaviour: tooling, docs, the verification machinery itself. Run what the change reaches, and **state in the ledger what the scoped run asserts and what it inherits rather than re-proves.**
- **Repeat/stability runs** (10×, 50×) — only where there's prior evidence of flakiness in that surface, never as a standing tax on every pass.

**This is claim-narrowing, not gate-weakening.** A narrower run must assert **strictly less** and say so out loud — it never lets a defect past a gate that would otherwise have caught it, and it never re-labels an unrun check as green. If you can't name precisely what the scoped run inherits, you haven't narrowed the claim: run the full battery.

## Keep the verification machinery proportionate

Verification apparatus compounds. Every check you add is re-run, maintained, and repaired forever after — left unbounded it quietly consumes the run, and you end up with more checker than product.

- **If you're writing a checker whose job is to police another checker** — or a repair whose only purpose is to let a previous verification close — **stop and simplify rather than extend.** That's the apparatus feeding itself, not the build getting safer.
- **If a single atomic verification chain grows longer than the window in which it reliably completes**, split it into independently-provable segments. A late failure in a long chain discards every good result before it, and you pay the whole chain again just to reach the next defect.
- Watch the ratio: when the machinery is growing faster than the thing it verifies, that's the signal to cut, not to build more.

## The different-model critic (default when design is load-bearing; optional for plain utilities)

The builder grading its own taste is a monoculture at the visual layer. A critic running a **different model**, handed **only** the screenshots + acceptance criteria + design bar (blind to the builder's own rationale), surfaces taste/quality judgments the builder shares with itself and can't see. Fold its defects into step 5's critique.

**Modularity is locked:** for a **plain utility** the critic is optional and the loop runs **fully without** it — the objective signals (build/test/flows/console/a11y) never need a second model. When **design is load-bearing**, run the critic **by default** as the taste check — but it stays an enhancement on the design track, never a gate on the objective signals, and never a substitute for actually rendering the UI. Honest limit: even with it you have two correlated models, not a user — the **human spot-check is the final taste gate**; still zero market signal.

## Environment & fallbacks (run anywhere)

The method is portable; only the tooling degrades. Substitute the fallback and **say so in the report** — a signal you couldn't run is reported as **not run**, never as passed (execute-discipline).

| Capability | If unavailable |
|---|---|
| `bash` build/test | Core — if you can't build/test, you can't loop; stop and say so. |
| Render + screenshot (*see*) | Prefer an interactive renderer (Preview MCP / Claude-in-Chrome / computer-use); else a Playwright screenshot script. If **none** can run: report the visual loop **NOT RUN** — and when design is load-bearing the design bar is unmet, so you cannot PASS; never fake it. For a plain utility, proceed on the objective signals and note the gap. |
| Playwright/headless (*exercise*) | Fall back to whatever drives the surface — run the CLI, call the API, hit the endpoint — and assert outputs. Skip only if there's genuinely no exercisable surface. |
| `axe` / Lighthouse (*check*) | Skip the a11y/perf checks; report them as not run. |
| Different-model critic | Run the loop without it (it's optional by design). |

**Non-browser surfaces** (a CLI, a library, a backend) have no *see* step — run build/test plus a targeted *exercise* (invoke the binary, call the function/endpoint, assert the result) and skip the visual steps. The loop still earns its keep on the objective signals.

## Pitfalls to avoid

- **Looping with no acceptance criteria** — guarantees thrash or an arbitrary stop. Lock the target first.
- **Chasing an unfalsifiable bar** — "make it beautiful / award-winning / production-grade" can never be closed, so the loop just burns the budget. Translate it into countable criteria before iterating, and label the taste part self-graded.
- **Re-proving what the change couldn't have touched** — a full battery on a docs or tooling edit isn't rigour, it's cost. Narrow the *claim* honestly instead — never the gate.
- **Substituting a unit test for the visual loop when design is load-bearing** — a green programmatic check is *not* a design pass. If feel is load-bearing, render + screenshot + critique the real UI every iteration, or report the visual loop NOT RUN. (This is the exact shortcut a proof run took once — don't repeat it.)
- **One-shot design instead of iterated** — judging the UI once and never again. The design bar is advanced every iteration alongside the machine facts, not eyeballed at the end.
- **One-and-done** — fixing a defect or two, then declaring done while the critic or the ledger still lists open Blocker/High/Medium defects. That's stopping *before* a real stop-condition fires; keep looping until none are open or BUDGET hits. (The exact shortcut a proof run took: one fix, the critic surfaced more, it stopped anyway.)
- **Treating self-graded "looks good" as a pass** — it's the monoculture. Pass on objective signals; let the critic + a human handle taste.
- **Faking a signal you couldn't run** — a skipped check is reported skipped, never green.
- **Reinventing the harness** — compose the existing tools; if you find yourself writing a bespoke test-runner/agent framework, stop (that's not this skill).
- **Looping past the plateau** — diminishing returns are a hand-off signal, not a reason to grind. The last-mile tail is the human's.
- **Reading "works + looks good" as "validated"** — market validation is not in scope; don't imply it.
- **Guessing at a content/correctness defect** — if settling it needs an external oracle the loop doesn't have, emit it as a human gate, don't invent the answer.

## Scale heuristics

| Situation | What to run |
|---|---|
| A tiny change that just needs to compile | One pass: build + test, eyeball. No full loop. |
| A fresh scaffold or feature (plain utility) | Full loop, N≈3–4, acceptance criteria; design bar = plain-but-clear. |
| A build where feel **is** the wedge | Full loop with the **visual design loop every iteration** (render → screenshot key states × viewports → critique) + the different-model critic **by default** + a flagged human spot-check as the final taste gate; substantive design bar (compose `frontend-design`). |
| A non-browser CLI/library/backend | Build/test + targeted exercise; skip *see*; objective signals only. |

The loop scales down to a single build/test pass and up to a multi-iteration, critic-augmented drive — but the discipline is constant: a checkable target, an honest ledger, a stop-condition, and a clean hand-off of the tail it cannot see.
