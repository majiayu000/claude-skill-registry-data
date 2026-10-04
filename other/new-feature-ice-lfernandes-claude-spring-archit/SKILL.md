---
name: new-feature
description: Orchestrates the feature pipeline — one use case per run, 5 design skills → spec.md for the executor, and implements an already-approved spec on the same argument
disable-model-invocation: true
argument-hint: "<feature description> | UC-NNN-slug | empty to list"
model: opus
---

# `/new-feature` — Feature pipeline orchestrator

## Why this is Form 2 (manual skill)

Axis 2 (manual trigger) + axis 5 (procedural) + axis 8 (both). Form 1 rejected — user
requested manual invocation. Subagent rejected — none of the three reasons apply
(context, tools, model). A fixed-order procedure rules out a rule and CLAUDE.md.

**Manual only.** `disable-model-invocation: true` hides this skill from the model: the
`Skill` tool can't call it, and trying is blocked. When a conversation reaches the point
of running it, print the exact command for the user to type — don't attempt the call.

---

Pinned to `opus`: consolidating the partials and settling their divergences is design, and the executor it chains declares its own model (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Contract

**Class:** orchestrator — the territory is `skill_classes.orchestrator` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. A run writes under
`docs/` only, and `ArchHook.java guard` also refuses a `Skill` call to a `build`-class skill
while this run is open: a design run does not materialize files, it records what is missing.

**Ownership:** Feature zero→spec orchestrator. Owns the sequence, the input table, the
spec lifecycle (`status:`), and the final output (`UC-NNN-spec.md`). Does **not** own the
use case number or slug — `use-case-design` does.

**Reads:**
- `pom.xml`, `.claude/forbidden-imports.txt`, and this project's domain package,
  discovered and never assumed — validates the generated project
- `docs/use-cases/UC-*/` — folder existence and each spec's `status:` line, by command
- `docs/use-cases/UC-NNN-<slug>/*.md` — the partials of the case being run

**Writes (indirectly via layer skills):**
- `docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md` and `docs/use-cases/BACKLOG.md` — via
  `use-case-design`
- `docs/use-cases/UC-NNN-<slug>/10-dominio.md` — via `domain-modeling`
- `docs/use-cases/UC-NNN-<slug>/20-persistencia.md` — via `persistence-architect`,
  migration SQL included as a code block, never as a file under `src/`
- `docs/use-cases/UC-NNN-<slug>/25-mensageria.md` — via `messaging-architect`, only if
  `10-dominio.md`'s Events block names external (Kafka) delivery
- `docs/use-cases/UC-NNN-<slug>/35-jobs.md` — via `jobs-architect`, only if
  `25-mensageria.md` chose Form B or `00-caso-de-uso.md`'s trigger is a schedule
- `docs/use-cases/UC-NNN-<slug>/30-rest.md` — via `rest-api-architect`
- `docs/use-cases/UC-NNN-<slug>/32-seguranca.md` — via `security-architect`, only if
  `00-caso-de-uso.md`'s `Access` asks for something the project's filter chain does not
  already give (step 3b)
- `docs/use-cases/UC-NNN-<slug>/40-testes.md` — via `test-architect`

**Writes outside `docs/`: none.** A run is docs-only, and that is enforced, not promised:
`ArchHook.java guard` refuses a `Skill` call to a `build`-class skill — `docker-architect`
included — while this orchestrator's phase is open, and refuses a write outside
`skill_classes.orchestrator`'s territory. A partial that needs a service the compose file
doesn't declare **records** it (`persistence-architect` step 9, `messaging-architect`
step 9); the consolidated spec carries the list, and the user runs `/docker-architect` from a
prompt of its own afterwards. Why: a design run once hand-wrote a `schema-registry` block
into `docker-compose.yml`, with no template, no tag verification and no healthcheck
(`lessons-learned-012.md` §§ 4, 12, 13), and the review was of a spec nobody read that file
through. Record: `@.claude/decisions/0058-skill-classes-territory-schema.md`

**Writes (directly):**
- `docs/use-cases/UC-NNN-<slug>/UC-NNN-spec.md` — implementation plan (executor-ready),
  including its `status:` line (`draft` → `approved`)

