---
name: learn-lessons
description: "Process lessons/ entries as doctrine change-requests."
version: 1.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# learn-lessons — Lesson Processing and Queue Activation

`learn-lessons` runs the `lessons` family of queue-grind profiles over `state/lessons/*.yaml` (and
`state/lessons-outbox/` in central mode) as change-requests against doctrine, agent prompts, hooks,
scripts, wiki guides, and improvement queues — one destination + change-kind per lesson. Success
metric: did doctrine and queues evolve, not did the file shrink. **Supersedes
`coordinator:lesson-triage`.** Taxonomy, change-kind apply dispatch, promotion-sprint procedure and
phase mechanics: wiki.

**Every coordinator CLI named on this page is engine-homed and has a settings-home launcher** —
resolve each by absolute path per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape W on a PowerShell
host, Shape A/B on POSIX). Never a bareword, and never `coordinator/bin/<cli>.py` cwd-relative:
this skill runs with cwd set to the consuming repo, where that path does not exist.

**Announce:** "I'm using the coordinator:learn-lessons skill in `<mode>` mode." Mode default: cwd
`~/.claude` central → `central`; else `local`; PM can override.

## Hard Rules (not engine-enforced)

- **Actor split.** The run's committer stage commits the run's fixes and closes. The EM commits
  everything outside a run: post-run promotes and `promoted_to` stamps, baton minting, PM-ruling
  writes, and the run stamp. A dispatched lead still never commits.
- **No-defer.** A `wiki-append`/`wiki-new` record with a named destination applies THIS run —
  never "the next pass." Legitimate deferrals: a structurally-required cross-mode block (e.g.
  `strip-local` before its central commit SHA lands), or a record needing PM authorization.
- **Wikis are the default destination.** `doctrine-edit`/`memory-pointer` are doctrine-plane-only
  — a worker NEVER emits either; downgrade to `wiki-*` + `doe_escalation: true` before the record
  reaches the PM gate.
- **Extraction never runs through an LLM** (`extract-lessons` — a parse). Routing judgment can,
  behind the verify gate.
- **Mechanical-contract lessons need an executable witness** (a passing test, live tool behavior,
  official docs) — discard if none can be found or one contradicts the claim.
- **Domain-looking universals default to `retag-local`**, never a blind `[universal]` string replace.
- **A `wiki-append`/`wiki-new` target must be reachable** from a real traversal surface (index,
  skill step, dispatch preamble) — not merely exist.
- **Local mode auto-applies** `discard`/`wiki-append`/`retag-local`/dedupe/age-sweep, plus a
  tradeoff-free `agent-prompt-edit`, `hook-edit`, `script-edit`, `snippet-sync-update` or
  `project-structural` row below plan weight. The PM-surface list keeps only direction and taste
  calls: `doctrine-edit`, `memory-pointer`, `doe_escalation`, and product or taste choices.
- **Central mode needs a PM decision per record** (apply / defer / reject, batching OK, per-cluster
  allowed) — never auto-applied; the `lessons-central-route` `pm-decision` hand-back is the mechanism.
- **A strip run follows the apply run it cites** — no row strips before its central commit exists.
- **Fail-close:** a strip-list id with no routed sibling record blocks the run's `COMPLETE`
  sentinel — surface to the PM, don't push through.
- **Universals-pending is a post-run count, not a pre-run stop.** A local run hands back
  `route-to-central`; surface ≥ 20 in the Phase 8 report with a central-run recommendation.
- **Never fabricate a routing `id`** — every cited id must exist in its extraction. Never
  hand-correct a router's fabricated output; re-dispatch it instead.
- **An emit refusal is reported, not routed around.**

## Phase Flow (invocation pointers — mechanics: wiki)

`coordinator_core.learn_lessons_pipeline`'s `brief`/`apply` entrypoints emit the Phase 4.5 cutoff
derivation and the Phase 8 `COMPLETE` stamp as engine directives — read them from the fired decision
object, never derive them by hand.

