---
name: init
description: Step 1 of the five-step flow. Run before any change. Inventory existing tools, read the original design intent, recall memory, claim the issue, and create an isolated worktree.
---

# init: question the requirement, inventory, isolate

Run this before the first edit.

## 1. Inventory before you build

Follow the **Key List Protocol**:

1. **Check the Key List**: Read the repository's SSOT index (`docs/ssot/MANIFEST.yaml`, `common/meta/data/MANIFEST.yaml`, or the App's contracts index).
   - Scan the capability keys (e.g., `deploy_v2`, `infra2-sdk`, `vault`, `signoz`, `pr_merge_gate`).
2. **Reuse if present**: If an existing component covers the need, reuse it directly. Do not build private alternatives.
3. **Append when new**: If no entry fits and a new capability is necessary:
   - Build the minimal implementation.
   - **Register the new key and summary into `MANIFEST.yaml` in the same PR.**
4. **First-turn contract**: State in your opening response:
   - `"Reusing existing component: <key>"` OR `"New capability: will register <key> in MANIFEST.yaml"`.

## 2. Read the original intent before you change a mechanism

- Find the issue, PR, or SSOT page that created the mechanism. Read it first.
- Write one sentence: "This exists because ...". If you cannot, you are not ready to change it.
- A fix that "does not take effect" needs the deep cause. Check that the host really loads the file. Do not retry the same edit.

## 3. Recall

Use the `recall` skill for the four-level search. Read hits as claims, not facts: check current code.

## 4. Scan issue and claim the lock

- Read the latest issue discussion (`gh issue view <N> --comments`).
- Search for an existing issue before you create one. Update it when it exists.
- Another worktree or running process for the same issue is an active lock. Do not take over. Match the full token:

```bash
git worktree list | grep -F "_issue<N>_"
```

A substring match is wrong: `issue12` would match `issue123`.

- **Scan open production decisions**: in a checkout of wangzitian0/infra2, run `uv run python -m tools.harness status --fetch --online`. A release tag that the production marker has not reached waits for a production decision. A `hold` in the handover notes (`recall` skill) answers it.

- **Scan stale leftovers**:
Run these in bash or zsh, in the repository you work in. The three counts are: branches whose upstream is gone, stashes older than 30 days, and local branches whose name is the head of a merged PR. Put each count above zero in the "facts you recalled" line. A count above zero shows a cleanup that nothing triggered. Do not delete what another session owns. A `gh` error is a failed scan, not a zero.
```bash
git fetch --prune --no-tags --no-write-fetch-head --no-auto-gc origin || echo "fetch failed: the counts can be stale"
LC_ALL=C git for-each-ref --format='%(upstream:track)' refs/heads | awk '/\[gone\]/ {n++} END {print n+0}'
git stash list --format=%ct | awk -v c=$(( $(date +%s) - 2592000 )) '$1 < c {n++} END {print n+0}'
gh pr list --state merged --limit 300 --json headRefName --jq '.[].headRefName' | sort -u | comm -12 - <(git for-each-ref --format='%(refname:short)' refs/heads | sort) | awk 'END {print NR}'
```

## 5. Init Swarm (M=4)

For complex tasks or large repositories, dispatch 1 Init Swarm (M=4 Interns via `subagent_batch`):
- **Intern 1 (Key List)**: Scans `MANIFEST.yaml` and `tools/` for reusable components.
- **Intern 2 (Intent & History)**: Runs git log search for past PRs touching the target subsystem.
- **Intern 3 (Memory Recall)**: Executes global `search_notes` across all projects.
- **Intern 4 (Worktree Locks)**: Checks active worktrees and process locks across repositories.

## 6. Create the worktree

- Name: `<repo>_issue<N>_<slug>`. Branch: `feat/issue<N>-<slug>`. Base: the latest `origin/main`.
- Never edit in a shared checkout (`git add` shares `.git/index`), and never auto-remove IDE worktrees under `~/.gemini/antigravity/worktrees/`.
- The worktree must work alone. Tools and tests must not use `../..` to find files outside it.

## 7. Report the baseline

Reply in the owner's language with four lines: the goal, the tools you reuse, the facts you recalled, the worktree path.
Do not execute test suites during baseline reporting. The baseline report is task metadata only.
