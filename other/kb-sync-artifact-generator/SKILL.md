---
name: kb-sync-artifact-generator
description: Generate interactive KB sync reports with sortable tables, charts, and drill-down details. Parses broken links and creates self-contained HTML with Grid.js table and Chart.js visualization.
compatibility: |
  - Python 3.10+
  - Node.js 16+
  - Access to C:\dev\cic-os\personal-knowledge-base/
---

# KB Sync Artifact Generator

Runs full KB sync pipeline and generates impact-scored interactive HTML artifact with sortable broken links table and category breakdown charts.

## Trigger

```
Generate an interactive KB sync report with sortable broken links table.
```

## Input Schema

```typescript
interface SkillInput {
  baseDir?: string;  // defaults to C:\dev\cic-os\personal-knowledge-base/
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  artifactId: string;
  filePath: string;
  summary: {
    pagesScanned: number;
    brokenLinks: number;
    categories: Record<string, number>;
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md). For workflow, examples, and troubleshooting: [docs/USAGE.md](docs/USAGE.md).

