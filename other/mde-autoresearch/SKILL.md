---
name: mde-autoresearch
description: Use for the continuous multi-agent research and auto-improvement loop that discovers tools, SDKs, libraries, techniques, blogs, tutorials, and repo patterns, then converts accepted findings into bounded implementation work.
---

# MDE Autoresearch

Use this skill for independent research and auto-improvement of setup, tooling, devcontainer, telemetry, and agent workflow.

## Core Loop

- discovery -> repo mining -> social/blog mining -> validation -> synthesis
- keep every run bounded with explicit `keep`, `discard`, `escalate`, or `crash` outcomes
- no unbounded autonomy
- no direct implementation changes unless the accepted output is a scoped PR-ready change

## Required Skills

- `skills/mde-agent-runtime-contract`
- `skills/mise-enforcement`
- `skills/research-source-discovery`
- `skills/github-repo-mining`
- `skills/social-signal-mining`
- `skills/evidence-synthesis`

## Required Commands

- `mise run mde:agent:preflight`
- `mise run mde:research:autoimprove -- --incremental`
- `mise run mde:research:autoimprove -- --full`
- `mise run mde:agent:report`

## Source Policy

- Dynamically mine `jdx`, `karpathy`, and `ottogin` as seed upstreams.
- Do not hardcode those as the only source universe.
- Capture tools, SDKs, libraries, techniques, blogs, tutorials, release notes, and repo patterns.

## Output Contract

Every run must produce evidence-backed records under `reports/mde-autoresearch/` and emit telemetry under `reports/agent-policy/`.
