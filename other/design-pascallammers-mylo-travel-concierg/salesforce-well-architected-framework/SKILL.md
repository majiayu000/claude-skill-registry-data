---
name: Salesforce Well Architected Framework
description: This skill should be used when the user asks to "design a package", "architect a solution", "check well architected", "validate against well architected framework", "review architecture", or mentions any of the five pillars (Trusted, Easy, Adaptable, Composable, Connected). Provides comprehensive guidance for designing Salesforce managed packages following the Well Architected Framework.
version: 0.1.0
---

# Salesforce Well Architected Framework

## Overview

The Salesforce Well Architected Framework provides architectural principles and best practices for building high-quality, scalable, and maintainable solutions on the Salesforce platform. When designing managed packages, apply all five pillars to ensure enterprise-grade solutions.

This skill guides architectural decisions for Salesforce managed packages using the five foundational pillars. Use this framework during initial design, architecture reviews, and validation phases to ensure solutions meet enterprise standards.

## The Five Pillars

### 1. Trusted

Build secure, reliable solutions that protect customer data and maintain platform integrity.

**Core Principles:**
- Security by design
- Data privacy and protection
- Compliance with regulations
- Reliable error handling
- Robust testing coverage

**Key Considerations for Managed Packages:**
- Implement CRUD/FLS checks in all Apex code
- Use `with sharing` appropriately for sharing rules enforcement
- Validate all user inputs to prevent injection attacks
- Encrypt sensitive data at rest and in transit
- Implement comprehensive logging without exposing sensitive data
- Design for graceful degradation when dependencies fail
- Achieve >90% test coverage with meaningful assertions

**Quick Checklist:**
- [ ] All Apex classes declare sharing mode (`with sharing`, `without sharing`, or `inherited sharing`)
- [ ] CRUD/FLS checks before DML operations
- [ ] Input validation for all user-supplied data
- [ ] Error handling with user-friendly messages
- [ ] No hardcoded credentials or sensitive data
- [ ] Audit trail for critical operations
- [ ] Test coverage >90% with edge cases

For detailed security patterns and compliance requirements, consult `references/trusted.md`.

### 2. Easy

Design intuitive, accessible user experiences that maximize adoption and productivity.

**Core Principles:**
- User-centered design
- Accessibility (WCAG 2.1 AA compliance)
- Performance optimization
- Intuitive navigation
- Consistent UX patterns

**Key Considerations for Managed Packages:**
- Follow Lightning Design System (SLDS) guidelines
- Optimize page load times (<3 seconds)
- Implement keyboard navigation and screen reader support
- Provide contextual help and documentation
- Use familiar Salesforce UX patterns
- Design mobile-responsive interfaces
- Minimize clicks to complete tasks

**Quick Checklist:**
- [ ] Lightning Web Components follow SLDS guidelines
- [ ] All interactive elements are keyboard accessible
- [ ] ARIA labels for screen readers
- [ ] Page load time <3 seconds
- [ ] Mobile-responsive design
- [ ] Contextual help available
- [ ] Error messages are actionable

For detailed UX patterns and performance optimization techniques, consult `references/easy.md`.

### 3. Adaptable

Create flexible solutions that evolve with changing business needs and scale with growth.

**Core Principles:**
- Configuration over customization
- Extensibility through APIs
- Bulkified operations for scale
- Governor limit awareness
- Version upgrade compatibility

**Key Considerations for Managed Packages:**
- Design for configurability (Custom Metadata, Custom Settings)
- Expose extension points via global classes/interfaces
- Bulkify all Apex code for large data volumes
- Optimize SOQL queries and avoid N+1 patterns
- Plan for backward compatibility across versions
- Use Platform Events for scalable integrations
- Design asynchronous processing for long-running operations

**Quick Checklist:**
- [ ] No SOQL/DML inside loops
- [ ] Queries use selective filters and indexes
- [ ] Batch/Queueable Apex for bulk operations
- [ ] Custom Metadata for configuration
- [ ] Global extension points documented
- [ ] Upgrade scripts for package updates
- [ ] Asynchronous processing where appropriate

For detailed scalability patterns and governor limit optimization, consult `references/adaptable.md`.

### 4. Composable

Build modular, reusable components that integrate seamlessly with the Salesforce ecosystem.

**Core Principles:**
- Modular architecture
- Separation of concerns
- Reusable components
- Standard APIs and interfaces
- Declarative over programmatic

**Key Considerations for Managed Packages:**
- Apply layered architecture (Service, Domain, Selector layers)
- Create reusable LWC components with clear APIs
- Use standard Salesforce platform features over custom code
- Design for composition (small, focused components)
- Implement standard interfaces (Callable, Queueable, Batchable)
- Expose functionality via Invocable methods for Flow integration
- Use Platform Events for decoupled communication

**Quick Checklist:**
- [ ] Clear separation of concerns (Service/Domain/Selector)
- [ ] Reusable components with well-defined interfaces
- [ ] Invocable Apex methods for Flow integration
- [ ] Platform Events for decoupled integrations
- [ ] Standard Salesforce interfaces used where applicable
- [ ] Declarative configuration options
- [ ] Component composition over monolithic design

For detailed patterns on service layers, domain logic, and selector patterns, consult `references/composable.md`.

### 5. Connected

Enable seamless integrations with external systems and Salesforce ecosystem components.

**Core Principles:**
- API-first design
- Event-driven architecture
- Real-time and batch integration
- Secure authentication
- Monitoring and observability

**Key Considerations for Managed Packages:**
- Design REST APIs for external integrations
- Use Named Credentials for secure authentication
- Implement Platform Events for real-time data flow
- Support both synchronous and asynchronous patterns
- Provide comprehensive API documentation
- Implement retry logic and circuit breakers
- Enable integration monitoring and logging

