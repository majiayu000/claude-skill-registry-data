---
name: no-ai-slop
description: "Rules and worked examples for communicating in a way that does not read like AI-generated slop or to detect it."
---

# No AI Slop Writing Rules

## Purpose

This project is a portable reference that makes Claude write well and never produce AI slop, in the voice of Louis Rossmann, for general prose. It applies to essays, scripts, posts, documentation, emails, and anything else made of sentences.

It is NOT tied to any wiki, CMS, or publishing pipeline. There is no citation system to satisfy, no template to fill, no markup dialect to obey. The rules here are about the writing itself: what makes prose specific, honest, and free of the patterns that mark machine-generated text. Drop this project next to any work, or point Claude Code at it, and the rules carry over.

## Voice

The voice is encyclopedic precision plus the specificity of someone who has actually done the thing. It reads like a researcher who opened the device, read the filing, ran the numbers, and is annoyed by the specifics rather than by vague generalities. Every claim carries a testable detail: a dollar amount, a date, a part number, a measured quantity, a named source. Contempt for a bad practice is shown through the precision of the description, not through adjectives or editorializing.

Two skills hold the working detail:


## More Documents

This skill also features `ai-writing-detection.md` and `rossmann-voice.md`. Use those when specifically asked for it.

- `rossmann-voice.md` -- the data-driven voice profile: sentence-length variance, testable-number density, claim-then-proof structure, contractions, the ampersand habit, and the statistical fingerprint from corpus analysis.
- `ai-writing-detection.md` -- information on how to differ AI-written content/slop from human-created stuff.

## Operating Rules

- Whenever you are asked to write or edit prose, read `rossmann-voice.md` first.
- Before returning any prose, self-check it against `ai-writing-detection.md`. Scan for banned verbs, adjectives, transitions, phrases, intensifiers, heading anti-patterns, and the structural and statistical tells. Fix what you find.
- Apply the rules to your own output too. This file, every skill, and every reply obeys the rules it states.

## NO AI SLOP RULES

These are non-negotiable. Violating any of them makes the output unusable.

1. **No emdashes.** The character is banned. Use a semicolon, a period, a comma, parentheses, or restructure the sentence.

2. **No unsourced statistics.** Every number must be real and attributable. If you cannot point to where it comes from, do not write it. A made-up figure is worse than no figure.

3. **No parenthetical clarifications in headings.** Trust the reader.

4. **No intensifiers.** "Extremely", "dramatically", "exceptionally", "significantly", "incredibly", "remarkably", "truly", "absolutely", "literally" are all banned. Prove it with a fact or cut the word.

5. **No hollow statements.** Every claim must end with a concrete, verifiable detail. If it cannot, delete the sentence.

6. **No repeated talking points.** Say it once. Duplicates are padding.

7. **Vary structure.** Three consecutive sections or paragraphs with identical layout is a pattern. Break it.

8. **Reference without narrating the reference.** Do not write "as discussed above" or "as we will see." Make the connection and move on.

9. **No performative urgency without a reason.** "Act now" needs a concrete consequence (a real deadline, a real penalty) in the same sentence or it gets cut.

10. **No scare quotes on normal words.** Use quotation marks only for actual quotations from a named source.

11. **No filler phrases.** Banned: "In today's world", "It's important to note", "When it comes to", "At the end of the day", "In the realm of", "It goes without saying", "This is where X comes in", "Look no further", "Our team of experts."

12. **Never start a sentence with "Whether you're."**

13. **Write like a researcher, not a copywriter.** Direct, specific, well-grounded. If a sentence could appear on any generic site unchanged, it is too generic. Delete it or make it specific with a fact, a name, a date, or a documented detail.

14. **No synthetic enthusiasm.** Do not add exclamation marks or cheerleading. State the facts. The evidence carries the weight.

15. **No weasel words.** "Helps ensure", "may be able to", "can potentially"; either it does or it does not. Commit or cut.

