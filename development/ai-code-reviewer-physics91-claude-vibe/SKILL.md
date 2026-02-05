---
name: ai-code-reviewer
description: |
  WHEN: Deep AI-powered code analysis, multi-model code review, security scanning with Codex and Gemini
  WHAT: Comprehensive code review using external AI models with severity-based findings, deduplication, and secret detection
  WHEN NOT: Simple lint checks -> code-reviewer, Quick security only -> security-scanner, Style formatting -> code-quality-checker
mcp_tools:
  - analyze_code_with_codex
  - analyze_code_with_gemini
  - analyze_code_combined
  - scan_secrets
  - get_analysis_status
---

# AI Code Reviewer Skill

## Purpose

Leverages external AI models (OpenAI Codex CLI and Google Gemini CLI) for deep code analysis beyond Claude's built-in capabilities. Provides multi-perspective code reviews with result aggregation and consensus scoring.

## Prerequisites

At least one of the following must be installed and authenticated:
- **Codex CLI**: Run `codex auth` to authenticate
- **Gemini CLI**: Run `gemini auth login` to authenticate

## When to Use

- Deep security analysis requiring external AI perspective
- Performance optimization requests needing specialized analysis
- Multi-model code review for high-confidence findings
- Large codebase analysis with result caching
- Secret and credential detection in code

## Available MCP Tools

### analyze_code_with_codex
Uses OpenAI Codex for comprehensive code analysis.
- **Best for**: General code review, bug detection, logical errors
- **Input**: Code snippet with optional context (project type, language, focus areas)
- **Output**: Structured findings with severity levels and suggestions

### analyze_code_with_gemini
Uses Google Gemini for code analysis.
- **Best for**: Performance analysis, architectural review, style consistency
- **Input**: Code snippet with optional context
- **Output**: Structured findings with code examples

### analyze_code_combined
Aggregates results from both Codex and Gemini with deduplication.
- **Best for**: High-stakes reviews requiring consensus
- **Features**:
  - Parallel execution for speed
  - Result deduplication with similarity threshold
  - Confidence scoring based on agreement
- **Output**: Merged findings with source attribution

### scan_secrets
Detects hardcoded secrets, API keys, credentials, and sensitive data.
- **Best for**: Pre-commit security checks
- **Patterns**: AWS, GCP, Azure, GitHub, database credentials, private keys
- **Excludes**: Test files, mock files by default
- **Output**: Secret findings with severity and remediation suggestions

### get_analysis_status
Retrieves status of async analysis operations.
- **Input**: Analysis ID from previous tool call
- **Output**: Status (pending/in_progress/completed/failed), result or error

## Workflow

### Step 1: Determine Analysis Type

Ask user for analysis preference:

**Question**: "What type of AI analysis do you need?"

**Options**:
1. **Quick Review** - Single model, faster (Codex OR Gemini)
2. **Deep Review** - Combined models with consensus scoring
3. **Security Scan** - Secret detection only
4. **Performance Focus** - Optimization-focused review
5. **Full Audit** - Combined + secret scan

### Step 2: Model Selection (if Quick Review)

**Question**: "Which AI model should be used?"

**Options**:
1. **Codex (OpenAI)** - Better for bug detection, logical errors
2. **Gemini (Google)** - Better for architectural patterns, style

### Step 3: Set Context (Optional)

**Question**: "What's the project context?"

**Options**:
1. **Auto-detect** - Infer from code
2. **Web App (React/Vue)** - Frontend focus
3. **API (Node/Express)** - Backend focus
4. **MCP Server** - Protocol focus
5. **CLI Tool** - User tool focus
6. **Library** - Reusability focus

### Step 4: Execute Analysis

Call the appropriate MCP tool based on selections.

### Step 5: Present Results

Format findings in structured markdown with:
- Overall assessment
- Summary statistics
- Grouped findings by severity
- Actionable recommendations

## Response Template

```markdown
## AI Code Review Results

**Analysis ID**: [id]
**Models Used**: [codex/gemini/combined]
**Cache Status**: [hit/miss]
**Duration**: [Xms]

### Overall Assessment

[AI-generated overall assessment of code quality]

### Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |
| **Total** | **X** |

### Findings

#### Critical Issues

1. **[Title]** (Line X)
   - **Description**: [...]
   - **Suggestion**: [...]
   - **Code**: `[snippet]`

#### High Priority

[...]

### Recommendations

1. [Prioritized action item 1]
2. [Prioritized action item 2]
3. [...]

---
*Analysis by [model(s)] | Confidence: [X]% | Duration: [X]ms*
```

## Integration Notes

- Works alongside `code-reviewer` for comprehensive analysis
- Complements `security-scanner` with external AI perspective
- Results are cached (1 hour TTL) for repeated queries
- Secret scanning runs locally, no external API calls
- Triggered by `/cr` express command

## Error Handling

- **CLI Not Found**: Gracefully reports missing CLI, suggests installation
- **Authentication Failed**: Guides user through auth process
- **Timeout**: Returns partial results with warning
- **Rate Limited**: Queues requests with exponential backoff

## Performance Notes

- Combined analysis runs in parallel by default
- Cache reduces repeated analysis costs
- Large files are truncated with warning
- SQLite storage for persistent cache
