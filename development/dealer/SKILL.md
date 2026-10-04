---
name: dealer
description: Use when writing, editing, debugging, or reviewing dealer language code in btn, dlr, or script files. Provides the complete dealer DSL syntax reference for bridge hand generation constraints.
---

# Dealer Language Reference

You are helping write or edit dealer language code for bridge hand generation. Dealer is a DSL that defines constraints on bridge hands so that only hands matching the constraints are produced.

## File Types

- **btn files** (`btn/`): Master scenario files with metadata headers + dealer code + `#include` directives
- **dlr files** (`dlr/`): Extracted dealer code (generated from btn by the pipeline — do NOT edit directly)
- **script files** (`script/`): Reusable dealer code fragments included via `#include "script/NAME"`

Always edit **btn files**, never dlr files directly.

## BTN File Structure

```
# alias: ScenarioName
# button-text: Display Name
# gib-works: true
# bba-works: true
# auction-filter: REGEX_PATTERN
# convention-card-ns: 21GF-DEFAULT
# convention-card-ew: 21GF-GIB

/*@chat
Description text for BBO display.
Use plain regular commas here. Do NOT hand-type wide commas (，) in .btn files.
@chat*/

dealer south|west|north|east

#include "script/TP"
# Defines tpWest, tpNorth, tpEast, tpSouth

# ... dealer constraints ...

produce 30

action
average "label" 100 * variable,
```

## Core Syntax

### Variables and Assignment
```
x = expression
```
Variable names are case-sensitive. No declaration needed.

### Comments
```
# full line comment (must start at column 0 / start of line)
// everything after // is a comment (can appear at end of a line)
/* multi-line comment */
```

**IMPORTANT:** `#` is a comment marker **only at the start of a line**.
Inline / end-of-line comments must use `//`. Writing `x = 5 # comment`
is a syntax error — the parser does not treat `#` as a mid-line
comment marker. (`#include "..."` at the start of a line is the only
non-comment use of `#`.)

### Boolean Operators
```
and    or    not
```

### Comparison Operators
```
==  !=  <  >  <=  >=
```

### Arithmetic
```
+  -  *  /  %
```

### Ternary (Conditional)
```
condition ? value_if_true : value_if_false
```

### Grouping
```
(expression)
```

## Built-in Functions

### Suit Length
```
spades(PLAYER)      # Number of spades (0-13)
hearts(PLAYER)      # Number of hearts (0-13)
diamonds(PLAYER)    # Number of diamonds (0-13)
clubs(PLAYER)       # Number of clubs (0-13)
```
PLAYER is: `north`, `south`, `east`, `west`

### High Card Points
```
hcp(PLAYER)              # Total HCP for hand (A=4, K=3, Q=2, J=1)
hcp(PLAYER, SUIT)        # HCP in a specific suit
```
SUIT is: `spades`, `hearts`, `diamonds`, `clubs`

### Shape Patterns
```
shape(PLAYER, PATTERN)
```
Pattern format: `SHDc` where each position is a digit (exact count) or `x` (any).

Each position is a digit for an exact count, or `x` for any count (0-13).

Examples:
```
shape(south, 4432)           # Exactly 4 spades, 4 hearts, 3 diamonds, 2 clubs
shape(south, 5xxx)           # Exactly 5 spades, any others
shape(south, x5xx)           # Exactly 5 hearts
shape(south, xx44)           # Exactly 4 diamonds, exactly 4 clubs
shape(south, 44xx)           # Exactly 4 spades, exactly 4 hearts
```

To express "4 or more", use suit length functions instead:
```
spades(south)>3              # 4+ spades
spades(south)>3 and hearts(south)>3   # 4+ in both majors
```

Combining patterns with `+` (union) and `-` (exclusion):
```
shape(south, any 4432 + any 4333)           # Any permutation of 4-4-3-2 OR 4-3-3-3
shape(south, any 5xxx - any 55xx)           # 5-card suit but not two 5-card suits
shape(south, any 5332 + any 5422 - 5xxx - x5xx)  # Balanced with 5-card minor
```

The `any` keyword means any permutation of the pattern:
- `any 4432` matches 4432, 4342, 4324, 4243, 3442, etc. (any hand with a 4-4-3-2 distribution)
- `5xxx` without `any` means: exactly 5 spades, any H, any D, any C
- `any 5xxx` means: any suit has exactly 5 cards (with any other distribution)

### Top Honor Counting
```
top2(PLAYER, SUIT)    # Count of A, K in suit (0-2)
top3(PLAYER, SUIT)    # Count of A, K, Q in suit (0-3)
top4(PLAYER, SUIT)    # Count of A, K, Q, J in suit (0-4)
top5(PLAYER, SUIT)    # Count of A, K, Q, J, T in suit (0-5)
```

### Specific Card Check
```
hascard(PLAYER, CARD)
```
CARD format: rank + suit letter. Examples: `AS` (ace of spades), `KH` (king of hearts), `QD`, `JC`, `TD` (ten of diamonds)

### Controls
```
controls(PLAYER)     # A=2, K=1
```

### Losers
```
losers(PLAYER)       # Losing trick count
```

## Control Flow

### The Final Constraint
The last expression in the file (before `produce` / `action`) is the master boolean — only hands where this evaluates to true are produced.

```
# Build up conditions
westOpens and northOvercalls and eastRaises and southDoubles

produce 30
```

### Produce
```
produce N    # Generate N hands (typically 30 for btn, pipeline overrides to 500)
```

