---
name: plot
description: Reactant tag-only data visualization. Use only when execute or execute-one dispatches an exact <@plot> tag from a document; never activate from ordinary chat or another skill.
---

# Plot

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@plot...>` annotation in a target document and hands off its
context. Never activate it from an ordinary chat chart request, semantic
similarity, or any skill other than those two routers. Without that handoff,
do not read data, run code, or create artifacts.

Produce a data visualization grounded in a real data file by generating and
executing a Python script, then replace the tag with a figure reference.

## Tag

```
<@plot: chart description, use ``data/results.csv``, save to ``figures/out.png``>
```

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it.
- **Prompt** — the desired visualization: chart type, styling, formatting.
  Its double-backtick context references name the data file and, optionally,
  the output path.

## Workflow

1. Identify the data file from the prompt's context references and read it
   first to learn its actual structure (columns, types, row count). Never
   assume column names. If the prompt has no data reference, fail cleanly and
   ask the user to add one.
2. Determine the output path: the output context reference if given,
   otherwise a `figures/` directory next to the document (create it if
   needed) with a sanitized name derived from the prompt (lowercase,
   underscores; for example `figures/completion_time.png`).
3. Write a complete, self-contained Python script that reads the data file,
   produces the requested visualization (matplotlib and/or seaborn; pandas
   for tabular loading), applies the prompt's styling, and saves the figure
   with `dpi=300` and `bbox_inches='tight'`. Default to clean,
   publication-ready styling: white background, legible fonts, labeled axes.
   If the prompt gives no chart type, infer the most appropriate one from the
   data structure and surrounding context.
4. Save the script next to the artifact with the same basename and a `.py`
   extension (for example `figures/completion_time.py`), then run it once
   with the host's Python. Keep the script file so the plot can be
   regenerated and audited.
5. Confirm the image file now exists, then replace the `<@plot: ...>` tag
   with a format-appropriate reference using a path relative to the document:
   - Markdown: `![description](figures/out.png)`
   - LaTeX: `\includegraphics{figures/out.png}`

## Rules

- Consume only this tag; do not rewrite surrounding prose. Preserve every
  unrelated tag, `<@comment: ...>` tag, `<@chat-model>` block, and escaped
  literal byte-for-byte.
- Resolve reference paths relative to the document's directory unless
  absolute.
- If the data file cannot be found or read, if plotting libraries are
  unavailable, or if the script errors, fail cleanly: leave the tag, report
  the error, and include the generated script so the user can debug.
- The rendered chart is accepted as produced; Reactant runs no quality check
  or second model pass on it.
