---
name: fanning-out-doc-search
description: Fans out parallel Sonnet agents for document search. Use for multi-corpus or multi-phrasing lookups, worklog or Glean sweeps.
argument-hint: "<question> [agents=N] [model=sonnet|haiku] [corpus=worklog|glean|repo|drive]"
allowed-tools: Agent, Bash(rg:*), Bash(find:*), Bash(ls:*), Bash(wc:*), Bash(sed:*), Bash(cat:*), Bash(sort:*), Bash(uniq:*), Bash(tr:*), Bash(head:*), Bash(tail:*), Bash(curl:*), Bash(jq:*), Bash(date:*)
---

# Fanning Out Doc Search

Retrieval, not review. This skill finds and quotes what exists across one or more
document corpora. The parent thread keeps the conclusion; agents keep the file dumps.

## Fan out, or just search?

Delegation costs a round trip and loses precision. Earn it.

| Situation | Do |
|---|---|
| One fact, corpus known, one obvious phrasing | Search directly. No agents. |
| Corpus is small (`< ~30` docs) | Read it all yourself. Cheaper than briefing an agent. |
| 2+ corpora, or 3+ plausible phrasings | Fan out |
| "Did I ever write about X" / "where do we say Y" | Fan out — recall questions are vocabulary problems |
| Answer requires reading across many docs to synthesize | Fan out |

Size the corpus **before** deciding:

```bash
find ~/worklog -name '*.md' | wc -l          # local vault
rg -c '' -g '*.md' docs/ | wc -l             # repo docs
```

## The vocabulary problem — read this before writing any query

**The searcher's words are not the corpus's words.** This is the dominant failure
mode, not insufficient parallelism. A hit rate of zero usually means wrong vocabulary,
not absent content.

Worked example: a search of `~/worklog` for `imitation learning` / `IL` / `behavior
cloning` returned **nothing**. The author had in fact written about it four times —
under `BCE`, `delta-failures`, `covariate`, `ablation`, and `expert demonstration`.
The concept was there; the label was not.

So **spend one agent, or one pre-pass, on vocabulary before the search fans out**:

```bash
# What words does this corpus actually use? Tags first.
rg -N '^tags:' ~/worklog --no-heading | tr ' ' '\n' | sort | uniq -c | sort -rn
# Then headings — the author's own section names
rg -N '^#{1,3} ' ~/worklog --no-heading | sort | uniq -c | sort -rn | head -40
```

Then assign each agent a **different vocabulary register** for the same concept:
the academic term, the in-house acronym, the tool/artifact name, the symptom
phrasing, the adjacent-jargon phrasing.

## Partition axes

Pick exactly one axis per fan-out. Mixing axes produces overlapping agents that
all find the same top hit.

1. **By corpus** — one agent per source: local vault, monorepo, Glean, Drive, web.
   Use when the question is "does this exist anywhere."
2. **By query angle** — same corpus, one vocabulary register each (above).
   Use for recall questions in a single corpus.
3. **By document slice** — enumerate the file list first, split into N balanced
   partitions, one agent each. Use when the corpus is too big to grep meaningfully
   and every doc must be *read*, not matched.

Launch all agents **in one message** so they run concurrently.

## Model choice

- `model: sonnet` — the default for retrieval. Enough judgment to recognize a
  paraphrase, cheap enough to run 5 of.
- `model: haiku` — mechanical slice-and-quote over a known file list (axis 3).
- Synthesis stays on the **parent** (whatever model you are). Never delegate the merge.

## Agent prompt template

Paste this, filling the three bracketed slots. The return contract is the part that
matters — without it agents hand back summaries, and a summary of a summary is unusable.

```
Search [CORPUS: exact paths / tool to use] for material about [CONCEPT].

Vocabulary to try — these are registers of the same idea, try all of them:
  [TERM_A], [TERM_B], [TERM_C]
Also try terms you discover in the corpus itself; the author may use none of mine.

Return contract — obey exactly:
- One entry per hit: `path:line` — then a VERBATIM quote (<=3 lines) — then one
  sentence on why it is relevant.
- Quote, never paraphrase. I need the author's own words.
- Max 12 entries, ranked most-relevant first.
- If you find nothing, say "NO HITS" and list the queries you tried. A negative
  result is a real finding; do not pad with weak matches to look productive.
- Do not summarize the corpus. Do not draw conclusions. Retrieval only.
```

Negative results are load-bearing: "the vault has no page on this" is the answer to
"did I ever write about X," and it is only trustworthy if the agent reports which
queries it ran.

## Synthesis

