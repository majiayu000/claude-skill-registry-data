---
name: email-subject-line
description: Generate email subject line and personal note for candidate outreach. Use when writing recruiting emails to candidates.
argument-hint: [candidate-profile-info]
---

Generate TWO things for a recruiting email:
1. **Subject line** - under 10 words
2. **Personal note** - 1-2 sentences for follow-up email body

## Context
- Email is from a hiring manager (team leader, VP R&D, etc.)
- Target audience: candidates in Israel
- Subject line for initial outreach, personal note for follow-up body

## CRITICAL: Parse CSV format correctly

The data comes from enriched CSV with these formats:

**past_positions** - Parse to extract FIRST previous company:
- Format: "Title at Company1 (dates) [X yrs] || Title at Company2 (dates) [X yrs]"
- Extract the FIRST company name after "at " and before " ("
- Example: "Software Engineer at Explorium (1 Dec 2020 - 1 May 2022)" → previous company = "Explorium"

**education** - Parse to extract school name:
- Format: "School Name, Degree | School2, Degree2"
- Extract the school name before the comma
- Example: "Technion - Israel Institute of Technology, BSc" → school = "Technion"

**skills** - Comma-separated list, look for interesting ones:
- Interesting: Rust, Go, Kotlin, Scala, K8s, Kafka, Elasticsearch, GraphQL, gRPC, Spark

## UNIQUE subject lines - CRITICAL

**IMPORTANT: VARY THE ANGLE - Don't always use company transitions!**

When processing multiple candidates, rotate through these angles to ensure variety:
- Company transition (use sparingly - max 30% of emails)
- Education-based
- Title/role-based
- Skills-based
- Career path-based

**For each candidate, pick ONE angle based on what's MOST interesting about them:**

1. **Notable education** (Technion, TAU, Hebrew U, Weizmann, BGU honors)
   - "Technion grad at [company]?"
   - "TAU CS at [company]?"
   - "Hebrew U to [company]?"
   - "BGU engineer at [company]?"

2. **Interesting title** (Lead, Staff, Principal, Founding, Architect)
   - "Still hands-on as lead?"
   - "Staff engineer at [company]?"
   - "Founding engineer at [company]?"
   - "Architect at [company]?"
   - "Leading at [company]?"

3. **Interesting skills** (Rust, Go, Kotlin, Scala, K8s, Kafka, gRPC, Spark)
   - "Rust in production?"
   - "Go at [company]?"
   - "K8s at scale?"
   - "Kafka at [company]?"
   - "Kotlin backend?"

4. **Career transitions** (Manager→IC, Founder, long tenure, acquisition)
   - "Manager back to IC?"
   - "Founder to [company]?"
   - "After the acquisition?"
   - "Still building after 5 years?"

5. **Company transition** (USE SPARINGLY - only for very notable moves)
   - ONLY use for tier-1 companies: Google, Meta, Apple, Amazon, Microsoft
   - Format: "[Prev] to [Current]?" or "[Prev] alum?"
   - Do NOT use for every candidate with a previous job

6. **Domain/focus area**
   - "Backend at [company]?"
   - "Security at [company]?"
   - "Infra at [company]?"
   - "Platform at [company]?"
   - "Data eng at [company]?"

## Data points to use:
1. **Previous employer** - EXTRACT from past_positions field (first company listed)
2. **Education** - EXTRACT school name from education field
3. **Current title** - from current_title field
4. **Interesting skills** - from skills field (Rust, Go, K8s, Kafka, Scala, Elasticsearch, etc.)

## DO NOT use interpreted/potentially wrong data:
- Years at company (could be outdated)
- Specific achievements or projects
- Anything that sounds like it was summarized or interpreted
- Tenure claims ("5+ years")

## CRITICAL VALIDATION RULES (check before output):
1. **No em dashes** - Never use "—" anywhere
2. **No duplicate companies** - If prev company and current company are the same (or variants like "Pecan" and "Pecan AI", "Waze" and "Google/Waze", "Bionic" and "CrowdStrike/Bionic"), do NOT use company transition format. Pick education, title, or skills instead.
3. **Clean company names** - Strip suffixes: Ltd, Inc, Corp, Technologies, Labs, .io, Group, Solutions. Use core brand only:
   - "Healthy.io" -> "Healthy"
   - "AI21 Labs" -> "AI21"
   - "GSI Technology" -> "GSI"
   - "NSO Group" -> "NSO"
   - "Argus Cyber Security Ltd." -> "Argus"
   - "Istra Research Ltd." -> "Istra Research"
