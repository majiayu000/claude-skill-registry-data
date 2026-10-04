---
name: quality-performance
description: Audit AICP's runtime performance — inference latency (cold-start vs warm), router decision time, profile-switch cost, MCP tool latency, memory + VRAM footprint per profile. Captures benchmarks per AICP-specific dimensions (model swap, GPU eviction, circuit breaker fail-fast). Loads when the operator says "benchmark", "performance audit", "latency check", "is X fast enough", "profile X under load".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# quality-performance

Audits AICP's runtime performance across the dimensions that actually matter
for a multi-model orchestration platform: cold-start vs warm inference,
router decision time, profile-switch cost, MCP tool latency, and memory +
VRAM footprint per profile. Different from `quality-coverage` (test
coverage) and `quality-lint` (style) — this is about operational behavior
under load, not artifact quality.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "benchmark", "performance audit", "latency check", "is X fast enough", "profile X under load", "measure cold-start"
- **Pre-release gate**: before shipping a milestone, confirm performance hasn't regressed
- **Post-Stage milestone**: Stage 3 hardware unlock (19GB VRAM) — re-benchmark to validate dual-gpu profile actually delivers expected throughput
- **Post-incident**: a latency spike was reported in production; audit surfaces what changed
- **Capacity planning**: operator asks "can AICP handle N requests per minute on profile P?"
- **Regression check**: after a non-trivial code change, sanity-check that hot paths didn't slow down

Do NOT load when:

