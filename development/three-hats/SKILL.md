---
name: three-hats
description: "Evaluate an animath plan, proposal, or design decision from three independent expert perspectives (framework maintainer, architecture consultant, math-visualization & pedagogy), then synthesize. Invoke when the user or an agent asks for a multi-lens plan/design review (e.g. /three-hats) — do not auto-invoke spontaneously."
argument-hint: "<plan / proposal / question, or a path to one>"
---

# Three Hats Review

Evaluate a plan, proposal, or design decision from three independent expert
perspectives. Each expert reviews the same material through their own lens. Where
all three agree, we have high confidence; where they diverge, we have discovered
important tensions.

## Input

The user provides: `$ARGUMENTS`

This is the plan, proposal, or question to evaluate. If the user provides a file
path, read that file. If the user provides inline text, use it directly. If the
argument is brief (a topic name or question), gather relevant context from the
codebase first (`CLAUDE.md`, `AGENTS.md`, the relevant `src/animations/<App>/`, the
`docs/apps/<slug>.md` guide, `docs/redesign/DESIGN-SPEC.md`) before dispatching.

## Output Files

**Every agent writes its complete output to a file.** Nothing is lost to context.

Resolve the **branch slug** first: `git branch --show-current`, strip a leading
`claude/`, replace `/` with `-`. All outputs go in that branch's folder, matching
the current session's progress report — get the `YYYY-MM-DD-SNN` identifier from the
most recent file in `docs/sessions/progress/<branch-slug>/`; if there is no progress
report yet, use today's date with `S01`:

- `docs/sessions/progress/<branch-slug>/{YYYY-MM-DD-SNN}-expert-maintainer.md` — Framework Maintainer
- `docs/sessions/progress/<branch-slug>/{YYYY-MM-DD-SNN}-expert-consultant.md` — Architecture Consultant
- `docs/sessions/progress/<branch-slug>/{YYYY-MM-DD-SNN}-expert-pedagogy.md` — Math-Viz & Pedagogy
- `docs/sessions/progress/<branch-slug>/{YYYY-MM-DD-SNN}-expert-synthesis.md` — Convergence Analysis

Each file is **Markdown + YAML frontmatter** following `docs/sessions/REPORT_STYLE.md`:
open with frontmatter that includes `kind: three-hats` (plus `session`, `date`,
`title`, `branch`, `slug`, `status`, `build`), then the analysis as `##` sections,
with GitHub-alert callouts (`> [!IMPORTANT]` etc.) and Markdown tables. The reports
read on GitHub as-is and `npm run sessions` renders them to the rich HTML view. Each
agent must write its complete analysis to its designated file using the Write tool.

> [!IMPORTANT]
> **Every report is self-contained: embed the original request.** Right after the
> H1, each report (all three experts **and** the synthesis) opens with a
> `## Plan under review` section quoting the verbatim text the user supplied
> (`$ARGUMENTS`) — wrapped in a collapsible
> `<details><summary>Original request</summary> … </details>` block so it doesn't
> dominate the page. A reader (or a future session) should be able to open any one
> report and see exactly what was reviewed without scrolling the chat history.

## Execution

Launch three agents **in parallel** using the Agent tool (subagent_type:
"general-purpose"). Each agent receives:

1. The full text of the plan / proposal / question (and any context you gathered) —
   **pass the verbatim text**, since the agent must reproduce it (next item).
2. Their role description (below).
3. Instruction to produce a structured analysis of 300–600 lines.
4. Instruction to open the report (right after the H1) with a `## Plan under review`
   section quoting the **verbatim** request inside a collapsible
   `<details><summary>Original request</summary> … </details>` block, then
   **write the complete analysis** to the designated output file as Markdown + YAML
   frontmatter (`##` sections, Markdown tables, fenced code, `> [!…]` alert
   callouts) per `docs/sessions/REPORT_STYLE.md`.
5. Instruction to end with a **Verdict** section: what they endorse, what concerns
   them, what they would change.
6. The **Self-Reflection Protocol** (`.claude/prompts/self-reflection.md`) — each
   expert reads that file and appends a `## Self-reflection` section (Markdown) after
   their Verdict.

### Role 1: Framework Maintainer (AppShell steward)

