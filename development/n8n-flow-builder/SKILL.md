---
name: n8n-flow-builder
description: Expert guidance for designing, building, and maintaining n8n workflows across dev/staging/prod environments on Railway with MCP integration. Handles flow authoring, node configuration, error handling, and deployment patterns.
---

# n8n Flow Builder

## Purpose
This skill provides comprehensive guidance for creating, testing, and deploying n8n workflows. It codifies best practices for flow design, node configuration, error handling, and multi-environment deployment (dev → staging → prod).

## When to Use This Skill
Claude should use this skill when:
- User asks to create or modify n8n workflows
- Building automation flows
- Configuring n8n nodes (HTTP, webhooks, database, etc.)
- Debugging n8n executions
- Deploying workflows across environments
- Integrating n8n with other systems via MCP

## Environment Context

### Three-Tier Architecture
1. **Dev (Local Docker)**
   - URL: `http://localhost:5678`
   - Purpose: Rapid iteration and testing
   - Database: Local SQLite or PostgreSQL
   - Usage: Initial development and experimentation

2. **Staging (Railway)**
   - Previously called "dev" (recently renamed to "staging")
   - Purpose: Pre-production validation
   - Database: Railway PostgreSQL
   - Usage: Integration testing, acceptance tests

3. **Prod (Railway)**
   - Purpose: Production workflows
   - Database: Railway PostgreSQL (separate instance)
   - Usage: Live automation for real business processes
   - Access: Railway-hosted n8n MCP server

### MCP Integration
- Railway hosts the n8n MCP server
- MCP provides programmatic access to n8n API
- Used for: deploying workflows, triggering executions, monitoring

## n8n Flow Design Patterns

### 1. Webhook-Triggered Workflows
**Pattern**: External systems trigger n8n via HTTP webhook

**Structure**:
```
Webhook Node (Trigger)
  ↓
Validate Input (IF node or Function)
  ↓
Process Data (various nodes)
  ↓
Branch on Outcome (IF node)
  ↓
Success Path → Respond with 200
Error Path → Log + Respond with 4xx/5xx
```

**Best Practices**:
- Always validate webhook payload structure
- Set webhook path to be descriptive: `/webhook/github-pr-created`
- Return appropriate HTTP status codes
- Include error handling for malformed payloads
- Log all webhook invocations for debugging

**Example Use Cases**:
- GitHub webhook for PR events
- Stripe webhook for payment events
- Slack webhook for slash commands

### 2. Scheduled Workflows
**Pattern**: Time-based automation (cron jobs)

**Structure**:
```
Schedule Trigger (Cron)
  ↓
Fetch Data (HTTP Request, Database Query)
  ↓
Process/Transform (Function, Code nodes)
  ↓
Take Action (Send notification, update records)
  ↓
Log Results
```

**Best Practices**:
- Use cron expressions for precise timing
- Include timezone considerations
- Add error notifications (Slack, email)
- Keep execution history for debugging
- Consider load during business hours

### 3. Long-Running Automations
**Pattern**: Workflows that take significant time or require human approval

**Structure**:
```
Trigger
  ↓
Initial Processing
  ↓
Wait Node (for approval or time delay)
  ↓
Continue Processing
  ↓
Complete
```

**Best Practices**:
- Use Wait nodes for delays or webhooks for approvals
- Store state in n8n's execution data
- Handle timeout scenarios
- Provide status endpoints for monitoring

## Common Node Configurations

### HTTP Request Node
**Purpose**: Call external APIs

**Configuration Tips**:
- Authentication: Store credentials in n8n credential system
- Error Handling: Enable "Continue on Fail" for non-critical requests

- Retry Logic: Configure retries for transient failures
- Timeout: Set appropriate timeouts (default may be too short)
- Headers: Use expressions for dynamic headers

**Common Patterns**:
```javascript
// Dynamic Authorization header
{{ $credentials.apiKey }}

// Query parameters from previous node
{{ $json.userId }}

// Conditional URL
{{ $node["IF"].json.environment === "prod" ? "api.prod.com" : "api.staging.com" }}
```

### Function Node
**Purpose**: Custom JavaScript/Python for complex logic

