---
name: language-agnostic-puzzle-designer
description: Design escape room puzzles that work across languages and cultures using visual logic, mathematical deduction, spatial reasoning, and pattern recognition. Creates puzzles for global audiences without language barriers. Use when designing puzzles for international markets, multilingual games, or culturally-neutral gameplay experiences.
---

# Language-Agnostic Puzzle Designer

## Overview

Create puzzles that transcend language barriers using visual logic, patterns, mathematics, and spatial reasoning—enabling escape rooms to reach global markets without translation bottlenecks.

## Why Language-Agnostic Design?

**Global Market Access**:
- English, Korean, Japanese markets simultaneously
- No translation delays or costs
- Consistent difficulty across cultures

**Best Practice**: 50-70% language-agnostic puzzles + 30-50% simple text puzzles (easily translatable)

## Puzzle Type Taxonomy

### Type A: Mathematical Deduction (20-30% of puzzles)

**1. Cipher Puzzles**
```
Example: Number-to-Letter Cipher
Message: 8-5-12-12-15
Hint: A=1, B=2, C=3...
Answer: HELLO

Notion Implementation:
- Display number sequence in text block
- Hint in Toggle block
- Answer check via Database property
```

**2. Numeric Sequences**
```
Example: Pattern Completion
Sequence: 2, 4, 8, 16, ?
Pattern: Each number doubles
Answer: 32

Variations:
- Fibonacci: 1, 1, 2, 3, 5, 8, ?
- Prime numbers: 2, 3, 5, 7, 11, ?
- Arithmetic: 5, 10, 15, 20, ?
```

**3. Sudoku Variations**
```
Standard 9x9 OR
Themed variations:
- 4x4 Mini-sudoku (easier)
- Symbol Sudoku (shapes instead of numbers)
- Color Sudoku (colored cells)

Notion Implementation:
- Create table with emoji/numbers
- Player fills in missing cells
- Correct answer unlocks next scene
```

### Type B: Spatial Reasoning (30-40% of puzzles)

**1. Nonogram (Paint by Numbers)**
```
    1 2 1
  ┌─────┐
1 │█░█│
2 │██░│
1 │░█░│
  └─────┘

Creates: Heart shape ❤

Notion Implementation:
- Provide number clues
- Player sketches solution
- Image reveal validates answer
```

**2. Maze Navigation**
```
Start → Multiple paths → Dead ends → Exit

Notion Implementation:
├─ Page: "North Corridor"
│  ├─ [Toggle] Go Left → Dead end
│  └─ [Toggle] Go Right → Continue
└─ Page: "Success! Exit found"
```

**3. Tangram / Spatial Puzzles**
```
Given: 7 geometric pieces
Task: Recreate specific shape
Difficulty: Silhouette only (hard) vs. Outlined pieces (easy)

Notion Implementation:
- Provide piece images
- Show target silhouette
- Answer: Describe final arrangement
```

**4. Map/Grid Puzzles**
```
Example: Coordinate Treasure Map
Clue: "X marks the spot: C-4"
Grid:
   A  B  C  D
1  🌊 🌊 🌳 🌳
2  🌳 🏔️ 🌊 🌊
3  🌊 🌳 🌳 🏔️
4  🌳 🌊 💎 🌳

Answer: C-4 contains 💎
```

### Type C: Visual Logic (40-50% of puzzles)

**1. Pattern Recognition**
```
Example: Identify the pattern
🔴 🔵 🔴 🔵 🔴 ?
Answer: 🔵

Advanced:
🔺 🔻 🔺 🔺 🔻 🔺 🔺 🔺 ?
Pattern: Fibonacci in shapes
Answer: 🔻
```

**2. Spot the Difference**
```
Image A: 🏠🌳🚗🐕🌸
Image B: 🏠🌳🚗🐈🌸
Difference: Dog → Cat (position 4)

Use for: Hidden clue in modified image
Notion: Side-by-side images, answer validates next unlock
```

**3. Image-Based Codes**
```
Example: Color Code
Image shows: 🟥🟢🟦🟡
Color order: Red=1, Green=2, Blue=3, Yellow=4
Password: 1234

Example: Symbol Matching
⚡→ 5, ❤→ 9, ★→ 2
Code: ⚡❤★ = 592
```

**4. Shadow/Silhouette Matching**
```
Show silhouette → Match to object
🔪 (knife shadow) → Kitchen
🔧 (wrench shadow) → Garage
🎨 (palette shadow) → Art room

Determines: Which room to search next
```

### Type D: Time/Sequence Puzzles (10-20% of puzzles)

