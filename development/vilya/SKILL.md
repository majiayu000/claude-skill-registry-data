---
name: vilya
description: Use when the user runs /vilya [start|ready|status|stop|log], or asks in plain words to "start the dev server", "serve the blog", "is the preview up yet", "wait for the rebuild", "stop that server". Holds a protocol-less local server — a Vite or webpack dev server, a Zola or Hugo preview, an API mock — alive across turns and sessions, registers its address as a clickable row on the statusline, and answers `ready` from the server's own log so a caller can act on a signal rather than sleep and hope. Any caller may use it — you in chat, /feanor between mends, /manwe before a shot. It boots no browser and navigates nothing.
purpose: Keeps a local web server standing and says when it is serving.
user_invocable: true
stage: forge
---

# Vilya — the Ring of Water

Narya keeps a flame alight; Vilya keeps a stream running. One background
process stands per (project, name), and every later turn, session or skill can
ask after it, read its log, wait on it, or put it out.

The gain is not only that the server survives the turn. It is that **someone
owns the process**, so its log is reachable — and the log is where a dev server
says it is serving. Without an owner there is no log to read, and a caller has
nothing to wait on but a clock.

## Verbs

Every verb runs through one hook:

    ~/.claude/hooks/vilya.sh <verb> --name <name> [flags]

| Verb | What it does |
|---|---|
| `start` | Raises the server and leaves it standing. Idempotent — a second `start` finds the first rather than raising a rival. |
| `ready` | Blocks until the server's own log says it is serving. **This is the verb that earns Vilya its keep.** |
| `status` | Is it alive, with which pid, since when. |
| `stop` | Kills it, clears its state, takes down its statusline row. |
| `log` | The server's own transcript — where a failed build explains itself. |

Flags: `--project <dir>` on every verb (default: the nearest ancestor of the
cwd bearing a `.git`), `--name <name>` **required** on every verb, and:

- on `start` — `--url <u>`, `--label <l>`, `--ready-pattern <regex>`, then the
  command after `--`
- on `ready` — `--since <bytes>`, `--timeout <s>` (default 120)
- on `log` — `-n <lines>` (default 40)

One server per (project, name), so a project may hold several at once — a web
dev server and an API mock — each answering to its own name.

## Starting one

    ~/.claude/hooks/vilya.sh start --name web \
      --ready-pattern 'ready in|page reload|hmr update' --label '🌐 Dev' \
      -- npm run dev

Nothing about the command is baked in: Vilya runs whatever you hand it after
`--`, from the project root. Name a `--ready-pattern` whenever the server has
one — without it `ready` cannot answer, and a caller is back to guessing.

**Pick a short, stable fragment**, not a whole banner line. The pattern is an
extended regular expression, so a line pasted whole can defeat itself —
`compiled (1234ms)` reads its own parentheses as a group and matches only the
text without them. `compiled`, `ready in`, `Serving HTTP` are the right size.

**A boot banner alone is not enough when `ready` will be asked twice.** A
server that announces itself once at boot and then reports each rebuild in
different words needs both phrasings in the pattern, joined with `|`. Vite is
the proven case: it prints `ready in 279 ms` once; an edit to `index.html`
then logged `[vite] (client) page reload index.html` — never `ready in`
again. Vite documents `hmr update …` as the wording for a module patch; that
line was not exercised in the run, and is carried in the pattern on Vite's
word rather than on observation. Taught only the banner, a second-pass `ready --since` waited
its whole timeout and returned `7` for a rebuild that had already landed.

Common patterns, as a starting point rather than a promise — read the server's
actual first run *and its first rebuild* and take the phrasing from there:

| Server | A fragment that works |
|---|---|
| Vite | `ready in\|page reload\|hmr update` |
| Zola | `Web server is available` |
| Python's `http.server` | `Serving HTTP` |
| webpack dev server | `compiled` |

## Waiting properly — `--since` is not optional on a second pass

A server announces itself once, and that line stays in its log forever. So a
bare `ready` on the second pass answers *yes* for a rebuild that has not begun.