**Quick Checklist:**
- [ ] REST APIs exposed with clear documentation
- [ ] Named Credentials for external authentication
- [ ] Platform Events for event-driven patterns
- [ ] Callout retry logic implemented
- [ ] Integration error handling and logging
- [ ] API versioning strategy
- [ ] Integration monitoring capabilities

For detailed integration patterns, authentication strategies, and API design guidelines, consult `references/connected.md`.

## Applying the Framework

### During Design Phase

When designing a new managed package, address each pillar systematically:

1. **Start with Trusted**: Define security requirements, compliance needs, and data protection strategies
2. **Design for Easy**: Map user workflows, identify pain points, plan UX improvements
3. **Plan for Adaptable**: Identify scalability requirements, plan for growth, design configuration points
4. **Architect for Composable**: Define component boundaries, establish interfaces, plan reusability
5. **Enable Connected**: Identify integration points, design APIs, plan event-driven flows

### During Architecture Review

Validate existing designs against all five pillars using the decision matrices in `references/decision-matrices.md`. Each pillar should score at least 70% compliance for production readiness.

### Continuous Improvement

Architecture is not static. Regularly reassess solutions against the framework as requirements evolve:

- Review quarterly for emerging patterns
- Update after major Salesforce releases
- Reassess when adding major features
- Validate before each package release

## Decision Framework

When making architectural decisions, use the decision matrices to evaluate tradeoffs across pillars. Common decision points include:

**Build vs. Configure:**
- Trusted: Custom code increases security surface area
- Easy: Configuration is easier for admins
- Adaptable: Configuration enables customer flexibility
- Composable: Platform features promote composition
- Connected: APIs available for both

**Synchronous vs. Asynchronous:**
- Trusted: Async provides retry mechanisms
- Easy: Sync provides immediate feedback
- Adaptable: Async scales better
- Composable: Both patterns have use cases
- Connected: Depends on integration requirements

**Monolithic vs. Modular:**
- Trusted: Smaller modules easier to secure
- Easy: Simpler interfaces with focused modules
- Adaptable: Modules update independently
- Composable: Modularity enables composition
- Connected: Modules integrate via APIs

For detailed decision matrices with scoring frameworks, consult `references/decision-matrices.md`.

## Integration with Package Development

This framework applies throughout the package development lifecycle:

**Discovery & Design:**
- Use framework pillars to structure requirements gathering
- Create architecture diagrams annotated with pillar considerations
- Document architectural decisions and rationale

**Development:**
- Apply pillar principles in code reviews
- Use checklists during implementation
- Validate components against pillar requirements

**Testing:**
- Test coverage validates Trusted pillar
- Performance testing validates Easy and Adaptable
- Integration testing validates Connected

**Release:**
- Architecture validation as release gate
- Document pillar compliance in release notes
- Plan improvements for next version

## Common Anti-Patterns

Avoid these architectural mistakes:

**Trusted Violations:**
- Missing CRUD/FLS checks ("It's an admin page")
- Using `without sharing` by default
- Storing credentials in code or static resources

**Easy Violations:**
- Complex, multi-step processes without progress indicators
- Inconsistent UI patterns across components
- Poor mobile experience

**Adaptable Violations:**
- SOQL queries without `LIMIT` clauses
- Synchronous processing for bulk operations
- No configuration options for customers

**Composable Violations:**
- Business logic in triggers
- Monolithic classes with multiple responsibilities
- Tight coupling between components

**Connected Violations:**
- No API documentation
- Hardcoded integration endpoints
- Missing error handling for callouts

## Additional Resources

### Reference Files

For detailed guidance on each pillar:

- **`references/trusted.md`** - Security patterns, compliance, testing strategies
- **`references/easy.md`** - UX patterns, accessibility guidelines, performance optimization
- **`references/adaptable.md`** - Scalability patterns, governor limits, configuration strategies
- **`references/composable.md`** - Service layer patterns, component design, reusability
- **`references/connected.md`** - Integration patterns, API design, authentication

### Decision Support

- **`references/decision-matrices.md`** - Scoring frameworks for architectural decisions, tradeoff analysis, compliance scoring

### External Resources

Consult official Salesforce Well Architected documentation:
- [Well Architected Framework Overview](https://architect.salesforce.com/well-architected/overview)
- [Trusted Pillar](https://architect.salesforce.com/well-architected/trusted)
- [Easy Pillar](https://architect.salesforce.com/well-architected/easy)
- [Adaptable Pillar](https://architect.salesforce.com/well-architected/adaptable)
- [Composable Pillar](https://architect.salesforce.com/well-architected/composable)
- [Connected Pillar](https://architect.salesforce.com/well-architected/connected)

## Quick Reference

### Pillar Summary

| Pillar | Focus | Key Metric |
|--------|-------|------------|
| Trusted | Security, reliability, compliance | Test coverage >90%, zero security violations |
| Easy | UX, accessibility, performance | Page load <3s, WCAG 2.1 AA compliance |
| Adaptable | Scale, flexibility, configuration | No governor limit violations, bulkified code |
| Composable | Modularity, reusability, standards | Clear separation of concerns, reusable components |
| Connected | Integration, APIs, events | API documentation complete, monitoring enabled |

### When to Use This Skill

Activate this skill when:
- Starting new package design
- Conducting architecture reviews
- Validating package before release
- Making significant architectural decisions
- Responding to scalability or security concerns
- Evaluating build vs. buy decisions

Apply the framework comprehensively for production-grade managed packages that meet enterprise standards.
