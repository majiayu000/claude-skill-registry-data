---
name: runtime-evidence-debug
version: "1.1.0"
user-invocable: true
description: "Default entry of the debug skill family when runtime observation is needed: static analysis stalled, a fix did not work, logs look correct but behavior is wrong, or fix verification needs before/after evidence. Covers escalation decision, targeted instrumentation (not shotgun logging), MRE reproduction, evidence tiers, confidence gating, escape hatches, and fix verification; composes with browser-debug-toolkit / hybrid-debug / channel enablers without demoting them. Triggers — 「打点调试」「打日志调试」「运行时调试」「运行时验证」「复现验证」「日志分析根因」「根因置信度不足」「静态分析碰壁」「修了还是不行」「日志正常但行为不对」「偶现」「调试默认入口」 / runtime evidence debugging, instrumentation debugging, escalate to runtime, evidence-driven debugging, fix didn't work, intermittent bug."
---

# Runtime Evidence-Driven Debugging

> **Role**: The methodology layer for runtime debugging — answers *when* to escalate from static analysis to runtime observation, and *how* to gather, analyze, and act on runtime evidence. **Referenced by** PDCA hosts via frontmatter `dependencies` (invoked after a prerequisite check). It delegates tool selection to `browser-debug-toolkit` and domain analysis to `hybrid-debug`.
>
> **Detailed framework entries** (author, year, method, source) and instrumentation templates live in [reference.md](reference.md).

## Why this skill exists

Static code analysis — reading code, tracing call chains, reasoning about logic — has a ceiling. It cannot observe:

- **Runtime data flow**: what value a variable actually holds at execution time
- **Call ordering**: which function runs first when timing matters
- **Platform/host interception**: silent behavior changes imposed by WebView, Electron, OS-level controls, or framework runtime — invisible in source code

When root-cause confidence is "fuzzy" or "unknown" after static analysis, the disciplined response is not to re-read the same code harder. It is to **escalate to runtime evidence gathering** — add targeted instrumentation, reproduce the problem, observe the actual execution, and anchor the root cause in observed fact rather than inferred logic.

This skill provides that methodology. The meta-lesson:

> **A root cause confirmed by runtime observation is an order of magnitude more trustworthy than one inferred from reading code. When confidence is low, do not reason harder — gather evidence.**

## When to use

Strong signals (any one):

- **Root-cause confidence is low** after static analysis — you can locate the likely module but cannot confirm the exact logic or trigger path.
- **Retry scenario** — a fix based on static analysis was applied, but the problem persists. Static analysis already hit its ceiling once; the next step must use runtime data.
- **Silent failure** — the call chain looks complete, parameters look correct, logs show execution — but the runtime behavior is wrong. This points to platform/host interception that only runtime observation can reveal.
- **You need to add logging/instrumentation** (`console.log`, `print`, debugger breakpoints) to observe what actually happens at runtime.
- **Fix verification** — you need to confirm a fix works by comparing behavior before and after, not just by reasoning about the code.

## Relationship to other skills

| Skill | Responsibility | Relationship to this skill |
|-------|---------------|----------------------------|
| PDCA hosts | Host workflows | **Referenced by** PDCA hosts via frontmatter `dependencies` (missing → host aborts). Runtime-evidence deep-dive of their technical-analysis instrumentation step. Hosts are SoT for that edge. |
| `browser-debug-toolkit` | Browser DevTools tool-selection decision table | This skill's **instrumentation** step delegates to it for browser-reproducible issues (UI/CSS/DOM as typical scenes) — DevTools live inspection is more efficient than `console.log` for runtime observation. |
| `hybrid-debug` | Hybrid app four-layer debugging model | This skill is the **general** runtime evidence methodology; `hybrid-debug` applies it within the four-layer model for native+web apps. For hybrid problems, use `hybrid-debug` first (it tells you where to look); this skill tells you how to gather evidence at whichever layer. |
| `debug-workflow` (if available) | Systematic debugging protocol (root-cause identification) | Complementary — `debug-workflow` drives the overall debugging process; this skill is the runtime-evidence-gathering phase within it. |
| `essence-diagnosis` | Evidence-chain construction and adversarial debate | For problems where runtime evidence is still insufficient, escalate to `essence-diagnosis` for multi-hypothesis evidence-chain verification. |

