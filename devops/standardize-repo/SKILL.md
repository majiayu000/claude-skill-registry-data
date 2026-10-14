---
name: standardize-repo
description: >-
  Apply the harmon-init Copier template's conventions (DevOps tooling, CI/CD, lint,
  security, git hooks, Taskfile) to a repo. Use whenever the user wants to "apply
  harmon-init", "scaffold a new repo with my conventions", "set up a new project",
  "adopt the template", "bring this repo up to my standards", "standardize this repo",
  or "audit this repo against my standards / check what's missing". Covers three
  modes: scaffolding a brand-new/empty repo, retrofitting an existing repo with git
  history, and auditing a repo for drift from the standards. Trigger it even if the
  user doesn't say the word "skill".
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, WebFetch
---

# Standardize Repo (apply harmon-init conventions)

Bring a repo in line with the **harmon-init** Copier template — the shared baseline
of DevOps tooling, CI/CD, linting, secrets scanning, lefthook git hooks, and a
`Taskfile.yml` task runner. harmon-init is the **template** repo of harmon-platform
(siblings: harmon-devkit, harmon-infra); this skill is
how an agent *consumes* that template to scaffold new repos or standardize existing
ones. harmon-init is NOT an application — it is used via
[Copier](https://copier.readthedocs.io/en/stable/), so the heavy lifting is
`copier copy` / `copier update`, not hand-copying files.

## Credential boundary

Keep secret and credential-store writes human-only. Use read-only checks to confirm
that a credential is configured without revealing its value. If CI is blocked by a
missing credential, report the exact maintainer action; never create, rotate, delete,
or widen access to credentials, or weaken a workflow merely to make CI green.

## Preconditions

Verify these before doing anything; stop and tell the user if one is unmet.

- **copier** installed — `copier --version` (needs `>= 9.4.0`, per `_min_copier_version`).
- **harmon-init** cloned locally at `~/git/harmon-init` — required by **every**
  mode. If missing:
  `git clone https://github.com/evanharmon1/harmon-init ~/git/harmon-init`.
  The one exemption is narrow: audit mode's guarded drift helper
  (`assets/diff-template.sh`) snapshots the canonical remote itself and needs no
  checkout. The rest of audit mode — the catalog comparison, which is the bulk of
  the work — reads the checkout directly as `$TEMPLATE`, and it is the *only*
  source of truth for a never-templated repo, where the drift helper cannot run
  at all.
- **task** (go-task) on PATH — `task --version` — for the verification gate.
- **yq** on PATH — reads and freezes the `.copier-answers.yml` lineage tuple.
- **gh** authenticated (`gh auth status`) — `gh api` requires a credential even on
  public repositories, so this is needed for:
  - the GitHub side-effect steps (remote create, release init);
  - **update mode's legacy-baseline branch**, taken whenever the recorded
    `_commit` is tag-valued — it reads the GitHub release record;
  - the **Code Security capability check** before selecting CodeQL on a
    private/internal repo (`mode-update.md` §3, `mode-audit.md` drift class G) —
    this one applies regardless of lineage, including full-hash baselines.

  Plain local scaffolding does not need it, and neither does **audit mode's**
  legacy-baseline recovery — that path is `git`-only (`assets/diff-template.sh`
  resolves via `git ls-remote`, never `gh api`).

## Mode routing

Detect the situation, then follow the matching reference file end to end.

| Situation | Mode | Reference |
| --- | --- | --- |
| Target dir is empty / does not exist yet (new project) | **new-repo** | `references/mode-new-repo.md` |
| Target is an existing repo **with git history** (retrofit) | **adopt-existing** | `references/mode-adopt-existing.md` |
| Repo already generated from harmon-init (**v3+**, has `.copier-answers.yml`) and user wants the **latest template changes** ("update", "keep in sync", "pull latest harmon-init") | **update** | `references/mode-update.md` |
| User says "audit" / "check" / "what's missing" / "bring up to standard" / drift report | **audit** | `references/mode-audit.md` |

If it is ambiguous (e.g. a non-empty dir that is not a git repo), ask the user which
mode they want rather than guessing — `copier copy` vs `copier update` behave very
differently.

## Cardinal copier rules (read before running any copier command)

These are load-bearing. Full rationale and edge cases in `references/copier-gotchas.md`.

- **Production scaffolds use the canonical GitHub URL at a remote-verified
  release ref.** Select `HARMON_INIT_REF`, verify that exact tag against
  `origin`, peel it once to `HARMON_INIT_COMMIT`, and pass that immutable commit
  to Copier using the guarded commands in the applicable mode reference. **Then
  freeze the tuple: `--vcs-ref` does not survive into the answers file.** Copier
  derives `_commit` from `git describe --tags --always`, so a released tag lands
  in `.copier-answers.yml` instead of the peeled hash — discarding the immutable
  evidence the guard just established. Every mode that renders must promote
  `_src_path`/`_commit` to the canonical URL and `HARMON_INIT_COMMIT` afterward.
  Update
  mode must also resolve the recorded `_commit` once, require maintainer-approved
  recovery when legacy tag-only lineage lacks immutable evidence, and run every
  trusted render from a read-only offline clone through process-scoped Git URL
  rewrites.
  Prove the target descends from the resolved baseline before rendering. This
  records durable lineage that another machine can resolve without allowing a
  retag between validation and trusted template execution. A local-path
  `--vcs-ref=HEAD` render is only for a disposable
  preview/test of unreleased template work. Copier may represent dirty local work
  with a throwaway commit that does not exist on GitHub; never promote that render
  by rewriting only `_src_path`. The recorded `_src_path` and `_commit` are one
  lineage tuple: before changing a local path to the canonical URL, prove the
  recorded commit is reachable from that remote, or re-render/re-adopt from a
  released remote ref. An update must reject a non-canonical recorded source and
  pass the immutable commit derived from the remote-verified `HARMON_INIT_REF`
  so preview and apply cannot select different releases. See
  `copier-gotchas.md` gotchas 1 and 8.
- **Side-effectful answers default to `no`** in `copier.yml` (`github_remote_create`,
  `github_release_init`, `bunch_add`, `obsidian_project_add`, `run_task_install`).
  Leave them off unless the user explicitly asks; only flip them on with confirmation.
- **Run non-interactively** with `--data key=value` for known answers and
  `--defaults` for the rest, so runs are reproducible and CI-safe. Use `--trust`
  (the template has `_tasks`). Example shape:

  ```bash
  copier copy https://github.com/evanharmon1/harmon-init.git ./new-project \
    --vcs-ref="$HARMON_INIT_COMMIT" --trust \
    --data project_name="My Project" --data project_type=general --defaults
  ```

  This is only the command shape; run the release-tag validation and derive
  `HARMON_INIT_COMMIT` in `references/mode-new-repo.md` before executing it.

- **Confirm the resolved answers before any `--trust` run.** `--trust` executes
  the template's `_tasks`, so every non-interactive mode (update,
  adopt-existing, new-repo) first prints the complete resolved question →
  answer set with `assets/confirm-answers.sh` — `CHANGED` against the recorded
  `.copier-answers.yml`, `NEW` where nothing is recorded, `SENSITIVE` where the
  answer grants trust, names a principal, or fires a side effect — waits for
  explicit human approval, records it with `--confirm`, and gates the trusted
  run on `--check`. The asset never runs copier. In the interactive new-repo
  form copier's own prompts are that checkpoint. Claude Code auto-mode's
  classifier may deny `copier … --trust` outright (it also denies the
  `--skip-tasks` discovery renders): this checkpoint is where the user settles
  that — preferably by approving the single run at the prompt, or by adding a
  `Bash(copier update:*)` / `Bash(copier copy:*)` permission rule, knowing it
  is a standing, prefix-wide grant that also authorizes every later trusted
  copier run. **Agents never self-grant permissions**, and a parallel worker
  prints the set, stops, and returns it to the parent/human instead of
  confirming. Questions whose default is a Jinja expression (`code_owner`,
  `claude_authorized_members`) show as `UNRESOLVED` — the gate never renders —
  and a sensitive one must be stated explicitly before `--confirm` accepts.

