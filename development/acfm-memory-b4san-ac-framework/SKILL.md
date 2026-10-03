---
name: acfm-memory
description: Autonomous memory system for persistent learning across sessions. Automatically saves architectural decisions, bugfixes, patterns, and insights. Use to recall context from previous work and build institutional knowledge.
---

# AC Framework Memory System

## Overview

The AC Framework Memory System provides **autonomous persistent memory** for AI agents. It automatically detects and saves valuable knowledge during development, then recalls relevant context when needed.

**Key Capabilities:**
- **Automatic saving**: Detects and stores important decisions, patterns, and solutions
- **Full-text search**: Find relevant memories instantly
- **Context recall**: Get relevant knowledge before starting tasks
- **Pattern analysis**: Detect recurring themes and errors
- **Timeline view**: See chronological context around any memory

## When to Use This Skill

### Before Starting Work
- **Recall relevant context**: `acfm memory recall "<task description>"`
- **Check for similar changes**: `acfm memory search "<topic>"`
- **Review patterns**: `acfm memory patterns`

### During Work (Automatic)
The agent automatically saves memories when:
- Completing architectural proposals
- Fixing bugs (especially after multiple attempts)
- Refactoring code successfully
- Optimizing performance
- Discovering important patterns

### After Work
- **Review learnings**: `acfm memory stats`
- **Export for sharing**: `acfm memory export team-memory.json`
- **Find gaps**: `acfm memory patterns --min-frequency 1`

## Memory Types

| Type | Description | Auto-Trigger |
|------|-------------|--------------|
| `architectural_decision` | Major design decisions | After proposal/design |
| `bugfix_pattern` | Solutions to bugs | After fixing error |
| `refactor_technique` | Successful refactoring patterns | After refactor |
| `performance_insight` | Optimization learnings | After performance work |
| `security_fix` | Security vulnerability fixes | After security patch |
| `api_pattern` | API design patterns | After API work |
| `convention` | Project conventions | After establishing pattern |
| `workaround` | Temporary solutions | After implementing hack |
| `context_boundary` | System limitations | After defining boundaries |

## Commands

### Core Commands

#### Initialize Memory System
```bash
acfm memory init
```
Creates the SQLite database at `~/.acfm/memory.db`.

#### Save Memory (Manual)
```bash
acfm memory save "Descripción de la decisión o patrón" \
  --type architectural_decision \
  --importance high \
  --tags "react,performance"
```

#### Recall Context
```bash
# For specific task
acfm memory recall "implementing authentication"

# For current project (general context)
acfm memory recall
```

#### Search Memories
```bash
# Basic search
acfm memory search "JWT"

# Filtered search
acfm memory search "database" --type architectural_decision --importance high
```

### Advanced Commands

#### Timeline View
```bash
acfm memory timeline <memory-id>
```
Shows what happened before and after a specific memory.

#### Connections
```bash
acfm memory connections <memory-id> --depth 2
```
Shows related memories as a graph.

#### Pattern Detection
```bash
acfm memory patterns
acfm memory patterns --type bugfix_pattern
```
Finds recurring topics and frequent error types.

#### Predictive Recall
```bash
acfm memory anticipate "caching strategy"
```
Predicts which memories will be relevant for a future task.

#### Statistics
```bash
acfm memory stats
acfm memory stats --project /path/to/project
```

#### Export/Import
```bash
# Export for sharing
acfm memory export team-memory.json

# Import shared knowledge
acfm memory import team-memory.json
```

## Auto-Save Behavior

### What Triggers Auto-Save

The agent evaluates content using a confidence score (0-1):

**High confidence triggers (auto-save):**
- Contains decision keywords: "decidimos", "optamos", "mejor usar"
- Describes solution to problem
- Contains architectural guidance
- Has error + solution pair
- Takes >10 minutes to resolve

**Low confidence (skip):**
- Very short content (<50 chars)
- Contains specific IDs/UUIDs
- Temporary TODOs
- Obvious/common knowledge

### Confidence Scoring

