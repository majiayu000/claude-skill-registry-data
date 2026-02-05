---
name: m-skills-collection
description: A comprehensive collection of Agent Skills for software engineering, database operations, and productivity automation. Use when building, optimizing, or debugging software systems with AI assistance.
---

# M Skills Collection

This collection provides structured guidance for software engineering, database operations, browser automation, and development productivity through specialized agent skills.

## When to Activate

Activate these skills when:
- Reviewing or writing code
- Querying enterprise databases (Maximo, AX, Fabric)
- Automating git workflows and CI/CD
- Generating tests or documentation
- Planning implementations or architectural decisions
- Extracting data from web pages
- Managing context across IDE sessions

## Skill Map

### Code Quality & Development

**Code Review** (`code-review`)
Expert code review covering security, performance, maintainability, and language-specific best practices. Ensures high-quality output through systematic verification.

**Refactor Suggest** (`refactor-suggest`)
Clean code advisor identifying code smells and proposing modern design patterns. Transforms technical debt into maintainable code.

**API Test Generator** (`api-test-gen`)
Generates API testing templates and patterns for REST APIs including unit tests, integration tests, and framework-specific patterns.

### Git & Version Control

**Git Smart Commit** (`git-smart-commit`)
Generates conventional commit messages by analyzing staged changes. Ensures consistent git history following conventional commits specification.

**PR Summary** (`pr-summary`)
Creates comprehensive Pull Request summaries giving reviewers all context needed for efficient review and approval.

**Daily Standup** (`daily-standup`)
Generates concise standup reports from git activity and GitHub PRs. Synthesizes accomplishments, plans, and blockers.

### Database Operations

**Database Query Guide** (`database-query-guide`)
Comprehensive MSSQL server routing and query best practices. Ensures correct server selection and prevents data fabrication.

**Maximo Helper** (`maximo-helper`)
Maximo database templates for work orders, assets, inventory, and labor. Includes mandatory site filtering.

**AX Dynamics Helper** (`ax-dynamics-helper`)
Dynamics AX templates for ERP data including financials, inventory, sales, and purchasing with DATAAREAID filtering.

**SQL Analyzer** (`sql-analyzer`)
Advanced SQL analysis and optimization including performance recommendations, index suggestions, and anti-pattern detection.

**Fabric Helper** (`fabric-helper`)
Microsoft Fabric reference for Lakehouse and Warehouse queries including Spark SQL and Delta Lake operations.

### Project Setup & DevOps

**Project Scaffold** (`project-scaffold`)
Project structure templates for Next.js, React, Node.js, and other modern frameworks with production-ready configuration.

**Dockerfile Generator** (`dockerfile-generator`)
Multi-stage Dockerfile templates optimized for security, size, and build efficiency.

**GitHub Actions** (`github-actions`)
CI/CD workflow templates for automated builds, tests, and deployments with security best practices.

### Planning & Documentation

**Implementation Plan** (`implementation-plan`)
Machine-readable implementation plans with requirements, phases, tasks, and definitions of done.

**ADR Generator** (`adr-generator`)
Architectural Decision Records capturing context, rationale, and consequences of technical decisions.

### Browser & Memory

**Chrome Data Extract** (`chrome-data-extract`)
Browser automation patterns for data extraction using MCP browser tools including navigation, selection, and verification.

**Cipher Memory** (`cipher-memory`)
Universal memory integration for persisting context, decisions, and learnings across IDE sessions.

## Core Concepts

The collection is organized around three themes:

1. **Development Quality**: Skills for writing, reviewing, and testing code (code-review, refactor-suggest, api-test-gen)

2. **Data Operations**: Skills for database queries and data extraction (database-query-guide, maximo-helper, ax-dynamics-helper, sql-analyzer, fabric-helper, chrome-data-extract)

3. **Workflow Automation**: Skills for git, CI/CD, and productivity (git-smart-commit, pr-summary, daily-standup, github-actions, dockerfile-generator)

## Practical Guidance

Each skill can be used independently or in combination. Skills reference each other through integration sections. For complex tasks, combine multiple skills:

- **Feature Development**: implementation-plan → code-review → api-test-gen → git-smart-commit → pr-summary
- **Database Analysis**: database-query-guide → maximo-helper/ax-dynamics-helper → sql-analyzer
- **Project Setup**: project-scaffold → dockerfile-generator → github-actions

## Integration

All skills integrate with **Cipher Memory** for cross-session persistence. Skills within the same domain (database, git, code) reference each other for comprehensive coverage.

## References

Internal skills in this collection:
- [code-review](code-review/SKILL.md)
- [git-smart-commit](git-smart-commit/SKILL.md)
- [database-query-guide](database-query-guide/SKILL.md)
- [maximo-helper](maximo-helper/SKILL.md)
- [ax-dynamics-helper](ax-dynamics-helper/SKILL.md)
- [sql-analyzer](sql-analyzer/SKILL.md)
- [fabric-helper](fabric-helper/SKILL.md)
- [api-test-gen](api-test-gen/SKILL.md)
- [pr-summary](pr-summary/SKILL.md)
- [daily-standup](daily-standup/SKILL.md)
- [refactor-suggest](refactor-suggest/SKILL.md)
- [chrome-data-extract](chrome-data-extract/SKILL.md)
- [cipher-memory](cipher-memory/SKILL.md)
- [project-scaffold](project-scaffold/SKILL.md)
- [dockerfile-generator](dockerfile-generator/SKILL.md)
- [github-actions](github-actions/SKILL.md)
- [implementation-plan](implementation-plan/SKILL.md)
- [adr-generator](adr-generator/SKILL.md)

External resources:
- Agent Skills for Context Engineering repository
- MCP Gateway documentation
- Claude Code documentation

---

## Skill Metadata

**Created**: 2025-12-19
**Last Updated**: 2025-12-22
**Author**: Abdullah
**Version**: 2.0.0
