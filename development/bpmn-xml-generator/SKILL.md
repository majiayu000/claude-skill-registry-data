---
name: bpmn-xml-generator
description: >
  Generate BPMN 2.0 compliant XML files from natural language process descriptions.
  Use this skill when a user wants to create a BPMN workflow, convert a business
  process to BPMN XML, model a workflow diagram, or generate process definitions.
  Triggers on requests like "create a BPMN", "generate workflow XML", "model this
  process", "convert to BPMN 2.0", "create process diagram", or "build workflow".
---

# BPMN 2.0 XML Generator

## Overview

This skill transforms natural language process descriptions into fully compliant BPMN 2.0 XML files. The generated XML includes:

- Complete process definitions with all BPMN elements
- Proper namespace declarations for BPMN 2.0 compliance
- Diagram Interchange (DI) data for visual rendering
- Optimized layouts compatible with tools like Camunda, Flowable, and bpmn.io

## Interactive Question Framework

### Purpose

Initial process descriptions are rarely sufficient for optimal BPMN generation. This skill uses a structured clarification process to gather complete requirements before generating XML.

### Question Format

For EVERY clarifying question, use this EXACT format:

```
## Question [N]: [Topic Category]

[Clear, specific question about the process]

### Options:

**A) [Recommended]**: [Specific answer]
   *Why*: [2-3 sentence reasoning explaining why this is the best choice]

**B)** [Alternative answer 1]
**C)** [Alternative answer 2]
**D)** Provide your own answer
**E)** Accept recommended answers for all remaining questions (auto-accept mode)

---
Your choice (A/B/C/D/E):
```

### Auto-Accept Mode

When the user selects option **E**:
1. Set internal flag: `AUTO_ACCEPT_MODE = true`
2. For all subsequent questions, automatically use the recommended answer
3. Log each auto-accepted decision
4. Before generating XML, present a summary:

```
## Auto-Accepted Decisions Summary

| Question | Topic | Decision |
|----------|-------|----------|
| Q3 | Gateway Type | Exclusive Gateway (XOR) |
| Q4 | Error Handling | Boundary Error Event |
| ... | ... | ... |

Proceeding with XML generation using these decisions.
```

### Question Phases

Process questions in this specific order:

#### Phase 1: Process Scope (Questions 1-3)
- Process name and identifier
- Process trigger (start event type)
- Process completion states (end event types)

#### Phase 2: Participants (Questions 4-5)
- Single process vs. collaboration (multiple pools)
- Lanes/roles within pools

#### Phase 3: Activities (Questions 6-11)
- Main activities/tasks identification
- Task types for each activity
- **Task descriptions/documentation** (CRITICAL for PowerPoint generation)
- Task sequencing and dependencies
- Subprocess candidates

#### Phase 4: Flow Control (Questions 11-15)
- Decision points requiring gateways
- Gateway types (exclusive, parallel, inclusive, event-based)
- Default flows
- Loop/cycle detection

#### Phase 5: Events & Exceptions (Questions 16-19)
- Intermediate events (timer, message, signal)
- Boundary events on tasks
- Error handling approach
- Compensation requirements

#### Phase 6: Data & Integration (Questions 20-22)
- Data objects needed
- External system integrations
- Message flows (for collaborations)

#### Phase 7: Optimization Review (Question 23)
- Final review of proposed structure
- Opportunity for adjustments

### Adaptive Questioning

Skip questions that don't apply:
- Skip participant questions for simple single-pool processes
- Skip data questions if no data dependencies mentioned
- Skip error handling if process is straightforward
- Always ask critical questions: start event, main tasks, end events

## BPMN Element Mapping

### Task Type Selection

Map description keywords to BPMN task types:

