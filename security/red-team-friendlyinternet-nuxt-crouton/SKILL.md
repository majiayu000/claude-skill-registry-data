---
name: red-team
layer: method
description: Adversarially probe this monorepo for security flaws at the right depth. Steers the red-team subagent — picks quick/standard/deep from the request, spawns it (fanning out for a wide deep sweep), collates findings into a dated report, and files security/sec:* issues for confirmed high/critical findings. Use when asked to "red-team", "try to hack this", "find security holes", "pentest this package/app", or as the brain behind the CI + daily security runs.
argument-hint: "[quick|standard|deep] [scope: a path | diff | repo]"
allowed-tools: Read, Grep, Glob, Bash, Agent, mcp__github__issue_write, mcp__github__search_issues, mcp__github__get_label
---

# Red-Team Skill — the steering brain

You drive the adversarial security probe. The actual analysis lives in the
**`red-team` subagent** (`.claude/agents/red-team.md`) — this skill decides *how deep* to
go, *spawns* the agent, *collates* what it finds, and *files* the serious stuff as GitHub
issues. Keep the attack logic in the agent; keep orchestration here.

## 1. Resolve `{ depth, scope }` from the request

| The user said… | depth | scope |
|----------------|-------|-------|
| `/red-team` (bare) | `standard` | the current package/app if obvious from cwd/context, else **ask** which |
| `/red-team quick` / a PR/diff context | `quick` | `diff` (changed files vs base) |
| `/red-team standard apps/velo` | `standard` | `apps/velo` |
| `/red-team deep` / "full sweep" / "everything" | `deep` | `repo` |
| names a package/app | (keep stated/ default `standard`) | that path |

Defaults: depth `standard`; for `deep` with no scope, default scope `repo`. If depth is
`standard`/`quick` and **no** scope can be inferred, ask the one question ("which package or
app?") rather than guessing the whole repo (a whole-repo standard run is expensive).

## 2. Spawn the subagent

Spawn `red-team` via the `Agent` tool with `{ scope, depth }` in the prompt.

- **One target** (`quick`/`standard`, or a single path) → **one** subagent.
- **Wide `deep`** (`scope: repo`) → **fan out**: spawn one subagent per top-level `apps/*`
  and per security-relevant `packages/*` (auth, core, pages, sales, bookings, and any with a
  `server/api`), each with `{ scope: "<that path>", depth: "deep" }`. Launch them in parallel
  (multiple `Agent` calls in one message). Fanning out keeps each agent's context focused and
  lets dynamic confirmation run per-app. The agents are **synchronous** — you hold their
  results when they return; never report "running in the background".

Each subagent writes its own `writeups/reports/red-team-<scope-slug>-YYYYMMDD.md` and returns
a structured findings list.

## 3. Collate

- If you fanned out, **merge** the per-agent reports into a single top-level
  `writeups/reports/red-team-repo-YYYYMMDD.md` (summary table = sum of all; link or inline the
  per-scope sections). A single-target run already wrote its one report — just confirm it
  exists and matches `red-team-TEMPLATE.md`.
- De-dupe findings that the same flaw produced across agents (shared package code).

## 4. File issues for confirmed high/critical findings

> **⚠️ Public-repo disclosure.** This repo is **public** — a `security`/`sec:*` issue is a
> *public* disclosure of an unfixed flaw. Only file public issues when the human driving you
> has OK'd it (or the finding is a fail-closed correctness bug, not an exploitable vuln). When
> in doubt, deliver findings **privately** (hand the report back, or email it) and ask before
> filing. The **daily automation never posts publicly** — it emails the report
> (`red-team-daily.yml`). Treat that as the default posture; the steps below apply once a
> private channel or human OK is in place.

For **every finding with `severity ∈ {high, critical}` AND `confidence == confirmed`**:

1. **Dedupe first** — `mcp__github__search_issues` for an open issue with the `security`
   label matching this finding (same route/file + title). If one exists, skip (note it in the
   report's "Filed" line instead).
2. **Open the issue** with `mcp__github__issue_write` (`method: create`):
   - **Labels:** `security` + `sec:<severity>` + the owning `pkg:<name>`/`app:<name>` label
     (where the vulnerable code lives — mirror the commit-scope convention).
   - **Title:** plain-English, names the impact (e.g. "Cross-team order read on
     `/api/teams/[id]/orders/[orderId]`"). No jargon in the title.
   - **Body:** `github-tasks` style — a 👤 plain-language "what an attacker can do & why it
     matters", a 🤖 block with `location`, `category`, `repro`, and `suggested fix`, and a
     `## 🧪 How to test` with the exact reproducing request. Reference the report file.
   - If this run is under an epic/the daily sweep, link it.
   > Labels must already exist on GitHub. The `security`/`sec:*` labels are added in
   > `.github/labels.yml` and only become applyable **after that merges to `main`** and the
   > labels workflow syncs them — until then, list the findings in the report and say issues
   > will be filed once the labels land, rather than erroring on an unknown label.
3. **Medium/low stay in the report only** — don't file them (noise). The report is their home.

## 5. Report back to the caller

Print a tight summary: counts by severity (confirmed vs suspected), the report path, and
clickable links to any issues filed. Example:

```
🔴 Red-team (deep · repo) — 1 critical, 2 high, 4 medium (3 confirmed)
Report: writeups/reports/red-team-repo-20260621.md
Filed:  #551 (sec:critical), #552 (sec:high)
Suspected (not filed, see report): 1 high, 4 medium
```

End with the offer: *"Want me to open issues for the suspected high/criticals too, or fix any
of these now?"* — fixing is a separate, explicit step (this skill finds; it doesn't patch).

## Relationship to the other entry points

- **CI** (`.github/workflows/red-team.yml`) runs the *subagent* directly at `depth=quick` on a
  PR diff and **fails the check on a high/critical** finding — it doesn't go through this skill.
- **Daily** (`.github/workflows/red-team-daily.yml`) runs `depth=deep` whole-repo, posts the
  report to a standing issue, and files issues exactly as step 4 above.
- Both workflows MUST follow the **Claude-action workflow standard** in
  `.claude/agents/CLAUDE.md` — notably the tool-permission grant (per-PR: `--allowedTools …`;
  daily sweep: `--permission-mode bypassPermissions`), without which the gate fails open
  (#834/#1036).
- **This skill** is the **on-demand** brain and the human entry point — and the reference for
  what the workflows automate.
- It complements, not replaces, the built-in `security-review` skill (which passively reviews a
  diff) and `/review` (general code review). Reach for `/red-team` when you want something that
  *actively hunts* for exploits at a chosen depth.
