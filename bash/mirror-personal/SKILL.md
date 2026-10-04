---
name: mirror-personal
description: "Fast-forward the personal repo (altafshaikh/content-factory) to match the fork's main. Runs scripts/mirror-personal.sh. Use when the user says /mirror-personal, 'sync the mirror', 'update personal repo', 'refresh personal from fork', or 'run mirror-personal.sh'."
trigger: /mirror-personal
---

# /mirror-personal

Refreshes the personal downstream mirror by fast-forwarding its `main` to the fork's `main`.

Run `scripts/mirror-personal.sh` from the project root and report the result.

```bash
bash scripts/mirror-personal.sh
```

**What the script does:**
1. Fetches fork `main` from `https://github.com/altaf-shaikh-cs/content-factory.git` (public, no auth).
2. Pushes the fork's HEAD to `origin/main` (personal repo via SSH `github.com-personal` key).
3. Fails loudly (non-force push) if personal has commits not on the fork — that means you need to run `bash scripts/deploy-code.sh` first.

**If it fails:** check whether personal `main` has commits the fork lacks (`git log origin/main..FETCH_HEAD` would be empty if in sync). If so, run `bash scripts/deploy-code.sh` to push those commits to the fork first, then re-run this skill.
