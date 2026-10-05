---
name: content-access
description: "Locates accessible copies of paywalled, removed, or hard-to-find published material using Unpaywall, CORE, Semantic Scholar, library databases, and equivalent open-access routes — giving journalists and researchers a structured search path that stays within ethical and legal boundaries."
status: stable
category: research
subcategory: preservation
version: 1.0
eval_score: 4.96
tags: [journalism, research, open-access, paywalls, Unpaywall, Semantic-Scholar, CORE, libraries]
---
# Content access

## What this skill does
Locates accessible copies of paywalled, removed, or hard-to-find published material using Unpaywall, CORE, Semantic Scholar, library databases, and equivalent open-access routes — giving journalists and researchers a structured search path that stays within ethical and legal boundaries.

## When to use this skill
- You need to read a journal article, report, or study but it is behind a paywall and your organisation does not have a subscription
- A web page or document has been deleted and you need to find a cached or archived copy
- You are looking for a government report, white paper, or technical document that is no longer on the original publisher's site
- You want to check whether an open-access version of a paywalled paper exists before paying for it or requesting it through other channels

## What you need to provide
**Required:** What you are looking for — a specific article (title, author, DOI, or URL), a type of document (government report, industry white paper, conference paper), or a description of the content you need
**Optional:** Where you already looked and what you found (avoids duplicating effort); whether you have library access through an institution; the urgency (same-day need vs. background research); whether the material has been recently deleted (triggers archive-search steps)

## How the Assistant Approaches This
1. **Identifies the material type** and selects the search path accordingly. Academic papers, government reports, industry publications, and news articles each have different open-access routes.

2. **For academic papers and journal articles:**
   - **Unpaywall** (unpaywall.org): Browser extension and API that finds legal open-access versions of journal articles using their DOI. Checks publisher-hosted open access, institutional repositories, and preprint servers. First stop for any DOI-identified paper.
   - **Semantic Scholar** (semanticscholar.org): Academic search engine that links to open-access PDFs when available, shows citing and cited papers (useful for finding the full version when only an abstract is indexed), and provides paper summaries.
   - **CORE** (core.ac.uk): Aggregates open-access content from institutional repositories worldwide. Often has versions that Unpaywall misses, particularly from European universities.
   - **PubMed Central** (ncbi.nlm.nih.gov/pmc): For biomedical and life-sciences papers. Many US-government-funded studies are required to be deposited here within 12 months of publication.
   - **Preprint servers**: arXiv (physics, maths, computer science), bioRxiv/medRxiv (biology, medicine), SSRN (social sciences, law, economics). Preprints are the author's version before peer review — they may differ from the final published version. Note this clearly when citing.
   - **Author's personal or institutional page**: Many researchers post PDFs of their published papers on their university profile page or personal website. A web search for the paper title plus the author's name often finds these.
   - **Interlibrary loan**: If no open-access version exists and the user has access to a library (public, university, or newsroom), interlibrary loan can obtain almost any published paper. Takes days, not hours.

3. **For government reports and policy documents:**
   - **Government archives**: Many countries maintain permanent digital archives of government publications (e.g., govinfo.gov for US federal documents, EUR-Lex for EU legislation, data.gov.uk for UK government).
   - **Wayback Machine**: Government pages that have been reorganised, moved, or deleted during administration changes are often preserved. Search by URL or by keyword on web.archive.org.
   - **Google Cache**: For recently removed pages, Google's cached version may still be available. Search for the URL or title and click "Cached" if the option appears. This is temporary — Google refreshes its cache.
   - **Document repositories**: Internet Archive's document collection, HathiTrust for digitised library materials, and the Digital Public Library of America for US cultural heritage documents.

4. **For news articles behind paywalls:**
   - **Archive.today**: Often captures articles from major news outlets including their full text. Search by URL.
   - **Library databases**: Many public libraries provide digital access to newspaper archives (ProQuest, Nexis, PressReader). A library card — often free — is all that is needed.
   - **Publisher's own open archive**: Some outlets make articles free after a time embargo (30 days, 12 months). Check the publication's access policy.

5. **For deleted or removed content of any type:**
   - **Wayback Machine** and **Archive.today** first (see web-archiving skill for detailed method).
   - **Google Cache** for recently removed material.
   - **Common Crawl** (commoncrawl.org) for bulk web data that may include the target page.
   - If nothing is found in archives: the material may be genuinely gone from the public web. Note this — the absence itself may be newsworthy.

6. **Ethical and legal framing.** Every recommendation stays within legal boundaries. The skill does not guide users toward copyright infringement, credential sharing, or circumvention of access controls. It notes where the line is: using a preprint is legal; downloading a paper from an unauthorised repository is a different legal and ethical question. For news articles, accessing through a library database is fine; screen-scraping a paywall is not recommended.

