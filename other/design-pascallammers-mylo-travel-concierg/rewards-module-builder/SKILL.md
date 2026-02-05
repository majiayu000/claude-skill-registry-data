---
name: rewards-module-builder
description: Automates development of TogetherOS Rewards module features. Use when building reward types, implementing validation, creating UI components, writing tests, or updating Rewards documentation. Handles end-to-end implementation from entity models through API handlers to frontend components.
---

# Rewards Module Builder

This skill automates development of the TogetherOS Rewards module, a gamification system that recognizes contributions through badges, skill trees, and visual progression.

## When to Use This Skill

Use this skill when:
- Creating new reward types or badges
- Implementing reward validation logic
- Building reward UI components
- Writing tests for reward functionality
- Updating Rewards module documentation
- Connecting rewards to member actions

## Core Concepts

### Reward Types

TogetherOS supports four reward categories:

1. **Badges** - Achievement markers (e.g., "First PR Merged", "10 Mutual Aids")
2. **Skill Tree Nodes** - Path-specific progression (Builder, Community Heart, etc.)
3. **Visual States** - Member progression visualization (seed → seedling → young tree → majestic tree)
4. **Capability Unlocks** - Feature access gates (e.g., create proposals, organize events)

### Domain-Driven Architecture

Rewards module follows TogetherOS's standard domain-driven pattern:

```
apps/api/src/modules/rewards/
├── entities/          # Domain models (Badge, SkillNode, etc.)
├── repos/             # Data access interfaces + in-memory implementations
├── handlers/          # API handlers (create, award, list)
└── fixtures/          # Test data

apps/web/app/(platform)/profiles/[handle]/rewards/
├── page.tsx           # Member rewards view
└── components/        # Reward display components

packages/types/src/rewards.ts         # TypeScript interfaces
packages/validators/src/rewards.ts    # Zod schemas
packages/ui/src/rewards/              # Shared reward components
```

## Implementation Workflow

### 1. Define the Reward

Start with clear specifications:
- **What triggers it?** (e.g., "merge 10 PRs")
- **What does it unlock?** (capabilities, recognition)
- **Which path?** (Builder, Community Heart, etc.)
- **Visual representation?** (icon, color, animation)

### 2. Create Entity Model

```typescript
// apps/api/src/modules/rewards/entities/Badge.ts
export class Badge {
  constructor(
    public id: string,
    public name: string,
    public description: string,
    public icon: string,
    public path: 'builder' | 'community_heart' | 'guided_contributor' | 'steady_cultivator',
    public criteria: BadgeCriteria,
    public createdAt: Date
  ) {}

  static create(input: CreateBadgeInput): Badge {
    // Validation logic
    if (input.name.length < 3) {
      throw new Error('Badge name must be at least 3 characters')
    }
    
    return new Badge(
      generateId(),
      input.name,
      input.description,
      input.icon,
      input.path,
      input.criteria,
      new Date()
    )
  }

  canAward(memberActivity: MemberActivity): boolean {
    // Check if criteria met
    return this.criteria.check(memberActivity)
  }
}
```

### 3. Implement Repository

```typescript
// apps/api/src/modules/rewards/repos/BadgeRepo.ts
export interface BadgeRepo {
  create(input: CreateBadgeInput): Promise<Badge>
  findById(id: string): Promise<Badge | null>
  listByPath(path: string): Promise<Badge[]>
  award(badgeId: string, memberId: string): Promise<void>
  getMemberBadges(memberId: string): Promise<Badge[]>
}

// apps/api/src/modules/rewards/repos/InMemoryBadgeRepo.ts
export class InMemoryBadgeRepo implements BadgeRepo {
  private badges = new Map<string, Badge>()
  private awards = new Map<string, string[]>() // memberId -> badgeIds

  async create(input: CreateBadgeInput): Promise<Badge> {
    const badge = Badge.create(input)
    this.badges.set(badge.id, badge)
    return badge
  }

  async award(badgeId: string, memberId: string): Promise<void> {
    const badge = await this.findById(badgeId)
    if (!badge) throw new Error('Badge not found')
    
    const memberBadges = this.awards.get(memberId) || []
    if (!memberBadges.includes(badgeId)) {
      memberBadges.push(badgeId)
      this.awards.set(memberId, memberBadges)
    }
  }

  async getMemberBadges(memberId: string): Promise<Badge[]> {
    const badgeIds = this.awards.get(memberId) || []
    return Promise.all(
      badgeIds.map(id => this.findById(id)).filter(b => b !== null)
    )
  }
}
```

### 4. Create Zod Schemas

```typescript
// packages/validators/src/rewards.ts
import { z } from 'zod'

export const createBadgeSchema = z.object({
  name: z.string().min(3).max(50),
  description: z.string().min(10).max(200),
  icon: z.string().emoji().or(z.string().url()),
  path: z.enum(['builder', 'community_heart', 'guided_contributor', 'steady_cultivator']),
  criteria: z.object({
    type: z.enum(['pr_count', 'mutual_aid_count', 'event_organized', 'custom']),
    threshold: z.number().positive(),
    timeframe: z.enum(['all_time', 'monthly', 'yearly']).optional(),
  }),
})

export const awardBadgeSchema = z.object({
  badgeId: z.string().uuid(),
  memberId: z.string().uuid(),
  reason: z.string().min(10).max(200),
})
```

