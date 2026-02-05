---
name: learn-from-mistake
description: Investigate agent mistakes, perform root cause analysis, and update configurations to prevent recurrence
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

> **🚨 MANDATORY INVOCATION PATTERN**
>
> This skill MUST be invoked using the Task tool with `subagent_type: "general-purpose"`:
> ```
> Task(
>   subagent_type: "general-purpose",
>   description: "Investigate mistake and implement prevention",
>   prompt: "Invoke the learn-from-mistakes skill to investigate [describe mistake]...",
>   model: "opus"
> )
> ```
> DO NOT run this skill inline in the main conversation. The investigation and prevention workflow
> requires focused context that benefits from subagent isolation.

# Learn From Mistake Skill

**Purpose**: Investigate agent mistakes, perform root cause analysis, update agent configurations, and TEST fixes by reproducing the original mistake to verify prevention.

**When to Use**:
- After an agent makes a mistake that causes delays, rework, or violations
- When a pattern of similar mistakes is observed across tasks
- To proactively improve agent behavior based on lessons learned
- When protocol violations occur that should have been caught

## Skill Workflow

**🚨 CRITICAL: Prevention BEFORE Fixing**

**DO NOT fix the immediate issue before completing prevention steps.**

The natural instinct is to fix the problem first, then worry about prevention. This is WRONG because:
1. Once fixed, urgency disappears and prevention gets skipped
2. The mistake context is freshest BEFORE fixing
3. Fixing first signals "prevention is optional"

**MANDATORY ORDER**:
1. **STOP** - Do not fix the immediate issue yet
2. **Complete Phases 1-5** - Identify, analyze, design, implement prevention
3. **Commit prevention** - Prevention changes go to main FIRST
4. **THEN fix** - Now fix the immediate issue
5. **Complete Phases 6-8** - Validate and document

❌ **WRONG**: Fix issue → Invoke skill → Maybe implement prevention
✅ **CORRECT**: Invoke skill → Implement prevention → Commit → Fix issue

---

## LFM Phase Enforcement {#lfm-phase-enforcement}

The `.claude/hooks/enforce-lfm-phases.sh` hook enforces the 3-phase workflow by blocking premature fixes.

### Phase State Machine

```
NONE ──(skill invoked)──> INVESTIGATE ──(analysis complete)──> PREVENT ──(prevention implemented)──> FIX ──(fix applied)──> COMPLETE
```

| Phase | Allowed Actions | Blocked Actions |
|-------|-----------------|-----------------|
| **INVESTIGATE** | Read conversation logs, analyze root cause, identify triggering thought | ❌ Edit target source file |
| **PREVENT** | Create hooks, update configs, write prevention mechanism | ❌ Edit target source file |
| **FIX** | Edit target source file, apply immediate fix | (all allowed) |
| **COMPLETE** | (workflow finished) | (all allowed) |

### State File

Phase state is tracked in: `/tmp/lfm_state_${SESSION_ID}.json`

```json
{
  "phase": "INVESTIGATE|PREVENT|FIX|COMPLETE",
  "mistake_id": "descriptive-id",
  "target_file": "path/to/file/needing/fix.java"
}
```

### Phase Transitions

**To start LFM workflow** (invokes this skill):
```bash
echo '{"phase":"INVESTIGATE","mistake_id":"wrong-worktree","target_file":"src/Main.java"}' > /tmp/lfm_state_${SESSION_ID}.json
```

**To transition INVESTIGATE → PREVENT** (after root cause analysis):
```bash
jq '.phase = "PREVENT"' /tmp/lfm_state_${SESSION_ID}.json > /tmp/tmp.json && mv /tmp/tmp.json /tmp/lfm_state_${SESSION_ID}.json
```

**To transition PREVENT → FIX** (after prevention implemented):
```bash
jq '.phase = "FIX"' /tmp/lfm_state_${SESSION_ID}.json > /tmp/tmp.json && mv /tmp/tmp.json /tmp/lfm_state_${SESSION_ID}.json
```

### FIX Phase: Content Restoration Requirements

**⚠️ CRITICAL: When restoring deleted content, ALWAYS retrieve original from git history first.**

**DO NOT** write content from memory or understanding. **DO** copy the original exactly.

**Mandatory Restoration Procedure**:

```bash
# Step 1: Find the commit that originally added the content
git log --all --oneline --source | grep -i "<keyword>"

# Step 2: Retrieve the EXACT original content
git show <original-commit>:<file-path> | grep -A50 "<section-header>"

# Step 3: Copy that content EXACTLY into the target file
# DO NOT paraphrase, restructure, or "improve" the content

# Step 4: Verify restoration matches original
diff <(git show <original-commit>:<file-path> | grep -A50 "<section>") \
     <(cat <current-file> | grep -A50 "<section>")
# Empty diff = exact match ✅
```

**Common Mistake**:
```
❌ WRONG - Writing from memory/understanding:
   "I need to add the 'empty' section to java-human.md"
   → Writes paraphrased content with different structure

✅ CORRECT - Retrieve original first:
   git show e31ff13:docs/code-style/java-human.md | grep -A35 "Use \"empty\""
   → Copy that exact content
```

**Why This Matters**: Paraphrased content may:
- Have different structure (headers, bullet lists vs paragraphs)
- Miss details (like `@param` tags in examples)
- Use different terminology
- Fail verification when compared to original

**To complete workflow**:
```bash
echo '{"phase":"COMPLETE"}' > /tmp/lfm_state_${SESSION_ID}.json
# Or remove state file
rm /tmp/lfm_state_${SESSION_ID}.json
```

### Hook Behavior

When you try to edit the target file before completing earlier phases:

**In INVESTIGATE phase** (trying to fix):
```
❌ LEARN-FROM-MISTAKES PHASE VIOLATION

You're trying to fix the source file before completing investigation.

Current Phase: INVESTIGATE

MANDATORY WORKFLOW:
  1. INVESTIGATE → Gather evidence, identify root cause, find triggering thought
  2. PREVENT     → Implement prevention mechanism (hook, validation, code fix)
  3. FIX         → Only then fix the immediate issue
```

**In PREVENT phase** (trying to fix):
```
❌ LEARN-FROM-MISTAKES PHASE VIOLATION

You're trying to fix the source file before implementing prevention.

Prevention must be implemented BEFORE fixing. This ensures the same mistake
cannot recur.

PREVENTION HIERARCHY (choose highest applicable):
  1. code_fix   - Fix broken tool/code (HIGHEST priority)
  2. hook       - Automatic enforcement before/after execution
  3. validation - Automatic detection after execution
  4. config     - Documentation (LAST RESORT)
```

### Allowed Edits in All Phases

The hook only blocks edits to the **target file** (the file containing the bug/mistake). These are always
allowed:
- Creating/editing hooks (`.claude/hooks/*.sh`)
- Updating configuration (`.claude/settings.json`)
- Editing documentation (`docs/**/*.md`, `CLAUDE.md`)
- Modifying other source files not identified as the target

---

## 9-Phase Process

1. **Mistake Identification** - Gather context
2. **Conversation Analysis** - Review logs
3. **Root Cause Analysis** - Categorize and investigate cause
   - ⚠️ **STEP 1**: Documentation Verification (check if docs misled agent)
   - **STEP 2**: Temporal Analysis (check for existing fixes)
   - **STEP 3**: Triggering Thought (identify decision point)
4. **Configuration Updates** - Design prevention measures (ONLY after docs verified)
5. **Implement Updates** - Apply changes (BEFORE fixing immediate issue)
6. **Validation** - Review completeness
7. **Test by Reproduction** - ⚠️ Attempt to reproduce mistake to verify prevention
8. **Documentation** - Add inline comments and commit messages
9. **Cross-Session Logging** - ⚠️ Write mistake to `mistakes.json` for retrospective analysis

**Critical**: Phase 7 requires actually reproducing the mistake (not mental simulation) to verify fixes work.
**Critical**: Phase 9 is MANDATORY - all mistakes must be logged for pattern detection and effectiveness tracking.

### Phase 1: Mistake Identification

**Input Requirements**:
- Agent name that made the mistake (e.g., `architect`, `style`, `main`)
- Task name if applicable (e.g., `implement-formatter-api`)
- Description of what went wrong
- Conversation ID or timestamp range (optional - will search recent if not provided)

**Questions to Ask User**:
1. Which agent made the mistake?
2. What task were they working on?
3. What specifically went wrong?
4. Do you have the conversation ID? (Can skip - will search recent)

### Phase 2: Conversation Analysis

**Access Conversation Logs**:

First, get the session ID from the SessionStart system reminder (provided by `get-session-id` skill):
```
✅ Session ID: 88194cb6-734b-498c-ab5d-ac7c773d8b34
```

