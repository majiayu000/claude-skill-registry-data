---
name: proposal-draft
description: "Generate client-ready proposal packages from discovery findings with evidence gathering, writing, and multi-critic review."
version: 0.1.0
---

## JTBD (Jobs To Be Done)

### Primary Job
When I have discovery findings and need to turn them into a proposal package,
I want a skill that drafts, critiques, synthesizes, revises, and produces both a technical and client-facing version with a single invocation,
so the final proposal reflects 5 expert perspectives rather than my first draft, and I'm not doing critic coordination manually.

### Secondary Jobs
- When 5 parallel critics disagree on a scope item, I want conflicts surfaced explicitly with both positions stated and a human decision gate, so I'm not left with a synthesized compromise that pleases nobody.
- When the proposal has been revised, I want a Google Docs sync so the client and internal team have a shared, live document rather than emailed attachments.

### Job Layers
- Functional: Produce `01-technical.md` + `02-client.md` under `docs/proposals/{date}-{slug}/`, run 5 critic agents and a synthesis agent, apply approved changes, sync to Google Docs.
- Emotional: Replace the anxiety of "is this proposal good enough?" with structured critique coverage — proposal scope, Drupal accuracy, implementation sequencing, UI/UX coverage, and design/frontend scope all reviewed before the client sees it.
- Social: Give the client a proposal that is outcome-oriented and jargon-free, demonstrating that the agency translated technical findings into business value — not a config dump.

### This Skill Is For
- An agency practitioner who has discovery findings and needs to write and review a proposal.
- A user picking up proposal drafting after investigation was completed in a previous session.
- A user who wants to revise an existing proposal by re-running the critic + synthesis cycle.

### This Skill Is NOT For
- Investigation — this skill starts after findings exist. Use `discovery-investigation` if you need to generate findings first.
- Non-Drupal proposals — the drupal-critic and drupal-planner agents apply Drupal-specific review criteria.
- Generating a brand new proposal without findings — findings.md is required input.

### Paired With
- `discovery-investigation`: The upstream skill that produces findings.md.
- `discovery-proposal`: The orchestrator that invokes this skill and passes the state file.
- `zivtech-writing-style`: Applied to both documents before Google Docs sync.
- `proposal-critic`: Complementary to the 5-critic review — can be run separately for additional structural review.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Fresh proposal from findings.md | Structure → draft → 5 critics → synthesis → human gate → revisions → client version → Google Docs | 01-technical.md, 02-client.md, two Google Docs |
| Existing proposal needs re-critique | Skip draft step, re-run critics on existing file, synthesize, apply approved changes | Revised 01-technical.md, 02-client.md, synced Google Docs |
| Proposal complete but Google Docs missing | Skip to STEP 9, sync existing documents | Google Docs URLs |

### When to Escalate
- If findings.md does not exist: stop and tell the user to run `discovery-investigation` first.
- If gcloud is not authenticated: produce both documents but skip Google Docs sync with recovery instructions.
- If 3+ MUST changes survive critique: announce the count and ask whether to continue or address findings interactively.

<Purpose>
proposal-draft converts discovery findings into a reviewed, deliverable proposal package using adversarial critique before the client sees anything.

The core insight: a first-draft proposal always has scope gaps, under-estimated line items, and Drupal-specific errors. Running 5 parallel specialist critics — each with a different lens — surfaces more gaps than a single reviewer, faster than sequential review.

The 5-critic design:
1. **proposal-critic** (opus): Scope gaps, under-estimated line items, missing exclusions, budget risks, change order risk
2. **drupal-critic** (opus): Technical accuracy — wrong modules, abandoned packages, architectural contradictions, missing dependencies
3. **drupal-planner** (opus): Implementation sequencing — wrong phase order, unaccounted dependencies, operational risks
4. **ui-critic** (sonnet): UI/UX scope coverage — editorial UX findings addressed, accessibility scoped, implied improvements missing
5. **web-design-critic** (sonnet): Design/frontend scope — design system work scoped, theme sequencing, component library needs

A synthesis agent (sonnet) de-duplicates and classifies changes as MUST / SHOULD / CONFLICT before the human sees any of it. Conflicts require explicit human resolution before proceeding.

Client version rules are non-negotiable: no module names, no internal tool names, no "stabilization" framing, no error specifics, outcome-oriented language throughout.

Requires: gcloud authenticated (for Google Docs sync via REST API).
</Purpose>

<Use_When>
- User says "draft the proposal", "write the proposal", "proposal-draft"
- discovery-proposal has invoked this skill as Phase 3
- User has findings.md and wants to produce a proposal package
- User wants to revise an existing proposal using critic feedback
</Use_When>

<Do_Not_Use_When>
- findings.md does not exist — run discovery-investigation first
- User wants only a proposal outline, not a reviewed package — just draft directly
- The engagement is not Drupal-based and Drupal critic review isn't applicable
</Do_Not_Use_When>

