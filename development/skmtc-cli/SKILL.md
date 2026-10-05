---
name: skmtc-cli
version: 0.5.1
description: |
  Use the Skmtc CLI to scaffold projects, install or clone generators
  from JSR, configure schema sources and enrichments, and produce code
  artifacts from an OpenAPI v3 or GraphQL SDL schema. Teaches the
  workspace mental model (`<root>/.skmtc/<project>/`, client.json,
  bundle, manifest) and the agent contract (strict text / strict JSON
  modes, exit codes, recipe errors, `agent-context` + `doctor`); the
  command surface itself is discovered from the binary — `skmtc
  --help`, `skmtc <cmd> -h` — rather than carried in this skill.

  Use this skill when the user asks to "run skmtc", "generate code
  from an OpenAPI schema", "install a skmtc generator", "scaffold a
  skmtc project", "watch a skmtc project", "configure enrichments",
  "publish a stack", "deploy to skmtc-hub" (the command is `publish`;
  there is no `deploy`), "skmtc in CI", or invokes any CLI
  subcommand. For *authoring* a generator package (Projections,
  Snippets, transform functions), defer to `skmtc-generator`. When
  something is broken (no output, wrong output, error messages, a
  failed bundle build), verify before proposing a fix: read the manifest and the
  parse issues, and reproduce the failure first.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  describes:
    '@skmtc/cli': '0.9'
---

# Skmtc CLI

The Skmtc CLI generates code from OpenAPI v3 or GraphQL SDL documents.
It's a Deno binary that wraps a project workspace under
`<root>/.skmtc/`, fetches generators from JSR, and runs them against a
schema source pinned in each project.

This skill carries what the binary cannot tell you: the workspace
mental model, the agent contract, and the decisions that need intent.
Everything else — the command list, per-command flags, argument
shapes — lives in the binary itself and is always current there;
§3 shows how to pull it on demand. This skill guides **using** the
CLI; for authoring generator packages see `skmtc-generator`, for
diagnosing failures see
[debug-failing-generation](https://github.com/skmtc/skmtc/blob/main/deno/docs/using/how-to/debug-failing-generation.md).

## 1. Mental model

| Concept | Where it lives | Notes |
|---|---|---|
| Skmtc root | nearest ancestor dir containing `.skmtc/` | Created by `skmtc init` |
| Project | `<root>/.skmtc/<project>/` | One schema + one set of generators |
| Project deps | `<root>/.skmtc/<project>/deno.json` | JSR imports of installed generators |
| Schema pin | `<root>/.skmtc/<project>/.settings/client.json` | `source` field — URL or path. Resolution: explicit schema arg → `client.json#source` → interactive prompt (TTY only; strict mode fails with a recipe error) |
| **basePath** | `client.json#settings.basePath` | **Must match the consumer app's `@` alias root.** Both the on-disk root for generated files AND the alias root in the bundler's resolver. Generators produce `@/<subdir>/...` paths assuming this alignment. Absolute paths are rejected at `init`. |
| Bundle | `<root>/.skmtc/<project>/bundle.js` | Compiled worker entry. Rebuilt before every run by `generate`/`dev`, and by `bundle`/`clone`/`install`. `describe`/`status`/`clean` build their own copy outside the project. |
| Manifest | `<root>/.skmtc/<project>/.settings/manifest.json` | Per-run record of every file written and every (generator × item) outcome |
| Generator | JSR package or local folder | Local: `<root>/.skmtc/<project>/<gen-name>/` |
| **Global state** | `~/.skmtc/` | `auth.json` (the hub PAT stored by `skmtc login`), shadow project state, schema caches. **Check this when local state alone doesn't explain a failure.** |

A "project" is **not** the consuming app — it's the *generator
configuration* the consuming app pulls code from.

**Generators are opinionated templates, not configurable libraries.**
Stock `@skmtc/gen-*` packages ship hardcoded defaults — export paths,
identifier naming, peer imports, output shapes — and there are no
config flags for any of them, deliberately. To change them,
`skmtc clone` the generator into the project and edit its source;
that is the customization seam, not a workaround. "Stock generator
hardcodes X" is almost never a CLI bug. Enrichments supply the
settings a generator's author declared it needs — its `enrichments.ts`
schema is the whole contract a consumer can fill; cloning changes the
shape.

Two engine facts that shape CLI expectations: generator order never
affects output (coordination is a memoized cache, not a dependency
graph — never sequence generators), and render does not run a
formatter (unformatted output is by design; consumers format
separately).

## 2. The agent contract

Every state-touching command supports three modes, picked
automatically:

| Mode | When | Behavior |
|---|---|---|
| **Interactive** | TTY attached and no `--json` / `--no-input` | Ink TUI; prompts for missing args |
| **Strict text** | Non-TTY (CI / pipes / agents) OR `--no-input` | Plain-text result on stdout; missing required args fail with a recipe error on stderr |
| **Strict JSON** | `--json` (implies `--no-input`) | Single JSON object on stdout; logs on stderr |

**For agents: add `--json` to every command.** The CLI auto-degrades
to non-interactive mode on any non-TTY stdin/stdout — no PTY wrappers
needed. (Two exceptions surface in help: `dev` is long-running and
has no `--json`; `create` has no `--json` yet.)

Exit codes are consistent across all commands: `0` success (including
documented no-ops), `2` required input missing or invalid (recipe
error on stderr), `1` anything else (registry unreachable, schema
parse failure, fatal parseIssue, typecheck failure). For `generate
--json`, an empty `errors` array is the success condition — not the
exit code alone.

**Recipe errors are the discovery mechanism.** When a required
argument is missing in strict mode, stderr carries the usage line, a
worked example, and a `Discover:` line naming the command that lists
the valid values (e.g. `ls .skmtc/` for project names). Trust it:
run the command, read the recipe, run the discovery, retry.

## 3. The command surface lives in the binary

Do not look for a command table in this skill — pull it live, where
it is always current with the installed version:

```bash
skmtc --help        # every command, with real descriptions
skmtc <cmd> -h      # full flags for one command
```

The newer commands' help descriptions (`status`, `eject`, `adopt`,
`publish`, `push`, `pull`) carry their full semantics — read them
there rather than guessing from the names. One naming trap help
cannot intercept: there is **no `skmtc deploy`** — stacks are
*published* (`skmtc publish`) as immutable semver versions;
deployments and the `production` alias belong to hub projects and are
driven from the web app, not the CLI.

