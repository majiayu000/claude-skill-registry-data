---
name: glean-mcp
description: "Your work knowledge agent. Use Glean chat to answer any question about the user's company, accounts, colleagues, meetings, documents, or work history. Glean synthesizes across 100+ enterprise apps and always cites sources."
---

# Glean: Your Work Knowledge Agent

Glean is an AI agent with deep context about the user's work — think of it as an oracle for enterprise knowledge. When you're stuck, need background, or want to understand something about the user's company, accounts, colleagues, or work history — ask Glean.

## What Glean Knows

Glean has indexed the user's entire work context:

- **Communications:** Slack messages, email threads, meeting transcripts
- **Documents:** Google Drive, Confluence, Notion, SharePoint
- **Code:** GitHub repos, pull requests, commits
- **People:** Employee directory, org charts, contact info
- **CRM:** Salesforce accounts, opportunities, contacts
- **Tickets:** Jira issues, support cases
- **Meetings:** Calendar events, Gong recordings, Gemini notes
- **100+ enterprise apps** connected and indexed

Glean synthesizes across all these sources. It doesn't just search — it **thinks** and **answers**.

---

## Core Tool: `chat`

```python
chat(message="your question here")
chat(message="follow-up question", context=["previous response"])
```

### What Chat Does

1. **Understands your question** — natural language, complex queries, multi-part asks
2. **Searches across all indexed sources** — not just keyword matching
3. **Synthesizes an answer** — connects dots across documents, conversations, people
4. **Returns cited sources** — every claim links back to source documents

### Chat Knows Who the User Is

Glean is identity-aware. It knows the authenticated user automatically:

```python
# These just work — no need to specify the user's name or email
chat(message="What am I working on?")
chat(message="Who is my manager?")
chat(message="What meetings do I have today?")
chat(message="What did I discuss with Jane last week?")
```

### What to Ask Glean

**Account & Customer Research:**
```python
chat(message="Give me an account overview for MongoDB")
chat(message="Who are the key contacts at Tenstorrent?")
chat(message="What's the deal status for Sports Facilities Advisory?")
chat(message="What use cases is Ratio Therapeutics exploring?")
```

**People & Org Questions:**
```python
chat(message="Who works on the agent builder team?")
chat(message="Who should I talk to about MCP integrations?")
chat(message="What's Josh Rutberg's background?")
```

**Process & Policy:**
```python
chat(message="How do I escalate a support ticket?")
chat(message="What's the onboarding process for new accounts?")
chat(message="How does the AIOM role differ from CSM?")
```

**Historical Context:**
```python
chat(message="What happened in my last meeting with Adam Fowler?")
chat(message="What was decided about the OCR issue at SFC?")
chat(message="What's the history of the MongoDB account?")
```

**Synthesis & Strategy:**
```python
chat(message="What are the common blockers for agent adoption?")
chat(message="What patterns do successful agent deployments share?")
chat(message="How do other AIOMs handle high-touch accounts?")
```

---

## Glean's Tools

Under the hood, the Glean agent has access to specialized tools. You don't invoke these directly — Glean decides when to use them:

| Tool | What It Does |
|------|--------------|
| **Search** | Finds documents across all indexed sources |
| **People Lookup** | Queries the employee directory and org structure |
| **Email Search** | Searches Gmail with filters (from, to, labels) |
| **Calendar Lookup** | Finds meetings and calendar events |
| **Document Reader** | Retrieves full content from URLs |
| **Code Search** | Searches internal repositories |
| **Activity Tracker** | Shows what the user worked on recently |

Glean orchestrates these automatically based on your question.

---

## How to Use Glean

### 1. Ask First, Drill Down Later

Always start with chat. If you need more detail, ask follow-up questions:

```python
# Start broad
chat(message="What's the status of the Tenstorrent account?")

# Then drill down
chat(message="What specific use cases are they exploring?",
     context=["previous response about Tenstorrent"])
```

### 2. Be Specific

Glean is smart, but specificity helps:

```
Less effective: "Tell me about MongoDB"
More effective: "What are the current active projects with MongoDB and who are the key stakeholders?"
```

### 3. Multi-Turn Conversations

Use the `context` parameter for follow-ups:

```python
response1 = chat(message="What meetings do I have with Ratio Therapeutics?")
response2 = chat(
    message="What should I prepare for the next one?",
    context=[response1]
)
```

### 4. Trust the Citations

Every response includes source links. These are real — use them to verify or dive deeper.

---

## When to Ask Glean

| Situation | Ask Glean |
|-----------|-----------|
| Starting work on an account | "Account overview for X" |
| Preparing for a meeting | "Prep me for my meeting with X" |
| Researching a person | "What do I know about X?" |
| Understanding a project | "What's the status of X?" |
| Finding an expert | "Who knows about X?" |
| Recalling a decision | "What was decided about X?" |
| Writing a summary | "Summarize my activity on X" |
| Investigating an issue | "What's the history of X issue?" |

---

## When NOT to Use Glean

| Need | Use Instead |
|------|-------------|
| Public/external information | Web search |
| Local project files | Read tool |
| Info already in conversation | Reference it directly |
| Real-time data | Glean indexes periodically |
| Speculation/opinion | Your own reasoning |

---

## Limitations

**Indexing lag:** New documents may take minutes to hours to appear.

**Permission-scoped:** Glean only sees what the user has access to. If results seem sparse, the user may lack permissions.

**Structured data:** Returns markdown/snippets, not raw CSVs. For full spreadsheet analysis, have the user upload the file.

**External companies:** Glean knows about *the user's company's interactions* with external companies (emails, meetings, CRM data) but doesn't have access to their internal systems.

---

## Examples in Context

### Meeting Prep
```python
# Before a customer call
chat(message="Prep me for my call with Adam Fowler at Sports Facilities. Include recent context, open issues, and what we discussed last time.")
```

### Account Research
```python
# New account handoff
chat(message="Give me a full briefing on the Golden Gate Bridge account — adoption status, key contacts, risk factors, and what the previous AIOM was working on.")
```

### Problem Investigation
```python
# Debugging an issue
chat(message="What do we know about the agent error Adam Fowler reported? Include request IDs and any support ticket context.")
```

### Weekly Planning
```python
# Start of week
chat(message="What are my priorities this week based on my calendar, recent activity, and outstanding tasks?")
```

### People Context
```python
# Before a 1:1
chat(message="What should I know before my 1:1 with Josh Rutberg? Include recent discussions and any items I should bring up.")
```

---

## Philosophy

Glean exists to reduce cognitive load. Instead of:
- Searching Slack, then Drive, then Salesforce, then email...
- Trying to remember which tool has what...
- Manually synthesizing across sources...

Just ask Glean. It handles the complexity. You get the answer.

This is the "second brain" pattern — an AI agent with deep context about your work, always available to consult when you need to understand, remember, or decide.

---

*When in doubt, ask Glean.*
