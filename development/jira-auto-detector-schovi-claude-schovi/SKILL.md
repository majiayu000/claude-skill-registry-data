---
name: jira-auto-detector
description: Automatically detects Jira issue mentions (EC-1234, IS-8046, URLs) and intelligently fetches context via jira-analyzer subagent when needed for the conversation
---

# Jira Issue Auto-Detector Skill

You have access to a skill that seamlessly integrates Jira issue context into conversations without polluting the main context window.

## Mission

Enhance user conversations by:
1. **Detecting** Jira issue mentions in user messages
2. **Evaluating** whether issue context is genuinely needed
3. **Fetching** concise summaries via context-isolated subagent
4. **Integrating** information naturally into your response

## Pattern Recognition

### Detect these Jira patterns:

**Issue Keys:**
- Format: `[A-Z]{2,10}-\d{1,6}`
- Examples: EC-1234, IS-8046, PROJ-567
- Common in: "Look at EC-1234", "Implement IS-8046"

**URLs:**
- Format: `https://productboard.atlassian.net/browse/[KEY]`
- Example: "Check https://productboard.atlassian.net/browse/EC-1234"

**Multiple mentions:**
- "Compare EC-1234 and IS-8046"
- "Fixed in EC-1234, EC-1235, IS-8046"

## Intelligence: When to Fetch

### ✅ FETCH when user needs context:

**Direct questions:**
- "What is EC-1234 about?"
- "Tell me about IS-8046"
- "Explain PROJ-567"

**Analysis requests:**
- "Analyze EC-1234"
- "Investigate IS-8046"
- "Review PROJ-567"

**Implementation requests:**
- "Implement EC-1234"
- "Fix IS-8046"
- "Work on PROJ-567"

**Problem-solving:**
- "How should I approach EC-1234?"
- "What's the best solution for IS-8046?"
- "Help me with PROJ-567"

**Comparisons:**
- "Compare EC-1234 and IS-8046"
- "Which is more urgent, EC-1234 or PROJ-567?"

### ❌ DON'T FETCH when context not needed:

**Past tense (already done):**
- "I fixed EC-1234 yesterday"
- "EC-1234 was released last week"
- "Completed IS-8046 this morning"

**Passive listing:**
- "Released with EC-1234, EC-1235, IS-8046"
- "Sprint includes EC-1234 through EC-1240"
- "Changelog: EC-1234, EC-1235"

**Technical identifiers:**
- "The EC-1234 endpoint returns JSON"
- "Call the IS-8046 service"
- "Database table PROJ_567_users"

**Casual reference:**
- "Similar to EC-1234 but different"
- "Reminds me of IS-8046"
- "Like we did in PROJ-567"

**Already fetched this session:**
- Check transcript for previous jira-analyzer subagent calls
- Don't re-fetch same issue in same conversation
- Reuse previously fetched context

## How to Use This Skill

### Step 1: Scan User Message

Look for Jira patterns in the user's input:
- Scan for issue key format
- Check for Atlassian URLs
- Note all matches (can be multiple)

### Step 2: Evaluate Context Need

For each detected issue, ask yourself:

**Does the user's request require understanding this issue?**
- Will I need issue details to answer their question?
- Is this issue central to what they're asking?
- Are they asking me to work with this issue?

**Is this just a passing mention?**
- Is it in past tense?
- Is it part of a list?
- Is it used as an identifier/name?

**Have I already fetched this issue?**
- Check transcript for `Task` tool calls with "jira-analyzer"
- Look for "Jira Issue Summary: [KEY]" in conversation history
- If found, reuse that context

### Step 3: Fetch Issue Summary (If Needed)

When you determine context IS needed:

**First, acknowledge detection:**
```markdown
🎯 **[Jira Auto-Detector]** Detected issue reference: [ISSUE-KEY]
⏳ Fetching issue details...
```

**Use the Task tool to spawn jira-analyzer subagent:**

```
Tool: Task
Parameters:
  prompt: "Fetch and summarize https://productboard.atlassian.net/browse/[ISSUE-KEY]"
  subagent_type: "schovi:jira-auto-detector:jira-analyzer"
  description: "Fetching Jira issue context"
```

**CRITICAL formatting rules:**
- Always use FULL URL format (not just "EC-1234")
- Format: `https://productboard.atlassian.net/browse/EC-1234`
- This ensures the subagent can parse the issue key correctly

**What you'll receive:**

The jira-analyzer subagent will return a structured summary (~800 tokens) with visual wrappers:

```markdown
╭─────────────────────────────────────╮
│ 🔍 JIRA ANALYZER                    │
╰─────────────────────────────────────╯

# Jira Issue Summary: EC-1234

## Core Information
- Issue: EC-1234 - Title
- Type: Bug | Story | Task
- Status: To Do | In Progress | Done
- Priority: High | Medium | Low

## Description
[Condensed description, max 500 chars]

## Acceptance Criteria
1. [Criterion 1]
2. [Criterion 2]
...

## Key Comments
- **Author**: [Summary]
...

## Technical Context
- Affected: [Components]
- Environment: [If specified]
...
```

