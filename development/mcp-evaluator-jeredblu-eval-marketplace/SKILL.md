---
name: mcp-evaluator
description: Comprehensive security and privacy evaluation system for MCP (Model Context Protocol) servers. Use when users provide GitHub URLs to MCP servers and request security assessment, privacy evaluation, or ask "is this MCP safe to use." Evaluates security vulnerabilities, privacy risks, code quality, community feedback, and provides actionable recommendations with risk scoring.
---

# MCP Server Security Evaluator

## Overview

Automatically evaluate the security, privacy, and reliability of MCP (Model Context Protocol) servers from GitHub repositories. This skill performs comprehensive assessments including code analysis, community feedback research, security vulnerability detection, and risk scoring to provide actionable recommendations.

## When to Use This Skill

Use this skill when users:
- Provide a GitHub URL to an MCP server repository
- Ask "is this MCP server safe?"
- Request security assessment of an MCP server
- Want to evaluate privacy risks before installing an MCP server
- Need to compare MCP servers with similar functionality
- Ask about community feedback or reviews of an MCP server

## Tool Strategy

This skill works with or without MCP servers through a graceful degradation approach:

**For GitHub repositories**:
- **Priority**: GitHub MCP (if available) for direct repository API access
- **Alternatives**: Bright Data MCP (The Web MCP) or built-in web tools for scraping
- **Optional**: Sequential Thinking MCP for systematic analysis (recommended but not required)
- **Fallback**: Claude's built-in web search when no MCP servers available

**For web search and community validation**:
- **Priority**: Bright Data MCP or Brave Search MCP for web search and content fetching
- **Fallback**: Claude's built-in web search

## Evaluation Workflow

### Step 1: Initial Setup

Ask the user their preferred output format:
- Markdown (.md) - default
- PDF (.pdf) - requires conversion after markdown creation

Acknowledge receipt and inform user that evaluation is beginning. Parse the GitHub URL to extract owner and repository name.

### Step 2: Tool Assessment

Check which tools are available and plan the evaluation approach:
- If GitHub MCP available: use for repository access (preferred for GitHub repos)
- If Bright Data MCP available: use for web scraping and searching (or as GitHub alternative)
- If neither available: use Claude's built-in capabilities with noted limitations

### Step 3: Create Assessment File

Use built-in `create_file` tool to create assessment file in `/mnt/user-data/outputs/`:
- File naming: `MCP_Security_Assessment_{owner}_{repo_name}.md`
- Update iteratively throughout evaluation process

### Step 4: Repository Content Access

**With GitHub MCP (Priority)**:
- Use GitHub MCP tools to directly access:
  - Repository metadata and statistics
  - File contents: README.md, package.json, LICENSE, source files
  - Commit history via `list_commits` for activity analysis
  - Repository tree/structure
- Use `search_repositories` for similar MCP servers

**With Bright Data MCP (Alternative)**:
- Use `scrape_as_markdown` to retrieve:
  - Repository main page: `https://github.com/{owner}/{repo}`
  - README: `https://github.com/{owner}/{repo}/blob/main/README.md`
  - Raw files: `https://raw.githubusercontent.com/{owner}/{repo}/main/{filepath}`
  - Key code files: package.json, index.js, src files, etc.

**Fallback Without MCP**:
- Use Claude's built-in web tools for available information
- Note limitations in assessment
- Request user provide critical files if needed

Document each file examined with code snippets of important sections.

### Step 5: Sequential Evaluation

Execute evaluation in this order, updating assessment file after each step:

#### 5.1 Repository Setup & Metadata
- Extract repository statistics (stars, forks, contributors, activity)
- Analyze commit history and frequency
- Review contributor diversity and patterns
- Check for security policies and contribution guidelines
- Document findings in "GitHub Repository Assessment" section

#### 5.2 Purpose & Functionality Analysis
- Review README and documentation thoroughly
- Identify stated purpose and capabilities
- List external services/APIs the server connects to
- Note required permissions and access levels
- Identify creator/maintainer background
- Create "Server Purpose" and "Expected Functionality" sections

#### 5.3 Alternatives Analysis
Search for alternative MCP servers with similar functionality:
- Use web search: "{functionality} MCP server"
- Check MCP directories: Smithery, Glama, PulseMCP, MCP.so
- Review repository forks for improved versions
- Document 2-3 alternatives minimum with comparisons
- Create "Alternative MCP Servers" section

#### 5.4 Code Review
Analyze codebase for:
- Authentication mechanisms and credential handling
- Data collection, storage, and transmission practices
- Security practices (input validation, encryption, sanitization)
- Suspicious or unexpected behaviors
- Code quality and error handling

**Reference the security patterns documentation**: Review `references/mcp_security_patterns.md` to identify known vulnerability patterns, and `references/safe_mcp_examples.md` to avoid false positives from legitimate patterns.

**Be specific**: Include actual code snippets as evidence. Categorize findings by severity (Critical, High, Medium, Low). Focus on concrete vulnerabilities, not generic statements.

Document in "Code Analysis" section.

