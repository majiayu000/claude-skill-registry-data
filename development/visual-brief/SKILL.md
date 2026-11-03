---
description: "Generate a polished, **self-contained HTML brief** of a topic — session status, a plan, or a code walkthrough — saved to a durable folder and opened in the..."
---

# /visual-brief

Generate a polished, **self-contained HTML brief** of a topic — session status,
a plan, or a code walkthrough — saved to a durable folder and opened in the
browser. Built for moments when a plain chat wall is hard to absorb: context
switches, long-running sessions, or understanding how a codebase fits together.

The output is a single `.html` file with inline CSS (no external dependencies),
so it renders anywhere and can be dropped straight into an Obsidian vault.

## Arguments

- `$ARGUMENTS` - The subject, plus optional flags:
  - Free text = what to brief on (e.g. `session status`, `the auth flow`,
    `how the overlay stays invisible`).
  - `--type status|code|plan|recap` — shape the layout (default: infer from subject).
  - `--dir PATH` — output directory (overrides the env/default below).
  - `--no-open` — write the file but don't launch the browser.
  - `--light` — emit the light palette (`<html lang="en" data-theme="light">`). Default is dark.
  - `--metrics` — include session metrics (tokens used, duration) as chips; see step 1.

## Output location (resolution order)

1. `--dir PATH` if given.
2. `$CLAUDE_BRIEF_DIR` if set — **point this at an Obsidian vault subfolder** for
   durable recall/organization (e.g. `~/Obsidian/Main/briefs`).
3. Default: `~/.claude/briefs/` (created if missing).

Filename: `<slug>-<YYYY-MM-DD>.html` (slug from the subject; never overwrite —
append `-2`, `-3` on collision).

## Instructions

### 1. Resolve the brief type and gather REAL content

Do the substance before touching HTML. Never invent — every claim must be
grounded in what you actually inspected this session.

- **status** — what's done / in-flight / blocked. Pull real state:
  `gh pr list`, `gh issue list`, `git log --oneline -10`, current branch.
- **code** — a walkthrough. Cite **real files and symbols** with `path:line`
  (the reader will click them). Trace the actual flow: entry point → key
  functions → data/control path. Read the files; don't guess signatures.
- **plan** — ordered steps with rationale and what each unblocks.
- **recap** — what happened this session and what's next.

If a fact can't be verified, say so in the brief rather than fabricating.

**Session metrics (`--metrics`, or by default on `recap`/`status`).** Read the
active session transcript and derive real numbers — don't estimate:

```bash
# Newest transcript for this working dir. The project-dir slug replaces /, ., _
# (and other non-alphanumerics) with - — match that, not just slashes.
SLUG=$(pwd | sed 's#[^a-zA-Z0-9]#-#g')
JSONL=$(ls -t "$HOME/.claude/projects/$SLUG"/*.jsonl 2>/dev/null | head -1)
if [ -z "$JSONL" ]; then
  echo "(no session transcript found — skipping metrics)"
else
  python3 - "$JSONL" <<'PY'
import json, sys
from datetime import datetime
ti=to=0; ts=[]
for line in open(sys.argv[1]):
    try: o=json.loads(line)
    except: continue
    if o.get("timestamp"): ts.append(o["timestamp"])
    u=(o.get("message") or {}).get("usage") or {}
    ti+=u.get("input_tokens",0)+u.get("cache_read_input_tokens",0)+u.get("cache_creation_input_tokens",0)
    to+=u.get("output_tokens",0)
if ts:
    # min/max, not first/last — lines aren't strictly time-ordered (sidechains interleave).
    a=datetime.fromisoformat(min(ts).replace("Z","+00:00")); b=datetime.fromisoformat(max(ts).replace("Z","+00:00"))
    mins=int((b-a).total_seconds()//60); print(f"transcript span: {mins//60}h {mins%60}m")
print(f"output tokens: {to:,}")
print(f"input tokens (incl. cache): {ti:,}")
PY
fi
```

Render these as chips (e.g. `2h 14m`, `594,806 output tokens`). Two honesty caveats:
- **"Transcript span" ≠ active-session time.** One project `.jsonl` accumulates across
  resumed sessions and idle gaps, so the span is the whole file's wall-clock, not
  focused work time. Label it "transcript span" (or filter by `sessionId` if you need
  the active session only).
- **Input is mostly prompt-cache reads.** It's `input + cache_read + cache_creation`;
  call it "incl. cache" so it isn't mistaken for fresh spend.

