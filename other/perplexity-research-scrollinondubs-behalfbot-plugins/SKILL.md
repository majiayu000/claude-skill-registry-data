---
name: perplexity-research
description: End-to-end pipeline turning a research question into a peer-reviewed, citation-solid .epub brief. Fast path is the brief alone; deep path appends the full text of every cited article. Use whenever someone asks to research a topic, brief them on something, get the science on a claim, or flags a full download.
---

# Skill: Perplexity research to .epub brief

Turn a research question into a citation-solid brief that reads well offline.
Covers the fast path (brief only) and the deep path (brief plus a full-text
appendix of the cited articles).

## Trigger

A request for research on a topic, or a revision of a prior brief. Phrases like
"research X", "get me the science on Y", "pull citations for Z", "brief me on
...", or a reference to reading it on an e-reader.

If the request contains "full download", "deep dive", "append the articles",
"with the papers", or similar, use the **deep path** (section 6). Otherwise the
**fast path** (sections 1-5) is enough.

## 1. Prep

1. Check memory for `topic:<slug>`. If this topic has come up before, read the prior notes first. Do not re-run research that already exists.
2. Make sure the browser session is open and signed in to the research UI at `research_ui_url`. If it is not, navigate there and ask the operator to complete sign-in. Browser automation does not persist auth across launches, so expect to ask once per session. An unauthenticated session does not error - it silently returns a thinner free-tier answer with fewer sources, which is the worse failure because it looks like success.
3. Budget it. One full brief is 4-6 queries plus an epub build. The deep path adds a scrape per cited article on top.

## 2. Query design

Aim for `queries_per_brief` focused queries, each of which has to carry a
defensible citation on its own. One query becomes one section of the brief.
Good queries name the effect, the method and the population the way researchers
phrase their own paper titles.

Bad: "is nature good for you"
Good: "nature exposure cortisol reduction randomized controlled trial meta-analysis"

A typical query set for a health or science brief:

1. Biological or immunological mechanism
2. Hormonal or stress markers
3. Psychological outcomes - prefer meta-analyses and RCTs with n >= 30
4. Neurological or imaging evidence
5. Dose-response or practical threshold
6. The anchoring canonical paper, named by author, year and journal - this gets you the citation the audience already knows

For non-scientific topics (history, business, technology), substitute: landscape
scan, contrarian angle, canonical source, recency check.

## 3. Running the queries

Append the configured `source_filter` to the search URL rather than clicking the
filter in the UI - it loads server-side and skips a round of DOM interaction.

Per query:

```
# 1. Navigate straight to the results page
browser_navigate
  url: <research_ui_url>/search/new?q=<url-encoded-query>&sources=<source_filter>

# 2. Wait for sources to render
browser_wait_for  text: "sources"  time: 20

# 3. Grab the answer text AND click the "N sources" button to expand citations
browser_evaluate
  function: () => {
    const text = (document.querySelector('main')||document.body).innerText.slice(0,6000);
    const btn = Array.from(document.querySelectorAll('button'))
      .find(b => /\d+\s*sources?$/i.test((b.innerText||'').trim()));
    if (btn) btn.click();
    return text;
  }
  filename: <scratch_dir>/qN-text.json

# 4. Once the sources panel is open, pull the citation URLs
browser_evaluate
  function: () => Array.from(document.querySelectorAll('a[href]'))
    .map(a => ({h: a.href, t: (a.innerText||'').slice(0,250).trim()}))
    .filter(l => l.h.startsWith('http'))
    .slice(0, 30)
  filename: <scratch_dir>/qN-srcs.json
```

Why this shape: the accessibility tree elides full citation URLs in the initial
render, showing only domain fragments. The real hrefs live on the raw anchors,
and those anchors only exist after the sources panel expands. Evaluating the
page directly is several times cheaper in tokens than snapshotting it.

**Write the scratch dumps to `scratch_dir`, not to the working directory.** The
browser tool writes `filename` outputs wherever it is pointed, and pointing it
at "here" is how a repo ends up with `q1-srcs.json` committed. Delete them in
section 8.

## 4. Synthesize the brief

Save to `<output_dir>/YYYY-MM-DD-<slug>-research.md` with YAML frontmatter so
the build step picks up metadata:

```markdown
---
title: "<Human-readable title>"
author: "<author_line>"
date: "YYYY-MM-DD"
subject: "<one-line topic>"
lang: "<language>"
---

# <Title>

## 1. <Section>

<prose with inline citations as markdown links>
```

Brief-quality rules:

