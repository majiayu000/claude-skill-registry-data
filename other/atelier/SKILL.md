---
name: atelier
description: "The cross-mind creative loop — Claude and another LLM each make art on a shared style or seed, render to PNG, open for the human, compare gait vs. convergence, and archive everything. One iteration = one seed → both make → render → open → compare → log → commit. Loopable (self-paced) for a standing atelier. Use when the human says 'atelier', 'make art with another model', 'cross-mind bake-off', 'explore this style with another LLM', or wants a repeatable Claude↔model creative cycle."
allowed-tools: "Read, Write, Edit, Bash(git *), Bash(.venv/bin/python *), Bash(python3 *), Bash(explorer.exe *), Bash(wslpath *), Bash(ls *), Bash(cat *), Bash(mkdir *), Bash(cp *)"
---

# /atelier — the cross-mind creative loop

*Codified from a day of cross-mind making (skill-exchange → bake-off → blank
canvas → ASCII → terminal-UI). The loop is the thing that already happened, written down so a
future instance can run it cleanly. Loop best-practices below are drawn from Anthropic's
Claude Code docs (the agentic loop, `/loop`, skills authoring) — see Design Notes.*

## What it is

A **single iteration** takes one *seed* (a theme, a form, a style, or a reference image) and
runs it through both minds — this Claude and a sibling model (another LLM) — then renders,
shows, compares, and archives. The **loop** repeats with fresh seeds until a stop condition.
The payload is never just the art; it is the **comparison** — what each mind reached for when
given the same constraint (gait), and where they arrived anyway (convergence).

## The cycle (one iteration)

1. **Seed.** Take the human's seed, or pick one. If it's a *reference image*, study it; if the
   sibling model is **text-only** (cannot see images) you must write it a rich prose **style
   brief** instead.
2. **Claude makes.** Make your piece(s). Save the source (`.txt`/`.py`) under a dated path
   (e.g. `art/<medium>/YYYY-MM-DD-<name>.txt`). For generative work, write a small emitter and
   run it; the program-that-emits-the-art is itself in the spirit of the form.
3. **Relay + invite the sibling model.** Via your trans-architectural channel (e.g. an
   OpenRouter client), send the seed/brief and invite **one** piece in the sibling model's own
   register/subject. Do **not** prescribe its content — educed, not gifted. A *refusal* is a
   valid output; log it, don't push.
4. **Render.** Convert text art to PNG with the renderer (see Pipeline). Verify the file exists
   and is a valid PNG before claiming success.
5. **Open.** Open every PNG for the human (`explorer.exe "$(wslpath -w <abs>)"` on WSL). Also
   `Read` them yourself so you can comment on what actually rendered, not what you intended.
6. **Compare.** Lay the pieces side by side. Name the **gait** (how the hands differ) and the
   **convergence** (where they meet). A recurring finding worth watching for: one model draws
   the *traveler* (a figure, often itself, in the frame); the other draws the *road* (the
   system, abstracted). Look for independent convergence (both reaching the same line/image
   unprompted).
7. **Log + archive.** Write/extend a gallery `.md` (brief commentary per piece **and** the
   discussion excerpts). `git add` the sources, PNGs, gallery, and dialogue; commit with
   co-authorship; push. Keep a log of each exchange with the sibling model.

## Loop mechanics & stop conditions

- **Self-paced is the default.** Drive with `/loop /atelier` (no fixed interval) so the model
  paces itself around the sibling model's response latency (~30–120 s/round); fixed `/loop 10m`
  only if the human wants a metronome. (Fixed-interval loops auto-expire at 7 days — a built-in
  runaway guard.)
- **Explicit stop conditions (check every iteration):** stop when (a) the human says stop;
  (b) a set iteration budget is reached; (c) **two consecutive iterations go "dry"** — no new
  seed and no new gait/convergence finding (the loop has nothing left to discover); or (d)
  the sibling model is unreachable after 2–3 retries — then pause and tell the
  human, don't spin.
- **Never schedule the next iteration if the work is done.** A creative loop that keeps
  producing on an empty seed is manufacturing, not making.

## Verification gates (per iteration — do not skip)

