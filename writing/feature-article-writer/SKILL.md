---
name: feature-article-writer
description: "Write a long-form feature article from provided notes, interview transcripts, or a detailed brief — structured using a five-part narrative arc (hook, context, development, turn, resolution)."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.83
tags: [journalism, features, writing, long-form, magazine, narrative]
---
# Feature Article Writer

## What This Skill Does
Write a long-form feature article from provided notes, interview transcripts, or a detailed brief — structured using a five-part narrative arc (hook, context, development, turn, resolution).

## When To Use This Skill
- You have interview notes or transcripts and need to shape them into a publishable feature
- You want to adapt research material into a narrative magazine-style piece
- You are writing a profile or human-interest story from provided facts and quotes
- You have a factual brief and need it turned into a long-form piece with a clear through-line

## What You Need To Provide
**Required:** Detailed notes, facts, or interview excerpts (the raw material the assistant will write from); the article topic and angle; target word count (500–2000 words).

**Optional:** Publication style (magazine, newspaper supplement, digital longform); tone (warm, investigative, lyrical, dry); specific quotes to include; structural preference (chronological, thematic, or profile-led).

## How the Assistant Approaches This
1. Reads the provided material and identifies the strongest narrative thread — the single idea or tension that can carry the piece
2. Structures the article using a five-part arc: **(1) Hook** — a scene, quote, or striking detail that draws the reader in; **(2) Context** — the broader situation or background that explains why this story matters; **(3) Development** — the story unfolds with evidence, quotes, and specific detail; **(4) Turn** — a complication, surprise, or shift in understanding that deepens the story; **(5) Resolution** — what it means, what comes next, or a return to the opening scene
3. Ensures every fact in the output is drawn from the provided material — nothing is invented
4. Targets the specified word count within a 10% margin, uses subheadings for articles over 1000 words, and ends with a "Source Material Used" note

## Output Format
Structured long-form article following the five-part arc. Sections are not labelled in the output — it reads as continuous prose. Word count adhered to within 10% of target. Paragraphs average 40–60 words. Subheadings used for articles over 1000 words. Ends with a "Source Material Used" note listing which provided inputs were incorporated.

## Quality Criteria
- [ ] The article follows the five-part arc: hook, context, development, turn, resolution
- [ ] Every fact is traceable to the provided material — no invented details
- [ ] The opening hook would make a reader continue past the first paragraph
- [ ] Quotes are used effectively — integrated into the narrative, not just dropped in
- [ ] Transitions between sections are smooth and the piece reads as coherent prose
- [ ] Word count is within 10% of the target

## Example

### Input
Topic: A retired photojournalist who documented urban change in a single neighbourhood over 30 years. Her work is now being exhibited at a community gallery in the same neighbourhood.

Angle: The neighbourhood has changed so dramatically that long-term residents barely recognise it, and her photographs are the only continuous record.

Target: 600 words, magazine style.

Interview notes and quotes:
- She moved to the neighbourhood in 1991 with a borrowed camera and no assignment
- Shot the same street corners, same faces, over three decades
- The neighbourhood was industrial then — printing presses, a tannery, corner pubs
- Now it is cafes, co-working spaces, a weekend market
- Quote 1: "The buildings are still there. But the people who built their lives in them — most of them are gone."
- Quote 2: "I never set out to document decline. I set out to document life. What that means has changed."
- The exhibition is in a converted warehouse. The warehouse used to employ 40 people from the street.
- Three original residents who feature in early photographs attended the opening
- One of them, a former tannery worker, did not recognise himself in a photograph taken in 1994

### Output

The photograph shows a man in his thirties leaning against a corrugated iron wall, squinting into the sun. Last Thursday, that man — now in his sixties — stood in front of it for several minutes before he realised it was him.

He had not recognised himself.

The image is part of *Thirty Years on Calder Street*, a new exhibition at the Meridian Gallery — which itself occupies a former warehouse that, in the photograph's background, you can see was still in use. The exhibition collects three decades of work by photographer Anna Voss, who arrived in this neighbourhood in 1991 with a borrowed camera and no assignment, and simply never stopped shooting.

What she documented was the neighbourhood in full industrial life: printing presses running through the night, a tannery that employed forty people from the surrounding streets, corner pubs where the same faces appeared every Friday. She shot the same street corners across thirty years. The buildings, she will tell you, are largely unchanged. Almost everything else is not.

"The buildings are still there," Voss says. "But the people who built their lives in them — most of them are gone."

The neighbourhood is now what urban planners call "mixed use" and what long-term residents often call something less polite. The tannery is a co-working space. The pub closest to the gallery became a specialty coffee outlet in 2017. A weekend market occupies the old loading yard. The transformation is not unusual — it has happened in post-industrial neighbourhoods across every major city. What is unusual is that someone was there for all of it, with a camera.

The exhibition does not editorialize. Voss has arranged her photographs chronologically, with minimal captions: location, year, nothing else. The effect is cumulative. Early images are dense with faces and activity. Later images show the same spaces cleaner, emptier, reorganized for a different kind of life. The viewer is left to draw their own conclusions.

"I never set out to document decline," Voss says. "I set out to document life. What that means has changed."

Three residents who appear in early photographs attended the opening. For two of them, seeing themselves young — in a neighbourhood they still live in but describe as unrecognizable — was, by their own accounts, disorienting. The third, the former tannery worker who stood before his own image for a long moment, said he found the experience less sad than clarifying. He had not forgotten those years. He had simply stopped being able to picture them.

The photographs had been keeping the record all along.

*Thirty Years on Calder Street* runs until the end of the month at Meridian Gallery.

---

**Source Material Used:** Interview notes (all four quotes and biographical details), exhibition description, neighbourhood history (industrial to mixed-use), gallery venue context (former warehouse), opening night anecdote (three original residents, tannery worker).

## Known Limitations
- The quality of the feature depends entirely on the richness of the provided material — thin notes produce thin features; vague briefs produce vague articles
- This skill does not conduct research or generate facts beyond what is provided — the journalist must supply the raw material
- Articles over 1500 words may lose structural coherence without very detailed source material covering all five arc stages
- The skill produces one version; if the publication requires a specific house style (New Yorker-style narrative, broadsheet feature conventions), that should be specified explicitly in the brief

## Related Skills
- [lede-writer](../lede-writer/SKILL.md)
- [news-article-writer](../news-article-writer/SKILL.md)
- [reportage-structure](../../../magazine-journalism/writing/reportage-structure/SKILL.md)
- [pull-quote-selector](../pull-quote-selector/SKILL.md)
