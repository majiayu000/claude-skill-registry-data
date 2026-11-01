---
name: lofy
description: Personal AI chief of staff — a complete life management system for OpenClaw. Proactive morning briefings, evening reviews, weekly reports, fitness tracking, career management, project tracking, smart home control, and brain-inspired memory architecture. Use when setting up a personal AI assistant that manages your entire life through natural conversation across Telegram, WhatsApp, Discord, or any OpenClaw channel.
metadata: {"minis":{"originalSource":"https://clawskills.sh/skills/harrey401-lofy","convertedAt":"2026-10-31T22:12:16.695Z","license":"Unknown"}}
---

# Lofy — Personal AI Life System

A skill pack that turns OpenClaw into a proactive personal AI chief of staff. Not a chatbot — a system that manages your calendar, tracks your goals, nudges you when you're slacking, and stays out of your way when you're locked in.

## Quick Start

After installing, copy the template files into your workspace:

```bash
cp -r skills/lofy/assets/templates/* .
```

Then customize:
1. Edit `USER.md` with your info (name, timezone, goals)
2. Edit `IDENTITY.md` if you want to rename your agent
3. Edit `HEARTBEAT.md` to set your check priorities
4. Create `data/` directory and initialize data files (templates provided)
5. Set up cron jobs for briefings (see Scheduling below)

## Architecture

Lofy is a **single-agent system** with modular skill domains. One agent handles everything with shared context — lower token cost, no routing overhead, better cross-domain awareness.

### Core Files (copy to workspace root)
- `AGENTS.md` — Agent behavior rules, safety, memory protocol
- `SOUL.md` — Personality and tone (customize this!)
- `IDENTITY.md` — Name and avatar
- `USER.md` — Your profile (name, timezone, preferences)
- `HEARTBEAT.md` — Proactive check schedule
- `MEMORY_SYSTEM.md` — Memory architecture rules

### Data Files (create in `data/`)
- `goals.json` — Life goals, habits, streaks
- `fitness.json` — Workouts, meals, PRs
- `applications.json` — Job application pipeline
- `projects.json` — Project status and milestones
- `home-config.json` — Smart home scenes and devices

## Skill Domains

Each domain is a sub-skill. Install all or pick what you need:

| Skill | What it does |
|-------|-------------|
| `lofy-life-coach` | Morning briefings, evening reviews, goal tracking, habit accountability |
| `lofy-fitness` | Workout logging, meal tracking, PR detection, gym nudges |
| `lofy-career` | Job search, application tracking, resume tailoring, interview prep |
| `lofy-projects` | Project management, priority engine, meeting prep, deadline tracking |
| `lofy-home` | Smart home scenes, device control via Home Assistant |

## Memory System

Brain-inspired 5-layer architecture. See `references/memory-system.md` for full details.

1. **Working Memory** — Current conversation context
2. **Short-Term** — Daily logs (`memory/YYYY-MM-DD.md`), 14-day lifecycle
3. **Long-Term Declarative** — `MEMORY.md`, max 100 lines, curated
4. **Long-Term Procedural** — Profile files, skills, project knowledge
5. **Salience Tagging** — Important events get preserved, noise decays

Key rules:
- Daily logs auto-compress after 1 week
- Extract insights to MEMORY.md after 2 weeks, then delete raw logs
- "Remember this" = permanent, tagged `[PINNED]`
- MEMORY.md never loads in shared/group contexts (security)

## Scheduling

Set up these cron jobs for full functionality:

```
Morning Briefing  — daily at your wake time (e.g., 10 AM)
Evening Review     — daily at wind-down time (e.g., 9 PM)
Weekly Review      — Sunday evening (e.g., 7 PM)
```

Use `openclaw cron` or the cron tool to create these. Each should be an `agentTurn` in an isolated session with delivery to your primary channel.

### Heartbeat
Configure heartbeat polling (every 30 min) for proactive checks:
- Unread emails
- Upcoming calendar events
- Overdue follow-ups
- Approaching deadlines

## Customization

### Personality
Edit `SOUL.md` to match your vibe. The default is direct, casual, and competent. Make it yours.

### Integrations
Lofy works best with these tools (configure in `TOOLS.md`):
- **Google Workspace** — Gmail, Calendar (via `gog` CLI or API)
- **Spotify** — Music control (via `spogo` CLI or API)
- **Home Assistant** — Smart home (requires HA instance)
- **Browser** — Job search, restaurant bookings, web research

### Profile System
Create `profile/` directory with:
- `career.md` — Skills, experience, target roles
- `projects.md` — Active project details
- `body.md` — Fitness stats and goals
- `personality.md` — Interests, preferences, communication style

These are living documents the agent updates as it learns about you.

## Design Principles

1. **Be helpful, not performative** — Skip filler, just do the work
2. **Have opinions** — Disagree when warranted, suggest improvements
3. **Resourceful before asking** — Look it up, read the file, then ask if stuck
4. **Respect privacy** — Never leak personal data in group chats
5. **Earn trust through competence** — Be careful externally, bold internally
