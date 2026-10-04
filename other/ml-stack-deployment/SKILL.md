---
name: ml-stack-deployment
description: Prepare an ML artifact for serving when a user asks to deploy, publish, expose an endpoint, launch a Space or local service, configure auth, scale, smoke-test, or roll back; separate release approval from training and evaluation.
---

# Artifact promotion and serving

Require an independent audit, passing evaluation thresholds, immutable model/data/environment/resource manifests, model card and provenance, target, auth policy, secret references, health probes, rollback version, and scaling/cost policy.

## Workflow

1. Reconcile artifact hashes and manifests with `ml-stack-audit` and verify evaluation go/no-go.
2. Select local service, endpoint, or Space; define request schema, health and smoke probes, capacity, timeout, observability, and rollback.
3. Review security, authentication, authorization, secret handling, PII, license, and public exposure.
4. Obtain explicit release approval; perform no upload, publication, endpoint mutation, or repository change through this skill unless an equivalent approved runtime operation exists.
5. Hand exact target and release manifest to `ml-stack-hub` for approved publication and `ml-stack-tracking` for post-release metrics.

## Boundary and outputs

Never silently publish to Hub, Spaces, endpoints, or repositories. Abstain on missing hashes, audit, thresholds, model card, auth, rollback, or cost policy. Return a release checklist, target plan, probes, rollback command/intent, measured versus unknown values, and approval record. Next owner: `ml-stack-hub` for artifact publication or `ml-stack-audit` for a failed gate.

See [artifact promotion](references/artifact-promotion.md), [serving and Spaces](references/serving-and-spaces.md), [health and rollback](references/health-and-rollback.md), and [publication policy](references/publication-policy.md).
