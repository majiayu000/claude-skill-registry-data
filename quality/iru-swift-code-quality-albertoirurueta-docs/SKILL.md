---
name: iru-swift-code-quality
description: Run this Swift package/app's wired static-analysis and formatting tools — SwiftLint (`swiftlint lint --reporter json [paths]`, only when `.swiftlint.yml` exists AND the `swiftlint` binary is on PATH), the Swift toolchain's bundled formatter (`swift format lint --strict --recursive [paths]`, when a `.swift-format` config exists — or the third-party SwiftFormat tool via its own `--lint` invocation when only a `.swiftformat` config is present and its binary is on PATH), and Periphery (`periphery scan --format json`, only when a `.periphery.yml` config exists AND the `periphery` binary is on PATH) — then report every issue found (file, line, rule id, severity, message), grouped by tool and classified by rule id/severity. Invoke as `/iru-swift-code-quality` to check the whole package/project, or `/iru-swift-code-quality [scope]` where `[scope]` is a file/directory path or a type/file simple name — SwiftLint and `swift format lint` both accept paths directly (so a scoped invocation narrows what actually runs, unlike Java's Checkstyle/PMD/SpotBugs trio), while Periphery has no path selector so a scoped invocation still runs the whole scan and only filters the report. Verifies each tool is actually wired (config file present AND its binary on PATH) before trusting a "zero issues" result from it, and never installs a missing tool itself — if `swiftlint` is missing it reports "SwiftLint not wired/installed" and uses `AskUserQuestion` to offer `brew install swiftlint` or skipping that tool (noting `mint run realm/SwiftLint` / `mint install realm/SwiftLint` and the official signed `.pkg` release on the SwiftLint GitHub Releases page as alternatives), with the same never-auto-install courtesy for Periphery and third-party SwiftFormat. When the prompt supplies a baseline (a prior per-rule-id issue count or list from an earlier run of this skill, e.g. captured by `iru-swift-code-one-task-group` before a task group's changes), reports only the new-vs-baseline diff per rule id instead of the full current list. Equivalent to `iru-java-code-quality`/`iru-typescript-code-quality`/`iru-android-code-quality` for the Swift stack. Use whenever the user wants a lint/static-analysis/formatting pass called out separately from `iru-swift-test`/`iru-swift-coverage`, instead of eyeballing `swiftlint lint`/`swift format lint` console output.
model: haiku
---

# Swift Code Quality

Run whichever static-analysis and formatting tools this Swift package/app actually has wired and report every
issue they find. This skill only runs static analysis/formatting checks and reports results — it never fixes
issues, never runs `swiftlint --fix`/`swift format format`/`swiftformat` in write mode, and never edits
`.swiftlint.yml`/`.swift-format`/`.swiftformat`/`.periphery.yml` — that's a follow-up the user drives explicitly.
It also never installs a missing tool on its own; see Step 1.

## Step 0 — Resolve inputs

`[scope]` (optional, positional) is a file/directory path or a type/file simple name (e.g. `Sources/Foo.swift`,
`Foo`) used both to narrow what SwiftLint/`swift format lint` actually run against (Step 2) and to filter the
report (Step 3) — Periphery has no per-path selector, so a scope only filters *its* report, the same "run whole,
report scoped" pattern `iru-java-code-quality` uses for Checkstyle/PMD/SpotBugs. No `[scope]` → check the whole
package/project.

If the calling skill/prompt passes explicit `key: value` lines instead of (or alongside) the positional form —
`scope: <path>`, `paths: <space-separated paths>` — honor them and skip the positional parse. A `baseline:` block
(a prior per-rule-id issue count or itemized list from an earlier run of this skill) is used in Step 4 to compute
a diff instead of reporting the full current list; treat any text following `baseline:` as that prior result, not
as another key to resolve.

Resolve the project root the same way `iru-swift-test`/`iru-swift-coverage` do: a `Package.swift` at the
repository root or a nearer ancestor of `[scope]` (Swift Package Manager library), or an `.xcodeproj`/
`.xcworkspace` (Xcode app project) when no `Package.swift` exists — the tools below run from that root regardless
of which project shape is in play; nothing in this skill is SPM- or Xcode-project-specific.

## Step 1 — Verify which tools are wired

