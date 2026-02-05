---
name: memory-cli-ops
description: Execute and troubleshoot memory-cli commands for episode management, pattern analysis, and storage operations. Use this skill when running CLI commands, debugging CLI issues, explaining command usage, or guiding users through CLI workflows.
---

# Memory CLI Operations

Execute and troubleshoot the memory-cli command-line interface for the self-learning memory system.

## When to Use

- Running memory-cli commands for episode or pattern management
- Debugging CLI command failures
- Understanding CLI command syntax and options
- Guiding users through CLI workflows
- Troubleshooting storage synchronization
- Explaining CLI output formats

## CLI Overview

The memory-cli provides a comprehensive interface for managing episodic memory, patterns, and storage.

**Location**: `./target/release/memory-cli`
**Aliases**: Many commands have short aliases (shown below)
**Output Formats**: human (default), json, yaml

## Global Options

```bash
memory-cli [OPTIONS] <COMMAND>

Options:
  -c, --config <FILE>    Configuration file path
  -f, --format <FORMAT>  Output format (human|json|yaml) [default: human]
  -v, --verbose          Enable verbose output
  --dry-run              Show what would be done without executing
```

## Commands Overview

| Command | Alias | Purpose |
|---------|-------|---------|
| episode | ep    | Episode management |
| pattern | pat   | Pattern analysis |
| storage | st    | Storage operations |
| config  | cfg   | Configuration management |
| health  | hp    | Health monitoring |
| backup  | bak   | Backup and restore |
| monitor | mon   | Monitoring and metrics |
| logs    | log   | Log analysis |
| completion | comp | Shell completions |

## Episode Commands

### Create Episode

Start a new learning episode.

```bash
memory-cli episode create --task "implement async storage" [--context context.json]
# Alias
memory-cli ep create -t "implement async storage" [-c context.json]
```

**Options**:
- `-t, --task <TASK>`: Task description (required)
- `-c, --context <FILE>`: Context file in JSON format (optional)

**Output**: Episode ID and metadata

**Example**:
```bash
memory-cli ep create -t "debug authentication bug" -f json
```

### List Episodes

List episodes with optional filtering.

```bash
memory-cli episode list [OPTIONS]
# Alias
memory-cli ep list [OPTIONS]
```

**Options**:
- `-t, --task-type <TYPE>`: Filter by task type
- `-l, --limit <N>`: Maximum episodes to return [default: 10]
- `-s, --status <STATUS>`: Filter by status (active|completed|failed)

**Example**:
```bash
# List last 20 episodes
memory-cli ep list -l 20

# List only completed episodes
memory-cli ep list -s completed -l 50

# Get JSON output
memory-cli ep list -f json -l 5
```

### View Episode Details

View detailed information about a specific episode.

```bash
memory-cli episode view <EPISODE_ID>
# Alias
memory-cli ep view <EPISODE_ID>
```

**Output**: Complete episode data including steps, outcome, and patterns

**Example**:
```bash
memory-cli ep view ep_abc123xyz -f json
```

### Complete Episode

Mark an episode as complete with an outcome.

```bash
memory-cli episode complete <EPISODE_ID> <OUTCOME>
# Alias
memory-cli ep complete <EPISODE_ID> <OUTCOME>
```

**Outcomes**:
- `success`: Task completed successfully
- `partial`: Partially completed
- `failed`: Task failed

**Example**:
```bash
memory-cli ep complete ep_abc123xyz success
```

### Search Episodes

Search episodes by query.

```bash
memory-cli episode search <QUERY> [--limit <N>]
# Alias
memory-cli ep search <QUERY> [-l <N>]
```

**Example**:
```bash
memory-cli ep search "authentication" -l 10
```

### Log Execution Step

Log a step in an active episode.

```bash
memory-cli episode log-step <EPISODE_ID> [OPTIONS]
# Alias
memory-cli ep log-step <EPISODE_ID> [OPTIONS]
```

**Options**:
- `-t, --tool <TOOL>`: Tool name (required)
- `-a, --action <ACTION>`: Action description (required)
- `--success`: Whether step was successful (required)
- `--latency-ms <MS>`: Step latency in milliseconds
- `--tokens <N>`: Token count
- `-o, --observation <TEXT>`: Step observation

**Example**:
```bash
memory-cli ep log-step ep_abc123xyz \
  -t "compiler" \
  -a "build project" \
  --success \
  --latency-ms 1250 \
  -o "Build completed with 0 warnings"
```

## Pattern Commands

