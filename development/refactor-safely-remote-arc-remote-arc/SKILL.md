---
name: refactor-safely
description: Restructure, rename, split or move code without changing behaviour, and prove that nothing changed. Use this for any refactor, cleanup, file move, module split or dead code removal, including when it is only one step inside a larger task.
---

# Refactor safely

A refactor promises that behaviour stays the same, so it needs evidence. Mixing
behaviour changes into a move makes that impossible to review.

## When to use

The goal is better structure with the same behaviour. If behaviour must change too,
do it in a separate commit.

## Steps

1. **Record the baseline.** Run the tests, type check and build, and save the
   results. Stop and fix the baseline first if it is failing in this area.

2. **Check that tests protect this code.** If the code has no tests, write tests
   that record its current behaviour first, using `write-tests`.

3. **Move in small mechanical steps.** Use the editor or language tools to rename
   and move where you can. Prefer `git mv`, so that history follows the file.

4. **Commit structure apart from behaviour.** A reviewer should be able to read a
   move commit as a move.

5. **Update everything that names the old path.** Search for it in imports, tests,
   docs, build config, CI, scripts, and strings built at runtime. Strings are easy
   to miss, because neither the compiler nor search-and-replace on imports finds
   them.

6. **Check that tests still test something.** A test that looks through a folder
   or matches a path can pass with nothing to check after a move. Confirm that test
   counts did not fall, and that each path-based check still finds its files.

7. **Prove that behaviour is unchanged.** Use the strongest check you can:

   - Compare the built output before and after, with paths normalized.
   - Compare the test count and results with the baseline.
   - Compare the public API or exported names.
   - Run the type checker with unused-name checks on.

8. **Finish.** Follow `verify-and-report`.

## Stop and ask when

- You find a bug. Mention it, and do not fix it inside the refactor.
- A clean move needs a public API change.
- The change is too large to review, and it could be split.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Fix a bug during the move | Reviewers cannot tell what changed | Use a separate commit |
| Reformat everything | Buries the real change | Keep formatting out |
| Say tests still pass | Fewer tests may be running | Compare the counts |
| Delete code that looks unused | It may be reached dynamically | Search for it, including strings |
| Add a new abstraction | That is a design change, not a refactor | Keep to the agreed goal |

## Report

```markdown
Structure changed: <what moved>
Behaviour changed: none
Equivalence proof: <what you compared, and the result>
Test count: <before> -> <after>
References updated: <imports, docs, CI, scripts>
```
