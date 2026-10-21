---
name: snowshoe-scratch
description: >-
  Study a path that is not this repo's Snowshoe map. Keeps an ephemeral mental
  map at ~/.snowshoe/learn/<sha256(utf8(realpath))> (not the git ledger). Optional
  read-only map status --cwd of a main checkout. Requires snowshoe on PATH for
  atlas queries only. Do not drain, init, or write ledger.sqlite. re-entry
  reprints the landed floor after a wiped-context break.
---

# Snowshoe-scratch

Satellite of the product skill. **Not** the git-map wedge. Product drain/learn
stays `skills/snowshoe/`. Do not add this as a third gate there.

Assume **`snowshoe` is on PATH** when you query a map. Always pass `--json`.
Global **`--cwd <dir>`** is git `-C` (discovery start). Not `--repo`.

On an offered main-map root, the atlas **allowlist** is only:

- `snowshoe map status --json --cwd <main> …`
- optional `snowshoe help --json` (command index; `--cwd` not required)

Do **not** run any other `snowshoe` command against that root. Do **not** write
`ledger.sqlite`. Viewport files on disk win over map prose.

Until install ships, using this skill **outside the Snowshoe clone** means
copying `skills/snowshoe-scratch/` into the harness skills dir (not
`snowshoe skill install`).

## Hash recipe (reconstruct the dir from a path)

Another chat must be able to open the same directory from the same target.

1. `target` = the explicit path they named, else cwd.
2. `realpath` = canonical absolute path (`realpath` / `os.path.realpath` /
   `fs.realpathSync`). Follows symlinks.
3. If `realpath` is not exactly `/`, strip **one** trailing `/` (keep `/` for
   root). Do not strip any other characters.
4. `id` = SHA-256 of the **UTF-8 bytes** of that string, lowercase hex
   (64 characters).
5. Directory: `$HOME/.snowshoe/learn/<id>/`.

```bash
python3 -c 'import hashlib, os, sys
p = os.path.realpath(sys.argv[1])
p = "/" if p == "/" else p.rstrip("/")
print(hashlib.sha256(p.encode("utf-8")).hexdigest())' "$TARGET"
```

`$HOME/.snowshoe/learn/<id>/` is personal/local. It is not `.snowshoe/` in the
target and not the ledger.

## origin.md

On bootstrap, write `origin.md` in the hashed dir:

```markdown
# origin

- realpath: `/abs/path/to/target`
- id: `<64 hex>`
- mainRoot: `/abs/path/to/main/checkout`
```

`realpath` and `id` are required. Omit the `mainRoot` line until a read-only
map was **offered and accepted**.

## Layout

| File | Role |
|---|---|
| `origin.md` | realpath, id, optional mainRoot |
| `CURRENT.md` | Ephemeral mental map of the target (concepts, not files/TOC) |
| `STATE.md` | Now / Re-entry / voice / journal |
| `PLAN.md` | Plan; read on phase shifts |
| `discrepancies.md` | Standing “should change” / bugs (not STATE) |
| `sessions.md` | Host chat ids for this dir (append-only; not teaching context) |

No ledger. No `mines.md` requirement. Scratch `STATE.md` is a journal plus a
**Re-entry** block (not product-learn retention cards or check-ins).

## Host chats (`sessions.md`)

The same hashed dir is reused across chats. Keep host conversation/session ids
out of STATE / CURRENT / origin.

`sessions.md` is an append-only list. When this turn has a host conversation
or session id (the opaque string the host already uses to name this chat;
look in the environment): if that id is not already in the file, append one
UTC line. Do not invent URLs. No id → skip; do not call host APIs.

```markdown
- 2026-10-19: `<id>`
```

Do **not** read `sessions.md` in the teaching loop (CURRENT / STATE / PLAN).
Read it only to check/append, or when they ask to find a prior chat.

## Loop

1. Resolve `target` → `realpath` → `id` → `$HOME/.snowshoe/learn/<id>/`.
2. **If the hashed dir is missing, or it exists but `CURRENT.md` is missing
   (partial bootstrap):** briefly propose creating the scaffold (and offer to
   write it if they agree). On OK: create the layout files (including
   `sessions.md`); write a **mental map** of the target (section below) into
   `CURRENT.md` **and** into the chat (same text). Append this chat’s host id
   if present. Do **not** block a one-shot question on scaffold. Do not resume
   a partial dir.
3. **If the hashed dir exists and `CURRENT.md` is present:** if a host chat id
   is visible and not already listed, append it to `sessions.md`. Read
   `CURRENT.md`, then `STATE.md`. If this turn is **re-entry** (section below),
   do that beat before any new slice. Voice after compaction: tutor prose in full sentences
   (not a status telegram). Match `STATE.md` → Now → `voice` when present;
   persist journal and Re-entry lines to `STATE.md` immediately so compaction
   cannot wipe them. Local STATE may use any language the human prefers; this
   skill stays English. Do not import product `learn.md` retention cards /
   check-ins.
4. Stay on the atlas allowlist above. Do not write `ledger.sqlite`. Scratch is
   not the git-map wedge.
5. Drain-shaped prompt on the mapped checkout (drain / `work next` / catch up
   the queue): one line pointing at product skill `skills/snowshoe/`
   (`drain.md`). Stay on scratch for this path; do not hard-block, and do not
   run drain commands from this skill.

## Teaching

- If something in the viewport **looks wrong, incomplete, or an eye-catcher**:
  **raise it in the chat this turn**. Do not swallow it to stay on the lesson.
  Do not start a fix unless they ask. If they agree it should change, one line
  in `discrepancies.md`.
