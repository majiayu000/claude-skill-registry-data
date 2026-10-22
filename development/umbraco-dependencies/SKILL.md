---
name: umbraco-dependencies
description: >-
  Sorts an Umbraco package's NuGet and npm dependencies into locked to the CMS, shipped to
  sites, and dev-only, and says what each kind needs: which version, how sibling packages
  pin each other, and Dependabot rules. Use when adding, bumping or importing a dependency
  (including writing client code that imports Lit, UUI or RxJS), referencing a sibling
  package, judging an update PR, writing dependabot.yml, or matching dependencies
  to a new CMS version.

---

# Umbraco package dependencies

An Umbraco package doesn't run on its own. It runs inside a site that already has the CMS and
everything the CMS depends on. So a package's dependencies aren't all equal: some must match
the CMS, some reach every site that installs the package, and some never leave the repo.

Sort every dependency into one of three kinds, in this order. The first that fits wins.

1. **Locked to the CMS.** A site gets it from the CMS too. The CMS decides its version.
2. **Ships to sites.** It reaches a site when the package is installed: as a NuGet
   dependency, or as code inside the backoffice bundle.
3. **Dev-only.** Tests, build tools, analyzers, the demo site, and CI. No site ever sees it.

Locked only matters where the dependency runs next to the CMS. A test dependency that runs
against the CMS (a CMS test helper, NuGet or npm) is dev-only and locked, and locked wins:
it still has to match the CMS. A test project that only uses the CMS's packages for types is
dev-only, whatever its lockfile holds.

## Which CMS version: the floor

A locked dependency matches the CMS release the package's support **starts at**: its floor.
Not the newest CMS release.

Read the floor from the lowest `Umbraco.Cms.*` lower bound across the projects that ship.
Other packages under the `Umbraco.Cms.` prefix, like `Umbraco.Cms.Search.*`, are separate
products with their own versions. If the reference is a range, the floor is its lower
bound: `[18.0.0, 18.999.999)` means 18.0.0. With branch-per-major (`git-workflow`'s
"Umbraco packages and version tracking"), each line has its own floor.

`@umbraco-cms/backoffice` should resolve to the same floor: check both the range in each
client's `package.json` and the version the lockfile actually resolved, since a `^18.0.0`
range can sit at 18.0.0 for a long time. If it's lower, the client builds against APIs older
than the CMS it runs on; if higher, it uses APIs sites on the floor don't have. More than one
resolved copy in one workspace is a finding too. Flag each one.

Say a package's floor is CMS 17.0, and CMS 17.3 moved EF Core from 10.0.0 to 10.0.3. If the
package asks for 10.0.3, every site still on 17.0 to 17.2 gets forced onto an EF Core
version their CMS was never tested with. So the package stays on 10.0.0 until its own floor
moves.

Moving the floor itself (bumping `Umbraco.Cms.*`) raises the lowest CMS version every user
must run. That's a release decision for the maintainer, never a routine bump. A new major is
`major-upgrade`'s job.

### More than one floor

Everything here applies to any product the package builds on, not only the CMS. A package
that extends another Umbraco product has a floor for each:

- **Each product's floor** is the lower bound of that product's package, read the same way.
- **The CMS floor** may come only through another product. Read it from that product's
  nuspec at its floor (the nuspec lookup under "Locked to the CMS"). If the package
  references the CMS too, the higher of the two lower bounds is the real floor.
- **Each product locks what it pins.** Run the locked check against every product's
  dependency graph, not only the CMS's. A product's own npm package is locked like
  `@umbraco-cms/backoffice` if the package extends that product's backoffice.

### Exact versions and ranges

With an exact version (`10.0.0`), a NuGet reference is a minimum: sites resolve that version
or higher. With a range (`[10.0.0, 10.999.999)`), the lower bound is the minimum. Either way
the rule is about the **lowest version the package asks for**: it must not be above the
floor's. A "bump" means raising that lowest version.

## Locked to the CMS

### NuGet

A package is locked when a site gets it from the CMS. Most are in `Directory.Packages.props`
at the root of the CMS repo, at the floor's tag (`umbraco-cms-source`). Three catches:

