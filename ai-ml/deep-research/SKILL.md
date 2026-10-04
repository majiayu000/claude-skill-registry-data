---
name: deep-research
description: Multi-source web research for non-trivial questions.
---

# Deep Research Skill

Systematic approach to thorough research on any topic.

## Research Process

- **Scope:** define core questions, boundaries, success criteria, and planned sources.
- **Gather:** broad overview → targeted deep dives. Tools: WebSearch, WebFetch, Context7, Explore agent. Sources: official docs, academic papers, industry reports, community (GitHub, forums).
- **Validate:** cross-reference claims across sources, verify publication dates for currency, note conflicts and controversies, assess source credibility and evidence quality (facts vs. opinions, methodology rigor, reasoning).
- **Synthesize:** executive summary (3-5 bullets) → detailed findings by theme → critical analysis (evidence quality, conflicts, gaps) → practical implications → cite sources with dates → state confidence level.

## Special Considerations

For AI/ML, current events, technical evaluations, or business topics: read `references/domain-tips.md` for domain-specific cautions.

## Quality Checklist

Before concluding research, verify:

- [ ] Multiple authoritative sources consulted
- [ ] Recent information included (check dates)
- [ ] Key perspectives represented
- [ ] Evidence quality assessed
- [ ] Conflicts/controversies noted
- [ ] Practical implications identified
- [ ] Sources properly cited
- [ ] Confidence level stated
- [ ] Gaps/limitations acknowledged
- [ ] Actionable conclusions provided

## Tools to Use

- **WebSearch** / **WebFetch**: general information, current events, specific URLs.
- **Context7**: library/framework documentation.
- **Agent (`general-purpose` subagent)** — pinned **opus/medium**: multi-step investigations synthesize across sources, not just locate, so route them here rather than to Haiku `Explore` (routing + why → `~/.claude/references/claude-models.md`).

## Iteration

If conflict, expand search and present multiple viewpoints; if insufficient, try different sources or terms; if outdated, search for recent sources; if gaps, ask the user to clarify.
