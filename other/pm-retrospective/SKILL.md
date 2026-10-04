---
name: pm-retrospective
description: Run a retrospective on a completed slice (milestone, sprint, epic, mission) — examine what worked, what didn't, what was surprising, what to keep / stop / start; produce specific action items with owners and dates; contribute generalizable lessons to the brain via `python3 -m tools.gateway contribute --type lesson`. For AICP this means looking at git log + task closures + incidents + handoff docs over the slice's window. Distinct from `pm-assess` (now-state, no reflection), `pm-status-report` (cadence outward, not reflective), `ops-incident` (single-incident response). Loads when the operator says "retro", "retrospective", "what did we learn", "post-mortem the milestone", "lessons from X".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# pm-retrospective

The reflect-and-extract-lessons skill. Looks back at a completed slice (milestone / sprint / epic / mission), separates what worked from what didn't, surfaces non-obvious surprises, produces actionable next-steps, and contributes generalizable lessons to the brain. Distinct from `pm-assess` (now-state synthesis without reflection), `pm-status-report` (outward cadence), `ops-incident` (single-incident response — incident reports are inputs to a retro, not the retro itself).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "retro", "retrospective", "post-mortem the milestone", "what did we learn", "lessons from X", "do a retro on Y", "look back at the sprint".
- **Slice-completion signal**: a milestone/epic/sprint just closed; operator wants to capture the learning before moving on.
- **Mission-level moment**: a mission was reached (e.g., Post-Anthropic 2026-04-25); operator wants to extract the lessons that shaped it.
- **Pattern-repeating concern**: operator notices the same friction surfacing across milestones; retro to identify the systemic root.

Do NOT load when:

- Single incident analysis is the request — load `ops-incident` (its Operation 3 is the per-incident retro).
- Operator wants now-state, not reflection — load `pm-assess`.
- Operator wants outward cadence report — load `pm-status-report`.
- Operator wants a forward plan — load `pm-plan`.
- Operator wants release notes — load `pm-changelog`.

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Define the slice + gather evidence

