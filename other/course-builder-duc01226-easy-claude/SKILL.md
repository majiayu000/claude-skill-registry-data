---
name: course-builder
version: 1.0.0
description: '[Content] Use when a workflow step or the user asks for course material: Bloom objectives, modules, lessons, exercises, assessments.'
---

## Quick Summary

**Goal:** Build a learner-ready course with Bloom-aligned objectives, progressive modules, lessons, practice, and assessments so learners achieve and demonstrate intended outcomes.

**Summary:**

- **Purpose:** Turn user/research scope into a template-compliant course with aligned outcomes, practice, and assessments.
- **Main flow:** Phase 0 detect course context; (1) define audience, prerequisites, duration, outcomes; (2) map objectives to Bloom; (3) structure modules → lessons → exercises → assessments.
- **Continue:** (4) develop each lesson's duration, concept, explanation, examples, exercise, assessment; (5) create module knowledge checks + comprehensive final; (6) review alignment, evidence, progression, prerequisites.
- **Gates/output:** Create `TaskCreate` tasks before work; map every objective to Bloom; use the enforced template; write `docs/knowledge/courses/{descriptive-slug}.md`; no modes/flags specified.

**Workflow:**

1. **Define scope** — Target audience, prerequisites, duration, objectives
2. **Map objectives** — Align to Bloom's taxonomy
3. **Structure curriculum** — Modules → Lessons → Exercises → Assessments
4. **Develop content** — Per lesson: concept, explanation, examples, exercise
5. **Create assessments** — Knowledge checks + final assessment
6. **Review pedagogy** — Alignment, progressive difficulty, prerequisite chains

**Key Rules:**

- Every objective maps to a Bloom's taxonomy level; include at least one Apply-level objective.
- Build progressive complexity; each module builds on previous prerequisites.
- Derive lesson depth, examples, exercises, and assessment format from learner context and objectives; do not fill templates mechanically.
- Use enforced template `.claude/templates/course-outline-template.md`.

**Critical thinking:** Be skeptical; reason sequentially; trace evidence for every claim; state confidence percentages; ideas >80%.

# Course Builder

## Phase 0: Detect Course Context

Classify course type, learner level, delivery mode, and constraints before choosing depth, examples, exercises, or assessment formats; ask for missing inputs or state assumptions.

## Bloom's Taxonomy Reference

| Level          | Verb Examples                             | Assessment Type                     |
| -------------- | ----------------------------------------- | ----------------------------------- |
| **Remember**   | Define, list, recall, identify            | Multiple choice, fill-in-blank      |
| **Understand** | Explain, describe, summarize, interpret   | Short answer, paraphrase            |
| **Apply**      | Use, implement, solve, demonstrate        | Problem sets, exercises             |
| **Analyze**    | Compare, contrast, examine, differentiate | Case studies, analysis papers       |
| **Evaluate**   | Judge, critique, assess, justify          | Debates, reviews, peer assessment   |
| **Create**     | Design, construct, produce, develop       | Projects, portfolios, presentations |

## Step 1: Define Learning Scope

Gather from user or research: **Target audience** — who + background; **Prerequisites** — prior knowledge; **Duration** — total hours/weeks; **Desired outcomes** — learner capabilities after course.

## Step 2: Map Objectives to Bloom's

Assign a Bloom's level to each desired outcome:
- Start lower: Remember → Understand; progress higher: Apply → Analyze → Evaluate → Create; ensure at least one objective at Apply level or above.

## Step 3: Structure Curriculum

Organize 3-8 modules per course:
- 2-5 lessons/module; module-specific learning objectives; modules build through a prerequisite chain.

## Step 4: Develop Lesson Content

For each lesson, provide: (1) **Duration** — estimated time; (2) **Concept** — core idea in 1-2 sentences; (3) **Explanation** — theory, context, why it matters; (4) **Examples** — 2-3 real-world illustrations; (5) **Exercise** — hands-on practice activity; (6) **Assessment** — how to verify learning.

## Step 5: Create Assessments

Per module: **Knowledge check** — 3-5 questions covering key concepts; questions align with module's Bloom's level.
Final: **Comprehensive assessment** — covers all modules; **Mix of Bloom's levels** — at least 1 question per level taught.

## Step 6: Review Pedagogy

Verify objective/activity/assessment alignment, evidence for content claims, labelled assumptions, progressive difficulty, and prerequisite chain; state confidence.

## Output

Write to `docs/knowledge/courses/{descriptive-slug}.md` using enforced template from `.claude/templates/course-outline-template.md`.

---

> **[IMPORTANT]** Create small tasks with `TaskCreate` before work, including a final review task.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Build a learner-ready course with Bloom-aligned objectives, progressive modules, lessons, practice, and assessments so learners achieve and demonstrate intended outcomes.
**IMPORTANT MUST ATTENTION** Course flow: Phase 0 detect context; (1) define scope; (2) map every objective to Bloom; (3) structure 3-8 modules with 2-5 lessons and prerequisite links; (4) develop each lesson's duration, concept, explanation, examples, exercise, and assessment; (5) create 3-5-question module checks plus a comprehensive final with every taught Bloom level; (6) review alignment, evidence, assumptions, progression, and prerequisites.

**IMPORTANT MUST ATTENTION** Gate/output: create `TaskCreate` tasks before work and a final review task; search 3+ similar patterns before creating code; cite `file:line` evidence with confidence >80%; use enforced `.claude/templates/course-outline-template.md`; write `docs/knowledge/courses/{descriptive-slug}.md`; no modes/flags specified.

**IMPORTANT MUST ATTENTION** use user/research evidence, label assumptions, and state confidence; NEVER fabricate course facts.

**Anti-Rationalization:**

| Evasion | Rebuttal |
| --- | --- |
| "Course is simple" | Wrong assumptions waste time; apply the full flow. |
| "Already searched" | Show `file:line` evidence; no proof means no search. |
| "Just do it" | Create task tracking first; skip depth only when justified, never skip tracking. |

**[TASK-PLANNING]** **MUST ATTENTION** Before acting, analyze scope; create small `TaskCreate` tasks, search 3+ similar patterns before creating code, cite `file:line` evidence, and complete a final quality review.
