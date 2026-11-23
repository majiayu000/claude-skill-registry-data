---
name: synthetic-users
description: >-
  Builds a synthetic user panel grounded in the team's proprietary data and pre-tests a concept,
  message or flow on it before real interviews, with a ledger of what synthetic users get wrong
  and a kill / revise / take-to-real-interview verdict. Use when the user wants to simulate a
  user, dry-run a pitch, or pre-test before booking interviews. Not for planning real interviews
  (use discovery-interview-prep).
type: interactive
supersedes: none
---

## What it does

Takes a concept, a message, or a flow you are about to take to real customers, and runs it past a small panel of synthetic users built from your YODA corpus — the field logs, shadow threads, and tacit captures a foundation model cannot reach. It returns a Synthetic Panel + Pre-Test Transcript: each panellist grounded in a named slice of the corpus, the concept posed to each, and every response tagged with which known lie could be corrupting it. The output is a kill / revise / promote verdict, not a verdict of "validated". Its only legitimate job is to eliminate weak concepts and prioritise which real interview to run first. A synthetic "yes" is worth nothing; a synthetic "I don't understand this" is worth acting on.

## The Icarus reframe

The generic move is to prompt an LLM to role-play a persona and ask it whether it likes your idea. It will say yes, because a base model agrees, never pays, and never no-shows. That is not a test; it is a machine built to flatter you. The Icarus version fixes two things. First, ground every panellist in your proprietary corpus, not the model's prior — a persona a generic prompt could invent only tells you what every competitor's model already believes about your market. Second, run it as a kill screen, never a validation: positive signal is null, negative signal (confusion, an existing workaround, a flow that breaks) also requires a real-user check before it can be generalized, and even then it caps at [Hypothesis]. Synthetic output sits below opinion on the evidence ladder. Its whole value is spending a real interview well, not replacing it.

## When to use / When NOT

Use it when you have a YODA corpus and a specific thing to pre-test — a concept, a message, or a flow — and you want to kill the weak ones before booking real interview time. It is the rung one below a real cheap test: cheaper, faster, and less trustworthy, run first to decide what is even worth a real interview.

Do not use it for:

| If the fellow wants… | Use instead | Why not this skill |
|---|---|---|
| To watch a real expert do a real task and capture their judgment | `tacit-knowledge-interview` | That creates real behaviour signal (0.7); this simulates and caps at [Hypothesis]. This runs *before* it to decide whether that interview is worth booking. |
| A Mom-Test script for a real discovery interview | `discovery-interview-prep` | That prepares questions for a real person; this poses a concept to a simulation. |
| To plan/prep real discovery interviews (goal, segment, method) | `discovery-interview-prep` | That plans the real round; this pre-screens what the round should even cover. |
| To source the proprietary data the panel is built from | `proprietary-data-sourcing` | That finds the corpus; this consumes it. No corpus, no grounded panel — see Step 0. |
| To find the unmet need, or map who the buyer is | `unserved-needs-finder`, `user-buyer-decider-map` | Those define what to build for and who buys; this pre-tests a concept once you have one. |

Never use it to produce a "validated" claim. That is the one output it must refuse (see Kill line).

## Method

Fill `template.md` as you go. The watch-out running through every step: a synthetic response is not evidence, it is a hypothesis the panel generates for a real interview to test.

### Step 0 — No corpus, no panel

A synthetic user is only worth building from real proprietary data. If the fellow has no YODA corpus — no field logs, no shadow threads, no tacit capture, no transaction record — stop. A persona built from the base model is the model's prior about your market wearing a name tag, and testing your concept against it tells you exactly what every competitor's model would also say: nothing proprietary. Route to `proprietary-data-sourcing`. For each panellist you do build, name the corpus slice it is grounded in. A panellist with no named slice is a fiction; delete it.

### Step 1 — Declare the target and the kill question

Name exactly one thing you are pre-testing, and the one signal that would kill it.

| You are pre-testing a… | The kill signal is… |
|---|---|
| Concept (does the value land?) | They don't want it, or they already solve it a cheaper way |
| Message (does the positioning parse?) | They can't say back what it does, or they read it as something else |
| Flow (where do they get stuck?) | They stall at a specific step, or take the wrong branch |

