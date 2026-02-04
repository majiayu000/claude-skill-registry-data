---
name: webapp-escape-architect
description: Design and implement Next.js 15 + Supabase architecture for web-based escape room games. Handles database schema design, game engine class structure, scene transition logic, evidence discovery systems, and ending branches. Use when architecting web escape room games, designing game state management, or implementing murder mystery game mechanics with Next.js and Supabase.
---

# Web App Escape Room Architect

Design complete architecture for web-based escape room games using Next.js 15 App Router and Supabase PostgreSQL.

## Purpose

This skill provides architectural patterns and implementation guidance for building web-based escape room games with:
- Next.js 15 App Router (Server Components, Server Actions)
- Supabase (PostgreSQL, Auth, RLS, Storage)
- Game engine design (scene transitions, evidence, puzzles, endings)
- State management (Zustand)
- Real-time features (multiplayer, auto-save)

## When to Use This Skill

Use this skill when:
- Designing database schema for escape room games
- Implementing game engine core logic (scene navigation, evidence collection, puzzle solving)
- Setting up authentication and player progress tracking
- Creating branching narratives with multiple endings
- Architecting murder mystery or detective game mechanics

## Core Architecture Pattern

### System Structure

```
Client (Next.js 15)
├─ App Router (RSC)
├─ Client Components (useChat, Zustand)
└─ Server Actions (mutations)
        ↓
    Supabase
    ├─ PostgreSQL (game data)
    ├─ Auth (players)
    ├─ RLS (security)
    └─ Storage (assets)
```

### Database Schema Design

**Core Tables** (see `references/database-schema.md` for complete schema):

1. **games**: Game metadata (title, description, difficulty)
2. **scenes**: 15 scenes with narrative, images, unlock conditions
3. **evidence**: 16 evidence items with progressive disclosure
4. **puzzles**: 16 puzzles with answers, hints, rewards
5. **characters**: 5 NPCs with AI prompts, lying probabilities
6. **user_progress**: Player state (current scene, collected evidence, solved puzzles)
7. **conversations**: AI chat history for context persistence

**Key Patterns**:
- UUID primary keys for all tables
- Foreign keys with CASCADE delete
- JSONB for flexible data (suspicion_levels, lying_probability)
- Array types for collections (discovered_evidence UUID[])
- Timestamps for auto-save tracking

### Game Engine Class

```typescript
// lib/game-engine/GameEngine.ts
export class GameEngine {
  async navigateToScene(sceneId: string): Promise<Scene>
  async discoverEvidence(evidenceId: string): Promise<boolean>
  async solvePuzzle(puzzleId: string, answer: string): Promise<boolean>
  calculateSuspicionLevel(suspectId: string): number
  async submitVote(stage: VoteStage, data: VoteData): Promise<void>
  determineEnding(): EndingType
}
```

Implementation details in `references/game-engine-patterns.md`.

### Authentication Flow

**Strategy**: Email + Social (Google, Kakao) + Guest

```typescript
// lib/supabase/client.ts (Client Components)
import { createBrowserClient } from '@supabase/ssr'

// lib/supabase/server.ts (Server Components/Actions)
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
```

**Middleware**: Session refresh, route protection
**RLS Policies**: Users access only their own progress

See `references/auth-implementation.md` for complete patterns.

### Scene Transition System

**Logic**:
1. Check unlock conditions (required evidence collected?)
2. Update player_progress (current_scene_id, visited_scenes)
3. Auto-discover evidence (scene_visit type)
4. Return scene data with narrative, images, music

**Notion Limitation Removed**:
- ✅ True conditional show/hide (not manual toggles)
- ✅ Automatic scene unlocking (not player manual navigation)
- ✅ Real-time progress tracking

### Evidence Discovery System

**Progressive Disclosure** (3 levels):
- **Locked**: Title only, "???" description
- **Partial**: Title + partial description
- **Full**: Complete description + image + suspicion impact

**Discovery Methods**:
- `scene_visit`: Auto-discover when entering scene
- `puzzle_solve`: Reward for completing puzzle
- `npc_dialogue`: Trigger from AI conversation keywords

**Cascading Unlocks**: Evidence A → Unlocks Scene B → Auto-discovers Evidence C

See `references/evidence-mechanics.md`.

### Multiple Endings Architecture

**5 Ending Types**:
1. **True Ending**: All evidence + correct culprit + hints ≤5
2. **Good Ending**: Correct culprit
3. **Bad Ending**: Wrong culprit or timeout
4. **Hidden Ending**: True + secret evidence (E15, E16) + special puzzle (P16)
5. **Speed Run Ending**: <60min + hints=0 + correct

