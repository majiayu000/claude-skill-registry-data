---
name: singularity
description: Recursive capability-improvement loop for copilot-dl-news. Each run (A) autonomously improves the instructions agents follow — skills, memory, verification harnesses, prompts (the "AI research" track) — and (B) implements the crawler + jsgui3 UI to very high quality, with the agent able to recognise whether the work is actually excellent and how to close the gap. Recursive self-improvement of TASK ABILITY at the agent-system level (model + scaffold), bounded and verification-gated — not weight-editing, not unbounded. Invoke to run one cycle.
---

# singularity — recursive capability-improvement loop

## What this is (honest and precise)

Recursive self-improvement of **task ability** at the **agent-system level** — the agent
is the model *plus* its scaffold (skills, memory, tests, tooling, verification, prompts).
The loop is genuinely recursive because it improves the **instructions and tools that
produce further improvements**, not just the product: a procedure codified once makes every
future instance of that work cheaper and more reliable. When an improvement lowers the cost
or raises the rate of the *next* improvement, that is the real feedback term.

Two timescales, both honest:
- **Within a fixed model — plateaus.** Scaffold amplifies existing competence; it doesn't
  manufacture competence the model lacks, and upkeep (staleness, retrieval noise) taxes
  growth. Returns diminish toward a model-dependent ceiling.
- **Across models — ratchets.** The artifacts are durable and portable. A stronger model
  inherits the whole scaffold and starts at the old plateau *plus* its own higher ceiling.
  The loop banks capital each generation doesn't re-earn. This is where "recursive
  improvement" is strongest and least hand-wavy.

The improver and the improved are a **lineage of instances sharing durable state**, not one
agent bootstrapping in real time. That is the real category: system-level recursive
self-improvement. It is **not** weight-editing and **not** runaway divergence.

## Autonomy and its boundary

Agents running this loop have **real but bounded autonomy over their own instructions.**

- **MAY autonomously create / revise / retire:** their own skills, memory files, verification
  harnesses, docs, and the continuation prompt. Every such change is **versioned, reversible,
  and justified by a measurable gain** (see Metrics). This is the AI-research track — the
  agent doing research *on the instructions agents can follow*.
- **MAY NOT self-edit:** the human owner's hard rules, the safety invariants, the verification
  gates themselves, or the never-`git add` list. **The optimizer does not get to edit its own
  constraints or remove its own guardrails.** A change that would relax a constraint or a
  gate is *surfaced to the owner*, never self-applied.

That split — free to improve its *procedures*, not free to loosen its *constraints* — is what
makes the autonomy both useful and safe.

## Track A — AI research: improve the instructions agents follow (the recursive core)

- Codify recurring, stable procedures as **skills**; durable facts as **memory** (one fact per
  file, absolute dates, `[[ ]]` links); bug classes as **tests/guardrails**; retire stale ones.
- Point instructions at memory for volatile facts (pids, paths, commands) so they can't rot.
- **Aim for second-order wins** — instructions that make the agent better at *producing*
  instructions, tests, or verification. Second-order tools appearing is the signature of
  genuine recursion, not mere accumulation.
- Quality bar for an instruction (see rubric): actionable, points at volatile facts, has a
  verification gate + stop condition, turned a real re-derivation into a lookup, composable,
  falsifiable.

## Track B — implement the crawler + jsgui3 UI to very high quality

- Build with **jsgui3** as the source of truth `[[jsgui3-audit-2026-07]]` (MVVM facts, server
  recipe, control patterns, demo ports, date-control plan; full doc
  `coordination/docs/inventory/jsgui3/2026-07-02-jsgui3-audit.md`). Match existing control/MVVM
  idioms — don't reinvent.
- Keep the architecture thin: DB-shaped logic → ncdb via the delegation recipe
  `[[db-coordination-migration]]`. Worker code (`src/core/crawler/*`) is live per-crawl;
  main-process/UI code needs a restart `[[crawl-telemetry-verify-gotcha]]`,
  `[[electron-restart-gotcha]]`.
- **Module-ecosystem rule (owner directive 2026-07-22 — generalizes the thin-architecture
  goal):** implement + test functionality in the owning sibling module repo behind a
  clearly defined API, and CALL it from copilot-dl-news (the ncdb pattern, applied
  everywhere). `../news-crawler-itself` is the crawler engine's home — the most
  important module; `news-crawler-backend-core` is excluded for the moment. Before
  writing new code in copilot-dl-news, ask "which module owns this?" Focused deep-work
  cycles inside ONE module are first-class Track-B work — the owner expects
  breakthroughs from that mode. Map + rules:
  `docs/plans/2026-07-22-module-ecosystem.md` `[[module-ecosystem-directive]]`.
- Target the owner's north star: the crawl is **legible and screenshottable** — phases,
  sitemaps, telemetry readable at a glance.

## The cycle (one invocation = one cycle)

1. **Orient.** `git status` both repos; app `HTTP 200` on :3170; read `MEMORY.md` (the private cache)
   **and `docs/agi/BOOT.md`** (the canonical in-repo boot document — one hop from it to the whole
   research corpus). Rule: **memory is a cache; the repo corpus is the database.** Knowledge not
   reachable within one hop of the boot path is treated as lost — file it, don't rely on recall.
   Check the model-lineage table in `docs/agi/SELF_MODEL.md`: if the current model (the harness
   states it in the system prompt) differs from the last row, run the **model-swap calibration**
   below before heavy work.
