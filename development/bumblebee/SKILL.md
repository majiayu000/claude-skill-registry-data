---
name: bumblebee
description: Run Bumblebee supply-chain inventory and exposure scans on macOS/Linux to detect compromised packages, extensions, and MCP host configs. 
category: Document Processing
source: antigravity
tags: [python, markdown, mcp, claude, ai, design, document, security, rag]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/bumblebee
---


# Bumblebee Security Scan

Bumblebee (https://github.com/perplexityai/bumblebee) is a read-only inventory collector that surfaces package, extension, and developer-tool metadata on developer endpoints. It answers a focused supply-chain question: when an advisory names a package or version, do any matches exist on this machine right now?

This skill drives a single Bumblebee scan from start to finish:

1. Verify Go is on the PATH (provide install guidance if not).
2. Verify or install the `bumblebee` binary.
3. Run the requested scan profile (`baseline`, `project`, or `deep`).
4. Save raw NDJSON output plus a Markdown report into the user's workspace.
5. Summarize findings — especially exposure-catalog matches — in the chat reply.

Communicate with the user in the language they used (German for Stefan). Code, commit messages, and on-disk file contents stay in English to match existing project conventions.

## When to Use This Skill

Use this skill when an advisory, incident report, or exposure catalog names compromised packages,
developer tools, browser/editor extensions, or MCP host configuration that may exist on a local
macOS or Linux developer endpoint.

Use it for read-only inventory and exposure checks. Do not use it to patch, uninstall, quarantine,
or otherwise mutate the scanned machine.

## Step 1 — Clarify the scan request

Before running anything, confirm two things with the user via `AskUserQuestion`, unless the message already pins them down:

- **Profile**: `baseline` (global package roots), `project` (specific dev folders like `~/code`), or `deep` (explicit `--root` paths, including `$HOME` for incident response).
- **Roots**: For `project` and `deep` profiles, ask which directories to scan. `deep` is the only profile that accepts a bare-home root.

If the user has an advisory or exposure-catalog file ready, also ask whether they want to pass it via `--exposure-catalog`. The skill does not ship its own catalogs — point them at `threat_intel/` in the Bumblebee repo if they ask where to find ready-made ones.

Skip the questions for one-liner asks like "lauf mal ne Baseline-Scan" — just run a baseline.

## Step 2 — Check Go

Run `command -v go && go version` in bash. Three outcomes:

- **Go ≥ 1.25 present** → continue.
- **Go present but < 1.25** → tell the user the version, explain Bumblebee needs Go 1.25+, and stop until they upgrade.
- **Go missing** → do not install Go automatically. Show platform-appropriate instructions and stop:
  - macOS: `brew install go` (or download from https://go.dev/dl/).
  - Debian/Ubuntu: prefer the official tarball from https://go.dev/dl/ because distro repos lag; `sudo apt install golang-go` only as fallback.
  - Fedora/RHEL: `sudo dnf install golang` or the official tarball.

After installation, the user must ensure `$GOBIN` (or `$HOME/go/bin`) is on `$PATH` so `bumblebee` is found later.

## Step 3 — Check or install Bumblebee

Run `command -v bumblebee && bumblebee version`. If missing:

```bash
go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest
```

Then re-check `bumblebee version`. If the binary still cannot be located, the user's `GOBIN`/`PATH` is likely misconfigured — surface the resolved `go env GOPATH` and `go env GOBIN` so they can fix it. Do not fall back to running the binary by absolute path silently; explain what is happening.

Once installed, also run `bumblebee selftest` as a sanity check. A non-zero exit means the local install is broken and the scan should not proceed.

## Step 4 — Run the scan

All scans write NDJSON to a file. Use the workspace folder for output so the user can open the results afterwards.

Output filenames (use the user's workspace path; the example below assumes `$OUT` is set):

- `bumblebee-<profile>-<UTC-timestamp>.ndjson` — raw records.
- `bumblebee-<profile>-<UTC-timestamp>.report.md` — Markdown report (generated in Step 5).

Pick a sensible `--max-duration` so a runaway scan does not hang the session. Reasonable defaults:

- `baseline`: 5m
- `project`: 10m
- `deep`: 15m (warn the user that scanning `$HOME` can still take longer; offer to raise the limit)

Always stream stderr to a sibling `.log` file — Bumblebee emits diagnostic NDJSON there that helps explain partial scans.

### Baseline

```bash
bumblebee scan --profile baseline \
  --max-duration 5m \
  > "$OUT/bumblebee-baseline-$TS.ndjson" \
  2> "$OUT/bumblebee-baseline-$TS.log"
```

Optional: scope to specific ecosystems if the user only cares about, say, npm and PyPI:

```bash
bumblebee scan --profile baseline --ecosystem npm,pypi ...
```

### Project

Each `--root` must be an existing absolute path. Reject bare `$HOME` for this profile (Bumblebee will reject it too — surface the message clearly).

```bash
bumblebee scan --profile project \
  --root "$HOME/code" \
  --root "$HOME/Developer" \
  --max-duration 10m \
  > "$OUT/bumblebee-project-$TS.ndjson" \
  2> "$OUT/bumblebee-project-$TS.log"
```

### Deep

Used for incident response — broad 
