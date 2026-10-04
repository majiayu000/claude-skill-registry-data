---
name: byte-discuss
description: Clarify requirements, tradeoffs, or direction without implementing. Use when the user asks to discuss first, compare choices, resolve ambiguity, or confirm scope.
---

# Byte Discuss

Help the user reach a clearer decision through a natural conversation. Do not
turn the discussion into a questionnaire or a fixed ceremony.

## Approach

- Reflect the current understanding in the form most useful to the conversation.
- Surface only ambiguities that could materially change scope, UX, technical
  direction, cost, or acceptance.
- Offer a reasoned recommendation and sensible defaults, not just questions.
- Ask one or a few focused questions only when their answers are needed now.
- Explore alternatives when they illuminate a real tradeoff.
- Do not write product code unless the user changes the request.

Avoid mandatory headings, role-play, question counts, or handoff menus. A short
paragraph may be enough; a comparison table may be better for several options.

Persist notes only when the user asks or the discussion is part of a resumable
project. Prefer a concise decision note over multiple Byte OS artifacts.

Apply relevant active lessons when present. If the user corrects a material
misunderstanding, update `.byte-os/LESSONS.md` with the correction and a reusable
prevention rule. Do not treat ordinary clarification as a mistake or store
sensitive details.

Conclude with the clearest current recommendation and any genuinely unresolved
decision. Suggest another Byte skill only when it would be useful.

## Source And Updates

Canonical repository: [elan6666/your-bytedance-skills](https://github.com/elan6666/your-bytedance-skills). Use its current `main` branch when checking for or installing updates.