### 5. Implement API Handler

```typescript
// apps/api/src/modules/rewards/handlers/awardBadge.ts
import { awardBadgeSchema } from '@togetheros/validators'
import { BadgeRepo } from '../repos'

export async function awardBadge(
  input: unknown,
  repo: BadgeRepo
) {
  const data = awardBadgeSchema.parse(input)
  
  // Check if badge exists
  const badge = await repo.findById(data.badgeId)
  if (!badge) {
    return { error: { code: 'BADGE_NOT_FOUND', message: 'Badge does not exist' } }
  }

  // Award badge
  await repo.award(data.badgeId, data.memberId)
  
  // Log transaction (append-only NDJSON)
  await logRewardTransaction({
    type: 'badge_awarded',
    badgeId: data.badgeId,
    memberId: data.memberId,
    reason: data.reason,
    timestamp: new Date().toISOString(),
  })

  return { success: true }
}
```

### 6. Build UI Component

```typescript
// packages/ui/src/rewards/BadgeCard.tsx
import { Badge } from '@togetheros/types'

interface BadgeCardProps {
  badge: Badge
  earnedAt?: Date
  locked?: boolean
}

export function BadgeCard({ badge, earnedAt, locked = false }: BadgeCardProps) {
  return (
    <div className={`
      relative rounded-lg border p-4 transition-all
      ${locked ? 'opacity-50 grayscale' : 'hover:shadow-md'}
    `}>
      {/* Icon */}
      <div className="text-4xl mb-2">{badge.icon}</div>
      
      {/* Name */}
      <h3 className="font-semibold text-lg">{badge.name}</h3>
      
      {/* Description */}
      <p className="text-sm text-gray-600 mt-1">{badge.description}</p>
      
      {/* Earned date */}
      {earnedAt && (
        <p className="text-xs text-gray-500 mt-2">
          Earned {earnedAt.toLocaleDateString()}
        </p>
      )}
      
      {/* Locked overlay */}
      {locked && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl">🔒</span>
        </div>
      )}
    </div>
  )
}
```

### 7. Write Tests

```typescript
// apps/api/src/modules/rewards/__tests__/awardBadge.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { InMemoryBadgeRepo } from '../repos/InMemoryBadgeRepo'
import { awardBadge } from '../handlers/awardBadge'

describe('awardBadge', () => {
  let repo: InMemoryBadgeRepo

  beforeEach(() => {
    repo = new InMemoryBadgeRepo()
  })

  it('awards badge to member', async () => {
    // Setup
    const badge = await repo.create({
      name: 'First PR',
      description: 'Merged your first PR',
      icon: '🎉',
      path: 'builder',
      criteria: { type: 'pr_count', threshold: 1 },
    })

    // Execute
    const result = await awardBadge({
      badgeId: badge.id,
      memberId: 'member-123',
      reason: 'PR #42 merged',
    }, repo)

    // Assert
    expect(result.success).toBe(true)
    
    const memberBadges = await repo.getMemberBadges('member-123')
    expect(memberBadges).toHaveLength(1)
    expect(memberBadges[0].id).toBe(badge.id)
  })

  it('returns error for non-existent badge', async () => {
    const result = await awardBadge({
      badgeId: 'fake-id',
      memberId: 'member-123',
      reason: 'Test',
    }, repo)

    expect(result.error?.code).toBe('BADGE_NOT_FOUND')
  })

  it('prevents duplicate badge awards', async () => {
    const badge = await repo.create({
      name: 'First PR',
      description: 'Merged your first PR',
      icon: '🎉',
      path: 'builder',
      criteria: { type: 'pr_count', threshold: 1 },
    })

    // Award twice
    await awardBadge({ badgeId: badge.id, memberId: 'member-123', reason: 'First' }, repo)
    await awardBadge({ badgeId: badge.id, memberId: 'member-123', reason: 'Second' }, repo)

    // Should only have one
    const memberBadges = await repo.getMemberBadges('member-123')
    expect(memberBadges).toHaveLength(1)
  })
})
```

### 8. Create Fixtures

```typescript
// packages/fixtures/src/badges.ts
export const badgeFixtures = [
  {
    id: 'badge-first-pr',
    name: 'First PR Merged',
    description: 'Congratulations on your first merged pull request!',
    icon: '🎉',
    path: 'builder' as const,
    criteria: { type: 'pr_count' as const, threshold: 1 },
  },
  {
    id: 'badge-10-prs',
    name: '10 PRs Strong',
    description: 'You've merged 10 pull requests. Impressive!',
    icon: '💪',
    path: 'builder' as const,
    criteria: { type: 'pr_count' as const, threshold: 10 },
  },
  {
    id: 'badge-first-mutual-aid',
    name: 'Helping Hand',
    description: 'Completed your first mutual aid transaction',
    icon: '🤝',
    path: 'community_heart' as const,
    criteria: { type: 'mutual_aid_count' as const, threshold: 1 },
  },
]
```

