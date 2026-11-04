---
name: sourcegraph
description: Use Sourcegraph MCPorter CLI for remote repository discovery, code and commit search, diffs, and targeted file reading across work repositories.
---

# Sourcegraph

Run the generated `sourcegraph` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/sourcegraph/scripts/run.mjs" list-repos --help
node "$PI_CODING_AGENT_DIR/skills/sourcegraph/scripts/run.mjs" keyword-search --help
node "$PI_CODING_AGENT_DIR/skills/sourcegraph/scripts/run.mjs" code-finder --help
node "$PI_CODING_AGENT_DIR/skills/sourcegraph/scripts/run.mjs" read-file --help
```

Use Sourcegraph when the answer may span remote work repositories or repository history; use local search tools for the current checkout.
Start with repository scope plus a symbol, literal, path, author, or time range.
Use `keyword-search` for exact evidence, `nls-search` or `code-finder` for discovery, and `commit-search` or `diff-search` for history.
Read only the files or diffs needed to verify the result, and cite repository, revision, and path.
When Sourcegraph OAuth is unavailable, authenticate with `npx --yes mcporter@0.13.3 --config "$MCPORTER_CONFIG" auth sourcegraph`.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- sourcegraph`, then run `nix run .#sync-agents`.
