---
name: operator-image-build
description: Deterministic Docker build, tag, push for harness-v3 and onnx-sidecar. SOURCE_DATE_EPOCH sealed, multi-stage builds, registry verification, air-gapped import.
compatibility: |
  - Runtime: Node.js 18+
  - System: Docker daemon, curl, ctr (air-gapped)
  - Dependencies: (see package.json)
---

# Operator Image Build

Deterministic Docker build, tag, push, verify for CIC harness components.

## Trigger

`/skill operator-image-build` — invoke with action and options

## Input Schema

```typescript
interface Input {
  action: "build" | "tag" | "push" | "verify" | "import" | "all";
  registry?: string;            // default: registry.internal:5000
  workdir?: string;             // default: .
  dryRun?: boolean;             // preview commands (default: false)
  verbose?: boolean;            // detailed output (default: true)
}
```

## Output Schema

```typescript
interface Output {
  status: "ok" | "error" | "warning";
  message: string;
  data: {
    action: string;
    images: Array<{
      name: string;
      status: string;
      digest?: string;
    }>;
    registry?: string;
    duration_ms: number;
  };
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For CLI usage, programmatic API, and troubleshooting:** See [docs/USAGE.md](docs/USAGE.md).
