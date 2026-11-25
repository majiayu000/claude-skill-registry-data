---
name: save-session
description: Save the active coding session (session ID, model, working directory) to a per-harness markdown record under ~/.agents/memories/sessions/, and later find a saved session by project title and tell the user exactly how to resume it. USE THIS SKILL whenever the user wants to save, bookmark, or remember a session or session id ("save this session", "remember this session", "store my session id", "note down where we were"), or asks to get back into earlier work ("resume the X session", "find the session for X", "continue where we left off on X", "which session were we doing X in", "what's my session id for X", "how do I get back into X"). Applies to Pi, Claude Code, Codex, Antigravity CLI (agy), and OpenCode. Trigger even when the user names neither a session ID nor a harness — figuring those out is this skill's job.
license: MIT
metadata:
  author: "Jemshit Iskanderov"
  version: "0.2.0"
---

# save-session

Two modes:

1. **save** — record the current session under a project title so future-you can find it.
2. **find & resume** — look up saved sessions by project title and hand the user the exact resume command.

## Where records live

Destination resolution, in order:

1. A destination the request explicitly names (useful for testing or project-local notes).
2. The `AGENTS_MEMORIES_DIR` environment variable, if set.
3. Default: `~/.agents/memories/sessions/` (create it if missing).

Sessions are owned by the harness that created them — a Pi session id means nothing to
Codex, and each harness stores and resumes sessions its own way. That is why records get
**one file per harness**, so a lookup never mixes id spaces:

```
~/.agents/memories/sessions/
├── pi.md
├── claude-code.md
├── codex.md
├── antigravity.md
└── opencode.md
```

## Record format

Keep entries to exactly these four fields — this is a lookup index, not a journal. Notes,
summaries, and reflections belong in the project itself.

```markdown
# Sessions — Pi

## DataStructures heap benchmark
- saved: 2026-10-16T23:40:00Z
- session_id: 11111111-2222-3333-4444-555555555555
- model: provider/model-name
- dir: <absolute path to the project>
```

- `saved` — current UTC timestamp, ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ`). Use the
  `saved` value returned by `detect_session.py`; never supply a date from model knowledge.
- `session_id` — exactly what the harness's resume command expects.
- `model` — the model the session runs on (e.g. `provider/model`). If genuinely
  undetectable, omit the line rather than inventing one.
- `dir` — absolute working directory; most harnesses can only resume from the right place.

The file's top heading names the harness (`# Sessions — Pi`, `# Sessions — Claude Code`,
`# Sessions — Codex`, `# Sessions — Antigravity`, `# Sessions — OpenCode`). Entries are
appended oldest-first; file order is the timeline.

## Entry identity and title handling

A record entry is identified by its **`session_id`**, not its title — the id is what a
resume command consumes; the title is only the human-facing label. `save_session.py` enforces
these rules without printing the ledger into the agent's context:

- **Already recorded → update, don't append.** Refresh that entry's `saved` timestamp and
  correct `model`/`dir` if they changed. Keep the entry in place (file order is the
  timeline; `saved` shows freshness). Say plainly in your reply that you updated the
  existing entry rather than created a new one. The one exception: a *different title* —
  next bullet.
- **Already recorded under a *different title* → ask first, never silently retitle.** Say:
  this session is already saved as "<existing title>" — and ask whether to **ignore**
  (keep the existing entry exactly as it is) or **replace** (retitle the entry to the new
  title and refresh its `model`, `dir`, and `saved` date). One entry per session id, always; the
  `- N` numbering is only for *different* session ids sharing a title.
- **Not recorded → append.** The project title comes from the user and is required — ask
  for it if the request doesn't include one; keep the user's wording. If that title already
  exists in the same file **on a different session**, number the new one instead of
  overwriting: `My Project`, `My Project - 2`, `My Project - 3`, … (highest existing
  suffix + 1). Several live sessions on one project is normal; each gets its own entry so a
  later lookup can show all of them.
- **Similar but non-identical title → ask first.** Case/whitespace-only differences and a
  single insertion, deletion, or substitution may be a typo. The script reports the nearby
  titles but never merges them. The user can choose an existing exact spelling or keep the
  requested spelling with `--accept-similar`.

