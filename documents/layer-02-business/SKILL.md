---
name: LAYER_02_BUSINESS
description: Expert knowledge for Business Layer modeling in Documentation Robotics
triggers:
  [
    "business process",
    "business service",
    "business actor",
    "business role",
    "business object",
    "BPMN",
    "business layer",
    "archimate business",
  ]
version: 0.6.0
---

# Business Layer Skill

**Layer Number:** 02
**Specification:** Metadata Model Spec v0.6.0
**Purpose:** Represents business services, processes, actors, and objects that define the organization's operational structure and capabilities.

---

## Layer Overview

The Business Layer captures the **operational structure** of the organization:

- **WHO** - Business actors, roles, and collaborations
- **WHAT** - Business services and products
- **HOW** - Business processes, functions, and interactions
- **INFORMATION** - Business objects and their representations

This layer uses **ArchiMate 3.2 Business Layer** standard without custom extensions, with optional extensions for BPMN integration, SLA tracking, and security controls.

---

## Entity Types

| Entity Type               | Description                                          | Key Attributes                                                        |
| ------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------- |
| **BusinessActor**         | Organizational entity capable of performing behavior | Examples: Customer, Employee, Partner, Supplier                       |
| **BusinessRole**          | Responsibility for performing specific behavior      | Examples: Sales Representative, Account Manager, System Administrator |
| **BusinessCollaboration** | Aggregate of business roles working together         | Examples: Sales Team, Customer Service Department, Project Team       |
| **BusinessInterface**     | Point of access where business service is available  | Examples: Customer Portal, Phone Support, Email Support               |
| **BusinessProcess**       | Sequence of business behaviors achieving a result    | Can include BPMN references, security controls, KPI targets           |
| **BusinessFunction**      | Collection of business behavior based on criteria    | Examples: Marketing, Sales, Customer Service, Finance                 |
| **BusinessInteraction**   | Unit of collective behavior by collaboration         | Examples: Sales Meeting, Contract Negotiation, Customer Onboarding    |
| **BusinessEvent**         | Something that happens and influences behavior       | Types: time-driven, state-change, external                            |
| **BusinessService**       | Service that fulfills a business need                | Includes SLA properties, motivation links, APM monitoring             |
| **BusinessObject**        | Concept used within business domain                  | Examples: Order, Invoice, Customer, Product, Contract                 |
| **Contract**              | Formal specification of agreement                    | Examples: SLA, Terms of Service, Purchase Agreement                   |
| **Representation**        | Perceptible form of business object                  | Formats: document, report, form, message, dashboard                   |
| **Product**               | Coherent collection of services with a value         | Aggregates services and contracts, delivers value to customers        |

---

## Intra-Layer Relationships

### Structural Relationships

| Source Type           | Predicate   | Target Type         | Example                                                           |
| --------------------- | ----------- | ------------------- | ----------------------------------------------------------------- |
| Product               | composes    | BusinessService     | "E-commerce Platform" composes "Payment Service"                  |
| BusinessCollaboration | composes    | BusinessRole        | "Sales Team" composes "Sales Representative" role                 |
| BusinessProcess       | composes    | BusinessProcess     | "Order Fulfillment" composes "Pick", "Pack", "Ship" sub-processes |
| BusinessFunction      | composes    | BusinessProcess     | "Sales Function" composes "Lead Generation Process"               |
| Product               | aggregates  | BusinessService     | Product bundles multiple services                                 |
| Product               | aggregates  | Contract            | Product includes SLA contracts                                    |
| BusinessCollaboration | aggregates  | BusinessRole        | Collaboration includes multiple roles                             |
| BusinessActor         | assigned-to | BusinessRole        | "John Smith" assigned to "Sales Rep"                              |
| BusinessActor         | assigned-to | BusinessProcess     | Actor directly performs process                                   |
| BusinessRole          | assigned-to | BusinessProcess     | Role responsible for process execution                            |
| BusinessRole          | assigned-to | BusinessFunction    | Role performs function                                            |
| BusinessCollaboration | assigned-to | BusinessInteraction | Collaboration performs interaction                                |
| BusinessProcess       | realizes    | BusinessService     | "Order Processing" realizes "Order Management Service"            |
| BusinessFunction      | realizes    | BusinessService     | "Customer Support Function" realizes "Support Service"            |
| BusinessInteraction   | realizes    | BusinessService     | "Contract Negotiation" realizes "Contracting Service"             |
| Representation        | realizes    | BusinessObject      | "Invoice PDF" realizes "Invoice" concept                          |
| BusinessObject        | specializes | BusinessObject      | "RetailCustomer" specializes "Customer"                           |
| BusinessRole          | specializes | BusinessRole        | "Senior Sales Rep" specializes "Sales Rep"                        |
| Contract              | specializes | Contract            | "Premium SLA" specializes "Standard SLA"                          |

