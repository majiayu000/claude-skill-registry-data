---
name: runlab-sync
description: Fetch new runs into the local cache and report what actually arrived — counts, coverage per channel, gaps and duplicates. Use when the user says "sync my runs", "import the latest activities", "update runlab", or invokes /runlab:runlab-sync. Talks to a network source and can take minutes, so only the user starts it.
allowed-tools: Read, Bash
disable-model-invocation: true
argument-hint: "[--since YYYY-MM-DD]"
---

# runlab sync

Fetching is the easy half. The half that matters is telling the athlete what did
**not** arrive, because a silently truncated import turns into a wrong finding
three weeks later.

## Standing rule

Run every script through the shim, and check `--help` before relying on a flag.
If a script is absent or its interface differs from what is written here, say so
and stop — do not fetch or parse the source by hand.

## Step 1 — fetch

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/sync.py"
```

Options: `--source <name>` to pick one configured source, `--since YYYY-MM-DD` to
limit the window, `--all` to rebuild from scratch, `--limit <n>` for a probe,
`--dry-run` to see what would happen, `--json` for the machine-readable report.
Without `--since` the script asks every source for everything and skips what the
cache already holds; it does not re-download what it already has, and `--since`
never removes older activities from the index.

Exit codes: `0` finished and every assurance held, `1` finished but something is
wrong, `2` could not start (no data root, no credentials, no readable directory).
On `1` and `2` the output carries `reason` and `hint` — relay the hint, it names
the missing thing.

An exit code of `1` has two causes and they read differently:

- `reason: partial_import` — a source delivered less than it holds. Name the
  source and its own reason.
- `reason: assurance_violated` — the import ran but the cache is not in a state
  worth analysing. Read `assurances[]`, name every entry whose `status` is
  `violated` together with its numbers, and **say that analyses should wait**.
  A shrinking activity count, an activity that claims samples and has none, a
  channel whose coverage collapsed, or a missing raw payload each invalidate
  results computed afterwards. Never summarise this as "sync finished".

`status: skipped` on an assurance is not a pass. It means the check could not
run — usually because this is the first sync and there is no baseline yet. Say
so rather than counting it as green.

This skill writes only into `cache/`. It never touches `state/` or
`profile.json`; a PreToolUse hook enforces that.

## Step 2 — confirm what landed

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" \
  --section computed.activities --section computed.data_quality --section computed.gates
```

| Where | What it settles |
|---|---|
| `computed.activities.n_running`, `.first_date`, `.last_date`, `.span_days` | how much history is now in the cache |
| `computed.activities.n_unusable_entries`, `.n_undated` | entries that arrived but cannot be used |
| `computed.activities.index.age_days` | how fresh the cache is |
| `computed.data_quality.channels[]` | per channel: `n`, `n_total`, `coverage` |
| `computed.gates` | which analyses the new data unlocked, and what the rest are short of |

The sync's own report answers what `read-db.py` cannot, because it knows what was
asked for and not delivered. Read these blocks out of it:

| Where | What it settles |
|---|---|
| `sources[].accounting` | files seen against activities built — the reference folder yields 35 activities from 104 files, and only this block says why |
| `sources[].placeholders` | iCloud stubs that were skipped; the athlete believes those runs are imported |
| `coverage.summary` / `coverage.running` | per channel, `n of n_total`, for everything and for the runs alone |
| `streamless.n_structural` / `.n_failed` | recordings that carry no samples versus fetches that failed — never add these together |
| `duplicates.decisions[]` | which version of a run was kept, which was dropped, and on what evidence |
| `gaps.gaps[]`, `gaps.empty_months` | holes in the time series, including a month the export skipped entirely |

Rules for reporting it:

- Always give counts as *n of n_total*. "Mechanics missing in 12 runs" is
  unusable; "12 of 76" is a fact. The block gives you both — use both.
- A gap in the calendar is not a training gap. It may be an import problem, a
  rest week, or an injury. State it as a data observation and ask.
- Failures and unusable entries are never rounded away, even when the count is
  small. Name the ids and the reason codes.
- If mechanics coverage is 0 and the configured source is GPX or TCX, say that
  this is the source's ceiling, not a device fault.
- If coverage dropped against the previous sync, say so plainly: a watch that
  stopped delivering mechanics after an update looks exactly like a form change
  to every analysis that follows.

## After a sync

- Nothing goes into the state database from here. A sync produces facts about
  the cache, not findings about the athlete.
- If the athlete wants the new runs interpreted, hand over to
  `/runlab:runlab-run` for a single run or `/runlab:runlab-report` for the
  overview.

## Do not

- Do not retry a failed source in a loop. One retry, then report.
- Do not fill a gap by interpolation, in the cache or in your answer.
- Do not quote a number that is not in this script's output.