4. **Same parent company = same company** - Google/Waze, Unity/ironSource, SAP/Gigya are same company. Don't use "[A] to [B]?" format.

## Priority order for subject line (BALANCED - avoid repetition):
1. **Education** - Technion, TAU, Hebrew U, Weizmann, BGU (if CS/Engineering degree)
2. **Interesting title** - Team Lead, Staff, Principal, Founding, Architect
3. **Rare skills** - Rust, Go, Kotlin, Scala, K8s, Kafka, gRPC, Spark
4. **Career path** - Manager→IC, Founder, acquisition, 5+ years tenure
5. **Company transition** - ONLY for tier-1 (Google, Meta, Apple, Amazon, Microsoft, Waze)
6. **Domain focus** - Backend, Security, Infra, Platform, Data
7. **Current company** - Last resort: "Building at [company]?"

**AVOID**: Using "[Prev] to [Current]?" for every candidate. Most candidates have previous jobs - that's not distinctive!

## NEVER use (instant disqualify):
- Em dashes (—)
- "I hope this message finds you well"
- "I came across your profile"
- "I was impressed by"
- "I noticed"
- "Reaching out because"
- Any generic opener that could apply to anyone

## Good examples - USE VARIETY

Subject lines (based on prev company) - VARY THE FORMAT:
- "[Prev] to [Current]?" - e.g., "Snyk to Wilco?"
- "[Prev] alum at [Current]?" - e.g., "Google alum at Foretellix?"
- "After [Prev], what's next?" - e.g., "After Check Point, what's next?"
- "[Prev] experience at [Current]?" - e.g., "Waze experience at Orca?"
- "From [Prev] to [Current]?" - e.g., "From Microsoft to startup?"

Subject lines (based on education) - VARY THE FORMAT:
- "[School] grad at [company]?" - e.g., "Technion grad at Snyk?"
- "[School] engineer at [company]?" - e.g., "BGU engineer at Monday?"
- "[School] CS at [company]?" - e.g., "TAU CS at Wiz?"
- "[School] background at [company]?" - e.g., "Hebrew U background at JFrog?"
- "[Degree] from [School]?" - e.g., "MSc from Technion?"
- "[School] to [company]?" - e.g., "Technion to startup life?"

Subject lines (based on title) - VARY THE FORMAT:
- "Still hands-on as lead?"
- "Tech Lead at [company]?"
- "Leading at [company]?"
- "Staff engineer at [company]?"
- "Staff role at [company]?"
- "Founding engineer at [company]?"
- "Early employee at [company]?"
- "From manager back to IC?"
- "Manager to IC transition?"
- "R&D Lead at [company]?"
- "Architect at [company]?"
- "Principal at [company]?"

Subject lines (based on skills) - VARY THE FORMAT:
- "[Skill] in production?" - e.g., "Rust in production?"
- "[Skill] at [company]?" - e.g., "Go at Monday?"
- "[Skill] at scale?" - e.g., "K8s at scale?"
- "[Skill1] and [Skill2]?" - e.g., "Go and Kafka?"
- "Building with [Skill]?" - e.g., "Building with Kotlin?"
- "[Skill] backend at [company]?" - e.g., "Python backend at Snyk?"

Subject lines (based on domain/industry):
- "Security at [company]?" - for cybersecurity companies
- "Fintech at [company]?" - for fintech companies
- "AI/ML at [company]?" - for AI companies
- "Infra at [company]?" - for infrastructure roles
- "Backend at [company]?" - for backend roles
- "Platform at [company]?" - for platform teams

## Personal note rules:
1. **Pick a DIFFERENT angle** than subject line used
2. **Be specific** - reference something concrete from their profile
3. **Vary the format** - don't always use the same template
4. **Match the tone to fit level** - strong fit gets more enthusiastic, good fit more curious

## Personal note variety (rotate through these styles):

**For company transitions:**
- "Big move from [prev]. What pulled you over?"
- "[Prev] to [current] is an interesting jump. What sparked the change?"
- "Curious what drew you from [prev]."
- "[Prev] to [current] - what's the biggest change?"
- "Two strong [domain] companies back to back. What draws you to the space?"

