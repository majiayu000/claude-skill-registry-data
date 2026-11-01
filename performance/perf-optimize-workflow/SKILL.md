---
name: perf-optimize-workflow
version: "1.0.0"
user-invocable: true
description: "Performance optimization paradigm workflow, proven across stacks: benchmark harness → evidence-validity gate (ten in-file disciplines: measurement artifacts, caliber pollution, device/profile mismatch, comparison environment state) → attribution → one-target-per-iteration optimization → A/B cross-run statistical verification → benchmark-log sediment, on an environment-gated iteration loop (no loop runner ⇒ honest stop). Seeds per-project code-insight/code-optimizer skills with probe scripts and evolves them every campaign (stack corpus in reference.md). Triggers — 「性能分析」「性能证据」「性能定位」「性能假设」「性能监控」「性能优化」「性能验证」「性能深入」「性能问题」「卡顿」「很慢」「前端性能」「Electron 性能」「伪影排查」「口径校准」「设备画像」 / performance analysis, perf evidence, locate bottleneck, perf optimization, perf verification, measurement artifact check. Do NOT use for non-performance bugs (solve-workflow) or trivial single-line edits."
dependencies:
  - clarifying-question-discipline
  - known-issue-research
---

# Performance Optimization Workflow

> Strong dependencies (frontmatter): `clarifying-question-discipline` (one question per turn), `known-issue-research` (known performance-pattern quick search at the locate stage). If any is missing, abort and print: `npx skills add FuDesign2008/open-skills -g --skill '*' --yes`.
>
> Runtime strong dependency (environment, not frontmatter): a loop-runner capability for the Stages 5-6 iteration loop — probed at Stage 5 entry; missing means optimization execution stops (see "Iteration loop").

## Scope

This workflow owns the full performance optimization paradigm: **build a reproducible benchmark, gate every conclusion through evidence-validity checks, attribute the bottleneck along the full chain, optimize one target per iteration, verify by A/B cross-run statistics, and sediment results in a benchmark log** — the optimize↔verify cycle running on an environment-provided iteration loop (honest stop when absent). Its per-project deliverables: the benchmark log + harness, and two **evolving project-level skills** (`code-insight` for attribution, `code-optimizer` for optimization) that carry the stack/project knowledge and improve with every campaign.

It answers: who triggers what expensive operation, under which conditions, on which devices — and then eliminates it measurably. Shipping/rollout decisions belong to the project, not this workflow.

**Paradigm provenance**: distilled from two complete campaigns on different stacks (a native C++ toolchain: 29.4s → 6.7s workload, -77%, byte-identical outputs; a large web rich-text editor: -27% commit time / -31% render volume / -34% memory, plus a multi-year user-jank attribution closed in four paths). The stages below are the stack-agnostic skeleton both campaigns followed.

## Layered architecture

| Layer | Lives in | Changes when |
|-------|----------|--------------|
| Paradigm + evidence disciplines (this file) | `SKILL.md` | Rarely — behavioral contract, versioned deliberately |
| Project attribution/optimization skills | The project's agent-skill directory (`code-insight`, `code-optimizer`) | Every campaign — seeded from the corpus, evolved from campaign lessons |
| Stack corpus (seed templates + evidence case archive) | [reference.md](reference.md) | Occasionally — stack chapters and cases refresh |

The paradigm is durable; the **project skills compound with every campaign** (that is where stack and project knowledge lives); the corpus is only the seed and needs occasional refresh. Keep perishable content out of this file.

## Trigger Recognition

Trigger words (each enters the workflow; with 「trigger + colon + space + description」 form, enters the named stage directly — colon/space punctuation is language-agnostic):

- **「性能分析」/「性能问题」/「卡顿」/「很慢」** or English equivalents ("performance issue", "it's slow", "jank") → enter at Stage 1
- **「性能证据」** → Stage 1: Benchmark & Evidence
- **「性能定位」/「性能深入」** → Stage 2: Locate the Bottleneck (「性能深入」 continues/deepens Stage 2)
- **「性能假设」** → Stage 3: Hypothesize the Root Cause
- **「性能监控」** → Stage 4: Build Toggleable Monitoring
- **「性能优化」** → Stage 5: Optimize
- **「性能验证」** → Stage 6: A/B Verify
- **「前端性能」/「前端性能优化」/「Electron 性能」** → Stage 1, with the frontend corpus in [reference.md](reference.md) as working knowledge until the project's `code-insight`/`code-optimizer` skills are seeded and mature
- **「伪影排查」/「口径校准」/「设备画像」** → evidence-gate mode: audit the suspect metric against the disciplines below before it drives any decision

