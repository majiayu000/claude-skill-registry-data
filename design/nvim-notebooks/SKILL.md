---
name: nvim-notebooks
description: Cheatsheet for editing and running Jupyter .ipynb notebooks in nvim (jupytext + molten + NotebookNavigator, cell boxes). Use for "open a notebook in nvim", :Ker, kernels, cell keys, or notebook servers.
---

# Notebooks in nvim cheatsheet

Config: `~/dotfiles/nvim/lua/custom/plugins/notebook.lua` (plugins, keys, `:Ker`) and
`lua/custom/notebook_cells.lua` (boxes, folds). The design notes for editing either are in the
commit message of the commit that added `:Ker` (`git -C ~/dotfiles/nvim log --grep=':Ker'`).
`<leader>` is Space. Plain `nvim` has all of it.

## Opening

`nvim path/to/nb.ipynb`, or `:e` / `<leader>sf` from inside. jupytext.nvim shows it as a `# %%`
Python script (pyright, `gD` and treesitter work) and `:w` writes the cells back with
`jupytext --update`, keeping outputs already stored in the file. Outputs run in nvim are not saved.

While open, jupytext keeps a companion `<nb>.py` beside the notebook and deletes it on a clean
quit. If nvim is killed it stays, and the **next open reuses it** -- stale cells, which a `:w`
then writes over the notebook. Delete a leftover `<nb>.py` before reopening.

## Kernel

| Command | Does |
|---|---|
| `:Ker` / `<leader>ei` | new kernel on the default server (`$NOTEBOOK_SERVER_URL` at launch, else `http://127.0.0.1:8899`) |
| `:Ker 8900` | new kernel on `http://127.0.0.1:8900` |
| `:Ker http://host:8900?token=abc` | any URL; the token is sent as an auth header |
| `:Ker` in a second notebook buffer | each buffer needs its own; `:MoltenInit shared` reuses one already running |
| `:MoltenInfo` | attached kernels; a server kernel is named by its URL |
| `:lua print(require('molten.status').kernels())` | the attached kernel's URL, or empty |
| `<leader>ex` / `<leader>er` | interrupt / restart (clears outputs) |
| `:MoltenDeinit` | shut the kernel down -- do this before quitting, or it stays on the server |

From outside: `curl -s localhost:8899/api/kernels`; `"connections": 0` is an orphan.

### Starting a server

Monorepo kernels come from a Bazel `notebook_server_local` target, which has only that target's
deps. molten creates kernels with a POST that carries no `_xsrf`, so a tokenless server (what
`--local` gives) must run with XSRF off, through a private config dir:

```
JUPYTER_CONFIG_DIR=~/.local/share/nvim/jupyter-config \
  bazel run --config cloudbench -c opt //learning/behavior/tools/notebooks:joint_ilp_mh_notebook -- \
  --ip=127.0.0.1 --port=8899 --notebook_dir=$PWD/learning/behavior/tools/notebooks
```

A browser server started the usual way rejects molten with `'_xsrf' argument missing`. A
password-protected server can't be used at all.

## Cells

| Key | Does |
|---|---|
| `<C-n>` / `<C-p>` | next / previous cell; counts; centered. Also motions: `d<C-n>` on a `# %%` line deletes the cell, `v<C-n>` extends |
| `]h` / `[h` | next / previous cell (any Python buffer) |
| `<leader>x` / `<leader>X` | run cell and move / run cell |
| `<leader>eb` / `<leader>ea` | run this cell and below / run all |
| `vih` `yah` `dah` | cell text object (`ih` body, `ah` with marker) |
| `zM` / `z1` / `zR` | outline (headings + one closed box per code cell) / cells open, functions folded / all open |
| `za` on a box's top edge | toggle that cell |

New cell: type a `# %%` line. Markdown cell: `# %% [markdown]`, then `# ## Heading`, `# prose`.
The cursor row always shows raw text, so a box's top edge turns back into `# %%` under it.

## Output

| Key | Does |
|---|---|
| `<leader>eo` | enter the output float (scroll, yank); `:q` leaves |
| `<leader>eh` / `<leader>ed` | hide / delete the cell's output |

Plots show in the float through image.nvim. Zoom: `plt.savefig('/tmp/p.png')`, then `:e /tmp/p.png`
and `+`/`-`/`hjkl`/`0`. GIFs show only their first frame (image.nvim converts `gif[0]`); no
animation. No ipywidgets, no interactive plotly.

## When it goes wrong

| Symptom | Cause / fix |
|---|---|
| raw JSON instead of cells | opened with a config without the notebook setup |
| stale cells after reopening | leftover `<nb>.py` companion; delete it and reopen |
| images missing at random | needs `allow-passthrough all` on the pane (set at startup inside tmux); popups never show images |
| `'_xsrf' argument missing` | server not started with the XSRF-off config dir above |
| "Config Change Detected… Press ENTER" | lazy noticed a config edit; it blocks `nvim --server … --remote-expr` until dismissed |
| `:checkhealth jupytext` errors | jupytext.nvim calls `vim.health.report_error`, removed in nvim 0.12; the plugin works |