Check every one of these before running anything — a "zero issues" result from a tool that was never actually
configured, or that isn't even installed, is meaningless and must not be reported as a clean pass:

- **SwiftLint** — wired when a `.swiftlint.yml` (or the newer `.swiftlint.yaml`) config exists at the project
  root (or a directory `[scope]` falls under) **and** `swiftlint` resolves on PATH (`command -v swiftlint`).
  SwiftLint also runs with its bundled default rule set if no config is found, but per this catalog's gate-skill
  convention (see `iru-android-code-quality`), a missing config means "not wired" here — report it as such rather
  than silently linting against SwiftLint's own defaults and calling the result this project's bar.
- **Formatter** — two mutually exclusive tools can hold this role; detect which one, if either, is configured
  and only run that one (the same "detect which plugin is applied, use its own invocation" pattern
  `iru-android-code-quality` uses for Spotless vs. the standalone ktlint plugin):
  - `.swift-format` (a JSON config) present → the **Swift toolchain's bundled formatter**, invoked as
    `swift format lint` (a subcommand of the `swift` driver, not a separate binary — confirm with
    `swift format --help`, which succeeds whenever the active toolchain is Swift 5.9/Xcode 15 or newer; older
    toolchains don't bundle it, in which case fall back to checking whether a standalone `swift-format` binary
    resolves on PATH instead and invoke that binary directly with the same flags).
  - else `.swiftformat` present → the **third-party SwiftFormat** tool (nicklockwood/SwiftFormat, a different
    project from Apple's `swift-format` despite the near-identical name and config-file convention) — wired only
    when the `swiftformat` binary also resolves on PATH (`command -v swiftformat`).
  - neither config present → formatter not wired; skip and say so.
- **Periphery** (unused-code detector) — wired when a `.periphery.yml` config exists at the project root **and**
  `periphery` resolves on PATH (`command -v periphery`). Periphery can also run driven entirely by CLI flags with
  no config file, but the task convention here gates it on `.periphery.yml` the same way the other two tools are
  gated on their own config file, so a project that never opted in doesn't get an unrequested unused-code scan.

**If a tool's config is missing, skip running it and say so in the report** (e.g. `"Periphery: not wired (no
.periphery.yml)"`) instead of silently omitting it or reporting a misleading "0 issues" — the one hard rule every
gate skill in this catalog enforces.

**If a tool's config exists but its binary is missing, never install it silently.** Report the gap explicitly —
for SwiftLint specifically: `"SwiftLint not wired/installed (.swiftlint.yml present but swiftlint isn't on
PATH)"` — then use `AskUserQuestion` (max four options) to offer:

- **Install via Homebrew** — `brew install swiftlint` (only offer this option when `command -v brew` succeeds).
- **Skip SwiftLint for this run** — continue with whichever other tools are wired and note the gap in the report.
- Mention, as plain text alongside the options (not as a third option unless the user's environment specifically
  needs it), the two Homebrew-free alternatives: `mint install realm/SwiftLint` (via
  [Mint](https://github.com/yonaskolb/Mint), if already installed) and the signed `.pkg` installer published on
  SwiftLint's own GitHub Releases page (https://github.com/realm/SwiftLint/releases) — useful when neither
  Homebrew nor Mint is available.

Never run `brew install`/`mint install`/download the `.pkg` yourself without the user picking that option first.
Apply the same never-auto-install courtesy to a missing `periphery` or `swiftformat` binary when their config
file is present but the binary isn't (`brew install periphery` / `mint install peripheryapp/periphery`, and
`brew install swiftformat` / `mint install nicklockwood/SwiftFormat`, respectively) — one `AskUserQuestion` per
missing binary, each with the same **install** / **skip** shape.

## Step 2 — Run each wired tool

```bash
swiftlint lint --reporter json [paths] > swiftlint-report.json   # only if wired (Step 1)

# formatter — exactly one of these two, whichever is wired:
swift format lint --strict --recursive [paths]                   # Apple toolchain formatter (.swift-format)
swiftformat --lint [paths] --reporter json                       # third-party SwiftFormat (.swiftformat)

periphery scan --format json [--config .periphery.yml] > periphery-report.json   # only if wired
```

- `[paths]` is `[scope]` when given, otherwise the package's source root(s) (`Sources` for an SPM library,
  whichever source group(s) the Xcode project builds for an app) — pass positional paths, not a `--path` flag;
  both SwiftLint and `swift format lint` accept one or more file/directory paths as trailing positional arguments.