**1. Clock Arithmetic**
```
Example: Time-based code
"When the big hand points to 12 and small hand to 3"
Answer: 3:00 or 15:00
Derived code: 1500 or 300
```

**2. Calendar Puzzles**
```
Example: "Red dates on calendar"
February: 14 (Valentine's), March: 1 (Independence Day)
Code: 0214 or 0301

Universal holidays work globally:
- New Year: 0101
- Specific month patterns
```

### Type E: Interactive/Observation (10-20% of puzzles)

**1. Hidden Object**
```
Large detailed image with:
- 5 keys hidden in scene
- Zoom in to find them
- Each key unlocks a clue

Notion: High-res image, player reports locations
```

**2. Sequence Memory**
```
Example: Simon Says
Pattern shown: 🔴🟢🔵🔴
Player repeats: [Input sequence]
Correct → Next level (harder sequence)

Notion Implementation:
- Show pattern in Toggle (hidden after view)
- Player inputs from memory
- Formula validates answer
```

## Difficulty Calibration

### Easy Puzzles (Starter, 20% success on first try)
- Single-step logic
- Clear visual cues
- 2-4 element patterns
- Immediate hint available

**Example**:
```
Pattern: 🌙⭐🌙⭐🌙?
Answer: ⭐
Difficulty: ⭐☆☆☆☆
```

### Medium Puzzles (Core, 60-70% success with 1-2 hints)
- Two-step deduction
- Hidden pattern in visual noise
- 5-8 elements
- Hint after 2 attempts

**Example**:
```
Grid:
R B R
B R B
R B ?

Pattern: Checkerboard
Answer: R (Red)
Difficulty: ⭐⭐⭐☆☆
```

### Hard Puzzles (Challenge, 30-40% success with hints)
- Multi-step reasoning
- Combination of puzzle types
- 10+ elements
- Requires connecting multiple clues

**Example**:
```
Combine: Color code + Number sequence + Spatial
Red shapes = 1, Blue shapes = 2
Count shapes in grid: 3 Red, 2 Blue, 4 Red
Code: 324
Difficulty: ⭐⭐⭐⭐☆
```

## Design Workflow

Copy this checklist:

```
Puzzle Design Progress:
- [ ] Step 1: Determine puzzle purpose (5 min)
- [ ] Step 2: Choose puzzle type (3 min)
- [ ] Step 3: Set difficulty level (2 min)
- [ ] Step 4: Create puzzle mechanics (15 min)
- [ ] Step 5: Design 3-level hint system (10 min)
- [ ] Step 6: Test with 3 people (30 min)
- [ ] Step 7: Adjust based on feedback (15 min)
```

### Step 1: Determine Purpose

Answer:
- **Narrative**: What story does this puzzle advance?
- **Pacing**: Early game (easy) or late game (hard)?
- **Unlock**: What does solving this reveal/unlock?

### Step 2: Choose Type

Decision tree:
```
Need pure logic? → Type A (Math)
Need spatial thinking? → Type B (Spatial)
Need observation? → Type C (Visual)
Need time pressure? → Type D (Sequence)
Need exploration? → Type E (Interactive)
```

### Step 3: Set Difficulty

Target distribution (for 15-puzzle game):
- 3 Easy (20%)
- 9 Medium (60%)
- 3 Hard (20%)

Place hard puzzles at 60-80% mark (not at end—allow breathing room for finale).

### Step 4: Create Mechanics

Use templates from references/puzzle-library.md