**Trigger**: skill loaded; operator named the slice (or it's clear from session context — e.g., "the post-Anthropic milestone").

**Process**:

1. Define the SLICE precisely — start, end, scope:
   - Time window: e.g., 2026-03-01 to 2026-04-25.
   - Scope: which epic / milestone / arc (named).
   - Exclusions: what's NOT in scope (other concurrent work that ran in parallel).
2. Pull evidence from the slice's window:
   ```bash
   git log --since="<start>" --until="<end>" --no-merges --oneline | head -50
   git log --since="<start>" --until="<end>" --shortstat --no-merges | tail -2   # volume signal
   ls wiki/backlog/tasks/T*.md 2>/dev/null   # tasks closed in window
   ls docs/incidents/INC-*.md 2>/dev/null    # incidents in window
   ls docs/HANDOFF-*.md 2>/dev/null          # handoffs that bridged sessions
   ls docs/POSTMORTEM-*.md 2>/dev/null       # one-off post-mortems already authored
   ```
3. Pull the PLAN that was active during the slice (if one existed):
   - `git show <pre-slice-ref>:.aicp/state.yaml` — what the plan said at slice start.
   - Compare to actual outcome: which milestones shipped, which didn't, which got reordered.
4. Pull commit-message themes (signals about the work's CHARACTER, not just count):
   ```bash
   git log --since="<start>" --until="<end>" --pretty="%s" | grep -oE "^[a-z]+:" | sort | uniq -c | sort -rn
   # ratio of feat / fix / refactor / docs tells you a lot about the slice's mode
   ```
5. Pull external context that shaped the slice — the "why this slice mattered" inputs:
   - Operator messages from the brain log / wiki/log/ entries authored in the window.
   - Hardware unlocks / pricing changes / cloud-provider events that drove decisions.

**Quality bar (Operation 1 done when)**:

- [ ] Slice boundaries explicit: start date / end date / scope / exclusions.
- [ ] Git activity over the window quantified (commits, files-changed, theme distribution).
- [ ] Tasks/incidents/handoffs/post-mortems in window enumerated.
- [ ] Plan-vs-actual delta captured.
- [ ] External context (operator quotes, hardware events) gathered.

### Operation 2: Extract findings — Worked / Didn't / Surprising / Keep-Stop-Start

**Trigger**: Operation 1 evidence assembled.

**Process**:

1. Author the retro in this 5-section structure:
   ```markdown
   # Retrospective — <slice name> (<start>..<end>)

   ## Slice scope
   <one paragraph: what was in/out of scope, why this slice was named>

   ## What worked (and why)
   - <fact>: <why it worked, evidence>. Example: <commit / handoff / incident>.
   - ...

   ## What didn't work (and why)
   - <fact>: <why it didn't, evidence>.
   - ...

   ## Surprises (things we didn't expect to learn)
   - <surprise>: <what we now know that the plan didn't anticipate>.
   - ...

   ## Keep / Stop / Start
   - **Keep doing**: <pattern>. Reason: <evidence from this slice>.
   - **Stop doing**: <anti-pattern>. Reason: <how it cost us>.
   - **Start doing**: <new practice>. Reason: <gap this slice exposed>.

   ## Action items
   - [ ] <action>. Owner: <op / next session>. Due: <date>. Skill: <which to load>.
   - ...

   ## Lessons (generalizable — candidates for brain contribution)
   - <lesson>: <one paragraph, AICP-or-fleet-relevant pattern that other projects could benefit from>.
   - ...
   ```
2. **Worked / Didn't / Surprising** must each have evidence — a commit SHA, an incident path, a quoted operator decision, a measured outcome. No "I think the routing went well" without a metric.
3. **Keep/Stop/Start** is THIS slice's signal, not generic advice:
   - ✅ "Stop deploying after 17:00 — the two recent late deploys both rolled back."
   - ❌ "Stop having so many bugs."
4. **Action items** are time-boxed and skill-named:
   - ✅ "[ ] Add `make profile-validate` to CI pre-merge gate. Owner: next session. Due: 2026-05-04. Skill: foundation-ci."
   - ❌ "Improve quality processes."
5. **Lessons** are FILTERED for "could another project benefit?" — only those go to brain. Project-specific ones stay in the retro.
6. Be honest about negative findings. The retro's value is the willingness to name what didn't work. If everything is "great", the retro isn't a retro — it's a victory lap.

**Quality bar (Operation 2 done when)**:

- [ ] All 6 sections populated with evidence per entry.
- [ ] Worked / Didn't / Surprising each have ≥2 entries (or the slice was too small for a retro — flag and stop).
- [ ] Keep/Stop/Start each have ≥1 entry, slice-specific not generic.
- [ ] Action items have owner + due date + skill.
- [ ] Lessons filtered: only generalizable ones marked for brain contribution.
- [ ] At least one negative finding present (or explicit note "this slice had no observable failures, which is itself a finding to investigate").

### Operation 3: Persist + contribute

**Trigger**: Operation 2 retro authored.

**Process**:

1. Persist the retro:
   - Write to `docs/retros/RETRO-<slice-slug>-<YYYY-MM-DD>.md`.
   - Cross-link from `.aicp/state.yaml` if appropriate (a `recent_retros:` field).
2. File action items where the project tracks tasks:
   ```bash
   # for each action item:
   python3 -m tools.gateway task new --title "<action>" --due "<date>"
   ```
3. Contribute generalizable lessons to the brain (only those filtered as cross-project):
   ```bash
   python3 -m tools.gateway contribute --type lesson --title "<lesson title>"
   # Body: the lesson paragraph + AICP slice as evidence + applicability conditions.
   ```
   Lessons that DO NOT generalize stay in the retro file; don't pollute the brain with project-specific narrative.
4. Commit retro + state.yaml updates as a separate commit:
   ```
   git commit -m "retro(<slice>): findings + <N> action items"
   ```
5. Hand off the most-important action item:
   - Identify the highest-leverage Keep/Stop/Start change.
   - Tell operator: "Top action: <X>. Skill to load: <Y>. Want to do it now or later?"

**Quality bar (Operation 3 done when)**:

- [ ] Retro persisted to `docs/retros/RETRO-*.md`.
- [ ] Each action item filed as a task (or "no tasks needed — all are conversational").
- [ ] Brain contributions submitted for filtered lessons (or "no lessons generalized — all project-specific").
- [ ] Commit made (separate from any other change).
- [ ] Top action item surfaced to operator with skill name and immediate-vs-deferred ask.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Sliding into a victory lap

Slice ended; everything mostly worked. Retro lists 8 things that worked, 0 things that didn't, 1 surprise framed positively. Reads as a self-congratulation document. The team learns nothing because nothing surfaced as wrong.

**The rule**: Operation 2 step 6 — every retro must surface at least one negative finding OR explicitly note the absence is itself a finding ("nothing observed went wrong; investigate whether the bar for noticing failure is too high"). A retro with no negatives is a retro that didn't look. Re-examine the evidence — what FRICTION existed even if no failure landed?

### Gotcha 2: Generic Keep/Stop/Start

Retro says: "Keep: shipping fast. Stop: cutting corners. Start: writing more tests." None of these names this slice's actual pattern. Generic advice is unactionable; nothing specific changes after the retro.

**The rule**: Operation 2 step 3 — Keep/Stop/Start must reference THIS slice's evidence. "Stop deploying after 17:00" beats "Stop cutting corners" because it names a specific pattern with a measurable boundary. If you can't write a Stop entry naming the slice's evidence, you don't have a Stop entry — you have a wish.

### Gotcha 3: Action items without owner or date

Retro lists 12 action items, none have owner or due date. Six months later, the retro file is read; nothing happened. The action items were aspirations dressed as plans.

**The rule**: Operation 2 step 4 + Operation 3 step 2 — every action item has owner + due + skill. If owner is "next session", that means it's filed as a task NOW; if no task is filed, the action item evaporates the moment the retro file is closed. Don't leave them dangling.

### Gotcha 4: Polluting the brain with project-specific narrative

Retro contains a story about how a specific config bug was found in `config/profiles/quality.yaml`. Operator clicks "contribute lesson". Brain now has a lesson titled "AICP profile quality.yaml has a band-1 routing bug" — useful to no other project. The brain accumulates AICP-specific noise.

**The rule**: Operation 2 step 5 + Operation 3 step 3 — lessons are FILTERED. Only those that generalize ("a profile system whose YAMLs override root config can re-introduce removed entries silently") go to brain. The specific incident stays in the retro file as evidence. The brain accepts patterns and standards, not project diaries.

### Gotcha 5: Retro on too-small a slice

Operator runs retro after a single 2-day work session. There isn't enough evidence to surface meaningful patterns; the retro produces 5 weak "findings" that are really just observations. Time spent retro-ing exceeded value extracted.

**The rule**: Operation 2 step 2 — if Worked / Didn't each have <2 substantial entries, the slice is TOO SMALL for a retro. Tell the operator: "This slice is short; consider rolling it into the next retro or just capturing one-off lessons via brain contribution directly." Retros are for slices with enough evidence to find patterns, not for every milestone.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning. For retro ARTIFACTS specifically, the Post-Anthropic mission (reached 2026-04-25) is a candidate slice for a mission-level retro at AICP scale.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP retros tend to be mission-scoped (Post-Anthropic) or stage-scoped (Stage 1 LocalAI bring-up; Stage 4 reliability). Evidence comes from git log + task closures + incidents + handoffs + brain contributions. The brain (at `~/devops-solutions-information-hub/`) is where generalizable lessons go — those become wiki/lessons/ entries that other projects in the ecosystem can benefit from. Project-specific narrative stays in `docs/retros/`. Sister projects (openfleet, dspd, nnrt) have their own retro homes; this skill adapts.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| pm-assess | Now-state synthesis, no reflection | Now; this skill is reflective |
| pm-status-report | Cadence outward report | Outward; this skill is internal reflection |
| pm-handoff | Forward continuity | Forward; this skill is backward |
| pm-plan | Forward planning | Forward; this skill informs the next plan |
| pm-changelog | User-facing release notes | User audience; this skill is operator-internal |
| ops-incident | Single-incident response (Op3 = per-incident retro) | Per-incident; this skill is per-slice across multiple incidents/work |
| incident-cycle | Compound incident → fix → prevention workflow | Per-incident lifecycle; this skill is slice-level |
