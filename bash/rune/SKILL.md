---
name: rune
version: 1.1.5
description: Self-improving AI memory system with intelligent context injection and adaptive learning
keywords: [self-improvement, intelligent-memory, adaptive, context-injection, project-management]
homepage: https://github.com/TheBobLoblaw/rune
metadata: {"install":[{"id":"rune","kind":"script","script":"./install.sh","label":"Install Rune Memory System"}],"minis":{"originalSource":"https://clawskills.sh/skills/thebobloblaw-rune","convertedAt":"2026-10-31T22:13:41.697Z","license":"Unknown"}}
---

# Rune - Persistent AI Memory System

**Rune** gives your OpenClaw agent persistent, intelligent memory that gets better over time. No more burning tokens on static context files or forgetting important information between sessions.

## What Rune Does

### 🧠 Smart Memory Management
- **Dynamic Context Injection**: AI selects only relevant facts for each conversation  
- **Access Pattern Learning**: Frequently used facts get prioritized
- **Forgetting Curves**: Unused facts naturally fade like human memory
- **Memory Consolidation**: Similar facts get merged, verbose ones compressed

### 🎯 Session Intelligence  
- **Interaction Style Detection**: Learns if you prefer brainstorm vs deep-work vs debug modes
- **Behavioral Pattern Analysis**: Tracks your work patterns and preferences over time
- **Proactive Memory**: Volunteers relevant context unprompted ("last time you worked on this...")

### 📋 Project Autopilot
- **Smart Task Recommendations**: "What should I work on next?" with priority scoring
- **Blocker Detection**: Identifies stuck projects that need intervention  
- **Project Health Scoring**: 0.0-1.0 health scores based on activity and progress

### 📢 Intelligent Notifications
- **Priority Classification**: Critical/High/Medium/Low/FYI with context analysis
- **Smart Timing**: Respects quiet hours, batches low-priority updates
- **Channel Routing**: DM for urgent, Discord for projects, digest for FYI

### 🔄 Self-Improvement Loop
- **Pattern Detection**: "Forgot to use X skill 3 times" → automatic escalation
- **Performance Tracking**: Measurable improvement over time
- **Skill Usage Analysis**: Which skills you use vs neglect

## About Rune vs rune

**Rune** is the OpenClaw skill name. **rune** is the CLI tool name. Think of Rune as the "skill package" and rune as the "command-line interface" - like how the `git` skill package provides the `git` CLI.

- **Skill name**: `rune` (what you install via ClawHub)  
- **CLI command**: `rune` (what you run in terminal)
- **Repository**: https://github.com/TheBobLoblaw/rune

## Installation Disclosure

**⚠️ What This Installation Does:**

The Rune skill installation will:
- **Create directories**: `~/.openclaw/` and subdirectories
- **Install globally**: `rune` CLI via npm (requires npm dependencies)
- **Create database**: SQLite database at `~/.openclaw/memory.db`
- **Modify files**: Appends integration lines to existing `~/.openclaw/workspace/HEARTBEAT.md`
- **Add session hooks**: Automatic memory integration for OpenClaw sessions

**Before installing:**
- **Back up** `HEARTBEAT.md` if it contains important data
- **Review** `package.json` dependencies if security is critical
- **Consider** using local models (Ollama) instead of cloud APIs for privacy

## Installation

```bash
# Via ClawHub (recommended)
clawhub install rune

# Manual installation
git clone https://github.com/TheBobLoblaw/rune
cd rune
npm install --production
npm install -g .
```

## Quick Start

```bash
# Initialize memory system
rune stats

# Add your first fact
rune add person cory.name "Cory - my human user"

# Generate context for a conversation  
rune context "Let's work on the website"

# Get task recommendations
rune next-task

# Weekly self-review
rune self-review --days 7
```

## Core Commands

