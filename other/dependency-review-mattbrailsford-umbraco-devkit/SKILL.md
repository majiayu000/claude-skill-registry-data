---
name: dependency-review
description: >-
  Reviews an Umbraco package repo's dependencies: bot update PRs, security alerts and
  outdated packages. Sorts each by kind and drafts one action per item (merge, close, hold
  or bump), plus fixes to dependabot.yml. Acts only with a yes. Use for "go through the
  Dependabot PRs", "can I merge this bump", "what's out of date", or tidying dependencies.
user-invocable: true
argument-hint: [PR number or URL, optional; reviews everything if empty]
---

# dependency-review

Dependabot doesn't know an Umbraco package runs inside a site that already has the CMS. It
opens PRs that would force a site onto a version its CMS wasn't tested with, and it labels
npm bumps "dev" or "prod" from `package.json`, which says little about what a backoffice
bundle ships. And on a repo with no Dependabot config, it only opens PRs for security fixes,
so ordinary updates never show up at all.

This skill looks at all three sources (bot PRs, security alerts, and newer versions with no
PR), sorts each dependency by what it really touches, and drafts what to do with it.

## Scope

- IN: open dependency update PRs from a bot (Dependabot, Renovate); open security alerts;
  newer versions of the project's dependencies; drafting merge/close/hold for PRs and
  bump/hold/leave for updates; drafting changes to `.github/dependabot.yml`.
