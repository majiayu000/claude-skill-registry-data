---
name: one-canonical
type: Skill
title: "one-canonical — find every instance of a thing, build one, move them all, prove none are left"
description: "Collapsing every copy of one kind of thing (tables, UIs, utilities, hooks, APIs, renderers) into a single canonical one. Use when asked to unify, merge, converge, or 'make one X used everywhere', or before migrating callers onto a new canonical piece. NOT for docs (use docs)."
tags: [doctrine, consolidation, migration, census]
timestamp: 2026-09-23T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/one-canonical/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# one-canonical

The rich-content census took three rounds and each one still found surfaces the last missed. Every step below ends on a check; skipping one is the failure.

## 1. Start THE LIST before you search

Create one list file the first minute (`<project>/LIST.md` or the project's register). Every instance
you find, in any round, by anyone, goes on it immediately: **what · where (file / table / route / repo)
· how found · status**. Never rebuild it from memory or from a summary. A find that is not on the list
was not found.

Done when: the list exists and every later step writes to it.

## 2. Research until the finds stop

Keyword grep is round one, never the last round. Each round uses a DIFFERENT method:

- enumerate, don't search: every route, every table, every package, every repo (not only this one);
- walk the import graph, the database (live columns, triggers, row counts, never estimates), overlays,
  windows, registries loaded by string key;
- read how each copy actually behaves, not just where it is.

Where copies do the same job differently, list every way on the list and pick a winner per capability.
Build the canonical one CLEAN from the winners: never promote the best existing copy and patch it.

Done when: a round using a new method adds nothing to the list.

## 3. Migrate one by one from the list

Work the list top to bottom. Each item: move it, verify it on its real surface, mark it done with the
proof. No bulk "all migrated" claims. Before moving each item, screenshot it in place and apply
[canonicalize without destroying](../../policies/no-dead-ends.md): an ordinary copy is
replaced; a copy that is visibly better in its spot is adopted into the canonical piece (feature,
option or new primitive) after one simple question to Arman with before/after links. Only then is
the old copy deleted, not left beside the new one.

Done when: every row is done-with-proof or explicitly out of scope with a reason.

## 4. Tear it apart before you believe it

When you think you are done, dispatch agents that did NOT build it and do NOT get your list: they
search every codebase from scratch for anything still doing the job the old way. Every find goes on the
list and back through step 3.

Done when: an independent sweep returns nothing new.

## 5. Look for what nobody called this before

Charge at least one agent to think outside the box: what does this same job under another name? (The
assistant answer is a note. A flashcard front is rich content. A system prompt is a document.) Anything
that fits joins the list.

Done when: that agent's finds are on the list and migrated or ruled out with a reason.

## 6. Lock the door

Add a guard that fails on any NEW use of an old copy, with a baseline that only shrinks, proven
failing-then-passing (`forcing-function-tests`).

Done when: the guard is in the release gates and its self-test goes red then green.
