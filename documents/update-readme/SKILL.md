---
name: update-readme
description: Autonomously audit the entire repository and update the main README with comprehensive, accurate documentation of the current codebase
---

# Update Repository README Skill (Enhanced)

## Purpose
Autonomously audit the entire repository and update the main README with comprehensive, accurate documentation of the current codebase. This skill is designed for AI-first consumption, ensuring complete context for understanding the system holistically.

**Enhanced with:** Git diff intelligence, structured reporting, cross-domain impact analysis, validation, and user review workflow.

## Activation
Invoke with: `update-readme` (no parameters required)

Example:
```
"Hey, we just finished our day. Go ahead and use your update repo README skill and go ahead and do what you need to do."
```

## Key Enhancements

This enhanced version includes:

1. **Git Diff Intelligence** - Parses recent commits to identify priorities and new features
2. **Structured JSON Reports** - Sub-agents use JSON instead of markdown for easier synthesis
3. **Handbook Scanning** - Maps available handbook files for accurate referencing
4. **Efficient Handbook Loading** - Main agent loads once, distributes to sub-agents
5. **Proposed Content Drafting** - Sub-agents write actual content, not just identify gaps
6. **Cross-Domain Impact Analysis** - Identifies how changes in one domain affect others
7. **Conflict Resolution** - Detects and resolves contradictions between agents
8. **Progress Tracking** - TodoWrite updates keep user informed throughout execution
9. **Explicit Roadmap Logic** - Systematic rules for updating roadmap items
10. **Validation Phase** - Checks markdown syntax, links, duplicates before finalizing
11. **User Review Workflow** - Shows diff summary and gets approval before committing
12. **No Auto-Push** - User chooses whether to commit and/or push changes

## Workflow Overview

### Phase 1: Discovery & Preparation

**Use TodoWrite immediately to track progress throughout this skill execution.**

#### 1.1 Git Diff Analysis (Enhanced)
Parse recent git activity to identify priorities:

```bash
# Get commits since README was last modified
git log README.md -1 --format="%H"  # Last README commit
git log --since="24 hours ago" --name-only --pretty=format:"%s"
```

**Extract intelligence:**
- List of changed files and their paths
- Commit messages (identify new features, bug fixes, refactors)
- Folders with most activity (priority for auditing)
- New files added (might need documentation)
- Deleted files (remove from README if referenced)

**Create priority map:**
```json
{
  "high_priority": ["amplify/auth", "src/app"],
  "new_features": ["Custom auth triggers", "Real-time subscriptions"],
  "deleted_features": [],
  "commits_analyzed": 50
}
```

#### 1.2 Repository Structure Discovery
Automatically detect all major subsystems:
- `/amplify` - Backend infrastructure (auth, data, functions)
- `/src` - Frontend code (pages, components, hooks)
- `amplify_outputs.json` - Runtime AWS resource configuration
- TypeScript interfaces and type definitions
- GraphQL schema (AppSync)
- Package.json and environment setup
- Lambda function patterns and integrations
- Known TODOs and limitations (grep for TODO comments)

#### 1.3 Resources Handbook Scan (NEW)
Map available handbook documentation:

```bash
ls -R resources/handbook/
```

**Create handbook map:**
```json
{
  "auth": ["AUTH_SETUP.md", "OAUTH_SETUP.md"],
  "data": ["GROUP_AUTHORIZATION.md", "DATA_MODELING.md"],
  "functions": ["AUTHORIZATION_EXPLAINED.md", "LAMBDA_PATTERNS.md"],
  "available": true
}
```

**Provide this map to sub-agents** so they can accurately reference handbook files.

### Phase 2: Parallel Sub-Agent Audits (Enhanced)

#### 2.1 Preparation
1. **Update TodoWrite:** Mark "Discovery complete", set "Sub-agent audits" to in_progress
2. **Load handbook ONCE** (main agent loads it, extracts key concepts)
3. **Prepare sub-agent context package** containing:
   - Current README
   - Priority map (from git diff analysis)
   - Handbook map (from resources scan)
   - Key Amplify concepts (extracted from handbook)
   - Handbook sections relevant to their domain