**Best Practices**:
- Keep functions small and focused
- Comment complex logic
- Handle null/undefined values
- Return consistent data structure
- Use try/catch for error handling

**Example**:
```javascript
// Transform data format
const items = $input.all();
return items.map(item => ({
  id: item.json.id,
  name: item.json.full_name || 'Unknown',
  created: new Date(item.json.timestamp).toISOString()
}));
```

### IF Node
**Purpose**: Conditional branching

**Configuration**:
- Use clear condition names: "Is Valid Email", "Has Permission"
- Chain multiple conditions with AND/OR
- Always handle both true/false branches
- Consider default/"else" path for unexpected values

### Set Node
**Purpose**: Store data for later use in workflow

**Best Practices**:
- Use descriptive key names
- Store intermediate results for debugging
- Keep values JSON-serializable
- Document expected structure

### Merge Node
**Purpose**: Combine data from multiple branches

**Modes**:
- **Append**: Combine all items (union)
- **Keep Key Matches**: Inner join on key
- **Combine**: Merge objects by key

**Common Use**:
```
Branch 1: Fetch user data
Branch 2: Fetch user's orders
  ↓
Merge (Keep Key Matches on userId)
  ↓
Result: User with their orders
```

## Error Handling Patterns

### 1. Try-Catch Pattern
```
Try Branch:
  → HTTP Request (Continue on Fail: enabled)
  → IF: Check for errors
    → Success path
    → Error path → Log + Notify
```

### 2. Global Error Workflow
- Configure at workflow level
- Catches all unhandled errors
- Sends notifications (Slack, email)
- Logs to monitoring system
- Pattern:
  ```
  Error Trigger
    ↓
  Extract Error Details
    ↓
  Format Error Message
    ↓
  Send to Slack/Email
    ↓
  Log to Database
  ```

### 3. Retry with Exponential Backoff
```javascript
// In Function node before HTTP request
const attempt = $json.attempt || 1;
const maxAttempts = 3;
const baseDelay = 1000; // 1 second

if (attempt <= maxAttempts) {
  return {
    ...item.json,
    attempt: attempt,
    delay: Math.pow(2, attempt - 1) * baseDelay
  };
}
// Max attempts reached, fail
throw new Error('Max retry attempts exceeded');
```

## Deployment Workflow

### Standard Deployment Process
1. **Develop in Local Docker**
   - Create workflow in local n8n
   - Test with sample data
   - Iterate quickly

2. **Export Workflow JSON**
   - Settings → Export Workflow
   - Save JSON file to project repo
   - Version control the JSON

3. **Deploy to Staging**
   - Use Railway n8n MCP to import workflow
   - Run acceptance tests
   - Verify integrations work
   - Check error handling

4. **Acceptance Testing**
   - Test happy path scenarios
   - Test error scenarios
   - Verify webhook responses
   - Check logging and monitoring

5. **Deploy to Prod**
   - Use Railway n8n MCP to import workflow
   - Enable workflow (set to active)
   - Monitor initial executions
   - Have rollback plan ready

### Rollback Plan
Always include in deployment documentation:
- Previous workflow version JSON (stored in git)
- Steps to restore previous version
- How to verify rollback succeeded
- Who to notify if rollback needed

## Integration Patterns

### GitHub Integration
**Use Cases**:
- PR created → notify team in Slack
- Issue labeled → update Linear ticket
- Push to main → trigger deployment

**Webhook Setup**:
1. GitHub repo → Settings → Webhooks
2. Add webhook URL: `https://n8n.railway.app/webhook/github-event`
3. Select events: Pull requests, Issues, Push
4. Set secret for verification

### Linear Integration
**Use Cases**:
- Issue status changed → update related GitHub issue
- New issue → post to Slack channel
- Issue assigned → notify assignee

**Best Practices**:
- Use Linear webhook for real-time updates
- Store Linear API key in n8n credentials
- Use GraphQL for complex queries

### Slack Integration
**Use Cases**:
- Send notifications
- Slash command handlers
- Interactive button responses

**Patterns**:
- Use Slack Bot token for posting messages
- Format messages with Block Kit
- Handle rate limits (1 message per second)

