---
name: index-plan-docs
description: Index plan/design docs across a multi-submodule workspace into a topic-organized + chronological table of contents (e.g. alldocs/PLANS_TOC.md), with per-plan abstracts and a "Key changes" list. Use when the user wants to catalog, organize, or build an index of many planning docs scattered across submodules — or to refresh an existing plans TOC after new plans were added.
argument-hint: "[plans glob or workspace path] (defaults to */.docs_claude/plans/{active,completed}/)"
allowed-tools: Read, Write, Edit, Agent, Bash(find:*), Bash(git:*), Bash(sort:*), Bash(comm:*), Bash(awk:*), Bash(ls:*), Bash(grep:*), Bash(wc:*), Bash(cat:*)
---

# Index Plan Docs into a Topic + Chronological TOC

Catalog many planning/design docs (one `.md` per plan, scattered across submodules)
into a single browsable index organized two ways: **by topic** (each plan with a prose
abstract + a "Key changes" list of created/modified/deleted classes/functions/files) and
**chronologically** (most recent first, dated by git creation date). Output is a TOC file
plus durable maintenance instructions so the index stays current.

This is an **ensemble** task: a fan-out to brainstorm categories, a synthesis step you
own, then a second fan-out (one agent per topic) to assign + abstract. Every plan must
land under ≥1 topic — coverage is verified by a diff, not assumed.

## Core Recipe

### 1. Enumerate every plan (alldocs is symlinks → use `find -L`)

```bash
find -L . -path '*/.docs_claude/plans/*' -name '*.md' | sed 's|^\./||' | sort -u > /tmp/master.txt
wc -l /tmp/master.txt
```

### 2. Pass 1 — categorize (≈5 Explore agents over partitions)

Split `master.txt` into ~5 balanced partitions (by submodule, or contiguous chunks).
Launch the agents **in one message** (parallel). Each agent reads title + summary of its
plans and returns: (a) 6–12 proposed broad category names + one-line defs, (b) a dense
`path | one-line summary | code-touched | cats` table for every plan it saw.
Stitch all per-plan summaries into one `corpus_map.md` (path | summary, all plans) in a
scratch dir — it grounds pass 2.

### 3. Synthesize the shortlist (you, not an agent)

Collapse the agents' overlapping category proposals into **N topics** (typically 10–14).
Mix *purpose* (training, viz, refactor, HPO…) with *code section* (the owning submodule).
Overlap is allowed; aim for filterable buckets, not MECE. Keep a draft topic→plan
assignment from pass 1 as the seed + coverage seed.

### 4. Pass 2 — assign + abstract (N agents, one per topic, parallel)

Give each agent: its topic name + definition, the path to `corpus_map.md`, and a
candidate prior list. It judges every plan for membership (opening borderline ones),
and for each plan it keeps, reads the full doc and emits a ready-to-paste entry:

```markdown
### [<basename.md>](../<full/relative/path/from/workspace/root>)
`<dir-of-the-plan>/` · <YYYY-MM-DD>
> <2-4 sentence prose abstract: what it does, the approach, the outcome>
>
> **Key changes:**
> - `+ NewClass` — `path/to/file.py`
> - `~ existing_fn()` — `path/to/file.py`
> - `- DeletedThing` — `path`
```

Rules for the agents: link target is `../` + the corpus path (the TOC lives in
`alldocs/`); `+`/`~`/`-` = created/modified/deleted; pull **real** class/function/file
names from the plan, never invent (if a plan lacks code detail, list the modules it
touches); 4–8 bullets max; group entries by submodule. End each agent's output with a
plain `ACCEPTED_PATHS:` list for the coverage diff. A plan under several topics is
abstracted once and the entry reused.

### 5. Guarantee coverage (diff, don't trust)

```bash
sort -u /tmp/covered.txt > /tmp/covered_sorted.txt   # union of all ACCEPTED_PATHS
comm -23 /tmp/master.txt /tmp/covered_sorted.txt      # orphans: in master, no topic -> must be 0
comm -13 /tmp/master.txt /tmp/covered_sorted.txt      # bad paths an agent invented -> must be 0
```

Force-file any orphan under its best-fit topic (or add a new `## Topic`). Re-run until both
diffs are empty.

