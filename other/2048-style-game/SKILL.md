---
name: 2048-style-game
description: Build a 2048-style slide-and-merge tile game on a fixed grid — generic slide/merge algorithm (works for numbers, letters, or any comparable value), weighted tile spawning, and game-over detection. Use when asked to build 2048, a sliding-tile puzzle, or any game where matching tiles merge on swipe/arrow-key input.
---

# 2048-style slide-and-merge game

## Grid representation

A `SIZE x SIZE` 2D array (`grid[row][col]`), cells are `null` (empty) or a value (number, letter, whatever the game merges). Classic 2048 is 4x4.

## The line-based slide algorithm

Every direction (left/right/up/down) reduces to the same operation applied to 1D "lines" extracted from the grid, so you only need to write the merge logic once.

```js
// Extract row `index` (left/right) or column `index` (up/down) as a flat
// array, oriented so "toward index 0" always means "the direction we're sliding".
function getLine(dir, index) {
  const line = [];
  for (let k = 0; k < SIZE; k++) {
    line.push(dir === "left" || dir === "right" ? grid[index][k] : grid[k][index]);
  }
  if (dir === "right" || dir === "down") line.reverse();
  return line;
}

function setLine(dir, index, line) {
  const ordered = dir === "right" || dir === "down" ? [...line].reverse() : line;
  for (let k = 0; k < SIZE; k++) {
    if (dir === "left" || dir === "right") grid[index][k] = ordered[k];
    else grid[k][index] = ordered[k];
  }
}

// Compact + merge one line toward index 0. Each tile merges at most once
// per move (classic 2048 rule — prevents 2,2,2,2 from collapsing to one 8).
function slideLine(line) {
  const tiles = line.filter((v) => v !== null);
  const merged = [];
  const merges = [];
  let i = 0;
  while (i < tiles.length) {
    if (i + 1 < tiles.length && tiles[i] === tiles[i + 1]) {
      merged.push(mergeValue(tiles[i])); // numbers: tiles[i]*2. Letters/other: tiles[i] unchanged.
      merges.push(tiles[i]);
      i += 2;
    } else {
      merged.push(tiles[i]);
      i += 1;
    }
  }
  while (merged.length < SIZE) merged.push(null);
  return { line: merged, merges };
}
```

Driving a move: run `slideLine` over all `SIZE` lines for the given direction, track whether *anything* changed (compare before/after per line — don't just check `merges.length`, a slide with no merges still counts as a move), and only spawn a new tile / advance turn state if something actually moved. Skipping this check causes an infinite tile pile-up on a no-op keypress.

## Spawning tiles

- Spawn into a uniformly random *empty* cell after each valid move.
- Weight *which* value spawns — don't spawn uniformly over every possible value if the value space is large (see "Balance" below).

## Game over detection

Board is stuck when there are no empty cells *and* no direction would produce a merge or shift. Cheapest correct check: run the same `slideLine` logic for all 4 directions against the *current* grid and see if any line would change — no need for a separate adjacency check.

```js
function canAnyLineMove() {
  for (const dir of ["left", "right", "up", "down"]) {
    for (let index = 0; index < SIZE; index++) {
      const before = getLine(dir, index);
      const { line: after } = slideLine(before);
      if (JSON.stringify(before) !== JSON.stringify(after)) return true;
    }
  }
  return false;
}
```

## Balance: keep the value space small relative to the board

This is the single biggest thing that makes or breaks a 2048-style game. Classic 2048 works because there are effectively only 2-3 *live* spawn values (2 and 4) at any time — so two random tiles are very likely to be mergeable, which is what lets the board sustain long play through cascading merges.

If you generalize the merge value beyond numbers (letters, colors, symbols...) and spawn from a large space (e.g. all 26 letters), most tiles become singletons that can *never* merge. The board fills in `~cell_count` moves and locks up almost immediately, regardless of player skill — this isn't a difficulty problem, it's a broken game. Fix it by keeping the total number of distinct spawnable values small (roughly board-size-dependent; for a 4x4/16-cell board, single digits of distinct values keeps merges frequent) — bias spawns toward a deliberately small pool rather than the full value space.

**Verify this with a scripted playtest, not by eyeballing.** Drive the game with a script that repeatedly picks the direction producing the most merges (or a fixed direction preference like classic "always try down, then left" 2048 strategy) and log how many moves survive before lockup and how far the game got. If a reasonable bot dies in ~15-20 moves on a 16-cell board, the value space is too large — narrow it before shipping.

## Controls

- Keyboard: arrow keys and WASD, `preventDefault()` on the keydown so the page doesn't scroll.
- Touch: track `touchstart`/`touchend` coordinates, compare `dx`/`dy` deltas with a minimum-distance threshold (~24px) to avoid firing on taps, pick the dominant axis.
- On mobile, also add visible on-screen direction buttons — swipe alone is not reliably discoverable or trustworthy across all embedding contexts (see the hybrid skill for a concrete example where swipe wasn't enough).

## Reference implementation

`game/game.js` in this repo (`getLine`/`setLine`/`slideLine`/`move`/`canAnyLineMove`).
