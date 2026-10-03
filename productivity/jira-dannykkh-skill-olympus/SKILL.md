---
name: jira
description: "Use for Jira issues/tickets, sprint/backlog workflow, create/view/update requests, or issue keys like PROJ-123."
---

# Jira

Natural language interaction with Jira. Supports multiple backends.

## Setup (최초 1회)

이 스킬은 `config.json`에 설정이 필요합니다.

1. `config.json`을 읽는다 (`skills/jira/config.json` 또는 현재 CLI의 글로벌 스킬 경로)
2. 빈 필드가 있으면 현재 CLI의 질문 방식으로 사용자에게 질문한다
3. 답변을 `config.json`에 저장한다
4. 이후 실행 시에는 `config.json`에서 자동으로 읽는다

| 항목 | 설명 | 예시 |
|------|------|------|
| `jira_base_url` | Jira 인스턴스 URL | `https://mycompany.atlassian.net` |
| `default_project_key` | 기본 프로젝트 키 (이슈 생성 시 자동 사용) | `PROJ` |
| `default_assignee` | 기본 담당자 (본인 Jira 사용자명) | `john.doe` |
| `preferred_issue_types` | 주로 사용하는 이슈 타입 목록 | `["Story", "Bug", "Task"]` |

**Setup 로직:**

```
config.json 읽기
  ├─ jira_base_url 비어있음? → "Jira 인스턴스 URL을 입력해주세요 (예: https://mycompany.atlassian.net)"
  ├─ default_project_key 비어있음? → "기본 프로젝트 키를 입력해주세요 (예: PROJ, 건너뛰려면 Enter)"
  ├─ default_assignee 비어있음? → "기본 담당자(본인 Jira 사용자명)를 입력해주세요 (건너뛰려면 Enter)"
  └─ 답변 수집 후 config.json에 저장 → 이후 자동 사용
```

> **모든 필드가 채워져 있으면 이 단계를 건너뜁니다.**

---

## Backend Detection

**Run this check first** to determine which backend to use:

```
1. Check if jira CLI is available:
   → Run: which jira
   → If found: USE CLI BACKEND

2. If no CLI, check for Atlassian MCP:
   → Look for mcp__atlassian__* tools
   → If available: USE MCP BACKEND

3. If neither available:
   → GUIDE USER TO SETUP
```

| Backend | When to Use | Reference |
|---------|-------------|-----------|
| **CLI** | `jira` command available | `references/commands.md` |
| **MCP** | Atlassian MCP tools available | `references/mcp.md` |
| **None** | Neither available | Guide to install CLI |

---

## Quick Reference (CLI)

> Skip this section if using MCP backend.

| Intent | Command |
|--------|---------|
| View issue | `jira issue view ISSUE-KEY` |
| List my issues | `jira issue list -a$(jira me)` |
| My in-progress | `jira issue list -a$(jira me) -s"In Progress"` |
| Create issue | `jira issue create -tType -s"Summary" -b"Description"` |
| Move/transition | `jira issue move ISSUE-KEY "State"` |
| Assign to me | `jira issue assign ISSUE-KEY $(jira me)` |
| Unassign | `jira issue assign ISSUE-KEY x` |
| Add comment | `jira issue comment add ISSUE-KEY -b"Comment text"` |
| Open in browser | `jira open ISSUE-KEY` |
| Current sprint | `jira sprint list --state active` |
| Who am I | `jira me` |

---

## Quick Reference (MCP)

> Skip this section if using CLI backend.

| Intent | MCP Tool |
|--------|----------|
| Search issues | `mcp__atlassian__searchJiraIssuesUsingJql` |
| View issue | `mcp__atlassian__getJiraIssue` |
| Create issue | `mcp__atlassian__createJiraIssue` |
| Update issue | `mcp__atlassian__editJiraIssue` |
| Get transitions | `mcp__atlassian__getTransitionsForJiraIssue` |
| Transition | `mcp__atlassian__transitionJiraIssue` |
| Add comment | `mcp__atlassian__addCommentToJiraIssue` |
| User lookup | `mcp__atlassian__lookupJiraAccountId` |
| List projects | `mcp__atlassian__getVisibleJiraProjects` |

See `references/mcp.md` for full MCP patterns.

---

## Triggers

- "create a jira ticket"
- "show me PROJ-123"
- "list my tickets"
- "move ticket to done"
- "what's in the current sprint"

---

## Issue Key Detection

Issue keys follow the pattern: `[A-Z]+-[0-9]+` (e.g., PROJ-123, ABC-1).

When a user mentions an issue key in conversation:
- **CLI:** `jira issue view KEY` or `jira open KEY`
- **MCP:** `mcp__atlassian__jira_get_issue` with the key

---

## Workflow

**Creating tickets:**
1. Research context if user references code/tickets/PRs
2. Draft ticket content
3. Review with user
4. Create using appropriate backend

**Updating tickets:**
1. Fetch issue details first
2. Check status (careful with in-progress tickets)
3. Show current vs proposed changes
4. Get approval before updating
5. Add comment explaining changes

---

## Before Any Operation

Ask yourself:

1. **What's the current state?** — Always fetch the issue first. Don't assume status, assignee, or fields are what user thinks they are.

2. **Who else is affected?** — Check watchers, linked issues, parent epics. A "simple edit" might notify 10 people.

3. **Is this reversible?** — Transitions may have one-way gates. Some workflows require intermediate states. Description edits have no undo.

4. **Do I have the right identifiers?** — Issue keys, transition IDs, account IDs. Display names don't work for assignment (MCP).

---

## NEVER

- **NEVER transition without fetching current status** — Workflows may require intermediate states. "To Do" → "Done" might fail silently if "In Progress" is required first.

- **NEVER assign using display name (MCP)** — Only account IDs work. Always call `lookupJiraAccountId` first, or assignment silently fails.

- **NEVER edit description without showing original** — Jira has no undo. User must see what they're replacing.

- **NEVER use `--no-input` without all required fields (CLI)** — Fails silently with cryptic errors. Check project's required fields first.

- **NEVER assume transition names are universal** — "Done", "Closed", "Complete" vary by project. Always get available transitions first.

- **NEVER bulk-modify without explicit approval** — Each ticket change notifies watchers. 10 edits = 10 notification storms.

---

## Safety

- Always show the command/tool call before running it
- Always get approval before modifying tickets
- Preserve original information when editing
- Verify updates after applying
- Always surface authentication issues clearly so the user can resolve them

---

## No Backend Available

If neither CLI nor MCP is available, guide the user:

```
To use Jira, you need one of:

1. **jira CLI** (recommended):
   https://github.com/ankitpokhrel/jira-cli

   Install: brew install ankitpokhrel/jira-cli/jira-cli
   Setup:   jira init

2. **Atlassian MCP**:
   Configure in your MCP settings with Atlassian credentials.
```

---

## Deep Dive

**LOAD reference when:**
- Creating issues with complex fields or multi-line content
- Building JQL queries beyond simple filters
- Troubleshooting errors or authentication issues
- Working with transitions, linking, or sprints

**Do NOT load reference for:**
- Simple view/list operations (Quick Reference above is sufficient)
- Basic status checks (`jira issue view KEY`)
- Opening issues in browser

| Task | Load Reference? |
|------|-----------------|
| View single issue | No |
| List my tickets | No |
| Create with description | **Yes** — CLI needs `/tmp` pattern |
| Transition issue | **Yes** — need transition ID workflow |
| JQL search | **Yes** — for complex queries |
| Link issues | **Yes** — MCP limitation, need script |

References:
- CLI patterns: `references/commands.md`
- MCP patterns: `references/mcp.md`