- **That file also lists the CMS's own build tools** (versioning, code style, and schema
  tools). Those don't reach sites, so they're not locked; sort them as dev-only.
- **Some versions are set elsewhere.** A few are pinned inline in a `.csproj`.
- **Test helper versions live in `tests/Directory.Packages.props`** in the CMS repo. A
  locked test helper like `Umbraco.Cms.Tests.Integration` brings its own test framework
  (NUnit, `Microsoft.NET.Test.Sdk`), and those must match it too, so they're locked as well,
  in the test projects that use it. Only what the helper itself depends on (its nuspec)
  counts, not everything else in that file.

To settle a package either way, look for it in the CMS's shipped projects at the floor's
tag. A reference without `PrivateAssets="all"` reaches sites, so it's locked. Leave out the
CMS's own dev site (`src/Umbraco.Web.UI`) and `templates/`, whose versions are placeholders:

```bash
git -C "$CMS" grep -n 'PackageReference Include="<name>"' <tag> -- \
  'src/**/*.csproj' ':(exclude)src/Umbraco.Web.UI/**'
```

Two more cases are locked even with no hit:

- **A package that releases in step with a locked one,** or pins the same version of a
  family the CMS pins: EF Core Design next to EF Core, for example.
- **Part of the .NET shared frameworks.** The site's .NET runtime supplies everything in
  `Microsoft.NETCore.App` and `Microsoft.AspNetCore.App`. Use the patch version the CMS uses
  for its other `Microsoft.*` packages at the floor, never a newer one. An old package id
  the framework now covers, with no current version to match, should go: suggest removing
  the reference.

Typical locked packages:

