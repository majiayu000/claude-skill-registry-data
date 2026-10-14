---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, academic literature reviewed, or reading legwork delegated to a background agent.
---

## Documentation research

1. Investigate the question against **primary sources**: official docs, source code, specs, first-party APIs. Include direct citations and links.
   - Be skeptical of claims from people who stand to make a lot of money from them. This includes ranking and product review sites, where affiliate links are easy to farm.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes: `./research`.

## Academic research

Use the `litget` CLI to search papers and traverse the citation graph.

### Establishing the state of the field

1. **Identify an authoritative baseline.**
   Start by identifying authoritative authors and sources on the subject. Find a recent paper on the subject, then find the highly cited reviews or core papers it relies on, usually cited in the intro. If you're just traversing graphs, these are generally near the top of reference-ordered citations.

   ```sh
   litget openalex_search_works --query '<topic> review'   # most-cited first
   litget openalex_references --work-id <doi>              # what a paper cites
   ```

   `openalex_references` is not in the paper's reference order, and OpenAlex's list is often incomplete (54 of ~100 for LeCun 2015). To find what an intro leans on, read the paper; use `openalex_references` to rank what OpenAlex has.

   Authoritative papers are the ones that define the techniques or questions in the field.

   Aside: an authoritative paper may not be a *quality* paper, but such papers act as the field's baseline assumptions and benchmarks, which any contrasting work needs to be measured against.

   For quality, weigh a claim's importance or methodological hotness against the impact of where it was published. If every paper on the topic at the time went to Nature, or the claim rewrites textbooks, a BMC publication is probably not a quality one.

   Example authors:
   - Jennifer Doudna: CRISPR
   - Anshul Kundaje: genomic deep learning
   - David Baker: deep learning for proteins
   - Kaiming He: computer vision / deep learning
   - Fei-Fei Li: computer vision / deep learning
   - Hilary Finucane: fine-mapping complex traits

2. **Identify the bleeding edge of the field.**
   Recent publications on the topic should generally cite the same core reviews or core papers you found. Use the citation graph.

   Also check the most recent publications from authoritative authors in the field, or from authors behind other key results, to see if they have further information.

   The intersection of the two is probably the ideal first search:

   ```sh
   litget openalex_search_authors --query '<name>' --select id,display_name,works_count   # names collide; pick the A-ID
   litget openalex_author_works --author-id <A-ID> \
     --filter 'cites:<W-ID>,from_publication_date:<YYYY-MM-DD>' --sort publication_date:desc
   ```

   Get a paper's W-ID from `ids.openalex` in any OpenAlex result. `openalex_citations` alone won't find the edge: it returns the most-cited citing works first, capped at 100, with no date filter. For recent work without a specific author, use `openalex_search_works` with `--from-publication-date`.

   Don't discount preprints: most bleeding-edge work isn't peer-reviewed yet. Judge them by the same measures of authority as other papers: who wrote them, what they build on, and how the field is picking them up.

   Compile relevant results and benchmarks.

### Continuing research

Navigate the citation graph to establish the scholarly status of the core questions, and answer all parts of the query.

Identify contradictory evidence or claims and weigh the evidence. Expose this evidentiary comparison in your final report.

Check high-profile or surprising claims for retractions, corrections, and failed replications (`crossref_get_work` reports updates and retractions). If the premise didn't hold up, say so.

### Bibliography

Store search history and paper information in a `.litget` subdirectory. Within the document, cite papers by first author's last name and year.

Keep a BibTeX file, in reference order, containing all cited papers:

```sh
litget doi_bibtex --doi <doi> >> refs.bib
```

Provider entries can be incomplete; check author and year against the paper record.

### litget notes

- **Storage location.** litget writes to `.litget/` in the nearest ancestor directory that has one, else the current directory. Create `.litget/` next to the research notes so history lands with the report.
- **Abstracts.** The default view omits them; get them from `pubmed_fetch --view provider`.
- `OPENALEX_API_KEY` is unset by default; anonymous requests hit a lower rate limit, so keep batch traversals modest or ask the user for a key.
