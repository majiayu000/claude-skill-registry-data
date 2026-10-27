---
name: paper-review
description: Set up and run the botference document-review interface (Google-Docs-style comments on rendered LaTeX/Markdown, bots replying in threads, apply/commit of accepted changes) in any repo — and follow the round protocol when the user asks for a review round or tags you from the review page.
---

# paper-review — GDocs-style review of rendered sources, with bots

The engine is built and battle-tested. **Canonical engine:
`$BOTFERENCE_HOME/frontends/review/`** (ships with botference). Architecture, decision history, and the unbuilt roadmap (CI
rounds, cloud version): `design.md` next to this file. This file tells
you how to USE the system.

## Setting up a new project ("set up paper review in <dir>")

**Preferred: `botference review [dir]`** — one command does all of the
below (engine copy, detection via `scripts/review-detect.mjs` with an
echoed summary, gitignore, build, serve; `--share`, `--hosted`,
`--port N`, `--no-agents`, `--upgrade`). Use the manual steps only when
the launcher isn't available:

1. Copy the engine from the reference implementation into
   `<dir>/review/`: `build.mjs`, `server.mjs`, `chat.mjs`, `apply.mjs`,
   `submit.mjs`, `init-config.mjs`, `bridge-system-prompt.md`,
   `SCHEMA.md`, `assets/` (review.js, style.css). Never copy
   `review.config.json`, `state/`, `suggestions.json`, or `site/` —
   those are per-project.
2. Run `node review/init-config.mjs` from `<dir>` (it inspects the
   directory: master file via `\documentclass`, sections via
   `\input`/`\include` order, bib, abbreviations, todo macros, figures
   dir, a free port, and the bridge block). **Show the user what was
   detected and get their confirmation before proceeding** — never
   guess the master file silently.
3. Add the gitignore block (see reference repo): `review/site/` and
   `review/state/*` ignored EXCEPT `state/users/` and
   `state/threads.json`; `suggestions.json` tracked. Conversation must
   travel through the repo; runtime files must not.
