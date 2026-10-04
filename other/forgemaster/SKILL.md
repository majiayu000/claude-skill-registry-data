---
name: forgemaster
description: Route a task by complexity and run the gated Forge pipeline (research → plan → implement → ship). Use when the user runs /forgemaster or wants the full guided feature pipeline.
---

# /forgemaster — Route by complexity, then run the Forge pipeline gated phase by phase

Judge the complexity of the request, **route** to the right-sized Forge path, then run it gated —
pausing at each boundary for your approval. Medium-or-higher work runs the full four-phase pipeline
(**research → plan → implement → ship**); low-complexity work is handed to the trimmed
`forge-mini` path to save turns and cost. You stay in control at every step.

See `.claude/workflows/forge.md` (full) and `.claude/workflows/forge-mini.md` (mini) for details.

## Usage

Accepts a **JIRA ticket**, a **Beads issue id**, or a **free-text description** — or nothing, to
resume the active run.

```
/forgemaster <description>             # free text → judge complexity, route, run
/forgemaster <BEADS-ID>                # e.g. agent-forge-harness-f25 → load that issue as the work
/forgemaster <JIRA-KEY>                # e.g. PROJ-1234 → mirror into Beads, then run
/forgemaster                           # resume the run in flight (see: bun run forge:runs)
/forgemaster --full <input>            # force the full pipeline (skip the complexity check)
/forgemaster --mini <input>            # force the mini path (skip the complexity check)
```

---

## Step 0 — Preflight (mandatory)

Beads is required for this pipeline. Confirm it is reachable before anything else:

```bash
bd ready >/dev/null    # if this errors, the Dolt server is down
```

If `bd` errors: run `bd dolt start`, then retry. **Do not proceed without Beads.** (The SessionStart
hook normally starts the server automatically; this is the manual recovery.)

### Resolve the input → a Beads-tracked work item + `<slug>`

Detect what was passed and normalize it to one Beads issue plus a kebab-case `<slug>`. Check in this
order (the first match wins):

1. **Strip flags** (`--full` / `--mini`) and trim whitespace.
2. **Empty** → **resume**: run `bun run forge:runs --active`. With exactly one run in flight, resume
   it at its first incomplete phase (always a full run; skip the triage in Step 0.5, go to Step 1).
   With several, ask which one — runs are concurrent, so "the active run" is not a thing to guess.
3. **Existing Beads id** — `bd show <arg>` succeeds (e.g. `agent-forge-harness-f25`):
   use that issue as the work definition (title, description, AC). **Do not create a duplicate** —
   it is the tracking issue; the plan phase may add child tasks under it. Derive `<slug>` from its
   title. Claim it when implementation starts.
4. **JIRA key** — matches `^[A-Z][A-Z0-9]+-\d+$` (e.g. `PROJ-1234`) and is *not* an existing bead:
   - Fetch the ticket **if** a JIRA integration is available (a JIRA MCP server or a `jira` CLI on
     PATH). If none is configured, ask the user to paste the ticket **summary + description +
     acceptance criteria** — do not invent them.
   - **Mirror it into Beads** (Beads stays the source of truth), linking back to JIRA:
     ```bash
     bd create --repo <repo> --type <feature|bug|task> --title "<summary>" \
       --priority <p> --external-ref "jira-<KEY>" --acceptance "<AC>" --description "<body + JIRA link>"
     ```
     Priority via `.claude/skills/beads-priority-assignment/SKILL.md`. Derive `<slug>` from the
     summary (e.g. `proj-1234-<short-title>`).
5. **Free text** → derive a kebab-case `<slug>`; the Beads issue is created later (full: in the plan
   phase; mini: in the scope step).

Confirm the resolved `<slug>` and a one-line work summary with the user before continuing.

---

## Step 0.5 — Complexity triage & route

Pick the right-sized path **before** doing real work — running the full pipeline on a one-file
change wastes turns and money (cost is the whole point of this step).

