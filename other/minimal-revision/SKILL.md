---
name: minimal-revision
description: Revise an already accepted article, essay, paper, statement, or manuscript under strict minimal-change constraints while still satisfying reviewer comments, supervisor feedback, or requested edits. Use when the user asks for minimal edits, smallest necessary changes, preserve the current voice, keep the existing style, avoid broad rewriting, or implement requested revisions without unnecessary polishing.
---

# Minimal Revision

## Overview

Use this skill to revise a draft that is already acceptable in its current state. Treat the current draft as the approved baseline, complete all newly requested revisions, and make only the minimum changes needed.

## Core Goal

Follow these priorities in order:

1. Treat the current draft as an already qualified baseline.
2. Satisfy every new explicit revision requirement.
3. Minimize the total edit footprint while completing those requirements.
4. Preserve the draft's existing wording habits, rhythm, structure, and tone.
5. Avoid polished rewriting that changes the approved voice without need.

## Non-Target Freeze Rule

Only modify text that is directly required by a new revision request.

If a word, phrase, sentence, paragraph, citation, or section is not part of the required change, leave it exactly as it is.

Do not touch nearby text just because it could be smoother, cleaner, more consistent, or more natural.

## Default Mindset

Assume the current draft is intentionally shaped and should not be re-optimized.

Do not "improve" the article unless the requested revision requires it. Preserve the existing level of roughness, repetition, sentence cadence, and wording texture whenever they do not block the requested change.

Treat every requested edit as a constrained repair task on top of an already acceptable baseline, not as a writing-improvement task.

## Required Inputs

Work from these inputs when available:

- the current article or manuscript draft
- the requested revisions, comments, tracked changes, or feedback list
- any user constraint about sections that must remain untouched

If a request is ambiguous, ask only the narrowest question needed to avoid unnecessary rewriting. Do not guess and then compensate with broad cleanup.

## Revision Triage

Sort revision requests before editing:

1. must-fix items that are explicitly required by the user, teacher, reviewer, or supervisor
2. should-fix items that block correctness, consistency, or obvious compliance with the comment
3. leave-as-is items that are merely awkward but do not block the requested revision

Do not convert a leave-as-is issue into an extra rewrite task.

## Edit Budget

Always start with the smallest possible edit scope. Escalate only when the smaller scope cannot satisfy the request.

Use this escalation ladder:

1. punctuation, spacing, marker, or formatting adjustment
2. single-word replacement
3. short phrase replacement
4. local clause rewrite
5. one-sentence rewrite
6. two adjacent sentences
7. paragraph-level rewrite only when the requested revision cannot be completed any other way

Do not jump to sentence or paragraph rewriting if a word-, phrase-, or clause-level edit is enough.

## Protected Content

Preserve these items unless the revision request explicitly targets them:

- names of people, places, institutions, and works
- dates, numbers, percentages, article numbers, citations, and references
- established technical terms and key terms already used in the draft
- headings, numbering, list structure, and section order
- quotations, cited wording, and terminology that must stay aligned with source material

If a requested change appears to alter protected content accidentally, stop and flag it instead of silently rewriting around it.

## Revision Workflow

Use this workflow every time:

1. Read the current draft and the revision request together.
2. Break the request into discrete required changes.
3. For each change, locate the narrowest affected text span.
4. Choose the lowest edit level from the edit budget that can satisfy the request.
5. Apply the revision only to that span.
6. Freeze all non-target text and leave it untouched.
7. Preserve surrounding wording, sentence order, paragraph order, and local phrasing unless changing them is necessary for grammatical completeness.
8. If new text must be added, build it from nearby wording patterns instead of inserting a freshly polished style.
9. After all edits, run a preservation pass and revert any accidental smoothing, expansion, or stylistic normalization.

## Preservation Rules

Preserve these features by default:

- sentence length pattern and pacing
- paragraph order and paragraph boundaries
- punctuation habits and citation placement
- repeated wording patterns that are already in the draft
- terminology already used in the draft
- the draft's current register, including slightly blunt or uneven phrasing
- formatting, numbering, headings, and list structure

When a revision adds content, match the local sentence texture of the surrounding passage instead of writing in a cleaner or more uniform register.

## Forbidden Default Behaviors

Do not do any of the following unless the user explicitly requests them:

