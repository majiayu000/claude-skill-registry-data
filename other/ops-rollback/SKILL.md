---
name: ops-rollback
description: Revert AICP/fleet to a recorded last-known-good state — uses the rollback contract that `ops-deploy` Operation 4 records (commit SHA + image tags + profile name in `docs/DEPLOY-LOG.md` and `/tmp/predeploy-*-<env>.txt`). Preserves the failed-state evidence first, executes the revert, smokes the result, then updates the log + hands off to `ops-incident` for diagnosis. Distinct from `ops-incident` (active response — rollback is one tool incident may use) and `ops-deploy` (forward action — this skill is the explicit reverse). Loads when the operator says "rollback", "revert the deploy", "go back to last good", "undo the release", "this deploy is broken — back it out".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# ops-rollback

The reverse-the-deploy skill. Reads the rollback contract that `ops-deploy` recorded, snapshots failed-state evidence, executes the reversion, verifies recovery, updates the deploy log. Distinct from `ops-incident` (broader incident process — rollback may be one of several tools an incident uses) and from `ops-deploy` (forward action with gates — this skill is its explicit reverse).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "rollback", "revert the deploy", "go back to last good", "undo the release", "back out the change", "deploy was bad — revert".
- **Within an incident**: `ops-incident` Operation 1 identified that the active deploy is the cause; rollback is the chosen restoration mechanism.
- **Post-deploy regret**: deploy succeeded smoke tests but is now showing problems in metrics — the operator wants to revert before the problem grows.

Do NOT load when:

- Multiple things are broken with unclear cause — load `ops-incident` first; rollback is one option there.
- The current deploy is the right code; rollback would just regress to a different problem — load `ops-incident` to find a forward fix.
- Operator wants to revert a single commit (not a deploy) — that's a `git revert` workflow, not this skill.
- No prior deploy was recorded — there's nothing to roll back TO; load `ops-incident` for restoration via other means.
- The "rollback" is a config change (profile switch, env var revert) — load `config-deploy` for surgical config reversion.

## Operations

This skill has 4 named operations. Execute in strict order — preservation of evidence comes BEFORE reversion.

### Operation 1: Identify the rollback target + verify it's good

**Trigger**: skill loaded; operator named the environment to roll back (or single-environment deployment is implied).

**Process**:

1. Find the rollback contract recorded by the prior `ops-deploy`:
   ```bash
   ls /tmp/predeploy-*-<env>.txt 2>/dev/null
   tail -5 docs/DEPLOY-LOG.md   # last successful deploys
   ```
   Capture: previous commit SHA, previous image tags, previous profile name.
2. If no contract exists (skill being run cold without a prior `ops-deploy`):
   - Look for the last successful deploy in `docs/DEPLOY-LOG.md` to identify the SHA.
   - If no log either: identify last-known-good by `git log` + operator confirmation. Don't pick blindly.
