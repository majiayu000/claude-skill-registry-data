---
name: iru-swift-docc
description: Audit given Swift type(s)/file(s) for complete DocC coverage — a `///` summary for every public/open type (struct/class/enum/protocol/actor), initializer, property, method, subscript, and enum case within the discovered documentation bar, with `- Parameters:` (or `- Parameter x:` for a single parameter, using the parameter's *internal* name), `- Returns:`, `- Throws:`, and `- Note:`/`- Important:` callouts where applicable — plus a DocC catalog landing page (`Sources/<Target>/<Target>.docc/<Target>.md`, starting with `# ``<Target>``` and a `## Topics` section) for every target touched, creating one if it's missing — generate any missing or incomplete DocC comments grounded in the actual code and current changes, audit actual completeness via `swift package dump-symbol-graph` (parsing each symbol's `docComment` presence in the emitted `*.symbols.json`, since DocC's own build does **not** warn on missing documentation by default), then run `swift package generate-documentation --target <Target> --warnings-as-errors` (or `xcodebuild docbuild -scheme <Scheme> -destination 'platform=macOS'` for an app/Xcode project) to confirm the result is structurally well-formed. Invoke as `/iru-swift-docc <Type1,Type2,...>` (or file paths), or `/iru-swift-docc` with no argument to scope to types touched by uncommitted changes plus commits on the current branch not yet on the base branch. Works against any Swift package or Xcode app project — it discovers the project's own documentation bar from a `.swiftlint.yml`'s `missing_docs` opt-in rule, a `.spi.yml`'s `documentation_targets`, and observed practice, rather than assuming a fixed style. Equivalent to `iru-java-javadoc`/`iru-typescript-tsdoc`/`iru-android-dokka` for the Swift stack. Use whenever the user wants DocC completeness checked and filled in for specific types, instead of relying on a full doc build to surface gaps (which, like Dokka, does not fail or warn on undocumented public members by default).
model: sonnet
---

# Swift DocC

Make sure a set of Swift declarations — and the DocC catalog(s) of the target(s) they live in — carry complete,
well-formed documentation comments, filling in whatever is missing, then prove the result actually builds via the
project's own DocC tooling. This skill only adds/completes documentation comments (including creating a missing
`<Target>.docc/<Target>.md` catalog landing page) — it does not change behavior, signatures, or non-comment code.
Test declarations (anything under a package's `Tests/` source root, or an Xcode `*Tests`/`*UITests` target) are
out of scope for documentation requirements — they don't need doc comments added, even if named explicitly — but
any documentation a test file already has must be left as-is; never strip or "clean up" existing comments in test
code. It makes no assumptions about this being any particular repository — discover the project's actual
conventions and DocC setup fresh each run.

## Step 1 — Determine scope

- **Argument provided** (comma-separated type names or file paths): resolve each to its file. If given a simple
  type name, locate it via `find`/`grep` across every target's main source root (`Sources/<Target>` for a Swift
  package, or the app/library target's source group for an Xcode project) rather than guessing the target. If a
  resolved file turns out to live under a `Tests/` directory or a `*Tests`/`*UITests` Xcode target, drop it from
  the scope audited/generated in Steps 3-5 — say so in the Step 7 report rather than silently ignoring it — since
  test code carries no documentation requirement here.
- **No argument**: default to every main-source `.swift` file touched by uncommitted changes plus commits on the
  current branch not yet on the base branch, same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a` if unclear; ask
  the user only if genuinely ambiguous). Filter the changed-file list to a main Swift source root — skip `Tests/`,
  `.build/`/`DerivedData/` output, `*.docc` catalog resources themselves (Step 4 handles those separately), and
  non-Swift files.
- If the resulting scope is empty (no argument and no relevant changes), tell the user there is nothing to
  document and stop.
- From the in-scope files, derive the distinct set of targets involved: resolve the project shape first —
  `Package.swift` at the repository root or a nearer ancestor (Swift Package Manager) or an `.xcodeproj`/
  `.xcworkspace` (Xcode app project) when no `Package.swift` exists, the same resolution `iru-swift-code-quality`/
  `iru-swift-test`/`iru-swift-coverage` use — then map each in-scope file to the SPM target (its `Sources/<Target>`
  ancestor) or Xcode target it belongs to. These targets feed Step 4, which checks each one has a DocC catalog
  landing page.

## Step 2 — Discover this project's actual documentation bar before auditing

Don't assume a fixed documentation scope — discover it from the project itself, since projects vary on whether
`internal`/`private` members need documentation:

- Check for a contributor guide (`CLAUDE.md`, `AGENTS.md`, a top-level `README`, or a `CONTRIBUTING` file) for any
  stated documentation convention.
- Check `.swiftlint.yml`/`.swiftlint.yaml` for the `missing_docs` rule — it is **opt-in**, so first confirm it's
  actually listed under `opt_in_rules` (or `only_rules`) before trusting its configuration. When active, its
  value is a per-access-level severity map, e.g.:
  ```yaml
  opt_in_rules:
    - missing_docs
  missing_docs:
    warning: [open, public]
    error: [package]
    excludes_extensions: true
    excludes_inherited_types: true
  ```
  Read which access levels appear under `warning`/`error` (that set *is* the enforced bar — an access level absent
  from both arrays is not checked), and note `excludes_extensions`/`excludes_inherited_types` if present (SwiftLint
  defaults both to `true`), since a project that flips either to `false` also expects extension members or
  protocol-conformance members it inherited to carry their own documentation.
- Check `.spi.yml` (the Swift Package Index build-configuration file, if the project publishes there) for a
  `builder.configs[].documentation_targets` list — the targets it names are the ones this project has explicitly
  opted into publishing documentation for, which is a strong signal of the intended completeness bar for those
  targets specifically (a target absent from the list may still be documented, but isn't the project's stated
  priority).
- If none of the above give a clear answer, skim 2-3 existing types near the ones in scope to see empirically
  whether the project already documents `internal`/`private` members or only `public`/`open` ones — treat that
  observed practice as the bar, since a stated convention looser than what the codebase actually does would leave
  real gaps unaddressed.
- Reconcile any conflict between a stated/configured convention and the actually-enforced/observed one by
  following the **stricter** of the two.

Skim a couple of existing, well-documented types in the project (prefer ones structurally similar to what's in
scope) to internalize the exact phrasing conventions before writing new documentation: person and tense used,
whether summary sentences end in a period, whether a longer explanation follows the summary as a separate
paragraph, the `- Parameters:`/`- Returns:`/`- Throws:` ordering, and whether `` `SquareBracket` `` vs. plain
double-backtick symbol links are used for cross-references. If the project has no existing documentation to learn
from, fall back to standard DocC convention:

- **Summary first**: one concise sentence, third person present tense, followed by a blank `///` line then any
  longer discussion.
- **`- Parameter name: description`** for a single parameter, or a `- Parameters:` block with one `- name:
  description` bullet per parameter for two or more — **`name` must be the parameter's internal name, never its
  external label** (see "Known quirks" — DocC warns and, under `--warnings-as-errors`, fails the build on the
  external form).
- **`- Returns: description`** — one sentence describing the returned value; omitted for a `Void`/no-return
  function.
- **`- Throws: description`** — one per distinct error type the implementation can actually throw, or that is
  documented on a `throws`/`rethrows` function.
- **`- Note:`/`- Important:`/`- Warning:`** — DocC's built-in Aside callouts, used for a caveat or cross-cutting
  detail that doesn't belong in the one-line summary (concurrency/thread-safety notes, a coordinate-system
  convention, a deprecation heads-up not yet formalized as `@available(*, deprecated)`).
