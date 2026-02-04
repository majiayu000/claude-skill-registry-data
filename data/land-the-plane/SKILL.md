---
name: land-the-plane
description: This skill should be used when the user says "let's land the plane", "land the plane", "end the session cleanly", "wrap up the session", or asks to prepare for a clean handoff between coding sessions. Provides a systematic protocol for ensuring all work is committed, tested, tracked, and ready for the next session.
version: 0.1.0
---

# Landing the Plane

## Purpose

This skill provides a clean session-ending protocol for software development work. "Landing the plane" ensures that when a coding session ends, all work is properly committed, tested, tracked in the issue system, and the repository is in a clean state. This systematic approach prevents lost work, maintains code quality, and creates smooth handoffs to future sessions.

## When to Use This Skill

Use this skill when:
- Ending a coding session and want to ensure nothing is left in an inconsistent state
- Preparing to hand off work to another developer or future session
- Need to context-switch away from current work cleanly
- Want to verify all quality gates pass before considering work complete
- Need to sync local and remote issue tracking systems

## The Landing Protocol

Follow this seven-step protocol to land the plane cleanly:

### 1. File Issues for Remaining Work

Before ending the session, capture any remaining work that needs follow-up in the issue tracker. This prevents losing track of incomplete tasks, bugs discovered, or future improvements identified during the session.

Use the Beads CLI to create issues:
```bash
bd create "Issue title" -t task -p 2 --json
```

Document:
- Incomplete features or tasks
- Known bugs discovered but not fixed
- Technical debt identified
- Follow-up improvements needed
- Questions or blockers

**Reference:** See `references/beads-integration.md` for detailed Beads CLI usage and issue management patterns.

### 2. Ensure All Quality Gates Pass

Only if code changes were made during the session, run all quality gates to verify the code is in a good state. File P0 issues immediately if any gates fail.

Run quality checks in sequence:
- **Tests**: Execute test suites (unit, integration, e2e as appropriate)
- **Linters**: Run code style and quality linters
- **Builds**: Verify the project builds successfully
- **Type checking**: Run static type checkers if applicable

**Script:** Use `scripts/run-quality-gates.sh` to execute quality checks systematically.

If any quality gate fails:
1. Attempt to fix the issue if it's quick (< 5 minutes)
2. Otherwise, create a P0 issue with details about the failure
3. Consider reverting changes if the failure is blocking

### 3. Update Issue Status

Review all issues worked on during the session and update their status to reflect current reality:
- Close issues that were completed
- Update progress on in-progress issues
- Add comments documenting what was done
- Update priority or labels as needed

Keep issue tracking synchronized with actual work completed.

### 4. Sync the Issue Tracker

Work methodically to ensure both local and remote issue databases are merged safely. This step requires careful handling of potential conflicts between local and remote issue state.

The sync process:
1. Review local changes (created, updated, or closed issues)
2. Pull remote changes from the issue tracker
3. Resolve any conflicts between local and remote state
4. Push local changes to remote
5. Verify consistency between local and remote

**Important:** Be creative and patient during this step. Conflicts between local and remote state require careful reconciliation. The goal is clean reconciliation where no issues are lost.

**Reference:** See `references/beads-integration.md` for detailed sync strategies and conflict resolution patterns.

### 5. Clean Up Git State

Clear old stashes and prune dead remote branches to maintain a clean repository state:

```bash
git stash clear              # Remove old stashes
git remote prune origin      # Clean up deleted remote branches
```

**Script:** Use `scripts/cleanup-git.sh` to perform git cleanup operations safely.

**Warning:** `git stash clear` permanently deletes all stashed changes. Only run this if you're certain stashed changes are no longer needed, or have been committed.

### 6. Verify Clean State

Confirm that all changes are committed and pushed, with no untracked files remaining:

```bash
git status                   # Should show clean working tree
git log origin/main..HEAD    # Should show no unpushed commits
```

**Script:** Use `scripts/check-git-state.sh` to verify the repository is in a clean state.

A clean state means:
- No modified files in working directory
- No staged but uncommitted changes
- No untracked files (or only expected untracked files like `.env`)
- No unpushed commits on current branch
- Current branch is up-to-date with remote

If the state is not clean:
1. Review what's uncommitted and determine if it should be committed or discarded
2. Push any unpushed commits
3. Decide whether to commit or stash untracked files

### 7. Choose a Follow-Up Issue for Next Session

