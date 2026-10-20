---
name: deprecation-and-migration
description: Plan or implement retirement of a system, API, feature, persisted configuration, or database shape. Use for compatibility cutovers, explicit deprecation review, or an explicit unreleased replacement decision, including determining whether consumers or data exist; not ordinary dependency bumps, local renames, prose edits, or generic architecture discussion.
license: MIT
---

# Deprecation and Migration

Choose the smallest safe removal path from actual consumers and retained data.
Keep analysis, repository edits, deployment, external communication, and data
destruction within the existing task authorization; a migration plan grants none
of those effects by itself.

1. Inventory consumers, owners, versions still running, persisted data and config,
   and observable behavior they depend on. Establish the reason for retirement,
   replacement or intentional loss of functionality, and compatibility boundary.
   For unreleased code with no external consumers or retained data, use direct
   replacement and existing checks rather than a staged migration framework.
2. Order the cutover around actual coexistence requirements. When old and new
   versions must run together, keep both valid at each phase. For schema changes
   that need it, expand additively, backfill in bounded batches, switch reads and
   writes with verification, then contract after old consumers are gone. Use
   adapters, dual writes, or flags only where that coexistence requires them.
3. Specify each phase's prerequisite, change, verification, owner, and recovery
   action. Check output correctness and retained data, not just zero code hits.
   Reuse existing fixtures and migration tooling. State how retries remain safe
   and how partial backfills or interrupted cutovers resume.
4. Distinguish reverting code from recovering data. Test recovery where possible;
   for irreversible changes, state what is lost, the backup/restore or forward
   recovery path and its limits, and any required authorization before proceeding.
   Never claim a down migration can recover destroyed data without evidence.
5. Define deletion conditions: supported consumers have switched, required data
   is preserved or its loss authorized, compatibility/recovery checks pass, and
   the observation window required by the task is complete. Remove obsolete
   code, tests, config, and docs only when those conditions hold. Keep customized
   user configuration unless its migration is explicitly authorized.

Finish with consumer/data inventory, cutover order, verification and recovery
per phase, deletion conditions, and unresolved blockers. Completion means the
requested planning or implementation phase is evidenced; a written plan is not
proof that a production migration or retirement happened.

Adapted from Addy Osmani's [deprecation-and-migration](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/deprecation-and-migration/SKILL.md), under the [MIT license](LICENSE).
