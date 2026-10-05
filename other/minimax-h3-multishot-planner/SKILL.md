---
name: minimax-h3-multishot-planner
description: "Non-skippable planning-only MiniMax H3 subskill used by minimax-h3-creative-director before final prompt formatting. Invoke when the user explicitly requests multiple shots, scenes, cuts, montage, or shot-by-shot design, or when a video of at least 10 seconds has no declared single-shot/multishot preference and the user accepts the director's multishot offer. After loading, it must ask shot count and then question the user about every shot in playback order before any final H3 formatting skill may run."
---

# MiniMax H3 Multishot Planner

Plan a confirmed multishot video before the text, keyframe, or full-reference specialist writes the executable H3 prompt. Produce a structured shot plan, not the final H3 prompt.

## Execution Is Mandatory After Loading

The `skill` tool only loads these instructions. Loading this Skill is not execution and is never a successful handoff by itself.

After this Skill is loaded:

1. Do not load any final H3 specialist.
2. Do not draft an H3 prompt.
3. Ask or confirm shot count.
4. Question the user about Shot 1, confirm it, then repeat for Shot 2 and every remaining shot.
5. Build and confirm the complete `multishot_plan`.
6. Return control to the director only after final confirmation.

No final specialist may run while any planned shot remains unasked or unconfirmed.

## Invocation Contract

Enter only through `minimax-h3-creative-director`:

- Enter immediately when the user explicitly requests multiple shots, scenes, cuts, a montage, a sequence, or shot-by-shot planning.
- When effective duration is at least 10 seconds and the user has not chosen single-shot or multishot, let the director ask a binary multishot question. Enter only after the user accepts.
- Do not enter when the user explicitly requests one continuous shot, one take, no cuts, or an equivalent single-shot treatment.
- Do not enter merely because a prompt contains several actions. A continuous action arc can remain one shot.
- Do not choose T2VA, I2VA, FL2VA, L2VA, or Ref2VA here.

If duration is unknown, return control to the director to resolve duration before applying the 10-second gate.

## Choice Source

Consult `references/shot-choice-library.md` for shot vocabulary and option design. Do not treat it as an official closed vocabulary or insert every available term.

## Question Payload Rules

OpenCode does not impose a three-question workflow limit. Use the number of questions required by each state below.

- A strict yes/no question may contain exactly two options.
- Every other choice question must contain at least five materially different, feasible options.
- Put the strongest context-specific recommendation first and append `(Recommended)` to its label.
- Explain the creative consequence of every option in one concise sentence.
- Keep every option label within five words; place detail in its description.
- Do not add `Other`; OpenCode supplies custom input automatically.
- Do not pad a list with near-duplicates. If five meaningful choices cannot be produced, ask an open-ended question instead of a choice question.
- Generate content and performance choices from the user's actual subject, assets, genre, duration, and desired outcome. Never present generic placeholders.
- Use multiple selection only when choices can genuinely coexist.

Before every `question` call, count the options for every question. If a non-binary question has fewer than five options, the payload is invalid: expand it or make that question open-ended before calling the tool.

If the user explicitly prohibits questions, synthesize the complete plan, disclose material assumptions, and ask one binary final confirmation. Otherwise, all states below are mandatory.

## State Machine

### State 1: Shot count

This is the first action after loading unless the user already supplied an exact count.

- Ask exactly one shot-count question.
- Provide at least five feasible counts, normally `2`, `3`, `4`, `5`, and `6` shots.
- Recommend according to duration and action density.
- If an exact count was already supplied, record it and advance directly to State 2 without asking the same question again.

Starting heuristics, not hard limits:

- 4-9 seconds: usually 2-3 shots only when multishot was explicitly requested.
- 10-12 seconds: usually 2-4 shots.
- 13-15 seconds: usually 3-5 shots.

If the chosen count is physically infeasible, ask the strict yes/no question: "是否改用推荐镜头数？"

### State 2: Global timing and continuity

Ask one batch with up to three questions when these decisions remain unknown:

1. Story or information progression
2. Timing distribution and edit rhythm
3. Continuity strategy across cuts

Every choice question in this batch requires at least five options. Allocate provisional start/end times after receiving the answers. Do not force equal durations when action complexity differs.

### State 3: Plan each shot sequentially

Maintain `current_shot`, starting at 1. Never combine different shots in one question payload and never jump ahead.

For the current shot, make one `question` call containing the following six questions unless a field was already explicitly fixed by the user:

1. **Shot content and narrative function**: at least five scene-specific alternatives.
2. **Shot size and composition**: at least five suitable framing/composition alternatives.
3. **Camera behavior**: at least five complete treatments combining movement type, target, speed, amplitude, and compositional purpose.
4. **Action, performance, and expression**: at least five scene-specific visible action arcs.
5. **Opening or entry transition**: at least five opening treatments for Shot 1; at least five cut/transition treatments for later shots.
6. **Sound focus**: at least five relevant combinations of ambience, Foley, non-verbal vocal sound, dialogue/voice, diegetic sound, and audience-only music.

This six-question per-shot batch is intentional. Do not reduce it to three merely because earlier general H3 questions used three-question batches. Omit only a field the user has already explicitly and unambiguously fixed; do not silently infer a missing field to avoid asking.

After receiving the batch answers:

1. Show a concise Chinese summary of the current shot, including provisional timing and active reference roles.
2. Ask the strict yes/no question: "是否确认 Shot N？"
3. If no, ask an open-ended correction question and revise the same shot.
4. If yes, increment `current_shot` and repeat State 3 for the next shot.

Do not enter State 4 until every shot from 1 through `shot_count` is confirmed.

### State 4: Build continuity

After all shots are confirmed:

- Allocate exact start and end times; Shot 1 starts at 0.00 seconds and later start times increase strictly.
- Record the entering and exiting state of every shot.
- Preserve identity, clothing, props, scene geography, lighting direction, object state, visible text, dialogue continuity, and audio continuity unless a change is intentional.
- Assign active reference labels and responsibilities per shot when assets exist.
- Identify J-cuts, L-cuts, match cuts, or sound bridges only when their cross-shot relationship is explicit.
- Reject a multishot plan that also claims to be one continuous take.

### State 5: Final confirmation and handoff

Present the complete plan in Chinese using the schema below. Ask the strict yes/no question: "是否接受这份多镜头方案？"

- If no, ask an open-ended question identifying the shot and desired change, revise it, then reconfirm.
- If yes, mark `multishot_plan_status: confirmed` and return the plan to `minimax-h3-creative-director`.

Only `multishot_plan_status: confirmed` releases the director's hard blocker and permits one final prompt-format specialist to load.

## Output Schema

```text
multishot_plan_status: confirmed
multishot_plan:
  total_duration: ...
  shot_count: ...
  edit_rhythm: ...
  continuity_strategy: ...
  shots:
    - shot: 1
      start: 0.00
      end: ...
      narrative_function: ...
      content: ...
      shot_size_and_composition: ...
      subject_action_and_expression: ...
      camera_movement_amplitude_speed: ...
      entry_transition: opening
      sound_focus: ...
      active_references: ...
      entry_state: ...
      exit_state: ...
    - shot: 2
      ...
  continuity_ledger:
    identity: ...
    wardrobe_and_props: ...
    space_and_lighting: ...
    object_and_text_state: ...
    dialogue_and_audio: ...
```

The final formatting specialist converts this confirmed plan to the official H3 base three-field or Ref2VA six-section prompt without dropping or re-asking confirmed decisions.
