---
name: mathodology-evidence-search
description: Use when finding literature, datasets, domain facts, citation details or licensed figure references.
---

# Mathodology Evidence Search

Use evidence to support a claim or model choice. Prefer primary work and official
data. Mark assumptions and unresolved gaps; never fill them with invented facts.

## Search and read

Inspect available tools. Normally combine built-in WebSearch with
`mcp__search__search`: complementary discovery queries can find different sources.
Record which channels actually contributed. If a channel is unavailable, continue
with the working one and note the coverage limitation; an unavailable search is
not evidence that a source does not exist. With no search, work from supplied
material and state which external claims remain unverified.

The project `.mcp.json` registers the keyless
[free-search-mcp](https://github.com/sweetcornna/free-search-mcp) server and a staged
download directory. Tool signatures vary by installed version: read the live
schema instead of assuming the argument names in an old example.

| Capability | Appropriate use |
|---|---|
| search / research | Focused discovery / an open research question |
| cache_search | Reuse material already read |
| fetch / fetch_batch | Read shortlisted web pages |
| read_doc | Read PDF and structured or office documents, with pagination |
| extract_structured | Confirm publisher metadata such as DOI and title |
| compare | Reconcile conflicting sources or definitions |
| paper_graph | Explore prior work and check available correction/retraction notices |
| download | Retain a file needed for reproduction or a licensed reference |
| engines | Diagnose thin results or unavailable sources |

Use the narrowest category the live tool exposes. Typical groups include `paper`
(with index, preprint, biomed, cs, openaccess, trial and math subgroups), `dataset`
(repository, ml, gov), `news`, `finance`, `github`, `forum` and `image`. Subgroup
availability depends on the server. A general web domain filter is not equivalent
to a bibliographic search. Do not silently treat a blocked engine as an empty corpus.

Merge results by DOI or canonical URL. Read an accepted source once, using the
appropriate reader. Prefer a few relevant, verified sources to a large list of
unread papers. Record disagreements and why the adopted value fits the model.

## Verify citations and retain evidence

Confirm the exact work, title, authors and version at the publisher or primary
repository. Only print bibliographic details that have been checked. For a
load-bearing paper, use paper_graph when available and inspect publisher notices.
A lack of a returned notice does not prove that a paper has never been corrected
or retracted; record the coverage limitation when that matters.

Keep a readable source note: supported claim, URL/DOI, version or date, access
date, discovery channel, extracted quantity, credibility, and uncertainty. Record
queries briefly so another researcher can retrace discovery. No fixed YAML
handoff or separate ledger file is required.

Numerical inputs need a retained data file or reproducible acquisition procedure.
For retained downloads, record source URL, license and SHA-256. MCP downloads are
staged and may expire; copy needed files to the working directory promptly and
verify that the retained bytes match the recorded hash. Do not leave the only
copy in staging. Do not redistribute material without permission to do so.

If download is unavailable, use a permitted existing file-transfer tool or give
the user a source link and explain the gap. Do not reconfigure custom MCP settings
or bypass access controls. Avoid collecting credentials in the conversation.

## Figure references

Use [figure presets](../mathodology-figure-presets/SKILL.md) for visual work. Its
reference collection distinguishes originals, counterexamples and synthetic
previews. For additional references, verify the individual asset's license and
any third-party credit lines. Open access alone is not a reuse license.

Save a small, relevant selection with attribution, version, original URL, access
date and hash. Prefer an immutable source revision for code examples. Keep copied
source as reference text, review it before adaptation, and do not execute it
automatically. Extract design principles; do not present another paper's image
or numerical results as the current model's output. Broad scraping is unnecessary
when the existing presets already fit the question.
