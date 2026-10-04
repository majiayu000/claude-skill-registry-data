---
name: regen-quest-builder
description: >
  Build complete quests for ReGen Civics from concept to code. Given a quest
  idea, Claude produces all artifacts: questData.ts entry, QuestDetailModal
  detail block, hero image prompt, PDF quest guide, forum seed post, seed
  comments, and questData integration. Triggers on: "build a quest", "new
  quest", "add a quest", "quest builder", "create a quest", "design a quest",
  "quest for", or any request to add a new quest to the site.
---

# ReGen Quest Builder Skill

## Purpose

Take a quest idea from concept to fully shipped. Rye describes the quest theme,
and Claude produces every artifact the site needs to display, explain, and
support the quest.

## Artifacts Produced

Every quest needs these 7 artifacts:

| # | Artifact | File / Location | Format |
|---|----------|----------------|--------|
| 1 | Quest card data | `client/src/data/questData.ts` | TS object in existing structure |
| 2 | Quest detail block | `client/src/components/QuestDetailModal.tsx` | Inline object in QUEST_DETAIL_MAP |
| 3 | Hero image | `client/public/images/quests/quest-{NN}-{slug}.webp` | WebP, generated via image skill |
| 4 | PDF quest guide | `client/public/quest-guides/quest-{NN}-{slug}.pdf` | 1-2 page guide |
| 5 | Forum seed post | Database insert or manual entry | Title + body markdown |
| 6 | Seed comments | Database insert or manual entry | 2-3 starter replies |
| 7 | PDF slug mapping | `QuestDetailModal.tsx` QUEST_PDF_SLUGS | Key-value entry |

## Phase 0: Gather Requirements

Ask Rye these questions (max 5, skip any already answered):

1. **Quest name and theme** -- what is the quest about?
2. **Duration and cadence** -- how long does it take? One-time or recurring?
3. **Section placement** -- which season (spring/summer/fall/winter), routine, or featured?
4. **Rewards** -- how many $ReGen and RGVoice? (default: 111 ReGen, 1 Voice)
5. **References** -- any existing content, videos, PDFs, or links to draw from?

Once answered, confirm the plan in one sentence and start building.

## Phase 1: Write Quest Card Data

Add an entry to `client/src/data/questData.ts`.

**Required fields:**
```typescript
{
  id: number,           // Next available ID (check existing max)
  slug: string,         // kebab-case, e.g. "love-to-heal-your-body"
  title: string,        // Display title
  subtitle: string,     // 3-5 word thematic subtitle
  description: string,  // 1-3 sentences, Rye's voice, no AI-isms
  reward: { regen: number, rvoice: number },
  icon: LucideIcon,     // Pick from lucide-react, import at top
  deliverable: string,  // What the player submits
  focus: string,        // Comma-separated keywords
  isRoutine?: boolean,  // true if repeatable
  forumSlug: string,    // kebab-case forum category
  forumUrl: string,     // Will be filled after forum post is created
}
```

**Placement rules:**
- Seasonal quests go in the appropriate season array
- Routine quests go alongside `routine` (Fasting) or `featured` (Food Foresting)
- New routine quests: add a new key like `routine2` or extend the structure

**Icon selection:** Pick a lucide-react icon that matches the theme. Common ones
already imported: Flame, Droplets, Sprout, TreeDeciduous, HomeIcon, Heart,
Users, Apple, Circle, MessageSquare, GitBranch, Wind, Brain, Sparkles. Add new
imports as needed.

## Phase 2: Write Quest Detail Block

Add an entry to the quest details map in `QuestDetailModal.tsx`.

**Required fields:**
```typescript
{
  id: string,              // "quest-{N}" matching questData id
  title: string,
  subtitle: string,
  description: string,     // Can be longer than card description
  storyCard: string,       // 3-4 sentences, narrative, Rye's voice
  rewards: { regen: number, rvoice: number },
  deliverable: string,
  estimatedTime: string,   // e.g. "2-4 hours" or "30 days (every other day)"
  steps: QuestStep[],      // 4-8 steps with title + description
  resources?: { title: string, url: string }[],
  tips?: string[],         // 3-5 actionable tips
  videoUrl?: string,       // YouTube URL if available
}
```