```
Base: 0.5
+ Decision keywords: +0.25
+ Contains solution: +0.20
+ Bug fix: +0.15
+ Architecture: +0.20
+ Optimization: +0.15
+ Security: +0.25
- Too short: -0.20
- Specific IDs: -0.15
- TODO/FIXME: -0.20

Threshold for auto-save: 0.60
```

### Notification

When auto-saving, the agent will display:
```
💾 Memory saved: [Brief description of what was learned]
   Type: bugfix_pattern | Confidence: 85%
```

## Privacy

Content between `<private>` tags is automatically redacted:

```markdown
Decidimos usar AWS para hosting. <private>Usaremos la cuenta
producción-env-123</private> para el deployment.
```

Saved as:
```
Decidimos usar AWS para hosting. [REDACTED PRIVATE CONTENT]
```

## Integration with Spec Workflow

### Before Creating Artifacts

When you request `acfm spec instructions`, the system automatically:

1. Queries memories related to the change topic
2. Includes relevant memories in the response
3. Displays them as context for the agent

Example output:
```json
{
  "instruction": "...",
  "relevantMemories": [
    {
      "id": 42,
      "type": "architectural_decision",
      "content": "Previous auth system used JWT...",
      "importance": "high"
    }
  ]
}
```

### During Apply Phase

When implementing tasks, the system recalls:
- Patterns from similar previous tasks
- Bugfixes related to current work
- Performance insights for optimization tasks

## Best Practices

### For Agents

1. **Always recall before starting**: Check `acfm memory recall` for relevant context
2. **Let auto-save work**: Don't manually save everything - trust the confidence scoring
3. **Use topic keys**: When manually saving, use consistent topic keys for deduplication
4. **Mark importance**: Critical decisions should be marked `critical` or `high`
5. **Add tags**: Tags improve searchability

### For Users

1. **Initialize once**: Run `acfm memory init` per machine
2. **Review periodically**: Check `acfm memory stats` to see what's been learned
3. **Export regularly**: Share knowledge with team via `acfm memory export`
4. **Prune old data**: Use `acfm memory prune` to archive obsolete memories
5. **Use private tags**: Mark sensitive content with `<private>` tags

## Examples

### Example 1: Bug Fix

**Agent fixes an authentication bug:**
```
💾 Memory saved: JWT refresh token fails when expired during request
   Type: bugfix_pattern | Confidence: 87%
   Solution: Implement token refresh interceptor
```

**Later, similar task:**
```bash
$ acfm memory recall "authentication token"
→ [Memory #42] JWT refresh token fails when expired...
```

### Example 2: Architectural Decision

**Agent completes proposal:**
```
💾 Memory saved: Microservices architecture chosen for scalability
   Type: architectural_decision | Confidence: 92%
   Tags: ["architecture", "microservices", "scalability"]
```

**Weeks later, new service:**
```bash
$ acfm memory search "microservices" --type architectural_decision
→ [Memory #15] Microservices architecture chosen for scalability
```

### Example 3: Pattern Detection

```bash
$ acfm memory patterns --type bugfix_pattern

Detected patterns:
- null-check-react (3×) - Null checks in React components
- async-race-condition (2×) - Race conditions in async code
- cors-preflight (2×) - CORS preflight issues

Recommendation: Consider adding ESLint rules for null checks
```

## Troubleshooting

### Memory not saving
- Check initialization: `acfm memory init`
- Content may be below confidence threshold
- May contain too many specific IDs

### Search not finding results
- Try broader keywords
- Use `acfm memory recall` without query for general context
- Check if memories exist: `acfm memory stats`

### Database locked
- Close other instances of `acfm`
- SQLite is single-writer; wait a moment and retry

## Related Skills

- `acfm-spec-workflow` - Foundation for spec-driven development
- `context-synthesizer` - For managing context in long conversations
- `systematic-debugging` - For complex problem resolution

## CLI Reference

See `acfm memory --help` for all commands and options.

---

**Remember**: The memory system learns from every interaction. The more you use it, the more valuable it becomes.
