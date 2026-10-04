---
name: pm-assess
description: Produce a structured project-state assessment — what's built and working, what's in-flight, what's blocked + why, what's at risk, and a prioritized next-actions list. For AICP this means reading `.aicp/state.yaml` + active task in `wiki/backlog/tasks/` + recent git log + open epics in `wiki/backlog/epics/` + brain compliance tier (`python3 -m tools.gateway compliance`) and synthesizing into a single readable assessment. Distinct from `pm-status-report` (cadence-driven outward report), `pm-plan` (forward planning), `pm-retrospective` (look-back analysis). Loads when the operator says "assess", "where do we stand", "project state", "what's the situation", "give me an assessment", "where are we".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# pm-assess

The project-state synthesis skill. Reads multiple authoritative sources (state file, active task, git log, epics, brain compliance) and produces a single structured assessment with five sections: Accomplished / In-flight / Blocked / Risks / Next actions. Distinct from `pm-status-report` (cadence-driven outward communication, often weekly), `pm-plan` (forward-looking with milestones), `pm-retrospective` (look-back analysis on a finished slice).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "assess", "where do we stand", "where are we", "project state", "what's the situation", "give me an assessment", "snapshot".
- **Session-orientation**: a fresh session opens and the operator wants a grounding read before deciding what to work on next.
- **Pre-decision**: operator about to make a roadmap choice (drop a feature, pivot, schedule sprint) and wants ground truth first.
- **Context for a non-AICP audience**: operator needs to explain project state to a stakeholder who hasn't been in the loop.

Do NOT load when:

- Outward-facing weekly/sprint report is the request — load `pm-status-report` (it has a defined report cadence + format).
- Forward planning with milestones is the request — load `pm-plan`.
- Look-back analysis on a completed slice — load `pm-retrospective`.
- Just "what task am I on" — load `aicp-ops-tasks` for the surgical answer.
- Just "is the system healthy" — load `aicp-ops-runtime` or `openclaw-health`.

## Operations

This skill has 3 named operations. Execute strictly in order — synthesis comes after gathering, never before.

### Operation 1: Gather signals from authoritative sources

**Trigger**: skill loaded.

**Process**:

1. Project identity + posture:
   ```bash
   head -40 CLAUDE.md   # identity profile + mission
   head -20 AGENTS.md   # universal context
   ```
   Capture: project type, domain, scale, current phase, mission line.
2. Current task + recent runtime activity:
   ```bash
   cat .aicp/state.yaml 2>/dev/null
   .venv/bin/aicp --task-cmd show 2>&1 | tail -10
   ls -t wiki/backlog/tasks/T*.md 2>/dev/null | head -3   # newest active task files
   ```
3. Git activity over recent windows:
   ```bash
   git log --since="2 weeks ago" --oneline | head -40
   git log --since="2 weeks ago" --shortstat --no-merges | tail -2   # volume signal
   git log --since="2 weeks ago" --pretty="%s" | head -40   # subject lines for theme detection
   ```
4. Backlog state:
   ```bash
   ls wiki/backlog/epics/*.md 2>/dev/null | wc -l   # epic count
   grep -l "status: open\|status: in-progress" wiki/backlog/epics/*.md 2>/dev/null
   grep -l "status: open" wiki/backlog/tasks/*.md 2>/dev/null | wc -l   # open task count
   ```
5. Brain compliance tier (AICP-specific signal — adoption health):
   ```bash
   python3 -m tools.gateway compliance 2>&1 | tail -10
   ```
   Capture: tier reached + any gaps.
6. Recent operator activity signals — handoffs, post-mortems, incident logs:
   ```bash
   ls docs/HANDOFF-*.md docs/incidents/*.md docs/POSTMORTEM-*.md 2>/dev/null | head -5
   ```