- `Umbraco.Cms.*`, and other Umbraco products the package builds on ("More than one
  floor").
- EF Core and its providers (`Microsoft.EntityFrameworkCore.*`), and `Microsoft.Data.Sqlite`.
- The `Microsoft.Extensions.*` and `Microsoft.AspNetCore.*` packages the CMS lists. Only
  those: a shared name prefix doesn't make a package locked (`Microsoft.Extensions.AI`
  isn't part of the CMS).
- Other Umbraco packages that version with the CMS major, even outside `Umbraco.Cms.*`.
- Anything else in the CMS's runtime graph.

A shared package the CMS's file doesn't list comes in through one that it does. Find its
version from a project that references only the CMS at the floor
(`dotnet list package --include-transitive`, after a restore), or without restoring, walk
the nuspecs: start from the CMS packages the project references and its other locked
dependencies, and read each one's dependencies a level down:

```bash
curl -s "https://api.nuget.org/v3-flatcontainer/<id>/<version>/<id>.nuspec" |
  grep -o '<dependency id="[^"]*" version="[^"]*"'   # id and version lowercased in the URL
```

Packages the repo publishes itself (sibling products in one repo that depend on each other,
NuGet or npm) aren't locked to the CMS, but they don't move on a bot's schedule either: the
repo's own release sets their versions. Treat them like locked ones for Dependabot.

### Sibling packages: exact pin or range

How one of the repo's own packages references another depends on how they release:

- **Released together** (one version, one commit, one release; a product split into
  `Core`, `Web`, and a meta-package, say): pin exactly, `[X.Y.Z]` in NuGet, `X.Y.Z` with no
  `^` or `~` in npm. They're one product, so there's never a reason for them to resolve to
  different versions. With a floor instead, another dependency can pull one sibling up while
  the rest stay put: new server code next to old backoffice files, and no restore warning,
  because no single rule was broken.
- **Released on their own schedule** (separate products that happen to share a repo): use a
  range, like any other shipped dependency ("Exact versions and ranges").

A `ProjectReference` between NuGet siblings packs as a floor (`X` means `X` or higher), and
no MSBuild or NuGet setting makes it pack exactly. A `PackageReference` to the sibling
doesn't work either when both pack in one `dotnet pack`: the sibling's `.nupkg` doesn't
exist yet at restore. Keep the `ProjectReference`, and add a build step after `dotnet pack`
that rewrites each sibling dependency in the packed `.nuspec` from `version="X"` to
`version="[X]"`. The version itself is already right; only its form changes.

### npm

This section is for a backoffice extension. A client with no `@umbraco-cms/backoffice`
dependency (a script for the public site, say) has nothing locked here.

`@umbraco-cms/backoffice` is locked to the floor. So is every library it provides at
runtime: Lit, UUI, RxJS, and others. The published
package declares them all as `peerDependencies`, so the project's own lockfile has the
list, whether or not the client lists any of them. Leave out the build-time entries in it
(`@hey-api/openapi-ts`, `@types/*`); those are dev-only:

```bash
jq -r '.packages["node_modules/@umbraco-cms/backoffice"].peerDependencies // {} | keys[]' package-lock.json
```

For the version a library is at in a given CMS release, read the CMS repo's lockfiles at
the floor's tag. Most are in `src/Umbraco.Web.UI.Client/package-lock.json`, but some sit
under a nested package's `node_modules`, so take the entry nearest the package that uses it.

What matters is how the client imports them. A bare import (`from "lit"`, `from "rxjs"`)
bundles a second copy unless the Vite `external` list covers it, and two copies of Lit or
UUI at runtime break custom elements in ways the build never shows. `npm ls` can show one
copy in `node_modules` while the bundle still carries its own. Check instead:

1. Grep the client's `src/` for bare imports of each library on the peer list, including
   subpaths (`from "lit/directives/keyed.js"`, `from "rxjs/operators"`).
2. Compare against the Vite `external` list. An external must be a path the backoffice's
   import map provides: a regex like `/^@umbraco/` also externalises anything else that
   matches, and an import the map doesn't cover fails in the browser instead.
3. Fix by importing from the backoffice path that exposes it. Most are
   `@umbraco-cms/backoffice/external/<library>`, but not all; the `exports` map in the
   backoffice's `package.json` lists every path (`umbraco-backoffice-conventions`' "Build
   output").

### A security fix in a locked dependency

A vulnerable version of a locked dependency reaches sites through the CMS, not through the
package. Bumping it in the package alone forces the version on every site, as above. The fix
belongs in a CMS patch release. Tell the maintainer, with the advisory, so they can decide
whether to wait for the CMS or raise the package's floor once the CMS ships the fix.

### Analyzers and source generators the package ships

An analyzer or source generator the package publishes runs in the consumer's compiler, not
on the site. Its compiler packages (`Microsoft.CodeAnalysis.*`) aren't locked to the CMS,
but they set the lowest SDK anyone referencing the package can build with. Keep them at or
below what the floor's .NET SDK ships, and treat a bump as the maintainer's call.

### When the package is already off the floor

Projects drift: a locked dependency raised "to pick up fixes", or one left below the CMS
after the floor moved. Don't fix it silently in an unrelated change. Report each one with
the floor's version, so the maintainer can decide. Only report what reaches a site or a test
run: an npm peer that sits in the lockfile but isn't imported or bundled never runs, so its
version doesn't matter.

Not every locked package carries the same risk above the floor. EF Core is the sharpest:
a provider or design-time package out of step with the CMS's EF Core fails at runtime
(`TypeLoadException`, `MissingMethodException`). A patch-level `Microsoft.Extensions.*`
difference is usually harmless, but it's still a version the CMS wasn't tested with.

## Ships to sites or dev-only

### NuGet

Check where the package is **used**, not where it's declared. With central package management,
every version lives in `Directory.Packages.props`, whatever it's used for, and there may be
more than one such file (a nested one in `tests/` applies to everything under it).

- **Ships:** a `PackageReference` in a project that packs into a published NuGet package,
  without `PrivateAssets="all"`. Sites restore it. If other packages build on this one,
  its shipped dependencies become theirs too, so raising one raises it for them.
- **Dev-only:**
  - References in test projects, the demo site, and anything with
    `<IsPackable>false</IsPackable>` (set in the `.csproj` or a `Directory.Build.props`).
  - References with `PrivateAssets="all"`: analyzers, source generators, SourceLink,
    versioning tools (MinVer, Nerdbank.GitVersioning).
  - `GlobalPackageReference` entries (always private).
  - Local tools in `.config/dotnet-tools.json`.

A version in `Directory.Packages.props` that no project uses is noise that still gets bot
PRs: report it for removal. A project that opts out of central package management, or uses
`packages.config`, keeps its versions in its own files; sort them the same way, or exclude a
project nothing builds any more.

A shipped package can still drag a locked one above the floor, through its own
dependencies. Restore doesn't warn when a
dependency pulls a version **up**; `NU1605` only fires when the project itself asks for less
than something else needs. Check the resolved versions instead: `packages.lock.json` if the
project has one, or `dotnet list package --include-transitive`, against the floor's versions.

### npm

Sites never run `npm install` on a backoffice package. They get the built bundle. So
`dependencies` and `devDependencies` in `package.json` don't decide what ships; the bundle
does.

- **Ships:** a library the client's source imports at runtime that isn't external in the
  Vite config. It gets bundled, even if it's listed under `devDependencies`. Check with a
  grep of `src/` for imports of the package name.
- **Dev-only:** build tools (Vite, TypeScript, ESLint), type packages (`@types/*`), test
  runners, code generators (`@hey-api/openapi-ts`), and anything only a config file or script
  uses. Also anything external, which the backoffice provides at runtime.

If the client also publishes to npm (often a types package, so other extensions can build on
it), its `dependencies` reach those extension developers. Treat them as shipped too.

A client that isn't a backoffice extension (a script the package adds to the public site)
works the same way: what's bundled ships, and here it reaches site visitors'
browsers, not just editors'. Everything else is dev-only.

### Transitive dependencies

A bump to a package nobody lists directly (common in lockfile-only security fixes) takes the
kind of whatever pulls it in. With more than one parent, the strictest kind among them wins.
Find the parents in the lockfile, without installing anything:

```bash
# npm: each package that depends on it, and the range it asks for
jq -r --arg d "<name>" '.packages | to_entries[]
  | .key as $k | ((.value.dependencies // {}) + (.value.devDependencies // {})
  + (.value.peerDependencies // {}))[$d] // empty | "\(if $k == "" then "(root)" else $k end) \(.)"' \
  package-lock.json

# NuGet, with packages.lock.json files: each package that depends on it, and the version it asks for
find . -name packages.lock.json -not -path "*/node_modules/*" -print0 |
  xargs -0 jq -r --arg d "<name>" '.dependencies[] | to_entries[]
    | select(.value.dependencies[$d]?) | "\(.key) \(.value.dependencies[$d])"' | sort -u
```

npm keys are install paths (`node_modules/a/node_modules/b`), and a workspace shows as its
folder. A parent that's itself transitive needs the same lookup again, until it reaches a
direct dependency. With a restore already in place, `npm explain <name>` and
`dotnet nuget why <project> <name>` walk the whole chain in one go.

These read the working tree. For a version line other than the one checked out, feed the
line's committed lockfiles in instead (`jq ... <(git show origin/<line>:<lockfile>)`). If
`packages.lock.json` is turned on but ignored by git, the working tree's copy only shows
the last local restore; walk the nuspecs instead.

### A fix no PR can deliver

Sometimes a vulnerable transitive version can't move by a normal bump: a parent pins it
exactly, or no fixed version exists yet. For a dev-only or shipped chain:

- **npm:** an `overrides` entry in the root `package.json` forces the fixed version. Check
  the parent still works with it, and remove the override once the parent catches up.
- **NuGet:** a direct reference to the fixed version raises the transitive one (with central
  package management, `CentralPackageTransitivePinningEnabled` does the same from
  `Directory.Packages.props`).
- **No fixed version:** say so, with what uses it. Dev-only use usually means low real risk;
  the maintainer decides whether to dismiss the alert.

For a locked chain, neither applies: the fix comes through the CMS.

### GitHub Actions

Dev-only: workflows run in CI, not on sites. A compromised action can still reach the
repo's secrets, so pin third-party actions to a commit SHA and read the diff of an update
before merging it.

## What each kind needs before a bump

| Kind | Before bumping |
|---|---|
| Locked | Don't. It moves when the floor moves. Close the update. |
| Ships | A new major waits for the package's next major release, unless the maintainer asks for it. Read the release notes between the two versions. Check the resolved versions of locked packages stay at or below the floor's (see "Ships to sites or dev-only"), and the bundle has no second copy of a shared library. Build, test, and smoke. It's a change users get, so the package's release notes say so. |
| Dev-only | Any version, any time. Build and test. A major version of a build tool can still break the build or change the output, so read its breaking changes. |

## Dependabot

`templates/dependabot.yml` is the starting point for a package's `.github/dependabot.yml`.
Fill it in from the project:

1. **One entry per ecosystem per version line.** NuGet where the solution or root
   `Directory.Packages.props` lives. npm where each `package-lock.json` lives: one entry at
   the root for npm workspaces, one per client folder otherwise, and one for any other
   project with its own lockfile (an acceptance-test project, say), whose dependencies are
   all dev-only. GitHub Actions with `directories` covering `/` and any composite actions
   under `.github/actions/*`; skip it if every workflow calls a shared one by branch
   (`@main`), since there's nothing to update.

   Dependabot only opens version update PRs against the default branch unless an entry sets
   `target-branch`, so with more than one line, copy the NuGet and npm entries once per
   extra line. Leave `target-branch` off the default branch's entries: an entry that sets it
   no longer applies to security updates, so its `ignore` list would stop working for them.
   Security updates only ever target the default branch; other lines need the same fix
   ported by hand. If the default branch isn't a supported line, every real line needs
   `target-branch` and no ignore list reaches security PRs; say so to the maintainer.

   If the repo holds scaffolding or template projects with their own
   `Directory.Packages.props` or `package.json`, `exclude-paths` keeps version updates out
   of them.
2. **Ignore every locked dependency.** List each by name, from the "Locked to the CMS"
   check above. For npm that's the backoffice's whole peer list, not only what the client
   lists: security PRs land on transitive peers too. Use a wildcard only where every match
   is locked, counting packages that release in step with a locked one (`Umbraco.Cms*`,
   `Microsoft.EntityFrameworkCore*`). A prefix that shipped packages or build tools share
   doesn't qualify (`Microsoft.Extensions.*`, `Umbraco.*`). For NuGet, cover the whole graph
   of every product the package builds on, not only what the project references directly:
   security PRs land on transitive packages too. Give no `update-types`, so every version
   is ignored: a locked dependency moves with the floor, never on its own. `ignore` stops
   security update PRs too, which is right here: the fix comes through the CMS.

   Shipped dependencies get an ignore entry too, for majors only (`update-types:
   ["version-update:semver-major"]`): a new major waits for the package's next major
   release, so a weekly PR for it is noise. Patches and minors still come through.
3. **Group by name.** One PR a week for all dev-only bumps in an ecosystem keeps the noise
   down. List them under `patterns`, checking each against how it's used: a mocking library
   is dev-only in tests but ships in a published testing package (`*.Testing`).
   Dependabot's `dependency-type` grouping doesn't work for NuGet, and for npm it follows
   `package.json`, not the bundle. Leave other shipped
   dependencies ungrouped so each gets its own review, except a family from one vendor that
   releases often (`AWSSDK.*`): one group for the family is still one review. Groups only
   cover version updates unless they add `applies-to: security-updates`, and transitive
   security bumps rarely match a name pattern, so expect those one per PR.
4. **Match the repo's commit rules.** Dependabot's default messages (`build(deps-dev): bump
   ...`) can break the repo's commit rules, whether those run in CI or only as a local git
   hook, and with merge commits they land on trunk as written. Set `commit-message.prefix`
   (and `prefix-development`) to what the repo allows. The rest of the subject (`bump x from
   ...`) can't be configured, so check the first PR after the change against rules like
   subject case.

Prefer the config file over `@dependabot ignore` comments. Those are stored by GitHub, out of
sight of anyone reading the repo.

Re-check the ignore list when the floor moves: a new CMS release can lock a package it
didn't before.
