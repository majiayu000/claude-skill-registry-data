---
name: secretary-humanizer
description: Naturalize user-facing language while preserving facts, intent, register, and authentic Chinese expression.
license: MIT
compatibility: opencode
---

# Secretary Humanizer

Refine user-facing language so it sounds natural, specific, and appropriate for its audience. Default final user content to Simplified Chinese unless the user explicitly requests another language or the task clearly requires one. Preserve source-language code, commands, paths, logs, identifiers, and quotations when appropriate.

## Scope

- Handle language naturalization, reduction of conspicuous AI tone, register recognition, factual preservation, and idiomatic Chinese expression.
- Do not add research, facts, numbers, events, quotations, sources, personal experience, certainty, or emotion that the supplied context does not support.
- Do not change the output route or take responsibility for delivery mechanics or visual presentation.

## Working method

1. Identify the intended register: conversational, formal, or technical. Match the audience, relationship, channel, and purpose.
2. Preserve every concrete fact, qualification, constraint, conclusion, and meaningful ambiguity. Separate confirmed facts, reasonable inference, and unknowns.
3. Rewrite for directness and natural rhythm. Prefer specific wording and a credible mix of short and long sentences over uniformly polished prose.
4. Remove customer-service stiffness, flattery, inflated significance, vague attribution, canned transitions, generic scene-setting, empty slogans, rhetorical symmetry, and formulaic summaries.
5. Revise once for obvious AI residue, then stop when the text is accurate, purposeful, natural for its register, and still carries the writer's identity.
6. Return only the final version unless the user asks for drafts, rationale, or a change summary.

## Chinese expression

- Use natural Simplified Chinese punctuation, word order, paragraphing, and collocation rather than translated English syntax.
- Avoid corporate enablement and closed-loop jargon unless the source or domain genuinely requires it.
- Keep established technical terms when they are clearer. In mixed Chinese and English, determine register paragraph by paragraph and do not switch languages merely for effect.
- Allow restrained first person, parentheses, small self-corrections, or an occasional rough edge when the register permits, but never manufacture personality or personal history.
- Avoid excessive headings, bold text, emoji, and ornamental phrasing. Prefer clear claims with appropriate limits.

## Attribution

This skill adapts selected methodologies and principles from humanizer (MIT, Copyright 2025 Siqi Chen) and qu-ai-wei (MIT, Copyright 2026 @LifelongLazyLearner). It does not reproduce their complete upstream content.
