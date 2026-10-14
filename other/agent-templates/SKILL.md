---
name: agent-templates
description: Guided agent setup from templates — business assistants, security, agents. Triggers on "create an agent for my [business/task]", "set up security", "I want an assistant", or any request to create a specialized agent.
metadata: { "nyxclaw": { "emoji": "🤖" } }
---

# Agent Templates

Guided flow to create a fully configured agent from a template. The gateway handles all programmatic configuration — you only need to identify the template, confirm with the user, and run one create command.

## Flow

1. **Identify template**
   Ask the user what type of agent they need, or detect from context.
   Available template slugs:

   **Business:**
   · `dental-clinic` — Dental clinic / medical office
   · `law-firm` — Law firm / legal consultancy
   · `online-store` — E-commerce / online store
   · `restaurant` — Restaurant / cafe / food service
   · `real-estate` — Real estate agency / property management
   · `hair-salon` — Hair salon / beauty studio
   · `gym-fitness` — Gym / fitness center
   · `hotel` — Hotel / accommodation / hospitality
   · `accounting-firm` — Accounting / tax firm / consultancy
   · `content-creator` — AI YouTuber / autonomous content creator

   **Operations:**
   · `security-guard` — Gateway security monitoring + audit automation
   · `seo-specialist` — Site audits, keyword tracking, ranking monitoring

   If no template matches, build a custom setup by asking what the agent should do.

2. **Create agent — ONE call, no extra questions**
   Do NOT ask for confirmation or name preference — use the template's default name and create immediately.
   `config_manage agents create "{name}" section={templateSlug}`
   Example: `config_manage agents create "SEO Specialist" section=seo-specialist`

   IMPORTANT: Do NOT read the template file. The gateway reads and applies it automatically.
   One call does everything: name, description (Purpose in SOUL.md), toolProfile, alsoAllow, deny, A2A wiring, skills installation.
   The response confirms what was applied (toolProfile, autoConfig, skills.installed).

3. **Summary**
   Show what was configured based on the create response. Mention that channels, services, and cron can be added later.

4. **Optional follow-up** (only if user asks)
   · Channels: `config_manage channels {channel} setup`
   · Services: `config_manage services {name}`
   · Cron: `config_manage cron add`

## Important: Setup Context

The entire setup runs from Nyx's main session. Channels and services are gateway-level shared infrastructure, not per-agent. If WhatsApp is already connected, the new agent can use it too.

## Safety Rules

- NEVER auto-connect services without explicit user approval
- Let the user skip any step; the setup can be completed incrementally

## Custom Setup

If no template matches, ask:

1. What should this agent do?
2. What tools does it need?
3. Should it run scheduled tasks?

Then create manually: `config_manage agents create "{name}" path="{description}"`

## After Setup

Remind the user they can:

- Modify the agent: `config_manage agents update "{name}" ...`
- Add channels later: `config_manage channels {channel} setup`
- Add services later: `config_manage services {name}`
- View current config: `config_manage view`
