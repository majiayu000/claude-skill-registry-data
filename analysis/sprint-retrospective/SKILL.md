---
name: sprint-retrospective
description: Facilitate effective sprint and team retrospectives that produce actionable insights and genuine improvement. Covers multiple retrospective formats (Start/Stop/Continue, 4Ls, Mad/Sad/Glad, sailboat), AI-assisted analysis of themes, action item creation with owners and success criteria, and retrospective health tracking over time.
triggers:
  - "run a retrospective"
  - "retro"
  - "retrospective"
  - "end of sprint"
  - "what went well"
  - "what could be better"
  - "team reflection"
  - "action items from retro"
  - "analyze our retrospective"
audience:
  - manager
  - engineer
---

# Sprint Retrospective

Facilitate retrospectives that produce real change — not just a list of complaints that gets forgotten.

> For production incident post-mortems, use the `incident-retrospective` skill instead.  
> This skill is for team/sprint/quarterly retrospectives.

---

## What Makes a Retro Valuable

A retrospective is only worth the action items it produces. Common failure modes:
- Same themes surface every sprint, nothing changes
- Action items have no owner or deadline
- Dominant voices crowd out quieter team members
- Facilitator skips synthesis — raw sticky notes ≠ insight
- No check-in on last sprint's actions (accountability vacuum)

**The measure of a good retro**: Did behavior change?

---

## Before the Retro (Facilitator Prep)

- [ ] Review last sprint's retro action items — which were completed? which weren't?
- [ ] Check sprint metrics: velocity, scope changes, blocked items, on-call load
- [ ] Choose a format that fits the team's current mood and last retro's format
- [ ] Book room / video call with 60-75 min timebox (< 8 people) or 90 min (8-12 people)
- [ ] Set up collaborative board: Miro, FigJam, Retrium, or EasyRetro

---

## Retrospective Formats

Choose based on team context:

### Start / Stop / Continue
Best for: new teams, post-process changes, when you want clear directional actions

| Column | Prompt |
|---|---|
| **Start** | What should we begin doing that we're not doing now? |
| **Stop** | What are we doing that isn't working or creates friction? |
| **Continue** | What's working well that we should keep doing? |

---

### 4Ls (Liked / Learned / Lacked / Longed For)
Best for: end-of-quarter, after a big delivery, or when team growth is the focus

| Column | Prompt |
|---|---|
| **Liked** | What did you enjoy or appreciate this sprint? |
| **Learned** | What did you learn — about the codebase, the team, yourself? |
| **Lacked** | What was missing — tools, clarity, support, process? |
| **Longed For** | What do you wish we had? What would have made this sprint better? |

---

### Mad / Sad / Glad
Best for: after a difficult sprint, when morale is low, when emotional acknowledgment matters

| Column | Prompt |
|---|---|
| **Mad** | What frustrated you or felt unfair? |
| **Sad** | What disappointed you or didn't go as hoped? |
| **Glad** | What are you proud of or grateful for? |

---

### Sailboat (Winds / Anchors / Rocks / Sun)
Best for: quarterly planning, when team wants to look forward as well as back

| Element | Meaning |
|---|---|
| **Wind** (🌬️) | What's helping us move forward? |
| **Anchor** (⚓) | What's slowing us down or holding us back? |
| **Rocks** (🪨) | What risks or obstacles are ahead? |
| **Sun** (☀️) | What's our goal / what are we sailing toward? |

---

## Running the Session

### Opening (5 min)
1. Check in on last sprint's action items: "We committed to X — did we do it?"
2. Set the tone: "This is a safe space. We improve systems, not blame people."
3. State the timebox and format

### Gather (10-15 min)
- Silent individual writing first — 5-7 min for everyone to add notes
- No discussion during this phase; prevents groupthink
- Encourage specifics: "Deploys were slow" is better than "things were bad"

### Group & Theme (10 min)
- Cluster similar items together (facilitator or team)
- Dot-vote on themes if too many to discuss: each person gets 3-5 votes
- Focus discussion on highest-voted clusters

### Discuss (20-30 min)
- One theme at a time — facilitator keeps focus
- Ask "why" for complaints: understand root cause, not just symptom
- Draw out quieter voices: "What do you think, [name]?"
- Time-box each theme: max 8-10 min per topic

### Action Items (10-15 min)
- For each discussed theme, ask: "What's one concrete thing we can change?"
- Every action item needs:
  - **What** — specific action, not vague aspiration
  - **Who** — single named owner (not "the team")
  - **By when** — specific date or sprint
  - **Success criteria** — how will we know it's done?

