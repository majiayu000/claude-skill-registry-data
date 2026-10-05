---
name: oncokb-code-comments-standards
description: Comment-writing standard focused on explaining non-obvious structure and behavior for first-time readers.
---

## Purpose

The goal of comments is to make system structure and behavior obvious enough that a reader can quickly find needed information and modify code with confidence.

Comments carry information that code alone does not make easy to deduce.

## When to use this skill

- Use when adding or editing comments in source code.
- Use when reviewing code and deciding whether current comments are sufficient.
- Use when refactoring comments to improve maintainability and reader confidence.

## Core standard

- Write comments for what is not obvious from code.
- Judge obviousness from the viewpoint of a first-time reader, not the original author.
- Prioritize details that help readers understand structure, behavior, assumptions, and constraints.
- Prefer improving code when possible, and use comments to close the remaining understanding gap.

## Required comment locations

- Add comments on business logic that is not basic CRUD logic.
- Add comments for fields and data types that are exposed via API calls.
- Add comments for fields and data types used in server-side rendering templating logic.
- For non-trivial business logic, include references to supporting context such as meeting notes, design docs, tickets, or other lookups readers can use to learn more.

## What comments should cover

- Why the code exists or why an approach was chosen.
- Key invariants, assumptions, and preconditions.
- Non-obvious control flow, side effects, and interactions.
- Important limitations, failure modes, or edge-case behavior.
- Information a maintainer needs before making safe changes.
- For referenced decisions, include enough identifier detail for retrieval (for example ticket ID, meeting date/title, or document name).

## What to avoid

- Restating code line-by-line.
- Comments that only repeat names or syntax already visible.
- Vague statements that do not change reader understanding.
- Defensive arguments about readability when a reviewer reports confusion.

## Review rule

If a reviewer says something is not obvious, treat that as valid signal. Do not
argue from author intent. Clarify the confusion with better comments,
better code, or both.

## Quick checklist

Before finalizing comments, ask:

- Would a first-time reader understand the design intent?
- Is each comment adding information not already obvious in code?
- Did I comment all non-CRUD business logic?
- Did I document API-exposed and SSR-template fields/data types where behavior or contract matters?
- For non-trivial logic, did I include a concrete reference readers can follow?
- Can a maintainer predict behavior well enough to change this safely?
- Did review feedback about confusion get resolved in code or comments?
