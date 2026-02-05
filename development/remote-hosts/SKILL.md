---
name: remote-hosts
description: |
  Connect to and manage remote hosts. Run commands, check logs, debug issues on remote servers.
  Use when asked about: ssh to server, connect to host, check remote logs, debug remote,
  run command on server, PPE server, db server, webservice server, remote debug.
---

# Remote Hosts - Remote Server Access for Claude

Allows Claude to connect to predefined remote hosts and run commands without needing credentials repeated each time.

## Quick Start

```bash
# List configured hosts
rhost list

# Run a command on a host
rhost exec <host-id> "command"

# Interactive shell (for user, not Claude)
rhost shell <host-id>

# Check host connectivity
rhost ping <host-id>

# View recent logs
rhost logs <host-id> [service]

# Database access (credentials from keychain)
rhost cred list                                    # List stored credentials
rhost cred set <host-id> mysql <username>          # Store MySQL password (interactive)
rhost mysql <host-id> --user <user> --query "SQL"  # Run MySQL query
```

## Host Configuration

Hosts are stored in `~/.remote-hosts/hosts.yaml`:

```yaml
hosts:
  ppe-db:
    hostname: 10.0.0.50
    user: admin
    key: ~/.ssh/ppe-access-2025
    description: "PPE environment database server"
    environment: ppe

  ppe-web:
    hostname: 10.0.0.51
    user: admin
    key: ~/.ssh/ppe-access-2025
    description: "PPE webservice server (container host)"
    environment: ppe
    docker: true  # Has docker installed
```

## CLI Reference

### Host Management

```bash
# Add a host
rhost add <host-id> --hostname <ip> --user <user> --key <path>
  --description "description"
  --environment dev|ppe|prod
  --docker                    # Mark as docker host

# List all hosts
rhost list
  --environment <env>         # Filter by environment

# Show host details
rhost show <host-id>

# Remove a host
rhost remove <host-id>

# Test connectivity
rhost ping <host-id>
```

### Remote Execution

```bash
# Run a command
rhost exec <host-id> "command"
  --timeout 30                # Command timeout in seconds

# Run command with sudo
rhost exec <host-id> --sudo "command"

# Get a file
rhost get <host-id> <remote-path> [local-path]

# Put a file
rhost put <host-id> <local-path> <remote-path>
```

### Docker Commands (for docker hosts)

```bash
# List containers
rhost docker <host-id> ps

# View container logs
rhost docker <host-id> logs <container>
  --tail 100
  --follow

# Exec into container
rhost docker <host-id> exec <container> "command"

# Restart container
rhost docker <host-id> restart <container>
```

### Logs & Debugging

```bash
# View system logs
rhost logs <host-id>
  --service <name>            # journalctl -u <service>
  --tail 100
  --since "1 hour ago"

# Check disk space
rhost df <host-id>

# Check memory
rhost free <host-id>

# Check processes
rhost top <host-id>
```

### Credential Management (macOS Keychain)

Store service credentials securely in the macOS Keychain for database access and other services.

```bash
# Store credentials (prompts for password)
rhost cred set <host-id> <service> <username>

# Examples:
rhost cred set ppe-db mysql vlink_admin
rhost cred set ppe-db postgres dbuser

# List all stored credentials
rhost cred list

# Delete credentials
rhost cred delete <host-id> <service> <username>
```

Credentials are stored in macOS Keychain with the format `{host-id}:{service}:{username}`.

### MySQL Commands

Run MySQL queries on remote hosts using credentials from the Keychain.

```bash
# Run a query (uses credentials from keychain)
rhost mysql <host-id> --user <username> --query "SQL"
  --database <db>             # Optional database name
  --timeout 60                # Query timeout

# Examples:
rhost mysql ppe-db --user vlink_admin --query "SHOW DATABASES"
rhost mysql ppe-db --user vlink_admin --database mydb --query "SELECT * FROM users LIMIT 5"
```

**Setup workflow:**
```bash
# 1. Store credentials first (one-time)
rhost cred set ppe-db mysql vlink_admin
# (prompts for password, stores in keychain)

# 2. Run queries (uses stored credentials)
rhost mysql ppe-db --user vlink_admin --query "SHOW TABLES"
```

If credentials are not found, you'll see:
```
No MySQL credentials found for vlink_admin on ppe-db.
Store them with: rhost cred set ppe-db mysql vlink_admin
```

## Environment Tags

Hosts can be tagged with environments for organization:
- `dev` - Development servers
- `ppe` - Pre-production/staging
- `prod` - Production (commands require confirmation)

## Security Notes

1. **SSH keys stay local** - Only key paths are stored in config, not key contents
2. **Service credentials in Keychain** - MySQL/database passwords stored securely in macOS Keychain (not in files)
3. **Prod safeguards** - Production hosts require confirmation for destructive commands
4. **Audit trail** - Commands are logged to `~/.remote-hosts/history.log`

## For Claude

When debugging remote issues:
1. Use `rhost ping` first to verify connectivity
2. Use `rhost exec` to run diagnostic commands
3. For docker hosts, use `rhost docker logs` to check container logs
4. Check `rhost df` and `rhost free` for resource issues

**For database queries:**
1. First check if credentials exist: `rhost cred list`
2. If credentials exist for the host/service/user, use: `rhost mysql <host-id> --user <user> --query "SQL"`
3. If credentials don't exist, tell the user to run `rhost cred set <host-id> mysql <username>` in their terminal (requires interactive password input)
4. **NEVER** extract credentials from container environment variables or other sources - always use the keychain

**Important:** The `rhost cred set` command requires interactive terminal input for the password. Claude cannot run this directly - the user must run it themselves.
