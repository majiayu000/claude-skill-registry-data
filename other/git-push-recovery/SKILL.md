---
name: git-push-recovery
description: "Use when git push fails (large file limit, hook, hang)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, push, github, recovery, large-files, reflog, windows, msys]
    triggers:
      - "git push rejected"
      - "push failed"
      - "GH001 Large files detected"
      - "exceeds GitHub's file size limit"
      - "git push hangs"
      - "accidentally committed a huge file"
      - "lost changes after git reset --hard"
      - "git rm --cached pathspec did not match"
    related_skills: [github-repo-management, autogit-integration, git-clone-divergence-reconciliation]
---
# Git Push Recovery

Recover from pushes that fail or hang, especially in repos that mix code with large media assets (videos, images, PDFs). GitHub rejects individual files over 100 MB. A stray `.part`/`.mp4`/image can silently land in a `git add -A` and block the whole push.

## Large-File Rejection (GH001)

### Symptoms

```text
remote: error: File <name>.mp4.part is 177.41 MB; this exceeds GitHub's file size limit of 100.00 MB
remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
 ! [remote rejected]   HEAD -> <branch> (pre-receive hook declined)
```

### Prevention

Always `git status --short` BEFORE `git add -A` — stray downloads (`.part`, `.mp4`, screenshots) accumulate in repo roots. Add `.gitignore` for the pattern first, then `git add`.

### Fix when committed

```bash
git reset --soft HEAD~1
git rm --cached <big-file>
git commit -m "..."
git push origin HEAD
```

**Pathspec trap (Windows/MSYS):** filenames with `$`, unicode, spaces (e.g. `How I Close $297⧸Month Clients…mp4.part`) make `git rm --cached "exact name"` fail. Use a glob:

```bash
find . -maxdepth 1 -name "How I Close*" -exec git rm --cached {} \;
```

### Lost-changes salvage after reset --hard

If `git reset --hard` or a mangled `git rm` lost staged/committed changes, recover from the reflog without redoing work:

```bash
git reflog | head -5
git cherry-pick -n <hash>           # -n applies changes without committing
# then remove the big file, recommit, push
```

## Push Hangs in Asset-Heavy Repos

Big commits (~1 GB images) push slowly and exceed foreground terminal timeouts. Pattern:

```bash
git add -A && git commit -m "msg"
# background push:
git push origin HEAD
```

Use `notify_on_complete=true`; don't claim success until exit 0 with `HEAD -> <branch>` in output.

## Verification

- `git push origin HEAD` exits 0 with `HEAD -> <branch>` and no remote errors.
- `git ls-remote origin <branch>` shows the new SHA.
- `git status --short` clean of the big file (should be in `.gitignore` or gone).