---
title: Chat UI Workflow Interaction
description: Implement chat-based user interface with selectable options, progressive disclosure, and workflow guidance for discipline-specific operations including procurement, civil engineering, and other domain workflows
version: 1.0
frequency_percent: 80.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/shared/chat-ui-workflow-interaction
gigabrain_tags: disciplines, shared, chat-ui, workflow-interaction, progressive-disclosure, selectable-options, chat-thread, multi-discipline
openstinger_context: chat-interface, user-experience, workflow-guidance
last_updated: 2026-04-02
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_AI-NATIVE-CIVIL-ENGINEERING-PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
related_skills:
  - workflow-implementation
  - ai-team-coordination
  - dispatching-parallel-agents
---

# Chat UI Workflow Interaction

## Overview

Implement chat-based user interface workflows with selectable options, progressive disclosure, context-aware suggestions, and workflow guidance. This skill applies to all discipline-specific chat interactions where users select from options rather than typing free-form commands.

**Announce at start:** "I'm using the chat-ui-workflow-interaction skill for chat-based workflow implementation."

## When to Use This Skill

**Trigger Conditions:**
- Implementing chat thread UI with selectable option buttons
- Designing progressive disclosure workflows (multi-step wizards via chat)
- Creating context-aware action suggestions based on workflow state
- Building discipline-specific chatbots (procurement, civil engineering, etc.)

**Prerequisites:**
- Domain workflow specification available (e.g., procurement 5-phase flow, civil engineering workflows)
- UI component library accessible
- Agent capabilities defined for the discipline
- User roles and permissions established

## Chat UI Architecture

### Message Types

| Message Type | Purpose | Example |
|-------------|---------|---------|
| **Agent Prompt** | AI asks user for input | "What type of order would you like to create?" |
| **Option Group** | Selectable buttons for user | [Purchase Order] [Work Order] [Service Order] |
| **Confirmation** | Yes/No or approve/reject | [Approve] [Reject with Comments] [Request Revision] |
| **Status Update** | Progress indicator | "Phase 3 of 5 complete. Processing line items..." |
| **Data Display** | Formatted data in chat | Order summary table, supplier details |
| **Error/Warning** | Validation feedback | "Quantity exceeds BOQ by 12%. [Accept Anyway] [Revise]" |
| **Action Complete** | Task completion confirmation | "Order PO-2026-0142 created. [View Details] [Create Another]" |
| **Escalation** | HITL handoff notification | "This order requires manager approval. Routing to Procurement Manager..." |

### Progressive Disclosure Pattern

```
USER INITIALIZES → Agent presents context-appropriate options
  ↓
USER SELECTS OPTION → Agent gathers required inputs via sequential prompts
  ↓
ALL INPUTS COLLECTED → Agent presents summary with confirmation options
  ↓
USER CONFIRMS → Agent executes with progress updates
  ↓
EXECUTION COMPLETE → Agent presents next-action options or return to main menu
```

## Implementation Procedure

### Step 1: Workflow State Definition

Define the chat workflow states and transitions:

```json
{
  "workflow": "procurement_order_creation",
  "states": {
    "main_menu": {
      "prompt": "What would you like to do?",
      "options": [
        {"label": "Create New Order", "action": "create_order", "next_state": "order_type_selection"},
        {"label": "Track Existing Order", "action": "track_order", "next_state": "order_tracking"},
        {"label": "Supplier Directory", "action": "supplier_directory", "next_state": "supplier_search"},
        {"label": "Approval Queue", "action": "approval_queue", "next_state": "pending_approvals"}
      ]
    },
    "order_type_selection": {
      "prompt": "Select order type:",
      "options": [
        {"label": "🛒 Purchase Order", "action": "po", "next_state": "phase1_basic_info"},
        {"label": "🔧 Work Order", "action": "wo", "next_state": "phase1_basic_info"},
        {"label": "⚡ Service Order", "action": "so", "next_state": "phase1_basic_info"}
      ]
    },
    "phase1_basic_info": {
      "prompt": "Phase 1 of 5 — Basic Information",
      "fields": ["order_title", "department", "cost_center", "priority", "required_date"],
      "validation": ["required_fields", "valid_cost_center", "date_in_future"],
      "next_state": "phase2_template_selection"
    }
  }
}
```

