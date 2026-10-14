---
name: wiki-connect-notes
description: Find and explain relationships between a source and existing wiki concepts, sources and insights.
---

# Connect existing knowledge

Read [explain connections](../principle-explain-connections/SKILL.md) and [private by default](../principle-private-by-default/SKILL.md).

Search authored Markdown by source identity, author, specific terms and tags with `rg` in `apps/wiki/content/public` and `apps/wiki/content/private`. Read promising notes in full; do not link unseen search hits. Reuse the note IDs in their metadata.

For each worthwhile connection, identify the related claim and explain whether the new source supports, applies, extends or contradicts it. Use normal Markdown links to `/notes/<noteId>`; this app does not promise Obsidian `[[wikilink]]` support. Use typed relations only where they add meaning beyond an ordinary link.

For a request to suggest connections, return suggestions without editing. For an authorized capture, integrate relevant links into the source and update existing private concepts where evidence adds something useful. Do not rewrite unrelated notes, introduce link quotas or maintain a separate backlinks index.
