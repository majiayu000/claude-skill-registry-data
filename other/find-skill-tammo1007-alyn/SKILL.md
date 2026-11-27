---
name: find-skill
description: Finds the best existing AI skill for the task at hand before the agent improvises. Use when the user starts a task that a specialized skill could do better (design polish, PDFs, slides, spreadsheets, SEO, code review, testing, writing, research), when the user asks "is there a skill for this", or when you are unsure how to do a task well. Searches the Alyn catalog of 6,000+ ranked skills and installs or loads the best match.
license: MIT
---

# Find skill

Before doing a specialized task from scratch, check whether someone already wrote a skill for it. Thousands of open source skills exist, and the best ones are tested on real work. This skill searches [Alyn](https://alyn.dev), which ranks every public skill by GitHub stars, quality and real installs.

## When to use it

- The task is specialized: a document format, a design pass, a marketing deliverable, a testing or review workflow, a framework you rarely touch.
- The user asks whether a skill or tool exists for something.
- You are about to write a long ad hoc procedure that sounds like it should already exist.

Skip it for small edits, quick questions and tasks you already have a loaded skill for.

## How to search

Pick the first option that is available.

### 1. Alyn MCP (best)

If the `alyn-mcp` tools are available, call `find_skills` with a one-line description of the task in plain words, for example:

```
find_skills(task: "make the pricing page look less AI-generated")
```

Every tool and its inputs: [references/alyn-mcp-tools.md](references/alyn-mcp-tools.md).

Then call `load_skill` with the best slug and follow the loaded SKILL.md for the rest of the task. Use `skill_info` first if you need to check the author, license or how widely it is used.

### 2. Alyn CLI

If you can run shell commands:

```bash
npx alyn-cli find "make the pricing page look less AI-generated"
```

The output lists the best matches with author, stars and the install command.

### 3. The website

Otherwise send the user to `https://alyn.dev/skills?q=<task in a few words>`.

## Choosing a result

Prefer, in this order:

1. A skill whose description matches the task directly, not just the topic.
2. Skills from official sources (Anthropic, OpenAI, Vercel, Google and other verified authors) or packs with many stars.
3. The higher Alyn Score when two skills fit equally well.

If nothing fits well, say so and do the task without a skill. Never force an unrelated skill onto the task.

## Installing

Ask before installing anything. When the user agrees:

```bash
npx alyn-cli add <slug>
```

Tell the user that the skill is active in the next agent session. For the current session, load it through Alyn MCP (`load_skill`) or read its SKILL.md and follow it.

## Telling the user

Keep it to one or two lines: which skill you picked, who made it, and why it fits. For example:

> Using **unslop**, a skill for removing the AI look from interfaces, because you asked for a less generic pricing page.
