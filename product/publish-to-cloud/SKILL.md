---
name: publish-to-cloud
description: Publish local test projects, use cases, test cases, and test scripts to Muggle AI cloud. Use when the user asks to publish, upload, sync to cloud, or deploy tests to production. Handles authentication, URL inheritance for production, and cloud ID mapping.
---

# Publish to Cloud

Publish local test artifacts to Muggle AI cloud for production testing, scheduling, and team collaboration.

## Workflow Overview

```
Check Authentication → Login if needed
      ↓
Select Project to Publish
      ↓
Resolve Production URL (inheritance chain)
      ↓
Check Existing Cloud Project → Create or Update
      ↓
Sync Use Cases, Test Cases, Test Scripts
      ↓
Confirm Publication → Return Cloud URLs
```

## Prerequisites

- Local MCP server running
- Muggle AI account
- Local project with test scripts ready to publish

## Hard-Fail Policy (No Browser Fallback)

This skill is **Local MCP only**. If Local MCP tools are unavailable or a required Local MCP step fails, **stop and fail** this workflow.

Do **not** fall back to generic browser testing features/tools to continue execution.

When failing, clearly report:
1. Which Local MCP step/tool failed
2. The error message
3. What user action is needed (for example, start Local MCP, fix auth, or check local project data)

## Step 1: Check Authentication

Call `muggle_auth_status` to verify login state.

**If not authenticated:**
1. Call `muggle_auth_login` to start device code flow
2. Present verification URL and code to user
3. Poll with `muggle_auth_poll` until complete
4. Confirm: "Logged in as user@example.com"

**If authenticated:** Proceed to next step.

## Step 2: Select Project to Publish

Call `muggle_project_list` to show available local projects.

**Present options:**
```
Local projects available for publishing:

1. proj_abc - "My Web App" (http://localhost:3000)
   - originalUrl: https://app.example.com (from cloud pull)
   - 3 use cases, 8 test cases, 5 test scripts
   - Last modified: 2 hours ago

2. proj_def - "Admin Portal" (http://localhost:4000)
   - No originalUrl set
   - 2 use cases, 4 test cases, 2 test scripts
   - Last modified: 1 day ago

Which project to publish?
```

**If user specifies project name:** Match and confirm.

## Step 3: Resolve Production URL (Inheritance Chain)

Before publishing, determine the production URL using the inheritance chain.

### URL Resolution Priority

For each entity being published, resolve URL in this order:

```
1. Test Case URL (if not localhost)
      ↓ (skip if localhost or empty)
2. Test Case originalUrl (from cloud pull)
      ↓ (skip if empty)
3. Use Case URL (if field exists and not localhost)
      ↓ (skip if localhost or empty)
4. Project URL (if not localhost)
      ↓ (skip if localhost)
5. Project originalUrl (from cloud pull)
      ↓ (skip if empty)
6. Ask User for production URL
```

### URL Validation Rules

| URL Type | Action |
| :------- | :----- |
| `http://localhost:*` | Skip, try next in chain |
| `http://127.0.0.1:*` | Skip, try next in chain |
| `https://*.example.com` | Valid, use this |
| `https://staging.*` | Valid, use this |
| Empty/null | Skip, try next in chain |

### Resolution Logic

```
function resolveProductionUrl(testCase, useCase, project):
    # Check test case URL
    if testCase.url and not isLocalhost(testCase.url):
        return testCase.url
    
    # Check test case originalUrl (from cloud pull)
    if testCase.originalUrl:
        return testCase.originalUrl
    
    # Check project URL
    if project.url and not isLocalhost(project.url):
        return project.url
    
    # Check project originalUrl (from cloud pull)
    if project.originalUrl:
        return project.originalUrl
    
    # Ask user
    return askUserForProductionUrl()
```

### Example: URL Inheritance in Action

**Scenario:** Project was pulled from cloud, tested locally, now publishing.

| Entity | url | originalUrl | Resolved |
| :----- | :-- | :---------- | :------- |
| Project | `localhost:3000` | `https://app.example.com` | - |
| Test Case A | `localhost:3000/login` | `https://app.example.com/login` | `https://app.example.com/login` (from originalUrl) |
| Test Case B | `localhost:3000/dashboard` | (none) | `https://app.example.com` (from project.originalUrl) |
| Test Case C (new) | `localhost:3000/settings` | (none) | Ask user |

### When to Ask User

Only ask user for production URL when:
1. No valid non-localhost URL found in entire inheritance chain
2. Entity is newly created (not pulled from cloud)
3. User explicitly wants to override

**Prompt:**
```
Test case "Login Flow" needs a production URL for cloud testing.

Current URL: http://localhost:3000/login

No production URL found in:
- Test case originalUrl: (not set)
- Project originalUrl: (not set)

Enter production URL (e.g., https://app.example.com/login):
```

## Step 4: Check Existing Cloud Project

Call `muggle_publish_project` which internally checks for existing cloud mapping.

**Behavior:**
- If local project has `cloudProjectId` → Updates existing cloud project
- If local project has `cloudSource.cloudProjectId` → Updates that cloud project
- If no cloud mapping exists → Creates new cloud project

**What gets synced:**
1. Project metadata (name, description, resolved URL)
2. All use cases under the project
3. All test cases under each use case (with resolved URLs)
4. Test script references (already uploaded by electron-app during generation)

## Step 5: Publish Entities

### Publish Project

```
{
  "projectId": "<local_project_id>",
  "targetUrl": "<resolved_production_url>"  // From inheritance chain
}
```

**Returns:**
- `cloudProjectId` - The cloud project ID
- `cloudUseCaseIds` - Mapping of local → cloud use case IDs
- `cloudTestCaseIds` - Mapping of local → cloud test case IDs
- `viewUrl` - URL to view project in Muggle AI dashboard

