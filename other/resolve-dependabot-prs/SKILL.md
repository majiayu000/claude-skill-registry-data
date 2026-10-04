---
name: resolve-dependabot-prs
description: Resolve every open GitHub Dependabot pull request in the current repository with gh. Use when asked to triage, update, fix, merge, close, batch, consolidate, or regenerate lockfiles for Dependabot dependency PRs. Consolidate stable low-risk updates into one verified replacement PR per base branch, adapt code from official release notes and breaking changes, merge it, then close the superseded sources. Major, prerelease, non-SemVer, or uncertain updates remain isolated behind explicit approval.
disable-model-invocation: true
---

# Resolve Dependabot PRs

Resolve the complete open Dependabot set. Prefer one consolidated replacement
PR for all stable low-risk updates on the same base branch. Review official
release notes, make required compatibility changes, validate the final combined
tree once, merge it, and only then close its source PRs.

## Safety contract

- Use `gh` for every GitHub read or mutation and pass the verified repository
  explicitly. Use `git` only for isolated local work and exact branch pushes.
- Preserve user changes. If the main worktree is dirty, use a temporary clone or
  worktree; never stash, reset, force-push, delete branches, or weaken checks.
- Never update to a known prerelease.
- Keep Node on the latest stable LTS. Never introduce a non-LTS Node version.
- Merge stable patch/minor batches autonomously only after local and remote
  checks succeed. Respect branch protections; do not bypass them.
- Do not enqueue a multi-source replacement in a merge queue. Leave it open and
  report the protection blocker because source PRs can change while queued.
- Isolate major, non-SemVer, unknown, or uncertain updates and require explicit
  approval before remote mutation.
- Never close a source PR until the exact consolidated replacement merge is
  confirmed.
- Leave PRs open on auth, network, parser, evidence, compatibility, or validation
  uncertainty.

## Locate the runner

Resolve this loaded `SKILL.md` directory and use:

```text
<skill-dir>/scripts/dependabot_prs.py
```

Read the JSON schemas in `<skill-dir>/schemas/` before creating candidates,
plans, or state. Do not assume the loaded copy is under `.claude`; the skill is
also distributed to `.agents` for Codex and OpenCode.

## 1. Inventory the complete set

Read repository and nested `AGENTS.md` instructions, verify `gh auth status`,
then run:

```bash
workdir="$(mktemp -d)"  # outside the repository
python3 <skill-dir>/scripts/dependabot_prs.py inspect \
  --root "$(git rev-parse --show-toplevel)" \
  > "$workdir/inventory.json"
```

Stop without mutations when `complete` is false. Do not replace a failed
inventory with a manual partial PR list.

`inspect` emits one mechanically consolidable group per base branch for sources
whose versions parse as stable `patch` or `minor`. Major, prerelease, unknown,
non-SemVer, and parser-error sources remain separate. A grouped Dependabot PR
contributes one transition per `Updates ... from ... to ...` line; it joins the
batch only when every one of its transitions is stable `patch` or `minor`. The batch base is the
current branch head; any later base or source-head movement invalidates the plan.

## 2. Review releases and choose the safe batch

For every dependency in a consolidable group, read an official registry entry,
release, or changelog. Determine:

- whether the target is a stable release;
- deprecations, behavior changes, migrations, and breaking changes;
- runtime and peer dependency requirements;
- required source, configuration, Docker, CI, or lockstep dependency changes.

Record evidence for every target identity as
`ecosystem:canonical-name@target-version`. Use one of these summary forms:

```text
breaking=none; adaptation=not-required
breaking=none; adaptation=<required non-breaking change>
breaking=not-applicable; adaptation=not-required
breaking=applicable; adaptation=<implemented compatibility change>
```

Cover additional lockstep dependencies with the same evidence. The runner
checks coverage, identity, classification, summary shape, and digest format. The
agent remains responsible for selecting official sources, hashing the reviewed
content, faithfully summarizing it, and applying it to the tree.

Run installs, builds, and tests without GitHub, SSH-agent, or cloud credentials.
If private dependencies require credentials, stop and request separate
authorization.

