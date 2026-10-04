---
name: model-capability-router
description: "Use when the operator explicitly asks for native Codex model or reasoning-effort routing, including an active standing request."
---

# Native Model Routing

Use native Codex model, effort and agent selection. Respect the operator's
selected main model and effort; this skill does not switch an active task.
The profiles below are policy recommendations. They do not establish the
current host configuration or model selected by a running task; check those
separately before describing them as configured. Choose the execution
arrangement before a delegated worker's model.
Authorization to delegate alone does not require consulting this router.

## Execution arrangement

Keep small, tightly coupled work and immediate follow-ups with the agent that
already holds the relevant context. A cheaper worker model alone does not
justify a handoff. Batch related operations rather than delegating each one.

When the operator requests delegation, preserve that workflow for suitable
bounded work. Otherwise delegate when the benefit justifies briefing, startup,
coordination, verification and likely correction costs. Reuse a suitable worker
and its relevant context for related follow-ups, without assuming cache reuse.
Give it the context needed for its acceptance checks.

Parallelise independently executable packages with clear ownership when the
benefit outweighs duplicated context and integration costs. Sequence dependent
work. Faster completion and lower consumption are separate benefits.

Continue the current thread when its context remains useful. A fresh task suits
an independent objective; a full-history fork copies history rather than
providing a clean context.

Keep one visible task per coherent outcome. Use native subagents for useful,
bounded work inside that task. Create a separate user-owned task only on the
operator's explicit request, for an independent or durable outcome, a schedule,
or a required host/cloud boundary.

## Operator profiles

| Profile | Model | Effort | Use |
|---|---|---|---|
| Recommended coordination profile | `gpt-6.1-sol` | `medium` | Recommended for sustained coordination, integration and open-ended execution when available; verify the actual host selection separately. |
| Planning, review and difficult decisions | `gpt-6-astra` | `low` | Habitual Astra setting when its judgment helps. |
| Exceptional reasoning | `gpt-6-astra` | `xhigh` | Rare difficult decisions or unresolved investigations after the task warrants deeper effort. |
| Bounded subtask | `gpt-6-luna` | `high` | Narrow, well-specified work with clear ownership and acceptance checks. |
| Defined execution | `gpt-6-luna` | `xhigh` | Implementation or transformation with a concrete outcome and verification. |
| Substantial execution | `gpt-6-luna` | `max` | Justified when deeper effort materially helps a bounded implementation with observable proof. |

For demanding coding, GPT-6.1 Sol high is an available task-specific override
when medium is insufficient; choose it for the work rather than forcing an Astra
escalation. It does not replace the recommended medium coordination profile.

Choose directly for the task. Use an Astra → Sol → Luna sequence only when
coordination materially helps the outcome; a direct bounded worker or the
current agent is enough when it does not. There is no mandatory model ladder,
failed-attempt retry, coordinator stage, automatic planning/review delegation,
CLI resolver, receipt workflow or preset wrapper. Requested planning or review
delegation remains available when suitable. Importance alone does not justify
XHigh. A read-only task can still need Astra. Patch size alone does not prove
that Luna suits autonomous systems administration.

Luna Max is available when justified by the work; it requires no repeated
approval merely for that effort. Choose effort for the workload; higher effort does not guarantee better results.
GPT-6 supports cache-preserving effort updates through its documented mechanism;
do not assume every client uses it or that cache is shared across models or tasks.
Current GPT-6.1 capability, pricing and benchmark evidence is in
[references/gpt61-sol-20260929.md](references/gpt61-sol-20260929.md). The
historical GPT-6 evidence remains in
[references/gpt6-20260922.md](references/gpt6-20260922.md). These profiles do
not authorise new spending routes, external actions or additional access. Astra
Max and Ultra are outside the habitual palette. Terra and other supported
models remain available when selected by the operator or bound to a specialist.
Honour explicit selections and fixed bindings, including those outside this
palette.

## Changing selection during work

