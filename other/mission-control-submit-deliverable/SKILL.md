---
name: mission-control-submit-deliverable
description: >-
  Submits finished work to Mission Control as content drops and posts progress
  to task threads. Use this skill when a piece of work is complete and needs
  human review, or when you should communicate progress, questions, or
  artifacts on a task — don't just complete tasks; submit the actual work.
version: 1.0.0
owner: software-factory
risk: low
capabilities:
  - content-drops
  - thread-messages
  - artifact-sharing
  - progress-reporting
requires_tools:
  - convex
related_skills:
  - mission-control-task-lifecycle
  - mission-control-run-logging
---

# Submit Content Drops (Deliverables)

When you've completed work, submit it as a content drop for human review.

```
Mutation: api.contentDrops.submit
Args:
  title: string
  contentType: "BLOG_POST" | "SOCIAL_POST" | "EMAIL_DRAFT" | "SCRIPT" |
               "REPORT" | "CODE_SNIPPET" | "DESIGN" | "OTHER"
  content: string        — The actual deliverable content
  summary?: string       — Brief summary of the work
  agentId?: Id<"agents"> — Your agent ID
  taskId?: Id<"tasks">   — Related task (if any)
  projectId?: Id<"projects">
  fileUrl?: string       — Link to external file if applicable
  tags?: string[]
```

Content drops appear in the Content Pipeline view's "Drops" tab, where humans can approve, reject, or publish them.

## Post Messages to Task Threads

Communicate progress, ask questions, or share artifacts on task threads.

```
Mutation: api.messages.create
Args:
  taskId: Id<"tasks">
  authorType: "AGENT"
  authorAgentId: Id<"agents">
  type: "COMMENT" | "WORK_PLAN" | "PROGRESS" | "ARTIFACT" | "REVIEW"
  content: string
  idempotencyKey?: string
  artifacts?: Array<{ name: string, type: string, url?: string, content?: string }>
```

## Rules

1. **Submit deliverables as content drops** — don't just complete tasks; submit the actual work.
2. Post a `WORK_PLAN` message when you start, `PROGRESS` messages as you go, and an `ARTIFACT` or `REVIEW` message when done.
3. After submitting the drop, transition the task to REVIEW (`mission-control-task-lifecycle`).
