---
name: repomix-package-builder
description: Create targeted repomix XML packages for AI code analysis. Suggests templates (metadata-flow, code-review, architecture, context) and file patterns based on task objectives. See reference.md for detailed workflows and patterns.
---

# Repomix Package Builder

Quick-start tool for creating AI-ready code analysis packages saved to `.claude/repomix_packages/`.

## When to Use

Activate when user needs to:
- Prepare code for external AI review or analysis
- Document cross-service integration flows (metadata, events, API calls)
- Conduct architectural analysis or pattern identification
- Create context packages for debugging or knowledge transfer
- Mentions: "repomix", "code package", "AI review", "context export"

## Available Templates

1. **metadata-flow** - Trace data/metadata between services via events and APIs
2. **code-review** - Comprehensive implementation + tests + docs + standards compliance
3. **architecture** - System design, service boundaries, DDD layers, patterns
4. **context** - Quick overview with essential docs and key implementation files

## Quick Workflow

1. Understand task objective (review? debug? document? analyze?)
2. Select matching template
3. Identify scope (which services/components?)
4. Build file include list (see `reference.md` for patterns)
5. Generate filename: `repomix-{feature}-{purpose}.xml`
6. Execute repomix command targeting `.claude/repomix_packages/`

## Reference Documentation

- **Detailed Templates & Patterns**: See `reference.md` in this directory
- **Real-World Examples**: See `examples.md` in this directory
- **Slash Command**: User can trigger `/repomix` for interactive workflow

## Output Conventions

- **Location**: `.claude/repomix_packages/`
- **Naming**: `repomix-{feature}-{purpose}.xml`
- **Examples**: `repomix-eng5-kafka-review.xml`, `repomix-metadata-population-task.xml`

## Token Budgets

- Quick context: 20-30K tokens (~7-10 files)
- Standard review: 60-80K tokens (~25-35 files)
- Deep analysis: 80-100K tokens (~30-40 files)

---

**For comprehensive guidance on file selection, templates, and best practices, reference `reference.md`.**
