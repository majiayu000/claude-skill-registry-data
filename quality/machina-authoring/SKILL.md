---
name: machina-authoring
description: >-
  Author valid, high-scoring state machines in Machina machine JSON format (spec v3.0.0 /
  v2.0.0 / v1.0.0). USE WHEN: writing or generating a machine definition (states, transitions, guards,
  actions, context, scenarios); modeling a real workflow (order fulfillment, refunds, signup,
  retries) as a Machina state machine; fixing or upgrading a machine JSON for validation or
  higher compliance score; explaining validation failures or low scores; running the bundled
  machina-validator.py CLI to validate, score, or generate gaps/scenarios; adding retry guards or cycle
  protection; or preparing machines for the compliance scorer ("Excellent" ≥90). DO NOT USE
  FOR: modifying the Machina simulator app, its engine, UI, or SPEC_REGISTRY (use
    machina-simulator-maintenance), debugging machine-validator.py scripts, XState config authoring,
  SCXML documents, or general diagramming.
metadata:
  version: 0.4.0
---

# Machina Machine Authoring

Guidance for writing state-machine definitions that open cleanly in the Machina simulator and
score well against its compliance scorer.

**Declaration-sound ≠ runtime-sound.** The scorer reads the definition and never runs a tool, so a
100 / "Excellent" score attests the JSON — never that a declared checker decides the right fact, or
that it would pass at runtime. Scoring a file from disk additionally verifies that one referenced
checker resolves (see "Compliance boundary"); nothing scores the rest.

## Glossary

Use these terms consistently — in prompts, output, and code comments:

| Term | Meaning |
|---|---|
| **Machina** | Brand name covering both the simulator app (served by the `machina-simulator` extension) and its machine schema spec. Qualify which: "**Machina simulator**" (the app) vs "**Machina schema spec**" (the JSON contract). Never use bare "Machina" where the referent is ambiguous. |
| **State machine** | The modeled FSM itself. Always write "state machine", never bare "machine". |
| **Machine definition** | The JSON document that encodes a state machine (the artifact you author). A file contains one definition. |
| **Schema spec / spec version** | The versioned field contract (`v1.0.0`, `v2.0.0`, `v3.0.0`) a definition targets via `spec_version`. Distinct from the definition's own `version` field. |
| **Final state** | A state typed `"type": "final"` (or with no outgoing transitions). Prefer "final state" over "terminal" — matches UML/XState. |
| **Event** | Named trigger (`UPPER_SNAKE`) that fires a transition from a state's `on` map. |
| **Transition** | `{ EVENT: { target, guard?, actions? } }` — moves between states. |
| **Guard** | Declarative predicate `{ type:"compare", key, op, value }` gating a transition. Matches SCXML/XState semantics. |
| **Action** | Declarative side effect `{ type:"increment"\|"assign" }` on context. No code strings, ever. |
| **Context** | Extended state data available to guards/actions; supports dotted paths. |
| **Scenario / entry point** | A named start into the state machine (`scenarios[]` with `initial`, `interface ∈ UI·API`). |
| **Checker** | A named script in `tools[]` that inspects the world and reports — read-only, never a mutator. |
| **Evidence** | A live reference to a checker from a state `checks[]` or a transition `requires[]` (the slots the driver executes). A reference from `ensures[]` or `invariants[]` never runs, so it is not evidence. |
| **Compliance scorer** | The deterministic 24-check evaluator producing score/grade/findings (in-app or via `machine-validator.py`). 22 checks are weighted (total weight 100 at v2.0.0, 134 at v3.0.0); `spec-version` and `tools-exist` are weight-0 informational review checks, and the whole `tools` family is `since 3.0.0`, so v1/v2 targets are graded without it. Not "checker", "linter", or "validator" (validation is only its blocking subset). |
| **Finding / gap** | Any check result. Failing findings are "gaps": `auto` (deterministically fillable) or `review` (needs human judgment). Only `auto` findings appear in the `gaps` patch list — a failed `review` check such as `tools-exist` or `checkers-used` appears in `score` output and never in `gaps`, and `apply` never re-scores. |

## Minimal viable machine

Every state machine definition needs at minimum: `id`, non-empty `states`, `initial` resolving
to a state key, and every transition `target` pointing at an existing state key.