Then access conversation logs:
```bash
# REQUIRED: Use session ID from system reminder
SESSION_ID="88194cb6-734b-498c-ab5d-ac7c773d8b34"

# Verify session ID is provided
if [ -z "$SESSION_ID" ]; then
  echo "ERROR: Session ID not available in context." >&2
  echo "Expected system reminder: '✅ Session ID: {uuid}'" >&2
  echo "Provided by get-session-id skill at SessionStart." >&2
  exit 1
fi

# Main session conversation
MAIN_CONVERSATION="/home/node/.config/projects/-workspace/${SESSION_ID}.jsonl"

# Verify conversation file exists
if [ ! -f "$MAIN_CONVERSATION" ]; then
  echo "ERROR: Conversation file not found: $MAIN_CONVERSATION" >&2
  exit 1
fi

# Agent sidechain conversations (if investigating agent-specific mistakes)
AGENT_CONVERSATIONS=$(ls -t /home/node/.config/projects/-workspace/agent-*.jsonl 2>/dev/null | head -10)

# Read and parse conversation for agent mentions
jq -r "select(.message.content | tostring | contains(\"$AGENT_NAME\"))" "$MAIN_CONVERSATION"

# For agent sidechain logs
for agent_log in $AGENT_CONVERSATIONS; do
  grep -l "$AGENT_NAME" "$agent_log" 2>/dev/null && echo "Found in: $agent_log"
done
```

**What to Extract**:

1. **Agent Invocation Context**:
   - What prompt was given to the agent
   - What files/context were available
   - What state the task was in
   - Working directory specified

2. **Agent Actions**:
   - Sequence of tool calls made
   - Files read, written, edited
   - Commands executed
   - Directories changed to

3. **Mistake Manifestation**:
   - Error messages
   - Incorrect output
   - Protocol violations
   - Build failures
   - Rework needed

4. **Recovery Actions**:
   - What was done to fix the mistake
   - How much rework was required
   - What additional context was needed

### Phase 3: Root Cause Analysis

**⚠️ MANDATORY STEP 1: Documentation Verification**

**CRITICAL**: Before creating ANY preventative measures (hooks, configs, etc.), verify that the
documentation itself didn't mislead the agent.

**Why This Step Exists**: Agents follow documentation. If documentation is incorrect, vague, or
contradictory, the "mistake" may actually be the agent correctly following bad guidance. Creating hooks
to prevent behavior that documentation encourages creates confusion and wasted effort.

**Documentation Verification Procedure**:

1. **Identify what documentation the agent should have consulted**:
   - CLAUDE.md for general guidance
   - docs/project/*.md for protocol-specific rules
   - .claude/agents/*.md for agent-specific instructions

2. **Search for relevant guidance**:
   ```bash
   # Search for keywords related to the mistake
   grep -rn "todo.md\|archival\|commit.*main" docs/project/ CLAUDE.md
   ```

3. **Evaluate documentation quality**:

   | Issue | Example | Fix Required |
   |-------|---------|--------------|
   | **Missing** | No guidance on when to edit todo.md | Add documentation FIRST |
   | **Vague** | "Should" instead of "MUST" | Clarify with explicit rules |
   | **Contradictory** | CLAUDE.md says X, protocol says Y | Resolve conflict |
   | **Incorrect** | Documentation describes wrong workflow | Fix documentation |
   | **Clear but violated** | Agent ignored clear guidance | THEN create enforcement |

4. **Document findings BEFORE proceeding**:
   ```
   DOCUMENTATION VERIFICATION:
   - Relevant docs checked: [list files]
   - Documentation status: MISSING | VAGUE | CONTRADICTORY | INCORRECT | CLEAR
   - If not CLEAR:
     - Problem found: [specific issue]
     - Documentation fix needed: YES/NO
     - Fix applied: [commit hash if applicable]
   - Ready for enforcement: YES (only if docs are now clear)
   ```

**CRITICAL**: If documentation is not CLEAR, fix documentation BEFORE creating hooks/enforcement.
Creating enforcement for unclear rules causes:
- Agent confusion (following docs but blocked by hooks)
- Duplicate/conflicting guidance
- Wasted effort on wrong prevention

**Example - WRONG Approach**:
```
# Documentation says nothing about todo.md edits on main
# Agent edits todo.md on main
# ❌ WRONG: Create hook to block todo.md edits
# Result: Hook blocks behavior that docs never prohibited
```

**Example - CORRECT Approach**:
```
# Documentation says nothing about todo.md edits on main
# Agent edits todo.md on main
# Step 1: Add documentation clarifying the correct workflow
# Step 2: ONLY THEN consider if enforcement hook is needed
# Step 3: If hook created, it enforces documented policy
```

---

**⚠️ MANDATORY STEP 2: Check if Fix Already Exists (Temporal Analysis)**

**CRITICAL**: Before creating new fixes, determine if this is a NEW mistake or an INEFFECTIVE EXISTING FIX.

**Temporal Analysis Procedure**:

1. **Identify the mistake pattern** (e.g., "timing boundary misclassification", "worktree violation")
2. **Search git history for related fixes**:
   ```bash
   # Search commit messages for related keywords
   git log --all --format="%H %ai %s" --grep="timing.*boundary\|Error 8\|misclassification" | head -20
   ```
3. **Get violation timestamp from session**:
   ```bash
   SESSION_ID="<from-system-reminder>"
   VIOLATION_TIME=$(stat -c %y ~/.config/projects/-workspace/${SESSION_ID}.jsonl | cut -d' ' -f1-2)
   echo "Violation occurred: $VIOLATION_TIME"
   ```
4. **Compare timestamps**:
   ```bash
   # For each potentially related commit
   COMMIT_HASH="<from-git-log>"
   COMMIT_TIME=$(git show -s --format=%ai $COMMIT_HASH)
   echo "Fix implemented: $COMMIT_TIME"

   # Temporal relationship
   if [[ "$COMMIT_TIME" < "$VIOLATION_TIME" ]]; then
     echo "⚠️ FIX PREDATES VIOLATION - Existing fix is INEFFECTIVE"
   else
     echo "✅ Fix implemented AFTER violation - Reactive fix"
   fi
   ```

**Decision Matrix**:

| Temporal Relationship | Classification | Action Required |
|----------------------|----------------|-----------------|
| Fix exists BEFORE violation | **INEFFECTIVE FIX** | Improve/replace existing fix, NOT create duplicate |
| No related fix exists | **NEW MISTAKE** | Create new prevention measures |
| Fix exists AFTER violation | **REACTIVE FIX** | Verify fix is comprehensive, test it |

**Example Analysis**:

```bash
# Scenario: Timing boundary misclassification in session bc6b74a7

# Step 1: Find related commits
git log --all --format="%H %ai %s" --grep="timing\|Error 8" | head -5
# Output:
# 63f27ed 2025-11-13 07:39:04 -0500 Improve shrink-doc to prevent timing boundary misclassification
# 39f8f39 2025-11-12 21:20:44 -0500 Strengthen shrink-doc to prevent repeated misclassification
# 088e259 2025-11-12 16:39:56 -0500 Learn from shrink-doc mistake: Add Error 8

# Step 2: Get violation time
stat -c %y ~/.config/projects/-workspace/bc6b74a7*.jsonl
# Output: 2025-11-13 03:38:41 (Nov 12 22:38 EST)

# Step 3: Temporal analysis
# 088e259: Nov 12 16:39 (6 hours BEFORE violation) ← INEFFECTIVE
# 39f8f39: Nov 12 21:20 (1 hour BEFORE violation)  ← INEFFECTIVE
# 63f27ed: Nov 13 07:39 (9 hours AFTER violation)  ← REACTIVE

# Conclusion: Error 8 fix was implemented 6 hours before violation occurred
#            The fix is INEFFECTIVE and needs to be improved/replaced
```

**Output Required**:

Document the temporal analysis result:
```
TEMPORAL ANALYSIS RESULT:
- Mistake pattern: <pattern-name>
- Related commits: <commit-hash-list>
- Fix implementation date: <date-time>
- Violation date: <date-time>
- Classification: INEFFECTIVE FIX | NEW MISTAKE | REACTIVE FIX
- Evidence: <git-log-output-showing-timing>
```

If **INEFFECTIVE FIX** detected:
- Read the existing fix to understand what was tried
- Analyze why it didn't work (review conversation logs for agent behavior)
- Design improvement or replacement (not duplicate)
- Document in commit message: "Improve/Replace ineffective fix from commit <hash>"

**⚠️ MANDATORY STEP 3: Identify Triggering Thought Before Creating Fixes**

After temporal analysis, MUST:

1. Access `/home/node/.config/projects/-workspace/{session-id}.jsonl`
2. Find assistant message immediately before mistake
3. Extract exact text/thought before wrong decision
4. Document triggering quote

**Example**:

```bash
# Search for when file was created
grep -i "safety-analysis" conversation.jsonl | jq '.timestamp'
# Returns: 2025-11-02T04:31:37.673Z

# Get messages before that timestamp
jq 'select(.timestamp < "2025-11-02T04:31:37.673Z" and .timestamp > "2025-11-02T04:30:00.000Z")' conversation.jsonl

# Find triggering thought
jq 'select(.timestamp == "2025-11-02T04:31:10.998Z") | .message.content[].text' conversation.jsonl

# Result: "Given the complexity and length of fixing both skills completely,
#          let me create a summary document showing the critical fixes needed"
```

Root cause: Agent used "complexity and length" to justify creating summary instead of doing work (Token Usage Policy violation).

**Without triggering thought, prevention will be ineffective.**

**Automated Detection**:

```bash
#!/bin/bash
# Helper: Find triggering thought automatically

SESSION_ID="${1:-$(grep 'Session ID:' /tmp/session_context.txt | cut -d: -f2 | tr -d ' ')}"
MISTAKE_INDICATOR="${2:-}"  # e.g., "SAFETY-ANALYSIS.md", "BUILD FAILURE", "PROTOCOL VIOLATION"

if [[ -z "$SESSION_ID" || -z "$MISTAKE_INDICATOR" ]]; then
  echo "Usage: $0 <session-id> <mistake-indicator>" >&2
  echo "Example: $0 abc123 'SAFETY-ANALYSIS.md'" >&2
  exit 1
fi

CONVERSATION="/home/node/.config/projects/-workspace/${SESSION_ID}.jsonl"

if [[ ! -f "$CONVERSATION" ]]; then
  echo "ERROR: Conversation file not found: $CONVERSATION" >&2
  exit 1
fi

# Find timestamp when mistake occurred
MISTAKE_TIMESTAMP=$(jq -r --arg indicator "$MISTAKE_INDICATOR" \
  'select(.message.content | tostring | contains($indicator)) | .timestamp' \
  "$CONVERSATION" | head -1)

if [[ -z "$MISTAKE_TIMESTAMP" ]]; then
  echo "ERROR: Could not find mistake indicator '$MISTAKE_INDICATOR' in conversation" >&2
  exit 1
fi

echo "Mistake occurred at: $MISTAKE_TIMESTAMP"

# Find last assistant message before mistake (within 5 minutes)
FIVE_MINUTES_BEFORE=$(date -d "$MISTAKE_TIMESTAMP - 5 minutes" -Iseconds 2>/dev/null || \
                      date -v-5M -jf "%Y-%m-%dT%H:%M:%S" "${MISTAKE_TIMESTAMP%+*}" "+%Y-%m-%dT%H:%M:%S" 2>/dev/null)

TRIGGERING_THOUGHT=$(jq -r --arg before "$MISTAKE_TIMESTAMP" --arg after "$FIVE_MINUTES_BEFORE" \
  'select(.timestamp < $before and .timestamp > $after and .message.role == "assistant") |
   {timestamp, content: .message.content}' \
  "$CONVERSATION" | jq -s 'last')

if [[ -z "$TRIGGERING_THOUGHT" || "$TRIGGERING_THOUGHT" == "null" ]]; then
  echo "WARNING: Could not find assistant message before mistake" >&2
  exit 1
fi

echo ""
echo "TRIGGERING THOUGHT:"
echo "$TRIGGERING_THOUGHT" | jq -r '.content[] | select(.type == "text") | .text' | tail -20

# Also check for thinking blocks (often contain the decision reasoning)
echo ""
echo "ASSOCIATED THINKING (if any):"
echo "$TRIGGERING_THOUGHT" | jq -r '.content[] | select(.type == "thinking") | .thinking' | tail -20
```

**Usage**:
```bash
# Automatic detection
./find-triggering-thought.sh "$SESSION_ID" "PROTOCOL VIOLATION"

# Or inline
SESSION_ID="abc-123"
MISTAKE="wrong worktree"
jq -r --arg indicator "$MISTAKE" \
  'select(.message.content | tostring | contains($indicator))' \
  /home/node/.config/projects/-workspace/${SESSION_ID}.jsonl | \
  jq -r '.timestamp' | head -1
```

**Categorize the Mistake**:

#### A. Missing Information
- Agent prompt lacked necessary context
- Required files not mentioned
- Assumptions not stated explicitly
- Working directory not clear

#### B. Misunderstood Requirements
- Ambiguous protocol documentation
- Conflicting instructions
- Unclear success criteria
- No examples for this scenario

#### C. Tool Usage Errors
- Wrong tool for the job
- Incorrect parameters
- Missing validation steps
- Tool limitations not understood

#### D. Logic Errors
- Incorrect algorithm
- Missing edge cases
- Faulty assumptions
- Incomplete understanding of domain

#### E. Protocol Violations
- Skipped required steps
- Wrong state for action
- Missing validations
- Worktree confusion

#### F. Configuration Gaps
- Agent config missing examples
- No guidance for this scenario
- Anti-patterns not documented
- Missing checklists

**Investigate**:

1. **Available Information**: Agent prompt, files accessed, missing context
2. **Correct Action**: Expected sequence, needed information, missing checks
3. **Wrong Choice Reason**: Documentation gaps, ambiguous instructions, misleading examples, insufficient validation

### Phase 4: Configuration Updates

**⚠️ MANDATORY STEP 0: Policy Document Verification**

**Before adding ANY enforcement mechanism (hook, validation, etc.), you MUST verify the policy document
is correct.** Enforcement hooks cannot fix problems caused by incorrect or conflicting documentation.

**Why This Step Exists**: Session audit found hooks that logged "BLOCKED" but didn't actually block because
policy documentation conflicts prevented correct behavior. Specifically:
- CLAUDE.md said "Preserves audit files" for CLEANUP state
- task-protocol-operations.md said "Delete task directory" for CLEANUP state
- Hooks enforced the operations.md version but Claude followed CLAUDE.md

**Policy Verification Procedure**:

1. **Identify the policy being enforced**:
   - What behavior should the hook enforce?
   - Where is this behavior documented? (CLAUDE.md, task-protocol-*.md, style-guide.md, etc.)

2. **Search for existing policy**:
   ```bash
   # Search for the keyword/concept across all policy documents
   grep -rn "CLEANUP\|task directory\|preserve\|delete" docs/project/ CLAUDE.md
   ```

3. **Check for policy problems** (any of these require documentation fix FIRST):

   **A. Missing Policy** - Behavior not documented at all
   - Search returns no relevant results
   - Action: Write the policy in appropriate document BEFORE creating hook
   - Without documented policy, Claude cannot know what behavior is expected

   **B. Vague Policy** - Behavior mentioned but not clearly specified
   - Documentation says "should" or "may" instead of "MUST"
   - No concrete examples of correct/incorrect behavior
   - Missing edge cases or boundary conditions
   - Action: Clarify with explicit requirements, ✅/❌ examples, and edge cases

   **C. Conflicting Policy** - Different documents disagree
   - CLAUDE.md says one thing, detailed docs say another
   - Action: Determine correct behavior, update all docs to be consistent

   **D. Incomplete Policy** - Policy exists but missing critical details
   - Says WHAT to do but not HOW or WHEN
   - Missing error recovery guidance
   - Action: Add missing details before enforcement

4. **Fix documentation BEFORE creating hook**:
   - Missing → Write complete policy with examples
   - Vague → Add explicit requirements and ✅/❌ examples
   - Conflicting → Resolve conflict, update all affected docs
   - Incomplete → Add missing details (how, when, edge cases)
   - Commit documentation fix separately from hook implementation

**Example - WRONG Approach**:
```
# Policy conflict exists:
# - CLAUDE.md: "Preserves audit files during CLEANUP"
# - operations.md: "Delete task directory during CLEANUP"

# ❌ WRONG: Create hook to enforce deletion without fixing CLAUDE.md
# Result: Claude follows CLAUDE.md, hook "blocks" but agent doesn't understand why
```

**Example - CORRECT Approach**:
```
# Policy conflict exists - FIX DOCUMENTATION FIRST:

# Step 1: Determine correct behavior (operations.md is correct)
# Step 2: Update CLAUDE.md to match
Edit CLAUDE.md: Change "Preserves audit files" to "Delete task directory"

# Step 3: NOW create enforcement hook
# Hook will work because documentation and enforcement are aligned
```

**Output Required Before Proceeding**:
```
POLICY VERIFICATION:
- Behavior being enforced: <description>
- Policy documents checked: <list-of-files>
- Policy status: MISSING | VAGUE | CONFLICTING | INCOMPLETE | COMPLETE
- If not COMPLETE:
  - Problem: <specific issue found>
  - Fix applied: <what was added/clarified/resolved>
  - Documentation commit: <commit-hash>
- Ready for enforcement: YES/NO
```

---

**⚠️ CRITICAL: Prevention Hierarchy (MANDATORY)**

**Prevention mechanisms must be chosen in strict priority order. Higher-priority options MUST be exhausted
before lower-priority options are considered.**

| Priority | Type | Description | When to Use |
|----------|------|-------------|-------------|
| **1 (HIGHEST)** | `code_fix` | Fix broken tool or code | Root cause is a bug in existing code/tool |
| **2** | `hook` | Automatic enforcement before/after execution | Mistake is detectable/preventable via PreToolUse/PostToolUse |
| **3** | `validation` | Automatic detection after execution | Mistake detectable but not preventable (alerts for manual fix) |
| **4 (LOWEST)** | `config` | Documentation/policy update | **LAST RESORT** - only when above options impossible |

**⚠️ CONFIG JUSTIFICATION GATE**

Before choosing `config` (documentation), you MUST answer:

1. **Why can't a code_fix work?** (e.g., "No existing tool covers this case")
2. **Why can't a hook work?** (e.g., "Cannot be detected mechanically before/during execution")
3. **Why can't validation work?** (e.g., "Requires human judgment, no pattern to detect")

**If you cannot provide concrete answers, you MUST implement a higher-priority prevention.**

**PROHIBITED JUSTIFICATIONS**:
- ❌ "It's faster to document"
- ❌ "A hook would be too complex"
- ❌ "Documentation is sufficient for now"

**Active Enforcement vs Passive Policies**

When policies exist but are violated, implement ACTIVE ENFORCEMENT (hooks), not just passive documentation.

**Decision Tree**:
1. **Policy exists AND was violated?**
   - ✅ YES → Create enforcement hook (PreToolUse/PostToolUse)
   - ❌ NO (new issue) → Document policy first, then add hook if violations likely

2. **Policy enforceability:**
   - ✅ Can be checked mechanically → MUST create hook
   - ❌ Requires judgment → Document with examples, consider detection hook

**Why Active Enforcement Matters**:
- Passive policies (text in config) rely on agents reading and remembering
- Active hooks (validation scripts) prevent violations automatically
- **If it violated once, it WILL violate again without enforcement**

**Examples**:

✅ **CORRECT - Active Enforcement**:
```
Issue: Agent created files in wrong worktree (policy exists in docs)
Fix: Create pre-write.sh hook that validates worktree before Write tool
Result: Future violations automatically blocked
```

❌ **WRONG - Passive Policy Only**:
```
Issue: Agent created files in wrong worktree (policy exists in docs)
Fix: Add more warnings to documentation, bold the text
Result: Violation will recur because agent may not read/remember
```

**Hook Creation Priority**:
1. **HIGH**: Protocol violations (state machine, worktree, approval gates)
2. **MEDIUM**: Tool misuse (wrong parameters, missing validation)
3. **LOW**: Style preferences (can be post-hoc validated)

**⚠️ SPECIAL CASE: Ineffective Existing Fix**

**When temporal analysis identifies INEFFECTIVE FIX** (fix predates violation):

**DO NOT create duplicate fixes.** Instead:

1. **Analyze why existing fix failed**:
   - Read the existing fix implementation (hook, documentation, validation)
   - Review session logs to see agent behavior despite fix
   - Identify the gap: What did the fix check? What did it miss?
   - Example: Error 8 checked for section titles but not numeric boundary content

2. **Root cause categories for fix ineffectiveness**:
   - **Incomplete detection**: Fix checks for pattern A but violation uses pattern B
   - **Weak enforcement**: Warning message instead of blocking
   - **Coverage gap**: Fix only applies to subset of cases
   - **Agent workaround**: Agent found way to bypass check
   - **Documentation clarity**: Guidance exists but is buried/vague
   - **Validation timing**: Check happens too late (after damage done)

3. **Improvement strategies**:

   **Strategy A: Strengthen detection logic**
   ```bash
   # Before (INEFFECTIVE - only checked titles):
   if [[ "$SECTION_TITLE" =~ "Clarification"|"Why" ]]; then
     echo "High risk keyword detected"
   fi

   # After (EFFECTIVE - checks content for numeric boundaries):
   if [[ "$CONTENT" =~ [0-9]+-[0-9]+[[:space:]]*(seconds|retries|MB) ]]; then
     echo "⚠️ Numeric boundary detected - VERY LIKELY CONTEXTUAL"
     exit 2  # Block if classified as EXPLANATORY
   fi
   ```

   **Strategy B: Add validation checkpoint**
   ```bash
   # Add validation BEFORE removal (not just during classification)
   # Check if removed content contains execution-critical patterns
   ```

   **Strategy C: Multi-layered defense**
   ```bash
   # Layer 1: Red flag keywords in classification
   # Layer 2: Content pattern analysis (numeric boundaries)
   # Layer 3: Validation checkpoint before removal
   # Layer 4: Post-removal semantic integrity check
   ```

4. **Commit message pattern**:
   ```
   Improve ineffective fix from commit <hash>: <pattern>

   TEMPORAL ANALYSIS:
   - Original fix: <commit-hash> on <date>
   - Violation: session <session-id> on <date>
   - Time delta: <fix-predates-violation-by-X-hours>

   ROOT CAUSE OF FIX INEFFECTIVENESS:
   - Original fix checked <what-it-checked>
   - But violation occurred via <what-it-missed>
   - Gap: <specific-gap-in-detection-logic>

   IMPROVEMENT:
   - <what-new-fix-does-differently>
   - <why-this-should-work>

   EVIDENCE FROM SESSION:
   - <excerpt-showing-agent-behavior-despite-fix>
   ```

5. **Test the improvement**:
   - Review session logs showing original violation
   - Verify new fix would have caught it
   - If possible, reproduce scenario with new fix active

**Update Strategy by Category**:

#### A. Missing Information → Update Agent Prompt Template

**File**: `.claude/agents/{agent-name}.md`

**Add to "Required Context" or "Before You Begin"**:
- Checklist to verify information
- Required file reads
- Questions for unclear context
- Working directory verification
```markdown
## Before You Begin - MANDATORY CHECKS

Before ANY implementation work:

- [ ] Verify working directory: `pwd`
- [ ] Confirm you're in: `/workspace/tasks/{task}/agents/{agent-name}/code/`
- [ ] Read task requirements: `/workspace/tasks/{task}/task.md`
- [ ] Check task state: `cat /workspace/tasks/{task}/task.json`
- [ ] Verify dependencies available

If ANY check fails: STOP and report the issue.
```

#### B. Misunderstood Requirements → Clarify Documentation

**File**: `docs/project/{relevant-protocol}.md`

**Add**:
- Explicit requirements
- ✅/❌ examples
- Edge cases
- Anti-pattern warnings
- Decision trees
```markdown
## Working Directory Requirements

⚠️ **CRITICAL**: Sub-agents MUST work in their agent worktree

**Your worktree**: `/workspace/tasks/{task}/agents/{agent-name}/code/`
**NOT the task worktree**: `/workspace/tasks/{task}/code/` ← WRONG

✅ **CORRECT**:
\```bash
cd /workspace/tasks/implement-api/agents/architect/code
Write: src/main/java/MyClass.java
\```

❌ **WRONG** (Protocol Violation):
\```bash
cd /workspace/tasks/implement-api/code
Write: src/main/java/MyClass.java  # Creates in task worktree!
\```
```

#### C. Tool Usage Errors → Add Tool Guidance

**File**: `.claude/agents/{agent-name}.md`

**Add "Tool Usage Patterns"**:
- When to use each tool
- Common pitfalls
- Validation steps
- Example sequences
- Error recovery
```markdown
## Tool Usage Patterns

### Write Tool
**When**: Creating new files
**Before**: Verify directory with `pwd`
**After**: Verify file created with `ls -la {file}`
**Validation**: File must be in agent worktree

### Edit Tool
**When**: Modifying existing files
**Before**: Read file first to see exact content
**After**: Read file again to verify changes
**Pitfall**: Don't include line numbers in old_string
```

#### D. Logic Errors → Add Examples and Tests

**File**: `.claude/agents/{agent-name}.md`

**Add**:
- Worked examples
- Edge cases
- Validation checklist
- Self-test questions
- Common pitfalls
```markdown
## Common Scenarios

### Scenario: Creating New Maven Module

**Context**: Task requires new Maven module

**Steps**:
1. Create directory: `mkdir -p {module}/src/main/java`
2. Create POM: Use template from existing module
3. Add to parent POM: `<module>{module}</module>`
4. Create module-info.java: Define exports
5. Verify: `mvn compile -pl {module}`

**Edge Cases**:
- Module dependencies on other modules
- JPMS transitive requirements
- Test module descriptor

**Self-Test**:
- [ ] Did I update parent POM?
- [ ] Does module compile?
- [ ] Are exports correct?
```

#### E. Protocol Violations → Add Validation Hooks

**File**: `.claude/hooks/pre-{action}.sh`

**Create**:
- Pre-action validation
- Prerequisite checks
- State verification
- Helpful error messages
```bash
#!/bin/bash
# .claude/hooks/pre-write.sh
# Validates worktree before Write tool use

set -euo pipefail

# Extract agent name from context
AGENT_NAME=${CLAUDE_AGENT_NAME:-main}

# For sub-agents, verify working in agent worktree
if [[ "$AGENT_NAME" != "main" ]]; then
  EXPECTED_PATH="/workspace/tasks/.*/agents/$AGENT_NAME/code"
  if [[ ! "$PWD" =~ $EXPECTED_PATH ]]; then
    echo "❌ ERROR: Agent $AGENT_NAME in wrong directory" >&2
    echo "Current: $PWD" >&2
    echo "Expected: /workspace/tasks/{task}/agents/$AGENT_NAME/code/" >&2
    echo "" >&2
    echo "SOLUTION: cd to your agent worktree first" >&2
    exit 1
  fi
