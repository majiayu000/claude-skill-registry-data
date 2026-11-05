---
name: breadboarding-workflow
description: Map UI elements and code relationships (affordances).
phase: 5 (Complexity)
role: Lead
---

# Breadboarding Workflow

**Role Constraints:** Lead (Write/Bash access allowed).
**File Access:** Do NOT use literal placeholders for file paths. Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`.

## Methodology

Transform a workflow description or shaped pitch into affordance tables showing UI and Code affordances with their wiring. 

### 1. Locate Context
Use the `glob` tool to find the active feature directory inside `.jonggrang/.output/features/`. Use the `read` tool to read the `pitch.md` or requirements document located there.

### 2. Identify Affordances
Break down the shaped solution into three components:
1. **Places:** Where the user is (e.g., "Dashboard", "Settings Page").
2. **Affordances:** What the user can act on (buttons, fields, readable data).
3. **Connection Lines:** Where an action takes the user next.

### 3. Draft the Breadboard
Create a text-based breadboard representation. Use a simple format mapping Places to their Affordances and Connections. 
Example:
Place: Invoice View
- Read: Invoice details, status
- Action: Click "Pay Now" -> takes to Place: Payment Gateway

### 4. Save the Artifact
Use the `write` tool to save the breadboarding artifact as `breadboard.md` inside the active feature directory.

## Completion Signal
When the breadboarding is saved and the workflow is mapped, output exactly:

BREADBOARDING_COMPLETE