### Step 2: Option Group Design

**Option Display Rules:**
- Maximum 5 options per message to avoid cognitive overload
- Use emojis or icons for quick visual scanning
- Group related options under section headers
- Include "Back" or "Main Menu" option for navigation escape

**Option Context Awareness:**
- Filter options based on user role and permissions
- Disable unavailable options with explanation ("Not available: No active orders")
- Highlight time-sensitive options ("⚠️ 3 orders awaiting approval")

### Step 3: Progressive Disclosure Implementation

**Per-Phase Chat Structure:**
```
Phase N of 5 — [Phase Name]
├── Prompt: "Please provide [specific information]"
├── Input: [text field / dropdown / file upload / date picker]
├── Validation: Real-time check
├── Feedback: "✓ Valid" or "✗ [error message + how to fix]"
├── Progress: [██████░░░░] 60% complete
└── Navigation: [← Back] [Next →] or [Submit]
```

### Step 4: HITL Integration in Chat

**Human Escalation Points:**
```
[When order value > threshold]
Agent: "This order value ($125,000) requires manager approval."
Options: [Continue to Manager] [Save Draft] [Cancel]

[When confidence is low]
Agent: "I'm not confident about the quantity for this item. BOQ shows 450 units but your input was 500."
Options: [Use BOQ: 450] [Keep My Input: 500] [Review Drawing] [Discuss with Engineer]

[When specialist input needed]
Agent: "This structural steel specification requires engineer confirmation."
Options: [Send to Structural Engineer] [Continue (Engineer Review Later)] [Pause]
```

### Step 5: Error Handling in Chat

| Error Type | Chat Response | Recovery Options |
|-----------|--------------|-----------------|
| **Validation Error** | "⚠️ [Field] can't be empty. Please enter a value." | [Retry] [Skip] |
| **Budget Exceeded** | "⚠️ Order total ($85k) exceeds budget ($70k) by $15k." | [Reduce Quantity] [Request Budget Increase] [Split Order] |
| **Approver Unavailable** | "⚠️ Approved approver is unavailable. Re-routing..." | [Select Alternate Approver] [Escalate to Director] [Wait] |
| **System Error** | "⚠️ Unable to reach supplier database. Please try again." | [Retry] [Switch to Offline Mode] [Contact IT] |

### Step 6: Multi-Discipline Chat Context

**Context Switching:**
When user switches between disciplines within the same chat thread:

```
User switches from Procurement to Civil Engineering:
Agent: "Switching context to Civil Engineering. Previous procurement session saved."
Options: [Start New Task] [Resume Saved Session] [Return to Main Menu]
```

**Context Memory:**
- Maintain session state across message turns
- Preserve context when switching between related tasks
- Offer to resume interrupted workflows

## Success Criteria

- [ ] All workflow states defined with transitions
- [ ] Option groups limited to 5 or fewer per message
- [ ] Progressive disclosure implemented per workflow specification
- [ ] HITL escalation points configured with appropriate options
- [ ] Error handling covers all validation failure modes
- [ ] Navigation includes escape hatches (Back, Main Menu)
- [ ] User role filtering applied to available options
- [ ] Session state persisted across chat interactions

## Common Pitfalls

1. **Too Many Options** — More than 5 options overwhelms users. Group into nested menus instead.
2. **No Escape Hatch** — Always provide Back and Main Menu options to prevent user being trapped.
3. **Lost Context** — When users switch tasks, preserve session state so they can resume.
4. **Missing Validation Feedback** — Show immediate feedback on input errors, not after submission.
5. **Role-Agnostic Options** — Filter options based on user permissions; don't show actions they can't perform.
6. **Ambiguous Option Labels** — Use clear, action-oriented labels. "Create Purchase Order" is better than "PO".

## Cross-References

### Related Skills
- `workflow-implementation` — Workflow design patterns
- `procurement-order-management` — Procurement-specific workflow
- `procurement-5phase-order-creation` — 5-phase wizard flow

### Related Agents
- Procurement Officer — Primary user of procurement chat flows
- Civil Engineer — Primary user of civil engineering chat flows
- QualityForge Reviewer — Reviews workflow implementations