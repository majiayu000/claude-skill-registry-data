---
name: first-mocks
description: >-
  Turns a concept into the cheapest concrete artefact a human can react to, via
  the no-code make-sequence: Crazy 8s → paper/Miro flow → digital mock →
  clickable hybrid in v0 or Figma Make, built in one afternoon. Fires on "mock it
  up", "run Crazy 8s", "clickable prototype", "turn this idea into something I can
  click", "get from a rough idea to a prototype in an afternoon". Output is a
  Clickable-Prototype Plan: the ONE thing the mock must provoke a reaction to, the
  fidelity band, the no-code ceiling, and the hand-off to a real reaction. NOT
  which experiment to run (probe-matrix), NOT running the test session
  (usability-test-protocol), NOT the visual / UI craft — colour, type, distinctive
  components — which it ROUTES to impeccable / shape / design and never restates.
  Bans jumping to code.
type: interactive
supersedes: none
---

## What it does

Takes a concept you can only describe in words and forces it down to the cheapest
artefact a human can actually react to. It runs the make-sequence — Crazy 8s →
paper/Miro flow → digital mock → clickable hybrid — and stops at a clickable
prototype built in one afternoon, no code. The output is a Clickable-Prototype
Plan (`template.md`): the ONE moment the mock must provoke a reaction to, the
fidelity band that reaches it, the hard no-code ceiling, where the visual craft
gets routed, and the hand-off to a real reaction. It does not draw the pixels and
it does not run the test. Its job is to convert an abstraction into something
concrete, fast, and disposable — then get out of the way.

## The Icarus reframe

A mock is not a small version of the product. It is the cheapest concrete thing a
human can react to, because people give useless feedback on a description and
useful feedback on an artefact. So fidelity is set by one question — what is the
least-built thing concrete enough to provoke a real reaction to the ONE moment I
am unsure of — under a hard ceiling: no code, one afternoon. Code is banned here
because it converts a disposable question into a defended commitment, and because
the Crazy 8s exist to force divergence that a code editor kills the moment you
start building the first idea you had. The generic fidelity ladder keys the choice
to how much you want to build; this keys it to how little you can build and still
get a real reaction.

## When to use / When NOT

Use it when you have a concept and need a concrete artefact people can react to,
before you write any product code. It sits after you know what you are testing and
before anyone watches a user or ships a line.

Do not use it for these — hand off instead:

| If the fellow wants… | Use instead | Why not this skill |
|---|---|---|
| Which cheap experiment answers their ONE learning question (paper / WoZ / concierge / agent) | `probe-matrix` | That selects the experiment and its honesty; this MAKES an artefact. Route there first if the question is "which test." |
| The paper sketch run as an evidence-gathering probe | `paper-sketch-probe` | That runs a sketch as a probe with a read-out; the paper step here is one rung in a make-sequence, not the probe. |
| To watch a user react to the mock and score it | `usability-test-protocol` | That runs the session and captures behaviour (0.7); this produces the thing the session uses. |
| The visual / UI craft — layout, colour, type, distinctive non-generic components | `impeccable` / `shape` / `design/*` | Those own the look and do it better. This routes to them and never restates them — restating one is the kill line. |
| To write the real product code | `compound-system-architecture`, `eval-first-spec` (07) | The moment you write product code you have left first-mocks. Code is banned at this stage. |

This skill owns the sequence and the anti-code discipline. It does not choose your
experiment, run your test, style your pixels, or build your product.

## Method

Fill in `template.md`. One question, then four make-bands, then two hand-offs.

**Step 0 — Name the ONE thing the mock must provoke a reaction to.** One moment,
one flow, one decision. Write the reaction you are hunting: "can they see the next
action cold", "which of these two flows confuses less", "does this moment read as
X." A mock answers legibility / comprehension / flow questions (does the artefact
make sense). It does NOT answer will-they-pay or would-they-use-it — those need a
probe (`probe-matrix`), because a mock tops out at "artefact shown" (0.5). If Step
0 is blank you will build a demo of everything and learn nothing. If Step 0 is a
solution ("mock the mobile app"), it is a solution-in-disguise — reframe to the job
first (`problem-statement`), then return.

**Steps 1–4 — The make-bands.** Climb only as far as the reaction needs. The
ceiling is fixed at each band; breaking it is the failure named in the last column.

| Band | Artefact | Concrete enough to provoke… | Timebox | Ceiling — do not cross |
|---|---|---|---|---|
| 1 Crazy 8s | 8 rough frames, one moment each | your own divergence; which directions even exist | 8 min | pencil only; no favourite yet |
| 2 Paper / Miro flow | one flow: screens as boxes, actions as arrows | is the path legible to you / a colleague | ~30 min | no pixels |
| 3 Digital mock | static frames (Figma / slides / Miro) | can someone read the moment cold | 1–2 hr | no code |
| 4 Clickable hybrid | frames wired to click the ONE flow (v0 / Figma Make) | can a hand click it and react | one afternoon (≤ ~4 hr) | no backend, no real data, no auth, no code you'd keep |
| — | product code | nothing new at this stage | — | BANNED here — belongs to build (07), gated by `v1-launch-bar` |

**Step 1 — Crazy 8s.** 8 frames, 8 minutes, one screen or moment per frame. The
first frame is a reflex; the value is in the strange 6th–8th. Keep the odd child.
Fewer than 4 genuinely different directions means you decorated your first instinct
— redo it cold. Do not skip to the layout you already had in mind. If real
divergence already exists — you arrive with several genuinely different rough
layouts — band 1 is already satisfied; converge them at Step 2 instead of forcing a
fresh eight-frame round. The bar is divergence, not the ritual.

