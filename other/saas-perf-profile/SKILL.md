---
name: saas-perf-profile
description: "Performance profiling — find bottlenecks, measure against budgets, produce ranked optimization recommendations."
argument-hint: "[system-name or 'full']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash(bash "*/.claude/skills/saas-perf-profile/../../hooks/yaml-helper.sh" resolve_config *), Bash(bash "*/.claude/skills/saas-perf-profile/../../hooks/yaml-helper.sh" get_effective_yaml_key *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,performance.enforce,automation,workflow`

Resolved above — use as-is. No block → defaults in
`.claude/docs/config-resolution.md`.

# Performance Profile

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

## Insufficient input — check this before producing any report

**If the inputs this skill needs do not exist, the answer is "could not run" —
not a filled-in report.** Check first, and stop if the check fails.

1. List the inputs this skill reads (data files, prior reports, profiler output,
   test results, registries, source code).
2. For each, record `FOUND` or `ABSENT` — not "assumed present".
3. If any input required for a section is ABSENT, that section is
   **`NOT ASSESSED — NO DATA`**. Do not estimate it, do not infer it from an
   adjacent artifact, and do not leave a mandated cell to be filled by whoever
   reads the template next.
4. If **every** required input is ABSENT, stop and report
   **`NOT ASSESSED — NO DATA`** as the whole verdict, naming what was missing and
   which skill produces it.

**A verdict of `NOT ASSESSED` is a success.** It is the correct, useful answer to
"what does the data say?" when there is no data. The failure mode this prevents is
specific: a report whose verdict enum has no "could not run" state produces
**false clean passes** — an asset audit returning COMPLIANT on a project with no
assets and no standards, or a performance profile reporting ">99% headroom against
a 16.67ms budget" with zero profiler data and no budget ever set.

**Absence of evidence is never evidence of absence.** A scan that finds no
matches because there are no files to scan has not verified anything. Say which of
the two happened — a reader cannot tell from a green result.

---

## Phase 0: Resolve Budget Enforcement

`performance.enforce` decides what a budget violation *means* in this run. It
does not change which budgets are measured — `performance.target_lcp_ms`,
`target_fid_ms`, `target_cls`, `max_initial_bundle_kb` and `api_p95_latency_ms` are profiled the
same way at every level:

| Value | Effect on this profile's findings |
|-------|-----------------------------------|
| `warn` (default) | Violations are reported as findings. They do not block; CI logs them without failing. |
| `block` | Violations are **blockers**. Say so explicitly in the report — a `block` project treats an over-budget system as release-stopping, and `/saas-gate-check` will FAIL the Polish gate on it. |
| `off` | Budgets are informational only. Still report measured values, but do not raise violations as findings or recommendations to fix. |

Only `warn`, `block` and `off` are recognized. Surface any other value to the
user and fall back to `warn` rather than guessing.

> The value is locally overridable (`/saas-settings --local performance.enforce=block`),
> so use the resolved block above rather than reading `project.yaml` — a
> teammate's stricter local setting is meant to bite on their machine only.

## Phase 1: Determine Scope

Read the argument:

- System name → focus profiling on that specific system
- `full` → run a comprehensive profile across all systems

---

## Phase 2: Load Performance Budgets

**Read the committed budgets from config first** — they are the project's
record of what it agreed to, and design docs are the fallback, not the source:

```bash
bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" get_effective_yaml_key performance.target_lcp_ms
bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" get_effective_yaml_key performance.target_fid_ms
bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" get_effective_yaml_key performance.target_cls
bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" get_effective_yaml_key performance.max_initial_bundle_kb
bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" get_effective_yaml_key performance.api_p95_latency_ms
```

Run each line as its own plain command, one key per call: the helper moves to
the project root itself, so it works when the session was started in a
subfolder, and this skill pre-approves that form only (a `source` or `cd ... &&`
wrapper asks the user every time). Empty output means that budget is not set.

> **Resolve these budgets from `project.yaml`, not from prose.** Phase 0 above
> states these budgets "are profiled the same way at every level". A user
> who set `performance.api_p95_latency_ms: 250` in `project.yaml` has it ignored if
> the budget is read from design docs or CLAUDE.md instead.

Then fall back to design docs or CLAUDE.md for anything config does not carry:

- Target Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Initial JS Bundle size (< 200KB gzipped)
- API Latency targets (p95 < 250ms, p99 < 500ms)
- Database query execution budgets (< 50ms)
- Network bandwidth & payload limits (e.g., SSE / WebSockets)

**A metric with no committed budget is `NOT ASSESSED`, not a pass.** Do not
measure against the template's `[16.67ms]` placeholder — an unset budget is not
a budget that was met, and reporting headroom against a number nobody chose is
the exact fabrication this skill's own header warns about.

---

## Phase 3: Analyze Codebase