Read the log's size **before** making the edit, and hand it back:

    before=$(~/.claude/hooks/vilya.sh log --name web -n 99999 | wc -c | tr -d ' ')
    # ... make the edit ...
    ~/.claude/hooks/vilya.sh ready --name web --since "$before"

The `tr -d ' '` is not decoration: BSD `wc` (macOS) pads its count with
leading spaces, and `--since '      49'` is refused as not a whole number.

Only an announcement made after that point counts. Skipping this is the same
mistake as sleeping and hoping, wearing better clothes.

The watermark is taken through `log` rather than by reaching into the state
directory, because `log` resolves the project exactly as every other verb does.
Reaching in by hand invites a glob like `~/.skadi/vilya/*/web/log`, which is
wrong the moment two projects each hold a server named `web` — an ordinary
thing, since the name is only a slot within one project. The `-n` is simply
larger than the log will grow; the offset is a watermark, not a measurement, so
any count at or past the last announcement serves.

Vilya carries no verb that prints its own state path. Until it does, `log` is
the honest way to ask.

## Reading the outcome

The exit code is the contract; a caller's loop branches on it, not on the prose.

| Code | Meaning | What to do |
|---|---|---|
| 0 | done — for `ready`, the server has announced itself | Carry on; what it serves is current. |
| 1 | the state directory could not be laid down | A filesystem fault; read the message. |
| 2 | bad arguments | Fix the call. A number that is not a number lands here. |
| 4 | no server by that name for this project | `start` one, or name the project with `--project`. |
| 5 | the process is gone | It died as it started, died while `ready` waited, or has since exited. Read `log`, then `stop` and `start` again. |
| 6 | readiness cannot be known — no ready pattern | **Fall back to whatever you did before Vilya.** Never read this as ready. |
| 7 | the pattern never came within the timeout | **Treat what it serves as stale.** Read `log`; the build may have failed. |

The `6` / `7` split is the one to respect. `7` says *I waited and nothing came* —
something is wrong. `6` says *I was never taught what to listen for* — nothing
is wrong, but Vilya cannot help, so use a fixed settle and say so.

## Choosing Vilya, Narya, or a plain background call

- **Vilya** — a local server that must outlive the turn, or that something
  downstream must wait on. Any web dev server, preview, or mock.
- **Narya** (`/narya`) — a Flutter app on a booted device. Do not reach for
  Vilya there: `flutter run` reads stdin, dies backgrounded, and needs a
  protocol Vilya does not speak.
- **A plain background Bash call** — a one-shot command that finishes on its
  own and that nothing waits on. A build, a script, a test run. Vilya holds
  long-lived processes; it is not a job runner.

## The statusline row

A server whose address can be learned becomes a clickable row on the
statusline's standing-windows band. `--url` is authoritative, and once named
it is kept in meta for later starts; absent it, the first `http(s)://` the
server printed in its own log is taken. Neither found
draws no row, and `start` still succeeds — the row is an ornament on the hold,
never a condition of it.

Two things to know rather than discover:

- A server slower to announce itself than the settle budget draws no row on
  that first `start`. A later `start` finds it alive and draws it then.
- `--url` and `--label` are remembered in the server's meta. A later bare
  `start` keeps them, and the situation board shows the stored address in
  place of the one read from the log.
- The situation board's Vilya tile follows `start`, `stop` and a `ready` that
  finds the process gone on its own, through a detached best-effort refresh —
  no `/board refresh` is owed, and a failing board writer never changes a
  verb's exit code.

## What Vilya does not do

- **It boots no browser and navigates nothing.** Raising the server is the
  whole job, the same boundary Narya keeps for devices.
- **It does not hold a server that daemonizes itself.** A process that
  double-forks and returns leaves a pid naming something already gone.
- **`stop` kills what it spawned, not that process's children.** A server that
  forks workers of its own may leave them behind.
- **It has been run on Linux only.** `nohup`'s behaviour under MSYS / Git Bash
  is unproven; do not trust it on Windows until someone has watched it there.
