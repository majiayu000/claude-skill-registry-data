---
name: new-repo
description: >-
  Start a new project from zero: create a repository to the platform standard with
  `new-repo`, local by default or GitHub-backed on request, register it for the loop,
  then hand the goal to `intake`.
---

# new-repo

`new-repo` (on `PATH`; `bin/new-repo` in the platform) creates a repository from the platform's
templates: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the empty specification
(`docs/spec/SDD.md`, `TDD.md`, `SPEC-AMENDMENTS.md`), the decision template, `docs/tasks/`, the
hygiene and version scripts, and a Bun and TypeScript skeleton with its check. It commits on
`main`, tags `v0.1.0`, and leaves the checkout on `develop`.

## Procedure

1. **Ask only what changes the command:** the directory, whether it is
   the owner's own project (`--personal`) or professional work, and whether it needs GitHub now.
   Local is the default and needs no network; GitHub can be added later.
2. **Run** `new-repo <directory> --register [--personal] [--owner <login>]`.
   - `--owner` is required when `gh` is not logged in; locally it only names the repository in
     `repos.conf` (`<owner>/<name>`).
   - With `--github <owner>/<name> [--private|--public]` it also creates the GitHub repository,
     pushes both branches and applies the rulesets. That leaves the machine: confirm first, and
     never for a professional repository without the owner's word.
   - `--register` appends `<owner>/<name> <path> local|owner develop` to
     `~/.config/dev-platform/repos.conf`; `--personal` lists the path in `personal.conf`, which
     decides what the guard hook allows.
3. **Verify** from the new checkout: `git branch --show-current` is `develop`,
   `dev-loop status <owner>/<name>` resolves it, and `bun run check` passes when Bun is installed
   (the script says when it is not).
4. **Hand over** to `intake` with the owner's goal as the source. It writes the first decisions,
   the first requirements in the empty specification and the first tasks; `loop` then builds
   them.

The stack is fixed by the templates (Bun, TypeScript, ESLint, Prettier). A project on another
stack keeps the instruction, policy, specification and task files and replaces the rest in its
first change. `docs/runbooks/new-repo.md` has the GitHub settings that are done by hand.