### Behavioral Relationships

| Source Type         | Predicate       | Target Type         | Example                                                      |
| ------------------- | --------------- | ------------------- | ------------------------------------------------------------ |
| BusinessEvent       | triggers        | BusinessProcess     | "Order Received" triggers "Order Fulfillment Process"        |
| BusinessEvent       | triggers        | BusinessFunction    | "Monthly Close" triggers "Financial Reporting Function"      |
| BusinessEvent       | triggers        | BusinessInteraction | "Customer Complaint" triggers "Issue Resolution Interaction" |
| BusinessProcess     | triggers        | BusinessEvent       | "Payment Complete" triggers "Order Confirmed Event"          |
| BusinessInteraction | triggers        | BusinessProcess     | "Sales Meeting" triggers "Proposal Generation Process"       |
| BusinessProcess     | flows-to        | BusinessProcess     | "Credit Check" flows to "Order Approval"                     |
| BusinessInteraction | flows-to        | BusinessProcess     | "Negotiation" flows to "Contract Signing"                    |
| BusinessService     | serves          | BusinessActor       | "Customer Portal" serves "Customer"                          |
| BusinessService     | serves          | BusinessRole        | "Reporting Service" serves "Manager" role                    |
| BusinessService     | serves          | BusinessProcess     | "Authentication Service" serves "Login Process"              |
| BusinessInterface   | serves          | BusinessActor       | "Mobile App" serves "Customer"                               |
| BusinessInterface   | serves          | BusinessRole        | "Admin Console" serves "Administrator" role                  |
| BusinessProcess     | accesses        | BusinessObject      | "Order Process" accesses "Order" object                      |
| BusinessFunction    | accesses        | BusinessObject      | "Billing Function" accesses "Invoice" object                 |
| BusinessInteraction | accesses        | BusinessObject      | "Contract Review" accesses "Contract" object                 |
| Contract            | associated-with | BusinessService     | SLA contract associated with service delivery                |
| BusinessObject      | associated-with | BusinessProcess     | "Customer" associated with "Onboarding Process"              |

---

## Cross-Layer References

### Outgoing References (Business → Lower Layers)

