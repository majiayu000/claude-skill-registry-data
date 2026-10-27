---
name: luke-docs
description: >
  Documentation generator, maintainer, and impact auditor for the Luke
  monorepo. Four modes: readme (creates/updates the root README.md,
  apps/*/README.md, packages/*/README.md and docs/README.md, with luke-docs
  markers), inline (JSDoc on TypeScript exports, tRPC procedure comments,
  Prisma /// field docs), adr (validates docs/decisions/ ADRs against the
  codebase and maintains the index), audit (read-only documentation-impact
  and semantic-drift review). Use when asked to generate, update, normalize,
  or review documentation, and after changes to architecture, public/API
  behavior, configuration, operations, release/deployment, developer
  workflows, or repository structure. One mode per invocation.
argument-hint: '<readme|inline|adr> [<path>] [--since <git-ref>] [--dry-run] | audit [<path>] [--since <git-ref>] | audit --full'
context: fork
agent: general-purpose
background: false
---

# Luke Docs — Documentation generator, maintainer, and impact auditor

Four modes:

| Mode     | What it does                                                                                       | Details reference                |
| -------- | ---------------------------------------------------------------------------------------------------- | --------------------------------- |
| `readme` | Creates/updates root `README.md`, `apps/*/README.md`, `packages/*/README.md`, `docs/README.md`       | `references/readme-templates.md` |
| `inline` | Normalizes source-code comments: JSDoc on TS exports, tRPC comments, Prisma field docs (`///`)       | `references/inline-rules.md`     |
| `adr`    | Validates the ADRs in `docs/decisions/` against the codebase, reports conflicts, maintains the index | `references/adr-rules.md`        |
| `audit`  | Audits documentation impact and semantic drift; reads and reports, but never writes                 | `references/audit-rules.md`      |

## Mode resolution — before anything else

**Invocation arguments:** $ARGUMENTS

Resolve the value above **first**: before reading any repository file, any
file in `references/`, the shared protocol, or running any git command. The
first whitespace-separated token is the mode. **One mode runs per invocation**
— there is no combined run; running all four modes requires four separate
invocations.

`<write-mode>` below is exactly `readme`, `inline`, or `adr`, case-sensitive.
Exactly these forms are accepted, in this order and no other:

| Form                                          | Effect                                        |
| --------------------------------------------- | --------------------------------------------- |
| `<write-mode>`                                | shared-protocol default scope                 |
| `<write-mode> --dry-run`                      | default scope, plan only                      |
| `<write-mode> --since <ref>`                  | files changed relative to `<ref>`             |
| `<write-mode> --since <ref> --dry-run`        | changed files, plan only                      |
| `<write-mode> <path>`                         | the owned target below `<path>`               |
| `<write-mode> <path> --dry-run`               | path-scoped plan only                         |
| `<write-mode> <path> --since <ref>`           | intersection of path and changed files        |
| `<write-mode> <path> --since <ref> --dry-run` | path-and-diff scoped plan only                |
| `audit`                                       | read-only audit on the shared default scope   |
| `audit --since <ref>`                         | read-only audit of files changed from `<ref>` |
| `audit <path>`                                | read-only audit below `<path>`                |
| `audit <path> --since <ref>`                  | read-only audit of the path/diff intersection |
| `audit --full`                                | read-only audit of the governed corpus        |

`<path>` and `<ref>` are each one token not starting with `--`. A path is
repository-relative, contains no `..` segment, and is accepted only when it
maps to the selected mode's ownership row below. Whether a path exists and
whether git can resolve a ref are checked later, before any write. Flag order
is fixed: the optional path precedes `--since <ref>`, which precedes
`--dry-run`. Quoting is not supported, so paths or refs containing whitespace
are not accepted. `--full` is exclusive to `audit`; `--dry-run` is exclusive
to the three write modes because `audit` is already read-only.

**Anything else fails closed.** Print

```
luke-docs: usage — <readme|inline|adr> [<path>] [--since <ref>] [--dry-run] | audit [<path>] [--since <ref>] | audit --full
```

and stop, having read nothing and written nothing:

| Case                               | Example                                                       |
| ---------------------------------- | ------------------------------------------------------------- |
| no mode                            | bare invocation, or `--dry-run` alone                         |
| unknown or differently-cased mode | `readm`, `ADR`, `Readme`, `all`                               |
| a flag before the mode            | `--dry-run readme`                                            |
| an unowned path                   | `readme docs/decisions/README.md`, `inline README.md`          |
| more than one positional path     | `readme apps/api packages/core`                               |
| an unknown or mode-invalid flag   | `readme --full`, `audit --dry-run`, `readme --force`           |
| a duplicated flag                 | `readme --dry-run --dry-run`                                  |
| `--since` without a value         | `readme --since`, `readme --since --dry-run`                   |
| reverse flag order                | `readme --dry-run --since HEAD~1`                             |
| tokens after the accepted form    | `readme packages/core --since HEAD~1 --dry-run extra`          |

