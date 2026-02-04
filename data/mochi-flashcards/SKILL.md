---
name: mochi-flashcards
description: Generate spaced repetition flashcards from learning materials (math, statistics, computational tools). Creates both Q/A and Cloze deletion cards using the Mochi API, with proper LaTeX formatting and syntax. Use when the user provides screenshots or text from educational material and wants flashcards created, or when they mention Mochi, spaced repetition, or flashcard generation.
---

# Mochi Flashcard Generator

Generate high-quality spaced repetition flashcards from learning materials using the Mochi API.

## When to Use This Skill

Use when the user:
- Provides screenshots or text from math, statistics, or computational tool material
- Requests flashcard creation from learning content
- Mentions Mochi, spaced repetition, or flashcard generation
- Wants to create study materials from technical content

## Core Workflow

### Step 1: Analyze the Material

Identify core concepts, definitions, theorems, or formulas from the provided material.

### Step 2: Determine the Deck

Select the appropriate deck:
- **Math Academy** (`AqFHmdTB`): Statistics, mathematics, quantitative methods
- **Vim** (`pci82xXE`): Vim commands, key bindings, editor operations
- If unclear, ask the user

### Step 3: Create Cards

For each concept, generate BOTH:
1. **Q/A card**: Traditional two-sided flashcard
2. **Cloze card**: Fill-in-the-blank style card

### Step 4: Execute API Calls

Use Desktop Commander MCP tools (not bash_tool) to create cards via the Mochi API.

## API Configuration

- **Base URL**: `https://app.mochi.cards/api/cards/`
- **Authentication**: `-u "71ccfe08d853d6b100001995:"`
- **Method**: POST
- **Content-Type**: `application/json`

## Card Format Rules

### Q/A Cards (Two-Sided)

Separate question and answer with three dashes on its own line:

```json
{
  "content": "Question text\n---\nAnswer text",
  "deck-id": "AqFHmdTB",
  "manual-tags": ["tag1", "tag2"]
}
```

### Cloze Deletion Cards

Hide keywords with double braces:

```json
{
  "content": "The {{keyword}} will be hidden.",
  "deck-id": "AqFHmdTB",
  "manual-tags": ["tag1"]
}
```

For grouped cloze (separate review cards):

```json
{
  "content": "The {{1::first item}} and {{2::second item}} create separate cards.",
  "deck-id": "AqFHmdTB"
}
```

## CRITICAL: LaTeX + Cloze Syntax

**The `{{` braces MUST be OUTSIDE the `$` or `$$` delimiters**

### ❌ WRONG
```
$x = {{y}}$                  // Will not render
$$\int {{f(x)}} dx$$         // Will break
```

### ✅ CORRECT
```
$x =${{$y$}}                 // Braces outside $
$$\int$$ {{$$f(x)$$}} $$dx$$ // Braces outside $$
{{$\mu$}}                    // Entire expression in braces
```

## Example API Calls

### Statistics Q/A Card

```bash
curl -X POST https://app.mochi.cards/api/cards/ \
  -u "71ccfe08d853d6b100001995:" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is the Central Limit Theorem?\n---\nAs sample size increases, the distribution of sample means approaches a normal distribution, regardless of the population distribution.",
    "deck-id": "AqFHmdTB",
    "manual-tags": ["statistics", "inference", "clt"]
  }'
```

### Statistics Cloze with LaTeX

```bash
curl -X POST https://app.mochi.cards/api/cards/ \
  -u "71ccfe08d853d6b100001995:" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The standard error of the mean is {{$\\sigma / \\sqrt{n}$}} where $\\sigma$ is population standard deviation.",
    "deck-id": "AqFHmdTB",
    "manual-tags": ["statistics", "standard-error"]
  }'
```

### Vim Command Card

```bash
curl -X POST https://app.mochi.cards/api/cards/ \
  -u "71ccfe08d853d6b100001995:" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What does `ciw` do in Vim?\n---\nChanges (deletes and enters insert mode) the inner word under the cursor.",
    "deck-id": "pci82xXE",
    "manual-tags": ["vim", "editing", "text-objects"]
  }'
```

## Tagging Guidelines

Use 2-4 lowercase tags per card:

**Statistics/Math**:
- `["statistics", "inference", "hypothesis-testing"]`
- `["probability", "distributions"]`
- `["linear-algebra", "matrices"]`

**Vim**:
- `["vim", "motion", "navigation"]`
- `["vim", "editing", "deletion"]`
- `["vim", "visual-mode"]`

## Quality Standards

- Keep Q/A answers concise (1-3 sentences)
- Hide only essential keywords in cloze cards
- Use LaTeX for all mathematical notation
- No headers (#) at start of cards
- Use proper technical terminology
- Include sufficient context for standalone understanding

## Response Format

After creating cards, provide:

```
✅ Created [N] flashcards:

Math Academy:
- [N] Q/A cards: [topics]
- [N] Cloze cards: [topics]

[Vim: ...]

Cards added to Mochi and ready for review.
```

## Additional Details

For comprehensive API documentation, syntax examples, and advanced features, see [references/api_reference.md](references/api_reference.md).