Performance-related logs or a profile handed over for analysis also enter at Stage 1 or 2.

## General Principles

**先建基准再动刀，证据过闸才定罪，链路归因一锤定音，一轮一个目标，A/B 交叉说了算，负结果也留痕。** (Build the benchmark before cutting; convict only through the evidence gate; attribute along the full chain; one target per iteration; the A/B cross-run verdict rules; negative results leave traces too.)

1. **Data-driven**: no conclusion precedes its measurement. No reproduction path or analyzable data yet → the first task is building one (Stage 1), not hypothesizing.
2. **Evidence-gated**: every metric that feeds a decision must first pass the Evidence Validity Disciplines (in-file section below). Non-decision-grade numbers may inform, never convict.
3. **Single variable, reproducible**: each hypothesis resolvable to yes/no with existing data or minimal targeted instrumentation; each optimization touches exactly one root-cause point so its benefit is attributable; results reproducible and falsifiable — correlation is not causation.
4. **Full-chain, top-down**: from the user-perceived chain (macro) to the hotspot (micro); identify *where* it is slow (time/resource share), then *who* triggers it and *under what conditions*. Avoid blind-men-and-elephant local analysis.
5. **Production caliber & device profile**: acceptance numbers come from production-caliber builds; conviction-grade conclusions come from device-profile-calibrated runs (CPU-throttle matrix), not from high-end developer machines alone.
6. **No premature optimization**: optimize only problems that are measured, user-affecting, and over threshold. Preventive optimization without data adds complexity for nothing.

- **⚠️ Ask proactively**: follow `clarifying-question-discipline` — one question per turn, multi-round until clear, clarify before answering.

## Stage Flow

Forward: **evidence → locate → hypothesize → (monitor) → optimize → verify**, iterating optimize↔verify until the target is met or cost-effectiveness runs out.

Common jumps:

- Stage 1 lacks data and monitoring must be built first → Stage 4, then back to Stage 1.
- Stage 2's data already pins the bottleneck → skip Stage 3, go to Stage 4/5.
- Stage 6 refutes the hypothesis → back to Stage 2/3; optimization fell short → back to Stage 5.
- Intermittent issue hard to capture → prioritize Stage 4 long-term monitoring, return when it reproduces.

---

## Evidence Validity Disciplines

> Hard gate: a performance conclusion may drive an optimization decision only after passing these checks. The traps fall into four classes — **measurement artifacts** (the environment or tool distorts the number), **caliber pollution** (the number is real but measures something else), **device-profile mismatch** (true, but only on machines nobody complains about), and **comparison environment-state invalidity** (the A/B verdict itself was produced in a polluted environment). Full anonymized case archive with real numbers: [reference.md](reference.md) Part 4.