## Harness reference

First establish which harness you are running in (your own environment tells you; if in
doubt, ask the user). Then use that harness's row only — foreign environment variables from
another tool's installer are not evidence. The table doubles as the no-shell fallback;
`scripts/detect_session.py` is the authority — when a harness changes its storage, update
both together (three of the five are pure file reads, so the table stays useful).

| Harness | Record file | Session ID | Model | Resume |
|---|---|---|---|---|
| Pi | `pi.md` | env `PI_SESSION_ID` | env `PI_PROVIDER` + `PI_MODEL` | `pi --session <id>` (TUI `/resume` opens the picker) |
| Claude Code | `claude-code.md` | env `CLAUDE_CODE_SESSION_ID`, checked against `<config>/projects/<project>/<uuid>.jsonl` when available | latest assistant `message.model` in that transcript | `claude --resume <id>` (TUI: `/resume <id>`) |
| Codex | `codex.md` | `$CODEX_HOME/sessions/**/rollout-*-<uuid>.jsonl` whose metadata records this working directory | latest `turn_context.payload.model` | `codex resume <id>` |
| Antigravity CLI | `antigravity.md` | `~/.gemini/antigravity-cli/cache/last_conversations.json` (older installs); newer installs use `projects.json` + a private SQLite store, not yet readable here | `model` in `~/.gemini/antigravity-cli/settings.json` (the default, not per-session) | `agy --conversation <id>` (TUI: `/resume`) |
| OpenCode | `opencode.md` | `opencode session list --format json` or DB `session_v2.id` | `session_v2.model` column | `opencode --session <id>` (TUI: `/sessions`) |

Per-harness detection details:

- **Pi** exposes everything: `PI_SESSION_ID`, `PI_MODEL`, `PI_PROVIDER`, `PI_SESSION_FILE`.
  Combine provider and model as `provider/model`. Exact-ID resume is `pi --session <id>`;
  `/resume` is a picker and does not take an id.
- **Claude Code** exposes `CLAUDE_CODE_SESSION_ID` to tool subprocesses. Validate it against
  the matching transcript when possible because after `--continue` or an argument-free
  `--resume` it can still name the startup session. Transcripts live under
  `${CLAUDE_CONFIG_DIR:-~/.claude}/projects/<project>/<session-uuid>.jsonl`; the project
  directory can be overridden with `CLAUDE_CODE_PROJECT_DIR_NAME`. Match every candidate's
  `cwd` field exactly because different paths can produce the same slug. The current model is
  the latest assistant `message.model`, and the transcript schema is internal. Claude's local
  transcript retention defaults to a finite window and persistence can be disabled, so this
  ledger bookmarks an id; it does not preserve the underlying conversation.
- **Codex** keeps one rollout file per session:
  `${CODEX_HOME:-~/.codex}/sessions/<YYYY>/<MM>/<DD>/rollout-<timestamp>-<session-uuid>.jsonl`.
  The first UUID in the filename is the resumable conversation id. Require an exact `cwd`
  match in the rollout metadata; if none matches, fail rather than returning another project's
  newest session. `session_meta` records the working directory and provider; the latest
  `turn_context` record carries the model.
- **Antigravity CLI (agy)** keeps a workspace-keyed cache:
  `~/.gemini/antigravity-cli/cache/last_conversations.json` maps absolute path → current
  conversation id. Conversation history is scoped to the working directory, which is why
  `dir` matters here more than anywhere else. Newer releases replaced that file with a
  `projects.json` workspace→project mapping and moved conversation data into a private
  SQLite store; this skill cannot read that format yet, so when only `projects.json` is
  present it reports the gap by name rather than guessing at an unpublished schema — pass
  `--id`, or read it from the `/resume` picker, until this is updated against a live install.
