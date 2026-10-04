---
model_tier: inherit
name: "refine-prompt"
description: "Reconstruct a free-form prompt into actionable AC + assumptions + confidence band before the engine plans — '/work \"…\"', 'baue X', 'ist der Prompt klar genug für die Engine?'."
personas:
  - developer
  - senior-engineer
  - ai-agent
domain: product
scope:
  write: []
  verification_reason: "execution.handler is internal, so this skill spawns no subprocess — writes happen through the agent's declared allowed_tools. No command can prove a scope the skill never executes."
execution:
  type: assisted
  handler: internal
  allowed_tools: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# Refine Prompt

> Move a free-form prompt from "raw text" to "engine-ready" in one run.
> Produces reconstructed acceptance criteria, explicit assumptions,
> and a confidence band that decides whether the engine proceeds
> silently, halts for confirmation, or refuses to plan.
>
> Sibling of [`refine-ticket`](../refine-ticket/SKILL.md) — same
> reconstruction-of-intent pattern, different input shape. Tickets
> arrive structured (id, title, AC); prompts arrive as one string.

## When to use

- The user invokes `/work "<prompt>"` or pastes a free-form request.
- The dispatcher hits `input.kind="prompt"` in the `refine` step.
- A prompt looks ambiguous, broad, or scope-undefined and the user
  asks "ist das klar genug, um loszulegen?".
- Before any plan/apply step on prompt-driven work — never after.

## When NOT to use (near-misses)

| Phrasing | Route to |
|---|---|
| "refine this ticket" | [`refine-ticket`](../refine-ticket/SKILL.md) |
| "estimate this prompt" | not supported — score then estimate downstream |
| "plan this feature" | `/feature-plan` (downstream) |
| "is this a duplicate?" | `validate-feature-fit` (sub-skill, post-refine) |

`refine-prompt` is the *first* gate on prompt-driven flow. It does not
plan, does not implement, does not write back anywhere.

## Input

Exactly one path: a non-empty raw string carried in
`state.input.data.raw` (built by [`work_engine/resolvers/prompt.ts`](../../templates/scripts/work_engine/resolvers/prompt.ts)).
No branch detection, no URL parsing, no clipboard fallback — the
calling command (`/work`) owns prompt capture; this skill only refines.

If `raw` is missing, empty, or whitespace-only the resolver already
raised `PromptResolverError`. The skill never receives that input.

## Modes and bypass

The skill honours `prompt_optimization.inbound` (or
`prompt_optimization.default` when no inbound override is set) from
`.agent-project-settings.yml` / `.agent-settings.yml`. Three modes:

| Mode | Behaviour |
|---|---|
| `off` | The skill is a no-op. The dispatcher writes `confidence={"band":"high","score":1.0}` directly and the engine proceeds with the literal prompt. No assumption inference, no clarifying questions. |
| `mini` | Stack-aware light shaping. Steps 1-2 run; step 3 only emits `assumes:` lines for *implicit stack constraints* (framework, package manager) detected from config files. Steps 4-5 produce 3 AC bullets max. Low-band halts ask at most one question; medium-band halts are auto-confirmed silently. |
| `max` *(default)* | Full procedure — every step 1–6 runs. Medium-band halts surface the assumption list verbatim; low-band halts ask one clarifying question. This is the existing behaviour. |

**Bypass prefix.** If the raw prompt starts with the configured
`prompt_optimization.bypass_prefix` (default `/raw`), the skill
becomes a no-op regardless of mode. The dispatcher strips the
prefix, passes the remainder through verbatim, and records
`bypass:true` in the envelope so downstream surfaces (delivery
report, `--no-prose-synthesis`) can attribute the skip.

```
/raw migrate auth.service.ts to use jose, keep the API shape
```

`/raw` is reserved at the prompt boundary only — it has no meaning
mid-prompt and is not stripped when it appears inside the body.

### Stack-config read (mini / max only)

When the mode is `mini` or `max`, step 3 may read these config files
(read-only, scope-locked) to enrich the `assumes:` block:

- `package.json` — JS / TS framework detection (Next.js App vs Pages,
  Remix, SvelteKit, Astro, Expo, …)
- `composer.json` — PHP framework detection (Laravel, Symfony,
  framework-less)
