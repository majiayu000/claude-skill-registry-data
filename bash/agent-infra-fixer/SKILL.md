---
name: agent-infra-fixer
description: Fix the agent's own environment when skill-miner surfaces infra-class failures - broken or over-broad hooks, permission-mode denials, wrappers, sandboxing, expired CLI auth. Use when session mining shows hook errors ("No stderr output", repeated "BLOCKED" on legitimate commands), denied permissions, or environment breakage that no skill could fix. The rule is that infra failures get fixed in the environment, never worked around with skills.
---

# agent-infra-fixer

skill-miner classifies clusters as `infra` or `task`. Infra clusters come here.
No eval, no skill draft - reproduce, fix, verify, record.

## Process

1. **Reproduce.** Re-run the failing component on a triggering input. For hooks:
   pipe a realistic tool-input JSON into the hook script and check exit code AND
   which stream the message lands on.
2. **Fix the environment** (hook, wrapper, permission config), minimal diff.
3. **Verify with a trigger/benign pair**: the fix must fire on the bad input and
   stay silent on good input.
4. **Record** in `$FORGE_ROOT/ledger.jsonl` as `decision: "infra-fix"` so the next
   mining run can confirm the cluster count dropped.

## Known failure class: stdout-block hooks

PreToolUse hooks that print block reasons to **stdout** instead of **stderr**
surface to the agent as `hook error: No stderr output` - the block works but the
agent never sees WHY, retries, and the error count explodes. Exit code must be 2
with the reason on stderr.

Detector/fixer: for every `exit 2` in a `*.sh` hook, the echo / printf / `cat <<EOF`
lines of the same block get `>&2`; `--exit2` also turns a message + `exit 1` (which does
not block at all) into `exit 2`. Dry run prints a diff; `--apply` writes `.bak-stderr`
backups. Idempotent.

```bash
python3 scripts/fix-hooks.py --exit2                       # ~/.claude/hooks, diff only
python3 scripts/fix-hooks.py --hooks-dir /root/.claude/hooks --exit2 --apply
```

Then verify each fixed hook with a must-block input: exit 2 AND non-empty stderr.
2026-09-16: this class was the #1 mined cluster on both test machines (117 errors in
40% of one machine's sessions, 180 in 22 sessions on the other). The generic fixer
reproduces the six hand-made fixes byte for byte.

## Known failure class: over-broad guard patterns

A guard that blocks legitimate work is as costly as a missing guard: the agent loses a turn,
invents a workaround, and learns nothing. Substring patterns are the usual cause:
`rm -rf /` matches every `rm -rf /tmp/x`, `truncate` matches "truncated", `curl.*|.*sh`
matches `| head`, and heavy-task patterns match `pgrep`/`du` arguments, code strings and
commands already wrapped in `ssh <server> '...'`.

Replay every past block through the current hooks, and prove the guards still hold:

```bash
python3 scripts/replay-hook-blocks.py --must-block /path/to/local-guard-cases.txt [--dump DIR]
```

- `now passes`: the block no longer fires (fixed hook, or confirm it was a false positive).
- `still blocked`: inspect each reason; keep the true positives, narrow the rest.
- `must-block cases missed` must be 0. Verify guards negatively: loosening a pattern until
  `rm -rf ~` passes is worse than any false positive.
Keep guard test inputs outside the installed skill. The repository's negative-test
fixture is under `tests/agent-infra-fixer/` and is not part of this package.

Fix pattern: match what is EXECUTED, not text. Anchor destructive targets (`/`, `~`,
`$HOME`, `*` as the whole argument), allow `--force-with-lease`, parse command position
(skip heredoc bodies and quoted ssh payloads) for heavy-task rules.
2026-09-17 on one real machine: 135 blocks in 26 sessions, 129 were false positives; after the
rewrite 6 remain blocked (all true positives) and 0 must-block cases were missed.
Reference implementations: `examples/block-destructive.sh` and `examples/block-heavy-local.sh`
(set `DEV_SERVER`); both parse in python3 and read the hook JSON from stdin.