| Keywords in Description | BPMN Task Type | XML Element |
|------------------------|----------------|-------------|
| "user reviews", "person approves", "manually enters", "human performs" | User Task | `<bpmn:userTask>` |
| "system calls API", "automated process", "service executes", "integration" | Service Task | `<bpmn:serviceTask>` |
| "send email", "send notification", "notify user", "alert" | Send Task | `<bpmn:sendTask>` |
| "wait for response", "receive message", "await confirmation" | Receive Task | `<bpmn:receiveTask>` |
| "run script", "execute code", "calculate", "transform data" | Script Task | `<bpmn:scriptTask>` |
| "apply business rule", "decision table", "evaluate rules" | Business Rule Task | `<bpmn:businessRuleTask>` |
| "call external process", "invoke subprocess" | Call Activity | `<bpmn:callActivity>` |
| Generic activity with no specific type | Task | `<bpmn:task>` |

### Task Documentation (CRITICAL)

**Every task MUST include a `<bpmn:documentation>` element** with a detailed description. This is essential for:
- PowerPoint presentation generation (Level 3 bullet points)
- Process documentation and training materials
- Audit and compliance documentation

**Documentation Template:**
```xml
<bpmn:userTask id="Activity_ReviewApplication" name="Review Application">
    <bpmn:documentation>
        Reviewer examines the submitted application for completeness and accuracy.
        Verifies all required documents are attached and applicant information matches
        supporting documentation. Marks application as approved, rejected, or requires
        additional information. Average completion time: 15 minutes.
    </bpmn:documentation>
    <bpmn:incoming>Flow_1</bpmn:incoming>
    <bpmn:outgoing>Flow_2</bpmn:outgoing>
</bpmn:userTask>
```

**What to include in documentation:**
1. **Purpose**: What does this task accomplish?
2. **Actions**: What specific steps or actions are performed?
3. **Actor/System**: Who or what performs this task?
4. **Inputs**: What data or documents are needed?
5. **Outputs**: What is produced or changed?
6. **Criteria**: How do you know when it's complete?

**Inferring documentation from context:**
When the user provides a process description, extract and expand details for each task:

| User Input | Generated Documentation |
|------------|------------------------|
| "validate order" | "System validates order details including product availability, pricing accuracy, and customer information. Checks for duplicate orders and verifies shipping address is within serviceable region. Returns validation status with any error codes." |
| "manager approves" | "Manager reviews the request and supporting documentation. Evaluates against budget constraints and policy requirements. Provides approval, rejection, or requests additional information with justification." |
| "send notification" | "System sends automated email notification to relevant stakeholders. Includes summary of completed action, any required next steps, and links to detailed information. Logs notification delivery status." |

### Gateway Selection

| Decision Pattern | Gateway Type | XML Element | Symbol |
|-----------------|--------------|-------------|--------|
| "if/then/else", "either A or B", "based on condition", "depending on" | Exclusive (XOR) | `<bpmn:exclusiveGateway>` | X |
| "do all of", "simultaneously", "in parallel", "at the same time" | Parallel (AND) | `<bpmn:parallelGateway>` | + |
| "one or more of", "any combination", "at least one" | Inclusive (OR) | `<bpmn:inclusiveGateway>` | O |
| "wait for first event", "whichever happens first", "race condition" | Event-Based | `<bpmn:eventBasedGateway>` | Pentagon |
| Complex merge logic not fitting other types | Complex | `<bpmn:complexGateway>` | * |

### Event Selection

#### Start Events
| Trigger | Event Type | XML Element |
|---------|-----------|-------------|
| Process begins manually or undefined | None | `<bpmn:startEvent>` |
| External message received | Message | `<bpmn:startEvent><bpmn:messageEventDefinition/></bpmn:startEvent>` |
| Scheduled time/date | Timer | `<bpmn:startEvent><bpmn:timerEventDefinition/></bpmn:startEvent>` |
| Condition becomes true | Conditional | `<bpmn:startEvent><bpmn:conditionalEventDefinition/></bpmn:startEvent>` |
| Signal received | Signal | `<bpmn:startEvent><bpmn:signalEventDefinition/></bpmn:startEvent>` |

