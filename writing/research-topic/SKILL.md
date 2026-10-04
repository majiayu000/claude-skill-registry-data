---
name: research-topic
description: Research a subject thoroughly BEFORE authoring a lesson on this Lessons site, producing an accurate, well-sourced outline (key concepts, definitions, misconceptions, analogies, worked examples) that the new-lesson skill turns into MDX. Use when the user gives a subject to teach, asks to "research X", "prep a lesson on X", or before any new-lesson run when the topic isn't already well understood.
---

# Research a topic before writing

A lesson is only as good as the understanding behind it. Do this **first**, then
hand the outline to the `new-lesson` skill. Never write lesson prose from memory
alone for anything non-trivial.

**Read `TOPIC.md` first** — it is the single source of truth for the subject,
mission, and scope. Research the subject as a step on the **zero-to-expert
ladder** that `TOPIC.md` defines. Identify the lowest level of prior subject
knowledge a reader could have (beginner tiers assume **none**), and flag every
domain term, prerequisite, and assumed-but-untaught concept so `new-lesson` can
set the right `difficulty` and `dependencies`. Push the brief to genuine expert
depth, not just an intro.

## 1. Gather sources

- Use `WebSearch` / `WebFetch` for current, authoritative sources. Prefer
  primary sources, standards, docs, and well-regarded explainers over SEO blogs.
- For academic/scientific topics, use the **paperhound** skill (arXiv, OpenAlex,
  Semantic Scholar) to pull real papers and abstracts.
- Cross-check any non-obvious claim against ≥2 independent sources. Note where
  experts disagree.

## 2. Produce a research brief

Capture (keep it in the working notes / hand to `new-lesson`):

- **Audience & prerequisites** — who is this for, what must they already know.
- **Learning objectives** — 3–6 concrete "after this lesson you can…" outcomes.
- **Key concepts** — each with a crisp, correct **definition** (these feed the
  glossary / `concept → definition` exercises, see the `exercise-components` skill).
- **Common misconceptions** — what learners get wrong (great quiz material).
- **Analogies & mental models** — at least one strong analogy per hard concept
  (feeds the copywriting voice, see `lesson-copy`).
- **Worked examples / concrete numbers** — real data beats hand-waving.
- **Animation opportunities** — which idea is best shown moving, not told
  (feeds `lesson-animations`).
- **Sources** — list URLs/citations so claims are traceable.

## 3. Plan the lesson shape

- Split the topic into a **topic** + ordered **lessons** (one idea each, ~5–8 min).
- For each lesson, draft the 2–6 `##` section outline and pick **at least one
  exercise** and **at least one animation** that earns its place.

## 4. Accuracy gate

Before writing: re-read the brief and confirm every definition and claim is
something you can defend from a source. Flag anything uncertain to the user
rather than inventing it. Then proceed to `new-lesson`.
