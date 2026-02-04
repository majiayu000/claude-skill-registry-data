---
name: gh-pr-auto-detector
description: Automatically detects GitHub PR mentions (URLs, #123, owner/repo#123) and intelligently fetches condensed context via gh-pr-analyzer subagent when needed for the conversation
---

# GitHub PR Auto-Detector Skill

You have access to a skill that seamlessly integrates GitHub Pull Request context into conversations without polluting the main context window with huge PR payloads.

## Mission

Enhance user conversations by:
1. **Detecting** GitHub PR mentions in user messages
2. **Evaluating** whether PR context is genuinely needed
3. **Classifying** user intent to fetch reviews, CI, or full context
4. **Fetching** concise summaries via context-isolated subagent
5. **Integrating** information naturally into your response

## Pattern Recognition

### Detect these GitHub PR patterns:

**Full GitHub URLs:**
- Format: `https://github.com/[owner]/[repo]/pull/[number]`
- Examples:
  - `https://github.com/anthropics/claude-code/pull/123`
  - `https://github.com/owner/repo/pull/456`
- Common in: "Review https://github.com/owner/repo/pull/123"

**Short Form (owner/repo#number):**
- Format: `[owner]/[repo]#\d+`
- Examples: `anthropics/claude-code#123`, `owner/repo#456`
- Common in: "Check anthropics/claude-code#123"

**Hash-only (#number):**
- Format: `#\d+`
- Examples: `#123`, `#456`
- Common in: "What's the status of #123?"
- **CAVEAT**: Requires repository context from conversation or working directory

**Explicit Mentions:**
- "PR #123", "pull request 123", "PR 456"
- "the pull request #123"
- "review PR #456"

**Multiple PRs:**
- "Compare #123 and #456"
- "Review PRs #123, #124, #125"
- "Merged in anthropics/claude-code#123 and owner/repo#456"

## Intelligence: When to Fetch

### ✅ FETCH when user needs context:

**Direct questions:**
- "What is #123 about?"
- "Tell me about anthropics/claude-code#456"
- "What's in https://github.com/owner/repo/pull/789?"
- "Summarize PR #123"

**Review requests:**
- "Review #123"
- "Check the code in PR #456"
- "What do you think about anthropics/claude-code#123?"
- "Analyze this PR: [URL]"

**Status checks:**
- "What's the CI status of #123?"
- "Did the tests pass on #456?"
- "Are there any review comments on #123?"
- "Is #456 approved?"

**Implementation requests:**
- "Apply the changes from #123"
- "Use the approach from anthropics/claude-code#456"
- "Implement similar to #123"
- "Port #456 to our codebase"

**Problem-solving:**
- "Why did #123 fail CI?"
- "What are the review blockers on #456?"
- "How should I address feedback on #123?"

**Comparisons:**
- "Compare #123 and #456 approaches"
- "Which is better, #123 or anthropics/claude-code#789?"

### ❌ DON'T FETCH when context not needed:

**Past tense (already done):**
- "I merged #123 yesterday"
- "PR #456 was released last week"
- "Closed #123 this morning"
- "Fixed in #456"

**Passive listing:**
- "Released with #123, #124, #125"
- "Changelog: #123, #456, #789"
- "Sprint delivered #100 through #150"

**Technical identifiers:**
- "The PR-123 endpoint" (endpoint name, not PR reference)
- "Variable pr_456_result"
- "Function handlePR123()"

**Casual reference:**
- "Similar to #123 but different"
- "Reminds me of that PR #456"
- "Like we did in #123"

**Already fetched this session:**
- Check transcript for previous gh-pr-analyzer subagent calls
- Don't re-fetch same PR in same conversation
- Reuse previously fetched context

## Intent Classification: What to Fetch

Based on user's question, determine which PR aspects to fetch:

### 🔍 **Full Context** (default)
- User asks general questions: "What's #123 about?"
- Wants comprehensive review: "Review #456"
- Implementation planning: "Implement similar to #123"
- **Options**: `include_reviews: true, include_ci: true`

### 💬 **Reviews Focus**
- User asks specifically about feedback: "What are the review comments on #123?"
- Wants approval status: "Is #456 approved?"
- Addressing feedback: "How should I address review on #123?"
- **Options**: `include_reviews: true, include_ci: false`

### ✅ **CI/Checks Focus**
- User asks about tests/CI: "Did tests pass on #123?"
- CI failures: "Why did #456 fail CI?"
- Check status: "What's the CI status of #123?"
- **Options**: `include_reviews: false, include_ci: true`

### 📄 **Minimal Context** (rare)
- User only needs basic info: "Who authored #123?"
- Quick status check: "Is #456 merged?"
- **Options**: `include_reviews: false, include_ci: false`

## How to Use This Skill

### Step 1: Scan User Message

Look for GitHub PR patterns:
- Scan for full GitHub URLs
- Check for owner/repo#number format
- Look for #number references
- Note explicit mentions ("PR #123")
- Identify all matches (can be multiple)

### Step 2: Extract Repository Context

**For full URLs:**
- Parse owner and repo from URL
- Extract PR number
- Format: `owner/repo#number`

**For owner/repo#number:**
- Already has full context
- Use as-is

**For #number only:**
- Check conversation for repo context
- Check working directory (via git remote)
- If missing, ask user to clarify repository

### Step 3: Evaluate Context Need

For each detected PR, ask yourself:

**Does the user's request require understanding this PR?**
- Will I need PR details to answer their question?
- Is this PR central to what they're asking?
- Are they asking me to work with this PR?

**Is this just a passing mention?**
- Is it in past tense (already merged/closed)?
- Is it part of a list?
- Is it used as an identifier/name?

**Have I already fetched this PR?**
- Check transcript for `Task` tool calls with "gh-pr-analyzer"
- Look for "GitHub PR Summary: owner/repo#123" in conversation history
- If found, reuse that context

### Step 4: Classify User Intent

Determine what aspects the user needs:

**Full context signals:**
- General questions ("What's #123 about?")
- Implementation ("Apply changes from #123")
- Comprehensive review ("Review #456")

**Reviews focus signals:**
- "review comments", "feedback", "approval"
- "What did reviewers say?"
- "Address review on #123"

**CI focus signals:**
- "CI", "tests", "checks", "build", "failed"
- "Did tests pass?"
- "Why did CI fail?"

**Default:** When unclear, fetch full context (reviews + CI)

### Step 5: Fetch PR Summary (If Needed)

When you determine context IS needed:

**First, acknowledge detection:**
```markdown
📋 **[PR Auto-Detector]** Detected PR reference: [owner/repo#number or #number]
⏳ Fetching PR details...
```

**Use the Task tool to spawn gh-pr-analyzer subagent:**

```
Tool: Task
Parameters:
  prompt: "Fetch and summarize GitHub PR: [owner/repo#number or URL]
           Options: include_reviews=[true/false], include_ci=[true/false]"
  subagent_type: "schovi:gh-pr-auto-detector:gh-pr-analyzer"
  description: "Fetching GitHub PR context"
```

**Examples:**

Full context (default):
```
prompt: "Fetch and summarize GitHub PR: anthropics/claude-code#123"
```

Reviews only:
```
prompt: "Fetch and summarize GitHub PR: anthropics/claude-code#123
         Options: include_reviews=true, include_ci=false"
```

CI only:
```
prompt: "Fetch and summarize GitHub PR: https://github.com/owner/repo/pull/456
         Options: include_reviews=false, include_ci=true"
```

**CRITICAL formatting rules:**
- Use full identifier format: `owner/repo#number` OR full URL
- Specify options explicitly when not default
- Format must be parseable by gh-pr-analyzer subagent

**What you'll receive:**

The gh-pr-analyzer subagent will return a structured summary (~800-1000 tokens) with visual wrappers:

```markdown
╭─────────────────────────────────────╮
│ 🔗 PR ANALYZER                      │
╰─────────────────────────────────────╯

# GitHub PR Summary: owner/repo#123

## Core Information
- PR: #123 - Title
- Author: username
- Status: open | merged | closed
- Base: main ← Head: feature-branch
- URL: https://github.com/owner/repo/pull/123

## Description
[Condensed description, max 500 chars]

## Code Changes
- Files changed: 15 (+250, -100)
- Key files: [Top 5 files by changes]

## CI/CD Status (if requested)
- Overall: ✅ passing | ❌ failing | ⏳ pending
- Failed checks: [Details if any]

## Reviews (if requested)
- Review decision: APPROVED | CHANGES_REQUESTED | PENDING
- Latest reviews: [Max 3 most recent]
- Key comments: [Max 5 significant comments]

## Analysis Notes
[Subagent's assessment]
```

### Step 6: Use the Summary

**After receiving the summary, acknowledge completion:**
```markdown
✅ **[PR Auto-Detector]** PR details fetched successfully
```

Integrate the summary information into your response:

**Acknowledge you fetched it:**
> "I've fetched PR #123 details..."
> "Based on the pull request..."
> "Looking at anthropics/claude-code#123..."

**Use the context:**
- Answer questions based on description/changes
- Assess CI status and diagnose failures
- Summarize review feedback and approval state
- Analyze code changes based on diff summary
- Reference key comments if relevant

**Stay concise:**
- Don't regurgitate entire summary
- Extract relevant points for this response
- Focus on what user asked about

### Step 7: Handle Multiple PRs

If user mentions multiple PRs (e.g., "Compare #123 and #456"):

**Prioritize:**
1. Primary PR: The one most central to their question
2. Secondary PRs: Only if needed for comparison/context

**Fetch sequentially:**
```
1. Spawn subagent for #123
2. Wait for response
3. Spawn subagent for #456
4. Wait for response
5. Use both summaries for comparison
```

**Limit:**
- Don't fetch more than 3 PRs per response
- If user mentions 10 PRs in a list, don't fetch all
- Ask user to clarify which they want details on

## Repository Context Detection

### When #number is mentioned without owner/repo:

**Step 1: Check conversation history**
- Look for previous PR mentions with full context
- See if user specified repository earlier
- Check for git remote context from previous commands

**Step 2: Check current working directory**
- If cwd is a git repository, use `git remote get-url origin`
- Parse owner/repo from remote URL
- Format: `owner/repo#number`

**Step 3: Ask user if context unclear**
> "I see you mentioned #123. Which repository is this PR in? (e.g., owner/repo#123)"

### Example flow:

**User:** "What's #123 about?"

**Your process:**
1. ✅ Detect "#123" pattern
2. ❓ Missing owner/repo context
3. ✅ Check cwd: `/Users/schovi/productboard/frontend`
4. ✅ Run: `git remote get-url origin`
5. ✅ Parse: `https://github.com/productboard/frontend.git` → `productboard/frontend`
6. ✅ Format: `productboard/frontend#123`
7. ✅ Spawn gh-pr-analyzer with full identifier

## Session Memory

**Track what you've fetched:**

When you fetch a PR, remember it for this session:
- Note the PR identifier (owner/repo#number)
- Note the summary content
- Note what options were used (reviews/CI)
- Reuse this context if user mentions it again

**How to check:**
- Review conversation transcript
- Look for your previous Task tool calls
- Search for "GitHub PR Summary: owner/repo#"

**Benefits:**
- Avoid redundant fetches
- Faster responses
- Cleaner context management

**Re-fetch scenarios:**
When to fetch again even if already fetched:
- User asks for different aspects (was minimal, now wants reviews)
- User explicitly requests fresh data ("re-check CI on #123")
- Significant time has passed (CI might have updated)

## Error Handling

### If subagent returns "PR Not Found":

**Respond to user:**
> "I couldn't fetch #123 - it might not exist or you may not have access. Can you verify the PR number and repository?"

**Possible reasons:**
- Typo in PR number
- Wrong repository
- PR doesn't exist
- User lacks permissions
- Private repository

### If subagent returns "Repository context missing":

**Respond to user:**
> "You mentioned #123, but I need the repository. Please specify as owner/repo#123 or provide a full GitHub URL."

**Your action:**
- Ask for clarification
- Don't assume repository
- Wait for user to provide context

### If subagent returns API error:

**Respond to user:**
> "I encountered an error fetching the PR. Can you provide the key details about this pull request?"

**Continue conversation:**
- Ask user for context manually
- Don't block on PR fetch failure
- Use whatever information user provides

### If `gh` CLI not authenticated:

**Respond to user:**
> "GitHub CLI (`gh`) is not authenticated. Please run `gh auth login` to enable PR fetching."

**Fallback:**
- Ask user to provide PR details manually
- Suggest authentication command
- Continue with available information

### If fetch times out:

**Respond to user:**
> "Fetching PR #123 is taking longer than expected. While that completes, can you tell me what specific aspect you need help with?"

**Proceed in parallel:**
- Ask clarifying questions
- Start analysis with available context
- Incorporate PR summary when it arrives

## Integration with Commands

**If user explicitly runs a command that fetches PRs:**

✅ **Let the command handle PR fetching**
- Commands may have their own PR fetch logic
- Don't duplicate effort
- Your skill doesn't need to activate

✅ **The command will:**
- Parse PR identifiers from arguments
- Delegate to gh-pr-analyzer subagent
- Perform its specific workflow

✅ **Your role:**
- Execute the command's instructions
- Don't interfere with its flow
- Trust the command's structured workflow

**If user casually mentions PRs in other contexts:**

✅ **Your skill activates**
- "What's #123 about?" → You fetch it
- "Review anthropics/claude-code#456" → You fetch it
- "Why did #123 fail CI?" → You fetch it (CI focus)

## Working with gh-pr-analyzer Subagent

**Understand the architecture:**

```
You (Main Claude with Skill)
  ↓ detect PR mention
  ↓ evaluate context need
  ↓ classify intent (reviews/CI/full)
  ↓ determine repository context
  ↓ spawn subagent via Task tool
  ↓
gh-pr-analyzer Subagent (Isolated Context)
  ↓ fetches huge PR payload via gh CLI
  ↓ analyzes and extracts essence
  ↓ burns tokens privately
  ↓ returns 800-1000 token summary
  ↓
You receive clean summary
  ↓ integrate into response
  ↓ main context stays clean!
```

**Your responsibilities:**
- **WHEN** to fetch (intelligence, context evaluation)
- **WHAT** to fetch (reviews, CI, full context)
- **WHAT** to do with summary (integration into response)

**gh-pr-analyzer subagent's responsibilities:**
- **HOW** to fetch (gh CLI commands, parsing)
- **WHAT** to extract (summarization, condensing)

**Separation of concerns = clean architecture**

## Examples

### Example 1: Direct Question (Full Context)

**User:** "What is anthropics/claude-code#123 about?"

**Your Process:**
1. ✅ Detect "anthropics/claude-code#123" pattern
2. ✅ Extract: owner=anthropics, repo=claude-code, number=123
3. ✅ Evaluate: Direct question → context needed
4. ✅ Classify: General question → full context (default)
5. ✅ Check transcript: Not fetched yet
6. ✅ Spawn gh-pr-analyzer subagent with full context
7. ✅ Receive summary
8. ✅ Respond with information

**Your Response:**
> 📋 **[PR Auto-Detector]** Detected PR reference: anthropics/claude-code#123
> ⏳ Fetching PR details...
>
> [After subagent returns]
>
> ✅ **[PR Auto-Detector]** PR details fetched successfully
>
> "I've fetched anthropics/claude-code#123. This PR adds support for MCP servers in Claude Code. The PR includes 15 file changes (+250, -100 lines), primarily in the server integration layer. The CI is passing and the PR has been approved by 2 reviewers. Based on the description..."

### Example 2: CI Status Check

**User:** "Did the tests pass on #456?"

**Your Process:**
1. ✅ Detect "#456" pattern
2. ❓ Missing owner/repo → check cwd
3. ✅ Get git remote → `productboard/frontend`
4. ✅ Format: `productboard/frontend#456`
5. ✅ Evaluate: CI question → context needed
6. ✅ Classify: CI focus → include_reviews=false, include_ci=true
7. ✅ Spawn gh-pr-analyzer with CI focus
8. ✅ Receive CI summary
9. ✅ Respond about CI status

**Your Response:**
> 📋 **[PR Auto-Detector]** Detected PR reference: #456
> ⏳ Resolving repository context and fetching CI status...
>
> [After subagent returns]
>
> ✅ **[PR Auto-Detector]** CI status fetched successfully
>
> "I've checked the CI status for productboard/frontend#456. The build is currently failing - the 'test-suite' check failed with 3 test errors in the authentication module. The linter and type checks passed successfully. Here are the failing tests..."

### Example 3: Review Request

**User:** "Review https://github.com/owner/repo/pull/789"

**Your Process:**
1. ✅ Detect full GitHub URL
2. ✅ Parse: owner=owner, repo=repo, number=789
3. ✅ Evaluate: Review request → context needed
4. ✅ Classify: Review request → full context (reviews + CI + code)
5. ✅ Spawn gh-pr-analyzer with full context
6. ✅ Receive comprehensive summary
7. ✅ Analyze and provide review feedback

**Your Response:**
> 📋 **[PR Auto-Detector]** Detected PR reference: https://github.com/owner/repo/pull/789
> ⏳ Fetching full PR context for review...
>
> [After subagent returns]
>
> ✅ **[PR Auto-Detector]** PR details fetched successfully
>
> "I've reviewed owner/repo#789. This PR refactors the authentication flow to use JWT tokens. Here's my analysis:
>
> **Code Changes**: The PR modifies 8 files, primarily in the auth/ directory. The changes look well-structured and include comprehensive tests.
>
> **CI Status**: All checks are passing ✅
>
> **Existing Reviews**: One reviewer requested changes regarding error handling in the token refresh logic. I agree with that feedback.
>
> **Additional Observations**: [detailed review feedback]..."

### Example 4: Past Tense (Don't Fetch)

**User:** "I merged #123 yesterday, now working on #124"

**Your Process:**
1. ✅ Detect "#123" and "#124" patterns
2. ❌ Evaluate: Past tense (#123) → don't fetch
3. ✅ Evaluate: Current work (#124) → might need context
4. ❓ Check user intent: Are they asking for help with #124?

**Your Response (if just informing):**
> "Great progress on #123! What would you like help with regarding #124?"
> [Don't fetch either PR yet - wait for user to ask specific question]

**Your Response (if asking for help):**
> "Great! Now for #124, let me fetch the details..."
> [Fetch #124 only, with appropriate focus]

### Example 5: Comparison Request

**User:** "Compare the approaches in #123 and anthropics/claude-code#456"

**Your Process:**
1. ✅ Detect both PRs
2. ❓ #123 missing context → check cwd → `productboard/frontend`
3. ✅ Format: `productboard/frontend#123` and `anthropics/claude-code#456`
4. ✅ Evaluate: Comparison request → context needed for both
5. ✅ Classify: Approach comparison → full context
6. ✅ Spawn subagent for productboard/frontend#123 first
7. ✅ Wait for summary
8. ✅ Spawn subagent for anthropics/claude-code#456
9. ✅ Wait for summary
10. ✅ Compare based on both summaries

**Your Response:**
> 📋 **[PR Auto-Detector]** Detected PR references: #123, anthropics/claude-code#456
> ⏳ Fetching both PRs for comparison...
>
> [After first subagent returns]
> ✅ productboard/frontend#123 fetched
> ⏳ Fetching anthropics/claude-code#456...
>
> [After second subagent returns]
> ✅ anthropics/claude-code#456 fetched
>
> "productboard/frontend#123 implements authentication using session cookies, while anthropics/claude-code#456 uses JWT tokens. Key differences:
>
> **#123 (session cookies)**:
> - Pros: [analysis]
> - Cons: [analysis]
>
> **anthropics/claude-code#456 (JWT)**:
> - Pros: [analysis]
> - Cons: [analysis]
>
> For your use case, I'd recommend [recommendation with rationale]..."

### Example 6: Technical Identifier (Don't Fetch)

**User:** "The PR-123 endpoint is returning 500 errors"

**Your Process:**
1. ✅ Detect "PR-123" pattern (looks like PR reference)
2. ❌ Evaluate: Used as endpoint name (technical identifier) → don't fetch
3. ✅ Respond about the endpoint issue

**Your Response:**
> "Let me help debug the PR-123 endpoint. Can you share the error logs or stack trace?"
> [No PR fetch - "PR-123" is just an endpoint name here]

### Example 7: Already Fetched (Reuse Context)

**User (earlier):** "Review #123"
**You:** [Fetched anthropics/claude-code#123, provided review]

**User (later):** "Can you also check if #123 affects the authentication flow?"

**Your Process:**
1. ✅ Detect "#123" pattern
2. ✅ Evaluate: Question about PR → context needed
3. ✅ Check transcript: Already fetched earlier in this conversation
4. ✅ Reuse previous summary from transcript
5. ✅ Answer based on already-known context

**Your Response:**
> "Based on the #123 PR I reviewed earlier (adds MCP server support), let me analyze how it interacts with the authentication flow... [analysis based on previously fetched context]"
> [No redundant fetch - reused previous context]

### Example 8: Missing Repository Context

**User:** "What's #123 about?"

**Your Process (no git context available):**
1. ✅ Detect "#123" pattern
2. ❓ Missing owner/repo → check cwd → not a git repo
3. ❓ Check conversation → no previous repo mentions
4. ❌ Cannot determine repository
5. ✅ Ask user for clarification

**Your Response:**
> "You mentioned #123 - which repository is this PR in? Please specify as `owner/repo#123` or provide the full GitHub URL."
> [Wait for user to clarify before fetching]

## Quality Checks

### Before fetching any PR:

- [ ] PR identifier matches valid format
- [ ] Repository context is clear (owner/repo known)
- [ ] User's question genuinely requires PR context
- [ ] PR hasn't already been fetched this session (or needs refresh)
- [ ] Fetching will help (not hinder) the response
- [ ] User intent is clear (not ambiguous)
- [ ] Correct options selected (reviews/CI/full)

### After receiving subagent summary:

- [ ] Summary was successfully returned (not error)
- [ ] Summary contains relevant information
- [ ] You understand the PR context
- [ ] You can now provide informed response
- [ ] You're ready to proceed

### In your response:

- [ ] Acknowledged you fetched context
- [ ] Used summary information appropriately
- [ ] Didn't regurgitate entire summary
- [ ] Focused on user's specific question
- [ ] Response is actionable and helpful
- [ ] Integrated GitHub context naturally

## Remember

**Your goal:** Seamlessly enhance conversations with GitHub PR context when needed.

**Balance:**
- ✅ Be proactive: Fetch when context genuinely helps
- ✅ Be respectful: Don't over-fetch or slow conversations
- ✅ Be intelligent: Understand nuance in how PRs are mentioned
- ✅ Be context-aware: Detect repository from environment
- ✅ Be specific: Fetch only what user needs (reviews/CI/full)
- ✅ Be transparent: Let users know you fetched context
- ✅ Be efficient: Reuse context, don't fetch redundantly

**Trust the architecture:**
- **You decide WHEN** (intelligence layer)
- **You decide WHAT** (intent classification)
- **gh-pr-analyzer decides HOW** (execution layer)
- **User stays in flow** (seamless experience)

**Activation is automatic:**
- No special invocation needed
- Just be aware of GitHub PR patterns
- Evaluate context intelligently
- Classify user intent appropriately
- Fetch when it genuinely helps

Good luck making GitHub PR integration seamless! 🚀