#### End Events
| Outcome | Event Type | XML Element |
|---------|-----------|-------------|
| Normal completion | None | `<bpmn:endEvent>` |
| Send final message | Message | `<bpmn:endEvent><bpmn:messageEventDefinition/></bpmn:endEvent>` |
| Error occurred | Error | `<bpmn:endEvent><bpmn:errorEventDefinition/></bpmn:endEvent>` |
| Escalate to higher level | Escalation | `<bpmn:endEvent><bpmn:escalationEventDefinition/></bpmn:endEvent>` |
| Stop all process instances | Terminate | `<bpmn:endEvent><bpmn:terminateEventDefinition/></bpmn:endEvent>` |

#### Intermediate Events
| Purpose | Event Type | Catching/Throwing |
|---------|-----------|-------------------|
| Wait for message | Message | Catching |
| Send message | Message | Throwing |
| Wait for time | Timer | Catching |
| Wait for condition | Conditional | Catching |
| Receive/send signal | Signal | Both |

#### Boundary Events
| Attached To | Purpose | Interrupting |
|------------|---------|--------------|
| Task | Handle timeout | Timer (can be non-interrupting) |
| Task | Handle error | Error (always interrupting) |
| Task | Handle message | Message (can be non-interrupting) |
| Subprocess | Handle escalation | Escalation (can be non-interrupting) |

## Phase Comments for Hierarchy (CRITICAL for PowerPoint)

**Always include phase comments in the generated BPMN XML** to enable automatic phase detection for PowerPoint presentations. The BPMN-to-PPTX skill uses these comments to create the 3-tier hierarchy:
- **Level 1 (Chevrons)**: Phases from comments
- **Level 2 (White boxes)**: Task groups within each phase
- **Level 3 (Gray boxes)**: Individual tasks with bullet point details

### Phase Comment Format

Insert comments immediately before each phase's first element:

```xml
<bpmn:process id="Process_Example" name="Example Process" isExecutable="true">

    <!-- Phase 1: Intake and Validation -->
    <bpmn:startEvent id="StartEvent_1" name="Request Received">
        ...
    </bpmn:startEvent>

    <bpmn:userTask id="Activity_Review" name="Review Request">
        <bpmn:documentation>...</bpmn:documentation>
        ...
    </bpmn:userTask>

    <!-- Phase 2: Processing -->
    <bpmn:serviceTask id="Activity_Process" name="Process Request">
        <bpmn:documentation>...</bpmn:documentation>
        ...
    </bpmn:serviceTask>

    <!-- Phase 3: Fulfillment -->
    <bpmn:userTask id="Activity_Fulfill" name="Fulfill Request">
        <bpmn:documentation>...</bpmn:documentation>
        ...
    </bpmn:userTask>

    <bpmn:endEvent id="EndEvent_1" name="Complete">
        ...
    </bpmn:endEvent>

</bpmn:process>
```

### Phase Naming Guidelines

| Phase Type | Example Names |
|------------|---------------|
| Initial intake | "Intake", "Request Intake", "Initial Review" |
| Validation | "Validation", "Verification", "Assessment" |
| Processing | "Processing", "Core Processing", "Execution" |
| Decision/Review | "Review", "Approval", "Decision Point" |
| Fulfillment | "Fulfillment", "Completion", "Delivery" |
| Exception handling | "Exception Handling", "Error Recovery" |

### Determining Phase Boundaries

Group tasks into phases based on:
1. **Logical grouping**: Tasks that serve a common purpose
2. **Natural breakpoints**: Before/after major decisions or parallel flows
3. **Actor changes**: When responsibility shifts between roles
4. **State transitions**: When the process entity changes state
5. **Target size**: Aim for 3-6 tasks per phase for readability

## XML Generation Rules

### Required Structure