## Debugging and Troubleshooting

### Common Issues

**Issue**: Webhook not triggering
**Debug Steps**:
1. Check webhook is active in n8n
2. Verify webhook URL is correct
3. Check webhook secret/authentication
4. Look at n8n execution history
5. Test with manual webhook trigger

**Issue**: Workflow times out
**Solutions**:
- Increase workflow timeout in settings
- Break into smaller workflows
- Use Queue nodes for long operations
- Add Wait nodes to prevent rate limits

**Issue**: Data not passing between nodes
**Debug**:
- Check each node's output in execution view
- Verify node connections
- Check expressions for typos
- Use Set node to inspect data structure

### Logging Best Practices
- Add descriptive notes to complex nodes
- Use Set nodes to log intermediate state
- Include timestamp in log messages
- Log both success and failure paths
- Store critical execution data for audit trail

## Performance Optimization

### Tips for Fast Workflows
1. **Minimize HTTP Requests**
   - Batch API calls when possible
   - Cache responses when appropriate
   - Use HTTP Request Bulk mode

2. **Efficient Data Processing**
   - Filter early to reduce data volume
   - Use Code nodes for bulk operations
   - Avoid unnecessary transformations

3. **Parallel Execution**
   - Use Split In Batches for parallel processing
   - Configure concurrent execution limit
   - Balance speed vs. resource usage

4. **Database Queries**
   - Use indexes on frequently queried fields
   - Limit result sets
   - Use pagination for large datasets
   - Consider caching for read-heavy operations

## Security Best Practices

### Credential Management
- Never hardcode API keys or passwords
- Use n8n's credential system
- Rotate credentials regularly
- Use environment-specific credentials
- Document which workflows use which credentials

### Webhook Security
- Always validate webhook signatures
- Use HTTPS for webhook URLs
- Implement rate limiting
- Validate input data structure
- Sanitize user input

### Access Control
- Use Railway's authentication for n8n UI
- Limit who can edit production workflows
- Audit workflow changes
- Use separate credentials for dev/staging/prod

## Workflow Documentation Template

When creating a new workflow, document:

```markdown
# Workflow Name: [Descriptive Name]

## Purpose
[What this workflow does and why it exists]

## Trigger
- Type: [Webhook/Schedule/Manual]
- Configuration: [Details]

## Environment
- Dev: [Status/URL]
- Staging: [Status/URL]
- Prod: [Status/URL]

## Data Flow
[How data moves through the workflow]

## Error Handling
[How errors are caught and handled]

## Acceptance Tests
- [ ] Test case 1: [Description]
- [ ] Test case 2: [Description]
- [ ] Error scenario: [Description]

## Rollback Plan
[Steps to revert if deployment fails]

## Dependencies
- External APIs: [List]
- Credentials: [List]
- Other workflows: [List]

## Monitoring
- Success metrics: [What to measure]
- Error alerts: [Where they go]
- Logs: [Where to find them]
```

## Common Gotchas and Pitfalls

### 1. Webhook Path Conflicts
- Each webhook must have unique path
- Use descriptive paths: `/webhook/linear-issue-created`
- Document all webhook paths in central registry

### 2. Execution Mode Settings
- **Production**: Workflows run independently
- **Integration**: Workflows can call each other
- Choose based on workflow dependencies

### 3. Data Persistence
- Workflow execution data is temporary
- Use database or external storage for persistence
- Don't rely on workflow variables across executions

### 4. Rate Limiting
- APIs have rate limits (GitHub: 5000/hour)
- Implement exponential backoff
- Cache when possible
- Consider webhook alternatives to polling

### 5. Node Version Compatibility
- Nodes get updated in n8n releases
- Test workflows after n8n upgrades
- Export/import may require node updates
- Keep local dev n8n version in sync with Railway

## Quick Reference Commands

### Using n8n MCP (via Railway)
```javascript
// List all workflows
n8n.listWorkflows()

// Get workflow by ID
n8n.getWorkflow(workflowId)

// Execute workflow
n8n.executeWorkflow(workflowId, inputData)

// Import workflow JSON
n8n.importWorkflow(workflowJson)
```

