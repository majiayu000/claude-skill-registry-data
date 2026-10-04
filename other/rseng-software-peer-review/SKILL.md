---
name: rseng-software-peer-review
description: >-
  Covers community peer review of research software: preparing a package for
  JOSS, pyOpenSci or rOpenSci submission, self-checking against their review
  criteria before submitting, writing the paper or statement of need,
  responding to reviews, and acting as a reviewer or CODECHECK-style
  codechecker who executes the artifact. Use when the user mentions JOSS,
  pyOpenSci, rOpenSci or CODECHECK, wants to submit software for peer review
  or publication, asks whether their package is review-ready, or is reviewing
  someone else's research software for one of these venues. (PR-level code
  review is rseng-version-control-review; overall publication channel strategy
  is rseng-software-publishing.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Peer review of research software

Software peer review is the publication pathway where the SOFTWARE is
the reviewed artifact: JOSS (any language), rOpenSci (R) and
pyOpenSci (Python) run open, constructive reviews against public
checklists, and CODECHECK issues certificates that a paper's
computations were independently executed. For a maintainer, review
readiness is a concrete bar to build toward; passing it earns a
citable publication (JOSS papers get DOIs) and a community quality
mark. This is review of the whole package - distinct from PR-level
code review (rseng-version-control-review).

## Pre-submission: self-review against the real checklist

Run the target venue's own checklist against the repository and fix
failures BEFORE submitting - reviewers check exactly these:

- License: OSI-approved LICENSE file at the root (rseng-licensing).
- Documentation entry points: installation that works from a clean
  environment, usage examples that run, API docs for the public
  surface (rseng-documentation).
- Statement of need: who this is for and what gap it fills - in the
  README and (for JOSS) the paper; write it for the target
  researcher, not the maintainer.
- Tests that run in CI, covering the core claims of the software
  (rseng-testing, rseng-ci-cd); reviewers will run them.
- Community files: contributing guidelines and code of conduct
  (rseng-community-governance).
- Citation metadata and archiving: CITATION.cff, and a Zenodo (or
  equivalent) archive with DOI at acceptance
  (rseng-citation-metadata, rseng-publishing-releasing).
- AI-usage disclosure: JOSS now asks about AI use in the submission -
  the project's aidecl.yaml (rseng-ai-declaration) is exactly the
  honest record to answer from.

Scope check before effort: each venue defines in-scope package types
and substantiality; read the venue's scope page first and say
honestly if the project is not there yet.

## The JOSS paper: the user writes it

Short by design (750-1750 words): summary for
non-specialists, statement of need, rough state of the field
(neighboring tools and how this differs - rseng-discovery and
rseng-software-reuse habits help here), acknowledgements, references
with DOIs. It reviews the software; do not pad it into a methods
paper. The agent's role is support only: outline against the
venue's template, gather the material, check the draft against the
criteria and verify its citations - never produce a
submission-ready manuscript; authorship and every signed claim stay
with the user (rseng-science-communication states the same boundary;
JOSS itself asks about AI involvement - answer from aidecl.yaml).

## Responding to reviews

Reviews are public issue threads. Respond to every point (fix,
discuss, or explain why not), push commits as you go, and summarize
changes when done. Tone: reviewers are volunteers improving your
software - thank them, and disagree with reasons, not defensiveness.

## Reviewing and codechecking

When the user is the reviewer:

- Work through the venue checklist honestly - install from scratch
  in a clean environment (rseng-reproducible-environments), run the
  tests, run the examples; "it probably works" is not a review.
- File findings as actionable issues, most important first;
  distinguish must-fix (checklist failures) from suggestions.
- CODECHECK mode: execute the paper's workflow, record what
  reproduced (with outputs), what did not, and produce the
  certificate-style summary of exactly what was checked.
- Constructive is the norm in this ecosystem: the goal is
  acceptance-after-improvement, not gatekeeping.

## Working with this skill

This skill is source-independent: its authority is the venues' own
review criteria and guides linked below.

Learn more (verified):
  - https://joss.readthedocs.io/en/latest/review_checklist.html -
    JOSS review checklist
  - https://joss.theoj.org - Journal of Open Source Software
  - https://devguide.ropensci.org - rOpenSci packaging and review
    guide
  - https://www.pyopensci.org/software-peer-review/ - pyOpenSci peer
    review guide
  - https://codecheck.org.uk/ - CODECHECK independent execution
    certificates

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - JOSS asks about AI use
- rseng-citation-metadata - CITATION.cff and DOI at acceptance
- rseng-discovery - state-of-the-field section material
- rseng-reproducible-environments - clean-room installs for reviewing
- rseng-software-publishing - JOSS within the channel mix
- rseng-version-control-review - PR-level review is distinct

<!-- related-skills:end -->
