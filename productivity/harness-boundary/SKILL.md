---
name: harness-boundary
description: "Design lens: which layer a harness mechanism belongs in, and whether it outlives the next model or runtime."
user-invocable: true
origin: shimo4228
disable-model-invocation: true
---

# harness-boundary — a design lens that treats as assets only what survives discarding the harness

"The harness is the asset" is only half right. Harness logic that compensates for model-specific weaknesses
goes stale with each model generation, and the runtime (tool execution, permissions, state, retry, agent loop)
is being standardized and replaced. What remains are **other layers mixed into** the harness. This skill
raises the questions for separating that mixture when a mechanism is added, changed, or reviewed.

This is not an enforced architecture but a lens for judging asset boundaries, portability, and obsolescence.

## Core principles

- Put model capability in the model. Do not reimplement it in the harness
- Put procedural knowledge in skills
- Keep values and responsibility boundaries explicit and inspectable
- Put the definition of quality in evals
- Put domain knowledge and history in data / memory
- Keep the runtime as thin and swappable as practically possible

And: **do not optimize to preserve the harness. Optimize to preserve what should survive
swapping the harness.** When a new model makes existing logic unnecessary, that is not a design
failure but the moment to delete. Delete / Simplify count as success.

## The 6 layers

| Layer | Contents | Counterpart in this harness | Existing vocabulary |
|---|---|---|---|
| Model capability | reasoning / planning / coding / tool-use judgment / self-correction / decomposition / reflection | Claude itself (including the system prompt + tool descriptions) | substrate, generation-audit's runtime layer |
| Skills (procedural memory) | this task follows this procedure / this review uses these angles / this failure has this runbook / this deliverable gets this verification | `skills/*/SKILL.md`, the body of `agents/*.md` | "procedures go in skills" (rules/README.md) |
| Values / Policies / responsibility boundaries | what to prioritize / what not to do / operations that need human approval / scope of delegation / source of truth / priorities on failure | `rules/common/` (identity / values layer, ADR-0018 D7), permissions in `settings.json`, authority in the task request | "environment-specific facts, wiring, traps" (ADR-0035) |
| Evals | acceptance criteria / tests / rubric / benchmark / regression / quality gate | `.claude/verify.sh`, `tests/`, `skill-comply`, `llm-as-judge`, dedicated judge agents | Verify, binding judgment |
| Data / Memory | deliverables / decision history / domain knowledge / preferences / provenance / historical state | `docs/adr/`, auto-memory, `.notes/`, `metrics/*.jsonl`, wiki | ADR = dated hypothesis |
| Runtime | tool calling / shell & fs / permission implementation / sandbox / connector / retry / logging / state / routing / agent loop | Claude Code itself, `hooks/*.sh`, MCP servers, the Workflow / Agent tools, launchd tick | control plane (ADR-0019), hooks are timing (ADR-0035) |

Hooks sit in the runtime layer, but they **easily encode policy silently** (e.g., the conditions of an approval gate,
what to block). When looking at a hook, separate "the timing wiring" from "the policy embedded in it," and
ask whether the latter is visibly stated in a rule / ADR.

## The 6 questions

For each target, use only the questions its scale calls for.

- **A. Which layer is it?** If it spans several, can it be separated?
- **B. Why can't it be left to the model itself?** If you cannot state a clear reason, do not add it to the harness.
  "The previous model was bad at this" is not a reason — have you tried it with the current model?
- **C. Is the next model generation likely to make it unnecessary?** If it is a workaround for a capability gap, do not make it
  permanent architecture. Mark it explicitly as temporary / removable and write its expiry condition
- **D. Is it worth keeping when the runtime is swapped?** If it is still needed after moving Claude Code → Pi → Codex → an unknown
  runtime, it is a candidate to hold separately from the runtime. If not, keep it thin as runtime-specific
- **E. Is it necessary infrastructure or a differentiating asset?** Both are "important," but do not conflate them. Infrastructure is
  assumed to be borrowed and replaced; differentiating assets are held in portable form
- **F. Can it move to a simpler layer?** Typical moves:
  custom agent loop → model / hard-coded workflow → skill / conditional branching inside the runtime → policy /
  prompt-based quality judgment → eval / embedded knowledge → data

