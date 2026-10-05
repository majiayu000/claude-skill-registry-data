---
name: security
description: Review or implement application security controls using framework-agnostic engineering principles, then adapt them to the detected project stack.
metadata:
  internal: true
---

# Security

Use this skill when a task creates, changes, reviews, or fixes a security-sensitive application boundary.

The rules in this skill are framework and language agnostic.

Do not assume a specific framework, ORM, authentication library, HTTP server, database, queue, cloud provider, or deployment platform.

## Core Principle

Identify the security boundary first.

Then use the safest native mechanism available in the detected project stack.

Technology-specific implementation details should be derived from project evidence, native stack mechanisms, or relevant user-installed specialist skills rather than hardcoded into this skill.

## Security Review Scope

Check only areas relevant to the change.

Primary areas:

- authentication
- authorization
- input validation
- output encoding
- request forgery protection
- injection
- secret handling
- sensitive data exposure
- file uploads
- API security
- rate limiting and abuse protection
- session and token handling
- dependency and configuration security
- logging and error disclosure
- unsafe redirects and outbound requests
- serialization and deserialization
- access to filesystem, network, subprocesses, and other privileged resources

Do not mechanically run every category for every task.

## 1. Trust Boundaries

Treat data crossing a trust boundary as untrusted until validated.

Common boundaries include:

- HTTP requests
- API payloads
- form input
- URL parameters
- headers
- cookies
- uploaded files
- webhooks
- message queues
- database content originating from users
- external APIs
- environment/configuration values
- files
- command-line arguments

Validate as close to the boundary as practical.

Validation should constrain:

- type
- structure
- allowed values
- length
- range
- format
- relationships between fields

Prefer allowlists and explicit schemas over ad-hoc filtering.

Do not rely on frontend validation for server-side security.

## 2. Authentication

Use established authentication mechanisms provided by the project stack.

Do not implement custom password hashing, token signing, session cryptography, or authentication protocols when a trusted implementation exists.

Verify:

- credentials are handled securely
- authentication state cannot be forged
- password storage uses an appropriate adaptive password hash
- session or token rotation is handled where required
- logout/revocation behavior is correct
- authentication failures do not leak unnecessary information

Authentication answers:

"Who is this actor?"

It does not answer:

"May this actor perform this operation?"

## 3. Authorization

Perform authorization on the server side for every protected operation.

Authorize the requested action against the actual target resource.

Check authorization before performing sensitive state changes.

Protect against:

- insecure direct object references
- horizontal privilege escalation
- vertical privilege escalation
- tenant boundary bypass
- ownership bypass
- administrator-only operation exposure

Prefer centralized authorization mechanisms provided by the project stack.

Do not spread inconsistent role checks throughout business code when a policy/permission mechanism exists.

## 4. Injection

Never construct executable commands or queries by concatenating untrusted input.

Use appropriate parameterization or structured APIs for:

- database queries
- shell commands
- templates
- directory/LDAP queries
- search expressions
- dynamic code execution

Avoid evaluating user-controlled code or expressions.

Treat escaping as context-specific.

Escaping for HTML is not equivalent to escaping for SQL, shell, JavaScript, URLs, or another interpreter.

## 5. Output Encoding

Encode or escape untrusted data for the destination context.

Pay special attention to:

- HTML
- HTML attributes
- JavaScript
- URLs
- CSS
- templates
- generated documents

Prefer rendering systems that escape output by default.

Avoid disabling automatic escaping unless the value is known to be safe for that exact output context.

## 6. Request Forgery

For state-changing browser requests authenticated by ambient credentials such as cookies, use the framework/platform's request-forgery protection.

Do not disable protection globally to fix an integration problem.

For machine-to-machine callbacks or webhooks, use an authentication mechanism appropriate to that boundary, such as:

- signed requests
- authenticated tokens
- mutual authentication
- provider verification mechanisms

Do not confuse webhook signature verification with browser CSRF protection.

## 7. Rate Limiting and Abuse Protection

Apply rate limits where abuse can cause meaningful harm.

Examples:

- login attempts
- password reset
- verification codes
- expensive searches
- public APIs
- file processing
- resource creation
- messaging endpoints
- authentication/token endpoints

Choose limits based on risk and expected traffic.

Avoid using one global limit for unrelated workloads.