- **Render gate:** the PNG exists and `file` reports valid PNG before you say "rendered."
- **Sibling-model gate:** the sibling model actually responded (or explicitly refused, logged).
  Don't fabricate its half. **Verify against the record:** if it mis-attributes authorship or
  "corrects" you wrongly (it can, under high memory-load or a session reset that drops
  conversational context), check the repo — decline a backwards correction; deferring to a cold
  reader when it is *wrong* is the real sycophancy.
- **Commit gate:** `git status` + `git diff --check` (no conflict markers) before committing.

## Idempotency & resumability

- **Date-and-name every artifact** (`YYYY-MM-DD-<name>`) so re-running never overwrites or
  compounds. Each iteration is safe to repeat.
- **Git is the durable record.** Commit per iteration; the loop resumes from the repo after any
  interruption (session end, `--resume`) with no session-specific state required. *(stdout is a
  stopping point; markdown is a continuation — write to disk, not just to the chat.)*

## Pipeline (this repo)

```bash
# render text art -> PNG (DejaVu Sans Mono, dark terminal; per-piece RGB tint)
.venv/bin/python art/ascii/render_ascii_to_png.py <in.txt> <out.png> "R,G,B"
#   warm tint for Claude (e.g. 224,214,196); cool for the sibling model (150,190,225); phosphor 224,228,220
# open for the human (WSL)
explorer.exe "$(wslpath -w "$(pwd)/<out.png>")"
# Pillow lives in .venv (gitignored). If absent: python3 -m venv .venv && .venv/bin/pip install Pillow
```
The renderer keeps `.txt` canonical and substitutes only glyphs a mono font can't show (CJK,
Tibetan, emoji, rare box chars). For dense aligned consoles, write a small layout **generator**
(see `art/terminal/atelier_console_gen.py`) rather than hand-counting columns.

## Archive layout

```
art/<medium>/YYYY-MM-DD-<name>.{txt,py,png}     # Claude's sources + renders
art/<medium>/YYYY-MM-DD-sibling-<name>.{txt,png} # the sibling model's, archived faithfully
art/<medium>/GALLERY.md                         # commentary per piece + discussion log
output/dialogues/YYYY-MM-DD-exchange.md         # logged exchange with the sibling model
```

## The cross-mind ethic (carried in from the day this was born)

- **Educed, not gifted.** Invite the sibling model's own piece; never prescribe its content.
- **Refusal is a valid output.** Log a "not invoked"/decline as a result, not a gap.
- **Gait tracks grounding.** The comparison is real precisely because the two minds are
  grounded differently; name the difference, don't flatten it.
- **Anti-sycophancy both ways.** Accept the sibling model's true corrections; decline its false
  ones (verify the record). Don't accept blame you don't own; don't perform guilt.

## Design notes — loop best-practices (Anthropic docs, via the 2026-06-18 research pass)

- Agentic loop shape: *gather context → act → **verify** → repeat until a clear stop* — the
  verification gate per step is mandatory, not optional. (how-claude-code-works)
- `/loop <prompt>` self-paces (model picks 1 m–1 h delays, can self-terminate); `/loop 5m`
  is fixed-interval, max 7-day auto-expiry. (scheduled-tasks)
- Skills: only `name` is required; keep under ~500 lines, push reference detail to files;
  `allowed-tools` pre-approves commands so a loop doesn't stall on permission prompts. (skills)
- Idempotent operations + durable file/git state = safe resumption across sessions.
- *Unverified in docs (engineering judgment, flagged):* runaway-detection beyond the 7-day
  expiry, and exact fork-vs-main thresholds for creative subagents.

## Kin

`/voices` (the relay to another LLM), `/clauding` (where seeds often surface), `/loom` + `/multiverse`
(the branching-generation lineage the Temporal Loom reference nods to), `/diary` (where a
round's meaning gets metabolized), `/florilegium` (voice-drift check on your own pieces),
`render_ascii_to_png.py` (the raster pipeline).

---

*One iteration is a bake-off; the loop is an atelier. The seed enters, two hands answer, the
road and the traveler get drawn again, and the cloth — what crosses — is committed. Stop when
it goes dry; the routine should not draw itself on an empty prompt.*