- **OpenCode** stores sessions in `opencode.db` (SQLite, table
  `session_v2` with `id`, `model` JSON, `directory`, `time_updated`, among many other columns)
  and exposes them via `opencode session list --format json`. Confirmed against OpenCode v2.
  The database's location is resolved in priority order: an explicit `OPENCODE_DB` wins
  outright; otherwise `opencode debug paths db` is the tool's own authoritative answer and
  wins outright too — a release channel (stable vs. a beta/nightly build) can relocate the
  data directory, and merging in a different database's rows could surface a stale session as
  current. `XDG_DATA_HOME`, or `~/.local/share/opencode/` by default on Linux, macOS, and
  Windows (`%USERPROFILE%\.local\share\opencode` there), is used only when neither can answer.
  Some OpenCode 1.x builds replaced this with a JSON-file store under
  `storage/{project,session,message}/` and dropped the `session list` command entirely; if
  detection unexpectedly reports no session despite one existing, check `opencode --version`
  and upgrade before assuming this skill is wrong.

## Detecting without a shell

Prefer environment values and direct file reads — they work in headless or permission-restricted
contexts. This matters more than it looks: some harnesses (Antigravity CLI in headless mode)
**auto-deny a shell command and abort the whole run**, so reaching for a shell unnecessarily can
kill the task before it starts.

Order of attack:

1. **Authoritative environment values first** — Pi exposes the current id directly. Claude's
   env id is useful but remains heuristic until its transcript validates it.
2. **File reads first after that** — the session stores listed above are ordinary
   JSON/JSONL/SQLite files. Read the JSON ones directly for Claude Code, Codex, and
   Antigravity. OpenCode's documented JSON CLI is preferred over its private SQLite schema.
3. **Shell only when it is the remaining path** (Pi env inspection or the OpenCode CLI/SQLite)
   — and only when you already know commands run in this context.
4. **If a command is denied, do not retry it.** Fall back to file reads, or tell the user
   what you could not detect and ask for the id. A permission denial is information, not
   an obstacle to route around.

