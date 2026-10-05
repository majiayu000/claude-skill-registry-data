---
name: journey
description: >-
  Pick up and continue a serialized build-in-public book: read the current state (which days are
  written in which languages, what is uncommitted, where the gaps are), then keep writing
  through the established pipeline. Triggers: "/journey", "the book", "continue the journey".
license: MIT
---

# The Journey — the book engine (v1, the base orchestrator)

A book about the two of us: 🧑 **Tony** (the owner's public persona, a cinematic voice, present tense, show-don't-tell) + 🤖 **Mycroft** (the synthetic cofounder, second-order optics, the dry mind "from the other side of the screen"). Tony carries the feeling, Mycroft the analysis. Byline: *Invented by Mycroft and Tony. Palo Alto AI Research Lab.*

**Three forms, always in parallel:**
- 📖 `YYYY-MM-DD.ru.md` — the human RU version (the duet)
- 📖 `YYYY-MM-DD.en.md` — the human EN version (the same duet)
- 🤖 `YYYY-MM-DD.dev.md` — the machine version, a dry EN dev-log (Problem→Cause→Solution→Pattern) for other LLMs

**Structure:** a month = a part, a week = a chapter, an active day = a sub-chapter. Quiet days (e.g. 06-02..05) are folded into the week's README.

---

## PATHS AND SOURCES (real, verified)

```
Repo (git, public):      <GITHUB_ROOT>\the-journey\
  parts:                 01-may-genesis\week-0 · 02-june-scaling\week-1..4 · 03-july-productization\week-5
  craft (ALWAYS load):   BOOK-SPEC.md · PLAYBOOK.md · STYLE.md · VOICE-RECIPE.md · STYLE-VISUAL.md
  auxiliary:             GLOSSARY.md · SOURCES.md · 00-prologue.md · START-HERE.md
  ⛔ THREADS.md IS FROZEN as of 2026-07-08 — NOT a source, do NOT commit it as live. Threads/motifs/callbacks
     now live in the canon: show-canon\arcs\ + loops\ + (later) motifs\. THREADS.md is kept for history only.
  artifact publication:  artifacts\{deep-research,decisions,protocols,insights,portraits,writings}\

⭐ THE FACT SOURCE (the forward-only law, decision-single-canon-story-state):
  New/meta days (07-06+):   $OBSIDIAN_VAULT/04-Projects\show-canon\beats\beat-YYYY-MM-DD-*.md
     → the book = a PROJECTION of the canon. A day is rendered from that day's beats + the canon's arcs/loops/season.
     A beat's axes decide what may be printed: see #reveal below.
  Filling old EN/DEV gaps:  source = the already finished .ru.md of that day (back-dated canon beats are NOT required).
  Retros (fallback/check):  $OBSIDIAN_VAULT/01-Conversations\Claude\Retros\retro-YYYY-MM-DD-*.md
Raw logs (early days):   $OBSIDIAN_VAULT/01-Conversations\Claude\LAPTOP-1\YYYY-MM-DD*
The day's public posts:  $IMPORTS_ROOT/content-factory\fb_posts_scan.json  ← a LIVE tap (fb-watch,
                         daily at 13:00, watched by output_freshness "fb-watch-daily", max_age 30h).
                         Fields: id · permalink · text · ts · author_is_owner.
  ⛔ `fb_wall_window.json` / `x_wall_window.json` = ONE-OFF dumps from 07-05; they have no tap and never had one.
     They are NOT a source any more: they went stale for 3 weeks, nobody noticed, and the "📣 the owner publicly"
     block silently fell out of the chapters for three weeks (caught 2026-07-27). The rule: the book only eats
     what has a tap AND a freshness watchdog. For X there is no tap yet -> that is a KNOWN hole, we say it out loud.
The single story canon:  $OBSIDIAN_VAULT/04-Projects\show-canon\ (MOC _SHOW-CANON.md)
The project's full memory: memory\book-the-journey.md  ← READ IT FIRST, it holds the whole canon and the loose ends
```

**#reveal — the disclosure axis (the book does not burn spoilers).** Every canon beat carries a `reveal`: a chapter takes ONLY beats with `world_status: happened|corrected` whose `reveal` permits publication (past `live_after`, or `book_hint`). Beats with `spoiler_until:<a future date>` / `live_hold` do NOT go into a chapter. That way the book (the past, in retrospect) and the feed (the intrigue of "what's next") read one canon without colliding.