- When a beat is about a real fragment, cite **repo-relative `path:line`**
  (compiler style — opens the editor). Prose first. Keep `CURRENT.md`
  readable without jumping — paths belong in chat / discrepancies, not as the
  map’s spine.
- If they ask to review local / agent patches mid-learn: do that, then return
  to the slice. If the picture of the target changed, refresh `CURRENT.md`.
  Patch review is not re-entry.
- End a teaching beat with a **next proposal** (or a pause). Short steering
  (“what’s next”, “go”, “use prose”) means take that default or fix voice —
  not re-entry.
- Landing a floor is progress, not re-entry. Quietly rewrite `STATE.md` →
  **Re-entry** (Landed / Current / Next / Do not reopen) and keep teaching —
  next-proposal as usual. Do not reprint the floor in chat.
- Stopping (they say they are leaving, ending the day, parking the session):
  same quiet rewrite. Then stop. Do not open a new slice. Still not the chat
  ritual unless they also typed `re-entry`.

## Re-entry

Assume wipe. Do not continue the last telegram.

**Trigger (one branch):** they type `re-entry` (optional leading `/`). Do not
treat short steering (“what’s next” / “go” / “ok”), a confirmation that the
floor landed, or a landed floor itself as this.

**Short auto:** first teaching turn after compaction, hashed dir already has a
journal, and this turn is not a content question about a named fragment. Then
print Landed / Current / Do not reopen in a few sentences and wait. A named
fragment question: answer it; do not dump the floor.

**Explicit `re-entry`:**

1. Read `CURRENT.md` and `STATE.md` → **Re-entry**. If that block is missing,
   reconstruct from Now + last journal lines + CURRENT first-level nodes, write
   it, then speak.
2. Chat in tutor prose (no file tree, no CURRENT dump):
   - what already landed (the floor), in words
   - the open slice
   - what not to reopen
   - **one** check question on the **current** slice only
3. Do not start the next slice until they confirm the floor is back or name
   the fog. Missed check → reprint that floor; do not go deeper.

`STATE.md` → Re-entry shape:

```markdown
## Re-entry

- Landed:
- Current:
- Next:
- Do not reopen:
```

Skill labels stay English. Local STATE / CURRENT may use any language the human prefers.

## CURRENT.md (mental map)

Same job as the product map tree. `drain.md`: the map is a **mental model, not
1:1 with code**. Scratch is markdown-only (no ledger, no slugs).

- Nodes are concepts (responsibility, flow, decision, seam) — not files, not
  the author's `##` headings.
- Shallow: about two listing levels; a handful of first-level nodes. If the
  honest list is huge, add a grouping layer (`drain.md` expand hop).
- **Readable without jumping.** A title is a named thing or a claim in words.
  A person scanning `CURRENT.md` must understand each node without opening the
  target. Coded labels (`A–F`, `P1`, `§6`) may follow in parentheses only after
  the words already stand alone. No telegram. Same posture as product entity
  bodies (`drain.md` Body shape).
- File TARGET: do not copy the table of contents. Directory TARGET: do not
  `ls`. Related files are edges, not extra chapters.
- Design-record scaffolding (tests, acceptance, canon touchpoints) is one
  grouped node, or omit until they ask to implement.
- Titles/tree match the human's session language. This skill file stays English.

Anti-patterns: filesystem dump; heading TOC; titles that only make sense after
opening the file (`Options A–F`, `Header`, `§8–14`).

## Optional read-only atlas

`GIT_C` = `$TARGET` if it is a directory, else the `dirname` of its realpath
(file-shaped TARGET still offers the atlas for its containing checkout).

```bash
git -C "$GIT_C" rev-parse --path-format=absolute --git-common-dir
```

If `--path-format=absolute` is unavailable, `realpath` the printed common-dir
relative to `$GIT_C` so a relative `.git` does not bind the agent cwd’s ledger.

Resolve that to the **main checkout** (parent of the `.git` directory when the
common dir ends in `.git`). If `<main>/.snowshoe/ledger.sqlite` exists, **ask
once** whether to use it as a read-only atlas. On yes: set `mainRoot` in
`origin.md`. If they decline, continue with viewport files only.

### Slug from a filesystem path

Do **not** dump `--all-fields` from `root`. Map TARGET (or the file under study)
to `--slug`:

1. `TOPLEVEL` = `git -C "$GIT_C" rev-parse --show-toplevel`. `rel` = path of
   TARGET relative to that checkout toplevel (posix, no leading `./`) — not
   relative to `<main>` on disk. Still query `--cwd <main>` (ledger lives there).
2. If TARGET is a directory and `rel` is empty or `.` (this checkout’s root):
   skip slug lookup. Do not pick a nested file as focus. If they already opted
   in, you may query `--slug root` (default fields / neighborhood only). Do not
   `--all-fields` from `root`.
3. Otherwise: `snowshoe map status --json --cwd <main> --fields slug,anchors`
   (tree, not `--all-fields`; `anchors[].path` is repo-relative).
4. Match a node whose `anchors[].path` equals `rel`, or (directory TARGET)
   whose anchor path is under `rel/`. Prefer the most specific match.
5. If none match: **skip the atlas for that file**; keep the viewport.

Then query only (allowlist):

```bash
snowshoe map status --json --cwd <main> --neighborhood --slug <focus>
snowshoe map status --json --cwd <main> --fields title,type,leaf,children,refs,bodyOverview --slug <focus>
```

Neighborhood / `bodyOverview` for the files under study — not full
`--all-fields` from `root`. Prefer viewport files you actually read over map
prose when they disagree; say so.

Optional: `snowshoe help --json` (no `--cwd`).
