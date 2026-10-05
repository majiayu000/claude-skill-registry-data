---
name: ecosystem-review
description: Review how a repository in any language actually uses its ecosystem technologies and their integration boundaries. Use for multi-language or polyglot library, framework, runtime, build, package, persistence, messaging, observability, testing, SDK, or platform integration reviews; infer languages automatically unless the user supplies them. Review-only by default; do not use for broad architecture, generic code style, security, performance, or every dependency.
---

# Ecosystem Review

Review concrete technology usage, not an abstract dependency inventory. Keep the review read-only unless the user explicitly authorizes changes.

## Scope

Use this workflow directly for focused single-language, multi-language, or
polyglot ecosystem reviews. Apply only language-specific claims supported by
the available repository and official-source evidence; otherwise continue with
the language-neutral checks and state the scoped uncertainty.

## Inputs

Accept these optional inputs:

- `languages`: `auto` by default, or an explicit list. In `auto`, infer every materially used language, including polyglot repositories.
- `priority_technologies`: technologies the user wants emphasized; treat them as priority hints, not an exhaustive scope.
- `allow_web_research`: default `true`; use official sources when they are available.
- `review_only`: default `true`.

## Workflow

1. Discover evidence before choosing technologies.
   - Inspect package manifests, lock files, build definitions, runtime and deployment configuration, CI, and generated metadata where relevant.
   - Locate actual import, module, registration, configuration, plugin, entrypoint, middleware, client, migration, task, and test usage.
   - Infer languages from both configuration and source use; do not reduce a polyglot repository to its top-level manifest.
   - Require concrete, technology-appropriate repository evidence of use: imports, modules, registrations, or source evidence for code libraries; relevant configuration, build, CI, entrypoint, deployment, plugin, or runtime evidence for declarative, tooling, or infrastructure technologies. For conflicting version or effective-configuration claims, prefer fresh executed runtime evidence, then lock evidence, then declarations. State conflicts and missing evidence.

2. Classify candidates.
   - Prioritize technologies that define application or request boundaries, validation, persistence, migrations, concurrency, background work, messaging, external clients, observability, testing, or runtime lifecycle.
   - Review heavily used boundary technologies next. Ignore tooling-only, trivial, and transitive dependencies unless user priority or concrete usage justifies review.
   - Make language-specific best-practice claims only when repository evidence and authoritative sources support them. Otherwise retain the language-neutral review boundary and state the resulting scoped uncertainty. Do not impose a universal lifecycle or architecture pattern.

3. Inspect usage and challenge findings.
   - Follow each prioritized technology through its setup, configuration, adapters, error handling, lifecycle, and integration tests.
   - Generate candidates, then run an explicit disproof pass against source, lock, runtime, configuration, local conventions, tests, and applicable official sources.
   - Treat unexecuted or absent tests as missing evidence, never as proof that behavior passes. Preserve scoped uncertainty when environment, runtime, or source evidence is unavailable.

4. Research only when it changes claim strength.
   - For version-sensitive, deprecation, migration, or compatibility claims that would otherwise be strong, check official documentation, changelogs, migration guides, or release notes when web research is allowed and available.
   - Cite official sources used. If network access or an official source is unavailable, continue the review but downgrade the claim and state what could not be verified.

5. Report only actionable evidence.
   - Ground each finding in exact locations and observed usage.
   - State the technology or boundary, evidence, impact, confidence and uncertainty, and a minimal testable recommendation.
   - Reject or downgrade optional modernization, disputed claims, and candidates disproved by repository evidence. List material non-issues only when useful.

## Output

Use this structure unless the user requests another format:

1. Discovery summary: inferred languages, evidence sources, and technology candidates.
2. Review scope: technology, detected version or uncertainty, category, priority, and reason.
3. Findings: priority, exact location, observed pattern, impact, confidence, and minimal testable recommendation.
4. Cross-technology boundaries inspected: findings or explicit non-findings with evidence limits.
5. Non-issues / rejected candidates: only when they add signal.
6. Follow-up prompts: 3-5 small, reversible review or change requests with acceptance criteria.