**Writing rules for storyCard and description:**
- Use Rye's voice: direct, grounded, specific
- No em-dashes (zero)
- No contrast-framing ("not X, but Y")
- No AI word patterns (see CLAUDE.md RULE 3)
- No rhetorical question openers
- No passive inspiration ("join us on this journey")
- Write as if someone inside the regen movement wrote it

**Steps format:**
Each step should be a concrete action, not a vague instruction.
- Bad: "Reflect on your journey"
- Good: "Sit quietly for 10 minutes. Scan your body from feet to crown.
  Notice where you hold tension. Write down 3 areas that spoke to you."

## Phase 3: Generate Hero Image

Use the nano-banana-pro skill (or provide a prompt for manual generation).

**Naming:** `quest-{NN}-{slug}.webp` in `client/public/images/quests/`
**Style:** Match existing quest images: nature-themed, painterly/illustrated,
warm earth tones with greens and golds, no text overlay.

**Prompt template:**
> A painterly digital illustration for a regenerative quest called "{title}".
> Theme: {description}. Style: warm earth tones, lush greens and golds,
> soft natural lighting, no text, evocative of healing and nature connection.
> Aspect ratio: 16:9.

## Phase 4: Create PDF Quest Guide

Use the pdf skill to create a 1-2 page quest guide.

**Location:** `client/public/quest-guides/quest-{NN}-{slug}.pdf`

**Contents:**
1. Quest title and subtitle
2. Story card text (the narrative intro)
3. What you will do (deliverable)
4. Step-by-step instructions (from the detail block)
5. Tips for success
6. Resources and links
7. Reward info

**Also update** the `QUEST_PDF_SLUGS` map in `QuestDetailModal.tsx`:
```typescript
"quest-{N}": "quest-{NN}-{slug}",
```

## Phase 5: Seed Forum Post + Comments (automated via DB)

Write a seed script at `scripts/seed-quest-{N}-forum.ts` following the
pattern in `scripts/seed-quest-forum-posts.ts`. The script must:

1. Use `mysql2/promise` with `DATABASE_URL` from `.env`
2. Support `--dry-run` flag
3. Be idempotent (skip if post title already exists)
4. Look up category by slug: `quests-gameplay`, `rites-quests`, or `general`
5. Look up author: `rieki.cordon@gmail.com` first, fallback to team user
6. Insert post with `isPinned: 1`
7. Insert 3 seed comments with `**Author Name** (@handle)` prefix
8. Print the resulting post ID and forum URL

**Seed comment personas:**
Write from the perspective of fictional people who have done the quest.
Specific, personal, grounded. No generic encouragement.
- Comment 1: Someone sharing their first attempt and what surprised them
- Comment 2: Someone sharing a practical tip they discovered
- Comment 3: Someone connecting the quest to a broader life change

**After running the script:**
1. Note the returned post ID
2. Update `forumUrl` in questData.ts to `/community/post/{ID}`

**Running the script:**
```powershell
# From project root on Windows:
set DATABASE_URL=<value from .env>
npx tsx scripts/seed-quest-{N}-forum.ts --dry-run   # verify first
npx tsx scripts/seed-quest-{N}-forum.ts              # run for real
```

## Phase 6: Generate Hero Image

**If nano-banana-pro skill is available (Cowork with API key):**
Run it directly to generate the image.

**If running in Claude Code or nano-banana-pro is unavailable:**
Save a prompt file at `docs/quest-{N}-image-prompt.md` with:
1. The full image generation prompt
2. Output filename: `quest-{NN}-{slug}.webp`
3. Conversion commands (cwebp or ffmpeg) to convert PNG to WebP
4. Git commands to commit the result

**Prompt template:**
> A painterly digital illustration for a regenerative quest called "{title}".
> [Specific visual description based on quest theme]. Style: warm earth tones,
> lush greens and golds, soft natural lighting, no text, no UI elements,
> evocative of healing and nature connection. Aspect ratio: 16:9.

**For Rye to run in Claude Code:**
```
Generate a quest hero image using the nano-banana-pro skill.
Use 2K resolution. Save as quest-{NN}-{slug}.png.
Prompt: [paste the prompt from the doc]
Then convert to WebP and move to client/public/images/quests/
```

## Phase 7: Integration, Build, and Deploy

1. Verify all imports are correct in questData.ts and QuestDetailModal.tsx
2. Verify Quest.tsx has a card for the new quest with onClick handler
3. Run build: `npm run build` via Desktop Commander
4. Fix any build errors
5. Commit all files with message: `feat: add quest {N} - {title}`
6. Push to main (Railway auto-deploys)
7. Verify live on regencivics.earth/quest

