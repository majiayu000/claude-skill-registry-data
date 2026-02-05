---
name: jules-api
description: Delegate asynchronous coding tasks to Jules (Google's AI coding agent) to maximize efficiency. Use for code reviews, refactoring, adding tests, bug fixes, and documentation. Proactively suggest Jules delegation when appropriate. Invoke when user asks to interact with Jules, create sessions, check task status, or when tasks are suitable for async delegation.
---

# Jules API Integration

This skill enables interaction with Google's Jules API for programmatic creation and management of asynchronous coding tasks.

## Overview

The Jules API allows you to:
- Create coding sessions with specific prompts and repository context
- Monitor session progress through various states
- Send messages and feedback to active sessions
- Approve generated plans before execution
- Retrieve session outputs (pull requests, artifacts)

## Delegation Philosophy

**KEY PRINCIPLE**: Use Jules for asynchronous tasks to maximize efficiency and free up Claude for strategic work.

### When Claude Should Delegate to Jules

Claude should **proactively suggest** creating Jules sessions for:

1. **Code Reviews** - After pushing a branch, delegate review to Jules
2. **Refactoring** - Improve code structure without changing behavior
3. **Adding Tests** - Generate unit/integration tests for existing code
4. **Bug Fixes** - Well-defined bugs with clear reproduction steps
5. **Documentation** - Improve comments, docstrings, READMEs
6. **Iterative Improvements** - Enhance previous work based on feedback

### Effective Delegation Patterns

**Pattern 1: Initial Implementation + Review**
```
1. Claude creates initial feature implementation
2. Push branch to remote
3. Claude creates Jules session: "Review and improve feature X"
4. Jules creates PR with improvements
5. Claude integrates feedback
```

**Pattern 2: Test Generation**
```
1. Claude implements feature
2. Claude creates Jules session: "Add comprehensive tests for module X"
3. Jules generates test suite
4. Merge when tests pass
```

**Pattern 3: Bug Fix Delegation**
```
1. User reports bug
2. Claude investigates and identifies root cause
3. Claude creates Jules session with reproduction steps
4. Jules fixes and adds regression tests
```

### Best Practices for Prompts

**Good prompts are:**
- ✅ **Specific**: "Add unit tests for authentication module"
- ✅ **Contextual**: "Review PR #123, focus on error handling"
- ✅ **Actionable**: "Refactor parser.py to use Polars instead of Pandas"
- ✅ **Scoped**: "Fix the timezone bug in commit abc123"

**Avoid vague prompts:**
- ❌ "Improve the code"
- ❌ "Make it better"
- ❌ "Fix everything"
- ❌ "Add features"

### 🔄 Jules Automatically Resumes From PR Comments

**IMPORTANT DISCOVERY**: Jules monitors PRs and automatically resumes sessions when you comment!

**How it works:**
1. Jules creates a PR (e.g., #466)
2. You comment on the PR describing an issue or requesting changes
3. **Jules automatically sees your comment** and resumes the session
4. Jules generates a NEW plan to address your feedback
5. Session state changes: `COMPLETED` → `AWAITING_PLAN_APPROVAL`
6. You approve the plan, Jules fixes the issues and updates the PR

**Real example from egregora:**
```
1. Jules session #10887318009267300343 created PR #466 (golden fixtures)
2. State was COMPLETED
3. Claude commented: "Wrong SDK used (google.generativeai vs google.genai)"
4. Jules AUTOMATICALLY resumed - state became AWAITING_PLAN_APPROVAL
5. Jules generated 8-step plan to fix SDK + modify pipeline
6. Claude approved: jules_client.py approve-plan 10887318009267300343
7. Jules executing fixes now
```

**Best practices:**
- ✅ **DO**: Comment on PRs with specific, actionable feedback
- ✅ **DO**: Check if session auto-resumed before creating duplicate session
- ✅ **DO**: Approve Jules' new plan if it looks good
- ✅ **DO**: Use detailed comments - Jules understands context
- ❌ **DON'T**: Create new session if existing one can resume
- ❌ **DON'T**: Use vague PR comments like "fix this"

**This creates a powerful feedback loop!** Comment on PRs to iterate with Jules.

### Claude's Role in Delegation

When delegating to Jules, Claude should:

1. **Prepare the context** - Ensure branch is pushed and up-to-date
2. **Write clear prompts** - Specific, actionable instructions
3. **Create the session** - Use jules_client.py or delegate via skill
4. **Return session info** - Give user the session ID and URL
5. **Suggest next steps** - Explain what Jules will do and when to check back

**Example dialogue:**
```
User: "Can you review my authentication changes?"
Claude: "I'll create a Jules session to review your authentication code.
         Jules works asynchronously and will create a PR with feedback.

         Session ID: 123456789
         URL: https://jules.google.com/sessions/123456789

         ⏱️  Jules typically completes tasks in ~10 minutes.
         You can continue other work while Jules reviews. I can check
         the status in ~10 minutes and help you integrate the changes."
```

**Important timing notes:**
- Jules sessions typically complete in **~10 minutes**
- Claude should check session status after ~10 minutes
- Use this time for other work - don't wait synchronously
- Jules will create a PR when done (AUTO_CREATE_PR mode)

## Base Configuration

**Base URL**: `https://jules.googleapis.com`
**API Version**: v1alpha
**Authentication**: API Key via `X-Goog-Api-Key` header

## Tools

### Feed Feedback (CI/Reviews)

This skill includes a script `feed_feedback.py` designed to run in a scheduled workflow. It enables Jules to receive feedback from CI failures and code reviews on its own Pull Requests.

**Purpose**: Closes the feedback loop by reporting CI errors and review comments back to the active Jules session so it can interactively fix issues.

**Usage**:
```bash
# Run locally (requires JULES_API_KEY and GITHUB_TOKEN)
python .claude/skills/jules-api/feed_feedback.py

# Run for a specific bot author (default: jules-bot)
python .claude/skills/jules-api/feed_feedback.py --author my-bot-name
```

**How it works**:
1. Scans for open PRs by `jules-bot`.
2. Checks CI status (failed) and Reviews (changes requested).
3. Extracts the Jules Session ID from the branch name or PR body.
4. Sends a prompt to the session with error logs and feedback.
5. Posts a comment on the PR to prevent spamming the same feedback.

## Core Operations

### 1. Create a Session

Create a new coding session with a prompt and repository context.

**Endpoint**: `POST /v1alpha/sessions`

**Request Body**:
```json
{
  "prompt": "Your coding task description",
  "sourceContext": {
    "source": "sources/github/username/repository",
    "githubRepoContext": {
      "startingBranch": "main"
    }
  },
  "title": "Optional session title",
  "requirePlanApproval": false,
  "automationMode": "AUTO_CREATE_PR"
}
```

**Example using curl**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for authentication module",
    "sourceContext": {
      "source": "sources/github/myorg/myrepo",
      "githubRepoContext": {
        "startingBranch": "main"
      }
    },
    "title": "Add Auth Tests",
    "requirePlanApproval": true,
    "automationMode": "AUTO_CREATE_PR"
  }'
```

### 2. Get Session Status

Retrieve details about a specific session.

**Endpoint**: `GET /v1alpha/sessions/{sessionId}`

**Example**:
```bash
curl https://jules.googleapis.com/v1alpha/sessions/abc123 \
  -H "X-Goog-Api-Key: YOUR_API_KEY"
```

**Session States**:
- `QUEUED`: Session is waiting to start
- `PLANNING`: Generating execution plan
- `AWAITING_PLAN_APPROVAL`: Waiting for user approval
- `AWAITING_USER_FEEDBACK`: Needs user input
- `IN_PROGRESS`: Actively executing
- `PAUSED`: Temporarily stopped
- `COMPLETED`: Successfully finished
- `FAILED`: Encountered error

### 3. List All Sessions

Retrieve all sessions.

**Endpoint**: `GET /v1alpha/sessions`

**Example**:
```bash
curl https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: YOUR_API_KEY"
```

### 4. Send Message to Session

Send user feedback or additional instructions to an active session.

**Endpoint**: `POST /v1alpha/sessions/{sessionId}:sendMessage`

**Request Body**:
```json
{
  "prompt": "Your message or feedback"
}
```

**Example**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions/abc123:sendMessage \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Please add more test coverage for edge cases"}'
```

### 5. Approve Plan

Approve a generated plan (when requirePlanApproval is true).

**Endpoint**: `POST /v1alpha/sessions/{sessionId}:approvePlan`

**Example**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions/abc123:approvePlan \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

### 6. Get Session Activities

Retrieve activity logs for a session.

**Endpoint**: `GET /v1alpha/sessions/{sessionId}/activities`

**Example**:
```bash
curl https://jules.googleapis.com/v1alpha/sessions/abc123/activities \
  -H "X-Goog-Api-Key: YOUR_API_KEY"
```

## Authentication Setup

To use the Jules API, you need an API key:

1. **Get your API key**:
   - Visit https://jules.google.com/settings#api
   - Create a new API key (max 3 keys allowed)
   - Copy the API key

2. **Set the API key**:
   ```bash
   # Export as environment variable
   export JULES_API_KEY="your-api-key-here"

   # Or pass directly to JulesClient
   client = JulesClient(api_key="your-api-key-here")
   ```

**Security Note**: Keep your API key secure. Don't share it or commit it to version control.

## Python Example

```python
import os
import requests

# It's recommended to set the JULES_API_KEY environment variable
API_KEY = os.environ.get("JULES_API_KEY")
BASE_URL = "https://jules.googleapis.com/v1alpha"

def create_jules_session(prompt, owner, repo, branch='main'):
    url = f'{BASE_URL}/sessions'
    headers = {
        'X-Goog-Api-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'sourceContext': {
            'source': f'sources/github/{owner}/{repo}',
            'githubRepoContext': {
                'startingBranch': branch
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_session_status(session_id):
    url = f'{BASE_URL}/sessions/{session_id}'
    headers = {
        'X-Goog-Api-Key': API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Usage
if API_KEY:
    session = create_jules_session(
        prompt='Add error handling to API endpoints',
        owner='myorg',
        repo='myproject'
    )
    print(f"Created session: {session['id']}")

    # Check status
    status = get_session_status(session['id'])
    print(f"Status: {status['state']}")
else:
    print("Please set the JULES_API_KEY environment variable.")
```

## Best Practices

1. **Use Descriptive Prompts**: Provide clear, specific instructions for the coding task
2. **Monitor State**: Poll session status to track progress
3. **Enable Plan Approval**: Set `requirePlanApproval: true` for sensitive operations
4. **Handle States**: Implement proper handling for AWAITING_USER_FEEDBACK and AWAITING_PLAN_APPROVAL states
5. **Check Outputs**: Review the `outputs` array for generated pull requests and artifacts

## Common Workflows

### Workflow 1: Simple Task
1. Create session with prompt
2. Poll status until COMPLETED or FAILED
3. Retrieve outputs (PRs)

### Workflow 2: Supervised Task
1. Create session with `requirePlanApproval: true`
2. Wait for AWAITING_PLAN_APPROVAL state
3. Review plan in activities
4. Call approvePlan
5. Monitor until completion

### Workflow 3: Interactive Task
1. Create session
2. Monitor for AWAITING_USER_FEEDBACK
3. Use sendMessage to provide feedback
4. Continue monitoring until completion

## Real-World Delegation Scenarios

### Scenario 1: Feature Implementation Review
```
User: "I just implemented user authentication, can you review it?"

Claude Action:
1. Check if branch is pushed to remote
2. Create Jules session with prompt:
   "Review the user authentication implementation in feature/auth-system.
    Check for security issues, test coverage, and code quality.
    Suggest improvements and add missing tests."
3. Inform user of session ID/URL
4. User continues other work while Jules reviews
```

### Scenario 2: Adding Tests to Legacy Code
```
User: "We need tests for the payment processor module"

Claude Action:
1. Review payment processor to understand functionality
2. Create Jules session:
   "Add comprehensive unit and integration tests for the payment
    processor module. Cover success cases, error handling, edge cases,
    and mock external payment gateway calls."
3. Jules generates test suite
4. Review and merge
```

### Scenario 3: Refactoring for Performance
```
User: "The data parser is slow, can we optimize it?"

Claude Action:
1. Identify performance bottleneck
2. Create Jules session:
   "Refactor parser.py to use Polars instead of Pandas for 10x
    performance improvement. Maintain same API and ensure all
    existing tests pass. Add benchmarks."
3. Jules refactors with benchmarks
4. Review performance gains and merge
```

### Scenario 4: Bug Fix with Regression Tests
```
User: "There's a bug in timezone handling"

Claude Action:
1. Investigate and identify root cause in commit abc123
2. Create Jules session:
   "Fix timezone bug in datetime_utils.py (commit abc123).
    The bug causes incorrect UTC conversion for dates before 1970.
    Add regression tests to prevent future issues."
3. Jules fixes and adds tests
4. Verify and merge
```

### Scenario 5: Documentation Improvement
```
User: "Our API documentation is outdated"

Claude Action:
1. Identify outdated sections
2. Create Jules session:
   "Update API documentation in docs/api.md to reflect current
    implementation. Add examples for new endpoints, update
    parameter descriptions, and ensure all code samples work."
3. Jules updates docs with examples
4. Review and merge
```

## Proactive Delegation Triggers

Claude should **automatically suggest** Jules delegation when:

- ✅ User pushes a branch and asks "what do you think?"
- ✅ User says "add tests" or "improve tests"
- ✅ User mentions "review", "refactor", or "optimize"
- ✅ Feature is complete and needs polish
- ✅ Code works but needs improvement
- ✅ User reports a well-defined bug
- ✅ Documentation needs updating

**Example proactive response:**
```
User: "Just pushed the new API endpoint to feature/api-v2"
Claude: "Great! I can see the implementation looks solid. Would you like me to
         create a Jules session to review it and suggest improvements? Jules
         can check for edge cases, add tests, and optimize the code while
         you continue working on other features."
```

## Error Handling

Always check response status codes:
- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: Session doesn't exist
- `403 Forbidden`: Insufficient permissions

## References

- Official Documentation: https://developers.google.com/jules/api/reference/rest
- Sessions API: https://developers.google.com/jules/api/reference/rest/v1alpha/sessions
