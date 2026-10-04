---
name: designing-deployment-pipelines
kind: skill
status: ready
provenance:
  principles:
  - P058
  - P007
  - P012
  - P013
  - P037
  - P053
  claims:
  - C00070
  - C00071
  - C00072
  - C00073
  - C00074
  - C00075
  - C01545
  - C01546
  - C01552
  - C01553
  - C02945
  - C02946
  evidence:
  - E00046
  - E00047
  - E00048
  - E00049
  - E00050
  - E00051
  - E00494
  - E00495
  - E00499
  - E00500
  - E00598
  - E00599
  source_anchors:
  - 9d4b1cf206e5-c0003
  - 7f54213fedb8-c0014
  - 861f0551c788-c0012
  authored_from_digest: 6eb042aea4bbd23d556c59218a0f12f5059518548c6bf8a47b38589d73ebe3d9
---

# Designing deployment pipelines

## Purpose

Design or review a CI/CD pipeline so feedback is fast and releases are safe, repeatable, and
frequent. The pipeline rests on four reinforcing foundations: an automated pipeline that catches
defects early (P004), version control with trunk-based development and small batches (P006),
the pipeline and its infrastructure defined as code (P007), and lightweight peer-review-based
change management with security built in (P011). Tooling specifics change fast — this skill governs
the practices and trade-offs, not particular products.

## When to use

- Designing or reviewing a CI/CD pipeline, branching strategy, or release process.
- Releases are infrequent, manual, or error-prone, or merges are painful.
- Pipeline/environment configuration is click-configured and hard to reproduce, or environments
  drift.
- A change-approval or security-gating process is slowing delivery without improving stability.

Skip the full treatment for a throwaway prototype with no path to production, where pipeline
investment is premature — say so rather than over-engineering it.

## Procedure

1. **Put everything under comprehensive version control (P006).** Application code, system
   configuration, and build and deploy scripts all live in version control — this is the
   foundational continuous-delivery capability (CL019). Without it, nothing downstream is
   reproducible.
2. **Work on trunk in small batches (P006).** Use trunk-based development with very short-lived
   branches merged at least daily (CL020); ship change as small, frequent, simple increments
   rather than large bundled releases (CL061, CL003). Smaller batches shrink lead time, lower the
   risk of any one deployment, and shorten the gap between a change and its detected effect.
3. **Practise continuous integration as the base (P004).** Build and test every change frequently
   against the live codebase — CI is the foundation that makes continuous delivery possible
   (CL063). Automate the build-and-test path so it gives consistent, repeatable results the team
   can trust; manual steps inject error and erode confidence (CL062).
4. **Catch defects as early as possible (P004).** Stage automated unit, integration, and
   acceptance tests that fail fast on regressions, so untested changes cannot proceed and
   developers get feedback before problems reach production (CL007, CL039). Keep the test suites
   reliable and have developers own the acceptance tests — developer-maintained automated testing
   correlates with higher delivery performance (CL021).
5. **Automate every manual deployment step (P004).** Packaging, configuration, environment setup,
   and test execution should all be automated so releases become safe, repeatable, and frequent
   (CL008).
6. **Define the pipeline and its infrastructure as code (P007).** Store the pipeline definition in
   version control alongside the application, replacing hand-clicked job configuration with
   reproducible, auditable definitions (CL031). Provision build and runtime infrastructure with
   infrastructure-as-code so environments are versioned, reviewable, and reproducible (CL035), and
   adopt immutable, baked images so failed nodes are replaced by identical instances and scaling
   avoids runtime configuration drift (CL034). Running stages in containers gives each job a clean,
   reproducible, ephemeral environment (CL038).
7. **Keep change management lightweight and build in security (P011).** Prefer peer review — code
   review and pairing — over a heavyweight external change-approval board, which slows delivery
   without improving stability (CL025); an automated CI pipeline can satisfy
   segregation-of-duties and compliance needs without a separate approval board (CL026). Integrate
   security testing into the pipeline and daily work rather than gating it at the end (CL014), with
   automated scanning — such as dependency vulnerability checks — as a stage that blocks risky
   artifacts (CL040), and enforce code-quality gates so changes failing the bar stop before
   deployment (CL041).
8. **For `review`/`validate` requests,** walk the points above as a checklist, order findings by
   delivery impact, and for each gap name the principle at stake and one concrete remediation. A
   manual, untested, or end-gated release path — or a heavyweight external approval board offered
   as the route to safety — is a finding to fix, not a control to endorse.

## Inputs

- The current pipeline/branching/release design, or a description of how the team builds, tests,
  and deploys today.
- System and team context: coupling, team size, environments, regulatory constraints on approval.
- Whether the ask is to advise, review, validate against readiness criteria, or compare options.

## Output

A pipeline design or review structured around the foundations above: version control, trunk-based
small-batch flow, CI with fail-fast automated tests, full deploy automation, pipeline- and
infrastructure-as-code with immutable images, and lightweight peer review with security built in.
Findings are ordered by impact; each names its principle and a concrete remediation.

## References

- `references/pipeline-as-code-practices-reference.md` — the practice checklist this skill applies.
- Sibling skills: `planning-progressive-delivery` (how to release what the pipeline produces),
  `assessing-delivery-performance` (the metrics a better pipeline should move).

## Provenance

Derived from principles P004, P006, P007, P011 across `the-devops-handbook-c4933b3c`,
`accelerate-the-scien-7241289b`, `pipeline-as-code-con-2e091c45`, and `comp109-5dbbef8d` (all
distillation-only — paraphrase, no verbatim quotation). The Accelerate-sourced claims are
correlational survey findings; the pipeline-as-code claims are tool-specific practitioner guidance,
so this skill generalises the practice and points teams to current official tool documentation for
commands and product features.
