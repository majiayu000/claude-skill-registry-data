---
model_tier: high
context: large
name: repomix-packer
description: "Use when packaging a codebase to a single AI-friendly file for LLM analysis — local or remote, XML/Markdown/JSON, token counting, gitignore filtering, peer-side `repomix` CLI."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

> **Pinned upstream:** `repomix` CLI (npm: `repomix`, brew: `repomix`). Re-verify per minor bump. Repomix is an **optional dependency** — this skill never installs it silently.

# repomix-packer

Wraps the upstream [`yamadashy/repomix`](https://github.com/yamadashy/repomix) CLI for codebase-snapshot workflows: pack a local or remote repo into a single XML / Markdown / JSON file with token counts and secret detection, then feed it to an LLM for review, audit, or migration scoping.

## When to use

- Producing an LLM-ingestible snapshot of a repo (or a sub-tree) for review or audit.
- Comparing two branches by packaging each and diffing the snapshots.
- Pulling a remote third-party library into context without cloning.
- Pre-flighting a token budget before sending a codebase to an LLM.

Do NOT use when:

- You only need a few specific files — read them directly with `view`.
- The snapshot will only feed a non-text format (PDF, image, audio) — route to [`markitdown`](../markitdown/SKILL.md).
- The repo is sensitive and `--no-security-check` would be needed — STOP, route to a human.

## Procedure: Snapshot a repo for LLM review

### 1. Inspect: verify `repomix` is installed (peer-side)

```bash
repomix --version
```

If the binary is missing, surface one of the install recipes and STOP — do not install silently:

```bash
# npm (preferred for project-local installs)
npm install -g repomix

# Homebrew (macOS / Linux)
brew install repomix
```

### 2. Decide local vs remote

```bash
# Local: pack the current directory.
repomix

# Remote shorthand: owner/repo
npx repomix --remote owner/repo

# Remote URL with a pinned commit
npx repomix --remote https://github.com/owner/repo/commit/<sha>
```

### 3. Filter the snapshot to the smallest useful slice

```bash
# Include patterns
repomix --include "src/**/*.php,*.md"

# Add ignore patterns on top of .gitignore
repomix -i "tests/**,*.test.js"

# Strip comments to save tokens
repomix --remove-comments
```

### 4. Pick the output format and destination

```bash
repomix --style markdown -o snapshot.md   # human-readable
repomix --style xml -o snapshot.xml       # default; clearest separators for LLMs
repomix --style json -o snapshot.json     # programmatic post-processing
repomix --copy                            # also copy to clipboard
```

### 5. Verify token budget and secrets

Repomix prints per-file and total token counts and runs Secretlint on the output. Check the totals against the target LLM context window:

| Model              | Approx context |
|--------------------|----------------|
| Claude Sonnet 4.5  | ~200K tokens   |
| GPT-4 family       | ~128K tokens   |
| GPT-3.5            | ~16K tokens    |

If Secretlint flags anything, STOP — sanitize the input or add the offending paths to `.repomixignore` before re-packing. Never use `--no-security-check` on an unfamiliar codebase.

### 6. Hand the snapshot to the consumer skill

Most workflows that call this skill pass the snapshot to:

- A code-review pass — pair with [`judge-bug-hunter`](../judge-bug-hunter/SKILL.md) or [`judge-security-auditor`](../judge-security-auditor/SKILL.md).
- Reference-repo analysis — route to [`analyze-repo`](../../commands/analyze/repo.md).
- Migration scoping — route to [`blast-radius-analyzer`](../blast-radius-analyzer/SKILL.md).

Cite the snapshot path so the consumer skill can read it.

## Output format

1. The repomix invocation (one shell line, with all filters and the output path).
2. The output file path + format + total token count.
3. Any Secretlint findings, verbatim. Empty section if none.

## Gotcha

- `--copy` puts the entire snapshot on the clipboard — surprising on large repos. Prefer `-o <path>` for anything > a few KB.
- `--no-gitignore` plus a wildcard include can pull in `.env`, `vendor/`, `node_modules/` — never combine without a tight `--include` first.
- Remote `npx repomix --remote owner/repo` defaults to the latest commit on the default branch — pin a commit SHA when reproducing a previous snapshot.
- Token counts are LLM-tokenizer estimates, not exact — leave a 10–15% headroom under the model's documented context window.

## Do NOT

- Do NOT run `repomix --no-security-check` on an unfamiliar codebase.
- Do NOT install repomix silently — surface the recipe and let the consumer install it.
- Do NOT commit `repomix-output.*` artifacts — add the pattern to `.gitignore`.
- Do NOT package `.env`, key material, or `.git/` — adjust `.repomixignore` first.
- Do NOT vendor repomix into the repo — it is a peer-side CLI.

## Auto-trigger keywords

- repomix
- pack codebase
- repository snapshot
- llm context bundle
- codebase to single file

## Provenance

- Upstream tool: https://github.com/yamadashy/repomix (MIT).
- Adopted from: an external reference (internal provenance, redacted) — wrapper-style adoption, no upstream code vendored.
- Provenance registry: `agents/settings/contexts/skills-provenance.yml` (entry: `repomix`).
- Iron-Law floor: `non-destructive-by-default`, `missing-tool-handling`, `tool-safety`.