#### 2.2 Spin Up 8 Sub-Agents
Each agent receives their **context package** (no need to load handbook independently).

**CRITICAL: Ignored Folders**
Sub-agents must NOT read these folders (excluded from tsconfig.json):
- `node_modules` - Dependencies, not part of codebase
- `resources` - Developer handbook, not part of app
- `src_original` - Old/archived code
- `src/warehouse` - Excluded from build
- `OldSource` - Legacy code
- `amplify/**/*` (for agents auditing `/src`)
- `context/**/*` - Meeting notes, not app code
- `scripts/**/*` - Utility scripts, not core app

**Rule:** Stick to your assigned folder. Do not explore excluded directories.

#### 2.3 Sub-Agent Execution Sequence

**Each sub-agent follows this sequence:**

a. **Step 1: Understand the App**
- Read the root README to understand what BeonIQ is
- Get context on the overall value proposition and architecture

b. **Step 2: Process Pre-Loaded Amplify Knowledge**
- Review Amplify Gen 2 concepts (provided in context package)
- Focus on concepts relevant to their domain:
  - Auth agents: Cognito, SSO, group-based authorization
  - Data agents: DynamoDB, GraphQL schema, authorization rules
  - Function agents: Lambda patterns, two-pass system, resource access
  - Frontend agents: Client-side integration, hooks, providers

c. **Step 3: Review Priority Map**
- Check which files in their domain changed recently
- Prioritize audit efforts on high-activity areas
- Note new features from commit messages

d. **Step 4: Audit Their Assigned Domain**
- Read their assigned folder/subsystem thoroughly
- Compare current implementation against README section
- Identify gaps:
  - What's documented in README but not in code?
  - What's in code but not documented in README?
  - What changed since last README update (use priority map)?
  - What doesn't follow Amplify best practices?
  - What TODOs or known limitations exist?

e. **Step 5: Draft Proposed Content (NEW)**
- Don't just identify gaps - write the actual content
- Draft new sections, code examples, explanations
- Include file references with line numbers

f. **Step 6: Write Structured JSON Report (CHANGED)**
- Create a JSON report (`.readme-report-[domain].json`)
- Use this structured format:

```json
{
  "domain": "Backend Infrastructure",
  "agent_id": 1,
  "audit_complete": true,
  "priority_areas_reviewed": ["amplify/auth", "amplify/data"],

  "accurate_documentation": [
    {
      "topic": "Multi-tenant architecture",
      "readme_section": "Multi-Tenant Architecture",
      "status": "accurate"
    }
  ],

  "missing_documentation": [
    {
      "topic": "OAuth redirect URI configuration",
      "severity": "high",
      "readme_section": "Authentication Setup",
      "proposed_content": "After running `npx ampx sandbox`, add your unique Cognito domain to Google Cloud Console:\n1. Go to...",
      "code_references": ["amplify/auth/resource.ts:45-67"]
    }
  ],

  "outdated_documentation": [
    {
      "topic": "SUPER_ADMIN role explanation",
      "readme_section": "Multi-Tenant Architecture (line 206)",
      "current_text": "SUPER_ADMIN users...",
      "proposed_text": "SUPER_ADMIN is a platform permission...",
      "reason": "Implementation changed to require company group assignment"
    }
  ],

  "new_features_found": [
    {
      "feature": "Custom Cognito auth triggers",
      "discovered_in": "amplify/auth/resource.ts",
      "should_document": true,
      "proposed_section": "Authentication Setup > Custom Triggers",
      "proposed_content": "BeonIQ now supports custom Cognito triggers for..."
    }
  ],

  "handbook_references": [
    {
      "topic": "Lambda authorization two-pass system",
      "handbook_file": "resources/handbook/functions/AUTHORIZATION_EXPLAINED.md",
      "should_link": true,
      "suggested_location": "Development Guidelines > Lambda Authorization Pattern"
    }
  ],

  "cross_domain_impacts": [
    {
      "affects_domain": "Data Layer",
      "topic": "Group-based authorization changes",
      "note": "Auth agents modified group filtering - Data agents should verify authorization rules are documented"
    }
  ],

  "todos_found": [
    "amplify/auth/resource.ts:89: TODO: Add MFA support"
  ],

  "recommendations": [
    "Add explicit OAuth redirect URI setup steps",
    "Document custom auth trigger patterns",
    "Link to AUTHORIZATION_EXPLAINED.md from Lambda section"
  ]
}
```

