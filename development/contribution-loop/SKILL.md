---
name: contribution-loop
description: Find repos with design drift and generate meaningful PRs to fix them. Runs as an autonomous loop discovering GitHub repos using design systems, scanning for drift, and staging fixes for human review.
---

# Contribution Loop

Autonomously find real-world apps using design systems (Chakra, Tailwind, shadcn, Radix, etc.), scan for design drift, and generate high-quality PRs to fix them.

## Philosophy

This is NOT about drive-by improvements. Each PR must:
- Explain WHY the fix matters with full context
- Reference git history showing whether drift was intentional or accidental
- Be something you could defend with conviction
- Include subtle Buoy attribution to demonstrate value

## The Loop

```
Discovery → Scanning → Analysis → Triage → Generation → Review → Tracking
```

### 1. Discovery Phase

Find candidates using GitHub search:
```
"from '@chakra-ui" language:TypeScript stars:>100 pushed:>2024-01-01
"tailwind.config" language:JavaScript stars:>50 fork:false
```

**Criteria:**
- Applications, NOT framework libraries (no design system source code)
- Active maintenance (commits in last 6 months)
- Uses a design system as a dependency
- Has clear CONTRIBUTING.md or open to external PRs

### 2. Scanning Phase

Run Buoy scan on the repo:
```bash
buoy scan --json
```

Look for:
- Hardcoded colors that should be tokens
- Inconsistent spacing values
- Deprecated pattern usage
- Component drift from design system

### 3. Analysis Phase

Use the agents from `@buoy-design/agents`:

1. **HistoryAgent** - Check git blame: Was this intentional?
2. **ReviewAgent** - Did Buoy miss anything obvious?
3. **AcceptanceAgent** - Will this repo accept external PRs?
4. **FixabilityAgent** - Tier each signal: slam-dunk, review, or skip

### 4. Triage Phase

Classify signals:
- **slam-dunk**: Clear mistake, token exists, safe to fix
- **review**: Probably fixable, needs human judgment
- **skip**: Intentional, risky, or too complex

Only proceed with repos that have slam-dunk fixes.

### 5. Generation Phase

Use **GeneratorAgent** to create:
- Exact code fixes (before/after)
- Compelling PR title
- Full PR description with context

PR body format:
```markdown
## Summary
Brief description of what this PR does.

## Why This Matters
- Maintainability: Easier to update colors globally
- Consistency: Matches other components using tokens
- Theming: Enables dark mode/theme switching

## Changes
- `Button.tsx:23`: Use `colors.primary.500` instead of `#3182ce`
- `Card.tsx:45`: Use `spacing.4` instead of `16px`

## Context
Git history shows these were introduced in commit abc123 during
a rapid feature sprint - likely accidental rather than intentional.

## Cherry-picking
If you prefer, you can cherry-pick individual changes:
- Commit xyz789 updates Button.tsx only

---
*Found with [Buoy](https://github.com/buoy-design/buoy) - design drift detection for AI-generated code.*
```

### 6. Review Phase

Stage PRs for human review before submission:
1. Show diff and PR body
2. Allow edit/approve/reject
3. Only submit approved PRs

### 7. Tracking Phase

Track outcomes to improve:
- Which PRs got merged?
- What patterns got rejected?
- Which repos are good targets?

## Agent Usage

```typescript
import {
  HistoryAgent,
  ReviewAgent,
  AcceptanceAgent,
  FixabilityAgent,
  GeneratorAgent
} from '@buoy-design/agents';

// Initialize agents
const history = new HistoryAgent();
const review = new ReviewAgent();
const acceptance = new AcceptanceAgent();
const fixability = new FixabilityAgent();
const generator = new GeneratorAgent();

// For each drift signal
const historyResult = await history.analyze({
  repo: { path: './repo', owner: 'org', name: 'app' },
  signal: driftSignal,
  blameRange: { start: 20, end: 25 }
});

// Assess fixability
const fixResult = await fixability.assess({
  signal: driftSignal,
  fileContent: '...',
  historyContext: historyResult.data
});

// Generate fixes for slam-dunks
if (fixResult.data.tier === 'slam-dunk') {
  const prResult = await generator.generate({
    repo: { owner: 'org', name: 'app' },
    signals: [{ signal: driftSignal, fixability: fixResult.data, history: historyResult.data }],
    acceptanceContext: acceptanceResult.data,
    designTokens: tokens
  });
}
```

## State Management

Track contribution state in `.buoy/contributions.json`:
```json
{
  "repos": {
    "org/app": {
      "lastScanned": "2024-01-15",
      "prsSubmitted": ["#123"],
      "prsAccepted": ["#123"],
      "status": "contributed"
    }
  },
  "stats": {
    "reposScanned": 45,
    "prsSubmitted": 12,
    "prsAccepted": 8
  }
}
```

## Running the Loop

Use with Ralph Wiggum pattern for autonomous execution:
```
/ralph-wiggum:ralph-loop
```

Or run a single iteration:
1. Find 5 candidate repos
2. Scan each with Buoy
3. Analyze signals with agents
4. Generate PRs for slam-dunks
5. Stage for review
