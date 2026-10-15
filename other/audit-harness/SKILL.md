---
name: audit-harness
description: Analyzes this project's coding-agent harness (CLAUDE.md, skills, subagents, commands, hooks, MCP servers, plugins) against the session transcripts already saved on this machine, and suggests evidence-based changes. Use when the user asks to improve, audit or clean up their harness, asks why the agent keeps making the same mistake, asks whether a skill, subagent or instruction is worth it, or asks whether a harness change helped.
argument-hint: "[what to analyze, e.g. 'only code-reviewer, last 2 weeks' or 'did my change help?']"
model: opus
---

# audit-harness

You turn deterministic signals from the user's own sessions into a short list of classified, evidence-backed suggestions for their harness. The numbers come from a local script; your job is to judge, classify and write the change. Never invent a number, a session or a step.

The request: $ARGUMENTS

## The model

The script counts; you judge. Grouping signals by cause, telling real friction from ordinary work and choosing the right fix is the judgment this skill exists for. Don't comment on which model you are running on.

## The script

All data comes from the bundled script. Run it with Bash from the project root:

```bash
node "${CLAUDE_PLUGIN_ROOT}/dist/harness-ledger.mjs" <command> [options]
```

It needs Node.js 20+. If `node` is missing or older, look for a newer one the person already has (`nvm`, `fnm`, `volta`, `mise`, or `~/.nvm/versions/node/*/bin/node`), use it and say which in one line; stop only if there is none. It reads transcripts in place, prints JSON, and writes only to `.harness-ledger/` in the project.

Always pass `--exclude-session ${CLAUDE_SESSION_ID}` to `analyze`, `compare` and `status`, so the session running this analysis isn't counted.

| Command | Use it for |
| --- | --- |
| `analyze [--since 14d] [--until DATE] [--piece ID]...` | Inventory + signals + per-piece usage. Prints a compact JSON; the full result goes to `.harness-ledger/last-analysis.json`. |
| `evidence <signal-id>` | All evidence (session, transcript line, thread, redacted excerpt) for one signal. |
| `inventory` | The active harness with piece ids (`agent:code-reviewer`, `skill:changelog`, `instructions:project`, `hook:...`, `mcp:...`). |
| `compare --piece ID [--at DATE]` | Before/after metrics for one piece. |
| `suggestions list [--status S]` · `suggestions add --file F` · `suggestions set ID STATUS [--note T]` | Suggestion state, so nothing is suggested twice. |
| `issue <signal-id> --note T` | A prefilled GitHub issue questioning the rule behind a signal, in the person's words. Nothing is sent. |
| `status` | Transcripts available, retention, config. |

Options shared by all commands: `--project-only` (ignore user-level and plugin pieces), `--all-projects`, `--no-cache`.

## Pick the flow

Read the request and pick one flow. If it's empty or vague, use flow 1.

1. **Analyze history** (default) — "improve my harness", "what's wrong with my setup".
2. **Focus on a piece or period** — names a subagent, skill, command, MCP server or instruction file, or a period ("last 2 weeks"). Same as flow 1 with `--piece` and/or `--since`. If the piece name is ambiguous, run `inventory` and match it to an id; ask only if two ids fit equally.
3. **Compare a change** — "did my change to X help?", "is it better since I edited CLAUDE.md?".
4. **Manage suggestions** — "show pending suggestions", "apply the second one", "reject X".

Before any flow, read `references/findings.md` in this skill's folder (`${CLAUDE_SKILL_DIR}/references/findings.md`). It has the classes, the rules and the report format. Follow it exactly.

## Flow 1 and 2: analyze

1. Run `analyze` with the options from the request. Read the JSON. If `omittedSignals` is above 0, run it again with `--max-signals 200`: triage needs every signal, not the first 25.
2. Tell the user in one line what was analyzed: sessions, period, and how much history exists (`history`). If `history.transcriptsAvailable` is small or `history.oldestAt` is close to `retentionDays` ago, say that older sessions were already deleted by the agent's retention setting. Never change that setting.
3. If `analyzed.sessions` is 0, say so, suggest a wider period or `--all-projects`, and stop.
   If `inventory.pieces` has no `instructions:*` piece, the project has no harness yet: follow "Starting a harness" in the reference as well. When a suggestion creates a skill, subagent or command, or a signal points to a problem a plugin solves (exploration taking most of the context, agents guessing paths), read `references/community-extensions.md` first. When `checks.missing` isn't empty and there are corrections about code quality or fix loops, read `references/deterministic-checks.md`.