3. Verify the rollback target is ACTUALLY good (don't roll back to another broken state):
   ```bash
   git log -1 --format="%H %s %ci" <target-sha>
   # confirm: this SHA was the deployed-and-smoked state, not a half-deployed step
   ```
   If the target's deploy log entry says `status=ok`, it's verified. If `status=failed` or no entry, escalate — operator must pick a different target.
4. Compute what specifically will change on rollback:
   ```bash
   git diff --stat <target-sha>..HEAD       # files that will revert
   git log --oneline <target-sha>..HEAD     # commits that will be undone
   ```
   Surface this to operator: "rolling back N commits across M files; the changes you're undoing are: [list]". Get explicit confirmation before proceeding.
5. Identify migration / state implications — the data class of "irreversible":
   - Any DB schema migration in the diff? (AICP has no SQL; fleet projects might.) If yes, rollback may strand data. Surface and pause.
   - Any config that changed file paths, retention windows, encryption keys? Rolling back doesn't unmove files or undelete state.
   - Any LocalAI Collection re-indexing? Rolling back doesn't undo that work but may make the new index incompatible.

**Quality bar (Operation 1 done when)**:

- [ ] Rollback target SHA + image tags + profile name explicitly identified.
- [ ] Target verified as last-known-good (deploy log entry or operator confirmation).
- [ ] Diff/log preview shown to operator with commit list + file count.
- [ ] Operator explicitly confirmed (not implied) — rollback is destructive of forward work.
- [ ] State-irreversibility implications surfaced: migrations, file moves, re-indexes.

### Operation 2: Preserve failed-state evidence

**Trigger**: Operation 1 confirmed; rollback is about to mutate state.

**Process**:

1. Snapshot the failed-state — same shape as `ops-incident` Op1 (this skill is reusing that pattern):
   ```bash
   ts=$(date -u +%FT%TZ); mkdir -p /tmp/rollback-$ts
   docker compose ps > /tmp/rollback-$ts/compose-ps.txt
   docker compose logs --tail 500 > /tmp/rollback-$ts/logs.txt 2>&1
   .venv/bin/aicp --check > /tmp/rollback-$ts/aicp-check.txt 2>&1
   .venv/bin/aicp --dlq-status > /tmp/rollback-$ts/dlq.txt 2>&1
   git log --oneline -10 > /tmp/rollback-$ts/recent-commits.txt
   git diff <target-sha>..HEAD > /tmp/rollback-$ts/diff-being-undone.diff
   ```
2. Capture the FAILING commit SHA (current HEAD before rollback) — needed for `ops-incident` to diagnose root cause AFTER service is restored:
   ```bash
   git rev-parse HEAD > /tmp/rollback-$ts/failed-sha.txt
   ```
3. If runtime state is at risk (e.g., DLQ entries, in-flight tasks): copy them to the snapshot dir before any restart:
   ```bash
   cp -r ~/.aicp/dlq/$(date +%Y-%m-%d).jsonl /tmp/rollback-$ts/ 2>/dev/null
   cp .aicp/state.yaml /tmp/rollback-$ts/ 2>/dev/null
   ```

**Quality bar (Operation 2 done when)**:

- [ ] `/tmp/rollback-<ts>/` exists with logs + ps + check + dlq + recent-commits + diff.
- [ ] Failed SHA captured to file (preserves identity through rollback).
- [ ] Runtime state copied if at risk.
- [ ] Snapshot completed BEFORE any rollback mutation.

### Operation 3: Execute the rollback

**Trigger**: Operation 2 evidence preserved.

**Process**:

1. Move the code:
   ```bash
   git checkout <target-sha>
   # or for branch-tip rollback:
   git reset --hard <target-sha>   # only if operator explicitly authorized destructive (rare; checkout is preferred)
   ```
   Prefer `git checkout` (detached HEAD) for safety; the operator can later branch off it. `reset --hard` only on explicit authorization — it can lose unpushed commits in environments where this checkout could lose work.
2. Move the profile if rollback contract included one:
   ```bash
   make profile-use PROFILE=<previous-profile>
   ```
3. Rebuild + restart services:
   ```bash
   docker compose build 2>&1 | tail -10
   docker compose up -d 2>&1 | tail -10
   ```
   Use `up -d` (not `--no-deps`) — env vars and shared config likely changed alongside the rollback.
4. Watch logs for first 30 seconds — same pattern as `ops-deploy` Op2:
   ```bash
   docker compose logs -f --tail 50 --since 30s &
   sleep 30; kill $!
   ```
5. If rollback itself fails (rolled-back code doesn't boot): this is an emergency. Either roll FURTHER back (to an even earlier known-good), or invoke `ops-incident` because the system has no known-good.

**Quality bar (Operation 3 done when)**:

- [ ] Code moved to target SHA (verified by `git rev-parse HEAD`).
- [ ] Profile activated if part of rollback contract.
- [ ] Compose services rebuilt and up.
- [ ] No service in `Restarting` state.
- [ ] No FATAL or "Exited" entries in first-30s logs.

### Operation 4: Smoke + log + handoff

**Trigger**: Operation 3 reverted state running.

**Process**:

1. Smoke test the rolled-back system — same shape as `ops-deploy` Op3:
   ```bash
   docker compose ps --format json | jq -r '.[] | "\(.Name): \(.State) (\(.Health // "no-healthcheck"))"'
   .venv/bin/aicp --check 2>&1 | head -20
   .venv/bin/aicp --backend local --prompt "say ok" 2>&1 | tail -5
   ```
   All services healthy + golden-path inference responds = rollback succeeded.
2. Update `docs/DEPLOY-LOG.md` with the rollback entry:
   ```
   <ts> deploy=<env> sha=<target-sha> status=rollback by=<op> reverted-from=<failed-sha> reason="<one-line>"
   ```
3. Notify operator surfaces:
   - ntfy: `ROLLBACK <env> reverted <failed-sha> → <target-sha> dur=<minutes>`
   - Mission Control / standing-orders update if fleet was affected.
4. Hand off to `ops-incident` for diagnosis:
   - The failed-state snapshot in `/tmp/rollback-<ts>/` is the evidence.
   - The diff in `diff-being-undone.diff` is the change set to investigate.
   - Tell operator explicitly: "service restored via rollback; load `ops-incident` to identify root cause and author durable fix before re-deploying."

**Quality bar (Operation 4 done when)**:

- [ ] All services smoke-test green at the rolled-back state.
- [ ] `docs/DEPLOY-LOG.md` updated with rollback entry naming both target and failed SHAs.
- [ ] Notification sent (ntfy / MC / explicit "no notification surface configured").
- [ ] `ops-incident` handoff explicitly stated to operator with snapshot path.
- [ ] No half-rolled-back state remaining (no service still on the failed image, no profile still on failed config).

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Rolling back to another broken state

Operator says "rollback to last week's deploy". Skill picks the SHA from a week ago — but that deploy was ALSO rolled back at the time, and the `status=ok` entry is the one from 9 days ago. Skill rolls back to a known-broken target; service stays broken; operator now has TWO incidents to debug.

**The rule**: Operation 1 step 3 verifies the target by reading `docs/DEPLOY-LOG.md` for `status=ok`. If the most recent entry for the target SHA is `status=failed` or `status=rollback`, that SHA is NOT a valid rollback target — keep walking back the log until a confirmed-good is found, or escalate to operator.

### Gotcha 2: Rollback wipes runtime state

Failed deploy added a new field to a config; operator's runtime now references entries with that field. Rollback reverts the config; on restart, the runtime crashes parsing entries that the rolled-back code doesn't understand. Rollback "succeeded" code-wise but the system is now broken in a new way.

**The rule**: Operation 1 step 5 surfaces state-irreversibility implications BEFORE rollback. If runtime state references the new code's shape, rollback alone isn't sufficient — either migrate state back or accept data loss. Don't rollback in the dark.

### Gotcha 3: Mutating before snapshotting

Same anti-pattern as `ops-incident` Gotcha 1: skill jumps to `git checkout <target>` without first capturing the failed-state. Logs that lived in the running container are gone after restart; the failed-state diff is unrecoverable; root cause is now a guessing game.

**The rule**: Operation 2 is non-negotiable. Snapshot to `/tmp/rollback-<ts>/` BEFORE any mutation in Operation 3. The five-second cost preserves the entire evidence base for `ops-incident` to use.

### Gotcha 4: `git reset --hard` loses unpushed forward work

Skill defaults to `git reset --hard <target-sha>`. But the operator had two un-pushed commits on the failed branch (a half-finished hotfix attempt that hadn't been committed cleanly). Reset destroys them; the operator's last 30 minutes of work are gone with no recovery.

**The rule**: Operation 3 step 1 prefers `git checkout <sha>` (detached HEAD). `reset --hard` is reserved for explicit operator authorization and is never the default. If the operator wants the branch tip moved, they say so AFTER the system is restored — restoration first, history surgery second.

### Gotcha 5: Rollback declared successful, root cause unidentified

Service is back; deploy log shows the rollback; operator moves on. But nobody loaded `ops-incident` — root cause is unknown, and the same broken deploy will be re-attempted next week with the same failure mode.

**The rule**: Operation 4 step 4 makes the handoff EXPLICIT. The rollback skill's job ends with "service restored AND `ops-incident` invoked-or-explicitly-deferred". If operator defers ("we'll diagnose later"), the deferral is logged in `docs/DEPLOY-LOG.md` (status=rollback diag-deferred), so the next deploy attempt has a record that the cause is unknown.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP rollback is mostly straightforward — code+config+profile, no schema migrations to worry about — because there's no SQL database. Sister fleet projects (openfleet, dspd, nnrt) may have schema migrations; this skill flags them in Op1 step 5 and stops if rollback would strand data. The rollback contract relies on `ops-deploy` having recorded predeploy state correctly; if the skill is run cold (no contract), `docs/DEPLOY-LOG.md` is the fallback source of truth. AICP profile YAMLs are part of the rollback contract — a deploy that activated `default` -> `personal` is incomplete to roll back without also reverting the profile.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| ops-deploy | Forward action with gates + recorded contract | Forward; this skill is its explicit reverse |
| ops-incident | Active incident response | Broader process; rollback is one mechanism this skill formalizes |
| config-deploy | Surgical config reversion (profile switch) | Just config; this skill reverts code+config+profile together |
| ops-maintenance | Routine upkeep | Preserves status quo; this skill is destructive of forward work |
| evolve-migrate | Cross-version foundation swap | Forward migration; this skill is reverse |
| incident-cycle | Compound incident → fix → prevention workflow | Compound; this skill is the rollback step within it |
