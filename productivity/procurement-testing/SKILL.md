---
title: Procurement Testing
description: Validate procurement workflows, skills, data extraction, compliance, and integration with systematic testing methodology for procurement domain
version: 1.0
frequency_percent: 50.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/shared/procurement-testing
gigabrain_tags: disciplines, 01900_procurement, testing-verification, workflow-testing, integration-testing, ai-native-operations
openstinger_context: procurement-testing, quality-assurance, validation-verification
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/skills/shared/testing-verification/SKILL.MD
related_skills:
  - pre-task-assessment-readiness
  - testing-verification
  - workflow-implementation
---

# Procurement Testing

## Overview

Systematically validate procurement workflows, skills, data extraction, compliance checking, and integration to ensure all procurement components work correctly. Covers unit testing patterns, integration testing, end-to-end workflow testing, data accuracy verification, and compliance rule validation for the procurement domain.

**Announce at start:** "I'm using the procurement-testing skill to validate procurement workflows, skills, and integrations."

## When to Use This Skill

**Trigger Conditions:**
- Validating procurement workflow implementations before deployment
- Testing new procurement skills for correctness
- Verifying data extraction accuracy and provenance
- Validating compliance rules and audit trail functionality
- Integration testing between procurement services and UI components
- Regression testing after code changes

**Prerequisites:**
- Procurement components to be tested identified
- Test data available (sample orders, quotes, invoices, contracts)
- Expected outcomes defined for each test
- Testing environment configured

## Step-by-Step Procedure

### Step 1: Test Scope Definition

Define test scope based on changes or requirements:

| Test Type | Scope | When to Use |
|-----------|------|-------------|
| **Unit Test** | Individual functions, validation rules, calculations | After code generation, before integration |
| **Integration Test** | Service interactions, API endpoints, data flow | After service deployment |
| **Workflow Test** | End-to-end procurement scenarios | Before release, after major changes |
| **Data Accuracy Test** | Data extraction, provenance, cross-references | After data pipeline changes |
| **Compliance Test** | Authority limits, audit trail, regulatory rules | Before audit, after rule changes |
| **UI Test** | Form submission, validation display, error handling | After UI changes, before release |

### Step 2: Test Data Preparation

Prepare test data covering positive, negative, and edge cases:

**Test Order Data:**
```
VALID_ORDER: {
  order_type: "PO",
  supplier: "approved_supplier_1",
  total_value: 50000,
  currency: "ZAR",
  budget_code: "WBS-01900-STR-01",
  line_items: [{item: "Steel W310", qty: 100, uom: "t", price: 18500}],
  incoterms: "DAP",
  delivery_date: "2026-07-15"
}

LOW_VALUE_ORDER: {
  order_type: "PO",
  total_value: 15000,  // Below $25k threshold
  workflow: "single_approval"
}

HIGH_VALUE_ORDER: {
  order_type: "PO",
  total_value: 250000,  // Above $100k threshold
  workflow: "multi_level_approval"
}

INVALID_ORDER_MISSING_FIELDS: {
  order_type: "PO",
  total_value: null,  // Missing required field
  expected: "validation_error"
}

INVALID_ORDER_OVER_BUDGET: {
  order_type: "PO",
  total_value: 150000,
  budget_code: "WBS-exhausted",  // Budget depleted
  expected: "budget_exceeded_error"
}
```

**Test Approval Scenarios:**
```
APPROVAL_<$25K: {value: 20000, expected_approvers: ["procurement_officer"]}
APPROVAL_$25K-$100K: {value: 50000, expected_approvers: ["procurement_manager", "project_manager"]}
APPROVAL_$100K: {value: 150000, expected_approvers: ["procurement_manager", "project_manager", "finance_manager", "director"]}
SELF_APPROVAL_BLOCKED: {value: 50000, created_by: "procurement_manager", expected: "approval_rerouted"}
```

**Test Invoice Data:**
```
VALID_INVOICE: {
  invoice_number: "INV-2026-001",
  po_reference: "PO-2026-0089",
  total_amount: 6290000,
  matches_po: true,
  expected: "pass_3way_match"
}

INVALID_INVOICE_AMOUNT: {
  invoice_number: "INV-2026-002",
  po_reference: "PO-2026-0089",
  total_amount: 6500000,  // Different from PO
  matches_po: false,
  expected: "fail_3way_match"
}

DUPLICATE_INVOICE: {
  invoice_number: "INV-2026-001",  // Same as processed invoice
  expected: "duplicate_detected"
}
```

### Step 3: Workflow Testing

Execute end-to-end procurement workflow tests:

**Test Scenario 1: Standard Order Creation**
1. Submit requisition with valid data
2. Verify requisition stored with correct fields
3. Create PO from requisition
4. Verify PO fields match requisition
5. Submit for approval (<$25k)
6. Verify single approver assigned
7. Approve order
8. Verify status changed to "approved"
9. Issue PO to supplier
10. Verify PO sent and status updated
11. Record SO acknowledgment
12. Verify SO terms match PO
13. Record delivery and GRN
14. Process invoice
15. Verify 3-way match passed
16. Process payment
17. Verify order closed

**Test Scenario 2: High-Value Order with Multi-Level Approval**
1. Create PO with value >$100k
2. Verify 4-level approval chain configured
3. Obtain all approvals
4. Verify no approver approved own order
5. Process through delivery and payment

**Test Scenario 3: Rejection and Rework**
1. Submit order for approval
2. Reject with reason
3. Verify order returned to draft status
4. Correct issue and resubmit
5. Verify rejection reason logged in audit trail