**Never writes under `src/`.** Neither does any skill it chains. Every file under `src/`
— migrations included — belongs to `java-spring-boot-developer`. The one exception: the
executor-offer pre-flight (§ End of flow) may trigger `archunit-installer` (via
`test-architect`'s setup mode) and `commons-logging-installer` (directly) before
delegating. Those writes are the installers' own, one-time, gated by their own
`AskUserQuestion` — not this orchestrator writing business code.

**Never runs `git add`, `git commit`, or `git push`.** Neither does any skill it chains.
Git happens only through `git-publish`, behind its two confirmations, at the end steps
below. No end of this flow is left without an explicit git instruction.

**Integrates with (sequence ordered by depends-on):**
1. `use-case-design` — invoked for a new case; skipped on resume when `00-caso-de-uso.md` exists
2. `domain-modeling` — invoked if `10-dominio.md` is missing (depends on 1)
3. `rest-api-architect` — invoked if `30-rest.md` is missing (depends on 2)
3b. `security-architect` — invoked per step 3b's table when `32-seguranca.md` is missing
   (depends on 1, 2, 3). Skipped when `Access` is public in a project with no filter chain, or
   authenticated in one whose chain already denies by default
4. `messaging-architect` — invoked if `10-dominio.md`'s Events block names external
   (Kafka) delivery and `25-mensageria.md` is missing (depends on 2). Skipped entirely
   when the event, if any, stays in-process — not every use case needs it
5. `jobs-architect` — invoked if `25-mensageria.md` chose Form B or the trigger is a
   schedule, and `35-jobs.md` is missing (depends on 1, 4). Skipped otherwise
6. `persistence-architect` — invoked if `20-persistencia.md` is missing (depends on 2, 3, 3b, 4, 5)
7. `test-architect` — invoked if `40-testes.md` is missing (depends on 2,3,3b,4,5,6)

**Why REST and messaging both run before persistence.** The order follows who generates
requirements for whom. REST generates schema requirements — `Idempotency-Key` on a
creation `POST` needs the shared key table — and persistence generates none for REST.
With persistence first, the table was discovered after the partial was written, and
persistence ran twice.

Messaging is the same shape and was learned the same way: a transactional outbox needs the
shared `outbox_events` table, a consumer needs the shared dedupe table, and neither is
visible from the domain partial alone. With messaging after persistence, `20-persistencia.md` was
written without the relay's retry columns and its partial index, and persistence ran twice
again. Messaging depends only on step 2, so running it before persistence costs nothing —
and persistence then reads both requirement lists, `30-rest.md` block 4 and
`25-mensageria.md` § 6, in its first pass.

Jobs sits between them for the same reason. The scheduling technology it picks brings tables
(`shedlock`, `QRTZ_*`, `BATCH_*`), the relay's claim depends on how many instances run the
pass, and the prune job needs a bounded delete — three schema facts invisible to persistence
until `35-jobs.md` § 3 and § 6 exist. Jobs itself needs only the use case and messaging's
publication form, so it costs nothing to run first
(`@.claude/decisions/0087-jobs-architect-skill.md`).

Security runs right after REST, for the same two reasons in opposite directions. It needs the
endpoints `30-rest.md` fixed — access rules written before them protect a guess — and it can
generate schema requirements: users owned by the application need a credentials store, an
API key needs a key store, both invisible to persistence until `32-seguranca.md` § 7 exists.
Ownership is not one of them: it is an invariant `domain-modeling` already modeled from the
`Access` row (`@.claude/decisions/0112-security-architect-skill.md`).

**Design order isn't implementation order.** Messaging is designed fourth and implemented
sixth: `UC-NNN-spec.md` keeps messaging as block 6, and the executor's conditional Block M
still runs between REST and Tests. Jobs is block 7, implemented by the conditional Block J
right after Block M — a trigger compiles against the inbound port it calls, so it comes last
among the production blocks. Security is block 4.5, implemented by the conditional Block S
right after Block 3 — its annotations and the actor resolution go on the controllers Block 3
just wrote. The pipeline orders by who needs whose requirements;
the spec orders by what compiles against what.
8. `java-spring-boot-developer` — offered, only for an `approved` spec, after the
   one-time setup pre-flight (§ End of flow) checks for ArchUnit and commons-logging gaps
9. `git-publish` — invoked at the end, per § End of flow

`gof-design-patterns` is not a pipeline step, and this orchestrator never invokes it — a
design run cannot reach a `build`-class skill. **Its catalog is still applied at design
time:** each design skill above runs its § Design-time use for its own layer and writes a
`## Design patterns` section into its partial, so the classes a pattern creates are in the
spec the user approves, not chosen by the executor afterwards. The executor implements
those rows, and applies the catalog on its own only for a symptom already on disk
(`@.claude/decisions/0089-design-patterns-decided-at-design-time.md`, superseding the
executor-side trigger of 0077).

---

## Spec lifecycle

`UC-NNN-spec.md` opens with a frontmatter carrying one field:

| `status:` | Written by | When |
|---|---|---|
| `draft` | this skill | at consolidation |
| `approved` | this skill | only after the user's explicit approval, § End of flow |
| `implemented` | `java-spring-boot-developer` | with a green build |
| `implemented-blocked` | `java-spring-boot-developer` | with a green build, when the run left an approved use case unreachable end to end — the code is on disk and verified, and a `Satisfied by` the spec named is not there yet |

A use case folder is **open** when it has no `UC-NNN-spec.md` yet, or its spec is `draft`.
`implemented-blocked` is **not** open: a case whose code is on disk, green and committed is not
work in progress, and its satisfier is usually a backlog row nobody is holding this run for.

**One `/new-feature` produces one use case.** The next one only starts once the previous
is `approved`, `implemented` or `implemented-blocked`.

**An approved spec is immutable.** Later cases read approved specs as a read-only
contract and reuse the aggregate already modeled. A change a new case needs in an
approved one goes into the `## Impact on approved use cases` section of the **new**
spec; the executor applies it in code. Don't edit the old spec — write the line in the
altered case's own `CHANGELOG.md` instead (consolidation step 2).

**A case can be nothing but changes.** Every component `CHANGE`, no new use-case class:
it still gets its own `UC-NNN`, and its slug names the capability added rather than the
trigger, which already belongs to the case being changed
(`@.claude/rules/naming.md` § Use case identifier).

Decide what the current case needs. Don't defer or anticipate a decision "for the future
case" — the future case decides it, in its own impact section.

---

## Entry guardrail

Runs before any skill invocation, any write, and any question. Every check is a command;
the model doesn't interpret the input.

### 1 · Input table — closed

Survey the use cases once:

```bash
find docs/use-cases -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort | while read -r d; do s=$(find "$d" -maxdepth 1 -name 'UC-*-spec.md' -exec grep -m1 '^status:' {} \;); echo "$d ${s:-status: (no spec)}"; done
```

**The disk is not the history.** A folder deleted from the working tree is invisible to
`find` and still in `HEAD`, so the next number looks free when it isn't:

```bash
git ls-tree -d --name-only HEAD docs/use-cases 2>/dev/null
```

A `UC-NNN` that `HEAD` has and the disk doesn't → **stop and report it**, before any
skill call. Two things can be true, and only the user knows which: the number was
recycled (the repository would end up with two different `UC-NNN`, and this run's commit
would delete one while adding the other), or approved work was deleted without being
committed. Name the folder, say which of the two it looks like, and ask. Don't infer the
next free number from the disk alone.

Same comparison for the backlog, and for the same reason — the entry of a deleted case
disappears with its folder, and a run that recreates it from scratch writes different
text nobody compares:

```bash
git diff --stat HEAD -- docs/use-cases/BACKLOG.md 2>/dev/null
```

Non-empty when a `UC-NNN` is missing from the disk → show the diff before
`use-case-design` writes a new entry.

Classify the argument with the argument in single quotes:

```bash
printf '%s' '<argument>' | grep -Eqx 'UC-[0-9]{3}-[a-z0-9]+(-[a-z0-9]+)*' && echo EXACT
printf '%s' '<argument>' | grep -Eiq 'uc-[0-9]' && echo UC_LIKE
test -d 'docs/use-cases/<argument>' && echo FOLDER

# The number the argument carries, and the folders it resolves to. RESOLVES_ONE when the
# argument names no folder of its own but its UC number has exactly one on disk.
N=$(printf '%s' '<argument>' | grep -Eio 'uc-[0-9]{3}' | head -1 | tr 'a-z' 'A-Z')
test -n "$N" && ls -d "docs/use-cases/$N"-*/ 2>/dev/null
```

Evaluate in order and **stop at the first row that matches**. There is no "any other
text" row.

| # | Input | Result |
|---|---|---|
| 1 | empty | ✅ list the survey above — each case with its `status` — and stop |
| 2 | `EXACT`, `FOLDER`, status `draft` or `(no spec)` | ✅ resume: skip `use-case-design`, generate only the missing partials, then consolidation |
| 3 | `EXACT`, `FOLDER`, status `approved` | ✅ **implement**: jump to § End of flow at *Implement now*, skipping steps 1-6, consolidation and the approval question. The argument is the request; nothing is asked again |
| 4 | `EXACT`, `FOLDER`, status `implemented` or `implemented-blocked` | ❌ `already implemented — describe the change as a new feature` |
| 5 | no `FOLDER`, and the argument's `UC-NNN` resolves to **exactly one** folder on disk | ❌ `<UC-NNN> is <real-slug>, status <status>` — plus the exact command for it. The case exists; the argument named it wrongly |
| 6 | `EXACT`, no `FOLDER`, number resolving to zero or several folders | ❌ `use case not found; to create one, describe the feature` |
| 7 | `UC_LIKE` but not `EXACT` (slug plus context, malformed slug, two slugs, a path) | ❌ `ambiguous argument` |
| 8 | free text, and the survey shows an open case | ❌ `<UC folder> is open — resume or approve it first` |
| 9 | free text, and no open case | ✅ new: pass the description **as is** to `use-case-design` |
| — | anything else | ❌ `unrecognized argument` |

Row 5 is the near miss, and it is an **error row, not a success one**: it reports and stops.
`/new-feature UC-003-spec` once answered `use case not found` while
`docs/use-cases/UC-003-initiate-kyc-verification/` sat on disk — literally true, since no folder
carries that name, and practically wrong, since the argument was the basename of the spec file
inside that folder (lessons-learned-014 § 12). The answer names the real slug and the status, so
the next attempt is one line away. It does **not** resolve the argument and carry on: the
argument was wrong, two rows above write `src/`, and guessing which case was meant is exactly
what the next paragraph forbids.

**The model doesn't interpret the input.** It doesn't fix a slug, separate a slug from
context, or infer intent. A text that almost matches a row doesn't match it. Row 5 is not an
exception: it reports what it found, it does not act on it.

**An error has a fixed shape and ends the run. After it: no side effect** — no skill call, no
write, no question. Reading is still allowed, and row 5 is why: the survey is `ls` and `grep`,
it changes nothing, and it is the cheapest way for a near miss to correct itself. The rule used
to say "no output", which a run broke by printing the survey after the error — the output the
user actually needed. A rule violated because it is slightly wrong is a rule to fix, not to
repeat.

```text
❌ /new-feature: <reason>.
Usage: /new-feature <feature description>   → new use case
       /new-feature UC-NNN-slug              → resume a draft case,
                                               or implement it once approved
       /new-feature                          → list
```

Row 5 keeps that shape and adds the one line that makes it actionable:

```text
❌ /new-feature: UC-003 is UC-003-initiate-kyc-verification, status approved.
Did you mean: /new-feature UC-003-initiate-kyc-verification
Usage: …
```

### 2 · Worktree — decided here, never later

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir --git-common-dir
```

Both fail → not a git repository yet: no worktree, paths are relative to the project
root. Different `--git-dir` and `--git-common-dir` → the session is inside a worktree. Every
path this run writes is under `--show-toplevel`, and nothing is written in the main
checkout. If the work should be isolated in a worktree and isn't yet, that is decided
**now**, before any question or write. Never enter or leave a worktree mid-flow — edits
get refused outside it and orphan folders appear in the main checkout.

**Third case: the project root itself is gitignored by a parent repository.**

```bash
git check-ignore -q . && echo IGNORED
```

Happens when this project lives inside another repo's ignored path (e.g. a demo under
this meta-repo's own `examples/`, which is 100% gitignored). The pipeline runs normally
— nothing above depends on the root being tracked — but flag it here, once, so the
run's own state carries the fact forward instead of `git-publish` discovering a `git
status` that doesn't match the feature just implemented (lessons-learned-006 § 8:
`src/`, `docs/use-cases/` all ignored, only an unrelated dirty file showed up in
`status`). `IGNORED` → note it in the run's context and pass it to `git-publish`'s
invocation at § End of flow so its own state check (`@.claude/skills/git-publish/SKILL.md`
step 1) knows to warn instead of assuming the diff matches the feature.

**Fourth case: the worktree already carries changes from before this run.**

```bash
git status --porcelain 2>/dev/null
```

Non-empty → work that is **not** this run's. Report it here, in full (path count and what
the paths are, staged and unstaged alike), and carry **the list itself** to `git-publish`
the same way `IGNORED` travels — not just the fact that something was dirty.

`git status --porcelain`, never `git diff --cached`: the index is half the picture, and the
half that was already known. An unstaged edit and an untracked file from a previous run are
invisible to the index and are swept into the commit by `git add -A` all the same — a modified
`.claude/audit-usage/history.jsonl` and one untracked report rode along exactly that way, while
the guardrail reported a clean start (lessons-learned-014 § 11). Harmless there, since
`git-publish` commits the audit trail with the run on purpose; the shape is not.

**`.claude/audit-usage/**` is never pre-existing work** — leave those paths out of the list.
The previous run's report and its `history.jsonl` line are written at `Stop` and on the next
prompt, both after that run's commit, so every run starts with them dirty by construction;
`git-publish` stages the directory with this run's commit anyway (lessons-learned-016 § 8).
Reporting them would make every start look dirty and teach the reader to ignore the report.

This is the cheap moment to decide: at the end of the flow the run's own deliverable is mixed
into the same worktree, and separating them costs a reset nobody planned. lessons-learned-012
§ 7: 1.503 staged deletions from before the run only surfaced at `git-publish`, and the
handling was improvised because no state in either skill described it.

### 3 · Project

Checks `pom.xml` (exists + parseable), `.claude/forbidden-imports.txt`, and that a domain
package exists. **Discover it, don't assume it.**

```bash
find src/main/java -type d -name domain
```

`src/domain/` and `adapter/` don't exist in any blueprint: they're Maven module paths,
and even in multi-module blueprints the layer lives at `<module>/src/main/java/…`. A
guardrail that checks a literal path either fails on a valid project or passes by
accident — neither case guards anything. The package name comes from the active
blueprint's `packages.map`; where the blueprint isn't at hand, it comes from the `find`
above.

### 4 · Disk

Available space > 100MB, write permission on `docs/use-cases/`.

Without ✅ validation, anti-pattern 9 (invoking against an invalid project).

---

## Procedure — 6 steps + consolidation

**Execution discipline** — the run's cost is turns × context size, not file size:

- **No progress messages** between steps or tools ("moving to step 3", "domain ok"). Each
  one is a turn that re-reads the whole conversation. The only report is § Final report.
- **Independent writes in one turn** — parallel tool calls, not one file per turn.
- **Dependency versions come from the build file.** Read `pom.xml` before resolving any
  version; no web search for a version the project already declares.
- A step's "Output" below is a check the run makes, not a message it prints.

### Step 1: Use case (new case only)

**Invoke** `use-case-design` via the Skill tool, with the user's description as is.

`use-case-design` owns the boundary, the number, and the slug. When the description
holds several use cases, it asks the user which one to design, designs that one, and
writes the rest to `docs/use-cases/BACKLOG.md`. This run continues with the one it
created — never with the others.

**Output:** `docs/use-cases/UC-NNN-<slug>/00-caso-de-uso.md` — its folder name is the
`UC-NNN-<slug>` every later step uses.

### Short path — checked right after step 1

A trivial case doesn't need five partials. Check all four against `00-caso-de-uso.md`
and the approved specs:

| Criterion | Unmet when |
|---|---|
| Aggregate reused from an approved spec | the component table has a NEW aggregate or value object |
| No new table, column, or migration | the component table has a NEW or CHANGE migration or entity |
| No new exception | an error situation has no exception already named in an approved spec |
| No question asked to the user | `use-case-design` needed `AskUserQuestion` |

All four met → skip steps 2–6 and write `UC-NNN-spec.md` from
`templates/feature-spec-short.md.example`: every row names its source, an approved spec or
a rule. A row that needs judgment to fill means the case isn't trivial — discard the
short spec and take steps 2–6. One criterion unmet → steps 2–6.

### Step 2: Domain (depends on 1)

If `10-dominio.md` is missing: **invoke** `/domain-modeling UC-NNN`.
If it exists: read, validate (four blocks: aggregate, VOs, invariants, ports).

**Output:** "✅ Domain ready" or a list of gaps.

### Step 3: REST (depends on 1,2)

If `30-rest.md` is missing: **invoke** `/rest-api-architect UC-NNN`.
If it exists: read, validate (six blocks: resources, DTOs, errors, pagination, idempotency,
personal data).

**Output:** "✅ REST ready" or gaps.

### Step 3b: Security (depends on 1, 2, 3, conditional)

Read `00-caso-de-uso.md`'s `Access` row, and whether the project already has a filter chain
(`grep -rl "SecurityFilterChain" --include='*.java' src/main`). If `32-seguranca.md` is missing,
**invoke** `/security-architect UC-NNN` when any holds:

| `Access` | Filter chain on disk | Why it runs |
|---|---|---|
| a role, a group, a scope, or the owner | any | this case's rules — and the setup when there is none |
| authenticated | none | first secured case: the project-wide setup |
| public | present | a `permitAll` needs its recorded reason |

Otherwise skip: public in an unsecured project, or authenticated behind a chain that already
denies by default — the spec's security block says which. An `00-caso-de-uso.md` with an HTTP
trigger and no `Access` row (written before the row existed) is not a skip: invoke it, it asks.
If `32-seguranca.md` exists: read, validate (eleven blocks: access per endpoint, mechanism,
authorities, project-wide setup, ownership, failure responses, schema requirements, declared
dependencies, configuration, contract test cases, deferred).

§ 7 is what step 5 reads; § 8 is the only list that entitles the executor to add a security
starter to `pom.xml`; § 10 is what step 6 turns into tests.

**Output:** "✅ Security ready", "— skipped (<which row>)", or gaps.

### Step 4: Messaging (depends on 2, conditional)

Read `10-dominio.md`'s Events block. If it names external (Kafka) delivery for the
event and `25-mensageria.md` is missing: **invoke** `/messaging-architect UC-NNN`. If
the event is absent or stays in-process, skip this step — not every use case needs it.
If `25-mensageria.md` exists: read, validate (nine blocks: topic and delivery, producer,
consumer and idempotency, retry/DLQ, configuration, schema requirements, declared
dependencies, personal data, deferred).

A missing § 6 is a gap, not an omission: it's the list step 5 reads. `none` is a valid
value there and means publication Form A with no consumer dedupe table to build. § 7 is
the same shape for build dependencies: it is the only list the executor may act on when it
writes `pom.xml`, so a missing one leaves a needed dependency with no owner
(lessons-learned-013 § 10). **This step is not the only check on it** — a run that reaches
consolidation without taking this step is exactly how two lists went missing and a spec was
approved anyway, so consolidation gates the same thing for every path.

**Output:** "✅ Messaging ready", "— skipped (no external delivery)", or gaps.

### Step 4b: Jobs (depends on 1, 4, conditional)

Invoke `/jobs-architect UC-NNN` if `35-jobs.md` is missing and at least one holds:
`25-mensageria.md` § 2 chose **Form B**, `00-caso-de-uso.md`'s trigger is a schedule, a
recurring run, a batch or a background job, or a partial's `Deferred` block names a scheduled
job. None holds → skip this step. If `35-jobs.md` exists: read, validate (nine blocks: jobs,
technology, coordination, execution guarantees, observability, schema requirements, declared
dependencies, configuration, deferred).

A Form B case with no `35-jobs.md` is a gap, not a skip: the relay would have no schedule and
the outbox no prune — the exact state lessons-learned-014 § 9 found. § 3's replica count and
§ 6's requirements are what step 5 reads; § 7 is the only list that entitles the executor to
add a scheduling dependency to `pom.xml`.

**Output:** "✅ Jobs ready", "— skipped (no scheduled work)", or gaps.

### Step 5: Persistence (depends on 1,2,3,3b,4,4b)

If `20-persistencia.md` is missing: **invoke** `/persistence-architect UC-NNN`. It reads
every schema requirement list in the same pass — `30-rest.md` block 4 (the idempotency
table among them), when step 3b ran `32-seguranca.md` § 7 (a credentials or API-key store),
when step 4 ran `25-mensageria.md` § 6 (the shared outbox table, the
dedupe table), and when step 4b ran `35-jobs.md` § 3 and § 6 (the replica count its claim
strategy must meet, the scheduling tables, the prune's bounded delete). If it exists: read, validate (seven blocks: schema, mapping, adapter and
ports, migrations, configuration, declared dependencies, deferred). § 6 is the persistence twin
of `25-mensageria.md` § 7,
and the same rule holds: it is the only list that entitles the executor to touch `pom.xml` —
and consolidation checks it again, for the paths that never take this step.

**Output:** "✅ Persistence ready" or gaps.

### Step 6: Tests (depends on 1,2,3,3b,4,5)

If `40-testes.md` is missing: **invoke** `/test-architect UC-NNN` (design mode).
If it exists: read, validate (five blocks: pyramid, cases, fixtures, coverage, test dependencies).
When step 3b ran, every case of `32-seguranca.md` § 10 has a test row — a missing one is a gap.

**Output:** "✅ Tests ready" or gaps.

### Consolidation (after 1,2,3,5,6 ✅ — steps 3b, 4 and 4b conditional)

If all specs that apply exist and validate (security only when step 3b wasn't skipped,
messaging only when step 4 wasn't, jobs only when step 4b wasn't):

1. **Resolve divergences before consolidating.** The partials are written by different
   skills, and downstream corrects upstream: `30-rest.md` fixes the path and status
   that `00-caso-de-uso.md` had sketched, `20-persistencia.md` fixes the key that the
   domain described in prose. Stacking both versions and explaining in a note which one
   wins pushes the work onto the reader — and the note ends up two hundred lines away
   from where it matters.

   Walk through every partial in the folder and, for each fact that appears in more than one with
   different values, apply this precedence:

   | Fact | Who wins |
   |---|---|
   | HTTP path, verb, status, body shape | `30-rest.md` — except the 401 and 403 rows, below |
   | Who may call each endpoint, the authentication mechanism, the claims-to-authorities mapping, the `permitAll` list and its reasons, the 401 and 403 rows, CORS, OpenAPI and Actuator exposure, where the controller reads the actor from | `32-seguranca.md`. The actor field, the owner field and the ownership invariant stay `10-dominio.md`'s; an owner-only `Access` whose domain partial has no actor is not settled by precedence: **stop and ask** |
   | Table, column, key, index, migration | `20-persistencia.md` — including every table or column another partial *asked for*: the requirement is born in `30-rest.md` block 4 or `25-mensageria.md` § 6, the final form (name, type, nullability, index, migration) is always this one's |
   | Topic, serialization, delivery guarantee, consumer retry and DLQ | `25-mensageria.md` |
   | Outbox table, its columns, the claim query, and the values the columns encode (batch size, backoff, attempt ceiling, retention window, the prune's statement) | `20-persistencia.md` — the whole table is its territory. `25-mensageria.md` declares the **guarantee** those values have to deliver, never the columns; a § 6 row naming columns is reported as a divergence and the guarantee is what carries over |
   | Scheduling technology, a job's trigger and cadence (the relay's poll interval included), coordination across instances and the replica count, overlap and missed-run policy, on/off property, job metrics, the prune job | `35-jobs.md`. A claim strategy in `20-persistencia.md` that does not meet `35-jobs.md` § 3's replica count is not settled by precedence — it is a guarantee dropped by a shape decision: **stop and ask** |
   | Aggregate name, value object, port, event | `10-dominio.md` |
   | Exception class and `errorCode` | `10-dominio.md` |
   | Use case boundary, invariants, error situations | `00-caso-de-uso.md` |
   | Name and level of each test | `40-testes.md` |
   | A design pattern and the classes it creates | The partial of the layer those classes live in. Two partials adopting different patterns for the same class is not settled by precedence: **stop and ask** |

   `UC-NNN-spec.md` carries **a single value per fact** — the winner — across all
   blocks, including those that had inherited the old value. The discarded versions go
   into a `## Resolved divergences` section at the end, one line each: fact, discarded
   value, adopted value, partial that decided. The executor reads one truth; the audit
   trail is still there.

   A divergence the table doesn't resolve — two facts from the same owner, or a
   business-rule contradiction — **stops the pipeline** and asks. Don't invent it or
   stack it.

   **A downstream partial never edits an upstream one's fact — it asks for it.** A requirement
   born downstream and landing upstream — `20-persistencia.md` bounding the producer's send
   time so the outbox lease outlives any send, a value `25-mensageria.md` owns — travels as a
   named requirement in the downstream partial, and this step resolves it like any other
   divergence: the owner's block in `UC-NNN-spec.md` carries the new value, and
   `## Resolved divergences` records who asked. Carried silently into the owner's block, it is
   a fact with two authors and no record of the second.

   **And one shape the table resolves only in appearance:** a column decision that changes
   behaviour. `20-persistencia.md` wins on the column, always — but when dropping a column
   also drops a guarantee `25-mensageria.md` declared (no `next_attempt_at`, so per-row
   exponential backoff becomes a fixed repoll), the winner is not the answer. That is a
   divergence the table doesn't resolve: **stop and ask**, and record which guarantee the
   chosen shape delivers. A precedence rule written for table shape must never be what
   settles a behaviour.

2. Consolidate into a single file: `UC-NNN-spec.md`, with `status: draft`, **by reference**
   - Each block holds only the final decisions — one value per fact — and the path of the
     partial that details it. Never copy a partial's tables, SQL, or code: a copied
     consolidation doubled the output of a real run and added nothing the partial lacked
   - Structure: 5 blocks (use case, domain, persistence, REST, tests), plus a 6th
     (messaging) only when step 4 wasn't skipped, a 7th (jobs) only when step 4b wasn't, and
     the security block (`## 4.5 Security`) only when step 3b wasn't — when it was, that block
     reads `none` with the skip row of step 3b, so "covered by deny-by-default" is a recorded
     fact and not a missing block
   - `## Impact on approved use cases`: every row from the same section of each partial —
     "none" when all are empty
   - `## Design patterns`: every row from the same section of each partial, with the partial
     that decided it — "none" when all are empty. **A partial that applies must carry the
     section, or consolidation stops**: absence is not `none`, the same test as the
     declared-dependency lists below. A row whose force is neither a spec line nor a
     `file:line` is not consolidated — the pipeline stops and asks
   - **A row that adds a precondition must name its satisfier, or consolidation stops.** Any
     row making an earlier case require a state it did not require before — a status, a flag, a
     related record — carries the `Satisfied by` column `00-caso-de-uso.md` already asks for:
     an approved `UC-NNN`, this case, or a backlog row **by its `BL-NN`**. Missing or vague, the
     pipeline stops and asks; it is not filled in by inference. A `UC` number is not a valid
     answer for a backlog case — it has none until it is designed, and two reports of a real run
     invented `UC-004` because the sentence needed a name and `BACKLOG.md` had none to give
     (lessons-learned-014 § 7). Where the satisfier is a backlog row, the consolidated spec says
     outright that the earlier case is unreachable end to end until that one ships, and the final
     report repeats it, citing the same `BL-NN` — a use case that answers 422
     on every real call is not a detail the reader should have to find in a test fixture
     (lessons-learned-013 § 5)
   - **A partial that applies must carry its declared-dependency section, or consolidation
     stops.** `20-persistencia.md` § 6 always; `32-seguranca.md` § 8 whenever step 3b ran;
     `25-mensageria.md` § 7 whenever step 4 ran;
     `35-jobs.md` § 7 whenever step 4b ran; `40-testes.md` § 5 always. The
     value `none` is legitimate and common — most cases need no new dependency — but **absence
     is not `none`**: one says the design skill decided nothing was needed, the other says
     nobody looked, and the executor cannot tell them apart. Steps 4 and 5 validate the same
     thing; they are conditional, and a spec once reached `approved` with both lists missing
     because its partials had been written in earlier runs (lessons-learned-014 § 6). The
     executor then added a dependency to `pom.xml` by inference — a defensible one, and
     precisely the decision this list reserves for the design skill. Consolidation is the block
     every run passes, which is why the check belongs here as well, exactly like `Satisfied by`
     above
   - **A personal-data field crossing the process boundary in clear carries a recorded
     decision, or consolidation stops.** `25-mensageria.md` § 8 and `30-rest.md` § 6 each list
     the fields of the payload and the response body that match
     `@.claude/rules/logging.md` § Masking candidates, with the form chosen. A `full value` row
     without a named receiver and a reason is not consolidated: the pipeline stops and asks, and
     it is not filled in by inference. `none` is a valid value and absence is not one. Until now
     this was a line in the **final report** — detection after the spec is approved, after the
     code is written and after the commit, and in the observed run it appeared there only because
     the executor volunteered it, for a CPF already published in clear on a topic
     (lessons-learned-014 § 8, `@.claude/rules/personal-data.md` § In transit)
   - **A deferred row leaves the run with an owner, or consolidation stops.** Each partial's
     `Deferred` block carries what it decided not to do, the norm that requires it, and an
     intended owner. `checklist` → add the item to this spec's checklist; the run implements it.
     `backlog` → **consolidation appends the row to `docs/use-cases/BACKLOG.md` and assigns its
     `BL-NN`**, then writes that id into this spec's `## Out of scope` with the consequence
     spelled out: what the project does not guarantee until that row ships. Consolidation is the
     only writer of a backlog row inside a feature run — two partials each computing "highest
     plus one" would issue the same `BL-NN`. An item whose norm makes it mandatory and whose
     owner is missing or vague stops the pipeline and is not inferred: a real run decided a
     7-day retention for `outbox_events`, left a commented `DELETE` in the migration, kept
     `app.outbox.prune-after` out of `application.yml` on purpose, and handed the job to nobody,
     over a table whose payload carries personal data (lessons-learned-014 § 9,
     `@.claude/rules/personal-data.md` § At rest)
   - **Every case named in that section gets a line in its own `CHANGELOG.md`**, at
     `docs/use-cases/UC-XXX-<slug>/CHANGELOG.md` — created on the first change, appended
     afterwards. One line: date, the `UC-NNN` making the change, and what changed
     (`2026-09-27 · UC-003 · RegisterCustomerUseCase now emits CustomerRegistered`). The
     approved spec stays untouched, which is exactly why the log is a separate file
     (`@.claude/rules/naming.md` § Use case identifier). Without it, nobody reading the
     altered case ever learns it changed — immutability keeps the text and loses the
     history
   - Order: implementation order (depends-on)
   - **Every `permitAll` carries its reason, or consolidation stops.** `32-seguranca.md` § 1
     lists the public paths of the project after this case, each with a reason; a public row
     with none, or a first secured case whose `## Impact on approved use cases` does not say
     what happens to the endpoints earlier cases published without a chain, is not consolidated
     — deny by default turns them into 401 on the next deploy, and nobody chose that
     (`@.claude/rules/authorization.md` § Default access)
   - Recipient: `java-spring-boot-developer` agent — a spec with § 4.5 runs the executor's
     conditional Block S (steps S1-S3, right after REST), which generates the filter chain, the
     mechanism wiring, the method-security annotations and the actor resolution from
     `32-seguranca.md`; a spec with § 6 runs the executor's
     conditional Block M (steps M1-M4, between REST and Tests), which generates the Kafka
     producer/consumer adapters from `25-mensageria.md`; a spec with § 7 runs Block J (steps
     J1-J3, right after Block M), which generates the scheduling wiring and triggers from
     `35-jobs.md`. Neither touches the fixed 19-item checklist

3. **Check whether the architecture tests can now be turned on.** The bootstrap doesn't
   install ArchUnit or the coverage gate by design: a `check` over an empty set proves
   nothing. After the first feature that condition no longer holds, and nothing in the
   pipeline was watching for it.

   ```bash
   grep -rl "ArchRule\|ArchTest" --include='*.java' src/test/ 2>/dev/null | head -1
   find src/main/java -name '*.java' ! -name 'package-info.java' | head -1
   ```

   Second command with a result and the first without: the project now has business
   classes and still has no boundary enforcement outside the editor. In `single-module`
   the compiler doesn't enforce anything either, so there's no verification at all.
   **Propose running `test-architect` in setup mode** — propose, don't run it: detection
   is mechanical, authorization is the user's.

---

## End of flow

Every branch below ends in an explicit instruction. None of them runs git outside
`git-publish`.

**Two entry points reach this section, and they differ in exactly one thing — whether the
implement question has already been answered.**

| Arriving from | Enters at | Asks *Implement now / Not now* |
|---|---|---|
| Consolidation, in the same run | § Approval | yes — the user has not said yet |
| Input row 3, `/new-feature UC-NNN-slug` over an `approved` spec | § Executor offer, at **Implement now**, skipping § Approval | no — the command is the request |

The second is the front door the second half of the pipeline did not have. Without it, an
approved spec's normal life — the run ends, the context is cleared — left no supported way to
reach the delegation, and every guarantee below became something a later session either
remembered or dropped: the pre-flight, the `CHANGELOG.md` writes, the four mandated findings of
the final report, and the `git-publish` chaining. Design:
`@.claude/decisions/0067-implement-entry-row.md`.

### Approval — asked on every run that consolidated a spec

`AskUserQuestion`: **Approve `UC-NNN-spec.md`** / **Keep as draft**.

- **Keep as draft** → report the spec path and the resume command
  (`/new-feature UC-NNN-<slug>`), and stop. No git: a draft isn't a deliverable.
- **Approve** → change the spec's line to `status: approved`, then the executor offer.

### Executor offer — only for `approved`

`AskUserQuestion`: **Implement now** (`java-spring-boot-developer`) / **Not now**.

**Asked only when the run itself just approved the spec.** Arriving from input row 3, the
question is skipped and the run starts at **Implement now** below: the command named an
approved spec, which is the answer.

- **Implement now** →
  - **One-time setup pre-flight, before delegating.** The executor is about to write the
    first `.java` under `src/` for this project run — the only point in the pipeline
    where "is the one-time infrastructure installed yet" actually matters. Detect what's
    missing, don't assume:

    ```bash
    grep -rl "ArchRule\|ArchTest" --include='*.java' src/test/ 2>/dev/null | head -1
    find . -type d -iname commons -o -type d -path '*shared/logging' 2>/dev/null
    ```

    First command empty → ArchUnit not installed yet (same gap step 3 already flagged,
    if this use case is the first one). Second command empty, or the directory it finds
    has nothing but `package-info.java` → commons-logging classes not installed yet.
    Either gap found → `AskUserQuestion`, one option per gap found: **Install now** /
    **Skip for this run**.
    - ArchUnit, install now → **invoke** `test-architect` via the `Skill` tool with **no
      argument at all** (setup mode) — same route step 3 already names, never invoke
      `archunit-installer` directly, it stays `test-architect`'s alone.
    - Commons-logging, install now → **invoke** `commons-logging-installer` directly via
      the `Agent` tool. No owning per-feature skill to route through: this orchestrator
      is the trigger, same as it owns `git-publish`'s invocation.
    - **Both gaps found and both answered "Install now" → either order works, and the
      same turn is fine.** This used to be the one place in the repo that could deadlock
      itself: `Skill(test-architect)` opened a design phase and
      `Agent(commons-logging-installer)` closed one, two `PreToolUse` hooks with no ordering
      guarantee between them, and the loser blocked every write the other agent made under
      `src/` for the rest of the run — lessons-learned-006 § 1 is the run that hit it (138k
      tokens, zero files written, had to relaunch alone). `agent_classes` retired it: a
      subagent's write is judged by its own `agent_type`, so no phase reaches it and nothing
      closes a phase on an `Agent` call any more
      (`@.claude/decisions/0059-agent-classes-territory-schema.md`).
    - Either **Skip** → proceed to the executor anyway. A spec that doesn't cite
      `@LogExecution`/`@MaskSensitiveData` or ArchUnit doesn't need either installed to
      compile; skipping isn't a gate failure, it's the user's call.
    - Neither gap found → skip this pre-flight silently, no question asked.
  - Delegate to `java-spring-boot-developer`, sending the spec path.
  - **Success** (final summary reports the checklist complete, the build green, and the
    spec at `status: implemented` — or at `implemented-blocked`, which is a success too, with
    the case it blocks on named) → **invoke** `git-publish` via the `Skill` tool, with
    `feat(UC-NNN-<slug>): <one-line summary>` as context.
  - **Failure** → report the executor's failure and stop. No git.
- **Not now** → **invoke** `git-publish` via the `Skill` tool, with context
  `docs(UC-NNN-<slug>): approved spec` and `docs/use-cases/UC-NNN-<slug>/` plus
  `docs/use-cases/BACKLOG.md` as the paths to stage. Nothing else: a design-only run writes
  nothing outside `docs/`, and the guard is what makes that true rather than intended.

  What used to be staged here — `docker-compose.yml` and `docker/init/**`, when the pipeline
  chained `docker-architect` — is no longer written during the run at all. The service the
  spec names is **pending**: say so in the final report, with the `/docker-architect`
  invocation the user should run next. An unmentioned pending service is how a `kafka`
  service went orphan once (`lessons-learned-010.md` § 7), and the fix is naming it, not
  writing the file mid-design.

`git-publish`'s two confirmation gates decide whether anything is committed or pushed —
this orchestrator only triggers the offer.

### Final report

Last message of the run, and the only report: the spec path and status, the backlog
entries left for later (if any), **every follow-up the run left pending outside `docs/`** —
each compose service or `docker/init` file a partial named, with the `/docker-architect`
command that materializes it, or "none" —
**every approved use case this run left unreachable end to end**, with the backlog row that
restores it named by its `BL-NN` (or "none") — never a `UC` number, which a backlog row does not
have — **every item a partial deferred, with the owner it left it to** (a checklist item, or a
`BL-NN`, or "none"), **every guarantee delegated to a consumer outside this project whose
idempotency is assumed or unknown** (or "none"), and **every personal-data field that crosses
a boundary in clear, with its receiver** (or "none") — now a repeat of what § 8 and § 6 of the
partials already recorded, not the first time anyone asks — three findings a reader must not have to
reconstruct from a fixture comment or a Javadoc sentence — what `git-publish`
did, and a recommendation to run
`/clear` before the next `/new-feature` — a clean context per use case keeps cost
measurable per case.

---

## Template: UC-NNN-spec.md

Lives at `.claude/skills/new-feature/templates/feature-spec.md.example`; the short path
uses `templates/feature-spec-short.md.example`.

Structure (5 blocks, implementation order — plus security, messaging and jobs when they apply):
- Frontmatter: `status:`
- Block 1: Use case
- Block 2: Domain model (aggregate, VOs, invariants, ports, events)
- Block 3: Persistence (JPA mapping, migrations, transactions)
- Block 3.5 (conditional): Messaging (producer/consumer, delivery semantics, retry/DLQ)
  — present only when `10-dominio.md` named external delivery for the event; "none"
  otherwise. See the known gap above — the executor doesn't consume this block yet
- Block 3.6 (conditional): Jobs (technology, triggers, coordination, replica count) —
  present only when step 4b ran; "none" otherwise. Implemented by the executor's Block J
- Block 4: REST API (resources, DTOs, errors, pagination, idempotency)
- Block 4.5 (conditional): Security (mechanism, access per endpoint, `permitAll` list,
  ownership, setup NEW/REUSE) — present when step 3b ran; otherwise `none` with the skip row.
  Implemented by the executor's Block S, right after Block 3
- Block 5: Tests (pyramid, critical cases, coverage, checklist)
- Impact on approved use cases ("none" when empty)
- Final section: Resolved divergences (empty when there were none)

See `templates/feature-spec.md.example` for the full shape.

---

## References

- **D14** — ordered pipeline: use-case → domain → persistence → REST → tests → executor. Order
  of REST and persistence swapped by `0037`.
- **D17** — pipeline skills without `disable-model-invocation` (so `/new-feature` can call them).
- **D20** — `/new-feature` deferred; `java-spring-boot-developer` executor; scope: both.
- **D22** — `/new-feature` design (this record).
- **`@.claude/decisions/0032-messaging-architect-skill.md`** — `messaging-architect`
  chained as a conditional step, same pattern as `persistence-architect`/`rest-api-architect`.
- **`@.claude/agents/commons-logging-installer.md`** — one-time logging/masking setup,
  triggered directly from the executor-offer pre-flight, same "installed once, not at
  bootstrap" shape as `archunit-installer`.
- **`@.claude/decisions/0037-lessons-learned-005-remediation.md`** — closed input table,
  one use case per run, spec lifecycle, no `src/` and no git outside `git-publish`.
- **Invariant 2** (`@CLAUDE.md`) — single owner. The orchestrator owns `UC-NNN-spec.md`;
  `use-case-design` owns number and slug.
- **Invariant 8** (`@CLAUDE.md`) — specs via skills; code via executor.

---

## Entry into generated projects

Step 6.6 writes the skills into the project. `/new-feature` travels the same way — the user runs
`/new-feature <feature description>` to design a new feature.

No adaptation needed — skills already use relative paths.

---

## Operational note: long-running background work

Implementing a complete feature takes dozens of minutes. An executor launched in the
background **doesn't survive the machine sleeping**: the watchdog cuts the stream and
execution dies where it was. This happened three times in a row on the first real
feature, with not a single file written, because all three died still in the reading
phase.

Before delegating in the background, warn and offer both options: keep the machine
awake during execution (`caffeinate -i` on macOS), or implement on the main thread,
which is resumable. The executor writes by checkpoint precisely so that an interruption
leaves reusable progress — but no checkpoint helps if execution dies before the first
`Write`.
