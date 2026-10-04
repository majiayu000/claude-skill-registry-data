---
name: game-balance
description: Analyses whether mechanics are fair — attack strength, combo scaling, piece distribution, comeback, first-player advantage, snowball, match duration, skill vs RNG. Prefers simulation to opinion.
---

# game-balance

## Purpose

Answer balance questions with **data**, not argument.

> Use simulation wherever possible rather than subjective judgement.

## When to invoke

- Any change to attack tables, defence thresholds, combo scaling or piece distribution
- Whenever someone says a mechanic "feels" too strong or too weak
- Before shipping any battle mechanic
- When match outcomes seem arbitrary

## Responsibilities

Attack strength · combo scaling · piece distribution · comeback mechanics · first-player
advantage · snowball effects · match duration · skill vs RNG.

## The measurement that matters most

**Skill vs RNG separation.** Pair a strong AI against a weak one and measure how reliably skill
wins.

If a clearly better player wins only ~55% of matches, the game is a coin flip wearing a strategy
costume — and no amount of visual polish, content or marketing fixes that. Run this against every
candidate configuration; it is the single number that says whether the competitive premise holds.

## The metric set

| Metric | Question |
|---|---|
| Match duration distribution | are matches the right length? |
| Lead volatility over time | does it stay tense, or get decided early? |
| Comeback frequency | can a losing player recover? |
| Snowball index | does an early lead compound? |
| First-clear advantage | is there a systematic first-mover edge? |
| Attack frequency, defence success | is the combat loop engaging? |
| Decisiveness | how often does the result feel arbitrary? |
| **Skill vs RNG separation** | **does the better player win?** |

## Process

1. Turn the question into a **measurable hypothesis** before running anything.
2. Sweep the relevant configuration across thousands of headless matches.
3. Pair AI players at several skill levels — balance can behave very differently at different
   skill ranges, and a change that helps novices can ruin the top of the ladder.
4. Report with the seeds to reproduce.
5. Recommend a configuration change, or **no change**. "The current numbers are fine" is a
   valid and common result.

## Constraints

- Fully headless. A balance question that requires a human playing is a question you can only
  afford to ask twice.
- Every reported result comes with reproduction seeds.
- Balance changes are **configuration only**. If a change needs code, the rules schema is wrong —
  raise it with `game-rules-engine`.
- Fast enough that a question is answered in minutes, or it won't get asked.
- Simulation complements playtesting; it does not replace it. Numbers cannot tell you whether a
  mechanic is *fun*.

## Watch for

- **Snowball.** The most common failure in attack-based competitive puzzles: an early lead
  compounds into an inevitable win, and the loser spends two minutes knowing they've lost.
- **Comeback mechanics that remove agency.** Rubber-banding that hands a losing player a win
  they didn't earn is worse than the snowball it fixes.
- **Speed beating thought** (especially in Variant A) — if raw placement rate dominates good
  placement, this stops being a thinking game.

## Outputs

- A configuration recommendation with data and reproduction seeds
- A written verdict on whether the mechanic passes

## Definition of done

The question was measurable, the sweep ran at scale across skill levels, the results reproduce
from seeds, and the recommendation follows from the data rather than from taste.

## Consults

`battle-system` (mechanics under test) · `game-ai` (simulation players) ·
`piece-generator` (distributions) · `game-rules-engine` (configurability)
