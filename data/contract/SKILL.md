---
name: contract
description: Use when a new source is connected or a source changes how it delivers, to write the data contract with the source system, the format, the schema, the quality rules, the delivery, the owner and the change process.
argument-hint: "[source]"
---

# Contract

The job: the data contract between the data platform and one source system, written from the profile and the metadata, and agreed with the source owner. It holds facts and agreements, never steps and never SQL. The contract with the consumers of a table is part of the data-product skill.

Input: the name of the source, with its profile and its metadata.

## Steps

1. Start from the profile of the source: every finding marked for the contract.
2. The format the source delivers: one delimiter, one encoding, one date format, one decimal separator, one null token.
3. The schema: take the tables, columns, types, keys and descriptions from the metadata file, never retype them. Mark the required columns.
4. The quality rules the source agrees to: unique keys, no empty required columns, values in range.
5. The delivery: how often, by what time, full or only the changes, and how a deleted row is marked.
6. The owner and the support channel on the source side.
7. The change process: the version of the contract, and how many days before a change the source announces it.
8. Write it in the Open Data Contract Standard, one file per source, and validate it against the schema of the standard.
9. List the open points for the meeting with the source owner.

## Output

One YAML file per source, like [references/purchasing.odcs.yaml](references/purchasing.odcs.yaml): the format, the schema with the keys and the required columns, the quality rules, the delivery, the owner, the support channel and the change process.

## Reads

- the profile, the metadata, the documents of the source, the existing contracts

## Writes

- the data contract of the source, and the list of open points

## Never

- Never sends the contract: the data engineer agrees it with the source owner.
- Never writes a transformation into the contract: it describes the data, and the pipeline is a separate change.
