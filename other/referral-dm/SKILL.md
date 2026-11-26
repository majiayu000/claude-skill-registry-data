---
name: referral-dm
description: Get noticed and referred at tech companies through the channels that actually work. It writes comments on LinkedIn hiring posts, LinkedIn connection notes (200 characters by default, 300 for Premium), DMs and InMails, alumni and recruiter outreach, cold emails, warm-up engagement before an ask, follow-ups, and a paste-ready referral blurb, all personalised and never spammy. Use when the user wants a referral, wants to reply to or comment on a hiring post, message a recruiter or employee on LinkedIn, cold email a company, reach alumni, or follow up on an application.
---

# Referral DM

A cold "please refer me" to a stranger rarely works. Many employees won't refer someone they don't know, and some companies don't allow it at all. Referrals and interviews come from a **path**: get noticed → start a real conversation → make a small, easy ask. This skill picks the right path and writes every message on it.

## 0. Inputs

1. Call the Skill tool with "cracked-profile" (name, status, role, resume, GitHub).
2. If a company is named, call the Skill tool with "company-intel". Its brief helps the "why this company" line, and tells you whether the role posts publicly.
3. Ask only for what's missing, in one round:
   - **The opening**: a hiring post (paste it), a job ID/link, a specific person, or "I just want to get into <Company>".
   - **Recipient** (if any): their role (engineer on the team / recruiter / hiring manager / alumnus / founder), plus any real connection (same college, their post or talk, their open-source project, a mutual connection).
   - **Best proof** for this role: one project, internship or achievement, ideally with a link.

Never scrape or guess personal details. Use only what the user provides, or public professional pages they point you to.

## 1. Pick the path

Recommend the path with the best odds, and say why in one line:

| Situation | Best path |
|---|---|
| A hiring post on LinkedIn/X ("We're hiring, comment below") | **Comment** (§2.1), then a **DM** to the poster referencing it |
| A recruiter is posting the role | A short **DM or InMail** to the recruiter with the job ID; no referral needed |
| A specific engineer on the team, no relationship | **Warm-up first** (§2.4): 1–2 genuine interactions over a week, *then* a connection note, then the ask |
| Alumni from their college at the company | An **alumni connection note**, where the shared college is the hook; ask for 10 minutes of advice first, a referral second |
| A startup or founder | A **direct, value-first DM or email** to the founder: what you built that's relevant, and a link |
| No person, just the company | Apply on the careers page first, then find a recruiter or alumnus and message them with the application ID |

## 2. Write the messages

### 2.1 Comment on a hiring post
- 1–3 lines, **specific and visible**: the role, one proof, and a hook. Not just "Interested".
- `Interested in the SDE-1 Backend role. I built a Go rate limiter handling [N] req/s (link in profile). Sending you a DM with my resume.`
- Then write the **follow-up DM** to the poster, referencing the comment.
- Give 2 variants. Tell them to comment early (posts get flooded) and to make sure their profile headline matches the role.

### 2.2 Connection note (LinkedIn)
- **Default limit: 200 characters.** That's the most-cited limit for free accounts. Premium is commonly 300, and some sources report 300 for everyone (checked 2026-11; LinkedIn changes this). Write every default variant at ≤ 200 and offer one ≤ 300 Premium variant. If you have a web tool, verify the current limit; otherwise tell the user the composer enforces the real limit.
- Free accounts get only a few personalised notes per month. **A blank connection request plus a DM after they accept** is a perfectly good path, so offer it.
- Shape: a hook (why them) → who you are in a few words → a soft reason to connect. **No ask in the note** unless the path is recruiter + job ID.
- Show the exact **character count** for each variant.

### 2.3 DM / InMail / email (after connecting, or to a recruiter)
- ≤ 100 words for a DM, ≤ 150 words for an email.
- Structure: a specific hook → one proof (with a link) → **one small, clear ask** ("Would you be open to referring me for SDE-1, Job ID 12345?", or for alumni "Could I ask you 3 quick questions about the team?") → an easy out ("Totally understand if not").
- Emails: 3 subject lines, short and specific, e.g. `SDE-1 (Job 12345): built a Go rate limiter`.

### 2.4 Warm-up (when there's no relationship)
Plan 1–2 genuine touches before the ask: a thoughtful comment on their recent post (draft it, but they must actually read the post), or a reaction to their talk, blog or open-source project. **No fake engagement.** Comments must add something real.

### 2.5 Referral blurb
2–3 lines the referrer can paste into their internal referral form: `<Name> is a <graduation year from profile> <degree> grad who built <X> with <Y> (<link>), strong in <skill>. Applying for <role>, Job ID <id>.` Fill every field from the profile or the user. Never guess a year or degree.

### 2.6 Follow-up
One polite follow-up after 5–7 days with no reply, adding something new (an updated project, a newly posted role). **Max one.** After that, move on.

## 3. Rules for every message

- No "Dear Sir/Ma'am", "I hope this finds you well", "I am writing to…", or "please refer me" with nothing else.
- One proof and one ask per message. Make yes take 30 seconds: include the job ID and resume link.
- Never fabricate a connection, a shared experience, or an achievement.
- Respect a no or no reply. Don't double-message, and don't message several people on the same team on the same day.

## 4. Tracker

For multiple targets, keep `$CRACKED_DIR/outreach.md` (append):
`| Company | Person (role) | Path | Sent | Status | Follow-up on |`
Personalise every message. No identical blasts.

## Hard limits

- You **draft**. You never send messages, comment, connect, or email on the user's behalf unless they explicitly ask and have a tool configured. Even then, confirm each one.
- No mass-messaging, scraping, or automation against LinkedIn's terms of service.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
