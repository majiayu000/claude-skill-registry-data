---
name: reviewer-response-builder
description: Draft structured point-by-point responses to peer reviewers and editors, including polite rebuttals, revision summaries, response tables, changed-text snippets, and claim-safety edits. Use for 审稿意见回复, rebuttal letter, response to reviewers, revise and resubmit, editor response, reviewer comments, or when reviewer/editor feedback is provided.
---

# Reviewer Response Builder

## Purpose

Create respectful, precise, and traceable responses to reviewer and editor comments. The goal is to clarify what was changed, what evidence supports the response, and what remains outside the study scope.

## Typical Inputs

- Reviewer comments copied from a decision letter.
- Editor comments or revision requirements.
- A manuscript excerpt, revised text, or line-number information.
- A list of analyses that were or were not performed.

## Core Rules

- Do not invent analyses, line numbers, results, citations, experiments, or supplementary materials.
- Do not promise revisions that were not actually made.
- Do not fabricate reviewer quotes.
- Do not conceal limitations.
- Preserve scientific claim boundaries, especially for clinical, statistical, and bioinformatics manuscripts.
- Recommend final human review and author verification of every response before submission.

## Workflow

1. Split reviewer feedback into individual actionable comments.
2. Classify each comment as:
   - accepted and revised
   - partially accepted
   - clarified in text
   - respectfully rebutted
   - outside scope or future work
3. Draft a response with:
   - brief thanks
   - direct answer
   - specific revision made
   - revised manuscript text when available
   - page/line location only if supplied or verifiable
4. Keep tone consistent and professional.
5. Add an editor-facing summary of major revisions.

## Output Format

```markdown
# Response to Reviewers

Dear Editor,

[brief revision summary]

## Reviewer 1

**Comment 1.** [comment]

**Response.** [direct answer]

**Revision made.** [changed text or location]
```

## Tone Rules

Use:

- "We thank the reviewer for this helpful comment."
- "We agree and have revised..."
- "We have clarified..."
- "We respectfully note that..."
- "We have added this as a limitation..."

Avoid defensive language, vague claims of improvement, and repeated formulaic gratitude.

## Quality Checklist

- Every response maps to a specific comment.
- No unsupported revision is promised.
- Locations are real or omitted.
- Limitations remain visible.
- The final letter requires author review before submission.