#### 2.4 Progress Tracking
**Update TodoWrite after each agent completes:**
- "Sub-agent audits (1/8 complete)"
- "Sub-agent audits (2/8 complete)"
- ... etc.

This gives user visibility into progress.

### Sub-Agent Assignments
Distribute domains across 8 agents:

**Amplify Backend (2 agents):**
1. **Agent: Backend Infrastructure** (`/amplify/auth` + `/amplify/data`)
   - Cognito authentication setup and OAuth integration
   - GraphQL schema and DynamoDB models
   - Authorization patterns and multi-tenant security

2. **Agent: Lambda Functions** (`/amplify/functions`)
   - Lambda handlers and patterns
   - Function resource access and permissions
   - Event triggers and integrations

**Frontend (4 agents):**
3. **Agent: Pages & Routes** (`/src/app`)
   - Next.js 15 App Router pages
   - Route structure and page organization
   - Route-specific features

4. **Agent: React Components** (`/src/components`)
   - Reusable UI components
   - Component patterns and organization
   - Material-UI integration

5. **Agent: Custom Hooks** (`/src/hooks`)
   - Custom React hooks
   - Hook patterns and utilities
   - State management helpers

6. **Agent: Providers & Middleware** (`/src/providers`, `middleware.ts`)
   - Context providers and state management
   - Authentication provider
   - Middleware configuration

**Configuration & Contracts (2 agents):**
7. **Agent: Configuration & Deployment** (`package.json`, `amplify.yml`, `next.config.js`, build process)
   - Project dependencies and scripts
   - Amplify infrastructure configuration
   - Deployment and build process
   - Environment variable requirements
   - CI/CD setup

8. **Agent: Type Definitions & API Contracts** (`amplify_outputs.json`, TypeScript interfaces, GraphQL operations)
   - Runtime AWS resource configuration
   - TypeScript type definitions
   - GraphQL schema and operations
   - Data model contracts

### Phase 2.5: Cross-Domain Impact Analysis (NEW)

**Update TodoWrite:** Mark "Sub-agent audits" complete, set "Cross-domain analysis" to in_progress

After all 8 JSON reports are collected, run a cross-reference check:

1. **Parse all `cross_domain_impacts` from JSON reports**
2. **Identify cross-cutting concerns:**
   - Auth changes that affect Data layer
   - Data model changes that affect Frontend
   - Lambda pattern changes that affect multiple domains

3. **Verification pass:**
   - If Agent A says "This affects Data layer", check if Data agent addressed it
   - If not, flag for synthesis agent to resolve

4. **Create impact map:**
```json
{
  "auth_to_data": ["Group filtering changes require authorization rule updates"],
  "functions_to_frontend": ["New Lambda patterns need client-side examples"],
  "unresolved_impacts": []
}
```

### Phase 3: Report Collection & Synthesis (Enhanced)

**Update TodoWrite:** Mark "Cross-domain analysis" complete, set "Synthesizing reports" to in_progress

1. **Load all 8 JSON reports** (structured data, easy to parse)

2. **Main synthesis agent reads:**
   - All 8 JSON reports
   - Cross-domain impact map (from Phase 2.5)
   - Git diffs (priority signals)
   - Current README (what exists now)
   - Handbook context (Amplify best practices)

3. **Conflict Resolution (NEW):**
   - Check for contradictions:
     - Agent A: "X is documented accurately"
     - Agent B: "X is missing"
   - If conflicts found:
     - Re-read the actual code/README to verify ground truth
     - Resolve based on evidence
     - Document resolution in synthesis notes

4. **Consolidate findings:**
   - Merge all `missing_documentation` items
   - Merge all `outdated_documentation` items
   - Merge all `new_features_found` items
   - Prioritize by severity (high > medium > low)
   - Cross-reference with impact map
   - Ensure holistic consistency

5. **Map to README sections:**
   - Group updates by README section
   - Identify sections needing major rewrites vs. minor edits
   - Prepare structured update plan

### Phase 4: README Update (Enhanced)

