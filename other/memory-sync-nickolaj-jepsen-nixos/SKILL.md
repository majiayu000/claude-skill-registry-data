---
name: memory-sync
description: Sync the current repo's memories both ways between pi's memory store and Claude Code's auto-memory, proposing every add and update for one approval. Runs in pi; needs its memory_save tool.
disable-model-invocation: true
---

Bring pi's and Claude Code's memories for this repo in line, one round of approval, nothing deleted. Without the `memory_save` tool (outside pi), say so and stop.

## Find both stores

- **Main checkout:** `realpath "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"`. If it differs from `git rev-parse --show-toplevel`, this is a linked worktree: stop and ask for a run from the main checkout, since `memory_save` would write the worktree's own store, which goes when the worktree does.
- **pi:** `${PI_CODING_AGENT_DIR:-~/.pi/agent}/memory/projects/<key>/*.md`, where `<key>` is `printf %s <main checkout> | sha256sum | cut -c1-16`. Frontmatter holds `id`, `kind`, `why_not_derivable` and `citations`; the first body paragraph is the statement, the rest is detail. The global store is out of scope.
- **Claude Code:** `~/.claude/projects/<slug>/memory/`, where `<slug>` is the main checkout path with every character other than a letter, digit or `-` turned into `-`. If it is missing, find the match in `ls ~/.claude/projects`. Each entry file has `name`, `description` and `type` (`user`, `feedback`, `project`, `reference`) frontmatter, sometimes nested under `metadata:`; `MEMORY.md` indexes them with one `- [file.md](file.md) — hook` line under a heading per type.

Either side may be empty or missing; that only means everything on the other side is an add.

## Match by topic

Read every entry on both sides and pair them by subject, not wording:

- same subject, same claim: in sync, leave it;
- same subject, one side newer, more specific or corrected: **update** the other;
- no counterpart: **add** it to the other side.

Skip status and plan entries on both sides: progress, plans, migrations not yet done, anything waiting on a date or an event. Say which ones you skipped.

## Propose once

Show one table: entry, direction (`CC → pi` or `pi → CC`), add or update, and the statement as it will land. Ask once; the user approves, drops or rewords rows in one reply. Write nothing before that reply.

## Apply

- **CC → pi:** one `memory_save` per row, never a direct file write. Kind: a correction or hard rule is `rule`, a taste is `preference`, a machine quirk is `environment`, a trap is `gotcha`, a pointer is `reference`. `why_not_derivable` comes from the entry's **Why:**; cite what the claim rests on that resolves now (a path, symbol or command, or a `quote` of the user's words from the entry). An update passes `replaces: <id>`. If the gate rejects a row, report its reason and move on; don't bend the claim to get it through.
- **pi → CC:** write `<id>.md` with `name: <id>`, `description: <statement>` and a `type` (`rule` and `preference` are `feedback`, `environment` and `gotcha` are `project`, `reference` stays). The body is the statement, then `**Why:**` from `why_not_derivable` and `**How to apply:**` from the detail. Add its line to `MEMORY.md` under the heading for that type. An update rewrites the body and the index hook, keeping the rest of the frontmatter.
- Never delete an entry or an index line on either side, and touch nothing of Claude Code's but those memory files: no settings, hooks or changes to how its memory works.

Finish with each row's outcome: saved, updated, rejected (with the gate's reason) or dropped.
