---
name: automation-blueprint
description: "Use when repeated work should be delegated and its spec isn't clear, or when designing agents that turn tickets into merged code. Design only, no build."
user-invocable: false
---
# Automation blueprint
Job: Specify repeated work well enough to delegate, down to who does what and what stops duplicates.
Takes: an idea or a pain.   Gives: workflow spec files, or a system design naming a product per role. Design only.

This block produces local files. It builds nothing, connects nothing and buys nothing.

## Steps

1. Pick the shape.

   | The work is | Open in this skill |
   |---|---|
   | Something a person repeats in their life or work | `personal-workflow.md` |
   | Agents on remote machines taking work from a ticket or a timer through to merged code | `agent-pipeline.md` |

2. Use the skill `question-tree`, with that file's output in place of a decisions artifact. Edit the spec files as answers land.
3. Follow the file's method until its finish condition holds.
4. Use the skill `source-trail` for any current fact about a product. Date what you find, because product facts expire.
5. Say where the files are and what remains unsettled.

## Done when

- A personal workflow: a builder could implement each spec without asking one question.
- An agent system: every role has a named product or a deliberate none. Every task states its start, reads and writes, next start, human re-entry and duplicate guard. Every ticket source states its duplicate guard.
- Product claims carry a date and a source, or are labelled.
- Nothing was built.
