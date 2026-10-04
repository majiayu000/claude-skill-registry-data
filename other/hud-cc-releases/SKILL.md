---
name: "HUD: Claude Code Releases"
description: "Summarise Claude Code's own CHANGELOG.md, filtered and grouped for what actually matters to Jason"
when_to_use: "When Jason asks what's new in Claude Code, whether to update or what changed since a given point."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: hud
disable-model-invocation: false # read-only viewer, no gate needed
disallowed-tools: ["Edit", "Write", "NotebookEdit"]
allowed-tools: ["Bash(curl:*)", "Bash(awk:*)", "Bash(grep:*)", "Bash(npm view:*)", "Bash(claude --version)", "Read", "AskUserQuestion", "Skill(track-cc_pain)"]
arguments: ["number", "unit"]
argument-hint: "[<n> <d|w|m|v>] e.g. \"1 w\", \"3 d\", \"10 v\" (default: since your installed version)"
---

# HUD: Claude Code Releases

Claude Code's real `CHANGELOG.md` lives at the root of `anthropics/claude-code` on GitHub, one flat bullet list per version, no subsections. It is long (thousands of lines) and mostly noise for this stack: Windows, WSL, Bedrock/Vertex/Foundry, self-hosted-runner fleets, Team/Enterprise admin. This skill fetches it, slices the requested range and reports only what earns a look, grouped by subsystem.

## Step 1: Resolve the range

Two positional args, `<number> <unit>`. Unit is one of:

| Unit | Meaning |
|---|---|
| `d` | days |
| `w` | weeks |
| `m` | months |
| `v` | versions back from latest |

Examples: `1 w` (last week), `3 d` (last three days), `10 v` (last ten versions).

**No arguments**: default to `claude --version` (installed version) as the floor; range is `installed..latest`. This is the actual question most of the time: "what have I missed."

**`v` unit**: that many versions back from latest, no date lookup needed.

**`d`/`w`/`m` units**: version headings (`## 2.1.238`) carry no dates, so resolve via the npm publish-time map:

```bash
npm view @anthropic-ai/claude-code time --json
```

Take that map's own most recent timestamp as "now" (no other clock is available to the script), compute `now - (number × unit)`, and use the first version published on or after that point as the floor.

If the npm time map and the changelog's version set diverge (a version in one but not the other), say so once and fall back to the nearest available version rather than guessing.

A single token with no unit ("1w", "3d") or a unit spelled out ("week", "days") should still resolve sensibly, don't reject on formatting when the intent is obvious; but the canonical form given to the user is always the two-token one above.

## Step 2: Fetch and slice, never load the whole file

```bash
curl -s https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md -o /tmp/cc-changelog.md
```

Use the session scratchpad, not `/tmp`, for the actual output file. Then slice with `awk` on `^## ` boundaries to pull only the resolved range into a second file. Read that slice, not the source file: at ~5,700 lines the full changelog blows the context budget for zero benefit, and pre-summarising it with WebFetch is worse, since WebFetch runs content through a small model that will chew the exact bullets this skill needs to judge verbatim.

## Step 3: Split every bullet into capability or fix

