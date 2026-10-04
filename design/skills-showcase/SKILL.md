---
name: skills-showcase
description: >
  Generate a polished Remotion video and X thread showcasing the full agent skills inventory.
  Use when creating social media content about skills, rendering category-based skill visualizations,
  or producing animated showcases of agent capabilities. Triggers on "skills video", "showcase skills",
  "skills thread", "render skills", "social content for skills", or requests to visualize the skills inventory.
---

# Skills Showcase

Render a category-by-category animated skills showcase video (1080x1080, 30fps, ~48s) and produce
a 7-post X thread that maps skill clusters to concrete value.

## Quick Start

```bash
cd skills-showcase
npm install
npx remotion studio          # Preview in browser
npx remotion render SkillsShowcase out/skills-showcase.mp4
npx remotion render SkillsShowcase out/skills-showcase.gif --every-nth-frame=3
```

## Output Artifacts

- `out/skills-showcase.mp4` — Primary X upload (H.264, ~4.7 MB)
- `out/skills-showcase.gif` — Fallback/preview (~7 MB)
- `thread.md` — 7-post X thread copy

## Architecture

```
src/
├── index.ts                  # registerRoot entry point
├── Root.tsx                  # Composition registry (1080x1080, 30fps, 1440 frames)
├── SkillsShowcase.tsx        # Master timeline using <Series>
├── data/skills.ts            # Typed dataset: categories, skills, derived aggregates
├── scenes/
│   ├── Intro.tsx             # Title + subtitle + stats pills (4s)
│   ├── CategorySection.tsx   # Category label + staggered skill chips (2.67s each)
│   └── Outro.tsx             # Summary metric + tagline + CTA (4s)
└── components/
    └── SkillChip.tsx         # Reusable animated badge with spring entrance
```

## Data Model

Edit `src/data/skills.ts` to add or remove skills. The video re-renders deterministically from this dataset.

- **Category**: `{ id, label, color, order }`
- **Skill**: `{ slug, categoryId, shortDescription }`
- **Derived**: `totalSkills`, `totalCategories`, `skillsByCategory`

## Animation Conventions

All animations use Remotion frame-driven patterns only:

- `useCurrentFrame()` + `useVideoConfig()` for frame/fps
- `spring()` for entrances (damping: 200 for smooth, damping: 20 + stiffness: 200 for snappy)
- `interpolate()` with clamp for opacity and translation
- Zero CSS transitions or Tailwind animation utilities

## Timeline Pacing

| Scene | Frames | Duration |
|---|---|---|
| Intro | 120 | 4.0s |
| 15 categories × 80 | 1200 | 40.0s |
| Outro | 120 | 4.0s |
| **Total** | **1440** | **48.0s** |

## Customization

- **Add a category**: Add to `categories` array in `src/data/skills.ts`, update `Root.tsx` duration
- **Change colors**: Each category has a `color` hex in the dataset
- **Adjust pacing**: Modify `CATEGORY_DURATION` in `SkillsShowcase.tsx`
- **Thread copy**: Edit `thread.md` directly

## Thread Strategy

See [thread.md](thread.md) for the full 7-post thread. Structure:

1. Hook + video attachment
2. Why skills beat one-off prompts
3. Consciousness & memory cluster
4. Research & analysis cluster
5. Full-stack implementation coverage
6. Niche high-signal specialist skills
7. CTA and discussion prompt