### List Patterns

List extracted patterns with filtering.

```bash
memory-cli pattern list [OPTIONS]
# Alias
memory-cli pat list [OPTIONS]
```

**Options**:
- `--min-confidence <FLOAT>`: Minimum confidence threshold [default: 0.0]
- `-p, --pattern-type <TYPE>`: Filter by pattern type
- `-l, --limit <N>`: Maximum patterns to return [default: 20]

**Pattern Types**:
- `tool-sequence`: Tool usage sequences
- `decision-point`: Decision patterns
- `error-recovery`: Error recovery strategies
- `context-pattern`: Context-based patterns

**Example**:
```bash
# List high-confidence patterns
memory-cli pat list --min-confidence 0.8 -l 10

# List error recovery patterns
memory-cli pat list -p error-recovery -l 5
```

### View Pattern Details

View detailed information about a specific pattern.

```bash
memory-cli pattern view <PATTERN_ID>
# Alias
memory-cli pat view <PATTERN_ID>
```

**Output**: Pattern metadata, confidence score, usage count, and examples

**Example**:
```bash
memory-cli pat view pat_xyz789abc -f json
```

### Analyze Pattern Effectiveness

Analyze how effective a pattern has been.

```bash
memory-cli pattern analyze <PATTERN_ID> [--episodes <N>]
# Alias
memory-cli pat analyze <PATTERN_ID> [-e <N>]
```

**Options**:
- `-e, --episodes <N>`: Number of episodes to analyze [default: 100]

**Output**: Success rate, usage frequency, and effectiveness metrics

**Example**:
```bash
memory-cli pat analyze pat_xyz789abc -e 200
```

### Pattern Effectiveness Rankings

Show top-performing patterns.

```bash
memory-cli pattern effectiveness [OPTIONS]
# Alias
memory-cli pat effectiveness [OPTIONS]
```

**Options**:
- `-t, --top <N>`: Show top N patterns [default: 10]
- `--min-uses <N>`: Minimum usage count [default: 1]

**Example**:
```bash
# Top 20 most effective patterns with at least 5 uses
memory-cli pat effectiveness -t 20 --min-uses 5
```

### Apply Pattern Decay

Apply time-based decay to pattern confidence scores.

```bash
memory-cli pattern decay [--dry-run] [--force]
# Alias
memory-cli pat decay [--dry-run] [--force]
```

**Options**:
- `--dry-run`: Show changes without applying
- `--force`: Skip confirmation prompt

**Example**:
```bash
# Preview decay
memory-cli pat decay --dry-run

# Apply decay
memory-cli pat decay --force
```

## Storage Commands

### Storage Statistics

Show comprehensive storage statistics.

```bash
memory-cli storage stats
# Alias
memory-cli st stats
```

**Output**:
- Episode count (total and recent)
- Pattern count (total and recent)
- Storage size
- Cache hit rate
- Last sync timestamp

**Example**:
```bash
memory-cli st stats -f json
```

### Synchronize Storage

Synchronize Turso (durable) and redb (cache) storage layers.

```bash
memory-cli storage sync [--force] [--dry-run]
# Alias
memory-cli st sync [--force] [--dry-run]
```

**Options**:
- `--force`: Force full synchronization
- `--dry-run`: Show what would be synchronized

**Use When**:
- Cache appears stale
- After database failures
- During periodic maintenance

**Example**:
```bash
# Preview sync
memory-cli st sync --dry-run

# Force full sync
memory-cli st sync --force
```

### Vacuum Storage

Optimize and compact storage files.

```bash
memory-cli storage vacuum [--dry-run]
# Alias
memory-cli st vacuum [--dry-run]
```

**Example**:
```bash
memory-cli st vacuum
```

### Storage Health Check

Check storage layer health.

```bash
memory-cli storage health
# Alias
memory-cli st health
```

**Output**: Health status for both Turso and redb layers

### Storage Connections

Show active storage connections.

```bash
memory-cli storage connections
# Alias
memory-cli st connections
```

## Configuration Commands

### Validate Configuration

Validate configuration file.

```bash
memory-cli config validate [--config <FILE>]
# Alias
memory-cli cfg validate [-c <FILE>]
```

### Show Configuration

Display current configuration.

```bash
memory-cli config show
# Alias
memory-cli cfg show
```

## Health Commands

### System Health Check

Check overall system health.

```bash
memory-cli health check
# Alias
memory-cli hp check
```

### Health Status

Show detailed health status.

```bash
memory-cli health status
# Alias
memory-cli hp status
```