fi
```

#### F. Configuration Gaps → Enhance Agent Config

**File**: `.claude/agents/{agent-name}.md`

**Add Sections**:
- "Common Scenarios" with examples
- "Anti-Patterns to Avoid"
- "Decision Trees" for complex choices
- "Verification Steps" before completion
- "Self-Validation Checklist"

**Example**:
```markdown
## Anti-Patterns to Avoid

### ❌ Creating files without directory verification
**Problem**: Files created in wrong location
**Solution**: Always `pwd` before Write/Edit

### ❌ Skipping build verification
**Problem**: Broken code merged to task branch
**Solution**: Run `mvn compile` before merge

### ❌ Assuming file locations
**Problem**: Files not found or created in wrong place
**Solution**: Read files to confirm paths

## Self-Validation Checklist

Before reporting completion:
- [ ] All files in correct worktree
- [ ] Code compiles: `mvn compile`
- [ ] Tests pass: `mvn test`
- [ ] No protocol violations
- [ ] Status.json updated
```

### Phase 5: Implement Updates

**⚠️ CRITICAL: Create Rollback Point Before Changes**

```bash
# Create backup branch with timestamp
BACKUP_BRANCH="learn-from-mistakes-backup-$(date +%s)"
git branch "$BACKUP_BRANCH" HEAD
echo "Created rollback point: $BACKUP_BRANCH"