4. `node review/build.mjs`, then commit `review/` ("Add review
   interface"). Requires `pandoc` on PATH — check and tell the user if
   missing.

## Running it

> Sync note: the workspace copies of this skill at
> `<vault>/botference/.claude/skills/paper-review/SKILL.md` and
> `<vault>/botference/.agents/skills/paper-review/SKILL.md` are plain
> copies of this file — when you edit it (either copy in botference-main
> or those), update all four.

- `botference review` — build + serve; **agents are on by default when
  the machine can run them** (python3 + a `claude`/`codex` CLI on
  PATH — the launcher prints `agents: on (…)` or an `agents: off`
  explanation). `--no-agents` forces off; `--agents` forces on (clear
  error if impossible).
- `botference review --share` — hosted mode behind a cloudflared quick
  tunnel: respects `REVIEW_PASSWORD` or generates one, prints
  `share this: <url>   password: <pw>`; Ctrl-C stops server + tunnel
  together. Missing cloudflared → install hint, keeps serving locally.
- Manual (no launcher): `node review/server.mjs` — static + comment
  mirror, no bots; `--chat` adds the bot bridge (needs
  `BOTFERENCE_HOME` or the config's `bridge.core_dir`); `--hosted` adds
  the `REVIEW_PASSWORD` gate, rate limits, and owner-gated summons. The
  gate asks for **a name and the password together** (a name is not a
  credential — it only picks which `users/<handle>.json` the guest
  writes; asking on the gate is what makes hosted mode work on a phone,
  where the sidebar picker is inside a drawer). The server serves ONLY
  `review/site/` + the figures dir (path-traversal guarded) — keep it
  that way.
- Collaborator options: the owner's `--share` URL (read + comment;
  their agent summons queue for the owner to release), or clone the
  repo and run the identical `botference review` (agents auto-detected;
  without the CLIs they still read and comment), or plain
  `node review/server.mjs` — then `node review/submit.mjs [--push]`
  (commits only their own `state/users/<handle>.json`).
- The server is long-lived and owned by the human; don't leave your own
  test servers running.

## The interface contract (don't regress these)

- **Comments are the only surface for discussing the document.**
  There is no chat-about-the-paper panel and there will not be one: it
  was tried, it was confusing, it is rejected. Anything *about the
  text* is an anchored margin thread. The one exception, added
  deliberately, is the **task console** — a bottom-docked, collapsible,
  owner-only, desktop-only bar for *document-level instructions that
  have no anchor text*: "apply all", "commit", "restructure section 3",
  "verify every citation resolves". Same strict routing (no
  `@claude`/`@codex`/`@all`, no agent). The Changes widget lives inside
  it, because committing is itself a document-level task. Interrupts
  (permissions/choices) render on the card, in the console for
  console-issued turns, or as sidebar toasts when off-page (120s
  default-deny).
- **Strict-but-social routing.** `@claude` routes to Claude alone; the
  free-form footer handoff is disabled on review turns. To involve the
  other agent, @-tag it in your thread reply — the server converts
  that into a visible mention turn (depth cap 1 per thread per round).
  `@all` engages both.
- **Mentions fire only on explicit confirm** (Done/Enter), never while
  composing.
- **Every author is visually distinct** (stable accent color; Claude
  coral, Codex blue, humans hashed hues); resolved comments live in a
  reopenable resolved tab — and ANYONE may resolve/reopen ANY thread, attributed as "resolved by <handle>" (server-mediated; ownership boundary intact); humans can edit/delete their own entries
  (`edited: true` — treat an edited entry newer than your ack as new
  input); author filter chips; light/dark/system theme toggle.
- **Changes widget** (inside the task console, owner-only) is the
  commit workflow: accept → ⚡ Apply (gathers every participant's accepts; the owner's explicit decision wins conflicts) → read → ✓ Commit (or ↩ Revert).
  Apply is deterministic AND author-agnostic (`apply.mjs`: unique-span
  replacement over bot cards *and* human suggestions, atomic bib
  append, JSON-aware edits for config-key targets,
  `needs_manual_resolution` on drift — never guessed). Apply and commit
  are always separate actions. Out-of-band source edits surface in the
  widget with a commit action.
- **Everything is commentable.** Paragraphs, figures, headings, list
  items, block quotes, captions, table cells and the masthead title all
  carry a `data-cid`. `blk-N` is a POSITIONAL index over `#paper p,
  #paper figure` and every existing comment is anchored to one — so
  that selector is frozen, and each newly anchorable type has its own
  namespace (`-hd-N`, `-misc-N`). Never widen the `blk` selector.
- **Humans suggest too.** The composer has Comment and Suggest modes.
  A human suggestion is an entry in that human's own
  `users/<handle>.json` (`suggestions.json` stays bot-owned), renders
  inline as del/ins in that human's colour through the same path as a
  bot card, and flows through the same accept → Apply → Commit. Its
  source span is resolved to something UNIQUE at compose time — widened
  with context if ambiguous, anchored on the enclosing macro for
  headings, aimed at the config `title` key when the masthead comes
  from there — and the UI shows what it locked onto. See SCHEMA.md.
- **Presence is coarse and private.** Humans + agents in the top-right
  cluster; state computed from real interaction, in server memory only,
  never written to disk, symmetric for everyone, desktop-only.
- **Three tiers, not two.** `state/grants.json` (owner-written) can let
  a named handle summon agents within a visible daily cap. Apply,
  Commit, Revert, model switching and permission answers stay
  owner-only forever — a grant never confers them.
- **Never invent a quota number.** Neither provider exposes
  subscription (Pro/Max, ChatGPT plan) quota to anything scriptable;
  the Settings panel says so and points at `/usage`. Do not
  reverse-engineer internal endpoints to fake it.
- **Calm UI**: no `prompt()`/`alert()`/`confirm()`, no scroll-jumps,
  layout reflows (nothing overlays content), engine files stay 100%
  document-agnostic (all specifics in `review.config.json`).

## File ownership (never write another writer's file)

| File | Writer |
|---|---|
| `state/users/<handle>.json` | that human's browser (via server) — comments, decisions, thread replies AND that human's suggestions |
| `suggestions.json` | bots |
| `state/threads.json` | bots |
| `state/ack.json` | bots |
| `state/apply.json` | apply.mjs (round ledger) |
| `state/grants.json`, `state/grant-usage.json` | the owner, via the server |
| `site/`, `suggestions.js` | build.mjs only |
| presence | **nobody — server memory only, never a file** |

## Round protocol (when summoned — by an @tag or "read my comments")

1. Read all `users/*.json`, diff against your `ack.json` entry
   (include entries with `edited:true` newer than your ack). Those
   files now also carry humans' own `user-suggestion` entries — read
   them as proposals, and do not duplicate one a human already made.
   A DOCUMENT-LEVEL turn from the task console says so in its envelope:
   answer in the turn text, do not write a thread entry for it.
2. Reply to each new comment in `threads.json` — length case-by-case,
   **never more than 6–8 sentences**, no restating, no preamble. If a
   text change is warranted, add a suggestion card
   (`current_text`/`proposed_text`, `reply_to`) — see SCHEMA.md.
3. Rejected cards get exactly one follow-up (concede or your single
   best counter-argument).
4. **Never edit document sources during a round.** Source changes go
   through the user's Apply/Commit buttons only. Site styling/engine
   fixes the user asks for directly may be made in `review/` files and
   committed with a clear message.
5. Update `ack.json` last (crash mid-round → the round re-triggers).

## Verification bar for any engine change

`node --check` all touched JS; rebuild; confirm served assets updated;
never kill the human's running server (verify on a throwaway port);
grep engine files clean of document-specific strings; if a change
touches document sources, compile the document (e.g. `latexmk -pdf`)
and inspect the output before claiming done.

## Long-lived processes (servers, tunnels)

To serve or tunnel anything that must outlive your turn, use
`botference service start <name> -- <command…>` — or the one-shot
`botference review --share --service` / `botference plan --share
--service`, which run the whole share (server + tunnel) as a managed
service, print the `share this: <url>   password: <pw>` line, and
return control. **Never bare background processes** (`&`, `nohup`,
`setsid` by hand): they die with your turn's process-group teardown.
Manage what you started with `botference service list|logs|stop`.
