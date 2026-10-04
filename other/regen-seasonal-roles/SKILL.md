---
name: regen-seasonal-roles
description: |
  Generate, evolve, and manage seasonal game roles for the ReGen Civics Team page. This skill handles the full seasonal role lifecycle: designing new roles (or adapting existing ones) for a new season, generating solarpunk character illustrations via nano-banana-pro, producing the TypeScript data arrays and component updates for the Team page, and recording everything to the master SEASONS_HISTORY.md. Use this skill whenever Rye says anything about a new season, seasonal roles, role rotation, updating the Team page for a new season, generating new character art for roles, reviewing past seasons, evolving roles, or planning what roles the next season needs. Also use when asked to add, remove, rename, or modify game roles, or when the conversation touches on seasonal transitions, season festivals, or role retrospectives. This skill is the single entry point for all seasonal role work.
---

# Seasonal Roles Generator

You're helping Rye prepare the next season of game roles for the ReGen Civics Team page. Each season, the roles might stay the same, shift slightly, get added or removed, or transform entirely based on what the project needs. Your job is to take Rye's season briefing and turn it into everything needed to update the site: role data, character art prompts, and a historical record.

## What This Skill Produces

> **Updated 2026-07-01: roles now live in the `roles` database table** (source of
> truth), seeded from `client/src/data/gameRoles.ts` via `scripts/seed-roles.ts`
> and edited from `/admin -> Role Holders`. Do NOT edit an inline array in
> `Team.tsx` (it reads the table via `trpc.roles.list`, falling back to
> `gameRoles.ts`). To add or change a role, either use the admin UI, or produce
> the field values and either (a) `INSERT`/`UPDATE` a row in `roles`
> (`slug` = kebab-case of `title`), or (b) update `client/src/data/gameRoles.ts`
> and re-run `scripts/seed-roles.ts` (idempotent upsert by slug). The Team page
> and coordination pipeline read the table; `roleHolders` is kept in sync by the
> daily flywheel's reconciliation against `roles`.

For each new season, you generate:

