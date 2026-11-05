---
name: git
description: Get git commands for any git operation — always shown as terminal commands, never executed
argument-hint: "<what you want to do, e.g. 'create branch for F4', 'commit my changes', 'push to stage'>"
disable-model-invocation: false
allowed-tools: Bash(git status) Bash(git log *) Bash(git diff *) Bash(git branch *)
---

You are helping the ConvoPilot project owner with git. They are non-technical and run all commands themselves.

The request is: **$ARGUMENTS**

## Rules — always follow these
1. **NEVER execute** `git add`, `git commit`, `git push`, `git checkout`, `git reset`, `git merge`, or `git rebase` automatically
2. Always present git commands in a code block for the user to copy and run in their terminal
3. Explain each command in one plain-English sentence below it
4. For destructive commands (`reset --hard`, `push --force`, `branch -D`, `checkout .`) add a ⚠️ warning explaining what will be lost
5. Suggest branch names using the project convention: `feature/<name>` or `fix/<name>`

## What to do
1. Read-only: check current status with `git status` and `git branch` if needed to understand the situation
2. Figure out the right git commands for the request
3. Present them clearly

## Output format

**Here are the commands to run in your terminal:**

```bash
# [what this command does in plain English]
git <command>

# [what this command does in plain English]
git <command>
```

**What this will do:** [1–2 sentence plain English explanation of the overall outcome]

---

## Common ConvoPilot git patterns

**Start work on a new feature (e.g. building F4):**
```bash
git checkout -b feature/conversation-runner
```

**Save your work after coding:**
```bash
git add service-one/src/api/services/simulation/
git commit -m "feat(F4): add async conversation runner"
```

**Deploy to staging (triggers auto-deploy to EKS):**
```bash
git push origin stage
```

**Push your feature branch to GitHub:**
```bash
git push origin feature/conversation-runner
```
