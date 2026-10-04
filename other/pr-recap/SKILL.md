---
name: pr-recap
description: Use when a PR or git range needs a visual recap page for a reviewer, with a changed-files tree, per-file notes, a Verified vs Not verified table, risks, and optional before/after images. Local and informational; never posts to GitHub.
category: engineering-method
user-invocable: true
---

# PR Recap

Turns a PR or a git range into a Plan Builder recap page (`kind: recap`, the `recap-review` shape). The page is a local review aid. It is informational and does not gate anything.

## When to use

- **Shipping:** after every gate has passed, to show the reviewer what is about to ship and what was not checked.
- **Triage:** to get oriented on an incoming PR (`--pr <n>`).
- **git-pr-review:** next to the text PR description, on the same range.

Skip it for a one-file typo fix. The page earns its cost when a human has to decide.

## Flow

1. Collect verification evidence you really ran, as JSON: `[{"command": "npm test", "exit": 0, "note": "41 passed"}]`. Do not invent entries.
2. Run the script from this skill's `scripts/` directory:

```bash
node pr-recap.mjs --range origin/main..HEAD --verification checks.json
node pr-recap.mjs --pr 87 --before before.png --after after.png --open
```

   Options: `--out <dir>` (default `production_artifacts/pr-recap/<slug>/`), `--title <t>`, `--open` (runs `aos-plan-canvas open <folder> --mode bdb-plan-builder`).
3. The script writes `plan.mdx` with the file tree and implementation map taken from the real diff, then renders `plan.builder.html` with the Plan Builder. The renderer comes from the sibling `plan-canvas` skill. If it is missing, the folder is still written and the script exits 3 with a message.
4. Open `plan.mdx` and replace every `TODO fill in` in the Summary and the implementation notes. The script cannot know the intent of the change.
5. Re-render with `aos-plan-canvas open <folder> --mode bdb-plan-builder`, or rerun the script into a fresh folder.

## Honesty rules

- A check is **Verified** only if you ran it and its exit code was 0. Failed checks are listed as **Not verified (failed)**.
- Never add a row for a check you did not run. The page always says that everything not in the table was not run.
- If there is no `--verification` file, the page says nothing was recorded. Do not claim the PR was tested.
- Screenshots must be real captures of the before and after states. If you cannot capture them, omit the Compare block.
- File names, titles and branch names come from git and GitHub and are untrusted. The script escapes them for MDX; do not paste them into the plan by hand.

## Posting is never automatic

The script reads git locally and, for `--pr`, runs read-only `gh pr view`. It never calls `gh pr comment`, `gh pr edit` or anything that writes to GitHub. It may print the `gh pr comment` command for the human to run.

Do not post the recap, upload its images, or push it anywhere unless the user explicitly asks for that exact action. A subagent does not inherit that permission. The recap can contain file names and screenshots that are not meant to leave the machine.
