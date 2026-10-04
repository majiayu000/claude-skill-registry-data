---
name: kyverno-policy-review
description: Use this skill for Kyverno policy review across the stable policies.kyverno.io/v1 API surface — ValidatingPolicy, MutatingPolicy, GeneratingPolicy, DeletingPolicy, and ImageValidatingPolicy. Trigger when the user asks whether an admission policy is safe, whether a PolicyException is justified, whether a policy should be enforced or audited, whether a Kyverno policy should be replaced by a native ValidatingAdmissionPolicy (CEL), or whether image signature verification is correctly configured.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-05"
  category: security
---

# Kyverno Policy Review

## Purpose

Review Kyverno policies and PolicyExceptions against admission correctness, supply chain integrity, blast radius, failure mode, and the Kyverno-vs-native-CEL architectural decision. Kyverno is the most widely deployed Kubernetes policy engine — every misconfigured policy is either a silent allow (security gap) or a silent deny (production outage).

## Lean operating rules

- Prefer live cluster evidence (`kubectl get policies.kyverno.io,clusterpolicies,policies,validatingpolicies,mutatingpolicies,imagevalidatingpolicies,policyexceptions -A -o yaml`) when the active client exposes it; otherwise fall back to official Kyverno documentation (kyverno.io) and sanitized YAML from the user.
- Separate confirmed facts from inference. If the cluster's Kyverno install state, admission webhook configuration, or PolicyReport status was not queried, say so.
- Treat `failureAction: Audit` (or legacy `validationFailureAction: audit`) on a production-relevant policy as a critical finding — admission violations become silent log lines.
- Treat any `PolicyException` as an audit-required artifact — every exception is a documented bypass with a name, reason, and reviewer.
- Challenge `background: false` paired with no `match` admission scope — the policy will never run.
- Challenge `ImageValidatingPolicy` with `verifyImages: skip` patterns, missing public keys, or `mutateDigest: false` — supply-chain attestations stop being enforced or stop being immutable.
- Challenge any policy that could compile to a native `ValidatingAdmissionPolicy` (CEL) — fewer moving parts, no Kyverno controller in the admission path.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.

## References

Load these only when needed:

- [Evidence path and tooling](references/mcp-and-evidence.md) — use when choosing live cluster evidence, confirming Kyverno install state, or switching to documentation mode.
- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review, applying stress checks, evaluating Kyverno-vs-native-CEL, or formatting the final answer.
- [Official sources](references/official-sources.md) — use when you need the detailed Kyverno documentation list, CEL expression references, or grounded insights from the Kyverno project.

## Response minimum

Return, at minimum:

- the scoped target (policy kind, name, match scope) and evidence level,
- the failure mode (`Audit` vs `Enforce`) and whether it matches the production posture,
- the main risks or control gaps (PolicyException, wildcard match, missing image signatures, weak CEL expressions),
- whether the policy could be replaced by a native ValidatingAdmissionPolicy (CEL) and the tradeoff,
- the safest next actions and rollback plan,
- the assumptions or blockers that prevent stronger conclusions.