**Test Scenario 4: Compliance Boundary Testing**
1. Attempt to order without budget allocation
2. Verify hard block enforced
3. Attempt to approve over authority limit
4. Verify approval rerouted or blocked
5. Attempt payment without GRN
6. Verify payment blocked

### Step 4: Data Extraction Testing

Validate data extraction accuracy:

| Test | Input | Expected Output | Pass Condition |
|------|-------|----------------|----------------|
| PO Data Extraction | Sample PO PDF | Extracted JSON with all fields | All required fields extracted, accuracy >95% |
| Invoice Data Extraction | Sample invoice PDF | Extracted JSON with line items | All amounts match, PO reference captured |
| Quotation Data Extraction | Supplier quotation PDF | Extracted pricing, validity terms | All prices extracted correctly, validity date parsed |
| GRN Data Extraction | Delivery note | Quantities received, dates match | Quantities match delivery, timestamp extracted |

**Provenance Verification:**
1. Verify every extracted value has source document reference
2. Verify source field mapping is correct
3. Verify extraction timestamp logged
4. Verify confidence score calculated

### Step 5: Integration Testing

Validate integrations between procurement components:

| Integration | Test | Expected Result |
|------------|------|----------------|
| Order → Approval | Submit order for approval | Approval chain triggered, approver notified |
| Order → Budget | Create order with cost code | Budget allocated, remaining balance updated |
| PO → Invoice Reconciliation | Match invoice to PO | 3-way match result correct |
| Contract → Order | Create order under contract | Order terms match contract, pricing correct |
| Supplier DB → Order | Select supplier for order | Supplier on approved list, tier verified |
| Audit Trail → All Actions | Execute workflow sequence | Every action logged with actor, timestamp, data |

### Step 6: Compliance Testing

Validate compliance enforcement:

| Compliance Rule | Test Scenario | Expected Result |
|----------------|---------------|-----------------|
| Authority Limits | Order at threshold boundary | Correct approver assigned |
| Budget Limits | Order at 105% of budget | Blocked with budget exceeded error |
| Approval Sequence | Attempt parallel approval | Sequential order enforced |
| Audit Trail | Complete workflow | All actions logged, no gaps |
| Immutability | Attempt to modify approved order | Modification blocked or requires re-approval |
| Segregation of Duties | User attempts to approve own order | Routed to different approver |
| Document Retention | Query historical records | Records accessible, complete |

### Step 7: Test Results Documentation

Document test results with pass/fail for each:

```
TEST RESULTS — [Test Suite Name]
Date: [YYYY-MM-DD]
Tester: [Agent/Person]

SUMMARY:
Total Tests: [N]
Passed: [N]
Failed: [N]
Skipped: [N]
Pass Rate: [X%]

FAILURE DETAILS:
| Test ID | Test Name | Expected | Actual | Root Cause |
|---------|-----------|----------|--------|------------|

REMEDIATION ACTIONS:
| Failure | Action Required | Responsible | Due Date |
|---------|----------------|-------------|----------|
```

## Success Criteria

- [ ] Test scope defined covering all changed components
- [ ] Test data prepared covering positive, negative, and edge cases
- [ ] All workflow tests executed with expected results
- [ ] Data extraction accuracy >95% for all tested documents
- [ ] All integration tests pass (order → approval → budget → audit)
- [ ] All compliance rules enforced correctly (no bypass possible)
- [ ] Test results documented with pass/fail for each test
- [ ] Failures logged with root cause and remediation actions

## Common Pitfalls

1. **Testing Happy Path Only** — Always test negative cases (missing data, over budget, unauthorized approval) and edge cases (threshold values, boundary conditions).
2. **Using Production Data** — Test data must be synthetic. Real orders contain sensitive pricing and supplier information.
3. **Skipping Compliance Tests** — Compliance rules are the most critical to test because failures create legal, financial, and regulatory risk.
4. **No Regression Testing** — After fixing one issue, always re-run the full test suite to ensure the fix didn't break something else.
5. **Ignoring Timing Tests** — Approval routing, workflow sequencing, and audit trail logging can fail under load. Test performance as well as correctness.

## Cross-References

### Related Skills
- `procurement-order-management` — Workflow testing for order creation
- `procurement-compliance` — Compliance rule testing
- `procurement-data-extraction` — Data extraction accuracy testing
- `procurement-document-generation` — Document generation testing
- `contract-intelligence` — Contract analysis validation
- `testing-verification` — General testing methodology

### Related Agents
- `Mobile Testing Specialist` (DomainForge) — Mobile procurement testing
- `Procurement Analytics Specialist` (DomainForge) — Data accuracy validation
- `QualityForge guardian` — Quality assurance oversight, test strategy
- `PromptForge Probe` — Component testing execution

## Example Usage

**Scenario:** Validate procurement order creation workflow before release

1. **Scope:** Order creation, approval routing, compliance checks
2. **Test Data:** 8 test orders (valid low value, valid high value, missing fields, over budget, self-approval attempt, expired quotation, duplicate, complex multi-line)
3. **Workflow Tests:** Full end-to-end for standard order, high-value order, rejected order
4. **Compliance Tests:** Authority limits, budget blocks, audit trail logging
5. **Results:** 47/47 tests passed (100%), no compliance bypasses found
6. **Documentation:** Full test results logged, signed off for release

## Performance Metrics

**Target Performance:**
- Workflow test coverage: 100% of workflow paths tested
- Compliance test coverage: 100% of compliance rules verified enforced
- Data extraction accuracy: >95% across all document types
- Integration test pass rate: >98% of integration points working
- Test execution time: <5 minutes for unit tests, <30 minutes for full workflow suite