---
name: kpa-cleanup-roadmap
description: Remove completed items from ROADMAP.md to keep it focused on upcoming work
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Remove completed items from `ROADMAP.md` to keep it focused on upcoming work.

## Steps

1. Read `ROADMAP.md`.
2. Identify all completed items — these are items whose heading line contains `- [x]`.
3. For each completed item found:
   - The item consists of its `### - [x]` heading line **plus** all subsequent non-heading lines (body/description) up to the next `###` heading, `---` separator, or `##` section heading.
   - Remove the item (heading + body) from `ROADMAP.md`.
4. Clean up `ROADMAP.md`:
   - Remove any sections that are now empty (contain no `###` items). Keep the section if it still has at least one `### - [ ]` item.
   - Keep the header and the `Success Metrics` section regardless.
   - Update the `*Last updated:*` date at the top to today's date.
5. Show a summary of what was removed (item IDs and titles).
6. If there are no completed items to remove, say so and stop — don't make any edits.
