---
name: pointing-to-code
description: Pushes code pointers into a live nvim session as a quickfix list, jumps there, and optionally saves the list to disk so it outlives the session. Use when answering where code lives.
allowed-tools: Bash(id -u), Bash(ls /run/user/*), Bash(nvim --server *), Bash(~/.claude/skills/pointing-to-code/scripts/push_qf.sh *), Bash(~/.claude/skills/pointing-to-code/scripts/save_qf.sh *), AskUserQuestion
---

# Pointing to Code

Deliver `file:line` answers into the editor: set a quickfix list in the user's running nvim,
jump to the first hit, and let them walk the rest with `:cnext`.

Always give the answer in chat too. The quickfix list is a convenience, not the answer — it
does nothing when no nvim is running, and chat `file:line` text is already clickable.

## Step 1: Get a socket

**If the user gives you a socket path, use it and push.** Naming a session is both the address
and the consent. Don't `id -u` — the uid is in the path. Don't glob the other sockets; their
state says nothing about this one and you were never going to push there. Don't test the path
first: `push_qf.sh` fails loudly on a dead socket, so the push is its own verification and
building the payload costs nothing worth pre-empting. Skip to Step 3.

Only when no socket was given, discover them:

```bash
id -u
```

```bash
ls /run/user/<uid>/nvim.*.0 2>/dev/null
```

Nvim opens this socket automatically for every terminal session; no `--listen` flag needed.
The file can outlive a crashed nvim, and sessions die between one message and the next — a
path that worked earlier in the conversation may not work now.

**Zero sockets** → skip the quickfix entirely. Answer in chat, and don't mention nvim.

## Step 2: Pick one (only when you discovered several)

Prefer the session that already has one of the target files open:

```bash
nvim --server <socket> --remote-expr 'join(map(filter(getbufinfo({"buflisted":1}), "v:val.name !=# \"\""), "v:val.name"), "\n")'
```

If exactly one session qualifies, use it. Otherwise show the buffer lists and ask which
session — never guess, since jumping the wrong window is disorienting.

## Step 3: Push and jump

**Never compute a line number — read it back.** Anchor each pointer on a distinctive
fragment of the line itself and let `grep -n` report where it sits. One call, alternation
of one anchor per pointer, each unique in the file, so the anchor→line mapping is
unambiguous:

```bash
grep -n "if not render_missing:\|reused = existing.get\|for chunk in _chunked" video_clips.py
```

The failure this prevents: you already have the file's contents from a windowed read that
carried no numbers — `sed -n '150,404p'`, a paged Read, a heredoc — and you add offsets to
the range start by hand. Error accumulates over a couple hundred lines, and every pointer
downstream of it is wrong by a different amount, so the list looks plausible and lands 5-10
lines off. `grep -n`, `rg -n`, and Read's `cat -n` prefixes are all trustworthy; arithmetic
on a window is not, and neither is memory of a number you saw earlier in the conversation.

Cheap to verify, so verify: re-grep every anchor before pushing rather than pushing and
correcting. Corrections cost the user a jump to the wrong place and their trust in the rest
of the list.

Order entries most-relevant first. `text` is the one-line reason the location matters.

```bash
cat <<'JSON' | ~/.claude/skills/pointing-to-code/scripts/push_qf.sh --socket <socket> --title 'claude: where retries are handled'
[{"filename": "/abs/path/client.cc", "lnum": 88, "col": 3, "text": "backoff loop"},
 {"filename": "/abs/path/client.h", "lnum": 24, "col": 1, "text": "max_retries default"}]
JSON
```

`filename` must be absolute. Use `--no-jump` to set the list without moving the cursor, and
`--copen` to also open the quickfix window.

Then say what you set: "2 pointers in quickfix, jumped to `client.cc:88` — `:cnext` for the other."

## Step 4: Offer to save them

A quickfix list dies with the session. Once the list is pushed and verified, ask — via
AskUserQuestion, one question, save / don't save — whether to persist it. Worth offering when
the pointers map a subsystem, encode a walkthrough, or took real digging; skip the ask for one
or two pointers the user is reading right now.

Read the list back out of nvim rather than re-sending your own array. That saves what is
actually in the editor, with `bufnr` resolved to absolute paths, so a list the user has since
edited stays honest:

```bash
~/.claude/skills/pointing-to-code/scripts/save_qf.sh \
    --socket <socket> --name walkthru \
    --description 'one line on what this list maps'
```

Writes a pair under `<git toplevel>/code-pointers/` (created if absent, and added to
`.git/info/exclude` so it never shows in `git status` and adds no tracked file):

```
walkthru.quickfix       path:lnum:col: text  — what :cfile parses
walkthru.quickfix.json  title, saved date, commit, tree_state, setqflist-ready items
```

The script reloads what it wrote in a throwaway `nvim --headless -u NONE` and fails if any
entry comes back invalid, so a saved file is a file known to load. Reload either way:

```vim
:cfile code-pointers/walkthru.quickfix
:call setqflist([], ' ', json_decode(join(readfile('code-pointers/walkthru.quickfix.json'))))
```

Prefer the JSON route when telling the user — it restores the title too, and `setqflist`
ignores the metadata keys sitting beside `items`.

On this machine there is a command for it, so point at that instead of the raw `:call`:

```vim
:Cload            " Telescope picker over every saved list found upward from the buffer
:Cload walkthru   " straight to one by name, with completion
```

`~/dotfiles/nvim/lua/custom/code_pointers.lua`, wired at the bottom of `lua/keymaps.lua`. It
walks up from the current *file's* directory collecting `code-pointers/` dirs, nearest first,
up to and including `$HOME` — deliberately past the first `.git`, since a submodule's own
`.git` would otherwise hide the superproject's saved lists. `vim.g.code_pointers_ceiling =
'git'` stops at the first `.git` instead. It warns when the sidecar's `commit` no longer
matches HEAD, which is the one silent way a saved list goes wrong.

**Keep the `.quickfix` file free of frontmatter.** `:cfile` parses with `errorformat`, and a
line matching no pattern is kept as a `valid=0` entry, so a YAML header becomes clutter in
`:copen`. That is why provenance lives in the sidecar instead.

Since the sidecar pins `commit` and `tree_state`, call it out when saving against a dirty tree —
the line numbers are only as good as the working copy they were read from.

## Notes

- Let the script build the list; don't hand-roll `setqflist`. Two traps it already handles:
  `setqflist(items, "r", {...})` fails with `E475` because a list and a `what` dict are
  mutually exclusive, and `--remote-send` needs a `<C-\><C-N>` prefix that yanks the user out
  of insert mode, while `execute("cfirst")` jumps without touching their mode.
- `--remote-expr` is a blocking rpcrequest — a session sitting on a hit-enter prompt hangs the
  call. The script caps each call at 10s.
- Pushing replaces the current quickfix list. Ask before overwriting only when you chose the
  session yourself and the user may be mid-review. A session the user named is one they have
  asked you to write to.
- Quickfix addresses physical lines, not records. A CSV whose quoted fields can hold
  newlines, or a log with wrapped entries, breaks the 1:1 — row N is not line N. Step 3's
  read-it-back rule handles this too; what differs here is the *unit*, not the arithmetic,
  and it is a property of the target rather than of the socket.

## When to skip

- A conceptual question rather than "where is X".
- The user is in another editor, or on a plain SSH session with no nvim.
- One pointer they just want to read — chat text is enough.
