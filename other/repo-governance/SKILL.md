---
name: repo-governance
description: Bootstrap or replicate battle-tested GitHub governance (Security/Quality/Workflow core Rulesets, an opt-in Review ruleset for Copilot code review + required conversation resolution — ADR-0021 in tarotene/dotfiles — consolidated CI with the `CI passed` aggregate, release automation, Renovate, git hooks, Justfile) into a Rust workspace (release-plz, MSRV-safe Renovate; telepath reference), a Typst/document repository (cliff.toml), or an Astro site (Biome/Vitest, cog.toml, release-please), picking the language profile rust / typst / astro-site. Use when asked to "撒く", "bootstrap governance", "apply rulesets", "apply GitHub settings", "set up release-plz", "set up release-please", "replicate telepath's CI setup", "seed CI to a new Rust repo", "seed CI to a new Typst repo", "seed CI to a new Astro repo", "rulesets / release / renovate をまとめて適用", "telepath の GitHub 設定を別リポジトリに持っていく", "Typst リポジトリに governance を播く", or "Astro サイトに governance を播く".
---

## What this Skill does

One procedure, three language profiles. The steps below are the same for every
profile; the parts that differ (parameters, `# ADJUST:` table, CI gates,
verification commands, browser flows) live in `reference/<profile>.md`. A
repository with none of the three profiles is the `core` type — see "Without a
language profile (`core`)" below.

1. Copies parameterised CI/CD templates and config files into the target
   repository, substituting `__PLACEHOLDER__` values for your repo's specifics.
   Every profile ships a consolidated `ci.yml` (every PR gate job plus the
   `CI passed` aggregate required check, ADR-591 in tarotene/dotfiles),
   `pr-title.yml`, a per-file language-mixing check `lang-mix.yml`, an
   ADR-number check `adr-number.yml` (ADR-380 in tarotene/dotfiles), CODEOWNERS,
   git hooks, `renovate.json` and the AGENTS.md/CLAUDE.md routing skeleton
   (ADR-0016 in tarotene/dotfiles). The profile decides the rest of the file
   set — see its "What this profile adds" section.
2. Applies repository merge settings (squash-only, delete-on-merge, wiki/projects
   disabled — same baseline `github-audit`'s `settings` domain judges, ADR-0015
   in tarotene/dotfiles) via `gh api`.
