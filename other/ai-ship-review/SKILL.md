---
name: ai-ship-review
description: Review whether an AI-built or rapidly prototyped application is ready to ship. Use when asked to audit launch readiness, review a repository before deployment, find blockers in vibe-coded apps, assess security/configuration/data/auth/payment/deployment risks, or generate shipping artifacts such as SHIP_CHECKLIST.md, RISK_REGISTER.md, DEPLOYMENT.md, and release notes.
---

# AI Ship Review

## Purpose

Assess whether an application is ready to release, with special attention to risks common in AI-generated and fast-moving codebases: hidden security issues, missing production configuration, shallow tests, fragile auth/payment flows, incomplete deployment docs, and code that works locally but is not operationally ready.

## Default Workflow

1. Inspect the repository structure, README, package/build files, deployment files, environment examples, tests, auth, payments, database, background jobs, and API boundaries.
2. Run `scripts/scan_repo.py <repo-path>` when working in a local repository. Treat its output as a starting inventory, not as proof of safety.
3. Read the relevant references only as needed:
   - `references/checklist.md` for the launch-readiness scoring model.
   - `references/security.md` for security review checks.
   - `references/auth-payments.md` for authentication, authorization, billing, and webhook checks.
   - `references/deployment.md` for deploy, rollback, observability, and operations checks.
4. Investigate the highest-risk areas directly in code before making claims.
5. Produce a concise ship decision with blockers first, then high risks, then concrete next steps.

## Ship Decision

Use one of these decisions:

- `Ready`: no known blockers; remaining items are low-risk polish or documentation.
- `Ready with caution`: no launch-blocking issue found, but there are meaningful risks to address soon.
- `Not ready`: at least one blocker can cause security exposure, data loss, billing/auth failure, broken production deploys, or a critical user workflow failure.

When evidence is incomplete, say what was inspected and what could not be verified. Do not imply a complete security audit unless one was actually performed.

## Severity

- `P0 Blocker`: must fix before launch. Examples: exposed secrets, missing auth on privileged routes, unverifiable payment webhooks, destructive data operations without safeguards, production build failure.
- `P1 High`: should fix before broad release. Examples: missing migration rollback, weak error handling in core flows, no production env example, no meaningful tests for critical paths.
- `P2 Medium`: fix soon. Examples: thin documentation, limited observability, incomplete empty states, missing rate limits on lower-risk endpoints.
- `P3 Low`: polish or maintainability.

## Output Format

Start with the decision and score:

```markdown
## Ship Readiness: Not ready

Score: 58 / 100
Decision: Do not ship yet.
```

Then list findings:

```markdown
### P0 Blockers
- [P0] Payment webhook accepts unsigned events
  Evidence: `src/api/stripe/webhook.ts` parses events without signature verification.
  Risk: Attackers can forge subscription updates.
  Fix: Verify the provider signature using the raw request body and webhook secret.

### P1 High Risks
- [P1] No `.env.example` for required production settings
  Evidence: code reads `DATABASE_URL`, `AUTH_SECRET`, and `STRIPE_SECRET_KEY`, but no example file documents them.
  Risk: deployments can silently miss required configuration.
  Fix: Add `.env.example` with safe placeholders and deployment notes.
```

End with:

- `Before launch`: the smallest ordered checklist to reach launch readiness.
- `Artifacts to create/update`: exact filenames such as `SHIP_CHECKLIST.md`, `RISK_REGISTER.md`, `DEPLOYMENT.md`, `.env.example`.
- `What I verified`: commands run, files inspected, and limitations.

## Artifact Guidance

When the user asks to generate durable files, create only the artifacts that match the repository's maturity:

- `SHIP_CHECKLIST.md`: launch decision, blockers, owner-ready checklist.
- `RISK_REGISTER.md`: risk, severity, evidence, mitigation, owner, status.
- `DEPLOYMENT.md`: build, environment, deploy, smoke test, rollback.
- `.env.example`: safe placeholders only; never include real secrets.
- `RELEASE_NOTES.md`: user-facing changes and known limitations.

Keep generated artifacts direct and actionable. Avoid generic compliance language unless the repository actually needs it.