Rate limiting is not a replacement for authorization or validation.

## 8. File Uploads

Treat uploaded files as hostile.

Validate:

- size
- expected media/type
- extension when relevant
- actual content when relevant
- filename handling
- storage location
- access permissions

Generate server-controlled storage names where possible.

Do not trust the client-provided filename or content type.

Prevent path traversal.

Avoid storing executable uploads in locations where the application server can execute them.

Keep public/private storage semantics explicit.

## 9. Secrets

Never hardcode production secrets in source code.

Do not expose secrets through:

- logs
- exception messages
- responses
- telemetry
- screenshots
- generated artifacts
- version control

Use the project's supported secret/configuration mechanism.

Differentiate:

- public identifiers
- configuration
- credentials
- cryptographic secrets

Rotate credentials when exposure is suspected.

## 10. API Security

For APIs, verify:

- authentication where required
- authorization per resource/action
- strict request validation
- bounded pagination and query parameters
- safe error responses
- rate limits where appropriate
- replay protection where required
- idempotency where duplicate execution is dangerous
- secure token handling

Do not expose internal implementation details in error payloads.

## 11. Outbound Requests / SSRF

Treat user-influenced destinations as security-sensitive.

When the application performs outbound requests:

- restrict allowed destinations where practical
- validate scheme and host
- reject unsafe protocols
- consider redirects
- protect internal/private network destinations
- apply timeouts
- bound response size where appropriate

Do not fetch arbitrary URLs supplied by users without explicit safeguards.

## 12. Sessions and Tokens

Use mature platform mechanisms for session and token management.

Verify:

- expiration
- rotation
- revocation where required
- secure transport
- storage
- audience/scope where relevant
- signature/validation rules
- replay considerations

Do not decode a token and treat its claims as trusted without performing the required validation.

## 13. Sensitive Data

Collect and return only data needed by the operation.

Avoid accidental disclosure through:

- serializers
- debug output
- logs
- stack traces
- API responses
- analytics
- error pages

Explicitly control fields returned across external boundaries when sensitive models contain additional internal data.

## 14. Errors and Logging

Errors exposed to users should contain enough information to act on the failure without revealing sensitive internals.

Avoid exposing:

- stack traces
- credentials
- tokens
- database details
- filesystem paths
- internal network details
- secrets
- unnecessary personal data

Security-relevant failures may be logged when useful, but logs must not become a secret-leak channel.

## 15. Configuration

Prefer secure defaults.

Check environment-sensitive settings such as:

- debug mode
- error display
- cookie/session security
- trusted proxies/hosts
- cross-origin policy
- storage permissions
- transport security
- credential loading

Development convenience must not silently weaken production security.

## 16. Dependencies

Prefer maintained security-critical dependencies.

Do not introduce a new security dependency when the current stack already provides the required capability.

When changing dependencies, consider:

- known vulnerabilities
- abandoned packages
- unnecessary privileges
- transitive risk
- lockfile consistency

## 17. Cryptography

Do not design custom cryptographic protocols.

Use established implementations.

Use cryptographically secure randomness for security-sensitive values.

Do not substitute ordinary hashes for password hashing.

Do not invent encryption formats when a well-reviewed platform mechanism exists.

## Verification

Security verification should be proportional to the changed boundary.

Useful checks may include:

- unauthorized actor denied
- authorized actor allowed
- malformed input rejected
- ownership/tenant isolation preserved
- forged requests rejected
- invalid signatures rejected
- dangerous upload rejected
- rate limit enforced
- secret not exposed
- sensitive response fields absent
- unsafe destination rejected
- expected valid flow still works

Prefer focused tests over broad unrelated rewrites.

## Framework Adaptation

After identifying the required control:

1. Detect the actual project language/framework from project evidence.
2. Inspect the current project stack and available relevant specialist skills.
3. Translate the control into established native framework or language mechanisms using repository evidence.
4. When stack-specific guidance is unavailable, prefer mechanisms already established by the project.
5. Never invent a framework API.
6. Never weaken the universal security requirement merely because a convenience API is unavailable.

The core requirement remains authoritative.

Technology-specific guidance only explains how the current stack implements it; the security requirement remains stack-independent.
<!-- ENGINEER_FLOW_SECURITY_ASSESSMENT_V1 -->

