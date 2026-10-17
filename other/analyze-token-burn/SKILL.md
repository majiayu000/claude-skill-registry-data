---
name: analyze-token-burn
description: Project month-end token costs and identify high-spend adapters by mode (daily/monthly/by-adapter).
compatibility: |
  - Node.js 18+
  - Access to token usage metrics
---

# analyze-token-burn

Analyze token burn rate and forecast monthly costs by spend driver.

## Trigger

```
analyze-token-burn [daily|monthly|by-adapter]
```

## Input Schema

```typescript
interface SkillInput {
  mode?: "daily" | "monthly" | "by-adapter";  // default: "daily"
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  mode: string;
  budget: number;
  spent: number;
  projectedEndOfMonth: number;
  topDrivers?: Array<{ name: string; cost: number; percent: number }>;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
