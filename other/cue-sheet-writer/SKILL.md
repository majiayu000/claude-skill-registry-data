---
name: cue-sheet-writer
description: "Produces a formatted broadcast cue sheet — including item numbers, in-cues, out-cues, durations, and technical instructions — from a programme rundown or description of planned content."
status: stable
category: writing
subcategory: broadcast
version: 1.0
eval_score: 4.2
tags: [cue sheet, broadcast, production, rundown, timing, television, radio]
---
# Cue Sheet Writer

## What This Skill Does
Produces a formatted broadcast cue sheet — including item numbers, in-cues, out-cues, durations, and technical instructions — from a programme rundown or description of planned content.

## When To Use This Skill
- A producer needs a print-ready cue sheet for a live or as-live broadcast programme — news, current affairs, magazine shows, documentary screenings
- You are preparing a floor or gallery team and need cues written to broadcast standard before the production meeting
- You have a rundown or rough order of content and need it formatted into a proper cue sheet that a presenter, director, and technical operator can all work from simultaneously
- You are writing cue sheets for a radio programme — including music, interview clips, and live links

## What You Need To Provide
**Required:**
- A list of programme items in order, with a brief description of each (e.g., "Interview with housing minister, approx. 4 minutes")
- Total programme duration (e.g., 28 minutes for a 30-minute slot, accounting for titles and credits)
- Programme type (television news magazine, documentary, live radio programme, etc.)

**Optional:**
- Presenter name(s), if cues are to be addressed directly
- Whether music beds, idents, or stings are needed between items
- Technical format preferences — whether VT, OB (outside broadcast), or studio segments need distinct labelling
- Any fixed-time or hard-out constraints (e.g., "news at the top of the hour — hard out at 28:00")
- Language of broadcast

## How the Assistant Approaches This
1. Reviews the full list of items and assigns each a sequential item number, estimates durations based on the descriptions provided (or uses supplied durations), and checks that all items fit within the total running time
2. Writes an in-cue (the first words of the item or the presenter's introduction line) and an out-cue (the last words spoken or the end of a music or VT item) for each entry, so the director and technical team know exactly when each element starts and ends
3. Formats the complete sheet as a structured table — item number, item type, title/description, in-cue, out-cue, duration, cumulative running time, and any technical notes — and flags any timing problems or gaps that would cause a broadcast overrun

## Output Format
A structured table with the following columns: **No.** | **Type** | **Item** | **In-Cue** | **Out-Cue** | **Dur** | **Running Total** | **Notes**. Each row is a discrete programme element. Technical notes (e.g., VT roll, mic open, music fade) appear in the Notes column. A summary line at the bottom shows total programme duration versus allocated slot. Formatting is clean and printable — no decorative elements, no colour coding that would be lost in greyscale print.

## Quality Criteria
- [ ] All items are numbered sequentially with no gaps
- [ ] In-cues and out-cues are specific — not "begins here" but the actual first and last words or a precise technical instruction
- [ ] Individual durations add up correctly to the running total, and the running total does not exceed the allocated slot
- [ ] Any hard-out constraints are clearly marked and obeyed
- [ ] Technical item types (VT, SYNC, LIVE, OB, MUSIC, STING) are consistent throughout and match broadcast convention
- [ ] The sheet can be handed to a director or studio manager without verbal explanation

## Example

### Input
Programme: Weekly 28-minute television current affairs magazine, going to air live
Items:
1. Titles and opening billboard
2. Presenter introduction and programme billboard — approx. 45 seconds
3. VT package — housing shortage report — approx. 6 minutes
4. Live studio interview with housing policy researcher — approx. 5 minutes
5. VT package — profile of a community self-build project — approx. 4 minutes 30 seconds
6. Presenter toss to weather presenter — 15 seconds
7. Weather — OB from rooftop location — approx. 2 minutes
8. Presenter introduction to final item — 20 seconds
9. VT package — opinion piece, rents and generational divide — approx. 4 minutes
10. Presenter close and goodbye — 30 seconds
11. End titles and credit roll
Hard out: 28:00
Presenter: Francesca Ndiaye

### Output

**PROGRAMME: Housing in Focus — Episode 14**
**TX DATE: [Producer to insert] | SLOT: 28:00 | HARD OUT: 28:00**
**PRESENTER: Francesca Ndiaye**

| No. | Type | Item | In-Cue | Out-Cue | Dur | Running Total | Notes |
|-----|------|------|---------|---------|-----|---------------|-------|
| 1 | TITLES | Opening titles and billboard | [Sting — VT roll on TX] | [Music out — cut to studio] | 0:30 | 0:30 | Director cue: VT 1 |
| 2 | LIVE | Presenter opening billboard | "Tonight on Housing in Focus —" | "— let's start." | 0:45 | 1:15 | Francesca on set, cam 2 |
| 3 | VT | Housing shortage report | [VT roll — black 3 secs] | "— and that number keeps rising." | 6:00 | 7:15 | Director cue: VT 2. Outcue confirmed with editor |
| 4 | LIVE | Studio interview — housing policy researcher | "Joining me now is —" | "— thank you very much." | 5:00 | 12:15 | Guest mic open. Cam 1/cam 3. Warning at 4:30 |
| 5 | VT | Community self-build profile | [VT roll — black 3 secs] | "— they call it home." | 4:30 | 16:45 | Director cue: VT 3 |
| 6 | LIVE | Presenter toss to weather | "Now let's check in with the weather —" | "— over to you." | 0:15 | 17:00 | Francesca to cam 2 |
| 7 | OB | Weather — rooftop location | [OB open — director cue OB TX] | "Back to the studio." | 2:00 | 19:00 | OB unit on standby from 18:30 |
| 8 | LIVE | Presenter intro — final package | "Finally tonight —" | "— take a look." | 0:20 | 19:20 | Francesca to cam 1 |
| 9 | VT | Opinion piece — rents and generational divide | [VT roll — black 3 secs] | "— and they are not wrong." | 4:00 | 23:20 | Director cue: VT 4 |
| 10 | LIVE | Presenter close | "That's Housing in Focus for this week." | "Good night." | 0:30 | 23:50 | Francesca to cam 2 |
| 11 | TITLES | End titles and credit roll | [Music in — VT roll on cue] | [Music out — TX END] | 0:30 | 24:20 | Director cue: VT 5 |

**TOTAL PROGRAMME: 24:20 | ALLOCATED SLOT: 28:00 | MARGIN: 3:40**

> **PRODUCER NOTE:** Programme runs 3 minutes 40 seconds short of slot. Options: extend studio interview (item 4) by up to 3 minutes, extend presenter billboard (item 2), or add a second studio interview. Confirm with exec before TX.

---

## Known Limitations
- The assistant estimates item durations from descriptions; actual timings must be confirmed against timed scripts, edited VT packages, and timed rehearsals before air — this skill does not replace a timed read-through
- In-cues and out-cues for VT packages are marked as placeholders unless the user provides the actual first and last words of each package; producers must insert confirmed outcues from edited material
- The skill does not generate a full rundown system export (e.g., ENPS, iNews, Dalet format) — it produces a print-formatted cue sheet only
- For programmes with highly complex technical requirements (multi-camera drama, live sport, OB-heavy productions), the cue sheet produced here covers editorial flow but does not substitute for a full technical running order prepared by a technical producer

## Related Skills
- [voice-over-writer](../../../radio-audio/scripting/documentary-narration-writer/SKILL.md)
- [cold-open-writer](../cold-open-writer/SKILL.md)