## Backup Commands

### Create Backup

Create a backup of the memory system.

```bash
memory-cli backup create [--output <PATH>]
# Alias
memory-cli bak create [-o <PATH>]
```

### Restore Backup

Restore from a backup.

```bash
memory-cli backup restore <BACKUP_FILE>
# Alias
memory-cli bak restore <BACKUP_FILE>
```

### List Backups

List available backups.

```bash
memory-cli backup list
# Alias
memory-cli bak list
```

## Monitor Commands

### Show Metrics

Display monitoring metrics.

```bash
memory-cli monitor metrics
# Alias
memory-cli mon metrics
```

### Live Monitoring

Start live monitoring dashboard.

```bash
memory-cli monitor live
# Alias
memory-cli mon live
```

## Logs Commands

### Search Logs

Search system logs.

```bash
memory-cli logs search <QUERY> [--limit <N>]
# Alias
memory-cli log search <QUERY> [-l <N>]
```

### Tail Logs

Follow logs in real-time.

```bash
memory-cli logs tail [--follow]
# Alias
memory-cli log tail [-f]
```

## Shell Completion

Generate shell completion scripts.

```bash
memory-cli completion <SHELL>

# Examples:
memory-cli completion bash > ~/.memory-cli-completion.bash
memory-cli completion zsh > ~/.zsh/completions/_memory-cli
memory-cli completion fish > ~/.config/fish/completions/memory-cli.fish
```

## Environment Variables

The CLI uses these environment variables:

- **TURSO_DATABASE_URL**: Primary database URL
- **LOCAL_DATABASE_URL**: Local SQLite database URL
- **REDB_CACHE_PATH**: Path to redb cache file
- **RUST_LOG**: Logging level (off, error, warn, info, debug, trace)

## Configuration File

The CLI can use a configuration file in JSON or YAML format:

```json
{
  "database": {
    "turso_url": "file:./data/memory.db",
    "local_url": "sqlite:./data/memory.db",
    "cache_path": "./data/cache.redb"
  },
  "cache": {
    "max_size": 1000,
    "ttl_seconds": 1800
  },
  "output": {
    "default_format": "human",
    "color": true
  }
}
```

Use with: `memory-cli --config config.json <command>`

## Common Workflows

### Track a Task End-to-End

```bash
# 1. Create episode
EPISODE_ID=$(memory-cli ep create -t "implement feature X" -f json | jq -r '.episode_id')

# 2. Log steps as you work
memory-cli ep log-step $EPISODE_ID -t "editor" -a "write code" --success --latency-ms 5000
memory-cli ep log-step $EPISODE_ID -t "compiler" -a "build" --success --latency-ms 1200
memory-cli ep log-step $EPISODE_ID -t "test-runner" -a "run tests" --success --latency-ms 3500

# 3. Complete episode
memory-cli ep complete $EPISODE_ID success

# 4. View results
memory-cli ep view $EPISODE_ID
```

### Analyze Performance Patterns

```bash
# 1. List patterns by effectiveness
memory-cli pat effectiveness -t 10

# 2. Analyze specific pattern
memory-cli pat analyze pat_abc123 -e 100

# 3. Check storage stats
memory-cli st stats
```

### Maintenance Workflow

```bash
# 1. Check health
memory-cli hp check

# 2. Check storage
memory-cli st health

# 3. Sync if needed
memory-cli st sync --dry-run
memory-cli st sync --force

# 4. Vacuum to optimize
memory-cli st vacuum

# 5. Create backup
memory-cli bak create -o ./backups/$(date +%Y%m%d).db
```

## Troubleshooting

### Common Issues

#### CLI Not Found

**Symptoms**: `command not found: memory-cli`

**Solutions**:
```bash
# Build the CLI
cargo build --release --bin memory-cli

# Add to PATH
export PATH="$PATH:$(pwd)/target/release"

# Or use full path
./target/release/memory-cli --help
```

#### Database Connection Failed

**Symptoms**: `Error: Failed to connect to database`

**Checks**:
1. Database files exist: `ls -la ./data/`
2. Environment variables set: `env | grep -E '(TURSO|LOCAL)'`
3. Permissions: `ls -la ./data/*.db`

**Solutions**:
```bash
# Create data directory
mkdir -p ./data

# Set environment variables
export TURSO_DATABASE_URL="file:./data/memory.db"
export LOCAL_DATABASE_URL="sqlite:./data/memory.db"
export REDB_CACHE_PATH="./data/cache.redb"

# Test connection
memory-cli st health
```

