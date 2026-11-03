---
name: legal-legal-audit
description: Audit a business's existing legal documents — contracts, policies, terms and governance records — against standards, finding missing, expired and non-compliant items ranked by severity with a remediation order. Use when the user wants to know what legal paperwork they are missing or which documents are out of date.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: legal
  phase: 0
  artifact: 00-assess.md
---

# Legal Audit

Conduct a comprehensive legal audit of "$ARGUMENTS". Inventory existing legal documents, check them against industry standards, and identify gaps requiring remediation.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"legal-legal-audit","workflow":"legal","phase":0,"project":"<project>","event":"skipped","artifact":"00-assess.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 0 (Assess) of the Legal Lifecycle workflow (`legal`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `legal` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole Legal Lifecycle workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After your section's italic line, add a `### Recalled` subsection of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"legal-legal-audit","workflow":"legal","phase":0,"project":"<project>","event":"started","artifact":"00-assess.md","note":""}`.

None — this is a Phase 0 Assess skill.

## Process

1. **Inventory existing legal documents:**
   - Contracts (customer, vendor, partner, employment)
   - Policies (privacy policy, acceptable use, data retention, security)
   - Terms of service and end-user license agreements
   - Compliance documentation and certifications
   - Corporate governance documents

2. **Check each against industry standards:**
   - Read `references/compliance-checklist.md` for reference
   - Compare document coverage against standard legal frameworks
   - Verify documents are current (not expired or outdated)
   - Check for internal consistency across documents

3. **Identify gaps:**
   - Missing policies that should exist for the business type
   - Expired or outdated contracts requiring renewal
   - Non-compliant documents that fail to meet regulatory requirements
   - Incomplete coverage areas (e.g., no data processing agreements)

4. **Categorize gaps by severity and urgency:**
   - **Critical** — immediate legal exposure or regulatory violation
   - **High** — significant risk if not addressed within 30 days
   - **Medium** — should be addressed within 90 days
   - **Low** — improvement opportunity, no immediate risk

5. **Prioritize remediation:**
   - Rank gaps by severity x urgency
   - Estimate effort for each remediation item
   - Identify quick wins vs. long-term projects
   - Recommend sequencing of remediation work

6. **Write the artifact** — append to `.singularskills/legal/<project>/00-assess.md` under a `## Legal Audit` section. Create the file with a `# Assess — <project>` heading if it does not exist; if a `## Legal Audit` section already exists, replace only that section. The section contains:

   - **Document Inventory** — all existing legal documents cataloged
   - **Standards Comparison** — how each document measures against benchmarks
   - **Gap Analysis** — missing, expired, or non-compliant items
   - **Severity Matrix** — gaps categorized by severity and urgency
   - **Remediation Priorities** — ordered action items with effort estimates

## Output

The legal audit appended to `.singularskills/legal/<project>/00-assess.md`. Present a summary to the user highlighting:
- Total documents inventoried vs. gaps found
- Critical and high-severity items requiring immediate attention
- Top 3 recommended remediation actions

**Record the run.** After you have written your section, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"legal-legal-audit","workflow":"legal","phase":0,"project":"<project>","event":"finished","artifact":"00-assess.md","note":""}`.

This artifact is shared by every skill of phase 0 (Assess). The frontmatter is written once, by whoever creates the file: if you create it, open it with the block below (`skill` is the phase title, `started` the time of that first write; `gate` is `none`, as this phase has no gate); if it already exists, leave the block alone except to update `finished`.

```yaml
---
skill: Assess
workflow: legal
phase: 0
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

Open your `## Legal Audit` section with one italic line, `*<skill name> · <ISO timestamp> · gate: none*` (your skill name is `legal-legal-audit`).

End your section with `### Decisions` and `### Open questions` (one level under your `## Legal Audit` heading, so the section stays one block), in this shape:

```markdown
### Decisions
- <what was chosen> — <why> — <what was rejected>

### Open questions
- <what the next phase or a reviewer must settle>
```