<Why_This_Exists>
Without structured critique, proposals:
- Under-scope line items that the engineer later discovers take 3x longer
- Include module recommendations that are abandoned or security risks
- Sequence implementation phases in the wrong order (e.g., theme work before content model is stable)
- Miss UI/UX improvements that the findings imply but the draft doesn't address
- Use technical language that alienates the client

The 5-critic + synthesis design catches all of these before the proposal is shared. The synthesis step prevents the practitioner from being overwhelmed by 5 separate review documents — they see one prioritized, de-duplicated change list.
</Why_This_Exists>

<Steps>
## STEP 0 — Context check

Check `.omc/state/discovery-proposal-state.json`. If it exists, read:
- `paths.findings_md` — the compiled findings file
- `client_name`, `client_slug`, `budget_anchor`
- `proposal.v1_budget` (0 means not yet drafted)
- `paths.google_doc_technical_id`, `paths.google_doc_client_id`

If `proposal.v1_budget > 0` and `completed_phases` includes `"proposal"`: announce "Proposal phase already complete. Run this skill again to revise."

If state file does not exist, ask:
1. "Where is the findings file?" (provide path)
2. "What is the client name and project type?"
3. "What is the budget anchor or expected range?"
4. "Do you have Google Doc IDs to sync to, or should I create new docs?"

---

## STEP 1 — Proposal structure

Based on the findings file, determine:

1. **Phases** — Group findings into implementation phases (e.g., Phase 0: Critical fixes; Phase 1: Core improvements; Phase 2: Editorial UX; Phase 3: Advanced features)
2. **Scope items per phase** — Each finding maps to one or more scope line items
3. **Effort estimates** — Assign hours per line item:
   - Config change only: 2–4 hours
   - Module install + config: 4–8 hours
   - Custom code (simple): 8–16 hours
   - Custom code (complex): 16–40 hours
   - Migration or data transform: estimate explicitly
4. **Total budget** — Sum all phases + 15% contingency

Announce the phase structure and total. Ask: "Does this structure look right before I draft the full proposal? (yes / adjust first)"

---

## STEP 2 — Draft technical proposal

Write to `docs/proposals/{YYYY-MM-DD}-{client-slug}/01-technical.md`:

```markdown
# [Client] — Technical Proposal
**Date:** [date]
**Version:** 1.0 (pre-review)

## Executive Summary
[2–3 sentences: what we found, what we're proposing, what the outcome will be]

## Discovery Findings Summary
[Brief — this audience already has the full report]
- Critical: N | Major: N | Minor: N

## Proposed Engagement

### Phase 0 — [name] (Weeks 1–N)
[Description of phase goal]

| Scope Item | Hours | Notes |
|-----------|-------|-------|
| [item] | [N] | [rationale] |

**Phase total: N hours / $X**

[Repeat for each phase]

## Timeline
[Week-by-week overview]

## Budget Summary
| Phase | Hours | Cost |
|-------|-------|------|
| [Phase 0] | N | $X |
| Contingency (15%) | — | $X |
| **Total** | **N** | **$X** |

## Assumptions
[Key assumptions: client-side time, content freezes, access, etc.]

## What's Not Included
[Explicit exclusions to prevent scope creep]
```

Update state: `proposal.v1_budget: [total]`, `paths.technical_proposal: "docs/proposals/.../01-technical.md"`.

---

## STEP 3 — Parallel critic dispatch (5 agents)

Announce: "Dispatching 5 critic agents in parallel."

Dispatch simultaneously:

The local catalog/meta-router selects each agent and its model; this wrapper does not override model policy.

**1. proposal-critic**
Prompt: "Review this agency proposal for scope gaps, under-estimated line items, missing exclusions, and budget risks. Be specific about which line items are under-scoped and by how much. Flag any assumption that could cause a change order."

**2. drupal-critic**
Prompt: "Review this Drupal proposal for technical accuracy. Flag: module recommendations that are wrong (wrong version, abandoned, security risk), architectural decisions that contradict Drupal best practices, missing dependencies. Correct factual errors about specific modules."

**3. drupal-planner**
Prompt: "Review this Drupal proposal for implementation sequencing. Flag: phases in the wrong order, dependencies between line items not accounted for, items requiring prerequisites not listed. Flag any recommendation that could cause operational problems (performance, data loss, revision bloat, cache issues)."

**4. ui-critic**
Prompt: "Review this proposal for UI/UX scope coverage. Are the editorial UX findings fully addressed? Is accessibility work scoped correctly? Are there UX improvements the findings imply but the proposal doesn't address?"

**5. web-design-critic**
Prompt: "Review this proposal for design and frontend scope. Is design system work scoped? Is theme work sequenced correctly relative to content work? Are component library and pattern library needs addressed?"

Wait for ALL 5 responses before proceeding.

---

## STEP 4 — Critic synthesis

Dispatch a **synthesis agent** through the local catalog/meta-router with all 5 critic outputs:

Prompt: "You have received 5 critic reviews of the same proposal. Produce a single, prioritized, de-duplicated change list. For each change: (1) identify which critic(s) raised it, (2) classify as MUST (scope error, factual error, budget risk) or SHOULD (improvement, missing coverage) or CONSIDER (nice-to-have), (3) if two critics contradict each other, flag it explicitly as CONFLICT with both positions stated. Output format: numbered list, MUST items first."

