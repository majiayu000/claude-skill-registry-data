---
name: deploy-flow
kind: rule
law: delivery
description: Rule under the delivery law for a tree on GitHub — the part about the rollout. Load when an edit goes to production — merge into the main branch, the pipeline, images and tags, storage migrations. Patterns git-workflow-migration, -restart, -docker, -secrets. Task and branch — rule git-workflow.
---
<!-- rt-kit v0.34.0 · rules/deploy-flow.github.md · 2dff8b632999 · правится надстройкой, не здесь -->

# Rollout — how it works here

Rule under the law `docs/constitution/delivery.md` — the part of it about production. The law
says what must be true; here — by which technique it is held in a tree that lives on GitHub.
Working with the queue, the branch, the commit and the PR — the rule `git-workflow` under the
same law.

## What it is called here

| In the law                            | Here                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- |
| an edit reaching the main branch      | a PR merge; what starts the rollout — the merge or a manual run — is named by the companion next to it |
| the image of that commit              | `IMAGE_TAG=<sha>` in the `docker compose` commands on the server                                  |
| a storage change                      | a migration in `prisma/migrations/<метка>_<имя>/`                                                 |

## Where it lives

In this tree — the table in `implementation.md` next to it. Paths live there, not here: the rule
travels between repositories, the layout does not, and a path named in the rule lies in the
first tree that keeps its code differently.

## Flow

The flow of a rollout: what leaves for production, how the image is tagged and what is done with
the old ones.

```mermaid
flowchart TD
    A[Merge into the main branch] --> B{The edit touched code}
    B -->|No| C[Build steps are skipped by the sign of the edit's makeup]
    B -->|Yes| D[The image is built and tagged with the sha of that commit]
    D --> E{The storage changes with this edit}
    E -->|Yes| F[The migration chain was run from an empty storage before the merge]
    E -->|No| G[The image is rolled out by sha, not by the tag "latest"]
    F --> G
    G --> H[Old images are removed, the last three sha stay as rollback depth]
    H --> I{Production answers with what was rolled out}
    I -->|No| J[Rollout analysis: the restart goes by sha, not by the latest tag]
    I -->|Yes| K[The work queue audit reads the last run of the main branch]
    C --> K
    J --> K
```

## How the law applies here

- **The pipeline judges by the makeup of the edit and does not run everything in a row.** Steps
  with nothing to check are skipped by a sign computed from the main branch: a branch that touched
  no line of code raises no stand, takes no frames and builds no images. The sign is computed once
  and declared as a step output, not re-asked in every condition. A skipped step is visible in the
  run as skipped — one that silently dropped out reads as passed.
- **What starts the rollout is named by the tree, not by the rule.** In one tree production
  moves on a merge, in another on a manual run, and an unconditional statement here lies about the
  second: the rule enters the context of every session, and whoever reads it takes the merged as
  rolled out. Production hundreds of commits behind the main branch was read exactly that way, as
  an application breakage. The line stands in the companion next to it, together with the way to
  ask what is actually rolled out.
- **The rollout goes from the merge — environment variables, secrets and name records are set
  before it.** Path exclusions cover documents only. A tree with a manual run reads this article
  differently: there the border is the run itself, and the same is set before it.
- **The mode sign is declared in the image, not only in the production stack.** A value set by
  the stack acts only on a container raised by that stack; a manual run of the same image goes
  with an empty value, and empty here means localhost — with all the debugging defaults it allows.
  The image default is set in the image itself.
- **The production stack is raised on one's own machine before the merge, not after.** A built
  image says only that the build passed: the migrate step, the storage login, the startup order
  and whether every container has enough put inside are visible from one launch of the stack. On
  one's own machine that costs one command; on the node it costs a rollout that can no longer be
  cancelled — the migrate failure surfaces as a container log on the node. The same launch is made
  before a merge that lifts packages without a line of code changed: the stack passes an unset
  variable as an empty string, and a new package version may stop accepting what the old one took.
- **A variable read by several procedures is turned on first on a stand from the production
  build.** On the stand every reader passes; on production one edit says nothing about the
  neighbours, and a variable left empty there turns into addresses built from nothing.
- **The name production is served under is confirmed by a live answer of that name.** `curl -s -o
  /dev/null -w '%{http_code} %{redirect_url}\n' https://<name>/`: a redirect to a foreign address
  means the name is dead, and the rollout does not go by it. Three files of one epoch agree by
  common origin, not by being right. When a domain moves, the old name is searched across the whole
  tree, not only the paths of one's own part.
