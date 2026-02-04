---
name: oss-analysis
description: Analyze OSS solutions for code quality, documentation, and best practices using Context7, DeepWiki, and Perplexity. Use when users request repository analysis, code review, library documentation lookup, or need insights about GitHub projects and open-source technologies.
groups: [agent, copilot]
---

# OSS Analysis

Comprehensive analysis of open-source software using multiple specialized tools: Context7 for library documentation, DeepWiki for repository docs, and Perplexity for web research.

## When to Use This Skill

Use when users:
- Request analysis of a GitHub repository
- Want to understand a project's structure or codebase
- Need library or framework documentation
- Ask about specific libraries, packages, or technologies
- Want code quality insights and best practices
- Request comparison of repositories or libraries
- Need current information about OSS trends or tools
- Want to research open-source solutions for specific problems

## Available Tools

### 1. Context7
Get up-to-date official documentation for libraries and frameworks. Use for:
- API references and usage examples
- Framework-specific patterns and conventions
- Library configuration and setup guides

**Workflow:**
1. Use `resolve-library-id` to find the Context7 library ID (e.g., "/vercel/next.js")
2. Use `get-library-docs` with the resolved ID to fetch documentation

### 2. DeepWiki
Access comprehensive repository documentation and ask questions about GitHub projects. Use for:
- Understanding repository architecture and design decisions
- Finding implementation patterns in codebases
- Getting context about specific features or components

**Workflow:**
1. Use `read_wiki_structure` to explore available documentation topics
2. Use `read_wiki_contents` to get full documentation
3. Use `ask_question` for specific queries about the repository

### 3. Perplexity (WebSearch)
Search the web for current information about OSS projects, trends, and comparisons. Use for:
- Latest news and updates about libraries
- Community opinions and comparisons
- Tutorials and blog posts
- GitHub repositories and release notes

## Instructions

When analyzing OSS solutions:

1. **Identify the Analysis Type**:
   - **Repository Analysis**: Look up repository details on GitHub + use DeepWiki
   - **Library Documentation**: Use Context7 first, then supplement with DeepWiki if it's a GitHub-based project
   - **Technology Research**: Use Perplexity for current info, then deep-dive with other tools
   - **Comparison**: Combine all tools for comprehensive comparison

2. **For Repository Analysis**:
   - Look up repository metadata and statistics on GitHub
   - Review file structure and organization
   - Check documentation files (README, CONTRIBUTING, etc.)
   - Use DeepWiki to understand architecture and design decisions
   - Analyze code patterns and conventions

3. **For Library Documentation Lookup**:
   - Use Context7's `resolve-library-id` to find the library
   - Fetch targeted documentation with `get-library-docs`
   - If more context needed, use DeepWiki for the repository
   - Supplement with Perplexity for tutorials and examples

4. **For Technology Research**:
   - Start with Perplexity to get current landscape and trends
   - Use Context7 for official documentation of identified libraries
   - Use DeepWiki for deep-diving into specific repositories
   - Look up repository details on GitHub to examine code structure if needed

5. **Review Documentation Quality** (for repository analysis):
   - Check README completeness and clarity
   - Verify presence of LICENSE, CONTRIBUTING guidelines
   - Assess inline code comments
   - Review wiki or docs directory

6. **Identify Key Technologies**:
   - Examine package.json, requirements.txt, or similar files
   - Use Context7 to get docs for identified dependencies
   - Note frameworks, libraries, and development tools
   - Check for testing frameworks and CI/CD setup

7. **Provide Insights**:
   - Summarize project purpose and structure
   - Highlight strengths and potential improvements
   - Note adherence to best practices
   - Reference official documentation from Context7
   - Suggest areas for enhancement if relevant

## Examples

### Repository Analysis
- "Analyze the structure and architecture of the facebook/react repository"
- "Review the documentation quality of anthropics/anthropic-sdk-python"
- "Compare the code organization between Next.js and Remix"

### Library Documentation
- "Show me the latest Next.js App Router documentation"
- "How do I configure Supabase authentication?"
- "What are the best practices for MongoDB schema design?"

### Technology Research
- "What are the most popular React state management libraries in 2025?"
- "Compare Prisma vs TypeORM for TypeScript projects"
- "Find OSS alternatives to Auth0 for authentication"

### Combined Analysis
- "Analyze how Vercel's Next.js handles routing and show me the official docs"
- "Research the best GraphQL servers for Node.js and analyze their repositories"
- "Find popular OSS CMS solutions, then analyze the top 2 candidates"
