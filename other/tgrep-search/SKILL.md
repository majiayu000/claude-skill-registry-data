---
name: tgrep-search
description: Search a local source tree efficiently with the tgrep trigram index. Use for repeated, focused codebase discovery and symbol or contract searches; not for editing or Internet research.
license: MIT
metadata:
  compatibility: Codex, Claude Code, OpenCode, and terminal-capable agents
  tested_tgrep_version: 1.2.4
---

# tgrep Search

`tgrep` is a ripgrep-compatible regex search with an optional trigram index and
local server. It is valuable for repeated discovery in large trees; a single
small-tree query generally does not justify setup. This guidance uses ordinary
shell commands and is portable across Codex, Claude Code, OpenCode, and other
terminal-capable agents.

Search output is discovery evidence, not proof that a behavior is reachable,
safe, or correct. Inspect the owning code and tests before acting on it.

## Choose the lightest useful mode

| Situation | Use | Why |
| --- | --- | --- |
| One query or a small tree | `rg -- ...` or already-available `tgrep -- ...` | Avoid setup cost. |
| Several queries in one task | `tgrep index ...`, then indexed searches | One bounded index amortizes repeated discovery. |
| Long-lived terminal session with many edits | One supervised `tgrep serve ...` | A single-root server maintains a live overlay and answers multiple clients. |
| Many linked worktrees with repeated searches | Consider opt-in managed v2; read [shared worktree guidance](references/shared-worktrees.md) first | Sharing can reduce duplicate storage/build work, but adds lifecycle cost. |
| Exact post-edit or exhaustive absence check | `rg -- ...` or `tgrep --no-index ...` | Read the current filesystem rather than a possibly stale snapshot. |

Do not start a persistent server for a short task or a non-persistent agent
runtime. A personal or non-coding agent can use the same modes over an
explicitly authorized text workspace; repository-specific ignore-file advice
applies only to repositories.

## Availability and boundaries

For a small or one-off search, start with the available `rg` installation (or
an already-available `tgrep` without setup). Both tools support `--hidden`;
use `rg` or `tgrep --no-index` for current-filesystem searches. `--no-index` is a
`tgrep`-only flag and must not be passed to `rg`. Do not install `tgrep`, build
an index, or start a server merely to perform that search. Install it only when
the user explicitly requests installation or when repeated discovery justifies
setup and normal authorization permits it.

