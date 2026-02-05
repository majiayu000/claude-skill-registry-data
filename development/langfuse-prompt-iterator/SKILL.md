---
name: langfuse-prompt-iterator
description: Comprehensive prompt iteration workflow for debugging and improving Langfuse prompts. Analyzes codebase usage, sets up reproducible tests, runs iterative refinement cycles with user feedback. Use when user says "prompt X isn't working right", "improve prompt", "iterate on prompt", "refine prompt", or "test prompt changes".
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Langfuse Prompt Iterator - Comprehensive Iteration Workflow

## Overview

This skill provides a complete workflow for iterating on Langfuse prompts with a test-driven, feedback-based approach. It handles everything from initial setup through multiple refinement cycles.

## When Claude Should Use This Skill

**Primary Triggers:**
- "Prompt X isn't working right"
- "Let's improve the [prompt_name] prompt"
- "I want to iterate on [prompt_name]"
- "Help me refine the [prompt_name] prompt"
- "Test changes to [prompt_name]"
- "Debug the [prompt_name] prompt"

**Context:** User has identified a prompt that needs improvement, either through observing bad behavior or wanting to enhance it proactively.

## The Complete Iteration Workflow

### Phase 1: Initial Setup & Context Gathering

**Step 1.1: Identify Environment & Version**
```
ASK USER:
1. Which environment should we pull from? (staging/production)
2. Do you want to work from a specific tag/label? (production/development/staging/etc.)
3. If known, what version number should we start from?

DEFAULT: staging environment, "production" label (latest active version)
```

**Step 1.2: Pull Current Prompt**
Use the `refresh_prompt_cache.py` script from langfuse-prompt-viewer:
```bash
cd .claude/skills/langfuse-prompt-viewer
uv run python refresh_prompt_cache.py PROMPT_NAME
```

This creates:
- `docs/cached_prompts/PROMPT_NAME_production.txt`
- `docs/cached_prompts/PROMPT_NAME_production_config.json`

Read both files to understand current state.

**Step 1.3: Investigate Codebase Usage**
Search for how this prompt is used in the codebase:

```bash
# Find where prompt is called
grep -r "PROMPT_NAME" api/src --include="*.py"

# Look for context_params being passed
# Common patterns to search:
# - build_agent_context(
# - build_agent_instructions(
# - get_prompt(
# - create_prompt(
```

**CRITICAL:** Identify what `context_params` are passed to this prompt. These tell you:
- What variables are available in the prompt template
- What data needs to be mocked/provided for testing
- How the prompt integrates with the application

**Step 1.4: Understand Iteration Goals**
```
ASK USER:
"What are the goals for improving this prompt? For example:
- Fix specific incorrect behavior (describe the issue)
- Improve tone/style (what direction?)
- Add new capabilities (what should it handle?)
- Reduce errors/hallucinations
- Better adherence to instructions
- Other?"

CAPTURE: User's specific goals as success criteria
```

### Phase 2: Establish Baseline (Milestone 1)

**Step 2.1: Choose Test Approach**

```
ASK USER:
"Do you have a Langfuse trace ID that demonstrates the problem?

If YES → We'll use that trace as our test case
If NO → We'll work together to create a reproducible test scenario"
```

**Option A: Starting from Trace ID**

If user provides a trace ID:

1. Use `fetch_trace.py` to pull trace data:
```bash
cd .claude/skills/langfuse-prompt-viewer
uv run python fetch_trace.py TRACE_ID
```

2. Extract from trace:
   - Input parameters (message content, context, etc.)
   - Actual context_params used
   - Original output
   - Why it was problematic

3. Create test case file: `test_case_from_trace_TRACE_ID.json`

**Option B: Creating New Test Scenario**

If no trace provided:

1. Use the test setup script:
```bash
cd .claude/skills/langfuse-prompt-iterator
uv run python setup_test_case.py PROMPT_NAME
```