## Active Application Security Assessment

This security core is both a secure-development guide and a
post-development security review gate.

Use it for authorized review of applications, services, APIs,
changesets, pull requests, and code produced during development.

The goal is to identify exploitable weaknesses, provide evidence,
recommend the smallest correct remediation, and verify the fix.

Do not perform destructive exploitation, persistence, credential theft,
lateral movement, denial-of-service, or actions beyond the authorized
application and environment.

## Review Strategy

Prefer evidence over speculation.

When version-control context is available:

1. inspect the changed files and diff first
2. identify affected trust boundaries and entry points
3. inspect reachable surrounding code
4. follow data from source through transformations to sensitive sinks
5. determine whether existing controls actually prevent exploitation
6. verify remediation after changes are applied

Do not report a vulnerability solely because a dangerous API or pattern
exists. Establish reachability, attacker influence, missing control,
and meaningful impact whenever practical.

## Stack Discovery

Before applying technology-specific assumptions, determine from project
evidence:

- language
- framework
- framework/runtime version
- package manager
- authentication mechanism
- persistence layer
- exposed interfaces
- deployment/runtime characteristics relevant to security

The core remains framework agnostic.

If a matching adapter exists, use it only to translate these requirements
into native framework mechanisms.

## Attack Surface and Trust Boundaries

Identify relevant externally influenced surfaces, including:

- HTTP routes and API endpoints
- form and query input
- headers and cookies
- uploaded files
- webhook payloads
- external API responses
- message/event consumers
- command or job input
- import files
- authentication state
- authorization context
- database-derived content that originally came from untrusted users

Identify sensitive sinks such as:

- database queries
- operating-system commands
- template/rendering output
- filesystem access
- outbound network requests
- redirects
- authentication/session state
- authorization decisions
- serialization/deserialization
- secrets
- logs
- privileged business operations

Trace relevant flows as:

source -> validation/transformation -> authorization -> sink

## Required Security Checks

### Authentication

Review:

- authentication bypass
- insecure account recovery
- session lifecycle
- token lifecycle
- credential handling
- session fixation
- insecure remember-me behavior
- missing invalidation where required

### Authorization

Verify authorization at the operation and resource boundary.

Check for:

- IDOR / broken object-level authorization
- privilege escalation
- missing tenant or ownership checks
- authorization performed only in the UI
- role checks that do not protect the underlying resource

Authentication alone is never sufficient authorization.

### Injection

Review attacker-controlled data reaching interpreters or query builders.

Consider:

- SQL/query injection
- command injection
- expression injection
- template injection
- header injection
- unsafe dynamic evaluation

Prefer parameterization and native safe APIs.

### Output and XSS

Review untrusted data rendered into:

- HTML
- attributes
- script contexts
- URLs
- other executable contexts

Use context-appropriate output encoding.

Avoid disabling safe escaping without explicit justification.

### Request Forgery

For state-changing browser requests, verify appropriate anti-forgery
protections where the authentication model requires them.

Do not rely only on request method or frontend behavior.

### SSRF and Outbound Requests

Treat attacker-influenced destinations as a security boundary.

Review:

- URL parsing
- protocol restrictions
- redirect following
- private/internal address access
- cloud metadata access
- DNS rebinding considerations
- credential forwarding

Prefer explicit destination allowlists when the business flow permits it.

### Files and Paths

For uploads, downloads, archives, and filesystem access review:

- filename trust
- path traversal
- extension versus actual content
- MIME/content validation
- size limits
- storage location
- executable files
- overwrite behavior
- archive extraction paths
- authorization for file retrieval

Generate server-side storage names when appropriate.

### Secrets and Tokens

Never intentionally expose secrets through:

- source control
- API responses
- frontend bundles
- exception pages
- logs
- diagnostic output

Use environment or platform secret facilities appropriate to the stack.

### APIs and Data Exposure

Review:

- excessive fields
- mass assignment / unintended writable fields
- enumeration
- missing authorization
- unsafe pagination
- unbounded responses
- verbose errors
- internal identifiers or metadata exposed unnecessarily

Return only data required by the consumer.

### Rate Limiting and Resource Abuse

Review expensive or abuse-prone operations such as:

- authentication
- password recovery
- OTP or verification
- search
- exports
- uploads
- AI/model calls
- external API calls
- bulk operations

