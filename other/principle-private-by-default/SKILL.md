---
name: principle-private-by-default
description: Preserve the wiki publication boundary when capturing personal knowledge or preparing public notes.
---

# Private by default

New personal knowledge goes to `apps/wiki/content/private`. Raw source material stays in ignored `raw/`. Both need a separate backup; Git intentionally ignores them.

Only explicit publication requests allow additions or changes to `content/public`. Public notes cannot reference private IDs or reveal private source material through summaries, quotations or metadata. A public URL is not permission to publish the user's notes about it.

Private filenames, titles and source URLs can themselves be sensitive. Do not include them in the tracked `docs/wiki-log.md`: use ignored `raw/wiki-log.md` for private activity. Use the tracked log for public changes only. Report private changes to the user in the current conversation without adding them to a public commit.

Commit and push only when requested. Never force-add ignored private files or raw evidence to a public repository. Publication involves deliberate content selection and public output validation; changing a file's directory alone is not a privacy review.