**Step 2 — Converge to one flow on paper / Miro.** Pick the clearest through-line,
not the prettiest frame. Lay the flow: boxes for screens, arrows for the actions
that move between them. This skeleton is what the clickable hybrid will wear. Still
no pixels.

**Step 3 — Digital mock, no code.** Turn the paper flow into static digital frames.
This is where the code editor calls. Do not answer it. The mock is disposable; code
is not, and the moment it exists you start defending it.

**Step 4 — Clickable hybrid in an afternoon.** Wire the frames in v0 or Figma Make
into something a hand can click through the ONE flow. "Hybrid" means real enough to
click, faked everywhere else — no backend, no real data, no auth. The scaffold v0 or
Figma Make emits to make the frames clickable is NOT the banned "code": the ban is
on hand-writing product code you would keep and defend. A disposable generated
scaffold you would delete without a pang is fine; a backend you start maintaining is
not. Timebox one afternoon. If it runs into days you are building the product, not
mocking it; stop.

**Step 5 — Route the visual craft OUT.** Do not polish pixels here. Hand the flow
to `impeccable` / `shape` to plan the UX/UI, and `impeccable` to build distinctive,
non-generic UI, or `design/*` for a specific surface. first-mocks owns the sequence
and the no-code discipline; the look is theirs. Restating their layout / colour /
type advice inside this skill is the kill line.

**Step 6 — Hand to the reaction, pre-registered.** The mock is an input, not an
answer. Route to `usability-test-protocol` to watch a user react (behaviour, 0.7),
or back to `probe-matrix` if the ONE thing needs a probe. Write the reaction that
counts as a pass BEFORE anyone sees the mock. The mock produces 0.5; the reaction
is where the 0.7 you actually want gets made.

## Evidence standard

A mock is an artefact shown — 0.5 on the ladder (money 1.0 → behaviour 0.7 →
artefact 0.5 → verbal 0.3 → opinion 0.1) — and no higher. It cannot tell you they
want it (behaviour, 0.7) or will pay (money, 1.0). Its only job is to convert an
abstraction into something concrete enough that a downstream test produces a real
0.7 / 1.0 read-out. Done means: a clickable hybrid, built in one afternoon, no
code, visual craft routed out, and a pre-registered reaction handed to
`usability-test-protocol` or `probe-matrix`. Tag every empirical claim `[Fact]`,
`[Assumption]`, or `[Hypothesis]`; a mock's look and feel is at most `[Hypothesis]`
until a user reacts to it. **Kill line — the moment the mock becomes product code,
or the moment this skill restates a design skill's craft instead of routing to it,
it has failed.**

## Gotchas

- **Code is the seductive shortcut and the trap.** v0 and Figma Make blur into a
  real app, and "I'll just wire the backend" turns a disposable mock into a defended
  commitment you now argue for instead of about. The ceiling — no backend, no data,
  no auth, one afternoon — is the whole discipline. If you would be sad to delete it,
  you built too much.
- **Skipping the Crazy 8s to the idea you already had.** The 8 frames exist to kill
  your first reflex. One or two variations is decoration, not divergence; if every
  frame is a tweak of the first, you diverged nothing. Redo cold, and force yourself
  past the obvious to the strange frames where the non-generic idea lives.
- **Polishing pixels inside first-mocks.** The pull to make it pretty here is
  strong, and it is `impeccable`'s job, done better. Writing colour, type, or layout
  guidance into this output is the kill line — route it out. Keep first-mocks about
  the sequence and the concrete-reaction logic.
- **Reacting to the mock as if it were evidence.** A polished clickable prototype
  feels like validation. It is 0.5, an artefact shown; no one used it under stakes
  and no one paid. When a fellow says "people loved the prototype," ask what they
  DID, not what they said — the mock is the setup for the test, not the test.
- **A mock aimed at everything.** With Step 0 blank the fellow builds a demo of the
  whole product and learns nothing clean, because no single reaction is isolated.
  One moment, one unknown, one mock.

## Examples

`examples/sample.md` — Mentix mocks the copilot's shift-handover card. The ONE thing
is whether a plant manager, mid-shift, can read the card cold and act on the flagged
line. The run diverges with Crazy 8s (keeping the odd "one sentence + expand"
frame), converges on paper, wires four frames into a clickable hybrid in v0 in an
afternoon with clearly-illustrative data, routes the look to `impeccable`, and hands
a pre-registered comprehension read-out to `usability-test-protocol`. The mock is
logged at 0.5; the read-out is where 0.7 is made.

## Related skills

Absorbs `discovery/prototyping-pretotyping` — it keeps the useful bones (match
fidelity to the question, throw the prototype away, behaviour over opinion) and
reframes them around one axis the old skill never names: the least you can build and
still get a real reaction, under a no-code afternoon ceiling. It does not supersede
it; `probe-matrix` already does, on the experiment-selection axis. first-mocks takes
the other half — the make-craft — and stays disciplined about not being the test.

Composes with: `probe-matrix` (selects the experiment; run it first if the question
is "which test," and return here to make the artefact a paper-sketch probe needs),
`usability-test-protocol` (runs the session that turns this 0.5 mock into a 0.7
read-out), `impeccable` / `shape` / `design/*` (own the visual craft this skill
routes to and never restates), and the build skills in section 07
(`compound-system-architecture`, `eval-first-spec`, gated by `v1-launch-bar`) that
own the product code this skill bans.
