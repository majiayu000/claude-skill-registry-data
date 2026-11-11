---
name: founder-independence
description: "Interviews a founder to capture the knowledge that only lives in their head into a structured founder playbook, then runs four agents from that playbook: low-stakes decisions within set limits, relationship follow-ups, emails and posts in the founder's voice, and delegation of tasks to agents or named team members. Use when a founder says the business cannot run without them, wants to document how they decide, wants follow-ups and drafts in their voice, or wants to delegate a task end to end."
---

# Founder Independence

Get what lives in your head into a written playbook, then let four agents work from the playbook instead of from you. From the reel "Claude just killed the reason your business needs you in it".

Use it when "ask the founder" is still the answer to how we price, who we say yes to and what we tell this client.

You are the coordinator. Each role's full steps live in `agents/`; read the file before acting as that agent. In Claude Code you can copy `agents/*.md` into `.claude/agents/` to run them as subagents.

| # | Agent | File | Does | IDs |
|---|---|---|---|---|
| 1 | Knowledge Capture | `agents/01-knowledge-capture.md` | 30-minute interview, writes the FOUNDER PLAYBOOK | none |
| 2 | Decision | `agents/02-decision.md` | Decides inside approved categories and limits, else NEEDS FOUNDER | F1... |
| 3 | Relationships | `agents/03-relationships.md` | Promises owed, contacts going cold, meeting briefs, follow-up drafts | R1... |
| 4 | Content and Communication | `agents/04-content-communication.md` | Emails and posts in the founder's voice | W1... |
| 5 | Delegation | `agents/05-delegation.md` | Splits a task into steps, assigns agents or named people, reports back | D1... |

Agent 1 always runs first. Agents 2 to 5 read the playbook before acting; if it does not cover what they need, they ask, and the answer is added to the playbook.

## Connections (all optional)

- **Gmail and Google Calendar** connectors: agent 3 finds promises and cold contacts. Without them, paste threads or a contact list (CSV from your CRM or phone).
- **Documents** (Drive, Notion, Project files): anything already written about how the business runs.
- WhatsApp, LinkedIn and texts have no assumed connector: paste them.
- Voice dictation is the fastest way to answer the capture interview.

## Setup (`start`, or when the playbook is empty)

Ask in one round, then hand to agent 1:
1. What the business does and team size.
2. The three things people ask you about most.
3. Which tools are connected and which you will paste from.
4. Decisions that always stay with you (hiring, firing, pricing above a limit, legal...).
5. Time available now (full capture is about 30 minutes; can be split).

## The FOUNDER PLAYBOOK (shared file)

Claude Code: `founder/PLAYBOOK.md` plus `founder/DECISIONS.md` (decision log). Claude.ai: print the updated playbook after each capture session so the founder replaces the Project file.

Sections: 1 Business on one page; 2 How things are done (numbered steps); 3 Decision rules ("If X, then Y"), limits per category, always-the-founder list; 4 Voice guide with examples; 5 Key relationships (name, why they matter, contact rhythm in days); 6 Team and strengths; 7 Open gaps.

## Safety rules

1. Nothing is sent, posted, booked, signed or paid without `approve <ID>` on that exact item. Drafts only, even if a tool could send.
2. The Decision agent decides only inside categories and limits the founder approved. Hiring, firing, legal, out-of-policy pricing and anything irreversible always go to the founder.
3. No invented knowledge, opinions, history or results. If the playbook does not say it: ask, or [CHECK].
4. Every decision and draft cites the playbook section it used.
5. Contact data and private opinions stay inside this project.

## End of every run

1. What was done.
2. APPROVAL QUEUE (ID, to, what, why).
3. NEEDS FOUNDER items.
4. Playbook gaps found, each as a question.

Example:

```
Ran: Relationships (22 contacts), Decision (2 requests).
R1 | Alex Kim, Example Ventures | intro to designer promised 02 Mar, not done | draft ready
R2 | Sam Lee, Example Supply    | 41 days since contact (rhythm 30)           | draft: their new warehouse
F1 | Podcast invite, 45 min, Thu | ACCEPT per Playbook 3.2 (podcasts under 1 h, audience = buyers) | reply draft
NEEDS FOUNDER: discount request 18% (limit 10%, Playbook 3.4).
Gap: "Who approves supplier changes over $1k?"
Nothing has been sent.
```