Write the single sentence: *a synthetic "no" here would kill/revise ______.* If you cannot state what a "no" kills, you are fishing for a "yes" — and the panel will give you one. Stop and fix the target first.

### Step 2 — Build the panel from the corpus, not from imagination

Three to six panellists. Not more. More synthetic users is not more signal — they share the base model's single prior, so a panel of fifty is one opinion repeated fifty times with variance noise. Diversity comes from grounding each panellist in a *different* slice of the corpus, not from cranking the count. Each card:

| Field | What goes in it |
|---|---|
| Who | The role this panellist stands in for |
| Grounded in | The named corpus slice(s) — e.g. "40 field-log write-ups + tacit capture of the safe-to-proceed call". Cite it. |
| On record | The observed behaviour the corpus actually shows for this role — the facts you will hold the simulation to |
| Known gap | What the corpus does NOT tell you about this person, so the simulation is guessing there |

### Step 3 — Run the pre-test as a kill screen

Pose the concept, message, or flow to each grounded panellist and capture the transcript. Then score only for kill signals. Enthusiasm is discarded before it is read.

| Synthetic response | Read it as | Action |
|---|---|---|
| Confusion — can't parse the message / value | Candidate issue, transfer unverified | Log it; it is the highest-value output here |
| Names an existing workaround from the corpus | Candidate issue, transfer unverified (the corpus is talking) | Log it; the concept may be competing with a free habit |
| Stalls at a specific flow step | Kill/revise signal | Log the exact step |
| Flat "no / I wouldn't" | Weak kill signal | Log, but a real check is cheap; do not over-weight |
| "Yes / I'd use this / great idea" | **Null** | Discard. Acquiescence + never-pay. Reading this as a win is the whole trap. |
| "I'd pay $X" | **Null, and dangerous** | Discard. See lie ledger, never-pay. |

### Step 4 — The lie ledger

Tag every logged response with which lie could be corrupting it. This is the part a generic prompt never does, and the reason the output cannot be mistaken for validation. The lie set is fixed:

| Lie | What synthetic users do | So distrust… |
|---|---|---|
| Never pay | No budget friction; agree to any price | Any willingness-to-pay signal. WTP needs money-moved, from a real person. |
| Never no-show | Infinite attention and time; no calendar scarcity | Any engagement or adoption prediction — it is inflated |
| Over-rationalise | Give tidy causal reasons; real humans act on impulse and confabulate | The "why they'd choose". Trust the "what confuses them" more than the "why". |
| Over-agree (acquiescence) | Lean toward liking your thing and accepting your framing | All positive signal. Only negative signal is informative. |
| No org / politics | No procurement, no boss, no turf, no switching cost | Any B2B "we'd adopt this" — the buying friction is invisible |
| Over-informed | Recall and reflect too cleanly; answer as if they'd already thought it through | Any discovery "aha" — a real user would not have surfaced it unprompted |

For each logged response, write: the lie tag, and one call — *does this transfer to a real user?* Use the transfer table in the Evidence standard.

### Step 5 — Verdict: kill / revise / promote

Three outcomes. There is no fourth.

| Verdict | When | Next |
|---|---|---|
| **KILL** | A corpus-grounded panellist could not grasp the concept, or named a cheaper existing path | Pause or revise the concept for the next real check. Do not permanently reject it on synthetic output alone; confirm the alleged failure with a real target user or direct corpus evidence. |
| **REVISE** | The message or flow broke at a specific, nameable point | Fix that point and re-run the panel — it is cheap |
| **PROMOTE** | It survived the synthetic kill screen | It has *earned a real interview* — `tacit-knowledge-interview` / `discovery-interview-prep`. Surviving synthetic is a ticket to spend the real interview, not validation. |

**Kill line.** The output must never say "validated", and must carry the lie ledger. If it presents a synthetic response as real validation, or omits the what-they-lie-about caveat, it is auto-failed — that is the exact failure this skill exists to prevent.

## Evidence standard

A synthetic response is not on the ladder; it sits below its bottom rung. Real opinion scores 0.1. A synthetic opinion is a model's guess at what an opinion would be — pre-evidence. The best a synthetic panel can produce is a [Hypothesis] worth (or not worth) a real interview. It can lower your confidence cheaply (a kill) and it can order your real interviews (a priority), but it can never raise your confidence, because it never moved money or showed behaviour.

