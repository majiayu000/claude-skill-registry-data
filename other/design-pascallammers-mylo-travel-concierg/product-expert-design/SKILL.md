---
name: product-expert-design
description: Design user-facing agent experts for adaptive UX and personalization. Use when building product features that learn from user behavior, creating per-user expertise files, or implementing AI-driven personalization.
allowed-tools: Read, Grep, Glob, Write
---

# Product Expert Design

Guide for designing agent experts that serve end users through adaptive, personalized experiences.

## Codebase Experts vs Product Experts

| Aspect | Codebase Expert | Product Expert |
| --- | --- | --- |
| **Scope** | One per domain | One per user |
| **Storage** | File system (YAML) | Database (JSONB) |
| **Updates** | After code changes | After user actions |
| **Size** | 300-1000 lines | Typically smaller |
| **Latency** | Not critical | Must be fast |
| **Privacy** | Internal only | User data concerns |

## When to Use

- Building product features that learn from user behavior
- Creating per-user expertise files for personalization
- Implementing AI-driven adaptive UX
- Designing recommendation systems with user mental models
- Evaluating whether product experts are appropriate for your use case
- Building progressive personalization with latency considerations

## Product Expert Architecture

```text
┌─────────────────────────────────────────────────────┐
│ User Action (view, click, purchase, etc.)           │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ Action Tracker                                      │
│ • Capture action type                               │
│ • Record context (time, device, etc.)               │
│ • Queue for expertise update                        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ User Expertise Store (Database)                     │
│ • Per-user JSONB column                             │
│ • Structured preference model                       │
│ • Behavior patterns                                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ UI Generation Agent                                 │
│ • Load user expertise                               │
│ • Generate personalized UI                          │
│ • Adapt recommendations                             │
└─────────────────────────────────────────────────────┘
```

## User Expertise Schema

```json
{
  "user_id": "uuid",
  "created_at": "timestamp",
  "updated_at": "timestamp",

  "preferences": {
    "categories": ["tech", "sports"],
    "price_range": {"min": 50, "max": 500},
    "brands": ["Apple", "Sony"],
    "style": "minimalist"
  },

  "behavior_patterns": {
    "active_hours": [9, 10, 11, 14, 15, 20, 21],
    "device_preference": "mobile",
    "session_length_avg": 420,
    "purchase_frequency": "monthly"
  },

  "interaction_history": {
    "views": [
      {"item_id": "123", "timestamp": "...", "duration": 45}
    ],
    "cart_adds": [
      {"item_id": "456", "timestamp": "..."}
    ],
    "purchases": [
      {"item_id": "789", "timestamp": "...", "amount": 299}
    ]
  },

  "inferred_interests": {
    "high": ["wireless headphones", "smart home"],
    "medium": ["fitness trackers"],
    "low": ["gaming"]
  },

  "recommendations_context": {
    "last_shown": ["item1", "item2"],
    "clicked": ["item1"],
    "dismissed": ["item3"]
  }
}
```

## Act-Learn-Reuse for Products

### ACT: User Takes Action

```typescript
async function trackUserAction(
  userId: string,
  action: UserAction
): Promise<void> {
  // Record the action
  await db.userActions.create({
    userId,
    actionType: action.type,
    context: action.context,
    timestamp: new Date()
  });

  // Queue expertise update
  await expertiseQueue.add({
    userId,
    action,
    priority: getActionPriority(action.type)
  });
}
```

### LEARN: Update User Expertise

```typescript
async function updateUserExpertise(
  userId: string,
  action: UserAction
): Promise<void> {
  // Load current expertise
  const expertise = await loadUserExpertise(userId);

  // Update based on action type
  switch (action.type) {
    case 'view':
      updateViewPatterns(expertise, action);
      break;
    case 'cart_add':
      updatePurchaseIntent(expertise, action);
      break;
    case 'purchase':
      updatePreferences(expertise, action);
      break;
  }

  // Recalculate inferred interests
  expertise.inferred_interests = inferInterests(expertise);

  // Save updated expertise
  await saveUserExpertise(userId, expertise);
}
```

### REUSE: Personalized Experience