Count: MUST items, SHOULD items, CONFLICT items.

---

## STEP 5 — Human review gate (mandatory)

Show the user:
```
Critic synthesis complete.
━━━━━━━━━━━━━━━━━━━━━━━━━━━
MUST changes:    N  (scope errors, factual errors, budget risks)
SHOULD changes:  N  (improvements)
CONFLICTS:       N  (critics disagreed — need your call)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Full synthesis output]
```

For each CONFLICT, explicitly ask: "Critics disagreed on [topic]. [Position A] vs [Position B]. Which is correct?"

Wait for responses. Do not proceed until all conflicts are resolved.

Ask: "Approve implementing all MUST changes? Review SHOULD items and tell me which to include. (approve-all / review-should / skip-should)"

---

## STEP 6 — Apply revisions

Implement all approved changes to `01-technical.md`.

For each change:
- Recalculate affected line item hours if scope changed
- Recalculate total budget

Update state:
- `proposal.final_budget: [revised total]`
- `proposal.critics_run: ["proposal-critic", "drupal-critic", "drupal-planner", "ui-critic", "web-design-critic"]`
- `proposal.findings_incorporated: [count of MUST + approved SHOULD]`

Announce budget delta: "Revised from $[v1] to $[final] (+$[delta] from critic review)."

---

## STEP 7 — Client-facing version

Write `docs/proposals/{date}-{slug}/02-client.md`.

**Non-negotiable rules for the client version:**
- No module names (e.g., "node_revision_delete", "Select2", "Canvas 1.2.0") — describe what it does instead
- No internal tool names (Probo, Lando, specific Jira ticket numbers)
- No "stabilization" framing — present everything as improvements, not fixes
- No "how we work" sections if this is an existing client who already knows
- No error specifics (jQuery bugs, specific PHP warnings) — frame as outcomes
- Budget presented as phase totals, not line items
- Language: outcome-oriented ("editors will be able to X") not implementation-oriented ("we will configure Y")

**Gate:** Ask: "Is there anything in the client version that shouldn't be there? (review now / looks good)"

---

## STEP 8 — Writing style audit

Invoke `/zivtech-writing-style` on both documents.

Apply all corrections. The writing style skill takes precedence over any draft language.

---

## STEP 9 — Google Docs sync

Check `environment.gcloud_authenticated` in state file. If false: "gcloud is not authenticated. To sync: run `gcloud auth login --update-adc`. Skipping sync for now."

If authenticated:

1. Get auth token: `TOKEN=$(gcloud auth print-access-token)`

2. If `google_doc_technical_id` is empty in state, create a new doc:
```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://docs.googleapis.com/v1/documents" \
  -d '{"title": "[Client] — Technical Proposal [Date]"}'
```
Save returned document ID to state.

3. Clear existing content and upload full markdown content using `documents.batchUpdate` with `insertText` requests.

4. Announce Google Doc URLs.

Update state:
- `paths.google_doc_technical_id: "[id]"`
- `paths.google_doc_client_id: "[id]"`
- `completed_phases` adds `"proposal"`
- `current_phase: "showcase"` (next phase)
- `updated_at: [timestamp]`

---

## STEP 10 — Completion

Announce:
```
✓ Proposal phase complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Budget:              $[v1] → $[final]  (+$[delta] from critique)
Critics run:         5 (proposal, drupal, planner, ui, web-design)
Findings applied:    N
Technical proposal:  [path]
Client proposal:     [path]
Google Doc (tech):   https://docs.google.com/document/d/[id]
Google Doc (client): https://docs.google.com/document/d/[id]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If running standalone: suggest "Run `/discovery-proposal` to continue with showcase pages, or share the Google Doc links with the client."
</Steps>

<Tool_Usage>
- Use Agent tool to dispatch the 5 parallel critic agents and the synthesis agent — all in one message for parallelism
- Use Skill tool to invoke `/zivtech-writing-style` on both documents
- Use Bash + gcloud CLI for Google Docs sync (see ~/claude/CLAUDE.md for gcloud patterns)
- Use Read/Write/Edit for proposal document files
- Critic agents must NOT spawn their own agents — pass the proposal file content directly in the prompt
- Wait for ALL 5 critics before dispatching synthesis (synthesis needs all 5 outputs)
</Tool_Usage>

<Escalation_And_Stop_Conditions>
- If findings.md path is missing from state and not provided: stop and ask the user for the path before proceeding.
- If gcloud returns a 401 on token request: skip sync, tell user to re-authenticate with `gcloud auth login --update-adc`.
- If synthesis finds 5+ MUST changes: announce the count prominently and ask whether to address interactively or proceed with all.
- If critics return conflicting verdicts on a Drupal technical claim: defer to drupal-critic over proposal-critic — drupal-critic is the Drupal accuracy authority.
</Escalation_And_Stop_Conditions>

Task: {{ARGUMENTS}}
