---
name: package-release
description: "Use when cutting, planning or reviewing the release of a published library or tool: version number, what counts as a breaking change, deprecation, toolchain floor, tag hygiene, publishing credentials, and recovery from a bad release."
---

# package-release

Extends step 10, `ship` (`WORKFLOW.md`), for anything other people install from a registry or a module proxy. A
release is a promise: once a version is out, someone depends on it. This block is the checklist for making
the promise correctly. **Status 🟡: base to confront with reality**, written from documentation read on
2026-10-02, not from a release run in house.

## When
A version is about to be tagged or published; a change touches the public surface of a published package; a
dependency floor or toolchain floor moves; a release went wrong. Applications that ship binaries only to
themselves skip steps 2 and 3 and keep the rest.

## Steps

1. **Pick the version from the change, not from the calendar.**
   1. The public surface is declared (documentation or exported symbols). Without a declared surface there
      is nothing to promise.
   2. Below 1.0 nothing is promised: anything may change. Staying there indefinitely while others depend on
      the package withholds a promise they need.
   3. Once released, the contents of a version never change; any fix is a new version.
   4. Deprecating existing behaviour raises the minor number; removal waits for the next major.
   5. In ecosystems whose module path carries the major (Go, from 2 up), a major bump is a new import path,
      so it is a new library in practice: reach for it only when the surface cannot be fixed additively.

2. **Know what breaks, per language.** Read the ecosystem's own compatibility rules before deciding a change
   is minor. Examples read on 2026-10-02:
   1. Go: removing or renaming an exported name, changing a signature, adding a method to an exported
      interface (every outside implementor stops satisfying it), changing a constant's value. Adding a
      field to a struct breaks unkeyed composite literals.
   2. Rust: removing a public item, adding a variant to an enum not marked non-exhaustive, adding a
      required trait item, adding a function parameter. Raising the minimum compiler version is classed
      possibly-breaking.
   3. Any language: tightening validation makes previously working calls fail, so treat it as breaking even
      when no signature changed. Error message wording is not a contract unless you export something
      matchable.

3. **Compare the surface mechanically before the tag.** Run the ecosystem's API-diff tool against the last
   release and read its verdict, rather than judging by eye. Run it on every change that touches the public
   surface, so a break is found in review and not after the tag. Where no such tool exists, diff the exported
   symbol list.

4. **Deprecate in a machine-readable way.** Use the convention the tooling understands (in Go, a paragraph
   starting exactly `Deprecated:`), name the replacement, release it as a minor, and keep the old path
   working for the rest of the major.

5. **Mind the floor you impose.**
   1. The minimum language or toolchain version in the manifest is a requirement on every dependent (in Go
      the `go` directive is a required minimum; a dependent's must be at least as high). Set it to the
      oldest version you actually need, not the one you run.
   2. Dependency minimums stay as low as the code allows.

6. **Tag only a clean tree.**
   1. No local override of a dependency in the tagged manifest: in Go, `replace` applies only in the main
      module, so dependents get something other than what you tested. Workspace files do not ship either.
   2. The lockfile or checksum file is regenerated in the same change as the version bump, and the tidy
      command leaves no diff.
   3. Build, vet, test (with the race detector where the language has one) and the vulnerability scan pass
      on the tagged commit.

7. **Publish with short-lived credentials, behind a person.**
   1. Prefer the registry's trusted-publishing mechanism: the CI job proves its identity by OIDC and the
      registry issues a token that expires in minutes (PyPI states 15 minutes; npm supports it from CLI
      11.5.1 and Node 22.14.0 on its documented CI platforms, and then writes provenance for public
      packages). No long-lived registry token in CI secrets.
   2. The publish job runs in a protected environment that needs a human approval, and its token permissions
      are the minimum the job needs. This approval gate is a house rule, not something the registry
      documentation above requires.
   3. A tag or push made with the workflow's own token does not start other workflows (only manual and
      repository dispatch events do). A release pipeline chained that way must use a dedicated app or
      credential, or be a single workflow.

8. **A bad release is fixed forward.** Do not delete a published version or move its tag: the proxy or registry has
   already cached it and your tag now disagrees with it. Ship a new version; where the ecosystem has a
   withdrawal marker, use it (Go: a `retract` directive with a reason, published in a higher version, which
   hides the version from latest queries while keeping it downloadable). Write release notes for humans:
   what is new, what is deprecated, any behaviour change.

## Output / checkpoint
A release note, the API-diff output, the computed next version with the reason, and the clean-tree checks
listed in step 6, attached to the `ship` checkpoint (`WORKFLOW.md` §5) as the proof that the merge is also a
releasable state. The operator triggers the publish.

## Guardrails
The agent prepares and verifies; it does not publish, create registry accounts or hold registry tokens.
Never decide "minor" because the diff looks small: step 2 and 3 decide. Release numbers and tool versions
quoted here are as read on 2026-10-02 and go stale: re-read the registry documentation before relying on
them (`skills/source-freshness`).

## Origin
Rewritten, no text copied. Go compatibility, deprecation and recovery mechanics from the MIT-licensed
`spf13/go-skills` release skill (read 2026-10-02) cross-checked against the Go modules reference; the version
rules from the semantic versioning specification (CC-BY-3.0, items on public API, immutability, major
zero, deprecation); Rust rules from the Cargo book's compatibility chapter; trusted publishing from the PyPI
and npm documentation; the workflow-token behaviour from the GitHub Actions documentation. Binary
distribution tooling (signing, packaging) was left out: not read deeply enough to state rules.
