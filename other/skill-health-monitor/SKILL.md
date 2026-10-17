---
name: skill-health-monitor
description: Ecosystem health audit. Reports staleness, never-run skills, manifest/directory drift. Distinct from structural-lint sibling tool.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: fs, path
---

# Skill Health Monitor

Reports ecosystem health for `toolforge/skills` using actual `manifest.json` and directory data.

## Trigger

```bash
npm run health-check -- --staleDays 30
```

## Input Schema

```typescript
interface HealthInput {
  manifestPath?: string;  // Default: toolforge/manifest.json
  skillsDir?: string;     // Default: toolforge/skills
  staleDays?: number;     // Default: 30
}
```

## Output Schema

```typescript
interface HealthOutput {
  status: "success" | "error";
  reportDate: string;
  totalSkills: number;
  neverRun: string[];
  stale: string[];
  orphanedEntries: string[];
  unregisteredDirs: string[];
  healthScore: number;
  recommendations: string[];
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For health score calculation, usage examples:** See [docs/USAGE.md](docs/USAGE.md).
