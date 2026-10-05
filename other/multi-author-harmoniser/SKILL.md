---
name: multi-author-harmoniser
description: "Takes a draft written by two or more contributors and rewrites it as a single, consistent voice — smoothing over clashing tones, register shifts, and stylistic inconsistencies while preserving every author's factual content and reported material."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, style, voice, collaboration, consistency]
---
# Multi-Author Harmoniser

## What This Skill Does
Takes a draft written by two or more contributors and rewrites it as a single, consistent voice — smoothing over clashing tones, register shifts, and stylistic inconsistencies while preserving every author's factual content and reported material.

## When To Use This Skill
- When two reporters have jointly written a news feature and their sections read noticeably differently
- When a freelance contribution has been stitched into a staff-written piece and the seams are visible
- When a multi-part investigation has been written by different team members over several months
- When translated content from different translators has been combined into one article
- Before a long-form piece goes to a senior editor and the multiple-author origin would be obvious

## What You Need To Provide
**Required:** The full draft text to be harmonised.
**Optional:** A target house style or reference publication (e.g., "write in the style of a quality broadsheet news feature — authoritative, direct, no first person"); the preferred tense (past or present); whether to preserve each author's section roughly intact or allow restructuring for flow; any passages that must not be changed (confirmed quotes, legal-approved text, translated sections).

## How the Assistant Approaches This
1. Reads the full draft and maps the stylistic variation: identifies shifts in sentence length, vocabulary register, use of first or second person, punctuation habits, tonal warmth or distance, and paragraph structure — noting roughly where each style shift occurs.
2. Establishes a target voice for the harmonised version, either from explicit instructions provided, or — if none are given — by averaging toward the more formal or more consistent of the styles present in the draft.
3. Rewrites the full text in the target voice, preserving all factual claims, quotes, and reported information. Where restructuring would help flow, it does so conservatively — keeping the original sequencing unless a clear improvement is available. Returns the harmonised draft in full, followed by a brief editor's note listing the main changes made and any passages that were left as-is (e.g., direct quotes, confirmed legally approved text).

## Output Format
- The full harmonised draft, ready to hand to a sub-editor.
- An editor's note (50–100 words) at the end of the output listing: the dominant style inconsistencies found, the voice standard applied, any sections left unchanged and why.
- Length matches the input — no compression or expansion unless instructed.
- Tone of the harmonised draft: matches the target style specified, or defaults to clear, authoritative, third-person newspaper register if none is given.

## Quality Criteria
- [ ] No factual content has been changed, added, or removed — only style and register
- [ ] Direct quotes are reproduced verbatim and not paraphrased
- [ ] The harmonised text reads as a single voice throughout — a blind reader could not detect the join points
- [ ] The editor's note accurately describes what was changed
- [ ] Passages flagged as must-not-change are preserved exactly

## Example

### Input
**Draft text (two-author join visible between sections):**

"The regional government announced Tuesday that it will close four public hospitals as part of its austerity programme. Officials said the move would save approximately €40 million annually.

Dr Amira Osei, who has worked at one of the affected facilities for eleven years, is devastated. 'These aren't just buildings — they're the heart of this community,' she told us, her voice cracking. 'People will die because of this decision.' The waiting room behind her was busy even on a Wednesday afternoon, families with small children, elderly patients clutching referral letters.

The cuts are part of a broader fiscal consolidation plan, per the government's Q4 budget statement. It is projected that service delivery in non-urban zones will be adversely impacted. The administration has indicated that a proportion of affected clinical staff may be redeployed to remaining facilities, though precise figures have not been confirmed at this stage."

**Target style:** Quality broadsheet news feature — third person, past tense throughout, no first person, authoritative but not cold.

### Output
**Harmonised draft:**

The regional government announced on Tuesday that it would close four public hospitals as part of its austerity programme, in a move officials said would save approximately €40 million a year.

Dr Amira Osei, who had worked at one of the affected facilities for eleven years, said the decision would devastate the communities the hospitals served. "These aren't just buildings — they're the heart of this community," she said. "People will die because of this decision." The waiting room behind her was busy on a Wednesday afternoon, with families with young children and elderly patients clutching referral letters.

The closures form part of a broader fiscal consolidation plan set out in the government's most recent budget statement. Officials projected that health service delivery in rural and semi-rural areas would be significantly affected. The administration said a proportion of clinical staff from the affected hospitals could be redeployed to remaining facilities, though precise numbers had not been confirmed.

---

**Editor's note**
Main changes: The third section had shifted into a more bureaucratic register ("per the government's Q4 budget statement", "adversely impacted", "at this stage") and mixed tenses. Rewritten to match the direct, third-person narrative register of the opening. "We" removed from the interview passage; "told us" changed to "said." Budget reference ("Q4 budget statement") generalised to "most recent budget statement" to avoid jargon. Dr Osei's quotes left verbatim. No factual content changed.

## Known Limitations
- The assistant cannot verify whether factual content has changed if the input contains ambiguous or vaguely worded claims — it preserves the wording it receives. Always read the harmonised draft against the original before publishing.
- Very long pieces (over 3,000 words) may show some residual variation in the harmonised output, particularly if the source styles are sharply different. A second pass may be needed.
- The assistant cannot enforce a specific publication's proprietary house style unless that style is described in the instructions. Naming a target publication without specifying the style rules will produce only an approximation.
- Dialect, idiolect, or deliberately unconventional writing in one author's section may be normalised out unless you explicitly flag it as intentional.
- This skill works on text. It cannot harmonise audio, video narration, or multi-author scripts without a transcript.

## Related Skills
- [house-style-enforcer](../../magazine-journalism/editing/house-style-enforcer/SKILL.md)
- [copy-editor-assistant](../../magazine-journalism/editing/copy-editor-assistant/SKILL.md)
- [jargon-flagger](../../magazine-journalism/editing/jargon-flagger/SKILL.md)
- [column-voice-adapter](../../magazine-journalism/writing/column-voice-adapter/SKILL.md)
