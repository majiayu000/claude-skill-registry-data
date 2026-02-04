---
name: claude-md-auto-updater
description: This skill automatically detects when CLAUDE.md files need updates based on codebase analysis. It identifies new patterns, code violations, stale documentation, and anti-patterns, then proposes specific markdown diffs showing exactly what CLAUDE.md sections should be added, modified, or removed. When codebase architecture changes, new patterns emerge, or documented practices diverge from actual code, this skill analyzes the robo-trader project structure and generates actionable recommendations with confidence scores. Should be invoked after major feature completions, during code reviews, or as periodic maintenance scans.
---

# CLAUDE.md Auto-Updater Skill

## Overview

This skill maintains documentation accuracy by detecting when robo-trader's CLAUDE.md files diverge from actual codebase patterns. It analyzes both Python backend and TypeScript/React frontend code to identify:

- **New Patterns**: When 3+ code instances share a similar pattern not yet documented
- **Violations**: When code breaks documented CLAUDE.md constraints
- **Stale Documentation**: When documented patterns no longer appear in the codebase
- **Anti-Patterns**: When repeated mistakes could be prevented with documentation

The skill generates specific, evidence-based recommendations with markdown diffs showing exactly what to change in which CLAUDE.md file. Each recommendation includes confidence scores, file:line references proving why the change is needed, and a learning mechanism to improve accuracy based on accepted/rejected feedback.

## When to Use This Skill

Invoke this skill when:

1. **Feature Completion** - After completing major features that introduce new architectural patterns
2. **Code Reviews** - Before merging PRs that change architecture or patterns
3. **Periodic Maintenance** - Weekly/monthly scans to catch documentation drift
4. **Manual Request** - On-demand analysis when unsure if CLAUDE.md is current
5. **Bulk Changes** - After refactoring or restructuring significant portions of the codebase

## Core Capabilities

### 1. Pattern Detection

Automatically scans the codebase to find:

- **New Patterns** (Python + TypeScript/React): When 3+ similar implementations exist without documentation
- **Critical Violations**: When code directly violates documented rules (e.g., direct DB access when docs say use locked methods)
- **Stale Documentation**: When documented patterns haven't appeared in code for 30+ days
- **Anti-Patterns**: Repeated mistakes (e.g., 4+ instances of `time.sleep()` in async code)

### 2. Recommendation Generation

For each detection, generates:

- **Specific Markdown Diff**: Exact text to add/modify/remove in CLAUDE.md
- **Evidence**: File:line references proving the pattern exists
- **Confidence Score**: 0-100% based on evidence quantity and clarity
- **Rationale**: Human-readable explanation of why the change is needed
- **Affected File**: Which CLAUDE.md file(s) need updates

### 3. Validation & Safety

Before proposing changes:

- **Consistency Check**: Verifies no conflicting rules across CLAUDE.md files
- **Reference Validation**: Confirms all referenced files still exist in codebase
- **Example Verification**: Checks that code examples in recommendations actually work
- **Impact Analysis**: Assesses consequences of proposed changes

### 4. Learning System

Tracks feedback to improve future recommendations:

- Records which recommendations you accepted/rejected
- Analyzes patterns in helpful vs. noisy suggestions
- Adjusts confidence scoring based on accuracy history
- Improves pattern detection thresholds over time

## How to Use This Skill

### Basic Workflow

1. **Trigger Analysis**: Call the skill with your codebase path and analysis scope
2. **Review Recommendations**: Examine generated markdown diffs with evidence
3. **Accept/Reject**: Approve recommendations and optionally apply them
4. **Track Feedback**: Provide acceptance/rejection feedback to train the learning system
5. **Update CLAUDE.md**: Apply approved recommendations to your documentation

### Example Usage

```
Analyze robo-trader codebase for CLAUDE.md updates
- Scope: Full backend (src/) + frontend (ui/src/)
- Output: Markdown diffs with >70% confidence
```

Result:
```
📋 RECOMMENDATION 1: New Queue Handler Pattern
File: src/CLAUDE.md
Confidence: 92%
Evidence: Found 3 new queue handlers (FORECAST, SENTIMENT, SIGNAL) at:
- src/services/scheduler/handlers/forecast_handler.py:12
- src/services/scheduler/handlers/sentiment_handler.py:15
- src/services/scheduler/handlers/signal_handler.py:18

Suggested addition to "Sequential Queue Architecture (CRITICAL)" section:
+ **Handler Examples**: RECOMMENDATION_GENERATION, PORTFOLIO_SYNC, DATA_FETCHER, FORECAST_ANALYSIS, SENTIMENT_ANALYSIS, SIGNAL_DETECTION
```

