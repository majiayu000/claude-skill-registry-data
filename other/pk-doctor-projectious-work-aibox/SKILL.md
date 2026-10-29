---
name: pk-doctor
description: |
  Aggregator health-check for a processkit-managed repository. Runs a fixed suite of checks over the live context/ tree plus src/context/ drift, then resolves ERROR / WARN / actionable INFO findings by default. Use when the user invokes `/pk-doctor`, asks "is this repo healthy", or has just finished an upgrade and wants a sanity pass. Info-only mode is opt-in: stop after the report only when the user explicitly says info-only, dry-run, report-only, check-only, or no fixes.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-pk-doctor
    version: "1.0.0"
    created: 2026-04-20T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Emit the single `doctor.report` LogEntry per run (the audit trail for every invocation).
      - skill: migration-management
        purpose: List pending migrations for the `migrations` check and apply them under `--fix`.
      - skill: index-management
        purpose: (future) surface index errors alongside doctor findings in Phase 2.
    commands:
      - name: pk-doctor
        args: "[info-only | dry-run | --category=... | --fix=... | --fix-all | --since=<ref> | --yes]"
        description: "Run health checks and resolve actionable findings by default."
    provides:
      mcp_tools:
        - run_pk_doctor
---

# pk-doctor

## Intro

`/pk-doctor` is the single user-visible health-check surface for a
processkit repository. It is the diagnostic and remediation entry point
you run after an upgrade, before a release, or any time you need to
answer the question "is this repo healthy?" in one command. The skill
pattern is deliberately modelled on `npm doctor`, `brew doctor`, and
`rustup doctor`, with one processkit-specific default: agents resolve
findings by default and stop at report-only mode only when the user
explicitly asks for info-only/dry-run output.

### Container/host boundary

`/pk-doctor`, `run_pk_doctor`, and `doctor.py` are the derived-project
health surfaces for the running development container. In aibox-derived
projects, agents must use these processkit surfaces from inside the
container for processkit repository, MCP, migration, context, and
runtime-health checks.

Host-side installer diagnostics belong to the owner/operator outside the
container. pk-doctor skill text, command text, MCP descriptions, and
findings must not direct an in-container agent to run host-side
orchestrator health checks. When a finding requires host installer repair
such as sync or rebuild, phrase it as an explicit host action for the
owner and keep the processkit-side fix generic.

Severity and actionability are separate contracts. `ERROR`/`WARN`/`INFO`
describe blocking severity; `action_required`, `action_kind`,
`default_agent_action`, `requires_user_confirmation`, and
`acceptable_resolution` tell agents what must happen next. A severity
downgrade is not a resolution. Clean means no blocking findings and no
unresolved actionable findings, or a durable disposition for every
actionable finding.

This skill is the Phase 1 landing. It started with four checks. Phase 2 and
Phase 3 add more checks, lift the aggregator into an MCP server, and
harden the `--fix` paths — each with their own WorkItem.

## Overview

### Invocation

```
/pk-doctor                              # check, then resolve actionable findings
/pk-doctor info-only                    # report only; do not resolve
/pk-doctor dry-run                      # synonym for info-only
/pk-doctor --category=schemas,migrations
/pk-doctor --fix=migrations             # script-level scoped fixer
/pk-doctor --fix-all                    # script-level fixers only; still review output
/pk-doctor --since=v0.18.2              # scope file-walk checks only
/pk-doctor --yes                        # non-interactive (auto-confirms safe fixes)
```

The MCP wrapper accepts the same confirmation explicitly as
`run_pk_doctor(fix="...", yes=true)`. Calls without `yes=true` remain
detect-only when a category requires confirmation.

The script flags `--fix` and `--fix-all` are mutually exclusive. Exit
code is `0` if no ERRORs were produced, `1` otherwise. Every script run
— regardless of outcome — writes exactly one `doctor.report` LogEntry
via the event-log MCP.

### Default remediation workflow

When a user invokes `/pk-doctor` or asks to check repository health, the
agent must treat remediation as the default:

