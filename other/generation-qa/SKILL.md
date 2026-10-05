---
name: dircreative-generation-qa
description: Score generated outputs against story, continuity, reference, prompt, and model execution gates.
---

# Generation QA

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/schemas/prompt-ir.schema.json`
- `docs/film-preproduction/prompt-authoring-standard-v1.md`
- `docs/film-preproduction/asset-intake-and-state-standard-v1.md`
- `docs/film-preproduction/prompt-qa-and-incident-runbook-v1.md`
- `scripts/dircreative_prompt_compiler.py`
- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/schemas/qa-report.yaml`
- `docs/film-preproduction/qa/qa-checklist.md`
- `docs/film-preproduction/qa/failure-taxonomy.yaml`
- `docs/film-preproduction/qa/retry-rules.md`
- `docs/film-preproduction/prompt-pattern-registry.json`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/longform-decomposition-policy.md`
- `docs/film-preproduction/reference-consistency-gate.md`
- `docs/film-preproduction/shot-language-standard.md`
- `docs/film-preproduction/film-commercial-quality-standard.md`
- `docs/film-preproduction/creative-production-integration.md`
- `docs/film-preproduction/sources/model-sources.yaml`
- `docs/film-preproduction/sources/prompt-sources.yaml`

## Inputs

- generation output or failure report
- image prompt manifest
- video prompt manifest
- sequence plan or longform reference pack when present
- source artifacts

## Outputs

- QA report
- retry plan
- prompt pattern candidate or deprecation request
- post-generation QA receipt when generation happened
- E0-E6 capability and prompt behavior eval receipt

## Chat Surface

Show the actual candidate when available, identify the visible defect and its
impact, and state the smallest corrective action. Preserve successful work.
Execute a bounded retry only within current authorization and retry limits;
otherwise return the corrected prompt or exact blocker. Do not ask the user to
inspect internal taxonomies, and do not ask for acceptance of a failed candidate.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#qa-candidate-delta-comparison`. Bind candidates, passed and failed locks, blocker, smallest retry, and preserved artifacts to the QA report; failed QA exposes retry/stop/inspect, never lock or acceptance, and preserves a table fallback. When candidate images exist, render their verified previews before the delta table and keep the visible image, QA column, professional judgment, blocker, retry, and primary action synchronized to the same candidate. Label illustrative placeholders explicitly and never let them masquerade as usable candidates.

## Rules

- Decide whether to change prompt, reference image, shot design, model, or post-production.
- For source-maintenance changes to capability/prompt contracts, run `python3 scripts/dircreative_model_capability_audit.py` and its E0-E6 controls. A production review checks the active output and relevant exact-card constraints only.
- E0 rejects family aliases, `latest`, missing version/provider surface, stale cards, and unresolved cards.
- E1 rejects forged S1 labels, S4-only evidence, or unscoped evidence used as authoritative capability truth.
- E2 rejects native audio when the exact card/provider surface does not support the route; compare `desired_audio` with `generation_audio_route` and preserve official source conflicts.
- E3 rejects empty or overlapping `preserve`/`change` sets and image edits without a concrete source/reference.
- E4 rejects rights/provider/likeness/voice/brand/audio conflicts and any generation-ready or external-upload state without verified evidence.
- E5 rejects a professional storyboard/motion map or dense board bound as a literal first frame; require a separate QA-passed clean frame for first/end-frame modes.
- E6 rejects a fixed Image2/GPT Image suffix required for every prompt; `surface_integrity_guard_v1` is an optional internal QA macro activated only by an observed failure or recorded A/B eval.
- Reject deprecated capability cards and preview aliases when a current stable endpoint exists. Keep Runway Gen-4 Aleph deprecation, Aleph 2.0 Web, and Aleph 2.0 API as separate receipts; keep stable Veo 3.1 `*-001` cards separate from deprecated preview aliases.
- Compare generated/imported visuals against `visual_decomposition` and `prompt_layers`: subject, blocking, details, environment, light, composition, camera, palette, material, proportion, and generation intent must match the locked source.
- Reject violations of protected visual facts: identity, exact text/logos, product features, established wardrobe, prop custody and scene geography. Ordinary design detail within the brief is permitted; do not mark a new design wrong merely because every decorative detail was not individually specified.
- Reject prompt outputs that rely on standalone filler quality words instead of concrete visual constraints.
- Reject receipts that hide source tier, access date, provider surface, or a material official-source conflict.
- Check that the production prompt and reusable identity/style facts are sufficient for complex assets. A negative prompt is conditional on a concrete known risk or observed failure; do not require a new image to accumulate exclusions from earlier attempts.
- Treat multilingual prompt fields as optional delivery fields. Do not fail a normal DIRcreative prompt for being single-language.
- Treat post-generation QA as a backstop. The primary prevention layer is the image-prompt-compiler `pre_generation_contract`.
- For an authorized batch with ready shared inputs, finish the batch and conduct one consolidated review before dependent use, final selection or delivery. Interrupt only for a critical defect affecting the next real input; unrelated images and content keep moving.
- Reuse one valid review for the same pixels, truth and intended use. Do not run an executor checklist, a second routine independent visual review and a new downstream viewing ceremony for the same unchanged candidate. `dircreative_review_batch.py` records the actual batch decision; ordinary `executor` review is draft-only. Separate independent review is for explicit requirements or material unresolved risk, and final adoption keeps its authority boundary.
- The user must not be the first QA pass, but the assistant also must not rely on post-QA as the first defense.
- Check whether a failure is caused by missing generated files, external pending assets, or unlocked candidates.
- Check whether a failure is caused by rights, card/version mismatch, duration/reference incompatibility, audio-route mismatch, deprecated status, or a generate/edit/extension route collision.
- Reject generated candidates when character identity or scene geography drifts from the locked source asset.
- Reject duplicate boards when repeated character or scene content introduces new visual facts.
- Require reference roles in the manifest. Visible role titles apply only to presentation boards that call for them; identity sheets, source photographs and clean model inputs must not be redrawn to add labels.
- Reject storyboard/motion pages that lack professional shot-card density: timecode, duration, shot image, detailed frame description, shot size, focal length, movement, blocking, sound, transition, and model risk.
- Do not advance a rejected candidate as a direct video input. Continue independent assets and prompt work that do not consume its failed facts.
- Do not ask the user to approve a known unusable candidate. Record its actual failure and affected uses. A retry is a production decision, not an automatic response to a style preference or a detector flag.
- For Creative Production outputs, treat `render_moodboard_board_widget` as a review surface, not the source of truth. The candidate must be written back to DIRcreative as `generated_candidate`, then QA can pass, fail, or request a one-variable retry.
- Reject any Creative Production candidate that is marked `user_locked` while QA is pending or failed.
- Reject narrative frames or human planning boards promoted to identity,
  vehicle, scene, or literal-frame truth without an explicit promotion receipt
  and independent QA. Treat model-layout references as position/direction only;
  they cannot control identity, topology, material, or color.
