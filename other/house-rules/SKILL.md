---
name: house-rules
description: "Use when you need the stack's shared rules: gates, evidence labels, artifact shapes, team levels or routes, or the user is unsure how to proceed or asks what exists."
user-invocable: false
---
# House rules
Job: Hold the stack's shared rules and help anyone find the right route.
Takes: a situation or a lookup.   Gives: a recommended route, or the rule.

## Steps

1. For a rule, open the file named under Files and answer from its text.
2. For a route, open `routes.md` and follow its navigator. Open each block before you describe it or advise skipping a step. The map only orients; the block's own text decides.
3. Apply Project language and the work rules below to all work, inside every block.

## Following a reference

Blocks point at each other in one form: ``Use the skill `<name>` `` and ``the file `gates.md` in the skill `house-rules` ``. Slash commands, plugin-prefixed names, skill-loading tool names and relative paths across skills only work on some hosts, so keep them out of skill text.

To follow that phrase:

- Claude Code: load the skill by name. Its base directory holds its files.
- Codex, OpenCode: open `~/.agents/skills/<name>/SKILL.md`. Its files sit beside it.
- Any MCP client: read it with the dami hub's `skills` tool. With no arguments it lists the skills, and `{name, file}` reads one.

## Roles

| Role | May | May not |
|---|---|---|
| lead | Talk to the user, hold the graph, cross gates with OK, land work, write glossary and records | Do long work in its own context when a worker can |
| worker | Change code in its own tree | Ask the user, cross a gate, reopen settled decisions |
| scout | Read and report | Change anything |
| checker | Verify and issue a verdict | Check its own work, fix what it finds |

Workers and scouts send questions up through `Open` and gate needs through `Needs OK`. In a nested tree, the gate goes up to the top lead.

## Work rules

1. Act on reversible work without asking. Stop only for a gate, a missing necessary detail, or a choice that materially changes the outcome.
2. Capture what the user asked as a numbered `Asked` list, in their words, on first contact with multi-part work. It travels in every packet and `finish-line` closes against it.
3. Copy explicit limits (no tests, no builds, planning only, someone else's area, timing, a named package manager) into `Limits`. Limits outrank every block's method.
4. Stay in the phase asked for. Never substitute a plan, mock or placeholder for the deliverable.
5. After a correction, reassess the evidence and fix the cause. Do not repeat the mistake or only reword.
6. Use cross-platform tools: Node scripts, not bash, for anything shipped. Windows with cmd.exe and PowerShell is the main machine. Hooks and scripts run through `node`.
7. Redact secrets and personal data from anything shown or leaving the session.

## Shared habits

- **Activation.** Reach for a block when its description fits the state of the work, whether or not the user named it.
- **Project language.** Before exploring code, read the glossary and the relevant decision records if they exist. Use their words in everything you produce. A concept you need that the glossary lacks is a signal: either you coined a term or the glossary has a real gap. If your output contradicts a record, say so openly and argue for reopening it.
- **Missing glossary.** Stay silent when reading. Offer to create one only when you are about to write to it.
- **Missing setup.** A block that finds no tracker or label configuration uses the skill `repo-fitting` itself. The user is never told to do it.
- **Tracker work.** Blocks say publish, fetch, comment, label, block, close and claim. The repo's tracker document maps each to a command or file edit.
- **Test seams.** `work-chart` checks seams with the user once. `failing-test-first` announces seams and continues, and asks only if a seam changes what gets built. Cards carry the agreed seam to workers.
- **Delegation.** Helpers start with an empty context. Keep exchanges short and pass references, not copies.

## Prefs

`~/.dami/prefs.md` holds the user's standing preferences, one line each. The session hook injects it on Claude Code; elsewhere, read it at session start if it exists. Only the user writes it: propose a line, and their saying yes is the OK to add it.

- `ok: <gate> <scope>`: a standing OK, defined under Standing OK in `gates.md`.
- `show: <command> <file>`: the delivery channel. When set, share pages, images and video only through it, give the URL it prints, and never publish host artifacts. A hook enforces this on Claude Code.
- `taste: <note>`: look and style preferences for visual work.

## Files

- `gates.md`: what needs the user's OK, how to ask, and the reminder line. Read before anything outward or hard to undo.
- `levels.md`: level detection, the tools behind each team move, the hub's limits, the check ladder. Read before the first team move.
- `deck-adapter.md`: what changes inside a Deck thread. Read it only when `levels.md` sends you there.
- `artifacts.md`: artifact shapes, packet, report, evidence labels, ref forms, bench layout. Read before writing or receiving any artifact.
- `routes.md`: routes, the navigator, every block and command. Read when unsure what fits.
- `routing-map.md`: the lead's always-on summary. The session hook injects it on Claude Code; the dami hub's MCP server sends it to other clients. Skip it if it is already in your context.
- `worker.md`: the short card the MCP server sends Claude subagents and hub runs in place of the map: role limits, waits, output caps, the report. Read it when a lead started you.
- `scripts/bench.js`: run `node <house-rules>/scripts/bench.js` to print the bench path and create the bench. `<house-rules>` is this skill's folder. Expand `~` yourself, because cmd.exe doesn't.

## Done when

- A lookup is answered from the text of the named file, not from memory.
- A route recommendation names one route, and every block it names was opened first.