1. Run `run_pk_doctor()` or the local `doctor.py` report.
2. Build a queue of every `ERROR`, every `WARN`, and every finding whose
   `action_required` is true, including actionable INFO findings.
3. Resolve safe local fixes immediately through the owning script,
   command, or MCP tool. Use the reported `fix_mcp_tool`,
   `suggested_fix`, `action_kind`, and `default_agent_action` fields to
   choose the narrowest correction.
4. For migration findings, route through migration-management. Apply or
   continue unambiguous migrations; reject malformed no-op migrations
   only when the finding itself identifies the defect and a rejection
   reason is clear. Ask the user only when the migration changes policy,
   deletes data, has unclear intent, or conflicts with local work.
5. For archive, policy, external-dependency, or user-confirmation
   findings, either resolve them if the fix is already known and
   non-destructive, create/link tracking when the finding calls for
   tracking, or ask a concise question when a human decision is required.
6. Rerun pk-doctor after remediation and report the final ERROR/WARN and
   action totals.

If the user explicitly says "info only", "dry run", "report only",
"check only", "no fixes", or equivalent, stop after the report and do
not mutate anything. In that mode, still highlight the concrete next
actions so the report is actionable.

### The four Phase 1 checks

1. **`schema_filename`** — walks every `context/<kind>/**/*.md`. Loads
   the matching schema from `src/context/schemas/<kind>.yaml` (the LIVE
   source, never the template mirror) and validates the file's frontmatter
   against it. Also checks that the filename stem equals `metadata.id`
   and that any date encoded in the filename matches `metadata.created`.
   Phase 1 is WARN-only for rename suggestions — no auto-fix.
2. **`sharding`** — logs must live under `context/logs/YYYY/MM/` subdirs;
   migrations must live under their `spec.state` subdir (`pending/`,
   `in-progress/`, `applied/`). WARN on any file in the wrong bucket.
3. **`migrations`** — calls
   `mcp__processkit-migration-management__list_migrations(state="pending")`.
   INFO for the pending count; WARN for any pending entry older than
   14 days. Under `--fix=migrations` or `--fix-all`, interactively
   prompts `Apply MIG-xxx? [y/N/s]` per entry and invokes
   `apply_migration` on yes.
4. **`drift`** — subprocess-invokes `scripts/check-src-context-drift.sh`
   from the repo root. Exit 0 → one INFO "trees in sync". Exit 1 →
   one WARN per offending line reported by the script.
5. **`commands_consistency`** — walks every
   `context/skills/*/*/SKILL.md` and verifies that each entry in
   `metadata.processkit.commands:` has a matching `commands/<name>.md`
   file alongside the SKILL.md, uses the reserved `pk-` prefix, and has
   matching `argument-hint` frontmatter. When `.claude/commands/` or
   `.agents/skills/` exists, it also verifies those harness projections
   exactly match the canonical command set.

Additional checks added after Phase 1:

- **`team_consistency`** — wraps `team-manager.check_all()`.
- **`team_member_exports`** — reconciles active TeamMembers under `context/team-members/` with Claude sub-agent export files under `.claude/agents/<slug>.md` (the path emitted by `team-manager.export_claude_subagent`). Emits WARN per active TeamMember missing an export (harness can't dispatch as `subagent_type`) and WARN per stale export whose slug no longer maps to an active TeamMember; INFO when the roster and the export dir are in sync. Detect-only — fix is to re-run `export_claude_subagent` (or `export_claude_subagents`) or delete the stale file. Lands the harness signal half of the sub-agent-dispatch clause from BACK-20260509_1317-WildPanda.
- **`release_integrity`** — see DEC-20260422_1348-SnowyWolf-local-only-release-bulletproofing.
- **`mcp_config_drift`** — reads `context/.processkit-mcp-manifest.json`
  (produced at release time by `scripts/generate-mcp-manifest.py`) and
  recomputes the per-skill `mcp-config.json` sha256es. A missing manifest
  or stale aggregate surfaces as WARN (run the generator). In a
  derived-project context (`aibox.lock` + `.mcp.json` both present at
  the repo root), any processkit server missing from `.mcp.json`'s
  `mcpServers` map surfaces as ERROR with an explicit host-action hint
  asking the owner to re-run the project installer/sync tool outside the
  container. Exists because some host installers gate `.mcp.json`
  re-merge on processkit version delta only, so per-skill MCP-config
  edits within a release cycle may not reach derived projects until the
  next version bump — see DEC-20260423_2049-VastLake.
- **`server_header_drift`** — walks every `context/skills/processkit/*/mcp/server.py`,
  hashes its PEP 723 inline metadata block (`# /// script` ... `# ///`),
  and compares against the manifest's `per_server_header` baseline. WARN
  on any drift listing the affected skill slugs — signal that someone
  edited a dep header without regenerating the manifest, and the harness
  needs a restart to pick up the new deps. Detect-only; the fix is
  user-driven (regenerate manifest + restart harness). Per
  DEC-20260424_0127-QuickPine (SharpBrook split, RapidSwan ships the
  dep-drift half).
- **`preauth_applied`** — compares
  `context/skills/processkit/skill-gate/assets/preauth.json` against
  `.claude/settings.json` and `.codex/config.toml`. WARNs when aibox has
  not merged processkit MCP preauthorization into either harness config,
  which is the common cause of reauthorization prompts after container
  rebuilds.
- **`context_consumption`** — emits an INFO-only estimate of processkit
  context footprint by group (`startup`, command adapters, skill docs,
  MCP configs) using `ceil(utf8 bytes / 4)` as the provider-neutral
  token heuristic. It is intentionally not an MCP tool, so measurement
  does not add another tool schema to the harness context.
  It also exposes a local checkpoint/report CLI:
  ```sh
  python context/skills/processkit/pk-doctor/scripts/checks/context_consumption.py checkpoint <label>
  python context/skills/processkit/pk-doctor/scripts/checks/context_consumption.py report <before> <after>
  ```
  Checkpoints are JSON files under
  `context/.state/context-consumption/checkpoints/`. Reports compare
  observed processkit payloads and label token counts as local estimates,
  not provider-billed usage.
- **`v2_contracts`** — validates v2 API contract invariants across WorkItem, Binding, Artifact, and LogEntry entities. Catches process-instance definitions missing their definition reference, time-window bindings without a recurrence rule, orphaned cost-policy artifacts (not bound to a budget), policy supersession chains with breaks, uncalibrated eval-spec judges, and stale or missing agent-card projections. Emits ERROR for all contract violations; detect-only.
- **`context_hygiene`** — validates artifact naming policies (model-spec and model-profile use timestamped `ART-YYYYMMDD_HHMM-*` scheme), model binding integrity (role/TeamMember defaults must target provider-neutral model-profile artifacts unless marked direct_model_pin), and cross-reference health. Also detects demoted schema kinds still present in src/, detects archive candidates, warns on mixed binding filename styles, and checks sqlite-vec semantic index health. Emits WARN / ERROR depending on severity; detect-only.
- **`sensitive_data` allowlist** — intentional public or synthetic email
  addresses may be listed in `.pk-doctor-allowlist.toml`:
  ```toml
  [sensitive_data.email_allowlist]
  addresses = ["info@projectious.work", "deploy@example.local"]
  ```
  The allowlist applies only to email-address findings; secrets and other PII
  are never suppressed.
- **`runtime_health`** — owns in-container runtime probes that host-side
  installer diagnostics cannot verify directly. Checks lnav availability
  for the Prefix L structured log viewer, sqlite-vec import/load health
  in the pk-doctor/MCP runtime, Codex bubblewrap sandbox smoke status
  when Codex is enabled, PID 1 sleep-infinity hygiene, cgroup
  memory/pid/OOM pressure, processkit Python MCP process counts,
  PowerKit image/plugin tree, status plugin scripts, local render
  helpers, and runtime-home write probes. Emits WARN only for
  container-local actionable failures; host-only runs emit a skip INFO.
- **`entity_storage_hygiene`** — validates local `context/`
  storage policy separately from template freshness: unmanaged host
  artifacts, demoted legacy roots such as `context/models/`,
  root-level migration briefings, mixed root/sharded entity layouts,
  mixed filename policies, placeholder `0000` timestamps, and
  TeamMember private/slug policy explanations. Emits WARN for
  actionable storage drift; legacy layouts and mixed filename policies
  are migration work. `storage.root-migration-briefings` can be
  auto-resolved via `--fix=entity_storage_hygiene` by archiving
  non-completed CLI migration briefings.
- **`schema_vocabulary`** — validates closed-vocabulary subtype fields across v2 entities by comparing frontmatter values against Schema-declared known-kinds/known-types (Artifact kind, Binding type, WorkItem type, LogEntry event_type, Migration kind). `legacy_known_*` schema fields are not accepted as a terminal state; legacy values require an explicit data-fix Migration or a schema migration. Also validates that Migration entities include required v2 version metadata fields. Emits ERROR for unknown vocabulary values or missing version fields; detect-only.
- **`migration_integrity`** — flags malformed pending migrations that exhibit the "empty-baseline" defect (same-version migrations with content in affected_groups/affected_files despite no-op intent, or affected_groups populated but affected_files empty). Per BACK-20260425_1711-CleverRiver, both patterns are defect signatures. Emits WARN with suggested fix to reject via migration-management MCP and refile the upstream bug; detect-only.
- **`mcp_gateway`** — reports processkit-gateway MCP config health and harness registration state. Validates gateway config presence/structure at `context/skills/processkit/processkit-gateway/mcp/mcp-config.json`, checks env vars and command launch target, detects mixed gateway+granular server registrations in `.mcp.json`, and warns on insecure daemon bindings. Emits INFO on healthy state, WARN on minor gaps (missing proxy --url, nonlocal daemon bind), ERROR on parsing failure; detect-only.
- **`skill_dag`** — builds the skill-dependency directed-acyclic-graph (DAG) from `metadata.processkit.uses[*].skill` entries in every `context/skills/**/SKILL.md` and validates references exist, graph is acyclic, and layer constraints are honored (skill layer N only uses skills with layer ≤ N). Emits ERROR for missing references, cycles (with full path), or layer violations; detect-only.
- **`v1_entity_drift`** — walks every registered v2 entity directory under `context/` and surfaces files whose frontmatter still declares `apiVersion: …/v1`. Emits WARN per file with a hardcoded successor table (Actor→TeamMember, Process→Scope+Gate, StateMachine→lifecycle metadata, Model→Artifact(model-spec)); v1 files in append-only buckets (`context/logs/`, `context/migrations/applied/`) are downgraded to a single INFO since they are intentionally historical. Under `--fix=v1_entity_drift` (or `--fix-all`) the check interactively records `apply_migration` intents when a pending v1->v2 Migration already covers the target, otherwise records `propose_migration` intents — it never auto-creates migrations or hand-edits files. Per BACK-20260509_1318-KindSpruce.
- **`agents_md_hygiene`** — validates the derived-project startup
  policy surface. Checks root `AGENTS.md` for `pk-managed:*` blocks
  (`pk-compliance-contract-v2`, `pk-commands`), compares managed block
  content against `src/AGENTS.md` or the latest template when available,
  verifies processkit references for session start, skill routing,
  entity IO, migrations, decision capture, sub-agent dispatch,
  TeamMember/model binding, MCP topology, provider pointer files, and
  command blocks, and flags stale guidance such as legacy actor roots,
  `spec.x_aibox`, model-tier role tables, or duplicated provider-specific
  policy. WARN findings include a `briefing` payload for a project agent
  to reconcile the file after processkit upgrades. Detect-only; managed
  block replacement and local policy merges remain user-reviewed.
- **`sensitive_data`** — scans tracked text/config files for
  deterministic high-signal secret and personal-data patterns: private
  key blocks, provider tokens, JWTs, URL credentials, assigned
  high-entropy secret values, email addresses, phone numbers, SSN-like
  values, and credit-card-like numbers with a valid Luhn checksum.
  Deterministic secret findings are ERROR/WARN and require human
  confirmation because the correct response may be rotation, redaction,
  migration, or explicit policy acceptance. The check also emits one
  INFO `sensitive-data.probabilistic-briefing` that tells the
  derived-project agent what regex cannot prove: real names and aliases,
  addresses, dates of birth, customer/account IDs, medical/financial/
  employment data, screenshots, archives, database dumps, logs, and
  non-standard short secrets. The briefing includes non-triggering
  deterministic and probabilistic example prompts so an agent knows what
  to search for without adding realistic secrets to the shipped scanner.
  This is an advisory layer, not a complete DLP engine.
- **`supply_chain`** — performs offline supply-chain hygiene checks for
  dependency manifests/lockfiles, license policy, and local scanner
  outcomes:
  - emits `ERROR` on denied licenses, missing application lockfiles, and
    high/critical vulnerabilities;
  - emits `WARN` on unknown/review/allowed-policy misses and skipped
    security scanners;
  - emits `INFO` for inventory counts and SBOM discoveries.
  Security/outdated/supplier-quality checks stay advisory and require
  explicit core-surface opt-in data; pk-doctor performs no outbound
  network calls during this check.

### What doctor will NEVER do

- Hand-edit any file under `context/`. All writes route through the
  appropriate MCP tool (e.g. `apply_migration`).
- Touch `context/templates/` (read-only diff baseline).
- Touch `.mcp.json` (merged file; use the generated per-skill
  `mcp/mcp-config.json` and gateway catalog instead).
- Write to `context/logs/` directly — reports go through
  `mcp__processkit-event-log__log_event`.
- Treat a clean severity tally as done while actionable INFO findings
  remain unresolved.
- Stop after the report unless the user explicitly asked for info-only,
  dry-run, report-only, check-only, or no-fix behavior.

### Report shape

After the stdout human-readable summary, the skill emits a single
`doctor.report` LogEntry:

```json
{
  "event_type": "doctor.report",
  "summary": "/pk-doctor --fix=migrations — 0 ERROR / 2 WARN / 3 INFO",
  "details": {
    "doctor_version": "1.0.0",
    "invocation": "/pk-doctor --fix=migrations",
    "categories": {
      "schema_filename": {"ERROR": 0, "WARN": 1, "INFO": 140},
      "sharding": {"ERROR": 0, "WARN": 0, "INFO": 1},
      "migrations": {"ERROR": 0, "WARN": 1, "INFO": 1},
      "drift": {"ERROR": 0, "WARN": 0, "INFO": 1}
    },
    "action_totals": {
      "actionable": 2,
      "needs_user_confirmation": 1,
      "needs_tracking": 0,
      "safe_fix": 1,
      "migration_needed": 1,
      "archive_needed": 0,
      "policy_decision_needed": 0,
      "external_dependency": 0
    },
    "top_findings": [
      {
        "severity": "WARN",
        "id": "migration.stale-pending",
        "entity_ref": "MIG-...",
        "message": "...",
        "action_required": true,
        "action_kind": "migration_needed",
        "default_agent_action": "create_migration",
        "requires_user_confirmation": true,
        "acceptable_resolution": "migrated"
      }
    ],
    "fixes_applied": [],
    "duration_ms": 2340
  }
}
```

`top_findings` caps at 20 to keep the log entry compact; the full
stdout report remains authoritative for the details of a specific run.
The structured JSON payload returned by `run_pk_doctor` includes the
same `action_totals` and actionability fields on every finding.

### Interactive prompts

Interactive prompts gate on `sys.stdin.isatty()`. If a `--fix` was
requested but the process isn't attached to a terminal, the skill emits
a `WARN` (`fix.non-interactive`) and skips the fix — it does not silently
prompt and hang. `--yes` auto-confirms every prompt except any marked
`data_loss=True` (none in Phase 1, but the hook is present).

### `--since` scope

`--since=<git-ref>` restricts only the file-walk checks
(`schema_filename`, `sharding`). The `migrations` and `drift` checks
always run full-scan: migrations pull from an MCP tool with its own
state, and drift compares entire trees.

### Resolved policy defaults

These were agreed with the owner during shape review:

- **YAML-datetime vs JSON-Schema string coercion** failures surface as
  `WARN schema.datetime-coercion` (not ERROR). Parser-layer quirk.
- **Command projections** — canonical command adapters live under
  `context/skills/**/commands/`; slash-capable harness projections live
  under `.claude/commands/`; natural-language command shims live under
  `.agents/skills/`. `src/context/` mirrors only the canonical source.
- **Filename auto-rename** — WARN only in Phase 1. Phase 2 adds
  orchestrated rename + reindex.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Confusing remediation mode with blind `--fix-all`.** The skill is
  remediation-first by default, but that does not mean `doctor.py
  --fix-all --yes` is safe. First run the report, read actionability,
  then apply the narrowest known fix through the owning tool. Ask only
  when a finding is destructive, policy-sensitive, external, or unclear.
- **Stopping after a report when the user did not ask for info-only.**
  `/pk-doctor` means "check and clean up what can be cleaned up." If the
  user only wants a briefing, they must say info-only, dry-run,
  report-only, check-only, or no fixes.
- **Treating drift warnings as noise.** The drift check exists because
  v0.15.0–v0.18.0 shipped four releases with silent drift. If the
  drift check produces a WARN, it has found a real divergence —
  do not dismiss without investigating.
- **Hand-editing files to "clear" a doctor warning.** Doctor warnings
  are diagnostic. Fixing the underlying cause through the right MCP
  write tool (not by editing the offending file directly) preserves
  the audit trail. A WARN that reappears next run is more useful than
  a hand-fixed tree with no record of the fix.
- **Validating against `context/templates/` schemas.** The template
  mirror is a diff baseline, not the live schema source. Validation
  must read `src/context/schemas/<kind>.yaml` — the authoritative
  copy. Validating against templates will produce stale false
  positives after any schema evolution.
- **Forgetting the `doctor.report` LogEntry on dry-run.** Even a
  detect-only run must emit the report: it is the audit record of the
  invocation. A run that prints to stdout but logs nothing strands
  the next session with no record of what was checked.
- **Running doctor mid-migration.** Doctor's `migrations` check will
  list pending migrations and (under `--fix`) offer to apply them. If
  you are already in the middle of a manual migration review, running
  `--fix=migrations` can reorder work silently. Finish or pause the
  manual review first.

## Full reference

### CLI contract

```
doctor.py [--category=LIST] [--fix=LIST | --fix-all] [--since=REF] [--yes]
```

| Flag           | Meaning |
|----------------|---------|
| `--category`   | Comma list of categories to run. Default: all four. |
| `--fix`        | Comma list of categories to enable fixes for. Mutex with `--fix-all`. |
| `--fix-all`    | Enable fixes for every category that supports them. Mutex with `--fix`. |
| `--since`      | Git ref; restricts `schema_filename` + `sharding` to files changed since. |
| `--yes`        | Auto-confirm all non-`data_loss` fix prompts. |

### Adding a check in Phase 2

1. Drop a new module in `scripts/checks/<name>.py` exporting a
   `run(ctx) -> list[CheckResult]` function (and optional
   `run_fix(ctx, results) -> list[dict]`).
2. Register it in `scripts/checks/__init__.py` in `REGISTRY`.
3. Add a gotcha for that check here in SKILL.md.
4. Mirror both files into `src/context/skills/processkit/pk-doctor/`.

The aggregator in `doctor.py` does not need to change.

### What this skill does NOT do (yet)

- Validate cross-references (Phase 2).
- Check `PROVENANCE.toml` drift (Phase 2).
- Check `mcp-config.json` integrity (Phase 2).
- Smoke-import MCP servers (Phase 2).
- Detect version skew between `aibox.lock` and installed SKILL.md pins
  (Phase 2).
- Expose itself as an MCP server for machine invocation (Phase 3, only
  if demand shows up).
