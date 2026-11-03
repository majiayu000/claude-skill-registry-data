---
name: legal-nda
description: Generate a mutual or one-way Non-Disclosure Agreement — definition of confidential information, standard exclusions, permitted use, term and survival, return of materials, remedies and governing law. Use when the user is about to share confidential information with another party and needs an NDA drafted.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: legal
  phase: 1
  artifact: 01-draft.md
---

# Non-Disclosure Agreement

Generate a Non-Disclosure Agreement for "$ARGUMENTS". Produce a comprehensive NDA tailored to the parties, relationship type, and confidentiality needs.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"legal-nda","workflow":"legal","phase":1,"project":"<project>","event":"skipped","artifact":"01-draft.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Draft) of the Legal Lifecycle workflow (`legal`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `legal` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"legal-nda","workflow":"legal","phase":1,"project":"<project>","event":"refused","artifact":"01-draft.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"legal-nda","workflow":"legal","phase":1,"project":"<project>","event":"started","artifact":"01-draft.md","note":""}`.

Check that `.singularskills/legal/<project>/00-assess.md` exists. If it does not exist, stop and tell the user:

> "Run an Assess skill first (e.g. `/legal-risk-assessment <project>`) to generate the prerequisite assessment artifact."

## Process

1. **Read inputs:**
   - Read `.singularskills/legal/<project>/00-assess.md` for context on parties and risk profile
   - Read `references/contract-template.md` for standard contract provisions

2. **Determine NDA type:**
   - **Mutual (bilateral)** — both parties share confidential information
   - **One-way (unilateral)** — only one party discloses confidential information
   - Identify the disclosing and receiving parties

3. **Define parties:**
   - Full legal names and entity types
   - Jurisdictions of incorporation
   - Principal business addresses
   - Authorized signatories

4. **Draft the following sections:**

   - **Definition of Confidential Information** — broad definition with specific examples relevant to the business context (technical data, business plans, customer lists, financial information, trade secrets, product roadmaps, source code, algorithms, etc.)
   - **Exclusions from Confidential Information** — standard exclusions:
     - Information in the public domain (not through breach)
     - Information independently developed without use of confidential information
     - Information already known to the receiving party prior to disclosure
     - Information received from a third party without restriction
     - Information required to be disclosed by law or court order (with notice obligations)
   - **Permitted Use and Disclosure** — scope of permitted use (evaluation, negotiation, specific project), permitted recipients (employees, advisors, contractors with need-to-know)
   - **Obligations of Receiving Party** — duty of care (at least same as own confidential information, but no less than reasonable care), security measures, marking requirements, access limitations
   - **Term of Agreement and Survival Period** — agreement duration (typically 1-3 years), survival of confidentiality obligations beyond termination (typically 2-5 years, indefinite for trade secrets)
   - **Return or Destruction of Information** — obligation to return or certify destruction upon request or termination, exception for legally required archival copies
   - **Remedies** — acknowledgment that breach may cause irreparable harm, right to seek injunctive relief without posting bond (where permitted), right to recover attorneys' fees
   - **Governing Law** — choice of law, jurisdiction for disputes, venue selection

5. **Include standard provisions from contract template:**
   - No implied license or IP transfer
   - No obligation to complete a transaction
   - Relationship of parties (no partnership, agency, or joint venture)
   - Assignment restrictions
   - Severability
   - Entire agreement
   - Counterparts and electronic signatures
   - Amendment requirements (written, signed by both parties)

6. **Write the artifact** — append to `.singularskills/legal/<project>/01-draft.md` under a `## Non-Disclosure Agreement` section. Create the file with a `# Draft — <project>` heading if it does not exist; if a `## Non-Disclosure Agreement` section already exists, replace only that section.

## Output

The NDA draft appended to `.singularskills/legal/<project>/01-draft.md`. Present a summary to the user highlighting:
- NDA type (mutual or one-way)
- Parties identified
- Term and survival period
- Key protections included
- Areas flagged for attorney review

**Record the run.** After you have written your section, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"legal-nda","workflow":"legal","phase":1,"project":"<project>","event":"finished","artifact":"01-draft.md","note":""}`.

This artifact is shared by every skill of phase 1 (Draft). The frontmatter is written once, by whoever creates the file: if you create it, open it with the block below (`skill` is the phase title, `started` the time of that first write; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`); if it already exists, leave the block alone except to update `finished` and to set `gate` to the worst value among the sections (`skipped` over `passed`).

```yaml
---
skill: Draft
workflow: legal
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

Open your `## Non-Disclosure Agreement` section with one italic line, `*<skill name> · <ISO timestamp> · gate: <passed|skipped>*` (your skill name is `legal-nda`).

End your section with `### Decisions` and `### Open questions` (one level under your `## Non-Disclosure Agreement` heading, so the section stays one block), in this shape:

```markdown
### Decisions
- <what was chosen> — <why> — <what was rejected>

### Open questions
- <what the next phase or a reviewer must settle>
```
