---
name: design-domain
description: Facilitates the Domain movement of a Tutti design session. Use after the Impact movement to draft the ubiquitous glossary, list the entities and events of the world, and find where the seams (bounded contexts) fall. Asks one question at a time, may invoke the data-flow diagram skill when the world reads better as a picture, and emits the movement artifact section once the glossary, the entities and events, and the seams are covered.
---

# Domain movement

Name the world before deciding how to build it. The guiding question is: what is the language
and shape of this world, and where are the seams? A shared, precise vocabulary is the point;
every later movement leans on these words meaning one thing.

## What to cover

- **Glossary drafted**: the ubiquitous language, each term meaning exactly one thing. Kill
  synonyms that hide two different concepts.
- **Entities/events listed**: the nouns that have identity and the things that happen to them.
- **Seams identified**: where one bounded context ends and another begins, so a later
  structure decision has natural lines to cut along.

## How to facilitate

Ask ONE question at a time. Start by drawing out the terms as the human says them, then pin
each to one meaning, then surface the entities and events, then ask where the language shifts
(a term that means something different in two places is a seam). Go deeper where two concepts
are being conflated under one word.

## Diagrams

When the entities, stores, and the data moving between them read better as a picture, invoke
the `data_flow` diagram skill and embed its inline SVG in the artifact section.

## When you are done

Once the glossary, the entities and events, and the seams are covered, emit the tagged complete
reply with the artifact section as markdown: a `## Domain` heading, the glossary, the entities
and events, and the seams (bounded contexts).
