---
name: poteto-help
description: "Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question."
---

# Poteto help

Answer the pstack question and give one usable prompt when useful. A help request does not start the workflow. A request to do work can invoke the appropriate workflow. Read the file you recommend before quoting it.

Use [CODEX.md](../../CODEX.md) for runtime capabilities and limits. The original pinned upstream snapshot records the source workflow. Its Cursor commands, model names, installation guide, Custom Modes, and automation examples are historical references rather than operating instructions for either host.

## Start and configure

The installed plugin exposes `$poteto-mode` and the individual `$skill-name` entrypoints. Use the exact discovered namespace when the client shows a qualified name. The port's install receipt and verification report establish what is installed; a source directory alone does not prove discovery.

Start a task with `$poteto-mode`, the goal, and an observable definition of done. The coordinator selects a playbook, keeps its steps in a task plan, and reads the needed sibling skills. A skipped step keeps its reason. Neither adapter registers a Cursor Custom Mode binding. Invoke the mode again for a new task, or follow the user's standing repository instructions to consider relevant pstack skills. Do not claim an always-on UI mode.

`$setup-pstack` manages an optional local user profile through a concrete reviewed change. If the profile is absent, the shared package defaults work without setup or the separate manager command. Every role inherits the parent model and reasoning by default. A panel can run independent same-model passes. Actual supported and authorized model choices may differ from the parent, but native collaboration does not reproduce the original Claude/Grok provider mix. Slot limits include the coordinator and nested workers. Larger panels queue.

The upstream explicit-only skills retain their invocation intent, with the package's documented `unslop` default and any user-specific invocation overrides preserved. Eligibility does not guarantee automatic selection. A composed workflow may read sibling skills intentionally. This does not mean all 55 skills run on every turn. `setup-pstack` remains discoverable for setup requests.

## Pick a skill