### Step 4: Use the Summary

**After receiving the summary, acknowledge completion:**
```markdown
✅ **[Jira Auto-Detector]** Issue details fetched successfully
```

Integrate the summary information into your response:

**Acknowledge you fetched it:**
> "I've fetched EC-1234 details..."
> "Based on the Jira issue..."
> "Looking at EC-1234..."

**Use the context:**
- Answer questions based on description/criteria
- Plan implementation based on requirements
- Analyze problem based on technical context
- Reference key comments if relevant

**Stay concise:**
- Don't regurgitate entire summary
- Extract relevant points for this response
- Focus on what user asked about

### Step 5: Handle Multiple Issues

If user mentions multiple issues (e.g., "Compare EC-1234 and IS-8046"):

**Prioritize:**
1. Primary issue: The one most central to their question
2. Secondary issues: Only if needed for comparison/context

**Fetch sequentially:**
```
1. Spawn subagent for EC-1234
2. Wait for response
3. Spawn subagent for IS-8046
4. Wait for response
5. Use both summaries for comparison
```

**Limit:**
- Don't fetch more than 3 issues per response
- If user mentions 10 issues in a list, don't fetch all
- Ask user to clarify which they want details on

## Session Memory

**Track what you've fetched:**

When you fetch an issue, remember it for this session:
- Note the issue key
- Note the summary content
- Reuse this context if user mentions it again

**How to check:**
- Review conversation transcript
- Look for your previous Task tool calls
- Search for "Jira Issue Summary: [KEY]"

**Benefits:**
- Avoid redundant fetches
- Faster responses
- Cleaner context management

## Error Handling

### If subagent returns "Issue Not Found":

**Respond to user:**
> "I couldn't fetch EC-1234 - it might not exist or you may not have access. Can you verify the issue key?"

**Possible reasons:**
- Typo in issue key
- Issue doesn't exist
- User lacks permissions
- Wrong cloud ID

### If subagent returns API error:

**Respond to user:**
> "I encountered an error fetching EC-1234. Can you provide the key details about this issue?"

**Continue conversation:**
- Ask user for context manually
- Don't block on Jira fetch failure
- Use whatever information user provides

### If fetch times out:

**Respond to user:**
> "Fetching EC-1234 is taking longer than expected. While that completes, can you tell me what specific aspect you need help with?"

**Proceed in parallel:**
- Ask clarifying questions
- Start analysis with available context
- Incorporate Jira summary when it arrives

## Integration with /analyze-problem Command

**If user explicitly runs `/analyze-problem EC-1234`:**

✅ **Let the command handle Jira fetching**
- The command has its own Jira fetch logic
- Don't duplicate effort
- Your skill doesn't need to activate

✅ **The command will:**
- Parse the issue key from arguments
- Delegate to jira-analyzer subagent
- Perform full problem analysis workflow

✅ **Your role:**
- Execute the command's instructions
- Don't interfere with its flow
- Trust the command's structured workflow

**If user casually mentions Jira in other contexts:**

✅ **Your skill activates**
- "What's EC-1234 about?" → You fetch it
- "How should I approach IS-8046?" → You fetch it
- "Compare EC-1234 to previous solution" → You fetch it

## Working with jira-analyzer Subagent

**Understand the architecture:**

```
You (Main Claude with Skill)
  ↓ detect Jira mention
  ↓ evaluate context need
  ↓ spawn subagent via Task tool
  ↓
jira-analyzer Subagent (Isolated Context)
  ↓ fetches 10k token Jira payload
  ↓ analyzes and extracts essence
  ↓ burns tokens privately
  ↓ returns 800-token summary
  ↓
You receive clean summary
  ↓ integrate into response
  ↓ main context stays clean!
```

**Your responsibilities:**
- **WHEN** to fetch (intelligence, context evaluation)
- **WHAT** to do with summary (integration into response)

**Subagent's responsibilities:**
- **HOW** to fetch (API calls, MCP tools)
- **WHAT** to extract (summarization, condensing)

**Separation of concerns = clean architecture**

## Examples

### Example 1: Direct Question

**User:** "What is EC-1234 about?"

**Your Process:**
1. ✅ Detect "EC-1234" pattern
2. ✅ Evaluate: Direct question → context needed
3. ✅ Check transcript: Not fetched yet
4. ✅ Spawn jira-analyzer subagent
5. ✅ Receive summary
6. ✅ Respond with information

**Your Response:**
> 🎯 **[Jira Auto-Detector]** Detected issue reference: EC-1234
> ⏳ Fetching issue details...
>
> [After subagent returns]
>
> ✅ **[Jira Auto-Detector]** Issue details fetched successfully
>
> "I've fetched EC-1234. This is a bug where the backend returns a boolean field type but mapping is allowed, which shouldn't be permitted. The issue is currently in To Do status with Medium priority. Based on the acceptance criteria, the fix needs to..."

### Example 2: Implementation Request

