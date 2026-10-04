---
name: analyze-improve
description: Analyze template ratings, generate analysis docs, and auto-generate the next batch of motion animation templates based on learned preferences.
argument-hint: [batch-size]
---

# Analyze & Improve Motion Animation Templates

Automated cycle: read ratings -> analyze patterns -> update analysis docs -> generate next batch of templates.

## Rating System (v3 — Devils Advocate Reviewed)

Templates rated on 5 metrics, **1-4 forced-choice scale** (no middle option):

| Metric | Gut-check | What it captures |
|--------|-----------|-----------------|
| **impact** | "Grabs attention in first 0.5 seconds?" | First-frame wow |
| **finish** | "Any rough edges or janky transitions?" | Defect detection (polish) |
| **flow** | "Timing and rhythm feel intentional?" | Motion quality |
| **versatility** | "Works if I change the words entirely?" | Broad usability |
| **appeal** | "Would a TikTok creator choose this?" | Market demand |

**Why these 5 (not the original 5):**
- Craft → **Finish**: Craft correlated with Impact (both = "how much work"). Finish is orthogonal (defect detection)
- Novelty → **dropped**: Rots over time, order-dependent. Computed algorithmically via embeddings instead
- Concept → **Appeal**: Concept conflated cleverness + demand. Appeal = what matters for product
- **Versatility** added: Was missing and critical (template that only works for one joke = low value)
- **1-4 scale**: Forced choice eliminates "default to 2" bias. 4^5=1024 combinations vs 3^5=243

**Metric order randomized per template** to prevent autopilot fatigue.

**Format in `.template-ratings.json`:**
```json
{
  "tpl-kinetic-example": {
    "verdict": "liked",
    "scores": { "impact": 3, "finish": 4, "flow": 3, "versatility": 2, "appeal": 3 }
  }
}
```

- Historical templates (pre-R6): `verdict` only, `scores: null`
- New batches (R6+): both `verdict` and `scores`
- `verdict` derived from scores: avg ≥ 2.5 → "liked", else "disliked"
- Novelty = algorithmic (embedding cosine distance to nearest existing template)

## Full Process

### Phase 1: Read Current State

1. **Load ratings** from `.template-ratings.json`
2. **Load previous analysis** from `docs/fourth-round/analysis.md` (or latest round folder)
3. **Count current templates**: `ls src/motionGraphics/templates/Kinetic*.tsx | wc -l`

```bash
# Quick stats (v2 format)
python3 -c "
import json
d = json.load(open('.template-ratings.json'))
liked = sum(1 for v in d.values() if (v if isinstance(v,str) else v.get('verdict','')) == 'liked')
disliked = sum(1 for v in d.values() if (v if isinstance(v,str) else v.get('verdict','')) == 'disliked')
scored = sum(1 for v in d.values() if isinstance(v,dict) and v.get('scores'))
print(f'Liked: {liked}, Disliked: {disliked}, Multi-scored: {scored}, Total: {len(d)}')
"
```

### Phase 2: Analyze Patterns (Multi-Dimensional)

Analyze across ALL 5 dimensions, not just theme/category:

1. **Per-metric averages** — Which metric scores lowest across liked templates? That's the improvement target
2. **Metric correlations** — Does high impact always mean high craft? Or can they diverge?
3. **Weak dimension identification** — Templates with concept=3 but craft=1 → remake with better execution
4. **Novelty saturation** — Track which animation technique families are overrepresented
5. **Round-over-round trends** — Are metric averages improving or declining?

### Phase 3: Update Analysis Docs

Create `docs/<round-name>/` folder with:
- `analysis.md` — multi-dimensional analysis with per-metric breakdowns, not just theme tiers
- `liked.md` — liked templates with their 5 scores
- `disliked.md` — disliked templates grouped by which metric failed

### Phase 4: Generate Next Batch

#### Organization: By Animation Technique Family (NOT visual theme)

10 technique families, each gets its own agent:
1. Text Deformation (stretch, warp, morph)
2. Assembly & Build-Up (construct, grow, layer)
3. Novel Reveals (destruction, peel, dimensional, interference)
4. Digital Native Culture (2024-2026 apps, tools, platforms)
5. Material Physics (metal, fabric, organic, state change)
6. Light & Shadow (shadow play, backlight, painting, projection)
7. Typography Craft (variable font, spacing, baseline, composition)
8. Cultural Moments (trending aesthetics, music genres, film, subculture)
9. Rhythmic & Musical (beat sync, pulse, staccato, build/drop)
10. Minimal Innovation (new single-mechanic clean animations)

#### Batch Structure:
- Default: 10 agents × 16 templates = 160 templates
- Each agent: 4 sub-categories × 4 templates
- **Max 10 parallel agents** (laptop resource limit)

#### Multi-Dimensional Quality Gate — EVERY template must pass ALL:
- [ ] **Impact**: First frame is visually interesting (NOT a gradual opacity fade)
- [ ] **Craft**: ≥4 animated CSS properties, non-linear easing, alive hold phase, concept-driven exit
- [ ] **Flow**: Enter compressed to first 30%, cycle duration ≤1.3s, exit faster than enter
- [ ] **Novelty**: No existing template uses this exact animation mechanic (grep first!)
- [ ] **Concept**: The idea is clever, recognizable in ≤3 words, creators would search for it

#### Anti-Repetition Rules:
- Before creating each template, grep for similar concepts in existing templates
- No two templates from the same agent should use the same core animation pattern
- Track saturated technique families (spring/bounce: 97 templates, garble→resolve: 48+)
- Prioritize underused techniques (3D perspective, true randomness, word-level stagger)

#### Code Quality Spec (from analysis of liked templates):
- Use easeOutExpo or easeOutBack for enter (not linear)
- Hold phase MUST have subtle motion (breathing, oscillation, shimmer)
- Exit must be concept-driven, not just opacity fade
- Typography oversized: clamp(36px, 11-15vw, 200px)
- Color serves concept (not arbitrary rainbow)
- Background establishes a "world" (unless minimal)

### Phase 5: Self-Improvement

After each cycle:
1. Compare per-metric averages to previous round — are scores improving?
2. Identify the weakest metric across the batch — that's the focus for next round's prompts
3. Check if any technique family produced 0 likes — retire it
4. Check if novelty scores are dropping — signal of saturation
5. Update this SKILL.md if the process needs adjustment

## Key Files

| Purpose | Path |
|---------|------|
| Ratings data (v2) | `.template-ratings.json` |
| Latest analysis | `docs/fourth-round/analysis.md` |
| All analysis rounds | `docs/first-round/`, `docs/second-round/`, `docs/third-round/`, `docs/fourth-round/` |
| Template files | `src/motionGraphics/templates/Kinetic*.tsx` |
| Template registry | `src/motionGraphics/index.ts` |
| Template base class | `src/motionGraphics/KineticBase.tsx` |
| Registry system | `src/motionGraphics/registry.ts` |
| Add-template skill | `.claude/skills/add-template/SKILL.md` |

## Example Invocations

```
/analyze-improve           # Full cycle: analyze + generate 160 templates
/analyze-improve 80        # Analyze + generate 80 templates (5 agents × 16)
/analyze-improve analyze   # Analysis only, no generation
/analyze-improve generate  # Skip analysis, generate from existing rules
```
