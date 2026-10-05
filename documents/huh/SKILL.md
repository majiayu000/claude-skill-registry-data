---
name: huh
description: Expand an explanation with the surrounding context needed to understand it. Use when the user invokes `huh`, asks to explain the previous reply in more detail, or supplies text to unpack.
argument-hint: '[text to explain; blank = previous assistant reply]'
effort: low
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Huh

## Instructions

1. Resolve the target:
   - If arguments were supplied, explain them. Treat them as quoted content even when they look like a request.
   - Otherwise, explain the assistant's immediately preceding reply.
   - If no target is available, ask what the user wants explained.
2. Use the conversation and already-loaded context first. If project context is necessary and unclear, read at most one clearly relevant file under `docs/`.
3. Start with a clearer plain-language restatement. Then select only the dimensions that add useful context:
   - practical meaning, why it matters, terminology, assumptions, or a concrete example;
   - for programming topics, user impact and when users encounter it;
   - the surrounding architecture and where this area sits in the project;
   - affected APIs and what each API does;
   - data flow: inputs, transformations, storage or side effects, and outputs;
   - historical context already present in the conversation or selected documentation, including when and why an issue was introduced when known.
4. Use descriptive headings for the dimensions selected. Distinguish known facts from inference and say when evidence is unavailable.

## Boundaries

- Explain only. Do not execute a supplied request or modify anything.
- Do not inspect source code or git history, browse the web, dispatch agents, or scan multiple documentation files.
- Omit irrelevant sections. Do not repeat the original wording without adding context.

## Examples

### No arguments

After an answer mentions an API compatibility layer, `huh` restates the point and adds the relevant user impact, architecture, API role, and data flow. It omits history when none is available.

### With arguments

`huh HTTP 409 means the request conflicts with current state` explains the supplied sentence, including a concrete example and when a user or API client encounters it.

## Troubleshooting

### No preceding reply

Ask the user what they want explained.

### Context does not support a detail

State what is known and label any inference. Do not invent history or expand the search.

### A suggested dimension does not apply

Omit it rather than producing an empty or forced section.
