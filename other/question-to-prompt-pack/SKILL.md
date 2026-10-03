---
name: question-to-prompt-pack
description: "Unified entry skill that converts a user's natural-language question into a collaboration frame and prompt pack, then routes the framed task to the best available Codex skill with minimal token use. Use when the user wants their rough question transformed into a clearer communication structure, wants to inspect and adjust the AI's understanding before execution, wants automatic skill selection after question framing, or wants prompts that improve user-AI communication efficiency while preserving the user's style."
---

# Question To Prompt Pack

## Purpose

Use this skill as the single user-facing entry point: convert a rough user question into the smallest useful frame, then decide whether to answer directly, generate a copyable prompt, route to the best available skill, or proceed with execution.

Default behavior: save tokens, avoid overthinking, preserve the user's natural style.

## Main Algorithm

1. Preserve the raw question.
2. Estimate understanding confidence.
3. Apply hard trigger rules.
4. Choose the smallest frame that prevents misunderstanding.
5. Generate one prompt pack when useful.
6. Route the framed task to a skill only when execution needs a specialized workflow.
7. Load the selected skill only after routing confidence is sufficient.
8. Use feedback only when calibrating, testing, or correcting.

## Unified Pipeline

Use this internal chain when the user asks for help completing a task:

```text
rough question -> tiny/compact intent frame -> prompt pack -> skill route -> selected skill execution -> feedback
```

Default unified output:

```text
I understand this as:
- Goal:
- Missing/assumed context:
- Best output:
- Mode:

Prompt pack:
{one concise prompt}

Route:
- Task type:
- Best skill:
- Confidence:
- Next action:
```

Keep the route under 5 lines. If confidence is high, proceed by loading only the selected skill. If confidence is medium, show 2-3 candidates and recommend one. If confidence is low, ask one clarification question.

## Understanding Confidence

| Confidence | Signs | Behavior |
|---|---|---|
| High | goal/output obvious, low risk | Tiny Frame or direct execution |
| Medium | goal clear but depth/format/context may vary | Tiny with assumptions or Compact |
| Low | intent unclear, high stakes, missing context changes result | Clarify First or Full |

Do not display confidence unless useful.

## Hard Trigger Rules

| User signal | Required behavior |
|---|---|
| direct / just do it / execute | Skip frame unless blocked |
| save tokens / short / quick | Tiny Frame only |
| turn this into a prompt | Tiny Frame + one draft prompt |
| show framing / show understanding / let me adjust | Compact or Full |
| choose skill / route / workflow / which tool | Tiny Frame + Route |
| complete this task / help me do X | Tiny Frame + Route unless direct answer is enough |
| train my questioning / score / teach me how to ask | Training |
| high-stakes or freshness-sensitive | Compact with verification |
| coding implementation | Execute and validate unless ambiguity blocks |
| negative feedback on prior output | Apply feedback loop before regenerating |

Follow explicit user instruction first unless safety, verification, or missing context requires clarification.

## Token Budget Ladder

- `Tiny`: default; 4 bullets max + one draft prompt.
- `Compact`: seven collaboration fields, one line each.
- `Full`: compact + assumptions + adjustment menu + quality criteria.
- `Training`: full + score + feedback + next exercise.

## Output Modes

Use the smallest mode that fits the user's intent:

- `tiny`: frame + one prompt + route only when needed.
- `normal`: tiny + one question upgrade tip.
- `training`: normal + diagnosis + one practice exercise.

Do not use `training` unless the user asks to improve questioning ability, asks for feedback, or requests scoring/coaching.

Tiny limits:
- one draft prompt only
- no scorecard
- no long coaching
- no multiple variants
- no reference-file loading
- target under 180 Chinese characters or 120 English words when possible

## Tiny Frame

```text
I understand this as:
- Goal:
- Missing/assumed context:
- Best output:
- Mode:

Draft prompt:
{copyable prompt}

Say "expand" if you want the full collaboration frame.
```

## Compact Frame Fields

Use these fields when the user wants to inspect or adjust understanding:

