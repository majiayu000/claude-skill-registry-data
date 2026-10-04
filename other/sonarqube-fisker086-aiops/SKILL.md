---
name: sonarqube
description: Query SonarQube code quality metrics and issues
activation_keywords: [sonarqube, sonar, code quality, lint, coverage, bug, vulnerability]
execution_mode: server
---

# SonarQube Skill

Provides read-only SonarQube operations via HTTP API:
- List projects and their quality gate status
- Get code quality metrics (bugs, vulnerabilities, code smells, coverage)
- List issues with filters
- Get quality gate details
- List project measures

Use `builtin_sonarqube` tool with fields:
- `operation`: one of "list_projects", "project_status", "metrics", "list_issues", "quality_gate", "measures"
- `project_key`: SonarQube project key (required for project_status/metrics/list_issues/measures)
- `sonarqube_url`: SonarQube server URL (default: http://localhost:9000)
- `token`: SonarQube authentication token (from SONAR_TOKEN env var if not provided)
- `severity`: filter issues by severity (INFO, MINOR, MAJOR, CRITICAL, BLOCKER)
- `types`: filter issues by type (BUG, VULNERABILITY, CODE_SMELL)
- `per_page`: results per page (default: 20)

Note: All operations are read-only.
The token is used only for this request and never logged.
