---
name: data-product
description: Use when a table is served to consumers, released or changed, to build everything a consumer needs as a data product, the guide, the data model, the metrics, the starter queries, the quality, the releases and the data contract.
argument-hint: "[table]"
---

# Data product

The job: the consumer side of one table, planned first. It changes no table and no SQL.

Input: the table to serve.

## Steps

1. Plan first: read the table, its code and the queries of its consumers, and show the plan before writing anything.
2. Overview: what the table is for, its grain, who reads it, and the service levels.
3. Guide: what to trust, the known issues, and where to start.
4. Data model: the tables behind it and how they join.
5. Metrics: every measure with its rule, and what is safe to sum.
6. Queries: the starter queries, taken from the query logs.
7. Quality: the quality rules and their results.
8. Releases: the release notes, the number diff between the versions, and the corrections the consumers reported.
9. Contract: the data contract with the consumers, in the Open Data Contract Standard.
10. Add the product to the data products page, where the consumers browse.

## Output

One HTML file, like [references/data-products.html](references/data-products.html): the data products page with every product, and each product with its tabs, from the overview to the contract. Read it for the layout before you write the page.

## Reads

- the table, its SQL, the query logs, the corrections the consumers reported, the knowledge

## Writes

- the documentation of the product, and the data products page

## Never

- Never changes the table or any SQL: a finding is listed as an open point for the data engineer.
- Never sends a release note: it drafts.
