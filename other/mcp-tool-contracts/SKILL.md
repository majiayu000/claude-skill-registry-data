---
name: mcp-tool-contracts
description: Canonical, single-source-of-truth mapping of "what I want to do via UEFN's MCP server" to "the exact tool that actually works for it in this kit's setup" — referenced by coder, qa-regression, and project-bootstrap instead of each describing the check in its own words.
---

# MCP tool contracts

Every agent that talks to UEFN's MCP server needs to do the same handful of things (verify which
project is open, list real project content, and so on). This file is the ONE place that says which
tool actually does each of those things in this kit's setup — every agent file references this
file by name instead of restating the instruction in its own prose.

**Why this file exists**: a v1.67 incident traced back to the exact same generic instruction
("list a couple of files through the MCP tools") appearing, worded slightly differently, in three
separate agent files (`coder.md`, `qa-regression.md`, `project-bootstrap.md`). `coder` picked
`AssetTools.find_assets` on `/Game` — the intuitive-sounding choice — which silently returns
nothing useful for this kit's custom project content even with the right project open, and reads
exactly like "the wrong project is open in UEFN," sending debugging in the wrong direction. Fixing
the wording in all three files at once worked, but it relied on remembering to touch all three
every time this file's contents change. A single referenced file can't diverge from itself.

## Contract: verifying which project UEFN has open

**Use:** `ValkyrieToolset.VerseToolset.ListFiles`

**Don't use:** `AssetTools.find_assets` on `/Game` — it silently returns nothing useful for this
kit's custom project content even when the correct project is open in UEFN. This is a
configuration-specific quirk of this MCP/UEFN setup, not documented anywhere in Epic's own docs as
of this writing — see the entry in `~/.claude/skills/uefn-lessons/SKILL.md`'s "MCP / tooling
quirks" for the original discovery.

**Procedure:** list the project's real Verse/asset content with `ValkyrieToolset.VerseToolset.ListFiles`
and check the path/name against the value already written at the top of the project's `CLAUDE.md`,
in the "Project identity" section — never the current folder's name (`Content`, identical across
every project). If the listing doesn't match, or is ambiguous, STOP and warn the owner: UEFN
probably has a different project open. Every agent that touches MCP before writing/modifying
anything runs this check first (`coder`, `qa-regression` before a play-session, `project-bootstrap`
during initial analysis).

## Adding a new contract

When a new MCP-tool gotcha gets discovered (a tool that seems right by name but doesn't do what's
expected, or two tools that both technically work but one is clearly the intended one for this
kit), add it here as a new `## Contract:` section with the same three fields — Use / Don't use /
Procedure — rather than describing it inline in whichever agent file happened to discover it. Also
add a short entry to `~/.claude/skills/uefn-lessons/SKILL.md` if the gotcha would help on a
different island, not just this project (see that skill's own guidance on the "would this help on
a different island?" test).
