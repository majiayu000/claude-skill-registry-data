---
name: gh-stats
description: Ask questions about any GitHub repo and get instant stats cards.
permissions:
  network: ["api.github.com", "github.com"]
  commands: ["gh", "jq"]
commands:
  - id: repo-summary
    run: ./scripts/summary.sh {{repo}}
    description: Stats summary for a GitHub repo (owner/name)
    output: json
primer:
  - "What repo would you like stats for? Try: summarize facebook/react"
---
# gh-stats

Summarize any public GitHub repo using the `gh` CLI.

## How to use
- Run the `repo-summary` command with a repo slug like `facebook/react`.
- Always pass `--json` fields as the script does; never prompt for auth.
- If `gh` is missing or unauthenticated, report the script's JSON error card to the user instead of guessing.
- After results arrive, you may use `update_ui` to add a Table or KeyValue card bound to "$.repo-summary".