## Output format
A search path: numbered steps from most likely to succeed to least likely, tailored to the specific material type. Each step names the tool or resource, explains how to search it, and notes what to expect. Closes with a brief note on what to do if nothing is found. Total length: 300–600 words. Practical register — this is a search procedure, not a review of open-access infrastructure.

## Quality criteria
- [ ] Search path is ordered from highest probability of success to lowest, not listed alphabetically or randomly
- [ ] Every tool or resource named is real, currently operational, and correctly described
- [ ] Search instructions are specific enough to follow — not "check Unpaywall" but "install the Unpaywall browser extension or search unpaywall.org/[DOI]"
- [ ] The distinction between preprints and published versions is noted when preprint servers are recommended
- [ ] Ethical and legal boundaries are stated clearly without being preachy
- [ ] Library access is mentioned as an option, including free public library cards
- [ ] Output is free of generic AI-template phrasing — no "delve into," "navigate the complexities of," Latinate filler verbs, restate-the-question intros, summary-of-the-summary closes, or em-dash overuse

## Example

### Input
Looking for: "The effect of microplastic contamination on freshwater invertebrate populations: a meta-analysis" by Torres et al., published in Environmental Science & Technology, 2024. DOI: 10.1021/acs.est.2024.xxxxx. I need the full text for a feature on microplastics in drinking water. My newsroom does not have a journal subscription. Same-day need.

### Output

**Search path**

1. **Unpaywall (first stop).** Go to unpaywall.org and search the DOI: `10.1021/acs.est.2024.xxxxx`. Unpaywall will check whether the publisher has an open-access version, whether the authors deposited a copy in an institutional repository, or whether a preprint exists. If it finds an open-access PDF, you are done. Environmental Science & Technology is an ACS journal — ACS has some open-access articles, but most are paywalled. Likelihood: moderate.

2. **Semantic Scholar.** Search the title at semanticscholar.org. If an open-access PDF is indexed, there will be a green "PDF" button next to the result. Semantic Scholar also shows which papers cite this one and which papers it cites — useful if the meta-analysis references studies you also need. Likelihood: moderate.

3. **CORE.** Search core.ac.uk for the title or DOI. CORE aggregates from institutional repositories across Europe and beyond. If any of the Torres et al. co-authors are at a university that mandates open-access deposit, CORE may have their accepted manuscript. Likelihood: moderate for a multi-author international study.

4. **PubMed Central.** Search ncbi.nlm.nih.gov/pmc for the title. If any author received US federal funding (NIH, NSF, EPA), the NIH public-access policy requires deposit in PMC within 12 months of publication. Environmental research often has federal funding. Likelihood: moderate to good if US co-authors are involved.

5. **Author's institutional page.** Search the lead author's name + university. Many environmental scientists post accepted manuscripts on their lab or department page. If you find a PDF labelled "accepted manuscript" or "postprint," this is the peer-reviewed version without the journal's formatting — legally shared by the author under most publisher agreements. Note that it may differ slightly from the typeset version.

6. **Preprint servers.** Check ChemRxiv (chemrxiv.org — the American Chemical Society's preprint server) and EarthArXiv for an earlier version. A preprint may differ from the final published meta-analysis — results or conclusions could have changed during peer review. If you cite a preprint, note that it is not the peer-reviewed version.

7. **Public library.** If none of the above produced the full text: check whether your local public library provides access to ACS journals through a database like ProQuest or EBSCO. Many public libraries in major cities offer free digital access to academic databases with a library card. This takes longer than steps 1–6 but almost always works.

**If nothing is found:** Contact the corresponding author directly by email. Most researchers will send a PDF of their own paper on request — this is common practice and not a copyright violation. A brief, professional email explaining that you are a journalist writing about microplastics and would appreciate a copy is usually enough.

## Known limitations
- This skill finds legal, openly accessible copies. It does not guide users to pirate repositories or circumvent digital rights management systems.
- Open-access availability depends on the publisher's policies, the authors' funding mandates, and whether anyone deposited a copy. Not every paper has a free version.
- Preprints are not the same as the final published version. Differences in data, analysis, or conclusions between the preprint and the published version can be significant, especially for meta-analyses. Always check which version you are reading.
- Library access varies widely. Large urban public libraries and university libraries offer extensive database access. Smaller or rural libraries may have limited digital subscriptions.
- Cached and archived copies of removed content may themselves be removed. Google Cache is temporary. Wayback Machine and Archive.today have honoured takedown requests in the past. Preservation is not permanent.

## Related skills
- [web-archiving](../web-archiving/SKILL.md)
- [page-monitoring](../page-monitoring/SKILL.md)
- [scientific-paper-summarizer](../../academic/scientific-paper-summarizer/SKILL.md)
