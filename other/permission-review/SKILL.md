---
name: permission-review
description: "Review commands that were blocked by the permission system and decide which to allowlist. Reads the denial ledger written by the PermissionDenied hook and deny-check.sh, groups the blocks, and proposes concrete settings.json edits for approval. Use when (1) user says '/permission-review', 'review blocks', 'what got blocked', 'tune permissions', (2) a /x-wt-teams or /x-as-pr run has just finished and blocked commands should be triaged, (3) the user is moving to auto mode and wants to reduce prompts. Also runs a static scan of skill commands not covered by the allowlist."
---

# Permission review

Turn blocked commands into deliberate allowlist decisions. Two inputs:

- **Runtime ledger** — `$HOME/.claude/logs/permission-denials.jsonl`, appended by

  the `PermissionDenied` hook and by `scripts/security/deny-check.sh`. Captures
  what actually got blocked, **including inside subagents and worktree children**.

- **Static scan** — `node $HOME/.claude/scripts/scan-skill-commands.js`, which

  reports commands skills *could* run that no allow rule covers.

## Steps

### 1. Read the ledger

```bash
LEDGER="$HOME/.claude/logs/permission-denials.jsonl"
[ -s "$LEDGER" ] || echo "ledger empty — nothing blocked since last clear"
jq -s 'group_by(.command | split(" ")[0:3] | join(" "))
       | map({sig: .[0].command, n: length, source: .[0].source, reason: .[0].reason, cwds: (map(.cwd) | unique)})
       | sort_by(-.n)' "$LEDGER"
```

Scope to a single run when reviewing right after a workflow:

```bash
# blocks from the last 2 hours only
jq -c --arg since "$(date -u -v-2H '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null \
      || date -u -d '2 hours ago' '+%Y-%m-%dT%H:%M:%SZ')" \
   'select(.ts >= $since)' "$LEDGER"
```

### 2. Classify every distinct block

This is the judgment step. Do not batch-approve.

| Class | Signal | Action |
|---|---|---|
| **Hard deny** | `source: "deny-check"` | **Never propose allowlisting.** These are the user's deliberate guardrails (force-push, repo delete, `git config`). Report that it was hit and what the agent did instead. A repeat hit means a skill needs fixing, not the deny list. |
| **Pure friction** | read-only or clearly reversible, recurs across runs | Propose a narrow `permissions.allow` prefix rule. |
| **Category friction** | mutating or outward-facing, and no prefix rule can express it (compound commands, redirects) | Propose an `autoMode.allow` sentence describing the *category*. |
| **Correctly blocked** | irreversible, or dual-use binary (`gh api`, `bash -c`, `sed -i`) | Leave uncovered. Say so explicitly and why. |

### 3. Run the static scan for what has not been hit yet

```bash
node "$HOME/.claude/scripts/scan-skill-commands.js" --min 2
```

Treat the output as candidates only. A signature appearing here has not
necessarily caused a prompt.

### 4. Present decisions, then apply

Show a table of proposed changes — rule, class, why, how often hit. Use
`AskUserQuestion` when more than two items need a call, one question per
non-obvious rule. Never widen the deny list without an explicit request.

Apply approved edits via the `/update-config` skill so array merge semantics
are respected. Preserve the literal `"$defaults"` as the first element of
`autoMode.allow` — dropping it silently discards every built-in allow rule.

### 5. Verify and clear

```bash
jq -e . "$HOME/.claude/settings.json" >/dev/null && echo "settings.json valid"
bash "$HOME/.claude/scripts/security/deny-check-test.sh"   # if present
: > "$HOME/.claude/logs/permission-denials.jsonl"          # only after applying
```

Clear the ledger **only** once decisions are applied, so an interrupted review
does not lose the evidence.

## Reporting

Per global instructions, headings state the verdict:

- `## 3 rules added, 1 left blocked on purpose`
- `## Nothing blocked this run`
- `## Hard deny hit twice: /x-wt-teams tried force-push`

Do not write a "nothing notable" section. If a class is empty, omit it.
