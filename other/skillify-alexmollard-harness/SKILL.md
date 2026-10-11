---
name: skillify
description: Turn something you just did into a reusable skill and register it in the resolver. Use when the user says "skillify this", "make that a skill", or after completing a non-trivial procedure worth repeating.
---

# Skillify

Capture the work you just did as a reusable, parameterized skill — then register it in the resolver so it can be found and reused. This is the move that compounds a one-off into a capability.

> "You just do anything, and then I like it, I say *skillify it* — and it becomes basically like a tool call or a method call. And the most important part is plugging it into the resolver." — Pete Koomen / Andrej Karpathy, YC

## When to run

- The user says "skillify this" / "make this a skill" / "save this as a skill".
- You just completed a multi-step procedure that you (or a teammate) will plausibly do again.

Do **not** skillify trivial one-liners or anything a single existing tool already does.

## Procedure

1. **Identify the procedure.** Look at what was just done in this session — the steps, the order, the decisions, the gotchas. Strip out the one-off specifics (this particular file, this particular value).

2. **Generalize into parameters.** Anything that changed between "this run" and "the next run" becomes an input, not a hardcoded value. A good skill is the *shape* of the work, not a replay of one instance.

3. **Check before you write — DRY.** Read the resolver (see "The resolver" below) and skim existing skills. If one already covers this, **extend it with a parameter** instead of adding a near-duplicate. Adding skill #2 that overlaps skill #1 makes the library worse, not better.

4. **Write the skill.** Create `skills/<kebab-name>/SKILL.md` with frontmatter and a tight procedure:

   ```markdown
   ---
   name: <kebab-name>
   description: <what it does> + Use when <the trigger>.
   ---

   # <Title>

   ## Inputs
   - `<param>` — <what it is>

   ## Procedure
   1. ...
   2. ...
   ```

   Keep it minimal. The procedure should read like the steps a careful teammate would follow — no speculative options, no abstractions for a single use.

5. **Register it in the resolver.** Add one line to the index the agent actually reads: `name` + a one-line **use-when** + a link to `skills/<kebab-name>/SKILL.md`. A skill that isn't in the resolver doesn't exist.

6. **Verify resolvability.** Run [`check-resolvable`](../check-resolvable/SKILL.md) to confirm the library is still DRY and MECE after the addition — no duplicate, no overlap, no gap.

## The resolver

The "resolver" is whatever flat index your harness reads to discover capabilities — `AGENTS.md` / `CLAUDE.md` skills list, a tool registry, the `skills/` directory itself. Treat it as the source of truth: every skill is reachable from it by name, with a one-line description that says *when* to use it. Register on create; prune on merge.

## Output

State plainly: the new skill's path, the one-line resolver entry you added, and whether `check-resolvable` flagged anything to merge.
