---
name: tcg-art-direction
description: Plan original trading card game and card-battler visual direction for TCG/CCG card frames, card illustrations, board styling, tokens/minions, hand/deck/graveyard zones, VFX, and Hearthstone-like fantasy tabletop polish while keeping references IP-safe.
engines: [AGNOSTIC]
---

## When to use

Use when the task asks for trading card game, collectible card game, deck-builder, card battler, card frame, board, token/minion, graveyard/discard, hand/deck presentation, rarity styling, or Hearthstone-like fantasy card-game visual guidance.

## Output

- Target style family and rationale.
- Original card, board, token, and VFX art direction.
- Asset brief using the TCG template when implementation or generation will follow.
- IP-safety notes when named commercial games are used as inspiration.
- Sanity/readability checks for generated or implemented visuals.

## Workflow

1. Identify the artifact type: card illustration, card frame, board UI, token/minion, VFX, style bible, or full TCG art pack.
2. Choose a style from `references/style-taxonomy.md`; default to `warm-tavern-fantasy` for Hearthstone-like warmth.
3. Read `references/ip-safety.md` whenever named games, studios, or commercial card-game references are part of the request.
4. Use `references/asset-brief-template.md` to produce a handoff-ready brief.
5. Preserve gameplay readability: hand, deck, graveyard/discard, battlefield tokens, counters, targeting, and active prompts must remain inspectable.
6. For generated images, compose with `generative-art-designer`, `iterate-art-to-sanity`, and `enforce-art-language-safety`.
7. For UI/vector implementation, compose with `board-ui-artist`, `css-vector-artist`, and `frontend-developer`.

## Notes

- Treat Hearthstone, Magic: The Gathering Arena, Might & Magic Fates, and Gods Unchained as broad reference points only.
- Translate references into original materials, shape language, mood, color hierarchy, readability goals, and interaction patterns.
- Do not copy proprietary card frames, boards, logos, characters, factions, iconography, UI layouts, or exact compositions.
- Keep Hephaera outputs reusable; host-project-specific art decisions belong in the host repository.
