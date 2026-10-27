---
name: idea-to-unity
description: "Develop unbuilt game ideas through targeted discovery, visual variants, contact sheets, and approval-gated Unity prototyping. Use when the user wants to flesh out a feature, explore an undecided concept, compare alternatives, or prototype models, animation, lighting, gameplay, or HUDs. Keep iteration lightweight and integration-ready."
---

# Idea to Unity

Turn an unmanifested idea into something the human can judge, refine, and explicitly choose to build. Optimize for learning about the feature, not polishing the machinery used to preview it.

## Workflow and gates

```text
Targeted discovery -> 3+ comparable variants -> Human review
                              ^                    |
                              +---- Refine --------+
                                                   |
                                     Explicit build approval
                                                   |
                                  Native iteration -> Verify
```

Keep discovery and comparison lightweight. Repeat the review loop until the human is satisfied. Move to a scoped native comparison earlier when external exploration stops being useful, but obtain approval before importing or building in Unity. Do not treat prototype approval as permission to replace production content.

## Non-negotiable operating rules

- Ask intelligently, not exhaustively. Reuse known answers and ask only questions that change the design or experiment.
- Cover visual experience with multiple feature-specific questions, not one generic aesthetic preference.
- Record an undecided design choice as **Viable for variation**. Do not turn it into a blocker or silently fix it.
- Present at least three meaningfully different options together in each variant review, including refinement rounds.
- Create labeled contact sheets for visual or model variants so the human can scan many alternatives at once. Reuse captures and a simple image-compositing step, not a gallery application.
- Explore successful alternatives and the actual framework's possibilities; compare benefits, drawbacks, implementation cost, and risk.
- Build no bespoke preview UI, configuration surface, dashboard, or standalone webapp unless requested. Prefer existing viewers, fixed presets, simple diagrams, and direct commands. For HUD requests, design the requested HUD, not an application around its preview.
- Keep a lab thin and integration-ready. Reuse real components, data contracts, assets, and input paths rather than building a parallel implementation. Keep experimental behavior inactive for existing production consumers unless its effects are approved.
- Watch for growing isolation. Suggest native iteration when mocks duplicate runtime behavior or integration assumptions dominate the work.
- Script repetitive, token-heavy work with small helpers around the existing pipeline when repetition justifies it. Do not build a new automation framework.
- Keep look approval, native prototype approval, and production installation scope distinct. Never infer approval from praise, preference, or silence.

## 1. Establish the idea and its context

Identify the feature, player need, audience, trigger, observable output, current stage, and intended world context from the request. State what it does and explicitly does not do. Inspect only the relevant project constraints and existing implementation or pipeline. Do not ask the human to rediscover repository facts.

If the request already contains answers or reviewed variants, resume from that stage instead of restarting discovery. Keep unresolved dimensions open. In a non-Unity project, complete concept discovery and identify the actual implementation target before applying Unity-specific instructions.

Make relevant suggestions throughout discovery, variation review, specification, and native iteration using existing research. Read [research-and-ideation.md](references/research-and-ideation.md) for focused use of `~/.claude/research`, project `.claude/research`, `~/llmwiki`, project `wiki`/`docs`, and `/skill:search-web` when fresh inspiration or evidence is needed. Tie suggestions to the current decision, cite their basis, and distinguish evidence from extrapolation.

## 2. Run the targeted questionnaire

Read [questionnaire.md](references/questionnaire.md). During creative discovery, ask 2–4 related questions per round and adapt follow-ups to the answers. When speccing out a chosen direction or conducting a deep requirements interview, switch to one question at a time with a recommended answer and wait for feedback before continuing. Across the conversation cover:

1. Purpose and evidence of success.
2. When and where the feature is encountered.
3. How it is surfaced and attracts attention.
4. Visual experience: ask at least three distinct questions suited to the target feature.
5. Interaction, inputs, feedback, interruption, and recovery.
6. Impact on world state, systems, or other actors, including how that impact becomes visible.
7. Where the player's challenge lies; keep technical implementation difficulty separate.
8. Feel, pace, weight, responsiveness, and emotional effect.
9. Fixed constraints and open possibilities.

