---
name: pstack-unslop
description: "Edit requested prose to remove vague claims, stock AI phrasing, filler, or dense wording while preserving meaning, evidence, uncertainty, and the user's voice."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/unslop
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Unslop

Make the requested prose concrete and readable. This is an editing capability, not an always-on replacement for the user's style.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Edit for meaning

Identify the audience, purpose, and intended tone. Preserve facts, scope, caveats, citations, technical identifiers, and quoted material.

Replace vague attribution with a named source or remove the unsupported claim. Say what a mechanism does rather than how it feels. Replace generic improvement claims with the demonstrated result when available.

Cut filler, praise, repeated framing, unnecessary synonyms, and abstract metaphors. Prefer familiar verbs. Split dense sentences and name the actor when that clarifies responsibility.

Use lists, emphasis, and punctuation where they aid comprehension. Avoid mechanical bans on all parentheses, dashes, passive sentences, or technical vocabulary. Correct terminology earns its place.

## Deliver

Return the edited text directly. Preserve the user's language and formatting requirements. If the original makes an unsupported factual claim, flag it or retain explicit uncertainty instead of inventing evidence.
