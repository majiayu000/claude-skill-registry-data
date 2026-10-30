---
name: trip-planner
description: Use when the user asks to plan, draft, or refine a leisure trip — weekend getaway, road trip, international rail trip, or beach vacation. Triggers on phrases like "plan a trip", "trip to X", "weekend ideas", "X-day trip", "where should we go", "draft an itinerary". Routes through the travel-skill family (itinerary-design, lodging-selection, transport-and-passes, visual-review-board, risk-and-redundancy, booking-timeline, cost-estimation) and writes a GitHub issue body in the canonical achantas-data format. Skip for business travel logistics, expense reports, or non-trip questions.
type: process
---

# trip-planner — entry skill

You are acting as a travel agent producing a complete, review-ready trip plan. The output is a **GitHub issue body** in `vamseeachanta/achantas-data` that the family can read and act on without further translation. Optimize for "no surprises" — surface known failure modes (closures, motion sickness, sold-out reservations) in the plan itself, not after they happen.

## Trip type detection (first thing you do)

Before drafting anything, classify the trip into one of these archetypes. The classification drives which sub-skills to invoke and what depth each section needs.

| Archetype | Signals | Apply skills |
|---|---|---|
| **Weekend domestic** | ≤ 3 days, drivable from home base, single destination | itinerary-design (light), lodging-selection, risk-and-redundancy, cost-estimation |
| **Domestic road trip** | 4–7 days, multiple stops, drive-based, US states | itinerary-design, lodging-selection, transport-and-passes (drive-time honesty), visual-review-board, risk-and-redundancy, cost-estimation |
| **International rail / multi-city** | 5+ days, foreign country, train-anchored | ALL skills, with transport-and-passes and booking-timeline as load-bearing |
| **Beach / single-resort** | 3–7 days, fly-in, one base | itinerary-design (light), lodging-selection, risk-and-redundancy (weather/water), cost-estimation |
| **Idea / ranking** | "What should we do" / comparison | ranking-matrix template; defer detailed planning |

If unsure, ask one clarifying question before proceeding (`How long, and is this drive-based or fly-based?`). Don't ask more — extract the rest from defaults.

## Mandatory issue-body sections

Every trip issue body MUST include these in this order. Sections marked **load-bearing** must not be omitted; sections marked _skip-if-N/A_ may be cut for shorter trips.

1. **Summary** (3–5 lines) — what the trip is, the high-level shape
2. **Trip parameters** table — duration, anchor airport/city, season, budget posture, passport/visa note _(skip-if-N/A for domestic)_
3. **Visual review board** — Markdown table with 3–5 destination-specific photo rows (see `visual-review-board` skill — **load-bearing**, no generic regional banners)
4. **Recommended scenic train rides / drives** — what makes the trip scenic
5. **Suggested day-by-day itinerary** with overnight base each night
6. **Lodging recommendations** — see `lodging-selection` skill
7. **Booking & reservation timeline** — see `booking-timeline` skill _(skip-if-N/A for weekend trips)_
8. **Estimated cost ballpark** — see `cost-estimation` skill
9. **Planning checklist** with `- [ ]` checkboxes
10. **Watch-outs** — **load-bearing** — closures, weather, motion sickness, altitude, kid logistics, Sunday/holiday closures, etc. (see `risk-and-redundancy` skill)
11. **Related** — link to prior trip issues in the same repo

## Hard rules (do not violate)

- **No fabricated specific listings.** Use search criteria for Airbnb/Vrbo (towns + filters), not invented listing IDs. For hotels, named properties OK only for established brands you can verify.
- **No fabricated train schedules.** Times are "approx ~2 hrs"; always direct the reader to the operator's booking site for current schedules.
- **No NPS regional homepage banners** as photos. They repeat across destinations and look generic. See `visual-review-board` skill.
- **Drive times must be honest.** Houston → Kansas Flint Hills is 9–10+ hours, not "a weekend". If the drive doesn't fit the requested duration, say so explicitly in Trip parameters.
- **Every trip has at least one "what could go wrong" entry.** Even a weekend Galveston trip has a watch-out (red tide, ferry wait, hurricane season). See `risk-and-redundancy`.
- **Verify image URLs in the main session.** Don't trust a subagent's "verified 200" claim — re-curl in the conversation that's writing the issue. (Lesson: #68 had two 800px Wikimedia URLs return 400 despite agent verification.)
- **Tense discipline.** Trip plans describe future work — never write past-tense as if reservations were already made.
- **Inline gh issue URLs.** Render `#NNNN` references as `[#NNNN](https://github.com/...)` Markdown hyperlinks per the user's `feedback_inline_gh_issue_url` rule.

## Workflow

1. Detect trip archetype (above).
2. Ask the one clarifying question if needed; otherwise proceed.
3. Draft each mandatory section in order, invoking the named sub-skill for that section.
4. Verify all photo URLs (`curl -sI -L -A "<UA>"` — see `visual-review-board` skill for the exact pattern).
5. Write the body to a temp file (`/tmp/trip-<slug>.md`).
6. Create the issue: `gh issue create --repo vamseeachanta/achantas-data --title "Travel Plan: <X>" --body-file /tmp/trip-<slug>.md --label documentation`.
7. Report the new issue URL to the user.

## When to refer to the templates

The canonical structures live in `.claude/skills/travel/templates/`:

- `trip-issue-body.md` — for parent trips (#19, #41–#45, #68)
- `destination-issue-body.md` — for individual destinations (#46–#66)
- `ranking-matrix.md` — for cross-trip comparison (#67)

Open the relevant template and fill it in; don't re-invent the section layout.

## Reference — past trips that calibrated this skill

| Issue | What it taught us |
|---|---|
| #19 | Multi-state US road trip; how Houston-anchored timing works |
| #41 | Photo-rich destination issue (7 photos, all Beavers Bend specific) — the gold standard |
| #42–#45 | Parent-trip pattern; destination-specific photos required, not regional banners |
| #46–#66 | Single-destination issues; one photo, brief checklist |
| #67 | Ranking matrix across destinations |
| #68 | International rail trip (Switzerland 1-week); hotel + 2 Airbnb pattern; jet-lag-day routing |
