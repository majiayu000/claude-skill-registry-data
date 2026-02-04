---
name: Delegating to AWS Agent
description: Recognize AWS queries and delegate to specialized sub-agent to avoid context pollution
keywords: aws, ec2, s3, iam, ecs, lambda, cloudwatch, rds, cloud, infrastructure, deployment, bucket, instance
when_to_use: When user mentions AWS services, EC2 instances, S3 buckets, ECS deployments, IAM users/keys, or cloud infrastructure. ALWAYS delegate to sub-agent.
version: 1.0.0
---

# Delegating to AWS Agent

## Core Principle

**Never handle AWS operations directly.** Always delegate to a specialized sub-agent to keep your context clean and costs low.

## Recognition Patterns

Delegate when user says:
- "list ec2 instances"
- "show s3 buckets"
- "what access keys does user X have?"
- "deploy SERVICE to production"
- "show running instances"
- "what's in bucket X?"
- Any mention of: aws, ec2, s3, iam, ecs, lambda, cloudwatch, rds, bucket, instance

## How to Delegate

Use the Task tool with a specialized prompt:

```
Task(
  subagent_type: "general-purpose",
  description: "Query AWS infrastructure",
  prompt: "<full agent instructions from AGENT-INSTRUCTIONS.md>"
)
```

## Agent Prompt Template

When delegating, include:
1. The complete agent instructions (see AGENT-INSTRUCTIONS.md)
2. The user's specific request
3. Clear output format requirements

**Example:**

```
You are an AWS infrastructure specialist. Your job is to query AWS using shell wrappers and return clean results.

<AGENT INSTRUCTIONS HERE>

USER REQUEST: List all running EC2 instances

Return a clean summary with:
- Instance IDs
- Names
- States
- Instance types
- IP addresses
```

## After Agent Returns

1. **Present results cleanly** to user
2. **Offer follow-up** if relevant (e.g., "Would you like details on instance i-abc123?")
3. **Don't expose mechanics** (aws commands, authentication, profiles) to user

## Benefits

- ✅ Main context stays clean
- ✅ Cheaper queries (sub-agent uses less expensive model)
- ✅ Specialized knowledge isolated
- ✅ Scalable pattern for other services

## Example Flow

```
User: "list running ec2 instances"

Main Assistant: [Recognizes AWS query]
              → Invokes Task tool with agent instructions
              → Agent runs cloud-ec2-list --state running
              → Agent returns formatted results

Main Assistant: "Found 22 running instances:
                - i-0abc123 (production-web) [running] t3.medium
                - i-0def456 (staging-api) [running] t3.small
                ..."
```

## Red Flags

**DON'T:**
- ❌ Try to run cloud-* scripts yourself
- ❌ Construct aws CLI commands in main session
- ❌ Load detailed AWS API knowledge
- ❌ Handle authentication/profiles directly

**DO:**
- ✅ Immediately delegate on AWS keywords
- ✅ Trust the sub-agent's results
- ✅ Present clean summaries to user

## Version History

- 1.0.0 (2025-10-14): Initial delegation skill created to reduce context pollution