| # | Discipline | One-line rule |
|---|-----------|---------------|
| 1 | Environment-throttling artifacts | Frame/scheduling-class metrics from a controlled runtime (headless / occluded / backgrounded) are invalid until proven otherwise — background throttling can clamp frame callbacks by orders of magnitude and focus emulation does not lift it; detect by sampling the executor during the suspect window (idle-dominant ⇒ artifact); measure same-task instead (stimulus and measurement in one scheduling unit, so the runtime cannot defer work in between) |
| 2 | Monitor self-pollution | Instrumented builds can differ several-fold from production (monitor overhead + unoptimized code); dev caliber is for relative A/B trends only — optimization decisions use production caliber; on conflict with runtime-native metrics, the runtime wins |
| 3 | Framework counter ambiguity | Audit any framework-internal statistic on a small scale before trusting it (cross-reconcile independent counts against a native metric); magnitude contradiction means the counter is the artifact — counters are trend signals, never conviction evidence |
| 4 | Device-profile calibration | Conviction-grade conclusions need a CPU-throttle matrix (e.g. 1x/8x/20x) × path × scale; an unthrottled "innocent" verdict is invalid for low-end users — one workload can yield three verdicts across cells |
| 5 | Input-event authenticity | Every synthetic input load must verify the observable state delta (produced change == intended change); synthetic key/scroll events that bypass the product's real input pipeline are void regardless of driver-reported success |
| 6 | Instrumentation toggle lifecycle | Toggles read at load time must be injected before product scripts load (via the debugging protocol's pre-load injection capability); measurement spans ended by a deferred callback inherit environment throttling (discipline 1) — phase conclusions use synchronous spans plus native long-work counters |
| 7 | Single-sample extrapolation ban | Developer-machine data is not a user profile; negative-ROI conclusions need user-profile evidence (aggregated telemetry / support feedback / field data) — one account cannot extrapolate |
| 8 | Ultimate control experiment | When profilers show no code hotspot (runtime internals dominant), clone the live scene into a pure static copy (same environment, zero product logic) and run the same load under the same conditions: copy ≈ original ⇒ bulk is the physical cost of content scale × environment, and the optimization direction shifts to cutting that base cost; the difference is the product-code margin — the ceiling of code-level optimization; ablation rider: "mechanism exists ≠ mechanism works" |
| 9 | Negative results leave traces | Mark contaminated benchmark-log rows with invalidation warnings (what/why/correct caliber); exclusion records keep later readers from re-walking dead ends or citing bad numbers |
| 10 | Comparison environment-state validity | Interleaved A/B assumes both arms see the same environment — after code switching, hot-reload state (mixed old/new modules, duplicated singletons, stale registrations) systematically pollutes one arm; changes touching structural units (modules/singleton topology) require an environment reset (restart / hard refresh) between arms before the judge's verdict counts |

**Gate rule**: for any metric, if the discipline covering its trap class is unresolved, the metric is **not decision-grade** — it may appear as trend-only context but must not drive optimization choices, priorities, or pass/fail verdicts.

---

## Stage 1: Benchmark & Evidence (性能证据)

### Goal

Turn a vague "it's laggy" into a **reproducible, standardized, logged workload** with a quantified baseline and a target/red-line — not a one-off manual repro. If a benchmark harness already exists, run it; if not, building a minimal one is part of this stage, because every later stage depends on repeatable numbers.

### Information to clarify

- **Symptom**: which action (click/scroll/type/open/IME…), what "slow" looks like (jank/blank/spinner/unresponsive), **quantified** where possible; pin the analysis boundary (start and end of the problem).
- **Data available**: existing logs/profiles/instrumentation? If none, determine in what environment, with what method, data can be captured.
- **Reproduction**: always vs intermittent; requirements on data volume / device class / duration.

### Benchmark harness contract (when building one)

- **Standardized workloads, planned from a scenario inventory**: first build or read the project's **user-scenario inventory** (the full set of real usage scenarios and their coverage state — file it next to the harness, e.g. `SCENARIOS.md`), then plan scripted loads to close its gaps (open × scale, input × chars, scroll × rounds, switch, session-long editing, IME, paste, …). Each load is driven through **real input paths** (discipline 5) and verifiable by content delta.
- **Long-session degradation is its own problem class**: short sessions expose single-operation cost; continuous editing / note-switching / history growth expose accumulated degradation (memory creep, latency-trend rise, undo-history bloat). Cover it with dedicated loads (session / switch / history class) and analyze by **trend slope and inflection point**, not single-run numbers.
- **Probe-script pattern**: every recurring attribution question is sedimented as a reusable probe script under the harness (naming convention `probe-*` — profiler sampling, phase-split timing, counter audits, throttle-matrix drivers, …). Pipeline steps in the project's `code-insight` invoke probes instead of ad-hoc scripting; the first campaign seeds the initial probe set, later campaigns extend it.
- **Automated capture**: metric collection wired once, reused every run — not manual copy-paste. Console/log parsing and structured JSON archives preferred.
- **Baseline first**: record the pre-optimization baseline before any change; every later claim is a comparison against it.
- **Benchmark log**: an append-only file (e.g. `BENCHMARK.md`) at repo root recording every run: date, commit, workload, scale, key metrics, note. This log is the campaign's memory — verdicts, retractions, and invalidations all land here (Stage 6).
- **A/B judge**: build or reuse a cross-run statistical judge (see Stage 6) so "did it improve" is never answered by eyeballing two numbers.

### Evidence gate (before any number leaves this stage)

Clear the in-file disciplines **1 (throttling artifacts), 2 (monitor self-pollution), 5 (input authenticity), 6 (toggle lifecycle)** for every metric you plan to carry forward. Numbers failing the gate are marked trend-only.

### Output

- What data is available / missing; if missing, the exact capture action (who runs what, what gets captured).
- Recommended output: a structured problem definition — symptom (quantified), reproduction conditions, analysis boundary, baseline, target threshold/red line.
- Benchmark harness status: existing / built-this-stage / deferred-with-reason.

---

## Stage 2: Locate the Bottleneck (性能定位)

### Goal

Find the anomalies in the data (who spent how much time/resources, when), trace the full trigger chain, and narrow to 1-2 core segments — with every load-bearing number already evidence-gated.

### Project attribution skill (`code-insight`)

The stack/project-specific attribution pipeline lives as a **project-level skill**, created and continuously improved by this workflow — the paradigm file stays generic.

- **Probe at stage entry**: look for the project's `code-insight` skill (in the project's conventional agent-skill directory). Found → run its pipeline for this stage's localization work, and note any gap it fails to cover (that gap is this campaign's improvement candidate). Not found (first campaign) → **seed it as a step-by-step pipeline**: attribution-pipeline template from [reference.md](reference.md) Part 5 (JS stack today), adapted with this run's project discoveries (tool paths, workload specifics, known pitfalls, initial `probe-*` scripts under the harness); Parts 1-2 serve as knowledge attachments per pipeline step; run the specialist-perspective pass over the seeded content before landing. Manual mode confirms the seed location; auto mode uses the project's convention.
- The seeded skill is a standing project asset: later sessions and other agents on the project can invoke it directly, independent of this workflow.