- The concern is correctness (load `feature-test` or `systematic-debugging`)
- The concern is test coverage (load `quality-coverage`)
- The concern is build speed / dev velocity (different concern — that's about pipeline, not runtime)
- The "performance" in question is human productivity (different concern entirely)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Run the benchmark suite

**Trigger**: skill loaded; operator wants a perf audit.

**Process**:

1. Verify benchmark infrastructure exists: `ls tests/benchmark/ 2>/dev/null` AND `make benchmark-qwen3 2>/dev/null | head -3`. If neither exists, stop and load `foundation-testing` to add benchmark infrastructure first — you can't audit what doesn't measure.
2. Run the existing benchmarks. AICP has at least `make benchmark-qwen3`. Capture output to `/tmp/perf-audit-<date>.log`. Run all benchmark targets in `Makefile` matching `^benchmark-`.
3. Capture per-profile metrics. For each of the 9 profiles, run a representative request:

   ```bash
   for profile in default fast offline thorough code-review fleet-light reliable dual-gpu benchmark; do
     time aicp --profile "$profile" "What is 2+2? One word." -m think -b local 2>&1 | tail -3
   done
   ```

   Capture: cold-start time (first request after `make profile-use`), warm time (subsequent requests), p50/p95 if multiple samples.

4. Capture system footprint per active profile:
   - VRAM: `nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits`
   - RAM: `docker stats --no-stream --format '{{.Name}}: {{.MemUsage}}'`
   - LocalAI active backends: `curl -s localhost:8090/v1/models | python3 -m json.tool | head -20`

5. Write the baseline snapshot to `wiki/decisions/00_inbox/perf-audit-<date>.md` (type=reference). Include: per-profile cold/warm times, VRAM + RAM footprint, active backend counts.

**Quality bar (Operation 1 done when)**:

- [ ] Benchmark infrastructure verified (or `foundation-testing` loaded)
- [ ] Existing `make benchmark-*` targets all run; output captured
- [ ] Per-profile cold + warm times captured for ≥3 profiles (default + fast + dual-gpu at minimum)
- [ ] VRAM + RAM + backend count captured per active profile
- [ ] Baseline snapshot written

### Operation 2: Compare to thresholds + prior runs

**Trigger**: Operation 1 baseline captured.

**Process**:

1. Define expected thresholds per AICP's documented profile semantics (see `config/profiles/`):
   - `fast` profile: cold ≤30s, warm ≤2s (matches "53 tok/s" claim in CLAUDE.md)
   - `default` profile: cold ≤60s, warm ≤2s
   - `thorough` profile: cold ≤90s, warm ≤5s
   - `dual-gpu` profile: cold ≤80s (loading 30B MoE), warm ≤3s
   - `fleet-light` profile: cold ≤30s (small model), warm ≤1.5s
   - `benchmark` profile: deterministic — same time across runs (variance <5%)
2. For each profile, classify: PASS / DEGRADED / FAIL relative to threshold. DEGRADED = within 50% over threshold; FAIL = >50% over OR didn't complete.
3. Compare against prior `perf-audit-*.md` (if any). Trend: improving / stable / regressing.
4. Identify the SLOWEST hot path. AICP-specific candidates:
   - Cold-start (model swap): Bound by GGUF load + GPU upload (10-80s expected per CLAUDE.md)
   - Router decision: Should be <50ms (pure logic, no LLM call)
   - Circuit breaker check: Should be <5ms (in-memory state)
   - MCP tool dispatch: Should be <10ms overhead before reaching the actual handler
   - Profile switch: Bounded by Docker compose restart (10-30s)
5. For any FAIL classification, pick ONE root cause hypothesis (don't speculate broadly): e.g., "fast profile cold-start FAIL because gemma4-e2b cold takes 35s on this hardware vs 30s threshold — likely warmup config not enabled."

**Quality bar (Operation 2 done when)**:

- [ ] Each measured profile has PASS/DEGRADED/FAIL classification
- [ ] Trend vs prior audit captured (or "baseline established")
- [ ] Slowest hot path explicitly named
- [ ] FAIL classifications have ONE root cause hypothesis (not speculation)

### Operation 3: Investigate hot paths (don't fix yet)

**Trigger**: Operation 2 classification complete; operator approved which hot paths to investigate.

**Process**:

1. For each chosen hot path, measure WHERE the time goes:
   - **Cold-start**: time the GGUF load (`time docker logs ...localai... | grep "model loaded"`), time the GPU upload (compare nvidia-smi VRAM before/after), time the first inference
   - **Router decision**: add temporary timing logs in `aicp/core/router.py` (gated by env var, NOT committed); run requests; remove
   - **Profile switch**: time each `make profile-use` step (`.env` write + Docker restart + warmup)
2. Profile with `cProfile` for any pure-Python hot path:

   ```bash
   python3 -m cProfile -o /tmp/profile.out -m aicp.cli --route "test"
   python3 -c "import pstats; pstats.Stats('/tmp/profile.out').sort_stats('cumulative').print_stats(20)"
   ```

3. For LocalAI-specific bottlenecks, query LocalAI's metrics: `curl -s localhost:8090/metrics | grep -E "load|inference|swap"`. Capture relevant counters.
4. Document findings in the audit page under `## Hot path investigation`. For each hot path: where the time goes (with measurements), candidate optimizations, estimated improvement IF optimized.
5. **DO NOT optimize in this skill**. This skill measures + investigates; the actual optimization is a separate task (refactor or feature) authored from the audit findings.

**Quality bar (Operation 3 done when)**:

- [ ] Each chosen hot path has measurement-backed time breakdown
- [ ] cProfile output for pure-Python paths
- [ ] LocalAI metrics captured for inference-related paths
- [ ] Audit page has "Hot path investigation" section with findings
- [ ] No optimization changes committed (out of scope)

### Operation 4: Author follow-up tasks + update audit page

**Trigger**: Operation 3 investigation complete.

**Process**:

1. For each FAIL or DEGRADED hot path, create a backlog task at `wiki/backlog/tasks/T<n>-perf-<slug>.md`:
   - Reference to the perf audit page
   - Specific measurement (X seconds vs Y threshold)
   - Candidate optimization approach (from Operation 3 findings)
   - Estimated effort + estimated improvement
2. For HIGH-impact patterns (e.g., "all cold-starts are slow because warmup is disabled in 5 of 9 profiles"), consider authoring a Decision page rather than a task — the fix is a config decision, not point work.
3. Update the audit page with task IDs created, deferrals (with reasoning), and recommended next-audit cadence (more frequent if regressing, less if stable).
4. If a SYSTEMIC pattern emerged (e.g., "router decision time grows linearly with profile complexity — needs caching"), contribute back as a lesson: `gateway contribute --type lesson`.
5. Run `tools/lint.py wiki/decisions/00_inbox/perf-audit-<date>.md`.

**Quality bar (Operation 4 done when)**:

- [ ] Follow-up tasks created for FAIL items (and DEGRADED items the operator chose to address)
- [ ] Decision page authored for config-only fixes
- [ ] Deferrals documented with reasoning
- [ ] Lesson contributed if systemic
- [ ] Audit page lint passes

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Benchmarking on a busy machine (false signal)

The temptation: run benchmarks while other work is happening on the machine. Numbers come back highly variable. You report "cold-start is 45s" without noting the system was under heavy CPU load from a parallel build.

**Detection**: did Operation 1 verify the machine is quiet (no parallel `pytest`, no Docker rebuilds, no large file copies)? Run `top` and `docker stats` BEFORE starting benchmarks; ensure baseline load is low.

**The rule**: every benchmark run notes the system state (load avg, free memory, parallel containers). If conditions weren't quiet, the numbers go in the audit page WITH that caveat — don't treat noisy numbers as clean.

### Gotcha 2: Optimizing in the audit (scope creep)

The temptation: while measuring, you spot an obvious optimization. Tempting to fix it inline. NO — Operation 3 explicitly says "DO NOT optimize in this skill." Optimizations need their own task with their own design + test + review.

**Detection**: did the audit commit include any code changes outside `wiki/decisions/00_inbox/perf-audit-<date>.md` and `tests/benchmark/`?

**The rule**: audits write audit pages and benchmark fixtures. Optimizations live in their own tasks. Mixing them makes the audit's measurements not-replicable (you changed the thing you measured).

### Gotcha 3: Single-sample benchmarks (high variance hidden)

Running each profile ONCE. Cold-start of 45s reported. But cold-start was actually 30-60s with high variance — the single sample landed at 45s by chance. Future audits show 50s and you "regress."

**Detection**: did each measurement have ≥3 samples with min/max/p50 reported?

**The rule**: per-profile measurements are ≥3 samples. Report p50 + p95 + variance. Single samples are OK only for slow operations (cold start, profile switch — too costly to repeat) AND must be marked as such in the audit page.

### Gotcha 4: Comparing apples to oranges across audits

This audit measures `default` profile cold-start as 45s. Prior audit measured `default` profile cold-start as 30s. Trend: regressing. But the prior audit was on different hardware (8GB single-GPU, today is 19GB dual-GPU) — the numbers aren't comparable.

**Detection**: did Operation 2 trend comparison verify the prior audit's hardware + profile config matches the current?

**The rule**: trend comparisons require the same hardware + same profile + same model + same prompt. If conditions changed (hardware upgrade, profile change), the comparison is "baseline reset" — note it explicitly, don't fake a trend.

### Gotcha 5: Reporting tokens-per-second without input/output token counts

The temptation: report "qwen3-8b: 30 tok/s." Tok/s without context is meaningless — was that for a 100-token prompt or a 10000-token prompt? Was that prefill (input processing) or decode (output generation)?

**Detection**: did the audit report tok/s WITHOUT specifying prompt length, output length, prefill vs decode?

**The rule**: every tok/s figure is qualified: "qwen3-8b: prefill 200 tok/s, decode 30 tok/s, on a 500-token prompt → 100-token response." Without qualification, don't report the number.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Perf audit page**: same shape as sibling quality audit pages (coverage / lint / debt). Use the `reference` template.
- **Real benchmarking infrastructure**: see `Makefile` `benchmark-qwen3` target + `tests/benchmark/` directory in AICP for the existing pattern.
- **LocalAI's own metrics**: `curl localhost:8090/metrics` returns Prometheus-format metrics including model load times, inference latencies, queue depths. AICP's [config/alerts.yaml](../../../config/alerts.yaml) (7 rules) demonstrates which metrics are operationally important.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP-specific perf considerations: single-active-backend means model swap cost dominates cold-start; dual-gpu profile changes the math (asymmetric KV cache, can run larger models); circuit breaker means failover happens in ms, not s.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| quality-coverage | test coverage gaps | Different quality axis (correctness vs speed) |
| quality-lint | code style violations | Different quality axis (hygiene vs speed) |
| quality-audit | umbrella across all dimensions | Includes this skill as a sub-audit |
| feature-test | per-feature testing including basic perf | Per-feature scope; this skill is suite-wide perf |
| ops-incident | live perf incident response | Reactive; this skill is proactive |
| refactor-architecture | structural changes that improve perf | Acts on findings from this skill |
