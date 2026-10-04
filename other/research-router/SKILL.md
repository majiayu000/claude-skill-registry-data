---
name: research-router
description: Route technical research across the local repository, official documentation, Exa, Context7, DeepWiki, and GitHub code search. Use when coding decisions depend on current APIs, dependency versions, standards, external repositories, or public implementation evidence; not for questions answerable from the checked-out repository.
---

# Research router

Resolve a concrete uncertainty with the smallest reliable evidence set. Do not research every task by default.

## Start locally

Inspect repository instructions, manifests, lockfiles, vendored sources, callers, and tests first. Record the exact dependency version or target standard when it affects the answer. Use repository-native search or CodeGraph for checked-out code; external tools are not substitutes for local inspection.

## Choose the source

- **Context7 MCP**: current, version-specific library or framework documentation. Resolve the library ID, then query the exact API and topic. Reconcile results with the version pinned by the project.
- **Exa `web_search_exa`**: current releases, issues, discussions, advisories, or ecosystem facts.
- **Exa `web_search_advanced_exa`**: research that needs official-domain or GitHub filtering, dates, text constraints, highlights, or a code-oriented query.
- **Exa `web_fetch_exa`**: read a known authoritative page returned by search or named by the user.
- **DeepWiki MCP**: understand architecture or behavior in a public GitHub repository. Verify decisions that matter against the repository source or its official documentation.
- **`gh search code`**: exact symbols, calls, strings, or syntax across public GitHub code. Prefer literal, narrowly scoped queries and inspect the matching file before drawing conclusions.

Do not depend on grep.app automation. The referenced `pi-search` project removed `grepsearch` after grep.app began returning a JavaScript security checkpoint.

## Evidence discipline

Prefer primary documentation, standards, release notes, and source code. Use examples to discover patterns, not to override official contracts. Fetch and read the decisive source rather than relying on a search snippet. Note relevant versions and dates, distinguish sourced facts from inference, and stop when the uncertainty is resolved.

If a remote tool is unavailable, continue with another authoritative source or report the missing evidence. Never paste credentials into queries, commands, logs, or repository files.
