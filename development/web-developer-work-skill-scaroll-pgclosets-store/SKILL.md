---
name: web-developer-work-skill
description: Persistent context management system for web developers that never loses work between Claude Desktop sessions. Features automatic context backup, work session continuity, project state management, and comprehensive error recovery.
version: 1.0.0
author: Claude Code Assistant
license: MIT
tags: [web-development, context-persistence, session-management, work-continuity]
---

# Web Developer Work Skill

A comprehensive persistent context management system designed specifically for web developers using Claude Desktop. This skill ensures you never lose work context between sessions, providing seamless continuity and intelligent work state management.

## Core Features

### 🔄 Persistent Context Storage
- **Automatic Context Backup**: Real-time saving of work context, files, and progress
- **Session Continuity**: Seamlessly resume work exactly where you left off
- **Project State Management**: Track project structure, dependencies, and configuration
- **Work History**: Complete audit trail of all development activities

### 💾 Intelligent Storage System
- **File-Based Memory**: Robust JSON-based storage with automatic versioning
- **Incremental Backups**: Efficient storage that only saves changes
- **Cross-Session Sync**: Maintains context across different Claude Desktop instances
- **Data Recovery**: Automatic recovery from unexpected interruptions

### 🛠️ CLI Integration
- **Claude Desktop Native**: Full integration with Claude Desktop CLI
- **Command Shortcuts**: Quick commands for common operations
- **Status Monitoring**: Real-time visibility into work session state
- **Easy Setup**: One-command initialization for new projects

### 🚨 Error Handling & Recovery
- **Graceful Degradation**: System continues working even if components fail
- **Automatic Recovery**: Self-healing mechanisms for common issues
- **Data Integrity**: Validation and checksums to prevent corruption
- **Rollback System**: Restore previous work states if needed

## Quick Start

### Installation
```bash
# Clone or create the skill in your skills directory
mkdir -p ~/.claude/skills
cp -r web-developer-work-skill ~/.claude/skills/
```

### Initial Setup
```bash
# Initialize in your project directory
cd your-project
claude skill web-developer-work-skill --init

# This will:
# - Create .claude-work/ directory structure
# - Initialize context storage
# - Set up automatic backup system
# - Configure project-specific settings
```

### Basic Usage
```bash
# Start a work session
claude skill web-developer-work-skill --start-session "Feature Development"

# Save current context
claude skill web-developer-work-skill --save-context

# Resume previous session
claude skill web-developer-work-skill --resume-session

# View work history
claude skill web-developer-work-skill --history

# Backup current state
claude skill web-developer-work-skill --backup
```

## Architecture

### Storage Structure
```
.claude-work/
├── sessions/
│   ├── active-session.json
│   ├── session-history/
│   └── session-backups/
├── context/
│   ├── current-context.json
│   ├── context-history/
│   └── context-snapshots/
├── projects/
│   ├── project-state.json
│   ├── file-changes.json
│   └── dependency-tracking.json
├── backups/
│   ├── automatic/
│   ├── manual/
│   └── recovery-points/
└── config/
    ├── settings.json
    ├── preferences.json
    └── ignore-rules.json
```

### Core Components

#### 1. Context Manager
- Manages current work context and session state
- Handles automatic context saving and loading
- Provides intelligent context reconstruction

#### 2. Storage Engine
- Reliable file-based storage with JSON format
- Incremental updates for performance optimization
- Data validation and integrity checks

#### 3. Session Manager
- Tracks work sessions with start/end times
- Maintains session history and metadata
- Handles session recovery and restoration

#### 4. CLI Interface
- Command-line interface for Claude Desktop integration
- Provides shortcuts for common operations
- Status reporting and monitoring

## Configuration

### Settings (.claude-work/config/settings.json)
```json
{
  "autoSave": {
    "enabled": true,
    "interval": 30000,
    "onFileChange": true,
    "onCommand": true
  },
  "backup": {
    "enabled": true,
    "frequency": "hourly",
    "maxBackups": 50,
    "compression": true
  },
  "session": {
    "timeout": 1800000,
    "autoResume": true,
    "trackActivity": true
  },
  "context": {
    "maxContextSize": 1000000,
    "compressionThreshold": 100000,
    "retentionDays": 30
  }
}
```

### Ignore Rules (.claude-work/config/ignore-rules.json)
```json
{
  "files": [
    "node_modules/**",
    ".git/**",
    "dist/**",
    "build/**",
    "*.log",
    ".env*"
  ],
  "patterns": [
    "*.tmp",
    "*.cache",
    "__pycache__/**"
  ]
}
```

## API Reference

### Core Functions

#### `initialize(config)`
Initialize the work skill system with custom configuration.

#### `startSession(name, metadata)`
Start a new work session with optional metadata.

#### `saveContext(context, options)`
Save current work context with various options.

#### `loadContext(sessionId)`
Load context from a specific session.

#### `createBackup(type, description)`
Create manual or automatic backups.

#### `restoreFromBackup(backupId)`
Restore work state from a backup.

#### `getSessionHistory(limit, filter)`
Get paginated session history with filtering options.

#### `searchHistory(query, options)`
Search through work history and context.

## Error Handling

### Automatic Recovery
- **Storage Failures**: Automatic retry with fallback storage locations
- **Data Corruption**: Restore from last known good state
- **Session Interruption**: Automatic session recovery on restart
- **Memory Issues**: Intelligent context compression and cleanup

### Manual Recovery
```bash
# Check system status
claude skill web-developer-work-skill --status

# Repair corrupted data
claude skill web-developer-work-skill --repair

# Restore from backup
claude skill web-developer-work-skill --restore-backup <backup-id>

# Reset to safe state
claude skill web-developer-work-skill --reset-safe
```

## Best Practices

### 1. Regular Backups
- Enable automatic backups
- Create manual checkpoints before major changes
- Verify backup integrity regularly

### 2. Context Management
- Keep context focused and relevant
- Use session names that describe your work
- Review and clean up old sessions periodically

### 3. Performance Optimization
- Configure appropriate backup frequency
- Use ignore rules to exclude unnecessary files
- Monitor storage usage and cleanup regularly

### 4. Security
- Don't store sensitive information in context
- Use environment-specific configurations
- Regular backup rotation and cleanup

## Troubleshooting

### Common Issues

#### "Context not loading"
- Check file permissions
- Verify storage directory integrity
- Run `--repair` command

#### "Backup failed"
- Check available disk space
- Verify write permissions
- Check backup configuration

#### "Session lost"
- Check session history
- Look for automatic backups
- Use `--recover-lost-session` command

### Debug Mode
```bash
# Enable debug logging
claude skill web-developer-work-skill --debug

# Verbose output
claude skill web-developer-work-skill --verbose

# Check system health
claude skill web-developer-work-skill --health-check
```

## Integration with Claude Desktop

### Native Commands
The skill integrates directly with Claude Desktop CLI:

```bash
# Start Claude Desktop with persistent context
claude --with-context web-developer-work-skill

# Resume last session automatically
claude --resume-session

# Work with specific project context
claude --project-context ./my-project
```

### Context Awareness
- Automatic project detection
- Intelligent file tracking
- Context-aware suggestions
- Seamless workflow integration

## Development

### Extending the Skill
```bash
# Development setup
cd web-developer-work-skill
npm install
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues, questions, or contributions:
- Check the troubleshooting section
- Review the API documentation
- Create an issue in the repository
- Join the community discussions

---

**Never lose your work context again with Web Developer Work Skill - Your persistent development companion.**