- **Validate after every apply.** Re-running `copier` or changing answers can churn
  files — confirm the result with the verification step below before committing.
- **Optimize for regular rolling updates, not every historical migration path.**
  harmon-init-managed repositories are expected to stay near the current release.
  Review new answers against the target repository and pass the decisions
  explicitly. Do not add or expect permanent version-pair migrations for unusual
  gaps or customizations; reconcile those case by case in the downstream PR.

The asked questions live in `~/git/harmon-init/copier.yml` (e.g. `project_name`,
`project_slug`, `project_description`, `github_org`, `project_type`
[general / web-astro / web-app / iac / docs], `snyk_scan_schedule`
[off / weekly / daily], `include_terraform`, `include_ansible`, `ci_runner`,
`license`, `use_codeql`, `codeql_languages`, `use_release_please`, `devcontainer`,
`use_codex_review`, `use_codex_cloud_review`, `use_coderabbit`, `git_init`).
Read that file to
confirm names/choices/defaults before scaffolding — do not invent answers.

## Standards catalog

The authoritative, itemized list of what "standardized" means — every tool, config
file, Taskfile target, hook, and CI workflow the template provides, and how to check
each — is **`references/standards-catalog.md`**. The audit mode and any manual
retrofit work off that catalog. Treat the generated template output (and that
catalog) as the source of truth, not memory.