- OUT: bumps a person opened (that's `pr-review`), moving to a new CMS major
  (`major-upgrade`), raising the package's CMS floor, and making a bump itself. A bump the
  user picks goes to `quick-fix`, which makes it and runs it past `reviewer`. A bump that
  needs code changes beyond the version gets held, with what broke, for the maintainer to
  route to `quick-fix` or the pipeline.

## Argument

`$ARGUMENTS` is a PR number or URL: review that one PR only (steps 1, 2, and 4 to 9, with
no updates to gather in step 5).

If empty, review everything: every open bot PR, every open alert, and every dependency with
a newer version, on every supported version line.

## Workflow

Read `umbraco-dependencies` first. Its three kinds and its floor rule drive every step below.
Until step 6, read everything from git, the lockfiles, and the package registries; don't
check out, install, or restore anything.

1. **Find the lines and their floors.** For one PR, the line is its `baseRefName`, if
   that's a supported line (see below). For a full
   review, it's every supported version line (`git-workflow`'s "Umbraco packages and
   version tracking", and the project's `CLAUDE.md`). If it's unclear which lines are still
   supported, check each line's CMS major against Umbraco's end-of-life dates and ask. A line
   in security-only support takes security fixes only: skip step 5 for it. For each line,
   read the floor as `umbraco-dependencies`' "Which CMS version: the floor" says,
   with `git show origin/<line>:<path>`.

   Also read how code reaches each line (`CLAUDE.md`, `CONTRIBUTING.md`, `git-workflow`). If
   a line only takes code through release or hotfix branches, a bot PR against it can't be
   merged as is: hold it, say which branch the change belongs on, and point the config's
   `target-branch` there (step 7).

   **Check the GitHub default branch is a supported line** (`gh repo view --json
   defaultBranchRef`). Dependabot's alerts, security PRs, and config all live on it. If it
   isn't a line (a stale integration branch, say), say so first: its PRs and alerts don't
   describe what ships, merging into it fixes nothing that ships, and every real line needs
   `target-branch`. Hold its PRs, check alerts against the real lines yourself, and leave
   the choice of default branch to the maintainer; it's a repo setting.

   In zsh, write placeholders in git paths as `"origin/${line}:${path}"`; a bare `$line:`
   is read as a modifier.

2. **Gather the bot PRs.**
   ```bash
   gh pr list --author app/dependabot --state open \
     --json number,title,baseRefName,headRefName,labels,createdAt
   ```
   For Renovate, use `--author app/renovate`. Read each with `gh pr view <n> --json
   title,body,files` and `gh pr diff <n>`. List every dependency it bumps, with the from and
   to version. A grouped PR bumps several; a lockfile-only PR (npm `package-lock.json` or
   NuGet `packages.lock.json`) may bump only a transitive dependency. A bot PR should touch
   only manifests (`package.json`, `Directory.Packages.props`, a `.csproj`'s
   `PackageReference` lines) and lockfiles. Anything else, or a `.csproj` change beyond a
   version, gets read by hand before going on (`pr-review` step 2 has why).

3. **Gather the open security alerts.**
   One line per package and lockfile: the alert numbers, the worst severity, and the
   version that fixes them all:
   ```bash
   gh api 'repos/{owner}/{repo}/dependabot/alerts?state=open' --paginate --slurp | jq -r '
     add | group_by([.dependency.package.name, .dependency.manifest_path])[]
     | "\(.[0].dependency.package.name)\t\(.[0].dependency.manifest_path)\t\(.[0].dependency.relationship)\talerts \([.[].number] | join(","))\t\(
         [.[].security_advisory.severity] | if index("critical") then "critical" elif index("high") then "high" elif index("medium") then "medium" else "low" end)\tfixed in \(
         [.[].security_vulnerability.first_patched_version.identifier // empty]
         | group_by(split(".")[0]) | map(sort_by(split(".") | map(tonumber? // 0)) | last)
         | join(", ") | if . == "" then "none" else . end)"'
   ```
   Match each to a PR from step 2. No `.github/dependabot.yml` means every Dependabot PR is
   a security update. An alert with no PR is an item of its own. To see why it has none,
   check recently closed bot PRs (`gh pr list --author app/dependabot --state closed
   --limit 30`): Dependabot doesn't reopen a closed PR for the same version, and their
   branches may still be on the remote, worth a note. GitHub's own
   runtime/development label on an alert reads `package.json`, like Dependabot's PR labels;
   sort it yourself in step 4.

   Match alerts to PRs by package name and the PR's diff, not its branch name: Dependabot
   updates a PR in place, and the branch keeps its first version in its name.

   One "fixed in" version per major: more than one means copies at different majors, each
   needing its own fix.

   Alerts only describe the default branch, so check every line for the same package.
   Check fixed alerts too (`?state=fixed`): a fix that landed on one branch in an earlier
   run may never have reached the others. A line can also carry a vulnerable version the
   default branch has already moved past, so it has no alert at all. For shipped
   dependencies, look each line's version up directly:
   ```bash
   gh api "/advisories?ecosystem=<nuget|npm>&affects=<name>@<version>" \
     --jq '.[] | "\(.ghsa_id) \(.severity) fixed in \(.vulnerabilities[0].first_patched_version)"'
   ```
   A package can sit at a different install path on each line, so match every copy:
   ```bash
   git show origin/<line>:<lockfile> | jq -r --arg d "<name>" '.packages | to_entries[]
     | select(.key | endswith("node_modules/" + $d)) | "\(.key) \(.value.version)"'
   ```
   For NuGet, read the line's `packages.lock.json` files the same way, or its requested
   versions if it has none.

   A closed security PR leaves its alert open for good, and an `ignore` entry doesn't close
   existing alerts either. Offer a dismissal where the alert can't be acted on from this
   repo, so the list keeps meaning something:
   - **Locked and not bundled:** `not_used`. The package never runs from this repo's
     output; sites get the fix through the CMS. If no CMS release has the fix yet, say so:
     the maintainer may prefer to hold it open as a reminder.
   - **Dev-only with no fixed version:** `tolerable_risk`, with what uses it.
   - **The alert doesn't apply** (the vulnerable code path isn't reachable): `inaccurate`,
     with why.

   Every alert number in the group gets the same reason:
   ```bash
   for n in <alert numbers>; do
     gh api -X PATCH "repos/{owner}/{repo}/dependabot/alerts/$n" -f state=dismissed \
       -f dismissed_reason=<reason> -f dismissed_comment="<why>"
   done
   ```

