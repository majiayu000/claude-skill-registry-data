---
name: litreview
description: Find and synthesize the literature on a topic or research question, returning a ranked reading list with a takeaway per paper. TRIGGER on "lit review", "find papers on X", "what is the literature on Y", "recent work on Z", "who has studied W", "find references for my intro", or a topic plus a scope phrase ("since 2022", "Marketing Science only"). One paper the user already has is reading-papers.
allowed-tools: Read, Write, Bash, Agent, Monitor, mcp__zotero__zotero_search_items, mcp__zotero__zotero_advanced_search, mcp__zotero__zotero_get_item_metadata
---

# litreview

Turn a topic into a ranked, deduped, honestly-scoped reading list, with a one-paragraph takeaway
per paper and a synthesis of what the cluster says. The output is what the user reads before
deciding what to cite.

## Boundary with reading-papers

This skill starts from a question and ends with a set of papers. The `reading-papers` skill starts
from one known paper and ends with its text. If the user hands over a DOI, a link, a title, or an
author name and wants that thing read, stop here and use `reading-papers`.

The two share machinery. Discovery here is `paper.py search`, reading here is `paper.py get`, and
both live in the `reading-papers` skill directory. Read
`~/.claude/skills/reading-papers/SKILL.md` before the reading phase if you have not
already; it owns the access ladder and the honesty rules that apply to every summary this skill
emits.

## Scope the question first

A one-word topic gives a one-word answer. Before searching, pin down the actual question and the
year window if the user implied one. Ask if the request is bare ("do a lit review"). Do not guess
a topic.

Scope phrases in the request map onto flags without the user having to type them: "since 2022" is
`--since 2022`, "Marketing Science only" is `--venue "Marketing Science"`, "top 30" is `-n 30`,
"recent" with no year is the last five years, and say that you read it that way.

## Step 1: search

```bash
~/.claude/skills/reading-papers/scripts/paper.py search "<topic>" -n 25 --json
```

Flags: `--venue "<journal>"`, `--since YYYY`, `--until YYYY`, `-n N`, `--json`.

One invocation runs one query against Semantic Scholar, OpenAlex, and arXiv, merges the three on
DOI, then arXiv id, then normalized title, and re-ranks by reciprocal-rank fusion. Use `--json`
whenever you are going to process the results (it carries abstracts, which is what scoring runs
on); the plain text form is for showing the user.

Write two or three query strings, not one. Strip filler, keep substantive nouns, expand acronyms
(DiD becomes "difference-in-differences"), and vary the vocabulary across fields: economists write
"algorithmic collusion", computer scientists write "multi-agent reinforcement learning pricing".
Run the variants as parallel Bash calls in a single message.

The JSON shape:

```json
{"query": "...",
 "sources": {"openalex": {"ok": true, "hits": 25, "note": null},
             "semanticscholar": {"ok": true, "hits": 25, "note": null},
             "arxiv": {"ok": false, "hits": 0, "note": "no response (rate limit or network)"}},
 "unique": 41,
 "results": [{"title": "...", "authors": [...], "year": 2020, "venue": "...",
              "doi": "...", "arxiv_id": "...", "abstract": "...",
              "is_oa": true, "best_url": "...",
              "cited_by": 579, "cited_by_source": "openalex",
              "citations": {"openalex": 579, "semanticscholar": 612},
              "sources": ["openalex", "semanticscholar"], "rrf": 0.03}]}
```

Read `sources` before reading `results`. A source with `"ok": false` means that slice of the
literature is missing from this run, and which slice depends on which source dropped: OpenAlex
carries the marketing and economics journals, Semantic Scholar carries citation counts and CS
venues, arXiv carries anything from the last few months. Name any failed source in the output so
the user knows the list is partial.

`citations` holds every count the sources returned and they disagree, often by a lot. Quote
`cited_by` with `cited_by_source` next to it and never mix sources down one column.

## Step 2: merge across query variants

Each invocation dedupes its own results only. Merging across variants is your job, on the same
ladder the script uses: DOI, then arXiv id, then normalized title (lowercase, punctuation to
spaces, compare token sets). Keep the union of `sources` and the higher `rrf` when a paper appears
under two queries; that agreement is a signal it is central.

Workshop and journal versions of one paper are near-duplicates that are not duplicates. Keep both,
cite the version of record, and mark the older one as superseded by the entry number of the newer.

## Step 3: check Zotero before fetching anything

The user's own library is faster than any API and holds their annotations. For each deduped
candidate, call
`mcp__zotero__zotero_search_items(query="<short title>", qmode="titleCreatorYear", limit=3)` and
mark hits `[in Zotero: <key>]`. Prefer their copy over re-fetching, and route the reading subagent
to the Zotero item when one exists.

