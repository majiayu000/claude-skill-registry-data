---
name: obsidian-cli
description: 'Runs the obsidian CLI to read, create, search and edit vault notes. Use when the user wants vault work done from a shell ("obsidian CLI", "vault command line", "obsidian read/create/search from shell"). Not for OFM syntax (use obsidian-markdown).'
argument-hint: '[vault operation: read|create|append|search|tags|backlinks|property]'
allowed-tools: Bash(obsidian read *), Bash(obsidian daily:read *), Bash(obsidian search *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian create *), Bash(obsidian append *), Bash(obsidian daily:append *), Bash(obsidian property:set *), Read
---

## Overview

The `obsidian` CLI is an official command-line interface that requires Obsidian to be running. It allows reading, writing, searching, and inspecting vault notes from a shell.

## When to Use

Running `obsidian` shell commands against a vault in the live Obsidian app: reading, creating, appending to, searching and inspecting notes, and setting properties, from the terminal or a script.

### When NOT to use

- Obsidian is not running — the CLI requires the live Obsidian app to be open.
- Obsidian is closed and a script needs the notes — read the Markdown files directly instead.
- OFM syntax questions with no shell interaction — use `obsidian-markdown`.

## Core Process

1. Verify Obsidian is running before issuing CLI commands.
1. Use `file=<name>` for wikilink-style resolution, or `path=<vault-relative-path>` for exact path resolution.
1. For multi-vault setups, add `vault=<name>` to target a specific vault.

## Techniques

### Parameter conventions

- Parameters use `=` syntax: `file=NoteName`, not `--file NoteName`.
- Flags are boolean with no value: `--copy`, `--silent`, `--total`.
- Multiline content uses `\n` and `\t` escape sequences.

### File resolution

| Form           | Meaning                                        |
| -------------- | ---------------------------------------------- |
| `file=<name>`  | Resolves like a wikilink (search across vault) |
| `path=<path>`  | Exact vault-root-relative path                 |
| `vault=<name>` | Target a specific vault (multi-vault setups)   |

### Read operations

- `obsidian read file=<name>` — print note content.
- `obsidian daily:read` — read today's daily note.
- `obsidian search <query>` — full-text search.
- `obsidian tags` — list all tags.
- `obsidian backlinks file=<name>` — list notes linking to this note.

### Write operations

- `obsidian create file=<name> content=<text>` — create a note.
- `obsidian append file=<name> content=<text>` — append to a note.
- `obsidian daily:append content=<text>` — append to today's daily note.
- `obsidian property:set file=<name> key=<k> value=<v>` — set a frontmatter property.

### Developer / inspection

- `obsidian plugin:reload name=<plugin>` — reload a plugin.
- `obsidian dev:errors` — show console errors.
- `obsidian dev:screenshot` — take a screenshot.
- `obsidian dev:dom` — inspect the DOM.
- `obsidian dev:console` — open the console.
- `obsidian eval code=<js>` — evaluate JavaScript in the Obsidian context.
- `obsidian dev:css` — show applied CSS.

## Red Flags

- Using `--file` syntax instead of `file=` — parameters use `=`, not `--`.
- Running CLI commands when Obsidian is not open — the command will hang or error.
- Using `path=` when `file=` would work — `path=` requires an exact vault-root-relative path and is brittle across vault reorganizations.

## Verification

Run `obsidian tags` and confirm output. Obsidian must be running.
