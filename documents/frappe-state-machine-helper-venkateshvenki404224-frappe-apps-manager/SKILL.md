---
name: frappe-state-machine-helper
description: Generate state machine logic for Frappe DocTypes. Use when implementing complex status workflows, state transitions, or document lifecycle management.
---

# Frappe State Machine Helper

Generate state machine logic for managing complex document states and transitions in Frappe DocTypes.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to implement document status management
- User needs state transition logic
- User mentions state machine, status workflow, or document lifecycle
- User wants to validate state transitions
- User needs state-dependent behavior

## Capabilities

### 1. State Transition Logic

**Order Status State Machine:**
```python
class SalesOrder(Document):
    def validate(self):
        self.validate_state_transition()

    def validate_state_transition(self):
        """Validate allowed state transitions"""
        if not self.is_new():
            old_status = frappe.db.get_value('Sales Order', self.name, 'status')

            # Define allowed transitions
            allowed_transitions = {
                'Draft': ['Pending', 'Cancelled'],
                'Pending': ['Confirmed', 'Cancelled'],
                'Confirmed': ['In Progress', 'Cancelled'],
                'In Progress': ['Completed', 'On Hold'],
                'On Hold': ['In Progress', 'Cancelled'],
                'Completed': [],  # Terminal state
                'Cancelled': []   # Terminal state
            }

            if old_status != self.status:
                allowed = allowed_transitions.get(old_status, [])
                if self.status not in allowed:
                    frappe.throw(
                        _(f'Cannot transition from {old_status} to {self.status}')
                    )

    def on_submit(self):
        self.status = 'Confirmed'

    def on_cancel(self):
        self.status = 'Cancelled'
```

### 2. State-Dependent Actions

**Actions Based on State:**
```python
class PaymentEntry(Document):
    def validate(self):
        if self.status == 'Draft':
            self.validate_draft_entry()
        elif self.status == 'Submitted':
            self.validate_submitted_entry()

    def before_submit(self):
        # Actions before state change
        if self.payment_type == 'Pay':
            self.validate_sufficient_balance()

        self.status = 'Submitted'

    def on_cancel(self):
        # Reverse actions
        if self.status == 'Submitted':
            self.reverse_gl_entries()

        self.status = 'Cancelled'
```

## References

**State Management Examples:**
- Sales Invoice: https://github.com/frappe/erpnext/blob/develop/erpnext/accounts/doctype/sales_invoice/sales_invoice.py
- Purchase Order: https://github.com/frappe/erpnext/blob/develop/erpnext/buying/doctype/purchase_order/purchase_order.py