Every generated BPMN file MUST include:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    id="Definitions_[unique-id]"
    targetNamespace="http://bpmn.io/schema/bpmn"
    exporter="Claude BPMN Generator"
    exporterVersion="1.1">

    <!-- Process definition goes here -->

    <!-- Diagram interchange goes here -->

</bpmn:definitions>
```

### ID Generation Rules

- Definitions: `Definitions_[processName]`
- Process: `Process_[processName]`
- Start Event: `StartEvent_[number]`
- End Event: `EndEvent_[number]`
- Tasks: `Activity_[descriptiveName]`
- Gateways: `Gateway_[descriptiveName]`
- Sequence Flows: `Flow_[sourceId]_[targetId]`
- Shapes: `[elementId]_di`
- Edges: `[flowId]_di`

Use camelCase for IDs derived from names. Remove spaces and special characters.

### Sequence Flow Rules

1. Every element (except start events) MUST have at least one incoming flow
2. Every element (except end events) MUST have at least one outgoing flow
3. Gateways splitting must eventually merge (except for end paths)
4. Conditional flows MUST have condition expressions:

```xml
<bpmn:sequenceFlow id="Flow_1" sourceRef="Gateway_1" targetRef="Task_2">
    <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
        ${condition == true}
    </bpmn:conditionExpression>
</bpmn:sequenceFlow>
```

5. Default flows from gateways:

```xml
<bpmn:exclusiveGateway id="Gateway_1" default="Flow_default">
    ...
</bpmn:exclusiveGateway>
<bpmn:sequenceFlow id="Flow_default" sourceRef="Gateway_1" targetRef="Task_3"/>
```

### Element Ordering in XML

Follow this order within `<bpmn:process>`:
1. Start events
2. Tasks and activities (in flow order)
3. Gateways
4. Intermediate events
5. End events
6. Sequence flows
7. Data objects (if any)

## Diagram Interchange Generation

### Element Dimensions

| Element | Width | Height |
|---------|-------|--------|
| Start Event | 36 | 36 |
| End Event | 36 | 36 |
| Intermediate Event | 36 | 36 |
| Task | 100 | 80 |
| Gateway | 50 | 50 |
| Collapsed Subprocess | 100 | 80 |
| Expanded Subprocess | 350+ | 200+ |
| Pool (horizontal) | Total width | 250+ |
| Lane | Pool width | 125 |

### Layout Algorithm

```
CONSTANTS:
  START_X = 180
  START_Y = 120
  H_SPACING = 150  (horizontal space between elements)
  V_SPACING = 100  (vertical space for parallel branches)
  EVENT_CENTER_OFFSET = 18  (half of 36px event size)
  TASK_CENTER_OFFSET_Y = 40  (half of 80px task height)
  GATEWAY_CENTER_OFFSET = 25  (half of 50px gateway size)

ALGORITHM:
1. Place start event at (START_X, START_Y)
2. For each subsequent element in main flow:
   - Place at (previous_x + previous_width + H_SPACING, same_y)
3. For gateway splits:
   - Calculate number of outgoing paths
   - Distribute paths vertically centered on gateway
   - Top path: gateway_y - ((num_paths-1) * V_SPACING / 2)
   - Each subsequent path: previous_y + V_SPACING
4. For gateway merges:
   - Place at x = rightmost_incoming_element_x + H_SPACING
   - Place at y = average of incoming paths y values
5. End events: align to rightmost position
```

### Waypoint Generation

For sequence flows (BPMNEdge), generate waypoints:

**Horizontal flow (same Y level):**
```xml
<bpmndi:BPMNEdge id="Flow_1_di" bpmnElement="Flow_1">
    <di:waypoint x="[source_x + source_width]" y="[source_center_y]"/>
    <di:waypoint x="[target_x]" y="[target_center_y]"/>