- **` ``OtherSymbol`` `** (double backticks) — DocC's own symbol-link syntax for cross-references to another
  documented symbol in the same module or an imported one, instead of a bare name in single backticks or plain
  text.
- **`@available(*, deprecated, ...)`** — carried over verbatim on a declaration that already has it; never add it
  new — that's a decision only the code owner makes.

## Step 3 — Audit each in-scope declaration

Read the full file, then check every one of the following is present, non-empty, and actually describes the
member's purpose (not just restates its name), scoped per the bar established in Step 2:

- **Type-level**: a doc comment on the struct/class/enum/protocol/actor itself.
- **Initializers**: every `init`/`init?`/`init(...) throws` within scope, with a `- Parameter(s)` entry per
  parameter (internal name) and `- Throws:` for any failable/throwing initializer.
- **Properties**: every stored and computed property within the discovered scope, including a custom
  getter/setter whose behavior isn't obvious from the type alone.
- **Methods**: every instance/static/class method and subscript within scope, with a `- Parameter(s)` entry per
  parameter, `- Returns:` unless the return type is `Void`, and `- Throws:` for every error the implementation can
  actually throw.
- **Enum cases**: a doc comment on each case whose meaning isn't self-evident from its name alone, and on any
  associated values it carries.
- **Nested/inner types**: recurse into these with the same checks as top-level types.
- **Extension members**: a `///` comment on a member declared in an `extension` block the same as any other
  member — the default `swift package dump-symbol-graph` output (no `--emit-extension-block-symbols` flag)
  attaches these directly to the extended nominal type's symbol entry (`pathComponents` reads `["Widget",
  "memberName"]`, not a separate extension-block entry), confirmed locally, so Step 6's audit finds them exactly
  like any other member of that type with no extra handling needed — this only changes for an extension of a type
  declared in a *different* module, where `--emit-extension-block-symbols` (or `--include-spi-symbols` for an
  `@_spi` extension) may be needed to see the member at all.
- **Protocol-conformance/`@Observable`/property-wrapper members**: same checks as any other member; only skip a
  member the project's own bar (Step 2's `excludes_inherited_types`, or an explicit `///` `` `` `- Note:`
  cross-reference to the protocol requirement's own doc) says is intentionally inherited without a local comment.