- **`swift format lint`** auto-discovers the nearest `.swift-format` ancestor config with no `--configuration`
  flag needed (verified locally — see "Known quirks" below); pass `--configuration <path>` explicitly only when
  `[scope]` sits under a directory with its own, more specific config the auto-discovery might not pick correctly.
  `--strict` is required by this skill's contract (it is what turns every finding into a build-breaking `error:`
  line instead of a non-failing `warning:` — see the exact diagnostic format below) and `--recursive` is required
  whenever any of `[paths]` is a directory (a bare file path doesn't need it).
- **SwiftLint's `--reporter json`** is not the tool's default console reporter (`xcode`) — always pass it
  explicitly so the output is machine-parseable in Step 3; the task's command deliberately omits `--strict`, so
  a run with only warning-severity violations exits `0` even though the JSON array still lists them (see "Known
  quirks").
- **Periphery** reads `.periphery.yml` from the project root automatically when present, matching `swift format
  lint`'s auto-discovery convention above; pass `--config` explicitly only when scanning from a different working
  directory than the config's own.
- None of these three tools expose a way to scope Periphery's *scan* itself — Periphery always analyzes the whole
  module graph its config/target points at; only the parsed report is filtered to `[scope]` in Step 3, the same
  "run whole, report scoped" handling `iru-java-code-quality` applies to Checkstyle/PMD/SpotBugs.

If a wired tool's underlying build step fails outright for a reason unrelated to lint/style/unused-code rules
(e.g. Periphery or `swiftlint analyze`-style deep checks failing to build the target at all, a genuine compile
error), report that and stop for that tool — its report wasn't meaningfully (re)generated, so don't read a stale
copy from an earlier run.

## Step 3 — Parse each report scoped to `[scope]` if given

**SwiftLint** (`--reporter json`) — a JSON array, one object per violation (a clean file contributes no entries
at all, it isn't listed the way Checkstyle/Detekt list an empty `<file>` block):

```json
[
  {
    "file": "/abs/path/Foo.swift",
    "line": 42,
    "character": 9,
    "severity": "Warning",
    "type": "Force Cast",
    "rule_id": "force_cast",
    "reason": "Force casts should be avoided"
  }
]
```

`rule_id` is SwiftLint's own snake_case identifier (`force_cast`, `line_length`, `trailing_whitespace`, …) —
bucket by this field verbatim in Step 4. `severity` is SwiftLint's two-level scale (`Warning`/`Error` — **the
exact casing is unverified locally**, SwiftLint isn't installable on this machine; treat the comparison
case-insensitively when classifying). **Unverified locally** (no Homebrew/Mint to install SwiftLint here) — this
shape is documented from SwiftLint's own `Reporters/JSONReporter.swift` output contract; verify field names and
casing against a real run before trusting them blindly. With `[scope]`, filter entries whose `file` falls under
it rather than re-running SwiftLint per file (it has no per-file CLI selector any more than Checkstyle does).

**`swift format lint`** — one plain-text diagnostic per line on stdout, **verified locally**:

```
Sources/Demo/BadStyle.swift:4:9: error: [AlwaysUseLowerCamelCase] rename the variable 'Value' using lowerCamelCase
Sources/Demo/BadStyle.swift:5:1: error: [Indentation] indent by 2 spaces
```

Format: `<file>:<line>:<col>: <severity>: [<RuleName>] <message>` — `<severity>` is `error` when `--strict` was
passed (required by this skill, Step 2) or `warning` without it. The rule id is the bracketed `[RuleName]`
segment (`AlwaysUseLowerCamelCase`, `Indentation`, `Spacing`, `DoNotUseSemicolons`, `AddLines`, …) — extract it
with a regex like `^(?P<file>.+):(?P<line>\d+):(?P<col>\d+): (?P<severity>warning|error): \[(?P<rule>[^\]]+)\]
(?P<message>.*)$` per line. A config-level problem (e.g. an unrecognized rule key in `.swift-format`) prints as a
separate `<unknown>: error: Configuration contains an unrecognized rule: <Name>` line with no `file:line:col` —
this doesn't stop the rest of the run (other files are still linted, verified locally), but it does mean the
config itself may not be enforcing what the project intends; surface it once in the report as a config warning
rather than folding it into a per-file rule-id bucket. With `[scope]`, filter parsed lines whose leading `<file>`
matches it (or pass `[scope]` directly as `[paths]` in Step 2, which is the cheaper option since this tool takes
paths natively — do that instead of running unscoped-then-filtering whenever `[scope]` is a valid path).

**Third-party SwiftFormat** (`swiftformat --lint --reporter json`), when that's the wired formatter instead —
**unverified locally** (not installable here). Documented output (SwiftFormat's own `--reporter json` option):
a JSON array of `{"line", "rule", "filePath", "reason"}`-shaped objects, one per formatting change it would make;
bucket by `rule` (SwiftFormat's own identifiers, e.g. `redundantSelf`, `trailingCommas` — a different id space
from both SwiftLint's `rule_id` and `swift format`'s bracketed rule names, keep it in its own bucket). Without
`--reporter json`, SwiftFormat's default `--lint` output is plain text (`<file>:<line>:<col>: warning: (<rule>)
<message>`) — prefer the JSON form for reliable parsing, the same reasoning as SwiftLint's `--reporter json`
above.

**Periphery** (`--format json`) — **unverified locally** (not installable here; documented from Periphery's own
README/scan-result output). A JSON array, one object per unused-code finding:

```json
[
  {
    "kind": "function",
    "name": "unusedHelper()",
    "modules": ["Demo"],
    "location": "/abs/path/Foo.swift:12:6",
    "hints": ["unused"],
    "ids": ["Demo.Foo.swift:12:6:unusedHelper()"]
  }
]
```

`location` is documented as a single `"<file>:<line>:<col>"` string (not a nested object) — split it to get
file/line for the report. `hints` is Periphery's own classification array (`unused`,
`redundantPublicAccessibility`, `redundantProtocol`, …) — bucket by the first hint, since that's the primary
finding kind; `kind` (`function`/`property`/`class`/…) is useful as a secondary grouping but isn't a rule id on
its own. With `[scope]`, filter entries whose `location` file segment falls under it — Periphery itself always
scans the whole module graph regardless (Step 2), so this filtering happens only here.

**Scoping, in general**: with no `[scope]`, report every parsed entry from every tool that ran. With `[scope]`,
filter each tool's parsed entries to ones whose file path falls under it; an empty result after filtering means
that tool found nothing in `[scope]`, not that it didn't run — say so rather than omitting the tool line entirely
from the report.

## Step 4 — Classify, diff against a baseline if given, and report

Bucket every issue by **tool, then by rule id** — SwiftLint's `rule_id`, `swift format`'s bracketed rule name,
SwiftFormat's `rule`, Periphery's primary `hints` entry — never merge buckets across tools even when a name looks
similar (SwiftLint and third-party SwiftFormat both happen to use snake_case-ish identifiers for unrelated rule
sets; keep them in clearly separate tool sections, the same convention `iru-typescript-code-quality` uses for
ESLint vs. Oxlint). Within each tool, also report the severity breakdown where the tool has one (SwiftLint:
Warning/Error counts; `swift format`/SwiftFormat: warning/error counts, driven entirely by whether `--strict`
was used; Periphery has no severity level, only `hints`).

**Report**: state an overall total across all tools at the top, then per tool: whether it ran or was skipped as
"not wired" or "installed? no — asked, user chose <choice>" (Step 1), a total issue count, the severity breakdown
(where applicable), and one line per rule-id bucket with its count and, for a scope smaller than the whole
project, the file:line list too.

**Baseline diff** — when the prompt that invoked this skill supplies a baseline (a prior run's per-rule-id counts
or itemized list, e.g. `iru-swift-code-one-task-group` capturing one before a task group's changes and asking for
the post-change result compared against it, the same contract `iru-java-code-one-task-group`/
`iru-typescript-code-one-task-group`/`iru-android-code-one-task-group` use for their language's code-quality
skill): compute the diff yourself — for each tool/rule-id bucket, report only issues that are new since the
baseline (a rule id whose count increased, or one that appears now but didn't in the baseline; a specific new
file:line entry when the baseline was itemized rather than just counts) — never report the full current list next
to the full baseline for the caller to diff themselves. A rule id whose count decreased or stayed the same is not
a regression and is omitted from this diff entirely, even though it's still reported in the plain (non-baseline)
count above it. State explicitly when a tool couldn't be diffed because it wasn't run in the baseline
(skipped/not wired/not installed then) — treat every one of its current issues as new in that case.

Do not attempt to fix any of the issues found, or modify SwiftLint/swift-format/SwiftFormat/Periphery
configuration — that's a follow-up the user drives explicitly.

## Known quirks / verification notes

- **Verified locally** in `$TMPDIR/iru-verify/swift/code-quality/Demo` (`swift package init --type library --name
  Demo`, Swift 6.4 toolchain, `swift format lint --help`): a `.swift-format` config at the project root is
  auto-discovered by `swift format lint` with no `--configuration` flag — confirmed by running the same
  deliberately mis-formatted file (`var Value: Int = 0;` plus bad indentation/spacing) both with and without
  `--configuration .swift-format` and getting identical output.
- **Verified locally**: the exact diagnostic line format is `<file>:<line>:<col>: warning: [RuleName] message`
  without `--strict`, and `<file>:<line>:<col>: error: [RuleName] message` with it — e.g.
  `Sources/Demo/BadStyle.swift:4:9: error: [AlwaysUseLowerCamelCase] rename the variable 'Value' using
  lowerCamelCase`. Exit code is `0` without `--strict` even when findings exist (they're warnings, not build
  failures) and `1` with `--strict` whenever at least one finding exists — treat a non-zero exit under `--strict`
  as "findings exist", not as a tool crash, and still go on to parse the output either way.
  `swift format lint --help` confirms the available flags this skill relies on: `--configuration`, `-s/--strict`,
  `-r/--recursive`, `-p/--parallel` (safe to add for a large source tree; doesn't change output shape), and
  confirmed `swift format lint [<paths>...]` accepts one or more positional file/directory arguments directly (no
  `--path` flag), the same "pass paths in, only those files are checked" behavior SwiftLint's own CLI documents.
- **Verified locally, a real quirk**: an unrecognized rule key in `.swift-format` (e.g. a rule name valid in a
  newer/older swift-format version than the active toolchain ships) prints `<unknown>: error: Configuration
  contains an unrecognized rule: <Name>` once **per file scanned** (not once for the whole run) and does not stop
  the rest of the lint — every other file is still checked and reported normally. Surface this line once in the
  report as a config-health warning distinct from the per-file findings.
- **Verified locally, a real quirk**: a single semicolon violation (`DoNotUseSemicolons`) was reported **twice**
  at the identical `file:line:col` in one run — dedupe by the full `(file, line, col, rule, message)` tuple before
  counting per-rule totals, rather than trusting the raw line count.
- **Not verified locally**: SwiftLint's JSON reporter shape, exit-code convention (documented elsewhere as `0`
  when clean or warnings-only without `--strict`/`--strict` config option, `2` when an error-severity violation
  exists), and the third-party SwiftFormat `--lint --reporter json` shape are all taken from each tool's own
  public documentation, not exercised on this machine — this machine has no Homebrew and no Mint installed, so
  `swiftlint`, `swiftformat`, and `periphery` could not be installed to confirm any of this directly (per this
  catalog's verification convention: mark unavailable-tool checks "unverified locally" rather than skip
  documenting them). Confirm field names/casing/exit codes against a real SwiftLint/SwiftFormat/Periphery
  installation before relying on them for anything beyond a best-effort parse.
- Periphery needs a buildable target (an SPM package or an Xcode project/workspace) to resolve symbol usage
  across the whole module graph — it is not a per-file syntactic linter the way SwiftLint/`swift format` are, so
  a `[scope]` narrower than the whole target still triggers a full build+analysis pass underneath; only the
  *report* narrows.
- Xcode-project (non-SPM) usage of `swiftlint`/`swift format lint`/`periphery` was not separately verified — all
  three tools operate on `.swift` source files directly regardless of build system, so the same commands are
  expected to work unchanged; only the "resolve the project root" step in Step 0 differs by project shape.
