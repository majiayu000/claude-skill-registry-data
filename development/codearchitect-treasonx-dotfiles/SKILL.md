---
name: codearchitect
description: Analyzes a codebase to generate comprehensive architectural documentation including technologies used, data flows, functional components, APIs, external dependencies, commit history analysis, and complexity hotspots.
---

# Codebase Architecture Documentation Guide

## Overview
This skill performs a comprehensive analysis of a codebase to generate architectural documentation that helps developers understand the project structure, organization, technologies, data flows, and areas of active development. The analysis is read-only and produces a detailed architectural overview document.

## Scope
By default, analyze the current directory as the project root. Users can specify a different directory if needed.

## Output
Generate architectural documentation and write it to `@docs/project-overview.md` in the project directory.

## Analysis Areas

### 1. Technologies & Frameworks
Identify and document:
- **Programming languages** used (primary and secondary)
- **Frameworks and libraries** (web frameworks, UI libraries, etc.)
- **Build tools and package managers** (npm, Maven, Gradle, etc.)
- **Testing frameworks** and test runners
- **CI/CD tools** and deployment configurations
- **Database technologies** and ORMs
- **Development tooling** (linters, formatters, type checkers)
- **Runtime environments** (Node.js version, JVM version, etc.)

### 2. High-Level Data Flows
Document how data moves through the system:
- **Input sources**: Where data enters the system (user input, APIs, files, databases)
- **Processing layers**: Major data transformation steps
- **Output destinations**: Where data goes (responses, storage, external systems)
- **Key data transformations**: Critical business logic that transforms data
- **State management**: How application state is managed and flows
- **Data validation points**: Where and how data is validated
- **Error handling flows**: How errors propagate through the system

### 3. Functional Components
Identify and describe major system components:
- **Component structure**: Main modules, packages, or logical groupings
- **Component responsibilities**: What each major component does
- **Component relationships**: How components interact and depend on each other
- **Layer architecture**: Presentation, business logic, data access layers
- **Design patterns**: Observable patterns (MVC, Repository, Factory, etc.)
- **Module boundaries**: Clear separation points between components
- **Shared utilities**: Common code used across components

### 4. Public APIs Consumed
Document external APIs and services the project depends on:
- **Third-party APIs**: External services consumed (payment, auth, etc.)
- **API purpose**: Why each external API is used
- **Integration points**: Where in the code external APIs are called
- **Authentication methods**: How the project authenticates with external services
- **Rate limits or quotas**: Known limitations of external APIs
- **Fallback strategies**: How the system handles API failures

### 5. Public APIs Exposed
Document APIs or interfaces the project provides:
- **REST/GraphQL endpoints**: Public API routes and their purposes
- **Library interfaces**: If it's a library, what public APIs does it expose
- **CLI commands**: If it's a CLI tool, what commands are available
- **Event interfaces**: Webhooks, event emitters, or pub/sub interfaces
- **Authentication/Authorization**: How consumers authenticate
- **API versioning**: How API versions are managed
- **Documentation**: Where API docs are located (Swagger, JSDoc, etc.)

### 6. External System Dependencies
Identify dependencies on external systems:
- **Databases**: Type, purpose, and connection details (without credentials)
- **Message queues**: RabbitMQ, Kafka, SQS, etc.
- **Caching layers**: Redis, Memcached, etc.
- **Storage systems**: S3, file systems, blob storage
- **Authentication providers**: OAuth, SAML, LDAP
- **Monitoring and logging**: Datadog, Sentry, CloudWatch, etc.
- **Email services**: SendGrid, SES, etc.
- **Payment processors**: Stripe, PayPal, etc.

### 7. Commit History Analysis (Last 30 Commits)
Analyze recent development activity with moderate detail:
- **Most frequently changed files**: Which files are modified most often
- **Active development areas**: Which components/modules are seeing the most work
- **Change patterns**: Types of changes (features, bugs, refactoring)
- **Commit message themes**: Common topics in recent commits
- **File change statistics**: Additions, deletions per file/area
- **Development velocity**: Pace of changes over time
- **Key contributors**: Who is working on what (if git history available)

