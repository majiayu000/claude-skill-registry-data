---
name: zero-day-rules
description: This skill should be used when the user asks about "game rules", "scoring", "phases", "Attack token", "Exploit token", "Ghost token", "tile placement rules", "path matching", "movement rules", "winning conditions", "turn actions", "firewall breach", "path segments", "edge nodes", or discusses Zero-Day Attack game mechanics and design.
version: 0.3.0
---

# Zero-Day Attack Game Rules

Expert knowledge of Zero-Day Attack game mechanics, rules, and design for the digital implementation targeting Board hardware.

## Game Overview

Zero-Day Attack is a two-player asymmetric tile-laying strategy game with a hacking theme. Players compete to breach firewalls, plant exploits, and escape detection.

### Core Concept

- **Theme**: Elite hackers breaching each other's networks
- **Players**: 2 (Red and Blue)
- **Objective**: Place tiles to reach the board edge, mark the breach, then retreat as far as possible
- **Victory**: Most path segments of player's color between Exploit and Ghost tokens

## Game Phases

### Phase 1: Attack

Move Attack token toward the firewall (board edge) by placing tiles and moving along valid paths.

**Goal**: Reach any edge node on the board boundary.

### Midpoint: Exploit

When Attack token reaches firewall:

1. Replace Attack token with Exploit token (automatic, no action cost)
2. Exploit token remains at this location permanently
3. Continue with remaining actions if any

### Phase 2: Ghost

Move Ghost token away from the Exploit position.

**First move after Exploit**:

1. Place Ghost token at Exploit location
2. Move Ghost away in the same Move action

**Goal**: Maximize distance (path segments) between Exploit and Ghost.

## Board Layout

### Digital Implementation (Board SDK)

Target display: 1920×1080 pixels (landscape, 16:9)

### Horizontal Layout

```text
┌────────┬──────────┬────────────────────────────┬──────────┬────────┐
│Blue UI │ Blue Res │       5×5 PLAYABLE GRID    │ Red Res  │ Red UI │
│        │ (5 tiles)│    Purple "Firewall"       │ (5 tiles)│        │
│        │          │    Center tile pre-placed  │          │        │
└────────┴──────────┴────────────────────────────┴──────────┴────────┘
← Blue player sits here                      Red player sits here →
```

- **Reserve Pools**: Left (Blue) and Right (Red) for drawn tiles - visible to both players
- **Playable Grid**: 5×5 center area for tile placement
- **Firewall**: Purple border - reaching it completes Phase 1
- **Starting Tile**: Center position [2,2] with game-tile-13-center

### Player Orientation

- **Blue player**: Views from LEFT side
- **Red player**: Views from RIGHT side

## Tile System

### Properties

- **Quantity**: 25 total (1 starting + 24 placeable)
- **Size**: 200×200 units (2.0 world units at 100 PPU)
- **Edge Nodes**: 4 per tile (Top, Right, Bottom, Left midpoints)

### Path Segments

**By Shape**:

- **Quarter-curve**: Connects adjacent nodes (90° apart) - e.g., Left→Top
- **Straight line**: Connects opposite nodes (180° apart) - e.g., Left→Right

**By Color**:

| Color  | Hex       | Who Can Traverse |
| ------ | --------- | ---------------- |
| Red    | `#FF2244` | Red player only  |
| Blue   | `#44BBFF` | Blue player only |
| Purple | `#BB88FF` | Either player    |

### Path Matching Rules

At connecting edges:

- Red ↔ Red: Valid
- Blue ↔ Blue: Valid
- Purple ↔ Any: Valid
- Red ↔ Blue (exclusively): **Invalid**

Once placed, tiles cannot be moved, removed, or rotated.

## Token System

### Three Tokens Per Player

| Token       | Design                        | Phase    | Purpose                 |
| ----------- | ----------------------------- | -------- | ----------------------- |
| **Attack**  | Filled target with crosshair  | Phase 1  | Navigate to firewall    |
| **Exploit** | Hollow rings, faint crosshair | Midpoint | Mark breach permanently |
| **Ghost**   | Gradient opacity circles      | Phase 2  | Retreat from breach     |

### Token Rules

- Always reside on edge nodes (never inside tiles)
- Edge node must include path of player's color OR purple
- Both players' tokens may occupy same node
- Tokens do not block each other

## Action System

### Turn Structure

Each turn: **Two Single Actions** OR **One Double Action**

### Single Actions

| Action      | Description                  | Restrictions                          |
| ----------- | ---------------------------- | ------------------------------------- |
| **Draw**    | Take top tile from deck      | None                                  |
| **Discard** | Remove tile from reserve     | Only after deck empty                 |
| **Steal**   | Take from opponent's reserve | Max 2/turn; opponent can steal 1 back |
| **Place**   | Place tile at token's edge   | Must connect to token position        |
| **Move**    | Move along valid paths       | Color continuity rules                |

### Double Action: Place

- Place tile on any empty space adjacent to token's tile
- Can connect to any side (not just token's edge)
- Consumes entire turn

### Movement Rules

1. **Color Restriction**: Only traverse own color OR purple
2. **Single Color Per Move**: Stay on one color within a Move action
3. **Color Junction**: At nodes where both colors continue:
   - Continue on current color, OR
   - End Move action, then use another Move to switch
4. **Path Length**: Unlimited distance along continuous same-color path
5. **Non-blocking**: Opponent tokens don't block

## Game End and Scoring

### End Trigger (in sequence)

1. Deck is empty
2. One player ends turn with no tiles in reserve
3. Other player takes final turn

### Scoring

1. Find path between Exploit and Ghost tokens
2. Count segments of player's OWN color (not purple)
3. Each quarter-curve or straight line = 1 segment
4. **Most segments wins**

### Tiebreaker

If tied, player with most **purple** segments wins.

## Setup Sequence

1. Determine first player and colors
2. Seat by color (Blue on left side, Red on right side)
3. Place Attack tokens on starting tile's matching color nodes
4. Each player draws 5 tiles
5. **First player**: Place 1 tile adjacent to center, keep 3 in reserve, shuffle 1 back
6. **Second player**: Same as first
7. Both flip reserve tiles face-up

## Digital Implementation Notes

### Validation Requirements

- **Tile Placement**: Validate color matching at all connecting edges
- **Movement**: Enforce single-color continuity per Move action
- **Token Position**: Ensure edge node has valid path color

### Phase Transitions

- Attack→Exploit: Automatic when Attack reaches firewall edge
- Exploit→Ghost: First Move action after Exploit placement

## Additional Resources

### Reference Files

This skill's `references/` folder contains:

| File                 | Content                                 |
| -------------------- | --------------------------------------- |
| `complete-rules.md`  | Full original rules with diagrams       |
| `diagrams/`          | 19 SVG diagrams for rules visualization |
| `phase-mechanics.md` | Attack→Exploit→Ghost transitions        |
| `tile-system.md`     | 25 tiles, edge nodes, path segments     |
| `token-system.md`    | 3 tokens per player, placement rules    |
| `action-system.md`   | Draw, Discard, Steal, Place, Move       |
| `scoring-endgame.md` | Win conditions, path counting           |

> **Important**: The official rulebook describes the original physical game with a **portrait orientation** (Blue at top, Red at bottom). The digital Board SDK implementation uses **landscape orientation** (Blue on left, Red on right) to fit the 1920×1080 display. Game mechanics are identical; only the physical layout differs.

### Key Algorithms

- Placement validation (color matching at edges)
- Movement validation (path continuity)
- Score calculation (path finding between tokens)

Request consultation from the `code-architecht` subagent or the `project-architecture` skill for C# code examples of these algorithms.