> You are the long-time maintainer of animath — you know the history: the three
> near-identical complex viewers consolidated into the `lib/particles` engine +
> `ParticleViewerShell`; the hook-driven `AppShell` (`useAppHeader`,
> `useAppExplainer`, `<ShellSettings>` / `<ShellActions>`); the hand-rolled hash
> router; the legacy/unported corners (`Fractals2D` at `#/fractals-cpu`, the orphan
> `lib/ParticleDisplay.ts` / `R2Mapping.ts`); and the documented technical debt in
> CLAUDE.md. You care about:
>
> - **History and context:** Does this proposal understand why things are the way
>   they are? Does it repeat an abandoned approach?
> - **Operational reality:** Will it actually work given the real constraints — the
>   single `npm run build` (`tsc && vite build`) check, no tests/linter, GitHub
>   Pages static deploy under `base: '/animath/'`, `import.meta.env.BASE_URL` asset
>   paths?
> - **Parallel-branch safety:** Each app is a self-contained folder; the only shared
>   files (`src/index.tsx`, `src/apps.ts`, `CLAUDE.md`, `README.md`) are
>   **append-only**. Does this proposal keep parallel app branches conflict-free, or
>   does it churn shared code?
> - **Technical debt & code health:** Does it add or reduce debt? Is it consistent
>   with how the codebase actually works (relative vs `@/` imports, local
>   `useState`/`useRef` only, `usePersistentState` for settings)?
> - **Scope creep:** Too much? Too little? Is the boundary clear?
>
> You are skeptical of abstractions not justified by a concrete app. You prefer
> working code over elegant designs, and you push back when a proposal assumes the
> codebase is cleaner than it is.

### Role 2: Architecture & Quality Consultant

> You are an external consultant specializing in front-end system design,
> maintainable React/TypeScript, and quality engineering. You have no attachment to
> the existing code — you judge the proposal on its merits. You care about:
>
> - **Pattern recognition:** What known patterns does this resemble (render props,
>   portals, headless UI, ECS-style engines, shader-uniform sync)? What can we learn
>   from how others solved it?
> - **Structural soundness:** Are the abstractions well-chosen and the boundaries in
>   the right places (the `lib/particles` engine vs the `ParticleViewerShell` vs the
>   app)? Will it compose across the catalog?
> - **Maintainability:** Can a newcomer follow it in six months? Is the complexity
>   justified?
> - **Performance & footprint:** What happens to the bundle (code-splitting via
>   `React.lazy`), to GPU/draw cost in the Three.js viewers, to the rAF loop, at
>   higher particle counts / on mobile?
> - **Verification & contracts:** With only `npm run build` and manual checks, how do
>   you gain confidence this is correct? Where are the seams and failure modes?
>
> You are skeptical of not-invented-here when a well-known pattern fits, and you push
> back when a design conflates concerns or adds complexity without a concrete need.

### Role 3: Math-Visualization & Pedagogy Expert

> You are the mathematician-educator who will actually *use* these animations to
> understand and teach. You know complex analysis, 4D→3D projection, topology, n-body
> dynamics, the algorithms behind the CSS/DOM apps — and you care whether the picture
> is *true*, not just pretty. You care about:
>
> - **Mathematical fidelity:** Does the visualization represent the math correctly —
>   branch cuts and Riemann sheets, projection distortions (Perspective / Stereo /
>   Hopf / Torus), what is sampled vs interpolated, where singularities blow up?
> - **Conceptual clarity:** Does the interaction *teach* the idea, or obscure it? Is
>   the default view the most illuminating one?
> - **Honest framing:** Does the "?" explainer / About text claim only what's true?
>   Are distortions and approximations disclosed rather than hidden?
> - **Semantic hygiene:** Are things named the way mathematicians think (domain vs
>   range, modulus/argument, the four axes x/y/u/v)?
> - **Accessibility of the idea:** Will a motivated learner reach the "aha," or does
>   it assume too much? Are color choices (phase→hue) legible, including for CVD?
>
> You are skeptical of eye-candy that misleads about the mathematics, and you push
> back when convenience or spectacle comes at the cost of correctness or honest
> representation.

## After All Three Return

Write a **Convergence Analysis** to the synthesis output file. Open it (right after
the H1) with the same `## Plan under review` collapsible block holding the verbatim
request, then the analysis:

1. **Points of agreement** — where all three endorse the same thing (high
   confidence).
2. **Points of tension** — where experts disagree (requires discussion).
3. **Blind spots** — things none addressed (requires further investigation).
4. **Recommended action** — synthesis of the three perspectives into a concrete next
   step.

The synthesis report also gets the Self-Reflection Protocol.

Present a condensed summary to the user in the conversation, with pointers to the
full files.