Provide a prompt for the user to give you in the next session. This creates continuity and makes it easy to resume work.

Format the continuation prompt as:
```
Continue work on bd-X: [issue title]. [Brief context about what's been done and what's next]
```

Example:
```
Continue work on bd-142: Add integration tests for sync. Implemented the sync logic and basic unit tests. Next: add integration tests covering conflict resolution scenarios.
```

This prompt gives the next session (or next developer) clear context about:
- Which issue to work on
- What's already completed
- What needs to happen next

## Example Landing Session

See `examples/landing-session.sh` for a complete example of landing the plane, including all seven steps with realistic command output.

## Validation Scripts

Three validation scripts are provided to automate and verify key steps:

### scripts/check-git-state.sh

Validates that the git repository is in a clean state:
- No uncommitted changes
- No unpushed commits
- No untracked files (with configurable exceptions)

Run before ending the session to catch anything that needs attention.

### scripts/run-quality-gates.sh

Executes quality checks in sequence:
- Detects project type (Node.js, Python, Go, etc.)
- Runs appropriate test commands
- Runs linters and formatters
- Runs build commands
- Reports results with clear pass/fail status

Customize the script for your project's specific quality gates.

### scripts/cleanup-git.sh

Performs safe git cleanup operations:
- Clears git stashes (with confirmation)
- Prunes deleted remote branches
- Optional: removes merged local branches

Run to maintain repository hygiene at session end.

## Beads Integration

This skill is designed to work with the Beads issue tracking system via the `bd` CLI. Beads provides local-first issue tracking with sync capabilities.

Key Beads commands used in the protocol:
- `bd create` - File new issues
- `bd update` - Update issue status
- `bd close` - Close completed issues
- `bd sync` - Sync local and remote databases

**Reference:** See `references/beads-integration.md` for comprehensive Beads CLI documentation, sync strategies, and common patterns.

## Customization

Adapt this protocol to your workflow:

**Quality gates:** Modify `scripts/run-quality-gates.sh` to match your project's test/lint/build commands.

**Issue tracker:** While designed for Beads, adapt the protocol to work with GitHub Issues, Linear, Jira, or other trackers by replacing `bd` commands with appropriate CLI tools.

**Skip steps:** Not all steps apply to every session. For example, if no code was written, skip quality gates. Use judgment to apply the protocol pragmatically.

**Automation:** Consider creating a single "land" command that orchestrates the full protocol with appropriate prompts and confirmations.

## Best Practices

**Run quality gates before creating issues:** Catch test/lint failures early so you can file them as issues rather than discovering them later.

**Be thorough with issue filing:** Future you (or your teammate) will appreciate detailed context about remaining work. Don't skimp on issue descriptions.

**Don't skip the clean state check:** It's easy to forget uncommitted changes or unpushed commits. The clean state check prevents losing work.

**Make sync conflicts visible:** When syncing issues, make conflicts explicit rather than silently choosing one version. Document resolution decisions.

**Use the continuation prompt:** The follow-up issue prompt is valuable for resuming work efficiently. Include enough context to jump back in without extensive investigation.

## Troubleshooting

**Quality gates fail:** File a P0 issue with failure details. Consider reverting recent changes if the failure is blocking.

**Merge conflicts during issue sync:** Resolve carefully by examining both local and remote state. Prefer preserving both versions when in doubt.

**Uncommitted changes at clean state check:** Decide whether to commit, stash, or discard. Don't leave the session with uncommitted work unless intentional.

**Can't push commits:** Check for remote changes that need to be pulled first. Resolve merge conflicts if necessary.

## Additional Resources

### Reference Files

For detailed Beads integration guidance:
- **`references/beads-integration.md`** - Comprehensive Beads CLI documentation, sync strategies, conflict resolution patterns

### Example Files

Working examples in `examples/`:
- **`landing-session.sh`** - Complete example showing all seven steps with realistic output

### Scripts

Validation and automation utilities in `scripts/`:
- **`check-git-state.sh`** - Verify clean git repository state
- **`run-quality-gates.sh`** - Execute tests, linters, builds
- **`cleanup-git.sh`** - Safe git cleanup operations

## Summary

Landing the plane is about ending sessions with intention and care. By following this protocol, ensure that:
- No work is lost or forgotten
- Code meets quality standards
- Issue tracking reflects reality
- Repository state is clean and consistent
- Next session can start with clear direction

This systematic approach transforms chaotic session endings into smooth, professional handoffs.