| Target Layer              | Reference Type                                      | Example                                                  |
| ------------------------- | --------------------------------------------------- | -------------------------------------------------------- |
| **Layer 1 (Motivation)**  | BusinessService delivers **Value**                  | "Payment Service" delivers "Revenue Generation" value    |
| **Layer 1 (Motivation)**  | BusinessService supports **Goal**                   | Service achieves business goals                          |
| **Layer 1 (Motivation)**  | BusinessService governed by **Principle**           | Follows business principles                              |
| **Layer 1 (Motivation)**  | BusinessActor **is** Stakeholder                    | Actor maps to stakeholder in motivation layer            |
| **Layer 1 (Motivation)**  | BusinessProcess achieves **Goal**                   | Process realizes business goals                          |
| **Layer 1 (Motivation)**  | Contract drives **Constraint**                      | SLA contract defines constraints                         |
| **Layer 4 (Application)** | BusinessService realized by **ApplicationService**  | "Order Service" realized by "OrderManagementAPI"         |
| **Layer 4 (Application)** | BusinessProcess automated by **ApplicationProcess** | Process workflow automated by application                |
| **Layer 4 (Application)** | BusinessObject represented in **DataObject**        | "Customer" business concept maps to customer data object |
| **Layer 4 (Application)** | BusinessEvent triggers **ApplicationEvent**         | Business event generates application event               |
| **Layer 3 (Security)**    | BusinessProcess protected by **SecurityControl**    | Process has authentication/authorization                 |
| **Layer 3 (Security)**    | BusinessCollaboration maps to **SecurityActor**     | Team maps to security roles                              |
| **Layer 6 (API)**         | BusinessInterface maps to **API Operation**         | Portal interface maps to REST endpoints                  |
| **Layer 7 (Data Model)**  | BusinessObject → **JSON Schema**                    | Business object defined as schema                        |
| **Layer 11 (APM)**        | BusinessProcess tracked by **BusinessMetric**       | Process performance measured                             |
| **Layer 11 (APM)**        | BusinessService defines **KPI Target**              | SLA targets for monitoring                               |

### Incoming References (Lower Layers → Business)

Lower layers (Application, Technology, API, etc.) reference Business layer elements to show:

- **Realization**: Application services realize business services
- **Support**: Technology supports business operations
- **Traceability**: APIs map to business interfaces

---

## Codebase Detection Patterns

### Pattern 1: Service Layer Classes

```python
# FastAPI Business Service
@app.post("/api/orders")
async def create_order(order_data: OrderRequest):
    """Creates a new customer order (Business Service: Order Management)"""
    pass
```

**Maps to:**

- BusinessService: "Order Management Service"
- BusinessProcess: "Create Order Process"
- BusinessObject: "Order"
- BusinessInterface: "API Interface"

### Pattern 2: Domain Models

```python
from dataclasses import dataclass

@dataclass
class Customer:
    """Customer business object"""
    customer_id: str
    name: str
    email: str
    status: str  # active, inactive, suspended
```

**Maps to:**

- BusinessObject: "Customer"
- Potential BusinessProcess: "Customer Management"

### Pattern 3: Event Definitions

```typescript
// Domain events
export enum BusinessEvents {
  ORDER_CREATED = "order.created",
  ORDER_FULFILLED = "order.fulfilled",
  PAYMENT_RECEIVED = "payment.received",
}
```

**Maps to:**

- BusinessEvent entities (order.created, order.fulfilled, payment.received)

### Pattern 4: BPMN Process References

```python
# Process definition with BPMN reference
class OrderFulfillmentProcess:
    """
    Order fulfillment business process
    BPMN: processes/order-fulfillment.bpmn
    KPI: 95% orders fulfilled within 24 hours
    """
    def execute(self, order_id: str):
        pass
```

**Maps to:**

- BusinessProcess: "Order Fulfillment"
- Properties: `bpmn-file`, `kpi-target`

### Pattern 5: Role-Based Authorization

```python
from enum import Enum

class BusinessRole(Enum):
    SALES_REP = "sales_representative"
    ACCOUNT_MANAGER = "account_manager"
    CUSTOMER_SERVICE = "customer_service"
    ADMIN = "administrator"

@require_role(BusinessRole.SALES_REP)
def create_opportunity(data):
    pass
```

**Maps to:**

- BusinessRole entities (SalesRepresentative, AccountManager, etc.)

### Pattern 6: SLA Configuration

```yaml
# Service SLA definitions
services:
  order_processing:
    sla:
      availability: 99.9%
      response_time: 500ms
      throughput: 1000 req/sec
    business_hours: "24/7"
```

**Maps to:**

- BusinessService with SLA properties
- Contract entity for formal SLA

---

## Modeling Workflow

### Step 1: Identify Business Actors and Roles

```bash
# Add business actors
dr add business actor "Customer" \
  --description "End user purchasing products"

dr add business actor "Sales Team" \
  --description "Internal sales organization"

# Add business roles
dr add business role "Sales Representative" \
  --description "Responsible for customer acquisition"

dr add business role "Account Manager" \
  --description "Manages existing customer relationships"
```