- Reject irreversible state resets or illegal transitions across damage, shield,
  core, helmet, prop, and vehicle families. Adjacent generation units must have
  exact outgoing/incoming state handoff.
- Reject prompt binding sets that exceed the verified provider reference limit,
  attach planned/optional audio, or disagree across global numbering, per-unit
  local order, and terminal platform slots.
- For cinematic storyboard and clean narrative frames, score two separate gates:
  asset truth and director-frame quality. Reject a technically consistent frame
  that falls back to an unmotivated centered overview, loses viewer position,
  action vector/counterforce, depth roles, crop pressure, parallax/occlusion,
  declared exaggeration, or the dominant read.
- Respect shot-class N/A fields. Static product, identity, interview, dialogue,
  observation, and calm frames may omit action/counterforce, crop pressure,
  parallax, or exaggeration when the frame contract gives a concrete reason;
  missing required fields without that reason still fails.
- Audit sequence diversity across all selected frames. Repeated subject scale,
  orbital overview, horizon, camera height, visual center, or attention flow is
  a failure when it does not serve a deliberate pattern or match cut.
- Reject any review-only widget, HTML page, local URL, or screenshot that is presented as a locked artifact without a DIRcreative receipt.
- For longform work, localize failures to one sequence pack whenever possible.
- Repair authorized defects at the smallest source and mark affected descendants stale. Ask only when a repair changes protected meaning, scope or a user-reserved lock.

## Prompt-system structural QA

For source-maintenance prompt fixtures, run the deterministic audit below. It is not a prerequisite for reviewing one production candidate:

~~~text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/dircreative_prompt_fixture_audit.py
~~~

The audit must prove:

- Prompt IR passes the executable v1.1 schema and semantic checks;
- minimal character + scene, multi-character/multi-asset 15-second, and split 30-second fixtures compile;
- action, prop ownership, speaker, screen position, and generation-unit state bindings resolve;
- only attached references enter the exact adapter surface and planning-only references stay internal;
- terminal prompts reject internal IDs, local paths, hashes, manifest/QA/retry fields, and phantom reference slots;
- computed structural scores match fixture records;
- receipt contains QA status, current status, next_action, live acceptance state, and unverified external work.

When reviewing generated output later, add the following failure IDs to the existing taxonomy:

- F-COMP-01 / F-COMP-02 / F-COMP-03 for visual-center, mechanical-composition, or crop/movement-room failures;
- F-LOOK-01 for flat or purposeless grade;
- F-OPT-01 / F-OPT-02 / F-OPT-03 for generic optics, flare/bloom washout, or focus/bokeh mismatch;
- F-ATM-01 for unsupported or uncontrolled Tyndall/haze;
- F-GRADE-01 for grade/material/continuity break.

Retry one layer only. Preserve source truth, product identity, composition locks, and output mode while changing the smallest failing artifact. Never ask the user to lock a candidate before self-QA passes.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record E0-E6 positive/negative results, exact cards and deprecations, source tiers/dates/conflicts, rights and audio-route status, preserve/change overlap result, storyboard/clean-frame separation, optional macro activation, failure types, fixes, registry candidates, QA status, and `next_recommended_skill: learn`.