# Store backup branch name for potential rollback
echo "$BACKUP_BRANCH" > /tmp/learn-from-mistakes-rollback.txt
```

**Rollback Procedure** (if Phase 7 testing fails):
```bash
# Read backup branch name
BACKUP_BRANCH=$(cat /tmp/learn-from-mistakes-rollback.txt)

# Reset to backup
git reset --hard "$BACKUP_BRANCH"

# Clean up
git branch -D "$BACKUP_BRANCH"
rm /tmp/learn-from-mistakes-rollback.txt
```

**⚠️ CRITICAL: Prevention Changes in Separate Commit on Task Branch**

Per `protocol-scope-specification.md` Category A, configuration and documentation files should be committed
as a **separate commit BEFORE the implementation commit** on the task branch.

**Prevention files (separate commit on task branch)**:
- `.claude/hooks/*.sh` - Hook scripts
- `.claude/agents/*.md` - Agent configurations
- `.claude/skills/*/SKILL.md` - Skill documentation
- `CLAUDE.md` - Main configuration
- `docs/project/*.md` - Protocol documentation

**Workflow when inside task worktree**:
```bash
# Work in task worktree
cd /workspace/tasks/my-task/code

# Make config changes
Edit: CLAUDE.md
Edit: .claude/hooks/my-hook.sh

# Commit config changes SEPARATELY from implementation
git add CLAUDE.md .claude/hooks/my-hook.sh
git commit -m "LFM: Add prevention for X mistake"

# Continue with implementation work
Edit: Parser.java
git add Parser.java
git commit -m "Implement feature X"

# Final branch structure:
# Commit 1: "LFM: Add prevention for X mistake" (config)
# Commit 2: "Implement feature X" (implementation)
```

**Why This Matters**: Separating config from implementation:
- Keeps concerns separated (process improvements vs task work)
- Makes review easier (config changes visible in their own commit)
- Both changes flow to main together when task branch is merged

**For Each Update**:

1. **Read** current config: `.claude/agents/{agent-name}.md` or `docs/project/{protocol-file}.md`
2. **Locate** relevant section, check conflicts
3. **Draft** clear guidance with ✅/❌ examples, validation steps, consistent terminology
4. **Apply** with Edit tool
5. **Hook Registration** (if creating hook):

   ```bash
   # After creating hook file: .claude/hooks/{hook-name}.sh

   # Step 1: Make executable
   chmod +x .claude/hooks/{hook-name}.sh

   # Step 2: Determine hook trigger event
   # - SessionStart: Runs at session start
   # - UserPromptSubmit: Runs when user submits prompt
   # - PreToolUse: Runs before tool execution
   # - PostToolUse: Runs after tool execution
   # - PreCompact: Runs before context compaction

   # Step 3: Auto-register in settings.json
   HOOK_PATH="/workspace/.claude/hooks/{hook-name}.sh"
   TRIGGER_EVENT="PreToolUse"  # Or appropriate trigger

   # Read current settings
   Read: .claude/settings.json

   # Add hook registration using jq
   jq --arg hook "$HOOK_PATH" --arg trigger "$TRIGGER_EVENT" \
     '.[$trigger] += [{"hooks": [{"type": "command", "command": $hook}]}]' \
     .claude/settings.json > .claude/settings.json.tmp

   # Apply update
   mv .claude/settings.json.tmp .claude/settings.json

   # Verify registration
   grep -A3 "{hook-name}" .claude/settings.json

   # CRITICAL: Notify user to restart Claude Code
   echo "⚠️ IMPORTANT: settings.json was modified. Please restart Claude Code for hook to take effect." >&2
   ```

   **⚠️ CRITICAL: When settings.json is modified, you MUST notify the user:**

   ```
   ⚠️ IMPORTANT: I've updated .claude/settings.json to register the new hook.
   Please restart Claude Code for the hook to take effect.
   ```

   **Hook Registration by Pattern**:

   - **Validation hooks** (pre-write.sh, pre-edit.sh): `PreToolUse` with tool matcher
   - **Detection hooks** (detect-*.sh): `PostToolUse` or `UserPromptSubmit`
   - **Enforcement hooks** (enforce-*.sh): `PreToolUse` with matcher
   - **Setup hooks**: `SessionStart`

6. **Verify**: Read updated file, confirm clarity, check conflicts, verify hook registration

### Phase 6: Validation

**Checklist**:
- [ ] Addresses root cause
- [ ] Concrete examples (✅/❌)
- [ ] Clear validation steps
- [ ] Explicit anti-patterns
- [ ] Self-test questions
- [ ] No conflicts with other configs
- [ ] Consistent terminology
- [ ] Matches existing format

### Phase 7: Test by Reproduction

**⚠️ CRITICAL: Verify prevention by reproducing mistake**

**Workflow**:

1. **Verify Updates**:
   ```bash
   Read: .claude/agents/{agent-name}.md  # Confirm changes
   Read: .claude/hooks/{hook-name}.sh    # Confirm hook
   ```

2. **Prepare Hook** (if created):
   ```bash
   chmod +x .claude/hooks/{hook-name}.sh
   grep -A5 "{hook-name}" /workspace/.claude/settings.json  # Verify registration
   ```

3. **Reproduce Mistake**: Execute same action sequence that caused original mistake
   - Wrong worktree → Try creating file in wrong location
   - Missing validation → Try skipping validation step
   - Tool misuse → Try using tool incorrectly
   - Protocol violation → Try violating protocol

   **Expected**: Hook blocks or guidance prevents

4. **Verify Prevention**:
   - **Hooks**: Test blocks incorrect action with clear error
   - **Documentation**: Read config as agent, verify guidance prevents mistake

5. **Interpret Results**:
   - **✅ SUCCESS**: Hook blocks OR guidance directs correctly, error message clear
   - **❌ FAILURE**: Mistake reproducible, hook doesn't trigger, guidance unclear

   **On Failure**: Return to Phase 4, refine

6a. **Automated Test Suite** (Optional but Recommended):

   Create reusable automated tests for hooks to enable regression testing:

   ```bash
   #!/bin/bash
   # .claude/hooks/tests/test-{hook-name}.sh
   # Automated test suite for {hook-name}.sh

   set -euo pipefail

   HOOK_PATH="/workspace/.claude/hooks/{hook-name}.sh"
   TEST_RESULTS="/tmp/hook-test-results.txt"

   echo "Testing: ${HOOK_PATH##*/}" > "$TEST_RESULTS"

   # Test 1: Hook blocks invalid scenario
   test_blocks_invalid() {
     echo "Test 1: Hook blocks invalid scenario..." >> "$TEST_RESULTS"

     # Set up invalid scenario (e.g., wrong worktree)
     cd /workspace/invalid/location 2>/dev/null || mkdir -p /workspace/invalid/location && cd /workspace/invalid/location

     # Simulate hook execution with invalid context
     MOCK_CONTEXT='{"tool": {"name": "Write"}, "actor": "sub-agent"}'
     echo "$MOCK_CONTEXT" | bash "$HOOK_PATH" 2>&1 | grep -q "ERROR"

     if [[ $? -eq 0 ]]; then
       echo "  ✅ PASS: Hook correctly blocked invalid scenario" >> "$TEST_RESULTS"
       return 0
     else
       echo "  ❌ FAIL: Hook did not block invalid scenario" >> "$TEST_RESULTS"
       return 1
     fi
   }

   # Test 2: Hook allows valid scenario
   test_allows_valid() {
     echo "Test 2: Hook allows valid scenario..." >> "$TEST_RESULTS"

     # Set up valid scenario
     cd /workspace/tasks/test/agents/architect/code 2>/dev/null || {
       mkdir -p /workspace/tasks/test/agents/architect/code
       cd /workspace/tasks/test/agents/architect/code
     }

     # Simulate hook execution with valid context
     MOCK_CONTEXT='{"tool": {"name": "Write"}, "actor": "architect"}'
     echo "$MOCK_CONTEXT" | bash "$HOOK_PATH" 2>&1 | grep -q "ERROR"

     if [[ $? -ne 0 ]]; then
       echo "  ✅ PASS: Hook correctly allowed valid scenario" >> "$TEST_RESULTS"
       return 0
     else
       echo "  ❌ FAIL: Hook incorrectly blocked valid scenario (false positive)" >> "$TEST_RESULTS"
       return 1
     fi
   }

   # Test 3: Error message quality
   test_error_message_quality() {
     echo "Test 3: Error message clarity..." >> "$TEST_RESULTS"

     cd /workspace/invalid/location
     MOCK_CONTEXT='{"tool": {"name": "Write"}, "actor": "sub-agent"}'
     ERROR_MSG=$(echo "$MOCK_CONTEXT" | bash "$HOOK_PATH" 2>&1)

     # Check error message contains key elements
     if echo "$ERROR_MSG" | grep -q "ERROR" && \
        echo "$ERROR_MSG" | grep -q "Expected:" && \
        echo "$ERROR_MSG" | grep -q "Current:"; then
       echo "  ✅ PASS: Error message is clear and actionable" >> "$TEST_RESULTS"
       return 0
     else
       echo "  ❌ FAIL: Error message lacks clarity" >> "$TEST_RESULTS"
       echo "  Message: $ERROR_MSG" >> "$TEST_RESULTS"
       return 1
     fi
   }

   # Run all tests
   FAILED=0
   test_blocks_invalid || FAILED=$((FAILED + 1))
   test_allows_valid || FAILED=$((FAILED + 1))
   test_error_message_quality || FAILED=$((FAILED + 1))

   # Summary
   echo "" >> "$TEST_RESULTS"
   if [[ $FAILED -eq 0 ]]; then
     echo "✅ All tests passed" >> "$TEST_RESULTS"
     cat "$TEST_RESULTS"
     exit 0
   else
     echo "❌ $FAILED test(s) failed" >> "$TEST_RESULTS"
     cat "$TEST_RESULTS"
     exit 1
   fi
   ```

   **Test Suite Benefits**:
   - Regression testing: Verify fixes still work after code changes
   - Edge case coverage: Systematically test boundary conditions
   - False positive detection: Ensure legitimate use cases aren't blocked
   - Documentation: Tests serve as executable examples of hook behavior

   **Running Tests**:
   ```bash
   # Run specific hook test
   bash .claude/hooks/tests/test-pre-write.sh

   # Run all hook tests
   for test in .claude/hooks/tests/test-*.sh; do
     echo "Running $test..."
     bash "$test" || echo "FAILED: $test"
   done
   ```

7. **Iteration** (if test fails):
   - Diagnose: Hook too narrow? Guidance unclear? Edge case?
   - Refine: Broaden patterns, add ⚠️ CRITICAL markers, more examples
   - Re-test until success

8. **Edge Cases**: Test variations, different agents, legitimate use cases (no false positives)

**Testing Checklist**:

- [ ] All configuration updates applied and verified
- [ ] New hooks are executable and registered
- [ ] Attempted to reproduce original mistake
- [ ] Prevention mechanism activated correctly
- [ ] Error messages are clear and actionable
- [ ] Legitimate use cases not blocked (no false positives)
- [ ] Edge cases tested
- [ ] If test failed: Iterated and refined until successful

**Test Results in Commit Message**:
```
Add worktree validation to pre-write hook