4. **Sort each dependency.** Use `umbraco-dependencies`' order: locked, then ships, then
   dev-only. Sort what the PRs bump and what the alerts name; for a full review, also every
   direct dependency on each line, from its `Directory.Packages.props` files, `.csproj`
   files, and each `package.json` outside `node_modules` (not `umbraco-package.json`).
   - For npm, check the bundle, not Dependabot's `dev`/`prod` label.
   - For a transitive dependency, find its parents in the lockfile ("Transitive
     dependencies") and sort by those.
   - A grouped PR takes the strictest kind among its bumps.
   - One package requested at different versions in different places on one line (a
     nested `Directory.Packages.props`, two workspaces) is one item per place, each sorted
     on its own: a test project tied to `Umbraco.Cms.Tests.Integration` can make it locked
     there and dev-only elsewhere.

5. **Gather updates with no PR** (full review only). Skip locked and sibling packages; they
   never move on their own. Skip the ones a step 2 PR already bumps. For the rest, start
   from what actually resolves: the version in `packages.lock.json` or the lowest requested
   version for NuGet, and the lockfile's resolved version for npm (a `^5.9.2` range may
   already resolve to 5.9.3). Then look up newer versions in the registry, without
   installing:
   ```bash
   # Newest stable overall, and newest stable in a major ("" for overall)
   newest='[.[] | select(test("-") | not) | select(startswith($m))]
     | sort_by(split(".") | map(tonumber? // 0)) | last'

   # NuGet
   curl -s "https://api.nuget.org/v3-flatcontainer/<id, lowercased>/index.json" |
     jq -r --arg m "<major>." ".versions | $newest"

   # npm
   npm view <name> versions --json | jq -r --arg m "<major>." "$newest"
   ```
   Registries don't always list versions in version order (a backport published late), so
   always sort. For a `0.x` package, pass the first two parts as the major (`0.3.`, or
   `0.0.57.`), so a breaking `0.x` step isn't counted as the same major. Skip pre-releases
   (anything with a `-`), unless the current version is itself a pre-release: then compare
   against later versions of any kind, and never offer one lower than the current. This
   sort orders pre-releases too:
   ```bash
   withpre='[.[] | select(startswith($m))] | sort_by(split("-") as [$v, $p]
     | ($v | split(".") | map(tonumber? // 0)), ($p // "~")) | last'
   ```
   `npm view <name> version` is the `latest` tag, which can be a pre-release, so don't use
   it for this. A package deprecated in favor of a new id (`xunit` to `xunit.v3`) won't show
   its successor here; nuget.org and `npm view <name> deprecated` name it.

   For a private feed in `NuGet.config`, find its flat container from the feed's service
   index (`curl -s <feed>/index.json | jq -r '.resources[] |
   select(."@type" == "PackageBaseAddress/3.0.0") | ."@id"'`) and use it in place of
   nuget.org's.

   Note each dependency with a newer version: current, newest in its major, newest overall.

