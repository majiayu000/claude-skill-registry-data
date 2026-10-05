---
name: subject-line-writer
description: "Generates five distinct subject line options for a newsletter edition, each using a different psychological approach proven to improve open rates, matched to the publication's voice and the edition's content."
status: stable
category: newsletter
subcategory: writing
version: 1.0
eval_score: 4.5
tags: [newsletter, writing, subject-line, open-rate, email-marketing]
---
# Subject Line Writer

## What This Skill Does
Generates five distinct subject line options for a newsletter edition, each using a different psychological approach proven to improve open rates, matched to the publication's voice and the edition's content.

## When To Use This Skill
- You have finished writing or briefing a newsletter edition and need to choose a subject line before sending
- Your open rates have plateaued and you want to test different subject line strategies
- You are launching a new newsletter and need to establish what subject line style fits your voice
- You are A/B testing subject lines and need a strong shortlist of candidates

## What You Need To Provide
**Required:** A summary of the newsletter edition's main topic or story (2–5 sentences); the newsletter's name and general tone (e.g. "analytical and dry", "warm and conversational", "urgent and activist")
**Optional:** Your typical subscriber profile; any subject lines that have performed well or badly for you before; the sending day and time; whether you allow emoji in subject lines

## How the Assistant Approaches This
1. Identifies the single most compelling element of the edition — the hook, the reveal, the tension, or the utility — that would make a reader stop scrolling
2. Applies five distinct psychological frameworks: curiosity gap, direct value statement, personal relevance, urgency or scarcity, and contrarian or counterintuitive angle
3. Calibrates each option to the newsletter's stated tone, keeping length under 50 characters where possible and avoiding spam-trigger language (all-caps, excessive punctuation, misleading claims)
4. Adds a one-line note after each option explaining the psychological principle it uses, so you can make an informed choice or test intelligently

## Output Format
Five numbered subject line options, each on its own line, followed by a parenthetical note explaining the technique. Total length: under 200 words. No preamble, no ranking. A single optional preview text suggestion (the 80–100 character line that appears after the subject in most clients) is appended at the end.

## Quality Criteria
- [ ] Each of the five options uses a genuinely different psychological approach (not five variations of the same hook)
- [ ] Every option fits the newsletter's stated tone — a dry analytical publication does not get emoji-heavy casual lines
- [ ] No option contains spam-trigger language or makes a claim not supported by the edition content
- [ ] All options are under 60 characters (ideally under 50) unless the publication's style explicitly favors longer lines
- [ ] The technique note is accurate and not generic ("curiosity gap" must actually create a gap, not just name the tactic)

## Example

### Input
Newsletter name: *The Friction Report*
Tone: Sharp, data-driven, slightly sardonic. Audience is product managers and UX professionals.
Edition summary: This week's main story looks at new research showing that adding a progress bar to checkout flows actually increases cart abandonment in one specific product category — subscription boxes — by 14%. The finding contradicts years of UX conventional wisdom. We also cover three other studies from the same research group.
Emoji: No.
Previous high-performer: "The UX rule everyone is breaking (correctly)"

### Output
1. The progress bar that kills conversions
   *(Direct value: names the specific element and the outcome — no ambiguity about what the reader gets)*

2. Everything you know about checkout UX is wrong
   *(Contrarian: challenges a widely held belief without being clickbait — the edition delivers the proof)*

3. Why your progress bar might be costing you subscribers
   *(Personal relevance: "your" makes it immediately applicable to the reader's own product)*

4. New data: progress bars hurt subscription box checkouts
   *(Credibility-forward: leads with "new data" for readers who respond to evidence over intrigue)*

5. The 14% problem hiding in your checkout flow
   *(Curiosity gap + specificity: the precise number creates intrigue; "hiding" implies something discoverable)*

---
**Preview text suggestion:** New research from 4,200 checkouts — and why the fix isn't what you'd expect. (87 characters)

## Known Limitations
- Subject line performance depends heavily on list quality, send time, and deliverability — this skill optimises for copy, not those external factors
- For newsletters with fewer than 500 subscribers, A/B testing subject lines produces statistically unreliable results; treat options as directional, not conclusive
- The skill cannot account for subject line fatigue in your specific list — if your subscribers have seen the same structural pattern for months, even a well-crafted line will underperform
- Emoji recommendations are deliberately conservative; if your brand voice is more playful, specify that explicitly for better results

## Related Skills
- [edition-writer](../edition-writer/SKILL.md)
- [re-engagement-email-writer](../re-engagement-email-writer/SKILL.md)