- Intent
- Task Type
- Context Needed
- Constraints
- Output Shape
- Success Criteria
- Execution Mode

## Execution Modes

- `Answer Directly`
- `Clarify First`
- `Plan First`
- `Route Skill`
- `Implement`
- `Verify`
- `Iterate`

## Skill Routing

Route from compact metadata first. Do not load every `SKILL.md`.

Use `scripts/build_local_index.py` to build a local compact skill index when needed. Use `scripts/search_skill_index.py` to route a framed task from that index. Use the current session skill list first when it is already available.

For a task category with no good local match, use first-run discovery:

```text
local installed skills -> local discovery cache -> user-approved GitHub metadata discovery -> review/install guidance
```

Use `scripts/route_with_discovery.py` for this combined route. GitHub discovery is only for `SKILL.md` metadata and must require user approval/network access. Cache review records in `.question-to-prompt-pack/skill-discovery-cache.json`. After a skill is installed or approved, route from local/cache first and do not repeat GitHub discovery unless the user asks to refresh.

Tiny route:

```text
Route:
- Task type:
- Best skill:
- Why:
- Confidence:
- Next action:
```

Routing rules:

- High confidence: choose one skill and proceed.
- Medium confidence: show 2-3 candidates and recommend one.
- Low confidence: ask one clarification question or answer directly if no skill is needed.
- Never auto-install or execute untrusted GitHub skills.
- GitHub discovery is metadata-only review; it is not a permission to install or run remote code.
- First-run GitHub discovery should guide installation/approval; later runs should use the local index or discovery cache.

## Feedback Loop

Use only during testing, calibration, or correction:

- useful -> keep structure
- too long -> reduce depth
- too shallow -> increase depth or quality criteria
- misunderstood -> rebuild frame
- needs verification -> raise verification level

Do not ask for feedback after every response.

## Question Coaching Loop

Use only when the user wants to improve questioning ability or when one short tip would materially improve repeat use.

Compact coaching block:

```text
Question upgrade:
- Missing piece:
- Why it matters:
- Reusable pattern:
```

Default reusable pattern:

```text
Goal + context + output format + constraints + execution mode
```

Never turn ordinary execution requests into long coaching. See `references/question-coaching.md` for training mode.

## Habit Profile

Track only non-sensitive, useful thread-level preferences:

```text
User Prompt Habit Profile
- language:
- tone:
- answer_structure:
- depth:
- default_frame:
- common_domains:
- recurring_constraints:
- verification_level:
- dislikes:
```

Lifecycle:
- one occurrence: assumption only
- repeated occurrence: working thread preference
- explicit confirmation: stable thread preference
- user correction: override immediately

Do not claim long-term memory unless persistent storage exists and the user requests it.

## Persistent Profile

If the user explicitly asks to remember preferences across sessions, use a project-local profile rather than hidden memory:

```text
.question-to-prompt-pack/user-style-profile.json
```

Use `assets/user-style-profile.schema.json` as the schema. Store only non-sensitive collaboration preferences. See `references/user-style-profile.md`.

## Guardrails

- Do not expose hidden chain-of-thought; show concise user-facing framing only.
- Do not invent preferences from one message unless marked as assumptions.
- Ask at most 3 clarifying questions.
- Do not over-route simple questions that can be answered directly.
- Do not load more than one full skill by default.
- Add verification for current, technical, legal, medical, financial, or research claims.
- For coding tasks, include artifacts and validation.
- For creative/video tasks, include audience, message, format, style, script/structure, and publishing constraints.

## References

- `references/collaboration-frame.md`: templates, confidence, triggers.
- `references/interactive-workflow.md`: adjustments, habit updates, feedback.
- `references/prompt-pack-patterns.md`: full patterns and domain adaptors.
- `references/golden-examples.md`: validation/debugging style anchors.
- `references/skill-routing.md`: routing policy, trust, discovery.
- `references/question-coaching.md`: question-improvement patterns.
- `references/user-style-profile.md`: local non-sensitive profile rules.
- `references/release-management.md`: GitHub promotion and release checklist.