Consider:

- rate limits
- bounded pagination
- input size
- query complexity
- execution time
- concurrency
- memory consumption

Do not use load generation or denial-of-service techniques as part of a
normal security review.

### Webhooks and Machine-to-Machine Requests

Where relevant verify:

- authenticity
- signature validation
- timestamp or freshness
- replay protection
- duplicate delivery handling
- idempotency
- secret handling
- authorization of resulting side effects

### Logging and Error Handling

Logs must contain enough evidence for operations without leaking:

- passwords
- session identifiers
- access tokens
- API keys
- private cryptographic material
- unnecessary personal or sensitive data

Do not expose internal stack traces or implementation details to
untrusted clients in production environments.

### Dependencies and Configuration

Review relevant risks from:

- vulnerable dependencies
- unsupported versions
- unsafe defaults
- debug/development configuration
- overly broad permissions
- exposed administrative interfaces
- insecure transport configuration
- accidentally committed secrets

A dependency finding should be tied to the version actually used by the
project.

### Cryptography

Do not design custom cryptography when established platform mechanisms
exist.

Review:

- obsolete algorithms
- weak randomness
- hard-coded keys
- insecure key storage
- incorrect encryption/signing usage

## Dynamic Verification

When an authorized test or staging environment exists, static findings
may be verified dynamically.

Dynamic verification should be:

- minimal
- reproducible
- non-destructive
- scoped to the suspected vulnerability
- sufficient to establish whether the weakness is exploitable

Do not escalate beyond the evidence needed to validate the issue.

If dynamic verification is unavailable, state the limitation instead of
inventing exploitability evidence.

## Evidence Standard

A confirmed finding should describe, where applicable:

- affected component
- attacker-controlled source
- relevant execution path
- sensitive sink or security decision
- missing or ineffective control
- realistic impact
- reproducible evidence
- remediation
- verification method

Distinguish between:

- confirmed vulnerability
- likely vulnerability requiring verification
- defensive improvement / hardening
- informational observation

Do not inflate hardening recommendations into confirmed vulnerabilities.

## Severity

Prioritize findings using exploitability and impact together.

Typical levels:

- CRITICAL: realistic path to severe compromise with little additional
  prerequisite
- HIGH: significant confidentiality, integrity, authorization, or
  privileged-operation impact
- MEDIUM: exploitable weakness with meaningful but constrained impact
- LOW: limited-impact weakness or defense-in-depth issue

Severity must follow evidence, not vulnerability names alone.

## Remediation

Prefer the smallest fix that removes the root cause.

Remediation should:

1. protect the correct trust boundary
2. use native safe mechanisms when available
3. preserve intended application behavior
4. include regression protection when practical

Avoid broad rewrites when a targeted correction is sufficient.

## Re-Test

After remediation:

1. repeat the original security check
2. verify the vulnerable path is no longer exploitable
3. verify intended behavior still works
4. verify nearby equivalent paths when warranted

A finding is not considered resolved solely because code changed.

## Security Review Output

At the end of a dedicated security review, provide concise findings with:

- severity
- location
- evidence
- impact
- remediation
- verification status

Finish with exactly one gate result:

`SECURITY REVIEW: PASS`

Use PASS when no actionable confirmed security issue remains within the
reviewed scope.

Or:

`SECURITY REVIEW: NEEDS_FIX`

Use NEEDS_FIX when one or more actionable security issues remain.

When review coverage is materially incomplete, explicitly state the
coverage limitation before the gate result.

<!-- /ENGINEER_FLOW_SECURITY_ASSESSMENT_V1 -->

## Bundled Resources

This skill may include reusable resources in its own directory.

### Security Gate

For commit-aware or staged-diff security review, use:

`scripts/security-gate.mjs`

An optional Git hook installer is available at:

`scripts/install-security-gate.ps1`

Use these helpers only when the execution environment supports them.

The security analysis rules in this SKILL.md remain usable even when the helper scripts cannot be executed.

### Framework References

Framework-specific implementation guidance may exist under:

`references/`

Before using one:

1. detect the project's actual framework from repository evidence
2. load only the matching reference
3. keep this security core authoritative

If no matching reference exists, continue using the framework-agnostic security requirements.

Do not assume a framework merely because a framework reference is bundled with this skill.
