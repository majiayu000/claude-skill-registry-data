---
name: incident-report
description: Generates professional incident reports using customizable templates. Supports outage, security, performance, and data-loss incident types. Extensible via templates/ and rules/.
argument-hint: "[incident description]"
allowed-tools: Read, Write, Glob, Bash(mkdir:*)
model: haiku
---

# Incident Report

Generate professional incident reports from symptoms, log data, and timeline information. Uses customizable templates and classification rules. Reports are saved to `docs/incidents/` and can optionally be published to Confluence.

---

## Extensibility

This skill loads templates from `templates/` and rules from `rules/` at runtime. To add a new incident type, create a template file in `templates/`. To customize severity thresholds or escalation contacts, edit the files in `rules/`. No changes to `SKILL.md` are needed.

New templates are auto-discovered via Glob — they must have a `.md` extension and valid frontmatter. New rule files are also auto-discovered and applied in filename-alphabetical order.

---

## Instructions

### Step 1 — Load Templates and Rules

Use Glob to find all `.md` files in `${CLAUDE_PLUGIN_ROOT}/templates/` and `${CLAUDE_PLUGIN_ROOT}/rules/` (the plugin's install directory). If `${CLAUDE_PLUGIN_ROOT}` is not set (e.g. running from a local checkout of the marketplace repo), fall back to `skills/incident-report/templates/` and `skills/incident-report/rules/` relative to the current working directory.

The shipped files (siblings of this SKILL.md) are:

- Templates: [templates/outage.md](templates/outage.md), [templates/security.md](templates/security.md), [templates/performance.md](templates/performance.md), [templates/data-loss.md](templates/data-loss.md), [templates/generic.md](templates/generic.md) — see [templates/README.md](templates/README.md) for the variable reference
- Rules: [rules/severity.md](rules/severity.md), [rules/escalation.md](rules/escalation.md), [rules/sla.md](rules/sla.md) — see [rules/README.md](rules/README.md) for ordering semantics

To save context, Read template **frontmatter only** (first ~6 lines) at this stage to build the registry; load a template's full body only after Step 3 selects it. Rules files are small — load them fully. Build an in-memory registry:

- **Templates registry:** keyed by `id` from frontmatter; store `name`, `incident_types`, `required_sections`, and the file path (full body loaded on selection).
- **Rules registry:** keyed by filename; store the full rule content for interpretation.

If either directory is empty or missing, warn the user and continue with built-in defaults.

### Step 2 — Gather Incident Information

Ask the user for the following (or accept from a prior `/log-correlation` output if available):

1. **What happened?** — A description of the symptoms observed.
2. **When did it start?** — Start time in UTC. Also ask: when was it resolved (if applicable)?
3. **What was the user impact?** — Number of users affected, features unavailable, error rates observed.
4. **What systems were involved?** — Services, databases, message queues, regions, third-party dependencies.
5. **What was the root cause?** — The confirmed or suspected cause. Accept "unknown — still investigating" if unresolved.
6. **What actions were taken?** — A timeline of response steps: who did what, and when. Format as `HH:MM UTC — action — who`.
7. **Is this incident resolved?** — Ongoing or post-incident (resolved)?

If the user provides a dump of log lines or a `/log-correlation` output, extract the above fields from it automatically and confirm with the user before proceeding.

### Step 3 — Classify the Incident

Apply the rules from `rules/severity.md` to determine severity (SEV1–SEV4). Show the classification logic:

1. List the severity criteria that match the user's description.
2. State the resulting severity level.
3. Show the severity label (e.g., `SEV1 — Critical / All-hands`).
4. Ask the user: "Does this classification look correct? Reply with the severity level to override, or press Enter to accept."

If the user overrides, record the override and the reason in the report's metadata.

### Step 4 — Select Template

Based on the incident type detected from the description, suggest the best matching template by matching keywords against each template's `incident_types` array.

Then show a numbered list of all available templates:

```
Available templates:
  1. Generic Incident Report (generic.md)
  2. Service Outage (outage.md)
  3. Security Incident (security.md)
  4. Performance Degradation (performance.md)
  5. Data Loss / Corruption (data-loss.md)
  [N. Any custom templates found in templates/]

Suggested: [N] — [template name] (matched on: [keywords])
Press Enter to accept, or enter a number to choose a different template.
You may also provide a file path to use a custom template not in this list.
```

### Step 5 — Fill the Template

Populate the selected template with all gathered information. Apply the following rules:

- Replace every `{{variable}}` placeholder with the corresponding value.
- For any section the user has not provided data for, insert a `[TODO: describe <field>]` placeholder. Never fabricate or assume data.
- For the `{{timeline}}` variable, format each action as a markdown table row: `| HH:MM UTC | action description | responder name |`.
- For the `{{action_items}}` variable, extract any follow-up tasks mentioned in the conversation and format them as table rows: `| N | action | [TODO: owner] | [TODO: due date] | Open |`.
- Generate `{{incident_id}}` as `INC-<YYYYMMDD>-<sequential-or-hash>`. Use today's date.
- Generate `{{duration}}` from start and end times. If unresolved, use "Ongoing".
- Populate `{{status}}` as either `Resolved` or `Ongoing`.

Check that all `required_sections` from the template frontmatter are filled. For any that are still `[TODO]`, warn the user: "The following required sections still need input: [list]. You can fill them now or complete them in the saved file."

### Step 6 — Apply Escalation Rules

Read `rules/escalation.md`. Based on the confirmed severity, determine the notification requirements. Populate the report's "Notifications Sent" section with:

- Who should have been/was notified
- The required notification timeline for this severity
- Placeholder rows for each notification channel, filled with actual data if the user provided it

### Step 7 — Apply SLA Rules

Read `rules/sla.md`. Based on the confirmed severity and the incident duration, calculate:

- **Time to acknowledge** — compare actual vs. SLA target
- **Time to mitigate** — compare actual vs. SLA target
- **Time to resolve** — compare actual vs. SLA target (if resolved)
- **Post-mortem due** — calculate due date from resolution time

Mark each metric as `MET` or `BREACHED`. If breached, state by how much. Populate the report's "SLA Status" section.

### Step 8 — Save the Report

> **Data handling:** Never include live credentials, tokens, session IDs, or victim PII in the report body — redact them (`[REDACTED]`) even if they appear in the logs or evidence the user provided. For **security-type incidents**, warn the user before saving: the report is stamped CONFIDENTIAL, and committing it to a shared repository may expose incident details to everyone with repo access. Offer to save outside the repo or to a restricted location instead.

1. Use Bash to create `docs/incidents/` if it does not exist: `mkdir -p docs/incidents`
2. Generate the filename: `INC-<YYYYMMDD>-<kebab-case-short-title>.md` (max 40 chars for the title slug).
3. Use Write to save the completed report to `docs/incidents/<filename>.md`.
4. Confirm the save path to the user.

### Step 9 — Offer Follow-Up Actions

After saving, present the user with these options:

```
Report saved to: docs/incidents/<filename>.md

Follow-up options:
  [C] Publish to Confluence  (requires Atlassian MCP tools)
  [J] Create Jira ticket for action items
  [A] Hand off to /agent-based-development workflow
  [N] Done — no further action needed
```

**If C (Confluence):** Check if Atlassian MCP tools are available. If yes, offer to create a new Confluence page with the report content in a space the user specifies. If MCP tools are not available, provide instructions for manual publishing.

**If J (Jira):** Extract all `[TODO: owner]` action items from the report. Offer to create one Jira ticket per action item, with summary, description, and severity-based priority. Use Atlassian MCP tools if available.

**If A (Agent workflow):** Create a handoff artifact at `handoffs/plans/` following the `/agent-based-development` artifact schema. Set `taskId` to the incident ID, `agent` to `planning`, `status` to `assigned`, and include the action items as task assignments.

---

## Output Format

After saving the report, display:

1. Incident ID and severity classification
2. Template used
3. SLA status summary (MET / BREACHED per metric)
4. File path where the report was saved
5. Any required sections still marked `[TODO]`
6. Follow-up action prompt