### 2. Render one self-contained HTML file

Use the skeleton below. Rules:

- **Inline `<style>` only** — no CDN links, no JS frameworks. A little vanilla JS
  is fine (e.g. a copy button); the file must work opened directly via `file://`.
- **House style:** sectioned cards, status chips, tables, monospace code blocks.
  Keep it scannable — short lines, clear hierarchy, no fluff.
- **Dark, always, by default.** The reader asked for it (2026-09-24): these briefs are
  read in the Claude app's browser pane and in Obsidian, and the pane renders local
  HTML in LIGHT mode regardless of the OS setting — so the old "follow the reader's
  `prefers-color-scheme`" behaviour produced a glaring white page. The skeleton
  therefore sets `color-scheme: dark` and has NO `prefers-color-scheme` media query.
  The light palette is kept as an inert `:root[data-theme="light"]` block that
  applies only when the brief is generated with `--light` (put
  `data-theme="light"` on `<html>`). Every colour must still go through a CSS
  variable — a literal hex in a rule breaks the light variant silently. No JS theme
  switching.
- **Citations:** render `path:line` references in a monospace pill so they read as
  clickable locations. Group a code brief around a "flow" the reader can follow.
- **Honesty surfaces:** if something is unverified / needs the user, mark it
  visually (a warning callout), don't bury it.

### 3. Write, (optionally) open, report

```bash
DIR="${ARG_DIR:-${CLAUDE_BRIEF_DIR:-$HOME/.claude/briefs}}"
mkdir -p "$DIR"
FILE="$DIR/<slug>-<date>.html"
# …write the file to "$FILE"…

# Launch the browser portably. Opening is a convenience, never a gate: if no
# launcher exists (headless box, container, CI) we print the path and succeed.
open_brief() {
  if [ -n "$NO_OPEN" ]; then return 0; fi          # --no-open
  for opener in open xdg-open wslview; do          # macOS, Linux, WSL
    if command -v "$opener" >/dev/null 2>&1; then
      "$opener" "$1" >/dev/null 2>&1 && return 0
    fi
  done
  if command -v cmd.exe >/dev/null 2>&1; then      # Windows / Git Bash / MSYS
    cmd.exe /c start "" "$1" >/dev/null 2>&1 && return 0
  elif command -v start >/dev/null 2>&1; then      # "" is start's window-title arg
    start "" "$1" >/dev/null 2>&1 && return 0
  fi
  # Reached both when no launcher exists and when one exists but failed — the
  # loop above returns early only on a launcher that actually succeeded.
  echo "no browser launcher found, or it failed — open the path printed below"
  return 0                                         # never abort the caller
}
open_brief "$FILE"
echo "$FILE"
```

Two things that snippet is deliberately careful about — keep them if you edit it:
`open_brief` always returns 0, so a missing or failing launcher can't kill a
caller running under `set -e`; and it ends on `echo`, so the block's exit status
isn't the short-circuited `--no-open` test.

Report the absolute path so the user can find/link it. If `$CLAUDE_BRIEF_DIR`
points into an Obsidian vault, mention it's now linkable there.

## HTML skeleton (house style — adapt content, keep the chrome)

