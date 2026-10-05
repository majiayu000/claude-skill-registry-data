---
name: discovery-proposal
description: "Run full discovery-to-proposal workflow — investigation, evidence gathering, writing, and review."
version: 0.1.0
---

## JTBD (Jobs To Be Done)

### Primary Job
When I'm preparing a client engagement proposal and need to go from a live site to a fully reviewed, client-ready proposal package,
I want a single orchestrating skill that runs investigation, drafting, critique, and delivery in sequence with session recovery,
so I don't have to manually coordinate phases across multiple sessions or lose work when a session breaks.

### Secondary Jobs
- When a discovery session was interrupted mid-run, I want to resume exactly where I left off by reading the state file, so I don't re-run work that already completed.
- When a client engagement needs optional technology research (e.g., page builder selection, search architecture) before the proposal is finalized, I want that research integrated into the proposal workflow as an optional gate, so the proposal reflects the actual tech decision rather than placeholder language.

### Job Layers
- Functional: Orchestrate three sub-skills (discovery-investigation, proposal-draft, optional tech research) with state file checkpoints, human gates at phase boundaries, and a final showcase page build.
- Emotional: Eliminate the anxiety of "where were we?" after a session break — the state file is the source of truth and recovery is automatic.
- Social: Produce a complete, reviewed proposal package (technical + client-facing + Google Docs + visual showcase) that can be handed to a client or shared internally with confidence.

### This Skill Is For
- An agency practitioner who needs to take a Drupal site from "we should audit this" to "here is the reviewed proposal and deliverables" in one workflow.
- A user resuming a previously started discovery session after a session break.
- A user who has completed investigation separately and wants to pick up at the proposal drafting phase.

### This Skill Is NOT For
- Investigation alone — use `discovery-investigation` if you only need findings, not a proposal.
- Proposal drafting alone from existing findings — use `proposal-draft` if findings already exist.
- Non-Drupal projects — the investigation phase is Drupal-specific (config YAML analysis, content type auditing).

### Paired With
- `discovery-investigation`: The investigation sub-skill — invoked by this skill at Phase 2.
- `proposal-draft`: The proposal drafting sub-skill — invoked by this skill at Phase 3.
- `zivtech-writing-style`: Applied by proposal-draft to both proposal documents before Google Docs sync.
- `frontend-design`: Used to build the visual showcase pages.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Starting fresh, no state file | 8-question interview → write state file → run all phases | State file, findings.md, technical + client proposals, Google Docs, showcase site |
| Resuming from interrupted session | Read state file → skip completed phases → resume from current_phase | Completed phases + all remaining deliverables |
| Has findings already, wants proposal | Invoke proposal-draft directly (discovery-proposal detects investigation is done) | Reviewed proposal package + Google Docs |

### When to Escalate
- If the site is not Drupal: stop and tell the user to describe the platform — investigation phase needs adaptation.
- If gcloud is not authenticated: investigation and proposal phases run, Google Docs sync is skipped with a recovery instruction.
- If the user only wants investigation (no proposal): suggest running `discovery-investigation` directly.

<Purpose>
discovery-proposal orchestrates the complete Zivtech engagement workflow from initial site investigation through final deliverables. It is the top-level coordinator for three composable sub-skills.

The key design insight: multi-phase work that spans hours or sessions needs a state file contract so each phase is recoverable without re-running earlier work. The state file at `.omc/state/discovery-proposal-state.json` is the source of truth; the skill reads it at startup and writes it at every phase boundary.

Phase sequence:
1. Interview (collect client context, write state file)
2. Investigation (invoke discovery-investigation: config analysis + browser testing + UX analysis + findings + HTML report)
3. Proposal drafting (invoke proposal-draft: draft + 5 critics + synthesis + human gate + revisions + client version + Google Docs)
4. Technology research (optional gate: research decision matrix for key tech choices)
5. Showcase pages (visual narrative of the workflow and deliverables)
6. Completion report

Works on the joyus-ai platform where Lando MCP and Playwright MCP are available. Investigation phase requires both.
</Purpose>