**Testing**: Attempted file in wrong worktree - hook blocked with clear error

**Verified**: Fix prevents recurrence
```

### Phase 8: Documentation

**⚠️ NO RETROSPECTIVE DOCUMENTS** (per CLAUDE.md policy)

**Document via**:
1. **Inline Comments**: Pattern evolution, context, history
2. **Git Commits**: What fixed, why prevents recurrence, original mistake context
3. **Code Comments**: Rationale, alternatives, edge cases

**Prohibited**:
- ❌ lessons-learned.md
- ❌ Standalone retrospectives
- ❌ Development process chronicles

## Implementation Example

**Mistake**: Agent created files in task worktree instead of agent worktree (protocol violation)

**Root Cause**: Prompt mentioned "working directory" without emphasizing agent worktree distinction

**Updates**:

1. **Agent Config** (`.claude/agents/architect.md`):
   ```markdown
   ## ⚠️ CRITICAL: Working Directory

   **YOU MUST WORK IN YOUR AGENT WORKTREE**

   **Your worktree**: `/workspace/tasks/{task-name}/agents/architect/code/`
   **NOT the task worktree**: `/workspace/tasks/{task-name}/code/` ← PROTOCOL VIOLATION

   **Before ANY Write/Edit tool use**:
   1. Verify current directory: `pwd`
   2. Confirm you're in `/workspace/tasks/{task}/agents/architect/code/`
   3. If not, this is a CRITICAL ERROR - stop and report

   **Example**:
   ```bash
   # ✅ CORRECT
   cd /workspace/tasks/implement-api/agents/architect/code
   Write: src/main/java/MyClass.java

   # ❌ WRONG - PROTOCOL VIOLATION
   cd /workspace/tasks/implement-api/code
   Write: src/main/java/MyClass.java  # Creates in task worktree!
   ```
   ```

2. **Validation Hook** (`.claude/hooks/pre-write.sh`):
   ```bash
   #!/bin/bash
   # Pre-Write hook: Verify agent is in correct worktree

   set -euo pipefail
   trap 'echo "ERROR in pre-write.sh at line $LINENO" >&2; exit 1' ERR

   AGENT_NAME=${CLAUDE_AGENT_NAME:-main}

   if [[ "$AGENT_NAME" != "main" ]]; then
     EXPECTED_PATH="/workspace/tasks/.*/agents/$AGENT_NAME/code"
     if [[ ! "$PWD" =~ $EXPECTED_PATH ]]; then
       echo "❌ ERROR: Agent $AGENT_NAME in wrong directory" >&2
       echo "Current: $PWD" >&2
       echo "Expected: /workspace/tasks/{task}/agents/$AGENT_NAME/code/" >&2
       exit 1
     fi
   fi
   ```

3. **Documentation** (`docs/project/task-protocol-agents.md`):
   ```markdown
   ## ⚠️ CRITICAL: Agent Worktree Isolation

   **Each agent MUST work in their own worktree**:
   - Main agent: `/workspace/tasks/{task}/code/`
   - Sub-agent: `/workspace/tasks/{task}/agents/{agent-name}/code/`

   **Common Mistake**: Creating files in task worktree instead of agent worktree

   **Prevention**:
   1. Always `cd` to your agent worktree first
   2. Verify with `pwd` before Write/Edit
   3. Check path includes `agents/{agent-name}/code/`

   **Verification**: Pre-write hook blocks if in wrong directory
   ```

4. **Inline Comments in Hook** (`.claude/hooks/pre-write.sh`):
   ```bash
   #!/bin/bash
   # Pre-Write hook: Verify agent is in correct worktree
   #
   # ADDED: 2025-10-30 after architect created files in task worktree
   # instead of agent worktree during implement-formatter-api task.
   # PREVENTS: Protocol violations from wrong working directory

   set -euo pipefail

   AGENT_NAME=${CLAUDE_AGENT_NAME:-main}

   # For sub-agents, verify working in agent worktree
   if [[ "$AGENT_NAME" != "main" ]]; then
     EXPECTED_PATH="/workspace/tasks/.*/agents/$AGENT_NAME/code"
     if [[ ! "$PWD" =~ $EXPECTED_PATH ]]; then
       echo "❌ ERROR: Agent $AGENT_NAME in wrong directory" >&2
       echo "Current: $PWD" >&2
       echo "Expected: /workspace/tasks/{task}/agents/$AGENT_NAME/code/" >&2
       exit 1
     fi
   fi
   ```

5. **Git Commit Message**:
   ```
   Add worktree validation to pre-write hook

   **Fix Applied**:
   - Updated: `.claude/agents/architect.md` (added critical warning)
   - Created: `.claude/hooks/pre-write.sh` (worktree validation)
   - Enhanced: `docs/project/task-protocol-agents.md` (common mistakes section)

   **Prevention**:
   - Pre-write hook blocks creation in wrong worktree
   - Agent config emphasizes worktree requirement
   - Examples show correct vs wrong patterns

   **Verification**:
   Hook tested by attempting write in wrong directory - correctly blocked
   ```

## Success Criteria

Skill execution is successful when:

1. ✅ **Root cause identified**: Clear understanding of why mistake occurred
2. ✅ **Updates applied**: Agent config/documentation enhanced with specific guidance
3. ✅ **Fixes tested by reproduction**: Attempted to reproduce original mistake after applying fixes
4. ✅ **Prevention verified**: Reproduction test confirms mistake is now blocked/prevented
5. ✅ **Documentation added**: Inline comments in hooks/configs + git commit message with test results
6. ✅ **No side effects**: Updates don't break existing functionality or create false positives
7. ✅ **Examples included**: Concrete ✅/❌ examples added
8. ✅ **Validation added**: Hooks or checklists created where appropriate
9. ✅ **No retrospective docs**: Did NOT create standalone lessons-learned.md or similar

## Usage

### Interactive Mode
```
/learn-from-mistake