Exclude a source from the candidate when its release is withdrawn, uncertain,
incompatible, or cannot be adapted safely. Keep it open with the exact blocker;
do not let it hold back the safe subset. Reject sources that target conflicting
versions of the same dependency in the same manifest.

## 3. Build one consolidated candidate

Use `replacement` mode whenever the candidate has multiple sources. Start from
the exact batch base SHA in an isolated clone/worktree, then:

1. Apply every selected stable version.
2. Update application code and configuration for all reviewed changes and
   breaking changes.
3. Add only officially justified lockstep dependencies.
4. Regenerate affected lockfiles with the repository package managers; never
   hand-edit generated locks.
5. Inspect the complete diff and remove unrelated changes.

Common lockfile commands include:

```bash
uv lock --directory backend
pnpm -C frontend install --lockfile-only
pnpm -C docs install --lockfile-only
```

After all updates and compatibility repairs are present, run one validation
matrix against the final tree. Derive the union of required checks from
`AGENTS.md`, nested instructions, and CI. For this repository, use as applicable:

```bash
just backend check
just backend check-migrations  # SQLAlchemy, Alembic, or database driver bumps
just backend test all
pnpm -C frontend verify
pnpm -C docs types:check
pnpm -C docs build
just template check
just agent-check
actionlint                      # github-actions bumps
uvx zizmor .github/workflows    # github-actions bumps
docker buildx build --target production -f backend/Dockerfile backend    # docker bumps
docker buildx build -f frontend/Dockerfile frontend                      # docker bumps
```

Do not run the complete suite once per dependency. If a check fails, repair the
candidate and rerun the affected final matrix. If a source stays risky, rebuild
and validate the candidate without it. Never skip or weaken a check to keep a
source in the batch.

Commit the final tree and record exact source heads, manifests, versions,
release evidence, compatibility rationale, validation commands, exit codes,
timestamps, commit SHA, and tree SHA in `candidate-v1`.

## 4. Create, verify, merge, and close the batch

Build the immutable plan:

```bash
python3 <skill-dir>/scripts/dependabot_prs.py plan \
  --inventory "$workdir/inventory.json" \
  --candidate "$workdir/candidate.json" \
  --output "$workdir/plan.json"
```

For `approval.kind: none`, publish and finalize without another prompt:

```bash
python3 <skill-dir>/scripts/dependabot_prs.py apply \
  --root "$repo" --candidate-root "$candidate_root" \
  --plan "$workdir/plan.json" --state "$workdir/<planDigest>.state.json" \
  --phase publish

python3 <skill-dir>/scripts/dependabot_prs.py apply \
  --root "$repo" --candidate-root "$candidate_root" \
  --plan "$workdir/plan.json" --state "$workdir/<planDigest>.state.json" \
  --phase finalize
```

The runner creates or safely updates one replacement PR containing every source
marker, version, adaptation, and validation command. `finalize` requires the
exact current plan/tree marker, waits for remote checks and protections, merges
the replacement, confirms its merge SHA, then comments and closes each source
idempotently. If merge confirmation fails, all source PRs stay open.

When correcting a published candidate, create a new plan. The runner may reuse
the same PR only for the exact repository, base branch, and source set, using a
fast-forward push and an idempotent body update bound to the new plan and tree.

## 5. Keep risky updates isolated

For `approval.kind: update-major`, do not run `apply`. Present the source PR and
head, versions and impact, official release/breaking evidence, candidate diff,
lockfiles, compatibility changes, validation results, destination, operations,
and exact approve/reject tokens. Ask one explicit approval question and wait.

Do not combine a major or uncertain update with the autonomous stable batch. A
rejection may close only the exact declined-major plan using the runner's parent
plan and rejection token. Other interpretive closures require their exact close
approval. Mechanically revalidated prereleases or merged replacements may close
autonomously under their schema predicates.

## 6. Reinspect and report

After every merge or closure, rerun `inspect`. Discard stale plans and continue
to a bounded fixed point of at most three discovery passes. Do not treat queued,
waiting, blocked, or awaiting approval as merged.

Report one row per observed source with dependency/version, impact, consolidated
replacement or isolated action, validation, merge SHA, final source state, and
the exact next action for anything unfinished. Clearly separate completed stable
work from risky updates awaiting approval.