These two kinds clear the relevance bar in different ways and get filtered separately. A bullet is a **fix** if its changelog wording is fundamentally "X was broken, now it isn't" (the file's own `Fixed`/`Hardened` prefixes, and any `Changed`/`Improved` bullet that's really a bug being quietly corrected). Everything else (genuinely new capability, a behaviour change you'd choose to use, a setting worth knowing exists) is a **capability**.

### Capabilities: filter by "would Jason recognise the use, unprompted"

Source the relevance signal live, don't hardcode a stack list that will drift:

- CLAUDE.md's technical profile (already in context every session): TypeScript/Bun/SvelteKit, Zed, macOS, git worktrees.
- `~/.claude/skills/` contents: he authors skills and plugins, so anything about `SKILL.md` parsing, `claude plugin validate`, marketplaces, frontmatter is relevant even if he wouldn't describe himself as "into plugin infrastructure."
- This session's own environment: worktrees, output styles, hooks, MCP servers, cross-session `SendMessage`/`ListAgents`, subagent forking: these are demonstrably in active use, not inferred from the changelog talking about them.

**Drop on sight, no exceptions:** Windows/WSL, Cygwin, PowerShell; Bedrock, Vertex AI, Foundry, apps gateway internals; self-hosted-runner fleet operations; Team/Enterprise admin policy, managed-settings schema; mTLS/cert rotation for gateway deployments; IDE-specific items for IDEs he doesn't use (check `~/.claude/skills` / config for VS Code or JetBrains signal before dropping `[VSCode]` items; if absent, drop).

**Keep even when small:** anything touching skills/plugins/marketplaces, subagents/Agent tool semantics, git/worktree behaviour, terminal/keybinding UX, cross-session messaging, MCP client-side behaviour, model/effort selection.

A capability only earns its place if the bullet is self-evidently actionable as written: the reader gets from the description to "oh, I'd use that" without help. If it takes an explained "why this matters" clause bolted on to justify itself, it isn't self-evident: cut it, don't prop it up with an explanation. Prefer three sharp keeps over five that need footnotes.

### Fixes: filter by logged pain points only, not by subsystem match

A fix bullet earns a place only if it plausibly resolves an entry in `library/state/cc-pain-points.json` with `resolvedIn: null`. Subsystem relevance (worktrees, skills, MCP) is not sufficient on its own: a fix for a bug Jason never hit is not news, however on-brand the subsystem is. Two narrow exceptions that surface regardless of the pain-point store: a fix for a genuine security/data-loss issue (framed as risk removed, not bug re-lived) and a fix explicitly requested this same run ("did they fix X" prompted the check).

Read the open entries and the fix bullets from this range, and match by meaning: the pain-point description and the changelog's eventual phrasing will rarely share vocabulary (worktree isolation blocking a safe git command vs. "worktree-isolated sessions... running destructive git commands" describe the same friction from opposite ends). Judge the underlying cause, not keyword overlap.

For each candidate match, do not resolve it silently. Ask first:

> `AskUserQuestion`: "This looks like it might fix a logged pain point: '{{entry.description}}'. {{version}}: {{bullet text}}. Does this address it?"

If confirmed, call `Skill(track-cc_pain)` with an instruction to mark that entry's `resolvedIn`/`resolvedNoted` (do not write to the JSON directly: this skill stays read-only; the write is `track-cc_pain`'s job). If not confirmed, leave the entry open and don't surface the bullet as a "this is fixed now" item.

## Step 4: Group thematically and report

Group by subsystem, not by the changelog's own `Added`/`Fixed`/`Improved`/`Changed` prefixes: those are change types, not themes, and grouping on them just yields a shorter copy of the same document. Useful groups tend to be: skills & plugins, agents & subagents, git & worktrees, MCP, terminal & rendering, models & effort, cross-session messaging. Cap at ~5 groups, ~5 items per group, drop empty groups silently. If the filtered set is genuinely small (a quiet week), say so in one line rather than padding.

Each item: one line, plain language, what changed, in the reader's own vocabulary where the changelog's wording buries the point. Name the version it landed in. State the change directly; don't append a justifying clause explaining why it matters: if it needs that explanation to land, it belongs in the drop pile, not on the page with a crutch attached.

If items were dropped for being out of scope, don't list them individually; a single closing line ("N other changes this range, all Windows/Enterprise/Bedrock: skipped") is enough so the omission reads as deliberate rather than incomplete. Fixes dropped for having no matching open pain point don't need their own tally; they were never candidates.

## Red flags

**Never** paste the raw changelog slice back as the answer, that isn't a summary. **Never** run this through WebFetch. **Never** report on the full file when a range was requested; scope discipline is the entire value of this skill over just reading the changelog directly. **Never** surface a fix bullet on subsystem relevance alone; it needs a matched, confirmed pain point (or the security/data-loss exception). **Never** write to `cc-pain-points.json` directly; that's `track-cc_pain`'s job, called only after explicit confirmation.

<raw-arguments value="$ARGUMENTS" />
