---
name: pm-status-report
description: Generate a cadence-driven outward status report (weekly / monthly / per-sprint) — progress since last report, what's next, blockers, metrics, decisions awaited. For AICP this means git activity over the cadence window + task closures + cost/token metrics from `aicp --metrics-history` + brain compliance tier + open epics. Lands at `docs/status/STATUS-<YYYY-MM-DD>.md`. Distinct from `pm-assess` (now-state synthesis, internal use), `pm-retrospective` (reflective lessons, slice-level), `pm-handoff` (cross-session continuity). Loads when the operator says "status report", "weekly update", "send the status", "monthly summary", "stakeholder update", "what should I tell X".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# pm-status-report

The cadence-driven outward report skill. Produces a regularly-scheduled report (weekly / sprint / monthly) for stakeholders — concrete progress, upcoming work, blockers, measurable metrics, decisions awaited. Distinct from `pm-assess` (internal now-state, no cadence), `pm-retrospective` (reflective lessons), `pm-handoff` (cross-session continuity for the operator/next-self).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "status report", "weekly update", "monthly summary", "send the status", "draft the stakeholder update", "what should I tell X about progress".
- **Cadence trigger**: it's the operator's regular reporting day (Monday weekly / first-of-month monthly / end-of-sprint).
- **Stakeholder ask**: a sister-project lead, sponsor, or external party requested a written progress update.
- **Pre-sync prep**: an upcoming sync needs concrete write-up beforehand to make the live conversation efficient.

Do NOT load when:

- Operator wants internal orientation snapshot (no audience) — load `pm-assess`.
- Operator wants reflective lessons from a finished slice — load `pm-retrospective`.
- Operator wants cross-session continuity context — load `pm-handoff`.
- Operator wants release notes (user-facing) — load `pm-changelog`.
- Operator wants a deep diagnostic — load `aicp-ops-runtime` or `openclaw-health`.

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Define the cadence window + gather metrics

**Trigger**: skill loaded; cadence + audience identified.

**Process**:

1. Identify cadence + audience explicitly:
   - Cadence: weekly / sprint (1-2 weeks) / monthly / ad-hoc.
   - Window: prior report's end (or `last-tag-or-status-file-date`) → today.
   - Audience: who reads this (stakeholder name / role) — affects depth/jargon level.
2. Pull progress signals over the window:
   ```bash
   git log --since="<window-start>" --no-merges --oneline | head -40
   git log --since="<window-start>" --shortstat --no-merges | tail -2
   ls wiki/backlog/tasks/T*.md 2>/dev/null   # tasks closed in window
   ls docs/incidents/INC-*.md 2>/dev/null    # incidents in window
   ls docs/HANDOFF-*.md 2>/dev/null          # cross-session bridges
   ```