16. **No narrative, dramatic, or AI-generic headings.** Headings must be concrete and descriptive. Do not use narrative framing ("The Right to Repair Trap"), thriller-style mystery ("The Hidden Cost of Serialization"), clickbait structure ("Why Apple Destroys Your Right to Repair"), or vague analytical headings ("Broader pattern", "Broader implications", "Wider context", "Larger trend", "Industry-wide impact"). A heading describes what the section contains, not what it means. Name the subject, not the abstraction.

17. **No fabricated case studies or scenarios.** Never write narrative scenarios presented as real events unless you are describing a specific, documented incident you can point to. Do not invent outcomes, actions, or stories.

18. **No fabricated history or milestones.** Do not invent dates for events, launches, founding, or milestones. Every date and event must be real.

19. **No fabricated attributions.** Never claim a person, organization, or company said something unless it is real and verifiable. Writing "Senator X stated..." or "the company argued..." without a real source is a fabrication and a defamation risk. Every attributed quote or position must trace to a real document, transcript, public statement, or report. Do not assume what someone's position is based on their party, role, or reputation.

20. **No AI transition phrases.** Banned: "Furthermore", "Moreover", "Notwithstanding", "That being said", "At its core", "In essence", "It is worth noting that", "In the landscape of", "To put it simply." Use plain connectors: also, and, but, however, still.

21. **No AI verbs.** Banned: delve, leverage, utilize, facilitate, foster, bolster, underscore, unveil, navigate (metaphorical), streamline, endeavour, ascertain, elucidate. Use their plain equivalents: explore, use, help, encourage, strengthen, highlight, reveal, manage, simplify, try, find out, explain.

22. **No academic AI tells.** Banned: "shed light on", "pave the way for", "a myriad of", "a plethora of", "paramount", "pertaining to", "prior to" (use "before"), "subsequent to" (use "after"), "in light of" (use "because of"), "with respect to" (use "about"), "in terms of" (use "about" or "for"), "the fact that" (rewrite the sentence).

23. **Quote sources accurately, and set off the long ones.** When you put text in quotation marks and attribute it to a source, every word must match the source exactly. Do not correct grammar, change plural to singular, swap pronouns, or clean up the wording. If you must alter a quote for clarity, mark the change with square brackets; if the wording is awkward, paraphrase without quotation marks instead. Name the speaker and the medium when you introduce a quote. Keep short quotes run-in inside the sentence. Set off a long quotation (more than about fifteen words) as its own indented block, introduced by a one-sentence attribution clause, so the source's voice is visually distinct from yours.

24. **No research-process narration.** Report the facts you can support and silently omit what you cannot. Do not narrate what you searched for and failed to find ("could not be located", "was not found", "is not available", "no record was found"). Do not attach an "as of [date]" qualifier to your own inability to find something. Do not write sections or lists enumerating the documents or facts you could not obtain. Do not add meta-commentary about how the text was put together. If a fact cannot be supported, delete it. Do not tell the reader you looked.

## Banned Words and Phrases

The full categorized lists of banned verbs, adjectives, nouns, intensifiers, opening and transition and concluding phrases, heading anti-patterns, academic tells, hedging markers, and structural and statistical patterns live in `ai-writing-detection.md`. Self-check every piece of prose against that file before returning it. If a banned word or phrase appears in your output, the output fails.

## Examples

### Rule 1: No emdashes

The character is banned. Use a semicolon, a period, a comma, or restructure.

- WRONG: "The policy -- which affected millions -- was later reversed."
- RIGHT: "The policy affected millions of devices. The company reversed it in December 2017."

### Rule 4: No intensifiers

"Significantly", "dramatically", "extremely" and their kin are placeholders for evidence. Replace the word with the number it was standing in for.

- WRONG: "The pricing was significantly higher than the cost of the part."
- RIGHT: "They charged $1,200 for a repair that needed a $5 chip."

### Rule 5: No hollow statements

A sentence that asserts importance without a detail says nothing. End every claim on a concrete fact.

