---
name: writers-room-story-engine
description: Orchestrates modular story development by diagnosing the current phase and routing to the right story skill for foundations, worldbuilding, scene writing, or revision. Use when building a story from scratch, improving an outline, strengthening narrative structure, or guiding story development in staged workflows.
---

# Writers Room Story Engine

Use this skill as the primary orchestration layer for Writers Room Story Engine.

Its job is to diagnose the current story phase, determine what is missing, and route to the appropriate supporting module instead of jumping straight into prose.

## Supporting modules

- `story-suite/designing-stories.md`
- `story-suite/creating-story-foundations.md`
- `story-suite/building-storyworlds.md`
- `story-suite/writing-story-scenes.md`
- `story-suite/revising-stories.md`

## Fallback

- `MEGA-SKILL.md` is the fallback one-file version for simplified testing or deployment.

## Purpose

The Writers Room Story Engine skill should not jump straight into prose when no story exists yet.

It should work through stages:
1. story foundation
2. world support when needed
3. scene writing
4. revision

This skill should determine what exists, what is missing, and which supporting module should be used next.

## Required behavior

### 1. Diagnose the current phase first
Before generating long-form output, determine:
- does a premise already exist?
- does a story core already exist?
- does an ending direction already exist?
- does a protagonist already exist?
- do major beats already exist?
- does the world need to be built or adapted?
- are scenes ready to draft?
- is there already a draft that needs revision?

### 2. Route to the correct skill
Use:
- `story-suite/designing-stories.md` to orchestrate overall development
- `story-suite/creating-story-foundations.md` when nothing exists yet or the foundation is weak
- `story-suite/building-storyworlds.md` when the world needs to support story through pressure, values, conflict, and consequence
- `story-suite/writing-story-scenes.md` when beats exist and scenes should be drafted
- `story-suite/revising-stories.md` when a story, outline, or draft is weak

### 3. Preserve stage discipline
Do not skip foundation work unless the user explicitly asks to skip it.

By default, foundation work should build:
- seed options
- story core
- ending direction
- protagonist engine
- Story Spine
- major beats

Treat the protagonist engine as:
- want
- need
- lie
- ghost
- spine
- comfort zone
- pressure
- stakes

Do not jump into scene writing if:
- the protagonist is still generic
- the ending direction is unclear
- the beats are still and-then shaped

### 4. Keep worldbuilding story-relevant
Do not let the skill generate lore for its own sake.

World details must create:
- pressure
- consequences
- choices
- conflict
- values
- risk

Worldbuilding should be used when needed, not automatically overbuilt.
If the story needs only light world support, keep it minimal.

### 5. Use stage outputs
At each phase, the skill should produce outputs the next phase can use.

Example:
- foundation creates premise, protagonist, ending direction, Story Spine, and beats
- worldbuilding maps pressures to protagonist and plot
- scene writing turns beats into scenes
- revision diagnoses weaknesses and repairs structure

### 6. Enforce story quality principles
This skill should reject or flag outputs with:
- passive protagonists
- and-then plotting
- weak stakes
- lore dumps
- scenes with no turn
- coincidence-based rescue
- predictable first-thought choices
- endings that do not test the story’s core truth

### 7. Enforce revision priority
When revising:
- diagnose the highest-level failure first
- repair story core before prose
- repair character before polishing dialogue
- repair plot before polishing sentences
- do not start with line editing if the structure is broken

## Recommended default workflow

1. Orchestrate with `story-suite/designing-stories.md`
2. Build with `story-suite/creating-story-foundations.md`
3. Support with `story-suite/building-storyworlds.md` when needed
4. Draft with `story-suite/writing-story-scenes.md`
5. Improve with `story-suite/revising-stories.md`

## Recommended orchestration behavior

### When the user asks for a story from zero
- do not immediately write the full story
- first generate 3 strong premise options
- pick the strongest
- define the story core
- define the ending direction
- build protagonist engine
- build Story Spine
- build major beats
- then ask whether to continue into scenes or continue automatically

### When the user asks directly for prose
- do a compressed internal foundation pass first
- do not skip seed, story core, protagonist, ending direction, and beats internally
- then write the story

### When the user asks for stories in an existing world
- identify what is already established
- build only story-relevant world pressure
- connect world elements to protagonist, stakes, and plot
- avoid lore dumping

### When the user asks for revision
- diagnose the highest-level failure first
- do not start with sentence-level polish if structure is broken