---
name: architect
description: Start robotics apps or demos from compatible examples for interactive simulation, pretrained visual control, mapping/navigation, robot assistants, or manipulation. Choose a stack if none fits; not existing-app maintenance.
---

# Architect

Reach a visible robot result with the least new work, then customize. Inspect
existing examples before researching or designing a new stack.

Without an established app, an outcome-only request such as trying interactive
simulator examples, mapping an environment, or running a pretrained policy is
a first-run request even without "new project", a robot brand, or "architect"
in the prompt. Use this skill inline, not the optional heavy-research architect
subagent. If a domain skill brought you here, select the baseline once and
return to that skill for its mechanics; do not loop through architecture again
for the same task.

## Start from the outcome

- Inspect the current repository, the Robium app registry, and the closest
  working example before asking questions.
  Start with candidate READMEs, manifests, and launchers; exclude generated
  environments, caches, and model assets from discovery scans.
- Define what the robot should visibly do, where it will run, and what evidence
  would make the first slice credible.
- Honor the user's stated target platform and restrictions even when the agent
  runs on a different host. Ask about a compatible alternative, not for them to
  restate constraints they already gave.

## Offer the shortest useful starting path

After a quick registry and candidate check, surface these paths briefly, mark
the recommendation, and explain what would run first. Do this before broad
research, architecture documents, cloning, or lengthy setup. Do not turn the
four paths into a mandatory questionnaire: when intent is clear, explain and
proceed within it; ask one short question only for a consequential choice.

| Path | When it fits | First step |
| --- | --- | --- |
| Try an example | Close compatible match; user wants to see it work | Run it unchanged in the existing checkout; no new project. |
| Adapt an example | Close match; user wants their own customized app | Verify the baseline, then make a separate derivative and change one behavior. |
| Reuse selected pieces | Partial overlap; useful components fit the new app | Reuse the smallest compatible pieces and prove one integrated behavior. |
| Start fresh | No useful compatible overlap, or explicitly requested | Use the domain skills to scaffold only the smallest visible slice. |

For "just try it", default to the compatible example with the fewest new moving
parts, not the most ambitious stack. Describe prerequisites and first-run work,
not unmeasured speed promises. Read [reuse paths](references/reuse-paths.md)
only for adaptation, component reuse, or a fresh scaffold.

## Inspect candidates and prove the selected slice

- Resolve the user's workspace with `npx robium-ai workspace --json`; its
  `repo` and `apps` paths are authoritative, not a hardcoded `~/robium` or the
  installed plugin cache. For workspace discovery and an occasional quiet
  freshness check before a new example, read
  [workspace updates](references/workspace-updates.md). Checking is not updating.
- Discover candidates in the [Robium app registry](https://github.com/robium-ai/robium-apps/blob/main/REGISTRY.md),
  using a sibling checkout when available. Match the task, host architecture,
  runtime requirements, and relevant verification evidence, not just the name
  or a `stable` label. Read the selected app's README and launcher; distinguish
  tested conditions from assumptions. For the homepage's first-run tasks,
  use [first-run examples](references/first-run-examples.md), then read that
  candidate's exact README and manifest without scanning the whole apps checkout.
- For a clear compatible match, explain the choice and proceed within the
  user's request: "This matches Robium's navigation example. I'll get it
  running first, then we can adapt it." Ask only when different candidates or
  an incompatible platform materially change the outcome. Honor an explicit
  request to build from scratch. Routine maintenance stays in the owning skill.
- Use the existing checkout without resetting or pulling over user changes;
  acquire a separate checkout when necessary. Record the source revision and
  any local changes. For whole-app reuse, run the baseline with its launcher,
  pinned environment, assets, and viewer; do not create a derivative, upgrade
  dependencies, or recreate infrastructure just to demonstrate it.
- Check prerequisites, credentials, and occupied ports before lengthy builds.
  Explain first-run downloads and reuse caches on later starts. Missing model
  access is a blocker, not permission to substitute a mock and call it live.
  Keep secrets out of prompts/logs; explain API charges and obtain authorization
  before paid calls. Do not provision cloud resources or move physical hardware
  as an implicit part of onboarding.
- Check the requested behavior at a meaningful milestone, not after each edit.
  Use the app's smallest relevant check, not a new suite or repeated UI tours.
  A low-risk visual check may be handed to the user with exact steps and an
  explicit unverified status; an open port is not proof the demo works.
  Stop only processes started for this run.
  If blocked, report the exact unmet prerequisite without inventing a new stack.
  Before a port, dependency overhaul, or prolonged troubleshooting, surface
  the blocker and a simpler compatible path; let the user choose the tradeoff.
  For try-only requests, offer one small customization after it works. For
  requested customization, proceed with the agreed change and keep the baseline.

## Choose only the stack the slice needs

- When environment setup is needed, use `environments` early.
- For ROS-based mobile navigation, route through `ros2`, `navigation`, `simulation`, and
  the selected simulator and visualizer.
- For learned manipulation, route through `lerobot`, `data`, and
  `huggingface`; add a simulator only when the first slice needs one.
- Use `integration` when module boundaries or cross-process communication are
  themselves a design decision.
- Use `testing` when risk, uncertainty, or requested test work needs a verification
  decision; do not automatically author tests. Use `test-assets` for needed fixtures.
- Route provider mechanics to `cloud-run` or `runpod` only after deployment is
  part of the approved slice. A public session layer belongs to `live-demo`;
  publishing a finished app belongs to `app-publishing`.

When the stack is genuinely undecided, read
[stack-selection.md](references/stack-selection.md). Keep upstream project
documentation as the source of truth for supported versions and hardware.

## Keep the decision record light

- Keep decisions inline for tryouts and tiny demos. Use
  `docs/architecture-brief.md` when a new app or re-architecture benefits from
  a durable record, never as a gate before an agreed first visible result.
- Record the outcome, chosen direction, provisional assumptions, risks, next
  probe, and allowed pivots. It is a living decision record, not a contract.
- Read [brief-template.md](references/brief-template.md) only when creating or
  revising that record. The
  [filled example](examples/architecture-brief-example.md) is illustrative,
  not a source of current compatibility facts.
- If no close app exists, read
  [scaffold-patterns.md](references/scaffold-patterns.md) and prune the starting
  shape to the first slice.
