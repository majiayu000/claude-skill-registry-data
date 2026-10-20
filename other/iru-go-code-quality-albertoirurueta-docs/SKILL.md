---
name: iru-go-code-quality
description: >-
  Run a Go module's wired static-analysis and style checks — golangci-lint v2 (`golangci-lint run --output.json.path …`, a `version: "2"` config with `linters` and `formatters` sections; issues bucketed as `<linter>` or `<linter>:<rule>` — `revive:exported`, `gosec:G204`, `staticcheck:SA1019`, `govet:printf`, `errcheck`, `unused` — and the `gofmt`/`goimports`/`gofumpt`/`gci` formatters as their own rule ids), `go vet -json` (analyzer names, `govet:<analyzer>`), `gofmt -l` when golangci-lint isn't wired, and govulncheck (`-format json`, `govulncheck:<GO-ID>`, split into called / imported-only / required-only) when installed — in any Go project (command-line tool, library, service), modules and `go.work` workspaces alike. Verifies each tool is installed and configured before trusting a "zero issues" result, reports an unwired tool as "not configured, skipped" rather than a clean pass, rejects a v1 golangci-lint config as a tooling failure (with the `golangci-lint migrate` fix) instead of silently linting with defaults, and parses every report with one embedded stdlib Python parser into per-tool totals and per-rule-id counts with a `file:line — message` list. Invoke as `/iru-go-code-quality` to check the whole module, or `/iru-go-code-quality <file-or-dir>[,<file-or-dir>...]` to scope the report (golangci-lint runs on the containing packages, since Go type-checks whole packages, and findings outside the scope are filtered out; govulncheck is always module-wide). When the prompt supplies a `baseline:` (a prior per-tool/per-rule-id count or itemized list from an earlier run of this skill, e.g. captured by `iru-go-code-one-task-group` before a task group's changes), reports only the new-vs-baseline diff per rule id. Report-only: never runs `golangci-lint run --fix`, `golangci-lint fmt` without `--diff`, `gofmt -w`, `goimports -w`, or `go mod tidy`, and never edits `.golangci.yml`. Use whenever the user wants a Go lint/vet/vulnerability pass called out separately from `iru-go-test`/`iru-go-coverage`, instead of eyeballing golangci-lint console output.
model: haiku
allowed-tools: Read Bash(go *) Bash(golangci-lint *) Bash(govulncheck *) Bash(gofmt *) Bash(goimports *) Bash(python3 *) Bash(command -v *) Bash(git rev-parse *) Bash(git ls-files *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(mkdir -p build*) Bash(rm -f build/iru-go-cq-*)
---

# Go Code Quality

Run every static-analysis and style check this Go project actually has wired — golangci-lint (linters and
formatters), `go vet`, and govulncheck — and report every issue, grouped by tool and by rule id. This skill only runs
checks and reports results — it never fixes issues, applies formatting, adds `//nolint`, tidies modules, or modifies
tool configuration unless asked to as a follow-up.

## Step 0 — Resolve inputs

- **Scope** (optional, comma-separated): `.go` files or directories (`internal/greet/run.go`, `internal/cli`). Drop
  paths that don't exist and say so. golangci-lint and `go vet` work on **packages** (a file is type-checked with the
  rest of its package), so map each scoped file to its directory (`./internal/greet`) for the run and filter the
  findings back down to the scope in Step 3. No scope → `./...` (or one `./<dir>/...` per module of a `go.work`
  workspace whose root isn't a module — `go list -m -f '{{.Dir}}'`; `./...` fails there, as in `iru-go-test` Step 1).
- **`baseline: <prior report>`** (optional) — per-tool/per-rule-id counts, or an itemized `tool rule file:line` list,
  from an earlier run of this skill; kept for Step 4.

Read the project's real invocation before choosing flags: `.github/workflows/*.yml` (a `golangci/golangci-lint-action`
step pins a `version:` and may pass `args:`), `Makefile`/`Taskfile.yml`/`magefile.go` lint targets, and
`.pre-commit-config.yaml`. Mirror its `--build-tags`/`--config`/`--timeout`, and note a version mismatch between the
installed `golangci-lint version` and the CI pin — different versions report different issues.

## Step 1 — Verify which tools are wired

| Tool | Wired when | Notes |
|---|---|---|
| **golangci-lint** | `command -v golangci-lint` **and** a config (`.golangci.yml`/`.yaml`/`.toml`/`.json`, found by walking up from the module) or a CI/Makefile `golangci-lint run` | Config must declare `version: "2"`. A v1 config (no `version`) makes v2 exit `3` with `can't load config: unsupported version of the configuration: ""` (verified) — report it as a **tooling failure** with the fix (`golangci-lint migrate`), never as "0 issues". Note `linters.default` (`standard` = errcheck, govet, ineffassign, staticcheck, unused; `all`; `none`; `fast`), `linters.enable`/`disable`, `linters.exclusions.presets` (the `comments` preset **hides** revive's `exported`/`package-comments` findings — say so, `iru-go-godoc` checks those with its own config), `exclusions.generated`, and `formatters.enable` (`gofmt`, `goimports`, `gofumpt`, `gci`, `golines`). Installed but no config → it runs with the `standard` defaults: run it and say "golangci-lint defaults (no project config)". |
| **go vet** | always (part of the toolchain; `go test` runs a subset anyway) | Runs separately from golangci-lint's `govet` (whose analyzer set the config controls) — both are reported, in separate buckets. |
| **gofmt** | always, but **only as a standalone check when golangci-lint isn't wired** or its config enables no formatter | With golangci-lint formatters enabled, formatting issues come back in its report as rule `gofmt`/`goimports`/…; running `gofmt -l` too would double-count. |
| **govulncheck** | `command -v govulncheck` (or a CI step / `go tool govulncheck` from a `tool` directive in `go.mod`) | Needs network access to vuln.go.dev (or `-db file://…`). Unreachable → "govulncheck: vulnerability database unreachable, skipped", never "0 vulnerabilities". |

A tool that isn't wired is **skipped and named in the report** ("govulncheck: not installed, skipped") — never omitted
silently, never reported as "0 issues". Recommend (don't fail on) missing expected tools: golangci-lint v2 with
`revive`, `gosec`, `errorlint` and the `gofmt`/`goimports` formatters, and govulncheck — the set `iru-setup-go-cli`
scaffolds.

## Step 2 — Run each wired tool

Write every machine-readable report under `build/`, prefixed `iru-go-cq-`, and delete them afterwards (`rm -f
build/iru-go-cq-*`; remove `build/` only if this run created it). Exit codes are information, not failures — always
read the report; only a "tool broke" exit (listed per tool) means the report can't be trusted.

1. **golangci-lint**:

   ```bash
   golangci-lint run --output.json.path="$PWD/build/iru-go-cq-golangci.json" --output.text.path=stderr \
     --show-stats=false --max-issues-per-linter=0 --max-same-issues=0 --uniq-by-line=false --path-mode=abs \
     [--build-tags …] <packages> 2>/dev/null
   ```

   - v2 output flags are `--output.<format>.path` (v1's `--out-format` is gone). Relative output paths and issue paths
     are resolved against the **config file's directory** in v2 (verified: with `-c ../cfg.yml` the report landed
     beside the config) — hence the absolute `$PWD/…` output path and `--path-mode=abs` (the parser makes paths
     project-relative again). `--max-issues-per-linter=0 --max-same-issues=0` lift the default caps (50 / 3) and
     `--uniq-by-line=false` the default one-issue-per-line dedup (verified: with it on, a `godot` finding on the same
     line as a `revive:exported` one was dropped) — all three would otherwise hide issues.
   - Exit `0` = clean, `1` = issues found, `3` = failure (bad config, a linter that can't load); `--issues-exit-code`
     only changes the `1`. A compile error comes back as exit `1` with linter **`typecheck`** issues (verified) —
     report those first: they stop the other linters for that package.
   - Shape: `{"Issues": [{"FromLinter": "gosec", "Text": "G204: Subprocess launched with variable", "Severity":
     "medium", "Pos": {"Filename": "…/run.go", "Line": 13, "Column": 9}, "SourceLines": […]}], "Report": {"Linters":
     [{"Name": "errcheck", "Enabled": true}, …]}}` — `Report.Linters` lists what actually ran.
2. **go vet**: `go vet -json [-tags …] <packages> > build/iru-go-cq-vet.json 2>&1`
   - `-json` exits `0` even with findings and writes a stream of JSON objects (`{"<pkg>": {"<analyzer>": [{"posn":
     "/abs/file.go:6:41", "message": "…"}]}}`, `{}` for clean packages) — to stdout in Go 1.27 (older releases used
     stderr, hence `2>&1`). Text mode (`go vet ./…`) exits `1` with `file:line:col: message` but no analyzer name.
   - A package that doesn't compile shows its compiler error instead — report it as a tooling failure.
3. **gofmt** (only per Step 1): `gofmt -l $(git ls-files '*.go') > build/iru-go-cq-gofmt.txt` (or the scope's
   files). `gofmt -l` **exits `0` even when it lists files** (verified) — the list is the result. Same for
   `goimports -l` when the project uses goimports without golangci-lint. Never `-w`.
4. **govulncheck**: `govulncheck -format json [-tags …] ./... > build/iru-go-cq-vuln.json`
   - `-format json` exits `0` with findings (verified); text mode exits `3` when the code calls a vulnerable symbol.
     Any other non-zero exit, or an empty file → tooling failure (network, a package that doesn't build).
   - The stream holds `config`, `SBOM`, `progress`, `osv` (database entries) and `finding` objects. Each finding's
     `trace[0]` says how deep it reaches: with `function` → the code **calls** the vulnerable symbol; with only
     `package` → the package is **imported** but the vulnerable symbol isn't called; with only `module` → the module
     is merely **required**. The same OSV id appears at several levels; the parser keeps the deepest.
   - Always module-wide (it needs the whole call graph), even for a scoped run.

## Step 3 — Parse every report into tool → rule id → issues

Pass `scope=<comma-separated paths>` (omit for an unscoped run) and one `tool=report` pair per tool that ran
(`golangci`, `govet`, `gofmt`, `goimports`, `govulncheck`):

```bash
python3 - scope=internal/greet,internal/cli golangci=build/iru-go-cq-golangci.json govet=build/iru-go-cq-vet.json govulncheck=build/iru-go-cq-vuln.json <<'PY'
import json
import os
import re
import sys
from collections import Counter, defaultdict

cwd = os.path.realpath(os.getcwd())
CODED = {"revive", "gosec", "staticcheck", "govet", "gocritic"}   # Text starts with "<rule>: "


def rel(path):
    p = os.path.realpath(path) if os.path.isabs(path) else path
    return os.path.relpath(p, cwd) if os.path.isabs(p) else p


def objects(text):                      # concatenated / pretty-printed JSON values, noise lines skipped
    dec, i = json.JSONDecoder(), 0
    while i < len(text):
        j = text.find("{", i)
        if j < 0:
            return
        try:
            obj, i = dec.raw_decode(text, j)
        except ValueError:
            i = j + 1
            continue
        yield obj


def golangci(text):                     # golangci-lint v2 --output.json.path
    for d in (json.loads(text or "{}").get("Issues") or []):
        linter, msg = d["FromLinter"], d["Text"]
        m = re.match(r"^([A-Za-z][\w-]*): (.*)$", msg, re.S)
        rule = f"{linter}:{m[1]}" if linter in CODED and m else linter
        lines = [ln for ln in (m[2] if linter in CODED and m else msg).splitlines() if ln.strip()] or [msg]
        yield rel(d["Pos"]["Filename"]), d["Pos"]["Line"], rule, lines[-1] if linter == "typecheck" else lines[0]


def govet(text):                        # go vet -json: {"<pkg>": {"<analyzer>": [{"posn": "file:l:c", "message"}]}}
    for obj in objects(text):
        for analyzers in obj.values():
            for analyzer, diags in analyzers.items():
                for d in diags if isinstance(diags, list) else []:
                    f, line = d["posn"].rsplit(":", 2)[:2]
                    yield rel(f), int(line), f"govet:{analyzer}", d["message"]


def gofmt(text):                        # gofmt -l / goimports -l: one path per line
    for line in text.splitlines():
        if line.strip().endswith(".go"):
            yield rel(line.strip()), 0, "gofmt", "File is not gofmt-formatted"


def goimports(text):
    for f, line, _, _ in gofmt(text):
        yield f, line, "goimports", "Imports are not goimports-formatted"


def govulncheck(text):                  # govulncheck -format json: one finding per trace level; keep the deepest
    best = {}
    for obj in objects(text):
        f = obj.get("finding")
        if not f:
            continue
        top = f["trace"][0]
        level = 2 if top.get("function") else 1 if top.get("package") else 0
        pos = top.get("position") or {}
        cur = best.get(f["osv"])
        if cur is None or level > cur[0]:
            where = top.get("module", "") + "@" + top.get("version", "")
            caller = next(((fr.get("position") or {}) for fr in reversed(f["trace"])
                           if (fr.get("position") or {}).get("filename")), pos)
            best[f["osv"]] = (level, where, f.get("fixed_version") or "none", caller)
    for osv, (level, where, fixed, caller) in sorted(best.items()):
        kind = ("called", "imported only", "required only")[2 - level]
        yield (rel(caller.get("filename", "go.mod")) if level == 2 else "go.mod", caller.get("line", 0) if level == 2 else 0,
               f"govulncheck:{osv}", f"{where} ({kind}; fixed in {fixed})")


PARSERS = {"golangci": golangci, "govet": govet, "gofmt": gofmt, "goimports": goimports, "govulncheck": govulncheck}
args = dict(a.split("=", 1) for a in sys.argv[1:])
scope = [s.rstrip("/") for s in args.pop("scope", "").split(",") if s]
for tool, path in args.items():
    issues = [i for i in PARSERS[tool](open(path, encoding="utf-8", errors="replace").read())
              if not scope or tool == "govulncheck" or any(i[0] == s or i[0].startswith(s + "/") for s in scope)]
    by_rule = Counter(i[2] for i in issues)
    print(f"{tool}: {len(issues)} issue(s)")
    files = defaultdict(list)
    for f, line, rule, msg in issues:
        files[rule].append(f"{f}:{line} — {msg}")
    for rule, n in by_rule.most_common():
        print(f"  {rule}: {n}")
        for item in files[rule][:20]:
            print(f"    {item}")
        if n > 20:
            print(f"    (+{n - 20} more)")
PY
```

Rule ids: linters whose messages carry their own rule code get `<linter>:<rule>` — revive (`revive:exported`,
`revive:package-comments`, `revive:var-naming`), gosec (`gosec:G204`, `gosec:G304`), staticcheck (which in v2 also
holds the former gosimple/stylecheck checks: `staticcheck:SA1019`, `staticcheck:S1000`, `staticcheck:ST1003`,
`staticcheck:QF1001`), govet (`govet:printf`, `govet:inline`), gocritic (`gocritic:ifElseChain`). Every other linter is
its own rule id (`errcheck`, `unused`, `ineffassign`, `errorlint`, `godot`, `typecheck`) and so is every formatter
(`gofmt`, `goimports`, `gofumpt`, `gci`, `golines` — one issue per file). Standalone `go vet` findings are
`govet:<analyzer>` in the separate `govet` tool bucket; govulncheck's are `govulncheck:<GO-ID>`. Paths come out
project-relative; the per-rule list is capped at 20 entries with "(+N more)".

## Step 4 — Classify, diff against a baseline if given, and report

Bucket every issue by **tool, then rule id**. Never merge buckets across tools even when they describe the same
finding (golangci-lint's `govet:printf` and standalone `go vet`'s `govet:printf` stay separate). Call out families a
caller hands off elsewhere: **`typecheck`** first (code doesn't compile — everything else on that package is
incomplete), **`gosec:*`** and **`govulncheck:*` called** (security — list early; imported/required-only
vulnerabilities are informational: "upgrade `<module>` to `<fixed>` when convenient"), **`revive:exported`/
`revive:package-comments`/`godot`** (doc comments — fixed by `iru-go-godoc`), and the formatters (fixed by running
the formatter, a follow-up the user drives).

**Report**: an overall total across all tools first, then per tool: whether it ran or was skipped (and why), the
config and version in force (e.g. "golangci-lint 2.15.0, `.golangci.yml` v2, default `standard` + revive, gosec,
errorlint, godot; formatters gofmt, goimports; exclusion presets std-error-handling", "govulncheck 1.9.0, db
vuln.go.dev"), its total, and one line per rule-id bucket with its count — plus the `file:line — message` list when the
scope is smaller than the whole module, or on request. Tool failures (golangci-lint exit `3`, a v1 config, `go vet` on a
package that doesn't build, govulncheck without network) get their own line with the first error line, never
"0 issues". Never paste the raw JSON reports.

**Baseline diff** — when the prompt supplies a `baseline:` (the contract `iru-go-code-one-task-group` uses for this
skill): report only issues that are new since the baseline — a rule id whose count increased, a rule id that didn't
exist before, or a new `file` + rule entry when the baseline was itemized (match on tool + rule id + file, not on line
numbers or message text, which shift). A rule id whose count fell or stayed the same is not a regression and is
omitted from the diff (it still appears in the plain counts). A tool that wasn't run in the baseline (unwired then,
newly wired since) → treat all its current issues as new and say so. govulncheck findings can appear without any code
change (a new advisory) — flag a new `govulncheck:*` id as "new advisory or new dependency", not as a code
regression. This is separate from the project's own suppressions (`//nolint:<linter> // reason`, `exclusions.rules`),
which golangci-lint already applied.

Do not fix any issue, add `//nolint`, extend `exclusions`, run a formatter in write mode, upgrade a dependency, or
modify any configuration — those are follow-ups the user (or a coding skill) drives explicitly.

## Verification notes

Verified with Go 1.27.2, golangci-lint 2.15.0 (built with go1.27.0), govulncheck 1.9.0, in
`$TMPDIR/iru-verify/cli/go-gates/demo` (a throwaway Cobra CLI module outside this repository) against deliberately bad
code (unchecked `cmd.Run()`, `exec.Command` with a variable, `strings.Title`, a mis-grouped import block, an
undocumented exported function, a missing package comment, an unused function, a wrong printf verb, a comment without
a final period, `golang.org/x/text@v0.3.5` with `language.Parse` called):

- A `version: "2"` config (`linters.default: standard`, enable revive/gosec/godot/errorlint, formatters
  gofmt/goimports) passed `golangci-lint config verify`. `golangci-lint run --output.json.path=… --show-stats=false
  --max-issues-per-linter=0 --max-same-issues=0 ./...` exited `1`; the parser bucketed `errcheck`, `errorlint`,
  `godot`, `gofmt`, `goimports`, `gosec:G204`, `govet:printf`, `revive:exported`, `revive:package-comments`,
  `staticcheck:SA1019`, `unused`; `--uniq-by-line=false` raised the count from 11 to 12. With
  `exclusions.presets: [comments, …]` the two revive findings disappeared.
- A v1 config → exit `3`, `can't load config: unsupported version of the configuration: ""`. An undefined identifier
  → exit `1` with one `typecheck` issue. `--issues-exit-code=0` → exit `0`. `-c ../cfg.yml` with a relative
  `--output.json.path` wrote the report next to the config and issue paths relative to it; `$PWD/…` +
  `--path-mode=abs` fixed both.
- `go vet -json ./...` exited `0` and printed `{}` per clean package plus `{"…/internal/greet": {"printf": [{"posn":
  "…/vet.go:6:41", …}]}}` on stdout; `go vet ./...` exited `1`. `gofmt -l` listed the mis-formatted file and exited `0`;
  `golangci-lint fmt --diff` exited `1` with a diff.
- `govulncheck -format json ./...` exited `0` with 7 `finding` objects for 4 OSV ids; the parser reported
  `GO-2021-0113` as called at `internal/lang/lang.go:8` (fixed in v0.3.7), `GO-2022-1059` imported only, two
  required only; text mode exited `3`.
- Still unverified: `gofumpt`/`gci`/`golines` formatter ids end to end, golangci-lint's `--new-from-rev` mode (not
  used here — the baseline diff covers it), govulncheck with `-db file://` offline, and Windows paths.

## Sources

- golangci-lint docs (golangci-lint.run): configuration file v2 (`version: "2"`, `linters.default`, `exclusions.presets`,
  `formatters`), `run` command flags (`--output.json.path`, `--path-mode`, `--max-issues-per-linter`), migration guide
  (v1 → v2, `golangci-lint migrate`), linters reference (revive rules, gosec G-codes, staticcheck SA/S/ST/QF codes)
- go.dev: `go doc cmd/vet` (`-json`), `go doc cmd/gofmt`; go.dev/doc/security/vuln and pkg.go.dev/golang.org/x/vuln/cmd/govulncheck
  (`-format json`, exit codes, call-graph precision)
- irurueta docs: ai/cli-for-agents/security.adoc (dependency auditing, never build shell strings — what gosec G204 flags)
