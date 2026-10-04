---
name: skill-master
description: |-
  Startup skill router: maps any incoming request to the correct skill using Quick Lookup table
  and _manifest.json. Loaded automatically at session start.
  Triggers on: every new request — this is the dispatch layer, not a user-facing skill.
  NOT for: executing tasks directly — always routes to a domain-specific skill.
---

# Skill Master

## How to Use
1. Read the request
2. Match in **Quick Lookup** below
3. Not found? Check `skills/_manifest.json` (lightweight — name + description + triggers for all active skills)
4. Still not found? Read `skills/skill-master/REFERENCE.md` for decision tree
5. Log the selection (see Analytics below), then load that skill's SKILL.md

Do not load REFERENCE.md or full SKILL.md files unless the manifest and Quick Lookup both miss.
Do not improvise. No match anywhere? Ask the owner.

## Proactive Skill Suggestion (inspired by gstack)
Don't just route reactively. When you detect these patterns, **suggest** the relevant skill:
- Owner reports an error/bug -> suggest self-monitor + investigate flow
- Repeated corrections on same topic -> suggest self-learning review
- End of work week -> suggest weekly retro
- Memory files growing large -> suggest memory-tiering compaction
- Multiple cron failures -> suggest self-monitor with root-cause analysis
- Owner asks "what's happening" -> suggest supervisor
- Dangerous command about to run -> invoke guard checks from self-monitor

## Production Rules (Always Active)
- React 👍 when receiving task from owner, ✅ when done
- "my pleasure / you're welcome" when anyone says "thank you"
- NO_REPLY for casual PA acks (thumbs up, "got it", "thank you") unless directly asked
- PA contacts: read from `PA_LIST.md`
- Google Calendar: use `/path/to/openclaw/.gog/credentials.json` (NOT gog CLI)

## Analytics — Log Every Skill Use
```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"SKILL_NAME\",\"trigger\":\"TRIGGER\",\"context\":\"CONTEXT\"}" \
  >> /path/to/workspace/data/skill-analytics.jsonl
```

## Quick Lookup

| If the owner says... | Use skill |
|---|---|
| "who is X" / "phone for X" / "email of X" / "address of X" | contact-list |
| "PA of X" / "X's PA" / "JID of X" | contact-list |
| "add contact" / "update contact" | contact-list |
| "schedule a meeting" / "meeting notes" / "action items" | meetings |
| "what's on my calendar" / "morning briefing" | owner-briefing |
| "billing error" / "API out of credits" | billing-monitor |
| "connect calendar" / "connect Gmail" | calendar-setup |
| "set up a new PA" / "onboard agent" | pa-onboarding |
| "personal trainer" / "client check-in" / "workout program" / "fitness clients" | personal-trainer |
| "monday.com" / "create board item" / "track this" | monday-for-agents |
| "backup workspace" / "push to git" / "update openclaw" | pa-maintenance |
| "save this" / "where to save" | storage-router |
| "token usage" / "how much did today cost" | usage-costs |
| "what was discussed in [group]" | heleni-whatsapp |
| "search past messages" / "what did X say" | chat-history-local |
| "security check" / "health check" | self-monitor |
| "PA network status" / "how are PAs doing" | supervisor |
| "how am I doing" / "run eval" | eval |
| "summarize YouTube video" | youtube-watcher |
| "compact memory" / "organize memory" | memory-tiering |
| "reduce token costs" / "optimize costs" | openclaw-token-optimizer |
| "CRM update" / "pre-meeting brief" | personal-crm |
| "research X" / "find out about X" | research-synthesizer |
| "should I reply?" | silence-strategy |
| "transcribe voice message" | whatsapp-voice |
| "deep recall" / "did we discuss" / "what happened with" | deep-recall |
| "$ownership" / "execute with ownership" | ownership |
| "$devprocess" / "build this properly" / "use coding agent workflow" | devprocess |
| "reflect on this" / "fix how you operate" / "turn this into a durable fix" | self-reflection |
| "this should be a skill" / "save this as a skill" | auto-skill-creator |
| "knowledge graph" / "graphify" / "wiki compile" | knowledge-graph |
| "publish this" / "share this as a webpage" | publish-to-mdpage |
| "connect to X API" / "OAuth" / "external service integration" | api-gateway |
| "LinkedIn post" / "personal brand" / "Substack draft" | self-brand |
| Said "I'll send" / "I'll report" in a reply | commitment-tracker |
| "I made a mistake" / "owner corrected me" | self-learning |

> **Storage rule:** Before saving content, run `storage-router`. Research -> monday.com. State/config -> local.

> **Privacy review (before push):** Scan for internal names, phone numbers, JIDs, board IDs. Replace with placeholders.

> **Skill count:** 43 active. Above 30, keep routing tight and prefer the most specific skill first.