### Local n8n (Docker)
```bash
# Start n8n
docker-compose up -d

# View logs
docker-compose logs -f n8n

# Stop n8n
docker-compose down

# Reset database (careful!)
docker-compose down -v
```

## Usage Examples

### Example 1: Create GitHub PR Notification Workflow
```
User: "Create an n8n workflow that sends a Slack message when a PR is created"

Claude (using n8n-flow-builder):
1. ✅ Designs webhook-triggered workflow
2. 📋 Configures Webhook node for GitHub events
3. 🔍 Adds validation for PR created event
4. 🔄 Extracts PR details (title, author, URL)
5. 💬 Configures Slack node with message format
6. 📝 Documents acceptance tests
7. 🚀 Provides deployment instructions for staging → prod
```

### Example 2: Daily Report Workflow
```
User: "Build a daily report that queries our database and emails results"

Claude (using n8n-flow-builder):
1. ⏰ Creates Schedule Trigger (cron: 0 9 * * 1-5) - weekdays at 9am
2. 🗄️ Configures PostgreSQL query node
3. 📊 Transforms data with Function node
4. 📧 Formats email with HTML template
5. ✉️ Configures Send Email node
6. ⚠️ Adds error handling with Slack notification
7. 📝 Documents expected output and rollback
```

### Example 3: Multi-Step Automation with Approval
```
User: "Create workflow that requires manager approval before executing"

Claude (using n8n-flow-builder):
1. 🎯 Trigger: Form submission webhook
2. 💾 Store request in database
3. 📧 Send approval email with unique URL
4. ⏸️ Wait node: Waits for webhook callback
5. ✅ On approval: Execute action + notify
6. ❌ On rejection: Log + notify requester
7. ⏱️ Timeout: Auto-reject after 24 hours
```

## Integration with Your Workflow

### When Claude Should Use This Skill
- Any mention of "n8n", "workflow", or "automation"
- Creating integrations between systems
- Setting up webhooks or scheduled tasks
- Deploying to Railway environments
- Debugging n8n executions

### Hand-off Artifacts
When completing n8n work, always provide:
- ✅ Workflow JSON (for version control)
- ✅ Documentation using template above
- ✅ Acceptance test checklist
- ✅ Deployment instructions (dev → staging → prod)
- ✅ Rollback plan
- ✅ Expected webhook URLs or schedule

### Coordination with Other Skills
- **linear-orchestration**: Create Linear issues for workflow deployment tasks
- **github-coordinator**: Store workflow JSON in version control
- **skill-manager**: Version and document new n8n patterns

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [n8n Workflow Templates](https://n8n.io/workflows)
- Railway n8n MCP: Use for programmatic deployment

## Notes

- Created: 2025-10-18
- Author: Kurt Anderson
- Version: 1.0.0
- This skill codifies Kurt's n8n workflow patterns and deployment process
- Environments were recently reorganized: old "dev" → "staging"
- Railway hosts both staging and prod instances plus n8n MCP server

## Meta-Pattern: Self-Improvement Protocol

### When Discovering n8n Workflow Improvements

**If the improvement is a general pattern:**
1. Update this skill (n8n-flow-builder)
2. Update the forked n8n MCP repository
3. Document in both places
4. Consider PR to upstream n8n MCP

**If the improvement is cross-system:**
1. Consider if it belongs in integration-workflows skill
2. Update integration-workflows if applicable

### Forked n8n MCP Repository
**Location:** [Your GitHub fork of n8n MCP]
**Purpose:** Community benefit + your own n8n agent improvements
**Update When:**
- New n8n node patterns discovered
- Better error handling approaches
- Deployment workflow improvements
- Railway-specific optimizations

### Example: Adding a New Pattern
```
Discovery: "Webhook validation pattern works great!"
  ↓
1. Add to n8n-flow-builder skill (this file)
2. Update forked n8n-mcp/docs/patterns.md
3. Test in n8n agent project
4. Commit both repos
5. Optional: PR to upstream n8n-mcp
```

This ensures improvements benefit:
- Future you
- Your n8n agent project  
- Other n8n MCP users
- The broader community
