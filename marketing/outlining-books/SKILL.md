---
name: "Outlining books"
description: "Creates outlines for non-fiction books and long articles. Use when user says 'create an outline', 'plan a book', 'structure a book about [topic]', or 'I want to write about [topic]'. Handles leadership, career, how-to, and thought leadership content."
---

# Outlining Books

Creates structured outlines with theme statements and chapter plans for non-fiction professional development content.

## When to use this skill

- User wants to write a book or long article
- User asks to "create an outline" or "plan a book"
- User mentions topics like leadership, career development, expertise, or thought leadership
- User has ideas but needs structure

## What this skill does

1. Identifies the book's core theme
2. Defines target audience and transformation goal
3. Creates chapter structure with clear purposes
4. Maps how each chapter serves the theme
5. Outputs `outline.md` file
6. Git commits the outline

## Required information

Ask user for:
- **Genre**: Leadership, how-to, career, thought leadership, or other
- **Topic**: What is this about?
- **Audience**: Who is this for? (Be specific: "first-time managers" not "managers")
- **Transformation**: What will readers know/do/believe after reading?
- **Length**: Target word count or page count

## Process

### Step 1: Extract theme

Create one sentence capturing the book's purpose.

**Good themes are:**
- Specific: "Leaders must build trust through radical transparency" > "Leadership is important"
- Testable: Can you check each chapter against it?
- Audience-aware: Resonates with target readers

**Bad themes:**
- Too generic: "How to be successful"
- Too narrow: "The 7-step process for X" (that's a chapter, not a theme)
- Vague: "Insights on leadership"

### Step 2: Propose chapter structure

Based on genre and typical patterns:

**Leadership/management books** → Framework-driven (5-8 chapters)
- Establish problem → Framework components → Application → Transformation

**How-to books** → Process-driven (6-10 chapters)
- Foundation → Steps in sequence → Advanced techniques → Troubleshooting

**Career books** → Journey-driven (7-10 chapters)
- Where you are → Challenges → Skills/mindsets → Actions → Future state

**Thought leadership** → Argument-driven (5-7 chapters)
- Current state → Why change needed → New model → Evidence → Implications → Call to action

Calculate target word count per chapter: `total_length / number_of_chapters`

### Step 3: Create outline.md

```markdown
# [Book Title]

## Theme Statement
[One sentence capturing core purpose]

## Target Audience & Transformation
- **Audience**: [specific description]
- **Transformation**: [what readers gain]
- **Total Target Length**: [word count]

## Chapter Structure

### Chapter 1: [Title]
- **Purpose**: [How this serves the theme - one sentence]
- **Key Points**: 
  - [Point 1]
  - [Point 2]
  - [Point 3]
- **Target Word Count**: [~X words]
- **Status**: not started
- **Theme Alignment**: [How this connects to theme]

[Repeat for all chapters]

## Chapter Alignment Map
- Chapter 1 → establishes [concept]
- Chapter 2 → builds by [action]
- Chapter 3 → deepens with [insight]
[etc.]

## Metadata
- **Genre**: [as specified]
- **Created**: [date]
```

### Step 4: Review with user

Present outline and ask:
- Does the theme feel right?
- Do the chapters make sense?
- Is anything missing or out of order?

Iterate until user approves.

### Step 5: Git commit

```bash
git add outline.md
git commit -m "Initial outline: [Book Title]"
```

## Examples

### Example 1: Leadership book

**User input:**
"I want to write a book about building high-trust teams for mid-level managers."

**Response:**
"Let me create an outline for you. First, a few quick questions:
- Target length? (thinking 40,000-50,000 words for a leadership book)
- What should managers be able to do after reading this?
- Any specific frameworks or experiences you want to include?"

[After gathering info, create outline with 7 chapters focused on trust-building]

### Example 2: How-to book

**User input:**
"Create an outline for a book teaching developers how to write technical documentation."

**Response:**
"Great topic. Before I outline this:
- What level of developer? (Junior, mid-level, senior?)
- What's the main transformation? (From 'avoiding docs' to 'writing clear docs'?)
- Target length?
- Any specific documentation types to cover (API docs, README files, etc.)?"

## Voice profile (optional)

If user provides sample writing, create `voice-profile.md`:

```markdown
# Voice Profile

Analyzed: [description of sample]

## Sentence Structure
- Length: [short/medium/long/mixed]
- Complexity: [simple/compound/complex/varied]

## Tone
- Formality: [conversational/professional/academic]
- Perspective: [first/second/third person]

## Techniques
- Examples: [frequent/occasional/rare]
- Metaphors: [frequent/occasional/rare]
- Data: [data-driven/balanced/story-driven]
- Personal stories: [frequent/occasional/rare]

## Technical
- Jargon: [heavy/balanced/plain language]
- Depth: [deep/balanced/accessible]
```

Then git commit:
```bash
git add voice-profile.md
git commit -m "Add voice profile"
```

## Edge cases

**User doesn't specify genre:**
Ask explicitly: "Is this leadership, how-to, career, or thought leadership?"

**Theme doesn't emerge clearly:**
Ask: "What's the one thing readers should take away? If they remember nothing else, what matters most?"

**Too many chapters:**
Suggest combining. Over 12 chapters usually means some should merge.

**Too few chapters:**
Under 4 chapters means either too short (make it an article) or chapters need splitting.

## Files created

- `outline.md` - The master outline
- `voice-profile.md` - Optional, if sample provided

## Next steps

After outline is approved, use the `draft-chapter` skill to begin writing.
