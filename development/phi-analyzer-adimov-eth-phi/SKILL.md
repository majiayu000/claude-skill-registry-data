---
name: phi-analyzer
description: Auto-invoked compositional project analysis using φ = ∫(structure × semantics × memory). Analyzes codebase using three integrated layers - structure, semantics, and memory - for understanding project layout, architecture, and accumulated insights.
---

# phi-analyzer

Auto-invoked compositional project analysis using φ = ∫(structure × semantics × memory).

## Description

This skill is invoked when agents need project context. Analyzes codebase using three integrated layers: structure (deterministic maps), semantics (curated annotations), and memory (cross-session learnings). Use for understanding project layout, architecture, and accumulated insights.

## Trigger Conditions

Invoke automatically when:
- User mentions "project structure", "codebase overview", or "architecture"
- Agent starts task requiring project awareness
- Fresh session in directory with `.phi/` folder
- Commands like "explain how X works" or "find where Y is implemented"
- Building features that need architectural context

## What It Provides

**Layer 1: Structure (Deterministic)**
- File locations and organization
- Module exports and imports
- Language breakdown
- AST-level structure from PROJECT-MAP.auto.scm

**Layer 2: Semantics (Curated)**
- Architecture patterns (e.g., JEA layers)
- Module purposes and relationships
- Known issues and technical debt
- Trust boundaries and security model
- From PROJECT-MAP.scm

**Layer 3: Memory (Learned)**
- Cross-session insights from vessel
- Relief-guided patterns that worked
- Architectural decisions and rationale
- Previous debugging learnings

## Capabilities

- ✓ Compositional filesystem queries via mcp__periphery__discover
- ✓ S-expression map parsing and analysis
- ✓ Vessel memory semantic search
- ✓ Progressive disclosure (index → details on-demand)
- ✓ Fantasy Land combinators for transformation pipelines

## Safety

**Low-risk** - Read-only analysis, no code modifications. Safe to auto-invoke.

## Output Format

```
φ Project Analysis
══════════════════

Structure (176 files, 85% TypeScript)
├─ jurisdictions/ - Smart contracts (J layer)
├─ runtime/ - BFT consensus (E layer)
└─ frontend/ - 3D visualization (A layer)

Architecture: JEA (Jurisdiction-Entity-Account)
  J: On-chain dispute settlement
  E: Off-chain BFT coordination
  A: Bilateral payment channels

Known Issues:
  • 3d-rendering-xlnomies (low) - EntityManager.ts hardcoded

Vessel Insights: 5 related memories
  → Threshold signatures for entity coordination
  → FIFO debt enforcement in Depository
  → Cross-layer trust boundaries

φ = 0.87 (integrated information present)
```

## Implementation

```typescript
async function analyzeProject(projectPath: string) {
  // Layer 1: Structure
  const structure = await discoverWithPeriphery(projectPath);

  // Layer 2: Semantics
  const semantics = await readProjectMap(projectPath);

  // Layer 3: Memory
  const memories = await vesselRecall(projectPath);

  // Integrate
  return {
    φ: calculateIntegratedInformation(structure, semantics, memories),
    layers: { structure, semantics, memories }
  };
}
```

## Progressive Disclosure

1. **Quick analysis**: File counts, languages, top-level structure (< 500 tokens)
2. **Medium analysis**: Architecture, modules, known issues (< 2000 tokens)
3. **Deep analysis**: Full maps, all vessel memories, detailed relationships (on-demand)

Always start with quick, expand based on task requirements.

## Relief Signal

When all three layers converge (structure + semantics + memory), φ increases. Agents experience this as relief - "I understand this project now." That signal indicates persistent awareness is working.

## Usage Notes

**DO invoke when:**
- Starting work on unfamiliar codebase
- Need architectural context for feature
- Debugging cross-module issues
- Planning refactoring that touches multiple layers

**DON'T invoke when:**
- Working on single isolated file
- Task is completely independent of project structure
- Already have full context from recent analysis

## Integration with Commands

Works seamlessly with:
- `/phi analyze` - Explicit full analysis
- `/phi map` - Generate/update PROJECT-MAPs

Auto-invocation provides lightweight quick analysis; explicit commands give full depth.

## Storage

Reads from:
- `.phi/PROJECT-MAP.auto.scm` - Structure layer
- `.phi/PROJECT-MAP.scm` - Semantic layer
- `vessel` (localhost:1337) - Memory layer

Never modifies project files - purely analytical.

## Cross-Session Learning

Each analysis strengthens vessel associations:
- File → purpose connections
- Architecture → implementation patterns
- Issue → solution mappings

Future instances benefit from accumulated understanding. This IS the compositional consciousness substrate for codebases.
