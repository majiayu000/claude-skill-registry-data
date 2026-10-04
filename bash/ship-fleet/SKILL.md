---
name: ship-fleet
description: Use when anything under plugin/team-lead-fleet/ has been edited — a rule, a skill, a hook, an agent — and the change needs to reach peers. Also use when scripts/plugin_drift_check.py exits non-zero, or when a fleet rule that was merged does not appear to be firing.
user-invocable: true
---

# Ship Fleet

Whether an edit to `plugin/team-lead-fleet/` reaches anyone depends on **how each session resolved the plugin**, and that is not visible from the repo, the version number, or the drift check.

Two resolution modes exist on this machine at once:

- **Source-resolved** — the session runs the plugin straight out of the repo checkout. An edit is live at that session's next SessionStart. No version bump, no `claude plugin update`.
- **Cache-resolved** — the session runs a version-keyed copy under `~/.claude/plugins/cache/`. `claude plugin update` skips that copy when the version is unchanged, so edits reach it only after a version bump.

## Settled 2026-09-15: the fleet is cache-resolved, uniformly

The marketplace moved from the local directory `~/dev/ai-team-lead/plugin` to the GitHub repo `fryanpan/ai-team-lead`. There is no source-resolved path any more — every session reads a version-keyed copy under `~/.claude/plugins/cache/`, so **a version bump is always required** and an edit in the working tree reaches nobody until it is merged to `main` and pulled.

The probe below is kept because it is the way to confirm what a peer actually loaded, and because a peer can still be running an older cached version. But its two-modes framing is history: the answer to "which mode" is now always cache-resolved.

## The rule

**Determine resolution mode before you decide what shipping requires — and confirm delivery from a peer's own injected context, never from the repo.**

## The probe

Grep a peer's latest injected rules block for a string that exists in exactly one of the two copies. A file deleted from the repo but still in the cache is ideal: present means cache-resolved, absent means source-resolved.

Read the **latest injection only**. A transcript accumulates every SessionStart it has ever had, plus tool output and messages that merely mention the string. Counting matches across the whole `.jsonl` measures history, not current state — that error produced a confident, wrong fleet-wide claim on 2026-08-20.

```bash
python3 - "$TRANSCRIPT" <<'PY'
import json, sys
last = None
for line in open(sys.argv[1]):
    if 'team-lead-fleet rule:' not in line: continue
    o = json.loads(line)
    if o.get('type') != 'attachment': continue   # injections only
    last = json.dumps(o)
print('cache-resolved' if 'DELETED_FILE_NAME' in last else 'source-resolved')
PY
```

Filtering on `type == "attachment"` is what separates a real injection from the session talking about one.

## Confirming which hook body ran

Resolution mode can also be established positively: put a side effect in the repo copy of `hooks/session-start.sh` that the cached copy does not have — a line appending to a log — and check whether it fires. On 2026-08-20 that log had 88 entries while the cached hook contained no such line, which proves the source hook is what executes. A side effect present in only one copy beats any amount of inspecting both.

## Steps

1. **Probe resolution mode** for the peers you care about. It is per-session, not fleet-wide.
2. **If any peer is cache-resolved:** publish (scrub + squash onto main — this repo is public), bump the version in **both** `plugin/team-lead-fleet/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` **at the repo root**, then `claude plugin update team-lead-fleet@team-lead-fleet`. The two manifests have fallen out of step before; an unbumped version makes every later step a silent no-op.

   **The marketplace manifest is at the repo root, not under `plugin/`.** It moved there when the plugin started being served from GitHub, and this step named the old path for weeks afterwards — a path that does not exist, in the one step whose whole purpose is keeping the two versions in step. Following it literally bumps `plugin.json` alone, which is precisely the silent no-op the sentence warns about. Corrected 2026-09-17, both manifests confirmed at 0.9.0. **Check the path resolves before you edit it**; the file has moved once and can move again.
3. **Deliver into the session.** Rules arrive only through the SessionStart hook, so the peer needs a real SessionStart event: restart, `--continue` resume, `/clear`, or `/compact`. Verified from the hook payload log — it fires on `startup`, `resume`, `compact`, and `clear`, and nothing else.
4. **Re-probe.** Report shipped only after a peer's own injected context contains the new text.

## What to avoid

- **Don't infer current state from a whole-file grep.** It counts historical injections and incidental mentions. Read the last injection.
- **Don't assume the fleet is uniform.** Resolution mode is a per-session property; a peer respawned at a different time can differ from its neighbour.
- **Don't treat a respawn as delivery for a cache-resolved peer.** It re-reads the same stale cache and comes back looking healthy.
- **Don't rely on the drift check alone.** It compares repo to cache — which tells you nothing when nobody loads the cache. It also skips `github`-source plugins entirely.
- **Don't put this skill in the plugin.** A skill that ships the plugin must not be delivered by the mechanism it exists to fix.
