---
name: umbraco-marketplace
description: >-
  Gets a finished package listed on the Umbraco Marketplace: the NuGet tag, the dependency
  Marketplace reads version support from, the v14+ compatibility gotcha, and
  umbraco-marketplace.json. Use when a package is ready to publish, or when reviewing its
  packaging.
user-invocable: true
argument-hint: [optional]
---

# umbraco-marketplace

Getting listed is almost entirely automatic — there's no submission form, no review queue, no
code-quality or security gate, and no revenue share. The whole mechanism is a NuGet tag plus a
dependency reference. Most packages that "aren't showing up" just have one of those wrong.

## *How listing actually works*

Marketplace syncs from NuGet, not from a submission: new packages are picked up daily, listing
metadata refreshes every couple of hours, and there's a self-serve validator
(marketplace.umbraco.com/validate) to check your metadata before or after publishing. There is
no human review step and no stated code-quality, security, or "actively maintained" bar — see
"What this skips, and why" below for what that means for this skill's scope.

## What actually gets you listed

1. **The `umbraco-marketplace` NuGet tag.** Add it to the package's `<PackageTags>` — and only
   to the top-level, installable package. Don't tag an internal `.Core`-style dependency
   package that isn't meant to be installed directly; that just duplicates the listing.
2. **A dependency on an Umbraco package.** Marketplace infers which CMS major version(s) your
   package supports from the version range of your `Umbraco.Cms.*` (or `UmbracoCms.*` for a
   v8 package, `Umbraco.Commerce.*` for a Commerce extension) package reference. If that
   reference is missing or wrong, the version compatibility shown on the listing will be wrong
   too.
3. **Standard NuGet metadata**, same fields as any NuGet package, pulled straight into the
   listing: `PackageId` (community convention: `Umbraco.Community.<PackageName>` for an
   unofficial package), `Authors`, `Description`, `PackageIcon`, `PackageReadmeFile`,
   `PackageProjectUrl`, `PackageLicenseExpression` (a real SPDX id — MIT is the common default,
   same as `github-init`'s recommendation), `Tags`.

## The version-compatibility gotcha

Umbraco 14 rewrote the backoffice. Because of that, Marketplace doesn't trust an open-ended
range across that line: **a dependency with a minimum of v13 or lower and no maximum (say
`Umbraco.Cms.Core` `10.0.0`) is listed as not supporting v14+**, even if the code works there.
That's right for anything with backoffice UI. For a package with no UI that really does work
on v14+, there are two fixes:

- Set `VersionDependencyMode: SemVer` in the optional `umbraco-marketplace.json` described
  below. Marketplace then takes the NuGet range as written, open maximum included. This
  fixes the listing without a new release.
- Or release a version whose range doesn't cross the line that way: a minimum of v14, or an
  explicit maximum (`[10.0.0, 18.0.0)`).

A range that already stops below v14 (`[10.0.0, 14.0.0)`) means what it says; neither fix
applies until the range itself changes.

## Optional: `umbraco-marketplace.json` — richer listing metadata

Hosted at your `PackageProjectUrl` (or `umbraco-marketplace-{package-id}.json` if one repo or
site hosts more than one package). Lets you set things NuGet metadata alone can't express:
title, a longer description, a category (Marketplace uses a fixed list — check the current
one on the docs page below rather than assuming it hasn't changed), a license type (Free /
Purchase / Subscription — a display label, not a billing integration; Marketplace doesn't take
a cut), package type, documentation/issue-tracker/discussion links, screenshots, video links,
author/contributor details, related packages, and the `VersionDependencyMode` override above.
A sibling `umbraco-marketplace-readme.md` file can override the listing's README independent
of the one NuGet ships.

**Field names and the category list change over time — confirm the current shape against
the docs (`umbraco-docs`) before hand-writing this file rather than copying an example verbatim.**

## Behavior — before you tag a release

1. Confirm the package's `.csproj`/`.nuspec` has the tag, the Umbraco dependency, and the
   standard metadata fields above. Don't invent values — pull description/icon/license from
   what the project already declares (`README.md`, `LICENSE`, `CLAUDE.md`'s stated CMS
   version(s)), the same discipline `github-init` uses for its README gate.
2. If the package works on Umbraco 14+ but its range is open-ended from v13 or lower, apply
   one of the two fixes in "The version-compatibility gotcha".
3. If richer listing metadata is wanted (screenshots, category, docs links), draft
   `umbraco-marketplace.json` — confirm the current field names/category list against the
   docs first.
4. After publishing to NuGet, run the package through marketplace.umbraco.com/validate before
   considering this done.

## *What this skips, and why*

- **No code-quality, security, or "actively maintained" gate.** Umbraco doesn't enforce one at
  listing time, so this skill doesn't invent one — that's `umbraco-security` and
  the `reviewer` agent's job, already covered elsewhere in this plugin.
- **No release pipeline.** Tagging a version and running `dotnet pack`/`dotnet nuget push` is a
  "build on top" concern, same as the README's own stated scope for `git-workflow` — this
  skill covers what makes a *published* package listable, not how you automate the publish
  step itself.
- **License type is a label, not a payment system.** Setting `Purchase`/`Subscription` in
  `umbraco-marketplace.json` doesn't wire up billing; if the package needs real payment
  handling, that's a separate, project-specific concern this skill doesn't cover.

## *Sources*

- https://docs.umbraco.com/umbraco-dxp/marketplace/listing-your-package
- https://docs.umbraco.com/umbraco-dxp/marketplace/introduction
- https://docs.umbraco.com/umbraco-cms/extend-your-project/packages/creating-a-package
- https://umbraco.com/blog/get-ready-for-the-new-umbraco-marketplace

## *Hand off*

Report which of the required items were already in place, which were added, and whether
`umbraco-marketplace.json` was created/updated and why. If any field's current shape couldn't
be confirmed against live docs, say so rather than guessing.