### Step 2: Define Business Services

```bash
# Core business service
dr add business service "Order Management Service" \
  --properties sla-availability=99.9%,sla-response-time=500ms \
  --description "Manages customer order lifecycle"

# Link to motivation layer
dr relationship add "business/service/order-management" \
  supports "motivation/goal/improve-order-efficiency"
```

### Step 3: Model Business Processes

```bash
# Main process
dr add business process "Order Fulfillment Process" \
  --properties bpmn-file=processes/order-fulfillment.bpmn \
  --description "End-to-end order fulfillment from creation to delivery"

# Sub-processes
dr add business process "Pick Items Process" \
  --description "Pick items from warehouse inventory"

dr add business process "Pack Order Process" \
  --description "Pack picked items for shipment"

# Composition relationships
dr relationship add "business/process/order-fulfillment" \
  composes "business/process/pick-items"

dr relationship add "business/process/order-fulfillment" \
  composes "business/process/pack-order"

# Process flows
dr relationship add "business/process/pick-items" \
  flows-to "business/process/pack-order"
```

### Step 4: Define Business Objects

```bash
# Core business objects
dr add business object "Order" \
  --description "Customer purchase order"

dr add business object "Customer" \
  --description "Individual or organization purchasing products"

dr add business object "Product" \
  --description "Item available for purchase"

# Process access to objects
dr relationship add "business/process/order-fulfillment" \
  accesses "business/object/order"
```

### Step 5: Model Business Events

```bash
# Events that trigger processes
dr add business event "Order Received" \
  --properties type=state-change,topic=orders.received \
  --description "New order submitted by customer"

dr add business event "Payment Confirmed" \
  --properties type=state-change,topic=payments.confirmed \
  --description "Payment successfully processed"

# Event triggering
dr relationship add "business/event/order-received" \
  triggers "business/process/order-fulfillment"
```

### Step 6: Establish Cross-Layer Relationships

```bash
# Link to application layer
dr relationship add "business/service/order-management" \
  realized-by "application/service/order-api"

# Link to motivation layer
dr relationship add "business/service/order-management" \
  delivers "motivation/value/customer-satisfaction"

# Link to data layer
dr relationship add "business/object/order" \
  defined-by "data-model/schema/order.schema.json"
```

### Step 7: Validate

```bash
dr validate --layer business
dr validate --validate-relationships
```

---

## Common Modeling Scenarios

### Scenario 1: E-commerce Order Management

```
Product: "E-commerce Platform"
├── composes → BusinessService: "Order Service"
│   ├── realizes ← BusinessProcess: "Order Fulfillment"
│   │   ├── triggers ← BusinessEvent: "Order Received"
│   │   ├── accesses → BusinessObject: "Order"
│   │   └── assigned-to → BusinessRole: "Order Processor"
│   └── realized-by → ApplicationService: "OrderManagementAPI"
├── composes → BusinessService: "Payment Service"
│   └── realizes ← BusinessProcess: "Payment Processing"
└── aggregates → Contract: "E-commerce SLA"
```

### Scenario 2: Customer Support System

```
BusinessFunction: "Customer Support"
├── composes → BusinessProcess: "Ticket Resolution"
│   ├── triggers ← BusinessEvent: "Support Request Received"
│   ├── assigned-to → BusinessRole: "Support Agent"
│   ├── accesses → BusinessObject: "Support Ticket"
│   └── flows-to → BusinessProcess: "Follow-up Communication"
├── realizes → BusinessService: "Support Service"
│   ├── serves → BusinessActor: "Customer"
│   └── properties: sla-response-time=2h, sla-resolution-time=24h
└── tracked-by → BusinessMetric: "First Response Time"
```

### Scenario 3: Sales Pipeline

