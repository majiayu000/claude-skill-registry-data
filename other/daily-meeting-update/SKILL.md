---
name: daily-meeting-update
description: "Generate interactive daily standup/status updates from GitHub, Jira, and AI session history; use for daily, standup, scrum, status update, yesterday/today/blockers, or team sync."
---

# Daily Meeting Update

Generate a daily standup/meeting update through an **interactive interview**. Never assume tools are configured—ask first.

---

## Setup (최초 1회)

이 스킬은 `config.json`에 설정이 필요합니다.

1. `config.json`을 읽는다 (`skills/daily-meeting-update/config.json` 또는 현재 CLI의 글로벌 스킬 경로)
2. 빈 필드가 있으면 현재 CLI의 질문 방식으로 사용자에게 질문한다
3. 답변을 `config.json`에 저장한다
4. 이후 실행 시에는 `config.json`에서 자동으로 읽는다

| 항목 | 설명 | 예시 |
|------|------|------|
| `github_username` | GitHub 사용자명 (GitHub 연동 시 자동 필터링에 사용) | `octocat` |
| `jira_project_key` | 기본 Jira 프로젝트 키 | `PROJ` |
| `slack_channel` | 스탠드업 결과를 공유할 Slack 채널 | `#daily-standup` |
| `standup_format` | 출력 형식 (`markdown` / `plain`) | `markdown` |
| `language` | 업데이트 생성 언어 (`ko` / `en`) | `ko` |

**Setup 로직:**

```
config.json 읽기
  ├─ github_username 비어있음? → "GitHub 사용자명을 입력해주세요 (건너뛰려면 Enter)"
  ├─ jira_project_key 비어있음? → "기본 Jira 프로젝트 키를 입력해주세요 (예: PROJ, 없으면 Enter)"
  ├─ slack_channel 비어있음? → "스탠드업을 공유할 Slack 채널을 입력해주세요 (예: #daily-standup, 없으면 Enter)"
  └─ 답변 수집 후 config.json에 저장 → 이후 자동 사용
```

> **모든 필드가 채워져 있으면 이 단계를 건너뜁니다.**

---

## Workflow

```
START
  │
  ▼
┌─────────────────────────────────────────────────────┐
│ Phase 1: DETECT & OFFER INTEGRATIONS                │
│ • Check: Claude Code history? gh CLI? jira CLI?     │
│ • Claude Code → Pull yesterday's session digest     │
│   → User selects relevant items by numbered list    │
│ • GitHub/Jira → Ask user, pull if approved          │
│ • Pull data NOW (before interview)                  │
├─────────────────────────────────────────────────────┤
│ Phase 2: INTERVIEW (with insights)                  │
│ • Show pulled data as context                       │
│ • Yesterday: "I see you merged PR #123, what else?" │
│ • Today: What will you work on?                     │
│ • Blockers: Anything blocking you?                  │
│ • Topics: Anything to discuss at end of meeting?    │
├─────────────────────────────────────────────────────┤
│ Phase 3: GENERATE UPDATE                            │
│ • Combine interview answers + tool data             │
│ • Format as clean Markdown                          │
│ • Present to user                                   │
└─────────────────────────────────────────────────────┘
```

---

## Phase 1: Detect & Offer Integrations

### Step 1: Silent Detection