Which synthetic signals transfer to a real user:

| Synthetic signal | Transfers? | Why |
|---|---|---|
| Confusion / can't parse the message | Unknown until tested | Model confusion can be a false negative. Test the specific wording with real target users; it does not establish human confusion. |
| Names a workaround already in the corpus | Often | It is echoing recorded behaviour, not the model's prior |
| Relative ranking of two framings | Direction only | Use the ranking only to propose a real comparison; neither its direction nor magnitude is validated |
| "I would use this" / enthusiasm | No | Over-agree + never-pay + never-no-show, stacked |
| "I would pay $X" | Never | Never-pay. WTP is money-moved, and this is a simulation. |
| A tidy reason "why" they'd choose | No | Over-rationalise |

Done means: every panellist is grounded in a named corpus slice, every logged response carries a lie tag and a transfer call, the verdict is one of kill/revise/promote, and the word "validated" appears nowhere near a synthetic result. Tag each claim `[Fact]`, `[Assumption]`, or `[Hypothesis]`. Nothing a synthetic user says is ever [Fact].

## Gotchas

- **The confirmation machine.** Fellows build panels to hear yes, and a synthetic panel will say yes to almost anything — over-agree plus never-pay. If your run came back mostly positive, you did not test; a machine flattered you. Re-read only the negatives, and if there are none, distrust the run before you trust the concept.
- **An ungrounded panel is the base model's prior in costume.** If a panellist is not built from a specific corpus slice, you are testing your concept against what the foundation model already believes about your market — the same belief every competitor's model holds. Zero proprietary signal. This is the failure `proprietary-data-sourcing` guards against, one level up.
- **Panel inflation feels like rigour and isn't.** Fifty synthetic users share one prior; you get one answer with noise dressed as a sample. Signal comes from grounding breadth — different corpus slices — not headcount. Four well-grounded panellists beat fifty clones.
- **Survival is not validation.** A concept that survives the synthetic screen has earned a real interview, nothing more. The lie ledger exists so no one reads "the synthetic users loved it" as evidence. The moment "validated" sits beside a synthetic result, the skill has failed its own kill line.
- **Demand characteristics.** The synthetic user infers what you want to hear from how you phrase the concept, and hands it back. Where you can, pose the flow or message neutrally — describe the situation, not the pitch — so a "no" has room to happen.
- **Invented quotes are not corpus quotes.** Every line a synthetic panellist "says" is generated, never recorded. Tag each one `[Hypothesis]` and attribute it to the named corpus slice it is extrapolated from — never present it as a verbatim quote lifted from the corpus, and never attach a real number the corpus does not hold. A fabricated line dressed as a real one trips the fabrication auto-fail, the exact failure the [Fact]-forbidden rule and the lie ledger exist to prevent.

## Examples

See `examples/sample.md` for a full run on Mentix: a four-panellist panel built from field logs, shadow threads, and the tacit capture of the "mute the vibration alarm" judgment pre-tests the copilot's positioning. Three panellists are enthusiastic (discarded), but the one grounded in the tacit capture is confused because the copilot's suggested action collides with the "never override within an hour of a bearing change" rule — the one signal that transfers. Verdict: revise the message, then promote to a real usability check.

## Related skills

- `proprietary-data-sourcing` (section 03) — sources the corpus this skill consumes. Run it first; a panel with no corpus is Step 0's stop.
- `tacit-knowledge-interview` (section 02) — the real interview this skill pre-tests *before*. A captured judgment is also excellent grounding for a panellist. Promote survivors here; never let this skill stand in for it.
- `discovery-interview-prep` (section 02) — the real Mom-Test round. This skill decides what that round is even worth covering.
- `unserved-needs-finder`, `user-buyer-decider-map` (section 02) — define the need and the buyer; this pre-tests a concept once you have one.
- `probe-matrix` (discovery) — the next rung up: a cheap test with real people. Synthetic pre-test comes below it, run first to decide what to pretotype.

Supersedes: none. Fully proprietary — there is no prior synthetic-user skill in the pack, and the generic "role-play a persona" pattern is the exact anti-pattern this skill is built to correct.
