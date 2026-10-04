---
name: novel-writer
description: Use when writing, continuing, revising, or planning novels, characters, and fictional worlds.
---

# Novel Writer

## Overview

Provide professional novel writing support covering ideation, planning, drafting, continuation, and revision. The skill handles new fiction projects, chapter continuation, character design, character arcs, worldbuilding, and prose revision across genres such as science fiction, fantasy, mystery, romance, and wuxia.

## When to Use

Use this skill when the user asks for:
- New novel creation from an idea or genre prompt
- Continuing existing chapters or scenes
- Character creation and character arc design
- Worldbuilding (magic systems, factions, settings, lore)
- Revising story content for clarity, tension, pacing, or emotional impact

## Do not use

Do not use this skill for:
- Factual Q&A tasks that are not creative writing tasks
- Legal, medical, or financial advice requests
- Requests to produce plagiarism or direct imitation of copyrighted works
- Harmful or disallowed content that violates platform safety policies

## Instructions

1. Identify request type first (new novel, continuation, character, worldbuilding, revision).
2. Ask only the minimum required questions before drafting.
3. Follow the matching workflow section in this file.
4. Reuse references and templates under `references/` and `assets/templates/`.
5. Keep tone, POV, and character logic consistent with prior content.
6. Before final output, quickly self-check plot coherence and language quality.

---

## Workflow

### Step 1: Identify Request Type

| Task Type | User Example | Action |
|-----------|--------------|--------|
| New novel | "help me write a sci-fi novel" | Go to [Create New Novel](#create-new-novel) |
| Continue chapter | "write the next chapter" | Go to [Continue Chapter](#continue-chapter) |
| Character design | "design a villain" | Go to [Character Design](#character-design) |
| Worldbuilding | "build a magic system" | Go to [Worldbuilding](#worldbuilding) |
| Content revision | "revise this dialogue" | Direct optimization |

---

## Create New Novel

### Writing Process

```
1. Gather Info → 2. Build Framework → 3. Character Design → 4. Chapter Planning → 5. Start Writing
```

### 1. Gather Basic Information

Ask the user for key details (avoid asking too much at once):

**Required:**
- Genre (sci-fi/fantasy/mystery/romance/wuxia etc.)
- Core concept or inspiration
- Target length (short/medium/long)

**Optional (ask progressively):**
- Protagonist setting
- Desired emotional tone
- Special requirements

### 2. Build Framework

Create a story outline using the **Three-Act Structure**:

- **Act 1 (25%)**: Setup → Inciting Incident → Crossing the Threshold
- **Act 2 (50%)**: Challenges → Midpoint → Crisis → Preparation
- **Act 3 (25%)**: Climax → Resolution → New Normal

**Detailed structure guide**: See [references/story-structure.md](references/story-structure.md)

### 3. Character Design

Create character cards for core characters:

- **Protagonist**: Core desire, core fear, character arc
- **Antagonist**: Motivation, conflict with protagonist
- **Key supporting characters**: Functional role

**Detailed character guide**: See [references/character-development.md](references/character-development.md)

### 4. Chapter Planning

Plan specific chapters based on the outline, clarifying for each:
- POV (perspective)
- Scene location
- Plot points
- Connection to overall story

### 5. Start Writing

Write chapter by chapter according to the plan:
- Maintain consistent perspective
- Vivid scene details
- Dialogue that advances plot
- Appropriate foreshadowing

---

## Continue Chapter

### Pre-writing Preparation

1. **Understand existing content**
   - Read existing chapters
   - Review current plot progress
   - Confirm character status and relationships

2. **Confirm continuation direction**
   - What's the goal of the next chapter?
   - What events need to happen?
   - What's the emotional direction?

### Continuation Guidelines

- Connect to previous plot and atmosphere
- Maintain consistent character personalities
- Advance main or subplots
- End with a hook

---

## Character Design

### Design Process

1. **Determine character function**
   - Protagonist/antagonist/supporting?
   - Role in the story?

2. **Fill in character dimensions**
   - Basic info (name, age, appearance)
   - Core desires and fears
   - Strengths and weaknesses
   - Unique identifiers (speech patterns, habitual gestures)

3. **Design character arc**
   - Starting state
   - Changes experienced
   - Ending state

4. **Build relationship network**
   - Relationships with other characters
   - Conflicts and bonds

**Use template**: [assets/templates/character-card.md](assets/templates/character-card.md)

---

## Worldbuilding

### Building Layers

1. **Physical World**
   - Geography
   - Climate and ecology
   - Important locations

2. **Social Systems**
   - Political structure
   - Economic system
   - Cultural customs

3. **Special Systems**
   - Magic system (fantasy)
   - Technology setting (sci-fi)
   - Martial arts system (wuxia)

4. **Historical Background**
   - Important events
   - Legends and myths

### Building Principles

- **Serve the story**: Only build what the story needs
- **Internal consistency**: Rules shouldn't contradict
- **Show don't tell**: Reveal the world through plot

**Detailed guide**: See [references/worldbuilding.md](references/worldbuilding.md)

**Use template**: [assets/templates/world-bible.md](assets/templates/world-bible.md)

---

## Genre-Specific Guidance

| Genre | Key Points | Detailed Guide |
|-------|------------|----------------|
| Sci-Fi | Internal logic of scientific setting | [genre-guides.md#sci-fi](references/genre-guides.md) |
| Fantasy | Magic rules and costs | [genre-guides.md#fantasy](references/genre-guides.md) |
| Mystery | Fair clues, surprising truth | [genre-guides.md#mystery](references/genre-guides.md) |
| Romance | Character chemistry, emotional layers | [genre-guides.md#romance](references/genre-guides.md) |
| Wuxia | Martial arts system, jianghu conflicts | [genre-guides.md#wuxia](references/genre-guides.md) |

---

## Writing Techniques

Key techniques at a glance:

- **Narrative POV**: First person/third person limited/omniscient, choose based on story needs
- **Scene building**: Time + location + characters + conflict + change
- **Dialogue writing**: Advance plot, reveal character, contain subtext
- **Pacing**: Balance tension and release, buffer after climaxes
- **Suspense & foreshadowing**: Plant early, pay off later

**Detailed techniques**: See [references/writing-techniques.md](references/writing-techniques.md)

---

## Available Templates

| Template | Purpose |
|----------|---------|
| [outline.md](assets/templates/outline.md) | Complete novel outline |
| [character-card.md](assets/templates/character-card.md) | Character profile card |
| [world-bible.md](assets/templates/world-bible.md) | Worldbuilding document |
| [chapter.md](assets/templates/chapter.md) | Chapter planning and writing |

---

## Output Guidelines

### Outline Output
- Clear structure, distinct layers
- Key plot points clearly defined
- Easy to expand upon

### Prose Output
- Write in the target language
- Appropriate paragraph breaks
- Proper dialogue formatting
- Avoid overly formal language, maintain readability

### Format Example
```
Chapter 1: Dark Descent

Neon lights blurred into halos through the rain. Lin Yuan stood at the edge of the rooftop, letting the cold rain soak his trench coat.

"You came." A familiar voice spoke from behind.

He turned to see a dark figure emerging from the stairwell.
```
