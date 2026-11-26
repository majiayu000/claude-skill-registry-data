---
name: project-voice
description: "Build the project's voice foundation — about-me.md + voice.md in .ai/ — that every content skill reads before personalized work. Foundation pattern adapted from charlie947/social-media-skills voice-builder."
personas:
  - SOCIAL
  - BRAND
  - MARKETING
  - CV
  - FREELANCE
triggers:
  - project voice
  - learn my voice
  - build my voice
  - voice profile
  - صوتي
  - بصمة الكتابة
  - اكتب بأسلوبي
  - brand voice
tech_stack:
  - charlie947/social-media-skills

---

[SKILL] project-voice
[OBJ] Produce the two foundation artifacts every content skill consumes — `<project>/.ai/about-me.md` (facts) and `<project>/.ai/voice.md` (style rules) — so post-writer/copy/proposal work starts from evidence, not zero.
[RULES]
1. [REQ] Interview first, no preamble: when triggered, the FIRST output is the interview questions. No summary, no "here is what this does", no options menu.
2. [REQ] Collect: name/role, audience, 3–5 writing samples, languages (ar/en mix), taboo phrases, tone sliders (formal↔casual, terse↔verbose, serious↔playful), platform targets.
3. [REQ] Produce `.ai/about-me.md`: facts only — bio, expertise, offers, metrics the user claims (never invented). Mark unverified claims.
4. [REQ] Produce `.ai/voice.md`: operational style contract — sentence length, vocabulary level, dialect (Egyptian/MSA/English), emoji policy, hook patterns, banned words, do/don't examples extracted FROM the samples.
5. [REQ] Read-before-write law: content skills (`social-media-marketing`, `linkedin-platform`, `copy-frameworks`, `proposal-writer`, `cv-writer`, `email-marketing`) MUST read `.ai/voice.md` before personalized output. Missing files → run this skill first; never invent a voice.
6. [PROHIBIT] Never inherit another project's voice files. Never write facts the user didn't supply (first-person experience, metrics). Drafting ≠ publishing.
7. [REQ] Refresh: `voice.md` evolves — on explicit request, update in place preserving unrelated facts; consumers must re-read the canonical file.
8. [CMD] Optional add-on `.ai/newsletter-voice.md` for newsletter-specific tone layered on top of `voice.md`.
