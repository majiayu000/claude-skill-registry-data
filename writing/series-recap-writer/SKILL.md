---
name: series-recap-writer
description: "Writes a concise \"previously on\" or \"catch-up\" block that brings new readers up to speed on a running story — summarising key developments in chronological order and framing what is at stake as the story continues."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [recap, running-story, series-journalism, explainer, catch-up, ongoing-coverage]
---
# Series Recap Writer

## What This Skill Does
Writes a concise "previously on" or "catch-up" block that brings new readers up to speed on a running story — summarising key developments in chronological order and framing what is at stake as the story continues.

## When To Use This Skill
- You are publishing a new instalment in an ongoing investigative series and need a brief recap for readers arriving mid-series
- A story has been running for weeks or months and your next article needs to orient readers who missed earlier coverage
- You are writing the introduction to a long-read that continues from previous reporting and want a crisp summary rather than a full recap section
- You need a standalone "story so far" page or newsletter section that consolidates a thread of coverage

## What You Need To Provide
**Required:**
- The name or topic of the running story
- A chronological list of the key developments so far — bullet points are fine; include approximate dates if relevant
- What the current article or instalment covers (so the recap can point clearly toward it)

**Optional:**
- Target word count for the recap block (default: 150–250 words)
- The tone of your coverage (e.g., investigative, news-feature, data journalism)
- Whether the recap should appear as inline prose, a separate labelled block ("The Story So Far"), or a bullet-point timeline
- Any developments that are contested or under dispute and should be framed carefully

## How the Assistant Approaches This
1. Identifies the through-line of the story — the central question or conflict that links all the developments — so the recap reads as a coherent narrative rather than a list of events
2. Selects the most essential developments (not every event, only those a reader genuinely needs to follow the new instalment)
3. Writes in chronological order with clear, unambiguous transitions that mark the passage of time without becoming a timeline of dates
4. Ends the recap block on the development that directly sets up the new instalment, so the transition from recap to new reporting feels earned, not arbitrary
5. Adjusts framing for any disputed facts: reported claims are attributed, confirmed facts are stated directly

## Output Format
Prose block of 150–250 words (or your specified length). Written in the same tense and register as the surrounding article. Clear, short sentences — this is not the place for complex subordinate clauses. Ends with a bridging sentence that leads naturally into the new reporting. If a labelled block format is requested, the block is headed "The Story So Far" or similar, set off visually from the surrounding text.

## Quality Criteria
- [ ] A reader with no prior knowledge of the story can follow the new instalment after reading the recap
- [ ] No development is included that is not necessary to understand the current instalment
- [ ] Chronological progression is clear without requiring a bullet-point list of dates
- [ ] Disputed or unconfirmed claims are attributed rather than stated as fact
- [ ] The final sentence of the recap connects directly to what the new article will cover

## Example

### Input
**Story name:** The council housing register investigation

**Key developments so far:**
- January: A source contacts the newsroom claiming that applicants on the council housing register are being passed over in favour of those with political connections
- February: Reporters obtain the full register under freedom-of-information law; analysis shows 47 applicants have been waiting more than eight years
- March: Three families agree to be interviewed on record; all describe being told their applications were "under review" despite meeting all criteria for priority status
- April: The council issues a statement saying the register is managed "in full compliance with statutory requirements"; refuses a further interview
- May (current instalment): Leaked internal emails show senior housing officials discussed "managing expectations" of specific applicants; reporters put the emails to the council for comment

**Tone:** Investigative, serious

**Format:** Labelled block ("The Story So Far"), approx. 200 words

### Output

---

**The Story So Far**

This investigation began in January when a source inside the council's housing department told reporters that applicants on the social housing register were being passed over for reasons that had nothing to do with their assessed need. The claim prompted a freedom-of-information request for the full register. The data, obtained in February, showed 47 households had been waiting more than eight years for a property — in several cases, significantly longer than the council's own guidelines suggested they should have waited.

In March, three families agreed to speak on record. Each described the same pattern: repeated assurances that their application was progressing, followed by no action. All three met the council's stated criteria for priority status. When approached for comment, the council said its register was managed "in full compliance with statutory requirements" and declined a formal interview.

This week, leaked internal emails obtained by this newsroom show that senior housing officials discussed specific applicants in terms that go further than the council's public position suggests. We put those emails to the council on Monday. Their response is below.

---

## Known Limitations
- The recap can only be as accurate as the developments you provide; the assistant does not have access to your previous articles and cannot fill gaps in your chronology
- For stories involving legal proceedings, the recap's framing of contested facts depends on clear guidance in your input — flag anything sub judice or disputed before running
- Very long-running stories (three or more years of developments) may require you to pre-select which developments to include rather than listing everything; the assistant will make choices, but editorial judgement on what is essential to the current instalment rests with you

## Related Skills
- [related-articles-teaser-writer](../related-articles-teaser-writer/SKILL.md)
- [reportage-structure](../../../magazine-journalism/writing/reportage-structure/SKILL.md)
- [document-analysis-brief](../../../magazine-journalism/investigation/document-analysis-summary/SKILL.md)