## 4. First steps in a workspace

```bash
skmtc agent-context --json    # enumerate projects, commands, state
skmtc doctor --json           # check for known frictions
```

These two give the full workspace picture without documentation
lookups — `agent-context` is the snapshot, `doctor` the diagnostic,
in that order. `doctor`'s `summary` is the worst status across checks
(`error > warning > ok`; exit 1 only on `error`), and every check
carries its own `id`, `status`, `message`, and remediation `hint` —
the output is self-describing. The check-id catalogue, if you need to
reason about a specific check: [`reference.md`](reference.md)
§"Doctor check ids".

## 5. The bundle is rebuilt on every generate

Generation runs the compiled `bundle.js`, not generator source. For a
local project, `generate` rebuilds `bundle.js` from `deno.json#imports`
and the generator source on disk before every run, so pin changes and
edits to cloned source apply on the next `generate` — no `skmtc bundle`
step. `dev` builds the same way; `describe`, `status` and `clean` build
a read-only copy in a temporary directory (`deno bundle --frozen`), so
after a pin change run `generate` once before them. A build failure exits 1 with the
`deno bundle` error; a module graph with two copies of `@skmtc/core`
(or a `@skmtc/lang-*`) exits 1 naming the packages that import each
copy.

## 6. Configuration: client.json and filters

`.skmtc/<project>/.settings/client.json` — top level is
`{ source?, settings }`; `settings` carries `basePath` (required,
relative, no `..`), `packages`, `enrichments`, `skip`, `include`,
`generatedSuffix`. Full annotated shape, every key:
[`reference.md` §6](reference.md) — read it before editing the file.

`packages` (optional) routes output into monorepo packages. Each
entry `{ rootPath, moduleName? }` is a folder forward from `basePath`,
which is then the common ancestor of every package, not a bundler
alias. Inside a root, imports render `@/` from that root; from
outside, they render the root's `moduleName`. Nested roots are subpath
exports (`@app/sdk/models`) that share the outer package's `@`. Config
load rejects `..`, a repeated root and the workspace root; render
fails on an outside import of a root with no `moduleName`. Task page:
`docs/using/how-to/generate-into-multiple-packages.md`.

Enrichment misaddressing never errors. When a customization does not
land, read `manifest.enrichmentWarnings` (printed after `generate`,
and re-read by `skmtc doctor` as `project-enrichments/<project>`): a
typo'd id, path, method, model name or leaf key is reported with the
nearest match. Routing is the literal path plus lowercase method,
never `operationId`, under a `main` variant key. A wrong-typed value
fails only that item, recorded as `error` in the manifest.

`settings.skip` / `settings.include` accept a whole generator, a
per-operation entry (`path → method → variant[]`), or a per-model
entry (`refName → variant[]`); `[]` means every variant. Filters are
where **user intent** is expressed — never a generator's
`isSupported`. Semantics and precedence:
[`reference.md` §7](reference.md).

Every command's `--json` envelope is one object discriminated by a
`type` field; per-command shapes: [`reference.md` §8](reference.md) —
read when parsing output, not before.

## 7. Task cards

End-to-end workflows (setup, adding generators, enrichments, CI,
publishing, customizing a stock generator, …) live in
[`task-cards.md`](task-cards.md) — open the one card for the job in
front of you. A single command doesn't need a card; `-h` covers it.

## 8. Boundary with other skills

This skill ends at the CLI surface. Hand off when:

- The next step edits a `.ts`/`.tsx` file under
  `<root>/.skmtc/<project>/<gen-name>/` → **skmtc-generator**
- The user reports something broken and the cause isn't yet known →
  verify before proposing: manifest, parse issues, then a reproduction
  ([debug-failing-generation](https://github.com/skmtc/skmtc/blob/main/deno/docs/using/how-to/debug-failing-generation.md),
  [error codes](https://github.com/skmtc/skmtc/blob/main/deno/docs/reference/error-codes.md))

## Companion files

Loaded on demand with the Read tool, never eagerly:

| File | What it holds | Read it when |
|---|---|---|
| [`reference.md`](reference.md) | §6 client.json shape, §7 filter semantics, §8 JSON envelopes, §11 operational principles, doctor check ids | Editing settings, writing a filter, parsing `--json`, reasoning about a doctor check |
| [`task-cards.md`](task-cards.md) | Twelve end-to-end workflow cards | Doing a multi-step job for the first time |
