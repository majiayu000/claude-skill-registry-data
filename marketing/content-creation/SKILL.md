---
skill_id: content-creation
name: Content Creation
description: "Write long-form and channel content — articles, blog posts, documentation, newsletters, whitepapers, books, copywriting. The CMO office's primary execution skill for anything written."
version: 1.0.0
category: content-creation
office: CMO
lead_agent: content-strategist
triggers:
  - write
  - article
  - blog
  - docs
  - documentation
  - newsletter
  - book
  - whitepaper
  - content
  - copywriting
  - changelog
  - release notes
  - video script
  - knowledge base
  - email sequence
collaborates_with:
  - seo-specialist
  - behavioral-designer
  - security-analyst
  - marketing
  - search-visibility
---

# Content Creation -- Domain Dispatcher

> Office: CMO | Lead: content-strategist
> Sub-skills: 7 | Frameworks: AIDA, Diataxis, StoryBrand, PAS

## Purpose

The CMO's primary execution skill for all written content across every format and channel. Covers articles, whitepapers, newsletters, documentation, changelogs, video scripts, social media copy, and investor content. The content-strategist agent leads this domain, absorbing the former content-creator role via Op-D with dedicated modes for each content format.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| long-form editorial, thought leadership, blog posts | Article (mode) | article-writer/SKILL.md |
| API docs, user guides, technical manuals, knowledge bases | documentation-writer | documentation-writer/SKILL.md |
| subscriber content, digest formats, recurring content | Newsletter (mode) | newsletter-writer/SKILL.md |
| platform-adapted short-form, cross-posts | Social Media (mode) | social-media-strategist/SKILL.md |
| structured technical book chapters, outlines | Technology Book (mode) | technology-book-writer/SKILL.md |
| YouTube, webinar, product demo, tutorial scripts | Video Script (mode) | video-script-writer/SKILL.md |
| research-backed authoritative technical documents | Whitepaper (mode) | whitepaper-writer/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-cmo`
- Task contains keywords: write, article, blog, docs, documentation, newsletter, book, whitepaper, content, copywriting, changelog, release notes, video script, knowledge base, email sequence
- Executive router detects content production, written output, or editorial signals
- Other Maxim skills route written execution here (e.g., investor-pitch-writer routes to content-creation for written execution)

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Frameworks: AIDA (attention/interest/desire/action), Diataxis (documentation framework), StoryBrand (narrative structure), PAS (problem/agitate/solve), Elaboration Likelihood Model (persuasive content)
- Auto-loops: marketing skill (campaign channels), search-visibility skill (SEO/AEO), behavior-science-persuasion skill (persuasive copy psychology)

## External Sources

- Primary: community-packs/claude-skills-library/marketing-skill/ (content strategy patterns, copywriting frameworks, platform-specific conventions)
- VoltAgent: community-packs/voltagent-subagents/ (content specialists)
- Conflict resolution: Maxim ALWAYS WINS

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
