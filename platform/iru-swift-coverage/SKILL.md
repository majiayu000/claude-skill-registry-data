---
name: iru-swift-coverage
description: "/iru-swift-coverage [scope] - reports Swift line and function coverage for a package (swift test plus llvm-cov) or an Xcode app (xcodebuild plus xccov), scoped to comma-separated files or type names. Optional key: value lines: package-path, kind, xcresult, scheme, destination, target. Reports \"coverage not wired\" instead of a false 0%."
model: haiku
---

# Swift Coverage

Run whichever coverage path a Swift package or Xcode app project actually has wired, and report the exact,
measured line/function coverage percentage for the scope the user cares about. This skill only measures and
reports coverage — it does not add tests or modify source/test code unless asked to as a follow-up (that's
`iru-swift-generate-all-tests`'s job).

## Step 0 — Resolve inputs

`[scope]` is a comma-separated list of file paths (`Sources/Demo/Calculator.swift`) or type simple names
(`Calculator`, `Calculator,Formatter`), or absent (whole package/target report). If the calling skill/prompt
passes explicit `key: value` lines, honor them and skip the matching inference below:

- `kind: package|app` — override the package-vs-app detection in Step 1.
- `xcresult: <path>` — an already-produced `.xcresult` bundle; skip Step 2's `xcodebuild` run entirely and go
  straight to parsing it (Step 3's app path).
- `scheme:`, `destination:`, `target:`/`module:` — override what would otherwise be inferred the same way
  `iru-swift-test` infers them (its Step 3: scheme from `xcodebuild -list` — for `iru-setup-apple-app`'s per-platform
  schemes `<AppName>-iOS`/`-macOS`/`-watchOS`/`-visionOS`, the scheme of the platform whose `Targets/<Platform>/`
  files are in scope; destination from its `resolve_destination` — `platform=<iOS|watchOS|visionOS>
  Simulator,name=<device>,OS=<newest runtime version>` — or `platform=macOS` for a macOS scheme; target from
  `Package.swift`'s test target(s)).
- `package-path: <dir>` — run the **package** path inside that directory (e.g. `Packages/Core`) even though the
  repository is an app: the way to measure an app's local SwiftPM package (see Step 1's rule 5).
- A bar/threshold line (e.g. `bar: 80`) is only used for Step 4's pass/fail wording — it never changes what runs.

## Step 1 — Detect which coverage path is wired

Same detection `iru-swift-test` uses:

```bash
find . -maxdepth 2 \( -name "Package.swift" -o -name "project.yml" -o -name "Project.swift" \
  -o -name "*.xcodeproj" -o -name "*.xcworkspace" \) -not -path "*/.build/*"
```

1. `kind:` from Step 0, if given — use it as-is.
2. `xcresult:` from Step 0, if given — always the app/`xccov` path (Step 3's app section), regardless of what
   else exists.
3. **Only `Package.swift` found** → **package** path (`swift test` + `llvm-cov`). No `.testTarget` in it at all
   → **stop and report "coverage not wired: Package.swift has no test target"**.
4. **Any of `project.yml`, `Project.swift`, `*.xcodeproj`, `*.xcworkspace` found** → **app** path (`xcodebuild
   test` + `xccov`), even when a `Package.swift` also exists alongside them (e.g. local SwiftPM modules pulled
   into an app target). No scheme has a test action → **stop and report "coverage not wired: no test scheme
   found"**. A `project.yml`/`Project.swift` present without a generated `.xcodeproj`/`.xcworkspace` yet needs
   `xcodegen generate`/`tuist generate` first — same caveat as `iru-swift-test`'s Step 1, this skill does not run
   that generation itself.

5. **An app whose scope lives in a local SwiftPM package** — every in-scope file is under a directory holding its
   own `Package.swift` (e.g. `Packages/Core/Sources/...` in the layout `iru-setup-apple-app`/`iru-setup-macos-app`
   scaffold), or `package-path:` was given → run the **package** path *inside that package directory* (`swift test
   --enable-code-coverage` + `llvm-cov`, every command below with `--package-path <dir>` or from `cd <dir>`). The
   app path can't measure it: the local package is linked statically into the app, and `xccov` on the app scheme
   attributes none of the package's sources (verified on 2026-10-16 against an `iru-setup-macos-app` scaffold with
   Xcode 27.1 — `Packages/Core` measured 100% lines through `swift test` + `llvm-cov`, while the app scheme's
   `.xcresult` listed only the app target's files). A scope mixing package files and app-target files takes both
   paths and reports each file from the path that measured it.

**Do not improvise an `xcodebuild test -scheme <PackageName>` run against a bare `Package.swift`-only
repository** even though SwiftPM auto-generates a scheme that makes it technically work — verified locally: the
resulting `.xcresult`'s `xccov --report --json` attributes **zero files** to the library's own build product
(its `PackageFrameworks/*_PackageProduct.framework` target shows `coveredLines: 0, executableLines: 0, files:
[]`); only the test target's own test-file source shows up, never the library code the tests exercise. A bare
package's coverage must go through the package/`llvm-cov` path (Step 2's package section).

## Step 2 — Run the coverage build

### Package path

```bash
swift test --enable-code-coverage [--filter <scope-pattern>]
```

Omit `--filter` to run the whole suite (same selector syntax as `iru-swift-test`). Coverage is only recorded for
code actually exercised by the tests that ran — same caveat as the other `*-coverage` skills: if the scope's
source file is covered by tests spread across multiple test targets, a filter narrow enough to exclude some of
them will undercount it; prefer the full suite when in doubt.

Locate the build products directory and every generated `.xctest` bundle:

```bash
BIN=$(swift build --show-bin-path)
find "$BIN" -maxdepth 1 -iname '*.xctest'
```

**Verified locally (Swift 6.4, default `swiftbuild` build-system backend, Xcode 27)**: `swift build
--show-bin-path` prints `.build/out/Products/Debug`, not the older `.build/debug` layout — but `.build/debug` is
kept as a compatibility symlink to the same directory (`.build/debug -> out/Products/Debug`), so either path
works. **The test binary is `<bin>/<TestTargetName>.xctest/Contents/MacOS/<TestTargetName>` — one bundle per
test target, named after that target, never a combined `<Package>PackageTests.xctest`** (verified with a
two-test-target package: it produced `DemoTests.xctest` and `DemoTests2.xctest` side by side, not a single
merged bundle). For a package with one test target this is unambiguous; for several, any one of them works as
the `llvm-cov` "covered executable" argument (each links the whole module, so the shared `default.profdata`'s
counts for library sources show up fully from just one binary) — but pass every `.xctest` binary found (the
first bare, the rest via repeated `-object <path>`) if the scope also includes files that live only in another
test target's own test sources.

The merged profile data is at:

```
$BIN/codecov/default.profdata
```

(equivalently `.build/debug/codecov/default.profdata`). `swift test --show-codecov-path` prints a *different*,
already-computed path — `$BIN/codecov/<PackageName>.json` — a ready-made `llvm-cov export`-format JSON report
SwiftPM writes as a side effect of the coverage-enabled test run (see Step 3's package JSON alternative). It is
not the `.profdata` path; don't confuse the two.

If `swift test` fails (compile error or test failure), report that failure and stop — don't convert or parse a
stale profile from an earlier run.

### App path

```bash
xcodebuild test -scheme <Scheme> -destination '<destination>' -enableCodeCoverage YES \
  -resultBundlePath <path>.xcresult
```

`<destination>` follows `iru-swift-test`'s Step 3 exactly — reuse its `resolve_destination` function rather than
re-implementing it: `platform=macOS` for a macOS scheme, otherwise `platform=<iOS|watchOS|visionOS>
Simulator,name=<device>,OS=<runtime version>` for the newest installed runtime the selected Xcode supports. The
`OS=` part is required: device names repeat across runtimes (`iPhone 17` under iOS 26.4 and 27.0). With
per-platform schemes (`<AppName>-iOS`/`-macOS`/`-watchOS`/`-visionOS`, `iru-setup-apple-app`), measure each
in-scope platform's `Targets/<Platform>/` files with that platform's scheme — one run and one `.xcresult` per scheme.
Delete a stale `<path>.xcresult` first — `xcodebuild` refuses to overwrite an existing result bundle at the same
path.

**No simulator runtime for the platform** (typically **visionOS** — `resolve_destination visionOS "Apple Vision Pro"`
prints nothing when `xcrun simctl list runtimes` has no visionOS runtime): don't download one and don't report 0%.
Report that scheme's app-target files **"unverified (no visionOS simulator runtime installed)"** (or the matching
iOS/watchOS wording) after `xcodebuild build-for-testing -scheme <AppName>-visionOS -destination
'generic/platform=visionOS Simulator'` confirms they compile. This never affects the bar in that layout: the
`Targets/**` UI layer is "not measured" anyway, and `Packages/Core` is measured through the package path (Step 1's
rule 5) with no simulator at all.

If `xcresult:` was given in Step 0, skip this command entirely and use that path directly in Step 3.

If the test run fails (build error or test failure), report that failure and stop — don't parse a `.xcresult`
that wasn't (re)generated for this invocation, or a stale one left over from before.

## Step 3 — Parse the coverage data

### Package: `llvm-cov`

```bash
TESTBIN="$BIN/<TestTargetName>.xctest/Contents/MacOS/<TestTargetName>"
xcrun llvm-cov report "$TESTBIN" -instr-profile "$BIN/codecov/default.profdata" \
  --ignore-filename-regex='(Tests/|DerivedSources)'
```

**Verified real column header** (Swift 6.4 / Xcode 27's `llvm-cov`):

```
Filename  Regions  Missed Regions  Cover  Functions  Missed Functions  Executed  Lines  Missed Lines  Cover  Branches  Missed Branches  Cover
```

**Verified quirks**:
- By default the report lists *every* file the test binary's coverage mapping touches — every source file in
  the module, every test file, **and** a synthesized `.../DerivedSources/test_entry_point.swift` (SwiftPM's
  generated test-discovery entry point, always ~50% covered and irrelevant to the user's own code). Scope with
  `--ignore-filename-regex` (shown above) to drop test files and the synthesized entry point, or to `grep` down
  to one file's row.
- **Passing a source file path as a bare positional argument does not filter the report** — verified locally: a
  report run with `Sources/Demo/Demo.swift` appended printed the identical, unfiltered, all-files table.
  `llvm-cov report`'s usage line (`Covered executable or object file. --sources <Source files>`) is misleading
  here; the only options that actually narrowed the output were `--ignore-filename-regex` and
  `--name`/`--name-regex` (function-level, not file-level). Filter with `grep` on the file's exact printed path
  if `--ignore-filename-regex` isn't precise enough for a single-file scope.
- **Branches column is always `0  0  -` for Swift sources** — verified with and without `-Xswiftc
  -profile-coverage-mapping` on `swift build`/`swift test`, and with `--show-branch-summary` added: neither
  changed it. `-profile-coverage-mapping` is a real `swiftc` flag ("Generate coverage data for use with profiled
  execution counts") but it does not populate `llvm-cov`'s branch counters for Swift as of Swift 6.4 — report
  branch coverage as **not available**, never as 0%.

For uncovered line ranges, export lcov and parse it (same format and parsing approach as
`iru-typescript-coverage`'s `DA:` handling):

```bash
xcrun llvm-cov export -format=lcov "$TESTBIN" -instr-profile "$BIN/codecov/default.profdata" \
  --ignore-filename-regex='(Tests/|DerivedSources)' > "$BIN/coverage.lcov"
```

Verified real shape (one `SF:`…`end_of_record` block per source file):

```
SF:/absolute/path/to/Sources/Demo/Demo.swift
FN:3,$s4Demo5helloyyF
FNDA:0,$s4Demo5helloyyF
FNF:5
FNH:3
DA:3,0
DA:4,0
...
BRF:0
BRH:0
LF:22
LH:11
end_of_record
```

`FN:`/`FNDA:` carry Swift's mangled symbol names (not human-readable — map back to source via the `FN:<line>,...`
line number, not the name). `FNF:`/`FNH:` are function-found/function-hit counts — function coverage % =
`FNH/FNF*100`. `LF:`/`LH:` are line-found/line-hit — line coverage % = `LH/LF*100`. `BRF:0`/`BRH:0` always,
confirming branch data is absent (not just zero-coverage — genuinely unrecorded).

**Path-matching quirk verified locally**: `SF:` paths are the compiler's *canonicalized* absolute paths. On
macOS, `$TMPDIR` resolves to `/var/folders/...`, a symlink to `/private/var/folders/...`; a plain
`$PWD`-relative path built without resolving that symlink silently fails to match the `SF:` line in `awk`
(`$0=="SF:"f` never fires, and every downstream query returns nothing with no error). Always `realpath` the
target source file before matching:

```bash
SF=$(realpath Sources/Demo/Calculator.swift)
awk -v f="$SF" '$0=="SF:"f{p=1} p&&/^DA:/{split($0,a,"[,:]"); if(a[3]==0) print a[2]} p&&/^end_of_record$/{p=0}' \
  "$BIN/coverage.lcov" | sort -n | awk '
  { if (NR==1) { start=$1; prev=$1; next }
    if ($1==prev+1) { prev=$1; next }
    print (start==prev ? start : start"-"prev); start=$1; prev=$1 }
  END { if (NR>0) print (start==prev ? start : start"-"prev) }'
```

Verified end-to-end against the fixture described in "Known quirks / verification notes" below: printed
`3-5`, `16`, `18`, `25-30` — matching the deliberately untested `hello()` body, two untested branches of
`classify(_:)`, and the entirely-untested `divide(_:_:)` respectively.

**Alternative (no manual `llvm-cov export`)**: `swift test --show-codecov-path` (Step 2) points at
`$BIN/codecov/<PackageName>.json`, already in `llvm-cov export`'s default JSON schema —
`{"data":[{"files":[{"filename","segments","summary":{"lines":{"count","covered","percent"},
"functions":{...},"branches":{"count":0,"covered":0,"percent":0},"regions":{...}}}]}]}` — read this file directly
with `python3 -m json.tool`/`jq` instead of running `llvm-cov export` again if it already exists and is fresh
(re-run `swift test --enable-code-coverage` first if in doubt, the same "don't trust a stale report" rule as
everywhere else in this skill).

### App: `xccov`

```bash
xcrun xccov view --report --json <bundle>.xcresult
```

**Verified real JSON shape** (Xcode 27's `xccov`):

```json
{
  "coveredLines": 13,
  "executableLines": 13,
  "lineCoverage": 1,
  "targets": [
    {
      "name": "DemoTests",
      "buildProductPath": "/.../Build/Products/Debug/DemoTests.xctest/Contents/MacOS/DemoTests",
      "coveredLines": 13,
      "executableLines": 13,
      "lineCoverage": 1,
      "files": [
        {
          "name": "DemoTests.swift",
          "path": "/absolute/path/to/Tests/DemoTests/DemoTests.swift",
          "coveredLines": 13,
          "executableLines": 13,
          "lineCoverage": 1,
          "functions": [
            {"name": "addWorks()", "lineNumber": 10, "executionCount": 1,
             "coveredLines": 4, "executableLines": 4, "lineCoverage": 1}
          ]
        }
      ]
    }
  ]
}
```

This confirms the task's expected shape exactly: `targets[].files[].lineCoverage`, `functions[]`,
`coveredLines`, `executableLines`. Compute the percentage as `lineCoverage * 100` (it's already a 0–1 fraction,
not a raw count) or recompute from `coveredLines`/`executableLines` when a per-function breakdown is needed.
There is **no branch-level field anywhere in this schema** — confirms branch coverage is unavailable from
`xccov`, not merely unreported.

Find the target/file you care about by walking `targets[]` → `files[]` and matching `path` by suffix (same
suffix-match convention `iru-typescript-coverage` uses for `coverage-summary.json` keys) or `name` for a type
simple name.

For uncovered line-level detail within one file, first get the exact path string `xccov` itself uses (do not
build it yourself — it must match exactly or the next command fails):

```bash
xcrun xccov view --archive --file-list <bundle>.xcresult          # exact paths, one per line
xcrun xccov view --archive --file "<exact-path-from-above>" --json <bundle>.xcresult
```

`--archive` is required whenever the target is a `.xcresult` bundle (not a raw `.xccovarchive`) — omitting it on
`--file`/`--file-list` fails with `Error: unrecognized file format`. Verified real per-line JSON shape:

```json
{"/absolute/path/to/File.swift": [
  {"line": 1, "isExecutable": false},
  {"line": 4, "isExecutable": true, "executionCount": 1},
  {"line": 16, "isExecutable": true}
]}
```

Uncovered lines are entries with `"isExecutable": true` and no `executionCount` key (or `executionCount: 0`);
collapse consecutive line numbers into ranges the same way the package path's `DA:` parsing does.

## Step 4 — Report results

State, per target file/type, the **line coverage percentage** and **function coverage percentage**, computed
from the actual `llvm-cov`/`xccov` numbers — never estimate or guess, and never paste the raw report/JSON into
the report. Branch coverage is always reported as **not available** for Swift (never 0% — 0% would wrongly imply
it was measured and found empty).

If the user's bar is "at least N%" (the group skills' convention is **80% line coverage**): say clearly whether
each file/type/the whole scope meets it, e.g. `Sources/Demo/Calculator.swift: line coverage 68.18% (15/22) —
under the 80% bar; uncovered: 16, 18, 25-30`, or `... line coverage 94.44% (17/18) — meets the 80% bar`.

For anything under the bar, give the uncovered line ranges from Step 3 so the user (or a follow-up skill, e.g.
`iru-swift-generate-all-tests`) knows exactly where to add tests, without opening Xcode's coverage gutter or an
HTML report.

If a named scope file/type doesn't appear in the report at all, it means no code in it executed during this run
(dead code, or the run didn't exercise it) — report 0%, not an error, the same convention every other
`*-coverage` skill in this catalog uses.

If coverage wasn't wired (Step 1's "coverage not wired" case), report that clearly instead of a percentage,
naming exactly what's missing (no test target in `Package.swift`; no test scheme in the `.xcodeproj`/
`.xcworkspace`).

Do not add tests, modify source/test/build code, or re-run anything to try to raise coverage — that's a
follow-up the user (or `iru-swift-code-one-task-group`, `iru-swift-generate-all-tests`) drives explicitly. This
skill is report-only and is normally invoked through the `iru-gate-runner` agent, which relays only the compact
summary above back to its caller — never the raw `llvm-cov`/`xccov` output.

## Known quirks / verification notes

- Verified end-to-end in `$TMPDIR/iru-verify/swift/coverage/Demo` against Xcode 27 / Swift 6.4
  (`swift-driver version 1.168.6`, target `arm64-apple-macosx27.0.0`): `swift package init --type library --name
  Demo` (Swift 6.4 scaffolds **Swift Testing** — `import Testing`, `@Test func` — by default, not XCTest), a
  `Calculator` type with `add`/`classify`/`divide` methods, tests covering only `add` and `classify`'s positive
  branch. `swift test --enable-code-coverage`, `swift build --show-bin-path`, `swift test --show-codecov-path`,
  `xcrun llvm-cov report`/`export -format=lcov`, and both DA-parsing and range-collapsing `awk` one-liners all
  ran successfully and produced the exact output shapes documented above.
- **`.build/out/Products/Debug`, not `.build/debug/...`, is the canonical bin path** as of Swift 6.4's default
  `swiftbuild` build-system backend; `.build/debug` is kept only as a symlink for backward compatibility. Prefer
  `swift build --show-bin-path` over hard-coding either form.
- **The `.xctest` bundle is named after its test target, never `<Package>PackageTests.xctest`** — this catalog's
  task brief assumed the latter; it does not hold on Swift 6.4/`swiftbuild`. Always glob
  `find "$BIN" -maxdepth 1 -iname '*.xctest'` rather than hard-coding a name.
- **Branch coverage is genuinely unavailable from both tools** for Swift as of Swift 6.4/Xcode 27: `llvm-cov
  report`'s Branches column stays `0 0 -` even with `-Xswiftc -profile-coverage-mapping` and
  `--show-branch-summary`; `xccov`'s JSON has no branch field at all. Report it as "not available", not 0%.
- **`xcodebuild test` on a bare SwiftPM package (no real `.xcodeproj`) does successfully run** via SPM's
  auto-generated scheme and produces a working `.xcresult` — but `xccov`'s per-target report attributes **zero**
  files/lines to the library's own package-product framework target in that specific setup; only the test
  target's own test-file source appears. This was verified directly (the `Demo` target showed `coveredLines: 0,
  executableLines: 0, files: []` while `DemoTests` correctly showed its own `DemoTests.swift`). Because of this,
  the app/`xccov` path in this skill should be trusted for a genuine Xcode **app** target's own source (an
  actual `.xcodeproj`/`.xcworkspace` with the app as the primary build product) but not relied on for a plain
  SwiftPM library's coverage — use the package/`llvm-cov` path for that even if an `.xcodeproj` also exists.
  **Unverified locally**: `xccov`'s behavior against a *genuine* Xcode app target (as opposed to a bare SPM
  package under an auto-generated scheme) was not independently exercised — no `.xcodeproj`/app scaffold was
  available in this environment (no `xcodegen`/`tuist`, `brew` not installed) — the JSON schema documented above
  is taken from the actual bare-package run, and there is no reason to expect the shape to differ for an app
  target, but the exact per-file attribution behavior for an app's own sources should be re-confirmed once
  `iru-setup-apple-app` produces a real app scaffold.
  `--file`/`--file-list` requires `--archive` and the *exact* path string `xccov` itself prints — passing an
  equivalent path built independently (even one that resolves to the same file) fails with `Error:
  XCCovErrorDomain Code=0 "Failed to find coverage lines for ..."`.
- **`SF:`/source-file path matching must account for macOS's `$TMPDIR` symlink** (`/var/folders/...` →
  `/private/var/folders/...`) — `llvm-cov export -format=lcov` always canonicalizes to the `/private/...` form,
  so any script matching `SF:` lines against a path it built itself must `realpath` that path first or the match
  silently fails (verified: an unresolved path produced zero matches with no error from `awk`).
- `swiftlint`, `xcodegen`, `tuist`, `xcbeautify`, `periphery`, `swiftformat` are irrelevant to this skill (no
  lint/format step here) and were not needed for verification.
- **macOS desktop app scaffold (`iru-setup-macos-app`: Automatic signing, empty `DEVELOPMENT_TEAM`)**: the app
  path's plain `xcodebuild test … -destination 'platform=macOS' -enableCodeCoverage YES` succeeds without signing
  overrides — verified 2026-10-16 (Xcode 27.1) on a copy of the `appkit-mvc` scaffold with a fresh
  `-derivedDataPath` ("Sign to Run Locally"; `xccov` reported `CoreTests` and `MyMacApp.app`). See `iru-swift-test`'s
  Known quirks for when `CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM=` is needed instead (a real
  team set but its certificate missing — unverified).
- The app path's simulator form was exercised on 2026-10-16 (Xcode 27.1) against copies of `iru-setup-apple-app`
  scaffolds: `iru-swift-test`'s `resolve_destination` gave `platform=iOS Simulator,name=iPhone 18 Pro,OS=27.0` and
  `platform=watchOS Simulator,name=Apple Watch Series 12 (46mm),OS=27.0` (both ran their schemes' tests, 11/11) and
  nothing for visionOS (no runtime installed — `build-for-testing` against `generic/platform=visionOS Simulator`
  succeeded, tests unverified). In that layout the bar is measured with `package-path: Packages/Core` (`swift test` +
  `llvm-cov`, 100% lines on both copies) — the per-scheme `xccov` runs only matter for app-target files, which are
  "not measured".
