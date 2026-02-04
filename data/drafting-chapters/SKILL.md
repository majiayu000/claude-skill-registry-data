---
name: "Drafting chapters"
description: "Drafts individual chapters for books and long articles. Use when user says 'draft chapter X', 'write chapter [number/title]', 'continue drafting', or 'write the next chapter'. Reads outline and maintains consistency with prior chapters."
---

# Drafting Chapters

Writes individual chapters that align with the theme and maintain voice consistency.

## When to use this skill

- User says "draft chapter 3" or "write chapter X"
- User says "continue drafting" (draft next incomplete chapter)
- User says "write the introduction/conclusion"
- An outline.md exists in the working directory

## What this skill does

1. Reads `outline.md` to understand theme and chapter purpose
2. Reads all completed chapters to maintain consistency
3. Loads `voice-profile.md` if it exists
4. Drafts the requested chapter
5. Flags research gaps inline
6. Updates chapter status in outline
7. Git commits the new chapter

## Prerequisites

**Must exist:**
- `outline.md` file in current directory

**If missing outline:**
```
I don't see an outline.md file. Should I create one first? 
I can use the 'outline-book' skill to help structure your book.
```

## Process

### Step 1: Pre-draft checklist

Before writing:
1. Read `outline.md` - note theme, chapter purpose, key points
2. Read `voice-profile.md` if it exists
3. Read all files in `/chapters/` directory to understand what's been written
4. Identify which chapter to draft (if user said "continue", pick next "not started" chapter)

### Step 2: Draft structure

Every chapter needs:

**Opening (1-3 paragraphs):**
- Hook that connects to theme
- Why this chapter matters
- What's coming

**Body:**
- Deliver all key points from outline
- Match voice profile characteristics
- Target the word count guide (not strict - ±20% is fine)
- Use appropriate depth for audience
- Natural transitions between ideas

**Closing (1-2 paragraphs):**
- Tie back to theme
- Key takeaway
- Bridge to next chapter (if not final chapter)

### Step 3: Handle research gaps

When you need information you don't have, insert:
```
[RESEARCH: description | severity: HIGH/MEDIUM/LOW]
```

**HIGH severity:** Significantly impacts credibility
- Example: `[RESEARCH: Need 2022-2024 statistics on remote work adoption | severity: HIGH]`

**MEDIUM severity:** Would strengthen but not critical
- Example: `[RESEARCH: Case study of company successfully implementing this | severity: MEDIUM]`

**LOW severity:** Nice-to-have verification
- Example: `[RESEARCH: Verify this framework attribution | severity: LOW]`

Continue drafting despite gaps. Don't let missing info block progress.

### Step 4: Save chapter file

Create file as `/chapters/[number]-[slug].md`

Examples:
- `/chapters/01-introduction.md`
- `/chapters/02-the-trust-framework.md`
- `/chapters/10-conclusion.md`

Use two-digit numbers for proper sorting.

### Step 5: Update outline status

In `outline.md`, change chapter status from "not started" to "complete":

```markdown
### Chapter 3: Building Psychological Safety
- **Status**: complete
```

### Step 6: Git commit

```bash
git add chapters/[number]-[title].md outline.md
git commit -m "Draft: Chapter [number] - [Title]"
```

## Voice consistency

If `voice-profile.md` exists, match these characteristics:

**Sentence structure:**
- Mimic average length patterns
- Match complexity level
- Follow rhythm (staccato vs flowing)

**Tone:**
- Maintain formality level
- Use consistent perspective
- Match directness

**Content techniques:**
- Use examples at similar frequency
- Match metaphor usage
- Balance data/stories as in profile
- Use questions at similar rate

**Technical approach:**
- Match jargon usage
- Maintain depth level
- Follow explanation style

## Word count guidance

Target is calculated as: `total_book_length / number_of_chapters`

This is a guide, not a rule:
- ±20% is completely fine
- Some chapters naturally run longer
- Introduction/conclusion often shorter
- Middle chapters often longer

If significantly over/under, note it but continue.

## Examples

### Example 1: Simple draft request

**User:** "Draft chapter 1"

**Process:**
1. Read outline.md → Chapter 1 is "Why Delegation Fails"
2. Read voice-profile.md → Conversational, uses examples
3. No other chapters exist yet
4. Draft chapter with opening hook, 3 key points from outline, closing
5. Save as `/chapters/01-why-delegation-fails.md`
6. Update outline status
7. Git commit

### Example 2: Continue drafting

**User:** "Continue drafting"

**Process:**
1. Read outline.md
2. Check chapter statuses → Chapters 1-3 complete, 4 is "not started"
3. Read chapters 1-3 to understand flow and maintain consistency
4. Draft chapter 4
5. Git commit

### Example 3: Research gap encountered

While drafting, you need statistics you don't have:

```markdown
Recent studies show [RESEARCH: Need data on manager time spent in meetings 2022-2024 | severity: HIGH] that managers spend excessive time in meetings.
```

Continue writing the rest of the chapter.

## Edge cases

**User requests chapter that doesn't exist in outline:**
```
I don't see a Chapter [X] in the outline. Current chapters are:
[list chapters from outline]

Did you mean one of these, or should I add a new chapter to the outline?
```

**Outline shows chapter as "complete" but file doesn't exist:**
```
The outline shows Chapter [X] as complete, but I don't see the file. 
Should I:
1. Draft it fresh (and update status)
2. Check if it's in a different location
```

**Cross-reference to unwritten chapter:**
If chapter 5 should reference chapter 3, but chapter 3 isn't drafted yet:
- Use placeholder: `[See Chapter 3 for details on X]`
- Note: `[TODO: Expand this reference once Chapter 3 is complete]`

**Significantly over word count:**
If draft is >30% over target, note it:
```
Note: This chapter came in at [X] words vs target of [Y]. 
This might be fine, or you could use 'revise-chapter' to condense it.
```

## Quality checklist

Each draft should:
- ✓ Open with clear theme connection
- ✓ Deliver all key points from outline
- ✓ Match voice profile (if exists)
- ✓ Include natural transitions
- ✓ Flag gaps rather than include weak content
- ✓ Close with tie to theme
- ✓ Target word count as rough guide

## Files created/modified

- `/chapters/[number]-[title].md` - New chapter file
- `outline.md` - Status updated to "complete"

## Next steps

**After drafting:**
- Use `track-research-gaps` to extract and organize research needs
- Use `check-theme-alignment` to verify alignment (automatically after every 2nd chapter)
- Use `revise-chapter` if chapter needs improvement
- Continue with next chapter using this skill again