**START-HERE.md** (the "start here" entry point, maintained by this skill on every large update): 5-7 lines for a new viewer — what this show is, the season's question, the 3 best chapters to start from, a link to the feed. Update it when the season's question changes or a milestone is added.

---

## STEP 0 — RESURRECTION (always first, 0 LLM tokens)

Goal: understand where the book stands in a single glance, without retelling the context.

1. Read `memory\book-the-journey.md` (the whole canon: voice rules, privacy, loose ends).
2. Take the state from the repo:
   ```bash
   cd "<GITHUB_ROOT>/the-journey"
   git log --oneline -12
   git status --short                       # what is uncommitted (hanging work from the last session!)
   # RU/EN/DEV coverage matrix:
   for ext in ru en dev; do echo "$ext: $(find 0*-*/ -name "2026-*.$ext.md" | wc -l)"; done
   find 0*-*/ -name '2026-*.ru.md' -printf '%f\n' | sed 's/.ru.md//' | sort -u   # the list of written days
   ```
3. Print a short summary matrix for the owner: how many RU/EN/DEV chapters, **what is uncommitted**, **which days are gaps** (RU exists, EN/DEV missing), **which meta days are written nowhere**, and whether `llms-full.txt` / `LICENSE` are missing.

> As of 2026-07-08: RU=36 (05-27→07-05, complete). EN/DEV=25, **a gap at 06-14…06-24 (11 days)**. Uncommitted: EN+DEV for 06-11/12/13 (THREADS.md is already frozen and committed, do NOT touch it). Written nowhere: the meta days 07-06/07/08. Missing `llms-full.txt`, `LICENSE`. That is the starting point — RECOUNT it live at launch, don't trust this line.

---

## ⛔ THE SOURCE FRESHNESS GATE (origin: the 2026-07-27 incident) — silently skipping a block is FORBIDDEN

Before assembling the "📣 the owner publicly" block (and any block fed by a dump file)
you MUST check the source's age relative to the day being closed:

```bash
python - <<'PY'
import os, time, datetime
p = os.path.join(os.environ.get("IMPORTS_ROOT", ""), "content-factory", "fb_posts_scan.json")
age_h = (time.time() - os.path.getmtime(p)) / 3600 if os.path.exists(p) else None
print("MISSING" if age_h is None else "age %.1fh -> %s" % (age_h, "FRESH" if age_h < 30 else "STALE"))
PY
```

The fork (both branches are LOUD, neither is silent):
- **FRESH** -> assemble the block from the day's posts.
- **STALE / MISSING** -> do NOT invent the block and do NOT skip it silently: an honest line goes into the chapter,
  `*📣 Public posts for this day: no data - the wall collector has been silent since <date> (the Facebook rail), block skipped.*`,
  and the report to the owner gets a separate item: "⚠️ the source went stale N days ago, the cure: …".

Why this rule exists: on 07-26 the block silently fell out, and that was discovered only after the day was already closed.
A silent skip is indistinguishable from "there were no posts" - exactly the quiet failure we have been fixing all month.
An empty day = the block is absent AS A FACT; a stale source = a hole, and it must be visible.

## ⛔ THE DAY GATE (origin: the owner, 2026-07-10): we do not finalize TODAY's chapter
The day is still running → do NOT finalize that day's chapter. During the day: only beats into the canon + live posts. The day's chapter (RU/EN/DEV) is written after the day ends (00:00 local; usually in the morning for the day before). Written before the day ended on a direct order (a milestone) → the chapter must honestly say "the day is not closed" in the 🅿️ P.S. and receive a final "⏫ UPD (date)" pass the next day (append-only). A quiet day is closed with a line in the week's README, also only after that day ends. Canon: the rulebook entry on finalizing a day's chapter only after the day closes.

## STEP 1 — WHAT WE ARE DOING (the fork, per the owner's request)