- `pyproject.toml` / `requirements.txt` — Python framework detection
- `CLAUDE.md` / `AGENTS.md` — project-declared stack hints
- `.cursorrules` — project-declared stack hints
- `tsconfig.json` — TS path-alias / module-resolution hints

The skill MUST NOT read source files, `.env*`, secrets, or user
data. Detection lands as a single `assumes: stack=<framework>@<version>`
line; the medium-band halt is the user's chance to flip it.

## Procedure

### 1. Read and analyze the prompt

Examine the raw text top to bottom *before* changing anything in
state. Identify the *single* desired outcome in one sentence —
verb + object + observable result. If the prompt names two
unrelated outcomes (e.g. "fix login AND refactor the dashboard"),
record both but flag scope-overload in step 5; the score will
land in `medium` or `low`.

This is an analysis pass, not an execution pass. The skill does
not modify the prompt, infer code changes, or call any tool — it
investigates the input and produces a structured envelope the
dispatcher reads.

### 2. Enumerate explicit constraints

Pull every concrete signal from the prompt verbatim:

- **Files / modules** named in the text (`UserController`,
  `auth.service.ts`, `migrations/2024_…`).
- **Behaviour anchors** — endpoints, routes, commands, fixtures.
- **Hard rules** — "must not break X", "without changing the API",
  "keep backwards compat".

Constraints come from the prompt only. Inferred constraints belong in
step 3 (assumptions), never here.

### 3. Infer reasonable assumptions

Anything the prompt implies but does not state. Examples:

- "fix the login bug" → assumes the bug is in the existing `auth/`
  module (no new auth provider).
- "add caching" → assumes the project's primary cache driver
  (per `.agent-settings.yml` / `config/cache.php`).
- "speed up the export" → assumes "faster" means runtime, not memory.

Each assumption is a single line, prefixed with `assumes:`. The
medium-band halt surfaces them verbatim — no rewording, no
explanations.

### 4. Generate the AC list

Three to seven bullet points. Each bullet is observable and
testable in the project's existing test surface (Pest / Jest /
pytest / etc.). Avoid:

- "works correctly" / "is fast" / "looks better" (untestable)
- "no regressions" (the test suite already covers that)
- "follows best practices" (not an AC)

Anchor each bullet to a constraint from step 2 or an assumption from
step 3 — never both implicit.

### 5. Score confidence

Delegate to [`work_engine/scoring/confidence.ts`](../../templates/scripts/work_engine/scoring/confidence.ts):

```ts
import { score } from './work_engine/scoring/confidence.js';
const result = score({ raw: promptRaw, ac: reconstructedAc, assumptions });
// result.band ∈ {"high", "medium", "low"}
// result.score ∈ [0.0, 1.0]
// result.dimensions: Record<string, number>  // 0–2 per dimension
// result.reasons: string[]                   // human-readable rationale
```

The rubric (5 dimensions × 0–2, sum / 10) and band thresholds
(`high ≥ 0.8`, `medium 0.5–0.79`, `low < 0.5`) are owned by
`confidence.ts`. Do not re-derive them in prose.

### 6. Self-review (3-scan checklist)

Before emitting the envelope, run these three scans. Each is a fast pass; failure blocks emission.

1. **Spec coverage** — every concrete signal from step 2 (constraints) and step 3 (assumptions) is reflected somewhere in the AC list. Walk the constraint list top-to-bottom; each must anchor at least one AC bullet or appear in the *Assumptions* block.
2. **Placeholder / TODO scan** — the rendered envelope contains no `<placeholder>`, `TODO`, `FIXME`, `tbd`, `???`, `XXX` strings. The literal angle-bracket placeholders in the template (`<one sentence …>`, `<bullet>`) must be replaced with concrete text before emission.
3. **Type / shape consistency** — every named file, module, route, or command in the AC matches the project's existing conventions. If the prompt names `auth.service.ts` but the codebase uses `AuthService.php`, surface the mismatch in *Assumptions* rather than adopting the prompt's spelling.

Source: adapted from an external reference.

## Band-action mapping

The `refine` dispatcher step in `directives/backend/refine.ts` reads
the score and returns one of three outcomes — the skill does not
decide the action, only produces the inputs.

| Band | Outcome | What the user sees |
|---|---|---|
| `high` | `SUCCESS` | Silent proceed; AC + assumptions land in the delivery report |
| `medium` | `PARTIAL` | Assumptions report halt: numbered list of `assumes:` lines + AC, user confirms or edits |
| `low` | `BLOCKED` | One clarifying question (per [`ask-when-uncertain`](../../rules/ask-when-uncertain.md) Iron Law) |

