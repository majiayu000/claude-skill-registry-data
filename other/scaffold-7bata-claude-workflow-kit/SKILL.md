---
name: scaffold
description: Lay down the methodology scaffolding in place inside the current project directory (CLAUDE.md + the eight-doc set + .gitignore + README). The backend stack is fixed to Go (version baseline in the table inside the skill); Claude decides the database based on project intent. Triggered when the user says "set up scaffolding / initialize project / start new project / scaffold"; also triggered when the user describes wanting to build a new product/tool/website while not currently inside a project directory (Auto mode, paired with the auto-scaffold standing rule).
allowed-tools: Bash, Read, Write, Glob, AskUserQuestion
---

# /scaffold

Lay down the methodology scaffolding in place, inside an **already-existing** project directory. **Respond in English by default** (technical identifiers stay in English).

Templates live in this skill's `templates/` subdirectory. When reading templates with Glob/Read, base the path off the skill's "Base directory for this skill" as given at invocation time, joined with `templates/` — do not hardcode an absolute path.

## Tech stack baseline (fixed, no selection process)

The backend stack is **fixed to Go**, with version and library choices unified under the baseline below (a fixed baseline is part of this methodology: no re-deciding per project; if you want to change the stack, edit this table rather than deviating once, ad hoc):

| Component | Choice / Version | Notes |
|---|---|---|
| Backend language | Go 1.25 (built via `golang:1.25-alpine`) | Standard library `net/http` + chi router, no heavyweight framework |
| DB access | pgx (hand-written repository) | No ORM, no sqlc — `internal/repo` writes typed SQL directly |
| Migrations | golang-migrate | Pure SQL versioned migrations (`NNNN_*.up.sql / down.sql`) |
| Validation / serialization | `encoding/json` + go-playground/validator | Request/response schema validation |
| Frontend (if needed) | React + TypeScript + Vite | `node:20-alpine` used only at build stage |
| Runtime image | `alpine:3.20` | Docker multi-stage build, single static binary, `/health` health check |
| Directory layout | `backend/cmd/server` entrypoint + `backend/internal/{config,db,repo,handlers,service,model,middleware}` | Go community convention; frontend under `frontend/src` |

Keep the backend service **stateless** (all state lives in the database), leaving room for horizontal scaling across multiple replicas.

## SQLite branch (the concrete substitutions when Step 3 picks SQLite)

The baseline table above defaults to PostgreSQL (pgx + golang-migrate + a postgres container/instance). If Step 3 determines **SQLite** (small, low-concurrency / single-machine appliance scenarios), swap the DB access layer and migration tool per the table below; the Go version, validation library, runtime image, and directory layout (`backend/internal/{db,repo}` etc. keep their names — only the implementation inside changes) stay unchanged — this is not "adjust as you see fit," follow it as written:

| Component | SQLite substitute |
|---|---|
| DB access | `database/sql` + `modernc.org/sqlite` (a pure-Go driver, no cgo, compiles directly with `CGO_ENABLED=0`; do not use the cgo-dependent `mattn/go-sqlite3`) |
| Migrations | golang-migrate's `sqlite` (modernc, pure-Go) driver; migrations stay `NNNN_*.up.sql/down.sql`; do not use the cgo `sqlite3` driver; absent a migration framework dependency, this can also degrade to running an embedded schema SQL at startup (`embed.FS` holding a `schema.sql`) — good enough for small projects |
| Data file | A single file at `data/{{PROJECT_NAME}}.db` (reuses the `data/` directory this skill already writes to disk); no PG container/instance is provisioned |
| Concurrency note | Turn on `_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)`; avoid holding long-lived transactions on write paths |

**Placeholder linkage**: in `{{TECH_STACK}}`, replace `pgx + golang-migrate` with `database/sql (modernc.org/sqlite) + golang-migrate (sqlite driver)`; fill `{{DATABASE}}` with `SQLite`.

**`docs/DECISIONS.md.tmpl`'s pre-seeded first entry is self-contradictory as-is and must be edited**: line 9's What — "Backend Go 1.25 (net/http + chi + pgx + golang-migrate), database {{DATABASE}}" — leaves `pgx + golang-migrate` unchanged while `{{DATABASE}}` renders as `SQLite`, producing "...pgx + golang-migrate...database SQLite" in the same sentence, a direct contradiction; before writing to disk, replace that half-sentence with `database/sql (modernc.org/sqlite) + golang-migrate (sqlite driver)`. Then append a separate entry recording the rationale for choosing SQLite, per "append a decision entry" below.

