---
name: awslabs-aws-api-mcp-server-suggest-aws-commands
description: "To get possible AWS CLI commands from a natural-language request, suggest candidate `aws ...` commands when the exact service, operation, or syntax is unclear; use before call-aws."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"awslabs.aws-api-mcp-server","tool_name":"suggest_aws_commands","arguments":{}}
```

## Tool Description
Suggest AWS CLI commands based on a natural language query. This is a FALLBACK tool to use when you are uncertain about the exact AWS CLI command needed to fulfill a user's request.      IMPORTANT: Only use this tool when:     1. You are unsure about the exact AWS service or operation to use     2. The user's request is ambiguous or lacks specific details     3. You need to explore multiple possible approaches to solve a task     4. You want to provide options to the user for different ways to accomplish their goal      DO NOT use this tool when:     1. You are confident about the exact AWS CLI command needed - use 'call_aws' instead     2. The user's request is clear and specific about the AWS service and operation     3. You already know the exact parameters and syntax needed     4. The task requires immediate execution of a known command      Best practices for query formulation:     1. Include the user's primary goal or intent     2. Specify any relevant AWS services if mentioned     3. Include important parameters or conditions mentioned     4. Add context about the environment or constraints     5. Mention any specific requirements or preferences      CRITICAL: Query Granularity     - Each query should be granular enough to be accomplished by a single CLI command     - If the user's request requires multiple commands to complete, break it down into individual tasks     - Call this tool separately for each specific task to get the most relevant suggestions     - Example of breaking down a complex request:       User request: "Set up a new EC2 instance with a security group and attach it to an EBS volume"       Break down into:       1. "Create a new security group with inbound rules for SSH and HTTP"       2. "Create a new EBS volume with 100GB size"       3. "Launch an EC2 instance with t2.micro instance type"       4. "Attach the EBS volume to the EC2 instance"      Query examples:     1. "List all running EC2 instances in us-east-1 region"     2. "Get the size of my S3 bucket named 'my-backup-bucket'"     3. "List all IAM users who have AdministratorAccess policy"     4. "List all Lambda functions in my account"     5. "Create a new S3 bucket with versioning enabled and server-side encryption"     6. "Update the memory allocation of my Lambda function 'data-processor' to 1024MB"     7. "Add a new security group rule to allow inbound traffic on port 443"     8. "Tag all EC2 instances in the 'production' environment with 'Environment=prod'"     9. "Configure CloudWatch alarms for high CPU utilization on my RDS instance"      Returns:         A list of up to 10 most likely AWS CLI commands that could accomplish the task, including:         - The CLI command         - Confidence score for the suggestion         - Required parameters         - Description of what the command does

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "properties": {
    "query": {
      "description": "A natural language description of what you want to do in AWS. Should be detailed enough to capture the user's intent and any relevant context.",
      "maxLength": 2000,
      "type": "string"
    }
  },
  "required": [
    "query"
  ],
  "type": "object"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"awslabs.aws-api-mcp-server","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
