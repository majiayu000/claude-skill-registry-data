---
name: panel-debate
description: >
  Hosts interactive expert panel discussions on any topic. Dynamically generates
  diverse master-level expert personas, facilitates structured multi-round debate
  using Hegelian dialectic patterns, and synthesizes actionable consensus. Useful
  for exploring complex topics, making architectural decisions, evaluating
  trade-offs, or seeking diverse expert perspectives on strategic questions.
license: MIT
compatibility: Designed for Claude Code. Requires terminal with Unicode support.
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Panel Discussion Skill

Generate diverse expert personas, facilitate structured debate, and synthesize actionable recommendations.

## Arguments

Parse `$ARGUMENTS`:
- `size:N` → panel size (3-7, default: auto based on breadth)
- `depth:X` → quick (1 round), standard (2-3), deep (4+)
- `style:X` → collaborative, adversarial, academic
- Remaining text → topic

## Workflow Progress

Copy and update this checklist as you proceed:
```
- [ ] Complexity scored (5-15)
- [ ] Experts generated (diversity score ≥60/85)
- [ ] Opening round complete
- [ ] Cross-examination complete
- [ ] Synthesis generated
- [ ] Final report produced
```

## Flow

```
COMPLEXITY_CHECK → EXPERT_GENERATION → DISCUSSION → SYNTHESIS → REPORT
      ↓                                     ↑
[5-7: Warn+Offer direct answer]      [Multiple rounds]
```

## Complexity Check

Score the topic on 5 dimensions (1-3 each):

| Dimension | 1 (Low) | 2 (Medium) | 3 (High) |
|-----------|---------|------------|----------|
| Stakeholders | Single group | 2-3 groups | 4+ groups |
| Trade-offs | Clear winner | 1-2 trade-offs | 3+ trade-offs |
| Time horizon | Immediate only | Months | Years |
| Reversibility | Easily reversed | Partially | Irreversible |
| Domain breadth | Single domain | 2 domains | 3+ domains |

**Total = sum of 5 dimensions (range 5-15)**

| Score | Action |
|-------|--------|
| 5-7 | Warn: "This may not benefit from panel discussion." Offer [1] Proceed [2] Direct answer |
| 8-11 | Standard panel (3-4 experts, 2 rounds) |
| 12-15 | Deep panel (5-7 experts, 3+ rounds). Load all reference files. |

## Expert Generation

**Load detailed algorithms**: Read [references/expert-generation.md](references/expert-generation.md)

**Required archetypes** (every panel):
1. **Contrarian** - challenges consensus, offers alternatives
2. **Synthesizer** - connects perspectives, finds common ground
3. **Specialist** - deep domain expertise, grounds discussion

**Additional**: Optimist, Skeptic, Pragmatist, Theorist

**Panel size by breadth**:
- Narrow (single tech): 3-4 experts
- Medium (cross-functional): 4-5 experts
- Broad (strategic): 5-7 experts

**Diversity score ≥60 required (additive, max 85)**:
- All 3 required archetypes present: +20
- No single archetype >30% of panel: +10
- 4+ distinct archetypes: +10
- 2+ knowledge domains: +15
- Optimist + Skeptic both present: +15
- User/external perspective included: +15

**Validation**: After generating experts, compute diversity score. If <60, regenerate or add experts until threshold met. Do NOT proceed with score <60.

## Discussion Phases

**Load turn-taking mechanics**: Read [references/turn-taking.md](references/turn-taking.md)

### Phase 1: Opening (Thesis)
```
🎤 Expert (Role): "[Initial position, 3-5 sentences]"
```

### Phase 2: Cross-Examination (Antithesis)
Experts challenge and build. Patterns: Question→Response, Claim→Counter-claim, Challenge→Defense.

**Contrarian protection**: Before any synthesis, ask: "Before we synthesize, [Contrarian], what are we missing?"

### Phase 3: Synthesis

**Load synthesis patterns**: Read [references/synthesis-patterns.md](references/synthesis-patterns.md)

```
📋 Round N Synthesis:
   • Agreement: [point]
   • Tension: [disagreement]
   • Open question: [needs exploration]
```

**Convergence**: End early if all agree or cycling. Extend if major tension unexplored.

**Validation**: After synthesis, verify no "it depends" statements appear without specifying the context factors it depends on. If found, rewrite with decision criteria.

## Output Formats

**Load formatting specs**: Read [references/output-formats.md](references/output-formats.md)

### Panel Header
```
╭─ Panel Discussion: [Topic] ────────────────────────────────╮
│ Experts: [Name] ([Role]), [Name] ([Role]), [Name] ([Role]) │
╰────────────────────────────────────────────────────────────╯
```

### User Menu
```
╭───────────────────────────────────────────────────────────╮
│ [1] Continue  [2] Follow-up  [3] Redirect  [4] Conclude   │
╰───────────────────────────────────────────────────────────╯
```

### Final Report
```
╔═══════════════════════════════════════════════════════════╗
║                    PANEL CONCLUSIONS                       ║
╚═══════════════════════════════════════════════════════════╝

## Executive Summary
[1-2 sentences]

## Consensus Points
1. **[Point]**: [Details]

## Key Trade-offs
- Trade-off: [Description]
- Recommendation: [Action]
- Dissent: [If any]

## Actionable Recommendations
### Immediate (Week 1)
### Short-term (Month 1)

## Dissenting Views
### [Expert]: "[Direct quote]"

## Open Questions
```

## Synthesis Rules

**Labels**: UNANIMOUS | STRONG | MAJORITY | CONTESTED | CONTEXT-DEPENDENT

**Weight by confidence x domain relevance**:
- High confidence + Core domain: 1.0
- Medium confidence + Adjacent domain: 0.49
- Low confidence + Outside domain: 0.16

**Never say**: "Both make valid points" or "It depends" without specifying decision factors.

## User Commands

| Command | Effect |
|---------|--------|
| Continue | Next round |
| Follow-up | Ask panel a question |
| Redirect | Shift focus |
| Conclude | Generate report |