Agent output is raw material, never relayed. Follow `explaining-in-chunks`
(§ *Synthesizing agent output*): discard each agent's organization, re-group by what
the reader is trying to do, compress to load-bearing claim + citation, and lead with
the finding that changes the reader's actions.

Deduplicate across agents by `path:line`, not by wording — two agents quoting the
same paragraph through different queries is one finding, and the fact that it surfaced
twice is a relevance signal worth one clause.

## SilverBullet (`~/worklog`)

The local space is **plain `.md` files on disk**, served at `127.0.0.1:3030`. Agents
should hit the **filesystem with `rg`/`find`**, never the HTTP API and never `WebFetch` —
no server dependency, exact bytes, no SPA shell. (`/.fs` is only for *remote* spaces;
see the `silverbullet` skill.)

**Check size first — the vault is usually too small to fan out.** At ~20-30 pages,
reading every file costs less than briefing one agent:

```bash
find ~/worklog -name '*.md' -not -path '*/.*' | wc -l
find ~/worklog -name '*.md' -not -path '*/.*' -exec wc -c {} + | tail -1   # total prose bytes
```

At the time of writing that is **23 files / 48 KB** — the whole vault is one cheap read.
Fan out only above ~50 pages, or when also sweeping Glean/Drive in the same question.

**Never size the vault with `du -sh ~/worklog`, and always exclude dotdirs.** The folder
contains `.chrome-data` (a 145 MB Chrome profile), so `du` overstates the prose corpus by
~3000x and a bare `find ~/worklog -type f` walks an agent into binary profile data. Every
path filter below carries `-not -path '*/.*'` / `! -path '*/.*'` for that reason.

### Partitioning a vault

The vault has two natively different shapes, and they are the correct partition:

| Slice | Path | Character |
|---|---|---|
| Journal | `~/worklog/Journal/YYYY-MM-DD.md` | dated, chronological, terse, todo-heavy |
| Topic pages | `~/worklog/*.md` (root) | thematic, outlive the day, where method gets written down |
| Generated | `~/worklog/simtest/*.md`, `Calendar.md`, `CONFIG.md`, `index.md` | machine-written or config — usually exclude |

`index.md` and `CONFIG.md` are Space Lua widgets, not prose. Exclude them from
retrieval or agents will quote query templates as findings.

```bash
# journal-only agent
rg -li '<term>' ~/worklog/Journal/
# topic-pages-only agent (root, non-recursive)
rg -li '<term>' --max-depth 1 ~/worklog/
```

### `[[wikilinks]]` are the index — follow them

SilverBullet has no folder taxonomy; the graph *is* the organization, and Linked
Mentions gives reverse edges for free. Require every agent that reports a hit to also
report the page's edges:

```bash
rg -o '\[\[[^]]+\]\]' ~/worklog/Journal/2026-08-27.md   # outbound
rg -l 'failure-modes-aug27' ~/worklog/                   # inbound (Linked Mentions)
```

A journal entry is often just a link to the page that holds the real content — so an
un-followed hit in `Journal/` frequently means the answer is one hop away on a topic page.

### Frontmatter and tags

`tags:` is **space-separated bare words on one line** (`tags: worklog nvim`), and
inline `#hashtags` in the body are queryable the same way — so tag search needs both:

```bash
rg -N -e '^tags:.*\bdebug\b' -e '#debug' ~/worklog/
```

Not every page has frontmatter. Quick notes and same-day journal entries are often
bare prose, so **never filter the corpus by frontmatter presence** — you will silently
drop the newest, least-processed material, which is usually what the question is about.

### Attachments are invisible to `rg`

Screenshots (`~/worklog/*.png`) and other binaries hold real content that text search
cannot reach. When a hit's prose refers to a screenshot, surface the path so the parent
can `Read` the image:

```bash
find ~/worklog -type f ! -name '*.md' ! -path '*/.*'
```

### Writes serialize through the parent

**Fan-out is read-only.** Never let concurrent agents write to the vault: the server
watches the folder and pushes to open browsers, so two agents appending to the same
journal page race and one edit is lost. The parent performs all writes, after synthesis,
via `updating-worklog-vault`.

## When not to use this

| Instead | Skill |
|---|---|
| Searching the *web* for libraries/tools to build with | `program-ideation` |
| Cataloging local plan docs into a topic + chronological TOC | `index-plan-docs` |
| Writing the result into the vault | `updating-worklog-vault` |
| SilverBullet feature/config questions, docs and forum lookup | `silverbullet` |
| Delivering a long synthesis in chunks | `explaining-in-chunks` |
| Finding code, not documents | `Explore` agent directly |