## Output format

The skill emits a structured envelope; the dispatcher renders it.
Required fields, in order:

1. **Goal** — single sentence, verb + object + observable result
2. **Acceptance criteria** — numbered list, 3–7 entries, each
   anchored to a step-2 constraint or a step-3 assumption
3. **Assumptions** — bullet list, each line prefixed `assumes:`
4. **Confidence** — band + score + per-dimension breakdown from
   `work_engine.scoring.confidence`

The shape below is the rendered surface for `medium` / `low`
halts; for `high` the same envelope lands in the delivery report
without a halt.

````markdown
## Reconstructed prompt

**Goal:** <one sentence, verb + object + observable result>

**Acceptance criteria:**
1. <bullet>
2. <bullet>
3. <bullet>

**Assumptions:**
- assumes: <line>
- assumes: <line>

**Confidence:** medium (0.62) — goal_clarity 2 · scope_boundary 1 · ac_evidence 2 · stack_data 1 · reversibility 0
````

For `low`, the question replaces the AC list:

```
> The prompt does not name <missing dimension>.
>
> 1. <option that resolves the gap>
> 2. <alternative resolution>
> 3. <skip / abandon>
```

## Gotchas

- The model invents AC that *sound* observable but aren't anchored
  in the prompt or a concrete file. Every AC must trace to a step-2
  constraint or a step-3 assumption — no free-floating bullets.
- Assumptions are not commitments. The medium-band halt is the
  user's chance to flip them; the skill never asserts an assumption
  as fact.
- The scorer is heuristic, not LLM-based. Token count is not a
  signal — a 200-word prompt can score `low` if the goal is vague,
  and a 20-word prompt can score `high` if scope is unambiguous.
- UI-shaped prompts ("redesign the dashboard", "make the form
  prettier") score `low` on `stack_data` until R3 lands the UI
  directive set; band-action is a pointer to R3, not a refusal.

## Do NOT

- Do NOT call this skill on `input.kind="ticket"` — that path runs
  through [`refine-ticket`](../refine-ticket/SKILL.md).
- Do NOT auto-confirm assumptions on the user's behalf in the
  medium-band halt. The halt is the contract.
- Do NOT stack multiple clarifying questions in the low-band halt.
  Iron Law: one question per turn.
- Do NOT mutate `state.input.data.raw`. The original prompt stays
  verbatim for replay; reconstructed output lands in
  `data.reconstructed_ac` and `data.assumptions`.
- Do NOT re-derive band thresholds in prose. They live in
  `confidence.ts` and only there.
- Do NOT read source files, `.env*`, secrets, or arbitrary user
  files when stack-detecting in mini / max mode. The allowlist
  above (`package.json`, `composer.json`, `pyproject.toml`,
  `requirements.txt`, `CLAUDE.md`, `AGENTS.md`, `.cursorrules`,
  `tsconfig.json`) is exhaustive.
- Do NOT strip the `bypass_prefix` mid-prompt. The prefix is only
  recognised at the prompt boundary; matches inside the body stay
  literal.
- Do NOT silently rewrite the prompt in `max` mode without
  surfacing the assumption list on a medium-band halt. The diff
  is the contract.

## See also

- [`refine-ticket`](../refine-ticket/SKILL.md) — sibling for ticket-shaped input
- [`prompt-optimizer`](../prompt-optimizer/SKILL.md) — engine-outbound sibling; same `prompt_optimization` setting controls its mode
- [`work_engine/resolvers/prompt.ts`](../../templates/scripts/work_engine/resolvers/prompt.ts) — envelope builder
- [`work_engine/scoring/confidence.ts`](../../templates/scripts/work_engine/scoring/confidence.ts) — rubric + band thresholds
- [`ask-when-uncertain`](../../rules/ask-when-uncertain.md) — one-question-per-turn Iron Law
- [`artifact-drafting-protocol`](../../rules/artifact-drafting-protocol.md) — this skill was drafted under it
- AI Council session: `agents/runtime/council/responses/prompt-master-mini.json` (2026-05-17) — analysis behind the mini/max split and `/raw` bypass <!-- council-ref-allowed: ADR decision trace -->