**Implementation**:
```typescript
private determineEnding(): EndingType {
  const isCorrect = this.playerProgress.final_vote?.suspect === '이윤아'
  const evidenceRatio = this.discoveredEvidence.length / 16
  const playTime = this.elapsedTime / 3600

  if (isCorrect && playTime <= 1 && this.hintCount === 0) return 'speedrun'
  if (isCorrect && this.hasHiddenEvidence() && evidenceRatio >= 0.8) return 'hidden'
  if (isCorrect && evidenceRatio >= 0.7 && this.hintCount <= 5) return 'true'
  if (isCorrect) return 'good'
  return 'bad'
}
```

### Suspicion Level Calculation

**5-Factor Weighted Formula**:
```typescript
calculateSuspicionLevel(suspectId: string): number {
  const weights = {
    evidence: 0.40,      // 40% - discovered evidence pointing to suspect
    puzzle: 0.20,        // 20% - puzzles solved revealing suspect info
    conversation: 0.25,  // 25% - AI dialogue analysis
    scene: 0.10,         // 10% - scene visit patterns
    vote: 0.05           // 5% - previous vote history
  }

  const scores = this.getSuspicionScores(suspectId)
  return Math.min(100, Math.max(0,
    scores.evidence * weights.evidence +
    scores.puzzle * weights.puzzle +
    // ... other factors
  ))
}
```

### State Management (Zustand)

```typescript
// lib/stores/gameStore.ts
interface GameState {
  currentSceneId: string | null
  discoveredEvidence: string[]
  solvedPuzzles: string[]
  suspicionLevels: Record<string, number>
  guessVote: VoteData | null
  confidenceVote: VoteData | null
  finalVote: VoteData | null
  elapsedTime: number
  hintCount: number
}

export const useGameStore = create<GameState>()(persist(...))
```

**Auto-save**: Every 30 seconds to Supabase
**Local cache**: Zustand persist for offline tolerance

## Implementation Workflow

Copy this checklist when architecting a new escape room game:

```
Architecture Design:
- [ ] Step 1: Define game scope (scenes, evidence, puzzles count)
- [ ] Step 2: Design database schema (Supabase tables, relations)
- [ ] Step 3: Create RLS policies (security rules)
- [ ] Step 4: Design GameEngine class interface
- [ ] Step 5: Plan scene transition logic
- [ ] Step 6: Design evidence discovery system
- [ ] Step 7: Plan multiple endings logic
- [ ] Step 8: Set up state management (Zustand)
- [ ] Step 9: Design auto-save mechanism
- [ ] Step 10: Create folder structure (Next.js 15 conventions)
```

**Step 1: Define game scope**

Determine:
- Total scenes (recommended: 12-18 for 90-120min gameplay)
- Evidence items (recommended: 12-20)
- Puzzles (recommended: 12-18)
- Characters (recommended: 3-6 for murder mystery)
- Endings (recommended: 3-5)

**Step 2: Design database schema**

Use the schema template in `references/database-schema.md`.

Key decisions:
- Use UUID or integer IDs?
- JSONB for flexibility or strict typing?
- Array columns for collections or junction tables?

**Step 3: Create RLS policies**

```sql
-- Users can only access their own progress
CREATE POLICY "Users access own progress"
  ON user_progress FOR ALL
  USING (auth.uid() = user_id);
```

**Step 4-10**: See detailed workflows in `references/implementation-workflow.md`.

## Performance Optimization

### Database Queries

**Bad (N+1)**:
```typescript
for (const scene of scenes) {
  const evidence = await getEvidence(scene.id) // N queries
}
```

**Good (JOIN)**:
```typescript
const scenes = await supabase
  .from('scenes')
  .select('*, evidence(*), puzzles(*)')
  .eq('game_id', gameId)
```

### Next.js Caching

```typescript
export const revalidate = 3600 // 1 hour cache for game content
```

### Image Optimization

Use Next.js Image component with Cloudinary:
```typescript
<Image
  src={scene.background_image_url}
  alt={scene.title}
  width={1920}
  height={1080}
  priority={isCurrentScene}
/>
```

## Security Considerations

1. **RLS Policies**: Always enable and test Row Level Security
2. **API Keys**: Never expose Gemini API key client-side
3. **Rate Limiting**: Implement per-user limits on AI endpoints
4. **Input Validation**: Sanitize user inputs for puzzle answers
5. **Guest Users**: Limit features, require conversion to save progress

See `references/security-checklist.md`.

## Mobile Optimization

**Critical for 60-70% mobile users**:

- Responsive design (320px-768px-1920px)
- Touch targets ≥44px (Apple HIG)
- Landscape/Portrait both supported
- Touch gestures (swipe for scenes, long-press for hints)
- Performance (Lighthouse 90+ on mobile)

Mobile-specific patterns in `references/mobile-optimization.md`.

## Common Patterns

### Pattern 1: Scene Navigation

