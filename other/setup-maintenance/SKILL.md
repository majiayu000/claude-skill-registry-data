---
name: setup-maintenance
description: Maintain and improve a Pi coding agent setup over time — prevent drift AND find new leverage. Use when auditing setup health, before adding a package/extension, before publishing, or when asked "is my setup healthy" / "audit my setup" / "how do I keep this sharp".
---

# Setup Maintenance

A setup that doesn't degrade is a setup with a maintenance discipline. This skill defines the cadence + the two loops: **maintenance** (prevent drift) and **improvement** (find new leverage). The one-command runner is `/setup-audit`.

## The two loops

**Maintenance loop — prevent drift.** Versions fall behind, new packages conflict, skills bloat, disk grows, AGENTS.md goes stale, extensions develop latent bugs. Without a check, you discover this when something breaks at the worst time.

**Improvement loop — find new leverage.** The Pi ecosystem ships new packages/features weekly. Other setups (cc10x, Archon, spences10, tomsej/pi-ext) invent techniques worth stealing. Without a scan, you plateau. This is the loop that turned a good setup into a best-contender.

## The cadence

| When | What | How |
| ---- | ---- | --- |
| **Monthly** | Full audit (both loops) | `/setup-audit` — fans out 6 subagents, writes a report |
| **On-add** (new package/extension) | Harmony re-audit | Read the new package's tools/commands/hooks/storage; check for collisions against existing packages + extensions (enumerate dynamically from settings.json + extensions dir). Reject if it duplicates an existing axis. |
| **Before-publish** (pushing my-pi) | Full audit + sync | `/setup-audit` → fix criticals → sync settings/extensions/skills to `~/Dev/my-pi` → commit + push |
| **On-extend** (new skill) | Coach coverage check | After adding a skill, grep `coach.ts` — does any intent route to it? If not, add a detector or it's unreachable via Coach. |

## The /setup-audit runner

`/setup-audit` dispatches 6 parallel read-only subagents:

1. **Version freshness** — installed vs latest for Pi core + all npm packages. Flags drift + deprecation.
2. **Harmony re-audit** — tool/command/hook/storage collisions across all packages + extensions. File:line evidence.
3. **Coach coverage scan** — lists EVERY command + skill, flags which Coach never routes to. **Each gap = leverage the setup has but doesn't surface.** This is the highest-value axis — it's how we found the wayfinder gap.
4. **Disk growth** — sessions, hermes DB, workflows, context sidecar. Flags unbounded stores > 100MB.
5. **AGENTS.md accuracy** — line count (must be < 200) + does it match reality.
6. **Ecosystem scan** — new Pi packages + public setups worth stealing from. Conflict-assessed.

Output: a report at `~/Dev/my-pi/docs/audits/setup-audit-YYYY-MM-DD.md` with health score per axis, critical/recommended/informational findings, Coach coverage gaps, ranked candidate steals, and ordered recommended actions.

## The on-add harmony gate (do this BEFORE installing any new package)

Before `npm install -g <pkg>` and adding it to settings.json `packages`:

1. **Read the package's main extension file** — what tools does it register? What hooks? What storage?
2. **Check against existing axes:**
   - Tool name collision? (grep all installed package manifests)
   - Command name collision?
   - Hook on the same event as an existing package? (ordering risk)
   - Storage path overlap? (same SQLite DB or directory?)
3. **Verdict:** install-clean / install-with-config / reject (duplicates an existing axis).
4. **If install-with-config:** determine the right load order in `packages` array (e.g. confirm-destructive before pi-hypa; context before pi-lens).
5. **After install:** runtime load test (`pi -p "ok" 2>err; grep -i error err`), verify 0 load errors.

The rule: **one axis, one owner.** If a new package duplicates an existing package's axis, reject it — no matter how popular. Harmony over capability.

## The improvement loop — how to steal well

When the ecosystem scan finds a candidate (a package, a setup, a prompt technique):

1. **Identify the steal precisely** — a specific technique, not "their setup is good."
2. **Check the axis** — does it duplicate something we have? (e.g. activeContext.md overlaps pi-hermes-memory → SKIP)
3. **Is it harmony-safe?** — steering text changes to loop.ts > new extensions > new packages (in order of risk).
4. **Verify before claiming done** — 0 LSP errors, 0 load errors, test the routing if it's Coach.
5. **Document the steal** — write to `docs/audits/` so the next audit knows what was considered + why.

## Don't

- Don't run `/setup-audit` and then skip the Coach coverage scan — that's the highest-value axis.
- Don't install a package without the on-add harmony gate. "It looked useful" is how conflicts arrive.
- Don't let AGENTS.md exceed 200 lines — every line is a token cost on every session.
- Don't prune skills just because they're old — prune because they stopped earning their system-prompt slot.
- Don't push the live `~/.pi/agent/` (not a git repo, contains secrets in auth.json/web-search.json/trust.json). Always sync to `~/Dev/my-pi` first.