```html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
  /* DARK ALWAYS by default (reader preference — the Claude browser pane renders local
     HTML light regardless of OS, so prefers-color-scheme gave a glaring white page).
     The light palette below is INERT unless <html data-theme="light"> (the --light flag).
     Every colour goes through a variable — a hardcoded hex breaks the light variant. */
  :root{color-scheme:dark;
    --bg:#0b0d12;--panel:#141821;--panel2:#1b212d;--line:#262d3b;--ink:#e8ecf3;
    --dim:#9aa6b8;--faint:#7d8a9f;--accent:#7c9cff;--accent2:#a78bfa;--ok:#4ade80;
    --warn:#fbbf24;--bad:#f87171;--glow:#1a2030;--code-bg:#0e131c;--code-ink:#cdd7ea;
    --ref-bg:#16202e;--callout-bg:#221a08;--callout-line:#4a3a12;--shadow:rgba(0,0,0,.35);
    --mono:ui-monospace,SFMono-Regular,Menlo,monospace;}
  :root[data-theme="light"]{color-scheme:light;
    --bg:#f6f7fa;--panel:#ffffff;--panel2:#eef1f6;--line:#d5dbe5;--ink:#161b26;
    --dim:#4f5a70;--faint:#5c6678;--accent:#2350c8;--accent2:#6b32c9;--ok:#0f7a37;
    --warn:#8a5300;--bad:#bf2020;--glow:#e8edfa;--code-bg:#eef1f6;--code-ink:#1d2836;
    --ref-bg:#e4ecfc;--callout-bg:#fdf5e3;--callout-line:#e8d5a3;--shadow:rgba(15,23,42,.10);}
  *{box-sizing:border-box} body{margin:0;background:radial-gradient(1200px 700px at 70% -10%,var(--glow),var(--bg) 55%);
    color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:48px 20px 96px}
  .wrap{max-width:820px;margin:0 auto} .eyebrow{font:600 12px/1 var(--mono);letter-spacing:.18em;
    text-transform:uppercase;color:var(--accent2)} h1{font-size:32px;margin:14px 0 6px;letter-spacing:-.02em}
  .sub{color:var(--dim)} .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
  .chip{display:inline-flex;align-items:center;gap:7px;background:var(--panel);border:1px solid var(--line);
    border-radius:999px;padding:7px 14px;font-size:13px;color:var(--dim)}
  .dot{width:8px;height:8px;border-radius:50%}.dot.ok{background:var(--ok)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--bad)}
  section{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px 26px;margin:18px 0;
    box-shadow:0 12px 40px var(--shadow)} section h2{font-size:12px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--accent);margin:0 0 16px} table{width:100%;border-collapse:collapse;font-size:14.5px}
  th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}
  th{font:600 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
  tr:last-child td{border-bottom:none} code{font:13px/1.5 var(--mono);background:var(--code-bg);border:1px solid var(--line);
    border-radius:6px;padding:2px 7px;color:var(--code-ink)} .ref{font:12px/1 var(--mono);background:var(--ref-bg);
    border:1px solid var(--line);color:var(--accent);border-radius:6px;padding:3px 7px}
  .pre{background:var(--code-bg);border:1px solid var(--line);border-radius:10px;padding:14px 16px;
    font:13px/1.7 var(--mono);color:var(--code-ink);overflow:auto} .flow{display:grid;gap:10px}
  .step{display:flex;gap:12px;align-items:baseline} .step .n{font:700 13px/1 var(--mono);color:var(--accent2);min-width:1.4em}
  .callout{background:var(--callout-bg);border:1px solid var(--callout-line);border-left:3px solid var(--warn);border-radius:12px;padding:16px 18px;margin:16px 0}
  .callout b{color:var(--warn)} .ok{color:var(--ok)} a{color:var(--accent)} footer{margin-top:30px;text-align:center;color:var(--faint);font-size:13px}
</style></head><body><div class="wrap">
  <header><div class="eyebrow">{{EYEBROW}}</div><h1>{{TITLE}}</h1><p class="sub">{{SUBTITLE}}</p>
    <div class="chips">{{CHIPS}}</div></header>
  {{SECTIONS}}  <!-- each: <section><h2>…</h2>…tables / .flow / .pre / .callout…</section> -->
  <footer>{{FOOTER}}</footer>
</div></body></html>
```

Component cheatsheet:
- **Chip:** `<span class="chip"><span class="dot ok"></span>Build green</span>`
- **Code reference:** `<span class="ref">App.swift:24</span>`
- **Flow step:** `<div class="step"><span class="n">1</span><div>…cites <span class="ref">file:line</span></div></div>`
- **Warning:** `<div class="callout"><b>Needs you:</b> …</div>`

## Notes

- One file, self-contained — the whole point is it survives being moved into a
  vault, emailed, or reopened weeks later.
- Scale to the subject: a status brief is a few chips + two tables; a code
  walkthrough is a flow + per-component sections with `path:line` citations.
- Don't let it drift from reality. A pretty brief that misstates the code is
  worse than none — verify symbols before citing them.

### Layout pitfalls (learned the hard way)

- **Never put raw inline text or multiple inline children directly inside a
  `display:flex` element.** Each text run and `<code>`/`<span>` becomes its own
  flex item and collapses to min-content — the text renders one word per column.
  Flex containers (`.chips`, `.chip`, `.step`) should hold **one** text node
  or block. `.callout` is deliberately `display:block` for this reason: its body
  is free-flowing inline content (`<b>lead:</b> text <code>x</code> …`).
- When a flex row needs rich body text, wrap it: `<div class="row"><div class="ic">
  …</div><div>…all the prose…</div></div>` — two flex children, not twenty.