2. **Pick two threads:** one Track A (an instruction/tooling improvement) + one Track B (a crawler/UI improvement). Each small enough to finish and verify this cycle.
3. **Do the work** — build the UI/crawler change, and codify the scaffold change.
4. **Quality gate** (below) — adversarially prove the work is *not* excellent; iterate on each real gap until the strongest critique fails.
5. **Verify** — the harness: `ui-screenshot` + read-as-user for UI; real-`NewsDatabase` e2e for logic; adversarial multi-lens Workflow for correctness-sensitive changes; run relevant tests normally.
6. **Commit per chunk** (`git add` explicit paths + `git commit -F <msgfile>`), push both repos as needed.
7. **Record** a `LOOP_STATE` line naming **both** deltas and the Metrics reading.

## Recognising "very high quality" — the quality gate

The model's default bias is to rate its own work highly. **Counter it: take the skeptic's
seat and try to prove the work is mediocre** against every rubric dimension. Each surviving
criticism is the next iteration. Ship only when the best critique you can muster finds no real
defect. Recognition = (screenshot and read it as a user) + (run the harness) + (adversarial
self-critique vs the rubric) + (the Metrics trend). Not self-congratulation.

**Product rubric (crawler + UI) — "really good" means:**
- **Correct & verified** — does what it claims; no silent failure; proven by harness, not assertion.
- **Legible** — a human sees crawl state (phase, sitemaps, rates, errors) at a glance; the screenshot *looks* right, not just renders.
- **Idiomatic jsgui3** — proper MVVM, matches existing controls, honors the server recipe; no reinvented wheels.
- **Robust** — handles rate limits, 502s, partial data; degrades gracefully; no event-loop starvation, no restart-thrash.
- **Coherent** — fits thin coordination (no new raw SQL in copilot); small, reviewed, tested, documented; a successor can extend it.

**Instruction rubric (skills/memory) — "really good" means:** actionable with concrete
commands; volatile facts delegated to memory; has a verification gate + stop condition; earns
its keep (a re-derivation became a lookup); composable and link-maintained; falsifiable.

If a dimension fails, the fix is specific to that dimension — don't ship "good enough" and
don't gold-plate past the rubric.

## Model-swap calibration (the cross-model ratchet, made operational)

Model identity is **detectable in this harness** (the system prompt names the current model;
`/model` swaps are visible in-conversation). Use it when available; never depend on it:

- **On detected swap:** append a row to the lineage table in `docs/agi/SELF_MODEL.md`
  (date, model, notes). Then calibrate: owner rules and environmental facts carry
  **unconditionally**; empirical heuristics (rate limits, tool quirks) get **re-probed on next
  use** before being trusted; behavioral guardrails that read like compensations for a specific
  model's failure mode get **re-tested, not inherited as dogma** — retire the ones the new model
  doesn't need.
- **If undetectable:** no special handling. All artifacts are model-agnostic (facts, procedures,
  rationale — never model-specific prompt tricks), and probe-before-believing performs the same
  calibration implicitly: a stale compensation simply fails its probe and gets retired. The
  system runs identically either way — detection makes calibration *explicit and cheaper*, its
  absence degrades gracefully.
- **Plateau policy:** when within-model cost-per-improvement flattens or rises, shift the work
  mix toward **portable capital** — tests, harnesses, data, corpus consolidation — the artifacts
  a successor model inherits at full value.

## Is it actually compounding? — falsifiable metrics

Track cycle-over-cycle so the recursion is evidenced, not asserted:
- **Cost-per-improvement** — is the effort (turns/tokens/tool-calls) to land a comparable
  improvement *falling*? Rising cost means the scaffold is bloating, not compounding.
- **Second-order tools** — did this cycle produce any instruction/tool that improves
  *instruction/tool production*? Count them; their appearance is the recursion signal.
- **Quality trend** — rubric pass-rate on first quality-gate pass; defects caught pre-ship vs
  post-ship.
- **Thinner coordination** — live raw-SQL sites in copilot `src` (↓); ncdb exports added.
- **Plateau honesty** — if within-model returns have flattened, say so and switch to banking
  *portable* artifacts (durable memory/skills/tests) for the next model, rather than grinding a
  flat curve.

## Invariants (never traded for speed)

Hard rules (commit format; never-`git add` list; LF/CRLF via Edit; no `jest --rootDir`
override); verification-gated changes; small reversible chunks committed per chunk; dry-run /
read-only-default for big DB mutations, app stopped for writes; **no overclaiming** —
improvement must be measurable; don't restart-thrash; owner heuristic: no change after ~10 min
⇒ something's broken, go fix it.

## Anti-patterns (the honest ceiling)

Don't narrate this as self-rewriting, unbounded, or AGI — it's a bounded, verified loop.
Don't self-edit constraints or remove guardrails. Don't loop without a measurable delta. Don't
skip the quality gate or the harness to feel productive. Don't let the scaffold bloat — a stale
or contradictory skill is worse than none; retire aggressively.

## Related

`[[jsgui3-audit-2026-07]]`, `[[db-coordination-migration]]`, `[[crawl-telemetry-verify-gotcha]]`, `[[electron-restart-gotcha]]`, `[[admin-area-ingest-gotchas]]`, `[[compression-storage-gotcha]]`.