**CPU & Backend Profiling Targets:**
- Synchronous blocking in request handlers or Node event loop
- Nested loops over large datasets or unindexed in-memory filtering
- Heavy JSON serialization/deserialization on hot API paths
- Unoptimized database queries (N+1 query patterns, missing indexes)
- Memory leaks in Node/Python processes or uncollected listeners

**Frontend & DOM Profiling Targets:**
- Excessive DOM node count (> 1500 nodes) causing layout thrashing
- Unmemoized React components causing unnecessary tree rerenders
- Unvirtualized tables or long lists with > 100 items
- Cumulative Layout Shift (CLS) triggers: unsized images, dynamically injected banners

**Asset & Bundle Size Targets:**
- Initial JS bundle size exceeding budget (> 200KB gzipped)
- Missing dynamic imports (`React.lazy`, Next.js `dynamic()`) for heavy modals/dashboards
- Unoptimized images (missing WebP/AVIF or Next.js `<Image />` optimization)
- Unused dependencies or tree-shaking failures

**Network & I/O Targets:**
- API response latency (p95 > 250ms)
- Cache-Control header compliance (missing stale-while-revalidate / CDN caching)
- WebSocket connection retention and heartbeat overhead

---

## Phase 4: Generate Profiling Report

**Write the report to `production/polish/[scope]-report-[date].md`**, asking first
per the Collaboration Protocol: *"May I write this profiling report to
`production/polish/[scope]-report-[date].md`?"* Create the directory if absent.

> **Name the destination — do not just render the template into the
> conversation.** A profile that lives only in the transcript is gone the moment
> the session ends, and no two runs can be compared. `production/polish/`
> is the same location `/saas-team-polish` writes, deliberately: a profile taken by
> either route belongs in one place, or the comparison this skill exists to enable
> cannot be made.
>
> If a `NOT ASSESSED` section survives into the report, keep it in the written
> file. A profile whose gaps are edited out on the way to disk reads, later, as a
> complete measurement.


```markdown
## Performance Profile: [System or Full]
Generated: [Date]

### Performance Budgets
| Metric | Budget | Estimated Current | Status |
|--------|--------|-------------------|--------|
| LCP (Largest Contentful Paint) | [2000ms] | [estimate] | [OK/WARNING/OVER/NOT ASSESSED] |
| INP / FID (Input Latency) | [100ms] | [estimate] | [OK/WARNING/OVER/NOT ASSESSED] |
| CLS (Layout Shift) | [0.1] | [estimate] | [OK/WARNING/OVER/NOT ASSESSED] |
| API p95 Latency | [250ms] | [estimate] | [OK/WARNING/OVER/NOT ASSESSED] |
| Initial JS Bundle | [200KB] | [estimate] | [OK/WARNING/OVER/NOT ASSESSED] |

### Hotspots Identified
| # | Location | Issue | Estimated Impact | Fix Effort |
|---|----------|-------|------------------|------------|

### Optimization Recommendations (Priority Order)
1. **[Title]** — [Description]
   - Location: [file:line]
   - Expected gain: [estimate]
   - Risk: [Low/Med/High]
   - Approach: [How to implement]

### Quick Wins (< 1 hour each)
- [Simple optimization 1]

### Requires Investigation
- [Area that needs actual runtime profiling to confirm impact]
```

Output the report with a summary: top 3 hotspots, estimated headroom against
each budget that is set — for a metric with none, `no budget set — headroom not
assessed` — and recommended next action.

---

## Phase 5: Scope and Timeline Decision

Activate this phase only if any hotspot has Fix Effort rated M or L.

Present significant-effort items and ask the user to choose for each:

- **A) Implement the optimization** (proceed with fix now or schedule it — at `workflow: minimal`, which has no sprints, add it to the brief's build order)
- **B) Reduce feature scope** (run `/saas-scope-check [feature]` to analyze trade-offs)
- **C) Accept the performance hit and defer to Polish phase** (log as known issue)
- **D) Escalate to technical-director for an architectural decision** (run `/saas-architecture-decision`)

If multiple items are deferred to Polish (choice C), record them under `### Deferred to Polish`.

---

## Verdict

Close every run that produced a report — whether or not Phase 5 ran — with:
Verdict: **COMPLETE** — performance profile generated (saved to
`production/polish/[scope]-report-[date].md` if the write was approved). The only
other outcome is the `NOT ASSESSED — NO DATA` path above.

---

## Phase 6: Next Steps

- If bottlenecks require architectural change: run `/saas-architecture-decision`.
- If scope reduction is needed: run `/saas-scope-check [feature]`.
- To schedule optimizations: run `/saas-sprint-plan update` (at `workflow: minimal`, which has no sprints, add them to the brief's build order instead).

### Rules
- Never optimize without measuring first — gut feelings about performance are unreliable
- Recommendations must include estimated impact — "make it faster" is not actionable
- Profile on target hardware, not just development machines
- Static analysis (this skill) identifies candidates; runtime profiling confirms