1. If indexed mode is selected and `tgrep` availability is unknown, check
   `tgrep --version` or `tgrep --help`. If installation is explicitly
   requested or justified by repeated discovery, use only the current
   installation instructions in the official
   [microsoft/tgrep repository](https://github.com/microsoft/tgrep): `brew
   install tgrep`, `cargo install --path tgrep-cli --locked` from an official
   checkout, or a platform-appropriate official GitHub Release. Verify
   `tgrep --help` afterwards. Do not substitute a similarly named package or an
   unverified binary. Respect the agent's normal installation and approval
   boundary. This guidance is checked against tgrep 1.2.4; inspect the installed
   version/help before using newer modes. Keep an existing package-manager
   installation under that manager rather than overwriting its executable.
2. Index only the assigned workspace or another explicitly approved root. An
   index records paths and searchable content-derived data: do not index a home
   directory, credential store, private logs, or unrelated data for convenience,
   and do not upload or share the index as a task artifact.
3. Select storage without creating unrelated repository changes:
   - Reuse an existing chosen directory. Upstream defaults to `.tgrep/`;
     `.tgrep-index/` below is an explicit custom path, not the default. Do not
     rename or duplicate an existing index merely to match these examples.
     When repository hygiene changes are authorized, ignore the chosen path
     in `.gitignore` and an existing `.dockerignore` so it is not published or
     sent to Docker builds.
   - For read-only work, personal-agent tasks, or tasks without authorization to
     edit ignore files, use an agent-private temporary directory through
     `--index-path`. Do not modify repository configuration merely to search.
   - Reuse an existing chosen index. Do not rebuild it until a query needs
     freshness. One process should own index rebuilds; concurrent readers may
     use a completed index or a supervised server. Ordinary `index` and `serve`
     take the same exclusive storage lock: stop that server before rebuilding
     its directory with `index`; do not race writers or point independent
     worktree servers at one shared index path.
4. If the agent exposes `tgrep` through a structured tool rather than a shell,
   constrain the root to the approved workspace, allow only search flags, and
   return stdout, stderr, and exit code together. Treat exit code `1` as an
   empty result, not a tool failure.

## Efficient workflow

### Build once, query many

When several searches are expected, build one bounded-memory snapshot from the
selected root:

```bash
tgrep index --index-path .tgrep-index .
tgrep --index-path .tgrep-index -n -S -C 2 -- 'parse_config' src tests
```

The default `external` strategy bounds the posting buffer, not total process
memory. In very large trees, consider `--index-buffer 16` (MiB) to lower that
buffer; do not choose the all-in-RAM `memory` strategy without a specific reason.
These builder flags apply to `index`, not `serve`. Exclude directories only when
they are genuinely outside the assigned scope.

For a long-lived coding session with many edits and searches, a supervised server
can keep the index warm and serve multiple clients:

```bash
tgrep serve --index-path .tgrep-index .
tgrep status --index-path .tgrep-index .
```

Start a server only when the environment can keep and later stop a background
process. A cold or incomplete ordinary server falls back to filesystem scans
until complete indexed coverage is available; do not interpret setup as a
reason to retry an empty result indefinitely. `status` exposes indexing and
hidden coverage. Completion is not a freshness guarantee: an existing server
can serve its prior index while reconciling edits. If background processes are
unreliable, use the on-disk index and rebuild it after relevant edits.

### Search deliberately

Place flags before `--`, then provide the pattern and an explicit root. This
prevents an accidental subcommand when searching for words such as `index` or
`serve`:

```bash
# Small or one-off search, including hidden files, without index setup.
rg --hidden -n -S --glob '!.git/**' -- 'parse_config' src tests

# Literal symbol/value: safest default for user-provided text.
tgrep --index-path .tgrep-index -F -n -C 2 -- 'OCR_REVIEW_PROGRESS' src tests docs

# Broad discovery: identify files first, then inspect the small result set.
tgrep --index-path .tgrep-index -l -t py -- 'render_.*report' .
tgrep --index-path .tgrep-index -g 'src/**' -C 3 -- 'TODO|FIXME' .

# Machine-readable locations for another tool or agent step.
tgrep --index-path .tgrep-index --json -F -- 'public contract' docs
```

- Use `-F` for literal user text, symbols, paths, and values; use regex only
  when needed. Use `-S` for smart case.
- For a broad question, use `-l` first, then search matching files with `-C 2`
  or `-C 3`. Narrow with `-t` or `-g` before truncating output with `-m`.
- Keep the command's result bounded for the receiving agent: start with a
  narrow root or `-l`, then inspect selected locations. Do not solve broad
  output by silently dropping arbitrary matches.
- Use `-q` for a yes/no check, `--files` for an indexed inventory, and
  `--json` or `--vimgrep` for location-aware automation. Preserve stderr and
  the exit code: `0` is a match, `1` is no match, and `2` is an error.
- A read error can accompany partial matches and exit `2`; never convert that
  into success or an exhaustive absence claim. Do not suppress diagnostics to
  manufacture a complete result.
- Use `--stats` to see whether a query is broad enough to merit better scoping
  or an index.

## Freshness and consistency

An on-disk index is a snapshot. After edits, rebuild it before treating an
absence result as exhaustive. A running server improves freshness but applies
filesystem events asynchronously; use `--no-index` for the one search that must
see the exact current filesystem. That intentionally performs a slower full
scan within the selected eligibility, ignore, hidden-file and size rules, not
an atomic snapshot or a search of every byte regardless of policy.

Keep index-membership flags aligned: `--index-path`, `--no-require-git`, and
file-size policy must agree between index, server, and indexed searches;
`--exclude` must agree between index and server. Outside a Git repository, add
`--no-require-git` to index, server, and searches if `.gitignore` rules must be
applied.

- Current indexes include hidden non-ignored files; `--hidden` exposes them in
  indexed content searches and `--files`, but does not disable ignore rules.
  Git metadata directory subtrees remain excluded from ordinary indexing.
- `--no-ignore`, non-auto encoding, `-a`/`--text`, `--binary`, `--no-index`,
  and explicit file arguments bypass the index. Explicit files also bypass
  glob/type filters: narrow the file list itself when necessary.
- For content searches, `--follow`, `--one-file-system`, `--ignore-file`, and
  `--ignore-file-case-insensitive` need `--no-index` to take effect. `--files`
  walks automatically for these options. A positive glob cannot reinclude
  ignored files in indexed mode; use a scan if those files are in scope.
- Indexes omit non-UTF-8 names and, outside Windows, names containing a
  backslash, with a warning. Use `--no-index` or `rg` to cover those paths;
  absence in the index does not prove absence from the workspace.

For other flags and mode differences, consult the
[official CLI documentation](https://github.com/microsoft/tgrep/blob/v1.2.4/README.md)
rather than assuming complete ripgrep equivalence. Older binaries may reject
the current index format; a downgrade requires rebuilding with the older
binary, preferably in a separate index directory, not deleting shared storage.

## Pre-action review

Before claiming an absence or editing from a result, confirm that:

- the root and index path are the intended workspace;
- the index is complete and fresh enough for the claim;
- filters and ignore rules did not exclude relevant files; and
- the owning implementation and relevant tests were inspected, not merely a
  matching line.

`tgrep` complements rather than replaces version-control inspection, dependency
tools, security analysis, tests, and domain-specific validation.