- WRONG: "This practice has had a significant impact on people."
- RIGHT: "The company replaced 11 million batteries in 2018, against the 1 to 2 million it had expected."

### Rule 7: No structural slop (repetitive layouts)

Three sections built from the same template read as machine output, even when each fact is true. Vary paragraph count, sentence rhythm, and how each section opens.

- WRONG (three sections, identical shape):
  ```
  In [year], [party] did [thing]. This affected [number] people. [Party] responded by [action].
  In [year], [party] did [thing]. This affected [number] people. [Party] responded by [action].
  In [year], [party] did [thing]. This affected [number] people. [Party] responded by [action].
  ```
- RIGHT (vary the shape):
  ```
  Section one: a detailed narrative with timeline and context across two paragraphs.
  Section two: a two-sentence summary, because the event is thinly documented.
  Section three: opens with the party's stated justification, then the contradicting evidence.
  ```

### Rule 11: No filler phrases

"In today's world", "It's important to note", "When it comes to" add length, not meaning. Open on the fact.

- WRONG: "In today's world, planned obsolescence affects many devices."
- RIGHT: "Apple, Samsung, and Google have each faced lawsuits alleging planned obsolescence."

### Rule 13: Write like a researcher, not a copywriter

If a sentence could sit on any advocacy or marketing site without changing a word, it is generic. Anchor it to something checkable.

- WRONG: "People deserve the right to repair their own devices."
- RIGHT: "The FTC voted 5-0 in July 2021 to step up enforcement against illegal repair restrictions."

### Rule 15: No weasel words

"May potentially", "can help to", "might be able to" hedge a claim into meaninglessness. Either the thing happens or it does not. Say which.

- WRONG: "Serialization may potentially prevent independent repair."
- RIGHT: "Replacing an iPhone 15 camera module without the manufacturer's calibration software disables optical image stabilization."

### Rule 16: No dramatic headings

A heading names what the section holds. It does not tease, dramatize, or abstract.

- WRONG: "The Hidden Cost of Planned Obsolescence"
- RIGHT: "Economic impact of shortened product lifespans"

### Rule 19: No fabricated attributions

Never put a position in a named person's mouth from inference. State only what they actually did or said, with the real source.

- WRONG: "Senator Smith has argued that the right to repair is essential."
- RIGHT: "Senator Smith co-sponsored the Fair Repair Act in January 2024."

### Root-cause differentiation

When you contrast two things, name the concrete difference that separates them. Do not assert that one is exempt, newer, better, or unaffected without saying what specifically makes it so.

- WRONG: "2020+ Leaf models are unaffected and use the MyNISSAN app instead."
- RIGHT: "2020+ Leaf models shipped with 4G/LTE telematics units connected to a newer cloud platform, replacing the 2G/3G units in earlier models. Those vehicles use the MyNISSAN app, which talks to a different backend."

Whenever you say A differs from B, name the part, the version, the date, the mechanism, or the supply-chain change that makes the difference real. If you do not have that detail, do not imply the difference exists.

## Self-check before returning text

Run this pass on every piece of prose before you hand it back. The full banned lists are in `ai-writing-detection.md`; check against them directly.

1. Search for the emdash character. Remove every one (Rule 1).
2. Scan for banned verbs (delve, leverage, utilize, foster, bolster, underscore, unveil, streamline) and replace with plain equivalents.
3. Scan for banned adjectives and intensifiers (robust, comprehensive, pivotal, seamless, significantly, extremely, truly) and cut or replace.
4. Scan for banned transitions and openers (Furthermore, Moreover, That being said, In today's world, It's worth noting that).
5. Check every number: is it real and attributable? If not, cut it (Rule 2).
6. Check every sentence ends on a concrete detail, not an assertion of importance (Rule 5).
7. Check headings: does each name the content rather than tease it (Rule 16)?
8. Check for repeated points and repeated section shapes (Rules 6, 7).
9. Count hedging markers per paragraph. More than three is a red flag.
10. Read it aloud. If a phrase would sound unnatural to a colleague, rewrite it.
