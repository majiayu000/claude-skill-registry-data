---
name: ssh-executor
description: Read-only SSH command execution for remote server inspection
activation_keywords: [ssh, remote, server, execute, shell, command, host]
---

# SSH Executor Skill

Provides read-only SSH command execution for server inspection:
- Execute read-only commands on remote servers
- Check system status, disk usage, memory, processes
- View log files and configuration
- Network diagnostics (ping, netstat, ss)

Use `builtin_ssh_executor` tool with fields:
- `host`: remote server address (hostname or IP)
- `port`: SSH port (default: 22)
- `user`: SSH username
- `command`: the command to execute (read-only commands only)

Note: Write operations (rm, mv, cp, chmod, chown, etc.) are blocked for safety. Only read-only commands are allowed.