Zotero reads only work while the Zotero 7 desktop app is open with the local API enabled. A failed
call almost always means the app is closed. If it is, skip the check and do not report papers as
absent from the library: a closed Zotero looks exactly like an empty one.

Say so explicitly at the top of the reply, not in a footnote: Zotero looks closed, open the Zotero
desktop app and this can be re-run to flag what is already in the library. It is a five-second fix
and the user would rather be told than get a silently degraded result. Carry on with the search
either way; nothing else here needs Zotero.

## Step 4: score relevance, 1 to 5

One score per paper, against the user's stated question, from title, abstract, venue, and year.
This is the only score in this skill. Anything else worth saying about a paper (how good the
identification is, whether it is superseded, whether the venue is serious) goes in the takeaway as
prose.

- 5: directly on the question, would be cited in the intro of a paper about it.
- 4: closely related, will be cited somewhere in the paper.
- 3: adjacent, worth knowing about, might appear in a robustness or related-work paragraph.
- 2: tangential, mention only if the user asks for breadth.
- 1: false positive, drop it before output.

Score honestly and let the count fall where it falls. If six papers clear 3, return six. A padded
list of 25 costs the user more time than it saves.

Score a paywalled paper from its abstract, mark it `read: abstract only`, and write nothing about
it that implies you saw the body.

## Step 5: read the top hits in parallel

Reading is where the value is, and the reading-papers skill documents the pattern: one subagent per
paper, structured summary back. A fan-out of a dozen concurrent readers is safe here because every
API call retries with backoff, responses are disk-cached for 30 days, and the keys are configured.
Keep concurrency near four to six when most hits are arXiv preprints, since arXiv politeness is one
request per three seconds.

Read the papers scoring 4 and 5, capped at twelve by default. Ask before going past that. Hand each
subagent an identifier, never a title: a DOI or arXiv id costs 1 OpenAlex credit, a title costs 10.
Launch every reader with the `Agent` tool. While the readers run, write the
`Paper/litreview-<slug>.tex` skeleton from the search metadata (header line, doi, cited_by, sources,
Zotero key) and fill each block's takeaway lines as its summary arrives.

Subagent prompt template:

```
Read one paper and return a structured summary. Do not read anything else.

Paper: <doi or arXiv id>       Question it is being read against: <the user's question>
Tool: ~/.claude/skills/reading-papers/scripts/paper.py
Follow ~/.claude/skills/reading-papers/SKILL.md for the access ladder.

  paper.py get "<id>" --list-sections     # map first, always
  paper.py get "<id>" --section "<substr>" # then pull only what you need

--list-sections then --section is the context saver on long papers: a 70K-character paper
becomes a 10K-character section with equations and cross-references intact. Read the abstract
and introduction, then the sections that bear on the question above. Do not dump full text.
Section slicing needs an arXiv e-print. When the paper has none, the script says so and hands
back a PDF path or HTML; read that with the Read tool and skip the section step.
If it is already in Zotero (<key>, when given), read the user's copy and their annotations.

Return exactly:
  id:            <doi or arXiv id>
  version_read:  published | arXiv preprint | NBER working paper | abstract only
  source_rung:   <the `source:` line paper.py printed>
  question:      <one sentence: what the paper asks>
  setting/data:  <one sentence>
  method:        <short phrase: RCT, DiD, RDD, structural, simulation, observational, theory>
  finding:       <one or two sentences, with the number that matters>
  bears_on:      <one or two sentences: how it speaks to the question above>
  limits:        <one sentence, the honest caveat a referee would raise>
  quote:         <verbatim, 25 words max, with its section name, or none>
  bibtex:        <a complete, ready-to-use BibTeX entry, key <lastname><year><firsttitleword>>

Build the BibTeX from the metadata paper.py returned, or from the Zotero item when there is one.
Never write one from memory: a fabricated year, volume, or page range is the failure mode this
whole pipeline exists to avoid. Fill author, title, year, journal or booktitle, volume, number,
pages, and doi, and leave a field out rather than guess it.

If no free full text is reachable, say so plainly, set version_read to `abstract only`, and
return what the abstract supports. Never paraphrase an abstract as if you read the paper.
```

## Step 6: output

The deliverable is two files in the current project's `Paper/` folder, created if it is absent. If
the request carries no project context, ask for the path and write nothing until you have it.

`Paper/litreview-<slug>.tex` holds the ranked list. Order by score descending, then year
descending, one block per paper:

```latex
\subsection*{[1] score 5, 2020, Calvano, Calzolari, Denicolò, Pastorello}
Artificial Intelligence, Algorithmic Pricing, and Collusion. \emph{American Economic Review}.
\texttt{doi:10.1257/aer.20190623}, cited\_by 579 (OpenAlex), found in openalex and
semanticscholar. Cite as \verb|\citep{calvano2020artificial}|.

Takeaway: Q-learning agents in a repeated Bertrand duopoly converge to supracompetitive prices
with no communication and no instruction to collude.

Bears on the question: the canonical simulation result that field evidence has to beat.

Method: agent-based simulation. Read: published version, arXiv HTML rung.
Free copy: \url{https://art.torvergata.it/.../aer.20190623.pdf}. In Zotero: 8KQ2M4TR.
```

Report a source in indirect speech. Wording kept from a paper goes inside quotation marks and
italics, formatted *"like this"*, with the page or section it came from, and the rule holds in the
`.tex`, in the chat reply, in a reader subagent's report, and in any `note` field written into
`references.bib`. A takeaway that reuses an author's sentence without those marks becomes
plagiarism the moment the review reaches a draft.

<example>
<user>find the recent work on how shoppers react to personalized pricing and tell me where it splits</user>
<response>
[paper.py search: personalized pricing consumer fairness perceptions]
[mcp__zotero__zotero_search_items: personalized pricing backlash]
[paper.py get --section: "Discussion"]
Both papers estimate what happens when a shopper learns the price was set for them individually,
and both measure a fall in repurchase of roughly the same size. They part on the mechanism. Aurand
and Petrov (2024) read it as a fairness violation and find the effect disappears once the retailer
states the rule behind the discount. Halloran (2023) reads the same drop as inferred exploitation
and finds that disclosure makes things worse among high-spend customers, calling it *"a signal of
how much the firm already knows"* (Section 5.2). Disclosure is the treatment that separates the two
accounts, and neither paper has run it on the other's population.
</response>
<rationale>CORRECT: The comparison is built around the finding the two papers share and the mechanism they dispute, in the assistant's own indirect speech. Exactly one short phrase is kept from Halloran, marked and italicized with its section number, and every other claim is reworded. The takeaway stays specific enough to act on.</rationale>
</example>

The same file closes with two things. A synthesis of four to six sentences covering what the
cluster agrees on, where it splits into camps (a split is where a new paper can position itself),
what is missing, and which two or three papers to read first if the user reads nothing else. Then a
coverage line: which sources answered, which failed, which venues were unreadable, and what the
user would have to do to close each gap.

`Paper/references.bib` gets the `bibtex:` field every reader returned, one entry per paper in the
list, verbatim. Append to an existing `references.bib` and match the key style already in it. Never
rewrite an entry that is already there.

The chat reply carries the two paths, the ranked list, and anything the user has to act on now
(Zotero looked closed, a source failed). Takeaways, the synthesis, and the coverage line live in
the `.tex` and are not repeated in chat.

Stop there. Ask before adding anything to Zotero; writes need the web key and the user did not ask
for a library edit unless they said so.

## Coverage limits and cost

Which venues are hard-blocked, the escalation ladder for a paywalled paper, and the OpenAlex credit
prices are all in `~/.claude/skills/reading-papers/SKILL.md`. Name in the output every
venue this run could not reach. One rule is specific to searching rather than reading: INFORMS and
SAGE own marketing, so run a `--venue` pass over Marketing Science, JMR, JCR, Journal of Marketing,
and Management Science alongside the open topic search. A marketing review that comes back all
arXiv is a failed search, not a thin field.

## Failure modes

Zero results: relax once, in this order, dropping `--venue`, then `--since`, then shortening the
query to its two strongest nouns. If it is still empty, say what was tried and ask for a seed paper.

One source down: the `sources` block names it. Continue with the others and report the gap.

Every source down: a network or rate-limit problem, not an empty literature. Retry once after a
pause, then say so.

A seed paper instead of a topic: resolve it first with `paper.py resolve`, then expand with
`paper.py cites "<doi>"` for forward and backward citations, and run the topic search on its title
keywords. Include the seed in the output at score 5.

Results dominated by one subfield: the query is inheriting that field's vocabulary. Rewrite it in
another field's terms and merge.

## Out of scope

Writing the lit review prose. This skill returns the ranked material.

PRISMA-style systematic review with inclusion logs and screening counts. This is fast discovery
plus a read, and it makes no claim to exhaustiveness.

Adding papers to Zotero unless the user asks.

Inventing a citation. If nothing turns up, the answer is that nothing turned up.