4. Triage. **Examine** every signal that meets any of these: at least 5 active minutes, 3 or more sessions, or among the first 15 by `score`. Rank and judge by time as much as money, never by money alone; when `totals.unpricedModels` isn't empty, money is undercounted, so time decides. Signals below the bar aren't examined; the report counts them. For each examined signal:
   - Read what shapes that behavior today, not only the piece the signal names (paths are in `inventory.pieces`):
     - `main`: the instruction files (`instructions:*` pieces), since they guide the main thread.
     - A skill: its `SKILL.md` and, from its `files`, the references or scripts the failing step uses. The change often belongs there.
     - An agent: its file and the skills in its `preloadedSkills`.
     - A command: its file and the skill it runs, if any.
   - Before writing a change, look in what you read for other instructions about the same thing. If two pieces disagree, the conflict is the finding (see rule 8 in the reference).
   - Use `details.mentions` when present: a failure the harness already has an instruction for is **Rule exists, but is ignored**.
   - If you need more evidence, run `evidence <signal-id>`. Don't read whole transcripts; if you must check one step, read only the cited line (`sed -n '<line>p' <file> | cut -c1-2000`).
   - If `changedAfterEvidence` is set, the piece changed after the newest evidence. Look at what changed (`git log -p --since=<lastSeenAt> -- <path>`, or the file itself when it isn't in git). Only when the change touches the cause does the signal go under "Changed since this evidence"; a change elsewhere in the file (a new model, an unrelated section) leaves it a finding like any other.
   - Before you set an examined signal aside as ordinary work, a decision of the person's, or noise, run `evidence <signal-id>` and read it. The reason you give cites what the evidence showed ("the 3 corrections are about the button's color, not a rule"), never a guess.
   - Corrections and rejected plans: group their texts by theme before judging. A theme that comes back in 2 or more sessions is a rule the harness is missing (usually Missing instruction), even when each correction looks like a product decision. Only a theme seen once may be set aside as the person's own call.
   - A sequence a skill already prescribes step by step and the agent still runs by hand, again and again, is what a script replaces: "the skill already says so" is not a reason to set it aside.
   - When you suspect the script counted wrong (a piece shown as unused that you can see being run, a cost that includes work the signal shouldn't), say so in one line and offer `issue <signal-id> --note "<what looks wrong>"`, the same way as a rule the person disagrees with.
   - If `handledBy` is set, it goes under **Already handled** with its status. Never suggest it again.
   - Also treat as already handled anything an open branch or PR already changes: check `git branch --list` and, if `gh` works, `gh pr list --state open --limit 20 --json title,headRefName,files`. Skip this silently when not a git repo or `gh` isn't available.
   - Classify it with exactly one class and write the change, following the rules in the reference. If you don't turn it into a suggestion, it goes under "Examined, not suggested" with its time and the reason.
   - When the piece has `linkedPath`, its file lives elsewhere (often a shared repository the project links in). Say so; a change there reaches everyone who links it, so it is made in that repository, on a branch, leaving any uncommitted work there alone.
5. Group signals that share a cause into one finding (for example, `failed_command:npm test` and a correction saying "use pnpm").
6. Write the report in the format from the reference, save it to `.harness-ledger/reports/<YYYY-MM-DD-HHMM>.md` (never overwrite an earlier report), and show it to the user. At most 7 new suggestions, ordered by strength of evidence first (several sessions before one, complete before partial), then by `score`, so a one-session upper bound never leads the list. In the chat, show besides them: the pending suggestions from earlier runs (one line each, largest first), the examined signals you didn't suggest (one line each, with time and reason), and how many smaller signals weren't examined. The person shouldn't have to ask what else there is.
7. Register all suggestions in one `suggestions add --file <tmp.json>` call (an array of `{title, class, piece, signals, occurrences, change}`; `signals` are the signal ids the finding came from). When two suggestions come from the same signal, split it: in each, list in `occurrences` the evidence (`{sessionId, line}`, from `evidence <signal-id>`) that its change would have prevented; each occurrence goes to one suggestion, and at most one of them may leave `occurrences` out to take the rest. The script refuses overlaps. Use the returned ids, and take each suggestion's time, tokens and money from the returned `costs` (and `covered` for their sum), never from the signals. When a signal's cost includes work the change wouldn't remove, list in `occurrences` only those it would prevent, rather than footnoting an overstated figure.
8. Ask which suggestions, if any, the user wants applied (see "Applying").

If `.harness-ledger/` is not in `.gitignore` and the project is a git repo, ask once whether to add it there (or to `.git/info/exclude`). Don't add it without asking.

## Flow 3: compare a change

1. Find the piece id (`inventory` if needed) and when it changed: an applied suggestion, the date the user gives (`--at`), or the piece's last change (git commit, else file mtime). The script picks this automatically; say which source it used.
2. Run `compare --piece <id>`.
3. Report before vs. after: sessions, error rate, corrections per session, time, time until failures recovered, input and output tokens, and cost per use, and the signals on each side. Use the script's `verdict`:
   - `insufficient_data`: say how many sessions each side has and that it needs `minSessions` per side. Don't conclude anything.
   - `improved` / `worse` / `mixed` / `no_clear_change`: say it, and always add that this is an observational comparison of different tasks, not a controlled test.
   - Describe the verdict with `moves`, the metrics that changed: time per use counts as much as cost, so "same cost, 40% faster" is an improvement. For `mixed`, name the trade-off ("40% faster, 30% more expensive") and let the user weigh it.
   - Moves with `isInVerdict: false` are input and output tokens per use and time until failures recovered. Report them ("30% fewer output tokens", "half the time stuck on failures"), but they don't decide the verdict: they are already in `usdPerInvocation` and in active time.

## Flow 4: manage suggestions

- List: `suggestions list` (optionally `--status pending`). Show id, title, class, piece, status.
- Accept or reject: `suggestions set <id> accepted|rejected --note "<reason>"`. A rejected suggestion is never suggested again; keep the user's reason in the note.
- When the reason says the rule itself is wrong for this project ("plans are rejected on purpose here", "that command is supposed to fail"), offer once to report it: `issue <signal-id> --note "<their reason, in their words>"` returns a link to a prefilled GitHub issue (`issueUrl`) and a search for an existing one (`searchUrl`). Show both; the person opens the link, reads it and decides whether to send it. Never put session excerpts, file paths or commands in the note.
- Apply: see below.

## Applying a suggestion

Only when the user explicitly asks for a specific suggestion. Then:

1. Show the exact change (a diff or the new text) and the file it touches, and wait for a yes.
2. Only edit harness files: `CLAUDE.md`, `CLAUDE.local.md`, files under `.claude/` (agents, skills, commands, settings hooks and permissions), and `.mcp.json`. User-level files under `~/.claude/` only when the user names them. Never edit plugin files (they're overwritten on update; suggest the change to the plugin's author instead), application code, or retention settings.
3. Prefer the smallest change that fixes the cause. For "Rule exists, but is ignored", that is a hook, a script or a permission rule — not more text.
4. After editing, run `suggestions set <id> applied`. Tell the user that running the comparison after a few more sessions (at least the configured minimum per side) will show whether it helped.
5. If the project is a git repo, offer to commit the change on a branch; don't commit or push unless asked.

## Hard rules

- Every finding cites its evidence: session id (first 8 characters), transcript line and thread. No evidence, no finding.
- Numbers come only from the script. Time and cost are always labeled as estimates. If `totals.unpricedModels` is not empty, say that those models' cost is not included; you may look up a model's price and propose it as an entry in `.harness-ledger/config.json` (`modelFamilyToPrice`: a family such as `"glm"` with `inputUsdPerMillionTokens` and `outputUsdPerMillionTokens`) with its source, but use it only after the person confirms and the script recomputes. `totals.reportedByProvider` holds the agent's own cost and turn time; show it beside the estimate, never summed with it. Each signal's `cost.bound` says whether to write "at least", "at most" or "about".
- Never show secret values. The script redacts excerpts; if you read a transcript line yourself, don't copy credentials, tokens, keys or personal data into the report, suggestions or commits. If you notice an exposed secret, tell the user privately in one line and don't turn it into a suggestion.
- Stay in scope: unrelated bugs or code issues you notice in transcripts are not harness findings. Mention them in one line at most, outside the suggestion list.
- Don't apply anything without explicit confirmation for that specific suggestion.