3. Creates the core GitHub Rulesets (Security / Quality / Workflow) that enforce
   branch protection, required status checks, and commit signatures. A fourth, Review, is **opt-in** (`--with-review`) —
   Copilot code review auto-request + required conversation resolution before
   merge. It is left out by default because forcing that review round trip on
   every commit of an early-stage or pre-release repository was judged
   excessive and noisy (ADR-0021 in tarotene/dotfiles). Opt in once the
   repository is past that phase, or strip it back out of an already-governed
   repository — remove `.github/rulesets/review.json` from the declaration,
   then `apply-rulesets.sh OWNER/REPO --delete-ruleset Review` (see "Removing
   the review layer" below).
4. Points you to the profile's `reference/manual-steps.md` for the steps that
   require browser flows (GitHub App, Pages, signing, registry set-up —
   depending on the profile).

---

## Step 0: Gather parameters

### Choose the profile

| Profile | Use for | Profile reference | Bundle directory |
|---------|---------|-------------------|------------------|
| `rust` | Rust workspace repository (the telepath reference implementation) | `reference/rust.md` | `~/.claude/skills/repo-governance/rust/` |
| `typst` | Typst / document repository (CV, slides, …) | `reference/typst.md` | `~/.claude/skills/repo-governance/typst/` |
| `astro-site` | Astro site repository | `reference/astro-site.md` | `~/.claude/skills/repo-governance/astro-site/` |

Read the profile reference for the chosen profile **before** running anything:
it lists the profile's extra parameters, the `seed.sh` flags they map to, and
the prerequisites. Below, `<profile>` means the bundle directory name above
(`rust`, `typst` or `astro-site`) and `<profile flags>` means the profile's own
required flags (for example `--canonical-crate`/`--cli-crate` for `rust`,
`--ats-email` for `typst`, `--package-name` for `astro-site`).

Where a static site is published depends on who may read it. The `astro-site`
profile publishes to GitHub Pages, which suits a public repository. For a
**private** repository whose site should be readable only by its owner and chosen
collaborators, publish a Cloudflare Worker behind Cloudflare Access instead:
`docs/agents/deploy-worker.md` in `tarotene/dotfiles` has the checklist, the
`wrangler.jsonc` and the workflow template, and the shared deploy action
(`.github/actions/deploy-worker`). GitHub Pages cannot limit its readers on a
personal account.

### Common parameters

Confirm the following values with the user (plus the profile's own):

| Parameter | Flag | Example |
|-----------|------|---------|
| GitHub owner | `--owner` | `acme` |
| Repository name | `--repo` | `my-lib` |
| Default branch | `--default-branch` | `main` (default) |
| Target repo path | `--dest` | `/home/user/src/my-lib` |
| Review layer? | `--with-review` | pass flag to also apply the Review ruleset (Copilot code review + required conversation resolution — ADR-0021). Ask whether the repository is past its early-development phase before defaulting this on. |

If any value is unclear, ask the user before proceeding.

Also check the prerequisites (common part; the profile adds its own tools):

```
gh auth status
command -v jq git
```

---

## Step 1: Dry-run preview

Run the profile's seed.sh with `--dry-run` so the user can review what will
change before any files are written or API calls are made:

```bash
~/.claude/skills/repo-governance/<profile>/scripts/seed.sh \
  --owner OWNER --repo REPO \
  <profile flags> \
  --dest /path/to/repo \
  --dry-run
```

Show the output to the user. Confirm they are happy to proceed.

---

## Step 2: Apply

Run without `--dry-run`:

```bash
~/.claude/skills/repo-governance/<profile>/scripts/seed.sh \
  --owner OWNER --repo REPO \
  <profile flags> \
  --dest /path/to/repo
```

Individual sub-scripts can be run independently (useful for re-runs):

```bash
# Copy files only (no GitHub API calls):
~/.claude/skills/repo-governance/<profile>/scripts/copy-files.sh \
  --owner OWNER --repo REPO <profile flags> \
  --dest /path/to/repo

# Create Rulesets only (files already copied — the generic apply script,
# not part of this skill, reads OWNER/REPO's own .github/rulesets/*.json;
# ADR-503):
apply-rulesets.sh OWNER/REPO --unverified-contexts

# Apply repo settings only:
~/.claude/skills/repo-governance/<profile>/scripts/apply-repo-settings.sh \
  --owner OWNER --repo REPO

# Wire git hooks only:
~/.claude/skills/repo-governance/<profile>/scripts/setup-hooks.sh \
  --dest /path/to/repo
```

---

## Without a language profile (`core`)

A repository that is none of Rust / Typst / Astro has no `<profile>` bundle and
no `seed.sh`. It is the `core` type: the language-independent baseline, taken
straight from `repo-governance-common` (the bundles above are that baseline plus
a language's files). This section is the canonical procedure for `core`;
`repo-charter` (new repositories, `create-repo.sh --type core`) and
`github-audit-triage` (drift fixes across repositories) refer to it instead of
restating it.

`create-repo.sh --type core` runs the first two commands below. They are also the
manual fallback when the script fails. Same order as every profile's `seed.sh`
(settings → files → rulesets). Skipping `apply-repo-settings.sh` leaves the
settings domain drifted (ADR-0013 Amendment 2026-09-29):

```bash
~/.claude/skills/repo-governance-common/scripts/apply-repo-settings.sh \
  --owner OWNER --repo REPO
~/.claude/skills/repo-governance-common/scripts/copy-files.sh \
  --owner OWNER --repo REPO --dest /path/to/repo
# commit + push, then:
apply-rulesets.sh OWNER/REPO --from-dir /path/to/repo/.github/rulesets --unverified-contexts
```

`copy-files.sh` also seeds a minimal `ci.yml` that has only the `CI passed`
aggregate job (an existing `ci.yml` is not overwritten). The rulesets declaration
requires `CI passed` and `PR title`, and `CI passed` is reported by `ci.yml`, so
**`ci.yml`, `CI passed` and the rulesets declaration go in the same stage.** If a
later stage carries `ci.yml`, the first PR waits about 22 minutes for `CI passed`
and then fails `rulesets-context-check`; if only the rulesets declaration is
dropped, `workflow-naming-check` fails with `ci-yml-missing` (#794, #815).

Because the minimal `ci.yml` has no gate job, `github-audit workflows rulesets`
reports `ci-gate-empty` for a `core` repository until a gate job is added
(`repo-charter` §9 says how to decide which).

Free-plan private repositories cannot apply rulesets; the declaration files are
still seeded for a later switch (`docs/agents/free-plan-declaration.md`).

---

## Step 3: Manual ADJUST checklist

After `seed.sh` completes, open each copied file and address every `# ADJUST:`
comment. The profile reference (`reference/<profile>.md`, section "Step 3")
lists the profile-specific locations. These rows are the same for every
profile and need no adjustment:

| File | What to update |
|------|----------------|
| `.github/workflows/pr-title.yml` | Nothing to adjust — calls tarotene/dotfiles' composite action (ADR-0031/ADR-591); the reported check context is simply this job's own `name: PR title`, no manual confirmation needed |
| `.github/workflows/close-linked-issues.yml` | Nothing to adjust — closes the issues a merged PR names with `Closes #N` even when the PR was stacked on a non-default base (GitHub only acts on the keyword for PRs targeting the default branch, tarotene/dotfiles#609); needs no secrets, only `issues: write` |
| `.github/workflows/kiriban.yml` | Nothing to adjust — celebrates an Issue / PR number that lands on a milestone (multiples of 100, 3+ digit repdigits, ±1 of a multiple of 1000) with a comment and the `kiriban` label, and opens a request issue for 1000-multiples and repdigits (docs/kiriban.md in tarotene/dotfiles); not a required check; needs no secrets, only `issues: write` and `pull-requests: write` |
| `.github/zizmor.yml` | Nothing to adjust — `"tarotene/*": ref-pin` covers the composite action's symbolic-ref `uses:` (#491); zizmor's own blanket default (hash-pin) still applies to every other `uses:` |

**Key invariant**: The `name:` field of each workflow job in `ci.yml`
**must exactly match** the entries in `ci-passed`'s `needs:` (job *id*, not
`name:`) — the Ruleset only ever requires `CI passed`/`PR title`
(ADR-591), so individual job `name:` values are display labels and no
longer need to match anything in `.github/rulesets/quality.json`.
`workflow-naming-check` (tarotene/dotfiles, a required check on every PR)
verifies this `needs:` coverage automatically.

**`pr-title.yml`** has no `workflow_call` concatenation to worry about
(ADR-591 replaced the old reusable-workflow form with a composite action,
docs/adr/591-ci-workflow-naming.md D3 in tarotene/dotfiles) — the reported
check context is simply this job's own `name: PR title`, pinned by the
`repo-governance-common/templates/.github/workflows/pr-title.yml` template
(each profile's copy is a symlink to it).

**Heavy jobs and stacked PRs (ADR-1005 D8).** Only the `rust` profile's
`ci.yml` carries a `stack-stage` job (see `reference/rust.md`); the `typst`
and `astro-site` templates have no job whose measured p75 is over 2 minutes.
If a job grows past that, copy the `stack-stage` job from the `rust` profile's
`ci.yml` template (it calls `tarotene/dotfiles/.github/actions/stack-stage@main`,
needs `permissions: pull-requests: read`), give the heavy job
`needs: stack-stage` and
`if: ${{ !cancelled() && needs.stack-stage.outputs.intermediate != 'true' }}`,
and add `stack-stage` to `ci-passed`'s `needs:`. Which jobs belong in `ci.yml`
at all is decided by the criteria in ADR-1005 D1 (a failing `main` would break
an invariant; not flaky; not dependent on external state or a shared queue; p75
under 10 minutes) — `github-audit gate-health` measures the last two.

---

## Step 4: Manual steps (browser flows)

Follow the profile's `~/.claude/skills/repo-governance/<profile>/reference/manual-steps.md`;
`reference/<profile>.md` (section "Step 4") summarises which flows it covers
for this profile. The shared Apps are documented once, in
`repo-governance-common/reference/releaser-app.md` and
`repo-governance-common/reference/renovate-app.md` (install the existing
shared App on the repository; do not create a new one).

---

## Step 5: Verification

### Local sanity
```bash
# Validate Ruleset JSONs
jq -e . ~/.claude/skills/repo-governance/<profile>/templates/.github/rulesets/*.json

# Check hooks are wired
git -C /path/to/repo config --local core.hooksPath
# → should print: .githooks
```

Then run the profile's own local checks (commit-message hook, build, test —
`reference/<profile>.md`, section "Step 5").

### After pushing the first PR

```bash
# Rulesets should appear:
gh api repos/OWNER/REPO/rulesets --jq '.[].name'
# → Security, Quality, Workflow (+ Review if seeded with --with-review)

# Required checks should be registered in Quality Ruleset:
gh api repos/OWNER/REPO/rulesets --jq '.[] | select(.name=="Quality") | .rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
# → CI passed
# → PR title

# Repo merge settings:
gh api repos/OWNER/REPO --jq '{allow_squash_merge, allow_merge_commit, allow_rebase_merge, delete_branch_on_merge}'
# → true / false / false / true
```

### Removing the review layer (ADR-0021)

Remove `.github/rulesets/review.json` from the repository first (the
declaration is the source of truth — ADR-503),
commit that, then run:

```bash
apply-rulesets.sh OWNER/REPO --delete-ruleset Review [--dry-run]
```

This refuses to run while `review.json` is still declared, so the order
above is enforced, not just recommended. It only handles the standalone
`Review` ruleset shape (each profile's own `review.json` layout) — it does not
recognize `copilot_code_review` or `required_review_thread_resolution: true`
bundled into some *other* active branch ruleset. An irregular layout like
that needs manual removal: `gh api repos/OWNER/REPO/rulesets/<id>` to
inspect, then a hand-built `PUT` with `copilot_code_review` dropped from
`rules` and `required_review_thread_resolution` set to `false` on every
`pull_request` rule (`crates/rulesets-write-guard` denies a raw `gh api`
write to this endpoint from a Claude session — run it yourself, or pass
`RULESETS_WRITE_GUARD_ALLOW=1` only when the human types it themselves with `!`; an
agent must not prefix it — auto mode rejects that as a safety bypass, and `apply-rulesets`
needs no prefix, #707).

### CI gates

The two required checks (`CI passed`, `PR title`) should turn green on the
first PR. `CI passed` aggregates every job in `ci.yml` via `needs:` — if one
of those individual jobs fails, `CI passed` fails with it, so check the
individual job's own logs (not the Ruleset context string) to diagnose a red
PR. The profile reference lists its jobs and the fixes for its usual failures
(`reference/<profile>.md`, section "Step 5").

---

## Template structure reference

```
~/.claude/skills/repo-governance/
├── SKILL.md                 ← this file (language-independent procedure)
├── reference/
│   ├── rust.md              profile: Rust workspace
│   ├── typst.md             profile: Typst / document
│   ├── astro-site.md        profile: Astro site
│   └── ci-failures.md       CI failure triage (distributed from repo-governance-common)
├── rust/  typst/  astro-site/   one self-contained bundle per profile
│   ├── templates/           files copied by copy-files.sh
│   │   └── .github/rulesets/  (declaration copied into the target repo — ADR-503)
│   │       ├── security.json  shared with repo-governance-common: deletion + non_fast_forward
│   │       ├── quality.json   signatures + linear history + the fixed pair
│   │       │                  CI passed/PR title (ADR-591); a symlink to
│   │       │                  repo-governance-common (astro-site: its own file,
│   │       │                  bypass_actors only)
│   │       ├── workflow.json  shared with repo-governance-common: squash-only (core)
│   │       └── review.json    shared with repo-governance-common: Copilot code review +
│   │                          required thread resolution (opt-in, --with-review only)
│   ├── scripts/
│   │   ├── seed.sh          main orchestrator — copy-files.sh, setup-hooks.sh,
│   │   │                    apply-repo-settings.sh, then the generic
│   │   │                    apply-rulesets.sh (not part of this skill;
│   │   │                    home-manager deploys it to ~/.local/bin)
│   │   ├── copy-files.sh    template + .github/rulesets/*.json copy, placeholder
│   │   │                    substitution, verify_declaration safety check
│   │   ├── apply-repo-settings.sh  gh api PATCH repo merge settings
│   │   └── setup-hooks.sh   git config core.hooksPath
│   └── reference/           the profile's runbooks (manual-steps.md, releasing.md, …)
```

The full per-profile file trees are in `reference/<profile>.md`
("Template structure reference").

## CI 障害の調査

CI の失敗を扱うときは `reference/ci-failures.md` を必ず読み、環境障害と実行済みテストの失敗を区別する。
