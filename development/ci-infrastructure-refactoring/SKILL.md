---
name: ci-infrastructure-refactoring
description: Use when refactoring how CI executes rather than what it checks — moving a gate between host and container, changing compose service orchestration, altering how a workflow invokes a make target, or adding a CI-only compose overlay. Covers the runner-only defect classes (bind mounts hiding installed dependencies, NODE_ENV leaking through exec, Compose health-check differences, root-owned artifacts) that code review cannot see.
---

# CI Infrastructure Refactoring

## Profile keys consumed

- `ci.provider`
- `ci.workflows`
- `make.lint_tsc`
- `make.start`
- `make.start_prod`
- `framework.package_manager`

## Overview

When a change alters the execution context of a gate, code review is structurally unable to catch
the defects: they live in bind-mount layering, inherited environment, Compose and image version
behaviour, and file ownership. The only reliable verification is running the change on the actual
runner, and the fastest route there is to push early and iterate.

## When to use

- Moving a gate between the dev container and the host, or introducing a mode switch for it.
- Adding or editing a compose overlay, a healthcheck, `depends_on`, or an `up --wait` call.
- Changing which service a workflow job starts, or how a job reaches the container.
- A gate is green locally and red on the runner with no code difference.
- Not for: adding a brand-new check (that is the
  [adding-ci-gates skill](../adding-ci-gates/SKILL.md)), or triaging one red check on an otherwise
  green pipeline (that is the
  [ci-single-check-validation skill](../ci-single-check-validation/SKILL.md)).

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — same compose/dev-container substrate, with a CI setup target plus
  ensure-container and wait-for-container targets around the service mapped by `make.start`, but no
  host/container mode switch; gates run in the container only.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — as described; an
  execution-mode variable selects `container` (default) or `host`, a host-stack variable
  additionally replaces the Docker production stack behind `make.start_prod`, and a CI-only compose
  overlay carries the runner differences.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  compose-based targets exist, but there is no CI setup target, no mode switch, and no CI overlay to
  refactor.

## The six runner-only defect classes

1. **A bind mount hides the image's dependencies.** Mounting the repository at the app path replaces
   the whole subtree, including the installed-dependency directory the image built. On a runner the
   checkout has none of its own, so the container ends up with no dependencies at all. The fix is an
   anonymous volume over that directory; note it is seeded from the image only when it is
   _created_, and carried forward on later `up`, so a lockfile change from
   `framework.package_manager` needs a reinstall or a renewed volume.
2. **Service environment leaks through `exec`.** `docker compose exec` inherits the service's
   `environment`, so pinning `NODE_ENV` there overrides the value each tool picks for itself and
   silently runs the test suite in the wrong mode. Leave it unset and let the dev server set its own
   in-process.
3. **Compose versions disagree about health checks.** `up --wait` fails outright on a service whose
   healthcheck is disabled on some Compose versions and not others. An overlay that replaces a
   port-based healthcheck must supply a trivial passing one, never disable it.
4. **A setup target and an ensure target fight.** If they compose different files, their config
   hashes differ and the second tears down the container the first created, so every job pays for a
   build it never uses. Keep the file set identical across both paths.
5. **A prerequisite defeats the escape hatch.** A make prerequisite that requires the Docker daemon
   does not disappear in host mode, so the host path fails before it starts. Guard prerequisites by
   mode, not just recipes.
6. **Container-written artifacts are root-owned.** Anything a generator writes inside the container
   blocks a later host-side step with a permissions error. Decide which side owns each generated
   path, and keep it there.

## Procedure

1. Make the execution context explicit and switchable rather than implicit in the recipe.
2. Never derive the switch from the ambient `CI` variable — `ci.provider` exports it into every
   step, so folding the two together silently moves pull-request jobs off the containers their gate
   definitions and visual baselines were produced in.
3. Exercise both paths locally before pushing. Run the target mapped by `make.lint_tsc` (skip with a
   recorded note when it maps to `null`) once per execution mode:

   ```bash # profile-example
   make lint-tsc
   EXEC_MODE=host make lint-tsc
   ```

4. Push early and read the first run of the workflows named by `ci.workflows`. Local green does not
   imply runner green; the runner is the only place these defects exist. Expect two or three
   iterations, each fixing one exposed defect.
5. Before declaring it done, confirm on the runner: dependencies resolve inside the container,
   service startup ordering holds under parallel jobs, no environment variable leaks into an exec'd
   tool, generated files are readable by whichever side consumes them next, and the prerequisite
   chain works in every supported mode.

## Common mistakes

- Treating a first-iteration runner failure as a flake — it is almost always environmental.
- Adding `|| true`, `set +e`, or `continue-on-error` so the job goes green — that removes the gate
  instead of fixing the context.
- Predicting environment differences instead of pushing and reading the run.
- Refactoring only the container path and leaving the host path untested, or the reverse.
- Changing the exec surface while moving PID 1: a CI overlay should change which process runs, not
  which binary the gate invokes.
