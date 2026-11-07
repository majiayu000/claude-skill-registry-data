---
name: metadata
description: Use when the metadata of a source has to be built or extended, to describe every table and column, the names and types from the data with a script, the descriptions from the documents, never guessed.
argument-hint: "[source]"
---

# Metadata

The job: extend the metadata of a source from its files and its documents. Facts from the data, descriptions from the documents, nothing invented.

Input: the source, its data files, its documents, and one example table written by hand.

## Steps

1. Read the example: one source, one table, the format to follow. Table name, description, then every column with its name, type, key and description.
2. Point at the data of the source: the exports or the landing files, one file per table.
3. Write a Python script that reads every file, every column as text first, and extracts the table names, the column names and the data types. IDs stay strings and keep their leading zeros. The script does this, not the model, so nothing is invented.
4. Take the keys from the profile of the source, never from a guess.
5. Read only the documents the data engineer points at: PDFs, handbooks, data dictionaries.
6. Take every description from the documents. A description must trace to a document.
7. Where the documents say nothing, leave the description empty and list it. Never guess a description.
8. Write every table into the metadata file, in the format of the example.
9. Report what was filled and what is still empty.

## Output

One metadata file per source, like [references/purchasing.yaml](references/purchasing.yaml): the source, its tables, and for every column the name, the type, the key and the description.

## Reads

- the data files of the source, the profile, the documents, the example metadata

## Writes

- the metadata file of the source, and the script that extracted the technical facts

## Never

- Never invents a column, a type or a description.
- Never reads a document the data engineer did not point at.
- Never changes a data file.
