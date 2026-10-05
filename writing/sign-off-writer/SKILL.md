---
name: sign-off-writer
description: "Writes a polished, broadcast-ready closing script for a presenter, reporter, or podcast host — matched to the show's tone and the specific episode content — that ends the programme with authority and purpose."
status: stable
category: writing
subcategory: broadcast
version: 1.0
eval_score: 4.2
tags: [broadcast, sign-off, closing-script, presenter, reporter, podcast, outro]
---
# Sign-Off Writer

## What This Skill Does
Writes a polished, broadcast-ready closing script for a presenter, reporter, or podcast host — matched to the show's tone and the specific episode content — that ends the programme with authority and purpose.

## When To Use This Skill
- You need a closing line or full sign-off passage for a broadcast report, documentary segment, or podcast episode
- Your regular sign-off formula has become stale and you want alternatives that still fit your show's identity
- You are launching a new programme and want to establish a sign-off style from the first episode
- You are producing a special edition, season finale, or commemorative episode that requires a closing moment with more weight than the standard outro

## What You Need To Provide
**Required:**
- Format (broadcast news report, documentary, podcast episode, live radio, video essay)
- Reporter or host name and role (e.g., "Maria Okonkwo, economics correspondent" or "solo podcast host")
- Topic or title of the episode or report
- Tone of the show (e.g., authoritative news, conversational, wry and analytical, serious documentary, upbeat lifestyle)

**Optional:**
- Location if the reporter is filing from a specific place (for traditional broadcast sign-offs)
- A one-sentence summary of the episode's conclusion or emotional note to land on
- Any standard elements the sign-off must include (programme name, network name, call to action, subscribe reminder)
- Number of sign-off variants required (default: three options at different tones/lengths)

## How the Assistant Approaches This
1. Identifies the register and conventions of the format — a broadcast news report sign-off, a podcast outro, and a documentary closing statement each follow different structural expectations
2. Establishes the emotional or intellectual landing point: what should the audience feel or think in the moment after the sign-off plays?
3. Writes the sign-off to carry that landing point cleanly — using rhythm, pacing, and precision rather than decoration
4. Produces multiple variants (short, medium, and extended; or different tones) so the producer can choose or adapt

## Output Format
- Three sign-off variants unless the user specifies otherwise
- Each variant labelled by length or tone (e.g., `[Short — traditional broadcast]`, `[Extended — documentary closing]`, `[Conversational — podcast outro]`)
- Each variant presented as spoken text only — no stage directions, no production notes unless specifically requested
- Broadcast news variants: typically one to four sentences, ending with name, role, programme, and location
- Podcast and documentary variants: one to two short paragraphs, closing with a purposeful final line
- No filler phrases: "join us next time," "don't miss out," "until then" only if the user has specifically asked for them

## Quality Criteria
- [ ] Each variant ends on a strong final line — not trailing, not decorative, but purposeful
- [ ] The tone of each variant is consistent with the show format and register described
- [ ] Broadcast variants include all required identity elements (name, programme, location) integrated naturally, not appended mechanically
- [ ] Podcast and documentary variants have a clear emotional or intellectual landing point — the audience knows what they are meant to take away
- [ ] All variants read cleanly aloud — no tongue-twisting constructions, no sentences that require a breath mid-clause
- [ ] No variant exceeds the appropriate length for its format

## Example

### Input
**Format:** Podcast episode
**Host:** Solo host, goes by first name only ("Reuben")
**Show:** The Long View — a history podcast for general audiences that finds contemporary relevance in overlooked historical events
**Episode topic:** The 1930s drought that forced the closure of the London docks and what it tells us about infrastructure fragility
**Episode conclusion:** The episode argued that large infrastructure systems are not built to be resilient — they are built to appear resilient, and the difference only becomes visible when they fail
**Show tone:** Thoughtful, unhurried, slightly literary — not academic
**Standard elements:** End with a prompt to subscribe and a line about the next episode (topic: the 1953 North Sea flood and the politics of coastal defences)
**Variants needed:** Three

### Output

---

**[Option 1 — Reflective closing, medium length]**

The docks did not simply close because the water table dropped. They closed because no one had designed them for the possibility that it might. Resilience, it turns out, is mostly a story infrastructure tells about itself — right up until it can't.

Thank you for listening to The Long View. If you found this episode worth an hour of your time, please subscribe wherever you get your podcasts. Next time, we're moving to 1953 and the North Sea flood — and the political arguments about who gets to decide which coastlines are worth defending. I'm Reuben. See you then.

---

**[Option 2 — Shorter, sharper ending]**

The lesson from the docks is a simple one: the difference between infrastructure that works and infrastructure that fails is mostly invisible until it matters. And by then, it is too late to be surprised.

Subscribe to The Long View if you haven't already — and join me next time for the 1953 North Sea flood, and the uncomfortable question of which land is worth protecting. I'm Reuben.

---

**[Option 3 — More literary, dwelling on the episode's central image]**

There is something worth sitting with in the image of a working dock going dry — not dramatically, not all at once, but slowly, over weeks, as the water retreats and the boats settle at odd angles in the mud. Infrastructure does not announce its vulnerability. It just keeps working, and working, and then one day it doesn't, and everyone is surprised who probably should not have been.

That's The Long View for this week. Subscribe if you'd like more of this — and next time, we're going to the North Sea in the winter of 1953, when the water came the other way. I'm Reuben. Thanks for listening.

---

## Known Limitations
- A sign-off depends heavily on the episode's concluding tone — if the episode itself does not have a clear landing point, the sign-off will feel disconnected; the user may need to decide the emotional note first and provide it explicitly
- For live broadcast, ad-lib sign-offs must be rehearsed even when scripted — a memorised closing sounds different from a read one, and this skill cannot account for live broadcast conditions
- Traditional broadcast news sign-offs have format-specific conventions (some organisations require a specific ordering of name, programme, and location) that vary by outlet; the user should check variants against house style before use
- The skill cannot write a sign-off that references specific future episode content unless that content is provided by the user

## Related Skills
- [podcast-episode-script-writer](../podcast-episode-script-writer/SKILL.md)
- [intro-outro-writer](../../../podcast/scripting/intro-outro-writer/SKILL.md)
- [voice-over-writer](../../../radio-audio/scripting/documentary-narration-writer/SKILL.md)