```json
{
  "id": "order-fulfillment",
  "name": "Order Fulfillment",
  "version": "1.0.0",
  "spec_version": "3.0.0",
  "initial": "pending",
  "context": { "attempts": 0 },
  "scenarios": [
    { "id": "default", "label": "Default", "initial": "pending", "interface": "API" }
  ],
  "states": {
    "pending": {
      "description": "Awaiting payment confirmation.",
      "on": {
        "PAY": { "target": "paid", "actions": [{ "type": "assign", "key": "attempts", "value": 0 }] },
        "RETRY_PAY": { "target": "pending", "guard": { "type": "compare", "key": "attempts", "op": "lt", "value": 3 }, "actions": [{ "type": "increment", "key": "attempts" }] }
      }
    },
    "paid": { "description": "Payment confirmed.", "on": { "SHIP": { "target": "shipped" } } },
    "shipped": { "type": "final", "description": "Order delivered to carrier." }
  }
}
```

This example is deliberately free of evidence, so it scores as a *viable* definition rather than an
Excellent one — a v3.0.0 definition needs a checker before it can reach the top band (see step 7).

## Authoring workflow

1. Read [references/schema-spec.md](references/schema-spec.md) — full field reference, naming
   conventions, guard/action semantics.
2. Model states first: identify every distinct status, mark true final states `"type": "final"`
   explicitly (never rely on implicit finals).
3. Wire events with declarative objects only — guards `{type:"compare",…}`, actions
   `{type:"increment"/"assign",…}`. Never embed code strings; the format must stay shareable and
   safe to ingest.
4. Add `scenarios[]` entry points (`{id, label, initial, interface ∈ "UI"|"API"}`) — one per
   meaningful way the workflow starts.
5. If any path can loop (retry, rework), add a genuine counter in `context`
   (`retry`/`attempt` naming) and gate the looping transition with a `compare lt` guard against
   it — this is the only pattern the compliance scorer recognizes as cycle protection.
6. Give every state a real, human `description` — placeholder text is auto-detectable
   (`generated: true`) and reads as a gap.
7. Declare evidence — a v3.0.0 definition needs at least one **usable checker**: a script beside the
   machine (`scripts/check_<fact>.py`), registered in `tools[]` with a path-bearing `cmd` and
   `expect_exit: 0`, and referenced from a state `checks[]` or a transition `requires[]`. The scorer
   weights that declaration (`checkers-used`), and when you score a file from disk it also verifies
   the required checker's script resolves — but the *other* tools in the registry are only reported
   (`tools-exist`, weight 0), so confirm their `cmd` paths yourself. Deriving the facts and the script
   contract: [references/checker-scripts.md](references/checker-scripts.md).
8. Validate & score — use the bundled deterministic engine (see below) or open in Machina:
   `validate` → iterate → target **≥90 ("Excellent")** via `score --text`.
   - Gaps flagged `auto` can be applied deterministically with the script's `apply`
     (or "Generate missing" in-app). `apply` rewrites the file only — it never re-scores, so run
     `score --text` again to see the result.
   - Gaps flagged `review` need your judgment: missing transitions, convention renames, event/state
     naming, unreachable states, missing evidence. They never appear in the `gaps` patch list — read
     them in `score` output. See [references/machine-quality.md](references/machine-quality.md) for what each
     check demands.
   - Finish only when `score --text` is at target **and** every `tools[].cmd` path token resolves next
     to the machine: only the one checker `checkers-used` requires is scored, and `tools-exist` reports
     every other dangling path at weight 0 — so it stays invisible to `gaps`. Never present a score as
     proof that the checkers exist or work.

## Hard rules

- Declare `"spec_version": "3.0.0"` explicitly so scoring never assumes latest silently. (`spec-version`
  is a weight-0 informational check, so nothing punishes an omission — and the target you declare decides
  whether the v3 `tools` checks apply at all.)
- Event names `UPPER_SNAKE`; state keys `kebab-case`.
- Guard `value` may be a literal number/string or a context-key name (resolved then numeric-coerced).
- Context paths support dotted notation (`"payment.attempts"`).
- Terminal = `type:"final"` or no outgoing transitions — prefer an explicit **final state**.

## Deterministic tooling — use the bundled script

All deterministic authoring logic from the Machina simulator (validation, the 24-check
compliance scorer, gap analysis, autofill patching, scenario generation, cycle detection,
coverage building) is bundled as a standalone CLI. Run it instead of re-deriving logic or
loading simulator source:

```powershell
# From workspace root; python3 on Linux/WSL
python3 skills/machina-authoring/scripts/machine-validator.py <command> <machine.json> [options]
```

