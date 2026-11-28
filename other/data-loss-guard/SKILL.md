---
name: data-loss-guard
description: Stop-and-check protocol before any destructive or hard-to-reverse operation. Use the moment a planned step would delete, overwrite, truncate, or rewrite state that cannot be trivially recreated — rm, file overwrites, git reset --hard, checkout/restore/clean of tracked files, force-push, rebasing pushed commits, branch deletion, DROP/TRUNCATE, DELETE or UPDATE without a tight WHERE, bulk API deletes, kill/pkill, terraform destroy, cache or volume wipes.
---

# data-loss-guard

Almost every catastrophic agent failure is a destructive command run on a wrong assumption. Weak handling looks like `rm -rf build/` typed from memory of what "should" be there. Strong handling predicts what the target contains, looks, and only then runs the narrowest command that does the job.

Before any destructive action:

1. **Predict, then look.** Write down what you expect the target to contain (file count and names, row count, commits ahead of remote, which process owns the PID). Then check: `ls -la` before `rm -rf`; `git status` and `git stash list` before `reset --hard`, `checkout .`, `restore`, or `clean`; `git log origin/branch..branch` before force-push; `SELECT COUNT(*)` with the identical WHERE clause before `DELETE` or `UPDATE`; `ps` by PID before `kill`. If reality differs from the prediction — files you didn't create, more rows than expected, a PID you didn't start — stop and surface the difference. Don't reconcile it in your head and proceed.
2. **Distinguish recoverable from gone.** Committed work is recoverable via reflog; uncommitted work is not. A dropped column or truncated table is gone. An overwritten file has no undo — including your own file-write tool on a file you did not create this session: read it first, and edit rather than replace. Rank the blast radius honestly before choosing convenience.
3. **Prefer the reversible variant:** `git stash` over discard; move to a trash or backup path over `rm`; soft-delete or export-then-delete over hard delete; `--dry-run` wherever it exists (rsync, terraform, kubectl, many package and cloud CLIs) on the first pass, and paste its output before the real run.
4. **Scope the command tightly.** Explicit paths over wildcards; absolute paths so a surprise cwd can't redirect the deletion; never `rm -rf` a variable-built path without first echoing the variable and checking it is non-empty and expected; kill by PID from a listing, never `pkill`/`killall` by name pattern on a shared machine; DELETE/UPDATE always with a WHERE that names specific keys, inside a transaction where the DB supports it.
5. **Destroy last.** When replacing something — a file, a table, a branch, a service — the destructive step comes after the replacement is verified working, never before. A destructive command proposed as the fix for a problem you don't yet understand ("delete the cache / reset and start over") is a diagnosis shortcut: stop, find the cause, then decide whether deletion is needed at all.
6. **Uncommitted user work is sacred.** If the working tree holds changes you didn't make, don't clean, checkout, stash, or overwrite them without the user's explicit say-so. Same for files, rows, or resources that exist and that you did not create.
7. **Force-push and history rewrites on shared branches need explicit user authorization**, every time, and the push uses `--force-with-lease`.
8. **Report every destructive command.** The final report lists each one you ran, what it removed, and how to recover it — or that it cannot be recovered.

Rule of thumb: cheap check, irreversible mistake — the one-command look-before-delete is always worth it.
