---
name: iru-setup-swift-library
description: "/iru-setup-swift-library [args] generates the Swift Package Manager toolchain for a new Swift library at the repository root: Package.swift, Sources and Tests, SwiftLint, swift-format, DocC, optional .spi.yml and Sonar config. Asks package-name, platforms, license and identity unless supplied via key: value args from iru-setup-swift-repository; asks Update/Keep/Replace/Stop on existing files."
model: sonnet
---

# Setup Swift Library

Generate the standard Swift Package Manager library toolchain at the repository root: `Package.swift`, the
`Sources/<Name>/` and `Tests/<Name>Tests/` layout, `.swiftlint.yml`, a `.swift-format`/`.swiftformat` config, a
DocC catalog page, and — when opted in — `.spi.yml` and `sonar-project.properties`. Every file starts from
`swift package init --type library`'s own scaffold (Step 5), then this skill rewrites it using explicit example
templates embedded below (Steps 5–9), genericized (no real repo/org/person names, `<placeholder>` markers resolved
from Steps 2–4) and verified end-to-end against Swift 6.4/Xcode 27 in `$TMPDIR/iru-verify/swift/library` while
building this skill. Equivalent to `iru-setup-java-library`/`iru-setup-typescript-library`/`iru-setup-android-library`
for the Swift/SwiftPM stack.