## The evidence-gathering lifecycle

Seven phases, from deciding to escalate through verifying the fix. Not every problem requires all seven — but skipping phases produces low-confidence conclusions.

### Phase 1 — Escalation decision (when to go from static to runtime)

**Framework**: Scientific debugging — Andreas Zeller, *Why Programs Fail* (2009, 2nd ed. 2022).

Before adding any logging, confirm that static analysis has genuinely hit its ceiling. The test: after tracing the call chain and reading the relevant code, can you state the root cause with **high confidence**? If yes, you do not need runtime evidence yet. If confidence is "fuzzy" or "unknown" — you can name the suspect module but not the exact mechanism — it is time to escalate.

The scientific method applies: form a **hypothesis** (the root cause is X), design an **experiment** (add instrumentation at point Y to observe Z), **observe** the result, and **conclude** (confirm or falsify X). Each round of instrumentation is a controlled experiment, not a fishing expedition.

### Phase 2 — Instrumentation design (targeted logging)

**Frameworks**: Observability triad (Charity Majors, *Observability Engineering*, 2022; Cindy Sridharan, *Distributed Systems Observability*, 2018); structured logging best practices (OpenTelemetry semantic conventions).

Design 2–5 instrumentation points — not a scatter-shot of `console.log` everywhere. Each point should target a specific hypothesis:

- **Function entry/exit**: confirm whether a function is reached, and with what arguments
- **State change points**: observe when and how a variable transitions to the wrong value
- **Data flow junctions**: trace data as it crosses module/service boundaries

**Good instrumentation** captures: position identifier (`[DEBUG-<location>]`), key variables (not all variables — the ones your hypothesis concerns), and a timestamp. Format: `console.log('[DEBUG-auth-check]', { userId, hasToken: !!token, timestamp: Date.now() })`.

**Anti-pattern**: adding logging everywhere "just in case." This produces noise that obscures the signal. Every logging point must map to a hypothesis.

> For browser-reproducible problems (UI/CSS/DOM as typical scenes), delegate to `browser-debug-toolkit` — DevTools live inspection (DOM, computed styles, box model, console, network) is more efficient than `console.log`.

### Phase 3 — Reproduction guidance

**Frameworks**: Minimum Reproducible Example (MRE/MCVE, Stack Overflow methodology; Benjamin C. Haller, *Ten Simple Rules for Reporting a Bug*, PLOS Computational Biology, 2022); deterministic reproduction (Google Testing Blog — flaky test mitigation, Micco 2016).

To produce useful runtime evidence, the problem must be **reproducible**. Guide the user through:

1. **Reproduction steps**: the exact sequence that triggers the problem (not "sometimes it happens" — the specific path)
2. **Environment**: browser version, OS, device, network conditions — anything that affects runtime behavior
3. **Minimum reproduction**: strip away everything unrelated until the smallest reproducing case remains. A smaller reproduction produces cleaner logs and faster iteration.

If the problem is **non-deterministic** (intermittent, timing-dependent), document the frequency and triggering conditions. Non-deterministic bugs (Heisenbugs — see reference.md) require special handling: the instrumentation itself may change timing and mask the bug.

**Tool constraint**: the AI designs instrumentation and provides reproduction guidance, but the **user** adds the logging and runs the reproduction (unless the user explicitly authorizes the AI to do so). Do not run reproduction steps without user confirmation.

### Phase 4 — Evidence analysis

**Framework**: Evidence hierarchy in debugging.

When the user provides the runtime output, analyze it with an evidence hierarchy in mind:

