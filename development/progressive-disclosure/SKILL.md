---
name: progressive-disclosure
description:
  Refactor a Claude Code skill so its conditional detail loads only when an
  observable project marker says it applies.
disable-model-invocation: true
version: 0.2.1
---

# Progressive Disclosure

Refactor one target skill so its core workflow stays in `SKILL.md` and
conditional detail loads only when it applies. Every fact, example, and caveat
in the old files survives the move.

Apply the refactor. When the user asks for analysis only, stop after step 2 and
report the proposed layout.

## Process

### 1. Trace the current loading paths

Read the target `SKILL.md` and every file it links. Find inbound links to those
files across the plugin.

Inventory each distinct topic, where it lives, and what makes it relevant. State
each topic's relevance as a **marker** - something observable in the project: a
filename, a config key, a command, a tool name, or a mode the user picks. Create
a separate file only when the topic has its own marker, so a long file with one
marker stays whole and a short file with three markers splits.

Done when every topic is marked always-needed or conditional, and every
conditional topic names its marker.

### 2. Choose the disclosure boundaries

Keep in `SKILL.md` the core procedure, the safety constraints, and the guidance
every invocation needs. Push conditional details into references.

Create one reference per topic that can apply on its own. Keep topics together
when they always fire together, or when separating them would send the reader
through a chain of references to assemble one answer. Name each file for its
narrow scope, sharing a prefix where that shows the grouping: `python_uv.md`,
`python_pip.md`.

Done when every line of a proposed reference applies whenever that reference's
marker fires.

### 3. Build the marker dispatch

Put discovery before reference loading, then map each marker straight to its
narrowest reference:

```markdown
Read only the files for the markers present:

| Marker                        | Reference                                                    |
| ----------------------------- | ------------------------------------------------------------ |
| `tool.lock`, `[tool.example]` | [tool_example.md](references/tool_example.md) - Example Tool |
```

Make each marker precise. When one filename can belong to more than one tool,
name the config key that distinguishes them and load only the matching row. When
a topic has no filesystem marker, its marker is an explicit user choice or a
condition the core procedure discovers.

Every link into the references is one dispatch row - a surviving catch-all
link ("see the references for details") pulls in the whole group and undoes the
split.

Done when every conditional topic maps to a reference and every reference has
one loading condition.

### 4. Split without losing guidance

Move each topic into its focused reference, carrying its facts, examples,
caveats, attribution, and source links intact. Co-locate a small prerequisite
with the guidance that needs it, so reading one part brings its neighbours along
instead of triggering a second load.

Update every link that named the old file, including links between references.
Delete the old file once its content and its inbound links are all accounted
for.

Done when the new files preserve the old guidance between them and no link names
a removed file.

### 5. Update versions and catalogs

Bump the target skill's version. Where the repository keeps synchronized version
declarations for the enclosing plugin or its marketplace entry, bump each one,
and update the catalogs when the skill list or the plugin description changed.

Done when every declaration naming this skill's version or contents agrees.

### 6. Verify the disclosure

Check every Markdown link and search the repository for the removed filenames.
Run the repository's existing skill or plugin validator.

Walk these loading cases:

1. One marker loads one focused reference.
2. Several markers load the union of their references and nothing more.
3. An ambiguous filename loads nothing until its contents identify the topic.
4. Zero markers leave the core workflow usable on its own.

Report the old and new reference layout, the marker-to-reference mapping, the
versions changed, and the validation result.
