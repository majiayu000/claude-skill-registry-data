---
name: iru-rust-code-quality
description: >-
  Run a Rust project's static-analysis and style checks — Clippy (`cargo clippy --workspace --all-targets --all-features --locked --message-format=json`, honoring the project's `[lints]`/`[workspace.lints]` table and `clippy.toml`; issues bucketed by lint id: `clippy::<lint>` such as `clippy::must_use_candidate`, `clippy::missing_errors_doc`, or rustc lint names such as `missing_docs`, `unused_imports`, `unused_variables`, plus `compile-error`/`E0425`-style codes when the code doesn't build), rustfmt (`cargo fmt --all --check --message-format short`, rule id `rustfmt`, one issue per file; unstable `rustfmt.toml` options on a stable toolchain as `rustfmt-config`), and cargo-deny when a `deny.toml` exists (`cargo deny --format json check <advisories|bans|licenses|sources>`, one run per check, rule ids `cargo-deny:<check>:<code>` such as `cargo-deny:licenses:rejected`, `cargo-deny:advisories:vulnerability`, `cargo-deny:bans:duplicate`) — in any Rust crate or Cargo workspace (command-line tool, library, service). Counts warnings without `-D warnings` (so one failing crate doesn't hide the lints of the crates that depend on it) and says how many would fail a CI that denies warnings. Verifies each tool is installed before trusting a "zero issues" result, reports a missing tool as "not installed, skipped", and parses every report with one embedded stdlib Python parser into per-tool totals and per-rule-id counts with a `file:line — message` list, deduplicating the copies Cargo prints once per target (lib and lib-test). Invoke as `/iru-rust-code-quality` for the whole workspace, or `/iru-rust-code-quality <file-or-dir>[,<file-or-dir>...]` to scope the report (Clippy and rustfmt still run workspace-wide — Rust checks whole crates — and findings outside the scope are filtered out; cargo-deny is always workspace-wide). When the prompt supplies a `baseline:` (a prior per-tool/per-rule-id count or itemized list from an earlier run of this skill, e.g. captured by `iru-rust-code-one-task-group` before a task group's changes), reports only the new-vs-baseline diff per rule id. Report-only: never runs `cargo clippy --fix`, `cargo fmt` without `--check`, `cargo deny fetch`/`init`, or edits `Cargo.toml`/`deny.toml`/`clippy.toml`/`rustfmt.toml`. Use whenever the user wants a Rust lint/format/supply-chain pass called out separately from `iru-rust-test`/`iru-rust-coverage`, instead of eyeballing Clippy console output.
model: haiku
allowed-tools: Read Bash(cargo *) Bash(python3 *) Bash(rustup *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(mkdir -p target*) Bash(rm -f target/iru-rust-cq/*)
---

# Rust Code Quality

Run Clippy, rustfmt and (when configured) cargo-deny on this Rust project and report every issue, grouped by tool and
by rule id. This skill only runs checks and reports results — it never fixes issues, applies formatting, fetches or
initializes a cargo-deny config, or modifies lint configuration unless asked to as a follow-up.

## Step 0 — Resolve inputs and read the project's policy

- **Scope** (optional, positional): comma-separated files or directories (`src/commands/greet.rs`, `src/output/`,
  `crates/core/`). Drop paths that don't exist and say so. No scope → the whole workspace.
- **`baseline: <prior report>`** (optional line, or a baseline block in the calling prompt): per-tool/per-rule-id
  counts or an itemized `tool rule file[:line]` list from an earlier run of this skill — keep it for Step 4.

Run from the workspace root (`cargo metadata --format-version 1 --no-deps` → `workspace_root`). Read, without
changing anything:

- **Lint policy**: `[lints.rust]`/`[lints.clippy]`/`[lints.rustdoc]` in the root `Cargo.toml`, or `[workspace.lints]`
  plus `lints.workspace = true` in each member (a member without that line doesn't inherit the policy — note which
  ones; this catalog's `xtask` is often one). Typical scaffold policy: `missing_docs = "warn"`, `unsafe_code =
  "forbid"`, `pedantic = { level = "warn", priority = -1 }` with a few `allow`s. `clippy.toml`/`.clippy.toml` holds
  lint *options* (`msrv`, `allow-unwrap-in-tests`, `too-many-arguments-threshold`).
- **CI invocation** (`.github/workflows/*.yml`, `Makefile`, `justfile`, `.cargo/config.toml` aliases): mirror its
  flags (`--all-features` vs a feature list, `-D warnings`, extra `-W clippy::…`) — the project's real invocation is
  the one to reproduce. Never add `#![deny(warnings)]`-style policy on your own.
- **Formatter config**: `rustfmt.toml`/`.rustfmt.toml` (`style_edition`, `max_width`, …).
- **Supply chain**: `deny.toml` (or `.deny.toml`, `.cargo/deny.toml`) — only then does cargo-deny run.
- **Toolchain**: `rust-toolchain.toml` (components `clippy`, `rustfmt` — rustup installs them on first use);
  `rustup component list --installed` shows what's there.

## Step 1 — Verify which tools are wired

| Tool | Wired when | Missing → |
|---|---|---|
| **Clippy** | `cargo clippy --version` succeeds | "clippy component not installed — `rustup component add clippy`", skipped |
| **rustfmt** | `cargo fmt --version` succeeds | "rustfmt component not installed", skipped |
| **cargo-deny** | a `deny.toml` exists **and** `cargo deny --version` succeeds | no `deny.toml` → "cargo-deny: not configured, skipped"; config but no binary → "cargo-deny not installed (`cargo install cargo-deny --locked`, or `EmbarkStudios/cargo-deny-action` in CI), skipped" |

A skipped tool is **named in the report** — never omitted silently, never reported as "0 issues". cargo-audit, when a
project uses it instead of cargo-deny, is out of this skill's scope (say so if CI runs it).

## Step 2 — Run each wired tool

Write every report under `target/iru-rust-cq/` (`mkdir -p target/iru-rust-cq`; `target/` is gitignored) and delete
them afterwards (`rm -f target/iru-rust-cq/*`). Exit codes are information, not failures — always read the report.
Pass `--locked` when `Cargo.lock` exists (a stale lock fails as in `iru-rust-test` Step 1 — report it).

1. **Clippy** — counted **without** `-D warnings`:
   ```bash
   cargo clippy --workspace --all-targets --all-features --locked --message-format=json \
     > target/iru-rust-cq/clippy.json 2> target/iru-rust-cq/clippy.err
   ```
   - `--all-targets` lints tests, benches and examples too; `--all-features` (or the CI's feature set) reaches
     feature-gated code. Add the CI's extra `-- -W clippy::<lint>` flags if it passes any.
   - Why no `-D warnings`: with it, the first crate with a warning fails to "compile", and every target that depends on
     it (the binary, `tests/*.rs`) is never linted (verified: the bin's `missing_docs` and the test crate vanished from
     the report). Count the warnings instead and say "CI with `-D warnings` would fail: N issues" when CI denies them.
   - stdout is one JSON object per line; `reason: "compiler-message"` entries carry `message.level`,
     `message.code.code` (the lint id: `clippy::useless_vec`, `missing_docs`, `E0425` for a rustc error) and
     `message.spans[]` (the `is_primary` span has `file_name` relative to the workspace root — `xtask/src/main.rs` for
     a member — and `line_start`). Each lint appears once per target that compiles the file (lib **and** lib-test):
     the parser deduplicates on lint + file + line + column. Exit `101` with `level: "error"` entries means the code
     doesn't compile — report those as `compile-error`/`E…` buckets first; every other count is then incomplete.
2. **rustfmt**:
   ```bash
   cargo fmt --all --check --message-format short > target/iru-rust-cq/rustfmt.txt 2>&1
   ```
   Exit `1` = at least one file would be reformatted; `short` prints one absolute path per file (the default output is
   a diff — never paste it). Unstable options in `rustfmt.toml` on a stable toolchain print `Warning: can't set
   `<option>`, unstable features are only available in nightly channel` (verified) — bucketed as `rustfmt-config`:
   the formatting result then differs from a nightly CI. A syntax error prints `error: …` (bucket `rustfmt-error`).
3. **cargo-deny** (only when wired) — one run per check, so every diagnostic is attributed to its check:
   ```bash
   for c in advisories bans licenses sources; do
     cargo deny --format json check "$c" 2> "target/iru-rust-cq/deny-$c.json" > /dev/null
   done
   ```
   - The JSON goes to **stderr**, one object per line: `{"type":"diagnostic","fields":{"severity":"error",
     "code":"rejected","message":"failed to satisfy license requirements","graphs":[{"Krate":{"name":…,
     "version":…}}],…}}` and a final `{"type":"summary",…}`; tool failures come as `{"type":"log","fields":
     {"level":"ERROR",…}}` (bucketed `cargo-deny:<check>:tool-error`).
   - Exit code is a bitmask of failed checks (advisories 1, bans 2, licenses 4, sources 8 — verified: a rejected
     license exited `4`) but a tool failure also exits `1`, so trust the parsed diagnostics, not the code.
   - `advisories` fetches the RustSec database over the network. If the fetch fails, re-run that check with
     `cargo deny --offline --format json check advisories` (uses the cached database) and say the advisory data may be
     stale; with no cached database, report advisories as **unverified (advisory DB unavailable)**.
   - `warning`-severity diagnostics (e.g. `license-not-encountered` — an allow-list entry no crate uses,
     `duplicate` under `multiple-versions = "warn"`) are reported in their own buckets but don't fail CI.

Never run `cargo clippy --fix`, `cargo fix`, `cargo fmt` without `--check`, `cargo deny init`, or `cargo update`.

## Step 3 — Parse every report into tool → rule id → issues

Pass `scope=<comma-separated paths>` (omit for an unscoped run) and one `tool=report` pair per tool that ran
(`clippy`, `rustfmt`, `deny:advisories`, `deny:bans`, `deny:licenses`, `deny:sources`):

```bash
python3 - scope=src/commands,src/output clippy=target/iru-rust-cq/clippy.json rustfmt=target/iru-rust-cq/rustfmt.txt \
  deny:advisories=target/iru-rust-cq/deny-advisories.json deny:bans=target/iru-rust-cq/deny-bans.json \
  deny:licenses=target/iru-rust-cq/deny-licenses.json deny:sources=target/iru-rust-cq/deny-sources.json <<'PY'
import json
import os
import sys
from collections import Counter, defaultdict

root = os.path.realpath(os.getcwd())


def rel(p):
    p = os.path.realpath(os.path.join(root, p))
    return os.path.relpath(p, root) if p.startswith(root + os.sep) else p


def clippy(path):  # cargo clippy --message-format=json: one JSON object per line on stdout
    seen = set()
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.startswith("{"):
            continue
        d = json.loads(line)
        if d.get("reason") != "compiler-message":
            continue
        m = d["message"]
        spans = [s for s in m["spans"] if s["is_primary"]]
        if not spans or m["level"] not in ("warning", "error"):
            continue  # "N warnings emitted" / "aborting due to" summaries have no span
        code = (m.get("code") or {}).get("code") or ("compile-error" if m["level"] == "error" else "warning")
        s = spans[0]
        key = (code, rel(s["file_name"]), s["line_start"], s["column_start"])
        if key in seen:  # the same lint is reported once per target (lib + lib test, …)
            continue
        seen.add(key)
        yield key[1], s["line_start"], code, m["message"]


def rustfmt(path):  # cargo fmt --all --check --message-format short: one path per line
    seen = set()
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith("Warning: can't set") and line not in seen:  # unstable rustfmt.toml option on stable
            seen.add(line)
            yield "rustfmt.toml", 0, "rustfmt-config", line[len("Warning: "):]
        elif line.startswith("error"):
            yield "-", 0, "rustfmt-error", line
        elif line and os.path.exists(line):
            yield rel(line), 0, "rustfmt", "File would be reformatted"


def deny(path, check):  # cargo deny --format json check <check>: JSON lines on stderr
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.startswith("{"):
            continue
        d = json.loads(line)
        f = d.get("fields", {})
        if d.get("type") == "log" and f.get("level") == "ERROR":  # cargo-deny itself failed (metadata, advisory DB fetch)
            yield "-", 0, f"cargo-deny:{check}:tool-error", f["message"].splitlines()[0]
        if d.get("type") != "diagnostic":
            continue
        if f.get("severity") not in ("error", "warning"):
            continue
        krates = [g["Krate"]["name"] + "@" + g["Krate"]["version"] for g in f.get("graphs", []) if "Krate" in g]
        yield ", ".join(krates) or "deny.toml", 0, f"cargo-deny:{check}:{f.get('code')}", f"[{f['severity']}] {f['message']}"


args = dict(a.split("=", 1) for a in sys.argv[1:])
scope = [s.rstrip("/") for s in args.pop("scope", "").split(",") if s]
for tool, path in args.items():
    if not os.path.exists(path):
        continue
    gen = deny(path, tool.split(":", 1)[1]) if tool.startswith("deny:") else {"clippy": clippy, "rustfmt": rustfmt}[tool](path)
    issues = [i for i in gen if tool.startswith("deny:") or not scope or i[0] in ("-", "rustfmt.toml")
              or any(i[0] == s or i[0].startswith(s + "/") for s in scope)]
    print(f"{tool}: {len(issues)} issue(s)")
    by_rule = defaultdict(list)
    for f, line, rule, msg in issues:
        by_rule[rule].append(f"{f}:{line} — {msg}" if line else f"{f} — {msg}")
    for rule, n in Counter(i[2] for i in issues).most_common():
        print(f"  {rule}: {n}")
        for item in by_rule[rule][:20]:
            print(f"    {item}")
        if len(by_rule[rule]) > 20:
            print(f"    (+{len(by_rule[rule]) - 20} more)")
PY
```

Paths come out workspace-relative. cargo-deny findings name the crate (`name@version`) rather than a file and are never
scope-filtered (the dependency graph is workspace-wide). The per-rule list is capped at 20 entries.

## Step 4 — Classify, diff against a baseline if given, and report

Bucket every issue by **tool, then rule id** — `clippy::<lint>` / rustc lint name / `E…` / `compile-error` for
Clippy, `rustfmt` / `rustfmt-config` / `rustfmt-error`, `cargo-deny:<check>:<code>`. Within Clippy, call out the
families a caller hands off elsewhere: **doc lints** (`missing_docs`, `clippy::missing_errors_doc`,
`clippy::missing_panics_doc`, `clippy::missing_safety_doc`, `clippy::doc_markdown`, `rustdoc::*`) — fixed by
`iru-rust-rustdoc`; **`unsafe_code`**/`clippy::undocumented_unsafe_blocks` (list first); and compile errors (they
block every other check on that crate).

**Report**: an overall total first, then per tool: ran or skipped (and why), version and config in force ("clippy
0.1.99, `[lints.clippy] pedantic = warn`, `--all-targets --all-features`", "rustfmt 1.10, `style_edition = 2024`",
"cargo-deny 0.20.2, `deny.toml`"), its total, and one line per rule-id bucket with its count — plus the `file:line —
message` list when the scope is smaller than the workspace, or on request. State whether a CI that runs Clippy with
`-D warnings` (and `cargo fmt --check`, `cargo deny check`) would pass. Tool failures (clippy exit `101` from a build
error, cargo-deny `tool-error`, a stale `Cargo.lock`) get their own line with the first error line, never "0 issues".
Never paste raw JSON or diffs.

**Baseline diff** — when a baseline is supplied (the contract `iru-rust-code-one-task-group` uses): report only issues
that are new since the baseline — a rule id whose count increased, a rule id that didn't exist before, or a new `file`
+ rule entry when the baseline was itemized (match on tool + rule id + file, never on line numbers or message text,
which shift). A rule id whose count fell or stayed the same is not a regression and is omitted from the diff (it still
appears in the plain counts). A tool that wasn't run in the baseline (newly wired) → all of its issues are new; say
so. In-source suppressions (`#[allow(...)]`, `#[expect(...)]`, `[lints]` `allow`s, `deny.toml` `ignore`/`skip`
lists) were already applied by the tools.

Do not fix any issue, add `#[allow]`/`#[expect]`, edit `[lints]`/`clippy.toml`/`rustfmt.toml`/`deny.toml`, run a
formatter in write mode, or update dependencies — those are follow-ups the user (or a coding skill) drives explicitly.

## Verification notes

Verified on 2026-10-16 with Rust 1.99.1 stable (clippy 0.1.99, rustfmt 1.10.0), cargo-deny 0.20.2, in
`$TMPDIR/iru-verify/cli/rust-gates/` (outside this repository) on a workspace with a `democli` lib + bin (`[lints]`
with `missing_docs = "warn"` and `pedantic` at `warn`, an undocumented `pub fn`, a `vec!` that should be an array, a
`usize as u32` cast, a `Result` fn without `# Errors`, a misformatted `main.rs` and `tests/cli.rs`) and an `xtask`
member, plus a `deny.toml` allowing only `Apache-2.0` while the crate is `MIT`:

- Clippy JSON exited `0` (warnings only); the parser reported 10 issues — `clippy::must_use_candidate` 3,
  `missing_docs` 2 (`src/lib.rs:23`, `src/main.rs:1` crate docs), `clippy::comparison_chain`,
  `clippy::cast_possible_truncation`, `clippy::missing_errors_doc`, `clippy::useless_vec`,
  `clippy::assertions_on_constants` 1 each — after dropping 9 lib/lib-test duplicates. With `-- -D warnings` it exited
  `101`, every lint became `level: "error"`, and the bin and `tests/cli.rs` were no longer linted. An unused variable in
  `xtask/src/main.rs` came back as `unused_variables` with the member-relative path. A scoped run
  (`scope=src/main.rs`) kept only that file's issues.
- `cargo fmt --all --check --message-format short` exited `1` and printed the two absolute paths; an unstable
  `imports_granularity` in `rustfmt.toml` added `Warning: can't set …` lines (bucketed once as `rustfmt-config`).
- `cargo deny --format json check licenses` exited `4` with `cargo-deny:licenses:rejected` (`democli@0.1.0-dev`) and
  `cargo-deny:licenses:license-not-encountered` (warning); advisories/bans/sources exited `0` after fetching the
  advisory DB; adding `MIT` to the allow-list made `cargo deny check` print `advisories ok, bans ok, licenses ok,
  sources ok`. `--offline` reused the cached DB; with an empty `CARGO_HOME` it emitted `type: "log"` `ERROR` lines
  and exited `1` (parsed as `tool-error`).
- Not verified: Clippy on a nightly toolchain or with `clippy.toml` `msrv` affecting lint selection, cargo-deny `bans`
  wildcard/`deny` lists and `sources` git rules on real dependencies, and Windows path separators in `file_name`.

## Sources

- irurueta docs: programming-languages/rust/tooling-clippy-rustfmt-and-rust-analyzer.adoc (Clippy groups, the `[lints]`
  table, `-D warnings` on the command line in CI rather than `#![deny(warnings)]`, `cargo fmt --check`, `rustfmt.toml`
  style edition, cargo-deny/cargo-audit, the CI workflow shape)
- irurueta docs: programming-languages/rust/cargo-and-workspaces.adoc (`[workspace.lints]` + `lints.workspace = true`,
  `--workspace`, `Cargo.lock`)
- irurueta docs: programming-languages/rust/documentation-with-rustdoc.adoc (`missing_docs` and the doc lints handed
  off to `iru-rust-rustdoc`)
- Clippy book (lint configuration, `--message-format=json` via Cargo), rustfmt configuration docs, cargo-deny book
  (checks, `--format json`, exit codes)