For each item found incomplete or missing entirely, record: the member, what's missing (whole comment vs. a
missing `- Parameter`/`- Returns`/`- Throws` entry), and its current access level.

## Step 4 — Ensure each touched target has a DocC catalog landing page

DocC's own documentation-coverage build (Step 6) never fails on a missing catalog — a target with no `.docc`
catalog still "builds" a bare, uncurated symbol list — so this step is this skill's own requirement, not something
a failing build would ever catch. For each target derived in Step 1:

- Look for `Sources/<Target>/<Target>.docc/` (SPM) or the equivalent `.docc` catalog folder inside the Xcode
  target's source group. If it exists, read its landing page (conventionally `<Target>.md`, matching the
  catalog's own folder name) and confirm it starts with a `# ``<Target>``` heading (double-backtick module-symbol
  link, exactly as `swift package init` generates for a fresh catalog) and has a non-empty `## Overview` (or
  equivalent introductory prose) plus a `## Topics` section — treat a missing file, a missing `# ``<Target>```
  heading, or a `## Topics` section with no entries under it the same as a missing catalog.
- If it's missing or incomplete, create/complete it:
  ```markdown
  # ``<Target>``

  <One or two sentences summarizing what this target provides.>

  ## Overview

  <A short paragraph of additional context, grounded in what the in-scope types actually do.>

  ## Topics

  ### Essentials

  - ``TypeOne``
  - ``TypeTwo``
  ```
  Base the summary and the `## Topics` entries on the in-scope types' actual responsibilities; for an existing
  catalog gaining new in-scope types, add them under the existing `## Topics` structure (creating a new subsection
  only if the new types introduce a concept not covered by an existing one) rather than replacing what's there.
- If the target has no `.docc` folder at all, create `Sources/<Target>/<Target>.docc/<Target>.md` at that path —
  a bare catalog folder containing only this one landing page is a valid, buildable DocC catalog; nothing else is
  required to wire it in (unlike Dokka's `includes.from(...)`, DocC auto-discovers any `.docc` folder inside a
  target's source directory with no build-file edit needed).

## Step 5 — Generate the missing documentation

For every gap found in Step 3, write the documentation directly grounded in:

- The member's actual implementation (parameter usage, return expression, thrown errors, a computed property's
  actual accessor logic) — read the function/property body, don't infer purely from the signature/name.
