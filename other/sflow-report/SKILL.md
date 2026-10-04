---
name: sflow-report
description: Generate a read-only Singularity Flow workflow performance report with phase duration, approval waiting, rework, committed model/token telemetry, provider or configured cost, and bottlenecks.
disable-model-invocation: true
argument-hint: "[WORK-ID] [--format md|html|json] [--out FILE]"

---
# Report workflow performance

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Run `singularity-flow report <arguments>`.
2. Summarize elapsed wall-clock time, active time, approval waiting, generations, rejections, self-approvals, token availability, and the approval-latency bottleneck.
3. Read committed `telemetry/` references returned by the CLI under immutable `workflow.resolution.workItemRoot`; never assume `singularity/work-items`. Treat token totals as exact only where the provider supplied exact usage. Preserve `partial` and `unavailable` disclosures.
4. Prefer exact provider cost captured by Copilot OTel. Otherwise show cost only when workflow YAML contains pricing for the exact recorded model; explain that configured prices are per million tokens and may be partial.
5. Explain that durations include nights and weekends and are not business-hours or productivity estimates.
6. Do not change workflow state, generate artifacts, submit, approve, reject, commit, or push. Only write a report file when the user explicitly supplies `--out`.
