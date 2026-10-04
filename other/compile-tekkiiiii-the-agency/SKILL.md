---
name: compile
description: Load the marketing assessment pipeline lessons, pitfalls, and quality checklist before generating or reviewing a client deck. Invoke with /compile before any pipeline run to ensure all 24 learned pitfalls are loaded into context. Also use after a pipeline run to verify output against the quality checklist.
---

# /compile — Marketing Assessment Pipeline Guard

Load the full pipeline reference before generating or reviewing a marketing assessment deck.

## On invoke

1. Read `~/.claude/skills/marketing-assessment-pipeline/SKILL.md` — the full pipeline skill with architecture, key files, Supabase access, and all 24 learned pitfalls
2. Read `~/.claude/memory/lessons/marketing-pipeline.md` — detailed lessons from production runs
3. Resolve brand colors from `{agency-root}/design-system/brands/{brand}.json` (see `strategic-deck` skill's Palette section for the mapping) — if the operator keeps a separate client brand-color log, check that too

## Output

After loading, confirm:
```
PIPELINE GUARD LOADED
- 24 pitfalls active (Vietnamese diacritics, PPTX layout, font installation, CTA rules)
- Brand colors resolved (design-system SSOT defaults + client colors)
- Quality checklist ready (12 items)
- Deck spec: `{agency-root}/skills/strategic-deck/SKILL.md` (implement directly with pptxgenjs — no template.js ships)
- Render: node deck.js → soffice --convert-to pdf
- Review protocol: 4 parallel critics (Design, Content, Marketing, Ops)

Ready to build or review.
```

## When to use

- Before generating a new client assessment deck
- Before reviewing an existing deck for quality
- Before re-running the pipeline after fixes
- When debugging pipeline issues (font rendering, layout overflow, diacritics)
