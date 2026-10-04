---
name: __SKILL_NAME__
description: M8M 3.1 product skill whose closed native source compiles into a displayable, executable milestone workflow.
---

# __SKILL_NAME__

Invoke `$__SKILL_NAME__` through `agents/openai.yaml`, the graph and public
contract authority. Each node owns `agents/<milestone>.yaml` and its complete
master prompt at `references/<milestone>.md`.

Author the full prompt first: role, goal, inputs and reference roles,
instructions, constraints, and deliverable. Start execution and recovery with
that whole prompt. Every milestone Markdown then lists numbered FlowSteps with
descriptive actions and actual tools, followed by named outputs. Match agent
bindings; leave no placeholder tool names.

Name new milestones `milestone01`, `milestone02`, etc.; keep IDs stable on edits.
Bind later inputs to earlier named outputs and explain their reference roles in
the prompt. Graph order controls execution.

Canonical `flow.yaml` is generated review output. Edit native source instead.
Generated tools remain `BUILD_REQUIRED` and `non_runnable` until implemented and
validated. `planning/m8m-flowchart.md` is an optional canvas projection.

Inputs are semantic context interpreted through the master prompt. Do not create
or validate a milestone input schema. Preserve useful upstream bindings. Every
milestone returns structured named outputs validated against its output schema.

Default to `loop: none`. Complete from actual named outputs and schema checks.
Do not add hashes, revisions, proof graphs, or automatic image reviews. A
checksum or review needs an explicit request or an external API requirement.
Keep one current chosen output per milestone.

Local coordination reuses existing tools without packaging. For an explicitly
packaged workflow, `scripts/m8m_run.py` uses the codebase launcher at
`flowsteps/flows/<flow_id>/launch.py`, which selects a digest-addressed runtime
release beside the harness. It must never import or invoke `m8m-harness-builder`.
This skill never pushes, publishes, deploys, or activates anything.
Builder 2.x run folders are untrusted import evidence.
