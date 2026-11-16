---
name: gain
description: "Show honey's measured benchmark gains as a one-shot scoreboard, with sources and no per-repo savings claims."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-11-14"
  sources: "DietrichGebert/ponytail 4.7.0 skills/ponytail-gain (scoreboard format and honesty boundary, adapted; MIT); honey-stack evals/webmcp/reports/2026-11-01-fast-qa-v3.md and evals/agent-browser/reports/2026-11-14-agent-qa.md (figures)"
---

# Gain

Show this scoreboard when invoked. It is a one-shot display: change no mode, write no file, persist nothing.

The figures come from honey's published benchmark reports. They were measured on honey's fixtures, not on the current repository. Each line names its report so the user can check it.

## Scoreboard

Render plain ASCII bars. A bar's length shows the measured ratio; the label carries the exact figure.

```
  honey gain                           measured on honey fixtures · medians

  Prepared QA run   older QA        ████████████████████  7.21s
  (24 cases)        e2e + WebMCP    █████████···········  3.40s          2.12× faster
  Live agent QA     Playwright MCP  ████████████████████  ≈1,231 tokens
  (12-step flow)    agent-browser   ████················  ≈270 tokens    4.6× less to read
                    wall time       tie (3.13s median each)

  Sources: evals/webmcp/reports/2026-11-01-fast-qa-v3.md
           evals/agent-browser/reports/2026-11-14-agent-qa.md
  This repo: /honey:review — deferred `shortcut:` debt and what's still cuttable
```

## Honesty boundary

These are benchmark medians from honey's fixtures, not this repository. Never print a per-repo saving ("you saved X tokens/lines/seconds here"): the alternative run never happened, so there is no baseline to subtract. Don't extrapolate the ratios to the user's app or to a whole agent session. Point to `review`'s debt scan for real per-repo counts instead.

If the user asks for a gain on their own project, offer to measure it: the same workload, before and after, repeated, with the ratio from the same run, following `perf`.

## Boundaries

One-shot display. It edits nothing and changes no mode.
