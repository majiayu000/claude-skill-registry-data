---
name: memory-crosslink
description: "Use when writing or editing a memory file that relates to 2+ other memories: add See also: [[stem]] wikilinks so mem-graph-build.py builds the edges. On-demand; moved out of CLAUDE.md."
---
# Memory cross-linking

When a memory relates to 2+ others, add `See also: [[target_file_stem]], [[other_target_stem]]` at the bottom: the target file's stem (no `.md`, no path) inside double brackets. `{agency-root}/scripts/mem-graph-build.py` parses these as edges. Legacy `[Title](file.md)` links still resolve, but use `[[wikilinks]]` for new links.
