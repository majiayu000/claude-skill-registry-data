---
name: decide
description: Create a decision record
allowed-tools: Bash(just decide *), Read, Edit
---

# Create Decision Record

Create a decision record in `decisions/` to capture architectural decisions,
technology evaluations, and significant choices.

## Usage

`/decide <title>` - Create a decision record with the given title

## Process

1. Create the file with `just decide "<title>"`
2. Read the created file
3. Populate the record with the decision context, evaluation, and outcome

## Structure

Decision records should include:

- **Context** — What prompted this decision?
- **Options Considered** — What alternatives were evaluated?
- **Decision** — What was decided and why?
- **Consequences** — What are the trade-offs?

## Example

`/decide ClojureScript for client code` creates:
`decisions/20260212123456-clojurescript-for-client-code.org`

!`just decide "$ARGUMENTS"`