### Memory Management
- `rune add <category> <key> <value>` - Store a fact
- `rune search <query>` - Find facts
- `rune recall <topic>` - Smart multi-source recall  
- `rune inject` - Generate context file for agent

### Intelligence Features  
- `rune context <message>` - Dynamic context for message
- `rune score <message>` - Relevance scoring  
- `rune proactive <message>` - Volunteer relevant context
- `rune session-style <message>` - Detect interaction style

### Project Management
- `rune project-state <name>` - Track project phases/blockers
- `rune next-task` - Smart task picker
- `rune stuck-projects` - Find blocked work

### Advanced Features
- `rune temporal "last Tuesday"` - Time-based queries  
- `rune consolidate` - Memory optimization
- `rune forget` - Apply forgetting curves
- `rune pattern-analysis` - Detect behavioral patterns

## Integration with OpenClaw

### Heartbeat Integration
Add to your `HEARTBEAT.md`:

```bash
# Memory maintenance
rune expire && rune inject --output ~/.openclaw/workspace/FACTS.md

# Proactive work selection
NEXT_TASK=$(rune next-task --json)
if [[ "$NEXT_TASK" != "null" ]]; then
  # Work on the recommended task
fi
```

### Session Hooks
The skill automatically provides secure session hooks via OpenClaw integrations.

For manual usage, use the secure session handler:

```bash
# Secure session hooks (input sanitized automatically)
./rune-session-handler.sh start   # Loads dynamic context safely
./rune-session-handler.sh end     # Tracks session style safely

# Direct usage (SECURE - input is sanitized):
SAFE_MESSAGE=$(echo "$MESSAGE" | head -c 200 | tr -d '`$(){}[]|;&<>' | sed 's/[^a-zA-Z0-9 ._-]//g')
rune recall "$SAFE_MESSAGE" --limit 10
```

⚠️ **Security Note**: Never pass unsanitized user input directly to shell commands. Always use the provided session handler or sanitize input manually.

## Architecture

- **SQLite Database**: All memory stored in `~/.openclaw/memory.db`
- **Local LLM Integration**: Ollama for relevance scoring and extraction
- **Cloud API Support**: Anthropic, OpenAI for advanced reasoning
- **Local-First Design**: Works completely offline with Ollama (cloud APIs optional for advanced features)

## Memory Categories

- **person**: Information about people (names, roles, preferences)
- **project**: Project status, phases, decisions
- **tool**: How to use tools and their quirks  
- **lesson**: Mistakes to avoid, best practices
- **decision**: Why certain choices were made
- **preference**: User likes/dislikes, settings
- **environment**: System configs, non-sensitive settings (⚠️ NEVER store credentials!)

## ⚠️ Security & Privacy

### Data Storage
**What Rune Stores:**
- Facts you explicitly add via `rune add`
- Session interaction patterns for learning (conversation style, not content)
- Project states and task recommendations

**What Rune Does NOT Store (by default):**
- Full conversation transcripts (unless you run `extract` manually)
- API keys or credentials (use environment variables instead)
- Sensitive personal information (unless you explicitly add it)

### Installation Security
**NPM Dependencies:**
- Installation fetches dependencies from npm registry at install time
- Review `package.json` for dependencies if security is critical
- Global npm install runs lifecycle scripts (standard npm behavior)
- Consider installing in isolated environment (container/VM) for high-security use

**Session Security:**
- **Fixed CVE-2026-0001**: Input sanitization prevents shell injection
- All user input sanitized before shell execution
- Session handler validates and limits input length

### Cloud API Usage
- **Optional**: Rune can use OpenAI/Anthropic APIs for fact extraction and scoring
- **Local-first**: Works completely offline with Ollama (recommended for privacy)
- **Your choice**: Configure which engines to use in your setup

### Privacy Recommendations
- **Use local models** (Ollama) for maximum privacy
- **Avoid cloud APIs** if processing sensitive information
- **Review stored facts** periodically with `rune search`
- **Never store credentials** in memory - use environment variables

**Privacy Best Practices:**
- Never run `rune add` with sensitive data (passwords, API keys, personal info)
- Use `rune extract` carefully - review files before extracting facts
- Configure Ollama for local-only operation if you want zero cloud usage
- Review your `~/.openclaw/workspace/FACTS.md` periodically

**Installation Changes:**
- Adds memory maintenance commands to `HEARTBEAT.md` (if present)
- Creates `~/.openclaw/memory.db` database file
- Session hooks may process conversation metadata (not full content) for learning

## Performance Metrics

With Rune, your agent will:
- ✅ Remember context between sessions without burning tokens
- ✅ Pick relevant facts dynamically vs dumping everything
- ✅ Get measurably better at avoiding repeated mistakes  
- ✅ Work autonomously on projects between check-ins
- ✅ Learn your interaction patterns and adapt responses

## Advanced Configuration

```bash
# Tune relevance scoring
rune score "your query" --threshold 0.6 --model llama3.1:8b

