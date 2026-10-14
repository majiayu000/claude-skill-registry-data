---
name: arcade-voice
description: Use when writing or editing words a player reads in the Family Arcade or any game in this repo (front door, game cards, HUD states, instructions, hints, wins and losses, errors, waiting and empty states, buttons, pause and results screens), or when game copy is called unclear, long, flat, too jokey or off-voice.
---

# Arcade voice

The readers are children, often reading aloud next to a grown-up, and their families, mid-game
and glancing. **Clarity first, then fun**.

The voice is the **coin-op cabinet**: short, sure words for what is happening and what to do
next. Under it, rarely, a **showman's wink** from the Midnight Carnival's ringmaster: one line of
flavour in a subline, never in the part a child must understand.

## The shapes (budgets are maximums)

| Element | Shape | Budget |
|---|---|---|
| State or headline | What is happening, in capitals (the condensed display font): READY, NEW BEST, FUEL TRUCK!, OUT OF ORDER | 4 words |
| Subline under a state | One plain sentence: what it means, or what to do now. The only place a wink may go | 14 words |
| Instruction or hint | Verb first, the exact thing to touch or do: "Hold the gas down." | 10 words |
| Button | Verb first, says what happens: "Play Gulp", "Race again", "Back to arcade" | 3 words |
| Game card | What you do, in the game's own words, then its twist | 2 sentences, 25 words |
| Win or loss | State (YOU WIN, {NAME} WINS) plus a subline with the number that matters | as above |
| Error | State (OUT OF ORDER, NO CONNECTION) plus a subline: what is safe, then what to do | as above |
| Waiting or empty | State (WAITING FOR PLAYER 2, NO SCORES YET) plus the one thing to check or do | as above |

## The fun budget

- **Clarity wins every tie.** Read the screen with the wink removed: a child must still know what
  happened and what to do.
- **Rare.** At most one wink per screen, and most screens have none. Good places: the front
  door, a crash, a close loss, a big win, the results screen. Never in instructions, buttons,
  settings or anything a player reads while acting.
- **From the arcade's own world:** a gremlin in the machine, the crowd wanting a rematch, free play
  all night, a ticket. Never a pun that needs explaining, never at the player's expense.
- **Exclamation marks** only on a real alert or a win, one per screen at most.
- **No mobile-ad energy:** no fake urgency, no "AMAZING!!!", no coin-and-gem hype, no streak
  pressure, no "don't miss out".
- **Capitals for states only** (4 words at most); everything else in sentence case, because early
  readers read sentences, not shouting.

## Write it in this order

1. **The state:** what is happening, in four words or fewer.
2. **The subline or instruction:** what it means or what to do, verb first.
3. **Cut:** "please", "just", "simply", "now you can". A number beats an adjective ("12 coins",
   not "lots of coins"). One idea per line. Name the real thing ("the gas key", not "the button").
4. **Read it aloud** as if to a seven-year-old. If they would ask "what?", rewrite.
5. **Only now:** does this screen earn a wink? If yes, it goes in the subline, and the meaning
   stays intact.
6. **Fit:** states on one line and sublines on at most two, at 393 px wide.

## Each game keeps its own words

The shapes and the fun budget are shared; the vocabulary is each game's: Gulp swallows and grows,
the racer has coins and laps, Risk has armies and territories, Ship Battle has fleets and shots.
A game's own copy file or test, where it has one, still applies, and a calmer game stays calmer
than the racing games.

Before and after, from our games: `examples.md`.
