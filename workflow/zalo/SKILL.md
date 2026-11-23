---
name: zalo
description: OpenClaw skill for Zalo Bot API workflows (bot token) plus optional guidance on unofficial personal automation tools.
---

# Zalo Bot Skill (Advanced)

## Purpose
Provide a production-oriented guide for Zalo Bot API workflows (token-based), with a separate, clearly marked branch for unofficial personal automation tools.

## Best fit
- You use the Zalo Bot Platform / bot token path.
- You need clear webhook or long-polling handling.
- You want professional conversation UX guidance.

## Not a fit
- You require guaranteed, officially supported personal-account automation.
- You need rich media streaming or advanced file pipelines.

## Quick orientation
- Read `references/zalo-bot-overview.md` for platform scope and constraints.
- Read `references/zalo-bot-token-and-setup.md` for token setup and connection flow.
- Read `references/zalo-bot-messaging-capabilities.md` for capability checklist.
- Read `references/zalo-bot-ux-playbook.md` for UX and conversation patterns.
- Read `references/zalo-bot-webhook-routing.md` for webhook/polling handling.
- Read `references/zalo-personal-zca-js.md` for the unofficial personal-account branch.
- Read `references/zalo-n8n-automation.md` for automation notes and cautions.

## Required inputs
- Bot token and bot configuration.
- Target workflow (notify, support, broadcast).
- Delivery model (webhook or polling).

## Expected output
- A clear bot workflow plan, method checklist, and operational guardrails.

## Operational notes
- Validate inbound events and handle retries safely.
- Keep replies concise; rate-limit outgoing messages.
- Prefer explicit allowlists for any automation flow.

## Security notes
- Never log tokens or credentials.
- Treat all state files and cookies as secrets.
