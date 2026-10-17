---
name: authoring-pipeline
description: Produce long-form work systematically — approved outlines, review passes, versioned builds, clean publishing.
version: 1
triggers: write a book, long-form, course modules, authoring, manuscript, publishing pipeline
category: Writing & documents
blurb: Produce long-form work systematically — approved outlines, recorded review passes, versioned builds.
archetype: knowledge
example: Plan the pipeline for turning my notes into a book.
---

# Authoring Pipeline

Books, courses, and long documents are builds: outline as contract, units with a point, review passes with records, and reproducible output.

## When to use
- Books, course modules, guides, strategy documents (the OCS-book / academy-module pattern).
- Converting research notes into publishable work.
- Any document that will have editions.

## Method
1. **Outline as contract**: chapters/modules → claims or learning outcomes; TOC approved BEFORE drafting; scope fences (what the work won't cover).
2. **Drafting loop**: small units; each unit has one point (courses: one testable outcome); examples before abstractions; running style sheet + glossary for consistency.
3. **Review passes (recorded)**: structure pass → technical/accuracy pass (domain expert) → style/read-aloud pass → facts/attribution pass; comments triaged, not blind-applied.
4. **Versioning**: sources in git (markdown); research kept separate from prose; editions tagged; changelog per edition — **no silent edition changes**.
5. **Builds**: deterministic pipeline (md → HTML/ebook/PDF), pinned templates; preview builds for reviewers; artifacts hashed + signed (`secure-build-pattern`).
6. **Publishing**: distribution channels defined; book metadata (ISBN/description/cover) or course platform setup (entitlements per `payments-and-billing`); launch checklist; sample/errata pages.
7. **Feedback loop**: reader/learner feedback → corrections list → next edition; errata visible; analytics on drop-off points for courses (`product-analytics`).

## Quality gates
- [ ] Outline approved before drafting; units map to outcomes/claims.
- [ ] Review passes recorded (who, when, what changed).
- [ ] Build reproducible; artifacts signed; previews distributed.
- [ ] Errata/feedback channel live.

## Red lines
- No publishing without an accuracy pass; no silent edits across editions; quotes and attributions verified.

## Related
`technical-writing` · `research-tooling` · `release-management` (editions as releases).
