---
description: Optimize forms for completion rate
---

# Form CRO

Optimize forms for "$ARGUMENTS" to maximize completion rate. Analyze form design, field selection, and user experience to reduce abandonment.

## Prerequisites

Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "$ARGUMENTS". Run `/marketing:customer-research $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/marketing/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md` for audience context
   - Read `.metapowers/marketing/$ARGUMENTS/02-act.md` if it exists

2. **Form audit (if URL or form provided):**
   - Evaluate number of fields (every field is friction)
   - Check field labels and placeholder text clarity
   - Analyze validation feedback and error messages
   - Review mobile form experience

3. **Field optimization:**
   - Which fields are truly necessary? Remove everything else
   - Multi-step vs. single-step form decision
   - Smart defaults and auto-fill opportunities
   - Progressive profiling (ask more over time, not all at once)

4. **UX improvements:**
   - Clear form title and context (why should they fill this out?)
   - Progress indicators for multi-step forms
   - Inline validation vs. submit-time validation
   - Submit button copy (specific benefit, not "Submit")
   - Social proof near the form (trust signals)
   - Privacy assurance near email fields

5. **Write the artifact** — append to `.metapowers/marketing/$ARGUMENTS/02-act.md` under a `## Form CRO` section:
   - **Current Form Assessment** — field count, friction points
   - **Field Recommendations** — what to keep, remove, add
   - **UX Improvements** — layout, validation, copy
   - **Multi-Step Recommendation** — if applicable
   - **Expected Impact** — estimated completion rate improvement

## Output

Form CRO analysis appended to `.metapowers/marketing/$ARGUMENTS/02-act.md`. Present a summary highlighting:
- Number of unnecessary fields identified
- Top UX improvement
- Recommended form structure
