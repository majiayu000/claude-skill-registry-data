---
name: setup-rig
description: >-
  Shape a project's OpenRig team: pick a named shape (build, review, solo), choose each seat's
  runtime, and record the team spec in the project's engagement folder with its own history.
  Use for /setup-rig, "shape the team", "change the rig", or "which seats should this project
  have". Never starts or changes a running team.
disable-model-invocation: true
---

# Setup rig

A project's team is a spec, `engagements/<project>/rig.yaml`, outside the repository. This skill
writes that spec from a named shape with `rig-shape`, the platform command the `ai` menu also
uses, so every surface records the team the same way. The engagement folder is its own small Git
repository: every shape change is a commit, and `rig-shape history` shows them.

Only the owner, or Helm on the owner's word, shapes a team. A seat never reshapes the team it
sits in: the control, worker and review seats refuse this skill.

## Steps

1. **Resolve the project.** Use the project the owner named, or the repository this session is
   in. `rig-shape` takes its id, `owner/repo`, or its checkout path.
2. **Show the current team.** `rig-shape show <project>` and `rig-shape history <project>`. A
   project with no spec yet starts with the `build` shape.
3. **Offer the shapes.** `rig-shape list` prints each with its summary. Ask which fits the goal;
   `build` is the default. Prefer AskUserQuestion over free text.
   - `build`: control, a Codex overseer, and worker seats. The standard team.
   - `review`: control, two overseers on different providers, and worker seats. For risky goals.
   - `solo`: control and worker seats, no overseer. For small goals where the check is the review.
4. **Offer seat runtimes.** Each seat runs `claude-code` or `codex`. Keep the shape's defaults
   unless the owner wants a change; the overseer on a different provider from the workers is the
   point of review.
5. **Write it.** `rig-shape write <project> <shape> [--runtime <seat>=<runtime> ...]`. It checks the
   spec with OpenRig's own validator when `rig` is installed, refuses an invalid one, and commits
   it to the engagement folder's history. Report its line as it printed it.
6. **Say when it applies.** A running team keeps its shape. The new one takes effect the next time
   the team starts: `ai` → the project → This project's team, after Stop this team.

Pinning a seat to a specific account (`config_home`) is not part of a shape yet;
`integrations/openrig/README.md` has the manual steps.