<Use_When>
- User says "discovery proposal", "run discovery", "start the client workflow", "let's do the full engagement"
- User has a Drupal site to audit and wants a complete proposal package
- User has a partially completed discovery session and wants to resume
- User provides a handoff note or state file path from a previous session
</Use_When>

<Do_Not_Use_When>
- User wants only investigation findings, not a proposal — use discovery-investigation
- User has existing findings and wants only proposal drafting — use proposal-draft
- User wants a plan for how to run discovery — use plan-writer
- The project is not Drupal or the site is inaccessible locally
</Do_Not_Use_When>

<Why_This_Exists>
The full discovery-to-proposal workflow involves:
- 10+ parallel agent dispatches across two investigation waves
- Playwright browser testing of 5-10 content types
- Proposal drafting with 5 adversarial critics + synthesis
- Two proposal documents (technical + client-facing)
- Google Docs sync
- Visual showcase pages

Without an orchestrating skill, each phase requires manual coordination, state is lost on session breaks, and work is duplicated across sessions. This skill encodes the phase sequence, state contract, and recovery logic so the practitioner can focus on the human decision gates rather than workflow plumbing.
</Why_This_Exists>

<Steps>
## STEP 0 — Check for existing state

Before anything else, check if `.omc/state/discovery-proposal-state.json` exists in the current working directory.

If it exists:
1. Read the file.
2. Announce: "Resuming discovery-proposal from phase: [current_phase]. Completed: [completed_phases]."
3. Skip to the appropriate phase below.

If it does not exist: proceed to STEP 1.

---

## STEP 1 — Interview (8 questions)

Ask these questions conversationally, not as a form. Combine related questions. Wait for complete answers.

**Context questions:**
1. **Client + project:** Who is the client and what is the project in one sentence?
2. **Tech stack:** Is this Drupal? If yes, which version. If not, what platform?
3. **Proposal type:** What kind of engagement? (UX overhaul / new feature / migration / technical audit / other)
4. **Client history:** Where does existing context live? (Slack channels, Gmail labels, Jira project codes, local handoff files, or "new client")
5. **Budget anchor:** Rough budget expectation or ceiling? ("unknown" is fine)
6. **Google Docs:** Where should final proposals land? (Google Doc URL/ID, or "create new")

**Operational prerequisites:**
7. **Local environment:** Is the local dev environment accessible? If yes: what is the local URL and admin path?
8. **Tool status:** Is gcloud authenticated for this account? Is gh CLI authenticated? (Check via Bash: `gcloud auth list` and `gh auth status`)

After collecting answers, write the initial state file to `.omc/state/discovery-proposal-state.json`:

```json
{
  "version": "1.0",
  "client_name": "[client]",
  "client_slug": "[kebab-case-slug]",
  "project_type": "[drupal|custom|other]",
  "proposal_type": "[type]",
  "budget_anchor": "[amount or unknown]",
  "current_phase": "investigation",
  "completed_phases": ["interview"],
  "paths": {
    "findings_md": "docs/discovery/findings.md",
    "technical_proposal": "",
    "client_proposal": "",
    "visual_report_url": "",
    "showcase_url": "",
    "google_doc_technical_id": "",
    "google_doc_client_id": ""
  },
  "investigation": { "content_types_tested": 0, "critical_findings": 0, "major_findings": 0, "minor_findings": 0 },
  "proposal": { "v1_budget": 0, "final_budget": 0, "critics_run": [], "findings_incorporated": 0 },
  "environment": {
    "local_url": "[url or null]",
    "gcloud_authenticated": true,
    "gh_authenticated": true
  },
  "started_at": "[ISO timestamp]",
  "updated_at": "[ISO timestamp]"
}
```

Announce: "Interview complete. Starting Phase 1: Investigation."

---

## STEP 2 — Investigation Phase

Invoke: **`/discovery-investigation`**

When complete, the state file will have:
- `completed_phases` includes `"investigation"`
- `paths.findings_md` set
- `paths.visual_report_url` set
- `investigation.critical_findings`, `.major_findings`, `.minor_findings` populated

