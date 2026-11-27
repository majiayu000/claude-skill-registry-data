---
name: cookbook-writing
description: Method and style for a cookbook tutorial chapter. One story, each term taught as a plain idea first, reading levels checked by a script. Use when you write or review a tutorial or onboarding document.
---

# Cookbook writing

A tutorial takes a new engineer through one complete feature, from the first question to the shipped change. The
reader knows the language and the tools of the stack. They do not know the product, its business, or its words. The
chapter must teach all three without fear, and every fact in it must be true.

The rules are in [`references/style.md`](references/style.md). This skill is the procedure. Read `style.md` in full
before you write. Do not copy its rules here.

## Project values

Take these from the project `AGENTS.md` (or `CLAUDE.md`). If a section is missing, ask the user once, and suggest
that they add it.

- `## Docs layout`: the paths of the cookbook, the handbook, the spec, and the decisions log. Links from a step go to
  the handbook.
- `## Commands`: the keys `lint` and `format` (docs folder), and a diagram command if the project has one. A
  command in a chapter comes from this table.
- `## Invariants` and `## Architecture rules`: the rules the story must keep true.

## Inputs

The caller gives one of these tasks:

- **New chapter:** the tutorial, the chapter number, and its topic.
- **Rewrite:** the chapters to rewrite in the cookbook style. Keep their facts. Change their form.
- **Update after the build:** the chapters to check against the real code. Replace each **Planned code** block
  with the real code.
- **Update after a change:** the handbook sections or files that changed. Correct each step that is now wrong.

## Procedure

1. **Read the rules.** Read `references/style.md`, the tutorial `README.md`, and the tutorial `terms.md`. If
   `terms.md` does not exist, create it with the table form below. If the tutorial has no story yet, write the
   story table first (style.md section 3).
2. **Read the chapters before yours.** You must know which terms the reader already has, and what the story has
   told so far. Never explain a term again that an earlier chapter introduced.
3. **Collect the facts.** Read the spec sections, the handbook sections, and the source files that the chapter
   names. Check each file name, symbol, command, setting, and route with `grep` before you write it. If the facts
   disagree, the spec wins over the code, and the code wins over the handbook. Report the disagreement.
4. **Plan the chapter.** Write down, for yourself:
   - the one thing the reader can do at the end;
   - the scene from the story that needs it;
   - the new terms (3 or fewer in one section);
   - the steps (7 or fewer in one procedure), and the check after each step.
5. **Write the chapter** in the structure of `style.md` section 4. For each new term, write the plain idea first,
   then the bold name. Add a row to `terms.md` for it. End each step with a link to the handbook section that
   explains the mechanism.
6. **Move detail out of the main path.** If a reader can do the step without a fact, put that fact in a "Go
   deeper" box. If new readers often fail at a step, add an "If it does not work" box after it.
7. **Write the code blocks.** Use the real API exactly. Mark code that does not exist yet with **Planned code**.
   Keep each block to 20 lines. Put one sentence before it that says what to look at. Show examples in the stack
   of the project. When a tutorial teaches an idea that is not tied to one stack, show it in two stacks.
8. **Check the result** (next section). Fix each finding, then check again.

## Checks

Run each check on every file that you changed:

1. The reading-level check, which uses only the Python standard library:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/cookbook-writing/scripts/readability.py <files>`. It must report
   0 findings. It checks the sentence length, the paragraph length, the code block length, the length of a numbered
   procedure, and the words that STE does not allow. It cannot count technical terms: count them yourself (2 or
   fewer in a sentence, 3 or fewer new terms in a section).
2. The term rule: for each term in your chapter, `grep -rn "<term>"` in the tutorial folder. One chapter introduces
   it. No later chapter explains it again. No chapter uses a second name for it.
3. The links: each relative link and each `#anchor` exists. An anchor is the heading in lower case, with
   punctuation removed and spaces as hyphens. Underscores stay.
4. The story: each example uses the story of the tutorial. No person is "he" or "she".
5. The diagrams: if you changed a diagram source, run the diagram command of the project. It must exit with 0.
6. The format: run the `format` and `lint` commands of the project on the cookbook folder. If the format command
   changes a file, read the change.
7. A read-through: read the chapter from the start, as a new engineer. Mark each sentence where you must stop and
   think. Rewrite it.

## The term list

Each tutorial has `terms.md` with this table. Keep the rows in alphabetical order.

```
| Term | Plain meaning | Introduced in | More |
|---|---|---|---|
| **Facade** | The one file of a module that other modules can use. | [01](01-understand-the-system.md#…) | [handbook: facades](../../handbook/03-architecture.md#facades) |
```

## Forbidden content

- Never write about a system that this product replaced, a migration from it, compatibility with it, or legacy
  data, unless the project docs say the tutorial must.
- Never name a real customer, a real person, or a real incident. Use the invented story.
- Never write a fact that you did not check in the code, the spec, or the handbook.

## Report

When you finish, report these items in ASD-STE100, outcome first:

- The files that you changed or created, with full paths.
- The new terms, and the chapter of each.
- The output line of the reading-level check for each file.
- Each fact that you could not check, and each disagreement between the spec, the code, and the handbook.
- Each place where the chapter depends on a proposed decision of the spec that is not accepted yet.
- Each handbook section that this chapter shows to be wrong. Name it. Do not edit the handbook unless the
  caller asks.