## Phase 8: Handoff (only for items that truly need Rye)

Report to Rye with one clear list. Most items should be done already.
The only remaining manual step is typically:

- **Hero image** (if nano-banana-pro wasn't available): run the prompt file
  in Claude Code. The file is at `docs/quest-{N}-image-prompt.md`.

Everything else (code, PDF, forum post, seed comments, deploy) should be
complete before handoff.

## Phase 7b: Update Master Reference Sheets

Every new quest MUST be added to these three documents, which are the source of
truth for all quest data:

1. **QUEST_MASTER_SHEET.md** - Add full quest entry (story card, steps, tips,
   connected quests) in the appropriate section (Part 3 for Rites, Part 4 for
   Seasonal, Part 4b for Routine). Include slug, rewards, time, deliverable.

2. **QUEST_ORGANIZATION_PLAN.md** - Add the quest to the appropriate inventory
   table (Section 2 for Rites, Section 3 for Seasonal, Section 4 for Epic).
   Update any carousel placement notes.

3. **docs/planning/QUEST_PROGRESSION_SPEC.md** - If the quest has special unlock conditions
   (routine, epic, etc.), verify the progression chain still matches. Update
   any unlock rules that reference specific quest IDs.

These sheets are the master reference for any work involving quests. Always
read them before making quest-related changes to code or content.

## SDT Rubric (score every quest before shipping)

Self-determination theory names the three needs that make a quest worth
returning to: autonomy, competence, relatedness. Score each 1-5 before any
quest ships. Multiplayer quests (shared/multiplayerQuests.ts) carry these
scores in their `sdt` field; solo quests record them in the quest's entry in
QUEST_MASTER_SHEET.md.

**Autonomy (1-5)** -- how much do players shape the quest themselves?
- 5: players choose the site, timing, method, and roles
- 3: players choose timing and some method within a fixed structure
- 1: a fixed checklist with one way through

**Competence (1-5)** -- does completing it produce a visible, earned result?
- 5: a real-world artifact or change the player can point at the same day
- 3: a completed practice or event with soft evidence
- 1: participation only, nothing to show

**Relatedness (1-5)** -- does the quest connect people?
- 5: structurally requires coordination (a crew, distinct roles, shared output)
- 3: solo work with a strong sharing moment (forum post, gathering)
- 1: fully solo, no sharing built in

Rules of thumb:
- No quest ships with any score of 1 unless there's a stated reason.
- Multiplayer quests must score 4+ on relatedness; that's what makes them
  multiplayer. If roles are interchangeable, redesign until the parts are
  distinct (a hauler is not a documenter).
- If autonomy is low, say so in the story card ("the stewards direct the
  work") so the trade is honest.
- Record one sentence of rationale per score. The rationale is what the next
  quest designer learns from.

## Multiplayer quests (crew quests)

Multiplayer quest definitions live in `shared/multiplayerQuests.ts`, keyed
`crew-quest-{N}`, with `status: "draft" | "live"`. Drafts never render and
never accept signups; Rye ratifies copy and rewards, then flips status to
live. Each needs: 3-7 crew size (min and max), 3+ distinct `crewRoles`, 4+
steps, a `definitionOfDone` the crew thread's welcome post names, and the
`sdt` scores above. Crew assembly, crew chat threads, and formation emails
are handled by `server/jobs/questCrewAssembly.ts`; the signup surface is
`/multiplayer` (client/src/pages/Multiplayer.tsx).

## Writing Quality Checklist

Before shipping any quest content, verify:

- [ ] Zero em-dashes in all text
- [ ] No contrast-framing patterns
- [ ] No AI word patterns (CLAUDE.md RULE 3)
- [ ] No rhetorical question openers
- [ ] No passive inspiration phrases
- [ ] storyCard is 3-4 sentences, narrative, grounded
- [ ] Steps are concrete actions with specific instructions
- [ ] Tips are actionable, not generic
- [ ] All slugs are kebab-case and consistent across artifacts
- [ ] Quest ID is unique and sequential
- [ ] Icon import exists at top of questData.ts
- [ ] PDF slug mapping added to QuestDetailModal.tsx
- [ ] Forum URL placeholder set (update after post creation)