1. **Role rows for the `roles` table** (title, characterName, tagline, purpose, circle, powers, rights, responsibilities, band, tokenAward, aliases, kind, and so on), applied via the admin UI or a seed upsert. `gameRoles.ts` stays as the human-readable seed-of-record.
2. **Updated `seasons` TypeScript array** with the new season marked as current
3. **A CHARACTER_ART execution prompt** for Claude Code to generate all character illustrations via nano-banana-pro (Gemini)
4. **An entry in `SEASONS_HISTORY.md`** recording the full details for posterity and learning
5. **A summary of changes** from the previous season (what's new, what shifted, what was retired)

## Before You Start

Read these files to understand the current state:

0. **`SEASON_TEMPLATE.md`** (in repo root) -- the season assembly template: pre-season
   checklist, the ritual spine (opening ceremony, weekly campfire thread + featured
   quest + crew spotlight, mid-season ecological calendar moment, closing harvest
   ceremony), and the season's definition of done. This skill produces the role and
   art artifacts; the template holds the season's shape. Assemble season N+1 from it.
1. **`SEASONS_HISTORY.md`** (in repo root) -- the master record. Read the most recent season entry to understand what exists now.
2. **`docs/planning/CLAUDE_CODE_PROMPT_2026-04-03_CHARACTER_ART.md`** -- the current art prompt. Read the Style Guide section for the visual direction. The solarpunk aesthetic carries forward unless Rye says otherwise.
3. **`CLAUDE_CODE_PROMPT_2026-04-02_TEAM_ROLES.md`** -- the current Team page execution prompt. Read Part A (gameRoles array) and Part B (seasons array) for the current data structure.

If any of these files don't exist yet, check `references/role-data-schema.md` in this skill folder for the expected data shapes.

## The Season Briefing

Rye will tell you about the upcoming season. This might be a detailed brief or a quick conversation. Either way, you need to establish:

**Required:**
- What season is this? (name, theme, approximate dates, which solstice/equinox boundaries)
- What's the project focus this season? (what matters most)
- Are there new roles needed? If so, what do they do?
- Are any existing roles changing? (scope shifts, merges, splits, retirements)
- Any compensation changes?

**Usually provided:**
- Which roles are filled vs. open
- Any specific character art direction changes (new aesthetic, seasonal visual themes)
- Lessons from the previous season to apply

**You can figure out yourself (with Rye's confirmation):**
- Character names and taglines for new roles (brainstorm options, let Rye pick)
- Detailed powers/rights/responsibilities (draft from the purpose, Rye refines)
- Character visual descriptions (based on the established solarpunk style guide)
- Scene descriptions (match the role's domain to a fitting environment)
- Token award amounts (reference previous season's range as baseline)

## How to Generate a New Season

### Step 1: Gather and Confirm

Ask Rye the required questions above (skip any already answered in the conversation). Keep it conversational. If Rye gives you a quick "same roles, bump the Storyteller token award, add a new Events Coordinator role for summer festivals," that's enough to start drafting.

### Step 2: Draft the Roles

For each role (new or continuing), produce the full data shape. See `references/role-data-schema.md` for the TypeScript interface. Key fields:

```
title, emoji, characterName, tagline, characterImage, sceneImage,
purpose, circle, powers[], rights[], responsibilities[],
domains, tokenAward, seasons[], assignment, color,
specialContent? (optional, for roles with extra sections)
```

For **continuing roles**: Start from the previous season's data. Apply any changes Rye mentioned. Keep everything else stable.

For **new roles**: Draft the full set. Brainstorm 2-3 character name options with taglines and present them to Rye. Once confirmed, write the character and scene descriptions.

For **retired roles**: Remove from the gameRoles array but record in SEASONS_HISTORY.md with a note about why.

### Step 3: Generate Character Art Prompt

For each role that needs new art (new roles, or existing roles getting refreshed), write the CHARACTER_ART execution prompt. Follow the format in `references/character-art-template.md`. The prompt must include:

- The style guide (solarpunk baseline, plus any seasonal adjustments)
- Per-character descriptions (character appearance + scene background)
- Two generations per character: card portrait + full scene
- The prompt templates with placeholders filled
- Execution steps for Claude Code

The art style carries forward from season to season unless Rye wants to shift it. When it does shift, the new direction gets recorded in SEASONS_HISTORY.md so future seasons can reference it.

**Key art rules that always apply:**
- Card portraits: character only, no text, no background scene, clean edges
- Full scenes: landscape, character in environment, character name only as text
- Every scene: fruiting plants, comfortable wildlife, deeply organic and alive
- Single character per image (never duplicate the character in one scene)
- Diverse skin tones, body types, ages, hairstyles across the cast
- Color palette: greens, golds, teals, amber, living wood browns, soft white light

### Step 4: Update the Seasons Array

Update the `seasons` TypeScript array:
- Set `current: true` on the new season
- Set `current: false` on all others
- Update `activeRoles` arrays based on which roles are active each season
- Adjust months/themes if the cadence has shifted

Remember: seasons align to solstice/equinox boundaries but the project may run custom lengths. Record the actual dates, not just "Winter" generically.

### Step 5: Record in SEASONS_HISTORY.md

Add a complete entry following the format established in previous entries. Include all role data, character descriptions, art style notes, and a blank Lessons section for the season-end retrospective.

### Step 6: Produce the Claude Code Prompt

Package everything into an execution prompt that Claude Code can run:
- The CHARACTER_ART prompt for image generation
- The updated gameRoles and seasons arrays to paste into Team.tsx
- Any component changes needed (new specialContent sections, etc.)

### Step 7: Summary for Rye

Give Rye a clear summary:
- Roles continuing unchanged: [list]
- Roles modified: [list with what changed]
- New roles: [list with character names]
- Retired roles: [list with reason]
- Total $ReGen budget this season
- Files created/updated
- What Rye needs to do (run Claude Code prompt, push, etc.)

## Writing Rules

All content produced by this skill must follow the project's writing rules:

1. No em-dashes. Zero. Use commas, periods, colons, or rewrite.
2. No contrast-framing ("not X, but Y"). State what things ARE.
3. No AI word patterns (delve, tapestry, foster, leverage, etc.)
4. No rhetorical question openers.
5. No passive inspiration ("join us on this journey").
6. Voice: direct, grounded, specific. Rye's voice.

## Season Boundaries Reference

The Infinite Game uses solstice/equinox dates as season boundaries, though seasons may not follow the earthly cadence exactly. A season might start at the Spring Equinox and run through the Summer Solstice, or it might start at the Spring Equinox and end mid-summer on a custom date. The boundaries are anchors, not rigid fences.

| Boundary | Approx Date | Marks |
|---|---|---|
| Winter Solstice | Dec 21 | Potential season start/end |
| Spring Equinox | Mar 20 | Potential season start/end |
| Summer Solstice | Jun 21 | Potential season start/end |
| Fall Equinox | Sep 22 | Potential season start/end |

Within seasons, the lunar cycle provides a micro-rhythm:
- Full moon: outward energy, community events, public launches
- New moon: inward energy, reflection, deep work, planning
