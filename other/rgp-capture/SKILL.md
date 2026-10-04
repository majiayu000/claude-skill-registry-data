---
name: rgp-capture
description: Install or locate the full AMD Radeon Developer Tool Suite and capture reproducible Radeon GPU Profiler (.rgp) traces from HIP applications on Windows. Use when Codex needs to create instruction-timing, SQTT, event-timing, or hardware-counter captures; select safe RGP capture options; diagnose failed captures; or hand an existing trace to a separate inspection workflow.
---

# RGP Capture

Create a small, reproducible `.rgp` capture with the full Radeon Developer Tool
Suite. Keep the panel CLI visible and keep capture separate from analysis.

## Workflow

1. Read [references/capture.md](references/capture.md) for installation and command examples.
2. Install or locate the full suite. Do not describe the suite archive as a standalone RGP download.
3. Identify the exact target executable and dispatch to capture without recursively scanning build or trace directories.
4. Choose one capture purpose:
   - instruction attribution: enable instruction tracing;
   - hardware counters: enable counter collection;
   - ordinary event timing: use a normal dispatch capture.
5. Run `RadeonDeveloperPanelCLI.exe` visibly in one terminal and wait for `Ready for capture`.
6. Run the target visibly in a second terminal.
7. Confirm that the panel reports `Successfully collected and dumped trace` and that the output file exists.
8. Record the suite version, capture command, target command, GPU, dispatch selector, and output path.

## Capture rules

- Never launch the panel or workload hidden in the background.
- Start with one captured dispatch. Increase the count only when the experiment requires it.
- Capture instruction timing and counters separately unless that exact combination is already verified on the installed driver and suite.
- Use the same workload shape, warmup, clock policy, and dispatch selector when comparing variants.
- Do not treat a connected client as a successful capture; require a completed trace file.
- If the client disconnects during collection, reduce the capture to one dispatch before changing the workload.
- Do not rerun successful variants merely because another variant failed.

When a trace exists and the task becomes decoding or interpretation, use the
`rgp-inspect` skill.
