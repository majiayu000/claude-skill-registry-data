---
name: marp-presen-review
description: >
  Marp形式プレゼンテーションの専門レビュー・評価・改善スキル。
  10軸スコアリング（100点満点）で品質を定量評価し、具体的な改善コード付きで提案する。
  Use when the user asks to:
  - Review, evaluate, or critique a Marp presentation / プレゼンをレビュー / 評価 / 添削
  - Improve, polish, or upgrade existing slides / スライドを改善 / ブラッシュアップ
  - Check slide quality, score slides, or audit a deck / スライドの品質チェック / 採点
  - "このプレゼンどう？" "スライドを見てほしい" "プレゼン資料のフィードバック"
  Reads .md files with Marp frontmatter, scores across 10 dimensions, and outputs
  a detailed review report with concrete before/after code improvements.
  Works as a companion to the marp-slides skill (generation → review → improvement cycle).
---

# Marp Presen Review — Professional Evaluation & Improvement

## Workflow

### Phase 1 — Read & Parse

1. Read the target `.md` file
2. Verify Marp frontmatter (`marp: true`)
3. Split into individual slides (by `---` separator)
4. Count slides, identify slide classes, catalog layout components used

### Phase 2 — Evaluate (10-Axis Scoring)

Score each axis 1–10. See `references/scoring-rubric.md` for detailed criteria.

| # | Axis | Weight | Key Question |
|---|------|--------|-------------|
| 1 | Message Clarity | x2 | Each slide has exactly ONE clear message? |
| 2 | Story Structure | x2 | Logical narrative arc from opening to CTA? |
| 3 | Visual Hierarchy | x1.5 | Priority grasped in 3 seconds? |
| 4 | Information Density | x1.5 | Within 5-bullet / 12-word limit? |
| 5 | Layout & Whitespace | x1 | Grids, alignment, margins professional? |
| 6 | Typography | x1 | Fonts, sizes, emphasis consistent? |
| 7 | Color & Contrast | x1 | Palette limited, meaningful, accessible? |
| 8 | Visual Variety | x1 | No 3+ consecutive same-type slides? |
| 9 | Slide Titles | x1 | Titles are messages, not topic labels? |
| 10 | Technical Quality | x1 | Valid frontmatter, correct classes, no broken HTML? |

**Total: 130 raw → normalized to 100 points.**

### Phase 3 — Diagnose

For each issue, produce:

```
[Slide N] [Axis] Severity: HIGH/MEDIUM/LOW
Problem: (one sentence)
Before: (current code)
After: (improved code)
Rationale: (design principle reference)
```

See `references/common-antipatterns.md` for frequent issues and fixes.
See `references/design-checklist.md` for visual design verification.
See `references/story-evaluation.md` for narrative structure patterns.

### Phase 4 — Report

Output format:

```markdown
# Marp Presen Review Report

## Score Summary
| Axis | Score | Grade |
|------|-------|-------|
| ... | 8/10 | A |

**Total: XX / 100** — Grade: S/A/B/C/D

## Strengths (Top 3)
## Critical Issues (Must Fix)
## Improvement Suggestions (Should Fix)
## Minor Polish (Nice to Have)
```

Grades: **S** (90+), **A** (80–89), **B** (70–79), **C** (60–69), **D** (<60)

### Phase 5 — Improve

Ask user: "自動改善しますか？" If yes:

1. Apply all Critical + Improvement fixes
2. Restructure narrative arc if story score < 7 (use `references/story-evaluation.md`)
3. Write improved file (same path with `-improved` suffix)
4. Show before/after score comparison

## Integration with marp-slides

Evaluation criteria align with `marp-slides` quality rules:
- Same CSS theme compatibility (excel-theme)
- Same layout component vocabulary (`.columns`, `.card`, `.highlight`, etc.)
- Same content rules (1 idea/slide, bold key phrase, vary visual types)

## Quick Modes

| Mode | Phases | Trigger |
|------|--------|---------|
| Full review | 1→2→3→4→5 | "レビューして" "評価して" |
| Score only | 1→2→4 | "採点だけ" "スコアだけ" |
| Auto-improve | 1→2→3→5 | "自動改善して" "直して" |
