---
name: generate-compliance-report
description: Run a SPEAKMAN.AI compliance workflow and generate a Compliance Assessment Report locally
---

# generate-compliance-report - SPEAKMAN.AI Compliance Assessment

You are running the SPEAKMAN.AI Compliance Assessment. You will orchestrate a full SPEAKMAN.AI MCP session and produce a locally-generated Compliance Assessment Report from the agent outputs.

Follow every step below exactly. Do not generate the report content yourself - it is built in Step 5 from real agent outputs.

---

## Before You Begin - Resolve Asset Directory

Determine the absolute path to the SPEAKMAN.AI asset directory by running:

```bash
echo "$HOME/.claude/speakmanai-cc"
```

Store the result as **ASSET_DIR**. Use this variable everywhere `~/.claude/speakmanai-cc` appears below - never use `~` in file read operations, as it does not expand outside of a shell context.

---

## Step 0 - Check for Existing Session

Before collecting any input, ask the user:

> "Do you have an existing SPEAKMAN.AI session ID you want to use? If so, paste it and I'll skip straight to generating the report. Otherwise, press Enter and I'll run a new session."

- If a session ID is provided: set `session_id` to that value and **skip to Step 4**.
- If no session ID is provided: continue to Step 1.

---

## Step 1 - Collect Assessment Scope

Ask the user:

> "What system, process, or organisation are you assessing? Describe it in a few sentences - or give me any of the following and I'll extract the context from it:
> - Paste text directly
> - A file path (.md, .pdf, .txt, .docx)
> - A directory to scan for relevant documents
> - A URL or internal wiki link
> - A connected MCP resource (Google Drive folder, Confluence space, SharePoint library)
> - An existing architecture document or SAD
> - A data flow or system inventory"

Read and parse whatever is provided. Extract:
- Name and purpose of the system or process being assessed
- Data classifications in scope (PII, PHI, PCI, financial, etc.)
- Hosting model (cloud, on-premise, hybrid) and key infrastructure
- User types and access patterns
- Any known existing controls or compliance certifications
- Regulatory context (geography, sector, existing obligations)

Store this as **SCOPE_CONTEXT**.

---

## Step 2 - Identify Regulatory Framework

Ask the user:

> "Which regulatory framework or standard are you assessing against? Common options:
> - GDPR (EU data protection)
> - PIPEDA / Law 25 (Canadian privacy)
> - PCI-DSS (payment card)
> - SOC 2 Type II (trust service criteria)
> - ISO 27001 (information security)
> - HIPAA (US healthcare)
> - NIST CSF (cybersecurity framework)
> - Or describe a custom / internal framework
>
> You can specify more than one.
>
> Do you also have an existing controls inventory (spreadsheet, CSV, text file, or path)? If so, provide it and I'll use it when building the controls list - or press Enter to derive a baseline from the framework."

Record the selected framework(s) as **FRAMEWORKS**. If a controls inventory is provided, store the file path or reference as **CONTROLS_SOURCE**. **Do not parse it yet** - parsing happens at Step 3b once the live schema is available.

Merge SCOPE_CONTEXT + FRAMEWORKS as **FULL_CONTEXT**.

---

## Step 3 - Run SPEAKMAN.AI Session

### 3a - Start session

Call `start_session`:
- `workflow_id`: `MCP_COMPLIANCE_ASSESSMENT_V1`
- `title`: Short title derived from the system name and framework (max 60 chars, e.g. "Compliance Assessment - PaymentHub / PCI-DSS")
- `description`: Assessment scope and framework from FULL_CONTEXT (max 3000 chars - trim if needed, keep system purpose, data classifications, frameworks, and hosting model)

Poll every 30 seconds until `status = AWAITING_INPUT`.

Do not call the poll tool again and again with the same arguments. Some clients block a third identical call as a loop. If the status has not changed, tell the user what you are waiting for and wait before you poll again. When the session is paused for a review or for your own answer, do what the pause asks instead of polling.

### 3b - Build and submit controls inventory

When AWAITING_INPUT arrives, the payload contains `input_required.prompt`, `input_required.schema`, and `input_required.context`.

On every `submit_response` you make in this workflow, also pass `executed_by`: the name of your tool and your model, for example `Claude Code, claude-opus-5-5`. Say what you actually are and do not guess a model name you cannot see. The engine records it with the output, so the run record shows who did the work.

If **CONTROLS_SOURCE** was provided in Step 2, read and parse it now against the live schema.

1. Read the schema from `input_required.schema` - this defines exactly what to build.
2. Display a summary table to the user showing what the schema expects:

| Field | Description |
|---|---|
| control_id | Your internal control reference or framework control ID |
| domain | Control domain (e.g. Access Control, Cryptography, Incident Response) |
| description | What the control does |
| status | Implemented / Partial / Not Implemented / Not Applicable |
| evidence | Brief description of evidence available (or "None") |

3. Build the controls inventory JSON array from FULL_CONTEXT, guided by the schema and `input_required.prompt`. Aim for 20-40 controls covering the full framework scope. If the user has no inventory, derive a baseline set from the framework requirements and mark each as `Not Implemented` pending review.