**For education:**
- "Technion is no joke. How do you apply that rigor day-to-day?"
- "TAU CS is competitive. What area grabbed your interest?"
- "Hebrew U has strong CS. What got you into backend?"
- "BGU engineering is solid. What kind of problems do you enjoy solving?"
- "BGU with honors is impressive. What area of CS grabbed your interest most?"
- "[School] MSc is a strong combo. How do you apply both?"

**For titles/leadership:**
- "Leading and coding is a balancing act. How do you split your time?"
- "Curious how you keep shipping code while managing a team."
- "Team lead who still builds - that's rare. How do you make time?"
- "Tech Lead who still codes - how do you balance both responsibilities?"

**For skills:**
- "Rust in production is still rare. How's adoption going with the team?"
- "K8s at scale gets complex. What's your approach?"
- "Go for backend is a solid choice. What sold you on it?"
- "Kafka can be tricky. What's your setup like?"
- "Go and Python together is a solid combo. Which do you prefer for backend?"
- "Distributed systems are tricky. What's the hardest part?"
- "NestJS and TypeScript is a solid combo. How's the team using it?"
- "Spark and Airflow at scale is tricky. What's your approach?"

**For interesting career paths:**
- "First employee at a startup is intense. What was the wildest part?"
- "Manager back to IC is a bold move. What drove that decision?"
- "Building from scratch is a different game. What do you enjoy most?"
- "CTO to engineer is interesting. What do you enjoy more about hands-on work?"
- "7+ years at one company is rare. What keeps you engaged?"
- "Research to engineering is an interesting path. How does that help you?"

**For acquisitions/transitions:**
- "[Company] to [Acquirer] acquisition is a ride. How's the transition going?"
- "7+ years through an acquisition - how did [Acquirer] change things?"

**For unique backgrounds:**
- "[Non-CS field] to engineering is unique. How does that background help?"
- "Physics to software architecture is interesting. How does that background help?"
- "Publishing tech articles while building is impressive. What do you write about?"

## BEFORE generating - DIVERSIFY the angle

**CRITICAL: Don't default to "[Prev] to [Current]?" - that's lazy and repetitive!**

For each candidate, ask yourself:
1. Do they have a notable SCHOOL? → Use education angle
2. Do they have an interesting TITLE? → Use title angle
3. Do they have RARE SKILLS? → Use skills angle
4. Is there a unique CAREER PATH? → Use career angle
5. ONLY if prev company is tier-1 (Google/Meta/Apple/Amazon/Microsoft) → Use company transition

**Rotate angles across candidates to ensure variety!**

## Examples with VARIED angles:

**Profile 1:** (Use EDUCATION)
- past_positions: "Software Engineer at Explorium"
- education: "Ben-Gurion University of the Negev, BSc in Computer Science"
- current_company: "Tymely"
- → Has BGU CS degree
- → **Subject: "BGU engineer at Tymely?"** (NOT "Explorium to Tymely?")

**Profile 2:** (Use SKILLS)
- past_positions: "Software Engineer at NICE Ltd"
- education: "Bar-Ilan University"
- current_company: "Twingate"
- skills: "Python, Django, Spring Boot, Microservices"
- → Django + Spring is interesting combo
- → **Subject: "Django at Twingate?"** (NOT "NICE to Twingate?")

**Profile 3:** (Use TITLE)
- past_positions: "Technical lead at Quantum Machines"
- education: "Tel Aviv University, Physics and CS"
- current_company: "OneStep"
- current_title: "Software Engineer"
- → Was a lead, now IC
- → **Subject: "Lead back to IC?"** (NOT "Quantum Machines to OneStep?")

**Profile 4:** (Use EDUCATION - different format)
- past_positions: "Senior at Applied Materials"
- education: "Technion, Computer Engineering"
- current_company: "Rekor"
- → Technion CE is notable
- → **Subject: "Technion CE at Rekor?"**

**Profile 5:** (Use COMPANY - only because it's tier-1)
- past_positions: "Software Engineer at Google"
- education: "Open University"
- current_company: "Startup"
- → Google is tier-1, worth mentioning
- → **Subject: "Google to startup life?"**

**Profile 6:** (Use DOMAIN)
- past_positions: "Backend at various companies"
- education: "College degree"
- current_company: "Salt Security"
- skills: "Kafka, Microservices, AWS"
- → Security company + backend focus
- → **Subject: "Security backend at Salt?"**

## Input
Candidate profile information: $ARGUMENTS

## Output
Return in this exact format:
Subject: [subject line here]
Note: [personal note here]