```
BusinessCollaboration: "Sales Team"
├── composes → BusinessRole: "Sales Representative"
├── composes → BusinessRole: "Sales Manager"
└── assigned-to → BusinessInteraction: "Sales Meeting"
    ├── accesses → BusinessObject: "Opportunity"
    ├── flows-to → BusinessProcess: "Proposal Generation"
    └── triggers → BusinessEvent: "Deal Closed"
```

---

## BPMN Integration

When business processes reference BPMN diagrams:

```bash
dr add business process "Loan Approval Process" \
  --properties bpmn-file=processes/loan-approval.bpmn,bpmn-version=2.0 \
  --description "End-to-end loan application review and approval"
```

**BPMN Properties:**

- `bpmn-file`: Path to BPMN XML file
- `bpmn-version`: BPMN specification version (2.0)
- `bpmn-task-mapping`: Map BPMN tasks to business roles

**Validation:** Ensure BPMN task IDs align with business process sub-processes.

---

## SLA and Performance Tracking

Business services can define SLA targets:

```yaml
business-service:
  id: "payment-processing-service"
  properties:
    sla-availability: "99.99%"
    sla-response-time: "200ms"
    sla-throughput: "5000 tps"
    business-hours: "24/7"
    escalation-time: "15m"
```

These SLAs flow down to:

- **Application Layer** - Application services inherit targets
- **APM Layer** - Monitoring dashboards track against targets
- **Motivation Layer** - SLAs trace to business goals

---

## ArchiMate Export

```bash
dr export archimate --layer business --output business.archimate
```

**Supported ArchiMate Elements:**

- All 13 business entity types map directly to ArchiMate 3.2 Business Layer
- Relationships: composition, aggregation, assignment, realization, specialization, triggering, flow, serving, access, association

---

## Best Practices

1. **Start with Services, Not Processes** - Identify WHAT the business provides before HOW it's delivered
2. **Use Process Composition** - Break complex processes into manageable sub-processes
3. **Model Events Explicitly** - Event-driven architectures need explicit BusinessEvent entities
4. **Link to Motivation Early** - Connect services and processes to goals for traceability
5. **Don't Over-Detail** - Focus on architecturally significant processes, not every task
6. **Use BPMN for Complex Workflows** - Reference BPMN files rather than modeling every detail
7. **Distinguish Role from Actor** - Role is responsibility; Actor is individual/team
8. **Model Contracts for SLAs** - Formalize service agreements as Contract entities
9. **Track Business Objects** - Identify key domain concepts even if data model comes later

---

## Validation Tips

| Issue                        | Cause                                        | Fix                                           |
| ---------------------------- | -------------------------------------------- | --------------------------------------------- |
| Orphaned Process             | No event triggers it, no service realizes it | Add triggering event or link to service       |
| Unrealized Service           | No process/function realizes the service     | Add process that implements the service       |
| Missing Business Objects     | Processes don't access any objects           | Identify key domain concepts and add them     |
| No Cross-Layer Relationships | Business not linked to application/data      | Add realization relationships to lower layers |
| Unassigned Roles             | Roles not assigned to processes              | Assign roles to show responsibility           |
| Missing SLA Properties       | Services lack performance targets            | Add SLA properties for monitoring             |

---

## Quick Reference

**Add Commands:**

```bash
dr add business actor <name>
dr add business role <name>
dr add business service <name> --properties sla-availability=<value>
dr add business process <name> --properties bpmn-file=<path>
dr add business object <name>
dr add business event <name> --properties type=<type>,topic=<topic>
dr add business function <name>
dr add business collaboration <name>
```

**Relationship Commands:**

```bash
dr relationship add <source> realizes <target>
dr relationship add <source> composes <target>
dr relationship add <source> assigned-to <target>
dr relationship add <source> triggers <target>
dr relationship add <source> flows-to <target>
dr relationship add <source> accesses <target>
dr relationship add <source> serves <target>
```

**Cross-Layer Relationship Commands:**

```bash
dr relationship add <business-service> supports <motivation-goal>
dr relationship add <business-service> realized-by <application-service>
dr relationship add <business-object> defined-by <data-schema>
```
