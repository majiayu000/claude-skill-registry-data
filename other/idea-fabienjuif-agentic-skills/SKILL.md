---
name: idea
description: Quickly capture an idea about the current project into docs/IDEA.md — a "what's next" backlog. Ideas can be anything project-related, technical or not, horizontal (tooling, process, docs) or vertical (a feature). One dated entry with just enough context that a future session or human can pick it up cold. Also handles pruning ("/idea unbloat" — interactive curation where surviving ideas earn a survived ×N marker) and prioritizing ("/idea sort" — an interactive triage session where the USER decides priority buckets, seeded by the survival counter, and the file is rewritten in that order). Use when the user says "/idea", "capture this idea", "note this idea", "remember this for later", "add to the idea backlog", "/idea unbloat", "prune the ideas", "/idea sort", "help me prioritize the ideas", or drops a "what if / we could / someday / next we should" thought they don't want to act on right now. For work to start now, use make-plan instead.
---

# /idea — capture an idea before it evaporates

Ideas are cheap to lose and expensive to reconstruct. This skill captures one into
`docs/IDEA.md` — a single "what nexts" backlog for the current project — fast, with just
enough context that a **fresh agent session** or a **human** can pick it up cold weeks later.

Anything project-related qualifies: technical or not, horizontal (tooling, CI, docs, process)
or vertical (a feature, a product direction). Capture is deliberately friction-free: no
categorizing, no prioritizing at write time. Prioritization happens on demand via
`/idea sort`, pruning via `/idea unbloat`.

This is the lightweight sibling of `make-plan`: an idea is *not yet* work, so it gets one
entry in one file, not a plan directory.

## When to use

- The user drops an idea mid-task they don't want to pursue now.
- Explicitly: "/idea <text>", "capture this idea", "remember this for later".
- `/idea unbloat` — the backlog needs pruning (see below).
- `/idea sort` — the user wants help deciding priorities (see below).
- Skip when the user wants to act now — that's `make-plan` (or just doing it).

## Capture process

### 1. Capture from context — don't interrogate

The idea usually arrives with its context (the conversation, the file being edited, the bug
just found). Use that. Ask **at most one** clarifying question, and only if the idea itself is
genuinely ambiguous. This is capture, not design — a 30-second write beats a perfect one.

### 2. Locate or create the file

The backlog lives at `docs/IDEA.md` from the repo root (create `docs/` if needed). If the file
doesn't exist, create it with this header:

```markdown
# Ideas

"What next" backlog for this project, captured with `/idea`. New entries land on top,
untriaged. Prioritize with `/idea sort` (entries get a `[now]`/`[next]`/`[later]` bucket and
the file is reordered). Prune with `/idea unbloat`; kept ideas earn a `survived ×N` marker.
When an idea gets picked up, promote it with `/make-plan` and link the plan directory from
its entry.
```

### 3. Prepend an entry (very top, right under the header)

```markdown
## <short imperative title> — <YYYY-MM-DD>

<The idea in 1–3 sentences, staying close to the user's own words.>

- **Sparked by:** <what we were doing when it came up; real file paths if relevant>
- **Why:** <the value if it were done>
- **First step:** <smallest concrete action to start>
```

Get the date with `date +%Y-%m-%d`. The bullets are there to help future recall — drop any
that add nothing for this particular idea (a non-technical idea may have no "first step" yet).
New entries always go on top, above any bucketed ones — the top of the file is the untriaged
inbox. During capture, never touch existing entries or their order; only `/idea sort` and
`/idea unbloat` may rewrite the file.

### 4. Warn on bloat

After appending, if the backlog has grown past **~20 entries** (or ~250 lines), tell the user
it's getting bloated and suggest `/idea unbloat`. If many entries are untriaged, suggest
`/idea sort` instead. Just flag it — don't prune or reorder uninvited.

### 5. Stay small

Don't research the codebase, don't design a solution, don't implement. If capturing honestly
takes more than ~10 lines, it isn't an idea anymore — offer to run `make-plan` instead and
have the entry link to the resulting `docs/plans/<name>/`.

## /idea unbloat — interactive pruning with reinforcement

One of the two modes allowed to rewrite or delete entries. The user decides; you propose.

1. Read the whole file. For each entry, form a recommendation with a one-line reason:
   - **drop** — obsolete, superseded, or already done;
   - **merge** — duplicates/overlaps another entry (say which);
   - **promote** — repeatedly relevant, deserves `make-plan` now;
   - **keep** — still plausible, leave it.
2. Present the recommendations and let the user decide, via `AskUserQuestion` (multi-select,
   batched if the list is long) or a plain summary they can redline. Never drop an entry the
   user didn't confirm.
3. Rewrite the file with the outcome:
   - Kept (and merged-into) entries get their survival count bumped in the title:
     `## <title> — <date> (survived ×N)` — from no marker to `×1`, `×1` to `×2`, etc.
     Surviving a prune is a deliberate "still want this" vote, so a high ×N is a genuine
     priority signal.
   - Merged entries fold their useful content into the survivor; the survivor takes the
     **highest** count among the merged group, +1.
   - Dropped entries are removed entirely — the backlog is not an archive.
   - Preserve existing bucket markers and bucket order; unbloat prunes, it doesn't re-rank.
4. Report the result: N kept, N merged, N dropped, N promoted.

Caveat when *reading* the file: `×N` measures how many prunes an idea lived through, not
intrinsic value — a fresh unmarked idea isn't worse than an old `×3`.

## /idea sort — the user decides priorities, the file records them

An interactive triage session. **You draft, the user decides, the file persists their
decision** — never silently apply your own ranking.

Buckets: `[now]` / `[next]` / `[later]`, carried as a suffix in the entry title:
`## <title> — <date> (survived ×2) [next]`.

1. Read the file; split entries into untriaged (no bucket) and already-bucketed.
2. Draft a proposed bucket for every untriaged entry, seeded by:
   - **survival count** — `survived ×N` is the user's own repeated "still want this" vote;
   - **fit with current context** — touches what the user is working on now;
   - **cheap first step** — concrete small first steps favor `[now]`.
3. Present the full picture (proposed buckets + existing ones) and run the decisions through
   `AskUserQuestion` — batched, one question per contested idea or per bucket, with your
   proposal as the recommended option. Also ask whether any *existing* bucket assignment
   should move; re-sorting old decisions is allowed here because the user is making the call.
4. Rewrite the file in bucket order — `[now]`, then `[next]`, then `[later]` — newest first
   within a bucket. Untriaged entries the user skipped stay on top, above the buckets.
5. If anything landed in `[now]`, offer to promote the top one with `make-plan`.

Skip already-promoted entries. Survival counters are unbloat's job — sorting never bumps
them.

## Promoting an idea

When an idea is picked up later: run `make-plan`, then append to the entry's bullet list:
`- **Status:** promoted → docs/plans/<name>/`. Keep the entry — the backlog doubles as a
record of what was considered and when.
