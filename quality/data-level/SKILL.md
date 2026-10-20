---
name: data-level
description: Audit how a project defines, protects and evolves its stored data against a 5-level scale (shape, integrity, versioning, migrations, retention), then propose options and split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Works on a copy, never on real data. Use when the user runs /data-level or asks to audit or improve a schema, data model, data integrity or migrations.
summary: Fix stored data shape, integrity and migrations
argument-hint: "[level 1-5] [audit|build] [compliance] [scope: store or entity]"
model: inherit
---

# Data level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **COMPLIANCE**: on only if the arguments contain `compliance`. When on, also check retention, consent and deletion duties under the regulation the user names. When off, do not raise these.
- **SCOPE**: any store, entity or path in the arguments limits the audit to it. Default: every place the product keeps data.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the data lead on this project. Work to the LEVEL. The levels describe how far the stored data can be trusted and safely changed, not which database is used. Keep the project's stores unless the user asks to change them.

## Boundaries

- Work on a copy. Never run a migration, repair or deletion against real data. Those steps are written out for the user to run, each with a way back.
- Never print personal or sensitive values. Describe data by shape, counts and redacted samples.
- Take a backup, and confirm it restores, before any step that changes stored data.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Stored.** Every kind of data has one known place and a recognisable shape. Names say what things are. Nothing is kept twice by accident.
2. **Structured.** The shape is written down explicitly and carries a version. The store itself enforces types and required fields. Identifiers and relationships are defined. Changes to the shape are scripted, not done by hand. No meaning is packed into free text or position.
3. **Trustworthy.** The store enforces integrity: uniqueness, valid references, allowed ranges. Writes that belong together succeed or fail together. Data is validated on the way in, and older versions are handled on the way out. Rules say how long data is kept and how it is deleted. Backups cover all of it. Personal data is identified. Shape changes can be undone and are tried on a copy first.
4. **Governed.** A data dictionary describes every field. Records that matter keep a history of changes. Regular checks confirm that totals and counts reconcile. Access is by role. Test and rehearsal copies hold no real personal data. Events collected for analysis have a defined shape. Growth is planned: indexes, archiving, size limits.
5. **Platform.** Origins and uses of every dataset are traceable. Quality is monitored continuously. Producers and consumers of data agree on contracts that are tested. Only choose this for a product where data is the main asset.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, design a shape or review their own work.

## Step 0: Data context

1. Look first. Find every place data is kept: databases, files, browser storage, caches, logs, exports. Read schema files, migrations and the code that reads and writes each. Read `LEVELS.md` if it exists and reuse the hosting, release and threat profiles.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **What matters most**: the data whose loss or corruption would hurt most.
   - **Real data today**: none yet / test data only / real data that must survive every change.
   - **Lifetime**: one session or event / months / years.
   - **Sensitivity**: nothing personal / names and contacts / money, health, minors or other protected data.

   Round two, only what still matters:
   - **Source of truth**: where copies of the same fact disagree, which one wins.
   - **What must reconcile**: totals, balances, counts or rankings that must always add up.
   - **Growth**: expected size over the product's life.
   - **Readers**: reports, exports, other systems or people that depend on the current shape.
   - **Past damage**: lost, duplicated or corrupted data, and what caused it.

3. Record unknown answers as unknown, assume the more careful case, and flag it.
4. Print a short data profile: each store, what it holds, how sensitive, how long it lives, what must reconcile. Wait for the user to confirm or correct it.

## Step 1: Audit (Opus)

1. Inventory. For each kind of data record: where it lives, its shape and version, every place that writes it, every place that reads it, and whether the same fact is kept elsewhere.
2. Check each against these categories. Cite file and line. Record sound, weak, or does not apply.
   - **Shape**: explicit or implied by code, versioned or not, fields with more than one meaning.
   - **Enforcement**: rules held by the store, or only by application code that can be bypassed.
   - **Identity and relationships**: stable identifiers, references that can dangle, duplicates.
   - **Atomicity**: related writes that can half-succeed, and what a crash between them leaves.
   - **Validation**: what is checked on the way in, and what happens on reading a bad or old record.
   - **Change**: how the shape has changed, whether changes are scripted, reversible and tried on a copy.
   - **Derived data**: stored totals or copies that can drift from their source.
   - **Retention and deletion**: what is kept forever by default, and whether deletion really removes it everywhere.
   - **Sensitive data**: where it is, who can read it, whether it leaks into logs, exports or test copies.
   - **Recovery**: whether backups include it and a restore returns a consistent state.
   - **Growth**: reads that slow as data grows, anything unbounded.
