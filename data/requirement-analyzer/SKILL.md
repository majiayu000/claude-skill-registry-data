---
name: requirement-analyzer
description: Extends generic requirement analysis with PHP/CakePHP specific considerations and technical mappings
---

# PHP/CakePHP Requirement Analyzer

A specialized skill that extends generic requirement analysis with PHP/CakePHP specific technical mappings and framework considerations.

**Note**: This skill extends `generic/requirement-analyzer` with technology-specific features.

## Core Responsibilities

### 1. Requirement Decomposition

Break down user requirements into:
- **Functional Requirements**: What the system must do
- **Non-Functional Requirements**: How the system should perform
- **Constraints**: Technical, business, or regulatory limitations
- **Success Criteria**: Measurable outcomes

### 2. Requirement Analysis Framework

#### Input Analysis
```yaml
User Story Format:
  As a: [user type]
  I want: [feature/functionality]
  So that: [business value]

Acceptance Criteria:
  Given: [context]
  When: [action]
  Then: [expected outcome]
```

#### Output Specification
```yaml
Requirement Specification:
  id: REQ-[number]
  type: functional|non-functional|constraint
  priority: high|medium|low
  description: [detailed description]
  acceptance_criteria: [list of criteria]
  dependencies: [related requirements]
  impact_analysis:
    affected_modules: [list]
    database_changes: [yes/no]
    api_changes: [yes/no]
```

### 3. PHP/CakePHP Specific Considerations

**Framework Constraints:**
- MVC architecture requirements
- ORM conventions (Table, Entity patterns)
- Plugin compatibility
- Version-specific features

**Database Considerations:**
- Multi-tenant architecture support
- Migration requirements
- Fixture implications

**Performance Requirements:**
- Response time targets
- Query optimization needs
- Caching strategy

### 4. Requirement Validation

**Completeness Check:**
- All user stories have acceptance criteria
- Non-functional requirements are measurable
- Dependencies are identified
- Edge cases are considered

**Feasibility Analysis:**
- Technical feasibility within CakePHP
- Resource availability
- Timeline constraints
- Integration complexity

### 5. Documentation Standards

**Requirement Document Structure:**
```markdown
# Feature: [Name]

## Overview
[Brief description]

## User Stories
### Story 1: [Title]
- As a: [user]
- I want: [feature]
- So that: [value]

## Functional Requirements
### FR-001: [Title]
- Description: [detail]
- Priority: [High/Medium/Low]
- Acceptance Criteria:
  1. [Criterion 1]
  2. [Criterion 2]

## Non-Functional Requirements
### NFR-001: [Title]
- Category: [Performance/Security/Usability]
- Metric: [Measurable target]
- Validation Method: [How to test]

## Technical Constraints
- CakePHP Version: [4.x]
- PHP Version: [8.x]
- Database: [MySQL/PostgreSQL]

## Impact Analysis
- Affected Modules: [list]
- Database Changes: [yes/no - details]
- API Changes: [yes/no - details]
```

## Analysis Process

### Step 1: Initial Requirement Gathering
```
1. Parse user input for key phrases
2. Identify action verbs (create, update, delete, view)
3. Identify entities (user, application, order)
4. Identify conditions (when, if, unless)
```

### Step 2: Requirement Categorization
```
Functional:
- CRUD operations
- Business logic
- Workflow steps
- Integration points

Non-Functional:
- Performance (response < 2s)
- Security (authentication required)
- Usability (mobile responsive)
- Reliability (99.9% uptime)
```

### Step 3: CakePHP Mapping
```
Requirement → CakePHP Component:
- "User can login" → AuthComponent/AuthenticationPlugin
- "Send email notification" → Mailer class
- "Generate PDF report" → Plugin integration
- "Real-time updates" → WebSocket/Ajax polling
```

### Step 4: Database Impact Assessment
```
New Entity? → New Table + Migration
New Relationship? → Foreign Key + Association
New Field? → Migration + Fixture Update
Multi-tenant? → Company-specific DB consideration
```

## Output Examples

### Example 1: User Authentication Requirement
```yaml
Requirement:
  id: REQ-001
  type: functional
  priority: high
  description: "Users must be able to login with email and password"

  acceptance_criteria:
    - Valid credentials allow access
    - Invalid credentials show error
    - Account lockout after 5 failed attempts
    - Session timeout after 30 minutes

  technical_mapping:
    controller: UsersController::login()
    component: AuthenticationPlugin
    table: users
    fields: [email, password, login_attempts, last_login]

  impact_analysis:
    database_changes:
      - Add login_attempts field
      - Add last_login timestamp
    api_changes:
      - POST /api/auth/login
      - POST /api/auth/logout
```

### Example 2: Reporting Requirement
```yaml
Requirement:
  id: REQ-002
  type: functional
  priority: medium
  description: "Generate monthly sales report in PDF format"

  acceptance_criteria:
    - Report includes all transactions for selected month
    - PDF format with company branding
    - Downloadable and emailable

  technical_mapping:
    controller: ReportsController::monthlySales()
    component: Custom PDF generator
    tables: [orders, order_items, products]
    plugin: CakePdf

  performance_requirements:
    - Generation time < 10 seconds
    - Support up to 10,000 records
```

## Integration Points

### With Other Skills:
- **functional-designer**: Receives analyzed requirements
- **test-case-designer**: Uses requirements for test planning
- **database-designer**: Gets schema requirements

### With Agents:
- **requirements-analyst-agent**: Orchestrates analysis workflow
- **project-manager-agent**: Tracks requirement completion

## Quality Criteria

**Good Requirement:**
- Specific and measurable
- Achievable within constraints
- Relevant to business goals
- Time-bound with clear deadline

**Poor Requirement:**
- Vague: "System should be fast"
- Unmeasurable: "User-friendly interface"
- Over-specified implementation: "Use specific algorithm X"

## Common Patterns

### CRUD Requirements
```
Standard pattern for entity management:
1. List (index) - Paginated, sortable, filterable
2. View (view) - Detailed display
3. Create (add) - Form with validation
4. Update (edit) - Form with current data
5. Delete (delete) - Soft delete with confirmation
```

### Multi-Tenant Requirements
```
Company-specific data isolation:
- Data filtered by company_id
- Separate databases per company
- Cross-company reporting for admins
```

### Workflow Requirements
```
State-based progression:
- Draft → Submitted → Approved → Completed
- Each transition has validators
- Notifications at each stage
- Audit trail required
```

## Best Practices

1. **Start with Why**: Understand business value before technical details
2. **Be Specific**: Avoid ambiguous terms
3. **Consider Edge Cases**: What happens when things go wrong?
4. **Think Iteratively**: Requirements can evolve
5. **Validate Early**: Confirm understanding with stakeholders

Remember: Good requirements are the foundation of successful development. Invest time here to save time later.