- Any current uncommitted/branch changes to that member (`git diff` / `git log -p` for that file/hunk if the
  member was just added or modified) — if the change altered behavior, the new documentation must describe the
  current behavior, not stale prior behavior a name alone might suggest.
- The phrasing conventions gathered in Step 2 — match voice, tense, and callout ordering/style exactly so the new
  comments are indistinguishable from hand-written ones in this codebase, and always document the parameter's
  *internal* name (see Step 2 and "Known quirks").

Apply the edits with the Edit tool. Do not modify code logic, signatures, formatting outside the added comments,
or reorder members — this skill only adds/completes documentation comments (and, per Step 4, the DocC catalog
landing page).

## Step 6 — Verify completeness and that the docs actually build

DocC's own build does not fail or warn on an undocumented public member by default (see "Known quirks"), so
verifying "it builds" and verifying "it's complete" are two different checks — do both:

**6a. Audit completeness — the primary mechanism, always run this:**

```bash
swift package dump-symbol-graph --pretty-print --minimum-access-level public
```

This builds the target(s) and writes one `<Target>.symbols.json` per module under `.build/out/symbolgraph/`
(there is no `--output-path` flag on this subcommand — confirmed locally against Swift 6.4; the path is fixed and
printed as `Files written to <path>` on success). Parse each file's `symbols[]` array: a symbol whose object has no
`docComment` key at all is undocumented; one that has it is documented (its `docComment.lines[].text` is the raw
comment text, useful for spot-checking phrasing). Match each `pathComponents` entry (e.g. `["Widget",
"increment(by:)"]`) back to the member recorded in Step 3. Pass `--minimum-access-level` matching Step 2's
discovered bar (`public` by default; widen to `internal`/`private` if the project's bar requires it). This is the
mechanism this skill relies on for the actual completeness gate — confirmed locally to precisely flag every
deliberately undocumented member in a test fixture and none of the documented ones.

**6b. Cross-check with DocC's own experimental coverage report (optional, corroborating):**

```bash
swift package --allow-writing-to-directory <out-dir> generate-documentation --target <Target> \
  --experimental-documentation-coverage --coverage-summary-level detailed --output-path <out-dir>
```

Confirmed locally: this prints a per-symbol table (`Abstract?` / `Curated?` / `Code Listing?` / `Parameters`
columns) to the console and writes a machine-readable `documentation-coverage.json` (one object per symbol, with a
boolean `hasAbstract` field and a `referencePath`) into `<out-dir>`. `hasAbstract: false` lined up exactly with the
`dump-symbol-graph` findings in verification. Treat this as a corroborating cross-check, not the primary source of
truth — the flag and its output shape are explicitly labeled **experimental** by DocC itself and may change
between toolchain versions; 6a's symbol-graph parse is the mechanism to actually rely on.

**6c. Verify the docs build cleanly (structural correctness, not completeness):**

For a Swift package library target:

```bash
swift package generate-documentation --target <Target> --warnings-as-errors
```

For an app or a project that only has an Xcode project/workspace:

```bash
xcodebuild docbuild -scheme <Scheme> -destination 'platform=macOS'
```

(substitute the platform destination for an iOS/watchOS/tvOS/visionOS target, e.g. `platform=iOS Simulator,name=<a
booted simulator>`; confirmed locally this also works unmodified against a plain SwiftPM package with no
`.xcodeproj` — Xcode auto-generates a scheme named after the package). This fails only on structural problems —
malformed doc-comment syntax, an unresolved `` ``SymbolLink`` ``, or (per the quirk below) a `- Parameter` entry
naming the wrong identifier — never on missing documentation. If it fails or warns, fix the offending comment(s)
and re-run until it succeeds. Warnings tied to files outside the current scope are pre-existing — note them in the
report but don't fix them unless the user asks.

If 6a/6b turn up gaps that Step 3's manual read missed (e.g. a synthesized member, or one added by a macro), treat
them the same as any other Step 3 finding and go back through Step 5 for them before re-running Step 6.

## Step 7 — Report

Per type in scope, state: how many members were already fully documented, how many gaps were found and filled
(name each, with its kind), and the symbol-graph audit result (Step 6a: total symbols checked vs. undocumented
count, per target). Separately, state per target whether its DocC catalog landing page already existed and was
complete, was extended, or was newly created. Report the final doc-build result (Step 6c: pass, or the exact
warning/error text and declaration names that failed) and, when 6b was run, the coverage percentages it reported.
State the output location used for verification (`.build/plugins/Swift-DocC/outputs/<Target>.doccarchive` for a
plain `generate-documentation` run with no `--output-path`, the given `--output-path` directory when one was
passed, or `<DerivedData>/Build/Products/<Configuration>/<Scheme>.doccarchive` for `xcodebuild docbuild`). If any
argument resolved to test code (Step 1), name it and note it was excluded since test code carries no documentation
requirement here. If any out-of-scope pre-existing doc-build warning surfaced in Step 6c, mention it separately as
a follow-up rather than silently leaving it out of the report.

Do not run a full documentation-site publish beyond what Step 6 needs, fix SwiftLint/`swift format`/Periphery
issues unrelated to documentation, or add/modify tests — those are `iru-swift-code-quality` and
`iru-swift-generate-all-tests`'s jobs respectively, not this skill's.

## Known quirks / verification notes

Verified locally in `$TMPDIR/iru-verify/swift/docc/Demo` (`swift package init --type library --name Demo`, Swift
6.4 / Xcode 27.0, `swift-docc-plugin` `from: "1.4.0"` resolved to the actual latest release, **1.5.0** — looked up
via `gh api repos/swiftlang/swift-docc-plugin/releases/latest`; `swift-docc-symbolkit` resolved transitively at
1.0.0), a `Widget` public struct with one documented and one deliberately undocumented property/method each, and a
`Sources/Demo/Demo.docc/Demo.md` catalog:

- **DocC does NOT warn on missing documentation by default — confirmed, this is the central quirk this skill
  exists to work around.** With two deliberately undocumented public members (`var undocumentedCount: Int` and
  `func reset()`) left in place, both `swift package generate-documentation --target Demo` and the same command
  with `--warnings-as-errors` completed successfully (exit `0`, "Finished building documentation") — no warning,
  no error, nothing in the console output naming either member. A doc build succeeding proves nothing about
  completeness; only the symbol-graph audit (Step 6a) or the experimental coverage report (Step 6b) actually
  catches this.
- **`swift package dump-symbol-graph` is the audit mechanism this skill's Step 6a relies on, and it works exactly
  as needed — verified.** No `--output-path` flag exists on this subcommand (confirmed via `-help`); output always
  lands at `.build/out/symbolgraph/<Module>.symbols.json`, one file per module, printed as `Files written to
  <path>`. Parsing the JSON's `symbols[].docComment` key presence correctly identified both deliberately
  undocumented members and none of the documented ones, matching Step 6b's `hasAbstract` output symbol-for-symbol.
  Default flags (`--minimum-access-level public`, `--omit-extension-block-symbols`) already associate a same-module
  `extension`'s members directly with the extended nominal type's `pathComponents` (verified with a
  `WidgetExtensions.swift` adding both a documented and undocumented extension method — both appeared as
  `["Widget", "<method>"]` entries, not as a separate extension-block symbol), so no extra flag is needed for the
  common case of extending a type declared in the same target.
- **`--experimental-documentation-coverage` (Step 6b) is real, useful, and exactly as labeled — experimental —
  verified.** `swift package --allow-writing-to-directory <dir> generate-documentation --target Demo
  --experimental-documentation-coverage --coverage-summary-level detailed --output-path <dir>` printed a
  per-symbol console table (columns: Abstract?, Curated?, Code Listing?, Parameters) and wrote
  `documentation-coverage.json` to `<dir>` with a `hasAbstract` boolean per symbol — both correctly showed `false`
  for the same two undocumented members the symbol-graph audit found. Treat it as a corroborating cross-check
  only, per its own "(EXPERIMENTAL)" label in `--help`.
- **`- Parameter <name>:` must use the parameter's internal name, not its external label — a real, verified
  quirk.** Documenting `func increment(by amount: Int)` as `- Parameter by: ...` (the external label) produces
  `warning: External name 'by' used to document parameter` with a suggested fix (`Replace 'by' with 'amount'`) at
  build time; under `--warnings-as-errors` this becomes a hard failure. Always document the internal name
  (`amount` here), even when only an external label is visible at the call site.
- **A `--warnings-as-errors` failure can surface a second, confusing, unrelated-looking error — verified.** When
  the underlying `docc convert` step fails, the `swift-docc-plugin`'s own file-move step also errors (observed:
  `error: Error Domain=NSCocoaErrorDomain Code=4 "'Demo.doccarchive' couldn't be moved to 'outputs' because either
  the former doesn't exist..."`), printed *before* the actual root-cause diagnostic further down the output. Always
  read past that move-failure line to the `error:`/`warning:` block naming the actual file/line — the move failure
  is a symptom, not the cause.