### 6. Chronological index (git creation date)

```bash
> /tmp/dates.txt
while IFS= read -r f; do
  sub="${f%%/*}"; rel="${f#*/}"
  created=$(git -C "$sub" log --diff-filter=A --follow --format=%as -- "$rel" 2>/dev/null | tail -1)
  [ -z "$created" ] && created=$(date -r "$f" +%F)   # uncommitted -> file mtime / today
  printf '%s\t%s\n' "$created" "$f" >> /tmp/dates.txt
done < /tmp/master.txt

sort -r /tmp/dates.txt | awk -F'\t' '{p=$2; n=split(p,a,"/"); \
  printf "- **%s** — [%s](../%s) `%s`\n", $1, a[n], p, a[1]}' > /tmp/chrono.md
```

### 7. Emit the three artifacts

1. **`alldocs/PLANS_TOC.md`** (lives beside the symlink aggregation dir): a maintenance
   header, then the **Chronological index** section (`/tmp/chrono.md`), then the **N topic
   sections** (`## 1. Topic` … with the `###` entries from pass 2). Build it incrementally
   with `cat >> file <<'EOF'` heredocs (quoted delimiter so backticks stay literal) —
   one topic per append keeps each step small.
2. **Meta-repo root `CLAUDE.md`** — a "Maintaining alldocs/PLANS_TOC.md" section (the same
   text as the TOC header) so future sessions keep it current.
3. **A memory** (`memory/plans-toc-index.md`, type `reference`) + a one-line `MEMORY.md`
   pointer recording where the index lives and how it's maintained.

### Verify

```bash
grep -oP '\]\(\K\.\./[^)]+\.md' alldocs/PLANS_TOC.md | sort -u | while read r; do
  [ -f "alldocs/$r" ] || echo "BROKEN: $r"; done        # 0 broken links
grep -oP '\]\(\K\.\./[^)]+\.md' alldocs/PLANS_TOC.md | sort -u | wc -l   # == plan count
awk '/^### /{h=$0;f=0;for(i=0;i<10;i++){getline l;if(l~/Key changes/){f=1;break}}if(!f)print "NO KEYCHANGES "h}' alldocs/PLANS_TOC.md
```

## Maintenance block to embed (TOC header + CLAUDE.md)

```markdown
## Maintaining alldocs/PLANS_TOC.md
When a plan is added, copied, moved, renamed, or deleted:
1. Find it: `find -L . -path '*/.docs_claude/plans/*' -name '*.md'` (alldocs is symlinks — use -L / rg --follow).
2. Read its title + summary to judge purpose and the code section it touches.
3. Add an entry (### link + code-location line + 2-4 sentence abstract + "Key changes" +/~/- list)
   under EVERY matching topic. A plan MUST appear under ≥1 topic; never drop it; new topic if none fit.
4. On move/rename/delete, update or remove the existing entry/entries.
5. Keep topic order stable; group plans by submodule within a topic.
6. Add it to the Chronological index too — date = git creation date
   (`git -C <sub> log --diff-filter=A --follow --format=%as -- <rel> | tail -1`); re-sort most-recent first.
```

## When Applying This Skill

1. **Confirm two decisions up front** (AskUserQuestion if unclear): where the TOC file
   lives (default `alldocs/PLANS_TOC.md`) and where maintenance instructions go (default:
   create/extend the meta-repo root `CLAUDE.md`).
2. **Scale the fan-out to corpus size.** ~5 categorizers is right for ~100–150 plans;
   shrink for fewer. N topics ≈ 10–14 for ~120 plans.
3. **You own the synthesis** (step 3) — the topic shortlist is your judgment call, not an
   agent's. Don't delegate it.
4. **Ground pass 2 with the corpus map** so topic agents judge cheaply and only deep-read
   the plans they claim.
5. **Coverage is a diff, not a vibe** — never declare done until `comm -23` is empty.
6. **Dates are git creation dates** by default (when the plan was authored). Offer
   last-modified instead if the user wants "recently touched" ordering.
7. **Don't invent code symbols** in Key changes — agents must pull real names from the
   plan or fall back to listing touched files/modules.
8. **Append the TOC in small batches** (heredoc per topic) to stay within output limits on
   large corpora.