2. Work with user to fill in:
   - Required context_params (from codebase investigation)
   - Example input data
   - Expected behavior

3. Save as: `test_case_manual_TIMESTAMP.json`

**Step 2.2: Run Initial Test (Baseline)**

Execute the test using:
```bash
cd .claude/skills/langfuse-prompt-iterator
uv run python test_prompt.py PROMPT_NAME test_case_FILE.json --baseline
```

This script:
- Loads the test case
- Calls the prompt with proper context
- Captures the LLM response
- Saves output with trace ID
- Returns formatted result

**MILESTONE 1 ACHIEVED:** You now have:
- ✅ Current prompt version
- ✅ Reproducible test case
- ✅ Baseline output
- ✅ Trace ID for baseline run

### Phase 3: Iterative Refinement Loop

**Step 3.1: Review Output with User**

```
SHOW USER:
1. The full LLM output
2. Highlight key sections (based on context_params and goals)
3. Ask: "What do you see wrong with this output?"

CAPTURE:
- Specific issues identified
- User's assessment against goals
- Any patterns noticed
```

**Step 3.2: Analyze Feedback**

Review the prompt against user feedback:
1. Read the current prompt text
2. Map feedback to specific prompt sections:
   - System instructions
   - Output format specifications
   - Examples provided
   - Constraints/rules
   - Variable usage

3. Identify root causes:
   - Missing instructions?
   - Ambiguous wording?
   - Conflicting directives?
   - Wrong examples?
   - Incorrect constraints?

**Step 3.3: Generate Improvement Options**

```
PRESENT TO USER:
"Based on your feedback, here are 2-3 options for improving the prompt:

**Option 1: [Brief title]**
- What: [Specific change]
- Why: [How it addresses feedback]
- Risk: [Any potential side effects]

**Option 2: [Brief title]**
- What: [Different approach]
- Why: [Alternative reasoning]
- Risk: [Trade-offs]

**Option 3: [Brief title]**
- What: [Third approach if relevant]
- Why: [Why this might work]
- Risk: [Considerations]

Which option do you prefer, or would you like to suggest a different approach?
Alternatively, point me to a specific section you think needs work."
```

**Step 3.4: Handle User Direction**

Be ready for:
- **Choice selection:** "Let's try Option 2"
- **Section focus:** "I think the problem is in the output format section"
- **Custom suggestion:** "Actually, I think we should..."
- **Combination:** "Option 1 for the instructions, but Option 2's approach for examples"

If user focuses on a specific section, re-analyze just that section and provide targeted options.

**Step 3.5: Make the Change**

Once agreed:

1. Use Edit tool to update the cached prompt file:
```
Edit the file: docs/cached_prompts/PROMPT_NAME_production.txt
- Make the specific change discussed
- Preserve all variable placeholders {{like_this}}
- Update version comment at top
```

2. Show diff of changes:
```bash
git diff --no-index docs/cached_prompts/PROMPT_NAME_production.txt
```

3. Get user confirmation: "Does this change look correct?"

**Step 3.6: Push Updated Prompt**

Push to staging (or production if explicitly requested):
```bash
cd .claude/skills/update-langfuse-staging-server-prompt
uv run python push_to_staging.py PROMPT_NAME

# For production (requires confirmation):
# uv run python push_to_staging.py PROMPT_NAME --production
```

**IMPORTANT:** The push creates a NEW VERSION in Langfuse (e.g., v2, v3, etc.)

**Step 3.7: Re-run Test with New Version**

```bash
cd .claude/skills/langfuse-prompt-iterator
uv run python test_prompt.py PROMPT_NAME test_case_FILE.json --version VERSION_NUMBER
```

This:
- Runs same test case
- Uses the NEW prompt version
- Captures new trace ID
- Returns new output

**Step 3.8: Fetch New Trace & Extract Response**

```bash
cd .claude/skills/langfuse-prompt-viewer
uv run python fetch_trace.py NEW_TRACE_ID
```

