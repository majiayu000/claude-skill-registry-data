---
name: sandbox-resources
description: Discover all resources in your Amplify sandbox (DynamoDB tables, Lambda functions, data models, auth config) by reading amplify_outputs.json and querying AppSync.
---

# Sandbox Resources Discovery Skill

## Purpose

When you run `npx ampx sandbox`, it deploys AWS resources (DynamoDB tables, Lambda functions, etc.) to your AWS account. This skill helps you quickly discover what resources are deployed without manually checking the AWS console.

**Common questions this skill answers:**
- "What DynamoDB tables are in my sandbox?"
- "What Lambda functions did my sandbox create?"
- "What's the physical AWS name of the Company table?"
- "Show me my sandbox resources"

## Activation

Invoke with simple phrases like:

- "Discover my sandbox"
- "Show my sandbox resources"
- "What's in my sandbox?"
- "List sandbox tables and functions"
- "Sandbox discovery"

**Example:**
```
User: "Discover my sandbox"

Claude: Uses MCP to find all DynamoDB tables and Lambda functions,
then shows you what exists with physical AWS names.
```

## How It Works

When you ask about your sandbox resources:

1. **Reads amplify_outputs.json** from your Amplify project (local file, no AWS API needed yet)
2. **Queries AppSync API** using the GraphQL URL from amplify_outputs.json
3. **Discovers all resources** connected to AppSync: DynamoDB tables, Lambda functions, data models, auth config
4. **Presents complete inventory** with physical AWS names, schemas, and metadata you can use with AWS CLI

## What Gets Discovered

### DynamoDB Tables
- Table name (physical AWS name)
- Data source name (how AppSync references it)
- Region
- Full table ARN for CLI access

**Example:**
```
ClaudeQueryLog Table
Physical name: ClaudeQueryLog-4mogzwizrffkrmux5kud2mtuiy-NONE
Region: us-east-1
```

### Lambda Functions
- Function name
- Function ARN (for invocation)
- Data source name (how AppSync references it)
- Runtime and configuration

**Example:**
```
queryClaude Function
ARN: arn:aws:lambda:us-east-1:755956835466:function:queryClaude
Data Source: QueryClaudeLambdaDataSource
```

### Data Models (GraphQL Schema)
- Model name (Conversation, Message, ClaudeQueryLog, etc.)
- Field count
- Field definitions
- Authorization rules
- Custom indexes

**Example:**
```
Conversation Model
Fields: 5 (id, topic, createdAt, updatedAt, messages)
Authorization: Public API Key access
Custom Index: conversationsByCreatedAt
```

### Authentication Configuration
- Cognito User Pool ID
- Identity Pool ID
- OAuth providers (Google, etc.)
- OAuth domain
- Password policy

## Workflow

### Step 1: Discover Resources
When user asks "discover my sandbox", Claude:
1. Calls the MCP tool `amplify_discover_sandbox_resources()`
2. Tool reads amplify_outputs.json from project directory
3. Tool queries AppSync using GraphQL URL from amplify_outputs.json
4. Returns complete inventory: tables, functions, models, auth config

### Step 2: Display Results
Claude presents formatted output:
```
🔌 AppSync API: 4mogzwizrffkrmux5kud2mtuiy
   URL: https://rg7i3n4o65cgzgquwyamxpki44.appsync-api.us-east-1.amazonaws.com/graphql

📊 DynamoDB Tables (3 found):
• ClaudeQueryLog-4mogzwizrffkrmux5kud2mtuiy-NONE
• Conversation-4mogzwizrffkrmux5kud2mtuiy-NONE
• Message-4mogzwizrffkrmux5kud2mtuiy-NONE

⚡ Lambda Functions (1 found):
• queryClaude (arn:aws:lambda:us-east-1:755956835466:function:queryClaude)

📚 Data Models (3 found):
• Conversation (5 fields, public access)
• Message (9 fields, public access)
• ClaudeQueryLog (10 fields, public access)

🔐 Authentication:
• User Pool: us-east-1_JAZUgr7FJ
• OAuth: Google
```

### Step 3: Enable Further Action
User can then:
- "Query the Company table with AWS CLI"
- "Show me what's in the User table"
- "Invoke the databricksAgent function"
- "Check Lambda function logs"

## Critical Rules

1. **Always discover first** - Get real resource names before suggesting CLI commands
2. **Show physical names** - Users need the full `amplify-...` names for AWS CLI
3. **Provide copy-paste CLI** - Make it easy to run commands immediately
4. **Handle errors gracefully** - If sandbox isn't running, explain clearly
5. **Region awareness** - Default to us-east-1 but allow override

## Common Use Cases

### "I just started my sandbox - what got created?"
→ Discover resources, show all tables and functions

### "How many items are in each table?"
→ Show item counts for all DynamoDB tables

### "I want to query the TransportationInsight table"
→ Discover, find physical table name, provide AWS CLI command

### "What Lambda functions do I have?"
→ List all functions with runtime and timeout details

### "Check if my data was created"
→ Show table item counts to verify data exists

## Error Handling

**If amplify_outputs.json is missing:**
```
Error: amplify_outputs.json not found in current directory

Make sure you've run: npx ampx sandbox

Try these steps:
1. Navigate to your Amplify project: cd my-amplify-project
2. Start the sandbox: npx ampx sandbox
3. Wait 2-3 minutes for resources to deploy
4. Then ask "discover my sandbox"
```

**If sandbox AppSync API not found:**
```
Error: Could not find AppSync API matching URL

The sandbox may not be running. Run "npx ampx sandbox" to start it.
```

**If AWS credentials are wrong:**
```
Error: Failed to query AppSync APIs - Access denied

Verify:
1. AWS_ACCESS_KEY_ID is set
2. AWS_SECRET_ACCESS_KEY is set
3. User has AppSync permissions (appsync:ListGraphqlApis, appsync:ListDataSources)
```

## Tips & Tricks

### 1. Check Sandbox Health
```
User: "What resources are in my sandbox?"
Claude: Discovers and shows counts
Result: Verify everything deployed correctly
```

### 2. Monitor Data Creation
```
User: First ask "discover sandbox"
User: Run your test
User: Ask "discover sandbox again" - compare item counts
Result: See exactly how many records were created/deleted
```

### 3. Find Physical Names for CLI
```
User: "Discover my sandbox"
Claude: Shows physical names like "amplify-tiapp-feather-san-company-abc123def"
User: Copy/paste that name into AWS CLI commands
```

### 4. Multi-Region Testing
```
User: "Show my sandbox in us-west-2"
Result: Discover resources in different region
```

## Related Skills & Tools

- **AWS CLI** - Use the physical names discovered here to query tables manually
- **handbook** - Learn best practices for data modeling in Amplify
- **webapp-testing** - Test your frontend against the sandbox

## See Also

- [AWS DynamoDB CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/)
- [AWS Lambda CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/lambda/)
- [Amplify Data Documentation](https://docs.amplify.aws/gen2/build-a-backend/data/)

## Success Criteria

✅ User asks about sandbox resources (e.g., "Discover my sandbox")
✅ Claude calls `amplify_discover_sandbox_resources` tool
✅ Tool reads amplify_outputs.json from current directory
✅ Tool queries AppSync and discovers all resources
✅ Claude displays: DynamoDB tables, Lambda functions, data models, auth config
✅ User gets physical AWS resource names and ARNs for CLI access
✅ Error messages are clear and guide user to next steps
✅ Works automatically from project directory with amplify_outputs.json present