#### Command Fails Silently

**Symptoms**: Command returns no output or error

**Solutions**:
```bash
# Enable verbose mode
memory-cli -v <command>

# Enable debug logging
RUST_LOG=debug memory-cli <command>

# Check JSON output
memory-cli -f json <command>
```

#### Cache Appears Stale

**Symptoms**: Old data returned, inconsistent results

**Solutions**:
```bash
# Check storage stats
memory-cli st stats

# Sync storage layers
memory-cli st sync --force

# Check health after sync
memory-cli st health
```

#### Invalid JSON Output

**Symptoms**: JSON parsing errors, malformed output

**Solutions**:
```bash
# Verify format flag
memory-cli -f json <command> | jq .

# Check for stderr mixed with stdout
memory-cli -f json <command> 2>/dev/null | jq .

# Disable color in JSON mode
NO_COLOR=1 memory-cli -f json <command>
```

## Best Practices

### Command Usage

✓ **DO**:
- Use aliases for faster typing (ep, pat, st, etc.)
- Specify output format (-f json) for scripting
- Use --dry-run before destructive operations
- Log steps frequently during long tasks
- Complete episodes promptly after tasks
- Check storage health periodically

✗ **DON'T**:
- Forget to complete episodes (leaves them orphaned)
- Skip --dry-run on sync/vacuum operations
- Ignore health check warnings
- Use default limits for large datasets
- Run without environment variables set

### Scripting

✓ **DO**:
```bash
# Use JSON output for parsing
RESULT=$(memory-cli ep create -t "task" -f json)
EPISODE_ID=$(echo "$RESULT" | jq -r '.episode_id')

# Check exit codes
if ! memory-cli st sync --force; then
  echo "Sync failed!"
  exit 1
fi

# Use verbose mode for debugging
if [[ "$DEBUG" == "1" ]]; then
  memory-cli -v ep list
fi
```

✗ **DON'T**:
```bash
# Parse human-readable output
EPISODE_ID=$(memory-cli ep create -t "task" | grep -oP 'ID: \K\w+')

# Ignore failures
memory-cli st sync --force
# continue without checking...

# Mix output formats
memory-cli -f json ep list | grep "completed"
```

### Output Formats

**Human** (default):
- ✓ Interactive use
- ✓ Reading results
- ✗ Scripting
- ✗ Parsing

**JSON**:
- ✓ Scripting
- ✓ Parsing with jq
- ✓ API integration
- ✗ Human reading

**YAML**:
- ✓ Configuration
- ✓ Human reading
- ✗ Scripting (less common)

## Integration Examples

### CI/CD Pipeline

```bash
#!/bin/bash
# Track deployment episode
set -e

EPISODE_ID=$(memory-cli ep create -t "deploy to production" -f json | jq -r '.episode_id')

# Log steps
memory-cli ep log-step $EPISODE_ID -t "docker" -a "build image" --success
memory-cli ep log-step $EPISODE_ID -t "kubectl" -a "apply manifests" --success
memory-cli ep log-step $EPISODE_ID -t "smoke-test" -a "health check" --success

# Complete
memory-cli ep complete $EPISODE_ID success
```

### Monitoring Script

```bash
#!/bin/bash
# Daily health check
memory-cli hp check -f json > /var/log/memory-health.json
memory-cli st stats -f json > /var/log/memory-stats.json

# Alert if unhealthy
if ! memory-cli hp check; then
  echo "Health check failed!" | mail -s "Memory System Alert" admin@example.com
fi
```

### Backup Automation

```bash
#!/bin/bash
# Weekly backup
BACKUP_FILE="./backups/memory-$(date +%Y%m%d-%H%M%S).db"
memory-cli bak create -o "$BACKUP_FILE"

# Keep last 4 weeks
find ./backups -name "memory-*.db" -mtime +28 -delete
```

## Related Resources

- **CLI Source**: `memory-cli/src/`
- **Command Implementations**: `memory-cli/src/commands/`
- **Configuration**: `memory-cli/src/config.rs`
- **Project Guide**: `AGENTS.md`

## Summary

The memory-cli-ops skill helps you:
- ✓ Execute all CLI commands correctly
- ✓ Understand command options and output
- ✓ Troubleshoot common CLI issues
- ✓ Integrate CLI into scripts and workflows
- ✓ Follow best practices for episode tracking
- ✓ Maintain storage health

Use aliases, check output with --dry-run, and always complete episodes!