**Gate:** Announce finding counts. Ask: "Ready to move to proposal drafting? (yes / no / I want to review findings first)"

---

## STEP 3 — Proposal Phase

Invoke: **`/proposal-draft`**

When complete, the state file will have:
- `completed_phases` includes `"proposal"`
- `paths.technical_proposal` and `paths.client_proposal` set
- `paths.google_doc_technical_id` and `paths.google_doc_client_id` set
- `proposal.v1_budget`, `.final_budget`, `.findings_incorporated` populated

**Gate:** Announce budget delta. Ask: "Do you want to run a technology research phase before the showcase? (yes / no)"

---

## STEP 4 — Technology Research (optional)

If the human said yes, proceed. Otherwise skip to STEP 5.

1. Ask: "What technology decision needs researching? Describe the options and the question."
2. Draft a research plan listing tracks and the specific question each track answers.
3. Self-critique the plan: "What track is missing? What assumption am I making?" Add missing tracks.
4. Announce tracks and agent count. Ask: "Approve this research plan? (yes / modify / skip)"
5. On approval, dispatch parallel research agents (sonnet/haiku by complexity). Compile into a decision matrix at `docs/discovery/tech-research.md`.
6. Update state: `completed_phases` includes `"research"`, `paths.tech_research` set.

**Gate:** Present recommendation. Ask: "Does this match your read? Should I update the proposal to reference this decision?"

---

## STEP 5 — Showcase Pages

1. Invoke `/frontend-design` to build the two-page showcase site (The Numbers + How It Works) using data from the completed state file.
2. Showcase pages go in `~/claude/zivtech-demos/projects/[client-slug]-process/`.
3. Update `deploy.yml` to include the new project with staticrypt password `[client-slug]2026`.
4. Commit and push. Wait for GitHub Actions to complete.
5. Update state: `paths.showcase_url` set, `completed_phases` includes `"showcase"`.

---

## STEP 6 — Completion Report

Update state: `current_phase: "complete"`, `updated_at: [timestamp]`.

Output:
```
✓ Discovery-to-Proposal workflow complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client:             [client_name]
Proposal:           $[v1_budget] → $[final_budget] (after critic review)
Critics run:        [count] | Findings incorporated: [count]
Technical proposal: [path]
Client proposal:    [path]
Google Docs:        [technical URL] / [client URL]
Visual report:      [visual_report_url]
Showcase:           [showcase_url]  pw: [client-slug]2026
State file:         .omc/state/discovery-proposal-state.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Recovery (session break mid-run)

If starting a new session with `.omc/state/discovery-proposal-state.json` present:
1. Read the file.
2. Check `completed_phases` to see what finished.
3. Check `current_phase` to see where you were.
4. Resume from the appropriate STEP above.

The state file is the source of truth. Trust it over memory.
</Steps>

<Tool_Usage>
- Use the Skill tool to invoke sub-skills: `/discovery-investigation` and `/proposal-draft`
- Use Bash to check gcloud and gh authentication status
- Use Read/Write for the state file at `.omc/state/discovery-proposal-state.json`
- Use Agent tool to dispatch parallel research agents in STEP 4
- Investigation requires Lando MCP (for config file access) and Playwright MCP (for browser testing) — both available on the joyus-ai platform
</Tool_Usage>

<Escalation_And_Stop_Conditions>
- If local_url is null and the user cannot start Lando/DDEV: stop and tell the user the investigation phase requires a running local environment accessible via Lando MCP or DDEV MCP.
- If gcloud is not authenticated: run investigation and proposal phases normally; skip Google Docs sync and tell the user how to authenticate (`gcloud auth login --update-adc`).
- If gh is not authenticated: run investigation and proposal phases normally; skip GitHub Pages deploy for showcase and HTML report.
- If the site is not Drupal: stop at STEP 2 and ask the user to describe the platform before proceeding — the investigation phase needs adaptation.
</Escalation_And_Stop_Conditions>

Task: {{ARGUMENTS}}