## Targets to suspect strongly

Not rejected automatically. But the following go through B–D without skipping:

elaborate agent loops / mandatory reflection / mandatory planning stages / fixed multi-agent
orchestration / excessive routing / long system prompts / model-specific behavioral workarounds /
duplicate implementations of model capability / workflows that remain because an old model needed them / runtime-specific
abstractions that contain domain knowledge / hooks that silently encode policy / opaque automation that hides responsibility boundaries /
mechanisms whose purpose is preserving the existing harness design itself

## Output

Do not overdo it. If one line is enough, use one line (e.g., "This is the skill layer. No reason to put it in the runtime → Move").
**Do not output every field every time.** Only when the judgment is contested or the impact is broad, use this form:

```
Classification        : layer (a separation proposal if several)
Keep outside model because : reason to keep it outside the model (if none, a Delete candidate)
Portability           : whether to keep it when the runtime / model is swapped
Obsolescence risk     : Low / Medium / High (1-line rationale, expiry condition if possible)
Recommendation        : Keep / Move / Simplify / Make temporary / Delete / Defer
```

## Connecting to existing verdicts

This skill issues a Recommendation directly only for **mechanisms being proposed or changed**.
When applied retroactively to **installed assets**, do not execute the conclusion yourself; pass it as evidence to the relevant stocktake
(the same "read, never require" contract as generation-audit. Do not split the source of truth for the verdict table — ADR-0022).

| This skill | Counterpart for installed assets |
|---|---|
| Delete | Retire / Dissolve in rules / skill / agent-stocktake |
| Move | Demote / Merge in the same, or rules-distill (skill → rule direction) |
| Simplify | Improve in the same, built-in `/simplify` |
| Make temporary | write a deadline in `review-when:` for a rule, `## Review-when` for an ADR, `## Expiry conditions` for a skill |
| Defer | skill: file it as a `draft` in your task ledger (the author's harness uses `rfc-writer`) (in a small repo with a single table, one line in `.notes/TASKS.md`) |
| Keep | leave a 1-line reason (it becomes grounds for future stocktakes) |

## Out of scope

- A standalone build-or-not decision on something not yet built → a fresh-context build-or-not judge (the author's harness uses the `architect` agent; zero-base test). This skill answers "if it is built,
  in which layer and until when"
- Validity of loop structure (servo / decidability / damping) → a loop-design review (the author's harness uses `loop-design-check`)
- Bulk cross-check at a model generation change → skill: `generation-audit`
- Human portability (whether others can install and use it) → `skill-creator/references/portability.md`

## Expiry conditions

- When the substrate natively handles judgments about layer decomposition, portability, and obsolescence, and asks them on its own when
  the harness changes, this skill retires (Downward, `rules/common/akc-cycle.md`)
- If the 6-layer division itself breaks down (e.g., eval is absorbed into model capability, the boundary between skill and data
  disappears), rewrite the division. Questions A–F are expected to outlive the division
- If this skill exceeds 150 lines, apply the 6 questions to this skill itself

## Related

- A build-or-not judge (the author's harness uses the `architect` agent) — the up-front twin: build-or-not. This skill answers "if it is built, in which layer and how far"
- A loop-design review (the author's harness uses `loop-design-check`) — isomorphic to its Step 0 subtract gate (subtract before adding)
- `generation-audit` — after-the-fact cross-check at a generation change. This skill is up-front judgment at design time; the evidence flows in the same direction
- `rules-stocktake` / `skill-stocktake` / `agent-stocktake` — the source of truth for verdicts. For installed assets, this skill's
  Delete / Move become evidence for these
- `rules-distill` — criteria for promoting skill → rule (tests 1–3 are the rule version of questions A and B)
- `rules/common/akc-cycle.md` — Scaffold Dissolution (Inward / Downward). Question C is its predictive version
- ADR-0012 / 0015 / 0038 — precedents for runtime portability (skills → shared via symlink, rules → reference-first,
  hooks / permissions are outside sharing but the hooks wiring section is portable). The measured grounds for question D