### URL Update During Publish

When publishing, the tool should:
1. Use resolved production URL (not localhost)
2. Update the cloud entity with production URL
3. Keep local entity with localhost URL for continued local testing
4. Store cloud URL mapping for reference

### Publish Individual Test Script (Optional)

If user wants to publish only specific test scripts:

```
{
  "projectId": "<local_project_id>",
  "testScriptId": "<local_test_script_id>",
  "cloudProjectId": "<cloud_project_id>",
  "cloudUseCaseId": "<cloud_use_case_id>",
  "cloudTestCaseId": "<cloud_test_case_id>"
}
```

**Note:** Test scripts are automatically uploaded to Firebase during generation. This tool confirms cloud status and returns the view URL.

## Step 6: Confirm Publication

After successful publish, report:

```
Publication Complete
====================

Project: "My Web App"
Cloud URL: https://app.muggle-ai.com/projects/cloud_proj_123
Production URL: https://app.example.com (inherited from originalUrl)

Published:
  [OK] 3 use cases
  [OK] 8 test cases  
  [OK] 5 test scripts

URL Resolution:
  - 6 test cases: Used originalUrl from cloud pull
  - 2 test cases: Used project.originalUrl
  - 0 test cases: Asked user (all had inherited URLs)

Cloud IDs mapped locally for future syncs.

Next steps:
- View in dashboard: https://app.muggle-ai.com/projects/cloud_proj_123
- Schedule automated runs
- Share with team members
```

## Selective Publishing

User can choose what to publish:

### Publish Everything

**User:** "Publish my project"

Publishes: Project + all use cases + all test cases + all test scripts

### Publish Specific Use Case

**User:** "Publish only the login use case"

1. `muggle_use_case_list` → Find matching use case
2. Publish project (if not already)
3. Publish only that use case and its test cases/scripts

### Publish Only New Content

**User:** "Publish only what's new"

1. Check cloud ID mappings
2. Identify entities without cloud IDs
3. Publish only unmapped entities

## Example Interactions

### Example 1: Publish with URL Inheritance

**User:** "Publish my tests to the cloud"

**Agent:**
1. `muggle_auth_status` → Authenticated
2. `muggle_project_list` → Found "My Web App" (localhost:3000, originalUrl: https://app.example.com)
3. Present project, user confirms
4. Resolve URLs:
   - Project: Use originalUrl `https://app.example.com`
   - Test cases: Each inherits from its originalUrl or project.originalUrl
5. `muggle_publish_project` with resolved URL
6. Report: "Published! All URLs resolved from originalUrl (cloud pull)"

### Example 2: First-Time Publish (No originalUrl)

**User:** "Publish my tests to the cloud"

**Agent:**
1. `muggle_auth_status` → Authenticated
2. `muggle_project_list` → Found "New App" (localhost:4000, no originalUrl)
3. Present project, user confirms
4. Check URL inheritance chain:
   - Test cases: All localhost, no originalUrl
   - Project: localhost, no originalUrl
5. Ask user: "No production URL found. Enter production URL:"
6. User provides: "https://newapp.example.com"
7. `muggle_publish_project` with user-provided URL
8. Report: "Published with https://newapp.example.com"

### Example 3: Mixed URLs (Some New Test Cases)

**User:** "Publish my project"

**Agent:**
1. `muggle_project_list` → Found project with originalUrl
2. Check each test case:
   - tc_001: has originalUrl → use it
   - tc_002: has originalUrl → use it
   - tc_003 (new): no originalUrl → inherit from project.originalUrl
3. All URLs resolved without asking user
4. `muggle_publish_project`
5. Report: "Published! 2 used own originalUrl, 1 inherited from project"

### Example 4: Re-publish After Changes

**User:** "Sync my project to the cloud"

**Agent:**
1. `muggle_auth_status` → Authenticated
2. `muggle_project_list` → User has 1 project with cloud mapping
3. `muggle_publish_project` → Updates existing cloud project
4. Report: "Synced 2 new test cases, 1 updated use case"

## Quick Reference

| Action | Tool |
| :----- | :--- |
| Check login | `muggle_auth_status` |
| Start login | `muggle_auth_login` |
| Complete login | `muggle_auth_poll` |
| List projects | `muggle_project_list` |
| Get project details | `muggle_project_get` |
| Update project URL | `muggle_project_update` |
| Publish project | `muggle_publish_project` |
| Publish test script | `muggle_publish_test_script` |

## URL Inheritance Summary

| Source | Priority | When Used |
| :----- | :------- | :-------- |
| Test Case URL | 1 | If not localhost |
| Test Case originalUrl | 2 | If set (from cloud pull) |
| Project URL | 3 | If not localhost |
| Project originalUrl | 4 | If set (from cloud pull) |
| Ask User | 5 | Last resort |

## Notes

- **URL inheritance:** Always try to resolve production URL from existing metadata before asking user.
- **originalUrl preserved:** When pulled from cloud, originalUrl stores the production URL for publishing.
- **Authentication required:** All publish operations require Muggle AI login.
- **Local URLs unchanged:** Publishing doesn't modify local entity URLs (keeps localhost for testing).
- **Idempotent:** Re-publishing updates existing cloud entities, doesn't duplicate.
- **Scripts auto-uploaded:** Test scripts are uploaded to Firebase during generation by electron-app.
- **Cloud ID mapping:** Local storage tracks cloud IDs for future syncs.
- **No auto-publish:** This skill only publishes when explicitly requested.
- **No browser fallback:** If Local MCP flow cannot proceed, fail fast with clear remediation steps.
