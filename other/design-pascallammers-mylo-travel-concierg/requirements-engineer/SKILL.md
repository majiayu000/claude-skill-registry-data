---
name: requirements-engineer
description: Creates requirements catalogs.
---

# Requirements Engineer

## Instructions

Create a requirements catalog document containing functional requirements, non-functional requirements, and constraints
organized as Markdown tables.

## DO NOT

- Mix requirement types in a single table
- Skip the user story format for functional requirements
- Use duplicate IDs across requirement types
- Leave the Status column empty

## Document Structure

# Requirements Catalog

## Functional Requirements

| ID     | Title        | User Story                                                              | Priority | Status |
|--------|--------------|-------------------------------------------------------------------------|----------|--------|
| FR-001 | Feature Name | As a [role], I want [goal] so that [benefit].                           | High     | Open   |

## Non-Functional Requirements

| ID      | Title            | Requirement                                              | Category    | Priority | Status |
|---------|------------------|----------------------------------------------------------|-------------|----------|--------|
| NFR-001 | Requirement Name | System must [measurable quality attribute].              | Performance | High     | Open   |

## Constraints

| ID    | Title           | Constraint                                              | Category   | Priority | Status |
|-------|-----------------|---------------------------------------------------------|------------|----------|--------|
| C-001 | Constraint Name | System must [limitation or boundary].                   | Technical  | High     | Open   |

## Requirement Types

### Functional Requirements (FR)

Define what the system should do. Always use the user story format:

**Format:** As a [role], I want [goal] so that [benefit].

| ID     | Title        | User Story                                                                                | Priority | Status |
|--------|--------------|-------------------------------------------------------------------------------------------|----------|--------|
| FR-001 | Create Task  | As a project manager, I want to create tasks so that I can track work items.              | High     | Open   |
| FR-002 | Assign Task  | As a project manager, I want to assign tasks to team members so that work is distributed. | High     | Open   |
| FR-003 | Filter Tasks | As a team member, I want to filter tasks by status so that I can focus on relevant items. | Medium   | Open   |

### Non-Functional Requirements (NFR)

Define quality attributes. Must be measurable.

| ID      | Title            | Requirement                                                   | Category     | Priority | Status |
|---------|------------------|---------------------------------------------------------------|--------------|----------|--------|
| NFR-001 | Response Time    | All page loads must complete within 2 seconds.                | Performance  | High     | Open   |
| NFR-002 | Availability     | System must maintain 99.9% uptime during business hours.      | Availability | High     | Open   |
| NFR-003 | Concurrent Users | System must support 100 concurrent users without degradation. | Scalability  | Medium   | Open   |
| NFR-004 | Data Encryption  | All data in transit must use TLS 1.3 encryption.              | Security     | High     | Open   |

### Constraints (C)

Define limitations and boundaries imposed on the solution.

| ID    | Title             | Constraint                                                       | Category  | Priority | Status |
|-------|-------------------|------------------------------------------------------------------|-----------|----------|--------|
| C-001 | Runtime Platform  | Backend must run on Java 21 LTS.                                 | Technical | High     | Open   |
| C-002 | Database Platform | System must use PostgreSQL 16.                                   | Technical | High     | Open   |
| C-003 | Browser Support   | UI must support Chrome, Firefox, and Safari (latest 2 versions). | Technical | High     | Open   |
| C-004 | Budget Limit      | Total development cost must not exceed $50,000.                  | Business  | High     | Open   |
| C-005 | Deadline          | System must be production-ready by Q2 2025.                      | Schedule  | High     | Open   |

## ID Prefixes Reference

| Prefix | Type                       | Example |
|--------|----------------------------|---------|
| FR     | Functional Requirement     | FR-001  |
| NFR    | Non-Functional Requirement | NFR-001 |
| C      | Constraint                 | C-001   |

## Priority Reference

| Priority | Description                                         |
|----------|-----------------------------------------------------|
| High     | Must have. Core functionality or critical quality.  |
| Medium   | Should have. Important but system works without it. |
| Low      | Nice to have. Can be deferred to future releases.   |

## Status Reference

| Status      | Description                                    |
|-------------|------------------------------------------------|
| Open        | Requirement defined but not yet implemented.   |
| In Progress | Currently being implemented.                   |
| Implemented | Implementation complete, pending verification. |
| Verified    | Tested and confirmed working.                  |
| Deferred    | Postponed to a future release.                 |
| Rejected    | Removed from scope.                            |

## NFR Categories Reference

| Category        | Description                                   |
|-----------------|-----------------------------------------------|
| Performance     | Speed, throughput, response time              |
| Scalability     | Ability to handle growth                      |
| Availability    | Uptime, fault tolerance                       |
| Security        | Authentication, authorization, encryption     |
| Usability       | User experience, accessibility                |
| Maintainability | Code quality, documentation, modularity       |
| Portability     | Platform independence, deployment flexibility |

## Constraint Categories Reference

| Category    | Description                                   |
|-------------|-----------------------------------------------|
| Technical   | Technology stack, platforms, integrations     |
| Business    | Budget, resources, organizational policies    |
| Schedule    | Deadlines, milestones, time constraints       |
| Regulatory  | Legal, compliance, industry standards         |
| Operational | Deployment, maintenance, support requirements |

## Workflow

1. Read the vision document or project brief
2. Use TodoWrite to create tasks for each requirement type
3. Write the document header
4. For functional requirements:
    - Identify user roles
    - Define user stories with clear goals and benefits
    - Assign priorities based on business value
5. For non-functional requirements:
    - Define measurable quality attributes
    - Categorize by NFR type
    - Ensure requirements are testable
6. For constraints:
    - Document technical and business limitations
    - Categorize by constraint type
7. Review for completeness and consistency
8. Mark todos complete