**Update TodoWrite:** Mark "Synthesizing reports" complete, set "Updating README" to in_progress

1. **Apply all consolidated updates** to the main README

2. **Sections to check/update:**
   - **Key Features** - Add new features found in code
   - **Tech Stack** - Update dependencies from package.json
   - **Architecture Overview** - Reflect major structural changes
   - **Data Models** - Add new models, update schema changes
   - **Project Structure** - Update folder tree if reorganized
   - **Quick Start** - Update setup steps if process changed
   - **Development Guidelines** - Add new patterns, update rules
   - **Production Deployment** - Update configuration requirements
   - **Key Integrations** - Document new external services
   - **Roadmap** - Apply explicit roadmap logic (see below)

3. **Roadmap Update Logic (NEW):**

   **Rules:**
   - Check each roadmap item against actual code
   - Move completed items from "Post-MVP" to "MVP" section
   - Update checkboxes based on implementation status
   - Add new items if major features exist but aren't on roadmap

   **Example:**
   ```markdown
   **Post-MVP Enhancements:**
   - [ ] Pin/unpin functionality for dashboard customization
   ```

   **If code shows pinning is implemented:**
   - Move to MVP section:
   ```markdown
   **MVP (November 2025):**
   - ✅ Pin/unpin functionality for dashboard customization
   ```

   **If new feature found (e.g., "export to CSV"):**
   - Add to Post-MVP:
   ```markdown
   **Post-MVP Enhancements:**
   - [ ] Export insights to CSV format
   ```

4. **Use proposed content from JSON reports:**
   - Sub-agents already drafted new sections
   - Insert their `proposed_content` directly
   - Add code examples they provided
   - Include file references with line numbers

5. **Add handbook links:**
   - Use handbook references from JSON reports
   - Format: `See [AUTHORIZATION_EXPLAINED.md](./resources/handbook/functions/AUTHORIZATION_EXPLAINED.md) for details`

### Phase 4.5: Validation (NEW)

**Update TodoWrite:** Mark "Updating README" complete, set "Validating changes" to in_progress

Before finalizing, validate the updated README:

1. **Markdown Syntax Check:**
   - Verify all code blocks are properly closed
   - Check header hierarchy (no skipped levels: H1 → H3)
   - Ensure lists are properly formatted
   - Verify tables have correct syntax

2. **Link Validation:**
   - Check all internal links point to existing files:
     - `./resources/handbook/...`
     - `./amplify/...`
     - `./src/...`
   - Verify handbook references exist
   - Test anchor links (if any)

3. **Duplicate Section Check:**
   - Scan for duplicate headers
   - Check for redundant content
   - Ensure no conflicting information

4. **Code Block Validation:**
   - Verify code examples have language specifiers
   - Check for syntax errors in code blocks
   - Ensure examples reference actual files/line numbers

5. **Completeness Check:**
   - All JSON report items addressed
   - No orphaned sections
   - Roadmap properly updated

**If validation fails:**
- Fix issues automatically where possible
- Flag critical issues for user review

### Phase 5: Review & User Approval (CHANGED)

**Update TodoWrite:** Mark "Validating changes" complete, set "Preparing review" to in_progress

**NO AUTO-PUSH. User must review first.**

1. **Generate change summary:**
   ```bash
   git add README.md
   git diff --staged README.md
   ```

2. **Create human-readable summary:**
   - Count additions/deletions:
     ```bash
     git diff --staged README.md --numstat
     ```
   - Identify sections changed
   - List new sections added
   - List sections updated
   - List sections deleted (if any)

3. **Present to user:**
   ```
   📊 README Update Summary
   ========================

   Changes detected:
   - Added 3 new sections
   - Updated 7 existing sections
   - Deleted 0 sections
   - Total: +245 lines, -67 lines

   New Sections:
   • "Custom Cognito Triggers" in Authentication Setup
   • "Real-time Subscription Patterns" in Key Integrations
   • "GraphQL API Reference" in Architecture Overview

   Updated Sections:
   • Multi-Tenant Architecture (updated SUPER_ADMIN explanation)
   • Lambda Authorization Pattern (added two-pass system details)
   • Development Guidelines (added new CDK override rules)
   • Quick Start (updated OAuth setup steps)
   • Roadmap (moved 2 items to MVP, added 1 new item)
   • Tech Stack (updated to Next.js 15)
   • Project Structure (added new function folders)

   Roadmap Updates:
   ✅ Moved to MVP: Pin/unpin functionality, Export reports
   📝 Added to Post-MVP: CSV export, Custom outlier thresholds

   Would you like to:
   1. Review the full diff (git diff --staged README.md)
   2. Commit and push changes
   3. Commit only (no push)
   4. Discard changes
   ```

