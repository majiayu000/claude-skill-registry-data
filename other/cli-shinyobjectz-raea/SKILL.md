---
title: "raea skill"
summary: "Print the agent skill this raea ships, matched to its version, or one of its references."
order: 126
sources: ["engine/cli/src/skill.rs"]
---

`raea skill` prints the raea skill, the instructions agents read to work with raea, exactly as this version ships it.
`--reference` prints one of its generated references instead: the CLI, the feed, the project's files or the SDK.
To put the skill where an agent reads skills, use [`raea skills install`](skills.md).

The skill raea ships matches the version it ships with. An agent can hold a copy from an older or newer install;
its front matter names the version it came with, and when that differs from `raea --version` the agent reads
`raea skill` instead.

```sh
raea skill
raea skill --reference sdk
```

<!-- generated:begin by tools/manual-ref/cli.ts from `raea help --json`; edit only the flag descriptions -->

## Usage

```sh
raea skill [NAME] [--reference cli|feed|files|sdk] | raea skills install --agent claude|codex|kimi|gemini [--pin MOVE]... [--no-mcp] [--no-hooks]   (the agent skill this raea ships, for its version, which raea --version prints: an agent whose copy names another version reads this; install puts raea's skills where that agent reads skills, adds the blender MCP server unless --no-mcp, makes each --pin MOVE a /MOVE of its own, and adds raea's hooks to that agent unless --no-hooks (raea hook AGENT: media opened in the Mac's viewer goes to raea show, and the quick check after a composition is saved); a skill folder that's a link is left as it is)
```

Headless: it needs nothing running and opens no window. Takes up to 1 argument besides its flags.

## Flags

| Flag | Takes | What it does |
| --- | --- | --- |
| `--agent` | `claude\|codex\|kimi\|gemini` | Used by `skills install`; see [`raea skills`](skills.md). |
| `--no-hooks` | – | Used by `skills install`; see [`raea skills`](skills.md). |
| `--no-mcp` | – | Used by `skills install`; see [`raea skills`](skills.md). |
| `--pin` | `MOVE` | Used by `skills install`; see [`raea skills`](skills.md). |
| `--reference` | `cli\|feed\|files\|sdk` | Print this reference of the skill's instead of the skill itself. |

<!-- generated:end -->
