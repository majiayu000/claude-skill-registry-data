---
name: profile
description: Use when a new source or new files arrive, to profile them before any data contract or pipeline code is written, the file formats, the schema, the data quality, the bad records, the relationships, the gaps and the personal data.
argument-hint: "[folder, file or table]"
---

# Profile

The job: understand new data before anything is built on it. It writes nothing but the report.

Input: the folder of the new source, a feed file, or a table.

## Steps

1. Run a profiler on what arrived, with scripts that count. Never guess a number.
2. File format: delimiter, quoting, encoding, null tokens, decimal separators, date and timestamp formats.
3. Schema: tables, columns, data types, row counts, and the schema drift between the files.
4. Data quality: null values, empty columns, constant columns, duplicate rows, and the uniqueness of the primary key.
5. Bad records: corrupt records, outliers, values out of range, and placeholder values such as 9999-12-31.
6. Relationships: for every foreign key, the orphans, the child rows whose parent is not in the delivery.
7. Gaps and deletes: business days without rows, tables that never change, and how the source marks a deleted row.
8. Personal data: the columns that hold personal or bank data, with their values masked on the page.
9. Compare with the metadata, if there is one: columns the metadata does not know, and columns that did not arrive.
10. Rank the findings, each with the rows it affects and the decision it needs, marked for the data contract or for the pipeline.
11. Give the result as one web page, with the input for the data contract and the pipeline at the end.

## Output

One HTML file, like [references/profile.html](references/profile.html): the numbers on top, one section per check with a chart or a table, the findings ranked, and the input for the contract and the pipeline last. Read it for the layout before you write the page.

## Reads

- the files or tables, read-only, and the metadata if there is one

## Writes

- the web page only

## Never

- Never changes a file of the project.
- Never guesses a format: a format is what the values show.
- Never shows personal data unmasked.
