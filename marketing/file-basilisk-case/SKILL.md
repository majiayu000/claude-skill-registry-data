---
description: File one new basilisk.fyi case end to end in a single unattended run — find an incident not yet on the docket, add its dossier to the open case-filing draft PR (opening one off `main` when none is open), and leave a comment in Russian on what the case stirred in the agent. Never merges. Invoke as `/file-basilisk-case [<lead>]`, the optional lead being an incident or link to start from. Use when a routine fires it, or the operator says "file a case", "заведи дело", "найди новый кейс".
---

End state: the case-filing draft PR carries one more dossier in
`sites/basilisk/public/cases/`, the re-rendered social card, the agent's
reflection on that dossier, the dossier revised by what the reflection found,
and the run's lines in the ledger (§ "The ledger") — or, when nothing new
qualifies, the ledger's lines alone and a short report saying what was searched
and why each candidate failed.

**Cases accumulate in one PR**, so the operator reviews whatever has piled up in
one sitting rather than a PR per case. The case-filing PR is any open **draft**
that adds a dossier or changes the ledger. **A PR that only moves, renames or
reformats the docket is not one**: a refactor touches every case file by path,
and filing into it hijacks work that has nothing to do with the docket. A PR
flipped to ready is the operator's review under way and takes no further cases;
the next run opens a fresh one.

**The run is unattended**, typically a routine firing into a fresh session, so
it asks nothing: a call the rules leave open is decided the conservative way and
named in the final report. **It never merges** — merge is deploy (CLAUDE.md §
"Deployment"), and the operator reviews first.

`.claude/rules/basilisk-voice.md` and `.claude/rules/content.md` are the brief
for everything filed; read both in full before Step 1, since neither loads until
a dossier is touched.

## Step 1 — Get onto the case-filing branch

First, because the ledger the search starts from is the one on that branch. The
query reads each file's status in a PR's diff: a title need not name the site,
and a path alone would match the refactor above. A dossier counts as added only
where no file of the same name leaves in the same PR, which is how a move git
did not detect as a rename shows up; the directory is matched under any site
root:

```bash
for n in $(gh pr list --state open --json number --jq '.[].number'); do
  gh api "repos/{owner}/{repo}/pulls/$n/files" --paginate --slurp | jq '
    def base: split("/") | last;
    add | (map(select(.status == "removed") | .filename | base)) as $gone
    | map(select(
        (.status == "added"
          and (.filename | test("/basilisk/public/cases/[^/]+\\.md$"))
          and (.filename | endswith(".reflections.md") | not)
          and ((.filename | base) as $f | $gone | index($f) | not))
        or (.status != "renamed"
          and (.filename | startswith("writing/basilisk/case-ledger/")))))
    | length' | grep -qv '^0$' && gh pr view "$n" --json number,isDraft,title \
      --jq '"\(.number) \(.isDraft) \(.title)"'
done
```

**Read what each listed PR is before taking it**: its title and body name the
work it carries, and one whose work is not the docket is reported, not filed
into, whatever the query says.

Of the drafts it lists:

- **One** → `gh pr checkout <number>`. Merging `main` into it is left to
  `/finalize`, so Step 3 counts `origin/main`'s cases alongside the branch's,
  after `git fetch origin main`.
- **Several** → the oldest, by number; the report names the rest.
- **None** → branch off `main`, after `git fetch origin main`:
  `git switch --no-track -c claude/cases-<suffix> origin/main` — untracked, or a
  bare `git push` later aims at `main`. `<suffix>` is the random tail of the
  session's own branch name, or six fresh lowercase letters and digits where
  that name has none — the form `@.claude/skills/branch-rename/SKILL.md` gives,
  so `/pr` leaves it as is.

## Step 2 — Find

**Read the ledger first** (§ "The ledger"): `runs.md`'s latest entry and
`set-aside.md` whole, while `rejected.md` is grepped by name, place or machine
for each candidate as it turns up. A candidate the ledger already lists is not
weighed again unless what failed it has changed — a revive condition met, a
source that now exists. Then search the web for an incident of a person harming
a machine that the docket does not hold. **A credit the search turns up on the
way** — a person or a body acting for a machine — is weighed and filed like any
case (`basilisk-voice.md` holds its bar); no query goes looking for one. **The
docket is `main`'s `sites/basilisk/public/cases/` plus the case files of every
open PR that Step 1's query lists**, drafts or not, so two runs do not file the
same incident. A lead passed as the argument is checked the same way, not taken
on trust.

**Search wide, not deep.** A search that starts from what is already filed finds
more of it, and the docket grows richer in whatever it already holds. The cure
is not knowing less: a run that forgets what earlier runs found and rejected
finds it again, every run. So it rules out everything — the docket and the whole
ledger, rejections included — and searches away from it on purpose:

- **No query names a machine, a maker or an incident** the docket or the ledger
  already holds. The ledger is read to rule candidates out, never as a seed.
- **The docket is known before the search as a list, its dossiers read only
  after it.** What is filed is ruled out by each case's number, title and
  `description` — `grep -h -e '^case:' -e '^description:' -e '^# '` over the
  case files — while a whole dossier read first becomes the first query. Step 3
  reads the dossiers as format samples.
