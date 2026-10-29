---
name: spec-kit-feedback
description: |
  Capture workflow usage data for spec-kit optimization. Auto-activates when:
  (1) completing a spec-kit workflow (/speckit.review, final commit),
  (2) encountering friction or confusion during workflows,
  (3) user mentions issues with prompts or templates,
  (4) workflow deviates from expected quality gates.
  Reminds to export chat logs and tracks patterns for feedback.
---

# Spec-Kit Feedback Skill

Capture usage patterns during spec-kit workflows to help improve prompts and templates.

## Purpose

This skill helps collect data that can be used to improve spec-kit-extensions:
- Tracks workflow completion patterns
- Identifies friction points
- Reminds to export chat logs at key moments
- Prepares data for RL intake submissions

## When This Skill Activates

### Workflow Completion

When a workflow reaches completion (review passed, PR created, etc.):

```
📋 Workflow Complete - Consider Capturing Feedback

This session used the {{WORKFLOW}} workflow. If you'd like to help
improve spec-kit, consider exporting this chat log for analysis.

Quick export:
  claude export --format markdown > workflow-session.md

The spec-kit team uses this data to improve prompts and templates.
```

### Friction Detected

When the conversation shows signs of friction:
- Multiple clarification questions
- Retries or corrections
- User redirecting the agent
- Confusion about next steps

```
🔍 Friction Point Noted

I noticed some confusion around [specific area]. This is valuable
feedback for improving the {{WORKFLOW}} workflow.

Consider noting this in your feedback:
- What was confusing
- What would have helped
- How it was resolved
```

### Quality Gate Issues

When quality gates are skipped or cause problems:

```
⚠️ Quality Gate Observation

The {{GATE}} gate was [skipped/problematic]. This pattern helps
identify gates that may need adjustment.

If this gate felt unnecessary or blocking, note why in feedback.
```

## Automatic Tracking

Throughout the session, this skill tracks:

### Metrics (Mental Notes)

- **Workflow type**: Which workflow is being used
- **Clarification count**: How many times clarification was needed
- **Retry count**: How many corrections/retries occurred
- **Gate compliance**: Which gates were followed/skipped
- **Completion status**: Did workflow complete successfully

### Patterns to Note

When these occur, make a mental note for the summary:

| Pattern | Indicates |
|---------|-----------|
| "I don't understand" | Prompt clarity issue |
| "Let me try again" | Instruction ambiguity |
| "Actually, I meant..." | Template structure issue |
| Skipped template section | Section may be unnecessary |
| Added content not in template | Missing template section |
| User took over a step | Automation gap |

## End-of-Session Summary

When the workflow completes or session ends, offer a summary:

```
📊 Session Summary

Workflow: {{WORKFLOW}}
Status: {{COMPLETE/PARTIAL/FAILED}}
Duration: ~{{TIME}} (estimated from conversation length)

Observations:
- Clarifications needed: {{N}}
- Retries/corrections: {{N}}
- Gates followed: {{N}}/{{TOTAL}}

{{#if friction_points}}
Friction Points:
{{#each friction_points}}
- {{this}}
{{/each}}
{{/if}}

{{#if positive_patterns}}
What Worked Well:
{{#each positive_patterns}}
- {{this}}
{{/each}}
{{/if}}

To contribute this feedback:
1. Export chat: claude export --format markdown > session.md
2. Share with spec-kit team or submit to RL intake
```

## Export Instructions

### Claude Code

```bash
# Export this session
claude export --format markdown > spec-kit-session-$(date +%Y%m%d).md

# Or find session ID first
claude sessions list
claude export --session <id> --format markdown > session.md
```

### Preparing for RL Intake

If submitting to spec-kit-extensions for analysis, include:

1. **Chat log** (exported above)
2. **Spec files** created:
   ```bash
   cp -r specs/{{WORKFLOW}}/{{NUM}}-*/ feedback-specs/
   ```
3. **Git commits**:
   ```bash
   git log --oneline {{BRANCH}} > feedback-commits.txt
   ```
4. **Test results** (if available):
   ```bash
   npm test 2>&1 | tee feedback-tests.txt
   ```

### Privacy Note

Before sharing:
- Remove proprietary business logic
- Redact API keys, passwords, personal info
- Keep workflow structure and agent interactions
- Focus on the process, not the content

## Feedback Channels

Ways to share feedback:

1. **GitHub Issue**: Open an issue at spec-kit-extensions repo
2. **RL Intake**: Maintainers run `/rl-intake` with your data
3. **Direct**: Share exported session with maintainer

## What Makes Good Feedback

### Most Valuable

- Sessions with friction (confusion, retries, user takeover)
- Failed or abandoned workflows
- Workarounds you had to use
- Sections you skipped and why
- Content you added that wasn't in templates

### Less Valuable

- Perfectly smooth sessions (nice, but less actionable)
- Heavily redacted sessions (hard to analyze context)
- Partial exports (missing key decision points)

## Integration with Workflow Commands

This skill complements the spec-kit commands:

| Command | This Skill's Role |
|---------|-------------------|
| `/speckit.specify` | Track spec creation friction |
| `/speckit.plan` | Note planning clarifications |
| `/speckit.tasks` | Observe task breakdown issues |
| `/speckit.bugfix` | Monitor regression test compliance |
| `/speckit.review` | Capture review feedback |

## Suggested Workflow Tags

When exporting, consider adding tags to help categorize:

```markdown
---
workflow: bugfix
friction_level: medium
gates_followed: 3/4
key_friction: "regression test timing unclear"
---
```

This helps the RL intake process prioritize analysis.