### Close (5 min)
- Read back the action items; get verbal confirmation from each owner
- Rate the retro: 1-5 thumbs (was this a good use of time?)
- Thank the team

---

## AI-Assisted Theme Analysis

Paste your raw sticky notes into an agent with this prompt:

```
Here are the raw retrospective notes from our sprint retro.
Please:
1. Group them into 3-5 themes with descriptive names
2. For each theme, summarize what the team is experiencing
3. Identify the top 2-3 themes by volume/sentiment
4. For each top theme, suggest 1-2 concrete, actionable improvements
   the team could try next sprint
5. Flag any items that indicate a systemic issue needing escalation

Notes:
[paste sticky notes here]
```

---

## Action Item Template

```markdown
## Retro Action Items — Sprint [N] — [Date]

| # | Action | Owner | Due | Success Criteria | Status |
|---|---|---|---|---|---|
| 1 | [specific action] | [name] | [sprint N+1 / date] | [measurable outcome] | ⬜ Open |
| 2 | | | | | ⬜ Open |

### Review at next retro:
- Item 1: [completed / in progress / dropped — with reason]
```

---

## Action Item Quality Check

Before the retro ends, test each action item:

| Test | Bad example | Good example |
|---|---|---|
| Is it specific? | "Improve communication" | "Add a #deploys Slack channel; post before + after every prod deploy" |
| Does it have one owner? | "The team will..." | "Priya will..." |
| Is it bounded? | "Eventually fix the flaky tests" | "Priya will fix the top 3 flaky tests by end of next sprint" |
| Can you tell if it's done? | "Be more proactive" | "Run a mid-sprint health check every Wednesday at standup" |

---

## Retrospective Health Over Time

Track these signals across retros to detect patterns:

| Signal | Healthy | Warning |
|---|---|---|
| Action item completion rate | > 70% each sprint | < 50% consistently |
| New themes surfacing | Yes — shows psychological safety | Same 3 themes every sprint = systemic block |
| Participation | Everyone contributes | 1-2 people dominate every time |
| Retro rating (1-5) | 3.5+ average | < 3 average = retro format needs change |
| Items escalated to manager | Rare | Frequent = problems beyond team's control |

---

## When Action Items Repeat

If the same theme shows up 3+ sprints in a row:

1. **Acknowledge it explicitly**: "We've flagged this 3 times. It's not getting better with small fixes."
2. **Escalate or time-box**: Either escalate to leadership (if it's systemic/resourcing) or time-box a dedicated fix sprint
3. **Consider a focused working session**: A 2-hour deep dive on one chronic problem > 6 sprints of 10-min discussion

---

## Quick Formats (< 30 min)

For busy periods or teams that need a lighter touch:

**Rose / Thorn / Bud** (async-friendly)
- 🌹 Rose: Something that went well
- 🌵 Thorn: Something that was difficult
- 🌱 Bud: Something to try or explore next sprint

**One-word check-in + one action**
Each person: one word describing the sprint + one thing to change. Facilitator synthesizes into 2-3 actions.

---

## References
- Esther Derby & Diana Larsen: *Agile Retrospectives* (the canonical text)
- Norman Kerth: *Project Retrospectives* (origin of the prime directive)
- Martin Fowler: [Retrospective Prime Directive](https://martinfowler.com/bliki/RetrospectivePrimeDirective.html)
- LeadDev: [Running retrospectives that actually lead to change](https://leaddev.com/agile-other-ways-working)
- [retromat.org](https://retromat.org) — 100+ retrospective activities

## MCP Integration

When Jira MCP and Confluence MCP are configured, close the loop between retro insights and team execution.

**Query completed sprint stories to ground the retrospective in data:**
```
jira_search_issues(jql: "project = PROJ AND sprint in closedSprints() AND sprint = '<sprint_name>'", max_results: 50)
```

**Create action items as Jira tickets:**
```
jira_create_issue(project: "PROJ", issue_type: "Task", summary: "Retro action: <action>", description: "<what, why, success criteria>", assignee: "<owner_username>", labels: ["retro-action"])
```

**Write the retrospective outcomes to Confluence:**
```
confluence_create_page(space_key: "TEAM", title: "<Sprint N> Retrospective", content: "<formatted retro summary with themes and actions>", parent_page_id: "<retros_page_id>")
```

**Check previous retro action items for carry-overs:**
```
jira_search_issues(jql: "labels = 'retro-action' AND status != Done AND project = PROJ")
```

**Graceful fallback:** Produce the retrospective summary and action items as Markdown; instruct the team to paste into Confluence and create Jira tickets manually.
