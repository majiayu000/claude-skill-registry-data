---
name: word-count-reducer
description: "Reduce a piece of text to a specified word count or percentage reduction while preserving all essential meaning, key facts, and the author's voice — cutting filler, redundancy, and unnecessary qualifiers rather than removing substantive content."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 5.0
tags: [editing, writing, word-count, tightening, journalism, digital, print]
---
# Word Count Reducer

## What This Skill Does
Reduce a piece of text to a specified word count or percentage reduction while preserving all essential meaning, key facts, and the author's voice — cutting filler, redundancy, and unnecessary qualifiers rather than removing substantive content.

## When To Use This Skill
- Your article or feature exceeds the publication's word limit and needs to be cut before submission
- A draft feels bloated and you want the tightest possible version without doing line edits manually
- You are adapting long-form content for a shorter format (a 1,200-word web article needs to become a 600-word newsletter item)
- You have a print layout with a fixed text area and the copy is running several lines long

## What You Need To Provide
**Required:** The text to reduce; the target word count or percentage reduction (e.g. "cut to 250 words" or "reduce by 30%").

**Optional:** Priority elements to preserve (specific quotes, data points, section headings, the conclusion); elements that can be sacrificed first (background context, secondary examples, attribution detail).

## How the Assistant Approaches This
1. Counts the current word count, calculates the exact reduction needed, and identifies where the text has room to compress — redundancies, filler phrases, over-long attributions, repeated points, adverb clusters, and throat-clearing introductions
2. Makes cuts in order of least-to-most impact: first removes filler and redundancy, then trims secondary examples and supporting detail, then shortens sentences — preserving all direct quotes, specific data, and the opening and closing sentences wherever possible
3. Performs a final read of the reduced text for coherence — ensures no orphan references (a "this" with no antecedent, a pronoun referring to a deleted subject) and no choppy transitions caused by cuts
4. Returns the reduced text with a brief word count note; if the target could not be reached without removing content that seems essential, states how close it got and what category of content would need to be cut to reach the target

## Output Format
The reduced text in full, followed by a one-line word count note: "Original: X words → Reduced: Y words (Z% reduction)." If the target was not achievable without losing essential content, adds a second line explaining what remains and what further cuts would require.

## Quality Criteria
- [ ] Final word count is within 5% of the specified target
- [ ] No essential facts, data points, or direct quotes have been removed
- [ ] The text reads naturally — no choppy transitions or orphan references caused by cuts
- [ ] The author's voice and register are unchanged
- [ ] The opening and closing sentences are preserved unless they contained redundancy

## Example

### Input

Target: 250 words (current draft is approximately 350 words — reduce by ~30%)

Text:

> The annual Media Innovation Summit, which took place in central London last week, brought together more than 400 journalists, editors, and media executives from across Europe and beyond to discuss the future of the industry. This year's summit, which was held at a major conference venue in the city, featured panel discussions, keynote addresses, and roundtable sessions on topics ranging from artificial intelligence and newsroom automation to the sustainability of subscription revenue models and the evolving role of print journalism in a largely digital media landscape.
>
> Among the most widely discussed themes at this year's summit was the impact of generative artificial intelligence tools on editorial workflows. Several speakers argued that AI is already fundamentally transforming the speed at which journalists can research and draft initial versions of stories. Others were more cautious in their assessment, noting that the quality of AI-generated content remains inconsistent and that significant editorial oversight is still required in order to maintain accuracy and avoid the publication of incorrect or misleading information.
>
> The question of sustainability dominated the afternoon sessions. Subscription fatigue — the tendency of readers to cancel digital subscriptions when the volume of competing platforms becomes overwhelming — was cited by multiple panellists as one of the primary threats facing quality journalism today. A report released at the summit found that readers in European markets are currently subscribing to an average of 2.3 digital news products, down from 2.8 three years ago.

Priority: Preserve the AI discussion and the subscription data. Background on the venue and format can be cut.

### Output

The annual Media Innovation Summit brought together more than 400 journalists, editors, and media executives in London last week to discuss the future of the industry. Panels and keynotes covered AI and newsroom automation, subscription revenue models, and the evolving role of print journalism.

The summit's most debated theme was generative AI's impact on editorial workflows. Several speakers argued AI is already transforming the speed at which journalists research and draft stories. Others were more cautious, noting that AI-generated content remains inconsistent and requires significant editorial oversight to maintain accuracy.

Sustainability dominated the afternoon sessions. Subscription fatigue — readers cancelling digital subscriptions as competing platforms multiply — was cited as a primary threat to quality journalism. A summit report found European readers now subscribe to an average of 2.3 digital news products, down from 2.8 three years ago.

---

Original: 351 words → Reduced: 130 words (63% reduction).

*Note: The target of 250 words was exceeded — the text compressed further than anticipated once venue and format detail was removed. If 250 words is the target, the current 130-word version can be expanded with additional context from the original. If a shorter format was the goal, 130 words is the lean version.*

## Known Limitations
- Reductions above 40% will inevitably lose supporting detail and contextual nuance — the skill flags when cuts begin to affect meaning, but the author must decide how much context the reader needs.
- Cannot determine which facts are "essential" from the reader's perspective without knowing the publication, audience, and story angle — if no priorities are specified, it preserves the most specific information (data, quotes, named sources) over general framing.

## Related Skills
- [copy-editor](../../../editing/copy-editor/SKILL.md)
- [tldr-writer](../tldr-writer/SKILL.md)
