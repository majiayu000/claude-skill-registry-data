---
name: desk-check
description: "Demonstrate work in progress, collect criterion-level feedback, and preserve what was actually reviewed."
metadata:
  category: Review
---

# Desk Check

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Identify the feature and its actual working checkout, acceptance criteria, branch, commit, and dirty state. Use the current work in progress; a new checkout of a pushed branch may omit the changes the user wants to see.
2. Do not switch, stash, clean, or commit the user's work to prepare a demo. If another task is editing it, coordinate a stable demonstration point. A desk check does not require a PR, green CI, or completion.
3. Discover how this project runs. Demonstrate the appropriate surface: browser, CLI, API, desktop app, or device. Follow the project's device/simulator requirements; do not impose a mobile-only process on other software.
4. For each criterion, quote the expected behavior, establish preconditions, demonstrate what exists, and capture appropriate evidence. Ask for the user's verdict on each demonstrated criterion; do not infer approval from silence.
5. Record approved, change needed, not built yet, or blocked. Preserve feedback accurately. Separate extra observations from acceptance criteria instead of silently expanding scope. Do not edit the implementation during the demo to manufacture a pass.
6. Save a record in an appropriate local report location, or publish it to the issue if authorized. Include the SHA, branch, dirty state, environment, criterion results, evidence paths, and follow-ups. Do not create an evidence branch or upload screenshots without authorization.
7. For later sign-off, offer to reuse explicit prior approvals only when the demonstrated behavior is unchanged and the user agrees. Dirty-tree evidence needs a reliable record of what was demonstrated; a commit SHA alone is insufficient.

## Deliverable

Return the demonstration record and follow-ups. Keep board state, PR state, and merge status unchanged: work-in-progress feedback is not a completion gate. Stop only preview processes you started, and preserve the original checkout.
