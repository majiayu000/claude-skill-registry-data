---
name: release-announcement-writer
description: Write release notes, GitHub release copy, website update blurbs, and short launch posts from changelogs, git diffs, README changes, shipped feature lists, or product/system updates. Use when the user asks to announce a release, summarize what changed, prepare public launch copy, write a changelog, turn implementation notes into marketing-safe copy, or create LinkedIn/GitHub/X posts for a new version.
---

# Release Announcement Writer

## Overview

Use this skill to turn a shipped change into clear public release communication. The output should be accurate, concrete, and safe to publish: what changed, why it matters, who it helps, where to try it, and what to do next.

## Workflow

1. Gather source material: changelog, release tag, README diff, commit list, issue list, screenshots, demo links, website URLs, and target audience.
2. Separate facts from interpretation. Facts include version, date, links, changed files, features, fixes, and install steps. Interpretation includes value proposition, positioning, and social copy.
3. Identify the release tier:
   - `patch`: fixes, docs, copy, small polish.
   - `minor`: new skill, new workflow, new install path, meaningful usability improvement.
   - `major`: compatibility change, large repositioning, or breaking behavior.
4. Draft the core release summary in plain language before writing channel-specific variants.
5. Write only claims supported by the source material. Avoid inflated wording such as "revolutionary", "first", "complete", or "production-grade" unless the source proves it.
6. Add links to the most useful destination: release tag, GitHub repo, website case study, docs, or demo asset.
7. Finish with a short verification checklist: links work, version is correct, screenshots/GIFs are public-safe, and private implementation details are absent.

## Output Set

Create only the formats the user needs. If they ask for a full launch pack, include:

- GitHub release notes: concise title, summary, highlights, install/upgrade notes, links.
- README or website blurb: 1 short paragraph that explains the user-facing value.
- Social post: 1 plain-language announcement with the repo/case-study link.
- Short version: 1-2 sentences for profile READMEs, cards, or newsletters.
- Optional changelog bullets: grouped under Added, Changed, Fixed, Docs, Safety.

## Voice

- Be specific and practical.
- Lead with the outcome, not the internal effort.
- Prefer "Added X so users can Y" over "Implemented X".
- Keep technical nouns when they matter to the audience.
- Avoid hype, vague AI claims, and unsupported metrics.

## Safety

- Do not publish private local paths, API keys, tokens, client names, internal prompts, logs, or deployment details.
- Do not claim compatibility with a platform unless the release material includes install or usage evidence.
- If source material is messy or private, rewrite from facts instead of quoting it.
- If screenshots or GIFs are included, confirm they contain only public-safe UI and assets.

## Reference Template

For a reusable structure, read `references/release-copy-template.md`.

## Final Response

Return the finished copy first. Then include a compact note listing source facts used, any assumptions, and links or assets that still need verification.