| Command | Purpose |
|---|---|
| `validate <file>` | Hard structural errors (blocking) — run first, always |
| `score <file> [--text] [--spec V]` | Full compliance report; JSON by default, `--text` for summary |
| `gaps <file>` | Ordered list of deterministic auto-fillable patches |
| `apply <file> id… [-o out.json]` | Apply selected patches (fixed order); default overwrites input |
| `scenarios <file>` | DFS-generated terminal paths + transition coverage % |
| `cycles <file>` | Cycle findings (CRITICAL depth / HIGH unguarded / MEDIUM valid) |
| `coverage <file>` | Exact coverage block "Generate missing" would embed |

Typical authoring loop: `validate` → iterate → `score --text` until ≥90 → `gaps` for remaining
auto-fillable items → `apply` (or hand-fix review items — they never appear in `gaps`) → confirm every
`tools[].cmd` path resolves → final `score`.

**Known divergences (deliberate, both ported-script-side):**

1. The simulator source's check-inclusion filter (`specRank(since) <= specRank(target)` over
   newest-first ranks) inverts v1/v2 inclusion versus §14's documented model. The ported script
   implements the documented semantics (all 17 checks at v2.0.0, weight = 100).
2. The ported script carries a **v3-only check set the simulator's engine does not have** (24 checks /
   134 at v3.0.0, against the simulator's documented 17 checks / total weight exactly 100). The
   in-app scorer therefore grades v3.0.0 definitions differently from `machine-validator.py`.

When editing the simulator itself, follow
[the machina-simulator extension's canonical maintenance docs](../../copilot-extensions/machina-simulator/simulator/docs/maintenance.md)
and keep these divergences in mind.

### Compliance boundary — what the scorer does and does not verify

The scorer analyzes the machine **declaration** only; it never executes anything:

| What it verifies | What it does NOT verify |
|---|---|
| Schema structure, internal consistency, reference resolution (targets, tools, `else_target`) | That any declared tool's **runtime behavior** actually holds |
| `tools[]` registrations are well-formed and referenced correctly | That a `checks[]`/`requires[]`/`ensures[]` predicate will **pass when run** |
| `checkers-used` (weight 15) — one checker is referenced from a driver-executed slot, by path, expecting exit 0, and (when the machine directory is known) resolving on disk | That the checker decides the fact it claims to decide. `python3 -c pass` is caught; a script that inspects the wrong thing is not |
| `tools-exist` — per tool, whether a path-bearing `cmd` resolves to a file on disk (weight-0 **review** check; static file-stat, no execution) | That a pathless `cmd` (e.g. `python3 check.py`) is checkable at all — it is skipped and passes — nor that a present script is correct, safe, or even runnable |

Consequences to teach authors and consumers alike:

- **"Score 100 / Excellent" means *declaration-sound*, not *runtime-sound*.** A machine can score
  100 while a tool's script fails in practice — the scorer never runs it.
- The scorer **never executes** checker scripts. Only the driver actually runs them; see the
  companion `machina-driving` skill's "Trust boundary" for where runtime verification happens.
- `checkers-used` (weight 15) is the one check that weights evidence, and it is deliberately
  context-sensitive in a single bit: `score <file>` also verifies that the required checker's script
  resolves on disk, while in-memory callers (the driver's gate, unit tests, temp workspaces) judge the
  declaration only, because they have no directory to look in.
- `tools-exist` is **informational** (weight 0): a dangling `cmd` reports a `warn`/review finding
  without lowering the score. When the machine file is scored from disk its machine-relative paths are
  stat'd; in in-memory or workspace-copied contexts with no resolvable directory the check passes
  trivially. A pathless `cmd` is skipped in both cases, and only the first path-bearing token is stat'd.
- `validate` (structural errors) and `score`'s `blocking` findings cover identity and structure only —
  `id-present`, `states-present`, `initial-resolves`, `targets-resolve`. Everything else, including
  evidence, is quality guidance.

## Reference map (load on demand)

| File | Load when |
|---|---|
| [references/schema-spec.md](references/schema-spec.md) | Any authoring work — field tables, versioning, guard/action semantics |
| [references/checker-scripts.md](references/checker-scripts.md) | Any v3.0.0 definition that needs evidence — deriving the facts, the script contract, which slots execute, the skeleton |
| [references/machine-quality.md](references/machine-quality.md) | Scoring below target, or proactively before finishing a definition — per-check author guidance, grade bands, review-vs-auto findings |

## Naming discipline in generated output

When authoring definitions or writing about them: say "state machine" or "machine definition"
(never bare "machine"), qualify "Machina simulator" vs "Machina schema spec", and use "final
state", "compliance scorer", "checker" vs "evidence", and "finding/gap (`auto`/`review`)" per the
glossary. Field-level vocabulary
(`guard`, `action`, `event`, `transition`, `context`, `scenario`) is already industry-standard —
keep it verbatim.