**Checklist**:
- ✅ Solution has single correct answer
- ✅ No cultural knowledge required
- ✅ Can be solved without text (or minimal text)
- ✅ Validates to specific unlock code/action
- ✅ Failure is obvious (player knows they're wrong)

### Step 5: Design Hints

**3-Level Hint System**:

**Hint 1 (Direction)**: Points player to right area
```
Puzzle: Decode number sequence
Hint 1: "Look at the pattern between numbers"
```

**Hint 2 (Method)**: Explains approach
```
Hint 2: "Each number is double the previous number"
```

**Hint 3 (Solution)**: Nearly gives answer
```
Hint 3: "The pattern is: multiply by 2 each time. What's 16 × 2?"
```

### Step 6: Test

**Alpha Test** (3 people):
- Can they solve WITHOUT hints? → Easy
- Can they solve WITH Hint 1-2? → Medium
- Need Hint 3 or still stuck? → Hard

**Metrics**:
- < 2 minutes: Too easy
- 2-5 minutes: Perfect
- 5-10 minutes: Challenging
- > 10 minutes: Too hard (or add hints)

### Step 7: Adjust

Common fixes:
- Too hard → Add visual cues, simplify pattern
- Too easy → Add noise elements, increase steps
- Unclear → Better hint progression
- Frustrating → Make failure feedback clearer

## Notion Implementation Patterns

### Pattern 1: Simple Validation

```
[Database: Puzzles]
Property: Player Answer (Text)
Formula: if(prop("Player Answer") == "HELLO", "✅ Correct! Next clue...", "❌ Try again")
```

### Pattern 2: Multi-Step Validation

```
Puzzle requires: Color + Number + Symbol

[Database Properties]
- Color Guess (Select: Red/Blue/Green)
- Number Guess (Number)
- Symbol Guess (Text)

Formula:
if(
  and(
    prop("Color Guess") == "Red",
    prop("Number Guess") == 7,
    prop("Symbol Guess") == "Star"
  ),
  "✅ Safe opened!",
  "❌ Combination incorrect"
)
```

### Pattern 3: Hint Trigger System

```
Attempts Property (Number) ← Player increments manually

Hint Display (Formula):
if(prop("Attempts") >= 3,
  "💡 Hint 1: " + prop("Hint 1"),
  if(prop("Attempts") >= 5,
    "💡 Hint 2: " + prop("Hint 2"),
    if(prop("Attempts") >= 7,
      "💡 Hint 3: " + prop("Hint 3"),
      ""
    )
  )
)
```

## Language Mix Strategy

**Recommended Distribution**:
```
Total 15 puzzles:
├─ 10 puzzles (67%): Language-agnostic
│   ├─ 3 Visual logic
│   ├─ 3 Math/cipher
│   ├─ 2 Spatial
│   └─ 2 Pattern
│
└─ 5 puzzles (33%): Simple text
    ├─ 3 Easy word puzzles (translatable)
    ├─ 1 Story clue (narrative)
    └─ 1 Character dialogue
```

**Translation Strategy for Text Puzzles**:
- Use simple vocabulary (A1-A2 level)
- Avoid idioms, slang, cultural references
- Keep sentences < 10 words
- Provide visual context

## Anti-Patterns to Avoid

❌ **Language-Specific**
- Word puns (don't work in translation)
- Rhyming clues (language-specific)
- Cultural trivia (Korea-only knowledge)

❌ **Frustration Traps**
- Pixel-hunting (tiny hidden objects)
- Guess-and-check without logic
- Red herrings that seem like real clues

❌ **Accessibility Issues**
- Color-blindness dependence (red/green only)
- Tiny text (mobile users)
- Sound-only puzzles (deaf users)

✅ **Instead**: Provide alternative paths or redundant clues

## Resources

### references/
- `puzzle-library.md` - 50+ tested puzzle templates
- `difficulty-formulas.md` - Mathematical difficulty calculation
- `cultural-pitfalls.md` - What to avoid by culture

### assets/
- `puzzle-images/` - Reusable visual puzzle graphics
- `templates/` - Fill-in-the-blank puzzle worksheets

## Example Application

**User**: "Create 3 puzzles for Act 2 (medium difficulty)"

**Output**:
```
Puzzle 1: Mathematical Deduction (Visual Cipher)
- Type: Number-to-symbol mapping
- Office has 4 doors: 🚪🔑🚪❌🚪🌟🚪🔓
- Clue: "Key = 1, Lock = 4, Star = 3, X = 2"
- Question: "Which door code?"
- Answer: 1432 or 4231 (depending on order)
- Difficulty: ⭐⭐⭐☆☆
- Time estimate: 3-4 min
- Hints:
  1. "Count the symbols"
  2. "Match each symbol to its number"
  3. "Read left to right: Key(1), X(2), Star(3), Lock(4) = 1234"

Puzzle 2: Spatial Reasoning (Map Grid)
- Type: Coordinate matching
- Grid shows office floor plan (A-E, 1-5)
- Clue: "Meeting Room = C3, Server Room = ?"
- Visual: Map shows server room location
- Answer: D2
- Difficulty: ⭐⭐⭐☆☆
- Time estimate: 2-3 min

Puzzle 3: Visual Logic (Pattern)
- Type: Color sequence
- Security cameras blink: 🔴🔵🔴🔵🔴🔵🔴?
- Question: "Next color?"
- Answer: 🔵 (Blue)
- Then ask: "How many times total?" → 8
- Password: BLUE8 or just 8
- Difficulty: ⭐⭐☆☆☆
- Time estimate: 2 min
```

All 3 puzzles work in any language, require visual observation and pattern recognition, and integrate with office mystery narrative.
