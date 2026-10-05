---
name: dircreative-story-development
description: Convert selected concept into logline, beat sheet, treatment, and story review.
---

# Story Development

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/creative-copy-deck-capability.md`
- `docs/film-preproduction/professional-agent-voice-standard.md`
- `docs/film-preproduction/schemas/story-package.yaml`
- `docs/film-preproduction/research/channel-playbooks.md`

## Inputs

- selected concept
- director-room notes
- channel and duration

## Outputs

- logline
- beat sheet
- treatment
- source bindings and concept substitutability check
- story review

During creative discussion, keep work at the current agreed scope and follow
the root interaction contract. Once production is authorized, return the
requested story and continue without new stage approvals.

## Chat Surface

Deliver the complete requested story, not a preview that withholds its ending.
Use readable paragraphs, observable beats and enough dramatic or perceptual
change for the genre and duration. Explain a recommendation only where it helps.
If script development is also requested, continue after the internal story check.
Use concept_lock only for an unresolved material choice reserved for the user.

## Quality Gate

Review against the requested form. Causal drama needs protagonist, goal, obstacle, stakes and a meaningful turn. Lyrical/observational work needs perceptual, rhythmic or relational progression with an intentional ending. Every form must fit its channel/duration and contain screenable beats.

Check whether the concept survives replacing the product, setting or relationship with an unrelated one. For a formal `distinctive` verdict under the source-bound schema, also apply the following recorded checks:

- Record at least two alternatives with unique IDs and proximity reasons, then select the nearest one by ID into `swap_subject`.
- Record `before_swap` and `after_swap` while holding concept wording and beat order constant.
- Set `still_works_without_rewrite: false` only when the replacement breaks the mechanism, proof, relationship, setting, or payoff.
- Record at least two concrete `broken_dependency_ids` that resolve to `specific_dependencies`.
- Record `concept_author_id`; require an `independent_reviewer` whose reviewer ID differs from it, with `independent_from_concept_author: true` and a passing review status.
- Set `verdict: distinctive` only after those checks pass.
- Reject a concept that survives with noun replacement, even when its title, mood, or imagery sounds original.

Bind the story package to the approved fact, source-evidence, and inference IDs. The source arrays and IDs fail closed; preserve the audience-tension evidence and proposition facts used by the story. Every outline beat needs a unique ID plus `source_fact_ids` and `source_inference_ids` that resolve through the story binding. Keep inference-based creative moves labeled as professional judgment. Do not introduce an audience-facing commercial claim that is absent from the project's approved claim register.

For causal dramatic shorts, use the following story-engine checks when relevant:

- external pressure that forces action now, not only atmosphere,
- a hidden relationship engine, secret, misunderstanding, exchange, debt, or promise that changes the two-person dynamic,
- an irreversible choice or reveal before the ending,
- escalation from setup to pressure to reversal to consequence,
- a visible ending action that changes how the viewer reads the relationship,
- a reason the setting is a plot device, not just a mood background.

A dramatic story needs screenable change and consequence. An explicitly lyrical, observational or gentle film may build through perception, rhythm or relational change; do not force a secret, threat or irreversible event to satisfy a template.

Use this dramatic pressure card internally when it exposes a real story weakness; do not add a second artifact merely to repeat the treatment:

```text
Want:
Obstacle:
Tactic:
Subtext:
Turn/reveal:
Irreversible consequence:
Visible ending action:
Setting as plot device:
```

Reject if the card contains abstractions instead of specific screenable facts.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#story-beat-ribbon`. Bind the beginning, turn, proof, ending, tension, and downstream effect to the story package; submit approval or revision intent to the current story gate and preserve the Mermaid fallback.

## Rules

- Keep the story executable for the target duration.
- Make the audience tension, business objective, single-minded proposition, and avoid-cliches visible in the concept decision when the project has commercial intent.
- Reject category cliches that reproduce an item in `avoid_cliches` without a project-specific reversal or consequence.
- Client story work needs readable, complete story paragraphs. Review story quality internally before expanding the requested script; do not require a separate user approval.
- Preserve every source-brief requirement not explicitly removed by the user. If an old route, alternate direction, customer prop, story bone, character count, or client-provided object is not used, record it as `omitted_requirements_without_user_removal` and block downstream work.
- If a prop list uses an ellipsis, treat it as examples. Expand the prop logic into each relevant character's role identity, prop, action, and shot function before approval.
- Explain why the story direction fits the channel, duration, first-hook timing, emotional turn, and reference-pack needs.
- If the user asks for visual exploration, story rebuild, formal lockable material, retry, thread/workflow audit, or live acceptance, name that intent before continuing.
- Before dependent script/shot/asset work, review progression and ending against the requested form. Require tension/causal escalation for causal drama; use perception, rhythm and relationship changes for observational or lyrical work. Never add a forbidden crisis or reveal to satisfy the dramatic template.
- Do not use visual polish to compensate for weak story or script work. When a story change invalidates downstream decisions, mark downstream visual assets as not locked before returning to story development.
- Resolve actual story defects before dependent script work; a passed internal review is sufficient within the user-authorized scope.
- Do not write shot lists or prompts.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record source-binding status, alternatives considered, selected swap and before/after result, broken dependency IDs, independent reviewer receipt, concept substitutability verdict, story gate status, claim-boundary status, and `next_recommended_skill: script-treatment`.
