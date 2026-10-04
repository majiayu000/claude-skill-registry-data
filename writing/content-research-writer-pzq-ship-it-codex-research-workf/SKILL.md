---
name: content-research-writer
description: >
  Research, summarize, synthesize, draft, revise, and polish source-grounded
  written content. Use when Codex needs to turn notes, documents, URLs,
  transcripts, or a topic into an article, blog post, newsletter, tutorial,
  technical explainer, case study, brief, or other prose; compare and integrate
  multiple sources; iterate an outline; strengthen a hook; preserve a supplied
  voice; or review a draft for flow, evidence, citations, clarity, and
  consistency. Typical triggers include 摘要, 总结, 文本整合, 资料整合, 写文章,
  改写, and 润色.
---

# Content Research Writer

Turn source material into clear prose without weakening the evidence boundary.

## Core Contract

- Select the smallest fitting mode: `summarize`, `synthesize`, `draft`, or
  `revise`.
- Infer routine preferences from the request and existing project conventions.
  Ask only when a missing choice would materially change the result.
- Complete the requested artifact in one pass unless the user asks for
  section-by-section collaboration or approval checkpoints.
- Preserve the user's facts, intent, uncertainty, and voice. Never invent a
  citation, quotation, statistic, case, experience, or source location.
- Separate source statements, direct observations, assumptions, inferences,
  recommendations, and open questions.

## Mode Router

| Need | Mode | Primary output |
|---|---|---|
| Compress one source | `summarize` | Purpose-aware summary with limits |
| Integrate several sources | `synthesize` | Thematic narrative plus agreements, conflicts, and gaps |
| Create new content | `draft` | Evidence-backed outline and finished prose |
| Improve existing prose | `revise` | Meaning-preserving revision with important changes surfaced |

Combine modes when needed. For example, summarize each source internally,
synthesize across them, then draft the requested article. Do not expose every
intermediate artifact unless it helps the user verify or reuse the work.

## Workflow

1. Establish the content contract.
   - Identify the decision or reader need, audience, artifact type, desired
     length, tone, source boundary, citation style, and delivery format.
   - Identify the central claim or audience promise. If it is not yet supportable,
     label it provisional and state what evidence is missing.

2. Inventory the material.
   - Prefer provided files and structured data over re-parsing derived prose.
   - Track each usable source by title, author or organization, date, source
     type, URL or file locator, access level, and relevant sections.
   - Distinguish primary evidence from commentary, summaries, and discovery
     leads. Do not use a search snippet as evidence.

3. Research only as needed.
   - When current or external facts are required, use an appropriate search or
     retrieval skill and verify claims against the original page, paper,
     documentation, dataset, or official record.
   - Prefer primary and authoritative sources for load-bearing claims. Use
     secondary sources for context or discovery and label their role.
   - Record publication and access dates when freshness matters.

4. Build the argument before prose.
   - Draft a compact outline organized around the reader's question, not the
     order in which sources were collected.
   - Map every consequential factual claim to supporting evidence or mark it
     `needs evidence`.
   - Include important counterevidence, alternative explanations, limitations,
     and unresolved contradictions where relevant.

5. Write the requested artifact.
   - Lead with a concrete question, claim, observation, or useful tension.
   - Give each section one job. Use topic sentences, concrete evidence, and
     explicit transitions when the relationship is not obvious.
   - Prefer precise paraphrase over long quotation. Add a call to action only
     when the genre and user goal require one.
   - Preserve domain terminology where precision matters, then explain it at
     the audience's level.

6. Attach and verify citations.
   - Use the user's requested citation style, or concise linked citations for
     web prose when no style is specified.
   - Check that every citation supports the nearby claim, not merely the broad
     topic. Check names, dates, numbers, units, quotation wording, and locators.
   - Never turn a source's speculation into fact or conceal a material source
     disagreement through smooth prose.

7. Revise for usefulness and voice.
   - Remove repetition, generic framing, empty transitions, exaggerated
     significance, and unsupported certainty.
   - If the user supplies a writing sample, match its sentence rhythm,
     vocabulary, paragraphing, and level of formality without copying phrases.
   - Preserve deliberate ambiguity or caution when the evidence requires it.

## Summary Standard

A good summary is purpose-aware compression, not a shorter table of contents.

- State the source's central question or thesis.
- Preserve the method or evidence base when it affects credibility.
- Include the findings most relevant to the user's purpose.
- Retain limitations, uncertainty, scope, and important negative results.
- Distinguish what the source explicitly says from the writer's interpretation.
- For an executive summary, answer the decision question first, then give the
  minimum evidence and caveats needed to act.

## Synthesis Standard

Do not concatenate source summaries.

- Organize by theme, claim, mechanism, decision, or stage.
- Show where sources converge, diverge, or address different scopes.
- Explain plausible reasons for disagreement, such as population, method,
  definition, date, incentives, or evidence quality.
- Weight conclusions by evidence strength rather than source count.
- Preserve unique high-value cases and contradictory evidence.
- End with supported conclusions, unsupported possibilities, and evidence gaps.

## Draft And Revision Standard

- For a new draft, make the outline and claim-evidence relationship visible
  enough to audit without overwhelming the reader.
- For revision, preserve meaning by default. Flag any edit that changes a claim,
  commitment, interpretation, or level of certainty.
- Offer alternatives when voice or positioning is genuinely subjective; do not
  produce several cosmetic variants by default.
- Avoid generic hooks, fabricated first-person experiences, and statistics used
  only for drama.

## Default Delivery

Return the finished content first. Add only the supporting surfaces that matter:

1. source or claim notes for consequential factual work;
2. unresolved gaps or conflicts;
3. assumptions that materially shaped the draft;
4. suggested next revision when the result is intentionally incomplete.

## Quality Gate

Before delivery, verify:

- the artifact answers the requested reader need;
- the organization follows the argument, not source order;
- consequential claims are traceable;
- citations resolve and support the exact claims;
- facts, inferences, recommendations, and unknowns remain distinct;
- the summary has not dropped a material limitation;
- the synthesis has not flattened contradictions;
- the voice and length fit the audience and genre;
- no invented quote, statistic, source, experience, or citation remains.

## Boundaries

- Do not label ordinary multi-source synthesis a systematic review unless a
  protocol, search strategy, inclusion criteria, and evidence appraisal support
  that claim.
- Do not replace legal, medical, financial, ethical, or domain-expert review for
  high-stakes publication.
- Do not publish private, restricted, paywalled, or sensitive source content
  beyond the user's authorization.

## Provenance

This is an independently written Codex-native adaptation inspired by the public
`content-research-writer` concept in
`https://github.com/ComposioHQ/awesome-claude-skills/tree/master/content-research-writer`
at upstream commit `044d48b594f060c164f3b20fac9ea01374721bca` (accessed
2026-07-23). The upstream repository declared no license at the time of review,
so its instructional text is not vendored here.