```typescript
async function generatePersonalizedUI(
  userId: string
): Promise<UIConfig> {
  // Load user expertise first
  const expertise = await loadUserExpertise(userId);

  // Generate UI based on expertise
  return {
    recommendations: await getRecommendations(expertise),
    layout: selectLayout(expertise.behavior_patterns),
    promotions: filterPromotions(expertise.preferences),
    navigation: prioritizeCategories(expertise.inferred_interests)
  };
}
```

## Latency Considerations

Product experts face latency challenges that codebase experts don't:

### The Problem

```text
User Request → Load Expertise → Generate UI → Response
                    ↓
              Agent thinking time (seconds)
                    ↓
              User waiting... (bad UX)
```

### Solutions

#### 1. Pre-computation

```typescript
// Update expertise async, not on-demand
// Pre-generate UI components during low traffic
```

#### 2. Progressive Loading

```typescript
// Show generic UI immediately
// Load personalized elements async
// Swap in when ready
```

#### 3. Expertise Caching

```typescript
// Cache hot user expertise in Redis
// Invalidate on significant changes only
```

#### 4. Tiered Personalization

```typescript
// Level 1: Instant (cached preferences)
// Level 2: Fast (simple inference)
// Level 3: Deep (full agent, async)
```

## Privacy and Data Handling

### Data Minimization

Only store what you need:

```json
// Good: Store patterns, not raw data
{
  "preferred_price_range": {"min": 100, "max": 300},
  "category_affinity": {"tech": 0.8, "fashion": 0.3}
}

// Bad: Store every view with full context
{
  "views": [/* hundreds of detailed entries */]
}
```

### User Control

Provide transparency and control:

```typescript
interface UserExpertiseControls {
  viewExpertise(): UserExpertise;
  clearExpertise(): void;
  disablePersonalization(): void;
  exportData(): DataExport;
}
```

### Retention Policies

```typescript
// Decay old data
function decayOldInteractions(expertise: UserExpertise): void {
  const cutoff = daysAgo(90);
  expertise.interaction_history =
    expertise.interaction_history.filter(i => i.timestamp > cutoff);
}
```

## When to Use Product Experts

| Use Case | Good Fit? | Notes |
| --- | --- | --- |
| E-commerce recommendations | Yes | High value, clear signals |
| Content personalization | Yes | Engagement improves |
| Search ranking | Yes | User-specific relevance |
| Simple preferences | No | Traditional settings work |
| Compliance-heavy domains | Maybe | Privacy concerns |
| Low-traffic products | No | Not enough data |

## Implementation Checklist

### Database Setup

- [ ] User expertise JSONB column
- [ ] Action tracking table
- [ ] Index on user_id for expertise lookup

### Backend Services

- [ ] Action tracking endpoint
- [ ] Expertise update worker (async)
- [ ] Expertise query API
- [ ] Cache layer (Redis)

### Agent Integration

- [ ] Expertise loading prompt
- [ ] UI generation prompt
- [ ] Recommendation prompt

### Frontend

- [ ] Progressive loading UI
- [ ] Skeleton states while personalizing
- [ ] Fallback to generic experience

### Privacy

- [ ] Data retention policy
- [ ] User control dashboard
- [ ] Export/delete functionality

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Sync updates | Blocks user | Async queue |
| Unbounded history | DB bloat | Rolling window |
| No fallback | Broken for new users | Default experience |
| Over-personalization | Filter bubble | Inject diversity |
| No decay | Stale preferences | Time-weighted data |

## Example: E-commerce Product Expert

```markdown
## User Expertise Structure

preferences:
  price_sensitivity: high|medium|low
  brand_loyalty: [list of preferred brands]
  category_interests: {category: affinity_score}

behavior:
  browse_vs_buy_ratio: 0.15
  cart_abandonment_rate: 0.4
  avg_time_to_purchase: 3 days

purchase_history:
  total_orders: 12
  avg_order_value: 150
  last_purchase: 2025-01-10

## Personalization Actions

1. Show price-sensitive users sale items first
2. Highlight preferred brands in search results
3. Remind high-abandonment users of cart items
4. Suggest reorder for repeat purchases
```

## Related Skills

- `agent-expert-creation`: Core expert patterns
- `expertise-file-design`: Schema design principles
- `self-improve-prompt-design`: Maintaining accuracy

---

**Last Updated:** 2025-12-15

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
