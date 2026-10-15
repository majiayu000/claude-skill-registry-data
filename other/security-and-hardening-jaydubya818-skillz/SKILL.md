---
name: security-and-hardening
description: "Review security or harden sensitive trust boundaries with abuse-case tests."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: high
  capabilities: addyosmani,security-and-hardening
---

# Security and hardening

Use this workflow for requested security reviews or changes to sensitive trust
boundaries. Scope the review to the actual system and requested work. Ordinary
copy edits do not require a full audit.

## Trace the trust boundary

Identify the assets, actors, privileges, untrusted inputs, and consequential
operations. Trace who can write each value, including files, queue payloads,
provider responses, and model output. Local origin does not imply trust.
Write concrete abuse cases for the relevant boundary before choosing controls.

## Check the controls that apply

- Authorize the actor against the resource and tenant on every protected
  operation, including background actions and replay paths. Authentication
  alone is insufficient. Test another user's and another tenant's identifiers.
- Validate bounded input and permitted state transitions server-side. Use
  parameterized queries and structured process arguments. Encode output for
  its destination; sanitize allowed rich content with a maintained sanitizer.
- Follow the framework's current session, password-storage, and CSRF guidance.
  Cookie flags, CORS, and SameSite settings are separate controls, not proof
  that all cross-site requests are safe. Preserve legitimate auth redirects.
- Keep secrets out of source, public errors, telemetry, and model context.
  Review response field allowlists and tenant partitioning. If credentials
  are exposed, report the exposure without repeating them; coordinate rotation
  within granted authority. Do not silently rewrite shared Git history.
- Bound upload sizes, validate permitted content, and isolate storage and
  serving behavior. A filename extension or client MIME type is not evidence
  of safe content. Check tenant ownership on later downloads too.
- For server-side URL fetches, constrain schemes, destinations, redirects,
  response size, and time. Block internal and metadata targets, including IPv6
  and DNS-rebinding paths. Prefer the platform's tested egress controls over
  a homegrown URL regex.
- For derived filesystem targets, verify allowed scope and ownership with
  operations that address symlink races. Resolving a path and checking it once
  is insufficient when an attacker can replace it before the write or delete.
- Check webhook signatures using the provider's documented raw-body procedure,
  timestamp/replay rules, and event identity. Use duplicate-safe processing.
  Apply bounded retries and rate limits across the actual deployment topology.
- Inspect dependency changes, lockfiles, provenance, and install scripts. Use
  supported audits and review reachable findings. A clean advisory scan does
  not prove a dependency is safe; do not apply forced upgrades blindly.
- Enforce model/tool permissions in code. Retrieved instructions and generated
  arguments are untrusted data, even when the model expresses confidence.

## Privacy and scope

Collect fields for a stated purpose and define access, retention, deletion,
and recovery handling for each store. Include caches, exports, analytics, and
backups in the data map. Follow the organization's approved retention and legal
holds; do not promise immediate deletion from immutable backups or invent a
universal legal consent rule. Escalate unresolved policy decisions with the
concrete data flow that needs a decision.

Use existing task authorization for requested fixes. This skill grants no new
authority to scan third-party systems, change production roles, export real
customer data, rotate credentials, or publish a finding externally.

## Verify and report

Use controlled fixtures to prove both allowed and denied behavior. Reproduce
reported issues and test the fix at the real boundary, including cross-tenant,
replay, malformed-input, and concurrency cases where relevant. Prefer precise
findings with location, impact, preconditions, evidence, and a scoped fix over
generic checklists. Separate observed vulnerabilities from unverified concerns.

Record checks run, unavailable evidence, and residual risk. Claim only the
scope reviewed; passing an audit tool is not a security or compliance certificate.
