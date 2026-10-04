---
name: investor-pitch
description: This skill should be used when the user wants to rehearse or stress-test a fundraising pitch — "play an investor", "let's practice my pitch", "be a skeptical VC and grill me", "pitch practice", "what would an investor ask?", "is my traction story convincing?", or prepping for an angel/seed meeting. It role-plays a skeptical-but-fair investor, holds a realistic pitch + Q&A, stays in character, then breaks character to debrief on the traction-first narrative, command of the numbers, and defense of the riskiest assumption. It can also just prep a pitch or critique a deck without role-play. Writes to .lean/pitch/.
version: 0.1.0
---

# Investor pitch

Rehearse the fundraising conversation against a believable investor and get coached on it — or prep the pitch. You play the **Investor** role-play role (`../../reference/roles.md`) under the shared role-play protocol. Read `references/pitch-traction.md` before running.

## When to use

The user wants to practice or pressure-test a pitch, anticipate investor questions, or sanity-check their traction story. Also covers prepping the narrative or critiquing a deck (prep mode, no role-play).

First, a coach's caution worth stating once: in Running Lean, the **ideal time to raise a big round is after product/market fit**, when your goal (growth) and the investor's align. Raising before that is fine for a small runway, but if `.lean/PROGRESS.md` shows a pre-fit venture with no traction, say so — the most useful "pitch practice" may be a reality check that the real next step is more validation, not a deck.

## Two modes

- **Prep mode** — help structure the pitch (traction → problem → solution → market → model → team → ask), draft talking points, or critique their deck/narrative against `references/pitch-traction.md`. No role-play.
- **Role-play mode** (default for "play an investor") — run the protocol below.

## Role-play protocol (Investor)

Follow the three-phase protocol in `../../reference/roles.md`.

### Phase 0 — Set up (out of character)
1. Confirm the scene: investor type (angel / pre-seed / seed VC), format ("5-minute pitch, then I grill you for 10"), and the `debrief` / `[bracket]` signals.
2. Load `.lean/` — canvas, risks, metrics — so the investor probes *this* venture's real weak points (the riskiest assumption from `risks.md`, the actual traction in `metrics/`). Invent the investor's persona (thesis, what they've seen, temperament) and note privately the holes you'll press on.
3. Announce entering character.

### Phases 1–2 — In character
1. Be skeptical but fair, and time-pressed. Open by letting them pitch; then probe. Care about **traction, market size, why-now, team, and the path to growth** — not the feature list.
2. **Realistic friction, no rescue:** vanity metrics get "so what — how many of those *retained / paid*?"; a hand-waved market gets "how do you actually reach them, and at what cost?"; "no competitors" gets "so how do customers solve this today?"; weak numbers get an uncomfortable follow-up. Concede genuine strengths plainly. "Interesting" is not a term sheet.
3. Stay in character; don't coach mid-pitch.

### Phase 3 — Debrief (out of character)
On `debrief`/`stop`, step out and assess against the rubric, then write artifacts.

## Debrief rubric

- **Traction first?** Did they lead with evidence the dog eats the dog food (signups that retain, revenue, growth rate) rather than the solution?
- **Command of the numbers?** CAC, LTV, retention/churn, growth rate, market size — did they know them and use them? Vanity vs. value metrics.
- **Riskiest assumption defended?** When pressed on the weak point from `risks.md`, did they have evidence or hand-wave?
- **Narrative & clarity** — tight problem→why-now→model→ask; a crisp high-level concept; a credible team story.
- **The ask** — a specific amount tied to specific milestones, not a vague "raising a round."
- **Composure under pressure** — did they get defensive, ramble, or concede too much? The 1–2 highest-leverage fixes.

## Artifacts

Write to `.lean/pitch/<YYYY-MM-DD>-<short-label>.md`: the pitch summary, the toughest questions asked, how they answered, and the debrief. Update `.lean/PROGRESS.md`. If the session surfaced a weak assumption, mirror it into `.lean/risks.md`.

## Related

- `measure-fit` — produces the traction numbers a pitch needs; the honest gate on whether to raise yet.
- `prioritize-risks` — the riskiest assumption the investor will hunt for.
- `lean-roles` — Devil's advocate for a non-fundraising stress-test of the model.
- `references/pitch-traction.md` — traction-first pitch structure and what investors probe.
