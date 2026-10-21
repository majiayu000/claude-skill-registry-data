---
name: typeset-math
description: Typesets math as LaTeX in a tmux split beside the chat. Use when a reply needs equations or derivations, or "show me the math".
allowed-tools: Bash(mdmath *), Bash(tview *)
---

# Typeset Math

The chat renders LaTeX as raw source and eats its backslashes (`\;` shows as `;`). When a
reply needs real equations, typeset them in a pane beside the chat instead.

Skip this for a stray symbol or two: inline Unicode in chat is fine for that.

## 1. Write the answer as markdown

Write the full answer to `<scratchpad>/math/<slug>.md`:

- Put all math in display blocks (`$$ … $$` or `\[ … \]`): mdmath turns inline `$…$` and
  markdown tables into Unicode, and only display blocks are typeset.
- Write tables as display `array`s.
- Make any sentence that relies on a symbol its own small display equation.
- amsmath and amssymb are loaded, plus `\bm`. `align*`, `gather*`, `cases`, `pmatrix` and
  `\operatorname` all work. Write the LaTeX itself in ASCII, with no Unicode symbols inside
  it.
- Prose, headings, lists and code blocks render through glow.
- For an explanation (not just a formula), follow the notating-math-naturally skill.

## 2. Check it compiles

```bash
mdmath --check <file>
```

Each failing block is reported as `<file>:<line>: block N failed` plus the TeX error, and
the exit code is 1. Fix the blocks and re-run until it prints `N/N blocks compiled`.
Rendering is local (tectonic) and cached, so re-runs are fast.

## 3. Open it beside the chat

```bash
tview split --name math --rerender -- mdmath <file>
```

This reuses the `math` pane if one is already open, and keeps focus on the chat. The pane
pages the result in `less`, where `q` closes it. Equations are kitty images drawn with Unicode
placeholders, so they scroll and search with the text. mdmath lays out to the pane width at
render time; `--rerender` re-runs it when the pane is resized, reopening at the top.

## 4. Reply in chat

Keep the chat reply to prose. Give the key result in plain Unicode (e.g. `ā = Δv/Δt`) and
say the full derivation is in the math pane. Don't paste the LaTeX into chat.

## Variants

- **"Pop it up":** use `tview popup -- mdmath --unicode <file>`. It's text-only math: a tmux
  popup doesn't pass image escapes through or report pixel sizes, so real typesetting only
  works in the split.
- **Existing markdown** (e.g. explain-math's output): open it with step 3 directly.
- **Images missing after a terminal restart or reattach:** Ghostty drops them. Re-run step 3
  to send them again.
- **Equations cropped on the right/bottom, or shrunk and left-aligned:** Ghostty 1.3.1 draws
  an image with the first placement ever sent for its id. mdmath deletes an id's placements
  before re-sending it; if this shows up anyway, check that the delete in `_transmit` is still
  there. Ghostty versions after 1.3.1 replace placements themselves.
- **Not inside tmux:** `tview` exits 1. Answer in chat instead.