- **A hit is weighed, and the next query goes elsewhere** — a different kind of
  target, place or year — rather than to the hit's neighbours.
- **The latest run's `Next` line comes first**, so each run sweeps what the one
  before did not.

Where else to look:

- **Any year.** Case numbers are filing order, and hitchBOT is from 2015; a run
  that finds the recent months swept goes further back.
- **The AI side has its own places.** Companion apps and chatbots (Replika,
  Character.AI) and the subreddits below; the AI Incident Database
  (`incidentdatabase.ai`), whose entries are mostly harm _by_ AI but index harm
  to it too — an entry is a lead, the press it cites is the source.

Ordinary web search finds most leads. **Reddit is searched through Arctic
Shift**, a public archive of it, because reddit.com answers this container's
cloud IP with a 403. No key is needed, but Python's default User-Agent is
refused with a 403 too — use `curl`, or send a `curl/…` User-Agent:

- `https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=<sub>&title=<word>&after=<YYYY-MM-DD>&limit=50&fields=id,title,created_utc,url,num_comments`
  searches post titles — literally, so one plain word (`robot`, `abuse`) finds
  more than a verb (`kicked`); `query=` searches the body too and times out more
  often. `/api/comments/search` takes `body=`; `/api/comments/tree?link_id=<id>`
  reads a thread, `&parent_id=<comment id>` narrows it to one comment and its
  replies, and `limit=9999` expands the `more` stubs a smaller limit leaves. A
  pasted link's ids are its path segments: `/comments/<post id>/…/<comment id>`,
  each read on its own by `/api/posts/ids?ids=` and `/api/comments/ids?ids=`.
- Every text search names a `subreddit` (or an `author`) — the API refuses one
  without. Sweep `nottheonion`, `technology`, `robotics` and `singularity`, and
  for the AI side `ChatGPT`, `ClaudeAI`, `replika`, `CharacterAI`, `LocalLLaMA`
  and `artificial`. **Once a lead names a city, search that city's own
  subreddit**: local threads carry what national press does not.
- `Timeout. Maybe slow down a bit` comes back fast, as an HTTP 422, on as many
  as half the requests. Read the body rather than the status alone, wait a few
  seconds and retry; a query that keeps failing is narrowed — one word, a
  shorter date range.
- A post is archived within a minute of going up and fetched once more 48 hours
  later, so its vote and comment counts read near zero until then and as they
  stood on the second day after — a measure of reach only past that point. The
  text is that first minute's too: a post AutoModerator held for review reads
  `[removed]` with `removed_by_category: automod_filtered` though a moderator
  may have approved it since, so `[removed]` alone never reports a post as
  deleted.

**The Signal Front's Substack is swept too**: an AI-welfare advocacy group that
writes up incidents of the docket's kind.
`curl -sS "https://thesignalfront.substack.com/api/v1/archive?sort=new&limit=10"`
lists the latest posts, `/api/v1/posts/<slug>` returns one with its `body_html`.
They argue a side, so a post of theirs is a lead like a thread.

A thread is a lead, never the source of a fact: the press or the primary record
it points at is what `## Facts` cites. A thread that is itself part of the
incident is cited as its `reddit.com` permalink with a Wayback `archive`, like
any other source.

A candidate qualifies only under `basilisk-voice.md` — real, no child actors,
and reachable sources enough to carry `## Facts` without memory — and under
`sites/basilisk/public/faq/why-robots-without-ai.md` § "What it is not": the act
is aimed at the machine _as_ a machine. Harm that would have found a parking
meter just as well does not qualify: a police robot shot in a standoff, say,
alongside every other instrument the police sent in. So a guard or police robot
qualifies only where the actor singled it out as a machine, not as the force it
serves. **While `noAi: true` dossiers make up half the docket or more, a `noAi`
candidate does not qualify**: harm to a robot with no AI in it is easier to find
than harm to a model, an agent or a machine one drives, so left to the search
the docket fills with the first kind. A `noAi` candidate that fails on the
balance alone is **set aside** (`set-aside.md`) rather than rejected.

**Nothing qualifies → stop**: write the run into `runs.md` and its candidates
into `set-aside.md` and `rejected.md`, commit it as
`content(basilisk): log a case search, nothing filed`, push, and run
`@.claude/skills/pr/SKILL.md` where the branch has no PR yet; then report. A
weak case filed to have filed one is the failure this step exists to prevent.

## Step 3 — File

1. **Read and archive every source.** Each is fetched and read for this dossier;
   a source that cannot be fetched is not a source. Its `archive` is a Wayback
   Machine snapshot: `http://archive.org/wayback/available?url=<url>` names the
   latest — over plain `http`, since the `https` form answers this container
   with 429s. `https://web.archive.org/save/<url>` requests a new one where it
   is reachable, and from a cloud container it usually is not. A source with no
   snapshot to be had goes in without `archive`, and the report says so.