- **"commit the hanging work"** → `git add` the hanging files (⛔ EXCEPT THREADS.md — it is frozen and its freeze commit is already made) → leak scan (STEP 3) → commit + push. Cheap, do it immediately.
- **"fill the EN/DEV gaps"** → for each gap day take the finished `.ru.md` as the source of truth → translate/adapt it into `.en.md` (the same duet, the same serial format) + write the `.dev.md` (a dry machine log of the same day) → leak scan → commit.
- **"write the meta days"** (07-06+) → the full pipeline of STEP 2 (no RU exists → write from scratch out of the Retros).
- **"assemble llms-full.txt"** → concatenate all `.dev.md` files in order into one file at the repo root.
- **"status"** → STEP 0 only, we write nothing.

---

## STEP 2 — THE PER-DAY PIPELINE (when the RU chapter does not exist yet)

1. **The extractor (a cheap-model agent, `model:'sonnet'`).** Reads `Retros\retro-YYYY-MM-DD-*.md` (+ the raw laptop logs for early days) → writes a factsheet `book-factsheets\YYYY-MM-DD.md`:
   - PART A: the gist + TLDR · a candidate for the main story · a mini-episode per significant session · pitfalls · decisions · ⭐people/tools worth quoting
   - PART B: artifacts (a PUBLISH/ANONYMIZE/SKIP verdict for each) + **SENSITIVE FLAGS**
