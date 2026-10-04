---
name: idea-capture
description: Capture a raw idea and produce a structured idea document — convert operator's stream-of-consciousness into `docs/idea.md` with vision, problem, core concepts, target users, differentiators, constraints, open questions, success criteria. Loads when starting a new project or feature direction with no doc yet, or when the operator says "capture this idea", "I have a new idea", "let's brainstorm X", "structure this".
argument-hint: [idea text or "interactive" for guided mode]
allowed-tools: Read, Write, Bash, Glob, Grep
effort: high
---

# idea-capture

The DOCUMENT-stage skill that converts a raw operator-supplied idea into a structured `docs/idea.md`. Sits at the very front of the project-lifecycle / feature-development chain — before architecture, before scaffold, before any code. The output feeds `idea-refine` (sharpen via questioning) or `architecture-propose` (translate to system design).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No idea doc exists**: project has no `docs/idea.md` and operator wants to start a new initiative.
- **Direct verb**: operator says "capture this idea", "I have a new idea", "let's brainstorm X", "structure this", "write up the vision".
- **Beginning of project-lifecycle**: a new sister project at the very first stage; idea-capture produces the first artifact.
- **New feature with no design doc**: feature work begins; operator describes intent verbally; document the intent before designing.

Do NOT load when:

- `docs/idea.md` already exists — load `idea-refine` (sharpen) or `architecture-propose` (advance to design).
- The change is a small bug fix — document the bug in the task file directly; idea-capture is for net-new directions, not maintenance.
- Operator wants the architecture, not the idea — load `architecture-propose` if there's already a clear vision.
- This is a refactor proposal — load `refactor-architecture` (proposes restructure) or `architecture-review` (audits existing).

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Receive the raw input

**Trigger**: skill loaded.

**Process**:

1. Read `$ARGUMENTS`:
   - If non-empty: operator passed the raw idea inline. Capture verbatim into a scratch space. Do NOT paraphrase yet — operator's exact wording matters (per the brain's "operator words are sacrosanct" principle).
   - If empty / "interactive": ask the operator to describe the idea in their own words. Listen, don't lead. Aim for 5-10 minutes of capture before structuring.
