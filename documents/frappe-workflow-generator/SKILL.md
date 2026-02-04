---
name: frappe-workflow-generator
description: Generate Frappe Workflows for document state management and approvals. Use when creating approval workflows, state transitions, or multi-step document processes.
---

# Frappe Workflow Generator

Generate production-ready Frappe Workflows for document state management, approvals, and business process automation.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to create approval workflows
- User needs document state transitions
- User requests multi-step approval processes
- User mentions workflows, approvals, or document states
- User wants role-based approval routing
- User needs to implement document lifecycle management

## Capabilities

### 1. Workflow JSON Generation

**Basic Approval Workflow:**
```json
{
  "name": "Sales Invoice Approval",
  "document_type": "Sales Invoice",
  "is_active": 1,
  "workflow_state_field": "workflow_state",
  "states": [
    {
      "state": "Draft",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "update_field": "status",
      "update_value": "Draft"
    },
    {
      "state": "Pending Approval",
      "doc_status": "0",
      "allow_edit": "Sales Manager",
      "update_field": "status",
      "update_value": "Pending"
    },
    {
      "state": "Approved",
      "doc_status": "1",
      "update_field": "status",
      "update_value": "Approved"
    },
    {
      "state": "Rejected",
      "doc_status": "2",
      "update_field": "status",
      "update_value": "Rejected"
    }
  ],
  "transitions": [
    {
      "state": "Draft",
      "action": "Submit for Approval",
      "next_state": "Pending Approval",
      "allowed": "Sales User",
      "allow_self_approval": 0
    },
    {
      "state": "Pending Approval",
      "action": "Approve",
      "next_state": "Approved",
      "allowed": "Sales Manager"
    },
    {
      "state": "Pending Approval",
      "action": "Reject",
      "next_state": "Rejected",
      "allowed": "Sales Manager"
    },
    {
      "state": "Rejected",
      "action": "Revise",
      "next_state": "Draft",
      "allowed": "Sales User"
    }
  ]
}
```

### 2. Conditional Transitions

**Workflow with Amount-Based Routing:**
```json
{
  "transitions": [
    {
      "state": "Draft",
      "action": "Submit",
      "next_state": "Pending L1 Approval",
      "allowed": "Sales User",
      "condition": "doc.grand_total <= 10000"
    },
    {
      "state": "Draft",
      "action": "Submit",
      "next_state": "Pending L2 Approval",
      "allowed": "Sales User",
      "condition": "doc.grand_total > 10000 && doc.grand_total <= 50000"
    },
    {
      "state": "Draft",
      "action": "Submit",
      "next_state": "Pending Director Approval",
      "allowed": "Sales User",
      "condition": "doc.grand_total > 50000"
    }
  ]
}
```

## References

**Frappe Workflow Core:**
- Workflow: https://github.com/frappe/frappe/blob/develop/frappe/workflow/doctype/workflow/workflow.py
- Workflow State: https://github.com/frappe/frappe/blob/develop/frappe/workflow/doctype/workflow_state/workflow_state.py

**Official Documentation:**
- Workflows: https://frappeframework.com/docs/user/en/desk/workflows
