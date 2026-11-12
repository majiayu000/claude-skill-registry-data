---
name: ak-repomix
description: "Pack repositories into AI-friendly XML, Markdown or plain-text files with Repomix."
when_to_use: "Invoke for onboarding, LLM context, security audits or library analysis."
category: engineering
keywords: [codebase, pack, snapshot, llm-context]
argument-hint: "[path] [--style xml|markdown|plain|json]"
metadata:
  author: agentkit
  version: "1.0.1"
---

# Repository packing

Choose the smallest scope that contains the requested module and necessary dependencies.
Inspect existing Repomix config/ignore rules and preserve secret exclusions. Determine local
or remote source, revision, output format and destination; do not pack a whole monorepo for
one module unless dependencies require it.

Use the installed CLI help for version-sensitive options; `references/cli-recipes.md` contains
setup and examples. Existing configuration guidance lives in `references/configuration.md`
and task examples in `references/usage-patterns.md`.

Run the scoped pack, inspect included files/token summary and secret-check warnings, then
verify no required dependency was omitted or sensitive content included. Reuse a previous
pack only when input file hashes, revision and config are unchanged. Report source/revision,
scope, output path, counts and limitations. Never disable secret checks just to obtain output.