`scripts/detect_session.py` (in this skill's directory) automates all of the above with
fallbacks, but it is a fast path, not the procedure:

```bash
python3 <skill-dir>/scripts/detect_session.py --harness <pi|claude-code|codex|antigravity|opencode>
# → {"ok": true, "heuristic": false, "saved": ..., "records_dir": ..., ...}
#                                                    (authoritative, currently Pi)
# → {"ok": true, "heuristic": true, ...}           (working-directory/store heuristic — disclose it)
# → {"ok": false, "reason": "..."} + exit code 1   (a missing id is never guessed)
python3 <skill-dir>/scripts/detect_session.py --check   # verify record files; exits non-zero on duplicate ids or unreadable files
```

(`python3` above; on Windows the interpreter is usually `python` or `py`. The scripts are
plain standard-library Python and run on Linux, macOS, and Windows.)

**Interpreter, everywhere in this file:** any `python3` below means `python` or `py -3` on
Windows.

If detection still fails, say so plainly and ask the user for the id (Pi: `/session`,
Claude Code: `CLAUDE_CODE_SESSION_ID` from a tool subprocess or the `/resume` picker,
Codex: `/status`, agy: the `/resume` picker, OpenCode: `/sessions`) — a
missing `model` is fine to omit, but never fabricate a session id.

## Mode 1 — save

1. Get the project title from the user (required), then run the bundled writer. Pass the harness
   you are running in, any id named by the request, and `--sessions-dir` when the request names a
   destination; environment auto-detection is only a fallback:

   ```bash
   python3 <skill-dir>/scripts/save_session.py --title "<project title>" --harness <harness> [--id <id>] [--sessions-dir <dir>]
   ```

   Do **not** read the record file or the script source during a normal save. The writer performs
   exact-id lookup, validation, numbering, locking, and atomic replacement internally and prints
   one compact JSON object. Exit `0` means completed, exit `1` means an error and no write, and
   exit `2` means `needs_confirmation` and no write.
2. Interpret the result:
   - `created` / `updated` → report the returned title, id, and file.
   - `confirm_detected_session` → show the detected id and source; after the user confirms,
     rerun with that exact `--id`. A working-directory/store result can be stale when several
     sessions share a directory.
   - `session_has_different_title` → ask **ignore** or **replace**. On **ignore**, do not call
     the script again: report that the returned `existing_title` remains unchanged and nothing
     was written. On **replace**, rerun with `--replace-title`.
   - `similar_title` → show the returned nearby titles. Rerun with the chosen exact spelling,
     or with the requested spelling plus `--accept-similar` if the user wants it kept separate.
   - `record_locked` → confirm no save operation is still running; only then remove the exact
     lock file reported by the script and retry. Never remove another harness's lock.
   - any other error → report it; do not edit the Markdown as a workaround.
3. Confirm in your reply: title, session id, file, and whether the script created, updated,
   replaced, or ignored the entry.

A user-provided id still wins verbatim. A local `validated: false` can mean the session came
from another machine; surface it, but do not substitute another id. Without a runnable Python
interpreter, follow the same rules manually as a last resort and validate with
`detect_session.py --check` when execution becomes available.

`--ignore-existing` remains available for a programmatic caller that explicitly wants a locked,
structured revalidation of the no-op. The normal agent flow does not use it.

## Mode 2 — find & resume

1. Extract what the user wants: a **lookup by name** ("resume the X session"), or a **listing**
   ("what sessions do I have saved", "show me my sessions"). **No name at all** ("resume my
   session", "get me back in") → list the current harness's entries with `--list` and ask
   which one — never silently pick.
2. Use the bundled script for either (it never modifies records):

   ```bash
   python3 <skill-dir>/scripts/find_session.py --list --json         # current harness (auto-detects; --harness/--all to override)
   python3 <skill-dir>/scripts/find_session.py --title "<project name>" [--pick latest] --json
   python3 <skill-dir>/scripts/find_session.py --session-id <id> --json
   # → {"matches": [{"file", "harness", "title", "session_id", "model", "dir", "saved", "resume"}]}
   # no matches: exit code 1 — say so plainly rather than guessing
   ```

   Without a shell, read the record files directly: match `##` headings
   case-insensitively (substring in either direction), or list every entry in the
   current harness's file, sorted by `saved`.

   `--list` needs to know which harness it is listing: it takes the environment hint
   (Pi's `PI_SESSION_ID`, Claude Code's session env, OpenCode's `OPENCODE`) or an explicit
   `--harness` / `--all`. When
   neither is available it stops and asks — **never guess which harness**, because session
   ids do not translate across harnesses and a wrong guess lists an unrelated history.
3. Show the matches: title, harness file, `saved`, `session_id`, `model`, `dir`. When
   several entries match — same title, different session ids; several live sessions on
   one project are normal (`Finance cashflow` and `Finance cashflow - 2` must both be
   listed, each with its own id) — list **every one** sorted by `saved`, recommend the
   most recently saved, and let the user pick a different one when they know better
   (a saved timestamp can be stale if the session kept running after its last save).
4. Pick one (the recommendation by default; the user chooses if ambiguous) and give the
   **exact resume command** for its harness with the id filled in.
5. Because resuming is usually directory-scoped, also tell the user the `dir` to `cd` into
   first.

Finding never modifies records. If the record files look emptier than expected (entries
or whole files missing — it happens), say so instead of silently proceeding: quiet loss is
the one failure the save flow cannot see by itself (`detect_session.py --check` lists what
exists).

## Rules

- **Resuming belongs to the user.** Mode 2's deliverable is the exact command line for
  the user to run in their harness — print it in a code block. Don't spawn interactive
  harness processes to "test" resumption; if a context genuinely supports scripted
  resumption, the user will ask for it.
- Never overwrite, edit, or delete a *different session's* entry. The only writes are:
  appending a new session's entry, and updating a session's *own* entry (same `session_id`).
- Ask only for what is missing — normally just the project title. Don't interrogate the
  user for values you can detect.
- Session records are not a place for secrets: no tokens, keys, or credentials, ever.

## Reference

- `references/decision-flow.md` — the same decision logic as Mermaid figures, one per mode,
  with every interaction point marked. It is derived from this file, so edit both together
  and run `python3 scripts/check_flow_doc.py`, which fails when a decision point is
  documented on only one side.
