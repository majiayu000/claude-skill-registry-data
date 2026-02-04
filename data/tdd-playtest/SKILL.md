---
name: tdd-playtest
description: Test-Driven Development combined with emergent playtesting for Quest Keeper AI. Use when running playtest sessions, writing tests, debugging game feel issues, or following the RED-GREEN-REFACTOR cycle.
---

# TDD + Playtesting Loop

## The Philosophy
> **We are the player.** Not a tester, not a developer. A player who wants to have fun.

## The Loop
```
1. PLAY        Experience the game as a player
2. DISCOVER    Find friction, confusion, missing features
3. DEFINE      What SHOULD happen? (Player perspective)
4. RED         Write test that fails
5. GREEN       Write minimal code to pass
6. REFACTOR    Clean up
7. PLAY AGAIN  Does it feel right now?
```

## Discovery Entry Format
Add to `Agents/EMERGENT_DISCOVERY_LOG.md`:
```markdown
### [CATEGORY-###] Title
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**Player Experience:** What happened vs what should happen
```