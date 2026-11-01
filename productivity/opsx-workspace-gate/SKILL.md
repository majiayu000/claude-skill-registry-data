---
name: opsx-workspace-gate
version: "1.1.0"
user-invocable: false
description: "Shared OpenSpec workspace gate for OPSX workflows: locate project root, verify openspec/, and require exact native OPSX skills before delegation. Triggers — 「OpenSpec 工程门禁」「OPSX 工程定位」「OpenSpec 原生技能检查」 / OPSX workspace gate, OpenSpec project root, native skill gate. Do NOT use for Jira, Git, retry binding, or implementation orchestration."
---

# OPSX Workspace Gate

> Internal shared skill for OPSX workflows. It establishes an OpenSpec project root and verifies native-skill prerequisites before the host starts its workflow-specific orchestration.

## 1. Locate the project root

Use this priority order and stop at the first unique result:

1. The current working directory contains `openspec/`.
2. Walk upward from the current edit file and use the first ancestor containing `openspec/`.
3. Scan direct children of the current working directory for `openspec/`.
   - One match: use it.
   - Multiple matches: list candidates and wait for the user to select one.
4. No match: stop and ask the user to enter an initialized OpenSpec project or run `openspec init`.

Output `【工程定位结果】目标工程根：<absolute path>`. Run subsequent OpenSpec paths, CLI commands, and native-skill delegation from that root; if changing the working directory is unavailable, use absolute paths.

## 2. Verify the OpenSpec directory

Confirm `<project-root>/openspec/` exists. If it does not, stop and instruct the user to run `openspec init`; do not silently initialize it.

## 3. Verify native OPSX skills

Search installed skill directories under the project root and require these exact names:

| Required skill | Workflow purpose |
|---|---|
| `openspec-new-change` | Create a change |
| `openspec-continue-change` | Create or continue artifacts |
| `openspec-apply-change` | Implement checked tasks |
| `openspec-archive-change` | Archive a completed change |

`openspec-verify-change` is optional. Legacy or alternate names do not satisfy this gate. If a required skill is missing, stop and direct the user to run `openspec init` (first setup) or `openspec update` (refresh skills).

## Delegation discipline

- Before delegating to any native OPSX skill, read that skill's current `SKILL.md`.
- CLI commands such as `openspec status` and `openspec validate` are allowed tools; they do not replace native skill delegation.
- Hosts retain stage ordering, Jira/Git operations, retry/change binding, artifact sinks, and all workflow-specific decisions.

## Integration guide

An OPSX host declares `opsx-workspace-gate` as a dependency, loads it for location plus gates, then continues with host-only setup. Do not copy this location algorithm, exact-name table, or delegation rules into the host.