Extract the LLM generation span to get the actual model output.

**Step 3.9: Compare & Loop**

Show user:
- New output
- Side-by-side comparison with baseline (if helpful)
- What changed in the response

Ask: "How does this look? Are we closer to the goal?"

**LOOP BACK to Step 3.1** until user is satisfied or needs different approach.

### Phase 4: Bulk Testing (Optional)

**When to use:** User wants to see behavior across multiple scenarios or iterations.

```
ASK USER:
"Would you like me to run this prompt N times to see consistency/variations?
Or would you like to test against multiple different test cases?"
```

**Option A: Run Same Test N Times**
```bash
cd .claude/skills/langfuse-prompt-iterator
uv run python bulk_test_runner.py PROMPT_NAME test_case_FILE.json --runs 5
```

**Option B: Test Against Multiple Cases**
```bash
# User provides multiple test case files
uv run python bulk_test_runner.py PROMPT_NAME test_cases/*.json
```

**Output:** Creates `bulk_test_results_TIMESTAMP.md` with:
- All outputs
- Comparison table
- Variance analysis
- Summary statistics

Present this to user for bulk feedback.

## Supporting Scripts Reference

### 1. setup_test_case.py
Creates a test case template with proper structure.

```bash
uv run python setup_test_case.py PROMPT_NAME [--from-trace TRACE_ID]
```

### 2. test_prompt.py
Executes a prompt with test case data.

```bash
uv run python test_prompt.py PROMPT_NAME test_case.json [--version V] [--baseline]
```

### 3. bulk_test_runner.py
Runs multiple test iterations.

```bash
uv run python bulk_test_runner.py PROMPT_NAME test_case.json --runs N
```

### 4. compare_outputs.py
Generates side-by-side comparison of outputs.

```bash
uv run python compare_outputs.py trace_id_1 trace_id_2
```

## Best Practices for Using This Skill

1. **Always establish baseline first** - Don't skip Phase 2
2. **One change at a time** - Make focused changes in Phase 3
3. **Save test cases** - They're reusable for future iterations
4. **Track versions** - Note which version corresponds to which change
5. **Bulk test before production** - Run multiple times before promoting
6. **Document learnings** - Keep notes on what worked/didn't work

## Safety Notes

- This skill pushes to STAGING by default (safe)
- Production pushes require explicit user confirmation
- All prompts pushed WITHOUT labels (human must activate in UI)
- Test cases may contain PII - handle according to data policies
- Langfuse traces contain actual user data - be careful with sharing

## Environment Setup

Requires same environment variables as other Langfuse skills:
```bash
# In arsenal/.env:
LANGFUSE_PUBLIC_KEY_STAGING=pk-lf-...  # pragma: allowlist-secret
LANGFUSE_SECRET_KEY_STAGING=sk-lf-...  # pragma: allowlist-secret
LANGFUSE_HOST_STAGING=https://langfuse.staging.cncorp.io

# Optional for production:
LANGFUSE_PUBLIC_KEY_PROD=pk-lf-...  # pragma: allowlist-secret
LANGFUSE_SECRET_KEY_PROD=sk-lf-...  # pragma: allowlist-secret
LANGFUSE_HOST_PROD=https://langfuse.prod.cncorp.io

# Required for test execution:
OPENAI_API_KEY=sk-...  # pragma: allowlist-secret
```

## Troubleshooting

**Prompt not found:**
- Check environment (staging vs prod)
- Verify prompt name spelling
- Ensure label exists in that environment

**Test execution fails:**
- Verify context_params match codebase usage
- Check that required environment variables are set
- Ensure test case JSON is valid

**Push fails:**
- Verify credentials for target environment
- Check network connection
- Ensure prompt file is valid format

**Trace fetch fails:**
- Verify trace ID is correct
- Check you're querying correct Langfuse server
- Ensure trace exists and hasn't been deleted