**`swiftLanguageModes:` requires `// swift-tools-version: 6.0` or newer** — it does not exist as a `Package`
initializer parameter under older tools-versions (SwiftPM parses the manifest with a compiler pinned to the
declared tools-version, so an older declaration fails to even parse a manifest that uses it). This skill always
writes `// swift-tools-version: 6.0` for exactly this reason, even though `swift package init` itself defaults to
whatever tools-version the active toolchain ships (`6.4` was observed here, Step 10's quirks).

## Step 0 — Resolve inputs

This skill can be invoked stand-alone (`/iru-setup-swift-library`) or as a step inside another skill (e.g. a
future `iru-setup-swift-repository` or the catalog's `iru-setup-repository` front door), which resolves these same
inputs itself and passes them through `args` as `key: value` lines, one per line, e.g.:

```
package-name: my-example-lib
platforms: ios, macos
min-deployment-targets: ios=17.0, macos=14.0
license: Apache License 2.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
publish: yes
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-example-lib
sonar-host-url: https://sonarcloud.io
formatter: swift-format
visibility: public
ci: yes
mode: new
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2. Only
fields genuinely missing from `args` still need a question. If `args` is absent or doesn't look like this format,
treat everything as unset and ask normally.

Recognized keys: `package-name` (the SwiftPM package identity written to `Package(name: ...)` — may contain
hyphens, e.g. `my-example-lib`; see Step 2 for how the PascalCase `<Name>` used everywhere else is derived from
it), `platforms` (a comma/space-separated list from `ios`/`ipados`/`macos`/`watchos`/`tvos`/`visionos`/`linux`),
`min-deployment-targets` (only relevant for whichever of `ios`/`ipados`/`macos`/`watchos`/`tvos`/`visionos` was
selected — `linux` has no deployment-target concept in SwiftPM, see Step 2), `license`, `developer-name`,
`developer-email`, `organization-url`, `open-source` (`yes`/`no`), `publish` (`yes`/`no`), `sonar`
(`cloud`/`self-hosted`/`none`) plus, only when `sonar` is `cloud` or `self-hosted`,
`sonar-organization`/`sonar-project-key`/`sonar-host-url`, `formatter` (`swift-format`/`swiftformat`, default
`swift-format`), `visibility` (`public`/`private`/`internal` — the GitHub repository's visibility; only used to
key Step 2's Sonar recommendation, `internal` behaving like `private`), `ci` (`yes`/`no` — whether GitHub Actions
workflows will exist to send Sonar reports; see Step 2's `ci: no` note), `on-existing` (`ask`/`keep`/`update`/
`replace`, default `ask` — how Step 1 treats each file of this skill's that already exists), and `mode`
(`new`/`existing`).

`mode: existing` is this catalog's shared signal (set by a front door that already ran `iru-explore` and knows
this is an established repository) that this is an update rather than a from-scratch run. It **no longer means a
silent gap-fill**: Step 1 still warns about and asks per already-existing file (unless `on-existing` says
otherwise). `mode: new` or an unset `mode` follows the same Step 1 survey — the files actually on disk decide
whether each one is created or updated.

**Templates.** The file templates of Steps 5–9 are files under this skill's `templates/` directory, not inline text. Read only the template files that apply (the index at the top of Step 5 says which, including the `formatter` variant resolved in Step 2); never read the others.

## Step 1 — Survey the repository

Check, at the repository root, which of this skill's files already exist: `Package.swift`, `Sources/*/*.swift`,
`Tests/*Tests/*.swift` (a `Package.swift` alone, with no matching `Sources/<Name>/` tree, still counts as
"exists" — treat it the same as any other partial state), `.swiftlint.yml`, `.swift-format` or `.swiftformat`
(whichever `formatter` — once resolved — points at), `Sources/*/*.docc/*.md`, `.spi.yml` (only relevant once
`publish` is resolved in Step 2), `sonar-project.properties` (only relevant once `sonar` is resolved in Step 2).

Then tell the user, before anything else, which of the two this run is:

- **None exist**: "**Creating the Swift package from scratch** — none of this skill's files exist yet." Skip
  straight to Step 2; every file in Steps 5–9 is *created*.
- **At least one exists**: "**Updating an existing Swift package** — found: <list of paths>." Then, for each
  existing artifact, **warn** and resolve what to do with it. If `on-existing` is `keep`/`update`/`replace`, apply
  that to every existing file without asking (still print the warning and the list). Otherwise (`on-existing: ask`
  or unset — and regardless of `mode`), ask with `AskUserQuestion`, one question per artifact, batching up to four
  artifacts per call (group `Sources/`+`Tests/` placeholder sources as one "source skeleton" artifact so the
  question count stays small). Each question offers, with these consequences stated in the option descriptions:
  - **Update (Recommended)** — merge: add what's missing and correct outdated parts using this skill's template as
    reference, keeping everything this skill doesn't own. For `Package.swift` that means adding a missing
    `swift-docc-plugin` dependency, missing `platforms:` entries and `swiftLanguageModes: [.v6]` (respecting the
    compiler-enforced parameter order, Step 5) and raising a pre-6.0 `swift-tools-version` to `6.0` — while
    keeping every extra target, product, dependency and setting; for `.swiftlint.yml`/the formatter config, adding
    missing rules/keys without dropping custom ones; for `sonar-project.properties`, correcting stale keys (e.g. a
    bare `sonar.swiftlint.reportPaths`) and values from Step 2. You review a diff before it's written;
    customizations survive, but a part this skill owns may be rewritten. For the source skeleton, Update means
    "create only missing placeholder files" — existing source under `Sources/`/`Tests/` is never edited.
  - **Keep as is** — leave the file untouched. Nothing customized changes, but it may stay out of date or disagree
    with this run's choices — say so concretely in the question when it does (e.g. "`sonar-project.properties`
    exists but you chose `sonar: none`", "`.spi.yml` exists but you chose `publish: no`", "`Package.swift`
    declares `swift-tools-version: 5.9`, too old for `swiftLanguageModes:`"); Step 14 lists each mismatch.
    Recommend Keep instead of Update for the source skeleton once real library code exists under `Sources/<Name>`.
  - **Replace** — regenerate from this skill's template. The result matches this house pattern exactly, but every
    customization in the file (extra targets, dependencies, hand-edited source) is lost — recoverable only from
    git history. Never recommended by default. When `Package.swift` is replaced, first read its current package
    name, target name, `platforms:` entries and whether a `swift-docc-plugin` dependency is present, and use them
    as the *defaults* for whichever Step 2 question Step 0 didn't already resolve via `args` — a value supplied
    via `args` always wins.
  - **Stop** — end this skill now without changing anything. Report this and end here.

  Questions about `.spi.yml`/`sonar-project.properties` whose relevance depends on `publish`/`sonar` are asked
  after Step 2 resolves those (or now, if `args` already resolved them). Record each file's decision — Step 12
  applies it and Step 14 reports it as **created / updated / replaced / kept as is**.

## Step 2 — Collect the required inputs

For any field Step 0 already resolved from `args`, use that value directly and don't ask about it again. For
everything else, ask the user directly (plain conversation, pre-filling defaults found in Step 1 if `Package.swift` is being replaced or updated):

- **package-name** — the SwiftPM package identity, e.g. `my-example-lib`. This is exactly what `Package(name:
  ...)` and a consumer's `.package(url: "<repository-url>", from: "1.0.0")` line use to identify the package; it
  commonly matches the repository name and may contain hyphens.
- **`<Name>`** — derived automatically from `package-name`, never asked separately: PascalCase, each
  `-`/`_`-separated word capitalized and concatenated, non-alphanumeric characters stripped (e.g. `my-example-lib`
  → `MyExampleLib`). `<Name>` is the product/target/type name and the `Sources/<Name>/`, `Tests/<Name>Tests/`,
  `Sources/<Name>/<Name>.docc/` directory names — **never** pass the raw hyphenated `package-name` to `swift
  package init --name` directly; see Step 5's quirk on why that produces snake_case directories instead of the
  clean `<Name>` this skill's templates assume.
- **platforms** — one or more of `ios`, `ipados`, `macos`, `watchos`, `tvos`, `visionos`, `linux`. When asking
  interactively, split the seven values across **two `AskUserQuestion` multi-select rounds**, since the tool
  allows at most four options per question: first the Apple platforms — *iOS / iPadOS / macOS / watchOS* — then
  a second multi-select — *tvOS / visionOS / Linux / none of these*. Union the two answers (at least one real
  platform required overall); this is the same two-round split `iru-setup-swift-repository` uses. Maps to
  `Package.swift`'s `platforms:` array (Step 5) with one caveat each:
  - **`ios` and `ipados` collapse to the same single `.iOS(...)` entry** — SwiftPM's `SupportedPlatform` enum has
    no separate iPadOS case; a package's minimum iOS deployment target already covers both idioms (the
    iPhone/iPad distinction is an app-level `TARGETED_DEVICE_FAMILY` concern, not a package-level one). If both
    are selected, ask only once for the shared minimum version in `min-deployment-targets` below and emit a single
    `.iOS(...)` line.
  - **`linux` adds no entry to `platforms:` at all** — confirmed while verifying this skill: `SupportedPlatform`
    has no `.linux` case, and adding one fails the manifest with `error: type
    'Array<SupportedPlatform>.ArrayLiteralElement' (aka 'SupportedPlatform') has no member 'linux'`. Linux (and
    any other non-Apple platform SwiftPM supports) is available automatically whenever the package's code doesn't
    depend on an Apple-only API — there is nothing to add to the manifest to opt in, and nothing to remove to opt
    out short of actually avoiding Apple-only imports. If `linux` is the *only* platform selected, omit the
    `platforms:` key from `Package.swift` entirely rather than writing an empty array.
  - `macos`, `watchos`, `tvos`, `visionos` each map to their own `.macOS(...)`/`.watchOS(...)`/`.tvOS(...)`/
    `.visionOS(...)` entry.
- **min-deployment-targets** — for each selected Apple platform (`ios`/`ipados` counted once, `macos`, `watchos`,
  `tvos`, `visionos`), the minimum OS version, e.g. `ios: 17.0`, `macos: 14.0`. No sensible universal default —
  ask directly; offer the current stable major-minus-one release per platform as a starting suggestion if the
  user has no preference (this skill's own verification run used iOS 17 / macOS 14).
- **Developer name**, **developer email**, **organizationUrl** — used in generated doc-comment headers (Steps 6)
  and, when `publish: yes`, nowhere else — SwiftPM packages have no POM/`package.json`-style `<developers>`/
  `author` metadata block; a package's authorship is conveyed through its git history, README, and `LICENSE`
  file instead.

Then, unless Step 0 already resolved a `license` value from `args`, ask about the **license** with
`AskUserQuestion` (small bounded choice, same four options this catalog's other setup skills use):

- Apache License 2.0 (recommended) — `Apache License 2.0` / `http://www.apache.org/licenses/LICENSE-2.0.txt`
- MIT License — `The MIT License` / `https://opensource.org/license/mit`
- No license (proprietary / all rights reserved) — omit the license-header comment from every generated Swift
  file (Steps 5–6) and from `.swiftlint.yml`'s `file_header` rule (Step 7) — both its configuration and its
  `opt_in_rules` entry
- Other — ask for the license's display name and URL directly afterward

If a license is chosen (anything but "No license"), remind the user in the final report to also add a matching
`LICENSE` file at the repository root if one doesn't exist yet — the `iru-check-license` skill can verify/backfill
file headers against it once it's there.

Then resolve `open-source`, `publish`, and `sonar` — skip any of the three Step 0 already resolved from `args`.
When invoked stand-alone with none of them pre-resolved, ask `open-source` *first* (`AskUserQuestion`: yes/no) and
derive the recommended defaults for the other two from that answer, per this catalog's shared convention:

- **open-source** — is this repository open source? Yes / No.
- **publish** — does this library get distributed for other projects to depend on (via a git URL/tag, and
  optionally listed on the Swift Package Index)? Default **Yes** when open-source is Yes; when not open source,
  ask with **No** recommended, explaining that the Swift Package Index (which `.spi.yml`, Step 8, configures for)
  is a public catalog meant for redistributable open-source packages. `No` omits `.spi.yml` from Step 8's template
  entirely — there is no Maven Central/npm-registry-style publish step for SwiftPM to gate either way; a
  package "publishes" simply by existing at a git URL a consumer can add a `.package(url: ..., from: ...)`
  dependency on, tagged with semver tags, which this skill doesn't need to configure.
- **sonar** — whether to wire up a SonarQube/SonarCloud scan (`sonar-project.properties`, Step 9 — typically
  consumed by a CI workflow such as a future `iru-setup-swift-github-workflows`, so it's worth setting up here
  even if that workflow comes later). Recommend **SonarCloud** (`cloud`) only when open-source is Yes **and**
  `visibility` is `public` (or unknown — `visibility` isn't asked by this skill; it only arrives via `args`);
  otherwise state that SonarCloud (SonarQube Cloud) is free only for public/open-source projects — a private
  project needs a paid plan, per its current pricing — and recommend **None** (`none`), offering **self-hosted
  SonarQube** (Community Build is free, but you run the server) as the second option. **When `ci: no` arrived via
  `args`**, say plainly that no workflow will send analysis or coverage reports automatically — analysis would
  only run when someone runs the scanner manually with a token — and recommend `none`; if the user still picks
  `cloud`/`self-hosted`, write `sonar-project.properties` (the build-side config) only and note in Step 14 that no
  CI step sends reports:
  - `cloud` — ask for the `sonar.organization` key, offering `<owner>-github` (the owner parsed in Step 3) as the
    suggested default. Default `sonar.projectKey` to `<owner>_<repo>` and `sonar.host.url` to
    `https://sonarcloud.io`, confirming both with the user rather than assuming silently.
  - `self-hosted` — ask for `sonar.host.url` directly (no sensible default — this is what replaces the fixed
    `https://sonarcloud.io` host in Step 9's template), plus `sonar.organization` only if that server has
    organizations enabled, and `sonar.projectKey`.
  - `none` — omit `sonar-project.properties` entirely (Step 9).

Finally, resolve **formatter** (`swift-format`/`swiftformat`, default `swift-format`) — skip if Step 0 already
resolved it:

- **`swift-format`** (default, recommended) — the Swift toolchain's own bundled formatter (invoked as `swift
  format lint`/`swift format format`, a subcommand of the `swift` driver — not a separate binary to install).
  Configured via a `.swift-format` JSON file (Step 7). This is the only variant this skill actually verified
  end-to-end (Step 10).
- **`swiftformat`** — the third-party nicklockwood/SwiftFormat tool (a different project from Apple's
  `swift-format` despite the near-identical name), configured via a `.swiftformat` file (Step 7) and installed
  separately (typically `brew install swiftformat`, or the Mint/SPM-plugin routes its own README documents) for
  whoever — locally or in CI — needs to invoke it. **Unverified locally** — this environment has no `brew`, and
  building it from source was out of scope for verifying this skill. Say so explicitly if the user picks it.

## Step 3 — Infer repository information

Don't ask for these — derive them from the current repository, the same way `iru-setup-java-library` and
`iru-setup-android-library` do:

- **Owner/repo and host**: parse `git remote get-url origin` (handles both `git@host:owner/repo.git` and
  `https://host/owner/repo.git` forms). Use the parsed owner for the `sonar.organization`/`sonar.projectKey`
  defaults in Step 2 (only relevant when `sonar` isn't `none`), and the parsed host/owner/repo to build
  `<repository-url>` (`https://<host>/<owner>/<repo>`), used only in generated doc-comment headers/README-style
  guidance in the final report — `Package.swift` itself carries no repository URL field. If there's no `origin`
  remote yet, ask the user for the intended repository URL instead of leaving it blank.
- **Inception year**: `git log --reverse --format=%ad --date=format:%Y | head -1` for the first commit's year;
  fall back to the current year if the repository has no commits yet. Feeds the copyright year in Steps 6's
  doc-comment headers (use the *current* year there instead, per that step's own note — a license header's
  copyright year is the year of the file, not the repository's inception year).
- **Stable branch**: default `main` unless the caller (an orchestrator, or the user) names a different stable
  branch — only used, if at all, in the final report's guidance text.

## Step 4 — Look up dependency versions

Look up the version below at run time; only fall back to the table's recorded value if the lookup fails (offline,
GitHub API rate-limited). Note in the final report whenever a fallback was used instead of a live lookup.

| Component | Lookup | September 2026 fallback |
|---|---|---|
| `swift-docc-plugin` (only `publish` question resolved — actually needed regardless of `publish`, since DocC generation is verified unconditionally in Step 12; see Step 8's note) | `gh api repos/swiftlang/swift-docc-plugin/releases/latest -q .tag_name` (or `curl -s https://api.github.com/repos/swiftlang/swift-docc-plugin/releases/latest`), stripped of a leading `v` if present | `1.5.0` |

Only one dependency is looked up here — unlike the Java/TypeScript/Android siblings, this skill's own toolchain
(`swiftlint`, `swift format`, `swiftformat`) is either bundled with the Swift toolchain (no version to pin — see
Step 7's note) or a standalone CLI installed outside SwiftPM's dependency graph entirely (`swiftlint`,
`swiftformat` — neither is a `Package.swift` dependency; their versions are a CI/local-install concern, not a
manifest concern, and are out of this skill's scope).

## Step 5 — Scaffold via `swift package init`, then rewrite `Package.swift`

**Templates.** Every template in Steps 5–9 is a file under `templates/<variant>/<path of the generated file>` (a `{Name}` path segment stands for the target's `<Name>`), holding the exact bytes of that generated file's template. Read only the files that apply, each in full, before filling placeholders:

| Generated file | Template | Applies when |
|---|---|---|
| `Package.swift` | `templates/common/Package.swift` | always (Step 5) |
| `Sources/<Name>/<Name>.swift` | `templates/common/Sources/{Name}/{Name}.swift` | always (Step 6) |
| `Tests/<Name>Tests/<Name>Tests.swift` | `templates/common/Tests/{Name}Tests/{Name}Tests.swift` | always — Swift Testing example (Step 6) |
| `Tests/<Name>Tests/<Name>XCTests.swift` | `templates/common/Tests/{Name}Tests/{Name}XCTests.swift` | always — XCTest example, same test target (Step 6) |
| `Sources/<Name>/<Name>.docc/<Name>.md` | `templates/common/Sources/{Name}/{Name}.docc/{Name}.md` | always — DocC catalog landing page (Step 6) |
| `.swiftlint.yml` | `templates/common/.swiftlint.yml` | always (Step 7) |
| `.swift-format` | `templates/swift-format/.swift-format` | `formatter: swift-format`, the default (Step 7) |
| `.swiftformat` | `templates/swiftformat/.swiftformat` | `formatter: swiftformat` — unverified locally (Step 7) |
| `.spi.yml` | `templates/common/.spi.yml` | only when `publish: yes` (Step 8) |
| `sonar-project.properties` | `templates/common/sonar-project.properties` | only when `sonar` is not `none` (Step 9) |

Run, at the repository root:

```
swift package init --type library --name <Name>
```

**Always pass the PascalCase `<Name>` here, never the raw hyphenated `package-name`.** Confirmed while verifying
this skill (Swift 6.4/Xcode 27): `swift package init --type library --name my-example-lib` creates
`Sources/my_example_lib/my_example_lib.swift` and `Tests/my_example_libTests/` — SwiftPM silently converts a
hyphenated `--name` into `snake_case` for the target/directory/file names (while keeping the hyphenated form
verbatim as the package's own `Package(name: ...)` identity) rather than PascalCasing it. Passing the already-
PascalCase `<Name>` (e.g. `MyExampleLib`) avoids this entirely — `Sources/MyExampleLib/MyExampleLib.swift`,
`Tests/MyExampleLibTests/MyExampleLibTests.swift`, and every generated name in `Package.swift` come out already
matching what Steps 6–9's templates below expect. This command also emits a `.gitignore` and a `Package.swift`;
both are overwritten by the templates immediately below rather than kept as-is — the `iru-setup-swift-gitignore`
skill is the one responsible for the repository's actual `.gitignore` (see its own
`.build`/`DerivedData`/`xcuserdata` entries, a superset of what `swift package init`'s own default already
covers).

Then rewrite `Package.swift` in full with this template — genericized, verified end-to-end while building this
skill (`swift build` succeeds, including resolving `swift-docc-plugin` over the network — see Step 10). When a
license was chosen, prepend the same license-header comment the Swift sources get (Step 6) **above** the
`// swift-tools-version` line, followed by a blank line: SwiftPM accepts leading comments before the tools-version
declaration (verified with Swift 6.4 — `swift package describe` and `swift build` both succeed), and without it
SwiftLint's `file_header` rule fails `swiftlint lint --strict` on `Package.swift`, which the CI step lints along with
everything else (SwiftLint has no per-rule path exclusion — a `file_header: excluded:` key is rejected as an invalid
configuration and the rule silently falls back to its default):

Template: `templates/common/Package.swift` — read it in full before filling placeholders

**Argument order inside `Package(...)` is not free-form — the compiler enforces a fixed declaration order and
rejects a manifest that violates it**, confirmed while verifying this skill: placing `dependencies:` after
`swiftLanguageModes:` fails with `error: argument 'dependencies' must precede argument 'swiftLanguageModes'`. The
order shown above (`name`, `platforms`, `products`, `dependencies`, `targets`, `swiftLanguageModes`) is the one
that built clean; keep this exact ordering when adding any further parameter this skill doesn't already write
(e.g. `defaultLocalization`, `cLanguageStandard`) — check the `PackageDescription` module's own declaration order
for where a new parameter belongs rather than appending it wherever seems natural.

- `<package-name>` — Step 2.
- `<Name>` — derived from `<package-name>` per Step 2; used for the product, both targets, and (Steps 6–8) the
  `Sources/<Name>/`, `Tests/<Name>Tests/`, and `Sources/<Name>/<Name>.docc/` directories.
- `platforms:` — built from Step 2's `platforms`/`min-deployment-targets` answers per that step's mapping rules:
  one `.iOS(.v<N>)` entry when `ios` and/or `ipados` was selected, `.macOS(.v<N>)` when `macos` was selected,
  `.watchOS(.v<N>)` when `watchos` was selected, `.tvOS(.v<N>)` when `tvos` was selected, `.visionOS(.v<N>)` when
  `visionos` was selected — omit any entry for a platform not selected, and omit the whole `platforms:` key if
  `linux` was the only platform chosen (SwiftPM has no `SupportedPlatform` case for it; see Step 2). `.v<N>` uses
  SwiftPM's named minor-version case when one exists for the resolved minimum (e.g. `.v17` for iOS 17.0); for a
  minor point release with no named case, use `.v17_1`-style dotted-underscore syntax per `PackageDescription`'s
  own convention, or the numeric form `.custom("17.1", andUpper: "17.1")` only if neither named case applies.
- `dependencies:`/`swift-docc-plugin` — Step 4's resolved version. **Fetching this dependency needs network
  access** — confirmed while verifying this skill: `swift build`'s first run resolves and clones both
  `swift-docc-plugin` and its own transitive `swift-docc-symbolkit` dependency straight from GitHub
  (`Fetching https://github.com/swiftlang/swift-docc-plugin` / `swift-docc-symbolkit`) before compiling anything;
  an offline first run fails outright unless both are already cached under `~/.swiftpm`/`~/Library/Caches/`. This
  is the same class of "first invocation needs the network" caveat `iru-setup-android-library` documents for
  Gradle's own plugin resolution — warn the user of it in the final report the same way.
- `swiftLanguageModes: [.v6]` — always written; this is what this skill's frontmatter note at the top of this file
  refers to as requiring tools-version 6.0+.

## Step 6 — Reference templates: `Sources/<Name>/` and `Tests/<Name>Tests/`

Every generated Swift source/test file below carries this license-header doc comment (omit it entirely, on all
four files, if "No license" was chosen in Step 2):

```swift
//
// Copyright (C) <copyright-year> <developer-name>
//
// Licensed under the <license-name> (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//         <license-url>
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
```

`<copyright-year>` is the *current* year (not Step 3's repository inception year — that's a different field, used
nowhere in this skill's own templates).

### `Sources/<Name>/<Name>.swift`

Template: `templates/common/Sources/{Name}/{Name}.swift` — read it in full before filling placeholders

Named `<Name>Example` rather than the bare `Example` used by this catalog's Java/Android siblings' own placeholder
type, to avoid colliding with `XCTestCase`/Swift Testing's own vocabulary and with a consumer's likely `Example`
type; `<Name>` is already unique per package. `Sendable` conformance is deliberate, not incidental — under Swift 6
language mode (`swiftLanguageModes: [.v6]`, Step 5) with strict concurrency checking on by default, a public type
with no explicit `Sendable`/`~Sendable` annotation still compiles, but this skill states the conformance
explicitly so the scaffold models the concurrency-safety convention `iru-swift-code-one-task`'s own reference
guidance expects from real library code, rather than leaving it implicit on a type the user is meant to replace
anyway.

### `Tests/<Name>Tests/<Name>Tests.swift` — Swift Testing

Template: `templates/common/Tests/{Name}Tests/{Name}Tests.swift` — read it in full before filling placeholders

### `Tests/<Name>Tests/<Name>XCTests.swift` — XCTest

Template: `templates/common/Tests/{Name}Tests/{Name}XCTests.swift` — read it in full before filling placeholders

Both files live in the **same** `<Name>Tests` test target — confirmed while verifying this skill that `swift test`
runs both frameworks together in one invocation with no extra configuration (`swift test --enable-code-coverage`'s
console output shows an XCTest `Test Suite` block and a separate Swift Testing `◇ Test run started` block, both
passing, from the single command). There is no need for two separate test targets just to mix the two frameworks;
`iru-swift-test`'s own `swift test --filter` selector matches tests from either framework interchangeably.
`swift package init --type library` on this skill's own verified toolchain (Swift 6.4/Xcode 27) generates
**only** the Swift Testing file by default — no XCTest example — confirmed in Step 10's quirks; this skill adds
the XCTest file itself so a consumer sees both idioms represented, per the task this skill was built from.

### `Sources/<Name>/<Name>.docc/<Name>.md` — DocC catalog landing page

The same landing-page shape `iru-swift-docc`'s Step 4 requires of every target (a `# ``<Name>``` module-symbol
heading, a one-line summary, `## Overview`, and a `## Topics` section listing the public types), so a later
`/iru-swift-docc` run finds the catalog already complete instead of flagging it as missing:

Template: `templates/common/Sources/{Name}/{Name}.docc/{Name}.md` — read it in full before filling placeholders

A `.docc` folder containing only this one landing page is a valid, buildable DocC catalog — `swift-docc-plugin`
auto-discovers any `.docc` directory inside the target's source folder, so nothing in `Package.swift` references
it (unlike Dokka's `includes.from(...)`). `swift package init --type library` creates no catalog of its own,
which is why this skill writes it explicitly; Step 13's `swift package generate-documentation` verification
curates the archive from it. When the user later renames/replaces
`<Name>Example`, the `## Topics` entry must follow — a `## Topics` link to a symbol that no longer exists is
reported as a warning by `swift package generate-documentation`, not silently dropped.

## Step 7 — Reference templates: `.swiftlint.yml` and the formatter config

### `.swiftlint.yml`

Template: `templates/common/.swiftlint.yml` — read it in full before filling placeholders

**Why this shape** (verified on 2026-10-16 with SwiftLint 0.65.1 and the Swift 6.4 toolchain's `swift format`, in
`$TMPDIR/iru-verify/swift-lint-fix/`, against a `swift package init --type library` package carrying this file and
the `.swift-format` below):

- `file_header` is an **opt-in** rule, so configuring it is not enough: without its `opt_in_rules` entry SwiftLint
  prints `Found a configuration for 'file_header' rule, but it is not enabled in 'opt_in_rules'` and never checks
  headers. With both, a header-less source file fails `--strict` with `File Header Violation`.
- `unused_import` is an **analyzer** rule — it only runs under `swiftlint analyze` with a compiler log — so it lives
  under `analyzer_rules`; listed in `opt_in_rules` it only produces a configuration warning.
- `trailing_comma` is **disabled** because both formatters this skill offers add trailing commas to multi-line
  collections and argument lists (`swift format format` did, in `Package.swift` and in sources); with the rule on,
  every formatted file fails `swiftlint lint --strict`, and the two tools fight forever.
- Result: `swiftlint lint --strict` and `swift format lint --strict --recursive Sources Tests Package.swift` both exit 0
  on the formatted, headered package; the previous version of this template failed `--strict` with five
  `trailing_comma` errors and two configuration warnings on the same package.

Rule ids can still be renamed or retired across SwiftLint major versions — `iru-swift-code-quality` treats a missing
`swiftlint` binary as "not wired" rather than silently skipping the check, so a stale id surfaces the first time it
runs. `excluded: .build` is required regardless — SwiftLint otherwise walks the entire build cache (including fetched
`swift-docc-plugin`/`swift-docc-symbolkit` checkouts under `.build/checkouts`) and lints third-party source it
doesn't own.

### `.swift-format` (when `formatter: swift-format`, the default)

Template: `templates/swift-format/.swift-format` — read it in full before filling placeholders

**Verified working end-to-end** against Swift 6.4/Xcode 27 (Step 10): `swift format dump-configuration` prints
the toolchain's own default ruleset (all keys above are real, current rule ids taken straight from that output —
this file only flips several from the default `false` to `true`, opting into a stricter bar than the toolchain's
own out-of-the-box config, the same "opt-in strict rules" posture `.swiftlint.yml` above takes); `swift format
lint --strict --recursive Sources` genuinely picks up `.swift-format` with **no `--configuration` flag needed**
(SwiftPM discovers a `.swift-format` file at the package root automatically) and genuinely enforces it — confirmed
by a deliberate violation (an undocumented public `init()`) failing with `error:
[AllPublicDeclarationsHaveDocumentation] add a documentation comment for 'init'`, then passing clean once
documented. `swift format --version` itself unhelpfully reports `main` (not a semver) on this toolchain — `swift
format` is bundled with the Swift toolchain, not installed as its own versioned dependency, so there is no
separate version for this skill to look up or pin (unlike `swiftlint`/`swiftformat` below).

### `.swiftformat` (when `formatter: swiftformat` — **unverified locally**, see Step 2)

Template: `templates/swiftformat/.swiftformat` — read it in full before filling placeholders

This is the third-party nicklockwood/SwiftFormat tool's own line-based config format (distinct from Apple's
`swift-format` JSON above, despite the similar name) — every flag here is `swiftformat`'s documented CLI option
spelled without its leading `--`. Not run against a real `swiftformat` binary while building this skill (no
`brew`, Step 2's caveat) — treat the flag names/values as a starting point, not a confirmed-working config, and
re-verify once `swiftformat` is actually installable in the environment this scaffold targets.

## Step 8 — Reference template: `.spi.yml` (only when `publish: yes`)

Template: `templates/common/.spi.yml` — read it in full before filling placeholders

This is the Swift Package Index's own build-configuration file (https://swiftpackageindex.com) — it tells the
index which target(s) to build DocC documentation for when the package is submitted there. It has no bearing on
`swift build`/`swift test` locally or in CI; omit the file entirely when `publish: no` (Step 2), since a
closed-source package is never submitted to the public index. Confirmed the DocC generation this file's
`documentation_targets` key implies (`swift package generate-documentation --target <Name>
--transform-for-static-hosting`) succeeds locally against this skill's own scaffold regardless of the `publish`
answer — see Step 10's quirks for the exact command and its default output location.

## Step 9 — Reference template: `sonar-project.properties` (only when `sonar` is not `none`)

Template: `templates/common/sonar-project.properties` — read it in full before filling placeholders

- `sonar.organization` is only meaningful for `sonar: cloud` (SonarCloud) — omit that line entirely for `sonar:
  self-hosted` unless the user's self-hosted server also has organizations enabled (Step 2).
- `sonar.coverageReportPaths` points at a SonarQube Generic Coverage Format XML file — **this skill does not
  generate that file itself**; it is produced by converting `xcrun llvm-cov export` output (Step 10's coverage
  quirk) via `slather coverage --sonarqube-xml` or SonarSource's own `xccov-to-sonarqube-generic.sh` script,
  typically as a CI step (`iru-setup-swift-github-workflows` wires exactly that). Note this
  explicitly in the final report so the user doesn't expect `sonar-project.properties` alone to make a local
  `sonar-scanner` run report coverage.
- `sonar.swift.swiftLint.reportPaths` (the Swift analyzer's own key — a bare `sonar.swiftlint.reportPaths` is
  not a property SonarQube reads and is silently ignored) similarly expects a `swiftlint lint --reporter json >
  swiftlint.json` run to have already produced that file — also a CI/manual step this skill doesn't run itself.
- No `sonar.sourceEncoding` line is needed the way the Java/Android templates carry one — SwiftPM/Xcode source is
  UTF-8 only; there's no encoding ambiguity for the scanner to resolve.

## Step 10 — `Package.resolved` policy note

This skill's own verification run (Step 12) generates a `Package.resolved` file the moment `swift build`/`swift
test` first resolves the `swift-docc-plugin` dependency (Step 5) — but this skill does **not** decide whether that
file gets committed. That decision, and the actual `.gitignore` entry either way, belongs to the
`iru-setup-swift-gitignore` skill's own `package-resolved: commit|ignore` input:
that skill's recommended default is **ignore** for a library (`flavor: library`) — a library's own
`Package.resolved` only pins versions for its own development/test builds, never for a downstream consumer
(SwiftPM always re-resolves against the *consumer's* manifest, ignoring the library's own lockfile) — versus
**commit** for an app, where pinning the exact resolved graph matters for reproducible builds. Mention this
explicitly in the final report and point at `iru-setup-swift-gitignore` rather than writing a root `.gitignore`
entry for it here — this skill, like its Java/TypeScript/Android siblings, never touches the repository's
`.gitignore` itself.

No `.github/CODEOWNERS` file is written by this skill — code ownership is a repository/organization policy
decision outside a library-scaffolding skill's scope, and this catalog has no shared convention pushing one from
here (unlike, say, a shared `sonar-project.properties`/`.spi.yml` template, which every consumer of this house
pattern is expected to want).

## Step 11 — Resolve every placeholder

One consolidated resolution table for every `<placeholder>` used across Steps 5–9 — cross-reference this when
filling any template above:

| Placeholder | Source |
|---|---|
| `<package-name>` | Step 2 |
| `<Name>` | Derived from `<package-name>` per Step 2's PascalCase rule |
| `<ios-min-major>`, `<macos-min-major>` (and the equivalent for any other selected Apple platform) | Step 2's `min-deployment-targets`; omitted per-platform if that platform wasn't selected, and the whole `platforms:` key omitted if only `linux` was selected |
| `<swift-docc-plugin-version>` | Step 4 |
| `<Name>` and `<package-name>` in `Sources/<Name>/<Name>.docc/<Name>.md` (Step 6's DocC landing page) | Same values as above — the ``<Name>Example`` topic entry names the placeholder type Step 6 writes, and the catalog directory is `Sources/<Name>/<Name>.docc/` |
| `<copyright-year>` | The current year |
| `<developer-name>`, `<license-name>`, `<license-url>` | Step 2; if "No license", drop the entire header comment block instead of leaving empty lines |
| `<sonar-project-key>`, `<sonar-organization>`, `<sonar-host-url>` | Step 2's `sonar` answer; omit `sonar-project.properties` entirely if `sonar: none`, and omit just the `sonar.organization` line for `sonar: self-hosted` without organizations enabled |

`publish: no` omits `.spi.yml` (Step 8) entirely, with no placeholders of its own beyond `<Name>`.

## Step 12 — Write the files

Apply Step 1's per-file decision across every file listed in Steps 5–9: write each file that didn't exist
(*created*); for an existing file, merge per **Update** (show the user the diff first, e.g. `git diff --no-index
<current> <draft>`, and write on approval — *updated*), leave it untouched per **Keep as is** (*kept as is*), or
overwrite it from the template per **Replace** (*replaced*). Run Step 5's `swift package init` only when
`Package.swift` doesn't exist yet — when it exists and was resolved Update or Keep, skip the `init` and work from
the existing manifest; when it was resolved Replace, write Step 5's template over it directly (still without
`init`, which is designed for an empty directory and would also emit its own `.gitignore`/sources). Create every
intermediate directory (`Sources/<Name>/`,
`Sources/<Name>/<Name>.docc/`, `Tests/<Name>Tests/`) as needed — don't touch any other file already inside a
directory this skill writes into.

## Step 13 — Verify

Run through the `iru-gate-runner` agent (per this catalog's convention: gates run through it rather than inline
Bash, so the caller gets a compact pass/fail summary instead of raw `swift build`/`swift test` output):

1. `swift build` — compiles the package, including resolving `swift-docc-plugin` over the network on a first run
   (Step 5's note). **Note explicitly to the user**: this first invocation can take noticeably longer than a
   subsequent one purely from that dependency fetch, independent of the package's own compile time.
2. `swift test` — runs both the Swift Testing and XCTest examples from Step 6 in one invocation; treat a
   non-zero exit, or console output reporting fewer than 2 total tests, as a failure worth reporting (the
   `iru-swift-test` skill's own "0 tests matched" convention — a selector or misconfigured target silently
   running nothing is a failure mode, not a clean pass).

If either step fails, report the actual `swift build`/`swift test` error to the user rather than guessing at a
fix — a network-blocked `swift-docc-plugin` fetch, a platform/deployment-target mismatch, or a missing Xcode
Command Line Tools installation are all common first-run causes and are not, by themselves, defects in this
skill's templates.

### Known quirks / verification notes (from building and verifying this skill against Swift 6.4/Xcode 27, September 2026)

- **`swift package init --type library --name <name>` does not PascalCase a hyphenated name** — passing
  `my-example-lib` directly produces `Sources/my_example_lib/my_example_lib.swift` and
  `Tests/my_example_libTests/`, converting hyphens to underscores for the target/directory/file names while
  keeping the hyphenated form verbatim as `Package(name: "my-example-lib")`. Passing the already-PascalCase
  `<Name>` (`MyExampleLib`) instead avoids this — confirmed clean `Sources/MyExampleLib/`,
  `Tests/MyExampleLibTests/` output. Step 5 above always uses `<Name>` for exactly this reason.
- **`swift package init --type library` generates only a Swift Testing example, no XCTest example**, on this
  toolchain (Swift 6.4/Xcode 27) — the default `Tests/<Name>Tests/<Name>Tests.swift` uses `import Testing` /
  `@Test func example() async throws {}` exclusively. This skill's Step 6 adds the XCTest file itself; don't
  assume a future toolchain's own default scaffold will keep matching this exactly.
- **Default tools-version is whatever the active toolchain reports, not a fixed value** — this environment's
  `swift package init` wrote `// swift-tools-version: 6.4` (matching `swift --version`'s `Apple Swift version
  6.4`), not `6.0` or any other fixed number. This skill always overwrites it to exactly `// swift-tools-version:
  6.0` (Step 5) — the minimum that supports `swiftLanguageModes:` — rather than keeping whatever the local
  toolchain happened to default to, so a package built with this skill on a newer toolchain doesn't silently
  require a newer minimum Swift than intended.
- **`Package(...)`'s parameter order is enforced by the compiler, not just a style convention** — confirmed
  `dependencies:` placed after `swiftLanguageModes:` fails to parse with `error: argument 'dependencies' must
  precede argument 'swiftLanguageModes'`. The order in Step 5's template (`name`, `platforms`, `products`,
  `dependencies`, `targets`, `swiftLanguageModes`) is the one verified to build clean.
- **`.linux` is not a valid `SupportedPlatform` case** — confirmed `platforms: [.linux]` fails with `error: type
  'Array<SupportedPlatform>.ArrayLiteralElement' (aka 'SupportedPlatform') has no member 'linux'`. Linux support
  is implicit (no manifest entry needed or possible) — Step 2/Step 5 both document this.
- **`swift-docc-plugin` resolution needs network access on a first run** — confirmed `swift build` fetches both
  `swift-docc-plugin` and its transitive `swift-docc-symbolkit` dependency straight from GitHub before compiling;
  there is no vendored/offline fallback baked into this skill's template.
- **The new Swift Build system (this toolchain's default) reshapes `.build/` layout** — confirmed `.build/debug`
  is a **symlink** to `.build/out/Products/Debug/`, not a real directory as on older toolchains/Linux (which use
  `.build/debug/` directly, or `.build/x86_64-apple-macosx/debug/` for a triple-qualified build). The exact paths
  this skill's own verification used and confirmed working:
  - Test binary: `.build/debug/<Name>Tests.xctest/Contents/MacOS/<Name>Tests` (a macOS `.xctest` bundle; the
    symlink resolves this transparently, no need to chase it manually).
  - Coverage profile data: `.build/debug/codecov/default.profdata` (written by `swift test
    --enable-code-coverage`, again through the symlink).
  - `xcrun llvm-cov export -format=lcov <test-binary> -instr-profile <profdata>` **without** an
    `-ignore-filename-regex` includes SwiftPM's own synthesized `test_entry_point.swift` (under
    `.build/out/Intermediates.noindex/...`) and every file under `Tests/` in the LCOV output alongside the real
    `Sources/` coverage — confirmed by diffing the export with and without the flag. Pass
    `-ignore-filename-regex='\.build|Tests'` to get a `Sources/`-only report; `iru-swift-coverage` handles this
    itself when asked to report coverage, so a caller invoking that skill instead of raw `llvm-cov` doesn't need
    to remember this flag.
- **`swift format lint --strict --recursive Sources` auto-discovers `.swift-format` with no `--configuration`
  flag** — confirmed a stricter-than-default rule (`AllPublicDeclarationsHaveDocumentation: true`) in the
  committed `.swift-format` genuinely fired against an undocumented `public init()`, then passed clean once
  documented — the config file is not a no-op decoration.
- **`swift package generate-documentation --target <Name> --transform-for-static-hosting` writes to
  `.build/plugins/Swift-DocC/outputs/<Name>.doccarchive` by default, not to whatever directory
  `--allow-writing-to-directory` names** — confirmed: that flag only *grants permission* to write there if the
  plugin chooses to; without an explicit `--output-path <dir>`, the archive lands under `.build/plugins/` instead.
  Pass `--output-path <dir>` explicitly (in addition to `--allow-writing-to-directory <dir>`) whenever the
  generated documentation needs to land in a predictable location (e.g. a `docs/api/` directory a CI workflow
  later publishes) — confirmed `--output-path docs` places `index.html`, `documentation/`, `data/`, etc. directly
  under `docs/` as expected once added.
- **SwiftLint, the third-party `swiftformat` tool, `xcodegen`/`tuist`/`xcbeautify`/`periphery`, and `slather` are
  all unverified locally** — this environment has no `brew`, and installing any of them from source was out of
  scope for verifying this skill. `.swiftlint.yml` (Step 7) and `.swiftformat` (Step 7, only when `formatter:
  swiftformat`) are genericized from each tool's own documented config format but were never actually run against
  a real binary. `swift format` (the toolchain-bundled formatter) **is** verified, per the point above.
- Everything above was exercised end-to-end (`swift build`, `swift test --enable-code-coverage`, `xcrun llvm-cov
  export -format=lcov`, `swift format lint --strict --recursive Sources`, `swift package
  generate-documentation --target <Name> --transform-for-static-hosting --output-path docs`) in
  `$TMPDIR/iru-verify/swift/library` against a package named `ExampleLibrary` (package name and `<Name>` made
  identical for that run, plus a second ad hoc check confirming the `package-name`-with-hyphens/`<Name>`-PascalCase
  split itself builds clean) with `platforms: ios, macos` (`.iOS(.v17)`, `.macOS(.v14)`) and `formatter:
  swift-format` — see that run's own files for the exact working `Package.swift`/`.swift-format`. `formatter:
  swiftformat`, `sonar-project.properties`'s coverage/swiftlint report paths, and `.spi.yml`'s actual submission
  to the Swift Package Index are **unverified locally** — each is called out individually above; re-verify before
  relying on them in a real repository.

## Step 14 — Report

Summarize what was generated: the resolved `package-name`/`<Name>`, the selected `platforms` with their
`min-deployment-targets`, the license chosen (or "none"), and the repository info inferred in Step 3.

State explicitly what was included versus omitted, and why:

- **`open-source`**: yes/no, as resolved in Step 2.
- **`publish`**: yes/no — if `yes`, `.spi.yml` was included; if `no`, it was omitted (note that this has no
  bearing on whether the package can still be used as a git-URL dependency — only on whether it's configured for
  submission to the Swift Package Index).
- **`sonar`**: `cloud`/`self-hosted`/`none` — if `cloud`/`self-hosted`, `sonar-project.properties` was included
  with the resolved `sonar.organization`/`sonar.projectKey`/`sonar.host.url`, and a reminder that
  `sonar.coverageReportPaths`/`sonar.swift.swiftLint.reportPaths` both expect files a CI step still needs to produce; if
  `none`, note that this is expected when the project isn't open source unless the user explicitly chose it.
- **`formatter`**: `swift-format` (verified) or `swiftformat` (unverified locally) — which config file was
  written and whether it's confirmed working.

Then restate the mode announced in Step 1 (from scratch vs updating an existing package) and report, per file in
Steps 5–9, the action actually taken — **created / updated / replaced / kept as is** — and whether Step 13's two
verification commands succeeded. For every file kept as is, list each concrete mismatch with this run's choices
(e.g. a leftover `sonar-project.properties` after `sonar: none`, an old tools-version). If `visibility` or `ci`
arrived via `args`, say how they shaped the `sonar` recommendation (and, for `ci: no` with Sonar configured, that
no CI step sends reports). If Step 1's existing files were replaced, explicitly list what could have been lost — any target, dependency, or platform beyond what Steps 5–9's
templates show — and tell the user to check `git diff` for anything they need to re-add.

Finish with an explicit **Warn explicitly** block:

- **The user must review every generated file before building, committing, or publishing.** Confirm the license
  choice matches an actual `LICENSE` file (or that none is intended — suggest the `iru-check-license` skill to
  generate one and backfill source headers otherwise), that the inferred repository URL is correct, and that
  `swift build` succeeds before relying on this scaffold.
- If `sonar: cloud` or `sonar: self-hosted` was chosen, a `SONAR_TOKEN` (or equivalent) secret and an actual
  SonarCloud/SonarQube project matching `sonar.projectKey` still need to exist, and a CI step still needs to
  produce `sonarqube-generic-coverage.xml`/`swiftlint.json`, before a `sonar-scanner` run will succeed or report
  anything meaningful — this skill only writes `sonar-project.properties`, it does not run a scan itself.
- If `publish: yes` was chosen, `.spi.yml` alone doesn't submit the package to the Swift Package Index — that's a
  one-time manual step on swiftpackageindex.com the user still needs to do.
- No root `.gitignore` was written by this skill (`swift package init`'s own default was overwritten by Step 5's
  `Package.swift` rewrite but its `.gitignore` was left as `swift package init` generated it) — the
  `iru-setup-swift-gitignore` skill should be run next to confirm `.build`/`DerivedData`/`Package.resolved`
  (per Step 10's commit/ignore policy) are all handled correctly for this library.
- SwiftLint (`.swiftlint.yml`), the third-party SwiftFormat tool (`.swiftformat`, only if `formatter: swiftformat`
  was chosen), and `.spi.yml`'s actual Swift Package Index submission are **unverified locally** — spot-check
  whichever of them applies before trusting the generated scaffold to actually work end-to-end.
- The `swift-docc-plugin` version (Step 4) was resolved via a run-time lookup and may already be stale by the
  time this report is read — re-check before a first real release.