### 8. Complexity & Problem Areas
Identify areas that may be difficult to work with:
- **High complexity files**: Large files, high cyclomatic complexity
- **Deep nesting**: Functions/files with deep nesting levels
- **Unclear abstractions**: Areas where code intent is hard to understand
- **Frequent bug fixes**: Areas with many bug-related commits
- **Missing documentation**: Critical areas without comments or docs
- **Tight coupling**: Components that are overly dependent on each other
- **Technical debt indicators**: TODOs, FIXMEs, or known workarounds
- **Configuration complexity**: Complex or hard-to-understand config

## Inspection Process

### Step 1: Project Discovery
1. Identify the root directory of the project
2. Look for configuration files (package.json, pom.xml, Cargo.toml, etc.)
3. Examine directory structure to understand organization
4. Check for README files or existing documentation
5. Identify the primary programming language(s)

### Step 2: Technology Stack Analysis
1. Read package manager files to identify dependencies
2. Look for framework-specific files (next.config.js, vite.config.ts, etc.)
3. Identify build and test configurations
4. Check for Docker, CI/CD configurations
5. Note development tooling (ESLint, Prettier, etc.)

### Step 3: Code Structure Analysis
1. Map out the directory structure
2. Identify main entry points (main.ts, index.js, App.tsx, etc.)
3. Locate core business logic directories
4. Find configuration and utility directories
5. Identify test directories and test organization

### Step 4: Data Flow Analysis
1. Trace how requests/inputs enter the system
2. Follow data through major processing steps
3. Identify state management approaches
4. Note validation and error handling patterns
5. Map data persistence points

### Step 5: API and Integration Analysis
1. Search for API client code (fetch, axios, SDK usage)
2. Identify API route definitions (Express routes, controllers, etc.)
3. Look for authentication/authorization code
4. Find webhook or event handler definitions
5. Check for API documentation files

### Step 6: External Dependencies Analysis
1. Identify database connection code
2. Look for cloud service integrations (AWS, GCP, Azure)
3. Find message queue or event bus usage
4. Identify third-party service integrations
5. Note monitoring and observability tools

### Step 7: Git History Analysis
1. Run `git log --oneline -30` to get last 30 commits
2. Run `git log -30 --name-only --pretty=format:` to see changed files
3. Analyze which files appear most frequently
4. Group changes by directory/component
5. Identify patterns in commit messages
6. Calculate change velocity and patterns

### Step 8: Complexity Analysis
1. Use file size as a proxy for complexity (find large files)
2. Look for deeply nested code structures
3. Identify files with many dependencies
4. Search for TODO, FIXME, HACK comments
5. Find frequently fixed files (many "fix" commits)
6. Note areas with sparse documentation

### Step 9: Generate Documentation
Compile all findings into a comprehensive, well-structured markdown document.

## Report Format

Structure the output document (`@docs/project-overview.md`) as follows:

