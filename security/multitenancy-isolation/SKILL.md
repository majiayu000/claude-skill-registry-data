---
name: multitenancy-isolation
version: "1.0.0"
description: Application multitenancy isolation and availability/DoS resilience for mid-2026 — principal-bound tenant identity, data-layer row-level-security under a non-bypass role, cross-tenant cache/queue namespacing, per-tenant rate/byte quotas, HTTP/2 Rapid Reset caps, bounded allocation, distributed-lock fencing, and circuit breakers
triggers:
  - multitenancy isolation
  - multi tenant
  - cross tenant
  - tenant isolation
  - row level security
  - rls
  - bola
  - broken object level authorization
  - idor
  - noisy neighbour
  - rapid reset
  - rate limit
  - per tenant quota
  - circuit breaker
  - distributed lock fencing
  - resource exhaustion
  - denial of service
discovery_mode: standalone
data_deps:
  - cve-catalog.json
  - atlas-ttps.json
  - attack-techniques.json
  - framework-control-gaps.json
  - cwe-catalog.json
  - rfc-references.json
atlas_refs: []
attack_refs:
  - T1078
  - T1499
  - T1499.001
  - T1530
framework_gaps:
  - NIST-800-53-AC-3
  - NIS2-Art21-network-security
  - UK-CAF-B4
  - AU-ISM-1268
cwe_refs:
  - CWE-639
  - CWE-770
  - CWE-863
  - CWE-668
  - CWE-400
last_threat_review: "2026-06-02"
---

# Application Multitenancy Isolation + Availability/DoS Resilience

## Threat Context (mid-2026)

Shared multitenant infrastructure has two linked failure classes. Isolation: if the tenant identifier is trusted from a client-controlled header/parameter/claim, or the tenant filter lives in per-query application discipline rather than the data layer, a single authenticated user of one tenant reads or writes another tenant's data — broken object-level authorization (CWE-639), the most common and highest-impact SaaS vulnerability class. Cache, pub/sub, and queue keys leak the same way when not tenant-namespaced. Availability: asymmetric denial of service — HTTP/2 Rapid Reset (CVE-2023-44487), unbounded per-request allocation — and the noisy-neighbour pattern (no per-tenant quota) deny service to all tenants; autoscaling pays the attacker's bill without stopping the attack.

## Framework Lag Declaration

Organisational controls treat "we have an authorization layer" as tenant isolation and "the cloud autoscales" as DoS resilience. NIST 800-53 AC-3 (access enforcement) is satisfied by an authorization layer existing and does not require tenant scoping be structurally enforced at the data layer rather than per-query discipline. SC-6 (resource availability) is named but rarely operationalised as per-tenant quotas, Rapid Reset caps, or circuit breakers. SOC 2 CC6 logical access is met with an auth layer. A clean "we have authorization and the cloud autoscales" audit is therefore NON-EVIDENCE for multitenancy isolation or DoS resilience; it confirms an auth layer and elastic infra, not data-layer RLS under a non-bypass role, cross-tenant namespacing, per-tenant quotas, or breakers.

## TTP Mapping

The multitenancy failures map to MITRE ATT&CK: **T1078 (Valid Accounts)** for cross-tenant access from a legitimate account via a client-trusted tenant id, an unscoped query, or an RLS-bypassing request role; **T1530 (Data from Cloud Storage / shared store)** for cross-tenant leakage through un-namespaced cache/queue keys; **T1499 (Endpoint DoS)** for the noisy-neighbour, distributed-lock, and circuit-breaker gaps; and **T1499.001 (OS Exhaustion Flood)** for HTTP/2 Rapid Reset and unbounded per-request allocation. The weakness classes are CWE-639 (authorization bypass through user-controlled key), CWE-863 (incorrect authorization), CWE-668 (exposure to wrong control sphere — shared keys), CWE-770 (allocation without limits), and CWE-400 (uncontrolled resource consumption).

## Exploit Availability Matrix

These are application-posture gaps exploited from a single authenticated account or client, so the exploit is the absent control. Cross-tenant access via a client-trusted tenant id requires only changing a header — trivially scriptable and the staple of SaaS bug-bounty reports. HTTP/2 Rapid Reset has public tooling and the CVE-2023-44487 catalog entry; it produced record-breaking DDoS. Unbounded allocation and the noisy-neighbour DoS require only a crafted or high-volume request. The real-world priority is set by whether one authenticated user can reach all tenants' data, or one client can deny service to all tenants — both maximum-blast-radius outcomes on shared infrastructure.

## Analysis Procedure

1. Determine the effective tenant id derivation and confirm it binds to the authenticated principal, not a client-supplied field. 2. Confirm tenant scoping is enforced at the data layer (row-level security) and that the request connection runs under a role SUBJECT to RLS (not a BYPASSRLS/owner role). 3. Confirm cache/pub-sub/queue keys include the tenant id. 4. Confirm HTTP/2 client-initiated stream resets are capped per connection (Rapid Reset). 5. Confirm per-tenant/per-IP rate + byte quotas and bounded per-request allocation (result-set, body, connections, fan-out). 6. Confirm distributed locks carry a TTL + fencing token and critical dependencies have circuit breakers. Run the `multitenancy-isolation` playbook to execute these as detect indicators with false-positive checks, then score by whether one account reaches all data or one client denies all service.

## Output Format

Report per surface, marking each isolation and availability control enforced / missing / inconclusive (visibility gap). For every missing control, state whether a single authenticated user could read another tenant's data or a single client could deny service to all tenants. Distinguish a control enforced at a lower layer (data-layer RLS, CDN/WAF quotas) from an absent one, and a dedicated single-tenant deployment (cross-tenant indicators not applicable) from a shared one. Provide the prioritised remediation (bind tenant to principal + data-layer RLS under a non-bypass role, namespace shared keys, cap Rapid Reset + per-tenant quotas, bound allocation, fence locks + circuit-break) and the negative validation tests (cross-tenant read blocked, unscoped query blocked, Rapid Reset capped) plus a functional test that two tenants get fair, isolated service.

## Compliance Theater Check

The recurring theater is "we have an authorization layer, so tenants are isolated," "row-level security is enabled," and "the cloud autoscales, so we are DoS-resilient." An auth layer is not data-layer isolation; RLS is bypassed by a superuser/owner/BYPASSRLS request connection; autoscaling pays the attacker's bill without stopping an asymmetric DoS. The distinguishing test: probe whether a query can run without a tenant predicate, whether the request connection bypasses RLS, whether the tenant id is client-trusted, and whether Rapid Reset / unbounded allocation is capped. If a cross-tenant read or an asymmetric DoS succeeds, the auth layer and autoscaling did not isolate or protect, and the assurance is paper.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: principal-bound tenant id + data-layer RLS under a non-bypass role realise Authorization Event Thresholding and Mandatory Access Control (countering T1078 cross-tenant access); tenant-namespaced shared keys realise Resource Access Pattern isolation (countering T1530 leakage); per-tenant quotas + HTTP/2 Rapid Reset caps + bounded allocation realise Resource Consumption Limiting (countering T1499/T1499.001); distributed-lock fencing and circuit breakers realise System Availability and Failure-Domain isolation. Pair data-layer RLS with an automated test asserting no query runs without a tenant filter. The residual risk after these controls is compromise of a legitimately-scoped tenant account, an identity-control concern, accepted at the CISO level.