## Vendored skills

After **every** template apply or update — in new-repo, adopt-existing, update, or
audit remediation — complete this step before the repository gate. Follow the
**"Vendor shared agent skills"** item in harmon-init's `docs/CHECKLIST.md` for the
setup context; do not replace it with hand-copied skills, agents, or consumer-side
helpers. For vendoring and its checks, use only `task sync:skills`,
`task verify:skills`, `task verify:skills:offline`, and (in the in-sync case)
`git ls-remote --tags SOURCE_REPO`.

Read `.skills-sync.yaml` and its destination provenance. **If the manifest is
absent** — the repo opted out of skills sync (e.g. `use_skills_sync=false`, as
general and IaC scaffolds and skills-source repos may) — there is nothing to
vendor: record `Vendored skills: not configured` in the summary and skip the rest
of this step. Otherwise report one of these states and take only its matching
action:

1. **Never vendored.** The manifest exists but the skills destination has no
   `# managed:` provenance line — or, when the manifest has an `agents:` block,
   its agents destination has none. **Ask for an explicit yes before doing
   anything.** Name both consequences of that yes: `verify:skills` will become live
   in `task ci` and the CI lint job; and the vendored `gauntlet` and `shepherd` will
   become the Dev Loop procedure under `AGENTS.md`. Only after an explicit yes, run:

   ```bash
   task sync:skills
   task verify:skills
   task verify:skills:offline
   ```

   Commit the materialized result in the same standardize PR as
   `chore(skills): vendor harmon-devkit REF (CATEGORIES)`.

2. **Pin moved.** Provenance is present, but `task verify:skills:offline` fails
   because the manifest pin and vendored ref differ (normally a Renovate pin bump).
   Do not change the pin again; materialize the existing requested pin and run:

   ```bash
   task sync:skills
   task verify:skills
   task verify:skills:offline
   ```

   Commit that refresh in the same standardize PR as
   `chore(skills): refresh harmon-devkit OLD to NEW`.

3. **In sync.** Provenance is present and the offline verification passes. Run:

   ```bash
   git ls-remote --tags SOURCE_REPO
   ```

   If it shows a release newer than the pin, report it and offer to bump the pin,
   sync, and commit the refresh. Default to **no**: Renovate owns the bump, and a
   version pin must never move silently.

Vendored skills and agents produced by this step **ride in the standardize PR**.
They are part of its deliverable, not scratch output to discard or split into a
separate PR. In the final summary, state `Vendored skills: <never vendored | pin
moved | in sync> — <what you did>`.

## Verification

Complete the **Vendored skills** step above before running the repository gate.

After applying any mode, run the bundled check:

```bash
assets/verify-applied.sh <target-repo-dir>
```

It confirms the expected files/tooling landed and then runs the repo's own gate
(`task verify` = the repo's fast check/build/validate/guard set; `task check` for lint only;
`task install:hooks` to wire lefthook). Report what passed and surface any gaps
against `references/standards-catalog.md`. Never bypass hooks (`--no-verify` is
prohibited); commit on a feature branch — no direct commits to `main`.