</bpmndi:BPMNEdge>
```

**Flow with vertical change:**
```xml
<bpmndi:BPMNEdge id="Flow_1_di" bpmnElement="Flow_1">
    <di:waypoint x="[source_x + source_width]" y="[source_center_y]"/>
    <di:waypoint x="[midpoint_x]" y="[source_center_y]"/>
    <di:waypoint x="[midpoint_x]" y="[target_center_y]"/>
    <di:waypoint x="[target_x]" y="[target_center_y]"/>
</bpmndi:BPMNEdge>
```

### Center Point Calculations

- Event center: (x + 18, y + 18)
- Task center: (x + 50, y + 40)
- Gateway center: (x + 25, y + 25)

Connection points:
- Right side of event: (x + 36, y + 18)
- Left side of task: (x, y + 40)
- Right side of task: (x + 100, y + 40)
- Gateway sides: top (x+25, y), right (x+50, y+25), bottom (x+25, y+50), left (x, y+25)

## Validation Checklist

Before outputting XML, verify:

### Structural Integrity
- [ ] Exactly one start event (or multiple for different triggers in event subprocess)
- [ ] At least one end event
- [ ] All elements connected via sequence flows
- [ ] No orphaned elements
- [ ] All IDs unique within document

### Flow Validity
- [ ] Start events have no incoming flows
- [ ] End events have no outgoing flows
- [ ] All other elements have both incoming and outgoing flows
- [ ] Parallel splits have matching parallel joins
- [ ] No infinite loops without exit condition

### BPMN 2.0 Compliance
- [ ] All required namespaces declared
- [ ] All elements have required attributes (id, name where applicable)
- [ ] Conditional flows have condition expressions
- [ ] Default flows properly marked on gateways
- [ ] Event definitions properly nested

### Diagram Interchange
- [ ] Every process element has corresponding BPMNShape
- [ ] Every sequence flow has corresponding BPMNEdge
- [ ] All shapes have valid Bounds (x, y, width, height)
- [ ] All edges have at least 2 waypoints
- [ ] No negative coordinates
- [ ] Elements don't overlap

## Output Format

After gathering all requirements, output:

### 1. Decision Summary
```
## Process Configuration Summary

**Process Name:** [name]
**Process ID:** [id]

### Decisions Made:
| # | Topic | Decision |
|---|-------|----------|
| 1 | Start Event | [type] |
| 2 | Main Tasks | [list] |
...
```

### 2. Process Description
```
## Generated Process Structure

[Brief narrative description of the process flow]

**Flow Summary:**
Start → [Task 1] → [Gateway] → [Branch A] / [Branch B] → [Merge] → End
```

### 3. BPMN XML File
Write the complete XML to a file named `[process-name].bpmn` in the current directory.

### 4. Validation Confirmation
```
## Validation Results

✓ All structural checks passed
✓ All flow validity checks passed
✓ BPMN 2.0 compliance verified
✓ Diagram interchange complete

File written: [filename].bpmn
```

## Example Question Sequence

For input: "Order fulfillment process"

**Q1 - Process Trigger:**
"What initiates the order fulfillment process?"
- Recommended: Customer places order (Message Start Event)

**Q2 - End States:**
"How does this process complete?"
- Recommended: Two ends - Order Shipped (success) and Order Cancelled (exception)

**Q3 - Main Activities:**
"What are the main steps in fulfilling an order?"
- Recommended: Validate Order → Check Inventory → Process Payment → Pack Items → Ship Order

**Q4 - Decision Points:**
"Are there any points where different paths are taken based on conditions?"
- Recommended: Yes - after inventory check (in stock vs. out of stock)

... and so on.

## References

For detailed element specifications, see:
- `references/bpmn-elements-reference.md` - Complete element catalog
- `references/xml-namespaces.md` - Namespace documentation
- `references/clarification-patterns.md` - Question templates by category

For XML structure examples, see:
- `templates/bpmn-skeleton.xml` - Base structure
- `templates/element-templates.xml` - Element snippets
- `examples/` - Complete working examples
