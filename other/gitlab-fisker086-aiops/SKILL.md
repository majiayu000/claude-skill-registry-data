---
name: gitlab
description: Query GitLab projects, merge requests, and CI pipelines
activation_keywords: [gitlab, project, pipeline, mr, merge, ci, repository]
execution_mode: server
---

# GitLab Skill

Provides read-only GitLab operations via HTTP API:
- List projects and get project details
- List merge requests and their changes
- List CI pipelines and jobs
- Get job logs
- List repository branches and tags

Use `builtin_gitlab` tool with fields:
- `operation`: one of "list_projects", "get_project", "list_mrs", "list_pipelines", "get_job_log", "list_branches", "list_tags"
- `project_id`: GitLab project ID or URL-encoded path (required for most ops)
- `gitlab_url`: GitLab instance URL (default: https://gitlab.com)
- `token`: GitLab personal access token (from GITLAB_TOKEN env var if not provided)
- `mr_iid`: merge request IID (for pipeline listing)
- `pipeline_id`: pipeline ID (for get_job_log)
- `per_page`: results per page (default: 20)

Note: All operations are read-only.
The token is used only for this request and never logged.