## File ownership per mode

**Mode selection bounds what you write, never what you read.** Read whatever
the mode needs; write only the paths in its row.

| Mode     | Writes — and only these                                                                                                                                                                          | Never                                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `readme` | root `README.md`; `apps/*/README.md`; `packages/*/README.md`; `docs/README.md` — inside the markers, or the whole file when it does not exist                                                      | `docs/decisions/README.md` (owned by `adr`); any README nested deeper than one level, until an explicit decision adds it   |
| `inline` | comments in `packages/**/src/**/*.ts`, `apps/web/src/lib/**/*.ts`, `apps/web/src/hooks/**/*.ts`, `apps/api/src/routers/**/*.ts`, `packages/db/prisma/*.prisma`, per `references/inline-rules.md` | every README; anything under `docs/`; any change to executable behaviour                                                   |
| `adr`    | `docs/decisions/README.md`; the `Status` line(s) of explicitly named ADR files, and only on an explicit user decision                                                                             | `docs/README.md` (owned by `readme`); ADR Context / Decision / Consequences, always manual                                 |
| `audit`  | nothing — its report exists only in the session                                                                                                                                                   | every repository file and every tracked report                                                                            |

Rule 7's never-touch list below wins over every row.

A file outside your row that looks like it needs the work — a README under
`docs/decisions/` carrying markers, an ADR title disagreeing with the index, a
JSDoc gap noticed while reading `src/index.ts` — is **reported, not edited**:
list it in the final report as `owned by <mode>, not touched`. Noticing is not
authority to write.

**Before running the mode, read its file in `references/`** — it contains
templates, merge logic, and mandatory quality checklists.

**Also read `.claude/skills/luke-shared/audit-protocol.md`** and apply the
sections its applicability table assigns to the selected mode. §1 scoping and
§7 concurrent sessions apply to all four modes; §7.2 applies only to the three
write modes. The findings-related sections apply only to `audit`, as the shared
table records. The grammar above deliberately narrows the shared selectors:
`--full` is read-only and audit-only, while a write-mode path must map to that
mode's ownership row. No invocation regenerates the whole documentation tree in
one pass.

**Ownership**: `.claude/skills/luke-shared/governance-map.md`. This skill owns
documentation impact and semantic documentation drift, plus generated README,
JSDoc, Prisma field docs, and the ADR index. It owns no code-compliance,
architectural, or platform decision. Within it, write ownership is per mode:
the table above is where that is written, and every other statement points here.

---

## Mandatory rules (take precedence over everything else)

1. **Read before write** — in a write mode, never generate content for a file
   without having read it first. `audit` never writes.
2. **No SQL, no migrations, no test runner** — the `packages/db/prisma/*.prisma`
   files are read as text; never `prisma migrate/generate`, `pnpm db:*`, `pnpm test`.
3. **Parallel agents: max 3** simultaneously.
4. **Preserve markers** — never overwrite content outside the
   `luke-docs:start/end` markers. Nothing listed under "What it checks" in the
   header of `tools/scripts/check-docs-integrity.ts` — markers, links,
   fragments, reachability, ADR index and citations, among others — is
   verified here: that checker owns it, blocking in CI. It's
   pure parsing, and parsing entrusted to an LLM is a level-4 control where a
   level-2 one is enough.
5. **Dry-run** — in a write mode, `--dry-run` prints the plan without writing
   any file. `audit --dry-run` is invalid because `audit` is always read-only.
6. **No placeholders** — never `TBD`, `TODO`, `…`, `{to be filled in}` in
   generated text. If information is missing: omit the section and flag it
   in the report.
7. **Never touch**: `.planning/`, `CLAUDE.md`, `lessons.md`, `lessons-archive.md`.
   Never change an ADR's `Status` without an explicit user decision.
8. **No volatile platform facts in generated text** — a framework or tool is
   named, never versioned. Versions are read from the manifests at the moment
   anyone needs them (`.claude/skills/luke-deps/references/platform-policy.md`).
   A README that states a version is a second source of truth that drifts: the
   template here said `Next.js 15` while `apps/web` was on 16.