| Evidence tier | Strength | Example |
|---------------|----------|---------|
| **Tier 1 — Runtime observation** | Strongest | Debugger breakpoint showing variable value; DevTools computed style; profiler hotspot |
| **Tier 2 — Log output** | Strong | `console.log` output confirming function was called with specific arguments |
| **Tier 3 — Code inference** | Moderate | Reading the code and inferring "this branch should execute because..." |
| **Tier 4 — Assumption/guess** | Weak | "I think it's probably the cache because..." |

Root causes anchored in Tier 1–2 evidence are trustworthy. Root causes resting on Tier 3–4 need further instrumentation to upgrade. Do not declare a root cause "confirmed" if the strongest evidence is Tier 3 (code inference) — that is still static analysis wearing a runtime hat.

### Common misdiagnosis traps (avoid first-hypothesis fixation)

Code reading tends to produce one plausible hypothesis and stop. But most symptom categories have many indistinguishable causes in source. Before committing to an instrumentation plan, scan these alternatives:

| Symptom | Hypothesis you likely jumped to | Alternatives code reading misses |
|---------|-------------------------------|--------------------------------|
| **Memory leak** (RSS growing) | Event listener not cleaned up | Closures capturing large scopes; unbounded cache/Map; uncleared timers; stream buffers; native addon leaks (Buffer/C++); V8 GC lag (not a leak at all); connection pool retention |
| **Intermittent crash / 500** | Race condition | Pool exhaustion under burst; DB timeout; network blip; OOM kill; upstream service hiccup; connection leak (different from listener leak) |
| **Stale UI render** | Wrong useEffect deps | Async race (old promise resolves last); stale closure in useCallback; React.memo holding stale props; concurrent rendering batching difference; StrictMode masking in dev |
| **Silent failure (no error, wrong behavior)** | Logic bug in our code | Platform/host interception (WebView quirk, Electron IPC); type coercion at boundary; serialization data loss (JSON.stringify dropping undefined/functions); env variable not loaded |
| **Performance regression** | Algorithm complexity | Memory pressure causing GC thrash; hidden N+1 query; bundle size bloat; lock contention; cache invalidation storm |

The rule: if your instrumentation only tests one hypothesis and it confirms, you still have not ruled out the alternatives causes. Design instrumentation that **falsifies** the top 2–3 candidates, not just confirms the first one.

### Phase 5 — Confidence gating

**Framework**: Bayesian reasoning applied to debugging (prior confidence + new evidence → posterior confidence).

After analyzing runtime evidence, calibrate your confidence:

- **High**: runtime evidence directly confirms the mechanism (e.g., log shows the variable is `null` when it should be an object; debugger shows the wrong branch executing). → Safe to proceed to fix.
- **Medium**: runtime evidence narrows the scope but does not uniquely confirm one mechanism. → One more targeted instrumentation round, or proceed with a stated uncertainty.
- **Low/Fuzzy**: runtime evidence did not clarify the mechanism — the logs show expected behavior but the problem persists. → Do NOT proceed to fix. Escalate to the escape hatch (Phase 6).

**The most expensive debugging mistake**: entering execution (writing a fix) on low confidence. The first attempt becomes a discarded surface patch. When confidence is low, the disciplined response is to keep gathering evidence, not to guess and hope.

#### Fix Readiness Gate — 3 conditions that must ALL be true before writing any fix

Before you propose or apply a code change, verify all three. If any one is missing, you are not ready to fix — go back to instrumentation.

1. **You can fill in this sentence with runtime evidence, not inference**: "I am confident the root cause is X because [specific runtime observation: log line / debugger value / profiler output shows Y]." — If you can only say "I think it's probably X" or "the code looks like X", you are NOT ready.
2. **You have falsified at least one alternative hypothesis** — not just confirmed your favorite. The common-misdiagnosis-traps table above lists alternatives for each symptom type. Your instrumentation should have ruled out at least one of them.
3. **You know how to verify the fix** — you have a reproduction path that you will re-run after the fix to confirm the behavior changed (Phase 7). If you cannot describe the verification before fixing, you are not ready.

