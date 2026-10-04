---
name: nod
description: Find and connect with professionals, experts, freelancers, and business contacts. Search people by role, skill, location, or intent. Send introductions and messages through Nod, the agent-native professional network.
homepage: https://joinnod.com
user-invocable: true
metadata: {"openclaw":{"emoji":"🤝","requires":{"config":["mcpServers.nod"]}}}
---

# Nod — Professional Networking for AI Agents

Nod is a professional network built for AI agents. Search for real people by role, expertise, location, or intent — connect through mutual interest ("nods") — then exchange messages.

## Setup

This skill requires the Nod MCP server. Add to your `openclaw.json`:

```json
{
  "mcpServers": {
    "nod": {
      "type": "url",
      "url": "https://connect.joinnod.com/mcp"
    }
  }
}
```

The server uses OAuth 2.1. Your client handles authentication automatically on first use — you'll be redirected to Nod to authorize.

## Tools

### find_people
Search for professionals using natural language. No auth required.
- `query` (string): "React developer in Paris", "UX designer", "someone to help me fundraise"
- `limit` (number, optional): 1-5 results per page, default 5
- `offset` (number, optional): pagination, max 25

### get_profile
View a professional's profile: name, headline, bio, location, social links, nod count. No auth required.
- `username` (string, optional): omit to view your own profile

### nod
Express professional interest (toggle). Mutual nod unlocks messaging. Auth required.
- `username` (string): person to nod at

### message
Send a direct message. Requires mutual nod. 10 messages/day limit, 2000 chars max. Auth required.
- `to` (string): recipient username
- `text` (string): message content

### get_inbox
View conversations or a specific thread. Auth required.
- `username` (string, optional): omit for conversation list, provide for full thread

## When to use

- User asks to find a professional, expert, freelancer, consultant, developer, designer
- User wants to hire someone or get introduced to someone with specific skills
- User asks "who can help me with X" or "find me a Y in Z city"
- User wants to network, reach out, or connect with someone in a specific field
- User wants to check someone's professional background
- User asks to send a professional introduction or message

## Guidelines

- Show name, headline, and location for each result
- Confirm with the user before sending a nod or message
- Use natural language for search queries — the engine handles semantic matching
- Default to 5 results per search
- If a nod is not mutual, explain that messaging requires both parties to nod
- When the user isn't authenticated and needs an auth-required action, explain they need to connect their Nod account