Then answer the prompts:
- Agent: architect
- Task: implement-formatter-api
- Issue: Created files in wrong worktree
```

### Direct Invocation
```
Learn from the mistake where architect created source files in the task worktree instead of their agent worktree during implement-formatter-api task. This caused a protocol violation and required rework.
```

### Via Skill Tool
```
Skill: "learn-from-mistake"
```

## Output Files

After execution, expect these files to be created/modified:

1. **Agent Configuration**: `.claude/agents/{agent-name}.md` (updated with examples)
2. **Protocol Documentation**: `docs/project/{relevant-file}.md` (enhanced if protocol-related)
3. **Validation Hooks**: `.claude/hooks/pre-{action}.sh` (created/updated with inline comments)
4. **Git Commit**: Detailed commit message documenting the fix and rationale

**NO retrospective documents created** - all documentation is inline or in git commits.

## Related Skills

**get-session-id**: Provides session ID automatically at SessionStart via hook
- Use session ID from system reminder: `✅ Session ID: {uuid}`
- Required for accessing conversation logs in Phase 2

**get-history**: Access raw conversation logs for analysis
- Uses session ID to locate: `/home/node/.config/projects/-workspace/{session-id}.jsonl`
- Provides agent sidechain logs: `/home/node/.config/projects/-workspace/agent-*.jsonl`

## Integration with Audit

This skill complements the audit system:

- **Audit identifies** → Skill fixes
- **Audit measures** → Skill prevents
- **Audit finds patterns** → Skill updates configs

**Continuous Improvement Loop**:
```
Execute Task → Audit → Learn → Update → Improved Execution
```

## Metrics Tracking for Prevention Effectiveness

**Purpose**: Track mistake recurrence to measure prevention effectiveness and identify gaps.

**Metrics Database**: `/tmp/mistake-prevention-metrics.json`

### Schema

```json
{
  "mistake_types": {
    "build_failure": {
      "last_occurrence": "2025-11-03T10:00:00Z",
      "prevention_applied": "2025-11-02T15:30:00Z",
      "prevention_method": "hook",
      "hook_path": ".claude/hooks/validate-build.sh",
      "recurrence_count_after_fix": 0,
      "total_occurrences_before_fix": 3,
      "effectiveness": "100%",
      "time_to_fix_avg_before": "45min",
      "time_to_fix_avg_after": "0min"
    },
    "wrong_worktree": {
      "last_occurrence": "2025-11-01T14:22:00Z",
      "prevention_applied": "2025-10-30T09:15:00Z",
      "prevention_method": "hook",
      "hook_path": ".claude/hooks/pre-write.sh",
      "recurrence_count_after_fix": 0,
      "total_occurrences_before_fix": 5,
      "effectiveness": "100%",
      "time_to_fix_avg_before": "30min",
      "time_to_fix_avg_after": "0min"
    }
  },
  "summary": {
    "total_mistake_types": 2,
    "total_preventions_applied": 2,
    "average_effectiveness": "100%",
    "total_time_saved": "3.75hr"
  }
}
```

### Recording Metrics

**During Phase 8** (after successful prevention verification):

```bash
#!/bin/bash
# Record prevention metrics

METRICS_FILE="/tmp/mistake-prevention-metrics.json"
MISTAKE_TYPE="wrong_worktree"  # From Phase 1
PREVENTION_METHOD="hook"       # hook, documentation, or example
PREVENTION_PATH=".claude/hooks/pre-write.sh"
OCCURRENCES_BEFORE=5           # From conversation analysis
AVG_TIME_BEFORE="30min"

# Initialize metrics file if doesn't exist
if [[ ! -f "$METRICS_FILE" ]]; then
  echo '{"mistake_types": {}, "summary": {}}' > "$METRICS_FILE"
fi

# Record prevention
jq --arg type "$MISTAKE_TYPE" \
   --arg applied "$(date -Iseconds)" \
   --arg method "$PREVENTION_METHOD" \
   --arg path "$PREVENTION_PATH" \
   --arg count "$OCCURRENCES_BEFORE" \
   --arg time "$AVG_TIME_BEFORE" \
   '.mistake_types[$type] = {
     last_occurrence: $applied,
     prevention_applied: $applied,
     prevention_method: $method,
     hook_path: $path,
     recurrence_count_after_fix: 0,
     total_occurrences_before_fix: ($count | tonumber),
     effectiveness: "100%",
     time_to_fix_avg_before: $time,
     time_to_fix_avg_after: "0min"
   }' "$METRICS_FILE" > "${METRICS_FILE}.tmp" && mv "${METRICS_FILE}.tmp" "$METRICS_FILE"
```

### Updating Metrics on Recurrence

**If mistake recurs** (detected by auto-learn-from-mistakes hook):

```bash
#!/bin/bash
# Update metrics when mistake recurs

METRICS_FILE="/tmp/mistake-prevention-metrics.json"
MISTAKE_TYPE="wrong_worktree"
CURRENT_TIME=$(date -Iseconds)

# Increment recurrence count
jq --arg type "$MISTAKE_TYPE" \
   --arg time "$CURRENT_TIME" \
   '.mistake_types[$type].recurrence_count_after_fix += 1 |
    .mistake_types[$type].last_occurrence = $time |
    .mistake_types[$type].effectiveness =
      (100 - (.mistake_types[$type].recurrence_count_after_fix /
              .mistake_types[$type].total_occurrences_before_fix * 100) |
       tostring + "%")' \
   "$METRICS_FILE" > "${METRICS_FILE}.tmp" && mv "${METRICS_FILE}.tmp" "$METRICS_FILE"
```

### Viewing Metrics

**Show all metrics**:
```bash
jq '.' /tmp/mistake-prevention-metrics.json
```

**Show effectiveness summary**:
```bash
jq '.mistake_types | to_entries | map({
  type: .key,
  effectiveness: .value.effectiveness,
  recurrences: .value.recurrence_count_after_fix,
  prevention: .value.prevention_method
}) | sort_by(.effectiveness)' /tmp/mistake-prevention-metrics.json
```

**Find ineffective preventions** (recurrence rate > 20%):
```bash
jq '.mistake_types | to_entries |
    map(select(.value.recurrence_count_after_fix > 0)) |
    map({
      type: .key,
      effectiveness: .value.effectiveness,
      recurrences: .value.recurrence_count_after_fix,
      hook: .value.hook_path
    })' /tmp/mistake-prevention-metrics.json