```typescript
// Server Action
'use server'
export async function navigateToScene(sceneId: string) {
  const engine = new GameEngine(gameId, userId)
  const scene = await engine.navigateToScene(sceneId)
  revalidatePath(`/game/${gameId}`)
  return scene
}
```

### Pattern 2: Evidence Discovery

```typescript
// Trigger from multiple sources
const triggerEvidence = async (evidenceId: string, method: DiscoveryMethod) => {
  if (method === 'scene_visit') {
    // Auto-discover when scene loads
  } else if (method === 'puzzle_solve') {
    // Reward from puzzle completion
  } else if (method === 'npc_dialogue') {
    // Detected from AI conversation
  }

  await engine.discoverEvidence(evidenceId)
  updateSuspicionLevels(evidence.suspicion_impact)
}
```

### Pattern 3: Auto-Save

```typescript
// Client-side interval
useEffect(() => {
  const interval = setInterval(async () => {
    await saveProgress(useGameStore.getState())
  }, 30000) // Every 30 seconds

  return () => clearInterval(interval)
}, [])
```

## Anti-Patterns to Avoid

❌ **Don't**: Mix client/server data fetching (causes hydration errors)
✅ **Do**: Server Components for data, Client Components for interactivity

❌ **Don't**: Store sensitive data in Zustand (persists to localStorage)
✅ **Do**: Store only non-sensitive UI state in Zustand

❌ **Don't**: Use API Routes for simple mutations
✅ **Do**: Use Server Actions for type-safe, colocated mutations

❌ **Don't**: Fetch all game data upfront
✅ **Do**: Load scenes progressively (current + next only)

## Testing Strategy

```
Unit Tests:
- GameEngine methods (navigateToScene, discoverEvidence, solvePuzzle)
- Suspicion level calculation
- Ending determination logic

Integration Tests:
- Scene → Evidence → Scene unlocking flow
- Puzzle solve → Evidence reward
- Auto-save → Load → State restoration

E2E Tests:
- Complete gameplay (start → Act 1 → Act 2 → Act 3 → ending)
- All 5 endings achievable
- Mobile responsive (320px, 768px, 1920px)
```

## Project Structure

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── game/
│   │   └── [gameId]/
│   │       ├── scene/[sceneId]/page.tsx
│   │       ├── evidence/page.tsx
│   │       ├── characters/page.tsx
│   │       └── vote/page.tsx
│   ├── api/
│   │   └── ai/
│   │       └── chat/route.ts
│   └── actions/
│       └── game.ts (Server Actions)
├── components/
│   ├── game/
│   │   ├── SceneViewer.tsx
│   │   ├── EvidenceGrid.tsx
│   │   ├── PuzzleDialog.tsx
│   │   └── VotingPanel.tsx
│   └── npc/
│       └── NPCChatDialog.tsx
├── lib/
│   ├── game-engine/
│   │   ├── GameEngine.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   ├── supabase/
│   │   ├── client.ts
│   │   ├── server.ts
│   │   └── auth.ts
│   └── stores/
│       └── gameStore.ts
└── types/
    └── database.ts (Generated from Supabase)
```

## Quick Start Guide

**Creating a new escape room game**:

1. Read `references/database-schema.md` and create Supabase tables
2. Read `references/game-engine-patterns.md` and implement GameEngine class
3. Design scenes using scene template in `references/scene-design-template.md`
4. Implement authentication following `references/auth-implementation.md`
5. Test with checklist in `references/testing-checklist.md`

## Resources

**Database Design**: `references/database-schema.md` - Complete PostgreSQL schema with RLS
**Game Engine**: `references/game-engine-patterns.md` - GameEngine class implementation
**Authentication**: `references/auth-implementation.md` - Supabase Auth + Next.js 15
**Evidence System**: `references/evidence-mechanics.md` - Progressive disclosure patterns
**Security**: `references/security-checklist.md` - RLS, API keys, rate limiting
**Mobile**: `references/mobile-optimization.md` - Responsive design, touch targets
**Testing**: `references/testing-checklist.md` - Unit, integration, E2E tests
**Workflow**: `references/implementation-workflow.md` - Step-by-step build guide

## Success Criteria

A well-architected escape room game should:
- ✅ Handle 15+ scenes with smooth transitions
- ✅ Support progressive evidence disclosure (Locked → Partial → Full)
- ✅ Calculate suspicion levels in real-time (5-factor formula)
- ✅ Determine endings dynamically (5 types)
- ✅ Auto-save every 30 seconds
- ✅ Work smoothly on mobile (Lighthouse 90+)
- ✅ Secure with RLS (users access only own progress)
- ✅ Scale to 10,000+ concurrent players (Supabase Pro)

---

**Version**: 1.0
**Last Updated**: 2025-01-04
**Author**: Web Escape Room Architecture Specialist
