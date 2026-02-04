---
name: study-guide-verifier
description: |
  CRITICAL AUTOMATION: Automatically performs comprehensive study guide verification using the study-guide-analyzer agent.

  ACTIVATES when user requests accuracy verification, post-creation validation,
  or analysis of existing study guides.

  Launches the study-guide-analyzer agent to implement systematic 6-step verification protocol,
  ensuring study guides contain only source-accurate information with complete coverage and proper formatting.
skill_type: domain
enforcement_level: suggest
priority: critical
version: 2.1.0
tools_required:
  - Task
  - Read
activation_confidence: high
---

# Study Guide Verifier

## Core Responsibility

**Automatically verify study guide accuracy and completeness** using the study-guide-analyzer agent for systematic 6-step analysis.

**CRITICAL: ALWAYS use the study-guide-analyzer agent for verification. NEVER perform manual inline verification for study guides.**

## When This Activates

**Prompt triggers:**
- "verify accuracy"
- "check study guide"
- "analyze accuracy"
- "verify [filename]"
- "/verify-accuracy [file] [source]"
- "post-creation verification"
- "check completeness"
- "validate study guide"

**File triggers:**
- Study guide files in `Claude Study Tools/`
- Files ending in `.xlsx`, `.docx`, `.html`
- After creating study guides (automatic post-creation)

**Intent patterns:**
- Need quality assurance for created materials
- Want to ensure source accuracy
- Checking for missing content
- Validating template compliance

## How This Works

### Automatic Agent Invocation

When verification is needed, this skill automatically:

1. **Launches the study-guide-analyzer agent**
2. **Agent performs systematic 6-step analysis:**
   - Step 1: Read source file completely
   - Step 2: Read study guide completely
   - Step 3: Systematic verification checks (source accuracy, names, merged cells, info accuracy, format, completeness, **LO text fidelity**)
   - Step 4: Document all issues (categorized by severity)
   - Step 5: Save analysis report to file
   - Step 6: Return to parent with summary and request approval

**CRITICAL - LO Text Fidelity Check (Check 3.7):**
Learning objective STATEMENTS must be verbatim from source. For every LO, compare character-by-character with source. Flag ANY rewording as CRITICAL issue. (Answers/explanations CAN be paraphrased.)

3. **Agent returns comprehensive report:**
   - Executive summary with overall assessment
   - Critical/Important/Minor issues documented
   - Statistics (coverage %, issue counts)
   - Specific fix recommendations
   - Request for approval before changes

### Required Action Pattern

When verification is needed, you MUST:

```
I'll use the study-guide-analyzer agent to perform comprehensive 6-step verification of [filename].
```

Then invoke the agent using the Task tool:

```markdown
Use the study-guide-analyzer agent to verify [study-guide-filename] against [source-filename]. Perform systematic 6-step analysis and save detailed report.
```

**CRITICAL:** Wait for the agent to complete and return the analysis report before proceeding.

## Example Workflow

**User request:** "Verify accuracy of HIV_Drug_Chart.xlsx"

**Your response:**
1. Identify source file for the study guide
2. **Invoke agent:** "I'll use the study-guide-analyzer agent to perform comprehensive verification"
3. **Wait for agent report**
4. **Review agent findings** from saved analysis file
5. **Present summary** to user
6. **Request approval** for any fixes
7. **Only implement fixes after approval**

## Agent Integration

### When to Launch Agent

Launch the study-guide-analyzer agent when:
- User explicitly requests verification
- Post-creation verification (automatic after study guide creation)
- User asks to check accuracy, completeness, or quality
- Before finalizing study guide for use
- After making significant edits to existing study guide

### How to Launch Agent

Use the Task tool:

```
Task(
  subagent_type="general-purpose",
  description="Verify study guide accuracy",
  prompt="Use the study-guide-analyzer agent to verify [study-guide-filename] against [source-filename]. Perform systematic 6-step verification: read both files completely, check source accuracy, template compliance, completeness, and quality. Save detailed analysis report to same directory as study guide. Report should include executive summary, categorized issues, statistics, and specific fix recommendations."
)
```

### Agent Output

The agent saves a comprehensive analysis report:

**File location:** `[study-guide-directory]/[filename]-analysis-report.md`

**Report structure:**
```markdown
# Study Guide Analysis Report: [Filename]

## Executive Summary
[Overall assessment, recommendation]

## Critical Issues (Must Fix)
[Detailed list with location, problem, fix]

## Important Improvements (Should Fix)
[Detailed list]

## Minor Suggestions (Nice to Have)
[Detailed list]

## Detailed Verification Results
[PASS/FAIL for each category]

## Statistics
[Coverage %, issue counts]

## Next Steps
[Specific actions needed]
```

## Integration with Study Guide Creation

### Post-Creation Verification (Automatic)

When creating study guides, this skill triggers automatically:

**After Excel drug chart creation:**
```
Post-creation verification complete. I'll now use the study-guide-analyzer agent to verify accuracy.
```

**After Word study guide creation:**
```
Study guide created. Running post-creation verification with study-guide-analyzer agent.
```

**After HTML guide creation:**
```
HTML study guide complete. Launching study-guide-analyzer agent for comprehensive verification.
```

### Manual Verification (On-Demand)

User explicitly requests:
```
User: "Verify accuracy of Cardiovascular_Study_Guide.docx"
You: "I'll use the study-guide-analyzer agent to perform 6-step verification."
```

## Quality Assurance

### Verification Checklist

