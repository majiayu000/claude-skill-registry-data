---
name: add-character
description: Use when implementing a Town Hall character ability in Salem 1692. Covers reading the rulebook edge cases, following the existing character pattern, handling ability inheritance, writing tests, and running the suite. Invoke once per character in priority order.
---

# Add Character Ability

## Implementation Priority

Implement in this order — later characters have interactions with earlier ones:
1. Tituba
2. Cotton Mather
3. Thomas Danforth
4. George Burroughs
5. John Proctor
6. Martha Corey
7. Mary Warren
8. Remaining characters

## Step 1 — Read Before Writing Anything

Read all three before writing code:
1. The most similar existing character implementation
2. Rulebook pages 12–14 for this character's edge cases (@docs/Salem_Rulebook.pdf)
3. Development guide Phase 5.2 (@docs/Salem_1692_Development_Guide.md)

## Step 2 — State the Ability and All Edge Cases

Write in plain English before coding:
- What the ability does
- When it triggers
- Every edge case from rulebook pages 12–14
- Any interactions with already-implemented characters

## Step 3 — Identify Hook Points

| Hook | When it fires |
|---|---|
| `onTurnStart` | Beginning of this player's turn |
| `onCardPlayed(card, target)` | When any player plays a card |
| `onAccusationPlaced(count)` | When an accusation is placed on this player |
| `onTryalRevealed(tryal)` | When one of this player's tryals is revealed |
| `onPlayerEliminated(player)` | When any player is eliminated |
| `onAbilityInherited(fromCharacter)` | When ability is inherited via John/Martha |

## Step 4 — Implement

- Ability logic in `server/src/characters/[character_name].js`
- If ability needs player input, use `promptPlayerChoice` helper
- Store accusation modifiers on the player object, not at calculation time
- Implement both `onAbilityInherited` and `onAbilityLost` if transferable

## Step 5 — Write Tests

One test per edge case in `server/tests/characters/[character_name].test.js`:
- [ ] Normal ability activation
- [ ] Each edge case from Step 2
- [ ] Interaction with other characters if documented
- [ ] Ability inheritance received and lost (if applicable)

## Step 6 — Run the Full Suite

```bash
cd server && npm test
```

All existing tests must still pass. Do not suppress or skip existing tests.

## Common Mistakes

- Checking character by name string in core logic — use the hook registry
- Applying ability effects before checking if the player is eliminated
- Forgetting `onAbilityLost` — if an ability can be gained, it can be lost
- Accusation math at calculation time — store modifier on the player object