2. Read project context: [README.md](../../../README.md), [CLAUDE.md](../../../CLAUDE.md). Note the existing identity profile (type, domain, scale, phase). Helps detect if the new idea is a NEW project or an extension of THIS project.
3. Capture surrounding signals: any conversation history, related tasks, prior `wiki/log/` entries that hint at the operator's recent thinking.
4. State back to the operator a **one-paragraph summary** of what you heard (not what you'll write). Wait for confirmation or correction before structuring. This is the alignment check — if the summary is wrong, structure built on it will also be wrong.

**Quality bar (Operation 1 done when)**:

- [ ] Raw input captured verbatim (preserved as a quote / scratch note before paraphrasing).
- [ ] Project context read; new-vs-extension determination made.
- [ ] One-paragraph summary stated back to operator and confirmed.
- [ ] Any clarifying questions asked surface CRITICAL unknowns only — don't ask 10 questions when 2 will reveal whether to proceed.

### Operation 2: Structure into the idea doc

**Trigger**: Operation 1 summary confirmed.

**Process**:

1. Write `docs/idea.md` with the 8-section structure:

   ```markdown
   # [Project/Feature Name] — Idea Document

   ## Vision
   One-line description of what this is and why it should exist. The "elevator pitch" — readable to anyone in the ecosystem in <30 seconds.

   ## Problem
   What problem does this solve? Who has this problem? How is it solved today? Why is the current solution insufficient?

   ## Core Concepts
   - **Concept 1**: definition + how it relates to the vision
   - **Concept 2**: definition + how it relates
   - (limit to ~5; more is a sign the idea isn't scoped yet)

   ## Target Users
   Who will use this — be specific (this operator? fleet agents? external developers? end-users?). What's their workflow? Where does this fit in their day?

   ## Key Differentiators
   What makes this different from existing solutions (named explicitly — "vs LocalAI alone", "vs the existing X tool"). For each differentiator: what's the user-visible improvement?

   ## Constraints
   - **Technical**: hardware/runtime/dependency limits this must respect.
   - **Resource**: time/effort budget for the operator.
   - **Timeline**: deadline or soft target.
   - **Identity**: must be consistent with project type/domain/scale (per CLAUDE.md).

   ## Open Questions
   - Decisions that block design but aren't yet made.
   - Don't list trivia — only questions whose answers shape the architecture.

   ## Success Criteria
   How do we know this worked? Each criterion is testable (a measurable signal, an artifact that exists, a user behavior change).
   ```

2. Use **operator's verbatim phrases** in the Vision and Core Concepts sections wherever possible. Paraphrase only when their phrasing is ambiguous; preserve the original as a footnote if you do.
3. Cross-link relevant existing knowledge: if the brain has a domain page covering the idea's domain, reference it (`see [[Backend AI Platform Domain]]`). If similar AICP epics exist, link them (`relates to E011 — Routing Integration`).
4. Limit Core Concepts to ~5. If more emerge, the idea is two ideas pretending to be one — flag for splitting.
5. For Open Questions: each one MUST be design-blocking. "What color is the logo" doesn't go here; "do we use OpenRouter or self-host" does.

**Quality bar (Operation 2 done when)**:

- [ ] All 8 sections present.
- [ ] Vision is one line (not a paragraph).
- [ ] Core Concepts limited to ≤5.
- [ ] Operator's verbatim phrases preserved in Vision and ≥1 Concept.
- [ ] Each Open Question is design-blocking (not trivia).
- [ ] Each Success Criterion is testable (names an artifact / metric / behavior).
- [ ] Project context (CLAUDE.md identity) referenced; consistency checked.

### Operation 3: Show, refine, hand off

**Trigger**: Operation 2 draft written.

**Process**:

1. Show the operator the path + a 3-line preview: the Vision, the top differentiator, the most interesting Open Question.
2. Wait for review. Apply targeted edits per their feedback. Don't rewrite from scratch — operator already aligned in Operation 1.
3. When operator says "good" or equivalent: suggest the next skill:
   - **If the idea has many open questions**: load `idea-refine` to sharpen via guided questioning before architecture.
   - **If the idea is clear and ready**: load `architecture-propose` to advance to design.
   - **If the idea reveals it should be a feature on existing system, not a new project**: load `feature-document` to write the feature requirements doc instead of architecture.
4. Update any task file (if a task is open) with `current_stage: document → design`, add `docs/idea.md` to `artifacts:` list.

**Quality bar (Operation 3 done when)**:

- [ ] Document path shown to operator.
- [ ] Operator reviewed and approved (or fed back targeted edits).
- [ ] Next skill suggested based on idea readiness.
- [ ] Task file (if present) updated.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Paraphrasing the operator's vision

Operator says "I want a thing that ALWAYS asks before doing something destructive." You write "Implement defensive guardrails." Operator reads it; the precision is gone — "ALWAYS" became "defensive" (suggests sometimes), "asks before doing" became "guardrails" (suggests blocks). The vision drifts from the first artifact.

**The rule**: per the brain's "operator words are sacrosanct" principle — preserve verbatim quotes for the Vision and at least one Core Concept. If you paraphrase, retain the original as a sub-bullet: *"Operator: 'ALWAYS asks before doing something destructive'"*.

### Gotcha 2: Filling Open Questions with trivia

Operator's open questions: "should we use Postgres or SQLite", "what's the JWT secret rotation cadence". You write 12 questions including "what color is the logo", "what's the favicon", "should the docs use Markdown or RST". Reader can't see signal from noise; design stalls "answering all the questions".

**The rule**: each Open Question MUST be design-blocking. Apply the test: *"if I answered the opposite, would the architecture meaningfully change?"* If no, drop it. ≤5 Open Questions for a normal idea; >10 signals scope sprawl.

### Gotcha 3: Skipping the alignment check (Operation 1 step 4)

Operator describes the idea; you immediately start writing the doc. By the time they read the structured version, you've baked in 3 wrong assumptions about what they meant. Now they correct each section instead of confirming the gist.

**The rule**: ALWAYS state your one-paragraph understanding before structuring. Wait for confirmation. The 30 seconds spent here saves 5 minutes of section-by-section correction later.

### Gotcha 4: Two ideas in one doc

Operator described "I want X. And also Y, which is similar but different." You write one idea doc that covers both. The Architecture phase tries to design both at once and produces a Frankenstein.

**The rule**: when Core Concepts exceed ~5 OR Vision contains "and also", split into two idea docs. Name them clearly: `docs/idea-X.md` and `docs/idea-Y.md`. Cross-link them. Each gets its own architecture pass.

### Gotcha 5: Vague Success Criteria

"Success Criteria: works well, users like it, no major bugs." Untested. Untestable. Can't verify when "done" is reached.

**The rule**: each criterion names an artifact, metric, or behavior. ✓ "`docs/architecture.md` exists, has 9 sections per architecture-propose's QB", ✓ "fleet agents call the new tool ≥10x in soak", ✓ "operator can complete the round-trip in <2 min". ✗ "works well", ✗ "user-friendly".

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain (or sibling fleet projects). Idea docs live at `docs/idea.md` (project-root pattern). Per [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml), document-stage allowed paths include `wiki/**/*.md` and `docs/**/*.md` — `docs/idea.md` falls under the latter.

This is the canonical entry-point skill of the project-lifecycle methodology chain (`scaffold → foundation → infrastructure → features`) and the front of the feature-development chain (`document → design → scaffold → implement → test`).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| idea-refine | Idea exists but unclear / has many Open Questions | Sharpens via guided questioning; idea-capture authors v1 |
| architecture-propose | Idea exists and is ready for system design | Translates idea to architecture; idea-capture is upstream |
| feature-document | New feature on existing project (not new project) | Different artifact (feature requirements vs project idea); idea-capture is project-level |
| pm-plan | Plan milestones from architecture | Comes after design; idea-capture is before |
| scaffold | Generate code structure from architecture | Comes after architecture-propose, not directly after idea-capture |
