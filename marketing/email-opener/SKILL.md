---
name: email-opener
description: Generate personalized email subject lines and openers for LinkedIn profiles. Use when the user wants to write outreach emails, personalize messages, create email openers, or prepare cold email campaigns for candidates.
argument-hint: [csv-file-path]
---

# Personalized Email Subject Lines & Openers

Generate human-sounding, personalized email subject lines and opening lines for recruiter outreach based on enriched LinkedIn profile data.

## Input

1. **Enriched profiles CSV**: User provides a file path (or use screening results JSON if available)
2. **Score threshold**: Only generate for candidates above a certain score (default: 5+)
3. **Tone**: User may specify tone. Default is short, punchy, conversational.

## Critical Rules

### 1. Normalize ALL company names

LinkedIn data is messy. NEVER output raw LinkedIn company names. ALWAYS clean them:

| Raw LinkedIn Name | Clean Output |
|---|---|
| Check Point Software Technologies, Ltd. | Check Point |
| Apple Inc. | Apple |
| WalkMe(tm) or WalkMe with unicode | WalkMe |
| Fiverr International Ltd. | Fiverr |
| Meta Platforms, Inc. | Meta |
| Palo Alto Networks | Palo Alto Networks |

Rules:
- Strip suffixes: Ltd, Ltd., Inc, Inc., Corp, Corp., LLC, GmbH, S.A., PLC, LTD
- Strip trailing parenthetical content like "(Israel)" unless it's part of the real name
- Strip unicode: trademark symbols, registered marks, copyright, em dashes, smart quotes, replacement characters
- Use the common brand name people actually say out loud ("Check Point" not "Check Point Software Technologies")
- When in doubt, Google what people call the company in conversation

### 2. Only reference RECENT positions (last ~8 years)

- Parse `past_positions` JSON and sort by `end_date` descending
- Only mention employers where the position ended 2018 or later (or has no end date = current)
- NEVER mention a company someone worked at 10+ years ago in a cold email. It feels stalkerish and irrelevant
- Prefer the most recent notable employer, not the oldest one

### 3. Avoid false keyword matches

Common traps:
- "intel" matches "Israeli Military Intelligence" - WRONG
- "unity" matches "Community Unity" - WRONG
- "meta" matches "Metadata" - WRONG
- "redis" matches "Redistribution" - WRONG

Solution: Match against the normalized `employer_name` field from positions data, NOT raw substring search. Use exact matching or starts-with matching.

### 4. Vary the templates (MANDATORY)

NEVER use the same subject line or opener phrasing for more than ~25% of candidates. Use at least 4 subject variations and 3 opener variations per category. Randomly assign templates.

Subject line categories:
- Notable past company reference
- Years of experience hook
- Current company/role reference
- Tech skill reference
- Generic but warm

Opener categories:
- Notable company + years (for senior people with brand-name employers)
- Notable company only (for mid-level at known companies)
- Years + current company (for senior people without notable past employers)
- Current role + company (for everyone else)
- Generic warm (fallback)

### 5. No special characters in output

Absolutely no:
- Em dashes or en dashes (use "," or "." instead)
- Smart/curly quotes (use straight quotes)
- Trademark, registered, copyright symbols
- Any non-ASCII unicode character
- Emoji (unless user explicitly asks)

### 6. Write like a human recruiter, not a bot

Good:
- "Hi Adir, saw you spent time at Fiverr and your GraphQL background stood out."
- "Hi Maxim, 15+ years in backend with time at Wix is a strong combination."

Bad:
- "Hi Adir, your extensive experience at Fiverr International Ltd. in backend development with GraphQL technologies is impressive and aligns perfectly with our requirements."
- "Dear Maxim, I came across your distinguished profile and was thoroughly impressed by your remarkable 15-year career trajectory..."

Rules:
- First name only, never "Dear" or full name
- One specific detail about THEM, not a generic compliment
- Max 1-2 sentences for the opener
- Subject line under 60 characters
- No buzzwords ("synergy", "leverage", "cutting-edge", "passionate")
- No over-complimenting ("incredible", "outstanding", "remarkable")
- Sound like a text from a colleague, not a formal letter

### 7. Optional personal touches (append only if opener is short enough)

If the opener is under ~120 characters, you can append ONE of:
- Military elite background: "(8200 alumni is a nice bonus too.)"
- Notable education: "Technion background is a plus."
- Specific tech match: "Your GraphQL experience is exactly what we need."

Never stack multiple touches. Pick the strongest signal.

## Output Format

Generate a CSV with columns:
- name, score, title, company, linkedin_url, subject_line, email_opener

Also split into tiered CSVs if screening scores are available.

## Process

1. Load profiles (CSV or JSON)
2. For each candidate above score threshold:
   a. Normalize current company name
   b. Parse past_positions, normalize employer names, sort by recency
   c. Find most recent notable employer (2018+)
   d. Extract years of experience, education, military background, tech highlights
   e. Select random template from appropriate category
   f. Fill template with clean data
   g. Clean output of any unicode/special characters
3. Export to CSV with UTF-8-BOM encoding for Excel compatibility

ARGUMENTS: $ARGUMENTS
