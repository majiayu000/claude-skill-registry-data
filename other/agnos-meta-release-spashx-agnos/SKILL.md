---
name: agnos-meta-release
description: "AGNOS maintainer skill. Rehearses a release of this repository in a folder: selects the delivered layers of a commit, writes them as a marketplace holding the plugin agnos, removes the IDs of AGNOS's own development, checks none is left, and proves on the demo that the output behaves as the repository does. USE FOR: checking what a release would hold before deciding to publish. It publishes nothing: no commit on main, no tag, no push."
argument-hint: "--dry-run --output <folder> [--demo <folder>] [--repo <folder>]"
---

<!-- FTR-MTA-002; RQ-MTA-006 to RQ-MTA-013 / ADR-MTA-002 (DEC-MTA-007 to DEC-MTA-011); RQ-PLG-001 to RQ-PLG-003, RQ-PLG-007 / ADR-PLG-001 (DEC-PLG-001, DEC-PLG-002) -->
# AGNOS Release Rehearsal

Canonical procedure, shared by GitHub Copilot (`.github/skills/agnos-meta-release/`) and Claude Code
(`.claude/skills/agnos-meta-release/`, which points here). It is a **maintainer tool**: it serves the development of AGNOS and is
not delivered.

## Procedure

1. Commit first: the rehearsal reads the files tracked at HEAD and ignores the working tree. Build the demo with `agnos-meta-demo`
   if it is absent.
2. Run, from the repository root, on all platforms:

   ```
   python .github/skills/agnos-meta-release/scripts/release.py --dry-run --output <folder>
   ```

   `<folder>` must be outside the repository and empty. The report is written beside it, as `<folder>.report.json` for tools and
   `<folder>.report.html` for a person. The demo is looked for beside the repository; `--demo <folder>` names another. Without
   `--dry-run` the script refuses: publishing does not exist yet.
3. Read the last line, which always holds the exit code: `agnos-meta-release: exit=<n>, <files> files, <ids> IDs
   removed, <lines> lines to read, <folder> written in <s> s`, or `exit=<n>, nothing written` after a refusal. A tool that does not show
   exit codes needs nothing else; to read it anyway, end the command with `; echo "exit=$LASTEXITCODE"` in PowerShell or
   `; echo "exit=$?"` in bash.
   - `0`: every check passed.
   - `1`: nothing is to be published. A refusal before writing is on the error stream; any other problem is printed as
     `problems: ...` and is in the report's `problems`. Report them to the maintainer.
4. Give the maintainer the printed lines as they are (`problems:`, `toRead:`, `mentions:`, `idsOutsideComments:`, each with its file
   and line) and the path of `<folder>.report.html`. Lines to read and mentions fail nothing: a person judges them. Do not open the
   JSON for them: everything to act on is printed. <!-- RQ-PLG-014, RQ-PLG-016 -->

## What it writes

| Path | What |
|---|---|
| `.claude-plugin/marketplace.json` | The catalogue read by Claude Code and Copilot, its description and version in `metadata` <!-- RQ-PLG-043 / DEC-PLG-033, RQ-PLG-044 / DEC-PLG-035 --> |
| `plugins/agnos/plugin.json`, `plugins/agnos/.claude-plugin/plugin.json` | The manifests, with the version of `agnos-init`'s template `VERSION.txt` and the listing fields of `assets/marketplace.json` <!-- RQ-PLG-032, RQ-PLG-045 --> |
| `plugins/agnos/assets/agnos.svg` | The logo both manifests declare: `assets/logo-template.svg` in the `color.brand-*` tokens of `agnos-perf-center`'s `tokens.json` at the commit rehearsed; a commit without them is refused <!-- RQ-PLG-046 / DEC-PLG-036 --> |
| `plugins/agnos/skills/<name>/` | Each delivered skill |
| `plugins/agnos/skills/agnos-instructions/SKILL.md` | The process instructions as a skill, generated |
| `README.md`, `COMPATIBILITY.md`, `LICENSE.md`, `CHANGELOG.md`, `assets/agnos-overview.png`, `.gitignore` | From the repository; the user's guide is `agnos-init`'s template, delivered with that skill <!-- RQ-PLG-022 --> |
| `.gitattributes` | The marketplace's own, from `assets/marketplace.gitattributes.txt` |
| `plugins/agnos/README.md` | The README the tools show for the plugin, from `assets/plugin-README.md` at the commit rehearsed; each relative link must lead to a file of the plugin <!-- RQ-PLG-042 / DEC-PLG-034 --> |

What the manifests say comes from `assets/marketplace.json`.

## What it checks

| Check | How | On failure |
|---|---|---|
| Every tracked file has a layer | `assets/layers.json`, and the prefix `agnos-meta-` for skills and sub-agents | Exit 1 before writing anything: add a rule |
| No ID of the repository is left | Reads the output: contents, binary files and paths | Exit 1, with file and line |
| The output behaves as the repository | Parses its Python, JSON, JavaScript, PowerShell and bash; compares what `agnos-index`, `agnos-perf-center` and `agnos-init` write | Exit 1, naming the file or the skill |
| The manifests are consistent | Reads the four manifests and catalogues: required fields, plugin folders that exist, the same name, version and description. No AI tool is called, so the verdict is the same on any machine; each tool's own validation and a real install are `agnos-meta-plugin-proof`'s <!-- RQ-PLG-015 --> | Exit 1, naming the file |
| The output holds what is declared | Lists the files on disk against the delivered and generated ones; the checks run Python with no bytecode written <!-- RQ-PLG-012 --> | Exit 1, naming the file |
| The plugin has what it needs | The instructions file, and `.github/skills/agnos-init/assets/templates/VERSION.txt` holding one SemVer 2.0.0 line, at HEAD <!-- RQ-PLG-032 --> | Exit 1 before writing anything, naming the file |
| The changelog is released | Counts the entries under `## [Unreleased]` of `CHANGELOG.md` at HEAD; prints `unreleased: <n> entries, version <VERSION> delivered` and records `unreleasedEntries` in the report and its page <!-- RQ-PLG-031 --> | Nothing fails: the line says the commit was not prepared |

An ID belongs to the repository when its trigram appears in the commit's `agnos-process/process.idx.md`, defined there or not. Examples
such as `RQ-EXP-001` use another trigram, and stay: keep it that way when writing an example.

The comparison uses the demo through a temporary clone, so the demo does not change. A language whose parser is absent is said on the error stream and not parsed.

## The report

| Key | Holds |
|---|---|
| `commit` | The commit rehearsed |
| `delivered`, `leftOut` | The files of each side |
| `removed` | The IDs removed per file |
| `toRead` | Lines a removal may have left reading badly; some are false alarms. Correct a real one by rewording it in the repository |
| `mentions` | Mentions of `agnos-meta-` or of a test the release leaves out |
| `idsOutsideComments` | IDs the commit's Markdown shows outside a comment, which the traceability rule forbids |
| `checks`, `problems` | Each check's result (`noIdLeft`, `manifests`, `sameBehaviour`), and what failed |

The same commit gives the same output, report and page, byte for byte. The page embeds the report and takes its look from the perf
center's design tokens of that commit; it needs no network. <!-- RQ-PLG-013, RQ-PLG-016, RQ-PLG-017 -->

## Tests

`python -m unittest discover -s .github/skills/agnos-meta-release/tests -v` from the repository root. One test rehearses this repository on the
demo, reads HEAD, and is skipped when the demo is not built.
