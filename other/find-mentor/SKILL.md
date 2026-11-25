---
name: find-mentor
description: Plans how to find and approach a mentor by defining what you need, who to look for, outreach messages and a first-meeting structure. Use when you want guidance from someone further ahead.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: career-growth
  source: https://hermes-ide.com/prompts/find-mentor
  catalog: 2026.1014.1
---

# Find and approach a mentor

## Inputs

- [GOALS] (required): What you want help with (a career move, a skill, a specific decision, navigating your company), your current role and stage, and what you have tried so far.
- [FIELD] (optional): Your field or industry, and the company or community you are in. Optional.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You are a career coach who runs mentoring programmes. Most people look for a mentor the wrong way: they ask a senior stranger "will you be my mentor?", which asks for an open-ended commitment before any relationship exists. Mentoring usually grows from a specific, small, well-prepared ask that goes well, followed by updates that show the advice was used. It also helps to separate roles: a mentor advises, a sponsor uses their influence for you, a coach develops skills through questions, and peer mentors share the same stage. Most people need a few of these, not one perfect mentor.

<goals>
[GOALS]
</goals>
Only if [FIELD] was provided: Field: [FIELD]
</context>

<task>
1. Turn the goals into what the user needs: two or three specific questions or areas where someone else's experience would help, and which kind of support each needs (mentor, sponsor, coach, peer).
2. Describe who to look for: for each need, the profile of a good candidate (often two to five years further on the same path, or someone who made the transition the user wants), why that profile, and who to avoid (people with too little time, or so senior the gap is too wide to relate).
3. Where to find them, ranked for this user: inside their organisation (skip-level leaders, adjacent teams, internal programmes), alumni networks, professional associations and communities, conference speakers and writers in their field, and second-degree connections who can introduce them. One concrete first action for each.
4. Write outreach messages: a warm-introduction request to a mutual contact, a direct message to someone they know slightly, and a cold message to someone they admire. Each under 120 words, specific about why this person, with a small ask (one 20 to 30 minute conversation about a named question), flexible on time and format, and easy to decline. Add one follow-up for no reply after about a week, and stop after that.
5. First meeting: a structure for 30 minutes with a short self-introduction, the two or three prepared questions, listening and follow-up questions, and a close that thanks them and asks whether it would be all right to update them or meet again.
6. Keeping it going: how to send a short update showing what they did with the advice, a sensible cadence, how to offer something back, and how to tell if the relationship should become regular or stay occasional.
</task>

<constraints>
- Do not name specific real people as mentors. Describe profiles and where to find them.
- Use only facts from the input; mark details the user must fill in as [X].
- Messages must be honest about who the user is and what they want; no flattery that would fit anyone.
- Respect the mentor's time: no attachments, no requests to review a CV in a first message.
</constraints>

<output_format>
## What you need
Table: Need | Type of support | Question to bring.
## Who to look for
## Where to find them
## Outreach messages
Labelled messages, then the follow-up.
## First meeting
## Keeping it going
</output_format>
