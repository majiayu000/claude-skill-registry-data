---
name: rseng-science-communication
description: >-
  Covers communicating research software outward to research audiences:
  supporting the user's software papers (JOSS/SoftwareX-style) with outlines,
  gathered material and structure - never writing a submission-ready
  manuscript - plus release announcements, lay summaries of what the software
  does, talk and poster outlines, blog posts, and making a package findable to
  its intended users. Use when the user wants to announce, present, promote or
  explain their research software, asks for help with a software paper, talk
  abstract or release post, or when a mature package has no visibility beyond
  its authors. In-repo docs live in rseng-documentation; public and
  citizen-science narrative in rseng-storytelling; venue mechanics and review
  preparation in rseng-software-peer-review.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Communicating research software

Software nobody hears about is software nobody reuses, cites or
funds. Communication is part of the engineering lifecycle, not an
afterthought: every release, paper and talk is a chance to reach the
researchers the software was built for. An agent is well placed to
draft these artifacts FROM the repository - README, changelog,
docs and citation metadata already contain most of the raw material.

## Know the audience before drafting

The same software needs different words for different readers:

- Domain researchers (potential users): what problem it solves,
  in domain language - never implementation-first.
- Fellow developers (potential contributors): architecture, stack,
  where help is wanted.
- Non-specialists (funders, institutions, the public): the lay
  summary - why the research matters and what the software enables,
  zero jargon, one analogy allowed.

Lead every artifact with the problem solved, not the technology
used.

## Software papers: support, never authorship

A software paper (JOSS, SoftwareX and domain journals) is the
citable face of the package - and it is the USER's publication, not
the agent's. The boundary is firm: help with the outline, the
research and the brainstorming; gather the raw material (the
README's purpose section informs the summary, issues and user
questions inform the statement of need, the neighbor comparison
from rseng-discovery and rseng-software-reuse informs
state-of-the-field); propose structure per the venue's template;
critique and fact-check the user's draft
(rseng-fact-checking, rseng-citation-hygiene). Never deliver a
finished, submission-ready manuscript - a publication that needs an
expert's authorship gets an expert's authorship, and the user
verifies every claim they sign (rseng-human-verification). AI
assistance with the paper is disclosed per the venue's policy
(rseng-ai-declaration). Venue mechanics and review preparation live
in rseng-software-peer-review; citation plumbing in
rseng-citation-metadata.

## Release communication

For every meaningful release (rseng-publishing-releasing):

- A human-readable announcement distilled from the changelog: 2-3
  headline changes phrased as user benefit ("fits are ~4x faster on
  large datasets"), breaking changes with migration one-liners, and
  install/upgrade command.
- Post where the software's users actually are - mailing list,
  community forum, institute news, social media - not everywhere.
- Time cost is minutes when drafted from a maintained changelog;
  that is the argument for maintaining one.

## Talks, posters and demos

- Talk outline rule: one idea per slide, problem before solution,
  a live or recorded demo beats architecture diagrams for software
  talks.
- Posters: the software's one-sentence purpose in the title region,
  a QR code to the repository, and a runnable example as the
  centerpiece.
- Prepare the demo against dependency rot: pin the demo environment
  (rseng-reproducible-environments) and have a recorded fallback.

## Findability and sustained visibility

- The README is the landing page: purpose in the first paragraph,
  badges that carry information (CI, docs, DOI, review acceptance),
  a quickstart that works (rseng-documentation).
- Register where the community looks: a Research Software Directory
  instance (rseng-software-reuse), domain registries, and the
  package index's metadata fields (rseng-fair-software).
- Blog posts for milestones and interesting internals: a "how we
  made X 10x faster" post recruits both users and contributors.
- Accessibility applies to communication too: alt text on figures,
  readable contrast on slides and posters (rseng-ux-accessibility).

## Working with this skill

This skill is source-independent: its authority is the community
communication guidance linked below.

Learn more (verified):
  - https://devguide.ropensci.org - rOpenSci dev guide (includes
    package promotion/marketing)
  - https://joss.theoj.org - JOSS, the software-paper venue

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-metadata - DOIs and citable releases
- rseng-documentation - README is the landing page
- rseng-fact-checking - fact-check the draft claims
- rseng-publishing-releasing - announcements draft from changelogs
- rseng-software-peer-review - venue mechanics and review prep
- rseng-storytelling - narrative spine for broad audiences

<!-- related-skills:end -->
