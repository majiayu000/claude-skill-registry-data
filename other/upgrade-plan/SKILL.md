---
name: upgrade-plan
description: Plan a library or framework upgrade from the installed version to the latest. Finds what breaks, which local patches and workarounds can go, and what to adopt, sorted into must do, should do, and do later.
disable-model-invocation: true
argument-hint: "One or more packages, optionally pinned (laravel/framework, vite@7). Default target: latest stable"
allowed-tools: "Bash(composer why-not *) Bash(composer show *) Bash(composer audit) Bash(composer audit *) Bash(npm view *) Bash(npm ls *) Bash(npm audit) Bash(npm audit *) WebFetch WebSearch"
compatibility: "The version script needs jq and curl, and covers Composer and npm. Other ecosystems resolve the same facts by hand"
---

# Upgrade Plan

Plan the upgrade of one or more packages from the installed version to a target. The
output is one plan file. The run is **read-only**: it never edits a manifest or runs an
install, update, or require. Upgrading is the user's next move, with the plan in hand.

The lead (this skill) resolves versions, writes briefs, judges, and writes the plan.
Reading changelogs fans out to cheap collectors. Reading the codebase fans out to scouts.
The lead re-reads the official upgrade guide for every major version crossed, because
a breaking change the collector misses is the costliest miss.

## Steps

1. **Resolve.** Split `$ARGUMENTS` into packages, each with an optional `@target`. Map a
   loose name to the installed package (`laravel` → `laravel/framework`); if several
   match, ask which one. For each package, run `bash <skill-dir>/scripts/versions.sh
   <package> [target]` from the project root. It prints the installed version, the
   constraint, the latest version, the stable releases crossed, what the target requires,
   and the installed packages that depend on this one. In another ecosystem (pip, Cargo,
   Bundler, Go), read the same facts from the lockfile and the registry. A package
   already at its target leaves the run. *Done when* every package in the run has
   installed, target, releases crossed, requires, and dependents.
2. **Cascade.** Use the script output to find what else has to move:
   - A required or peer package whose installed version is outside the target's
     constraint. It must move.
   - A dependent whose constraint excludes the target. It must move to a release that
     allows the target. If no such release exists, it is a **blocker**: name the highest
     target it allows. For Composer, confirm with `composer why-not <package> <target>`
     (it also sees `replace`d packages that the script misses).
   - A companion that moves in lockstep (`react` + `react-dom` + `@types/react`, a
     framework's first-party packages, one scope's plugins).
   - A raised runtime (PHP, Node, an extension). This is a requirement item, not a package.

   Add each package that must move to the run, with its own target, and run step 1 on
   it. Repeat until nothing new appears. Past 8 packages, list the rest and ask which to
   include. *Done when* the run set is closed, and every blocker and runtime requirement
   is named.
3. **Collect and inventory.** Split each package's releases into spans: one per major
   line, and no more than 20 releases per span. Dispatch all of these **in parallel**:
   one collector per span, and one inventory scout per package. Each brief carries the
   run facts and the matching section of [BRIEFS.md](BRIEFS.md) (**Collector** or
   **Inventory**). In Claude Code with this plugin installed, use
   `subagent_type=leek-skills:release-notes-collector` and
   `leek-skills:upgrade-impact-scout`. In plain Claude Code, use `general-purpose` with
   `model: haiku` for collectors and `model: sonnet` for scouts. Elsewhere, use any
   sub-agent on the cheapest model for collectors and a mid-tier one for scouts, or run
   them inline one after another. While they run, fetch the official upgrade guide for
   each major version crossed, and run `composer audit` or `npm audit` for advisories
   against the installed versions. *Done when* every span has returned (send each
   `uncovered` list to one more collector), every package has an inventory, and every
   `breaking` change in each upgrade guide is an item, added by you if the collectors
   missed it.
4. **Match.** Split each package's items into batches of about 15. Dispatch one match
   scout per batch **in parallel** (same agent and fallbacks as step 3). Each brief
   carries the package's inventory and the **Match** section of BRIEFS.md. Then open
   every site behind a `hits`, `retires`, or `adopt` verdict yourself, and settle every
   `unsure`. *Done when* every item has a final verdict that you checked.
5. **Triage.** Put every item with a verdict other than `none` in exactly one bucket.
   Use the first rule that fits:
   - **Must do**: a blocker; a runtime or package requirement the project does not meet;
     a `breaking` hit; a `security` item that affects the installed version.
   - **Should do**: a `deprecation` hit; a `retires` (a patch, pin, override, or
     workaround that upstream made redundant: remove it and its comment); an `adopt`
     that deletes code or removes a known bug class; a `fix` for a bug the code works
     around.
   - **Do later**: any other `adopt`, such as a feature that improves the code or the
     user experience but needs design work, or a refactor whose payoff is small.

   Give each item a size: S (under an hour), M (a day), or L (more). *Done when* every
   non-`none` item has a bucket and a size, and the `none` items are counted.
6. **Write the plan** in the format in [PLAN-FORMAT.md](PLAN-FORMAT.md), at
   `.scratch/upgrades/<package-slug>-<from>-to-<to>.md` (the first package names the
   file). Fill its upgrade checklist with only the lines that apply to this project, with
   the exact commands. *Done when* the file exists and every bucket item cites a site and
   a source URL.
7. **Report** in 5–8 lines: the packages and their version jumps, any blockers, the count
   in each bucket, the three most important Must do items, and the plan path. Start each
   blocker line with ⚠️; no other marks.
