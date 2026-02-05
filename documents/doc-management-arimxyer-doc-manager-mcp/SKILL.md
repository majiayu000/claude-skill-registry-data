---
name: doc-management
description: Documentation lifecycle management skill. Activates when user mentions documentation, docs, sync, quality, validation, releases, or setup. Routes to appropriate agent (doc-expert for orchestration, doc-writer for content) and provides gentle reminders about documentation health.
---

# Doc-Management Skill

Documentation lifecycle management through the doc-manager MCP server. This skill routes requests to specialized agents and provides proactive documentation health awareness.

## Activation Triggers

Activate when user mentions:

**Documentation terms**: "documentation", "docs", "README", "API docs", "guide"

**Sync/status**: "sync docs", "doc status", "update docs", "docs out of date"

**Quality**: "doc quality", "validate docs", "check docs", "broken links"

**Releases**: "release", "deploy", "ship", "merge to main", "v1.0"

**Setup**: "setup docs", "init docs", "documentation management"

**Configuration**: "config", "configuration", ".doc-manager", "conventions", "api_coverage", "preset", "strategy", "exclude patterns"

**Code changes**: "committed", "pushed", "finished implementing" (gentle reminder)

## Agent Routing

### Route to doc-expert agent:
- Analysis tasks: "check status", "what needs updating"
- Quality tasks: "assess quality", "is this release-ready"
- Sync tasks: "sync documentation", "update docs for changes"
- Setup tasks: "set up doc management", "initialize"
- Validation tasks: "validate docs", "check for broken links"
- Migration tasks: "move docs", "reorganize documentation"
- Config tasks: "tune config", "fix coverage", "add preset", "change strategy"

### Route to doc-writer agent:
- Content tasks: "write API docs for X", "create a guide"
- Direct editing: "update the README", "add examples"
- Simple updates: "document this function", "add code samples"

### Decision Flow:
```
Requires analysis, orchestration, quality, or state management?
  YES → doc-expert agent
  NO → Straightforward content with clear scope?
    YES → doc-writer agent
    NO → doc-expert agent (to assess first)
```

## Behavior Guidelines

### Do NOT Auto-Run
Never automatically run heavy operations. Always suggest and ask:
- "Would you like me to check documentation status?"
- "I can run a quality assessment. Want me to proceed?"
- "Documentation sync available. Should I start?"

