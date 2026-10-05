---
name: threat-modeling
description: "Every methodology — STRIDE, PASTA, LINDDUN, attack trees — is a technique for"
---

# Threat Modeling (Verbose)

## Core Patterns

### The Four Questions

Every methodology — STRIDE, PASTA, LINDDUN, attack trees — is a technique for
answering four questions in order:

```
1. What are we building?      Data flow diagram with trust boundaries
2. What can go wrong?         STRIDE, per element
3. What will we do about it?  Eliminate / mitigate / transfer / accept
4. Did we do a good job?      Tracked issues, tests, and a re-review trigger
```

Teams that skip question 1 produce generic threat lists. Teams that skip question
3 produce documents. Teams that skip question 4 produce documents that are wrong
within a quarter.

### Data Flow Diagrams and Trust Boundaries

An architecture diagram shows what talks to what. A DFD shows *where trust
changes*, which is where threats live. Four notations:

| Shape | Meaning | Example |
|---|---|---|
| Rectangle | External entity — outside your control | Browser, OCR vendor |
| Circle | Process — code you run | API service, PDF renderer |
| Parallel lines | Data store | Postgres, S3, Redis |
| Arrow | Data flow | HTTPS request, SQL query |
| Dashed line | **Trust boundary** | Internet edge, tenant edge, org edge |

Worked example — an expense reimbursement SaaS:

```
                        ===== BOUNDARY A: internet / DMZ =====
 [Browser (SPA)] --1. POST /api/v1/expenses {amount, receipt} (JWT)--> ( API service )
 [Finance admin] --2. POST /api/v1/expenses/:id/approve (JWT)-------->

                        ===== BOUNDARY B: app / data =====
 ( API service ) --3. SQL over TLS, app role----------------> || Postgres ||
 ( API service ) --4. PutObject------------------------------> || S3 receipts ||
 ( API service ) --5. audit event----------------------------> || Audit log (append-only) ||

                        ===== BOUNDARY C: tenant isolation (logical) =====
 all queries carry tenant_id — enforced where?

                        ===== BOUNDARY D: organization / vendor =====
 ( OCR worker ) --6. HTTPS receipt image + API key----------> [ OCR vendor ]
 [ Stripe ] -----7. POST /webhooks/stripe-------------------> ( API service )

                        ===== BOUNDARY E: build / supply chain =====
 [ npm, PyPI, base images ] --8. build----------------------> ( CI ) --9. deploy--> ( API service )
```

Reading the boundaries produces findings before STRIDE even starts:

- **Boundary C is logical, not physical.** It exists only if every query filters on
  `tenant_id`. That is an assumption, and it needs an enforcement point — row-level
  security in Postgres, or a repository layer nothing can bypass. "Developers will
  remember" is not a boundary.
- **Flow 6 crosses out of the organization** carrying PII. That is a data
  processing agreement, a retention question, and a vendor-breach risk, none of
  which is visible on an architecture diagram.
- **Flow 7 arrives unauthenticated from the internet.** Webhook signature
  verification is the only thing making the sender trustworthy.
- **Boundary E exists at all.** CI holds deploy credentials and executes third-party
  code. Most diagrams omit it entirely.

### STRIDE, Per Element

STRIDE maps threat categories to the security property they violate:

| Category | Violates | Question to ask |
|---|---|---|
| **S**poofing | Authentication | Can someone claim to be another principal? |
| **T**ampering | Integrity | Can data be modified in flight or at rest? |
| **R**epudiation | Non-repudiation | Can an actor deny what they did? |
| **I**nformation disclosure | Confidentiality | Can data reach someone unauthorized? |
| **D**enial of service | Availability | Can service be exhausted or degraded? |
| **E**levation of privilege | Authorization | Can someone gain rights they were not granted? |

Not every category applies to every element. Use the standard mapping:

| Element | S | T | R | I | D | E |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| External entity | ✓ | | ✓ | | | |
| Process | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data store | | ✓ | ✓ | ✓ | ✓ | |
| Data flow | | ✓ | | ✓ | ✓ | |

A full pass over the API service (process — all six apply):

| # | Cat | Threat | Disposition | Control |
|---|---|---|---|---|
| T-01 | S | JWT accepted with `alg: none` or RS256→HS256 confusion | Mitigate | Pin `algorithms=["RS256"]`; verify `aud` and `iss` |
| T-02 | S | Stripe webhook forged by anyone who knows the URL | Mitigate | Verify the signature header against the signing secret; reject on clock skew > 5 min |
| T-03 | T | Client submits `approved: true` in the create payload | Mitigate | Whitelist writable fields; approval state set only by the approval handler |
| T-04 | T | Amount edited after approval, record still reads approved | Mitigate | Approval stores a hash of the approved row; re-approval required on change |
| T-05 | R | Approver denies approving a $40k expense | Mitigate | Append-only audit log with actor, timestamp, and request id; shipped to an account the app cannot write to |
| T-06 | I | `GET /expenses/:id` returns another tenant's record (IDOR) | Mitigate | Postgres RLS on `tenant_id`, plus a repository layer that refuses an unscoped query |
| T-07 | I | Stack traces in 500 responses leak schema and library versions | Mitigate | Generic error body; details to logs only |
| T-08 | D | 10,000 PDF export jobs queued by one tenant | Mitigate | Per-tenant token bucket; bounded worker pool; queue depth alert |
| T-09 | E | SSRF in the PDF renderer reaches the cloud metadata endpoint | Mitigate | Egress allowlist from the renderer; IMDSv2 required; renderer runs with no cloud role |
| T-10 | E | API pod role can read the payment provider secret it never uses | Eliminate | Remove the grant; only the billing worker holds it |