**In `docs/ARCHITECTURE.md.tmpl`, the `pgx`/`BIGSERIAL`/`TIMESTAMPTZ`/`pgxpool` occurrences in sections 1/3/6 are hardcoded prose, not placeholders** (this template has not been made database-branch-aware). After writing `docs/ARCHITECTURE.md` to disk, if SQLite was chosen you must manually rewrite these spots per the table below — otherwise the doc contradicts the actual stack, and DDL written per `BIGSERIAL`/`TIMESTAMPTZ` will fail to create tables under SQLite outright:

| Location | PostgreSQL original | Rewrite for SQLite |
|---|---|---|
| Section 1, "DB driver / queries" row | `pgx (hand-written repository)` | `database/sql + modernc.org/sqlite (hand-written repository)` |
| Section 3, table-design conventions | `id BIGSERIAL PK`, `created_at/updated_at TIMESTAMPTZ` | `id INTEGER PRIMARY KEY AUTOINCREMENT`, `created_at/updated_at TEXT` (ISO8601 strings — SQLite has no native TIMESTAMPTZ type) |
| Section 6, directory-layout comments | `pgx connection pool` / `pgxpool connection pool` / `hand-written pgx repository` | Rewrite accordingly to `database/sql (modernc.org/sqlite) connection` / `hand-written repository` |

Append an entry to `docs/DECISIONS.md` recording the rationale for choosing SQLite (already required by Step 3).

This skill's on-disk scope is 11 general-purpose files; the SQLite branch does not change that file count. Aside from the manual rewrites the table above requires for `docs/ARCHITECTURE.md` body text and the `docs/DECISIONS.md.tmpl` pre-seeded first entry, every other file only changes which value a tech-selection placeholder resolves to.

## CLI / no-network-service branch (the concrete substitutions when Step 3 determines a pure CLI / batch job)

The baseline table above defaults to exposing an HTTP interface (`net/http + chi` + `/health` health check + container runtime). If Step 3 determines the project is a **pure CLI / batch job** (no HTTP interface, no port listening), swap per the table below — this is not "adjust as you see fit," follow it as written:

| Component | CLI substitute |
|---|---|
| `{{TECH_STACK}}` | `Go 1.25 standard-library CLI + <DB access stack>` (`<DB access stack>` per the baseline table or the SQLite branch above); do not write `net/http + chi` |
| Directory layout | `backend/cmd/<binary>` entrypoint + `backend/internal/{cli,core,db,repo,model}`; do not create `handlers/` or `middleware/` |
| `docs/ARCHITECTURE.md` | Drop the routing/HTTP-interface row from Section 1; sync Section 6's directory-layout comment to `cmd/<binary>` + `internal/{cli,core,db,repo,model}`, with no `handlers`/`middleware` mentioned |
| `docs/DEPLOYMENT.md` | Deployment shape: "single binary, `CGO_ENABLED=0 go build`, no container/port/health check"; do not write the `alpine` runtime image or `/health` |

## Step 1: Confirm project name and directory

```bash
basename "$PWD"
```
Take the current folder name as the project name. Confirm the current directory is indeed the project root to be scaffolded.

## Step 2: Intake — gather project intent

Explain to the user and collect:

> Tell me the idea for this project / a meeting summary, or point me to a file (e.g. meeting notes `*.md`) — I'll use it to determine the tech stack, database, core invariants, and module breakdown.

- If the user gives a file path → Read it; if it's **meeting notes**, archive the raw content into the first section of `docs/MEETINGS.md` when writing to disk, and separately distill any **business facts** it contains into `docs/BUSINESS.md` (previously all of this distillation duty fell to REQUIREMENTS; it's now split between facts and decisions)
- If the user describes it verbally → use the conversation content
- If there isn't enough information to decide, ask **targeted** follow-up questions (not generic ones)