9. **Always a final report** — files created/updated/unchanged for write modes,
   findings for `audit`, what stayed out of mode, and flagged issues. One block,
   for the mode that ran; see the report section below.
10. **Commit suggestion** at the end — the one for the write mode that ran,
    from the report table. `audit` reports `none — read-only audit`. Never name
    a mode that did not run.

## Language

All generated or updated technical prose is English. The canonical rule,
including the temporary product-UI exception and the treatment of frozen
historical material, is in `CLAUDE.md`; its rationale is ADR-030. This skill
implements that policy and does not restate or extend it.

---

## Scope resolution

After the grammar is accepted, resolve the selector through
`audit-protocol.md` §1. An explicit selector always wins; never derive the
default diff first.

**Path validation for write modes is fail-closed:**

- `readme` accepts `README.md`; `apps/<workspace>` or its `README.md`;
  `packages/<workspace>` or its `README.md`; and `docs` or `docs/README.md`.
  The workspace directory must contain a tracked `package.json`. A directory
  maps to its one owned README; it does not recursively select nested READMEs.
- `inline` accepts only a file or directory inside the source roots in the
  ownership row. After recursive expansion, every selected file must match an
  owned `.ts` or `.prisma` pattern.
- `adr` accepts only `docs/decisions`, its `README.md`, or one tracked
  `NNN-*.md` ADR. Selecting one ADR still permits regenerating the one shared
  index; it never permits changing that ADR's Context, Decision, or
  Consequences. A `Status` line changes only on an explicit user decision, per
  the ownership table.
- `audit` accepts any existing repository-relative file or directory because
  code can create documentation impact. It writes nothing. `audit --full`
  selects the governed Markdown corpus and reads code only as evidence.

Reject absolute paths, `.` or an empty path token, `..` segments, paths outside
the repository, and paths that do not satisfy the selected mode's rule. Do not
reinterpret a rejected path as a default-scope invocation.

For `--since <ref>`, first require git to resolve `<ref>`, then derive changed
paths with `git diff --name-only --diff-filter=d <ref>` plus
`git ls-files --others --exclude-standard`: the working tree against `<ref>`,
uncommitted and untracked work included, deleted paths left out. So
`audit --since HEAD` sees the change about to be staged, and a write mode's
`--since HEAD~1` includes uncommitted work too. A path plus `--since` is the
intersection of that list and the validated path. For the default and
`--since`-only scopes, the mode maps resolved paths to targets:

- `inline`: owned `.ts` and `.prisma` files only;
- `readme`: a workspace README when that workspace is selected; root
  `README.md` when a root manifest or any workspace is selected; and
  `docs/README.md` when a document below `docs/` is selected;
- `adr`: ADRs whose decisions bear on the selected changes, plus the index;
- `audit`: governed documentation affected by the selected code or document
  paths, with directly relevant code and authorities read as evidence.

An explicit `readme <path>` selects only the README mapped from that path,
including a missing owned README. It never adds other missing READMEs. An
explicit `adr <ADR path>` validates only that ADR and maintains the index.

No relevant path after resolution → stop with
`No relevant file in the resolved scope. Nothing to do.` and write nothing.

---

## `readme` mode

**Phase 1 — Explore (mandatory).** Read in order:

1. Root `package.json` (workspaces, scripts, engines) + `turbo.json`
2. For every workspace: `package.json`, `src/index.ts(x)`, existing `README.md`
3. `.env.production.example` + env policy in `CLAUDE.md` — env var catalog
   (enforcement is `assertEnvPolicy()` in `apps/api/src/server.ts`)
4. `packages/db/prisma/*.prisma` — model names only (multi-file schema, split by domain)
5. `apps/api/src/routers/` — list of router files (names, not content)
6. `apps/web/src/app/` — 2-level directory tree
7. `docs/` — recursive listing of `.md` files (H1 titles, path). Input for
   `docs/README.md` only: the ADR titles it surfaces belong to `adr` mode, and
   noticing that `docs/decisions/README.md` disagrees with them is a report
   line, not work for this mode