### Detection Patterns

The skill looks for specific patterns in your codebase:

#### Python Backend Patterns
- Queue handler decorators (`@task_handler()`)
- Coordinator class definitions (inheriting from `BaseCoordinator`)
- Database access methods (detecting direct vs. locked access)
- SDK usage patterns (detecting `ClaudeSDKClientManager` usage)
- Error handling (custom exception types)
- Async operations (detecting sleep vs. condition polling)

#### TypeScript/React Frontend Patterns
- Component organization (checking feature-based structure)
- Hook patterns (custom hooks, Zustand stores)
- State management patterns
- API integration patterns
- Error handling approaches

### Output Format

Each recommendation includes:

```markdown
## RECOMMENDATION [#]: [Title]
**File**: [Which CLAUDE.md to update]
**Confidence**: [0-100%]

### Evidence
[File:line references proving the pattern exists]

### Why This Update?
[Human-readable explanation]

### Proposed Change
[Markdown diff showing exact text to add/modify/remove]

### Related Changes
[Other CLAUDE.md files that might need updates]
```

## Bundled Resources

### scripts/detector.py
Core pattern detection engine that scans Python and TypeScript/React code to identify new patterns, violations, stale documentation, and anti-patterns. Returns structured JSON with all findings.

Usage:
```bash
python scripts/detector.py /path/to/robo-trader --scope full
```

### scripts/analyzer.py
Analyzes detector output, assigns confidence scores, identifies affected CLAUDE.md files, and prioritizes recommendations.

Usage:
```bash
python scripts/analyzer.py detector_output.json
```

### scripts/generator.py
Converts analyzed findings into specific CLAUDE.md update proposals with markdown diffs, evidence references, and human-readable rationale.

Usage:
```bash
python scripts/generator.py analysis_output.json --output-format markdown
```

### scripts/validator.py
Validates recommendations before proposing them: checks for conflicting rules, verifies examples work, confirms referenced files exist, and performs impact analysis.

Usage:
```bash
python scripts/validator.py recommendations.json
```

### scripts/feedback_tracker.py
Records accepted/rejected recommendations and updates confidence scoring based on feedback patterns to improve accuracy over time.

Usage:
```bash
python scripts/feedback_tracker.py --record-feedback recommendation_id accepted
```

### references/ROBO_TRADER_PATTERNS.md
Comprehensive reference of robo-trader-specific patterns to detect: queue handlers, coordinators, database access, SDK usage, anti-patterns, and learning rules.

### references/CLAUDE_MD_STRUCTURE.md
Reference for CLAUDE.md file organization, required sections per file type, metadata format, and naming conventions.

### references/DETECTION_RULES.md
Detailed detection rules including AST patterns for Python, regex/AST patterns for TypeScript, confidence thresholds, and evidence collection requirements.

### assets/claude-md-template-section.md
Template snippets for adding new sections to CLAUDE.md: new pattern sections, anti-pattern sections, quick reference templates, code example templates.

### assets/feedback-schema.json
Schema for tracking feedback on recommendations: recommendation ID, accepted/rejected status, user notes, timestamp, confidence impact.

## Integration Points

This skill is designed to integrate with:

- **GitHub Actions**: Automated analysis on every PR
- **Git Hooks**: Pre-commit validation
- **Claude Code CLI**: Manual `/claude-md-update` command
- **robo-trader-dev MCP**: Runtime pattern validation
- **Feedback Loop**: Learning system improves from acceptance/rejection patterns

## Next Steps

1. **Run Initial Scan**: Analyze your codebase to get baseline recommendations
2. **Review High-Confidence Suggestions**: Accept/reject >80% confidence recommendations first
3. **Apply Changes**: Update your CLAUDE.md files with approved recommendations
4. **Provide Feedback**: Record which recommendations were helpful
5. **Iterate**: Run periodic scans to keep documentation synchronized

---

**Remember**: This skill proposes changes—it never auto-commits. Always review recommendations before updating your CLAUDE.md files.
