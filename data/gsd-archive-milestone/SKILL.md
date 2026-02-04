---
name: gsd-archive-milestone
description: Use gsd-complete-milestone instead. This command has been unified into the completion workflow. Shows deprecation notice and exits.
allowed-tools: Read
---

# Archive Milestone (DEPRECATED)

**This command has been replaced by gsd-complete-milestone.**

<objective>
DEPRECATED: This command has been unified into gsd-complete-milestone.
</objective>

<process>

<step name="show_deprecation_and_exit">
Display deprecation notice using GSD branded banner format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GSD ► DEPRECATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This command has been unified into the milestone completion workflow.

**Old workflow (deprecated):**
1. {{COMMAND_PREFIX}}complete-milestone    # Mark complete
2. {{COMMAND_PREFIX}}archive-milestone     # Move to milestones/ ← YOU ARE HERE
3. {{COMMAND_PREFIX}}restore-milestone     # Retrieve from milestones/

**New workflow (unified):**
{{COMMAND_PREFIX}}complete-milestone       # Archives directly to history/v{X.Y}/

All milestone files now move directly to `.planning/history/v{X.Y}/`
with mirrored directory structure during completion. Archives are
permanent and git-tracked.

───────────────────────────────────────────────────────────────

## Why This Changed

The old multi-step workflow created confusion about when files were
truly archived. The new unified workflow moves everything to permanent
history/ storage in a single atomic operation.

**To review archived milestones:**
{{COMMAND_PREFIX}}list-milestones

**To start new milestone:**
{{COMMAND_PREFIX}}new-milestone

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Exit immediately without executing any operations.
</step>

</process>

<success_criteria>
- [ ] Deprecation message displayed with branded banner
- [ ] Clear explanation of old vs new workflow
- [ ] User directed to correct command (complete-milestone)
- [ ] No file operations executed
- [ ] Template variables ({{COMMAND_PREFIX}}) used for cross-platform support
</success_criteria>
