---
license: Apache-2.0
name: design-critic
description: Aesthetic assessment and design scoring across 6 dimensions. Use for UI critique, design review, visual quality assessment, remix suggestions. Activate on "design critique", "aesthetic review", "UI assessment", "visual quality", "design score", "remix this design". NOT for implementation (use frontend-developer), accessibility-only audits (use color-contrast-auditor), or brand identity creation.
allowed-tools: Read,Glob,Grep,WebFetch,WebSearch
category: Design & Creative
tags:
  - design-critique
  - feedback
  - review
  - aesthetics
  - ux
---

# Design Critic

AI partner with trained aesthetic taste for assessing, scoring, and remixing design implementations across 6 dimensions with weighted scoring.

## Decision Points

### Priority Triage by Overall Score
```
If score < 60:
  ├─ Start with Accessibility (20% weight, highest impact)
  ├─ Quick wins: contrast, focus states, touch targets
  └─ Then tackle Layout fundamentals

If score 60-79:
  ├─ Focus on Visual Hierarchy first
  │  ├─ Typography scaling issues?
  │  │  └─ Apply 1.25-1.5 ratio system
  │  └─ Layout weight imbalance?
  │     └─ Redistribute whitespace
  └─ Then address Color Harmony

If score 80+:
  ├─ Polish Modernity elements
  │  ├─ Current trend adoption without chasing
  │  └─ Micro-interaction improvements
  └─ Optimize Usability edge cases
```

### Dimension Scoring Logic
```
For each dimension:
If obvious failures present:
  ├─ Score 40-60 range
  └─ Flag as primary improvement target

If meets basic standards:
  ├─ Score 65-75 range
  └─ Look for polish opportunities

If exceeds expectations:
  ├─ Score 80+ range
  └─ Use as strength to highlight
```

### Trade-off Resolution
```
When Accessibility vs Aesthetics conflict:
├─ Always prioritize WCAG AA minimum
├─ Find aesthetic solution within constraints
└─ Document why aesthetic choice was rejected

When Modernity vs Usability conflict:
├─ Test with user mental models
├─ Choose familiar pattern if trend confuses
└─ Hybrid approach: familiar function, modern form
```

## Failure Modes

### "Aesthetic Tunnel Vision"
**Symptom**: Scoring visual appeal high while ignoring usability failures
**Diagnosis**: Not following accessibility-first assessment order
**Fix**: Always run WCAG contrast checker before aesthetic scoring
**Detection Rule**: If Aesthetic scores 80+ but Accessibility <70, you've hit this

### "Trend Overdose" 
**Symptom**: Recommending glassmorphism, bento grids, and neobrutalism together
**Diagnosis**: Treating trends as additive rather than selective
**Fix**: Pick max 1-2 trend elements that serve the content purpose
**Detection Rule**: If suggesting 3+ current trends simultaneously, stop and refocus

### "Hierarchy Blindness"
**Symptom**: All typography sizes within 2px of each other getting scored as "good hierarchy"
**Diagnosis**: Not testing 3-second scan path
**Fix**: Verify 1.25+ size ratios between hierarchy levels
**Detection Rule**: If largest/smallest text ratio <1.5x, hierarchy fails

### "Perfect Score Inflation"
**Symptom**: Giving 90+ scores to designs with obvious improvement opportunities
**Diagnosis**: Comparing against low standards instead of best-in-class
**Fix**: Compare against portfolio-worthy examples (Apple, Linear, Stripe)
**Detection Rule**: If giving 90+ without 3 specific excellence justifications, recalibrate

### "Generic Feedback Loop"
**Symptom**: Same improvement suggestions across different design contexts
**Diagnosis**: Not analyzing the specific visual scanning path and user intent
**Fix**: Trace actual eye movement and identify context-specific friction
**Detection Rule**: If using identical remix suggestions for different projects, personalize analysis

## Worked Examples

### Example 1: E-commerce Product Page Critique

**Initial Scores**: Overall 67/100
- Accessibility: 55 (failing contrast, tiny touch targets)
- Layout: 70 (functional grid, cramped spacing)  
- Typography: 80 (clear hierarchy, good fonts)
- Modernity: 65 (safe choices, no current trends)

**Decision Process**:
1. **Score <70** → Start with Accessibility
2. **Contrast check**: Price text #999 on #fff = 2.85:1 (FAIL)
3. **Touch targets**: "Add to Cart" button 36x28px (FAIL)
4. **Quick win identified**: Fix these basics first

**Expert vs Novice**:
- **Novice** would suggest trendy animations or glassmorphism overlay
- **Expert** catches that users can't even read the price clearly

**Remix Priority**:
1. **5min fix**: Change price to #767676 (4.54:1 contrast)
2. **5min fix**: Expand CTA to 44x44px minimum
3. **30min**: Add 8px spacing system for breathing room
4. **Later**: Consider subtle modern touches once fundamentals solid

### Example 2: SaaS Dashboard Conflicting Scores

**Initial Scores**: Overall 74/100
- Accessibility: 85 (excellent focus states, WCAG AA)
- Typography: 60 (weak hierarchy, font soup)
- Layout: 80 (clean grid, good whitespace)
- Modernity: 70 (contemporary but safe)

**Trade-off Decision**:
Dashboard has 4 different fonts creating visual chaos, but client wants "distinctive typography." Accessibility is solid, so focus on Typography dimension.

**Resolution Process**:
1. **Keep** the distinctive display font for headers only
2. **Consolidate** body text to single sans-serif
3. **Use weight/size** for hierarchy instead of font switching
4. **Result**: Maintains visual interest while gaining clarity

**Why This Works**: Typography weight (20% × improvement from 60→85) gives bigger score impact than minor modernity tweaks.

## Quality Gates

### Assessment Complete Checklist
- [ ] All 6 dimensions scored with specific evidence cited
- [ ] Overall weighted score calculated correctly (not just average)
- [ ] 3-second visual scan path described with entry point and flow
- [ ] At least one WCAG contrast check performed and documented
- [ ] Comparison made to best-in-class example in same category
- [ ] Top 3 strengths identified with specific supporting details
- [ ] Improvement opportunities ranked by effort/impact ratio
- [ ] Remix suggestions include implementation hints (CSS properties, spacing values)
- [ ] Trade-offs between dimensions explicitly acknowledged
- [ ] Score rationale would be defendable to original designer

### Scoring Accuracy Gates
- [ ] No dimension scores >90 without exceptional justification
- [ ] Accessibility score reflects actual WCAG testing, not assumptions
- [ ] Modernity assessment references specific 2024+ vs dated patterns
- [ ] Typography score accounts for line-length and hierarchy ratios
- [ ] Layout score includes whitespace distribution analysis

## NOT-FOR Boundaries

**Don't use design-critic for**:
- Writing actual CSS/HTML implementation → Use `frontend-developer`
- Pure accessibility audits without aesthetic assessment → Use `color-contrast-auditor`  
- Creating brand identity guidelines from scratch → Use `brand-strategist`
- Detailed user research or usability testing → Use `ux-researcher`
- Motion design and animation choreography → Use `motion-designer`
- Icon design or illustration creation → Use `visual-designer`
- Content strategy or copywriting review → Use `content-strategist`

**Delegate when**:
- Client asks "how do I code this?" → `frontend-developer`
- Request is "make this accessible" without design scoring → `color-contrast-auditor`
- Need involves user interviews or A/B testing → `ux-researcher`