**Gate the staged rollout against the target policy.** Before publication, read
the generated target's `AGENTS.md`. Use the draft-workbench lifecycle only when
that authoritative file defines draft publication and ready-for-review as the
human handoff. If it still defines an ordinary PR or stop-at-green handoff, the
selected harmon-init release predates this lifecycle. Do not let a newer
vendored `integrate` (or `shepherd`, in a target that has not yet migrated)
override it: select a compatible harmon-init release, or
follow the target policy and report that lifecycle adoption remains blocked.
When `.coderabbit.yaml` is present, also require
`reviews.auto_review.drafts: true` before relying on CodeRabbit as a gate; an
older generated `false` value is the same upgrade blocker, not permission to
promote early.

On a compatible target, open a draft PR. When the target has a vendored
`integrate` (or `shepherd`, in a target that has not yet migrated) skill,
follow that procedure through its complete
draft-time checks/review gate and final promotion.

If the target has no vendored `integrate`/`shepherd` skill, use this fallback instead: keep the PR
draft while work is active; after each push, bounded-poll every required check
to a terminal result and inspect reviews, top-level comments, and every inline
thread. Settle every finding and deferred PR-body checkbox, run the target's
full local gate on the exact clean commit before each fix push, and repeat until
the unchanged head is clean. Use the shepherd-round cap in the target's policy,
or four rounds when it states none: one fix push or one no-change adjudication
cycle is a round. Stop early when the sole blocker survives two consecutive
rounds unchanged, or immediately for a permission, secret, external-service, or
maintainer-decision blocker; every non-success stop remains draft.

Before promotion, establish that every required workflow and review app runs on
drafts or was explicitly dispatched and settled on the exact head. Treat
automation available only through `pull_request.ready_for_review` as a
configuration blocker: ready can notify human reviewers immediately and is not
a reversible automation probe. Freeze one final snapshot of the head, draft
state, checks, reviews, mergeability, deferred findings, and unanswered threads.
For the content half of that snapshot, use the `integrate` skill's readiness-gate
script (`integrate/assets/readiness-gate.sh`, per `integrate/SKILL.md` §6 — or
the equivalent `shepherd/assets/readiness-gate.sh` per `shepherd/SKILL.md` §6
in a target that has not yet migrated —
`check` prints the fingerprint on a pass, `fingerprint` recomputes it after
promotion) whenever that skill
is installed alongside this one — one implementation, not a re-derivation. When it is
not (this fallback exists precisely for targets without a vendored
`integrate`/`shepherd` skill,
and this skill can be installed without it), construct the fingerprint to the
same contract, which is stated here in full because the file may be absent:
fetch each component (PR title/body, reviews, top-level comments, inline
comments, GraphQL thread resolution) into a checked capture and abort on any
non-zero exit — never pipe unchecked `gh` calls into a hash, which turns a
failed fetch into a stable hash of the components that survived; pipe
`--slurp` output to a standalone `jq` (`gh api` refuses `--slurp` with
`--jq`, and `--slurp` is what makes `--paginate` page-safe); hash
content-bearing fields only (IDs, authors, bodies, comment `updated_at`,
review states and `submitted_at`, thread `isResolved`), in stable order
(`sort_by(.id)`), excluding the PR's own `updated_at` and the draft flag,
which promotion itself mutates. A locally constructed fingerprint is only
ever compared against itself within this session — pre-promotion against
post-promotion — so satisfying the contract, not byte-identity with the
integrate skill's own recipe's hash, is what correctness requires. A failed component
means the fingerprint is unknown, and unknown cannot promote: the PR stays
draft.
Promote that head with `gh pr ready`, confirm it is still the same open head and
is no longer draft, then stop. Reconcile the remote state even if promotion or
confirmation fails; if an open PR is ready on an unverified head, run
`gh pr ready --undo` and confirm it is draft before resuming or stopping. Never
merge, and never report the human handoff from a failed or indeterminate gate.

At both stages, watch every required check to a terminal green result and inspect
every review thread.
Apply feedback you agree with and reply with a concrete repository-specific
rationale when you disagree. Never merge; promote only the unchanged clean draft.
Report the human handoff only after the final ready promotion is confirmed.
