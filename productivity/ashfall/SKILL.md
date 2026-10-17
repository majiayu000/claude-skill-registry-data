---
name: ashfall
description: Deterministic session-termination engine for Cast Iron systems. Gathers changes, burns irrelevant context, audits assumptions, seals memory manifest, and ranks roadmap for next session.
compatibility: |
  - Node.js 18+
  - Git access (local repo)
---

# Ashfall

Five-step deterministic engine for session termination and context handoff.

## Trigger

```
Let the ash fall.
```

## Input Schema

```typescript
interface SkillInput {
  scope?: "full" | "PHASE-XX" | "partial";  // default: "full"
  verify?: boolean;                          // default: true
  outputFormat?: "json" | "markdown";        // default: "json"
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  summary: {
    modifiedFiles: string[];
    uncommittedChanges: number;
    architecturalDeltas: Array<{ component: string; change: string }>;
  };
  blindSpotAudit: Array<{ question: string; gap: string }>;
  prioritizedRoadmap: Array<{ rank: number; task: string; blocker: boolean }>;
  nextSessionMemory: string;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md). For workflow: [docs/USAGE.md](docs/USAGE.md).