8. `.planning/ROADMAP.md` — only to understand direction (don't reproduce)

Build a dictionary: `workspace → { name, description, dependents[], envVars[], exports[], scripts[], routerNamespaces[] }`.

**Phase 2 — Generate README** using the templates in
`references/readme-templates.md`, and no other README, in this order: root +
apps (max 3 in parallel) → packages (max 3 in parallel) → `docs/README.md`.
The order is fixed; the membership is not — regenerate only the targets the
resolved scope selected. A missing README is created only when its workspace is
selected by the resolved scope. An explicit path selects exactly one target.

**Phase 3 — Semantic consistency:** package names in "Used by"/"Internal
dependencies" match the real names; sections omitted for missing information
are flagged in the report.

Nothing listed under "What it checks" in the header of
`tools/scripts/check-docs-integrity.ts` is to be verified by hand:
`pnpm check:drift` checks it in CI. If it fails, the link must be fixed or removed — never added to an
exceptions list, or the checker becomes furniture.

---

## `inline` mode

**Phase 1 — Audit (mandatory).** Build the target list:

- `packages/**/src/**/*.ts`: exports without JSDoc, drifted JSDoc, `//` on public exports
- `apps/web/src/lib/**/*.ts` and `apps/web/src/hooks/**/*.ts`: same treatment
  (`references/inline-rules.md` holds the boundary — not `components`, not `app`)
- `apps/api/src/routers/**/*.ts`: procedures without `/** */` or without input/output/RBAC permission
- `packages/db/prisma/*.prisma`: fields and models without `///`

**Phase 2-4 — Write** following the templates and merge logic in
`references/inline-rules.md`: package JSDoc (max 3 in parallel) → tRPC
comments (max 3 routers in parallel) → Prisma field docs.

---

## `adr` mode

**Phase 1 — Discover:** read the files in `docs/decisions/`; for each one
extract the title, `Status`, and key statements from the Decision section.
If `docs/decisions/` doesn't exist: flag it in the report and stop.

**Phase 2 — Validate** against the codebase (max 3 ADRs in parallel) per
`references/adr-rules.md`. **Change no `Status` field.** An Accepted ADR is
normative until a human supersedes it, so a contradiction with the code is
reported as `ADR/CODE CONFLICT` and left for decision — see the reference for
why the alternative lets an agent repeal an architectural decision by noticing
the code disagrees with it.

**Phase 3 — Regenerate the index** `docs/decisions/README.md` — the only file
this mode regenerates; an ADR `Status` line is the one other thing it may
write, and only on an explicit user decision (see the ownership table).
`docs/README.md` links to this index and is readme-owned: a stale entry there
is reported as `owned by readme, not touched`.

---

## `audit` mode

Read `references/audit-rules.md` and remain read-only for the entire mode.

**Phase 1 — Establish impact:** resolve the scope, identify the documentation
owned by or describing the changed surfaces, and load the relevant current
authorities. A code-only scope is valid: the question is whether its behavior,
architecture, configuration, operation, release process, developer workflow,
or repository structure changed in a way documentation must reflect.

**Phase 2 — Compare semantics:** verify claims in the affected documentation
against repository evidence. Report stale, contradictory, missing, or
misclassified current guidance with specific evidence. Do not duplicate the
mechanical checks listed under "What it checks" in the header of
`tools/scripts/check-docs-integrity.ts`, and do not judge whether code complies
with `CLAUDE.md` or an ADR — that belongs to `/luke-audit`.

**Phase 3 — Report only:** apply the findings-related protocol sections, state
the documentation-impact verdict, and emit the report in the session. Create
no report file, modify no documentation, and suggest no commit.

---

## Final report (mandatory format)

One block, for the mode that ran. Never print a block — or a counter — for a
mode that did not run: the run reports what it did, not what the skill can do.

```
=== luke-docs report — <mode> ===

  <the counter lines for that mode, from the table below>

Out of mode (not touched): <path — owned by <mode>> | none

Suggested commit:
  <the commit line for that mode, from the table below>
```

| Mode     | Counter lines                                                                                                    | Commit line                                    |
| -------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `readme` | `Created` / `Updated` / `Unchanged` file counts; `Sections omitted (missing info)`                                | `docs: update readme tree [luke-docs]`         |
| `inline` | `JSDoc added` / `JSDoc updated` symbols; `tRPC comments`; `Prisma fields`; `Flagged stale code`                   | `docs: normalize inline comments [luke-docs]`  |
| `adr`    | `Validated`; `Confirmed`; `ADR/CODE CONFLICT` (with evidence, awaiting decision); `Not verifiable`; `Status changed` (normally 0); `Index updated` | `docs: update adr validation [luke-docs]`      |
| `audit`  | `Documentation impact`; `Confirmed findings`; `Needs decision`; `Suppressed by baseline`; `Files written: 0`      | `none — read-only audit`                       |

The `Out of mode` line is **mandatory in every report**, `none` included: a
missing line and an empty one are different claims, and only one of them says
you looked.