Keep a compact decision ledger with **Confirmed**, **Viable for variation**, **Assumption**, and **Technical unknown** statuses. Verify technical unknowns through inspection or scoped experiments; do not confuse them with creative freedom.

Summarize the brief and open dimensions before generating variants. Do not force a decision on every detail to proceed.

For large, ambiguous, or integration-heavy features, read [requirements-and-experiments.md](references/requirements-and-experiments.md) and deepen the brief through scope, verified technical context, relevant edge cases, integration ownership, and testable acceptance criteria. Follow its specification interview rules: resolve upstream decisions first, explain recommendations, sharpen domain language, and cross-check existing code and docs. Scale the depth to the risk; do not impose a full technical interview on a silhouette study. When a full requirements interview is explicitly requested, cover all five phases in order, summarize and confirm each, and complete the brief before writing code.

## 3. Choose the lightest useful prototype medium

State the question each prototype must answer and the evidence that will answer it. Separate appearance, logic/state, and native feel/integration questions instead of defaulting to a webapp or terminal tool. Before creating an executable experiment, read [requirements-and-experiments.md](references/requirements-and-experiments.md) for the short experiment card, run/reset path, state visibility, and exit rules.

| Target | Start with | Prove natively when needed |
|---|---|---|
| 3D model or modeling-heavy visual | Existing design-kit recipes and viewer | Scale, materials, sockets, placement, and interaction |
| Animation | Pose strip, timing diagram, or storyboard | Timing, interruption, transitions, and feel |
| Major lighting | Composition/value study and attention hierarchy | Actual camera, URP materials, volumes, shadows, and cost |
| Gameplay | Action-feedback-consequence diagram | Real input, state transitions, challenge, and world impact |
| HUD | Wireframes and relevant UI states | UI Toolkit behavior, real bindings, readability, and input |

Before native animation, major lighting, gameplay, or HUD work, review a small diagram, wireframe, storyboard, or value/composition sketch with the human; reuse an existing reviewed artifact when available. Use `/skill:ascii-design` when useful and consult its instructions if available. Otherwise use a plain diagram or direct sketch with a short explanation. Keep this visual validation small, not a separate design project.

For mixed features, explore the modeling questions in design-kit first and the runtime questions natively. Do not recreate gameplay in a browser just because model sketches live there.

Read [unity-handoff.md](references/unity-handoff.md) before extending a lab or deciding to move into Unity. Identify the integration destination early. Prefer a native test scene that hosts the intended real implementation over a disposable duplicate.

For visual evidence, read [visual-evidence.md](references/visual-evidence.md). Select Scene View, Game View, isolated-object, or named-camera capture according to the question and current project pipeline. Use the bundled contact-sheet helper for labeled, downsampled comparisons while retaining originals. For Sector complaints about what looked wrong, use its documented grievance capture before diagnosing from memory.

## 4. Generate and review variations

Read [variation-review.md](references/variation-review.md). Inspect relevant precedents and the current framework with a bounded research pass. Cite sources for claimed precedents; label unverified inspiration and unsupported capabilities honestly. When independent perspectives will help, use the `idea-form`, `idea-feel`, `idea-system`, and `idea-wildcard` definitions selectively, following [research-and-ideation.md](references/research-and-ideation.md). Give them distinct open axes, one shared comparison scenario, and bounded output; aggregate their work into one review rather than separate applications.

Bundled agent definitions: [form](assets/agents/idea-form.md), [feel](assets/agents/idea-feel.md), [system](assets/agents/idea-system.md), and [wildcard](assets/agents/idea-wildcard.md). They are installed separately in `~/.claude/agents/` for this setup. Under omp, delegation is the `task` tool and agents load from the project's `.omp/agents/` or `~/.omp/agent/agents/`; a delegated agent cannot address the human, so every review question returns through the orchestrating session. On another host, verify its agent convention and install these assets only when requested, without overwriting existing definitions; otherwise use their role briefs through supported delegation.

Create at least three distinct directions. Hold confirmed requirements constant and vary open dimensions deliberately. Give each option a stable ID, comparable visual or behavioral evidence, intended feel, world consequence, benefit, drawback, framework fit, and relative implementation cost. Do not hide all the useful differences in prose or offer cosmetic recolours when the question is structural.

