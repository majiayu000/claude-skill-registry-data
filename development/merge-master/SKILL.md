---
name: merge-master
description: Merge dev branch into master/main and push. Use when dev changes are ready for production branch. Invoked by saying "merge to master" or "merge to main".
---

# Merge Dev into Master

Merge the `dev` branch into `master` (or `main`) and push. Includes safety checks.

---

## Steps

1. **Ensure all dev changes are pushed** — run `git status` and `git log origin/dev..dev`. If there are unpushed commits, push them first (with user approval).

2. **Switch to master/main:**
   ```bash
   git checkout master   # or main
   git pull origin master
   ```

3. **Merge dev:**
   ```bash
   git merge dev --no-ff -m "merge(dev→master): <summary>"
   ```
   If there are conflicts, report them and wait for user instructions.

4. **Push master:**
   ```bash
   git push origin master
   ```

5. **Switch back to dev:**
   ```bash
   git checkout dev
   ```

---

## Rules

- **Only merge pushed changes.** Never merge uncommitted or unpushed work.
- **Never force push to master/main.**
- **If merge conflicts occur, STOP and report.** Do not auto-resolve.
- **Always push immediately after merging.**
- **Switch back to dev when done.**