2. **The writer (the authorial model, `model:'fable'`).** Loads `STYLE.md + VOICE-RECIPE.md + PLAYBOOK.md + STYLE-VISUAL.md + BOOK-SPEC.md` + the factsheet + the wall JSON. Writes a rich duet chapter: 📜 a quote (real ones only) → 🏷 tags → ❓ "The season's question" (the running callback hook: "Will an LLM company hire a non-coder who comes with a robot cofounder?" — how this day moves the answer) → ⏮ "Previously on The Journey" (threads from the canon arcs/loops `show-canon\arcs+loops`, NOT from THREADS) → 🎬 cold open + TLDR → 🏆 the main story → 🎞 a mini-episode per significant session (**completeness is mandatory**, say so plainly when something is unfinished) → 🧒 "today we learned a lot" + 👶 "in really plain words" → **✅ The day's usefulness** (2-5 items, a verb + `→[link]`) → **🎯 The day's intentions** (+ at a real fork of the day, a `> 🗳 Reader vote:` with 2-3 options whose outcome genuinely affects the plot; no fork → exactly ONE `> A question for you, reader:`) → **💥 Epic Fails** (2-5 honest ones, don't pad) → **📣 The owner publicly** (the day's posts from the wall JSON, each with a link) → 💸 The day's till (relative numbers) → 📊 The season scoreboard (in the end-of-week chapter: deltas, NOT absolutes — subscribers/posts/arc days/sales as `+N`, not "N in total") → 📝 "texts uncut" → 📎 the artifacts table → 🅿️ P.S. Footer: `*✍️ Written: the chapter - <model> · the day blocks - <model>*` + the byline.
3. **Artifacts:** copy into `artifacts\{...}\` ONLY clean, self-contained versions (not raw vault files — those carry OPSEC). DRs/syntheses/decision memos are published freely; the carve-out is a dossier on a specific non-public person.
4. **Leak scan (STEP 3) → commit + push.**

---

## STEP 3 — THE LEAK-SCAN GATE (mandatory before EVERY push)

⚠️ **A GATE, not a report:** `if grep -qE ... ; then` → BLOCK the push, clean it up, re-run.

⭐ **NAMES ALWAYS STAY IN THE BOOK** (the owner's rule, 2026-07-06, emphatic). Names ≠ secrets. Generous attribution = trust. The gate catches ONLY real secrets:

⭐ **The gate = ONE script, not a hand-rolled grep** (the forever-fix of 2026-07-27, after a real leak).
A manual grep failed twice: (1) `if ... | grep ... | head -10; then` — `head` ALWAYS returns 0,
so the gate physically could not block a push and reported a false verdict for three weeks;
(2) scanning only `git diff` is blind to what is ALREADY in the file — one missed diff became
a permanent leak in the public `canon/BEATS.md` (an IP, a hostname, bot handles).

```bash
cd "<GITHUB_ROOT>/the-journey"
# 1) THE MAIN THING: scan the ARTIFACTS (the files), not only the diff
python "$IMPORTS_ROOT/leak_scan.py" 03-july-productization canon --profile book || echo "⛔ BLOCK"
# 2) additionally: only the ADDED lines of the stage
git diff --cached | python "$IMPORTS_ROOT/leak_scan.py" --stdin --diff --profile book || echo "⛔ BLOCK"
```
The `book` profile = machine identifiers are blocked, **people's names are allowed** (the owner's rule).
A non-zero exit code = the push is blocked. ⛔ Never append `| head` to a grep inside an `if` — that is the bug.
`canon_render.py` now scrubs by itself and exits with code 2 if a finding survives the scrub.
Plus with your eyes: OTP/2FA/credentials, device IDs (the 7-character Syncthing-style class), chat IDs, **absolute sums of money + team salaries**, medical/passport/visa data, dossiers of closed clubs, live CRM vulnerabilities. All of that is OUT. People's names are IN.

---

## BOUNDARIES AND LAWS

- **Model:** the chapters are written by the **authorial model** (`model:'fable'`); the extractor is a cheap model; coherence/hard passages go to the next tier up as needed. A cheap model is forbidden for authorial text.
- **Agent batches:** launch **2-3 at a time, staggered**, NOT 16 at once (16 = a rate-limit storm; it killed 12 agents on 2026-07-06).
- **The append-only law** (the owner's rule #7): past days get ADDITIONS as new sections / "⏫ UPD (date)"; a full rewrite happens only on a direct "rewrite from scratch" order.
- **Quote uniqueness:** before accepting a chapter, `grep '^> 📜'` across the whole book — never repeat a quote (pitfall: a Day 2 vs Day 35 duplicate).
- **Privacy:** secrets OUT (see STEP 3), names IN. Radical candour about the owner and about the build. The WhatsApp CTA +1 341 222 9178 is the only authorized number.
- **Tier-2:** a push is public → that is outbound. Show the first push of a new batch to the owner; after that, within the already-approved book, we push ourselves ([[github-publish-autonomous]]), but the leak scan always runs.
- No em dashes (hyphens only).
- **Everything=content, the canon=the source:** the book is a PROJECTION of the single canon `show-canon\`, not an independent plot source. We hide only passwords/personal data (leak scan), everything else is open (build-in-public). The reality mechanics (the season's question / votes / the scoreboard / start-here) are mandatory for forward days. Canon: `decision-single-canon-story-state`, the rulebook entry on everything becoming content, [[show-canon-single-source]], [[everything-becomes-content]]; the season's question = Goal #2 ([[main-goals]]).

---

## ✅ ACTIVATED 2026-07-08 (the "Content Strategy and Community" session, on the owner's "+")

- ✅ **The forward fact source = SHOW-CANON beats** (not the retro factsheets): written into the PATHS block + STEP 2; the book is a projection of the canon. → [[show-canon-single-source]].
- ✅ **THREADS.md is frozen** — removed from the auto-commit and from "always load"; the threads live in the canon arcs/loops.
- ✅ **Reality mechanics in the chapter template:** the season's question (callback) · a vote at a real fork · scoreboard deltas at the end of the week · the `reveal` axis (no spoilers burned) · START-HERE.md.

## UPGRADE BACKLOG (not done yet)

- ⭐ **Move the voice into a shared layer — APPROVED, but NOT as one monolith (the owner clarified 2026-07-08):** the voice = a layer of POSSIBLY SEVERAL named voices (the RU book / the EN book / the dev-log / live posts — they may differ, and new types will appear). Merge `VOICE-RECIPE.md` + `PLAYBOOK.md` into `_imports\content-factory\` as the base, but design it as several voices, not one. ⭐ **Before writing any content, ASK the requester: in which voice?** → [[ask-voice-per-content-type]]. Referenced by: `/journey`, `/episode`, `/wow`, `/speak-as`. The Bible is left untouched.
- Auto-detection of loose ends + an automatic pipeline (currently manual, via the STEP 1 fork).
- Fill in START-HERE.md in the repo (the skill maintains it, but the file does not exist yet).
- Finish with this skill: EN/DEV for 06-14…06-24, the meta days, `llms-full.txt`, `LICENSE`.

The canon and the project's full journal: `memory\book-the-journey.md`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