- **Output directory layout — verified for all three invocation shapes used in this skill:**
  - `swift package generate-documentation --target <Target>` with no `--output-path`: writes the archive to
    `.build/plugins/Swift-DocC/outputs/<Target>.doccarchive` (confirmed by the command's own final "Generated
    documentation archive at:" line).
  - `swift package --allow-writing-to-directory <dir> generate-documentation --target <Target>
    --transform-for-static-hosting --output-path <dir>`: writes a ready-to-host static site directly into
    `<dir>` — top-level `documentation/`, `data/`, `index/`, `css/`, `js/`, `img/`, `favicon.ico`/`.svg`,
    `index.html` — note the *lowercased* module name in path segments (`docs/documentation/demo/...` for a target
    named `Demo`).
  - `xcodebuild docbuild -scheme <Scheme> -destination 'platform=macOS' -derivedDataPath <dd>`: succeeds
    (`** BUILD DOCUMENTATION SUCCEEDED **`) directly against a plain SwiftPM package with no `.xcodeproj` present —
    Xcode auto-generates a scheme matching the package name (confirm with `xcodebuild -list`, which also prints a
    harmless "Failed to load code for plug-in com.apple.dt.DVTCoreDeviceCore"/simulator-device warning block on
    this machine that has no bearing on the docbuild result). The archive lands at
    `<derivedDataPath>/Build/Products/Debug/<Scheme>.doccarchive` (or `Release`/another configuration if
    `-configuration` is passed) — always pass `-derivedDataPath` explicitly rather than relying on Xcode's shared
    DerivedData location, so the archive's path is predictable and doesn't require a Spotlight/`find` search
    afterward.
- **Network need**: the first `generate-documentation`/`--warnings-as-errors` run in a fresh checkout resolves
  `swift-docc-plugin` and its `swift-docc-symbolkit` dependency from GitHub (or the local SPM package cache, if
  warm) — this needs network access (or a pre-populated `~/.swiftpm`/`.build` cache) exactly like any other new
  SwiftPM dependency; `dump-symbol-graph` alone needs no such resolution once the package's own dependency graph
  is already resolved.
- **`swift-docc-plugin` version**: pin `from: "1.4.0"` (the task's floor) in a project's `Package.swift`; look up
  the actual current release at run time via `gh api repos/swiftlang/swift-docc-plugin/releases/latest --jq
  .tag_name` (September 2026 fallback if that call fails: **1.5.0**, the version this skill's own verification
  resolved to).
- **Not independently verified**: `.swiftlint.yml`'s `missing_docs` opt-in rule's exact enforcement/output shape —
  this machine has no Homebrew and no way to install `swiftlint` locally (see `iru-swift-code-quality`'s own
  "Known quirks" section for the same constraint), so its configuration is read and reconciled in Step 2 as
  *input* to this skill's own bar, never run as a second enforcement pass. `.spi.yml`'s
  `documentation_targets` field is documented Swift Package Index convention, not exercised against a real
  SPI-configured project in this verification — read it for signal in Step 2, but don't treat its absence as
  proof a target isn't meant to be documented.
