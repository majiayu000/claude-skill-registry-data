---
name: war-journal
description: Sokka's war journal, the short record of what the campaign actually won. Use for what-did-i-get-done, /what-did-i-get-done, "what did I get done", "what did I ship", "summarize my commits", standup notes, or a status update over a time range such as yesterday, the last 3 days, or last week. Summarizes the current git user's authored commits in that range into a concise, dated update.
---

# Sokka's war journal

Sokka writes the day's entry the way a scout reports. What was taken, what held, and nothing about how brave anyone felt. A journal entry is short, dated, and true to the record.

## Steps

1. **Resolve the window.** Turn the requested range ("yesterday", "last 3 days", "last week") into concrete dates in the user's local time zone. State them.
2. **Read the record.** List the commits the current git user authored in that range. Match on `git config user.email`. Exclude merge commits. Ignore uncommitted changes.

   ```sh
   git log --all --no-merges --author="$(git config user.email)" \
     --since="<start date> 00:00" --until="<end date> 23:59" \
     --date=short --format='%h %ad %s'
   ```

   Read the full message or `git show --stat <sha>` for any commit whose subject does not say what changed.
3. **Pick what mattered.** Keep substantial behavior and architecture changes. Drop cosmetic-only changes (formatting, imports, minor renames).
4. **Write the entry.** Synthesize the kept changes into one status update.
5. **Date it.** Include the actual date range you used.

## Rules

- Be extremely concise and information-dense.
- Describe changes by what they do. Do not infer intent or motivation.
- Write with `tea-time`. No long dashes, no filler.

## Output

- One short summary, ready to paste as a status update.
- The real date range.
- Optionally two to five bullets, for major changes only.
