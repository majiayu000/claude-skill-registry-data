---
name: crm-operations
description: Use when adding or modifying CRM-related tools (create_crm_process, update_crm_status), the CRM client interface, or the CRM mock. Covers Customer/Lead/Task object shapes per spec.
---

# CRM Operations skill

## When to invoke

- Touching anything under `src/integrations/crm/`
- Touching tools `create_crm_process` or `update_crm_status`
- Designing CRM data flows
- Writing tests for CRM operations

## Object shapes (from spec)

### Customer
```ts
{
  customer_id: string;
  full_name: string;
  phone: string;
  email: string;
  status: 'new' | 'active' | 'pending_docs' | 'closed' | ...;
  assigned_advisor: string;
  lead_source: string;
  documents_status: Record<string, 'received' | 'missing' | 'rejected'>;
}
```

### Lead
```ts
{
  lead_id: string;
  source: string;            // Facebook / Google / referral / ...
  priority_score: number;    // 1-10
  intent_level: 'cold' | 'warm' | 'hot';
  meeting_booked: boolean;
}
```

### Task
```ts
{
  task_id: string;
  assigned_to: string;
  due_date: string;          // ISO date
  task_type: string;
  completion_status: 'pending' | 'in_progress' | 'completed';
}
```

## Patterns

- **Interface first** — `src/integrations/crm/client.ts` defines the contract; mock and (future) real provider both implement it
- **No CRM-specific shapes leak past the integration boundary** — always go through the interface
- **Idempotent writes** — `create_crm_process` must be safe to retry (Make.com may resend webhook on failure)
- **Errors are typed** — `CrmNotFoundError`, `CrmDuplicateError`, `CrmValidationError`

## Error handling (from spec)

If CRM fails: retry 3 times → log failure → notify operations agent
