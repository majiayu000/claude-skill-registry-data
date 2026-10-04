---
name: social-content
description: Use when drafting truthful, channel-specific social or editorial content for X, Reddit, Hacker News, Product Hunt, blogs, or newsletters from supplied source material, or planning approved data visuals for those channels. Prefer a connected Canva capability for visual authoring when available, with local rendering as fallback. Use for blog posts from existing social content. Do not use for LinkedIn-specific workflows, publishing, outreach, engagement, fabricated testimonials, or unsourced promotional claims.
---

# Social content

Create unpublished drafts from approved source material. Keep every non-obvious
claim traceable to a real, named, linkable source; distinguish verified facts,
approved positioning, user-provided opinion, inference, and unknowns; and leave
publication decisions to the user.

## Boundaries

- Do not invent metrics, outcomes, testimonials, partnerships, capabilities,
  pricing, urgency, or personal experience.
- Do not publish, schedule, post, reply, vote, contact users, access social
  sessions, or create accounts.
- Research current facts only when explicitly requested and approved. Cite
  named, linkable sources and preserve important caveats.
- Do not impersonate people or communities, disguise promotion, or use fake
  scarcity, outrage bait, undisclosed sponsorship, or instructions to evade
  platform or community rules.
- Do not turn a goal, forecast, plan, or aspiration into a reported result.
- Do not own LinkedIn-specific post drafting, carousel production, publishing,
  engagement, lead follow-up, or workspace state; hand those requests to the
  corresponding `linkedin-*` skill.
- Do not use unrelated private or internal communications as source material;
  this workflow is for user-provided or approved public-content drafts.
- Before presenting or saving a public draft, check supplied material for
  secrets, credentials, confidential business details, and personal data. Do
  not carry sensitive content into public copy; flag anything that needs the
  user's explicit publication decision.
- Do not hardcode personal or product identity. Use supplied brand rules and
  assets, and ask for the exact name, title, and domain before rendering a
  footer.
- Do not create files, start browsers, render images, or install tools until the
  user explicitly approves that work.

## Workflow

Read [references/workflow.md](references/workflow.md) for the full content-pack,
research, review, file-output, blog, and completion-checklist workflow. For
visual assets, also read [references/visuals.md](references/visuals.md).

1. Confirm the channel, audience, objective, topic, and source material. If a
   content-pack input is missing, ask for it instead of guessing.
2. If factual research is requested, build a short evidence ledger with source,
   claim, status, and caveat. If evidence is weak, label the draft opinion.
3. Draft for the selected channel using the compact guidance below. Load
   `humanizer` after the structure is complete when that companion skill is
   available; otherwise perform the same factual and voice-preservation audit
   directly.
4. Fact-check every claim, label the draft unpublished, and present it for
   review. Revise before saving.
5. After explicit approval, save under `<project-root>/sm_<slug>/posts.md` with
   channel headings and a `Sources` section. Resolve `<project-root>` before
   writing; never publish or commit.

## Channel targets

| Channel         | Shape                                                             |
| --------------- | ----------------------------------------------------------------- |
| X               | Concise post/question; 3-6 hashtags; URL counts as 23 characters. |
| Reddit          | Relevant context, useful contribution, transparent affiliation.   |
| Hacker News     | Factual/technical; lead with what was made and why.               |
| Product Hunt    | Maker context, solution, limits; no manufactured proof.           |
| Blog/newsletter | Evidence, examples, takeaway, sources.                            |

Use the source's own words only for necessary exact names, titles, or numbers;
paraphrase everything else. Lead with the strongest real finding, explain the
mechanism, and end with a concrete implication rather than a generic CTA.

## Blog and visual branches

For a blog from existing social content, expand the core insight into a thesis,
evidence-backed sections, implications, and sources. Save `blog.md` only after
approval. For visual assets, read [references/visuals.md](references/visuals.md)
before proposing deliverables. When a connected Canva capability is available,
also read [references/canva-workflow.md](references/canva-workflow.md) and use
Canva as the preferred authoring path. Wait for approval before creating or
exporting any visual.

Every handoff includes sources, claims needing approval, required disclosures,
and wording that must not be presented as fact.