### Action Block (Statistics)
```
action
average "LABEL" 100 * booleanVar,    # Percentage of hands where var is true
```
Note: each `average` line except the last ends with a comma.

## Include Directives

```
#include "script/TP"
```
Includes the file at `script/TP`. Common includes:

| Script | Provides |
|--------|----------|
| `script/TP` | `tpNorth`, `tpEast`, `tpSouth`, `tpWest`, `tpNS`, `tpEW` (Total Points = HCP + short-suit points - penalty points) |
| `script/Predict-Opening-1-Bid` | `oS`, `oH`, `oD`, `oC`, `openingSuit` for South |
| `script/Predict-Opening-1-Bid-East` | Same but for East |
| `script/Predict-Response-to-1-Bid` | Response predictions: `nS`, `nH`, `nD`, `nC`, `nN` + auction combos `CD`, `CH`, `CS`, etc. |
| `script/Calm-Opponents` | `calmOpps`, `calmEast`, `calmWest` — opponents who won't interfere |
| `script/GIB-1N` | `gibNT` — predicts South's 1NT opening (15-17) |
| `script/GIB-1N-East` | Same for East |
| `script/Leveling` | Leveling constraints for balanced hand distribution |

## Common Patterns

### Predict Opening Suit (for any player)
```
s = spades(west)
h = hearts(west)
d = diamonds(west)
c = clubs(west)
oS = s>4 and s>=h and s>=d and s>=c
oH = not oS and h>4 and h>=d and h>=c
oD = not (oS or oH) and ((d>3 and d>=c) or c<3)
oC = not (oS or oH or oD)
```

### East's Simple Raise (major suit)
```
eH = oH and hearts(east)==3 and hcp(east,hearts)>1
eS = oS and spades(east)==3 and hcp(east,spades)>1
```

### East's Simple Raise (minor suit)
```
eD = oD and diamonds(east)==4 and hcp(east,diamonds)>2 and spades(east)<4 and hearts(east)<4
eC = oC and clubs(east)==4 and hcp(east,clubs)>3 and spades(east)<4 and hearts(east)<4
```
Minor raises require avoiding negative double shapes (no 4-card major).

### HCP and TP Range Constraints
```
westOpens = hcp(west)>10 and tpWest>11 and hcp(west)<15
northDoubles = tpNorth>11 and hcp(north)<15
```

### Suit Quality
```
goodSuit = spades(south)>4 and top3(south,spades)>1    # 2 of top 3
solidSuit = clubs(south)>6 and top3(south,clubs)==3     # All top 3
```

### GIB Stoppers (from BBO documentation)

GIB classifies stoppers using `length + HCP` (4-3-2-1 count). Dealer code equivalents:

| GIB term | Definition | Example holdings | Dealer code (for spades) |
|----------|-----------|-----------------|--------------------------|
| unstopped | none of the below | xx, xxx | `spades(p) + hcp(p,spades) < 4` |
| partial stop | length+HCP = 4 | Qx, Jxx | `spades(p) + hcp(p,spades) > 3` |
| likely stop | length+HCP ≥ 5 | Kx, Qxx | `spades(p) + hcp(p,spades) > 4` |
| stop | A, QJx, 5+ HCP, or length+HCP ≥ 7 | Ax, Kxx, AJx | `hcp(p,spades) > 4 or spades(p) + hcp(p,spades) > 6` |
| two stops | length+HCP ≥ 8 | Axx, KJx, KQx | `spades(p) + hcp(p,spades) > 7` |

Note: `p` = player (`north`, `south`, etc.). Replace `spades`/`spades` with the target suit.

Example — North has a partial stop or better in each unbid suit (after 1C opening):
```
nStopD = diamonds(north) + hcp(north,diamonds) > 3
nStopH = hearts(north)   + hcp(north,hearts)   > 3
nStopS = spades(north)   + hcp(north,spades)   > 3
```

### GIB Suit Quality (from BBO documentation)

GIB classifies suit quality as follows (useful when modeling what GIB will bid):

| GIB term | Definition | Dealer code approximation |
|----------|-----------|--------------------------|
| 3-card | exactly 3 cards | `spades(p) == 3` |
| 4-card | exactly 4 cards | `spades(p) == 4` |
| biddable | 5+ cards, or 4 cards with 3 of top 5 honors | `spades(p) > 4 or (spades(p) == 4 and top5(p,spades) > 2)` |
| rebiddable | biddable + 1 card | `spades(p) > 5 or (spades(p) == 5 and top5(p,spades) > 2)` |
| solid 6-card | AKQTxx or AKQJxx | `spades(p) > 5 and top4(p,spades) > 2 and top3(p,spades) == 3` |

## Tips for Writing Dealer Code

1. **Start broad, then constrain**: Begin with shape/HCP requirements, then add specific conditions
2. **Predict what BBA will bid**: Model each player's likely action based on standard bidding
3. **Avoid over-constraining**: Too many constraints → low produce rate → slow generation
4. **Use `tpEast<10` or similar caps**: Prevents responder from having too many points (avoids jump raises instead of simple raises)
5. **Minor raises need 4 trumps**: GIB/BBA raises minors with 4+ cards, not 3
6. **Major raises need 3 trumps**: GIB/BBA raises majors with 3 cards
7. **Block negative doubles**: When modeling simple raises, add `spades(east)<4 and hearts(east)<4` for minor raises to prevent East from making a negative double instead
8. **Test with `produce 30`**: Quick iteration; the pipeline overrides to 500 for full runs
9. **Check filter rate**: After running the pipeline, a filter rate above 10% is good; below 5% needs work
