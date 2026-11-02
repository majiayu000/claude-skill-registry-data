---
name: ssrf-boundary-review
description: Review server-side URL fetching and webhook integrations for SSRF boundaries, redirect handling, DNS rebinding, and egress restrictions.
---

# Ssrf Boundary Review

## Goal

Ensure user-controlled or third-party URLs cannot reach privileged internal services or unintended network destinations.

## Inputs to inspect

URL fetch code, webhook endpoints, DNS/redirect behavior, network policies, allowed schemes/hosts, and service deployment topology.

## Workflow

1. Inventory every server-side HTTP fetch where URLs or hostnames may be influenced by users, imported documents, callbacks, or third-party data.
2. Define allowed schemes, ports, hostnames, and destination classes; reject ambiguous parsing, embedded credentials, unsupported protocols, and disallowed IP ranges.
3. Validate all resolved addresses and revalidate after redirects; consider DNS changes/rebinding and block link-local, loopback, private, metadata, and privileged internal ranges as appropriate to deployment.
4. Enforce network-level egress restrictions and response size/time limits so application checks are not the only barrier.
5. Test redirect chains, IPv4/IPv6 representations, unusual encodings, DNS changes, oversized bodies, timeouts, and allowed legitimate webhook cases in an isolated environment.

## Validation checklist

- [ ] URL parsing and validation use a well-defined canonical representation.
- [ ] Redirect destinations are revalidated against the same policy.
- [ ] Private/metadata/internal destinations are blocked according to the deployment threat model.
- [ ] Egress policy limits blast radius if application validation fails.
- [ ] Timeout, response-size, and content-type limits prevent resource exhaustion.

## Required output

Deliver a URL-fetch inventory, allow/deny contract, redirection/DNS test matrix, confirmed gaps, and layered remediation plan.

## Boundaries and failure handling

Do not run probes against real metadata endpoints or third-party systems without authorization; do not treat a hostname allowlist as sufficient if redirects bypass it.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