- `--full` / `--mini` flag present → honor it, skip the judgment.
- Resuming an existing full run → stay full.
- Otherwise judge complexity from cheap signals (a quick look, not a research project): aligns with
  the tiers in `.claude/commands/go.md` and the model-tier rubric in
  `.claude/protocols/model-tier-policy.md`.

| Signal | → Mini | → Full |
|--------|--------|--------|
| Files touched | ≤ ~3 | > 3 |
| New architecture / component / system | no | yes |
| Genuine unknowns or design decisions | ≤ 1 | several |
| Scope clarity | clear from the ask + code | ambiguous, needs investigation |
| Cross-cutting / shared interfaces | no | yes |

**Default when uncertain: ask, don't assume.** Use `AskUserQuestion` to state your read and the
recommended route, letting the user confirm or override:

- **Mini** → follow `.claude/workflows/forge-mini.md` (scope → build → wrap). Do **not** use the
  `forge:phase-gate` / run state files or write `plans/`/`reports/` docs; track in Beads only.
  Then go straight to that workflow — the phase-walk below is for the full path.
- **Full** → continue to Step 1 with the `<slug>` resolved in Step 0.

If a mini run outgrows its size mid-flight, escalate to full (`/forge-research <slug>`) as described
in `forge-mini.md`.

---

## Step 1 — Walk the phases *(full path)*

For each phase in order — `research`, `plan`, `implement`, `ship` — do this loop:

1. **Gate entry.** Run `bun run forge:phase-gate <phase> --slug <slug>`. If it exits non-zero, the
   prerequisite artifact is missing — stop and tell the user which earlier phase to run.
2. **Announce.** Tell the user which phase is starting and where its output will land
   (see the table in `.claude/workflows/forge.md`).
3. **Run the phase** by following its skill end to end:
   - research → `.claude/skills/forge-research/SKILL.md`
   - plan → `.claude/skills/forge-plan/SKILL.md`
   - implement → `.claude/skills/forge-implement/SKILL.md`
   - ship → `.claude/skills/forge-ship/SKILL.md`
   The phase records its own completion (`forge:phase-gate <phase> --slug <slug> --write`).
4. **Show the exit artifact.** Surface what the phase produced (the research/plan/ship doc, the
   demoed checkpoints, the PR) so the user can inspect it.
5. **Gate the transition.** Use `AskUserQuestion` to ask whether to proceed to the next phase:
   - **Proceed** → continue to the next phase.
   - **Revise this phase** → re-run the current phase skill with the user's feedback.
   - **Stop here** → end the run; the state file preserves progress for later resumption.

   Never auto-advance across a phase boundary. The pause is the point.

---

## Step 2 — Finish

After the ship phase records complete:
- Confirm `reports/<slug>-ship.md` and the PR exist.
- The Stop exit hook goes quiet automatically once ship is complete.
- Summarize the whole run: the slug, the four artifacts, the Beads epic/feature closed, and the PR.

---

## Notes

- **Within a phase**, the implement phase still pauses at its own demo/test checkpoints — those are
  finer-grained stops than the phase boundaries this command gates.
- **Resuming**: `/forgemaster <slug>` (or bare `/forgemaster`, when exactly one run is in flight)
  picks up at the first incomplete phase recorded in `.tmp/work/forge-runs/<slug>.json`.
- **Concurrent runs**: each run owns its own state file, so several can be in flight at once.
  `bun run forge:runs` lists them. Give each code-touching run its own worktree
  (`bun run worktree create <branch>`, then `--checkout <path>` on the phase-gate write) so two
  runs do not build on top of each other.
- **Unattended**: `/forgemaster-auto` runs the same four phases with a subagent review at each
  boundary instead of asking you — see `.claude/workflows/forge-auto.md`.
- **Standalone phases**: you can always run a single phase directly (`/forge-plan <slug>`) instead of
  the full orchestration; the same gates apply.
