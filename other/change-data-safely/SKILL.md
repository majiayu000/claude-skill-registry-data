---
name: change-data-safely
description: Change a database schema or stored data without breaking running code or losing data. Use this for any migration, new or changed column, backfill, bulk update, delete, index, or change to a stored format, including in small projects. Data mistakes are often impossible to undo.
---

# Change data safely

Code can be rolled back, but lost data often cannot. During a deploy, old and new
code run against the same data at the same time, so each step must work for both.

## When to use

Any change to stored data or its shape.

## Steps

1. **Read the current state.** Read the schema and existing migrations. Find every
   reader and writer of the affected data.

2. **Ask what already exists.** Think about rows with nulls, duplicates, old
   formats and very large tables. Test against these, not only fresh data.

3. **Split risky changes into stages.**

   | Stage | Action | Safe because |
   | --- | --- | --- |
   | Expand | Add the new column or table, nullable | Old code ignores it |
   | Write both | New code writes old and new | Either version can read |
   | Backfill | Copy old rows in small batches | Can stop and resume |
   | Read new | Switch reads to the new field | Old data is still there |
   | Contract | Remove the old field, in a later release | Nothing uses it now |

   Renaming a column in place breaks whichever code version is not expecting it.

4. **Make each step safe to rerun.** A migration or backfill can stop halfway.
   Running it twice must not corrupt data.

5. **Consider locks and size.** Adding an index or rewriting a large table can block
   production. Use the database's online option, and process rows in batches.

6. **Test it.** Run the migration on a copy of the schema with realistic old rows.
   Run all migrations from empty too. Confirm that row counts and values are right.

7. **Plan recovery.** Write down how to undo each step. If a step cannot be undone,
   say so. Confirm that a recent backup exists and can be restored.

8. **Get approval before production.** Show the exact statements, the affected row
   count and the recovery plan. Do not run them against production without explicit
   approval for that specific action.

9. **Check the result.** Compare counts and sample rows. Then follow
   `verify-and-report`.

## Stop and ask when

- The change deletes or overwrites data, or removes a column or table.
- You are unsure which environment a connection points to.
- There is no tested backup.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Rename a column in one step | Breaks old or new code | Expand, migrate, contract |
| Add `NOT NULL` with no default | Fails on existing rows | Add nullable, backfill, then constrain |
| `UPDATE` or `DELETE` without a preview | Can hit every row | Run a `SELECT` with the same filter first |
| Update one huge batch | Locks the table | Use small batches |
| Test only on an empty database | Misses real data | Include old-format rows |
| Edit a migration that already ran | Environments drift apart | Add a new migration |

## Report

```markdown
Change: <schema or data change>
Affected: <tables and row counts>
Compatibility: <how old and new code both work during deploy>
Tested on: <data used, and the result>
Recovery: <how to undo, or why it cannot be undone>
Production: <not run / run with approval, and the result>
```
