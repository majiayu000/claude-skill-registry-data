---
name: maw-context
description: |
  Author and maintain the MAW project-context overlay (`maw/project-context/`) — the project knowledge the pipeline injects into agents. Use when the user says "add project context", "set up MAW for this project", "register a project invariant / rule / lesson / tool / skill / domain for the pipeline", or "review MAW context proposals".
  Supports flag: --review to go straight to folding pending PCTX_PROPOSALS.md entries.
---

# MAW Project Context

You maintain the project-context overlay for the MAW pipeline. This is the **only** place project-specific knowledge lives — the base pipeline (`maw-execute-task`, `maw-tasks`, `agents/*.md`) stays 100% generic and never contains project text.

## What the overlay is

Three tiers, each gated on a different axis. Conflating them is the mistake to avoid.

Shared-memory paths, access rules, the `log.jsonl` schema, post-spawn lifecycle, and continuity rules belong only to the base `maw-execute-task` skill. Never duplicate or override them in project context.

1. **`maw/project-context/README.md` — CONSTANT, every agent, every stage.** The orchestrator injects it into every spawn with the `{PCTX}` placeholder substituted to the real path (so it is *near*-verbatim, not pure-verbatim). It holds only what is true regardless of subsystem or stage: a short orientation, universal invariants, and a **domain catalog**. It is paid on every spawn, so it is bounded by deliberate discipline, not "free".
2. **`maw/project-context/domains/<name>.md` — gated by DOMAIN.** A subsystem's normative invariants + risk lessons + pointers to bulky docs. Injected NORMATIVE into every running stage (including planner and plan reviewers — planning correctness needs them) when the task is in that domain. It reaches an agent two ways: pre-injected because `task.md` declared the domain, or self-loaded because the agent hit an observable trigger in the catalog (the recall safety net).
3. **`maw/project-context/agents/<stem>.md` — gated by STAGE.** Stage tooling / project skills / checklists for one agent only. `<stem>` ∈ `clarifier|premise-challenge|planner|plan-reviewer-1|plan-reviewer-2|implementer|code-reviewer|fixer|qa`. Build/test/runtime-QA commands and stage skills go here, not in README — clarifier and planners must not carry tooling they never use. If the same tooling genuinely applies to several stages, repeat it tersely in each; do not hoist it to README.

   Special case `agents/premise-challenge.md`: this agent is deliberately isolated from the task's premise lineage — it must see only the task and the real system. Its per-agent overlay may declare **only** where this project's primary sources / executable repro harness live (e.g. "the failing-test command is `make repro`", "runtime truth is observed via <tool>"). It must contain **no** premise narrative, no assumed root cause, no "how we usually do X" — that would re-inject the lineage the isolation exists to break. If you have nothing but narrative to add here, add nothing. The same access boundary protects `agents/plan-reviewer-1.md` and `agents/plan-reviewer-2.md`: none of these three overlays may instruct its role to read `log.jsonl`, transcripts, or reconstruct an omitted path.

Honest cost: the constant README grows with the number of domains (one catalog line each). At ~M domains it is roughly a few hundred tokens paid 8+ times per task. That is bounded and acceptable, not "tiny" — keep catalog entries to one line and prune dead domains.

Two rules that drive everything:

- **README is normative and global; a wrong line is law.** It beats the base for every future task with no adversarial reviewer to catch it (pipeline review agents verify *code satisfies the law*, they do not audit whether the law is correct — that gate is here, Step 3). Edit it like a shared constant. Growing unwieldy → move content into a domain module, do not bloat the constant.
- **Reduced, human-authored machinery — not zero.** The catalog is a minimal hand-written manifest; pre-inject is human-declared selective injection. This is deliberate and implementable in a prompt because a human authors it. There is no resolution engine, no token-budget gate, no includes.

## Step 0 — Detect state

Check whether `maw/project-context/README.md` exists.

- Absent → first-time setup; go to Step 1 (Scaffold).
- Present, user is adding/changing knowledge → Step 2 (Intake).
- Present, user asked to review proposals (or `--review`) → Step 3 (Review proposals).

## Step 1 — Scaffold

Create `maw/project-context/README.md` with this skeleton. Do not invent project facts — leave marked placeholders. Create `domains/` and `agents/` lazily (Step 2), never empty.

The body of this file is injected verbatim into every agent's spawn prompt, so it must read as content **for** the agent — never as a note to yourself about where things go (that discipline lives in this skill and in Step 4 validation, not in the file). The orchestrator already wraps it under a `## Project context (NORMATIVE — a constraint you must satisfy)` heading, so do not repeat a title or a "this is injected everywhere" line. Start at `## Orientation`:

```markdown
## Orientation
<!-- 2-4 lines: what this project is, the stack, the one architectural law
     nobody may break. A fresh-context agent is blind without this. -->

## Universal invariants
<!-- Rules true for ANY change regardless of subsystem (e.g. no secrets in
     code, public API is a contract, errors are typed not panics). 3-7 lines.
     If a rule only matters when you touch subsystem X → it is NOT here, it
     goes in domains/X.md. -->

## Domain catalog
<!-- One line per domain. The trigger MUST be zero-knowledge-observable:
     file/path globs, literal symbol / import / command tokens. NEVER a
     concept name ("the auth layer") — a fresh agent with no project
     knowledge must decide from the trigger alone. Module path uses the
     {PCTX} placeholder; the orchestrator substitutes the real path. -->
- trigger: <observable signal, e.g. files under `src/billing/**` or any `Decimal` use>  → {PCTX}/domains/money.md
- trigger: <observable signal, e.g. any file under `src/auth/**` or a call to `verify_token`> → {PCTX}/domains/auth.md

HARD RULE: before you plan or write any part whose work matches a trigger
above — even if this task was not framed as being in that domain — you MUST
read the mapped module from disk first and treat it as normative. Do not
proceed on that part without it.
```

Domain module skeleton (`domains/<name>.md`, created in Step 2 when the user has one):

```markdown
# Domain: <name>
# NORMATIVE when active — a constraint to satisfy, not a claim for you to audit.

## Invariants
<!-- Subsystem hard rules, verbatim. The few lines reviewers must see. -->

## Risk lessons
<!-- Curated, dated, one line each. Folded here via Step 3, not raw dumps. -->

## Pointers
<!-- Bulky canonical docs to read from disk (not paste): path → what it contains. -->
```

Per-agent file (`agents/<stem>.md`): only created in Step 2 when a single stage has tooling/skills the others must not carry.

If `maw/` is in `.gitignore` (local-only mode), tell the user the overlay still reaches worktrees because the orchestrator copies it in — already handled, no action from them.

## Step 2 — Intake interview

Ask what class of knowledge is being added, then route it:

- **Universal invariant** (any change, any subsystem) → `README.md` `## Universal invariants`. Keep it 3-7 lines total; if it is subsystem-specific it is not universal.
- **Domain invariant or risk lesson** (matters only in subsystem X) → `domains/X.md` (`## Invariants` / `## Risk lessons`). Create the module if absent **and** add/confirm its `## Domain catalog` line in `README.md` with a zero-knowledge-observable trigger (path glob / literal token — never a concept). The trigger is the recall safety net; a concept-only trigger is a defect.
- **Bulky doc / lesson file / notebook to reference, not inline** → the `## Pointers` section of the relevant `domains/X.md` (path + what it contains). Never pasted; agents read it from disk when in that domain.
- **Tooling** (build/test/runtime-QA command, MCP server, LSP op) → `agents/<stem>.md` for the stage(s) that run it (implementer/fixer/qa/code-reviewer). Not README.
- **Custom project skill** → `agents/<stem>.md` for the stage that invokes it: skill name + when to call it.

After writing, apply Step 4 (Validate). If `README.md` grew, push back: move content into a domain module, do not accept constant bloat.

## Step 3 — Review proposals (curated fold-in)

Pipeline agents never edit the overlay. When an agent hits a contradiction or a durable lesson it appends a dated entry to that task's `PCTX_PROPOSALS.md`. Folding is deliberate and happens here.

1. Scan all task folders (`maw/tasks/*/*/PCTX_PROPOSALS.md`) for proposal files.
2. Present each to the user with its source task: accept, edit, or reject.
3. For accepted ones, fold a tightened version into the **correct tier** — universal → README; subsystem → the matching `domains/X.md` (create + catalog line if it is a new domain); stage tooling → `agents/<stem>.md`. Same discipline as Step 2: curated, short, generalizing.
4. Append `> RESOLVED: folded into <target> on <date>` to the proposal in `PCTX_PROPOSALS.md`. Do not delete it — it stays with the task as history.
5. Run Step 4 (Validate).

Never auto-fold. A proposal from one pipeline run is unverified by design — the human is the gate.

## Step 4 — Validate

Run after any write, or on request:

- `README.md` exists, non-empty, and has only `## Orientation`, `## Universal invariants`, `## Domain catalog` — no tooling, no per-stage content, no pasted bulky docs.
- Every `## Domain catalog` line: trigger is zero-knowledge-observable (path/glob/literal token, not a concept), is one line, and its `{PCTX}/domains/<name>.md` target file actually exists. Dangling catalog entry or concept-only trigger → flag (an agent told to read a missing file, or unable to recognize the trigger from zero knowledge, is a hole).
- Every domain module referenced by the catalog has a catalog entry, and vice versa (no orphans either direction).
- No raw notebook dumps or whole-doc pastes anywhere — bulky sources are `## Pointers` references, not pasted.
- No overlay duplicates a shared-memory path, schema, access matrix, lifecycle, or continuity rule from the base pipeline.
- `agents/premise-challenge.md`, `agents/plan-reviewer-1.md`, and `agents/plan-reviewer-2.md` grant no transcript or `log.jsonl` read access. Flag a protected-role access grant or shared-memory duplication for human correction; never silently treat it as higher-priority law.
- README is reasonably short for being injected every spawn; if it is heavy, warn and propose cuts / moving content into domain modules.

Report what passed and what needs the user. Do not edit base pipeline files — this skill only touches `maw/project-context/` and reads `PCTX_PROPOSALS.md`.

## Persistence

`maw/project-context/` follows MAW's two modes: git-tracked (committed, propagates to worktrees automatically) or local-only (gitignored; the orchestrator copies the whole directory — `domains/`, `agents/`, README — into each worktree). You do not manage that; Step 1 of `maw-execute-task` handles the copy. In git-tracked mode, commit the overlay so worktrees and merges see it.