3. Pull METRICS — concrete numbers, not feelings:
   - **Test count + status**:
     ```bash
     grep -E "^[0-9]+ passed" tests/.last-run 2>/dev/null
     # or live: .venv/bin/pytest --collect-only -q | tail -1
     ```
   - **Cost / token usage** (over the window):
     ```bash
     .venv/bin/aicp --metrics-history --since "<window-start>" 2>&1 | tail -10
     ```
   - **Test coverage** (if tracked):
     ```bash
     .venv/bin/coverage report 2>/dev/null | tail -3
     ```
   - **Compliance tier**: `python3 -m tools.gateway compliance | tail -3`.
   - **Lint debt**: `make lint-count 2>/dev/null` (or operator's tracking).
4. Pull blocker + decisions-awaited signals:
   - Open tasks blocked >7 days (status flagged or comment indicating blocker).
   - Open epics with no recent activity (last commit on epic >14 days).
   - Operator's recorded "needs decision from X" notes.
5. Pull UPCOMING — what's planned for the next window (from `.aicp/state.yaml` plan or active epics).

**Quality bar (Operation 1 done when)**:

- [ ] Cadence + window + audience explicit.
- [ ] Git activity quantified (commits, files-changed, themes).
- [ ] Metrics pulled with NUMBERS (not "many tests pass" — actual count).
- [ ] Blockers enumerated with age.
- [ ] Upcoming work identified from plan.

### Operation 2: Author the report

**Trigger**: Operation 1 evidence + metrics gathered.

**Process**:

1. Author at `docs/status/STATUS-<YYYY-MM-DD>.md` using this structure (audience-tuned):
   ```markdown
   # Status — <project>, <cadence> (<window-start> .. <window-end>)

   **Audience**: <who this is written for>
   **Period**: <window>

   ## Headline
   <one sentence: the most important fact about this window. Pick ONE.>

   ## Progress (since <prior-report-date>)
   - <fact>: <one-line outcome>. Evidence: <commit / link>.
   - ...

   ## Upcoming (<next-cadence>)
   - <planned item>: <one-line>. Skill: <which to load>. Effort: <S/M/L>.
   - ...

   ## Blockers
   - <blocker>: <description>. Age: <N days>. Owner: <who can unblock>.
   - (none) if nothing blocked.

   ## Metrics
   | Metric | Now | Δ since prior |
   |--------|-----|---------------|
   | Tests passing | <N> | <±N> |
   | Coverage % | <N>% | <±N pp> |
   | Lint debt | <N> items | <±N> |
   | Cost (cloud, $CAD/period) | $<N> | <±$N> |
   | Brain compliance | Tier <N>/4 <name> | <change> |

   ## Decisions awaited (from <audience>)
   - <decision>: <what's blocked behind it>. Required by: <date>.
   - (none) if nothing pending.

   ## One-line summary
   <40-60 words, suitable for paste into Slack/email/standup>
   ```
2. Write for the audience — strip AICP-internal jargon if the stakeholder isn't AICP-native:
   - ✅ "LocalAI inference is now self-hosted and routes 65% of agent calls."
   - ❌ "Tier_map band 2 now resolves to k2_6_openrouter pinned-provider."
   Translate, don't dilute. The stakeholder needs accurate signal in their vocabulary.
3. **Headline** is ONE sentence. Pick the most important fact. If you can't pick one, the report has no signal.
4. **Metrics table** uses CONCRETE NUMBERS. The Δ column is critical — it tells the stakeholder whether the number is moving the right direction. No Δ = the metric was just collected this period; flag that.
5. **Decisions awaited** is the most-actionable section for the stakeholder — make it specific and time-boxed.

**Quality bar (Operation 2 done when)**:

- [ ] Headline is ONE sentence (not a paragraph, not a bullet list).
- [ ] Progress section has evidence per entry.
- [ ] Metrics table has 4-6 metrics, each with Now + Δ.
- [ ] Blockers enumerated with age + owner (or "(none)").
- [ ] Decisions-awaited section explicit.
- [ ] One-line summary fits Slack/email paste (40-60 words).
- [ ] Audience-tuned: jargon stripped or translated where needed.

### Operation 3: Persist + deliver

**Trigger**: Operation 2 report authored.

**Process**:

1. Persist to `docs/status/STATUS-<YYYY-MM-DD>.md`:
   - Filename includes ISO date so future-grep finds them.
   - Cross-link from `.aicp/state.yaml` (if a `recent_status:` field exists) or from sister project board (Plane / Mission Control).
2. Deliver:
   - If audience is internal-self: just present in conversation. Operator decides where it goes.
   - If audience is stakeholder: prepare the delivery vehicle (Slack message, email body, ticket comment) with the one-line summary up top + link to full report.
   - If audience is fleet (cross-project): post to standing-orders.yaml or Mission Control board update.
3. Commit the status file separately:
   ```
   git add docs/status/STATUS-<YYYY-MM-DD>.md
   git commit -m "status(<cadence>): <window>"
   ```
4. Schedule next cadence (if the operator wants automation) — offer `/schedule` for next reporting date.

**Quality bar (Operation 3 done when)**:

- [ ] Report persisted with date-stamped filename.
- [ ] Delivery vehicle prepared (Slack/email/comment) for external audience (or "internal-self" noted).
- [ ] Commit made.
- [ ] Next-cadence reminder offered (or noted "operator runs manually each Monday").

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Status report that's just a git log dump

Skill pastes 40 commit subjects under "Progress". Stakeholder reads "fix: F841 in stream_batch_sampling" and has no idea what that means or whether it matters. Report is technically populated but functionally noise.

**The rule**: Operation 2 step 2 — translate every commit/event into a stakeholder-comprehensible outcome. The stakeholder cares about WHAT CHANGED FOR THEM, not internal naming. If a commit doesn't affect the stakeholder, it doesn't go in the Progress section. Compress 40 commits into 5-8 outcome-level entries.

### Gotcha 2: Metrics without deltas

Metrics table says "Tests: 1840". No baseline, no change, no signal. Stakeholder doesn't know if 1840 is good, growing, shrinking, or stagnating. The number is decorative.

**The rule**: Operation 2 step 4 — every metric has a Δ column. If this is the first report and there's no prior baseline, mark Δ as "baseline" explicitly. The Δ is what carries the signal; without it, the number is a coin sitting on a desk.

### Gotcha 3: "No blockers" while real blockers are ignored

Skill writes "Blockers: (none)". But there IS a blocker — operator has been waiting on stakeholder X's decision for 3 weeks; the team is working around it. Reporting "(none)" buries the very thing the report should surface.

**The rule**: Operation 1 step 4 + Operation 2 step 4 — actively pull blockers from BOTH internal flags AND operator-known external waits. A "decision awaited from stakeholder X" IS a blocker; surface it explicitly with age. The job of a status report is to make blockers visible, not invisible.

### Gotcha 4: Audience-misaligned jargon

Stakeholder is a non-technical sponsor. Report says "Stage 4 reliability components include per-backend circuit breakers with retry budget and DLQ failover chain." Stakeholder reads gibberish, can't tell if the project is healthy.

**The rule**: Operation 2 step 2 — translate to audience vocabulary. For non-technical: "the system can now recover from transient cloud failures without operator intervention". Same fact, different vocabulary. Pick the audience's vocabulary BEFORE writing — re-translating after the fact is harder and produces awkward hybrids.

### Gotcha 5: No one-line summary

Report is 80 lines of well-written content. Stakeholder asked "give me the gist" — operator has to read all 80 lines, manually compress. The report didn't do its compression job.

**The rule**: Operation 2 step 5 — every status report ends with a 40-60 word ONE-LINE SUMMARY suitable for Slack/email paste. This is the report's atomic unit. If a stakeholder reads only this one paragraph, they get the period's signal. Everything else is supporting evidence.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP's status surfaces are the operator (most reports are operator-self), occasional sister-project reports (when AICP capacity affects fleet planning), and brain log entries (for cross-project visibility). Cost/token metrics come from `aicp --metrics-history`; brain compliance tier from `python3 -m tools.gateway compliance`; test count from pytest. The project uses Conventional Commits, so theme distribution from `git log` is a free signal. Sister projects (openfleet, dspd, nnrt) have their own status conventions — this skill adapts to those (DSPD uses Plane status; openfleet uses standing-orders.yaml).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| pm-assess | Internal now-state synthesis | Internal; this skill is outward |
| pm-retrospective | Reflective lessons on a finished slice | Reflective; this skill is forward-looking |
| pm-handoff | Cross-session continuity | Continuity; this skill is cadence outward |
| pm-changelog | User-facing release notes | User audience; this skill is stakeholder audience |
| pm-plan | Forward planning with milestones | Plans the future; this skill reports against the plan |
| aicp-ops-metrics | Live metrics inspection | Snapshot of live state; this skill aggregates over a window |