#### 5.5 Community Validation
Perform specific web searches using Bright Data MCP or web search:
- Reddit: "{owner} {repo_name} MCP"
- Twitter/X: "{owner} {repo_name} MCP"  
- MCP Directories: "smithery.ai {repo_name}", "glama.ai {repo_name}", "pulsemcp {repo_name}", "mcp.so {repo_name}"
- Security forums: "{owner} {repo_name} security vulnerability"
- Developer forums: implementation examples and feedback

For each search:
- Document exact query used
- Summarize relevant results with links
- Note security concerns raised by community

Document all findings in "Community Feedback" section with clear source attribution.

#### 5.6 Risk Assessment
Analyze all collected information and evaluate across dimensions:

| Dimension | Evaluation Criteria |
|-----------|-------------------|
| Security | Protection against attacks, credential handling, code vulnerabilities |
| Privacy | Data collection practices, data minimization, transmission security |
| Reliability | Code quality, maintenance activity, error handling |
| Transparency | Documentation quality, purpose clarity, open source practices |
| Usability | Setup complexity, integration quality, user experience |

For each dimension:
- Provide concrete examples supporting the score
- List specific strengths and weaknesses  
- Assign score (0-100) with clear justification

**Scoring Guidelines**:
- 0-49: Critical security flaws or dangerous functionality
- 50-69: Significant security concerns but not immediately dangerous
- 70-84: Reasonably secure with minor concerns
- 85-100: Very secure with robust practices

Create "Risk Assessment" section with scoring table and "Final Verdict" with definitive recommendation.

#### 5.7 Usability Assessment
Evaluate practical aspects:
- Installation complexity and requirements
- Documentation quality for setup/usage
- Configuration options and flexibility
- Potential performance issues
- Integration smoothness with Claude
- Edge cases and limitations

Document in "Usability Assessment" section with specific examples.

### Step 6: Make Confident Judgments

Provide definitive recommendations. Avoid hedging. Be clear about:
- Whether users should use this MCP server
- Specific use cases where appropriate/inappropriate
- Critical risks that must be addressed
- Alternatives that may be better

### Step 7: Completion

- Provide summary of key findings
- Link to assessment file in `/mnt/user-data/outputs/`
- If PDF requested, convert markdown to PDF

## Assessment Document Structure

Create assessment with this exact structure:

```markdown
# Security Assessment: [MCP Server Name]

## Evaluation Overview
- Repository URL: [GitHub URL]
- Evaluation Date: [Current Date]
- Evaluator: Claude AI
- Repository Owner: [Username/Organization]
- Evaluation Methods: [Tools used]
- Tool Availability: [Which MCP servers were available]
- Executive Summary: [1-2 paragraphs on safety and key risks/benefits]

## GitHub Repository Assessment
[Repository stats, contributor analysis, activity patterns]

## Server Purpose
[Functionality description, external services, permissions, creator info]

## Expected Functionality
[Detailed explanation of capabilities, APIs, typical usage, limitations, examples]

## Alternative MCP Servers
[List of alternatives with comparisons]

## Code Analysis
[Security review findings categorized by severity with code snippets]

## Community Feedback
[External references, user reviews, discussions with source attribution]

## Risk Assessment
[Comprehensive evaluation across all dimensions]

## Usability Assessment
[Practical evaluation of setup, documentation, integration]

### Scoring
| Dimension | Score (0-100) | Justification |
|-----------|---------------|--------------|
| Security  | [Score]       | [Specific evidence] |
| Privacy   | [Score]       | [Specific evidence] |
| Reliability | [Score]     | [Specific evidence] |
| Transparency | [Score]    | [Specific evidence] |
| Usability | [Score]       | [Specific evidence] |
| **OVERALL RATING** | [Score] | [Summary] |

### Final Verdict
[Clear statement on whether to use this MCP server, with specific use cases]

### Evaluation Limitations
[If applicable, note any limitations due to unavailable tools]
```

## Error Handling

If issues occur during evaluation:
- Document specific error in assessment file
- Note which tool/function failed and error message
- List fallback methods used
- Mark sections with limited information
- Include "Evaluation Limitations" section if significant errors
- Continue with remaining steps using alternatives
- Provide recommendations based on available information

## Ongoing Communication

Keep user informed at key milestones:
- When repository files successfully accessed
- When GitHub metadata analysis complete
- When code review complete
- When community validation searches complete
- When using fallback methods due to tool unavailability

Show exactly what tools/functions being called and their results. If evaluation requires extended time, provide interim updates.

## Key Principles

**Be Specific, Not Generic**: 
- ❌ "This has moderate security concerns"
- ✅ "Line 47 stores API keys in plain text without encryption (Critical severity)"

**Make Confident Judgments**:
- ❌ "This might be relatively safe depending on your use case"
- ✅ "This MCP server is safe for personal use but should not be used in production environments handling sensitive data due to weak authentication implementation"

**Include Evidence**:
Always back up scores and recommendations with specific code examples, community feedback quotes, or measurable metrics.

**Adapt to Available Tools**:
Use the best tools available but continue evaluation even without ideal tools. Document what methods were used and any resulting limitations.

## References

This skill includes reference documentation in the `references/` directory:

- `mcp_security_patterns.md` - Comprehensive catalog of security vulnerabilities and attack patterns specific to MCP servers
- `safe_mcp_examples.md` - Examples of legitimate MCP patterns that might look suspicious but are safe

Read these references as needed during code analysis to improve detection accuracy and reduce false positives.
