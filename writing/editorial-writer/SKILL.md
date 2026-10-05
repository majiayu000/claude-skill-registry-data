---
name: editorial-writer
description: "Drafts a publication editorial — a structured opinion piece written in the collective institutional voice of a publication's editorial board, arguing a clear position on a specific issue of public concern."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [editorial, opinion, argument, institutional-voice, commentary]
---
# Editorial Writer

## What This Skill Does
Drafts a publication editorial — a structured opinion piece written in the collective institutional voice of a publication's editorial board, arguing a clear position on a specific issue of public concern.

## When To Use This Skill
- Your editorial board has agreed on a position and needs a first draft that argues it clearly and without ambiguity
- You need to respond editorially to a breaking development — a policy announcement, a court ruling, a public controversy — on a tight deadline
- Your draft editorial exists but is unfocused, and you need help restructuring it around a single, defensible argument
- You are writing an editorial for a specialized publication (trade press, regional paper, subject-specific journal) and need it calibrated to that audience and tone

## What You Need To Provide
**Required:**
- The issue or event the editorial addresses
- The publication's position — what you are arguing for, against, or calling for
- The most important evidence or reasoning that supports that position (two to four points)

**Optional:**
- The intended audience (general public, policymakers, professionals in a specific sector)
- The publication's editorial tone (measured and formal, direct and campaigning, cautiously centrist)
- Word count target (standard editorial range: 350–600 words)
- The strongest counterargument to your position, so the assistant can address it rather than ignore it
- Any specific call to action the editorial should end with

## How the Assistant Approaches This
1. Opens with a framing paragraph that establishes the issue, its stakes, and why the publication is taking a position now — without burying the argument
2. States the editorial's position plainly in the first third of the piece, then devotes the middle section to building the argument with the evidence and reasoning provided
3. Addresses the strongest counterargument — if supplied — to demonstrate the board has considered it, then explains why the publication's position still holds
4. Closes with a specific, actionable conclusion: what should happen, who should act, and — where relevant — by when

## Output Format
Continuous prose, no subheadings. Three to five paragraphs. First paragraph: issue and stakes. Second and third paragraphs: argument and evidence. Fourth paragraph (optional): counterargument and rebuttal. Final paragraph: conclusion and call to action.

Tone: authoritative but not hectoring. Uses "we" sparingly — the institutional voice is implied, not announced. Avoids passive constructions that dilute the argument. No rhetorical questions as a substitute for argument.

Length: 400–550 words unless a specific target is provided.

## Quality Criteria
- [ ] The position is stated unambiguously within the first 100 words
- [ ] Every paragraph advances the argument — no filler, no throat-clearing
- [ ] Evidence cited matches what was provided in the input; no invented statistics or attributions
- [ ] The conclusion is specific: it tells someone to do something, not merely to "consider" or "reflect"
- [ ] The tone is consistent throughout — does not shift from measured to polemical without cause

## Example

### Input
Issue: A regional government has proposed cutting funding to public libraries by 30% as part of a broader austerity package. The cuts would close fourteen branch libraries and reduce opening hours at twelve others.
Position: The cuts should be reversed. Libraries serve functions no other public institution replicates, and the savings are too small to justify the damage.
Evidence:
1. The 14 branches proposed for closure serve neighborhoods with above-average rates of digital exclusion — residents without home internet access depend on library terminals for job applications, benefits claims, and government services.
2. The total saving from all library cuts amounts to 0.4% of the department's annual budget.
3. Research across three comparable regions shows that library closures increase demand for more expensive social services within 18 months.
Counterargument: Budgets are constrained and every department must contribute.
Call to action: The council should commission a full impact assessment before any vote, and pause the closure timetable until that assessment is published.
Audience: General readers in the region
Tone: Direct and clear, not polemical
Word count: 450 words

### Output
Fourteen branch libraries are scheduled to close. Twelve more will cut their hours. The regional government calls this a necessary contribution to a difficult budget. We call it a false economy — one that will cost more than it saves, and fall hardest on the people least able to absorb it.

Libraries are not discretionary. In the fourteen branches marked for closure, a significant share of regular visitors have no broadband connection at home. They use library terminals to apply for jobs, to access benefits, to submit the forms that keep them connected to public services. When those buildings close, those people do not simply find another way. The need does not disappear — it migrates to housing officers, welfare advisers, and emergency services, all of which cost more per interaction than a library visit ever did. Research from three comparable regions shows this pattern consistently: library closures increase demand for higher-cost social services within eighteen months of taking effect.

The government's counterargument is that all departments must share the burden of austerity. That is a reasonable principle. It is not a reasonable conclusion when applied to a service whose total budget represents 0.4% of departmental spending. The savings are real but marginal. The damage is real and lasting. A budget decision that permanently removes infrastructure from the most digitally excluded communities in the region is not a balanced sacrifice — it is a disproportionate one.

We recognize that no budget round is painless. But proportionality matters. Before fourteen libraries are locked and their communities left without recourse, the council owes those communities a clear-eyed account of what will replace the functions those buildings perform. No such account has been produced.

The council should pause the closure timetable immediately and commission an independent impact assessment before any vote takes place. That assessment should quantify the downstream costs — not just the savings — of each proposed closure. If the case for cutting libraries still holds after scrutiny, let it be made in the open. If it does not, the council will have saved itself from a decision it would have spent years trying to undo.

## Known Limitations
- This skill writes in a general institutional editorial voice. If your publication has a very specific, long-established editorial style — particular sentence rhythms, idiomatic phrases, recurring structural patterns — the assistant will approximate it but not replicate it. Pass the draft to a senior editor for voice calibration.
- Editorials that engage with live legal proceedings, pending legislation, or active criminal investigations require legal review before publication. This skill does not flag legal risk.
- The skill works from the evidence and reasoning you supply. If your inputs are thin (one point, no counterargument), the draft will reflect that. Strong editorials come from strong editorial positions — garbage in, garbage out.

## Related Skills
- [column-voice-adapter](../../../magazine-journalism/writing/column-voice-adapter/SKILL.md)
- [story-angle-finder](../../../magazine-journalism/ideation/story-angle-finder/SKILL.md)
- [reportage-structure](../../../magazine-journalism/writing/reportage-structure/SKILL.md)
