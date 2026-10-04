---
name: add-workflow-trigger
description: Create an automation workflow trigger that fires on entity events (lead created, deal stage changed, etc.) and executes a sequence of actions. Use when building the automation engine.
---

# add-workflow-trigger

Creates a new trigger type for the workflow automation engine. When the trigger condition is met, the engine starts a workflow run that executes configured actions in sequence.

## Inputs to gather

- **Trigger name** — e.g., `lead_created`, `deal_stage_won`, `appointment_missed`, `lead_score_above`
- **Entity type** — which table/entity fires this trigger (leads, deals, appointments)
- **Condition** — when does it fire (on create, on field change, on schedule)
- **Available context** — what data is passed to workflow actions (entityId, userId, orgId, changed fields)

## Steps

1. **Register the trigger type** in `apps/api/libs/workflow-engine.ts`:
   ```typescript
   export const TRIGGER_TYPES = {
     lead_created: { entity: "leads", event: "create", label: "عميل جديد" },
     deal_stage_changed: { entity: "deals", event: "update", field: "stage", label: "تغيير مرحلة الصفقة" },
   } as const;
   ```

2. **Add the emit point** in the relevant API route. After the mutation succeeds:
   ```typescript
   await workflowEngine.checkTriggers("lead_created", { entityId: lead.id, orgId });
   ```

3. **Implement `checkTriggers`** in the workflow engine:
   - Query `workflows` table: active workflows with matching trigger type and orgId
   - For each match, create a `workflow_runs` record with status `PENDING`
   - Enqueue the first step for execution

4. **Add trigger to the builder UI** palette:
   - Node component with trigger icon + label
   - Config panel: condition parameters (e.g., "stage equals WON", "score above 70")

5. **Test with a sample workflow:**
   - Create workflow: trigger = `lead_created` → action = log to console
   - Create a lead via API
   - Verify workflow_runs record created and step executed

## Verification checklist

- [ ] Trigger fires on the correct mutation
- [ ] Only active workflows with matching orgId are triggered
- [ ] Workflow run is created with correct entityId and context
- [ ] Condition filtering works (e.g., only fires when score > 70)
- [ ] Does not fire on unrelated mutations
- [ ] `/typecheck` passes

## Anti-patterns

- Don't execute workflow steps synchronously in the API request — enqueue for async processing
- Don't trigger workflows for system/admin operations — only user-initiated mutations
- Don't allow infinite loops — max 50 steps per workflow, max 10 active runs per entity
- Don't skip org isolation — workflow can only access data within its own org
