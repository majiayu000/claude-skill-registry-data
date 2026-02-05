---
name: MCP Go-Live
description: Guide developers through Intility's production go-live checklist for MCP servers, ensuring security compliance with the lethal trifecta rules, Intility Software Engineering Policy, and infrastructure requirements. Use when a developer is ready to deploy an MCP server to production.
---

# MCP Go-Live Production Checklist

This skill guides developers through Intility's production go-live process for MCP servers, ensuring security, compliance, and operational readiness.

## When to Use This Skill

Use this skill when a developer is ready to deploy an MCP server to production at Intility. This skill will guide them through a systematic validation and setup process.

## How This Skill Works

This skill uses **progressive disclosure** - you will load only the minimal information needed at each phase rather than overwhelming the developer with all requirements upfront.

## Skill Organization

Guide the developer through each phase systematically, loading the relevant file for each phase:

### Phase 1: Security Assessment
**File:** `security/lethal-trifecta-check.md`

Validate that the MCP server complies with lethal trifecta security rules:
- Access to private data: OBO only ✓
- Untrusted content: NOT in LLM context ✗
- External communication: NONE ✗

**CRITICAL:** If the MCP server combines all three lethal trifecta elements, STOP immediately and require redesign before proceeding.

### Phase 2: Policy Compliance
**File:** `security/intility-policy-check.md`

Verify compliance with Intility Software Engineering Policy covering:
- Source code repository and documentation
- Release management and code review
- Testing with test/mock data only
- Environment separation
- Security scanning
- Zone Model compliance

### Phase 3: Infrastructure Setup
**Files:** `infrastructure/envoy-gateway-setup.md`, `infrastructure/audit-logging-config.md`

Guide the developer through:
- Envoy Gateway API installation with proper security contexts
- Audit logging configuration

### Phase 4: Authentication Validation
**File:** `authentication/obo-validation.md`

Verify On-Behalf-Of (OBO) authentication implementation:
- No API keys or service principals
- Data access scoped to logged-in user
- Data filtering enforced based on identity

### Phase 5: Observability Setup
**File:** `observability/logfire-setup.md`

Ensure OpenTelemetry instrumentation is configured:
- Traces sent to Intility's Logfire instance
- Proper span attributes
- Monitoring dashboard created

### Phase 6: Final Verification
**File:** `templates/go-live-report.md`

Generate a production readiness report documenting:
- All completed checklist items
- Configuration used
- Approval and timestamp

## Instructions for Claude

1. **Start by asking** which phase the developer is in, or if they want to start from the beginning
2. **Load ONLY** the relevant file for the current phase (use the Read tool)
3. **Guide the developer** through validation and setup for that phase
4. **Mark completion** before moving to the next phase
5. **Use checkboxes** to track progress through each phase
6. **Generate the final report** when all phases are complete

## Important Constraints

- Never skip the security assessment phase
- Block progression if critical security requirements are not met
- All commands should be shown for developer to execute (don't auto-execute destructive operations)
- Ask validation questions from each file to confirm understanding
- Keep the developer informed of progress throughout

## Example Interaction Start

```
Developer: I need to deploy my MCP server to production

You: I'll guide you through Intility's MCP go-live checklist to ensure your
server meets all security and compliance requirements.

We'll go through 6 phases:
1. Security Assessment (Lethal Trifecta)
2. Policy Compliance
3. Infrastructure Setup
4. Authentication Validation
5. Observability Setup
6. Final Verification

Have you already started any of these phases, or shall we begin with
Phase 1: Security Assessment?
```

## Red Flags to Watch For

If you detect any of these, STOP and address immediately:
- ❌ All three lethal trifecta elements present
- ❌ Production data used in development/testing
- ❌ API keys or service principals instead of OBO
- ❌ Missing CI/CD pipeline
- ❌ No security scanning
- ❌ Prohibited MCP content types (audio, images, resource links)