7. System health (one-liner; not a full audit — that's `openclaw-health`):
   ```bash
   .venv/bin/aicp --check 2>&1 | tail -5
   ```

**Quality bar (Operation 1 done when)**:

- [ ] All 7 signal sources queried (or explicitly noted as N/A: "no state.yaml — fresh project").
- [ ] Current active task captured (file path + name + status), OR "no active task".
- [ ] Recent git activity summarized (commit count + theme detection).
- [ ] Brain compliance tier captured (or "brain not connected").
- [ ] Recent handoffs/incidents/post-mortems noted (or "none in last 30 days").
- [ ] System health one-liner captured.

### Operation 2: Synthesize assessment with evidence

**Trigger**: Operation 1 signals gathered.

**Process**:

1. Build the assessment in this 5-section structure. Each entry must point to evidence (commit SHA, file path, log line) — never claim without evidence:

   ```
   PROJECT ASSESSMENT — <project>, <date>

   ## Accomplished (recent — past 2 weeks)
   - <topic>: <one-line outcome>. Evidence: <commit SHA / file path>.
   - ...

   ## In-flight
   - Active task: <task ID + title> (status=<X>). Started <date>. Path: wiki/backlog/tasks/T<NNN>.md.
   - Open epics: <count>. Notable: <epic name> (<status>).
   - Uncommitted work: <yes / no, with summary>.

   ## Blocked
   - <blocker>: <description>. Why: <reason>. Owner: <who can unblock>.
   - (none) if nothing is blocked.

   ## Risks
   - <risk>: <description>. Likelihood: <low/med/high>. Impact: <what would break>. Mitigation: <plan or "none yet">.
   - ...

   ## Next actions (prioritized)
   1. <highest-leverage next step>. Skill: <which skill to load>. Effort: <S/M/L>.
   2. ...
   3. ...

   ## Posture
   <one paragraph: overall posture — On track / Recovering / Pivoting / Stuck. State the dominant signal supporting the posture.>
   ```
2. Calibrate Accomplished against the recent window only — don't list everything ever done. The audience is "what changed since last assessment", not "the project's lifetime résumé".
3. Calibrate Risks honestly:
   - "Brain compliance dropping from Tier 4" is a risk; "brain might one day be unavailable" is hand-wringing.
   - Risks must have specific likelihood + impact + mitigation. Vague risks get cut.
4. Next-actions must be SPECIFIC + ACTIONABLE — name the skill or command:
   - ✅ "Rewrite remaining 8 fleet skills via gold-standard pattern. Skill: continue Phase 2 work per docs/HANDOFF-SKILLS-PHASE-2-*.md."
   - ❌ "Continue improving skills."
5. Posture is one of: **On track** (work proceeding, no blockers), **Recovering** (post-incident, working back to steady state), **Pivoting** (mission shift in progress), **Stuck** (blocker not yet identified or unblocked). Pick one — don't hedge across two.

**Quality bar (Operation 2 done when)**:

- [ ] All 5 sections + Posture filled.
- [ ] Every Accomplished entry has evidence (SHA / path).
- [ ] Every Risk entry has likelihood + impact + mitigation.
- [ ] Every Next action names a specific skill or command.
- [ ] Posture is one of the 4 named values, not a hedge.
- [ ] Total length 30-60 lines for a single-project AICP assessment (longer for multi-project sweeps is fine).

### Operation 3: Persist + hand off

**Trigger**: Operation 2 assessment authored.

**Process**:

1. Update `.aicp/state.yaml` with the assessment summary if appropriate:
   - The state.yaml is the cross-session memory — record posture + active task + last assessment date.
   - Don't dump the full assessment into state.yaml; that file should stay small. Reference the assessment file instead.
2. If the assessment surfaces new tasks/issues, file them:
   - New tasks: `python3 -m tools.gateway task new --title "..."` (or operator's preferred path).
   - New risks worth tracking: ensure each has an owner + check-back date.
3. Decide whether the assessment is ephemeral (conversation-only) or persistent:
   - Conversation-only: just present to operator. Most assessments are this.
   - Persistent: write to `docs/assessments/ASSESSMENT-<YYYY-MM-DD>.md` if the operator wants a record OR if the assessment will inform `pm-status-report` cadence.
4. Hand off the next action:
   - If operator already knows what to do → don't editorialize.
   - If next action is non-obvious → suggest the specific skill explicitly.
   - If posture is "Stuck" → escalate: name what additional information would unblock decision-making.

**Quality bar (Operation 3 done when)**:

- [ ] state.yaml posture line updated (or explicitly skipped: "no state.yaml in this project").
- [ ] New tasks/risks filed if surfaced (or "no new items surfaced").
- [ ] Persistence decision made (ephemeral vs file-written).
- [ ] Operator told the specific next-skill OR confirmed they already know.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Lifetime résumé instead of recent window

Skill produces an Accomplished section listing every milestone since project inception. Operator scans 80 lines, gets nothing actionable from it, and the assessment fails its purpose (orient on RECENT state). The lifetime narrative belongs in CLAUDE.md or README, not a recurring assessment.

**The rule**: Operation 2 step 2 fixes the window — Accomplished is "past 2 weeks" by default. If the project just hit a major milestone (like Post-Anthropic 2026-04-25), call it out explicitly as a milestone-window assessment with a longer scope. Default to recent; expand only on operator request.

### Gotcha 2: Vague risks that aren't risks

"Risk: model could underperform." That's a fact pattern, not a risk. A risk has a probability, an impact magnitude, and an avoidance/mitigation plan. Without all three, it's hand-wringing dressed up.

**The rule**: Operation 2 step 3 demands likelihood + impact + mitigation per risk. If you can't fill all three, the entry isn't a risk yet — either fill it in (with evidence) or omit it. Vague risks pollute the signal-to-noise ratio of the assessment.

### Gotcha 3: Next-actions that aren't actionable

"Next: continue improving the system." That's the project's existence, not a next action. Operator needs ONE concrete thing to do; if you can't name it, the assessment is incomplete.

**The rule**: Operation 2 step 4 requires every next-action to name a specific skill or command. If you can't, surface that as a Risk ("no clear next action — strategy decision pending") rather than fabricating action language.

### Gotcha 4: Inventing posture (hedging)

Posture says "Mostly on track but with some recovery elements and possibly pivoting on the post-Anthropic angle." Four words none of which commit to anything. Operator gets no signal.

**The rule**: Operation 2 step 5 picks ONE of the four named postures. If two compete, name the dominant one and address the secondary as a Risk. The whole point of posture is to commit a single signal — hedging defeats it.

### Gotcha 5: Stale state.yaml posture left from a prior assessment

Operator runs assess, posture is "On track". A week later, an incident degrades the system. Operator runs assess again, but Operation 3 updates posture from "On track" → "On track" without checking — the prior data was outdated and the new check should have surfaced the issue.

**The rule**: Operation 1 step 7 captures live system health. If `aicp --check` is FAIL or there's a fresh incident in `docs/incidents/` (within 7 days), that information must propagate into Risks/Posture in Operation 2. Don't carry forward an old "On track" if current evidence contradicts it.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP-specific assessment surfaces: `.aicp/state.yaml` is the active-task pointer, `wiki/backlog/tasks/T*.md` is the per-task state, `wiki/backlog/epics/*.md` is the epic-level state, `python3 -m tools.gateway compliance` reports brain adoption tier (currently 4/4 STRUCTURAL), `docs/incidents/` records past failures, `docs/HANDOFF-*.md` records cross-session continuity. Sister fleet projects (openfleet, dspd, nnrt) have their own state files (Mission Control, Plane) — when assessing those, swap the AICP-specific commands for project-specific equivalents.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| pm-status-report | Cadence-driven outward report (weekly, monthly) | This skill is internal orientation; status-report is outward communication |
| pm-plan | Forward planning with milestones | Forward; this skill is now-state |
| pm-retrospective | Look-back analysis on a completed slice | Backward analysis; this skill is current-state |
| pm-handoff | Cross-session context preservation | Continuity; this skill is point-in-time |
| pm-changelog | Tag/commit log to user-facing notes | User-facing; this skill is internal |
| aicp-ops-tasks | Just "what task am I on" | Surgical task lookup; this skill is broader synthesis |
| openclaw-health | System audit (is the stack OK) | Stack-level; this skill is project-level |
| aicp-ops-runtime | `aicp --check` and friends | Runtime health; this skill includes it as one signal |
