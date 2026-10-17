---
name: cic-roadmap-updater
description: Calculate roadmap progress, suggest semantic version bumps, and generate updated entries. Integrates with CIC_MASTER_ROADMAP.md.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: (see package.json)
---

# CIC Roadmap Updater

Calculate progress and suggest version bumps for roadmaps.

## Trigger

`/skill cic-roadmap-updater` — invoke from gstack or CLI

## Input Schema

```typescript
interface Input {
  roadmapPath: string;          // path to roadmap file
  completedWaves: string[];     // wave IDs marked complete
  targetVersion?: string;       // optional: override suggested version
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  currentVersion: string;
  suggestedVersion: string;
  percentComplete: number;
  updatedEntries: Array<{
    wave: string;
    status: string;
    completion: number;
  }>;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
