---
name: rsi-phase3-metasketills
description: "RSI Phase 3: Cross-domain metasketill extraction"
---
## RSI Phase 3: Cross-Domain Metasketill Extraction

### Purpose
Extract reusable domain-agnostic metasketills from accumulated Phase 2 learned proposals, promote to permanent core rules (P8, P9, etc.), and build the pattern library for Phase 4 Benchmark.

### Phase 3 Trigger ✅
Condition: Phase 2 acceptance rate ≥ 0.5 (≥5 learned/10 cycles)  
Status: Infrastructure documented, data accumulation pending

### Metasketill Definition
Domain-agnostic patterns vs. domain-specific skills.

### Extraction Algorithm (3-Phase)
- **3A**: Accumulate from improvements.jsonl, cluster by family
- **3B**: Abstract each cluster to domain-agnostic pattern (name, trigger, recipe, anti-patterns)  
- **3C**: Validate against ≥2 new files, promote to permanent rules (P8, P9+)

### Success Criteria
≥3 metasketills + ≥2 permanent rules → transition to Phase 4

### Phase 3 → Phase 4
Export patterns to Benchmark schema, build test cases, publicly make Benchmark Suite.

### Safety
Never promote failing validations; log all extractions; keep learned-proposal fallback.

### Files
- Skill: rsi-phase3-metasketills/SKILL.md
- Library: rsi-pattern-library/ (emerging)  
- World Model: phase3 design log
- Logging: improvements.jsonl with "metasketill" tag

### Checklist
- [ ] Accumulate 50-cycle learned proposals
- [ ] Cluster by pattern family (timing/quality/safety)
- [ ] Abstract to domain-agnostic templates
- [ ] Validate against 2+ new files
- [ ] Promote 3+ as permanent rules (P8, P9, P10)
- [ ] Measure acceptance rate before/after

### Expected Outcome
3-5 reusable metasketills, 2-3 permanent rules, measurable acceptance rate improvement, Phase 4 benchmark foundation.
---
RSI Phase 3: Extract cross-domain metasketills from learned proposals, promote to permanent core rules, build Pattern Library for Phase 4 Benchmark.