- **Data the screens need that migrations do not create is a step of the rollout.** A seed run once
  by hand heals one storage; a new or restored one stays empty, and a screen that shows an empty
  list for an empty answer looks the same as an unreachable server. The step runs on every rollout
  and is safe to repeat: found records are not overwritten. After the first rollout that depends on
  seeded data the count of records is read on production.
- **A move of the pipeline to another runner is closed by a search for the labels across all
  workflows.** A flow left on the host is named in the task with its reason. An order worded by a
  set — "all", "every" — is closed against the list of that set, not against the member that got in
  the way first. A rollout with production keys from a developer machine needs a separate word of
  the owner.
- **The epic plan is checked line by line against the pitfalls of the rollout step before the merge
  of the epic.** Every empty secret in the preparation script becomes a step "before the merge" or
  a decision of the owner, not a line "left to do".

- **The image carries every file its own startup steps read.** The storage schema, the client
  settings, the environment template — everything lying next to it in the repository does not get
  inside the image by itself, and the build answers only whether it built. The failure comes on the
  first startup, that is, already on the rolled-out one.
- **Images are rolled out by commit sha, not by the tag "latest".** The tag in the registry lags
  behind the main branch, and production silently falls back to the previous version while still
  answering.
- **The machine that builds the images cleans up after itself too.** The selection is the same on
  both — its own registry name, the last three sha, running containers stay — and it is called by
  one script: diverged, two cleanups would start leaving different things, and there is nothing to
  notice that by. They differ in the tail: the server then removes dangling layers and the build
  cache, the build machine keeps them, otherwise every build goes as the first. Cleanup on the
  build side does not wait for the merge: a branch image takes as much space, never leaves for the
  registry and is never a rollback point. The build step names its builder explicitly: without the
  name the build goes through the machine's current builder, which may have no cache limit, while
  the declared one stands empty. The build machine keeps the build cache and removes dangling
  images: the builder cache lies in its own volume, and dangling images are not part of it.
- **The rollout cleans up old images after itself, keeping the last three sha.** An image tagged
  with a sha is never dangling, and a dangling cleanup does not touch it: in half a year they eat
  the server disk whole. Three sha is the rollback depth, and fewer cannot be taken: a breakage
  noticed two rollouts later has nowhere left to roll back to.
- **A production breakage that has happened is analysed in a record, not by a fix alone.** The fix
  leaves as a branch, the task closes — and the reason the application stopped stays the knowledge
  of one executor. The record names what broke, how it became visible and why the fix fixes the
  cause and not the sign; it lies among the records of what has happened, and the directory is
  named by the companion of the wording rule.
- **An edit to the rollout itself is run before the merge, and "I will check after the merge" is
  never the executor's decision.** There is no other way to run it: it executes only where it
  rolls out. When there is no way to run it by hand either, that is said to the owner in words,
  together with what the check would cost, and the decision to postpone is theirs.
- **The description of production is edited together with the production stack.** The layout,
  the request path, the gates and the backups are described in texts outside the rules layers, and
  neither linter nor build reads them: the divergence piles up silently, and these texts are read
  as current. The pair is watched by the documents guard.
- **An edit to the pipeline is run before the merge with a manual run.** The rollout's
  `workflow_dispatch` starts it on any branch, while the rollout itself is pinned by a condition to
  the main branch: a run for the sake of checking reaches the builds and ends there. The trigger is
  registered by the main branch, so an edit that creates or moves it is not covered by a manual
  run. Running the step's commands on one's own machine does not cover it either: that checks the
  commands, not the pipeline file — the correctness of the file itself is read only from the list
  of runs after the push.
- **A PR is checked before the merge by the same pipeline as the main branch.** Checks and image
  builds go on the `pull_request` event, the rollout does not: it is held by the main-branch
  condition on its step, and a PR image does not leave for the registry.
- **Which PRs the pipeline wakes for is named by the tree, and it sets the order of handing in.**
  A base filter is not a detail of the settings: a PR the pipeline does not wake for has nothing
  to wait for, and a draft on it costs a locked button and an extra turn. A tree with a single
  runner pays a whole run for every PR into an epic branch, and pays it for checks the push gate
  has already run on the same machine; a tree with runners to spare buys the earlier refusal. The
  answer is written in the pipeline file next to the trigger, together with what is lost by it.
