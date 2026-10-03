---
description: Write down a procedure worth keeping — a multi-step process, a trap that cost real time, or something that has now come up three times. Use it the moment you finish such a task, while the details are still exact.
disable-model-invocation: true
---

# Record what you just worked out

Write a file into `.chamnan/skills/<short-name>.md`.

## First: is this already covered somewhere?

**Before writing anything, check what the workspace already has.** A skill you write can collide
with one that arrived from a plugin the person installed, and the collision is invisible to them:
nothing errors, both files look authoritative, and the only symptom is the assistant answering
inconsistently on exactly the kind of work the skill covers. Someone who is not an engineer has no
way to connect that to a file.

```bash
python3 -c "import sys; sys.path.insert(0, '<plugin>/lib'); import skill_overlap; \
            [print(o['kind'], o['name']) for o in skill_overlap.overlaps('.')]"
```

`skill_overlap.overlaps()` reports only what is true by construction — the same name in two active
stores with different contents, one name served by two plugins, or a workspace file that repeats a
shipped skill's text verbatim. It does **not** score similarity: that was prototyped over the 26
real skills here and measured unusable in both directions (over 100 of 325 pairs scored above an
0.35 title threshold on shared boilerplate alone, while no pair scored above 0.30 on body content —
so it would cry wolf constantly *and* stay silent on a real duplicate written in other words).

**What to do with a result: record it, do not refuse.** If the check names something, say so in one
line and extend the existing skill rather than writing a second one beside it. Nothing here blocks
the capture — a refusal the person cannot understand or override is worse than the overlap, and the
host ignores `disable-model-invocation` anyway (claude-code#22345), so a hard gate could not be
enforced where it would matter.

## When this is worth doing

- A task took several steps that were not obvious, and will come up again
- Something failed in a way that was expensive to diagnose
- You have now done the same thing a third time
- A decision was made whose *reason* will not be visible in the code afterwards

## When it is not

Anything a competent reader gets from the code itself. A file that restates what the code says costs
tokens on every future session and returns nothing. When in doubt, don't — an over-full skills
directory trains the next session to skip the directory.

## Format

```markdown
---
description: <one line, under 100 chars — this is what a future session sees in the registry>
---

# <what this is about>

## The trap / the task
What actually happens, concretely. Name real files, real commands, real error text.

## What to do
The steps, in order.

## Why it is like this
The reason. This is the part that stops someone "fixing" it back to the broken version.
```

**The `description` line is not optional.** Session start lists every skill by name *and*
description; a file with no description shows as a bare filename, and a bare filename is not enough
for a future session to decide whether to open it. That is the whole cost of the registry wasted.

Write in the language set as `language` in `.chamnan/config.json` (default `en`). These files are re-read on every session, which is why English is the default — but a procedure your team cannot read is worth nothing however cheap it is.

Be specific. "Be careful with the cache" is worthless. "`_write_index` is a plain `write_text` with
no atomic replace, so two threads writing the same index drop one update and can interleave into
invalid JSON, which `_read_index` turns into `[]` — batch such updates into one pass" is worth
keeping.
