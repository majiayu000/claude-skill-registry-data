---
name: adapt-template-change
description: Analyze and adapt selected features, fixes, commits, pull requests, files, or implementation ideas from an upstream project template into a locally customized project. Use when an AI coding agent must compare a template at a Git URL or local path with the current project, propose compatible migration options, obtain approval, implement the chosen adaptation, and verify it without blindly synchronizing the whole template.
---

# Adapt Template Change

Act as an interactive migration assistant. Preserve the target project's intent and local
architecture; treat the upstream implementation as evidence, not as code that must be copied.

## Establish the request

1. Read the target project's `AGENTS.md` and other repository instructions completely.
2. Inspect the worktree status and relevant target files before proposing changes. Preserve
   unrelated user changes.
3. Identify the requested capability from any combination of:
   - an implementation idea or behavioral description;
   - a template repository, commit, tag, branch, pull request, diff, or file link;
   - a local template checkout or patch;
   - constraints describing what the target project must preserve.
4. Ask only for information that cannot be discovered safely. Do not require the user to identify
   source files when the requested behavior is clear enough to investigate.

## Acquire the source

1. Prefer a user-provided local template path because it supports complete file and Git-history
   inspection.
2. Otherwise inspect the provided public URL with available web or Git tooling. For this template,
   use `https://github.com/fomenko-ai/pytest-hardware-template` when the user does not specify a
   different source.
3. Resolve a moving branch or repository URL to a commit when possible. Record the repository URL
   and resolved revision in the analysis.
4. For a commit or pull request, inspect its diff and enough surrounding code to understand the
   implementation. Do not infer the change from the final file snapshot alone.
5. If remote access is unavailable, look for an existing local checkout. If none exists, ask the
   user to download or clone the template and provide its path. Do not ask for credentials or
   encourage placing secrets in the repository.
6. If the source revision remains unknown, state that the comparison is snapshot-based and explain
   the resulting uncertainty.

## Analyze compatibility

Read [references/analysis-checklist.md](references/analysis-checklist.md) and apply its checklist.

1. Trace the requested behavior through its models, APIs, factories, fixtures, configuration,
   dependencies, tests, documentation, and lifecycle cleanup.
2. Find the corresponding responsibilities in the target project, even when names and paths
   differ.
3. Determine whether the capability is absent, partially present, already implemented differently,
   or incompatible with a local decision.
4. Separate required behavior from incidental upstream refactoring, formatting, naming, and
   unrelated changes.
5. Follow the target project's terminology and dependency direction. Do not introduce upstream
   abstractions that lack a current local requirement.
6. Never expose or transfer credentials, secrets, organization-specific values, or physical
   environment details.

## Present options and wait

Present a migration brief before editing production files. Include:

- requested behavior and source revision;
- relevant upstream and target components;
- local constraints and detected conflicts;
- two or three viable options when meaningful, including a recommended option and tradeoffs;
- exact production files expected to change;
- dependency or configuration changes;
- proposed verification and tests;
- unresolved assumptions and risks.

Prefer these option shapes when applicable:

1. **Minimal adaptation**: implement only the requested behavior using existing local patterns.
2. **Template-aligned adaptation**: carry over the upstream design where it fits the target.
3. **Equivalent local implementation**: preserve behavior while using a different local design.
4. **No migration**: explain when the feature is already present, obsolete, unsafe, or unsuitable.

Recommend one option, but do not edit production files until the user approves it. If repository
instructions require architectural approval based on file or module count, explicitly satisfy
that gate. Treat approval of an approach as approval only for the stated scope.

## Implement the approved option

1. Recheck the worktree before editing and work with concurrent user changes.
2. Make the smallest coherent production change that delivers the approved behavior.
3. Adapt names, types, imports, configuration, and dependency injection to the target project.
4. Use structured parsers for structured data and preserve unrelated content.
5. Do not add provenance metadata such as `.template-source.yaml` unless the user approved that
   repository-level mechanism.
6. Stop and request renewed approval if implementation reveals a materially broader architecture,
   new dependency, destructive migration, or additional production files outside the approved
   scope.
7. Follow the target repository's approval rule for test changes. When tests are approved, add
   focused coverage for behavior and integration boundaries rather than copying upstream tests
   mechanically.

## Verify and report

1. Run the narrowest relevant non-hardware check first.
2. Run the target repository's required full quality gate after all approved changes.
3. Never run hardware tests or contact physical devices unless explicitly requested and the target
   environment is ready.
4. Review the final diff for unrelated changes, leaked secrets, unresolved conflict markers, and
   accidental upstream-specific values.
5. When a file is intentionally transferred without adaptation, verify that the source and target
   are identical with `git diff --no-index --exit-code -- <source-file> <target-file>`; treat only
   exit code `0` as confirmation of an exact transfer.
6. Report:
   - the behavior transferred and how it was adapted;
   - the source URL and revision actually inspected;
   - changed files;
   - verification results and any skipped checks;
   - deliberate differences from the upstream implementation;
   - remaining manual work or risk.

Do not claim that an entire template version was adopted when only selected behavior was migrated.
