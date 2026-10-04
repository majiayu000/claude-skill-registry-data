---
name: bootstrap
description: Use when a repository must be conditioned for continuous autonomous development (CDev) — a new repo, an existing one without docs/develop/, or a re-audit of one already conditioned; when the user asks to "bootstrap", "condition this repo for cdev", "prepare it so /cdev can work alone", "condicionar para cdev" — for any role (backend, frontend, other), with or without a folder of source docs.
---

# Bootstrap (CDev)

Conditions one repository for autonomous execution with an **elevated autonomy threshold**: the
agent that later runs `/cdev` stops only at real blockages, never to ask "now what?". Two
mandatory halves — skipping the second is what makes autonomy dangerous:

- **Half A — Structure:** write the CDev machinery into the repo, adapted to what the repo
  actually is.
- **Half B — Clarity:** audit how far it is clear *what* must be produced; clarity bounds
  autonomy.

Idempotent: on an already conditioned repo it acts as an audit and proposes diffs, never
overwrites silently.

Base material: the package's `templates/` (placeholder contract in `templates/PLACEHOLDERS.md`;
zero unresolved `{{` at the end) and the role profiles in `profiles/` — resolve this skill's
base directory to its **real path first** (dereference junctions/symlinks), then both live at
`../../` from there.

## Resolve the role

Inspect before assuming: own schema/services and no UI → **backend** (`profiles/backend.md`);
consumes an external backend and renders UI → **frontend** (`profiles/frontend.md`); both or
neither → **other**: no profile ships — the conditioning itself must write into the repo's
protocol the four things a profile would supply (what "verified" means, what "evidence" means,
the hardest gate, the self-chosen work order). What the user declares wins over the guess.

## Half A — Structure

1. **Recognize before writing.** Read the real repository: stack, manifest and lockfile, real
   scripts, schema/migrations, targets, existing guides and docs. Compose the **recognition
   document** (`docs/develop/RECOGNITION.md` — drafted now, written to disk with everything
   else after the human gate): what the repo actually is, its real architecture
   patterns (extracted from code, they exist nowhere else), and **every place a generic
   assumption must be overridden**. A conditioning that renders templates without this step
   produces a plan for a repository that does not exist.
   While reading, **check the repo's operational documents against each other** (runbooks,
   deploy docs, existing guides): the loop trusts instructions, so two documents disagreeing
   about the same switch is an incident waiting. A contradiction found is resolved with the
   human or recorded as an open question — never left standing.
2. **Materialize the role profile into the repo's protocol.** The profile brings the role's
   four things; conditioning makes them concrete here:
   - **Verification** (profile §1): fix the exact sequence from the repo's real scripts — and
     **verify each gate before trusting it**; the profile lists the role's known traps (gates
     that lie, missing frameworks). A missing mandatory gate becomes the plan's first batch or
     a written blocking requirement, never an omission.
   - **Evidence** (profile §2): write what a `DONE` must prove here, and with which tooling;
     missing tooling is a written blocking requirement.
   - **Hardest gate** (profile §3): perform the role's classification (e.g. the database's
     shared-vs-ephemeral nature, the consumed backend's contract and pins) and write the
     resulting gates into guide + protocol.
   - **Self-chosen work order** (profile §4): write it into the protocol's stop-conditions
     section — when the plan runs out the agent derives next work itself in that order and
     stops only at real blockages. This is what legitimizes `/cdev` not stopping.
3. **Render the core artifacts** from `templates/`, resolving every placeholder: repo guide
   (`AGENTS.md` — the agent-neutral standard; when the running host reads a different guide
   filename, also write that host's pointer file, whose entire content is the import line —
   under Claude Code: a `CLAUDE.md` containing exactly `@AGENTS.md`), `docs/develop/`
   (protocol with local deltas only, SPRINTS, PROGRESS, DECISIONS, PRODUCT). The handoff log's ordering is **declared explicitly in the protocol**
   (default: newest-first). Optional on request: TESTING, RUNBOOK, ROADMAP, ARCHITECTURE, and
   the night-runner script (a quota-resumption convenience only — the primary loop is the
   `cdev` skill; continuity is a property of the repository, not of a live process; its
   `gitignore-additions` render with it, not by default). **Not rendered by default:** the
   reviewer/runner agent templates and the per-repo runtime skills — unevidenced in six weeks
   of field use; render them only if the repo asks for them. The greenfield conditioning-plan
   document is gone entirely.
4. **Existing files are never clobbered:** diff and ask, file by file.

## Half B — Clarity

1. **Source inventory.** Product/spec docs, designs, contracts (a consumed producer's schema or
   reports), READMEs, existing code. Order by authority.
2. **Score every domain area:**
   - `DEFINED` — spec + derivable acceptance criteria (for a consumer role: the upstream
     contract exists too). The agent may work it alone.
   - `PARTIAL` — intent clear, detail ambiguous — or the upstream contract is missing, which
     caps an area at PARTIAL. Work the clear part; every assumption recorded in DECISIONS.
   - `ABSENT` — only the name exists. Inventing it is forbidden: open question, never a batch.
3. **Write the clarity map** in `docs/develop/PRODUCT.md` (table: area → level → source → open
   questions). It is the boundary of autonomy: `/cdev` self-selects work only inside
   DEFINED/PARTIAL.
4. **Derive SPRINTS.md as far as clarity reaches.** Sprint 01 `ACTIVE`, Batch 01 `READY`,
   observable acceptance written before the work (including the role's required evidence).
   PARTIAL areas → batches with assumptions noted; ABSENT → open question only.

## Human gate (single)

Before writing any file: present the resolved-placeholder table + the clarity map + the
phase/sprint outline. One confirmation (or edits), then write everything.

## Safety gates the bootstrap leaves written (non-negotiable)

The core shape — blast radius beyond the working branch, irreversible operations on shared
state, real money and live credentials — plus the role's typical list from profile §3, made
concrete for this repo. The elevated profile raises *what to work on*, never these.

## On finishing

Validate: zero unresolved `{{`, exactly one `ACTIVE` sprint (`scripts/verify-bootstrap.ps1`
automates both). Seed the first `AGENT_PROGRESS.md` entry (bootstrap done, Sprint 01 ACTIVE,
next action = `/cdev`), **commit the conditioning artifacts on the current branch** (the
branch convention governs batch work, not this commit; the machinery must not sit as
uncommitted WIP under the first batch), and print a "conditioned — how to launch" summary.