- **A package the tree's own applications install is released from a tip their end-to-end suites
  went green on.** Where the release pipeline runs none of these suites, a PR merged past the
  pipeline reaches them first after the release. When a PR without a green run of its own entered
  the main branch after the last green run of a PR merged into it, those suites must go green on
  the tip of the main branch before the release.
- **A divergence of production from the main branch is visible by the work queue audit.** A task
  leaves the queue by a merge, but a merge is not yet production: a failed or unstarted rollout
  touches neither the task nor its column, and there is nowhere to notice it. The audit asks for
  the last successful rollout and counts how far the main branch has gone from it. The main-branch
  run is no use for that: where the rollout is started by hand, a merge does not move production
  at all, and the run says nothing about it — production was 476 commits behind, and the audit was
  silent. A tree that has not named its rollout workflow gets no audit, and it says so out loud.
- **The migration chain is run from an empty storage before the merge.** The apply order is
  lexicographic by directory name, and the timestamp is set at creation: a migration from a branch
  started earlier lands before the one it depends on.
- **A migration without a reverse is merged only after a copy of the production storage, and the PR
  body names the copy.** Rolling back the image does not bring a dropped column or table back. When
  the executor cannot reach the server, the owner is told which step is blocked and what opens it:
  the owner's word replaces a check only when the owner was told the check did not run.
- **The divergence of migrations from the schema is measured on a shadow storage, not on the one
  the pusher works with.** That one lawfully carries the trace of any unfinished branch, and a
  check against it would hold up someone else's edit. The gate and the rollout call one and the
  same check — otherwise "matched" would mean different things in two places.
- **Skipping the schema audit is lawful while the branch has not touched the storage.** A stopped
  database is a state of the machine, not a reason to refuse a documentation push; but a branch
  that edited the schema or the migrations leaves for main blind without a chain run, and it is not
  the branch that falls but the rollout. In such a branch the check refuses and names how to bring
  the database up.
- **A failed rollout is visible by the work queue audit apart from lagging production.** A merge
  is not yet a rollout: a failed one leaves the main branch ahead of the server, and merges on top
  go the same way. The lag is counted from the last successful rollout and does not tell "not
  started" from "failed".

- **A check standing in the gate set refuses when it could not do its work.** "Nowhere to check"
  and "the check is broken" are different things: the first the tree names itself — no subject, no
  address set, the service not answering — and each such exit returns zero with its own line. The
  second — a missing package, an empty name in the settings, an unexpected exception — returns a
  non-zero code and says that the check itself broke, not the subject. A shared zero for both makes
  a broken check indistinguishable from a passed one: the schema-to-migrations audit stood like that
  in the gate set, checking nothing, and hid three causes at once behind its zero.

## What of the law is not here

**A merge into the main branch rolls nothing out to production.** `.github/workflows/deploy.yml`
has one trigger — `workflow_dispatch` — and the rollout is started by hand. Everything the rule
says about a merge as the start of a rollout does not apply to this tree: a merged edit reaches
production when someone presses the start, and not a minute earlier.

The price for this has already been paid. Production lagged the main branch by 476 commits, four
migrations of the cargo-analysis epic were never applied to it, and the columns the receiver
expected were physically absent from the tables. This read as a broken receiver — because the
rule promised production that travels by itself.

```bash
# what is actually rolled out: the last successful rollout and its commit
GH_TOKEN=$(cat ~/.config/rt-tools-bot-token) command gh run list \
    --workflow=deploy.yml --status=success --limit 1 --json headSha,createdAt
# by how much production lags the main branch
git rev-list --count <sha of the rollout>..origin/main
```

From here comes the boundary of the work queue audit too. It asks the last run of the main
branch, and a run of the main branch says nothing about production: a merge does not move it. The
divergence of 476 commits was exactly what the audit stayed silent about.

The state of production is invisible to a machine in the rest as well: whether production answers
with the build it rolled out nobody asks. This is held by whoever rolled it out.

The completeness of the registry cleanup is counted by nothing: the script keeps the last three
shas, and a miss in its selection shows only when the server's disk has run out.

## Patterns

- `git-workflow-migration` — editing the storage schema and its migrations.
- `git-workflow-restart` — a manual production restart.
- `git-workflow-docker` — images on one's own machine: the daemon, the registry, building for
  the server platform.
- `git-workflow-secrets` — keys of external services: where they live, how they are created,
  what their state says.