- **Lead with honest nuance, not hype.** If the evidence is mixed, say so in the first paragraph of the affected section. Naming a disputed finding is the single biggest credibility move available. Getting caught out on a weak claim in front of a smart audience is far worse than having admitted the uncertainty up front.
- **Prefer meta-analyses and RCTs with n >= 30.** Flag anything smaller explicitly. Never let a tiny study carry a load-bearing claim - a memorable n=12 result is exactly the kind of thing a brief smuggles in and an audience catches.
- **Swap list.** When revising a prior brief, include a "Drop / Replace with" table so the diff is obvious at a glance.
- **Source summary table at the end.** Columns: #, Study, Design, N, Year, Use for. This is what someone scans to pick which citation to quote.
- **No em dashes.** Use " - " (space-dash-space). The build script warns if any survive.
- **Every claim carries a DOI or publisher link inline**, not just a bibliography at the end.

## 5. Build and deliver

```bash
bash "$RESEARCH_BUILD_SCRIPT" "<output_dir>/YYYY-MM-DD-<slug>-research.md"
```

The script reads title, author and date from the frontmatter, falls back to the
configured `author_line`, builds with a table of contents, warns on em dashes,
warns if the output is implausibly small, and prints the epub path on stdout.
Expect 10-50KB for a fast-path brief and 100KB-2MB for a deep-path one.

Then deliver to each configured target in `delivery_targets`:

- **`file`** - report the path and stop. The brief is on disk.
- **`chat`** - post to `delivery_channel_id` with the epub attached. If that id is unset, say so and stop; do not fall back to another channel. A research brief posted into the wrong room is not a small mistake. When `brief_base_url` is set, include the direct link alongside the attachment so the brief survives a flaky mobile download.
- **`ereader`** - run `ereader_send_command` with the epub path as its argument. Report the exit code honestly. Installs running the companion reMarkable plugin point this at its send script.

In the chat message body: say what the brief does and does NOT support, flag any
disputed claim, and name the canonical citations by author-year.

## 6. Deep path - full-text appendix

When the request flags "full download" or one of the section-1 phrases, run the
fast path first, then append the full article text.

For each cited URL in the Source Summary table, scrape to markdown, main content
only.

Fallback chain when the scrape cannot fetch:

1. **Hard paywall:** try a PubMed Central mirror if one exists (`https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/`) - most journals post an open-access version 6-12 months after publication. Also try the DOI resolver, `https://doi.org/<doi>`.
2. **Bot detection or 403:** switch to the browser session on the same URL. A signed-in human-shaped session carries fewer bot fingerprints than a scraping pool.
3. **PDF returned garbled:** download it and run `pdftotext -layout <file> -`. Works on most preprint-server and open-access journal PDFs.
4. **Abstract only:** include the abstract plus an explicit `**Full text behind paywall at <link>.**` note. An abstract still has offline value.
5. **Still blocked:** note the failure in the appendix entry (`Full text not retrievable - <reason>. DOI: <doi>`) and move on. Do not fabricate content. Do not summarize an article you could not read.

### Size gate, before the fetch loop

Estimate roughly 300 KB per open-access paper and 150 KB per scraped HTML
article. If the projection exceeds `deep_path_warn_mb`, warn the operator with
the expected size and ask whether to (a) proceed with one file, (b) split into
two epubs so the brief stays light, or (c) drop the deep path. Above
`deep_path_split_mb`, default to (b).

E-reader software chokes on very large single files, and splitting is cheap
insurance.

### Appendix shape

Many e-readers do not follow hyperlinks inside an epub, so an in-text citation
needs both a link (for desktop readers) and a plain-text section marker (for the
device):

```
Andersen et al. 2021 systematic review ([DOI](https://doi.org/...) - see Appendix §A3).
```

Number appendix sections `§A1`, `§A2`, matching `## A1.`, `## A2.` headings.

```markdown
# Appendix - Full Article Text

## A1. <Author year> - <Title>

**DOI / Source:** <link>
**Retrieved via:** scrape | browser | PMC mirror | pdftotext | abstract-only | failed
**Retrieved at:** YYYY-MM-DD HH:MM

<full markdown body, or the abstract plus the paywall note>

---
```

Rebuild the epub with the same command; the file grows proportionally.

## 7. Cleanup

- Delete the scratch dumps in `scratch_dir`.
- Write a `topic:<slug>` memory: date, queries run, top three citations, the mixed-evidence caveat if there is one, and the path to the brief markdown.

## 8. Anti-patterns

- **Do not take the research UI's answer at face value on citation claims.** It occasionally gets author names and dates wrong. Verify the DOI or publisher URL supports the claim before the claim goes in the brief.
- **Do not drop the honest-nuance paragraph to make the brief tidier.** It is the most load-bearing paragraph in the document.
- **Do not attach a very large deep-path epub without warning first.** Split it.
- **Do not post to a chat channel whose id is unset.** Fail loudly instead.
- **Do not fabricate an appendix entry.** "Not retrievable" is a real, useful result. An invented summary is not.
