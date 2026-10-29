---
name: mcp-access-guide
description: Use when someone asks how MCP connects Claude to company systems, wants to understand what data or tools Claude can access, asks to onboard to connectors, wants to check connector availability or permissions, or asks what to do when access is missing. Triggers include "how does MCP work", "what can Claude access", "explain our connectors", "onboard me to MCP", "do I have access to X".
---

## What This Skill Does

Teaches beginners how MCP (Model Context Protocol) connects Claude to real company systems, using one interactive, explorable diagram instead of a linear lecture. It verifies connector availability where possible, explains accessible data, permissions, and ownership, and guides safe escalation when access is missing — without ever exposing secrets or modifying configuration.

This is a **teaching and diagnostic** skill. It never changes settings, grants access, or handles credentials.

## Hard Rules (never break these)

1. **Never store or display passwords, tokens, connection strings, or other secrets.** Not even examples with placeholder-looking values that could be mistaken for real ones.
2. **Never modify configuration, connections, or permissions.** This skill only explains and diagnoses.
3. **Never claim a connector is verified without checking.** Every connector status shown must be labeled exactly one of:
   - **"Live verified"** — confirmed by inspecting Claude's actual available/connected tools in this session, just now.
   - **"Registry verified"** — confirmed by reading `references/connector-registry.md` and its `Verification date` / `Evidence source` fields.
   - **"Demo only — Needs confirmation"** — simulated or illustrative data used to teach the concept. This is the default for anything not freshly checked.
   - **"Installed — Not authenticated"** — the connector is detected or configured, but authentication is incomplete, so it cannot yet be treated as usable or Live verified.
4. **Simulated connectors and sample data must be clearly labeled as such** (e.g., "Example CRM Connector (demo)"). Never let demo data look like a real result.
5. If the registry has no entry for a connector, or an entry is stale/incomplete, treat it as "Needs confirmation" rather than filling gaps with assumptions.

## Step-by-Step Workflow

### Step 1: Check live tools
At the start of the conversation, check what MCP tools are actually available in this session (look at the tool list / use `tool_search` if connectors may be deferred). This becomes the "Live verified" data source. If a connector appears in the tool list but a call to it fails or reports an authentication/authorization error, label it "Installed — Not authenticated" rather than "Live verified" — it's present but not yet usable.

### Step 2: Read the registry
Read `references/connector-registry.md` for anything live inspection can't tell you: system owner, escalation contact, prohibited actions, permission level detail. Note each entry's `Verification date` — treat entries older than 90 days as stale and label them "Needs confirmation" instead of "Registry verified."

### Step 3: Build the interactive board (one Artifact)
Create a single React or HTML Artifact containing:

**A. Layered workflow diagram** (top level, always visible)
- Nodes: User → Claude → MCP Server → Company System → Data
- Each node is clickable and expands a plain-language explanation of that layer (e.g., clicking "MCP Server" explains it's a translator that lets Claude call a company system's API without Claude ever holding credentials).
- Beginners should be able to explore non-linearly — clicking any node in any order.

**B. Connector panel** (collapsed by default)
- A list/grid of connectors (real ones from Step 1, plus clearly labeled demo connectors from the registry's example entry if useful for teaching).
- Selecting a connector expands a detail card showing: verified availability (with the correct label from the Hard Rules), accessible data, permission level, prohibited actions, system owner, escalation contact, and evidence source.
- Collapsed-by-default keeps beginners from being overwhelmed; only the selected connector's details show.

**C. Escalation guidance**
- When a connector shows missing/insufficient access, display generic guidance: what kind of role usually grants access, and to check the connector's `Escalation contact` field if the registry has one. If the registry doesn't have a contact, say so plainly rather than inventing one.

### Step 4: Walk through it conversationally
Don't just hand over the artifact and stop. Introduce it, invite the user to click around, and check in via `AskUserQuestion`: "Want me to walk through what a specific connector can and can't do?" — options **Yes, walk me through one (Recommended)** / **No thanks, I'll explore it myself**. If yes and 4 or fewer connectors are shown, offer them by name as the question's options (grounded in what Step 1/2 actually found); if more than 4 exist, ask which one as free text instead, since the board already lists them. Keep this conversational and paced for a beginner, not a wall of text.

### Step 5: If asked to check a specific connector
Re-run Step 1 (live check) before answering, and cross-reference the registry. Never answer a "do I have access to X" question from memory alone.

## Output Format

- One Artifact: interactive board per Step 3.
- Inline conversation: framing, explanations, and check-ins around it.
- Every connector status string must literally read one of: `Live verified`, `Registry verified`, `Demo only — Needs confirmation`, or `Installed — Not authenticated`.

## Notes / Edge Cases

- If no MCP tools are connected at all, say so plainly and use only clearly-labeled demo connectors to teach the concept.
- If the registry file doesn't exist or is empty, still build the workflow diagram (Step 3A) — just show all connector details as "Needs confirmation" and suggest the user or an admin populate `references/connector-registry.md`.
- Don't infer permission levels, owners, or prohibited actions from a connector's name or general reputation — those must come from Step 1 or Step 2, not assumption.
- Keep the tone beginner-friendly: avoid jargon without explanation on first use (MCP, connector, permission scope, etc.).
- Clickable-question convention: Step 4's walkthrough check-in uses `AskUserQuestion` (with the actual connector names offered as options when 4 or fewer exist). A specific connector question in Step 5, when the user asks it themselves, stays free text.