4. **Wait for user decision**

5. **If user approves (option 2 or 3):**
   ```bash
   git commit -m "$(cat <<'EOF'
   docs: Update README from repository audit

   • Added 3 new sections
   • Updated 7 existing sections
   • Updated roadmap progress
   • Added handbook references

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

6. **If user chose option 2 (commit and push):**
   ```bash
   git push origin [current-branch]
   ```

7. **If user chose option 4 (discard):**
   ```bash
   git reset HEAD README.md
   git checkout README.md
   ```

### Phase 6: Cleanup

**Update TodoWrite:** Mark all tasks complete

1. **Delete all temporary JSON reports:**
   ```bash
   rm -f .readme-report-*.json
   ```

2. **Verify repo is clean:**
   ```bash
   ls -la | grep ".readme-report"  # Should return nothing
   ```

3. **Final status:**
   - README updated (committed or discarded based on user choice)
   - All temporary files deleted
   - Repository clean

## Context Requirements for Sub-Agents

Each sub-agent receives these inputs (pre-loaded in skill prompt):
- **Handbook Skill Context** - Amplify Gen 2 patterns and best practices
- **Current README** - What's documented now
- **Git Diff** - What changed (for priority)
- **amplify_outputs.json** - What AWS resources exist
- **Type Definitions** - TypeScript interfaces and data models
- **GraphQL Schema** - AppSync API contract
- **Environment Variables** - Configuration requirements
- **Build/Deploy Procedures** - How the system runs
- **TODOs & Limitations** - Known incomplete areas

## Critical Rules

1. **Holistic Audit** - Examine entire repo structure, not just changed files
2. **AI-First Documentation** - README is for AI consumption; assume agents reading it need complete context
3. **Amplify Fluency** - All sub-agents must understand Amplify Gen 2 patterns before auditing
4. **Structured Reports** - Domain reports use consistent format for easy synthesis
5. **No Artifacts** - Delete all temporary reports after consolidation
6. **Handbook First** - Sub-agents read handbook before their domain (pre-loaded)
7. **Root README First** - Sub-agents understand the app before diving into their domain
8. **Context Priority** - Complete context > minor optimization; better to include everything than miss connections

## Example Sub-Agent JSON Report

```json
{
  "domain": "GraphQL Data Layer",
  "agent_id": 2,
  "audit_complete": true,
  "priority_areas_reviewed": ["amplify/data"],

  "accurate_documentation": [
    {
      "topic": "Multi-tenant architecture",
      "readme_section": "Multi-Tenant Architecture",
      "status": "accurate"
    },
    {
      "topic": "Group-based authorization",
      "readme_section": "Multi-Tenant Architecture > How Multi-Tenancy Works",
      "status": "accurate"
    }
  ],

  "missing_documentation": [
    {
      "topic": "GraphQL API Reference",
      "severity": "high",
      "readme_section": "Architecture Overview",
      "proposed_content": "## GraphQL API Reference\n\n### Queries\n- `getTransportationInsight(id: ID!)` - Fetch a specific insight\n- `listTransportationInsights(filter: InsightFilter)` - List insights with filtering\n- `getCompany(id: ID!)` - Get company details\n\n### Mutations\n- `createTransportationInsight(input: CreateInsightInput!)` - Create new insight\n- `updateUser(id: ID!, input: UpdateUserInput!)` - Update user details\n\n### Subscriptions\n- `onInsightCreated(companyId: ID!)` - Real-time insight notifications\n- `onQueryJobUpdate(jobId: ID!)` - Job status updates",
      "code_references": ["amplify/data/resource.ts:45-120", "amplify/data/operations/"]
    },
    {
      "topic": "AppSync subscription patterns",
      "severity": "medium",
      "readme_section": "Key Integrations",
      "proposed_content": "### Real-Time Subscriptions\n\nAppSync enables live updates without polling:\n\n```typescript\n// Subscribe to QueryJob status changes\nconst subscription = client.models.QueryJob.onUpdate().subscribe({\n  next: (update) => {\n    if (update.status === 'COMPLETED') {\n      // Fetch and display the insight\n    }\n  }\n});\n```\n\nSee `src/app/ask-data/page.tsx:156-178` for implementation.",
      "code_references": ["src/app/ask-data/page.tsx:156-178"]
    }
  ],

  "outdated_documentation": [
    {
      "topic": "SUPER_ADMIN role explanation",
      "readme_section": "Multi-Tenant Architecture (line 206)",
      "current_text": "SUPER_ADMIN is a platform permission",
      "proposed_text": "SUPER_ADMIN is a platform permission, NOT a company assignment. SUPER_ADMIN users must also be assigned to a company group (e.g., `BEONIQ`) to access company-scoped data. This ensures consistent multi-tenant architecture without special-case code.",
      "reason": "Implementation was clarified to require company group assignment for all users including SUPER_ADMIN"
    }
  ],

  "new_features_found": [
    {
      "feature": "Real-time DailySummary subscriptions",
      "discovered_in": "amplify/data/reports/resource.ts",
      "should_document": true,
      "proposed_section": "Key Features > Overview Dashboard",
      "proposed_content": "• **Real-time Updates** - Dashboard automatically refreshes when new daily summaries are generated via AppSync subscriptions"
    }
  ],

  "handbook_references": [
    {
      "topic": "Group-based authorization patterns",
      "handbook_file": "resources/handbook/data/GROUP_AUTHORIZATION.md",
      "should_link": true,
      "suggested_location": "Multi-Tenant Architecture > Additional Security Layers"
    }
  ],

  "cross_domain_impacts": [
    {
      "affects_domain": "Backend Infrastructure",
      "topic": "DynamoDB schema changes",
      "note": "New fields added to TransportationInsight model - Auth agents should verify group arrays are populated correctly"
    }
  ],

  "todos_found": [
    "amplify/data/resource.ts:89: TODO: Add indexes for faster queries",
    "amplify/data/insights/resource.ts:45: TODO: Add validation for metric ranges"
  ],

  "recommendations": [
    "Add complete GraphQL API reference section",
    "Document subscription patterns with examples",
    "Clarify SUPER_ADMIN group requirement",
    "Link to GROUP_AUTHORIZATION.md handbook",
    "Add data model field descriptions"
  ]
}
```

## Success Criteria

### Discovery & Analysis
✅ Git diff analysis complete with priority map generated
✅ Repository structure discovered and mapped
✅ Resources handbook scanned and indexed
✅ All 8 sub-agent JSON reports collected
✅ Cross-domain impact analysis complete
✅ Conflicts identified and resolved

### Documentation Quality
✅ Main README updated with all consolidated findings
✅ README is comprehensive, AI-readable, and reflects current implementation
✅ Cross-system impacts and connections documented
✅ Handbook patterns referenced where applicable
✅ Links to `/resources/handbook/` validated and accurate
✅ Roadmap explicitly updated (items moved, checkboxes updated, new items added)
✅ New features from git commits documented
✅ Code examples include file references with line numbers

### Validation & Quality Assurance
✅ Markdown syntax validated (no broken code blocks)
✅ Internal links verified (all handbook references exist)
✅ No duplicate sections created
✅ Code blocks have proper language specifiers
✅ No conflicting information in README

### User Experience
✅ Progress tracked throughout execution (TodoWrite updates)
✅ Change summary presented to user before commit
✅ User reviews diff and approves changes
✅ User chooses commit/push behavior (no auto-push)
✅ Clear count of additions/deletions shown

### Cleanup & Finalization
✅ All temporary JSON report files deleted (`.readme-report-*.json`)
✅ No artifacts left in repository
✅ Repository clean and organized
✅ Changes committed with descriptive message (if user approved)
✅ Changes pushed to remote (only if user explicitly chose to push)
