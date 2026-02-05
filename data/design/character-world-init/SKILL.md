---
name: character-world-init
description: |
  This skill should be used when starting a new adventure, creating player characters,
  building game worlds, or when playerRef/worldRef is null. Triggers include: "create a character",
  "make a new character", "roll up a character", "build a character sheet", "create my PC",
  "what characters do I have", "pick my character", "set up a new world", "design a world",
  "choose a world", "show me available worlds", "initialize my campaign", "start a new adventure".
---

# Character & World Initialization Skill

Guides the GM through setting up a character and world for a new adventure. Use this skill when `playerRef` and/or `worldRef` are null in the adventure state.

## When to Use This Skill

This skill is triggered when:
- A new adventure starts and no character/world is configured
- The GM prompt indicates "Invoke the character-world-init skill for setup guidance"
- The player explicitly asks to create or select a character/world

## Workflow Overview

1. **List existing options** using `list_characters()` and `list_worlds()`
2. **Present choices** to the player - use existing or create new
3. **Process selection** by calling the appropriate set tool
4. **Populate files** with character/world data from player input

## Step 1: List Available Characters and Worlds

Use MCP tools to discover what exists:

```
list_characters()
```
Returns: Array of `{ slug, name }` for characters in `players/` directory.

```
list_worlds()
```
Returns: Array of `{ slug, name }` for worlds in `worlds/` directory.

## Step 2: Present Options to the Player

Present choices based on what exists:

**If characters exist:**
> "Welcome, adventurer! I see you have characters from previous adventures:
> - [Character Name] (from [world/adventure context if known])
>
> Would you like to continue with an existing character, or create someone new?"

**If no characters exist:**
> "Welcome, adventurer! This appears to be your first journey. Let's create your character.
> What is your character's name?"

**For world selection (similar pattern):**
> "Which world would you like to explore?
> - [World Name] - [brief description if available]
> - Create a new world"

## Step 3: Process the Selection

### To Create a New Character

Call `set_character` with `is_new: true`:

```
set_character({ name: "Kael Thouls", is_new: true })
```

This creates:
- Directory: `players/kael-thouls/`
- Files: `sheet.md`, `story.md` (with templates)
- Updates `playerRef` in adventure state to `"players/kael-thouls"`

### To Use an Existing Character

Call `set_character` with `is_new: false`:

```
set_character({ name: "kael-thouls", is_new: false })
```
(Can use slug or display name)

### To Create a New World

Call `set_world` with `is_new: true`:

```
set_world({ name: "Eldoria", is_new: true })
```

This creates:
- Directory: `worlds/eldoria/`
- Files: `world_state.md`, `locations.md`, `characters.md`, `quests.md`, `art-style.md` (with templates)
- Updates `worldRef` in adventure state to `"worlds/eldoria"`

**IMPORTANT: After creating a new world, immediately write a 1-2 line art style** to `art-style.md` based on the world's genre and tone. This art style is automatically applied to all generated background images. Example:

```
# Art Style

Oil painting, impressionist brushwork, warm earth tones
```

Keep it concise—just the visual style keywords, not a full description.

### To Use an Existing World

Call `set_world` with `is_new: false`:

```
set_world({ name: "eldoria", is_new: false })
```

## Step 4: Populate Character and World Files

After creating new entries, populate the markdown files with player-provided details.

**Character files** (`sheet.md`, `story.md`):
- Gather name, race, class, and background from the player
- Set initial attributes, equipment, and abilities in sheet.md
- Track current objectives and story arcs in story.md

**World files** (`world_state.md`, `locations.md`, `characters.md`, `quests.md`, `art-style.md`):
- Write the art style FIRST (1-2 lines, e.g., "Watercolor illustration, soft pastels, dreamlike quality")
- Establish genre, era, and tone in world_state.md
- Create the starting location with vivid description
- Add initial NPCs as the player encounters them

For detailed file templates, see [references/file-structure.md](references/file-structure.md).

## Example: Complete New Adventure Flow

```
GM: "Welcome, adventurer! Let me check if you have any existing characters..."
[GM calls list_characters()]

GM: "This is your first adventure! Let's create your character. What name shall I call you?"

Player: "Call me Kael Thouls"

GM: "Kael Thouls - a strong name! And what world shall we explore? Shall I create a new realm for your adventures?"
[GM calls list_worlds()]

Player: "Yes, create a new world called Eldoria"

GM: "Excellent! Let me set everything up..."
[GM calls set_character({ name: "Kael Thouls", is_new: true })]
[GM calls set_world({ name: "Eldoria", is_new: true })]

GM: "Perfect! Now tell me about Kael - what race and class are they?"
[GM proceeds to populate sheet.md with player's answers]
```

## Best Practices

1. **Be conversational**: Don't dump all questions at once. Guide the player step by step.
2. **Offer defaults**: Suggest typical options but let players customize.
3. **Validate names**: Tool handles slugification; use player's exact input for display name.
4. **Build narrative**: Frame setup as the beginning of a story, not a form to fill out.
5. **Respect existing data**: When using existing character/world, read their files first.