```markdown
# Project Architecture Overview
Generated: [Date]
Project: [Project Name/Directory]

## Executive Summary
[2-3 paragraph overview of the project, its purpose, tech stack, and architecture]

## Technology Stack

### Languages
- [Primary language and version]
- [Secondary languages if applicable]

### Frameworks & Libraries
- **[Category]**: [Framework/library name and version]
  - Purpose: [Why it's used]

### Build & Development Tools
- [Build tool]: [Version/config]
- [Testing framework]
- [Linters/formatters]

### Infrastructure & Runtime
- [Runtime environment]
- [Container/orchestration tools]
- [CI/CD platform]

## Architecture Overview

### High-Level Architecture
[Describe the overall architecture pattern - monolith, microservices, serverless, etc.]

### Directory Structure
```
[Key directories with brief descriptions]
```

### Core Components

#### [Component Name]
- **Location**: `path/to/component`
- **Responsibility**: [What it does]
- **Dependencies**: [What it depends on]
- **Key Files**: [Important files in this component]

[Repeat for each major component]

### Component Relationships
[Describe how major components interact with each other]

## Data Flows

### Input Sources
- [Source]: [Description of how data enters]

### Key Processing Flows
1. **[Flow Name]**: [Description of data transformation]
   - Input: [What goes in]
   - Processing: [What happens]
   - Output: [What comes out]

### State Management
[Describe how application state is managed]

### Error Handling
[Describe error handling strategy]

## APIs Consumed

### External Services
| Service | Purpose | Integration Point | Auth Method |
|---------|---------|-------------------|-------------|
| [Service name] | [Why used] | [Where in code] | [How auth] |

### Key Dependencies
- [Dependency]: [Purpose and usage]

## APIs Exposed

### Endpoints
| Method | Path | Purpose | Auth Required |
|--------|------|---------|---------------|
| [GET/POST] | [/api/path] | [What it does] | [Yes/No] |

### Public Interfaces
[Describe public API, library exports, or CLI commands]

### API Documentation
[Location of API docs, if any]

## External System Dependencies

### Databases
- **[Database type]**: [Purpose and schema notes]

### Cloud Services
- **[Service name]**: [Purpose and usage]

### Third-Party Integrations
- **[Integration name]**: [Purpose and configuration]

### Monitoring & Observability
- **[Tool name]**: [What it monitors]

## Development Activity Analysis
Last 30 Commits

### Most Active Areas
| Area/Component | Number of Changes | Change Type |
|----------------|-------------------|-------------|
| [Directory/file] | [Count] | [features/fixes/refactor] |

### Recent Development Themes
- **[Theme]**: [Number of commits] - [Description]

### Frequently Modified Files
1. `[file path]` - [number] changes - [Pattern of changes]
2. `[file path]` - [number] changes - [Pattern of changes]

### Change Velocity
[Describe pace and pattern of recent changes]

### Key Recent Changes
- [Commit summary with key changes or features added]

## Complexity & Challenge Areas

### High-Complexity Components
1. **[Component/File]** (`path/to/file`)
   - **Why Complex**: [File size, nesting, many dependencies]
   - **Improvement Suggestions**: [How to make it easier]

### Areas Requiring Attention
- **[Area]**: [Why it's problematic and what could help]

### Technical Debt Indicators
- [Location]: [Issue description]

### Documentation Gaps
- [Area lacking documentation]

## Recommendations

### For New Developers
[Key areas to understand first, where to start reading code]

### For Maintenance
[Areas that need refactoring or better documentation]

### For Feature Development
[Which components are easiest to extend, which need caution]

## Additional Resources
- [Link to other docs]
- [Link to wiki or confluence]
- [Link to API docs]

## Notes
- This document is auto-generated and should be updated as the project evolves
- For questions about specific components, see [relevant documentation]
```

## Important Notes

- **Read-Only Operation**: This skill MUST NOT modify any code files
- **No State Changes**: Do not run builds, tests, or any commands that modify the project
- **Document Only**: All output goes to the project overview document
- **Be Accurate**: Verify findings by reading actual code, not assumptions
- **Be Specific**: Include exact file paths when referencing code
- **Be Comprehensive**: Cover all 8 analysis areas thoroughly
- **Respect Privacy**: Do not include credentials, API keys, or sensitive data
- **Git Available**: Assume git is available for commit history analysis
- **Handle Missing Info**: If certain information isn't available, note it in the document

## Completion Criteria
- All 8 analysis areas have been thoroughly examined
- Technology stack is completely documented
- Major components and their relationships are clearly described
- Data flows are mapped out
- External APIs and dependencies are cataloged
- Last 30 commits have been analyzed with moderate detail
- Complexity areas have been identified
- Report is written to `@docs/project-overview.md`
- User is notified that the architectural analysis is complete
