---
name: explore-approach
description: Prototype and explore technical approaches. Use when (1) multiple valid technical approaches exist, (2) performance characteristics unknown, (3) implementation path unclear, (4) need evidence-based technical recommendation.
tools: [Bash, Read, Write, Edit]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: explore-approach 호출 - {주제}` 시스템 메시지를 첫 줄에 출력하세요.

# explore-approach Skill

**Purpose**: Systematic technical exploration and evidence-based recommendation

## When to Use

Agents should invoke this skill when:

- Multiple valid technical approaches exist
- Performance characteristics unknown
- Integration complexity unclear
- New technology/library evaluation needed
- plan.md indicates technical uncertainty

## Quick Start

### 1. Create Spike Branch

```bash
git checkout -b spike/[topic-name]
```

### 2. Define Approaches (2-3)

Evaluation criteria:
- Performance (latency, throughput, resources)
- Complexity (LOC, learning curve)
- Maintainability (docs, community)
- Integration (stack compatibility)

### 3. Implement & Measure

- Time-box each prototype (1-2 hours max)
- Create `spike-prototypes/[approach-name]` directories
- Measure: setup time, LOC, dependencies, performance

### 4. Document Findings

Create `docs/spikes/[topic-name].md` with recommendation

## Usage

```javascript
skill: spike("realtime-tech-evaluation");
skill: spike("state-management", { focus: "performance" });
skill: spike("image-optimization", { quick: true });
```

## Critical Rules

1. **Spike Branches are Temporary**: NEVER merge to main
2. **Prototype, Don't Perfect**: Minimal viable implementation
3. **Measure Everything**: Metrics mandatory
4. **Evidence-Based Recommendations**: NEVER recommend without data
5. **Document for Future**: Spike docs are permanent

## Common Scenarios

| Scenario | Approaches | Duration |
|----------|------------|----------|
| Real-time | WebSocket vs SSE vs Polling | 2-3 hours |
| State Management | Zustand vs Jotai vs Redux | 1-2 hours |
| Image Optimization | next/image vs Cloudinary | 2-3 hours |
| Authentication | NextAuth vs Supabase Auth | 3-4 hours |

## Related Skills

- `spec` - Use recommendation in specification
- `implement` - Implement recommended approach
- `verify` - Validate implementation

## References

For detailed documentation, see:

- [Workflow](references/workflow.md) - 8-phase spike process, cleanup
- [Documentation Template](references/documentation-template.md) - Spike doc structure, output format
