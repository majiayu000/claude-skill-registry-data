---
name: Context Handover
description: Create concise handover summary for seamless continuation in new chat session
version: 2.0.0
triggers:
  - handover
  - context summary
  - session summary
  - continue in new chat
  - save context
  - export session
---

# Context Handover Skill

Create context handover for new chat session - works for any conversation type.

## Goal

Enable seamless continuation in fresh chat. Works for: projects, research, planning, coding, decisions, etc.

## Output Structure

Generate summary with exactly these 3 sections:

### 1. [[Current Situation]]

- Where we are now
- What's decided/done
- Open questions/blockers

### 2. [[Key Info]]

- Important decisions made
- Critical facts/links/references
- Names, dates, numbers
- File paths (if relevant)
- Key quotes or requirements

### 3. [[Next Steps]]

- What needs doing next
- Priority order
- Open tasks

## Style Constraints

- **Extremely concise** - sacrifice grammar for brevity
- **Telegraphic style** - no filler words
- Bullet points only, no prose
- Max ~500 words total
- Include only actionable/critical info

## Example Outputs

### Example 1: Travel Planning
```
## [[Current Situation]]
- Destination: Barcelona, June 15-22
- Budget: €1500/person, 2 people
- Flights booked (Lufthansa LH1134)
- Blocker: hotel not confirmed yet

## [[Key Info]]
- Must-see: Sagrada Familia, Park Güell, Gothic Quarter
- Restaurant rec: Cervecería Catalana (from Maria)
- Hotel shortlist: Hotel Jazz (€120/night), Praktik Rambla (€95/night)
- Rail pass: €50 for week, covers all metro

## [[Next Steps]]
1. Book hotel by tomorrow (prices rise)
2. Reserve Sagrada Familia tickets (time slot 10am preferred)
3. Check travel insurance options
```

### Example 2: Research Task
```
## [[Current Situation]]
- Topic: AI coding assistants comparison
- Tested: Cursor, Windsurf, Cline, Kilo Code
- Winner so far: Kilo Code (BYOK + OpenRouter)
- Still need: pricing breakdown

## [[Key Info]]
- Cursor: $20/month, proprietary models
- Windsurf: $15/month, limited free tier
- Kilo Code: BYOK, transparent costs via OpenRouter
- Key factor: want cost control + transparency
- Source: Reddit r/LocalLLaMA thread (Dec 2024)

## [[Next Steps]]
1. Calculate monthly costs for Kilo Code usage
2. Test Roo Code as final alternative
3. Write comparison doc for team
```

### Example 3: Coding Project
```
## [[Current Situation]]
- Building: Spotify stats dashboard (Next.js + React)
- Auth: OAuth working, tokens refreshing
- DB: Supabase connected
- Blocker: top artists API pagination broken

## [[Key Info]]
`/lib/spotify.ts` - main API logic
`/app/api/auth/callback/route.ts` - OAuth handler
Using: SWR for data fetching, Tailwind CSS
Bug: only returns 20 artists, need 50

## [[Next Steps]]
1. Fix pagination in getTopArtists()
2. Add caching layer (Redis?)
3. Deploy to Vercel
```

## When to Use

- Context window filling up
- End of work session
- Before switching topics
- User asks to "save progress"
- Handing off to someone else
- Major topic shift coming

## Important

- Adapt sections to conversation type
- Skip irrelevant sections (e.g., no code paths for travel planning)
- Focus on what's needed to continue seamlessly
- Include only info that would be hard to reconstruct
