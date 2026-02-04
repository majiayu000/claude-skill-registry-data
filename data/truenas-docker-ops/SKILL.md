---
name: truenas-docker-ops
description: Interact with Docker containers running on a TrueNAS server via SSH. Use this skill when working with containers on the remote TrueNAS server, including querying databases, inspecting logs, executing commands, or managing container state. Particularly useful for complex operations requiring nested SSH and docker exec commands with special escape sequences.
---

# TrueNAS Docker Operations

## Overview

Enable seamless interaction with Docker containers running on a TrueNAS server accessed via SSH. The skill provides helper scripts for complex nested command execution and reference documentation for server layout and container discovery.

## When to Use This Skill

Use this skill when:
- Querying databases inside containers on the TrueNAS server
- Executing Python or SQL code in remote containers
- Inspecting container logs, status, or configurations
- Working with containers where nested SSH and docker exec commands require complex escape sequences
- Discovering container locations, volume mappings, or configurations on the server

## Server Access

Access the TrueNAS server using the pre-configured SSH alias:

```bash
ssh truenas
```

Authentication is already configured. For detailed server layout information including directory structure and container patterns, refer to `references/server_layout.md`.

## Core Operations

### Discover Running Containers

List all running containers:
```bash
ssh truenas docker ps
```

Filter for specific containers:
```bash
ssh truenas docker ps | grep <container-name>
```

### View Container Configuration

Check the docker-compose file for volume mappings, networks, and settings:
```bash
ssh truenas cat /mnt/performance/home/admin/Develop/nixonomicon/nas/stacks/<container-name>/docker-compose.yml
```

### Execute Python Code in Container

For complex Python execution requiring nested heredocs and escape sequences, use the provided helper script:

```bash
~/.claude/plugins/marketplaces/claude-skills-marketplace/homelab-plugin/skills/truenas-docker-ops/scripts/docker_exec_python.sh <container_name> '<python_code>'
```

**Example:**
```bash
~/.claude/plugins/marketplaces/claude-skills-marketplace/homelab-plugin/skills/truenas-docker-ops/scripts/docker_exec_python.sh anypod '
import sqlite3, json
conn = sqlite3.connect("/data/db/anypod.db")
conn.row_factory = sqlite3.Row
result = conn.execute("SELECT * FROM feed").fetchall()
print(json.dumps([dict(r) for r in result], indent=2))
conn.close()
'
```

The script handles complex quoting and escape sequences for:
1. SSH connection to remote server
2. Docker exec with stdin input
3. Python code containing quotes, newlines, and special characters

**Note**: When using dictionary access in f-strings (e.g., `f"{dict['key']}"`), extract to variables first to avoid quote escaping issues:
```python
# Instead of: print(f"{row['status']}")
# Use:
status = row["status"]
print(f"{status}")
```

### Execute SQLite Queries in Container

For direct SQLite queries, use the provided helper script:

```bash
~/.claude/plugins/marketplaces/claude-skills-marketplace/homelab-plugin/skills/truenas-docker-ops/scripts/docker_exec_sqlite.sh <container_name> <db_path> '<sql_query>'
```

**Example:**
```bash
~/.claude/plugins/marketplaces/claude-skills-marketplace/homelab-plugin/skills/truenas-docker-ops/scripts/docker_exec_sqlite.sh anypod /data/db/anypod.db '
SELECT feed_id, status, COUNT(*) as count
FROM download
GROUP BY feed_id, status;
'
```

### View Container Logs

```bash
ssh truenas docker logs <container-name>
```

Add `-f` to follow logs in real-time:
```bash
ssh truenas docker logs -f <container-name>
```

### Simple Command Execution

For straightforward commands without complex escaping needs:
```bash
ssh truenas docker exec -i <container-name> <command>
```

**Example:**
```bash
ssh truenas docker exec -i anypod ls -la /data
```

## Directory Structure Reference

Key locations on the TrueNAS server:

- **Compose files**: `/mnt/performance/home/admin/Develop/nixonomicon/nas/stacks/`
- **Configs**: `/mnt/performance/docker/`
- **Large data**: `/mnt/capacity/watch/`

For complete directory structure details and container patterns, see `references/server_layout.md`.

## Determining What to Run Where

**Use helper scripts when:**
- Executing multi-line Python code in containers
- Running SQL queries with complex syntax
- Dealing with nested heredocs or quote escaping
- The command would require trial-and-error to get the escaping right

**Use direct commands when:**
- Running simple single commands
- Viewing logs or status
- Listing files or inspecting basic container state
- The operation doesn't involve complex escape sequences

## Resources

### scripts/

**`docker_exec_python.sh`** - Execute Python code inside a Docker container on TrueNAS
- Handles complex escape sequences for nested SSH and docker exec with heredoc
- Usage: `~/.claude/plugins/marketplaces/claude-skills-marketplace/homelab-plugin/skills/truenas-docker-ops/scripts/docker_exec_python.sh <container_name> '<python_code>'`
- Avoids manual trial-and-error of nested quoting

**`docker_exec_sqlite.sh`** - Execute SQLite queries inside a Docker container on TrueNAS
- Handles complex escape sequences for SQL queries
- Usage: `~/.claude/plugins/marketplaces/claude-skills-marketplace/homelab-plugin/skills/truenas-docker-ops/scripts/docker_exec_sqlite.sh <container_name> <db_path> '<sql_query>'`
- Simplifies database inspection workflows

### references/

**`server_layout.md`** - Complete TrueNAS server structure documentation
- SSH access patterns
- Directory structure for compose files, configs, and data
- Container discovery techniques
- Common container patterns and examples
- Volume mapping conventions
