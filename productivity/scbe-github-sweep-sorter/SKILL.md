---
name: scbe-github-sweep-sorter
description: Sort GitHub and local repo sweeps into governed agent lanes using HYDRA formations, roundtable role assignments, repo triage buckets, and deterministic handoff packets. Use when classifying repos, PRs, issues, security alerts, or dirty trees before assigning collaborative AI work in one shared codebase.
---

# SCBE GitHub Sweep Sorter

Use this skill when a repo or org needs to be swept, sorted, and routed into explicit agent lanes before coding starts.

Pair this skill with:
- `scbe-ai-to-ai-communication` for packet delivery and handoff logging
- `multi-agent-orchestrator` when the sweep turns into parallel execution

## Quick Start

1. Collect the sweep surface.
   - Local: `git status`, repo hygiene reports, branch state, changed roots.
   - GitHub: PRs, issues, alerts, repo inventory, review queues.
2. Bucket items before fixing anything.
   - `keep-in-repo`
   - `archive-or-cloud`
   - `ignore-or-cache`
   - `security-now`
   - `manual-review`
3. Choose a HYDRA formation with `scripts/choose_formation.py`.
4. Build one roundtable packet with `scripts/build_roundtable_packet.py`.
5. Hand the packet to the communication lane instead of letting agents collide.

## Formation Selection

Read `references/formations.md` when the right formation is not obvious.

Default formation rules:

- `scatter`
  - Use for discovery across many repos, many alerts, or broad org triage.
  - Best when the work is mostly classification and evidence gathering.

- `hexagonal-ring`
  - Default coding and repo-governance formation for the six Sacred Tongues.
  - Best when multiple agents collaborate on one shared codebase but ownership stays explicit.

- `tetrahedral`
  - Use for smaller, high-focus, higher-risk implementation packets.
  - Best when four critical roles are enough and shared-file pressure is high.

- `ring`
  - Use when order matters.
  - Best for approvals, critical security actions, release gates, and chain-of-custody decisions.

## Role Map

Read `references/role-map.md` for the full mapping.

Default six-tongue roundtable:

- `KO` architecture curator
- `AV` transport and discovery
- `RU` policy and governance
- `CA` implementation engineer
- `UM` security auditor
- `DR` schema, release memory, and evidence keeper

Optional spine role:

- `SPINE` integration coordinator
  - owns packet routing, status rollup, and conflict resolution
  - does not compete with the six tongues for the same file edits

## Governance Thresholds

Read `references/governance-thresholds.md` when deciding quorum.

Use risk-tiered thresholds, not one fixed quorum claim:

- low-risk classification and discovery: `3/6`
- medium-risk code or config changes: `4/6`
- critical security, destructive, or release actions: `5/6`
- ordered attestation path required: use `ring` and preserve signer order

Use the corrected language:
- prefer `BFT-informed threshold governance`
- do not claim a single hard Byzantine quorum for every action

## Sweep Workflow

### 1. Collect

Gather only what the sweep needs:

- repo name and branch
- dirty-tree summary
- PR / issue / alert counts
- high-risk roots or files
- whether the task is discovery, implementation, review, or release

### 2. Classify

Use `scripts/classify_sweep_targets.py` for a first pass.

The target buckets are:

- `keep-in-repo`
- `archive-or-cloud`
- `ignore-or-cache`
- `security-now`
- `manual-review`

The purpose is not deletion. The purpose is separating source, evidence, outputs, and cache so the repo stays readable.

### 3. Choose Formation

Use `scripts/choose_formation.py` to pick:

- formation
- quorum target
- whether ordering is required
- whether a shared-file collision risk exists

### 4. Assign Work

Every packet must declare:

- `task_id`
- `formation`
- `quorum_required`
- `owner_role`
- `allowed_paths`
- `blocked_paths`
- `goal`
- `done_criteria`

Never let two agents edit the same mutable file without explicit ownership.

### 5. Emit Packet

Use `scripts/build_roundtable_packet.py` to create a machine-readable packet.

If the work will be handed to another AI, route the packet through `scbe-ai-to-ai-communication`.

## Output Contract

Read `references/packet-schema.md` for the full packet.

Minimum output:

```json
{
  "task_id": "sweep-20260314-001",
  "repo": "SCBE-AETHERMOORE",
  "branch": "main",
  "formation": "hexagonal-ring",
  "quorum_required": "4/6",
  "summary": "Sort security alerts and repo hygiene roots into owned lanes",
  "work_packets": [
    {
      "tongue": "KO",
      "role": "architecture-curator",
      "goal": "Confirm boundaries and non-goals",
      "allowed_paths": ["docs/", "schemas/"],
      "blocked_paths": ["src/", "tests/"]
    }
  ]
}
```

## Safety Rules

- Keep one shared mission, not one shared file free-for-all.
- Preserve evidence and artifacts; sort them before deciding whether they belong in repo or archive.
- For critical actions, preserve ordered roundtable signatures.
- Treat `Word`, `browser`, `workflow`, and `repo` clients as outer execution planes. The sweep packet governs them; it does not get replaced by them.
- Do not confuse cache outputs with successful workflow templates.

## GitLab pond bucket (optional)

When a sweep item is clearly "lore/research pond" work:
- bucket it explicitly as `gitlab-pond`
- route to `scbe-gitlab-pond-integration` for pond flush + mirror decisions

## References

- `references/formations.md`
- `references/role-map.md`
- `references/governance-thresholds.md`
- `references/packet-schema.md`

## Scripts

- `scripts/choose_formation.py`
- `scripts/classify_sweep_targets.py`
- `scripts/build_roundtable_packet.py`