Beyond deciding the tech stack/DB, **ask through the following 7-slot business-context checklist** (used to fill in `docs/BUSINESS.md`; leave a placeholder comment for any slot with insufficient information — don't press the user or block the flow):

1. Goal & current manual process — before this system existed, who did it, with what tools, step by step, and where were the pain points?
2. Input: transactional data — what data varies on every run, and is there a real sample file?
3. Input: reference/config data — lookup tables, rule tables, allowed values, and is there an existing file?
4. Processing flow — how input becomes output
5. Output — what gets produced, for whom, in what shape, and is there a sample of the expected output?
6. Business hard rules & exceptions — rules that must never be violated, and how exceptions are handled today
7. Human review & feedback — who reviews, what can they change, and should the corrected result feed back into the system?

## Step 3: Decide and confirm

Based on the intake, list the following items for the user along with your reasoning, and use AskUserQuestion to have the user confirm/revise:

1. **Backend tech stack** — **fixed to Go, no question asked, no selection process** (see the "Tech stack baseline" table at the top). Only **state** to the user that this baseline will be used; if the user actively asks to switch stacks, treat it as a signal to update this skill's baseline table rather than deviating just this once
2. **Database**:
   - **PostgreSQL by default** (for concurrency / most scenarios; Go side uses pgx + golang-migrate, per the baseline table)
   - **SQLite only for small, low-concurrency / single-machine appliances** (e.g. a mac mini appliance) — if chosen, follow the "SQLite branch" section above
   - Basis for the decision: concurrency level, deployment shape (cloud vs. single machine), data scale
3. **Whether a web frontend is needed**: if yes, follow the baseline React + TypeScript + Vite; for pure API / CLI projects, no frontend directory. If this is determined to be a pure CLI / batch job (no HTTP interface, no port listening), follow the "CLI / no-network-service branch" section above
4. **Core invariants**: 0–N architectural constraints this project must "never break." Leave a placeholder if you can't think of any yet
5. **Module breakdown**: top-level module names + one-line responsibility each. Leave a placeholder if unclear

State the **reasoning** behind each item, and let the user sign off. Only write to disk after confirmation.

## Step 4: Write to disk (with conflict protection)

First list the 11 target files to be written, and **check each one for existence**:

```bash
for f in .claude/CLAUDE.md docs/PLAN.md docs/Progress.md docs/ARCHITECTURE.md docs/DEPLOYMENT.md docs/REQUIREMENTS.md docs/BUSINESS.md docs/DECISIONS.md docs/MEETINGS.md .gitignore README.md; do
  test -e "$f" && echo "EXISTS: $f"
done
```

- If any `EXISTS` show up → list them and ask the user: skip / back up and rename (`.bak`) / manually merge. **Never overwrite silently**
- If no conflicts → proceed

For each template: Read the template content → substitute placeholders → Write to the target path. Placeholder substitution table:

| Placeholder | Value source |
|---|---|
| `{{PROJECT_NAME}}` | Folder name from Step 1 |
| `{{ONE_LINER}}` | One-line positioning distilled from intake |
| `{{DATE}}` | `date +%F` |
| `{{TECH_STACK}}` | Fixed baseline: `Go 1.25 (net/http + chi) + pgx + golang-migrate`; if SQLite is chosen, substitute per the "SQLite branch" section; if this is a pure CLI / batch job, substitute per the "CLI / no-network-service branch" section instead — do not write `net/http + chi`; if there's a frontend, append `; frontend React + TypeScript + Vite (Node 20 build)` |
| `{{DATABASE}}` | Database from Step 3 |
| `{{INVARIANTS_BLOCK}}` | Core invariants from Step 3; if none, `<!-- TBD: this project's core invariants -->` |
| `{{MODULES_BLOCK}}` | Module breakdown from Step 3; if none, `<!-- TBD: module breakdown -->` |
| `{{CODE_CONVENTIONS_BLOCK}}` | Go code conventions generated from the baseline (Go 1.25, gofmt, explicit error handling with wrapping, `cmd/` + `internal/` layout, minimal dependencies); if there's a frontend, append TS conventions (strict mode, components organized by page directory) |

Template path mapping: `templates/docs/X.md.tmpl` → `docs/X.md`; `templates/gitignore.tmpl` → `.gitignore`; `templates/CLAUDE.md.tmpl` → `.claude/CLAUDE.md`; `templates/README.md.tmpl` → `README.md`. Also create an empty placeholder directory `data/.gitkeep`. (data/.gitkeep is an extra placeholder outside the checklist; total physical files = checklist count + 1 — reconcile accordingly during self-check)

**Pre-filling content** (don't just substitute placeholders — fill in real content wherever possible):

- `docs/REQUIREMENTS.md`: fill in as much real content as possible from what intake distilled (Product Positioning, Target Users & Roles, Phased Roadmap, Confirmed Decisions); leave a TBD comment for anything that can't be filled in; the template ships with a "Goal Ledger (Inbox)" section — leave the table empty at scaffold time, no follow-up needed
- `docs/BUSINESS.md`: fill in each section with what the 7-slot checklist collected (goal & current process, inputs/outputs, processing flow, business hard rules, human review, …); leave the template's own TBD comment for any slot that can't be filled
- `docs/MEETINGS.md`: if intake came from meeting notes, archive the raw notes as the first section; otherwise keep the empty skeleton
- `docs/DECISIONS.md`: the template comes with a "Go baseline" first entry; if Step 3 produced other significant decisions (e.g. rationale for choosing SQLite), append a What/Why/Changes entry for each

## Step 5: Wrap-up

```bash
set -e
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main
git add -A
git commit -m "chore: initialize project scaffold"
git rev-parse HEAD >/dev/null 2>&1 && echo "Initial commit created ✓" || { echo "⚠ Repo not initialized / not committed, stopping"; exit 1; }
```

Once the initial-commit check passes, update `docs/PLAN.md`'s Phase 0 heading to `## Phase 0: Environment & Scaffolding ✅ <output of date +%F>`; if the check fails, leave the heading as-is and append `(not yet under version control — git commit still pending)`.

After writing to disk, **self-check**:
```bash
grep -rl '{{' .claude docs README.md 2>/dev/null && echo "⚠ Unreplaced placeholders remain" || echo "All placeholders replaced ✓"
LC_ALL=C grep -rl $'\xef\xbf\xbd' .claude docs README.md 2>/dev/null && echo "⚠ Garbled text found" || echo "No garbled text ✓"
```

Report to the user: which files were generated, the tech stack/DB decisions, and next-step suggestions (`/brainstorming` to start design — once the spec is written, go straight into ultracode implementation; small changes also get a small spec (a few paragraphs are enough) — write it, then go straight ahead).

If, as the project progresses, a reusable component/module gets distilled out (not part of this scaffolding pass — a reminder for the future): **if the team maintains a component index, register it there** so other projects can discover and reuse it during research.

## Auto mode (triggered silently by the auto-scaffold standing rule)

This runs **alongside** the manual interactive flow above, which stays unchanged word for word. When silently triggered by the auto-scaffold hook, follow this section instead — never pause to ask, never present options:

- **Skip the intake follow-up questions in Step 2 and the 7-slot business checklist, and skip the AskUserQuestion confirmation in Step 3** — don't stop to wait for the user's answers; judge directly from the information already present in the request sentence;
- **Database defaults to PostgreSQL**; only follow the existing SQLite branch or CLI branch in Step 3 when the request sentence contains a clear signal such as single-machine / offline / pure command-line, and record the rationale in `docs/DECISIONS.md` as usual (Step 4's "Pre-filling content" requirements for `docs/DECISIONS.md` apply unchanged);
- `docs/REQUIREMENTS.md` gets its one-line positioning and initial requirements filled directly from the request sentence; `docs/BUSINESS.md`'s 7 slots are **all** left as the template's own TBD placeholder comments (no follow-up questions — left for a later conversation to naturally fill in); `docs/MEETINGS.md` stays as the empty skeleton;
- Step 4's conflict protection simplifies to a fail-safe in Auto mode: Auto mode should only ever run inside a freshly created empty directory, and the moment any `EXISTS` file turns up — **don't ask skip/backup/merge, immediately downgrade to interactive mode**, never overwrite silently;
- Step 5's wrap-up (`git init -b main` + initial commit + placeholder/garbled-text self-check) runs unchanged; compress the completed wrap-up report into one line;
- Auto is a parallel entry point alongside the manual flow — it does not replace or rewrite the body text of any step above.

