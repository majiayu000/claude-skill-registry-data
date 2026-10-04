---
name: pm-handoff
description: Author a handoff document that lets the next session (or operator) pick up where this one left off — the north star, what's done, what's in-flight, what to do next, exact paths to authoritative sources, and the gotchas that aren't obvious from the code. For AICP this typically lands at `docs/HANDOFF-<topic>-<YYYY-MM-DD>.md`. Distinct from `pm-assess` (point-in-time analysis), `pm-status-report` (cadence outward report), and `pm-retrospective` (look-back). Loads when the operator says "handoff", "let's not lose context", "before we compact", "write what the next session needs", "session is ending — preserve the state".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# pm-handoff

The cross-session continuity skill. Produces a self-contained document the next session reads first to resume orderly — north star, brain references, progress map, how-to-resume procedure, gotchas. Distinct from `pm-assess` (synthesis for orientation, not transition), `pm-status-report` (outward cadence), `pm-retrospective` (look-back).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "handoff", "write a handoff", "preserve context", "before we lose state", "before compaction", "what does the next session need".
- **Pre-compaction signal**: operator notices the conversation is approaching context limits and wants the work captured durably.
- **Mid-arc handoff**: an in-flight epic/sprint/refactor needs to span sessions — operator wants the next picker-upper to be productive immediately.
- **Onboarding-style ask**: a new contributor / future-self / sister-project agent needs to understand this work.

Do NOT load when:

- Operator wants the now-state without forward direction — load `pm-assess`.
- Operator wants a cadence report (weekly/monthly outward) — load `pm-status-report`.
- Operator wants user-facing release notes — load `pm-changelog`.
- Operator wants to launch a new agent (project-onboarding, not session-handoff) — load `onboarding-cycle`.
- Operator wants what changed since last week (no forward direction) — load `pm-status-report`.

## Operations

This skill has 3 named operations. Execute in order.

### Operation 1: Gather signals — what is the handoff actually about?

