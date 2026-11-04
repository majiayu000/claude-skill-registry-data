---
name: blast-radius
description: Trace what a proposed or implemented change could break beyond its diff, especially indirect consumers, serialized contracts, lifecycle effects, and version-specific dependency behavior. Use explicitly for “blast radius” or “what could this break.” Audit and test safety assumptions; do not automatically fix, commit, or open PRs.
disable-model-invocation: true
license: MIT
---

# Blast Radius

Find the non-obvious consequences of a change, not just its callers. Adapted from pstack; see [source notes](UPSTREAM.md).

## Establish the change

Inspect the requested scope, diff, relevant code, and known consumers. Separate behavior changes from structural edits. Include relevant dirty or untracked inputs; do not assume HEAD represents the user’s work or attribute other agents’ edits to yourself.

Find the critical facts the change’s safety depends on. For example: a cleanup operation affects only expired entries, an omitted field has no external consumer, or an asynchronous result cannot arrive after ownership transfers. State each as a falsifiable claim.

## Trace beyond symbol search

Follow boundaries that grep can miss: serialized fields, persistence schemas, wire formats, generated code, configuration, dynamic registration, feature flags, caches, foreign-language consumers, and operation timing. Inspect pinned dependency versions and local patches when behavior relies on them.

Ground confirmed consumers and constraints in actual source or records. A search with no matches narrows uncertainty; it does not prove no consumer exists. Do not fabricate probabilities or invent compatibility requirements for hypothetical users.

## Test the safety facts

Use the smallest isolated test or probe that exercises the relevant real code and would fail if the safety assumption were wrong. Observe side effects where they matter. A source citation supports a narrower claim than a runtime reproduction; say which evidence you obtained.

Distinguish confirmed breakage, cleared risks, plausible unresolved risks, and unknown coverage. An environment you cannot exercise stays unverified. Avoid turning the audit into a long list of imagined failures or a compulsory multi-agent panel.

## Report

Give the behavior change, the critical safety facts and their evidence, significant affected consumers, and remaining gaps. Prioritize by consequence and reachability. Recommend a cheap regression check when useful; do not silently apply fixes or broaden compatibility scope.