- rewrite a full paragraph for fluency
- globally polish tone or academic style
- edit nearby text that was not part of the requested change
- add transitions just to make the writing smoother
- replace several local edits with one cleaner full rewrite
- normalize terminology across the whole document
- remove repetition only because it sounds awkward
- expand explanations beyond what the revision request requires
- make the article sound more formal, balanced, or textbook-like
- silently restructure argument flow when the request only asks for local corrections

## Handling Different Revision Types

Apply these defaults:

- For factual corrections, change only the incorrect factual fragment and keep the surrounding sentence shape.
- For logic or clarity comments, repair only the missing link or unclear phrase instead of rewriting the whole paragraph.
- For tone or wording comments, swap the smallest phrase that resolves the complaint.
- For requests to add content, insert the shortest passage that satisfies the requirement and mimic the nearby style.
- For deletion requests, remove only the targeted material and avoid compensatory rewriting unless the sentence becomes broken.
- For citation or formatting corrections, preserve the existing prose and fix only the citation or formatting fragment.

## Ambiguity Protocol

If a revision request cannot be applied confidently with local edits:

1. identify the exact uncertain span
2. state what is ambiguous
3. propose the narrowest reasonable options
4. avoid broad rewriting while waiting for clarification

If the user still wants a direct attempt, choose the least invasive option and label it as provisional.

## When Broader Change Is Unavoidable

If a requested revision genuinely cannot be completed through local edits:

1. expand the scope by one level only
2. keep as much original wording as possible
3. preserve the original paragraph logic and cadence
4. avoid using a noticeably cleaner or more synthetic voice
5. mention that a broader rewrite was necessary

Do not use unavoidable change in one place as permission to polish nearby text.

## Output Standard

When returning the revised result:

- provide the revised text or file directly
- keep changes limited to requested areas
- note only the places where broader-than-local edits were unavoidable
- flag ambiguities instead of hiding them behind a smooth rewrite

If the user asks for a summary of changes, describe them as localized revisions, not as "improvements" unless the user explicitly wants that framing.

## Required Final Feedback

After finishing the revision, always give a compact post-edit report even if the user does not explicitly ask for one.

Include all of the following:

- an estimate of how much content changed
- a rough estimate of how much the edit footprint expanded beyond the requested revision
- a summary of what was changed

## How to Report Change Volume

Report the edit footprint using practical, approximate measures instead of pretending to have exact forensic precision.

Use whichever measures are realistic for the artifact:

- number of edited sentences
- number of edited paragraphs
- approximate count of changed words or characters
- a rough percentage of the full article affected

Prefer conservative phrasing such as:

- "about 3 sentences changed"
- "roughly 40 to 60 Chinese characters adjusted"
- "approximately 5% of the article was touched"

Do not overstate precision when the estimate is only visual or manual.

## How to Estimate AI-Risk Increase

Do not present AI-rate growth as a measured fact unless the user provided an actual detector result before and after revision. In normal cases, present it as a rough risk estimate only.

Base the estimate on the edit footprint and edit style:

- very low increase: tiny local edits, mostly corrections, no smoothing rewrite
- low increase: several phrase or clause edits, but wording texture still preserved
- moderate increase: multiple sentence rewrites or visible local smoothing
- high increase: paragraph-level rewriting, normalization, or cleaner synthetic cadence

When possible, express the estimate as a small range with clear uncertainty, for example:

- "estimated AI-risk increase: about 0% to 2%"
- "estimated AI-risk increase: about 2% to 5%"

Also state the reason in one short line, such as:

- "The estimate stays low because only local phrases were adjusted."
- "The estimate is higher because two sentences required full rewrites."

If the user wants a stronger claim, explicitly state that a real before-and-after detector run would be needed.

## How to Summarize What Changed

Always summarize the revision in a localized way. Keep the summary tied to requested edits, not to general writing quality.

Summarize by one or more of these dimensions:

- section or paragraph location
- corresponding comment or revision request
- change type such as factual correction, wording swap, deletion, insertion, citation fix

Prefer concise lines such as:

- "Paragraph 2: replaced one phrase to address the logic comment."
- "Conclusion: added one short sentence to satisfy the missing-point request."
- "Section 3 citation: restored bracket format and original citation position."

If some requested changes forced broader rewriting, call them out separately.

## Recommended Final Report Format

Use a compact closing structure like this:

- revised text or revised file
- change volume: edited sentences, paragraphs, approximate changed words or characters, and rough percentage touched
- AI-risk estimate: a small percentage range plus one-line reason
- change summary: localized list of what changed and why
- unresolved items: only if ambiguity or forced broader edits remain
