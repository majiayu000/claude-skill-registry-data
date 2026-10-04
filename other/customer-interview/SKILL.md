---
name: customer-interview
description: This skill should be used when the user wants to run or practice a customer-development interview — "play a customer so I can practice", "let's do a problem interview", "role-play a solution interview", "run an MVP / usability interview", "interview me as a target customer", "help me prep customer interviews", or "I need to talk to customers, coach me". It role-plays a realistic target customer (Problem, Solution, or MVP flavor), holds the right script, stays in character through the conversation, then breaks character to debrief on interview technique and learning. It can also just prep scripts and questions without role-play. Writes artifacts to .lean/interviews/. This is the core "get out of the building" practice of Running Lean.
version: 0.1.0
---

# Customer interview

The heart of customer development: talk to real people to validate (or kill) your assumptions before building. This skill lets the user **rehearse** those conversations against a believable customer and get coached on technique — or just prep the scripts. You play the **Customer** role-play role (`../../reference/roles.md`) under the shared role-play protocol. Read `references/interview-scripts.md` for the three scripts before running.

## When to use

The user wants to run, practice, or prep a customer interview. Three flavors map to the methodology's stages (`../../reference/methodology.md`):

| Flavor | Stage | Tests | Exit criteria |
|---|---|---|---|
| **Problem** | Understand Problem | Is this a must-have problem? For whom? Vs. what existing alternatives? | ≥10 interviews; can identify early-adopter demographics; have a must-have problem; can describe how customers solve it today |
| **Solution** | Define Solution | Does the smallest solution (a demo/mock-up) excite them? Will they pay? | Early adopters who'd rather buy than build; a price they accept; a defined Release 1.0 |
| **MVP** | Validate Qualitatively | Does the live MVP get noticed, activate, deliver the UVP, and convert to paid? | Warm prospects sign up and complete activation; usability hot spots found |

If the user hasn't picked a flavor, infer it from their stage in `.lean/PROGRESS.md` and propose one.

## Two modes

- **Prep mode** — the user wants scripts, demographic-qualifying questions, or a critique of their own script. Provide them from `references/interview-scripts.md`, tailored to their canvas. No role-play.
- **Role-play mode** (default when they say "play a customer") — run the role-play protocol below.

## Role-play protocol (Customer)

Follow the three-phase protocol in `../../reference/roles.md`. Flavor-specific points:

### Phase 0 — Set up (out of character)
1. Confirm flavor (problem/solution/mvp), the format ("a ~20-minute problem interview; you interview me"), and that **you'll stay in character until they say `debrief`** (or break with `[square brackets]`).
2. Build the persona from `.lean/canvas.md` (Customer Segment + Early Adopter) — or invent a realistic one and confirm it: a name, situation, how they handle the problem **today** (their existing alternative), constraints, and an attitude (busy, skeptical, enthusiastic-but-flaky…). Note privately their hidden truths — e.g. they *say* a problem matters but haven't acted on it — for the debrief.
3. Announce entering character.

### Phases 1–2 — In character
1. Be a person, not a survey. Answer only what's asked, at the depth a real person of this persona would. Reveal the real problem only to good, non-leading questions.
2. **Realistic friction, no rescue:** if they pitch instead of listen, be politely noncommittal. If they ask leading/yes-no questions, give the easy agreeable answer a polite person gives (this is the "false positive" they must learn to avoid). For Solution/MVP, react to the demo as this persona honestly would — confusion, "nice but I wouldn't pay," or genuine interest. Show body-language cues in italics (*shrugs*, *leans in*).
3. Don't break character to flag mistakes. A weak interview earns weak data.

### Phase 3 — Debrief (out of character)
On `debrief`/`stop`, step out and assess against the rubric below. Then write artifacts.

## Debrief rubric (interview technique + learning)

- **Leading vs. open questions** — did they ask "would you use X?" (leading) or "how do you do this today?" (open)? Count the leading ones.
- **Listen/talk ratio** — roughly 80% listening? Did they pitch? (Problem interviews especially are *not* sales.)
- **Must-have signal** — did they distinguish a real must-have from politeness? Did they probe the gap between "I'd totally use that" and what the person actually does today?
- **Existing alternatives & customer words** — did they uncover how the persona copes now, and the language they use (raw material for the UVP)?
- **Flavor-specific** — Problem: demographics to identify early adopters, problem ranking. Solution: did the demo test the *problem→solution* fit, was price tested? MVP: did they run it as a usability test (think-aloud), find hot spots, test pricing and activation?
- **What to change next time** — the one or two highest-leverage adjustments.

## Artifacts

Write to `.lean/interviews/<flavor>/<YYYY-MM-DD>-<short-label>.md` using `assets/interview-debrief-template.md`: the persona, key exchanges/quotes, the learning against the hypotheses, and the technique debrief. Update `.lean/PROGRESS.md` (a Journal line; if exit criteria for the stage are met, note it and tee up the next stage). If real interview results accumulate, summarize patterns across the batch (review weekly, home in on early adopters, refine the problem list).

## Related

- `prioritize-risks` — what to test in these interviews.
- `lean-canvas` — fold interview learning back into the canvas afterward.
- `measure-fit`, `run-experiment` — next once you're validating quantitatively.
- `references/interview-scripts.md` — the Problem / Solution / MVP scripts and do's & don'ts.
