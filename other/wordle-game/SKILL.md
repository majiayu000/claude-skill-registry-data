---
name: wordle-game
description: Build a Wordle-style word-guessing game — secret word selection, guess evaluation with correct duplicate-letter handling, green/yellow/gray feedback UI, and guess-history rendering. Use when asked to build a word-guessing game, a Wordle clone, or add Wordle-style feedback to another game.
---

# Wordle-style game

## Core loop

1. Pick a secret word of fixed length `N` (classic Wordle: 5) from a curated word list.
2. Player submits guesses of the same length, up to a max guess count (classic: 6).
3. Each guess is evaluated letter-by-letter against the secret and rendered with three states: `correct` (right letter, right position), `present` (right letter, wrong position), `absent` (not in the word, or all copies already accounted for).
4. Win when a guess matches exactly. Lose when guesses run out.

## The one part that's easy to get wrong: duplicate letters

A naive per-index comparison over-counts `present` when the secret has fewer copies of a letter than the guess does. The correct algorithm is two passes: first mark exact matches and consume one count per match from the target's letter tally, then in a second pass mark `present` only if the target still has unconsumed copies of that letter.

```js
function evaluateGuess(guess, target) {           // guess, target: arrays of single-char strings, same length
  const len = guess.length;
  const statuses = Array(len).fill("absent");
  const remaining = {};

  for (let i = 0; i < len; i++) {
    if (guess[i] === target[i]) {
      statuses[i] = "correct";
    } else {
      remaining[target[i]] = (remaining[target[i]] || 0) + 1;
    }
  }
  for (let i = 0; i < len; i++) {
    if (statuses[i] === "correct") continue;
    const letter = guess[i];
    if (remaining[letter] > 0) {
      statuses[i] = "present";
      remaining[letter] -= 1;
    }
  }
  return statuses;
}
```

Test this specifically with a guess that repeats a letter more times than the target has (e.g. guess `ARENA` vs a target with only one `A`) — that's the case naive implementations get wrong.

## Word list

- Curate a "secret answers" list of common, guessable words — avoid obscure words as secrets even if you accept them as valid guesses. A few hundred common words of the target length is plenty for casual play.
- If you want to validate guesses against a dictionary (reject non-words), keep that list separate and much larger than the secret-answer list.
- For letter-frequency-weighted spawning (used in tile/merge variants), a rough English frequency table by letter is enough — no need for anything more precise.

## UI conventions

- Guess history: one row per past guess, each cell colored by its status. Render top-to-bottom in submission order.
- Current guess (if typed rather than assembled some other way): a row of empty/dashed boxes that fill as letters are entered.
- Color palette: green for `correct`, yellow/gold for `present`, gray for `absent` — these are now a widely recognized convention, don't reinvent them without a reason.
- Show remaining guess count and/or a clear win/loss end state with the secret word revealed on loss.

## Reference implementation

`game/game.js` in this repo (`evaluateGuess`/`submitGuess`) and `game/words.js` for word-list and letter-weight examples.
