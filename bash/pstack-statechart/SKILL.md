---
name: pstack-statechart
description: "Check a TLA+ state-transition model with TLC and explain its reachable states or a counterexample as a chart. Use for statechart requests or when a modeled state path needs visual explanation."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/4dd1d05818d19792e7cd6e818f1667f95f7e1dbe/pstack/skills/statechart
  upstream-commit: 4dd1d05818d19792e7cd6e818f1667f95f7e1dbe
  adaptation: portable-chat-inherited
---

# Statechart

Check a bounded TLA+ model with TLC and explain its states and violation paths in the reader's terms. A chart describes the model and its assumptions, not automatically the running system.

## Environment contract

Use the active chat model and its current reasoning settings. Work directly by default; delegate only when authorized and inheritance is guaranteed. Follow the user's scope, repository instructions, and resource controls. The skill does not authorize publication, messages, changes to unrelated projects, or global dependency installation.

Discover Node 22.18–22.x or 23.6+, Java 11+, and a `tla2tools.jar`. Prefer existing trusted dependencies. If unavailable, obtain the official TLA+ tools release in task-owned storage; the upstream-pinned [TLC 1.7.4](https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar) has SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`. Verify the hash before use and report any unavailable prerequisite. Set `TLA2TOOLS` to the jar and `JAVA` to the Java executable before execution so the upstream helper does not auto-install tools. Review view modules before executing them: they are code.

## Model and run

Write the spec, config, and optional view in task-owned storage. Map modeled actions, atomicity, and assumptions to source when the model represents code. Define each agreed rule as an invariant or property, keep the model finite, and include intended terminal behavior. For labeling, model constraints, TLC result semantics, and chart limits, read [modeling and results](references/modeling.md).

Run the bundled helper under the host's finite-job resource controls. On a Unix-like host use `sh scripts/statechart` with a spec and optional `--config`, `--view`, and new `--out` directory. The command exits 0 when checks pass, 1 on a rule violation, and 2 on errors. A chart may be omitted for larger state spaces; inspect `report.md` and TLC output in all cases.

On Windows the upstream CLI uses Unix process groups and is not supported natively. Run the bundled `scripts/worker.ts` directly with Node instead, supplying four separate arguments: an existing empty task-owned stage directory, the spec path, config path, and optional view path. Use the host's resource launcher for the Node process. The worker writes `done/report.md`, `done/tlc.out`, and when available `done/chart.mmd` under that stage; it exits 0 for a pass, 1 for a violation, and 2 for an error. The stage and any residual temporary files belong to this run. This direct worker does not provide the Unix CLI's interrupted-process cleanup; use the host's normal cancellation and inspect owned processes and files if interrupted.

Do not run the worker concurrently against the same stage. Preserve output and command, dependency versions, model bounds, assumptions, unchecked rules, and any hidden chart steps. An execution failure or a rule not checked is not a pass.

## Render with Pele

Render each delivered Mermaid chart with Pele and provide the SVG alongside its `.mmd` source. Reuse the installed global package; discover its location rather than adding a dependency to the repository. For invocation, limits, standalone SVG styling and bug marks, read [Pele rendering](references/render.md). Use another renderer when the user requests it. On rendering failure, preserve the Mermaid source and report the error. Rendering does not rerun TLC or change its verdict.

## Explain

Show the reachable transitions or each shortest reported violation path in the reader's language. Give the Mermaid source or an appropriate host-supported visualization, and make clear when a chart groups states or omits paths. Explain each violated rule, evidence, and limits. Replay a model's counterexample against actual code when the request concerns a real implementation; treat an unreproduced path as a model or correspondence question, not a confirmed product defect. Differentiate bounded model checking from code proof and production behavior.
