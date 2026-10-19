---
name: commit
description: Use when the user asks to commit changes to git. Generates a commit message from the diff and commits directly by default — no approval prompt. Pass `--confirm` to ask for approval first. Pass `--push` to also push to the default remote after the commit lands.
purpose: Generates a commit message from the diff and commits, optionally pushing, without asking unless told to.
args: "[--push] [--confirm]"
stage: forge
---

# Git Commit with Generated Message

## Workflow

1. Run `git status` and `git diff HEAD` in parallel to understand all changes
2. Draft a commit message based on the diff
3. By default, commit directly with the generated message — no approval step. If `--confirm` was given, ask for approval first (see *Approval*) and use the user's answer instead if they reject or ask for a different message.
4. If `--push` was given, push to the default remote after the commit lands

## Commit Message Rules

- Imperative mood: "Add X" not "Added X"
- First line ≤ 72 characters, summarizes the *what*
- Body (if needed) explains the *why*, separated by a blank line
- Stage specific files by name — avoid `git add .` or `git add -A`
- Never skip hooks (`--no-verify`)

## Approval (opt-in via `--confirm`)

Only when `--confirm` was passed: use AskUserQuestion with the generated message as the single option, plus "Other" for custom input, before committing. Frame the question by whether `--push` was also requested:

- Without `--push`: "Commit with this message?"
- With `--push`: "Commit and push with this message?"

```
options:
  - label: "<generated message>"
    description: "Use this commit message"
```

Without `--confirm`, skip straight to *After Drafting* below.

## After Drafting

```bash
git commit -m "$(cat <<'EOF'
<message here>
EOF
)"
```

Include a `Co-Authored-By: <model name>` trailer unless the user opts out. Use your actual model name (e.g. "Claude Sonnet 4.6") — no email address.

## Push (when `--push` is given)

After a successful commit, push to the default remote:

```bash
git push
```

If the branch has no upstream tracking branch, use:

```bash
git push -u origin HEAD
```
