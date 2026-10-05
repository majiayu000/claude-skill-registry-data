---
name: security-review
description: Use when auditing code or a change for vulnerabilities. Produces severity-ranked findings with exploit paths and fixes, covering the OWASP Top 10, authorization, secrets, and dependency risk.
metadata:
  category: security
  version: 1.0.0
  tags: [security, audit, owasp, review, vulnerability]
---

# Security Review

## Purpose

Find the vulnerabilities in a codebase or a change, with enough specificity that each finding can be fixed and verified. A security review that produces a list of theoretical concerns is not a security review.

## When to Use

- Reviewing a pull request that touches authentication, authorization, or user input.
- Auditing a service before it becomes internet-facing.
- Responding to a penetration-test report.
- Periodic review of a security-sensitive codebase.

## Capabilities

- OWASP Top 10 analysis against actual code.
- Authorization audit, including object-level checks.
- Secrets and credential discovery.
- Dependency and supply-chain risk assessment.
- Input-validation and output-encoding review.

## Inputs

- The code, the diff, or the service.
- The threat model: who the attacker is and what they want.
- The deployment context: is it internet-facing, multi-tenant, handling payments?

## Outputs

Findings ranked by severity, each with:

- The vulnerable code, by file and line.
- The exploit path — how it would actually be abused.
- The fix, concretely.
- How to verify the fix.

## Workflow

1. **Map the attack surface** — Every route, every queue consumer, every file upload, every parameter. You cannot audit what you have not enumerated.
2. **Follow untrusted data** — From each entry point, trace where the data goes: into a query, a command, a template, a file path, a redirect. Each of those is a potential injection.
3. **Audit every authorization check** — For each endpoint taking an identifier: is there a check that the caller may access *that specific object*? This is where the real vulnerabilities are.
4. **Look for the secrets** — In the repository, the history, the config, the logs, and the error messages.
5. **Assess the dependencies** — Known vulnerabilities, unmaintained packages, and anything with install scripts.
6. **Rank by exploitability, not by CVSS alone** — An unauthenticated remote data leak outranks a theoretical timing attack, whatever the score says.

## Best Practices

- A finding without an exploit path is a suggestion. State how it would actually be abused, or it will be deprioritized — correctly.
- Check the tests, not just the code. A missing authorization test usually means a missing authorization check.
- Search the git history for secrets, not just the working tree. A key removed in a later commit is still in the history and still compromised.
- Automated scanners find known-bad patterns. They do not find missing authorization, which is where the serious findings live. Read the code.
- Rank findings by what an attacker would actually do first. That is the order they will be exploited in, and it should be the order they are fixed in.
- Verify the fix. A fix that was not re-tested is a hypothesis.

## Examples

**A finding written so that it gets fixed:**

```markdown
### Critical — Broken object-level authorization on the invoice endpoint

**Location:** `api/invoices.py:47`

**Vulnerability:** `GET /invoices/{id}` authenticates the caller but does not
verify that the invoice belongs to them. Invoice IDs are sequential integers.

**Exploit:**
    curl -H "Authorization: Bearer <any valid token>" https://api.example.com/invoices/1
    for i in $(seq 1 100000); do curl .../invoices/$i; done

Any authenticated user — including a free-tier account — can enumerate and read
every invoice in the system, including customer names, addresses, and amounts.
This is a reportable data breach under GDPR.

**Fix:**
```python
invoice = await db.invoices.get(invoice_id)
if invoice is None or invoice.tenant_id != user.tenant_id:
    raise HTTPException(404, "Invoice not found")   # 404, not 403: do not confirm existence
```

**Also:** migrate invoice IDs from sequential integers to ULIDs, so that
enumeration is not possible even if an authorization check is missed again.

**Verification:** `test_cannot_read_another_tenants_invoice` — authenticate as
tenant A, request an invoice belonging to tenant B, assert 404.
```

**Searching the history, not just the tree:**

```bash
# The key was deleted in a later commit. It is still in the history, and still
# compromised. Deleting it from the tree changes nothing.
git log --all -p -S "AKIA" --pickaxe-regex | grep -E "^\+.*AKIA[0-9A-Z]{16}"

# Findings here require rotating the credential. Rewriting history is optional;
# rotation is not.
```

## Notes

- Any secret that has ever been committed must be considered compromised, regardless of whether the commit was pushed, force-pushed away, or in a private repository. Rotate it.
- SAST tools produce a high false-positive rate and miss authorization flaws entirely. They are a useful first pass, not a review.
- The most valuable question in a security review is "who is allowed to do this, and where is that enforced?" If the answer is "the frontend does not show the button", there is no enforcement.