### Analysis approach

1. **Full-chain topology**: segment the path from user action to problem end (code execution, system calls, network/storage), no gaps, no overlap; each segment independently timeable.
2. **Two-dimensional capture**: time (per-segment duration/share) + resources (CPU/memory/IO/network). Neither skipped. Resource utilization >70% is a common alert line — beyond it, response time rises non-linearly.
3. **Initial screen**: rank segments by time-share (e.g. >20% = high-cost); flag resource anomalies (saturation, sustained growth, error rate); rule out low-cost + resource-normal segments.

### Attribution techniques (pick by what the data shows)

- **Text logs**: filter by keyword/duration/error code, read snippets + stacks.
- **Profiles**: read the wide bars / high-share regions first, drill to function/component. **Editor/web-app four-bucket split** when Rendering dominates: framework commit / style insertion / layout / paint — their fixes differ entirely; do not read "Rendering" as one blob.
- **Forced-reflow reading** (write→read patterns; rich-text editors: DOM mutation followed immediately by selection-boundary reads is the classic #1 source).
- **No JS hotspot** (`(program)`/`(idle)` dominant)? → discipline 8's static-copy control experiment decides: product-code cost vs DOM-scale physical cost. This single experiment can end a multi-year argument.
- **Known-pattern quick search**: when `known-issue-research`'s triggers fire, load it and run its performance-pattern variant before deeper custom analysis.

### Evidence gate

Disciplines **3 (counter audits — audit any framework-internal statistic before use)** and **8 (control experiment)** apply here.

### Output

- Anomaly summary (slow/high-volume/high-frequency + location); causal chain "action → … → bottleneck" in a sentence or diagram.
- 1-3 preliminary hypotheses with confirming/refuting evidence stated; core bottleneck segment list (1-2) with shares.

---

## Stage 3: Hypothesize the Root Cause (性能假设)

### Goal

Distill anomalies into **verifiable, falsifiable** root-cause hypotheses, classified against common patterns; ranked by user impact × verification cost.

### Reasoning references

- **USE method** (resource bottlenecks): utilization / saturation / errors.
- **RED method** (execution/request bottlenecks): rate / errors / duration.
- **Common patterns table** (response-scope-too-broad, unbatched updates, high-frequency triggers, backlog-fires-at-once, resource leak, synchronous blocking, redundant computation): generic forms in this file's paradigm; concrete frontend manifestations in [reference.md](reference.md).

### Evidence gate

Discipline **7 (single-sample extrapolation ban — "users don't hit this" needs user-profile evidence)** and discipline **4 (throttle matrix — hypotheses about user-perceived jank are validated on calibrated cells)** apply here.

### Output

- The 1-2 most likely hypotheses, each resolvable to yes/no ("is it a full re-render?" is answerable; "the code is badly written" is not); ranked; with verification method (existing data, or which monitoring points from Stage 4).

---

## Stage 4: Build Toggleable Monitoring (性能监控)

### Goal

When existing data cannot verify the hypothesis, add **toggleable, production-grade observability** on the critical path — permanent code, gated at runtime.

### Design principles

1. **Toggle-controlled** (env var / config / feature flag / debug switch): off in production = zero output, zero sampling, negligible overhead; on = structured output aligned with existing logs.
2. **Permanent, not temporary**: a standing capability, not instrumentation to rip out later.
3. **Alignable**: stable timestamps + location identifiers, joinable with existing logs/profiles on one timeline.
4. **Just enough**: location + timestamp + the few key variables that confirm/refute the hypothesis; reuse the project's log format.
5. **Toggle lifecycle**: toggles read at module load must be injected before page scripts (discipline 6).

### Point selection

Direct trigger point first (the state update / request fire / recompute entry), then intermediate chain nodes (call order/frequency), then the expensive computation's entry/exit (per-call duration/count).

### Output

Monitoring-point list (file:line or function, purpose, toggle name) + the user action to enable/reproduce/capture. Root cause already confirmable → skip to Stage 5.

---

## Stage 5: Optimize (性能优化)

> This stage and Stage 6 execute as the iteration loop (see "Iteration loop"); the environment gate is probed at this stage's entry.

### Goal

Implement the change that eliminates/mitigates the confirmed bottleneck — **one root-cause target per iteration**, sized by impact.

### Project optimization skill (`code-optimizer`)

Same lifecycle as `code-insight`: probe the project's `code-optimizer` skill at stage entry; found → follow its optimization pipeline for this target and note gaps; not found → **seed it as a step-by-step pipeline** from the Part 5 template (JS stack) plus this run's discoveries. The seed MUST include a **deep-attribution step that delegates to the project's `code-insight`** (the two are cooperating pipelines, not isolated tools). It accumulates this project's validated optimization patterns and rejected attempts, so every campaign starts smarter.

### Principles

- **Fix the root cause, not the symptom**: the change maps to the Stage 3 pattern (narrow the scope, batch, throttle, cache, move off-thread…), not a generic "make it faster".
- **Technology-selection decisions escalate to the user**: introducing a new dependency, replacing a data structure, or changing an allocation/memory strategy → present the candidate options with trade-offs (performance / portability / maintenance) and let the user pick — the agent does not decide unilaterally.
- **One target per iteration**: every commit optimizes exactly one thing, keeps the change reviewable and revertible, and makes Stage 6's benefit attribution unambiguous. Multiple good ideas queue as separate iterations.
- **Layer priority** (high → low): business logic → application code → framework/dependency → system/hardware; prefer upper layers and "low change cost, high payoff" moves.
- **Time-share priority**: optimize the highest-share segments first; a <10% segment improved 100x barely moves the total (Amdahl).
- **Stability**: no semantic change, no functional bugs, no new performance side effects.
- **No gain → revert**: Stage 6 rejects the change → revert it (the benchmark log keeps the negative row), do not stack a second speculative change on top.

### Output

Change list (file, location, summary) + suggested verification scenario/metrics aligned with Stage 4 monitoring, for Stage 6.

---

## Stage 6: A/B Verify (性能验证)

> This stage normally runs inside the iteration loop (see "Iteration loop"); a single pass is only the explicit user-requested exception.

### Goal

1. Render a yes/no verdict on the hypothesis.
2. If Stage 5 changed code: prove the optimization worked **statistically**, at production caliber, without side effects — or revert.

### Evidence gate

Disciplines **2 (production-caliber acceptance)**, **4 (user-jank verdicts from throttle-matrix cells)**, **9 (rejections and invalidations logged)**, and **10 (environment reset between arms when structural units changed)** apply to every verdict this stage produces — including single-pass runs.

### A/B cross-run statistical judge

- Keep the previous commit's build as Baseline (snapshot keyed by commit hash).
- Alternate runs **B₁ A₁ B₂ A₂ B₃ A₃** (Baseline, New, interleaved) so system-load noise hits both sides roughly equally.
- Accept an improvement **only if `avg_B − avg_A > max(stdev_B, stdev_A)`** (the acceptance rule; referenced elsewhere, stated only here). Single runs and minimum-of-N are not verdicts (min-of-N chases idle moments; single runs chase noise).
- Before judging, honor discipline 10: structural changes ⇒ reset the environment between arms.
- Intentional divergence from the source paradigm (recorded): the source accepts "certainly correct" micro-optimizations even within noise; this workflow keeps the hard statistical gate for agent execution — agents systematically overestimate "certainly correct". Restoring the exception would require static equivalence proof plus user confirmation.
- Why it works: alternating runs experience the same machine states, so the difference is far more stable than absolute numbers — no machine lockdown, core pinning, or service-killing required.

### Verification checklist

- **Hypothesis verdict**: confirmed / refuted / uncertain (+ what's missing, next monitoring or re-analysis).
- **Effectiveness**: same repro path, before/after key metrics, pass criteria stated up front.
- **Regression**: functional correctness (normal/edge/peak) intact — for optimization of transformation pipelines, output-equivalence checks (e.g. byte-identical) are the strongest form.
- **Side effects**: no secondary performance issues (e.g. latency fixed but memory climbing).
- **Caliber**: acceptance numbers from production-caliber builds (discipline 2); user-jank verdicts from device-profile-calibrated cells (discipline 4).
- **Sediment**: append the run to the benchmark log — including **rejections** (discipline 9: no-gain and artifact rows are recorded with reason, keeping others from re-walking dead ends or citing bad numbers).

### Stop condition

Every hypothesis verified, targets met — or remaining bottlenecks' cost-effectiveness too low (change cost ≫ payoff). This is the campaign-level stop; the loop section's stop conditions govern round-level termination. Then optionally fold key metrics into standing monitoring/CI gates.

---

## Iteration loop (environment-gated, mandatory for Stages 5-6)

Optimize (Stage 5) and A/B verify (Stage 6) execute as a repeating loop **mounted on a real environment loop runner** — never as one-off passes, and never as a self-invented prose loop. The compounding gains come from sustained rounds; a manual one-pass run stops at the first visible hotspot and silently loses the paradigm's core value.

### Environment gate (at Stage 5 entry)

Probe the environment for a loop capability — an installed loop runner (ralph-loop-style runner, `/loop`, goal-driven long-run, or any mechanism that auto-continues the agent across rounds with per-round context management):

- **Found** → mount the loop body below on it and enter the loop. The runner drives round cadence and continuation; this workflow supplies what each round contains and when to stop.
- **Not found** → **stop optimization execution**. Report the analysis stages' findings (they remain valid and deliverable), and state the exact blocker: install a loop runner, then re-enter at Stage 5. Do not degrade to a single manual pass — an honest abort beats a fake loop.

This gate is a runtime strong dependency on the environment (not a frontmatter dependency — loop runners are environment plugins, not installable skills).

### Loop body (each round, in order)

1. **Profile** — re-acquire hotspots fresh this round; last round's list is stale input.
2. **Pick exactly one target** — top hotspot by user impact × time-share; queue the rest.
3. **Optimize that target** — per the Optimize stage (root-cause-mapped, revertible).
4. **A/B judge** — Stage 6's acceptance rule decides accept/revert; honor discipline 10 before judging (environment reset between arms when structural units changed); rejected → revert this round.
5. **Correctness gate** — full test suite / output-equivalence before commit; never commit red.
6. **Commit + snapshot + log** — one commit per round; snapshot the accepted build as next round's baseline (keyed by commit hash); append the round to the benchmark log, accepted or rejected, with reason.

### Stop conditions (any one)

- **5 consecutive no-gain rounds** — the optimization set has converged.
- **Target met** — stage-1 threshold/red line reached and verified.
- **ROI exhausted** — remaining bottlenecks' gain no longer justifies change cost.

On stop: summarize rounds accepted/rejected, total measured gain vs baseline, remaining bottlenecks with ROI assessment.

### Context discipline (long loops die of context bloat)

Each round persists its outcome to the benchmark log and carries forward only: the round summary, the baseline-snapshot pointer, and the stop-condition counters. Raw profiles and intermediate data stay in the archive files — they are retrieved on demand, never carried in full across rounds.

### Skill evolution (at every stop; or every ~5 rounds in long loops)

Skills are code too — the project's `code-insight` / `code-optimizer` are themselves artifacts of the paradigm, improved by use. At each stop condition:

- Fold this campaign's **validated lessons** into the two skills: attribution patterns that worked, optimizations that failed (with the rejection data), stack/project-specific pitfalls discovered.
- The benchmark log's invalidation rows and negative results are the primary feed — they encode exactly what the skills got wrong or missed.
- **Review the update from the stack's specialist perspectives** (e.g. language semantics / runtime & framework / hardware & platform) before landing: lessons gathered mid-campaign can contradict each other or the skill's existing content — correct the inconsistencies, then write.
- Update the skills in place; the next campaign starts smarter. This is where the paradigm compounds **across** campaigns, not just within one.

## Output detail level (adaptive)

- Simple problem, ample data: condense to "anomaly + causal chain + verdict".
- Complex/multi-module: brief per-stage outputs, key snippets attached.
- Stack-specific knowledge (framework versions, thresholds, patterns, tool tables): fold in from [reference.md](reference.md) conversationally — never hardcode stack specifics into this file's paradigm.