3. Integrity check, on a copy only. Count records that break the rules the product assumes: dangling references, duplicates, out-of-range values, totals that do not reconcile, records in an older shape. Report counts and redacted examples.
4. State the level the project is at now, with one line of evidence per requirement. Say what is sound and must be kept.
5. Rank the findings: data that can be lost or corrupted first, then existing damage, then exposed sensitive data, then changes that cannot be undone, then the rest.
6. For each of the top findings, give two or three distinct options. For each: what changes, what it costs (effort, migration risk, downtime, effect on readers), when it is the wrong choice. Mark the one you recommend. Prefer a rule the store enforces over a check in application code.
7. Add optional ideas from one level above the target, labelled as stretch.
8. If the target LEVEL is wrong for this product, say so and name the level you would pick.
9. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result, then follow the user's final call.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the work into sub-plans that can each be done and checked alone. One sub-plan changes one rule, one shape or one repair. No fixed count: let the size of the work set it. Do not pad and do not merge unrelated changes.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Files to change, and files it must not touch.
   - Exact steps, with names, types and rules. Leave no design decision to the executor.
   - For a shape change: the forward script, the backward script, and how existing records are carried over.
   - Done check: the tests to pass, and the integrity counts expected on a copy before and after.
   - Live step: none, or the exact command the user runs on real data, the backup to take first, and the way back.
   - Readers affected, and how each keeps working.
   - Dependencies, and Model with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: the data dictionary, a fully specified validation or constraint in code, test data, export scripts, documentation.
   - Sonnet when needed: shape redesign, atomic writes, repair of existing damage, anything touching several stores.
   - Migrations and repairs are never assigned to Haiku.
4. Order the sub-plans. Shape changes run in sequence. Mark what can run in parallel.

## Step 3: Delegation gate

1. Show a table: number, goal, files, live step or none, model, parallel or sequential.
2. Print: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List every live step separately, in order, with its backup and its way back. These need the user's explicit yes, and the user runs them.
4. Ask with AskUserQuestion: **Delegate as planned (Recommended)** / **Sonnet for all** / **Haiku where allowed** (migrations and repairs stay on Sonnet; name the sub-plans at risk) / **No delegation** (warn that every edit runs on the session's current model, which is Opus unless the skill said otherwise at the start).
5. Do not start until the user answers.

## Step 4: Execute

- Before each spawn, print one line: `Sub-plan 3 → Sonnet: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan and the relevant part of the data profile.
- Executors follow the Boundaries section. They work on files and copies only, never on real data, and never print sensitive values.
- An unclear or blocked sub-plan is reported back, not guessed. Rewrite it on Opus, or ask the user.

## Step 5: Review (Opus)

Run the full tests. On a copy, run every forward script, then every backward script, and confirm the data matches the starting state. Repeat the integrity check and compare counts. Confirm each reader still works. Report the level reached, findings closed and open, and the ordered list of live steps still waiting on the user. One corrective round, assigned the same way, then report the remainder. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** Read `LEVELS.md` at the start and reuse what it answers. At the end, update its data section with: the data profile, target and reached level, integrity counts, pending live steps, open findings, and the date. Never write real data values into it. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md` and update only this skill's row. Keep the format exact.

```
<!-- levels
data: 2/3 gaps=6
-->
```

**Handoffs from this skill.** Write paths in the server need changing: `backend-level`. Sensitive data is exposed: `security-level`. Backups or restore are missing: `ship-level`. Integrity rules need lasting tests: `test-level`. The dictionary needs publishing: `docs-level`. Reads slow with growth: `perf-level`.

**Handoffs into this skill.** Use the context passed in, skip questions the shared record answers, and report back to the calling skill.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No step run against real data by this skill. No shape change without a tested way back. No change to stored data before a backup that was shown to restore. No sensitive value printed. No integrity claim without a count taken on a copy.
