---
name: awslabs-aws-api-mcp-server-call-aws
description: "To run an exact AWS CLI command, execute a validated `aws ...` command for direct AWS operations when you already know the precise service and parameters; use instead of suggesting commands."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"awslabs.aws-api-mcp-server","tool_name":"call_aws","arguments":{}}
```

## Tool Description
Execute AWS CLI commands with validation and proper error handling. This is the PRIMARY tool to use when you are confident about the exact AWS CLI command needed to fulfill a user's request. Always prefer this tool over 'suggest_aws_commands' when you have a specific command in mind.     Key points:     - The command MUST start with "aws" and follow AWS CLI syntax     - Commands are executed in us-west-2 region by default     - For cross-region or account-wide operations, explicitly include --region parameter     - All commands are validated before execution to prevent errors     - Supports pagination control via max_results parameter     - Commands can only reference files within the working directory (/var/folders/_0/ff3ds_c93pv14wnhx96y00400000gn/T/aws-api-mcp/workdir); use forward slashes (/) regardless of the system (e.g. if working directory is 'c:/tmp/workdir', use 'c:/tmp/workdir/subdir/file.txt' or 'subdir/file.txt'); relative paths resolve from the working directory.      Best practices for command generation:     - Always use the most specific service and operation names     - Always use the working directory when writing files, unless user explicitly mentioned another directory     - Include --region when operating across regions     - Only use filters (--filters, --query, --prefix, --pattern, etc) when necessary or user explicitly asked for it      Command restrictions:     - DO NOT use bash/zsh pipes (|) or any shell operators     - DO NOT use bash/zsh tools like grep, awk, sed, etc.     - DO NOT use shell redirection operators (>, >>, <)     - DO NOT use command substitution ($())     - DO NOT use shell variables or environment variables      Common pitfalls to avoid:     1. Missing required parameters - always include all required parameters     2. Incorrect parameter values - ensure values match expected format     3. Missing --region when operating across regions      Returns:         CLI execution results with API response data or error message

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "properties": {
    "cli_command": {
      "description": "The complete AWS CLI command to execute. MUST start with \"aws\"",
      "type": "string"
    },
    "max_results": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional limit for number of results (useful for pagination)"
    }
  },
  "required": [
    "cli_command"
  ],
  "type": "object"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"awslabs.aws-api-mcp-server","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
