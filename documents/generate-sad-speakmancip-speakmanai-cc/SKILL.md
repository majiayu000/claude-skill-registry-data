---
name: generate-sad
description: Run a SPEAKMAN.AI architecture workflow and generate a Solution Architecture Document locally
---

# generate-sad - SPEAKMAN.AI Local SAD Generator

You are running the SPEAKMAN.AI SAD Generator. You will orchestrate a full SPEAKMAN.AI MCP session and produce a locally-generated Solution Architecture Document (SAD) from the agent outputs.

Follow every step below exactly. Do not generate the SAD content yourself - it is built in Step 5 from real agent outputs.

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

> "Do you have an existing SPEAKMAN.AI session ID you want to use? If so, paste it and I'll skip straight to generating the document. Otherwise, press Enter and I'll run a new session."

- If a session ID is provided: set `session_id` to that value and **skip to Step 4**.
- If no session ID is provided: continue to Step 1.

---

## Step 1 - Collect Business Input

Ask the user:

> "What do you want to build? Describe it in a few sentences - or give me any of the following and I'll extract the description from it:
> - Paste text directly
> - A file path (.md, .pdf, .txt, .docx)
> - A directory to scan for relevant documents
> - A URL or internal wiki link
> - A connected MCP resource (Google Drive folder, Confluence space, SharePoint library)
> - RAG search results or document links
> - Terraform files (.tf or terraform.tfstate) - I'll extract your tech stack from these"

Read and parse whatever is provided. Extract:
- Business goal and problem being solved
- Target scale and success metrics (look for numbers - transactions/month, users, uptime targets)
- Key user types or stakeholders mentioned
- Regulatory or compliance requirements (PCI-DSS, GDPR, HIPAA, ISO 27001, etc.)
- Preferred or existing technology stack

Store this as **BUSINESS_CONTEXT**.

---

## Step 2 - Collect Capabilities Source (Reference Only)

Ask the user:

> "Do you have any additional context for your current or planned technology capabilities? This helps build a richer architecture. You can provide:
> - An existing systems inventory (any format)
> - Terraform files (.tf / terraform.tfstate) - I'll map resources to capabilities
> - Architecture documents, RFPs, or technical briefs
> - A connected doc store, Google Drive folder, or RAG search
> - Or press Enter to use the business description only"

**Store the file path, text, or reference as `CAPABILITIES_SOURCE`. Do not parse it yet.**

Parsing happens at Step 3b, once the live schema arrives from the workflow. Loading and interpreting capabilities before the schema is available wastes context and may not match what the workflow expects.

---

## Step 3 - Run SPEAKMAN.AI Session

### 3a - Start session

Call `start_session`:
- `workflow_id`: `MCP_SOLUTION_ARCHITECTURE_V1`
- `title`: Short title derived from the business description (max 60 chars)
- `description`: Business description from **BUSINESS_CONTEXT only** (max 8000 chars - keep goal, scale, personas, compliance, and key constraints). Do NOT include technology stack or capabilities detail - that belongs only in Step 3b.

Poll every 30 seconds until `status = AWAITING_INPUT`.

Do not call the poll tool again and again with the same arguments. Some clients block a third identical call as a loop. If the status has not changed, tell the user what you are waiting for and wait before you poll again. When the session is paused for a review or for your own answer, do what the pause asks instead of polling.

### 3b - Build and submit capabilities

When AWAITING_INPUT arrives, the payload contains `input_required.prompt`, `input_required.schema`, and `input_required.context`.

On every `submit_response` you make in this workflow, also pass `executed_by`: the name of your tool and your model, for example `Claude Code, claude-opus-5-5`. Say what you actually are and do not guess a model name you cannot see. The engine records it with the output, so the run record shows who did the work.

Now read and parse `CAPABILITIES_SOURCE` (from Step 2). Extract:
- Current/existing technology systems and their deployment states (Current)
- Planned or proposed tools (Proposed)
- Legacy systems being replaced (Legacy)
- Any migration strategies mentioned

If Terraform files are provided:
- Parse `resource` blocks to identify AWS/Azure/GCP services → map to technology capability names
- Use `terraform.tfstate` as ground truth for Current state; `.tf` files for Proposed
- Infer migration_strategy from context (rename, replace, lift-and-shift)

1. Read the schema from `input_required.schema` - this defines exactly what to build.
2. Display a summary table to the user showing what the schema expects:

| Field | Description |
|---|---|
| name | Capability name |
| type | Business or Technology |
| deployments[].tool_name | Tool or platform name |
| deployments[].state | Current / Proposed / Legacy |
| deployments[].migration_strategy | N/A, Replace, Replatform, etc. |

3. Build the capabilities JSON array from FULL_CONTEXT, guided by the schema and `input_required.prompt`. Aim for 15-25 capabilities covering the full scope. Include both Business capabilities (functions, processes) and Technology capabilities (tools, platforms, APIs, infrastructure).

4. Present a draft table to the user:

| # | Name | Type | Tool | State |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Say: "Here are the capabilities I've extracted - confirm to submit, or describe any changes."

5. On user confirmation, call `submit_response(session_id, <capabilities JSON array>)`.

Poll every 60 seconds until `status = COMPLETED`. This takes 10-15 minutes.

---

## Step 4 - Download Supporting Agent Outputs

Call `get_outputs(session_id)` to get the manifest.

Then call `get_output` for these agents **only** - fetch in parallel where possible:

| Agent ID | Contains |
|---|---|
| `MCP_BUSINESS_CONTEXT_CLARIFIER_V1` | Project brief, business context |
| `MCP_BUSINESS_ANALYST_V1` | Requirements, personas, process flows, data entities |
| `MCP_BUSINESS_APPLICATION_ARCHITECT_V1` | Component catalog, data flows, ADRs |
| `MCP_TECHNICAL_SOLUTION_ARCHITECT_V1` | Infrastructure decisions, deployment strategy, ADRs |
| `MCP_COMPLIANCE_OFFICER_V2` | Traceability matrix, violations, compliance score |
| `MCP_TECHNICAL_VISUALIZATION_SPECIALIST_V1` | Raw Mermaid diagrams |

> **Do NOT download `MCP_TECHNICAL_WRITER_V2`.** The local prompt replaces it.

Create the output directory: `outputs/YYYY-MM-DD_{slug}/raw/` where slug is a lowercase-hyphenated version of the session title and YYYY-MM-DD is today's date.

**Save each agent output using the `Write` tool directly** - the `content` field returned by `get_output` is already in context. Do not use bash scripts or Python to write files; the `Write` tool handles large content natively and is reliable across all platforms.

Use the stable filename mapping below (not the raw `agent_id`):

| Agent ID | Save as |
|---|---|
| `MCP_BUSINESS_CONTEXT_CLARIFIER_V1` | `business_context_clarifier.txt` |
| `MCP_BUSINESS_ANALYST_V1` | `business_analyst.txt` |
| `MCP_BUSINESS_APPLICATION_ARCHITECT_V1` | `business_application_architect.txt` |
| `MCP_TECHNICAL_SOLUTION_ARCHITECT_V1` | `technical_solution_architect.txt` |
| `MCP_COMPLIANCE_OFFICER_V2` | `compliance_officer.txt` |
| `MCP_TECHNICAL_VISUALIZATION_SPECIALIST_V1` | `visualization_specialist.txt` |

---

## Step 5 - Generate Local SAD

Using the downloaded raw agent outputs saved in `outputs/YYYY-MM-DD_{slug}/raw/`, follow the instructions in `{ASSET_DIR}/prompts/sad_agent_prompt.md` exactly to generate the SAD.

Key rules for this step:
- Read all 6 agent output files from the raw directory
- Follow the synthesis and template instructions in `sad_agent_prompt.md`
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
python "{ASSET_DIR}/scripts/render_html.py" "outputs/YYYY-MM-DD_{slug}/{slug}.md" "outputs/YYYY-MM-DD_{slug}/{slug}.html" --title "<the document's title>" --subtitle "Solution Architecture Document - {today's date}"
```

The script uses only the standard library, and its output is the same as the `render_document` tool's. Use `python3` if `python` is not found. Do not write your own renderer.

**If you cannot run code**, call the `render_document` MCP tool with `markdown` (the full content of the
Markdown file), `title` (the first `#` heading) and `subtitle` (`"Solution Architecture Document - {today's date}"`). It returns
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
Session ID   : {session_id}
Credits used : {session_cost}   (only if a tool reported a cost; leave this line out otherwise)
Compliance   : {score}/10 - {status}
Outputs
  Markdown   : outputs/{slug}/{slug}.md
  HTML       : outputs/{slug}/{slug}.html   (only if requested)
```

Then say: "Review `{slug}.md` (and `{slug}.html` if you asked for it): this is your draft SAD, ready for architect review before ARB submission. I can also make an HTML version, which you can print to PDF, if you want one."
