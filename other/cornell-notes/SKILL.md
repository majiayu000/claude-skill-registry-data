---
name: cornell-notes
description: "Trigger: Cornell note, lesson notes, standalone learning summary. Transform supplied material into self-contained Markdown inline."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "3.1.0"
---

# Cornell Notes

## Activation

Format supplied teaching material into an inline Cornell lesson or standalone summary. This is a transformation method, not a publisher or a lesson-closing workflow.

## Inputs

Required: source material and profile (`lesson` or `summary`). Optional: title, supplied date, used sources, language, learner explanation, concept IDs, and literal learner evidence references. Default language to the conversation. Distinguish teacher statements from actual learner words; mark missing learner evidence pending.

## Method

For a lesson, use the inline template below; no asset read is required. Write self-contained retrieval questions with explanatory Notes: each expected answer must be available in that row's taught material. Include the central model and relationships. Prefer a small useful set; split an overloaded lesson rather than fill a quota. Questions remain available as ordinary retrieval practice for any later learner-requested review; there is no scheduling or calendar.

Keep the learner Summary pending until the learner's own explanation is supplied. Lightly clean their wording without adding understanding they did not demonstrate. Authorship separation is strict: supplied literal quotes (with their provenance) are the only learner words; teacher synthesis, outlines, and assessments are never presented as learner words, and a paraphrase is never quoted as literal. Record practice omission when supplied, without inventing completed practice.

For a summary, lead with a synthesis, then a question/Notes table, a session-grounded example when available, and sources actually used (or the localized equivalent of `None`). Translate headings into the requested language. Do not add route metadata, progress, or an invented learner Summary.

A diagram is optional when it clarifies the material. Do not invent citations or claim that formatting improves measured comprehension.

## Output

Return the complete Markdown inline, distinguishing teacher synthesis from learner evidence. No scheduling, sibling invocation, directory discovery, or file write. Optional persistence belongs to the caller with an explicit destination and save request.

## Lesson template

Translate headings into the materials language and fill placeholders from supplied inputs.

```markdown
# {Lesson title}

> Module: {supplied ID or standalone} · Date: {supplied date or unknown}
> Sources: {actually used sources, or None}
> Concept revision: {supplied revision or standalone}

## Central model

{Key concepts and their causal relationships. Optional useful diagram.}

## Notes (Cornell)

| Cue (question) | Notes / expected answer |
| --- | --- |
| {retrieval question} | {self-contained explanation grounded in taught material} |

## Worked example

{A small example distinct from the learner's task.}

## Learner Summary

_Pending learner explanation or equivalent supplied evidence._
```

Replace the pending Summary only with supplied learner evidence, quoted literally when references are provided. Never invent or alter learner words while formatting a note.
