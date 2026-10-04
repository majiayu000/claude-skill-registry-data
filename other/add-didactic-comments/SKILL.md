---
name: add-didactic-comments
description: Comment tagged files so the user learns the APIs they are studying, with a doc link in every comment.
disable-model-invocation: true
argument-hint: "topics: the APIs the user wants to learn, ex: pandas, Pathlib"
arguments: [topics]
---

## Unstaged work

Files with unstaged changes, tracked and untracked:

!`git status --porcelain --untracked-files=all | grep -E '^.[^ ]' || true`

- If that list is empty, go ahead with the skill.
- If it is not empty, stop.

Reply with exactly this line and nothing else, no file list, no explanation, no preamble:

```
Stopping - unstaged files detected. Stage them and then invoke this skill again.
```

# Add didactic comments

The user tagged files and folders and named the `topics` they want to learn. Teach those topics inside those files. Change nothing but comments.

- Comment every call that belongs to `topics`. Skip the rest of the code: plain python, obvious assignments, imports.
- One comment per call, on the line above it.
- Say what the call does **here**, on **this** data. Not what the API does in general.
- End the comment with the doc URL of the exact symbol you commented, deep link included: `pandas.DataFrame.groupby`, not `pandas`.
- IF `topics` is empty, THEN infer them from the imports of the tagged files, and say which ones you picked.
- IF a folder is tagged, THEN comment every source file under it.

## Links

- Get the URL from the docs, never from memory. Fetch the page, confirm the anchor names the symbol, then paste the URL.
- IF the anchor does not exist, THEN link the closest page that does and drop the anchor. Never invent a fragment.
- Same symbol used twice in a file: link it once, at the first use.

## Format

```python
# {what this call does to this data}, {the argument that matters and why}
# https://{deep link to the symbol}
frame_by_year = sales.groupby("year")
```

## Rules

- Never edit code, names, or order. Comments only.
- Never delete a comment. Rewrite one only if it starts with `AI` and it is wrong.
- No temporal anchors, no change narration.
- No comment restates the line. `# read the file` above `path.read_text()` is noise; explain the encoding, the failure mode, the return type.
