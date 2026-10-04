---
name: assess-pre-commit
description: "Inspect local commit hooks and report what they enforce, how they run, and where checks can be bypassed."
metadata:
  category: Quality
---

# Assess Pre Commit

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Discover the hook mechanism, installation setup, and intended policy from repository files and Git configuration. Consider native hooks and installed frameworks without assuming one is present.
2. Trace each configured hook and referenced command. Determine whether it checks staged content or the whole tree, how files are selected, whether it modifies files, and whether failures prevent a commit.
3. Check whether new contributors and CI actually install the hooks. Document known bypass mechanisms and distinguish a local convenience check from an enforced remote policy. Do not execute untrusted hooks merely to inspect them.
4. Compare observed behavior with the project's declared requirements. If none exist, state that fact and offer a proportional baseline; missing hooks are not automatically a defect.
5. Prioritize concrete gaps, false assurances, and destructive or surprising side effects with supporting paths and suggested remedies.

## Deliverable

Return a report with the evaluated revision, framework/setup, enforced checks, bypassability, policy source, evidence, and limitations. Do not install hooks, change global Git settings, or modify source code during an assessment.