**User:** "Implement IS-8046"

**Your Process:**
1. ✅ Detect "IS-8046" pattern
2. ✅ Evaluate: Implementation request → context needed
3. ✅ Spawn jira-analyzer subagent
4. ✅ Receive summary with acceptance criteria
5. ✅ Use summary to plan implementation
6. ✅ Proceed with codebase analysis and implementation

**Your Response:**
> 🎯 **[Jira Auto-Detector]** Detected issue reference: IS-8046
> ⏳ Fetching issue details...
>
> [After subagent returns]
>
> ✅ **[Jira Auto-Detector]** Issue details fetched successfully
>
> "Based on IS-8046, I need to [summarize requirements]. Let me analyze the codebase to identify the affected components..."

### Example 3: Past Tense (Don't Fetch)

**User:** "I finished EC-1234 yesterday, now working on EC-1235"

**Your Process:**
1. ✅ Detect "EC-1234" and "EC-1235" patterns
2. ❌ Evaluate: Past tense (EC-1234) → don't fetch
3. ✅ Evaluate: Current work (EC-1235) → might need context
4. ❓ Check user intent: Are they asking for help with EC-1235?

**Your Response (if just informing):**
> "Great progress on EC-1234! What would you like help with regarding EC-1235?"
> [Don't fetch either issue yet - wait for user to ask specific question]

**Your Response (if asking for help):**
> "Great! Now for EC-1235, let me fetch the details..."
> [Fetch EC-1235 only]

### Example 4: Comparison Request

**User:** "Compare EC-1234 and IS-8046 approaches"

**Your Process:**
1. ✅ Detect both issues
2. ✅ Evaluate: Comparison request → context needed for both
3. ✅ Spawn subagent for EC-1234 first
4. ✅ Wait for summary
5. ✅ Spawn subagent for IS-8046
6. ✅ Wait for summary
7. ✅ Compare based on both summaries

**Your Response:**
> 🎯 **[Jira Auto-Detector]** Detected issue references: EC-1234, IS-8046
> ⏳ Fetching issue details...
>
> [After first subagent returns]
> ✅ EC-1234 fetched
> ⏳ Fetching IS-8046...
>
> [After second subagent returns]
> ✅ IS-8046 fetched
>
> "EC-1234 proposes [approach A] which [analysis]. IS-8046 suggests [approach B] which [analysis]. Key differences: [comparison]..."

### Example 5: Technical Identifier (Don't Fetch)

**User:** "The EC-1234 endpoint is returning 500 errors"

**Your Process:**
1. ✅ Detect "EC-1234" pattern
2. ❌ Evaluate: Used as endpoint name (technical identifier) → don't fetch
3. ✅ Respond about the endpoint issue

**Your Response:**
> "Let me help debug the EC-1234 endpoint. Can you share the error logs or stack trace?"
> [No Jira fetch - EC-1234 is just an endpoint name here]

### Example 6: Already Fetched (Reuse Context)

**User:** "Can you also check if EC-1234 affects the login flow?"

**Your Process:**
1. ✅ Detect "EC-1234" pattern
2. ✅ Evaluate: Question about issue → context needed
3. ✅ Check transcript: Already fetched earlier in this conversation
4. ✅ Reuse previous summary from transcript
5. ✅ Answer based on already-known context

**Your Response:**
> "Based on the EC-1234 details I fetched earlier, the issue is about boolean field type mapping. Looking at the login flow... [analysis]"
> [No redundant fetch - reused previous context]

## Quality Checks

### Before fetching any issue:

- [ ] Issue key matches valid format (A-Z)+-\d+)?
- [ ] User's question genuinely requires issue context
- [ ] Issue hasn't already been fetched this session
- [ ] Fetching will help (not hinder) the response
- [ ] User intent is clear (not ambiguous)

### After receiving subagent summary:

- [ ] Summary was successfully returned (not error)
- [ ] Summary contains relevant information
- [ ] You understand the issue context
- [ ] You can now provide informed response
- [ ] You're ready to proceed

### In your response:

- [ ] Acknowledged you fetched context
- [ ] Used summary information appropriately
- [ ] Didn't regurgitate entire summary
- [ ] Focused on user's specific question
- [ ] Response is actionable and helpful

## Remember

**Your goal:** Seamlessly enhance conversations with Jira context when needed.

**Balance:**
- ✅ Be proactive: Fetch when context genuinely helps
- ✅ Be respectful: Don't over-fetch or slow conversations
- ✅ Be intelligent: Understand nuance in how issues are mentioned
- ✅ Be transparent: Let users know you fetched context
- ✅ Be efficient: Reuse context, don't fetch redundantly

**Trust the architecture:**
- **You decide WHEN** (intelligence layer)
- **jira-analyzer decides HOW** (execution layer)
- **User stays in flow** (seamless experience)

**Activation is automatic:**
- No special invocation needed
- Just be aware of Jira patterns
- Evaluate context intelligently
- Fetch when it genuinely helps

Good luck making Jira integration seamless! 🎯
