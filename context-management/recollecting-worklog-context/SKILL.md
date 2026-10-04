---
name: recollecting-worklog-context
description: Reads ~/worklog journal pages to recollect todos, insights, and open problems. Use for "what was I doing", catch-up, post-PTO.
argument-hint: a journal page, a date, or a span like "end of last week"
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(date:*), Bash(rg:*), Bash(sed:*), Bash(head:*), Bash(tail:*), Bash(find:*), Bash(wc:*)
---

# Recollecting worklog context

Reading, not writing. The journal is a scratchpad: half-sentences, bare links,
notes-to-self. The job is to reconstruct **what was being worked on, why, and
what has since moved** — never to append to the vault (that's
`updating-worklog-vault`) and never to guess at state the pages don't record.

## Core recipe

```bash
cd ~/worklog
date +%F                       # never take today's date from memory
ls Journal/ | tail -15         # dates are SPARSE: no entry ≠ no work
cat Journal/2026-09-14.md      # the anchor page the user named
```

Then read the 2–4 *populated* entries before the anchor, in full — entries are
short, and excerpts lose the notes-to-self that carry the intent.

```bash
for f in Journal/2026-09-11.md Journal/2026-09-10.md; do echo "=== $f ==="; cat "$f"; done
```

Follow the trail outward only when the journal points there: a wikilink, or a
topic page whose name matches a thread (`rbf-improve.md`,
`failure-modes-aug27.md`, `simtest/<job-id>.md`).

```bash
rg -l 'dense traffic' --glob '*.md' .   # topic pages carrying a thread
```

## What to pull out of a page

| Bucket | Looks like |
|---|---|
| **Todos** | `Today:` / `Today you are:` / `You are:` lists, `- in prog` |
| **Assignments** | "X wants…", "Todos from X", meeting residue |
| **Insights** | prose paragraphs, hypotheses, notes-to-self ("you gotta…") |
| **Problems** | bare triage/Slack/video links, often with a one-line verdict under them |
| **Bets** | tables mapping situation → response → proposed fix |
| **Runs** | pasted commands with `tag=`, launch times |

A bare link with a scribble under it *is* a finding — that scribble is the whole
diagnosis. Quote it.

## Reporting the evolution

Compare the anchor against the earlier entries and name the **arc**, not just
the deltas. Typical shape: diagnose → structure into bets → execute a subset.

1. One short paragraph per earlier day: what was in flight, with the concrete
   artifact (command, table, link) that proves it.
2. A then/now table for the todos themselves — what got promoted, demoted,
   sharpened, or absorbed into a run.
3. **Name what silently dropped.** Items listed earlier and absent now are the
   highest-value output; say they're unpicked rather than letting them vanish.
4. Flag external pressure that reordered priorities ("X wants this solved") and
   new collaboration angles separately from self-directed work.

## Rules

- **Never invent progress.** If a page doesn't say an item finished, it's
  in-progress or unknown — say which.
- **Sparse dates**: "end of last week" means the last populated entries, not
  Thu/Fri by calendar. State which dates you actually read.
- **No git.** `~/worklog` isn't a repo; the dated files are the only history.
- Attribute per-day, so the user can tell Thursday's thinking from Friday's.
- Quote their phrasing for hypotheses and self-directives — the wording is the
  memory hook.
