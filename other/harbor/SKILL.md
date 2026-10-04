---
name: harbor
description: Query Harbor container image registry projects and artifacts
activation_keywords: [harbor, registry, container, image, artifact, docker]
execution_mode: server
---

# Harbor Skill

Provides read-only Harbor registry operations via REST API:
- List projects and their metadata
- List repositories within a project
- List artifacts (tags) for a repository
- Get artifact details (digest, size, os, vuln status)
- List robot accounts
- Get system info and status

Use `builtin_harbor` tool with fields:
- `operation`: one of "list_projects", "list_repos", "list_artifacts", "get_artifact", "system_info", "list_robot_accounts"
- `project`: project name (required for list_repos/list_robot_accounts)
- `repository`: repository name (required for list_artifacts/get_artifact)
- `artifact`: artifact reference (tag or digest, required for get_artifact)
- `harbor_url`: Harbor server URL (default: http://localhost:80)
- `username`: Harbor username (from HARBOR_USERNAME env var if not provided)
- `password`: Harbor password or API token (from HARBOR_PASSWORD env var if not provided)
- `per_page`: results per page (default: 20)

Note: All operations are read-only.
Credentials are used only for this request and never logged.
