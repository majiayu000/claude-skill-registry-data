---
name: onboard-customer
description: Create customer onboarding checklist from template with customer details
auto_trigger: true
trigger_keywords:
  - "onboard customer"
  - "onboard new customer"
  - "create customer onboarding"
  - "customer onboarding checklist"
  - "new customer setup"
  - "new client setup"
  - "client onboarding checklist"
  - "start customer onboarding"
allowed-tools: Task, Read, Write, mcp__flywheel__get_note_metadata, mcp__flywheel__search_notes, mcp__flywheel__get_folder_structure
---

# Onboard Customer

Create a new customer onboarding checklist from template, with customer details pre-filled.

## Trigger Detection

Activate when user:
- Has a new customer to onboard
- Needs to create an onboarding checklist
- Wants to start customer setup process

## Examples

- "Onboard Acme Corp"
- "New customer: TechStart Inc"
- "Create onboarding checklist for Big Enterprise"
- "Start onboarding for [[New Client]]"

## Process

1. **Parse Customer Name**
   - Extract customer name from request
   - If unclear, ask for confirmation

2. **Delegate to Agent**
   ```
   Task(
       subagent_type="customer-onboarding-agent",
       description="Onboard customer",
       prompt="Create onboarding checklist for [Customer Name]"
   )
   ```

3. **Confirm Creation**
   - Show created note path
   - Link to related resources

## Customization

The onboarding template can be customized:
- Edit `templates/customer-onboarding.md` for your workflow
- Add/remove checklist phases
- Include company-specific steps

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | ✅ | Agent reads template first |
| 2. File Exists Check | ✅ | Agent checks template exists |
| 3. Chain Validation | N/A | Single delegation |
| 4. Mutation Confirm | ✅ | User confirms before creation |
| 5. MCP Health | N/A | Agent handles |
| 6. Post Validation | ✅ | Agent verifies creation |
