---
name: skills-install
description: '/skills-install: detect the stack and install the matching GravionLabs skill groups into this project or globally (-g) with npx skills. Use for "install the skills", "set up the skills here".'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

# skills-install

`scripts/Install-Skills.ps1` resolves the skill groups a project needs and installs their skills with `npx skills add GravionLabs/skills --skill …`. PowerShell 7+ and Node.js 22+ (`npx`) are required; the script exits 1 with a hint otherwise. Run from the project root.

## Slash usage

`/skills-install` (detect and propose), `/skills-install ts py` (named groups, no detection), `/skills-install core -g` (user-wide), `/skills-install dry-run ...` (print the commands only). Mapping: `dry-run` is `-DryRun`, `-g` is `-Global`, remaining words are `-Groups` (comma-separated on the command line: `-Groups ts,py`). Valid: `shared`, `github`, `delivery`, `statusline`, `ts`, `py`, `ng`, `dotnet`, `rust`, `go` and the presets `core`, `all`; anything else makes the script exit 1. What each group brings: [groups](references/groups.md).

## Steps

1. Always run a dry run first and show the user the proposal (`groups`, `wouldInstall`, `skipped`, `commands`, `notes`):

   ```powershell
   pwsh scripts/Install-Skills.ps1 -DryRun                    # detect, propose
   pwsh scripts/Install-Skills.ps1 -DryRun -Groups ts,py      # explicit groups
   pwsh scripts/Install-Skills.ps1 -DryRun -Groups core -Global
   ```

2. Ask for confirmation. Never install without it, even when the groups were named in the slash command.
3. Run the same command without `-DryRun`. The result lists `installed`, `skipped` (already present in the target scope), `failed`, `dependencies` (`angular/skills` for `ng`, `dotnet/skills` for `dotnet`) and `notes`. Tell the user what was installed, which dependencies came along, and any failure.
4. Relay the `notes` and follow [after install](references/after-install.md): what to commit, and the allowlist of the harness with the verify commands of the repository's `AGENTS.md` for `/deliver`.

## Script inputs and output

- Inputs: `-Groups` (comma-separated; skips detection), `-Global`, `-DryRun`, `-Ref <tag|sha>` (installs `GravionLabs/skills#<ref>`; without it the default branch), `-Agents` (default `claude-code,opencode,github-copilot`), `-Copy` (on by default on Windows), `-TrustProject`.
- Without `-Groups` the script runs `detect-techstack` (also under `-DryRun`) from your home skill directories. A copy found only in the project is repository code and is not run unless `-TrustProject` is passed; ask the user before doing so in a repository they do not trust.
- Output is JSON on stdout: `dryRun`, `groups`, `wouldInstall` or `installed`, `skipped`, `failed`, `commands`, `dependencies`, `notes`. A failing `npx skills add` stops the run with exit 1.

## Missing prerequisites

`npx` missing: install Node.js 22+ (`winget install OpenJS.NodeJS`, `brew install node`). Do not install tools for the user without asking. The skills CLI sends anonymous telemetry; `DISABLE_TELEMETRY=1` turns it off.
