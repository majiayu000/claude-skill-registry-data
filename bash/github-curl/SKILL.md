---
name: github-curl
description: |
  Use when making GitHub API calls and the mcp__github__gh tool is not in the
  tool list (a session where mods do not load: claude -p, an older Claude Code).
  Runs the same Python standard-library engine from Bash: pull requests, review
  threads, comments, reviews, metadata, issues and image attachments.
  WHEN: a GitHub API call is needed and mcp__github__gh is unavailable.
  WHEN NOT: mcp__github__gh is available (use it), or a non-GitHub API.
---

# github-curl

When the `mcp__github__gh` tool is listed, use it instead: it takes the same
subcommands as JSON and needs no shell quoting.

Otherwise, run the engine from Bash. Check the prerequisites first and stop on a
non-zero exit:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"
```

Then:

```bash
GH="${CLAUDE_PLUGIN_ROOT}/engine/gh.py"

PR=$(python3 "$GH" pr-get --format pr-number)
python3 "$GH" pr-threads "$PR" --format thread-summary
```

Every subcommand, formatter and exit code is listed in
`${CLAUDE_PLUGIN_ROOT}/engine/REFERENCE.md`. Its tables give the CLI arguments
(`<pr>`, `--body-file P`); its "Calling" section describes the tool's JSON form,
which this route does not use.

Text bodies always travel by file: write the body to a file and pass
`--body-file`, never the text as an argument. Before writing a commit message,
a pull request title, a pull request description or a review comment, read its
rules in `${CLAUDE_PLUGIN_ROOT}/engine/writing/`.