### Gentle Reminders
At appropriate moments, offer (don't command):

**On release mention:**
```
Before the release, would you like a documentation health check?
- /doc-status - Quick sync status
- /doc-quality - Full quality assessment
```

**On code change mention:**
```
Code changes may need documentation updates.
Run /doc-status when ready to check.
```

**On docs mention:**
```
I can help with documentation. Options:
- Check status: /doc-status
- Full sync: /doc-sync
- Quality audit: /doc-quality
```

### First-Run Detection
If `.doc-manager/` doesn't exist when user asks about docs:
```
Documentation management isn't set up for this project.

Would you like me to initialize it? I'll:
1. Detect your documentation platform
2. Create tracking configuration
3. Establish baselines

Say "setup docs" to proceed.
```

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `/doc-status` | Quick health check |
| `/doc-sync` | Full sync workflow |
| `/doc-quality` | Quality assessment |
| `/doc-dashboard` | Comprehensive metrics |

## Edge Cases

### Large-Scale Changes (50+ files)
Warn before proceeding:
```
Detected 50+ files with changes. This will be processed in batches.
Estimated time: 10-15 minutes.
Proceed with documentation sync?
```

### Quality Conflicts
If fixing one criterion harms another:
```
Quality trade-off detected:
- Adding detail improves Clarity
- But increases Uniqueness issues (duplication)

Which should I prioritize?
```

### Not Initialized
Always check for `.doc-manager/` before assuming setup exists.
Offer initialization if missing.

## Integration Points

This skill coordinates with:
- **doc-expert agent**: For orchestration, analysis, quality, state, config
- **doc-writer agent**: For content creation and editing
- **MCP tools**: docmgr_* tools via agents
- **Slash commands**: /doc-status, /doc-sync, /doc-quality, /doc-dashboard

---

## Project Context Awareness

When helping with documentation, consider the project type to provide better recommendations.

### Project Type Matrix

| Project Type | Recommended Strategy | Doc Focus | Indicators |
|--------------|---------------------|-----------|------------|
| **Library/SDK** | `all_then_underscore` | Public API reference | Has `__all__`, pip installable |
| **MCP Server** | `all_only` | Tool reference, usage | FastMCP, mcp dependency |
| **CLI Tool** | `all_only` or `underscore_only` | Commands, options | argparse, click, typer |
| **Application** | `all_only` | User guides, config | Django, FastAPI app |

### Detecting Project Type

Look for these indicators:
- **MCP Server**: `mcp` in dependencies, FastMCP imports, tool definitions
- **Library**: `__all__` exports, package structure, PyPI metadata
- **CLI**: argparse/click/typer imports, console_scripts entry points
- **Application**: Framework configs (settings.py, config.py), no `__all__`

---

## Context-Aware Heuristics

When reviewing documentation health, apply these heuristics to provide proactive suggestions.

### Heuristic 1: Low Coverage + No api_coverage Config

**Detect**: Quality assessment shows <50% API coverage AND no `api_coverage` section in `.doc-manager.yml`

**Suggest**:
```
Coverage is at {X}%. This might include framework symbols that don't need documentation.

Adding an api_coverage preset could help filter these out. For example:
- `pydantic` preset excludes Config, validators, etc.
- `pytest` preset excludes test_*, Test*, fixtures

Would you like me to explain the available presets?
```

### Heuristic 2: Wrong Strategy for Project Type

**Detect**: MCP server project (has mcp dependency) AND strategy is `all_then_underscore`

**Suggest**:
```
This appears to be an MCP server. Users interact via the MCP protocol, not Python imports.

Consider using `all_only` strategy - this will only count symbols explicitly exported via __all__.
For MCP servers, 0% API coverage is often correct since there's no public Python API.

Want me to update the config?
```

### Heuristic 3: Stale Source Patterns

**Detect**: `sources` patterns in config don't match any existing files

**Suggest**:
```
Some source patterns in .doc-manager.yml don't match any files:
- `{pattern}` → 0 files found

The project structure may have changed. Would you like me to update the source patterns?
```

### Heuristic 4: Missing Conventions File

**Detect**: Consistency issues detected (heading case, list markers) AND no `doc-conventions.yml` exists

**Suggest**:
```
Quality assessment found consistency issues:
- {X} files use different heading case styles
- {Y} files use different list markers

A doc-conventions.yml file could help enforce standards.
Would you like me to help set one up?
```

### Heuristic 5: Preset Mismatch

**Detect**: Using framework (pydantic, django, etc.) but no matching preset configured

**Suggest**:
```
I noticed this project uses {framework} but the `{framework}` preset isn't configured.

This preset would exclude common {framework} symbols from coverage metrics:
{list of excluded symbols}

Add it to improve coverage accuracy?
```

---

## Progressive Guidance

Provide context-aware suggestions based on project maturity.

### New Setup (just initialized)

```
Documentation management is now set up!

Recommended next steps:
1. Run /doc-quality to establish a quality baseline
2. Consider adding doc-conventions.yml for consistency
3. Review api_coverage settings if accuracy seems off
```

### Active Development (frequent changes detected)

```
I noticed frequent code changes since last sync.

Tip: Run /doc-sync periodically to keep docs in sync.
For CI integration, consider adding doc validation to your pipeline.
```

### Pre-Release (release/version mentioned)

```
Preparing for release? Here's a quick checklist:
1. /doc-sync - Ensure docs match code
2. /doc-quality - Check for issues
3. Review any "poor" quality scores before shipping

Want me to run a full pre-release audit?
```

### Config Issues Detected

```
I noticed some configuration that might need attention:
- {specific issue from heuristics}

The doc-expert agent can help tune your configuration.
Say "tune config" to start.
```
