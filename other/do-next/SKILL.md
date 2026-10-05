---
name: do-next
description: Dispatch NEXT.md's open items as worktree-isolated coordinator sub-agents and land each one as it lands. Invoke when the operator says "do next", "work the backlog", "clear NEXT.md", or when a landed batch leaves items still open.
---

# do-next — work `NEXT.md`'s open items with the coordinator model

This skill turns `NEXT.md`'s **Open items** section into a dispatched batch of worktree-isolated
sub-agents, keeps `NEXT.md` itself as the live tracking surface while they run, and lands each
one's work the moment it's ready rather than waiting for the whole batch.

> **Invoke it by telling a session:** *"Follow the `do-next` skill"*, or "work the open items in
> NEXT.md", or "do NEXT".

## When to run this

- `NEXT.md`'s **Open items** section has one or more entries and nobody is actively working them.
- A prior batch just landed and items remain — a landed batch should be followed by dispatching
  the next one, not by stopping (see `CLAUDE.md`'s "an approved plan is authorization" rule; this
  skill's own dispatch is exactly that authorization for the batch it launches).
- The operator asks to "work the backlog", "clear NEXT.md", or names this skill directly.

## Procedure

1. **Read `NEXT.md`'s Open items fresh, don't work from memory of a prior run.** The list changes
   shape every time a batch lands — an item from three sessions ago may already be gone.
2. **Filter before dispatching.** Not every open item is actionable code work. A gotcha note (a
   resolver-behavior reminder, a naming convention learned the hard way) documents something
   already correct — it stays in `NEXT.md` as reference, it doesn't get a track. Only dispatch
   items that describe a real, boundable change.
3. **Saturate. Concurrency is bounded by file ownership, not by batch cadence.** The default is a
   wave: every file with open work against it gets a track, and every track carries as many items as
   its files hold. One agent taking one item is the wrong shape — group all of a file's open items
   into one brief and let that agent work them in order.
   **This is standing, not a one-off.** The moment a track lands and frees its files, refill them in
   the same turn rather than waiting for the batch to drain. A wave that decays to one running track
   because the others finished is the failure mode; check what is free every time something lands.
   **Refill from `NEXT.md`, and from nowhere else.** This step is about how the operator's backlog
   gets run, not a licence to invent work that keeps the wave full. When `NEXT.md` is empty or
   fully claimed, say so and stop — an idle session is the correct state, and it is the operator's
   call what happens next. Manufacturing a playtest, a hunt, a sweep, an audit of documents nobody
   named, or a benchmark run nobody asked for is not saturation, it is unrequested work, and it has
   cost a whole session before now. The one thing you DO add without being asked is a breakage found
   on the way — a failing test, a red pipeline, a bug a track trips over. Those belong to this batch.
   When a hot file (`mudiii-viz.mjs` has been the usual one) carries a dozen items, that is one big
   sequential brief, not a dozen dispatches and not three agents fighting over the same lines —
   parallel edits to one file cost more in merge conflicts than the sequencing saves.
   Say plainly in the in-flight block which files are the bottleneck and what is queued behind them,
   so the next session does not have to re-derive it.
   **The one real cap is the machine**: at most one or two tracks needing `npm run demo:build` or a
   browser at a time. That is a measured limit — three concurrent builds cost two tracks' work.
4. **Decompose into tracks with clear file-ownership boundaries.** Two tracks that both need to
   touch the same file are a merge-collision risk, not two independent tracks — either sequence
   them (land the smaller one first, dispatch the second against updated `main`) or scope each to
   non-overlapping regions of the shared file and say so explicitly in both briefs, the way you'd
   flag it for the coordinator to watch at merge time.
5. **Pick each track's model tier deliberately**, per `CLAUDE.md`'s coordinator ladder — group
   tracks needing similar depth so one hard track doesn't price a whole batch at the top tier:
   - **Opus** — novel design work: a projector/algorithm that doesn't exist yet, a decision with
     real architectural weight, anything in a large/subtle engine file.
   - **Sonnet** — a bounded decision plus mechanical implementation against an existing pattern
     (porting a feature from one page to another, extending a contract that already has worked
     examples to follow).
   - **Haiku** — pure mechanical sweeps: renames, manifest updates, format-only edits.
6. **Write `NEXT.md`'s in-flight tracking block before dispatching**, one line per track naming
   what it covers and its status (`started`). Commit this alone, docs-only — it's the record that
   a batch is running even if the session dispatching it ends before any track lands.
7. **Dispatch each track as an isolated-worktree agent**, self-contained (fresh agents carry no
   conversation context — the brief must stand alone). Every brief needs:
   - Enough project background to work without asking (tmct is pure-JS, deterministic, no LLM in
     the product path — state this explicitly if the task is anywhere near the query/answer path,
     so an agent never reaches for an API call as a shortcut).
   - The exact file-ownership list — what it owns, what it must not touch and why (another track
     owns it concurrently).
   - **Minimal testing only**: `npm run test:smoke` after each meaningful edit, `npm run test:fast`
     plus the specific unit tests covering touched files before its final commit. No full suite,
     no e2e/Playwright — that's the coordinator's job, after merge, at the actual push moment.
   - **Git discipline**: confirm repo-local identity, commit early and often with clean messages,
     never `git stash`/`reset --hard`/`checkout --`/`clean`, never push, never merge to `main`,
     never edit `NEXT.md` (the coordinator owns it — concurrent edits from multiple tracks are a
     guaranteed collision on one file).
   - **For any item whose result is visual, a screenshot the agent actually looks at.** A rendered
     scene, a panel's layout, a legend, a label, a camera angle — an assertion can prove a mesh
     exists at the right height and still say nothing about whether the board reads correctly. The
     brief must tell the agent to drive the page with Playwright, save a PNG, **open that PNG with
     the Read tool**, and describe what it sees against what the item asked for. Reading the image
     is the step that gets skipped; name it explicitly. `scripts/gen-screenshots.mjs` is the
     existing pattern for driving the page and capturing plates. Ask for the before-and-after pair
     when the item is a fix, and require the file paths in the report so the coordinator can look
     too.
   - **A report-back contract**: what it implemented and why, any bugs found along the way even if
     unrelated to the task (name file/line), exact test commands run with pass/fail counts, the
     screenshot paths and what they show, and anything deliberately left out of scope and why.
8. **As each track's completion notification arrives**, land it immediately — don't wait for
   siblings:
   - `git status --short` inside the agent's worktree first. Uncommitted work is a real loss if
     skipped, not just an oversight to note.
   - `cd` to the actual repo root and confirm (`pwd`, `git branch --show-current`) before merging —
     a stale working directory silently merging inside a worktree instead of `main` is a known
     failure mode.
   - `git merge --no-ff` with a message naming the track and what it covers.
   - Run that track's blast-radius tests plus `npm run test:fast` on the merged `main`, not just
     trust the agent's own report.
   - Green: `git push`. Then `git worktree remove` and `git branch -d` the merged branch — leaving
     it is how `.claude/worktrees/` and stale branches silently accumulate.
   - Red: don't push through it. Diagnose before merging the next track, since a broken `main`
     blocks every subsequent push in the batch.
9. **Update `NEXT.md` in the same breath as each landing**, not batched at the end. Move the
   track's in-flight line to a landed note (commit SHA, test counts), and remove the item it
   resolved from Open items — but only once nothing that item's own track surfaced is still
   outstanding (see next point). Narrow the item's text instead of removing it, if the track only
   closed part of a multi-part item.
   **A bug the track's report surfaces is that item's remainder, not a new item** — fold a small,
   safe one into the current fix per `CLAUDE.md`'s "don't narrow scope on your own judgment" rule
   and close both together; a large or engine-wide one still gets written as a sub-clause of the
   SAME item (what landed, what's still open) and keeps that item's checkbox open, even if fixing
   the sub-clause is deferred to the next batch. Only write it as a genuinely separate new item
   when it's actually unrelated to the item's own scope (a different file or subsystem the track
   never touched), and say so explicitly when you do. Closing the item outright and opening a
   freshly-labeled one for the same discovery is stalling dressed as progress — the open-item count
   looks flat or improved, but the record now hides that the original item was never actually
   finished.
   **A failing test a track reports is an open item and a job for this batch, whether or not the
   track caused it.** "Unrelated", "pre-existing", "a flake", "an environment timeout" — none of
   those downgrade it. Write it into Open items with what you actually know (the file, the line, the
   failure text, whether it reproduces on merged `main`), and dispatch a track to resolve it in the
   current batch rather than carrying it forward. If it turns out to be a flake, the fix is to harden
   the test, which is still work this batch does. A red test nobody owns is how a suite rots into
   background noise that stops meaning anything, and the moment a track hands you one is the only
   moment you have its full context.
10. **Track the build honestly, without editorializing.** State what CI actually shows — which
   stage passed, which didn't, why if known — and leave it there unless asked for more. A known,
   already-documented infra blocker doesn't need re-explaining every time it's mentioned.
11. **Roll the patch version once the build is green** (per whatever this project's actual roll
    command is at the time — check `package.json`'s scripts, don't assume a name), running the
    full suite before that push per `CLAUDE.md`'s own rule (the one moment the full suite is
    mandatory, regardless of how narrow every track's own testing was).
12. **Loop.** Anything still open — an item no track picked up, a bug logged during landing, a
    track that failed and needs a retry — becomes the next batch. Dispatch it the same way, don't
    stop to ask permission if the operator's own instruction already covers "keep going" for this
    kind of batch.

## What NOT to do

- Don't dispatch a track for an item that's a documentation note, not a task — check first.
- Don't let a sub-agent push, merge to `main`, or edit `NEXT.md` — those are the coordinator's own
  integration work, and letting several agents touch `NEXT.md` concurrently guarantees a conflict.
- Don't run the full suite inside a sub-agent — `test:fast` plus a named blast radius is the rung
  that replaces it for worktree work; the full suite is for the coordinator's own push to `main`.
- Don't batch every track's merge for the end of the session — merge, test, and push each one as
  it lands, so a slow track doesn't hold back four fast ones.
- Don't silently drop a bug a sub-agent surfaces because it's outside the current track's scope —
  track it in `NEXT.md` as a sub-clause of the item that surfaced it, even if fixing it is
  deferred, and leave that item open rather than closing it and filing the bug as a new one.
- Don't leave a merged worktree or its branch behind — remove both in the same breath as the merge.
- Don't re-litigate or re-explain a known, already-tracked blocker (e.g. an external infra issue)
  every time the build comes up — state the current fact once and move on.
