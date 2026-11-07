---
name: toolkit
description: Use to build or rebuild the documentation site of the project from the repo, the architecture, the data lineage, the call graph, the data model, the data quality, the runs and the data catalog.
---

# Toolkit

The job: the engineering toolkit of the project as a website, built from the repo, one page per tool. Rebuilt after every release.

Input: none, it reads the whole repo.

## Steps

1. Write a site builder: one script that reads the repo and writes the pages, so the site can be built again after every release.
2. Overview: the sources, the layers and the latest runs.
3. Architecture: drawn from what runs, not by hand. The high-level picture first, the detail below it.
4. Data lineage: every table, clickable, upstream and downstream.
5. Call graph: who calls what in the code, clickable.
6. Data model: the entities and their relationships, then the star schema with the keys.
7. Data quality: the checks and their results, day by day.
8. Runs: what ran, how long it took, and the result.
9. Data catalog: every table and column, with a sample and a description. Personal data is masked in the samples.
10. When the project is big, ask how many agents may run, give one agent per page, and let every agent check its page against the repo.
11. Build the site and say where to open it.

## Output

One folder of HTML files, like [references/](references/): [index.html](references/index.html) as the hub and one page per tool, nothing fetched from the network. Read them for the layout before you write the builder.

## Reads

- the metadata, the pipeline code, the run records, the check results, the knowledge

## Writes

- the site builder, and the pages it writes

## Never

- Never edits a page by hand: fix the input or the builder, and build again.
- Never adds a library or a fetch from the network to a page.
