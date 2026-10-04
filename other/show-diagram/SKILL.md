---
name: show-diagram
description: Makes a diagram of whatever is under discussion and opens it in nvim in a new tmux pane beside this one. Use for "diagram this", "show me a graph", "open it here".
allowed-tools: Bash(~/.claude/skills/show-diagram/scripts/open_in_pane.sh *), Bash(~/.claude/skills/charting-code-chains/scripts/render_mermaid.sh *)
---

# Show Diagram

Draw the thing the conversation is about, check the result, open it beside this pane.

## 1. Pick the source from context

| Content | Source | Produces |
|---|---|---|
| Graph, dataflow, callstack, branch ladder | mermaid `.mmd`, rendered by `~/.claude/skills/charting-code-chains/scripts/render_mermaid.sh -i X.mmd -o X.png` | `.png` |
| Numbers, curves, distributions, trajectories | matplotlib script run with whatever the project uses (Bazel in the monorepo, `uv run` elsewhere) | `.png` |
| Existing image (a plot, screenshot, render) | nothing, open it as is | the file |
| Small structure where the text *is* the picture | ASCII in a `.md` code block | `.md` |

For mermaid, follow `charting-code-chains` for shape, labels and palette. For plots,
follow `dataviz`. `dot`, `d2` and `plantuml` aren't installed, so don't reach for them.

Build it from facts in this conversation or read from source. Mark untraced links
(dashed edge, `?`) instead of guessing at them.

## 2. Look before opening

Read the PNG back. Fix overlaps, clipped labels and mid-phrase wraps, then render again.

## 3. Open it

Write to the session scratchpad and keep the source next to the output. Then:

```bash
~/.claude/skills/show-diagram/scripts/open_in_pane.sh /abs/path/X.png      # beside
~/.claude/skills/show-diagram/scripts/open_in_pane.sh /abs/path/X.png -v   # below
```

Use `-v` when the image is much wider than tall. nvim shows the PNG through image.nvim:
`+`/`-` zoom, `hjkl` pan, `0` fit. `tmux resize-pane -Z` gives it the full screen.

## 4. Report

Give the absolute path and one line on what the diagram makes obvious that the code or
text doesn't. Offer to move the files into the repo; don't do it unasked.