Check for available integrations **silently** (suppress errors, don't show to user):

| Integration | Detection |
|-------------|-----------|
| **Claude Code History** | Claude transcript directory exists with `.jsonl` files |
| **Codex/Antigravity Project History** | `conversations/*-codex.md` or `conversations/*-antigravity.md` exists; `*-gemini.md` is legacy history only |
| GitHub CLI | `gh auth status` succeeds |
| Jira CLI | `jira` command exists |
| Atlassian MCP | `mcp__atlassian__*` tools available |
| Git | Inside a git repository |

### Step 2: Offer GitHub/Jira Integrations (if available)

> Claude Code: use a structured question UI when available.
> Codex/Antigravity: use plain-text questions and concise numbered options.

**GitHub/Git:**

If `HAS_GH` or `HAS_GIT`:

```
"I detected you have GitHub/Git configured. Want me to pull your recent activity (commits, PRs, reviews)?"

Options:
- "Yes, pull the info"
- "No, I'll provide everything manually"
```

If yes:

```
"Which repositories/projects should I check?"

Options:
- "Just the current directory" (if in a git repo)
- "I'll list the repos" → user provides list
```

**Jira:**

If `HAS_JIRA_CLI` or `HAS_ATLASSIAN_MCP`:

```
"I detected you have Jira configured. Want me to pull your tickets?"

Options:
- "Yes, pull my tickets"
- "No, I'll provide everything manually"
```

### Step 3: Pull GitHub/Jira Data (if approved)

**GitHub/Git** — For each approved repo:
- Commits by user since yesterday
- PRs opened/merged by user
- Reviews done by user

**Jira** — Tickets assigned to user, updated in last 24h

**Key insight**: Store results to use as context in Phase 2 interview.

### Step 4: Offer AI Session History

This integration captures everything you worked on with Claude Code — useful for recalling work that isn't in git or Jira.

**Detection:**
```bash
ls ~/.claude/projects/*/*.jsonl 2>/dev/null | head -1
```

**If Claude Code history exists, ask:**

```
"I can also pull your Claude Code session history from yesterday. This can help recall work that isn't in git/Jira (research, debugging, planning). Want me to check?"

Options:
- "Yes, pull my Claude Code sessions"
- "No, I have everything I need"
```

**If yes, resolve `module_root` from the exact loaded `SKILL.md` and run the bundled digest script:**

```bash
python3 "<module_root>/scripts/claude_digest.py" --format json
```

**Then present sessions with numbered selection:**

Use a structured multi-select UI if the runtime provides one; otherwise list the items in plain text and ask the user to reply with the relevant numbers:

```
"Here are your Claude Code sessions from yesterday. Select the ones relevant to your standup:"

Options:
- "Fix authentication bug (backend-api)"
- "Implement OAuth flow (backend-api)"
- "Update homepage styles (frontend-app)"
- "Research payment providers (docs)"
```

**Key insight:** User selects which sessions are work-related. Personal projects or experiments can be excluded.

**Do NOT run digest script when:**
- User explicitly says "No" to Claude Code history
- User says they'll provide everything manually
- Claude transcript directory doesn't exist

**Codex/Antigravity fallback:**

- If Claude history is unavailable but `conversations/*-codex.md` or `conversations/*-antigravity.md` exists, read the previous day's project conversation file directly. Read `*-gemini.md` only as legacy history.
- Summarize relevant work items from that file in plain text.
- Ask the user to confirm which items belong in the standup; do not require structured multi-selection UI.

**If digest script fails:**
- Fallback: Skip Claude Code integration silently, proceed with interview
- Common issues: Python not installed, no sessions from yesterday, permission errors
- Do NOT block the standup flow — the script is supplemental, not required

---

## Phase 2: Interview (with insights)

> Claude Code: use a structured question UI for better UX.
> Codex/Antigravity: ask the same questions in plain text and keep options short.

**Use pulled data as context** to make questions smarter.

### Question 1: Yesterday

**If data was pulled**, show it first:

```
"Here's what I found from your activity:
- Merged PR #123: fix login timeout
- 3 commits in backend-api
- Reviewed PR #456 (approved)

Anything else you worked on yesterday that I missed?"
```

**If no data pulled:**

```
"What did you work on yesterday/since the last standup?"
```

If user response is vague, ask follow-up:
- "Can you give more details about X?"
- "Did you complete anything specific?"

### Question 2: Today

```
"What will you work on today?"

Options:
- [Text input - user types freely]
```

**If Jira data was pulled**, you can suggest:

```
"I see you have these tickets assigned:
- PROJ-123: Implement OAuth flow (In Progress)
- PROJ-456: Fix payment bug (To Do)

Will you work on any of these today?"
```

### Question 3: Blockers

```
"Do you have any blockers or impediments?"

Options:
- "No blockers"
- "Yes, I have blockers" → follow-up for details
```

### Question 4: Topics for Discussion

```
"Any topic you want to bring up at the end of the daily?"

Options:
- "No, nothing to discuss"
- "Yes" → follow-up for details

Examples of topics:
- Technical decision that needs input
- Alignment with another team
- Question about prioritization
- Announcement or info for the team
```

---

## Phase 3: Generate Update

Combine all information into clean Markdown:

```markdown
# Daily Update - [DATE]

## Yesterday
- [Items from interview]
- [Items from GitHub/Jira if pulled]

## Today
- [Items from interview]

## Blockers
- [Blockers or "No blockers"]

## PRs & Reviews (if pulled from GitHub)
- [PRs opened]
- [PRs merged]
- [Reviews done]

## Jira (if pulled from Jira)
- [Tickets updated]

## Topics for Discussion
- [Topics or "None"]

---
*Links:*
- [PR links]
- [Ticket links]
```

---

## Core Principles

1. **Interview is primary** — Tools supplement, they don't replace human context
2. **Consent before access** — Always ask before pulling from any integration
3. **Context-aware questions** — Show pulled data during interview to trigger memory ("I see you merged PR #123...")

---

## Quick Reference

| Phase | Action | Tool |
|-------|--------|------|
| 1. Detect & Offer | Check gh/jira/claude history, ask user, pull data | Bash (silent), structured question UI* |
| 2. Interview | Ask 4 questions with insights | structured question UI* |
| 3. Generate | Format Markdown | Output text |

*Structured question UI is an optional UX enhancement, not a requirement for the workflow.

### Claude Code Digest Script

```bash
# Get yesterday's sessions as JSON
python3 skills/daily-meeting-update/scripts/claude_digest.py --format json

# Get today's sessions
python3 skills/daily-meeting-update/scripts/claude_digest.py --date today --format json

# Filter to specific project
python3 skills/daily-meeting-update/scripts/claude_digest.py --project ~/my-app --format json
```

---

## Example Session

```
Claude: "Let's prepare your daily! I detected GitHub configured. Want me to pull your recent activity?"
User: "Yes"

Claude: "Which repos should I check?"
User: "backend-api and frontend-app"

[Claude pulls GitHub data silently]

Claude: "I can also pull your Claude Code session history from yesterday. Want me to check?"
User: "Yes"

[Claude runs digest script, gets 5 sessions]

Claude: "Here are your Claude Code sessions from yesterday. Select the ones relevant to your standup:"
  ☑ Fix authentication timeout bug (backend-api)
  ☑ Implement OAuth flow (backend-api)
  ☐ Update personal blog (blog) - [user unchecks personal project]
  ☑ Research payment providers (docs)
  ☐ Debugging test failures (experiments)

User: [selects 3 relevant items]

Claude: "Here's what I found from your activity:
- Merged PR #120: fix login timeout
- Opened PR #125: feat: add OAuth flow
- Reviewed PR #123 (approved), PR #456 (changes requested)
- 5 commits in backend-api
- [From Claude Code] Fix authentication timeout bug
- [From Claude Code] Implement OAuth flow
- [From Claude Code] Research payment providers

Anything else you worked on yesterday that I missed?"
User: "No, that covers it"

Claude: "What will you work on today?"
User: "Continue the OAuth feature and deploy to staging"

Claude: "Any blockers?"
User: "No"

Claude: "Any topic to bring up at the end of the daily?"
User: "Yes, I want to discuss the architecture of the new payments module"

[Claude generates update]
```

---

## Output Example

```markdown
# Daily Update - 2026-01-22

## Yesterday
- Worked on authentication feature
- Research on payment providers
- Merged PR #120 (fix: login timeout)
- Opened PR #125 (feat: add OAuth flow)

## Today
- Continue OAuth feature
- Deploy to staging

## Blockers
- No blockers

## PRs & Reviews
- **Opened:** PR #125 - feat: add OAuth flow
- **Merged:** PR #120 - fix: login timeout
- **Reviews:** PR #123 (approved), PR #456 (changes requested)

## Topics for Discussion
- Architecture of the new payments module

---
*Links:*
- https://github.com/org/repo/pull/125
- https://github.com/org/repo/pull/120
```

---

## Anti-Patterns

| Avoid | Why (Expert Knowledge) | Instead |
|-------|------------------------|---------|
| Run gh/jira without asking | Users may have personal repos visible, or be in a sensitive project context they don't want exposed | Always ask first, let user choose repos |
| Assume current directory is the only project | Developers often work on 2-5 repos simultaneously (frontend, backend, infra) | Ask "Which projects are you working on?" |
| Skip interview even with tool data | Tools capture WHAT happened but miss WHY and context (research, meetings, planning) | Interview is primary, tools supplement |
| Generate update before all 4 questions | User might have critical blocker or discussion topic that changes the narrative | Complete interview, then generate |
| Include raw commit messages | Commit messages are often cryptic ("fix", "wip") and don't tell the story | Summarize into human-readable outcomes |
| Ask for data after interview | Showing insights during interview makes questions smarter ("I see you merged PR #123, anything else?") | Pull data first, then interview with context |

---

## NEVER

- **NEVER assume tools are configured** — Many devs have gh installed but not authenticated, or jira CLI pointing to wrong instance
- **NEVER skip the "Topics for Discussion" question** — This is often the most valuable part of standup that tools can't capture
- **NEVER generate more than 15 bullets** — Standup should be <2 minutes to read; long updates lose the audience
- **NEVER include ticket/PR numbers without context** — "PROJ-123" means nothing; always include title or summary
- **NEVER pull data from repos user didn't explicitly approve** — Even if you can see other repos, respect boundaries
