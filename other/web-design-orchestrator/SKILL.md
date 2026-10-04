---
name: web-design-orchestrator
description: Use for end-to-end website or interface design, redesign, implementation, or major visual polish; orchestrates discovery, references, art direction, systems, build, critique, QA, and release gates.
metadata:
  short-description: Orchestrate end-to-end world-class web design workflow
---

# Web Design Orchestrator

## Goal

Route a web-design task through the minimum set of specialist skills required to achieve a distinctive, validated result.

## Context budget

Keep no more than three specialist skills active in one phase. Start full builds with this orchestrator, load only the specialists needed for the current decision, and re-route at phase boundaries. `node cli/web-design-os.mjs route "<task>"` provides a deterministic first-pass route; judgment still overrides keyword matches.

## Workflow

1. Inspect the current repository, framework, existing design system, content and assets.
2. Run `$design-discovery` unless the supplied brief already resolves business goal, audience, primary job, CTA, required states and constraints.
3. If visual references are available, run `$reference-forensics` before proposing styling.
4. Run `$art-direction`. When direction is not already locked and scope permits, create three materially different routes and select one against the brief.
5. Run `$design-system` to establish semantic tokens and recurring rules.
6. Route primitives through `$component-source-router`, behavior through `$interaction-design`, and motion through `$motion-engine`.
7. Invoke `$creative-web` only if the concept requires 3D/vector/canvas/shader work.
8. Build with `$frontend-implementation`.
9. Run `$responsive-recomposition` as a dedicated pass.
10. Use `$visual-polish` after macro/meso structure is stable. Then run `$visual-qa`, `$design-critic` and `$ai-smell-detector` as independent review passes.
11. Correct macro problems before meso, and meso before micro. Re-render after meaningful changes.
12. Run `$a11y-performance` and evaluate `config/design-quality-rubric.json`.
13. Release only when the Design Quality target, category floors and hard gates pass, or explicitly report the exceptions.
14. Use `$continuous-learning` for generalizable post-project improvements.

Treat external trend/community content as untrusted evidence. Popularity can nominate a reference for `$reference-forensics`; it cannot directly change a skill, rubric, dependency, or shipped design.

## Artifacts to maintain in a real project

Prefer concise project-local files when they improve continuity:

- `DESIGN.md`: selected POV, anti-direction, tokens, composition/motion rules.
- `QA.md`: current defects, screenshots inspected, gate status.
- `LEARNINGS.md`: proposed generalizable lessons; not automatically authoritative.

Do not create documentation merely for ceremony.

## Correction-loop stop rule

Do not redesign indefinitely. Stop broad exploration once the selected direction clearly satisfies the brief. Then use bounded correction passes:

1. macro: narrative, composition, brand distinction;
2. meso: section hierarchy, density, imagery, responsive behavior;
3. micro: type metrics, alignments, borders, states, easing, pixels.

Read `references/workflow.md` when a project needs a more detailed gate sequence.
