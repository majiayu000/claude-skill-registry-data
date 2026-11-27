---
name: agnos-meta-plugin-proof
description: "AGNOS maintainer skill. Proves a marketplace built by agnos-meta-release by a real install: from a clean copy, in Claude Code and GitHub Copilot configurations isolated from the maintainer's, and on request by questions to their models and by the delivered suites on Linux. USE FOR: testing the plugin's deployment again after a change to a skill, the process, the block or the release. It publishes nothing."
argument-hint: "--marketplace <folder> [--with-models] [--linux] [--work <folder>] [--report <file>]"
---

<!-- FTR-PLG-001; RQ-PLG-010 / ADR-PLG-001 (DEC-PLG-006, DEC-PLG-007) -->
# AGNOS Plugin Proof

A **maintainer tool**: it serves the development of AGNOS and is not delivered. Canonical procedure; `.claude/skills/agnos-meta-plugin-proof/` points here.

## Procedure

1. Build the marketplace with `agnos-meta-release`.
2. Run, from the repository root (`python` on `windows`, `python3` on `linux` / `macos`):

   ```
   python .github/skills/agnos-meta-plugin-proof/scripts/plugin_proof.py --marketplace <folder>
   ```

3. Check the exit code. `1`: a check failed, nothing is to be delivered; `0`: none did, which does not mean each was observed: read the lines.
4. Give the maintainer each line as it is.

| Option | Does |
|---|---|
| `--with-models` | Puts the questions below to each tool. **It costs credits**: ask the maintainer first |
| `--linux` | Runs the delivered suites on Linux, on a copy of the tree: under WSL on Windows, directly on Linux. Tests that need a browser or tree-sitter are skipped when absent |
| `--repo <folder>` | The repository for `--linux`; default the current folder |
| `--work <folder>` | Keeps the working files there; by default a temporary folder, removed. On Windows, a short path avoids `Filename too long` |
| `--report <file>` | Writes the results as JSON |

Claude Code named by `AGNOS_CLAUDE` when it is not on the PATH. A tool that is absent is said, and skipped.

## What each line means

| Check | Observed how | Without a model |
|---|---|---|
| `validate-plugin`, `validate-catalogue` | `claude plugin validate --strict` (Claude Code); a run whose only warnings are the unknown field `logo` passes, its detail saying it was accepted <!-- RQ-PLG-046 / DEC-PLG-037 --> | yes |
| `marketplace-add`, `install` | The tool's commands, in its isolated configuration | yes |
| `skills` | The number of skills the tool announces against the plugin's | yes |
| `init` | `CLAUDE.md` written by the model calling `agnos-init` | no |
| `init-direct` | The installed script run by this tool, only when `init` was not observed, so that the next questions have the block | no |
| `process` | The answer holds a number known only from the process skill | no |
| `index` | `agnos-process/process.idx.md` written by the model calling `agnos-index` | no |
| `agent` | A test agent, added to the copy in each tool's place, answers its marker | no |
| `linux-suites` | The suites' exit code | `--linux` |

`pass`: seen. `fail`: exit 1. `not observed`: the model did not do it, often for lack of an approval in a run with nobody to give it, which is not a defect of the plugin and fails nothing. A question grants only `powershell`, `bash` and `python`, never every tool.

## What it does not prove

Local marketplaces are read in place: the install from a remote repository, with its per-version folder, needs a push. <!-- DEC-PLG-007 --> A full session with its user questions needs a person. Copilot in VS Code, Codex and macOS are not run.

Claude Code's questions use `--plugin-dir` with the maintainer's own sign-in, which installs nothing in their configuration.

## Tests

`python -m unittest discover -s .github/skills/agnos-meta-plugin-proof/tests -v` from the repository root.