Discovery roots: `learn-lessons-roots` (machine-registry-derived, never a
committed list). Baton lift source: batons joined to the plan under distillation by
`deliverable_id`, each `## What I Learned` bullet a candidate lesson, never an auto-promote.

One flow per run kind, each `pre-run directives → emit → fire → consume hand-back → post-run
directive`:

- **local:** the `learn_lessons_pipeline` brief's age-sweep directive as the only pre-run step —
  never write routing records under `state/lessons/`; the grind writes them under
  `<run_dir>/records/`. Emit with `emit-dispatch-workflow --queue state/lessons --profile
  lessons --appetite <a> --out <scratch>`, fire with the `Workflow({scriptPath, args})` call it prints, never `--fire`.
- **central route:** drain the outbox, then assert cross-plane emptiness first (a FAIL stops the
  run and goes to the PM). Emit `--queue state/lessons-outbox --profile lessons-central-route`,
  fire, then present the `pm_decision` hand-back to the PM; the EM writes each ruling as
  `pm_decision` and commits. `defer` rows go to `coordinator-queue-append --schema
  improvement-queue` with `queue_scope: central`; `reject` rows close as `discarded` through
  `backlog-grind-assemble grind-row close`. Cluster rulings: wiki § Phase flow detail.
- **central apply:** emit `--profile lessons-central-apply`, fire, then write the run stamp once
  every apply commit has landed and the fail-close holds.
- **strip:** emit `--profile lessons-strip` per repository after the apply run, with `--where
  promoted_to in [...]` copied from the apply run's settled list. A sibling launch needs the PM's
  cross-repo assent, asked once per strip session as one bundled ask; without it the strip waits.

**Actor per flow.** Whichever actor executes this skill (EM, or a dispatched lead) runs each flow's
pre-run directive, emits, fires, and consumes the hand-back. Commit authority stays EM-only.

**Post-run consumption, all runs.** `baton` → cluster and mint batons carrying triage's sizing
evidence, with no second gate (the fire authorized them); `needs-judgment`, `doe-escalation` and
`direction-call` → the PM; `route-to-central` → `coordinator-lesson-promote` per row with
`--title-file`/`--body-file`, then write `promoted_to` on the row and commit; engine-originated
types → counted in Phase 8, rows left open.

**Cross-repo write-without-commit channel (local mode, run in a sibling).** The sibling EM commits
only its own row's `promoted_to` stamp; the central-mode EM commits the outbox file(s) before the
central route run reads them. **No dry-run mode;** the Phase 8 report cites the run-cost record
`state/queue-grind/<profile>/runs/<run-id>.json`.

Emit the Phase 8 end-of-run report (exempt from the ≤200-word budget — the run's only audit trail),
built from the engine's receipt and hand-back document, as that same actor's own run output, before
writing the `COMPLETE` sentinel. `COMPLETE` is blocked while a route-run row carries no `pm_decision`, or the apply run
handed back an engine-originated type — surface those to the PM before writing the sentinel. The
top-level EM writes the sentinel last, after every apply/commit lands, never a dispatched lead,
which cannot commit and so cannot know the applies landed.

Wrap the emitted report in the marker pair, which is how the exemption is declared to the comms
hook (`em-pm-comms-instrumentation.md` § The ceremony-mandated marker):

```
<!-- ceremony-mandated:start -->
...the Phase 8 report...
<!-- ceremony-mandated:end -->
```

## Anti-Patterns

Auto-applying central promotions without the PM gate. `git add -A` for strips. True-deleting a
discard instead of archiving first. Default-routing to CLAUDE.md instead of a wiki. Defer-chaining
wiki promotions — every record is (a) applied, (b) PM-surfaced, or (c) mode-escalated. A hand-rolled
fallback when the emitter is unavailable — none exists. Full list: wiki.

## Related

wiki (full reference) · `${CLAUDE_PLUGIN_ROOT}/queue-profiles/lessons.yaml`,
`lessons-central-route.yaml`, `lessons-central-apply.yaml`, `lessons-strip.yaml` ·
`${CLAUDE_PLUGIN_ROOT}/snippets/em-operating-doctrine.md § How to Plan and Hand
Off, "Improvement Queue"`