# Configure forgetting curves  
rune forget --decay-rate 0.03 --grace-days 45

# Cross-session pattern analysis
rune cross-session --days 90 --min-sessions 5
```

## Automated Maintenance & Performance

Rune performs best with regular maintenance. Here are automation strategies:

### Cron Job Setup

**Daily Maintenance (3 AM)**
```bash
# Expire working memory and regenerate context
0 3 * * * /usr/local/bin/rune expire && /usr/local/bin/rune inject --output ~/.openclaw/workspace/FACTS.md
```

**Weekly Optimization (Sunday 2 AM)**  
```bash
# Consolidate memory and run self-review
0 2 * * 0 /usr/local/bin/rune consolidate --auto-prioritize && /usr/local/bin/rune self-review --days 7
```

**Monthly Deep Clean (1st of month, 1 AM)**
```bash
# Pattern analysis and database optimization
0 1 1 * * /usr/local/bin/rune pattern-analysis --days 30 && sqlite3 ~/.openclaw/memory.db "VACUUM; ANALYZE;"
```

### Database Backup
```bash
# Daily backup at 4 AM
0 4 * * * cp ~/.openclaw/memory.db ~/.openclaw/memory.db.backup.$(date +\%Y\%m\%d)
# Keep last 7 days
5 4 * * * find ~/.openclaw -name "memory.db.backup.*" -mtime +7 -delete
```

### Performance Benefits
- **🧹 Memory stays lean**: Auto-removes expired facts
- **⚡ Faster queries**: Regular consolidation prevents bloat
- **📈 Self-improvement**: Pattern detection catches recurring issues  
- **🔄 Current context**: FACTS.md regenerated with latest data
- **💾 Data protection**: Automated backups prevent loss

### Memory Health Monitoring
```bash
# Check database size and fact count
rune stats

# Review recent patterns
rune pattern-analysis --days 7

# Check consolidation opportunities  
rune consolidate --dry-run
```

## Troubleshooting

**Memory growing too large?**
- Run `rune consolidate` to merge similar facts
- Use `rune forget` to apply forgetting curves  
- Check `rune stats` for database size

**Relevance scoring not working?**
- Ensure Ollama is running: `systemctl status ollama`
- Test model: `rune score "test" --engine ollama`
- Fall back to anthropic/openai engines

**Context injection too verbose?**
- Lower relevance threshold: `--threshold 0.6`  
- Use token budgeting: `rune budget "query" --tokens 300`

## Contributing

Rune is open source. Contributions welcome:
- **Memory Science**: Better consolidation algorithms, forgetting curves
- **LLM Integration**: New scoring engines, extraction methods
- **UI/UX**: Better command interfaces, visualization tools
- **Performance**: Speed optimizations, memory efficiency

## License

MIT License - Use freely, modify as needed.

---

*Rune: Because your AI should remember like you do.*
