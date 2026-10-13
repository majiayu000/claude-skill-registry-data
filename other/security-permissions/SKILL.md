---
name: security-permissions
description: 'Apply backend security controls for HIVMeet endpoints. Use for permission design, object ownership checks, premium feature gating, rate limiting, PII-safe logging, and sensitive data exposure prevention.'
argument-hint: 'Describe endpoint/action, actor roles, protected resources, and current security concern.'
user-invocable: true
---

# Security and Permissions

## Purpose
Reduce security and privacy risk in a sensitive healthcare-adjacent social product by enforcing strict access control and safe defaults.

## Use When
- Adding/modifying protected endpoints
- Implementing custom permissions
- Reviewing sensitive field exposure
- Designing rate limits and abuse controls

## Mandatory Workflow

### 1. Access Matrix Definition
- Identify actors: anonymous, authenticated, owner, matched user, premium user, admin
- Identify resources and allowed actions by actor
- Define deny-by-default policy

### 2. Permission Implementation
- Endpoint-level permission classes (IsAuthenticated, custom classes)
- Object-level permission checks for owner/match constraints
- Premium feature checks with expiration awareness

### 3. Abuse Mitigation
- Apply rate limiting to high-risk endpoints (login, register, messaging)
- Ensure deterministic 429 behavior and retry hints when available
- Validate large payload and spam pathways

### 4. Privacy Review
- Ensure serializers do not expose sensitive fields by default
- Ensure logs do not include PII/secrets/tokens/medical details
- Ensure user-facing errors do not leak internal state

### 5. Security Headers and Runtime Posture
- Verify relevant production settings for HTTPS and secure cookies
- Validate CORS is explicit and environment-appropriate
- Validate JWT handling rules in endpoints touching auth/session

### 6. Auditability
- Add or verify audit log events for critical actions
- Include actor, action, timestamp, and safe context fields
- Keep audit data minimally sufficient and privacy-aware

### 7. Validation and Output
1. Threat model summary
2. Permissions and controls applied
3. Exposure risks closed
4. Abuse controls and expected responses
5. Residual risk and follow-up actions

## Quality Gates
- No protected endpoint without explicit authz strategy
- No critical action without audit traceability
- No PII leak in logs introduced by the change