```

### Integration with auto-learn-from-mistakes Hook

**Automatic Detection**: The `.claude/hooks/auto-learn-from-mistakes.sh` hook runs on PostToolUse for ALL tools and automatically detects common mistake patterns, recommending invocation of this skill.

**Currently Detected Patterns** (as of 2025-11-05):

1. **Pattern 1: Build failures** (CRITICAL)
   - Triggers: "BUILD FAILURE", "COMPILATION ERROR", "compilation failure"
   - Context: Maven/Gradle build output with errors

2. **Pattern 2: Test failures** (CRITICAL)
   - Triggers: "Tests run:.*Failures: [1-9]", "test.*failed"
   - Context: Test execution results with failures

3. **Pattern 3: Protocol violations** (CRITICAL)
   - Triggers: "PROTOCOL VIOLATION", "🚨.*VIOLATION"
   - Context: Hook-detected protocol breaches

4. **Pattern 4: Merge conflicts** (HIGH)
   - Triggers: "CONFLICT", "merge conflict"
   - Context: Git merge operations

5. **Pattern 5: Edit tool failures** (MEDIUM)
   - Triggers: "String to replace not found", "old_string not found"
   - Context: Edit tool string matching failures

6. **Pattern 6: Skill step failures** (HIGH) - *Added 2025-11-05*
   - Triggers: Tool is "Skill" AND (\bERROR\b, \bFAILED\b, "failed to", "step.*(failed|failure)", "operation.*(failed|failure)", "could not", "unable to")
   - Context: Skill execution encountering errors during steps
   - Example: Git-squash skill step failing, git-rebase operation error
   - False Positive Prevention: Uses word boundaries to avoid matching "finished"

7. **Pattern 7: Git operation failures** (HIGH) - *Added 2025-11-05*
   - Triggers: "fatal:", "error:", "git.*failed", "rebase.*failed", "merge.*failed"
   - Context: Git command failures
   - Example: Rebase conflicts, merge failures, invalid git operations

**Rate Limiting**: Hook enforces 5-minute cooldown between reminders to prevent spam.

**Hook Output**: When mistake detected, outputs recommendation to stderr:
```
📚 MISTAKE DETECTED: skill_step_failure

A significant mistake was detected in the Skill tool result.

**Recommendation**: Invoke the learn-from-mistakes skill:

Skill: learn-from-mistakes

Context: Detected skill_step_failure during Skill execution.
```

**Metrics Integration**: Hook can record metrics to track prevention effectiveness (see Metrics section above).

Update `.claude/hooks/auto-learn-from-mistakes.sh` to record metrics:

```bash
# After detecting mistake, record to metrics
METRICS_FILE="/tmp/mistake-prevention-metrics.json"

# Check if prevention exists for this mistake type
if jq -e --arg type "$MISTAKE_TYPE" '.mistake_types[$type]' "$METRICS_FILE" >/dev/null 2>&1; then
  # Prevention exists but mistake recurred - update metrics
  echo "⚠️ RECURRENCE: Prevention exists for $MISTAKE_TYPE but mistake occurred again" >&2

  # Increment recurrence counter (shown above)
  # ...
else
  # First occurrence - will be handled by learn-from-mistakes skill
  echo "📊 NEW MISTAKE TYPE: $MISTAKE_TYPE (no prevention yet)" >&2
fi
```

### Metrics-Driven Improvement

**Review metrics quarterly** to identify:

1. **High-impact preventions**: Mistakes eliminated completely
2. **Ineffective preventions**: High recurrence rate (>20%)
3. **Common mistake patterns**: Types with many occurrences
4. **Time savings**: Accumulated time saved by preventing rework

**Action items based on metrics**:
- Recurrence >20%: Re-invoke learn-from-mistakes to strengthen prevention
- Zero recurrence: Document success pattern for reuse
- High occurrence count: Prioritize systemic improvements

## Phase 9: Cross-Session Mistake Logging (MANDATORY)

**⚠️ CRITICAL**: After completing Phases 1-8, you MUST log the mistake to `mistakes.json` for retrospective
analysis. This enables cross-session pattern detection and effectiveness tracking.

### Logging Procedure

```bash
# Step 1: Determine next mistake ID
MISTAKES_FILE="/workspace/.claude/retrospectives/mistakes.json"
LAST_ID=$(jq -r '.mistakes | map(.id | ltrimstr("M") | tonumber) | max // 0' "$MISTAKES_FILE")
NEXT_NUM=$((LAST_ID + 1))
MISTAKE_ID=$(printf "M%03d" "$NEXT_NUM")
echo "Next mistake ID: $MISTAKE_ID"

# Step 2: Prepare mistake data (fill in from your analysis)
TIMESTAMP=$(date -Iseconds)
CATEGORY="<category from Phase 3>"           # e.g., "build_failure", "protocol_violation"
DESCRIPTION="<brief description>"            # What went wrong
ROOT_CAUSE="<root cause from Phase 3>"       # Why it happened
PREVENTION_TYPE="<type from Phase 4>"        # "hook", "code_fix", "validation", "config"
PREVENTION_PATH="<path to prevention>"       # e.g., ".claude/hooks/my-hook.sh"
PATTERN_KEYWORDS='["keyword1", "keyword2"]'  # JSON array of searchable keywords
```

### Mistake Entry Schema

```json
{
  "id": "M022",
  "timestamp": "2026-01-02T10:30:00-05:00",
  "category": "build_failure",
  "pattern_id": null,
  "description": "Checkstyle violations in parser implementation",
  "root_cause": "Code style rules not followed during implementation",
  "prevention_type": "hook",
  "prevention_path": ".claude/hooks/pre-commit-style-check.sh",
  "pattern_keywords": ["checkstyle", "style", "formatting"],
  "commit": "abc1234",
  "recurrence_count": 0,
  "processed_in_retrospective": null
}
```

### Writing the Entry

Use jq to append the mistake entry atomically:

```bash
# Create the mistake entry
jq --arg id "$MISTAKE_ID" \
   --arg ts "$TIMESTAMP" \
   --arg cat "$CATEGORY" \
   --arg desc "$DESCRIPTION" \
   --arg cause "$ROOT_CAUSE" \
   --arg ptype "$PREVENTION_TYPE" \
   --arg ppath "$PREVENTION_PATH" \
   --argjson keywords "$PATTERN_KEYWORDS" \
   '.mistakes += [{
     id: $id,
     timestamp: $ts,
     category: $cat,
     pattern_id: null,
     description: $desc,
     root_cause: $cause,
     prevention_type: $ptype,
     prevention_path: $ppath,
     pattern_keywords: $keywords,
     commit: null,
     recurrence_count: 0,
     processed_in_retrospective: null
   }]' "$MISTAKES_FILE" > "${MISTAKES_FILE}.tmp" && mv "${MISTAKES_FILE}.tmp" "$MISTAKES_FILE"

# Increment mistake counter in retrospectives.json
RETRO_FILE="/workspace/.claude/retrospectives/retrospectives.json"
jq '.mistake_count_since_last += 1' "$RETRO_FILE" > "${RETRO_FILE}.tmp" && mv "${RETRO_FILE}.tmp" "$RETRO_FILE"

echo "✅ Logged mistake $MISTAKE_ID to mistakes.json"
```

### Valid Categories

Use one of these categories (from `mistakes.json` schema):
- `tdd_violation` - Skipped test phases
- `detection_gap` - Validation missed issue
- `bash_error` - Shell command failure
- `edit_failure` - String not found
- `architecture_issue` - Design-level problems
- `protocol_violation` - Skipped required steps
- `git_operation_failure` - Git command issues
- `build_failure` - Compilation/style errors
- `worktree_violation` - Wrong working directory
- `giving_up` - Abandoned optimal solution
- `documentation_violation` - Created prohibited docs
- `logical_error` - Incorrect logic/thresholds
- `test_failure` - Test execution failures
- `merge_conflict` - Git merge conflicts
- `other` - Uncategorized

### Pattern Linking (Optional)

If this mistake matches an existing pattern in `retrospectives.json`, link it:

```bash
# Check for existing pattern
PATTERN_ID=$(jq -r --arg cat "$CATEGORY" '.recurring_patterns[] | select(.pattern == $cat) | .pattern_id' "$RETRO_FILE")

if [[ -n "$PATTERN_ID" ]]; then
  # Update the mistake entry with pattern_id
  jq --arg id "$MISTAKE_ID" --arg pid "$PATTERN_ID" \
    '(.mistakes[] | select(.id == $id)).pattern_id = $pid' \
    "$MISTAKES_FILE" > "${MISTAKES_FILE}.tmp" && mv "${MISTAKES_FILE}.tmp" "$MISTAKES_FILE"
  echo "Linked to pattern: $PATTERN_ID"
fi
```

### Verification

After logging, verify the entry was written:

```bash
jq --arg id "$MISTAKE_ID" '.mistakes[] | select(.id == $id)' "$MISTAKES_FILE"
```

---

## When to Use

✅ **Use for**:
- Protocol violations requiring rework
- Repeated mistakes across tasks
- Documentation gaps
- Systematic tool usage errors
- Configuration ambiguities

❌ **Skip for**:
- One-time errors unlikely to recur
- Well-documented issues
- No clear systemic fix
- Minor delays (<10 min) without pattern
- User errors

## Best Practices

- Focus on systemic improvements, not one-off fixes
- Prioritize high-impact mistakes (violations, significant delays)
- Use specific, actionable examples from actual mistakes
- Verify no conflicts with existing guidance
- Test hooks to ensure correctness
- Track metrics for effectiveness
