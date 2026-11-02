---
name: implement-change
description: Plan, make and check a code change from start to finish. Use this for any feature, bug fix, enhancement or behaviour change, including requests that sound small such as "add a field", "fix this" or "make it support X". It keeps the change small, complete and verified.
---

# Implement a change

A good change is complete and small. It updates every place that needs it and
touches nothing else. The common failures are missing a related place, doing
extra work, and stopping before anything was checked.

## When to use

Any task that changes behaviour. For structure-only work use `refactor-safely`.
For a failure with an unknown cause, start with `debug-failure`.

## Steps

1. **Restate the task.** Write one sentence on the goal and a short list of what
   must be true when it is done. If two readings would produce different code,
   ask before you start.

2. **Orient.** If you have not read this area, follow `orient-in-codebase`.

3. **Find every affected place.** Search for the names you will change. Check
   callers, tests, docs, translations, schemas, config, and lists that repeat a
   value such as routes, plans or permissions. A missed copy is the most common
   cause of a half-finished change.

4. **Choose the smallest design.** Reuse existing helpers and patterns. Do not
   add options, abstractions or dependencies the task did not ask for. Write the
   plan as a short list of files and what changes in each.

5. **Open the matching skill.** Use `secure-change` for permissions, input or
   secrets, `change-data-safely` for stored data, and `use-external-api` for a
   third-party call.

6. **Write a test first where practical.** Make it fail for the expected reason
   before you change the code. Follow `write-tests`.

7. **Make one small edit at a time.** Run the nearest test after each step. If it
   breaks, you know which edit caused it.

8. **Handle the unhappy paths.** For each new input or dependency, decide what
   happens when it is empty, invalid, slow, unauthorized or failing.

9. **Review your own diff.** Run `git diff` and read every line:

   - Is each line needed for this task?
   - Did you leave debug output, commented code or unused imports?
   - Did you change formatting in unrelated lines?
   - Are existing users and existing data still fine?

10. **Finish.** Follow `verify-and-report`.

## Stop and ask when

- The requirement is ambiguous and the choice affects behaviour.
- The change needs a new dependency, a public API change or a data migration
  that the task did not mention.
- You have failed three times with the same approach.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Rewrite the whole file | Hides real changes and adds risk | Make targeted edits |
| Fix nearby issues too | Makes review harder and adds risk | Mention them in your report |
| Add a config option "just in case" | Adds code nobody needs | Build what was asked |
| Stop at the happy path | Most incidents are in failure paths | Handle each failure in step 8 |
| Say it should work | Nothing was tested | Run it and report the result |

## Example

Task: "Add a `nickname` field to user profiles."

Weak plan: "Add `nickname` to the User model."

Strong plan:

```markdown
Done when: users can save, see and clear a nickname of at most 40 characters.
Files:
- migrations/: add a nullable column
- models/user: add the field
- api/profile: accept, validate and return it; reject over 40 characters
- ui/profile: add the input and error message
- locales/: add the label in each language
- tests: both sides of the limit, blank value, another user's profile
Unchanged: existing users keep a null nickname.
```

## Report

Use the template in `verify-and-report`.