## Transaction Logging

All reward awards must be logged to NDJSON:

```typescript
// Log format
{
  "id": "uuid",
  "timestamp": "2025-01-15T10:30:00Z",
  "event_type": "reward_awarded",
  "metadata": {
    "reward_type": "badge",
    "reward_id": "badge-first-pr",
    "member_id": "member-123",
    "reason": "PR #42 merged",
    "member_handle": "alice_organizer"
  }
}
```

Store logs in: `logs/rewards/transactions-YYYY-MM-DD.ndjson`

## Visual Progression System

Members progress through visual states based on contributions:

```typescript
export type VisualState = 'seed' | 'seedling' | 'young_tree' | 'majestic_tree'

export function calculateVisualState(contributionScore: number): VisualState {
  if (contributionScore < 10) return 'seed'
  if (contributionScore < 50) return 'seedling'
  if (contributionScore < 200) return 'young_tree'
  return 'majestic_tree'
}

export function getContributionScore(member: Member): number {
  let score = 0
  
  // PR contributions
  score += member.prsMerged * 5
  
  // Mutual aid
  score += member.mutualAidTransactions * 3
  
  // Proposals created
  score += member.proposalsCreated * 10
  
  // Events organized
  score += member.eventsOrganized * 15
  
  return score
}
```

## Capability Unlocks

Rewards can unlock new features:

```typescript
export interface CapabilityUnlock {
  capability: 'create_proposal' | 'organize_event' | 'moderate' | 'steward'
  requirements: {
    badges?: string[]
    contributionScore?: number
    paths?: string[]
  }
}

export function checkCapability(
  member: Member,
  capability: string
): boolean {
  const unlock = CAPABILITY_UNLOCKS[capability]
  if (!unlock) return false

  // Check badges
  if (unlock.requirements.badges) {
    const hasBadges = unlock.requirements.badges.every(badgeId =>
      member.badges.some(b => b.id === badgeId)
    )
    if (!hasBadges) return false
  }

  // Check contribution score
  if (unlock.requirements.contributionScore) {
    const score = getContributionScore(member)
    if (score < unlock.requirements.contributionScore) return false
  }

  // Check paths
  if (unlock.requirements.paths) {
    const hasPath = unlock.requirements.paths.some(path =>
      member.archetypes.includes(path)
    )
    if (!hasPath) return false
  }

  return true
}
```

## Documentation Updates

After implementing a reward, update:

1. **Module spec**: `docs/modules/rewards.md` - Add reward type to list
2. **Data models**: `packages/types/src/rewards.ts` - Export new interfaces
3. **Fixtures**: `packages/fixtures/src/badges.ts` - Add example data
4. **STATUS**: `docs/STATUS_v2.md` - Bump progress marker

## Common Patterns

### Auto-Award on Activity

```typescript
// In governance handler after PR merge
export async function handlePRMerge(prId: string, memberId: string) {
  // ... merge logic ...

  // Check for badge eligibility
  const member = await memberRepo.findById(memberId)
  const prCount = await getPRCount(memberId)

  if (prCount === 1) {
    await awardBadge({
      badgeId: 'badge-first-pr',
      memberId,
      reason: `PR #${prId} merged`,
    }, badgeRepo)
  }
}
```

### Display Badge Progress

```typescript
export function BadgeProgress({ badge, member }: Props) {
  const progress = calculateProgress(badge, member)
  
  return (
    <div>
      <BadgeCard badge={badge} locked={progress < 100} />
      <div className="mt-2">
        <div className="h-2 bg-gray-200 rounded">
          <div 
            className="h-full bg-blue-500 rounded"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="text-xs text-gray-600 mt-1">
          {progress}% complete
        </p>
      </div>
    </div>
  )
}
```

## Validation Checklist

Before submitting PR:

- [ ] Entity model includes validation logic
- [ ] Repository interface defined with in-memory implementation
- [ ] Zod schemas created with proper constraints
- [ ] API handler validates input and handles errors
- [ ] UI component handles all states (loading, empty, error, success)
- [ ] Unit tests cover happy path and error cases
- [ ] Fixture data added for testing
- [ ] NDJSON transaction logging implemented
- [ ] Documentation updated (module spec, data models, STATUS)
- [ ] `./scripts/validate.sh` passes with:
  - `LINT=OK`
  - `VALIDATORS=GREEN`
  - `SMOKE=OK`

## References

For detailed patterns and examples, see:
- **Reward Builder Guide**: `docs/dev/reward-module-guide.md` - Comprehensive templates and workflows
- **Data Models**: `packages/types/src/rewards.ts` - Complete type definitions
- **Social Economy**: Knowledge base document on gamification and progression systems
