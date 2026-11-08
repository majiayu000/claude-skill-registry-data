---
name: unslop
description: Review and improve prose that sounds formulaic, generic, robotic, or AI-generated while preserving the author's facts, intent, voice, and useful structure. Use for writing audits, humanization, editing, documentation, emails, posts, and rewrites.
metadata:
  origin: https://github.com/theclaymethod/unslop
  mirror: https://github.com/Badhon-00/unslop
  integration: mdcp-adapter
---

# Unslop — MDCP writing quality skill

Use this skill to improve writing without flattening the author's voice or changing meaning.

## Safety and operating contract

1. **Audit before editing.** If the user asks for review, detection, feedback, or an audit, report issues and do not modify the text.
2. **Rewrite only when requested.** If the user explicitly asks to rewrite, humanize, polish, or clean up, produce a revised draft.
3. Preserve factual claims, names, numbers, dates, quotations, code, technical terms, links, legal wording, and the author's intended meaning.
4. Prefer targeted edits over wholesale reconstruction. Keep sentences that already work.
5. Do not treat a phrase list or writing-style heuristic as proof that a human or AI wrote something. Never make authorship accusations.
6. Avoid replacing one formulaic pattern with another. Do not add fake anecdotes, invented citations, unsupported specifics, or artificial imperfections.
7. If a requested change conflicts with factual preservation, explain the conflict and ask before changing the fact.

## Workflow

### Audit-only

- Identify exact excerpts that sound generic, repetitive, over-signposted, inflated, or structurally repetitive.
- Explain briefly why each excerpt weakens clarity or voice.
- Separate clear problems from subjective style choices.
- Return a prioritized list of suggested edits. Do not rewrite the source.

### Rewrite

- Identify the author's audience, purpose, register, and any explicit style constraints.
- Diagnose only the passages that need work.
- Rewrite with concrete language, varied but natural sentence rhythm, direct transitions, and the author's original level of formality.
- Preserve paragraph order and structure unless the user asks for restructuring.
- Compare the result against the source for changed facts, omitted constraints, invented content, and accidental tone shifts.
- Return the revised text; include a short validation note when the user asks for analysis.

### Teach a voice

When the user explicitly asks to learn or reuse their voice, request or use writing samples they provide for that purpose. Summarize observable style traits and let the user approve the profile before applying it to future writing. Do not infer private traits or imitate a third party without authorization.

## Commands

- `audit`: report-only review.
- `rewrite`: targeted humanization, only when requested.
- `teach`: build a user-approved voice profile from supplied samples.
- `mimic`: draft in the user's approved voice profile.

## Upstream implementation

For the full UNSLOP scanner suite, command references, voice tooling, and benchmark harness, install the upstream project separately:

```bash
npx skills add theclaymethod/unslop -g
```

MDCP does not bundle or execute the upstream Python scripts. The upstream README reports that its latest core product evaluation was a **no-ship** against its precision, damage, and whole-document safety thresholds. Treat scanner results as review suggestions, not a quality or authorship guarantee.

Upstream: [theclaymethod/unslop](https://github.com/theclaymethod/unslop)  
Owner mirror: [Badhon-00/unslop](https://github.com/Badhon-00/unslop)