**Trigger**: skill loaded; operator named the topic (or it's clear from session context).

**Process**:

1. Identify the SCOPE of the handoff. Three classes:
   - **Active task** (most common): an in-flight piece of work that must continue. Example: skills audit Phase 2.
   - **Whole project at session-end**: orientation snapshot — covers identity, state, immediate next move.
   - **Cross-arc / cross-session direction**: post-mission posture, mid-pivot, mid-refactor. Larger scope; longer doc.
2. Pull the same signals as `pm-assess` (state.yaml, active task, recent commits, brain compliance, incidents) — but with a forward bias:
   ```bash
   cat .aicp/state.yaml 2>/dev/null
   .venv/bin/aicp --task-cmd show 2>&1 | tail -10
   git log --since="3 days ago" --oneline   # the trailing context the operator has in head
   ls -t docs/HANDOFF-*.md 2>/dev/null | head -3   # prior handoffs to reference
   ```
3. Identify the SOURCES that the next session must consult. Two layers:
   - **Authoritative**: brain Extension Standards path / AICP CLAUDE.md / specific decision file. The handoff cites them but does not duplicate them.
   - **Live**: the current working state — uncommitted changes, in-flight files, recent thinking. The handoff captures these because they're not yet in any committed source.
4. Identify the operator's framing for the work — the verbatim phrase that anchors WHY this work matters. Preserve it exactly:
   - ❌ paraphrase: "the operator wants the brain's pattern applied"
   - ✅ verbatim: "the second-brain knows better. but get back on track after going and ingesting what it has to teach"
5. Identify the gotchas of the resumption itself — what would the next session get WRONG if not warned:
   - "Don't try to teach the brain — it's the source of truth here."
   - "Don't pattern-match this handoff alone — re-read the brain references first."
   - "Don't fabricate values — verify."

**Quality bar (Operation 1 done when)**:

- [ ] Handoff scope classified (active-task / whole-project / cross-arc).
- [ ] Live state snapshot captured (state.yaml + active task + recent commits + uncommitted).
- [ ] Authoritative sources identified by absolute path/URL.
- [ ] Operator framing captured verbatim (one or two phrases).
- [ ] Resumption gotchas listed.

### Operation 2: Author the handoff document

**Trigger**: Operation 1 signals gathered.

**Process**:

1. Pick the right shape for the scope:
   - **Active-task handoff**: 8 sections ≈ 200 lines. North star / brain references / pattern / progress / how-to-resume / outside concerns / right-way-to-act / impatient-summary.
   - **Whole-project handoff**: 5 sections ≈ 100 lines. Project identity / state now / next move / open risks / pointers.
   - **Cross-arc handoff**: 10+ sections ≈ 400 lines. Adds milestone-by-milestone history + decision log.
2. Use this self-contained-on-resume structure (active-task variant — the most common):
   ```markdown
   # Handoff — <topic> (<YYYY-MM-DD>)

   **Written**: <YYYY-MM-DD>, <where in the arc>.
   **For**: next session (same operator), to resume <task> without re-discovery.
   **Read first**: this document. It tells you the north, what's done, what's left, and how to resume orderly.

   ---

   ## 1. North star (one paragraph)
   <mission posture, current direction, why now>

   ## 2. Authoritative references
   | Reference | Location |
   ...
   <brain standards / decision files / sister-project manifests>

   ## 3. The pattern / standard being applied
   <verbatim reproduction of the structure or rule, so next session doesn't pattern-match imperfectly>

   ## 4. Progress as of <date>
   ### ✅ Done — <N> items
   <list with one-line summary each>
   ### 🔲 Remaining — <N> items, in suggested order
   <ordered list>
   ### Already-correct items (do NOT redo)
   <list — equally important>

   ## 5. How to resume orderly
   1. Read this handoff in full.
   2. <next concrete step>
   ...
   ### What "orderly" means (operator's rules from the session)
   - ✅ DO ...
   - ❌ DON'T ...

   ## 6. Critical context outside the main task
   ### Stable — committed
   ### Active — uncommitted at handoff
   ### Pre-existing technical debt (separate concerns)

   ## 7. The right way to act on resume
   <verbatim operator framing + any operational rules learned from the session>

   ## 8. One-paragraph summary for the very impatient
   <60 words; the whole handoff in case the next session can only read one paragraph>
   ```
3. Write where the next session will FIND it:
   - `docs/HANDOFF-<topic>-<YYYY-MM-DD>.md` is the AICP convention.
   - Title in filename and in document header so the IDE-opened-file context surfaces it.
4. The handoff is self-contained: it answers "where are we / what do I do / what would I get wrong" without needing the next session to ask.
5. Reproduce structures verbatim, don't summarize them. If the next-session needs the gold-standard SKILL.md template, paste the template into section 3 — don't summarize "uses the standard structure".
6. Authoritative facts go to authoritative sources via cross-link; the handoff captures them BY REFERENCE. Don't duplicate authoritative content — duplication rots.

**Quality bar (Operation 2 done when)**:

- [ ] Document written at `docs/HANDOFF-<topic>-<date>.md` (or sister-project equivalent).
- [ ] All 8 sections (active-task variant) populated with NO placeholder TBDs.
- [ ] Operator framing captured verbatim.
- [ ] Authoritative sources cited with absolute paths.
- [ ] Self-contained: a fresh session reading only this doc + the cited sources can resume.
- [ ] Pattern/standard reproduced verbatim (no "uses the standard" summaries).

### Operation 3: Verify + announce

**Trigger**: Operation 2 document written.

**Process**:

1. Self-test the handoff: read it as if you've never seen the work before.
   - Can you tell what to do FIRST?
   - Can you tell what NOT to do?
   - Can you find every authoritative source via the paths cited?
   - If a key fact is missing, fix it now — the value of a handoff is its completeness at write-time.
2. Update cross-references:
   - Add a link to the handoff in `.aicp/state.yaml` (if state.yaml exists and has a `recent_handoffs` field).
   - If the work was tracked under a wiki epic / Plane project: add a link there too.
3. Confirm the operator can find the handoff:
   - State the absolute path: `docs/HANDOFF-<topic>-<date>.md`.
   - State the filename pattern (so future-grep finds it): `ls docs/HANDOFF-*-2026-04-*.md`.
4. If the session is also about to compact: the handoff is now the BRIDGE document. Tell the operator: "Document is at <path>. The next session should be told to read this file first."

**Quality bar (Operation 3 done when)**:

- [ ] Handoff self-tested: a fresh session can resume from it alone (with cited sources).
- [ ] state.yaml or equivalent updated with the handoff reference (or "no state.yaml in this project").
- [ ] Operator told the absolute path.
- [ ] If pre-compaction: explicit instruction to next session to read the handoff first.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Handoff that summarizes the brain instead of citing it

Handoff section "the standard" paraphrases the brain's gold-standard pattern in two paragraphs. Next session reads the paraphrase, applies what it remembers — which is the paraphrase, not the brain. Pattern drifts each handoff cycle until the brain's actual standard is unrecognizable.

**The rule**: Operation 2 step 5 reproduces the pattern VERBATIM (or, if too long, includes the path AND a verbatim sample). Authoritative sources must be cited so the next session goes to THEM, not to the handoff's interpretation. The handoff is a router, not a redaction.

### Gotcha 2: Forgetting the operator's verbatim framing

Handoff sanitizes the operator's "the second-brain knows better. but get back on track" into "operator prefers brain-aligned approaches". The verbatim phrasing CARRIED context — "get back on track" implies prior drift; "knows better" is a deference signal. The sanitization loses both.

**The rule**: Operation 1 step 4 captures verbatim. Operation 2 step 1's section 7 reproduces it. The operator's words are evidence about WHY the work matters; sanitizing them throws that away. If the verbatim is profane or terse, that's INFORMATION about the operator's mood/urgency at the moment of decision — keep it.

### Gotcha 3: Handoff missing "do NOT" rules

Handoff lists 12 things to DO. Doesn't list a single thing NOT to do. Next session re-treads a wrong path the prior session already learned to avoid — wastes the lesson.

**The rule**: Operation 2 step 2's "How to resume orderly" subsection ALWAYS has DO and DON'T columns. If the session learned a "don't" (e.g., "don't try to teach the brain"), it must be captured. The cost of missing a DO is some inefficiency; the cost of missing a DON'T is repeating a mistake the operator already paid for.

### Gotcha 4: Listing "remaining work" without order

Handoff section "Remaining" has 12 items in alphabetical order. Next session picks alphabetically — but the operator-preferred order was by sibling-skill clusters or by dependency. Next session does it wrong order, has to re-context-switch, work is messier.

**The rule**: Operation 2 step 1's progress section orders Remaining by RECOMMENDED EXECUTION SEQUENCE — sibling clusters, dependency chains, lowest-risk-first, whatever the session learned was the right order. If the order doesn't matter, say so explicitly. Don't default to alphabetical.

### Gotcha 5: No "what's already correct, leave it alone"

Handoff lists "remaining work". Next session goes to do work — but doesn't realize that 17 items were ALREADY in good shape and shouldn't be rewritten. Next session redoes already-correct work, wastes effort, may even regress good work to a less-good version.

**The rule**: Operation 2 step 1's progress section has THREE categories: ✅ done this session, 🔲 remaining, and "already-correct, do NOT redo". The third category is equally critical to call out — every handoff has it (work that was already done before this session) and listing it prevents redundant effort.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning. Specifically for handoff DOCUMENTS (the artifact this skill produces), the recent exemplar at `docs/HANDOFF-SKILLS-PHASE-2-2026-04-27.md` demonstrates the 8-section active-task variant.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP cross-session continuity is an ongoing operational concern: long arcs (Post-Anthropic mission, skills audit Phase 2, MCP Phase 2a/b) span many sessions. The handoff convention is `docs/HANDOFF-<topic>-<YYYY-MM-DD>.md`. The state.yaml + wiki backlog tasks + brain compliance tier are AICP's persistent state — the handoff captures the LIVE state above and beyond those (uncommitted thinking, mid-flight understanding, learned-this-session gotchas). Sister projects (openfleet, dspd, nnrt) handle handoff differently: openfleet has standing-orders.yaml + Mission Control board; this skill adapts to those when invoked there.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| pm-assess | Synthesis for orientation, not transition | Now-state synthesis; this skill is forward-looking continuity |
| pm-status-report | Cadence-driven outward report | Outward; this skill is internal continuity |
| pm-retrospective | Look-back analysis | Backward; this skill is forward |
| pm-changelog | User-facing release notes | User audience; this skill is operator-self/next-session audience |
| pm-plan | Forward planning with milestones | Multi-session plan; this skill is single-transition bridge |
| onboarding-cycle | New contributor onboarding | New person; this skill is same operator across sessions |