This gate is the single highest-leverage discipline in this skill. Most wasted debugging cycles come from skipping it — writing a fix on Tier 3 evidence, watching it not work, and repeating.

### Phase 6 — Escape hatch (when runtime cannot penetrate the layer)

**Frameworks**: git bisect (binary search through commit history); web research for known platform/framework issues.

Runtime instrumentation has a ceiling too: it can observe **code-layer execution paths** but cannot penetrate **platform/host-layer silent interception** (WebView `prefers-color-scheme` quirks, Electron IPC serialization, OS-level controls). When logs show the code executing correctly but the behavior is still wrong:

1. **Git bisect**: if the problem is a regression, use binary search through commit history to isolate the introducing commit (`git bisect start` → `git bisect bad` → `git bisect good <commit>` → test each midpoint). This narrows the cause to a specific diff.
2. **Web research**: search for known platform/framework issues matching the symptoms (symptom keywords + platform/framework + year). If `effective-web-research` skill is available, apply its discipline.
3. **Escalate to domain expertise**: for hybrid apps, escalate to `hybrid-debug` (four-layer model). For evidence-chain multi-hypothesis verification, escalate to `essence-diagnosis`.

### Phase 7 — Fix verification

**Frameworks**: Before/after comparison; regression testing (Kent Beck, *Test-Driven Development*, 2002); blameless postmortem (Google SRE, *Site Reliability Engineering*, 2016).

After a fix is applied, verify it with runtime evidence — not just by reading the fixed code:

1. **Before/after comparison**: reproduce the problem with the SAME reproduction steps and environment used in Phase 3. Compare the runtime behavior before and after the fix. The fix is confirmed only if the previously-observed wrong behavior is now correct.
2. **Regression check**: verify the fix did not break other behavior. Run the test suite; check adjacent code paths that share the modified logic.
3. **Heisenbug awareness — the fix itself is a timing intervention**: for timing-sensitive bugs (race conditions, deadlocks, flickering UI), both instrumentation AND the fix can change timing enough to mask the bug. A mutex lock is even more invasive than `console.log` — it fundamentally reorders thread execution. An `async/await` refactor changes microtask scheduling. A `debounce` changes event timing. Verify that:
   - The fix works **without** any debug logging enabled, in a release/production-equivalent build
   - The fix survives **many runs** (10+ for race conditions, 50+ for intermittent UI bugs) — not just one manual test
   - The fix does not introduce **new timing problems** (deadlock from lock-ordering, throughput collapse from serialization, starvation from mutex hold time)
   A fix that only "works" because its timing side-effects happen to mask a different race is not a real fix — it is a time bomb.
4. **Cleanup**: remove temporary instrumentation. Identify which logging points are worth promoting to permanent monitoring.

## Anti-patterns (forbidden moves)

1. **Re-reading code instead of escalating** — when static analysis already failed once, doing it again harder produces the same result. Escalate to runtime evidence.
2. **Shotgun instrumentation** — scattering `console.log` everywhere "just in case." Every logging point must map to a hypothesis.
3. **Declaring root cause from code inference** — "the code says X, so runtime must be X" is Tier 3 evidence, not confirmation. Runtime observation (Tier 1–2) is required for high confidence.
4. **Acting on low confidence** — entering execution (writing a fix) when confidence is still "fuzzy." The fix becomes a discarded first attempt.
5. **Ignoring Heisenbugs** — if adding logging changes whether the bug reproduces, you have a timing/concurrency issue. Do not declare victory on an instrumentation-dependent fix.
6. **Skipping fix verification** — "the code change looks correct" is not verification. Reproduce with the same steps and confirm the behavior changed.
7. **Running reproduction without user authorization** — the user must add instrumentation and run reproduction steps (unless they explicitly delegate this to the AI).
