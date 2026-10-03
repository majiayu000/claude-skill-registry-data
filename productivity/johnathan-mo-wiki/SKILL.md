---
name: johnathan-mo-wiki
description: Use when a task should consult Johnathan Mo's personal LLM wiki, memory card, public profile, biography, projects, timeline, YouTube history, career/recruiting context, or source-backed personal facts. Trigger on requests like "use my wiki", "what do you know about me", "draft from my context", "point an LLM to my profile", or "Johnathan Mo context".
---

# Johnathan Mo Wiki

Use Johnathan Mo's Karpathy-style LLM wiki as the factual context layer. The wiki is source-backed and separate from the writing-style skill: use this skill to know what is true or uncertain, then use `johnathan-writing-style` when the task is to write in Johnathan's voice.

## Canonical Locations

- Local schema: `/Users/johnathanmo/johnathan-llm-wiki/AGENTS.md`
- Local wiki index: `/Users/johnathanmo/johnathan-llm-wiki/wiki/index.md`
- Local overview: `/Users/johnathanmo/johnathan-llm-wiki/wiki/overview.md`
- Local source notes: `/Users/johnathanmo/johnathan-llm-wiki/wiki/sources/`
- Raw harvested sources: `/Users/johnathanmo/johnathan-llm-wiki/raw/`
- Public-safe LLM page: `https://site-ku6ol9inj-johnathans-projects-b2a37f0a.vercel.app/llm-wiki.md`
- Compact public entrypoint: `https://site-ku6ol9inj-johnathans-projects-b2a37f0a.vercel.app/llms.txt`

Prefer the local wiki when available. Use the public-safe URL when the user wants a link to share with another LLM or when local files are not available.

## Workflow

1. Read `AGENTS.md` first if maintaining or changing the wiki.
2. Start with `wiki/index.md`, then open only the specific linked pages needed for the task.
3. Check `wiki/open-questions.md` before making strong claims.
4. For bios and public summaries, prefer `wiki/bio-drafts.md`, `wiki/overview.md`, `wiki/timeline.md`, `wiki/entities/johnathan-mo.md`, and relevant project/topic pages.
5. For writing style, read `wiki/topics/writing-style.md` and use the `johnathan-writing-style` skill if available.
6. Cite source pages or raw source files for non-obvious claims when the output needs accuracy, reviewability, or public publication.

## Privacy And Source Rules

- Treat the local wiki as private by default.
- Do not publish raw private Gmail, Notion, or Drive material unless Johnathan explicitly asks and reviews it.
- Connector harvest notes in `raw/notion/` and `raw/gmail/` are summaries, not full exports. Re-query connectors before exact quotes, sensitive claims, or high-stakes decisions.
- The deployed Vercel export is public-safe and intentionally incomplete. Do not assume it contains everything in the private wiki.
- Flag contradictions or stale claims instead of smoothing them over, especially internships, GPA, subscriber counts, sponsorships, and active project status.

## Output Style

Be concrete and source-aware. Distinguish:

- "Known from the wiki" for source-backed facts.
- "Suggested positioning" for framing or synthesis.
- "Open question" for claims that need another ingestion pass.

When drafting externally visible text, avoid overclaiming. Pair ambition with proof, artifacts, or context from the wiki.