Before accepting verification results:
- ✓ Agent completed all 6 steps
- ✓ Analysis report saved to correct location
- ✓ Executive summary includes overall assessment
- ✓ Issues categorized by severity (Critical/Important/Minor)
- ✓ **LO text fidelity checked** (LO statements verbatim from source)
- ✓ Statistics calculated (coverage %, issue counts)
- ✓ Specific fix recommendations provided
- ✓ Approval requested before changes

### What Gets BLOCKED

❌ Manual inline verification for complex study guides
❌ Skipping systematic analysis
❌ Implementing fixes without approval
❌ Incomplete verification (missing steps)

## Enforcement

This skill works with study guide workflow:
- **Suggests**: "Use study-guide-analyzer agent for verification"
- **Does not block**: Verification can be skipped, but not recommended
- **Critical priority**: Strongly recommended for all study guides before use

## Examples

### Example 1: Post-Creation Excel Verification

**Trigger:** Just created Excel drug chart

**Skill activation:**
```
Post-creation verification complete. I'll now use the study-guide-analyzer agent to verify the drug chart against the source file.
```

**Agent performs:**
- Reads source file completely
- Reads Excel file completely
- Checks all 4 tabs
- Verifies drug names, classifications, merged cells
- Checks Master Chart completeness
- Documents all issues

**Returns:** Analysis report with 0 critical issues, 2 minor suggestions

**Result:** User approves study guide for use

### Example 2: Manual Word Guide Verification

**Trigger:** User asks to verify existing Word doc

**Skill activation:**
```
I'll use the study-guide-analyzer agent to verify your Word study guide for completeness and accuracy.
```

**Agent performs:**
- Reads source lecture notes
- Reads Word document
- Checks all learning objectives answered
- Verifies comparison tables
- Checks Master Chart
- Identifies 3 missing topics

**Returns:** Analysis report with 3 critical issues (missing topics)

**Result:** Agent recommends fixes, waits for approval, adds missing content

### Example 3: HTML LO Guide Verification

**Trigger:** Slash command `/verify-accuracy`

**Skill activation:**
```
I'll use the study-guide-analyzer agent per the verify-accuracy command.
```

**Agent performs:**
- Systematic 6-step analysis
- Checks all 4 HTML tabs
- Verifies learning objectives completeness
- Checks key comparisons accuracy
- Validates master tables

**Returns:** Analysis report - PASS all checks

**Result:** Study guide approved, ready for exam prep

## Troubleshooting

### Agent not launching

**Check:**
- Is study-guide-analyzer.md in `.claude/agents/` directory?
- Is Task tool available?
- Are file paths correct (study guide + source)?

**Fix:** Verify agent file exists and launch manually with correct paths

### Analysis incomplete

**Agent should complete all 6 steps:**
- If analysis seems incomplete, re-launch agent
- Check analysis report file for all sections
- Verify agent had access to both files

### Can't find source file

**Agent needs source file path:**
- Ask user for source file location
- Check common locations (Extract/, Sources/)
- Look in same directory as study guide

### No issues found but study guide seems wrong

**Re-run verification:**
- Verify agent read correct source file
- Check if template expectations match actual template used
- Manual spot-check a few items

## Best Practices

1. **Always use agent** - Don't perform manual verification for study guides
2. **Verify immediately after creation** - Catch issues early
3. **Read analysis report** - Don't just rely on summary
4. **Request approval before fixes** - Never auto-fix without permission
5. **Re-verify after fixes** - Ensure fixes didn't introduce new issues
6. **Save analysis reports** - Keep for future reference

## Slash Command Integration

The `/verify-accuracy` slash command automatically invokes this skill and agent:

**Command usage:**
```
/verify-accuracy "path/to/study-guide.xlsx" "path/to/source.txt"
```

**What happens:**
1. Slash command triggers this skill
2. Skill launches study-guide-analyzer agent
3. Agent performs 6-step analysis
4. Agent saves report and returns summary
5. User reviews findings and approves fixes

## Progressive Disclosure

**This skill is lightweight:**
- Main instructions: This file (~360 lines)
- Agent file: Loaded only when agent launched
- Deep-dive resources: Loaded on-demand when needed

**Performance:** Agent analysis takes 1-2 minutes, but provides comprehensive verification that would take 10-15 minutes manually and catches issues that might be missed.

### Deep-Dive Resources

For comprehensive guidance on verification methodology:

**[6-Step Protocol Detailed](resources/6-step-protocol-detailed.md)** - Complete walkthrough of the study-guide-analyzer agent's systematic verification methodology, with examples for each step

**[Common Errors Guide](resources/common-errors.md)** - Reference for the top 10 most common errors in study guides, with detection and prevention strategies

**Note:** Resources provide detailed methodology that complements the agent's automated verification. Load these if you need to understand the verification process in depth.

---

## Integration with Other Skills

**Works with:**
- **source-only-enforcer:** Verifies source-only policy during verification
- **template-compliance-checker:** Validates template adherence
- **mnemonic-researcher:** Checks mnemonics were researched (not invented)
- **drug-classification-assistant:** Validates drug groupings

**Workflow:**
1. source-only-enforcer ensures creation uses only source
2. study-guide-verifier (this skill) performs post-creation analysis
3. template-compliance-checker validates formatting
4. User approves fixes
5. study-guide ready for use

---

**Remember:** The study-guide-analyzer agent is your quality assurance automation. Always use it for comprehensive verification instead of manual checking. It catches issues you might miss and provides systematic, reproducible analysis.