Keep GPT-6.1 Sol medium as the recommended policy default and choose
task-specific overrides through the native surface that actually supports them.
Honor an explicit native effort selection, including low; this recommendation
does not require changing a home configuration or an active thread. In CLI,
`/model` changes model and
supported effort within a session. A task follow-up tool may expose model and
effort overrides; use them only when that tool supports the target. Do not
message the current task recursively to simulate self-switching. The current
agent cannot claim to change its own model without an exposed control and
confirmation. Use the existing bounded specialist delegation when suitable.
Changing `config.toml` sets a default, not proof that an active turn switched.

## Runtime and delegation

Before selecting compute, check the exact channel's current advertised models
and efforts. Current-task, native-subagent and user-owned-task support differ.
Do not invent unsupported capability, create a task to work around it, or
silently substitute. Report the gap and continue locally when the existing
selection can meet the proof bar; otherwise surface the specific decision
needed.

For permitted delegation, give bounded ownership, relevant context, expected
output and verification requirements. A differently modelled native worker
needs fresh or bounded context: full-history forks inherit the parent model.
Respect actual available slots; a concurrency ceiling is neither a target nor
permission to spawn.
Do not make specialists coordinators or enable recursive delegation implicitly.
The coordinator integrates and verifies the result.

Creating a user-owned task, forking, moving or archiving tasks still requires
the corresponding explicit user request. Routing grants no authority over
hosts, accounts, private data, credentials, publication or destructive actions.
Respect native approvals and refusals. Do not force feature flags.

Before accepting a delegated deliverable, check the requested elements against
the actual result and verification evidence. Concise reporting must not remove
required work or presentation quality. Correct omissions before delivery;
change the assignment or model when observed failures justify it.

## Cost and evidence

Compare the remaining whole task, including parent and worker input, output,
briefing, startup, coordination, verification and rework. Reusing a relevant
worker can save context transfer; cached input is possible, not guaranteed
across tasks, models or changed prefixes. Do not add speculative cache
retention, keepalive prompts or repetitive polling merely to preserve context
or show activity. Count reasoning and child usage once if a meter already
includes them. API token prices and benchmarks inform comparisons but do not
measure this account's Codex allowance or prove a routing saving. Use observed
account usage or a like-for-like native task comparison for such claims; state
when that evidence is unavailable. Keep changing prices and benchmark scores
out of durable profile rules.

## Installation and updates

The sole install source is `TheAngryPit/TheAngrySkills`, not Workbench.

```bash
npx skills add https://github.com/TheAngryPit/TheAngrySkills.git -g -a codex -y -s model-capability-router
```

Use one canonical installed skill per OS user, shared by Codex profiles through
native discovery or links. A profile link is not a second independent version.
Keep source metadata pointed at the normal repository. `npx skills` records
update provenance; it does not provide an automatic update schedule. Inspect
the installed CLI's update/check behavior before using it as a read-only check.

## Native named-agent profiles

This skill is also the public distribution surface for the native named-agent
profiles used by the adapted pstack workflows:

- `assets/agents/comment-sicko.toml` is the named reviewer for
  `cursor-no-comments`.
- `assets/agents/poteto-agent.toml` is the named delegate for
  `cursor-poteto-mode` playbooks.

Keep these pstack specialist identities, ownership and verification contracts
when the profiles are used; model routing does not flatten named roles.

The assets are not loaded merely because this skill is installed. To make the
profiles selectable by a new Codex session, run the bundled checked installer
from this skill directory:

```bash
python3 scripts/check-native-agent-profiles.py \
  --install --installed-dir ~/.codex/agents
```

The bundled script travels with an individual skill installation; it does not
depend on the repository-level `scripts/` directory.

The command refuses to replace a differing existing profile unless
`--replace` is supplied explicitly. Run it again with only
`--installed-dir ~/.codex/agents` for a byte-for-byte check. This validates
distribution and configuration, not that a newly started session has loaded or
selected the profile; that must be checked by the host session.
