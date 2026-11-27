---
name: agent-operating-contract-evolution
description: >-
  Rewrite an assistant's standing instructions, persona and permissions across its identity file,
  AGENTS.md and memory. When the owner changes the agent's role or authority, make delegation and
  publishing boundaries stick across handoffs; measure prompt compression without dropping rules.
  Not for agent-harness-settings-parity.
metadata:
  revision: "9"
  areas: "software-development,work-management,self-management"
  targets: "runtime-agnostic"
  summary: "evolve an agent's identity file and operating protocol by layer, with coverage markers, behavioral evals, and load-scope probes"
  summary_zh: "按分层演进 agent 身份文件与操作协议：覆盖标记、行为评测、加载范围探测"
  kind: "entry"
---

# Agent Operating Contract Evolution

## Before writing

- A shortcut or a finding from a trace is not consent to change persistent instructions. Clarify
  the intended behavior and layer; confirm the target, durable edit and any authority change
  unless the owner already explicitly authorized that scope. A draft request is read-only.
- Use the owner's risk policy; Yellow/Red labels have no universal meaning. Back up authorized
  durable edits with timestamps. Protected files require their own approval; a denial or timeout
  leaves the file unchanged. Do not retry or bypass it. Report the blocked lines and pending edit.
- Changes to permissions must agree across all affected layers; restate the limits that remain.
  Compression must preserve all rules, especially hard limits.

## Edit and prove

1. **Establish the baseline.** Read the relevant files and traces. Identify the correction and
   the observable result. Use [loading probes](references/context-file-loading-probes.md) to
   verify actual files, cwd scope and precedence before moving a rule. Check the installed
   runtime version; a loader recipe does not prove behavior. Pass required rules explicitly to
   subagents that do not load them. Do not change runtime source to fix the contract.
2. **Choose one canonical owner.** Identity owns stance, voice and cwd-independent hard limits;
   the operating protocol owns routing and execution; memory owns stable facts and preferences;
   skills own reusable procedures; config owns runtime settings; long outputs are artifacts.
   For subjective design, offer a few concrete choices and resolve one section at a time.
   Distinguish borrowed ideas from local conventions.
3. **Patch narrowly.** State trigger, action and proof. For a permission change, search all
   layers and update affected references together. Keep profile deltas to differences; rebuild
   from the canonical file plus deltas and check wrapper flags, section pointers, counts and
   drift using [the reconciliation procedure](references/pitfalls.md).
4. **Prove coverage and behavior.** For compression, declare one distinctive marker per rule
   before editing and run `uv run scripts/contract-coverage-check.py OLD NEW markers.txt`.
   Keep the minimum voice anchors and disambiguating examples; measure bytes and non-heading
   rule lines before and after. Keep replies human-facing. For any contract change, use
   [behavioral evals](references/behavioral-evals.md) in equivalent fresh contexts before and
   after. Default to 10-15 one-shot cases; size the set to the changed behaviors and restraint
   paths. Compare raw outputs and expect/forbid outcomes. Keep cases out of the workspace and
   fail contaminated runs. Use read-only tools or safe mode for gate cases; check external state.
   If a write escaped, report what changed, ask whether to keep or revert, and record the
   decision. Same-family reviews are not independent.
5. **Report** the layer, final and backup paths, meaningful diff, and proof or verification
   limits. After meaningful work, identify where the lesson belongs; applying another durable
   change still requires authority.

Only if a script command fails (for example `uv` is not found), read
[references/troubleshooting.md](references/troubleshooting.md).

## Read on demand

- **Prompt budget:** measure the actual assembled prompt and verify the largest reducible block
  with [context budget measurement](references/context-budget-measurement.md).
- **Storage and migration:** verify store ownership, gate implementation and call sites with
  [routing probes](references/asset-store-vs-workspace-routing.md). Inventory to full depth and
  sweep old references before retirement; use [the migration procedure](references/knowledge-vault-migration-execution.md).
- **Control-plane review or refactor:** use the [review checklist](references/agent-contract-system-review.md)
  or [refactor playbook](references/agent-repo-refactor-playbook.md). For repo-owned skill
  placement, use [the port procedure](references/repo-owned-skills-port.md).
- **Voice and role rewrite:** see the [case study](references/contract-evolution-case-study.md).
