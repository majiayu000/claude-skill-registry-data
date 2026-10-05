---
name: studio-intro-writer
description: "Writes a presenter-delivered studio introduction that sets up a field report or pre-recorded package, giving viewers the context and stakes they need before the package begins."
status: stable
category: writing
subcategory: broadcast
version: 1.0
eval_score: 4.2
tags: [broadcast, presenter, studio, introduction, television, anchor, package]
---
# Studio Intro Writer

## What This Skill Does
Writes a presenter-delivered studio introduction that sets up a field report or pre-recorded package, giving viewers the context and stakes they need before the package begins.

## When To Use This Skill
- A reporter's package is ready to air and you need a studio introduction for the presenter or anchor to read before the package rolls
- The programme editor has asked for an intro that goes beyond restating the headline — one that frames why the story matters right now
- You are running a multi-story bulletin and need intros that vary in register (hard news, human interest, investigative) to avoid every introduction sounding identical
- You have a late-breaking development that changes the framing of an existing package and need the intro rewritten quickly

## What You Need To Provide
**Required:**
- A summary of the package contents: what the report covers, who appears in it, and its main finding or revelation
- The news peg — why this story is being broadcast today, not last week
- Target duration for the intro (typically 20–35 seconds for a standard package intro)

**Optional:**
- The tone of the package (hard news, human interest, investigative, explainer)
- The name and title of the presenter, if the script should be personalised to a specific voice
- Any facts, statistics, or named individuals the presenter must introduce before the package begins
- Whether the intro will be read to camera or over a graphic or still image

## How the Assistant Approaches This
1. Identifies the single most important piece of context a viewer needs before watching the package — not a summary of the package, but what the viewer must understand for the package to land with full force
2. Constructs a short, clear opening sentence that carries the news value, followed by one or two sentences of essential context, ending with a clean hand-off line that cues the package without stating the obvious
3. Checks that the intro does not duplicate the first ten seconds of the package — the presenter's words and the reporter's opening should not repeat the same information

## Output Format
- Plain prose, one paragraph
- Sentences are short and declarative; spoken register throughout — contractions where natural
- Ends with a hand-off line that names the reporter and signals the package is beginning (e.g. "Correspondent Name has this report." or "[Reporter] reports.")
- No rhetorical questions, no speculation, no "only time will tell"
- Word count stated at the end in brackets, e.g. [62 words / approx. 25 sec]

## Quality Criteria
- [ ] The opening sentence carries a clear, specific news value — not a vague scene-setter
- [ ] The intro provides context the package does not provide — it does not duplicate the reporter's opening narration
- [ ] The hand-off line is clean and unambiguous — a viewer knows the package is about to begin
- [ ] Spoken register throughout — no phrase that would be awkward to say aloud
- [ ] Duration matches the requested target (within two seconds at 2.5 words per second)

## Example

### Input
Package summary: A six-month investigation into water contamination at a large industrial estate. The reporter interviews three residents with unexplained health problems and a former factory worker who describes unsafe chemical disposal practices. The main finding is that local authorities received complaints eighteen months ago but took no action.

News peg: Authorities announced this morning they are opening a formal inquiry.

Target duration: 30 seconds.

Tone: Hard news, investigative.

### Output
Authorities have this morning opened a formal inquiry into contamination at the Harwick Industrial Estate — eighteen months after residents first raised concerns. Three families living near the site say they have suffered unexplained health problems since moving in. And a former factory worker has now told this programme that chemicals were routinely disposed of in ways that breached safety regulations. No one from the estate's management has agreed to be interviewed. Maria Fontes has been investigating. She reports.

[78 words / approx. 31 sec]

## Known Limitations
- This skill writes the presenter's words only — it cannot verify that the facts in the intro match the final cut of the package; a producer must check them against the edited version before broadcast
- If the package opens with the reporter delivering a strong, fact-laden stand-up, the intro may feel redundant at first draft; share the package's opening narration as optional input to help the assistant avoid duplication
- For very short news summaries (under 20 seconds), the intro may feel compressed; a brief (10–15 second) reader format may serve better — ask for a "reader" version if needed

## Related Skills
- [standup-script-writer](../standup-script-writer/SKILL.md)
- [teleprompter-script-writer](../teleprompter-script-writer/SKILL.md)
