---
name: read-the-damn-docs
description: Use when an answer or implementation depends on a third-party library, framework, SDK, API, CLI, cloud service, provider, or other version-sensitive contract. Also use for current or official behavior and consequential auth, security, billing, data, migration, deployment, compliance, or privacy claims.
---

# Read The Damn Docs

Read the smallest authoritative evidence set that can answer the question. Do not replace a quick local fact with a research project, and do not rely on model memory when the contract can change.

## Evidence order

1. Read project truth first. Check the project wiki and docs, installed version, source and types, nearby usage, schemas, tests, and repository rules.
2. Use Context7 as the normal source for current upstream library documentation.
3. Read direct official pages, changelogs, source, schemas, or migration guides when Context7 is missing, unclear about the installed version, or the claim affects a consequential boundary.
4. Use general web search only for discovery and gaps.

Project evidence decides how the dependency is used here. Upstream evidence decides what the dependency supports. When they conflict, name the conflict and inspect the installed source before changing code.

## Proportion

A tiny edit with an established local pattern needs a quick local confirmation. An unfamiliar integration, version upgrade, changed API, public contract, or consequential boundary needs direct upstream evidence.

Stop when the required facts are established. Gather option names, imports, lifecycle behavior, defaults, breaking changes, limits, permissions, and one relevant example. More links do not improve a weak claim.

## Apply and verify

Before recommending a fork, check whether the package’s supported configuration or a suitable maintained alternative meets the requirements. Use a bounded trial when documentation cannot settle the decision.

Use the evidence to answer or implement the request. Verify with the smallest useful check, such as a typecheck, focused test, build, schema check, dry run, or local reproduction.

Name the documentation or source that materially affected the decision. If authoritative evidence is unavailable, state the missing source and narrow the claim instead of presenting memory as current fact.