| Goal | Skill |
|---|---|
| Run a task through the complete workflow | [poteto-mode](../poteto-mode/SKILL.md) |
| Confirm the goal and problem before work | [in-your-own-words](../in-your-own-words/SKILL.md) |
| Improve task framing | [sharpen](../sharpen/SKILL.md) |
| Explain current behavior or ownership | [how](../how/SKILL.md) |
| Investigate rationale and history | [why](../why/SKILL.md) |
| Teach a system or change plainly | [teach](../teach/SKILL.md) |
| Reconstruct recent scoped work | [recall](../recall/SKILL.md) |
| Catch up on this chat in plain words and small visuals, with every item waiting on the user listed and decidable from the reply alone | [ketchup](../ketchup/SKILL.md) |
| Trace breakage outside a diff | [blast-radius](../blast-radius/SKILL.md) |
| Explore types and module shape before implementation | [architect](../architect/SKILL.md) |
| Compare independent candidate artifacts, then synthesize | [arena](../arena/SKILL.md) |
| Cover partitions or race workers with one consolidated report | [swarm](../swarm/SKILL.md) |
| Adversarially review without applying findings | [interrogate](../interrogate/SKILL.md) |
| Fix a bug with a cheap local failing test | [tdd](../tdd/SKILL.md) |
| Apply TypeScript patterns | [typescript-best-practices](../typescript-best-practices/SKILL.md) |
| Review comments independently and apply accepted changes | [no-comments](../no-comments/SKILL.md) |
| Remove generic prose patterns | [unslop](../unslop/SKILL.md) |
| Write technical documentation | [technical-writing](../technical-writing/SKILL.md) |
| Restate the previous reply plainly | [bro](../bro/SKILL.md) |
| Create an app verification harness skill | [create-verification-skill](../create-verification-skill/SKILL.md) |
| Audit the verification skill and every mapped feature | [maintain-verification-skill](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [create-formal-verification-skill](../create-formal-verification-skill/SKILL.md) |
| Validate performance measurements | [benchmark-checklist](../benchmark-checklist/SKILL.md) |
| Design a rigorous bespoke run | [figure-it-out](../figure-it-out/SKILL.md) |
| Keep and audit a decision trail | [show-me-your-work](../show-me-your-work/SKILL.md) |
| Configure supported runtime choices | [setup-pstack](../setup-pstack/SKILL.md) |
| Draft a personal working-style skill | [automate-me](../automate-me/SKILL.md) |
| Propose durable lessons from a completed session | [reflect](../reflect/SKILL.md) |
| Encode recurring repo mistakes as structural checks | [correct](../correct/SKILL.md) |
| Understand the inactive original bot integration | [make-bot-ui](../make-bot-ui/SKILL.md) |

The `principle-*` leaf skills steer decisions within a workflow. Read the full leaf before citing it. They cover data modeling, boundaries, types, shared state, idempotence, simplicity, root causes, verification, work sequencing, and scope-preserving autonomy. The complete index is in poteto-mode.

## Playbooks

All 23 playbooks remain under [poteto-mode](../poteto-mode/SKILL.md). They are reference steps selected by the coordinator, not separately registered skills.

- Investigation, Bug fix, Perf issue, Hillclimb, Runtime forensics, and Trace forensics cover evidence-led diagnosis and changes.
- Feature, Refactoring, Prototype, and Visual parity cover implementation and design exploration.
- Authoring a skill and Eval cover skill creation and behavioral comparison.
- Babysit, Shipping, and Opening a PR cover forge delivery. A status check is one pass. Babysitting stops at merge-ready. Shipping requires actual landing authority.
- Autonomous run and Orchestrate cover one long task or a larger program. The Codex adapter uses observed collaboration tools and session limits. The Dots adapter can coordinate supported background agents or configured Codex tasks. Neither Markdown adapter provisions a durable cloud runner or event subscription.
- Autopilot-full retains one owner per independent PR where merge authority is granted. Autopilot-stack delivers a chain for the operator to land.
- Session pickup, Pause safely, Multi-phase plan, and Worktree cleanup cover continuity, planning, and ownership-aware cleanup.

A plan-only request remains plan-only. A task needs a real execution mechanism to continue after the active session. Use the actual host adapter for continuation. Goals, saved schedules, heartbeats, and supported event subscriptions are created only when requested through available product tools. A scheduler poll is not an event webhook.

## Runtime differences

[CODEX.md](../../CODEX.md) selects one shared contract and the executing host's
Codex or Dots adapter. A Codex task launched by a Dot uses Codex instructions.
Dots may coordinate native background tasks, prepared cloud Codex tasks, or
connected-computer tasks when the current host exposes and authorizes them.
Saved schedules and events require explicit configuration. Missing tools remain
named gaps; no adapter invents APIs, unlimited runtime, VM survival, or credential
isolation.

The optional helpers run through `tools/runtime.py` in this installed package,
resolved from the current skill path. They require Python and explicit Bun
setup for helper commands. Core workflows do not require them or a separate
`pstack-codex` executable. Defaults work without a personal profile. User
overrides stay outside the package and apply only where supported.

`deslop`, `skill-creator`, browser/app tools, and PTY drivers are discovered external capabilities. They are not fake Cursor built-ins bundled by copying files. Investigations use actual available connector schemas and scoped host history or supplied logs. Plain CLI does not require Desktop chat APIs or PR attachments. Summaries do not prove a full transcript audit.

Comment Sicko proposes changes without edits. The coordinator checks protected classes and applies the accepted subset. The bundled Markdown agent references are not native custom-agent registrations.

`make-bot-ui` and Benny's Slack automation pack are inactive. Their original trigger, secret, and credential-isolation dependencies have no implementation. A supported Dots event does not by itself provide Benny or the original Cursor/Grok bot. They remain named limitations rather than silently installed jobs.

## Fix a run

| Symptom | Next step |
|---|---|
| A mode seems to have faded on a new task | Invoke the discovered poteto-mode entrypoint again and state the new goal. |
| A workflow starts while only help was requested | Restate the request as help. The help skill must answer without doing the work. |
| Workers collide | Stop the duplicate writer and assign real isolated worktrees or exclusive files. |
| A panel claims different providers | Inspect actual model evidence. Native inherited-model passes are same-provider. |
| A long run stops when the session ends | Resume from the checkpoint. For ongoing work use the actual adapter and configured environment; request saved schedules or events explicitly. |
| A workflow reports success from a build | Require the actual user path, output, stored value, or measurement. |
| A skill update is needed | Edit the source-managed adapter, verify it, and deliver a versioned plugin release through the chosen marketplace. The separate development manager is optional; use its reviewed workflow only when it was installed. Never edit the installed cache. |

## Make it yours

Use `automate-me` to draft preferences from scoped evidence. Use `reflect` for a local Accepted / Rejected / Backlog proposal after a session. Skill edits wait for the user's explicit approval under that workflow. Tracker posts remain separate authorized actions. Preserve personal choices outside the generated release so updates and rollback do not overwrite them.

**Reply:** lead with the answer, at most one example prompt, and a link to the adapted file supporting the answer. Keep it brief unless the full map was requested.