Present the options together. Recommend one with reasons without eliminating the others. When a recommendation rests on a 3D or game-design principle, state it in first-principles register: build the idea, give one picture, say what breaks, give the number. Ask what to keep, combine, or reject, and invite the human to invent missing details. Ask one or two targeted questions about unexplored pieces rather than only asking “Which one?”

Update the ledger and repeat with at least three comparable options. Retain a favourite alongside two refinements when useful. Keep each round focused on the highest-value uncertainty; do not rebuild the preview infrastructure.

## 5. Check whether external exploration still pays off

At each review, look for duplicated runtime logic, lab-only data or components, increasing manual translation, or decisions that depend on Unity's actual rendering, timing, input, or physics. Also check whether more effort is going into controls and scaffolding than the feature.

When isolation is becoming costly, explain the specific limitation and propose a small native experiment using the real integration path. Ask for scoped native prototype approval if not already granted. Once approved, iterate there rather than maintaining two implementations. Keep three-way review through presets, captures, or clips, not separate apps.

When setup, generation, import, reset, or capture is repeating, reuse or add a small script around existing commands. Verify the helper's output. Keep automation proportional to the work saved.

## 6. Build only the approved scope

When the human is satisfied and explicitly asks to build, record approved variant IDs or hybrid choices, remaining tunables, native comparison versus production scope, destination, and acceptance checks. Do not force one winner if the human wants multiple variants imported.

Follow [unity-handoff.md](references/unity-handoff.md) and the repository's current pipeline. For approved model variants, export and import through design-kit's existing native receivers. For animation, lighting, gameplay, and HUD, implement the required behavior with native Unity assets and components; do not pretend the static geometry importer transports those systems.

Preserve source links, stable IDs, editable assets, and existing user tuning. Keep native lab wiring close to the intended production path. Validate the integration seam early; do not defer all integration risk until after visual polish.

Exercise the actual experience in Unity and capture evidence. Distinguish imported, playable, integrated, visually reviewed, and untested states. If blocked, state the missing prerequisite and finish reachable concept work without inventing native results.

When the human must observe what you cannot (feel, timing, a look on their screen), apply `/skill:human-in-the-loop-testing` and consult its instructions if available: write the hypothesis-to-observable map before asking, give the make-or-break test first, offer a symptom menu mapped to causes with a "none of these" escape, and keep one cumulative known-noise ledger. Under omp, present the menu through the `ask` tool. Do not ask "does it work?"; a delegated verifier that cannot observe returns the map, and the orchestrating session asks.

Verify cost, not just look. When the approved variant adds per-frame work, new materials or shader keywords, transparent layers, mesh rebuilds, or repeated geometry, run the project's performance experiment card (in Sector: `.claude/rules/performance.md`, "Measure before you fix") and report the delta against a baseline. A screenshot or a compile is not a cost measurement. If the project has no such card, record the baseline and the delta with the measurement route stated; do not adopt a budget from another project.

Capture what the experiment taught the human and mark unreviewed conclusions pending. Keep validated decisions and reusable implementation; remove or absorb only the temporary scaffolding when safe and authorized. Do not ship a preview shell or discard real components just because the experiment was temporary. Use the lifecycle guidance in [requirements-and-experiments.md](references/requirements-and-experiments.md).

## 7. Learn without creating more process

After a meaningful experiment, capture the question, evidence, human verdict, and reusable lesson in the conversation or existing project record. Keep taste decisions separate from technical proof and leave unreviewed outcomes pending.

When asked to synthesize session learnings, or when repeated friction suggests a concrete skill improvement, read [learning-loop.md](references/learning-loop.md). Use available learning logs and verified outcomes, check existing skill coverage, and prefer a focused update over a duplicate skill. Do not fabricate historical patterns, install collection tooling, or edit user-authored skills without authorization. Keep learning capture brief; do not turn each variant review into a skill-generation project.


## Keep session output compact

Maintain only the current brief, decision ledger, variant comparison, and next design question or approved implementation action. Reuse an existing project record when appropriate; do not create a documentation suite. At build handoff, give paths to the resulting assets, observed verification, and remaining open choices.
