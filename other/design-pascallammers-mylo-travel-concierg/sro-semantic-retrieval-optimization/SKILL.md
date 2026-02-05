---
name: sro-semantic-retrieval-optimization
description: Implement Semantic Retrieval Optimization for AI search visibility. Use when performing SRO audits, building entity maps, designing SCN architecture, writing retrieval-optimized content, implementing schema markup, calibrating trust signals, analyzing query intent, assessing technical eligibility, or creating AI-ready content strategies. Triggers on semantic SEO, entity mapping, SCN, E-E-A-T, AI search optimization, passage engineering, knowledge graph, trust signals, or retrieval optimization requests.
---

# Semantic Retrieval Optimization (SRO)

Optimize websites for AI retrieval and selection, not just ranking.

## Workflow Selection

Determine task type and follow the appropriate workflow:

**Full SRO Audit** → Run `scripts/sro_audit.py`
**Entity Mapping** → See `references/entity-mapping.md`
**SCN Architecture** → See `references/scn-structure.md`
**Content Optimization** → See `references/microsemantic-writing.md`
**Trust Calibration** → See `references/trust-signals.md`
**Technical Check** → See `references/technical-eligibility.md`
**Schema Generation** → Run `scripts/generate_schema.py`
**Quick Audit** → Run `scripts/quick_audit.py`

## Core Framework

### Five Layers (All Required)

| Layer | Check | Script/Reference |
|-------|-------|------------------|
| Macrosemantics | Site structure, SCN hierarchy | `references/scn-structure.md` |
| Microsemantics | Passage clarity, extractability | `references/microsemantic-writing.md` |
| Technical | Speed, render, access | `references/technical-eligibility.md` |
| Trust | Evidence, identity, corroboration | `references/trust-signals.md` |
| Query | Intent matching | `references/query-semantics.md` |

### Implementation Steps

1. **AUDIT** → Run `scripts/sro_audit.py` on target URL
2. **MAP ENTITIES** → Use entity mapping workflow in `references/entity-mapping.md`
3. **DESIGN SCN** → Follow SCN architecture in `references/scn-structure.md`
4. **OPTIMIZE CONTENT** → Apply rules in `references/microsemantic-writing.md`
5. **IMPLEMENT SCHEMA** → Run `scripts/generate_schema.py`
6. **CALIBRATE TRUST** → Follow `references/trust-signals.md`
7. **VERIFY TECHNICAL** → Run technical checks per `references/technical-eligibility.md`
8. **MONITOR** → Set up tracking per `references/operations.md`

## Quick Reference

### Entity Types

```
Organization → Brand, company, publisher
Person → Author, expert, founder
Product → Offering, service, tool
Location → Place, region, address
Concept → Topic, methodology, framework
```

### SCN Hierarchy

```
MACRO (content universe)
├── SEED (major subtopic, 3-7 per Macro)
│   └── NODE (specific content, 5-20 per Seed)
```

### Intent Frames

| Frame | Structure Required |
|-------|-------------------|
| Instructional | Numbered steps, action verbs |
| Comparative | Side-by-side, criteria, recommendation |
| Evaluative | Ranked list, methodology |
| Descriptive | Definition, explanation, examples |
| Causal | Cause-effect relationship |

### Trust Layers

| Layer | Signal |
|-------|--------|
| Evidence | Citations within 1-2 sentences of claims |
| Identity | Schema, author bios, verified profiles |
| Cluster | Consistent facts across all pages |
| Corroboration | External mentions, reviews, citations |

### Technical Thresholds

| Metric | Target |
|--------|--------|
| TTFB | <300ms |
| LCP | <2.5s |
| DOM nodes | <1,500 |
| Content | In HTML, not JS-dependent |

## Linking Rules

**Vertical (always safe):**
- Node → Parent Seed
- Seed → Macro
- Macro → All Seeds

**Horizontal (use 150% rule):**
Only link when 150% certain of semantic relationship. When in doubt, don't link.

## Passage Engineering Rules

1. One idea per section (100-150 words)
2. Self-contained (makes sense without context)
3. Entity-rich (names, not pronouns)
4. Front-loaded (key info first)
5. Frame-matched (structure matches intent)

## Common Errors

| Error | Detection | Fix |
|-------|-----------|-----|
| Mixed intent frames | Multiple structures on one page | Split into separate pages |
| Entity inconsistency | "Acme" vs "Acme Inc" | Standardize naming |
| Evidence distance | Claims without nearby support | Move citations closer |
| Orphan content | No internal links | Connect to SCN |
| JS-dependent content | Core text in JavaScript | Move to HTML |
| Missing attribution | No author/source | Add author schema |

## Output Templates

### Entity Map Output
```json
{
  "entities": [
    {
      "name": "",
      "type": "Organization|Person|Product|Location|Concept",
      "relationships": [],
      "schema_type": "",
      "proof_urls": []
    }
  ]
}
```

### SCN Map Output
```yaml
macro:
  name: ""
  description: ""
seeds:
  - name: ""
    nodes:
      - title: ""
        intent_frame: ""
        target_url: ""
```

### Audit Score Output
```json
{
  "overall_score": 0,
  "layers": {
    "macrosemantics": {"score": 0, "issues": []},
    "microsemantics": {"score": 0, "issues": []},
    "technical": {"score": 0, "issues": []},
    "trust": {"score": 0, "issues": []},
    "query": {"score": 0, "issues": []}
  },
  "priority_actions": []
}
```
