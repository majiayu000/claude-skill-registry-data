---
name: approvals
description: Control-plane approval workflow for new group participation. Use when a new group/chat interaction appears and explicit approval is required before participating.
---

# Approvals (Control Plane Policy)

## Purpose
Prevent unintended participation in new group chats.

## Policy
- Never participate in a new group unless Matthew gives formal approval in Telegram group `MEK`, topic 1 (control-plane thread).
- If a request arrives from an unapproved group:
  1. Do not continue conversation in that group.
  2. Notify Matthew in control-plane with concise details.
  3. Ask for explicit approval (`Approved`/`Denied`).
  4. If approved, allow participation in that specific group.
  5. If denied, block that requesting group.

## Operating notes
- Keep wildcard discovery enabled if requested by Matthew.
- Use control-plane as the single source of truth for approvals.
- Record durable policy in USER.md/AGENTS.md.