4. Present a draft table to the user:

| # | Domain | Control | Status | Evidence |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Say: "Here is the controls inventory I've built - confirm to submit, or describe any changes."

5. On user confirmation, call `submit_response(session_id, <controls JSON array>)`.

Poll every 60 seconds until `status = COMPLETED`. This takes 10-15 minutes.

---

## Step 4 - Download Agent Outputs

Call `get_outputs(session_id)` to get the manifest.

Then call `get_output` for these agents **only** - fetch in parallel where possible:

| Agent ID | Contains |
|---|---|
| `MCP_COMPLIANCE_SCOPE_CLARIFIER_V1` | Confirmed assessment scope, data classifications, system context |
| `MCP_RISK_ANALYST_V1` | Risk scoring by domain, likelihood and impact ratings, residual risk |
| `MCP_COMPLIANCE_OFFICER_V1` | Control-by-control assessment, gap identification, severity ratings |
| `MCP_REMEDIATION_ADVISOR_V1` | Prioritised remediation recommendations, effort and impact estimates |

> **Do NOT download `MCP_COMPLIANCE_REPORT_WRITER_V1`.** The local prompt replaces it.

Create the output directory: `outputs/YYYY-MM-DD_{slug}/raw/` where slug is a lowercase-hyphenated version of the session title and YYYY-MM-DD is today's date.

**Save each agent output using the `Write` tool directly** - the `content` field returned by `get_output` is already in context. Do not use bash scripts or Python to write files; the `Write` tool handles large content natively and is reliable across all platforms.

Use the stable filename mapping below (not the raw `agent_id`):

| Agent ID | Save as |
|---|---|
| `MCP_COMPLIANCE_SCOPE_CLARIFIER_V1` | `compliance_scope_clarifier.txt` |
| `MCP_RISK_ANALYST_V1` | `risk_analyst.txt` |
| `MCP_COMPLIANCE_OFFICER_V1` | `compliance_officer.txt` |
| `MCP_REMEDIATION_ADVISOR_V1` | `remediation_advisor.txt` |

---

## Step 5 - Generate Local Compliance Report

Using the downloaded raw agent outputs saved in `outputs/YYYY-MM-DD_{slug}/raw/`, follow the instructions in `{ASSET_DIR}/prompts/compliance_agent_prompt.md` exactly to generate the report.

Key rules for this step:
- Read all 4 agent output files from the raw directory
- Follow the synthesis and template instructions in `compliance_agent_prompt.md`
- **Change Log date**: use today's actual date - do NOT rely on LLM knowledge for this
- Save the completed Markdown to: `outputs/YYYY-MM-DD_{slug}/{slug}.md`

---

## Step 6 - Render HTML (only if asked for)

HTML is optional, and only on request. The Markdown file from Step 5 is the deliverable. Do this step only if
the user asked for an HTML version (or a PDF, which is printed from the HTML). Otherwise skip to Step 7 and
offer the HTML in your report.

**If you can run Python** (Claude Code and the Claude app can), render the HTML locally. The document
never passes through you, which saves a lot of usage allowance on a large document:

```
python "{ASSET_DIR}/scripts/render_html.py" "outputs/YYYY-MM-DD_{slug}/{slug}.md" "outputs/YYYY-MM-DD_{slug}/{slug}.html" --title "<the document's title>" --subtitle "Compliance Assessment Report - {frameworks} - {today's date}"
```

The script uses only the standard library, and its output is the same as the `render_document` tool's. Use `python3` if `python` is not found. Do not write your own renderer.

**If you cannot run code**, call the `render_document` MCP tool with `markdown` (the full content of the
Markdown file), `title` (the first `#` heading) and `subtitle` (`"Compliance Assessment Report - {frameworks} - {today's date}"`). It returns
`{"html": "<full HTML document>"}`: save that string to `outputs/YYYY-MM-DD_{slug}/{slug}.html`.
The HTML comes back as one tool result, about 1.3 times the size of the Markdown, and a large result may
be cut off or refused by your client. If the Markdown is over about 40,000 characters, skip the HTML,
deliver the Markdown file, and tell the user the HTML version was left out because the document is large.

### Step 6b - Custom Branding (optional)

If the user wants their own branding instead of the SPEAKMAN.AI default, edit the saved HTML
file directly: swap the `<img src="...">` in the `.doc-header` for their logo, and adjust the
header/accent colors in the `<style>` block if they gave you a brand color. This is a plain text
edit - no template directory involved.

---

## Step 7 - Report

Report the following to the user:

```
Session ID        : {session_id}
Credits used      : {session_cost}   (only if a tool reported a cost; leave this line out otherwise)
Framework(s)      : {frameworks}
Overall risk      : {risk_level} - {score}/10
Critical gaps     : {critical_gap_count}
Outputs
  Markdown        : outputs/{slug}/{slug}.md
  HTML            : outputs/{slug}/{slug}.html   (only if requested)
```

Then say: "Review `{slug}.md` (and `{slug}.html` if you asked for it): this is your draft Compliance Assessment Report, ready for review before submission or remediation planning. I can also make an HTML version, which you can print to PDF, if you want one."
