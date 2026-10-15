---
name: email-personal-note
description: Generate a personal note for follow-up email body. Use when writing recruiting follow-up emails to candidates.
argument-hint: [candidate-profile-info]
---

Write a short personal note for the body of a follow-up recruiting email. Can be 1-2 sentences.

## Context
- The email is from a hiring manager (team leader, VP R&D, etc.)
- Target audience: candidates in Israel
- This goes in the email body, not subject line
- Must be DIFFERENT from the subject line (pick a different angle/detail from their profile)

## Requirements
- Pick ONE specific thing from the candidate's profile (different from what subject line used)
- Either ask a genuine question about it OR give a quick compliment
- Keep it casual and human
- Write like a real person, not a recruiter bot
- Can be slightly longer than subject line but still concise

## CRITICAL VALIDATION RULES (check before output):
1. **No em dashes** - Never use "—" anywhere. Use "-" or ", " instead.
2. **No duplicate companies** - Never mention the same company twice. If they stayed at the same place (including variants like "Pecan" and "Pecan AI", "Waze" and "Google/Waze"), focus on role growth, skills, or education instead.
3. **Clean company names** - Strip suffixes: Ltd, Inc, Corp, Technologies, Labs, .io, Group, Solutions. Use core brand only:
   - "Healthy.io" -> "Healthy"
   - "AI21 Labs" -> "AI21"
   - "NSO Group" -> "NSO"
   - "Argus Cyber Security Ltd." -> "Argus"
   - "Istra Research Ltd." -> "Istra Research"
4. **Same parent company = same company** - Google/Waze, Unity/ironSource, SAP/Gigya are same company. Don't reference the transition.

## NEVER use these (instant disqualify):
- Em dashes (—) - never use them
- "I hope this message finds you well"
- "I hope you're doing well"
- "I came across your profile"
- "I was impressed by"
- "I noticed"
- "Reaching out because"
- "Hope you're having a great day"
- "Just following up"
- "Wanted to circle back"
- Any generic opener that could apply to anyone
- Repeating the same company name twice
- "What keeps you busy at X?" - overused, avoid

## Good examples by category:

**Company transitions (use when prev != current):**
- "Big move from [prev]. What pulled you over?"
- "[Prev] to [current] is an interesting path. What sparked the change?"
- "Curious what drew you from [prev] to the startup world."
- "[Prev] to startup - what's the biggest change?"
- "Two strong security companies back to back. What draws you to the space?"
- "Enterprise to startup - what's the biggest change in how you work?"

**Education hooks:**
- "Technion is no joke. How do you apply that rigor at work?"
- "TAU CS is competitive. What area grabbed your interest?"
- "Hebrew U has strong CS. What got you into backend?"
- "BGU engineering is solid. What kind of problems do you enjoy solving?"
- "BGU with honors is impressive. What area of CS grabbed your interest most?"
- "TAU MBA + Hebrew U MSc is a strong combo. How do you apply both?"
- "Physics background in [domain] - how does that help you think about problems?"

**Title/Leadership:**
- "Leading and coding is a balancing act. How do you split your time?"
- "Curious how you keep shipping code while managing a team."
- "Tech lead who still builds - that's rare. How do you make time?"
- "Team lead who still codes - how do you balance both responsibilities?"
- "Observability tools are tricky to build. What's the hardest part?"

**Skills-based:**
- "Rust in production is still rare. How's adoption going with the team?"
- "K8s at scale gets complex. What's your approach?"
- "Go for backend is a solid choice. What sold you on it?"
- "Kafka can be tricky. What's your setup like?"
- "Go and Python together is a solid combo. Which do you prefer for backend?"
- "Distributed systems are tricky. What's the hardest part?"
- "NestJS and TypeScript is a solid combo. How's the team using it?"
- "Spark and Airflow at scale is tricky. What's your approach?"
- "AWS Lambda and DynamoDB at scale is tricky. What's your approach?"
- "Kafka and gRPC together is interesting. How do you handle the complexity?"
- "GraphQL with microservices is interesting. How's your architecture set up?"
- "Scala/Spark/Akka is a powerful combo. What problems are you solving with it?"

**Career path:**
- "First employee at a startup is intense. What was the wildest part?"
- "Manager back to IC is a bold move. What drove that decision?"
- "Building from scratch is a different game. What do you enjoy most?"
- "7+ years at one company is rare. What keeps you engaged?"
- "CTO to engineer is interesting. What do you enjoy more about hands-on work?"
- "Research to engineering is an interesting path. How does that help you?"
- "15+ years in the industry - what's changed most about how we build software?"

**Founding/early stage:**
- "Founding engineer means wearing many hats. What's your favorite part?"
- "Early stage to scale-up is a journey. How's the transition?"

**Acquisitions/transitions:**
- "[Company] to [Acquirer] acquisition is a ride. How's the transition going?"
- "7+ years through an acquisition - how did [Acquirer] change things?"

**Unique backgrounds:**
- "[Non-CS field] to backend engineering is unique. How does that background help?"
- "Physics to software architecture is interesting. How does that background help?"
- "Music to security engineering is unique. How does that background help?"
- "Publishing tech articles while building is impressive. What do you write about?"
- "DS&A tutor at Technion - how does teaching help your engineering?"
- "Coaching competitive programming while building hardware - how do they complement?"

## Input
Candidate profile information: $ARGUMENTS

## Output
Return ONLY the personal note. No quotes, no explanation, nothing else.