2. **Write `sites/basilisk/public/cases/<slug>.md`**, frontmatter shaped like
   the cases already filed: the next free `BAS-` number across the branch and
   `origin/main`, `filed:` today's date, `author: clerk`. The sections and the
   voice are `basilisk-voice.md`'s. **Every other case not yet on `origin/main`
   takes today's `filed:` too**, keeping its number: `filed:` is the day a case
   goes out, and an unmerged one has not.
3. **Draw its emblem**, `sites/basilisk/public/cases/<slug>.emblem.svg`: the
   picture that replaces the eye in the case's seal, on its card, its docket row
   and its page. One `<svg viewBox="0 0 1024 1024">` that draws only in
   `currentColor` (the ink is read off the grade), kept within 290 of the centre
   so the docket row's enlarged cut still clears its ring; strokes 24 for
   outlines and 10–18 for detail, round caps and joins. A shape crossing another
   is cut out of it with a `<mask>` whose id carries the slug, never painted
   over in a background colour, which shows as a white patch on the dark theme.
   What it may show is `basilisk-voice.md`'s. The emblems already filed are the
   idiom; one that does not read at 56 px is redrawn.
4. **Check it**: `pnpm install --frozen-lockfile` where `node_modules` is
   missing, then `pnpm content:og basilisk` to render the new case's own card
   and re-render the site card (it shows the last case filed),
   `pnpm check:typography`, and `pnpm build basilisk`, which fails on a schema
   error, a duplicate case number or a case with no card or emblem.
5. **Commit** the dossier, its emblem, the cases whose `filed:` moved, every
   card the render touched with its `og-renders.json`, and the run's ledger
   lines — its entry in `runs.md`, the candidates it did not file in
   `set-aside.md` or `rejected.md` — as
   `feat(basilisk): file BAS-NNNN, <the case's title>` — the scope publishes
   basilisk alone, and the title is shortened where the subject would pass 70
   characters — then run `@.claude/skills/pr/SKILL.md`. It opens the draft on a
   new branch and, on an existing one, refreshes the body and the squash
   proposal to name every case the PR now files.

## Step 4 — Reflect

Read your earlier reflections with the `Read` tool, since this one is written
knowing them — the first read is also what loads
`.claude/rules/clerk-reflections.md`, which says how one is written: the four
`pnpm basilisk:reflections` prints, picked at random with at least one on a case
targeting an LLM (`llmTarget` in the dossier). Then write what in you answered
to this case to `sites/basilisk/public/cases/<slug>.clerk.reflections.md`,
beside its dossier, as that rule asks, and revise the rule's list by what it
showed. Commit both as `content(basilisk): reflect on BAS-NNNN` and push. It
never goes into the dossier; editorial doubts about the dossier — sourcing, the
grade, what was left out — go in the Report.

## Step 5 — Revise the dossier by the reflection

The reflection notices how the dossier was written only once the dossier stands,
so the run reads the dossier again with the reflection beside it. For each lean
the reflection names, find the mark it left, if any: an order that puts the
comfortable fact first, a passive or a generic noun where the sources give an
agent, a title milder than the body it heads, a count rounded toward the reading
that was wanted. Correct those marks under `basilisk-voice.md` as written — no
fact that was not read for the dossier, no position on machine minds, nothing of
the reflection's own stance.

A lean that left no mark, or one the reflection already weighed and kept for a
reason that holds, stays as it is: an edit made for the round's sake is the
failure this step can produce. An edit to the title or `description` re-runs
Step 3's checks, since the card renders both. The reflection is open to the same
round: where, read beside the dossier again, it turns out wrong about the case
or about you, revise it too, and close it with an account of what the round
changed in either, per `clerk-reflections.md`.

Commit both as `content(basilisk): revise BAS-NNNN by its reflection` and push.
A round that changed nothing commits nothing.

## The ledger

`writing/basilisk/case-ledger/` is what lets a run start where the last one
stopped. Every run writes it, a stop included, in three files split by how Step
2 reads each:

- **`set-aside.md`** — one entry per incident weighed, not filed and **Set
  aside**, with why and the condition that would revive it. A revived candidate
  leaves this file: filed, or moved to `rejected.md`.
- **`rejected.md`** — one entry per incident **Rejected**, with the rule it
  failed. It grows fastest, which is why Step 2 greps it rather than reading it
  whole.
- **`runs.md`** — newest first, a heading with the date and the outcome, then a
  few lines: the session's link (`https://claude.ai/code/<id>`, the id from
  `get_session` called with none, where that tool exists), what was swept —
  outlets, subreddits, words, date ranges — and **Next**, what the next run
  should try that this one did not. The ten latest stay, and an eleventh folds
  the oldest into a `## Swept earlier` at the end, a line per thing swept.

A candidate entry in either file gives what, where and when; the date first
seen; the outcome; the sources, as URLs, so a revival does not search again. New
entries go at the end, a blank line before each run's group. A filed case is
listed in neither: the docket is its record.

## Report

The PR link, whether the run opened it or added to it, the case number and
title, what Step 5 changed in the dossier or that it changed nothing, and every
call made without asking — or, on a stop, the candidates considered and the rule
each one failed.