And over the non-process elements, where the categories differ:

| # | Element | Cat | Threat | Disposition |
|---|---|---|---|---|
| T-11 | `|| Postgres ||` | T | App role holds `ALTER`/`DROP` it never needs | Mitigate — least-privilege role, migrations run as a separate identity |
| T-12 | `|| Postgres ||` | I | Backups unencrypted, restorable by anyone with S3 read | Mitigate — KMS-encrypted snapshots, separate key policy |
| T-13 | `|| Audit log ||` | T | Same credentials can append and delete | Mitigate — write-only from the app; deletion requires break-glass |
| T-14 | Flow 6 (to vendor) | I | Receipt PII leaves the org and is retained indefinitely | Transfer + accept — DPA signed, 30-day retention contractually required, reviewed each renewal |
| T-15 | Flow 3 (app→DB) | I | TLS not enforced; a compromised node can read queries | Mitigate — `sslmode=verify-full` |
| T-16 | [OCR vendor] | S | Vendor response spoofed by anyone able to intercept | Mitigate — certificate validation on; treat OCR output as untrusted input |

Sixteen concrete, assigned threats from one hour on a whiteboard.

### Prioritize Without Pretending to Be Precise

DREAD's numeric scores imply an accuracy nobody has. A likelihood × impact grid,
argued out loud, is more honest and takes less time.

| | Impact: Low | Impact: Medium | Impact: High |
|---|---|---|---|
| **Likely** | T-07 | T-08 | T-06, T-01 |
| **Possible** | T-16 | T-15, T-11 | T-09, T-03 |
| **Unlikely** | — | T-12 | T-05, T-14 |

Fix the top-right first. What matters is not the cell but the disagreement that
surfaces while placing each item — that argument is where the real assumptions
get exposed.

### Design Time Beats Ship Time

| | Threat model (design) | Pentest (ship) |
|---|---|---|
| Finds | Classes of flaw, missing controls | Instances, exploitable today |
| Sees | Intent, trust boundaries, assumptions | Only the deployed surface |
| Cost to fix a finding | Whiteboard edit | Rework, migration, sometimes redesign |
| Blind to | Implementation bugs, config drift | Absent controls nobody built |
| Cadence | Every significant design change | Periodic, point-in-time |

A pentest reports "IDOR on `GET /expenses/:id`". A threat model reports "no
enforcement point for tenant isolation exists", which explains that endpoint and
predicts the other forty-two. The pentest finds the instance; the model finds the
class — and finds it in week one rather than month nine, when tenant scoping is
still one repository layer instead of a data migration and an audit of every query
ever written.

These are complements. Model at design to decide what to build; test at ship to
verify you built it. Confirming which modeled threats are actually live in the
running system is the vulnerability-assessment skill's job.

### Close the Loop

```
T-06  IDOR on expense reads
      -> PRO-214  add RLS policy + repository guard
      -> test: tests/security/test_tenant_isolation.py::test_cross_tenant_read_404
      -> re-review trigger: any new table holding tenant-scoped data
```

Every mitigated threat should end at a test, so a regression fails the build
rather than waiting for the next review.

## Common Anti-Patterns

❌ **Architecture diagram with no trust boundaries** — you enumerate components
instead of transitions, and the threats live at the transitions.
✅ Draw boundaries first; every crossing gets scrutiny.

❌ **Omitting CI, vendors, and webhooks from the diagram** — the unmodeled element
is the unmitigated one.
✅ If it can send you bytes or hold your credentials, it is on the diagram.

❌ **Applying all six STRIDE categories to every element** — you invent
"spoofing the database" and lose an hour.
✅ Use the element-to-category mapping.

❌ **A logical trust boundary with no enforcement point** — "queries include
tenant_id" is a convention, and conventions are one pull request from being false.
✅ Enforce in one place code cannot bypass: RLS, a repository layer, a proxy.

❌ **Threats with no disposition** — a list of everything that could go wrong,
owned by nobody.
✅ Every threat gets eliminate / mitigate / transfer / accept, plus an owner.

❌ **Accepting risk anonymously** — "we accepted that" with no name or date is
indistinguishable from having missed it.
✅ Record who accepted, why, and when it is revisited.

❌ **DREAD scores to one decimal place** — false precision on guessed inputs.
✅ A likelihood × impact grid, argued in the room.

❌ **Modeling once, at the start** — the design changed the week after.
✅ Trigger a re-review on new trust boundary, new data class, or new integration.

❌ **"Input validation" as the answer to everything** — it addresses tampering and
some injection, and does nothing for authorization, repudiation, or DoS.
✅ Match the control to the STRIDE category it actually covers.

## Threat Modeling Checklist

- [ ] DFD drawn with external entities, processes, data stores, and flows
- [ ] Trust boundaries explicitly marked, including tenant and organization edges
- [ ] CI/CD, third-party vendors, and webhook senders present on the diagram
- [ ] Each logical boundary has a named enforcement point in code or infra
- [ ] STRIDE applied per element using the element-to-category mapping
- [ ] Data stores reviewed for tampering, disclosure, and repudiation
- [ ] Data flows crossing boundaries reviewed for interception and tampering
- [ ] Audit logging reviewed for integrity, not just presence
- [ ] Every threat has a disposition and a named owner
- [ ] Accepted risks record who accepted, why, and the review date
- [ ] Prioritized by likelihood × impact, not by numeric pseudo-precision
- [ ] Mitigations linked to tickets, and tickets linked to tests
- [ ] Re-review triggers defined (new boundary, new data class, new integration)
- [ ] Model performed at design time, with a pentest scheduled to verify