6. **Decide each item.** `umbraco-dependencies`' "What each kind needs before a bump" table
   applies to PRs and updates alike. Per kind:
   - **Locked.** Never "newest": it should match the floor's version. A PR that raises it
     above the floor's version, or moves the floor itself, gets a drafted close comment
     saying which CMS release pins it. If it's a security fix, don't just close it: say
     where the fix has to come from (`umbraco-dependencies`' "A security fix in a locked
     dependency"), whether a CMS release has it yet, and offer hold or dismiss (step 3). A
     locked dependency already off the floor is an item too (`umbraco-dependencies`' "When
     the package is already off the floor").
   - **Ships.** Read the dependency's release notes or changelog between the two versions.
     For a family that releases daily, or a long run of releases, skim for "breaking",
     "removed", and "obsolete" rather than reading each one; if the notes can't be read at
     all, say so in the row and hold it. Then check that the new version doesn't pull a
     locked package above the floor's version: for a PR after restoring, for an update
     with no PR through `umbraco-dependencies`' nuspec lookup, walked down its dependency
     chain.
     For a PR, check its checks (`gh pr checks <n>`), then check it out (`git status`
     first, then `gh pr checkout <n>`), restore, and compare the resolved versions of locked
     packages against the floor's; for npm, check the bundle for a second copy of a shared
     library. Dispatch `reviewer` (Agent tool, `subagent_type: reviewer`) with the bump as
     the task, for its build, test, and consumer-impact checks. If checking out isn't
     possible (the tree isn't clean and the user won't stash), hold the PR as "not verified
     locally". A breaking change in the notes, a locked package pulled above the floor, or
     any reviewer finding means hold.
     An update with no PR is "bump" only for a patch or minor version whose notes show
     nothing breaking and that pulls nothing locked above the floor. A minor that fails
     either check is "hold", with why, for the maintainer to decide.

     **A new major of a shipped dependency waits for the package's next major release**,
     because consumers only expect breaking changes then. With no PR it's "leave"; a PR for
     it gets a drafted close comment saying so. `major-upgrade`'s "Third-party dependencies"
     step picks these up. The exception is a user who asks for it now: then it's a bump like
     any other, and the hand-off says it's a breaking change for consumers if the
     dependency's types appear in the package's public API.
   - **Dev-only.** Any version can move at any time, majors included: no site ever sees it.
     For a PR, check its checks. Patch and minor bumps with green checks are merge
     candidates. For an update with no PR, patch and minor versions are "bump", grouped
     into one bump per ecosystem. A major is its own row: read its breaking changes, and
     it's a bump (or a merge, for a PR) unless they need code or config changes, which make
     it a hold with what has to change.

     Tools that shape what gets published are the exception, at any version: versioning
     tools (Nerdbank.GitVersioning, MinVer) can change the computed package version, and a
     new analyzer release can add build errors. Hold those, and keep them in step with
     sibling repos and the CMS unless the maintainer says otherwise.

   A PR whose checks are failing or still running is never a merge candidate. Say which
   check, and hold it. Checks that ran on an older base still count if the base hasn't
   changed the same manifests or lockfiles since (`git diff --name-only $(git merge-base
   origin/<base> origin/<head>) origin/<base> -- '*package-lock.json' '*package.json'
   '*.props' '*.csproj' '*packages.lock.json'` lists any); if it has, the PR needs a rebase
   (`@dependabot rebase`, a comment that needs a yes like any other) before it's a
   candidate. If the repo lints commit messages, in CI or only in a local git hook, and the
   bot's message would fail it, say so: with merge commits, that message lands on trunk as
   written.

7. **Check the Dependabot config.** Read `.github/dependabot.yml` on the default branch.
   Draft the file, or the change to it, from `umbraco-dependencies`' "Dependabot". A new file
   ignores every locked dependency the project references, on every line. A change to an
   existing file adds the locked ones it misses, at least every one this run closed or left.
   Add dev-only grouping, and a commit prefix if the bot's messages break the repo's rules.
   Judge that from the bot's recent commits, not its defaults: with no config, Dependabot
   copies the style it sees in the repo's history, so its messages can drift. A full review
   that found many updates with no PR on a repo without the file is the strongest case for
   adding it.

8. **Show the plan and wait.** Up to three tables, each with what it bumps (from and to),
   the kind, the action, and the reason in a few words:
   - **Bot PRs:** merge / close / hold.
   - **Security alerts with no PR:** bump / override / dismiss / hold, and the lines that
     carry it.
     A fix no PR can deliver follows `umbraco-dependencies`' "A fix no PR can deliver".
   - **Updates with no PR:** bump / hold / leave. Keep this one short: group dev-only bumps
     per ecosystem, let one row name several lines when the change is the same on each, and
     list leaves only by name with their reason.

   Then a short list, one line each, of locked dependencies off the floor and second copies
   of a backoffice library in the bundle. These need the maintainer, not a bump.

   Then each drafted close comment, written following `plain-writing`, and the config draft.
   Ask before doing any of it. The user may say yes to some rows and not others.

   Several PRs that edit the same lockfile may conflict once the first merges. Order them,
   and say the rest may need Dependabot to rebase and re-run checks.

9. **Do only what was confirmed.**
   - **Merge** with the method the repo actually uses: read `git log --first-parent
     --oneline -20` on the base branch (merge commits, or squashed single commits). If it's
     unclear, ask. Never merge past failing or required checks, never with `--admin`. Merge
     one PR at a time when they share a lockfile, and re-check the next after its rebase.
   - **Dismiss** each confirmed alert with the drafted reason.
   - **Close** with `gh pr close <n> --comment "<drafted comment>"`. Dependabot won't reopen
     a closed PR for that version, but opens one for the next. The config change is what
     stops that.
   - **Bump or override.** Start `quick-fix` once per confirmed bump or override row and
     line, on that line, with the
     package, the from and to version, its kind, and what step 6 found (release notes,
     resolved locked versions to keep at the floor's). One grouped dev-only row is one
     `quick-fix`. Do them one at a time.
   - **Config change.** Commit it on a short-lived branch and open a PR, following
     `git-workflow`. Ask before committing to `main` or a version line.

## Rules

- Never merge, close, comment, bump, dismiss an alert, or push without a yes for that item.
- Never merge or bump a locked dependency above the floor's version, even with green checks.
  Green checks only prove it works on the CMS version CI builds against, not on the floor.
- Never edit the bot's branch to make a bump pass. That's a code change; hold it and say
  what broke.
- Return to the branch you started on when done.

## Hand off

Report: what was merged, closed, bumped, held, and left (with why), and whether the config PR
is open. For each held item, the one thing that needs a human decision. Then, one line each:

- Security fixes landed on one branch that supported version lines still need.
  Dependabot never opens security PRs against them; `change-backport` ports a merged fix.
- Locked dependencies found off the floor while sorting.
- Other version lines that carry a vulnerable version from an alert.

- **If another skill started this one**, return the plan (or what was done) and stop. That
  skill decides what runs next.
- Otherwise, if the config wasn't changed, suggest doing it now so the same PRs don't come
  back, and ordinary updates arrive as PRs instead of waiting for the next review.
