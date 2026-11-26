---
name: linkedin-platform
description: "LinkedIn content automation, profile optimization, and lead generation via the octopus-linkedin MCP server. Use when drafting, approving, scheduling, publishing, or analyzing LinkedIn posts — governed draft→approve→publish workflow."
personas:
  - PROPOSAL
  - CV
  - DOC
  - ARCH
  - DEV
  - DEVOPS
triggers:
  - linkedin platform
  - linkedin
  - linkedin post
  - لينكدإن
  - بوست لينكدإن
  - b2b outreach
  - profile optimization

---

# LinkedIn Platform Skill

## Overview

This skill provides AI agents with LinkedIn automation capabilities through the
`octopus-linkedin` MCP server. It follows a **governed workflow**:

```
draft → review → approve → publish → comment → analyze
```

Drafting and approval are **local-only** — they never touch LinkedIn. The
`publish_draft` tool is the single gate that sends content out, and it refuses
to publish unapproved drafts.

## Prerequisites

1. **LinkedIn Developer App** — create at https://www.linkedin.com/developers/apps/new
2. **Products enabled**: Share on LinkedIn, Sign In with LinkedIn (OpenID Connect)
3. **Access token** — generate via `octopus-linkedin authorize` or the
   [Token Generator](https://www.linkedin.com/developers/tools/oauth/token-generator)
4. **Token storage** — `site-packages/token.json` (local, never committed)
5. **Scopes**: `r_liteprofile`, `w_member_social`, `r_member_social`

## MCP Tools (18 total)

### Profile (read-only)

| Tool | Description |
|------|-------------|
| `linkedin_get_profile` | Get authenticated user's profile (name, headline, email) |

### Direct posting

| Tool | Description |
|------|-------------|
| `linkedin_create_post` | Publish a text post (text, visibility=PUBLIC\|CONNECTIONS) |
| `linkedin_share_link` | Publish a post with URL preview card (text, url) |
| `linkedin_share_image` | Publish a post with one local image (text, image_path) |
| `linkedin_delete_post` | Delete a post by URN |

### Draft workflow (governed)

| Tool | Sends to LinkedIn? | Description |
|------|:---:|-------------|
| `linkedin_create_draft` | ⬜ local | Save a draft (text, kind=text\|link\|image) |
| `linkedin_list_drafts` | ⬜ local | List drafts, optionally by status |
| `linkedin_get_draft` | ⬜ local | Read one draft by ID |
| `linkedin_update_draft` | ⬜ local | Edit a draft (resets approval) |
| `linkedin_approve_draft` | ⬜ local | **The review gate** — approve before publishing |
| `linkedin_delete_draft` | ⬜ local | Delete a draft |
| `linkedin_schedule_draft` | ⬜ local | Schedule an approved draft (ISO 8601 datetime) |
| `linkedin_unschedule_draft` | ⬜ local | Clear a draft's scheduled time |
| `linkedin_publish_draft` | ✅ | Publish an **approved** draft now |
| `linkedin_publish_due` | ✅ | Publish all approved drafts whose time has come |

### Comments & engagement

| Tool | Description |
|------|-------------|
| `linkedin_list_comments` | List comments on a post you control |
| `linkedin_reply_comment` | Reply to a comment on your post |

### Analytics

| Tool | Description |
|------|-------------|
| `linkedin_get_post_stats` | Get likes + comments count for a post |

## Use Cases

### 1. Content automation (PROPOSAL + DOC personas)

**Scenario**: Auto-generate LinkedIn posts from project completions.

```
User: "اكتب post عن إني خلصت مشروع Laravel جديد"

Agent workflow:
1. linkedin_create_draft(text="...", kind="text")  → draft_id
2. Show draft to user for review
3. User approves
4. linkedin_approve_draft(draft_id)
5. linkedin_publish_draft(draft_id)
```

### 2. Profile optimization (CV persona)

**Scenario**: Analyze and improve LinkedIn profile.

```
User: "حسن الـ profile بتاعي"

Agent workflow:
1. linkedin_get_profile()  → current profile data
2. Analyze headline, about, experience
3. Suggest optimized versions with keywords
4. User applies suggestions manually on LinkedIn
```

### 3. Scheduled content (DEVOPS persona)

**Scenario**: Schedule a week of posts in advance.

```
User: "جدول 5 posts للأسبوع الجاي"

Agent workflow:
1. Generate 5 draft posts
2. linkedin_create_draft() × 5  → 5 draft_ids
3. User reviews + approves each
4. linkedin_approve_draft() × 5
5. linkedin_schedule_draft(draft_id, publish_at) × 5
6. linkedin_publish_due() runs via cron/CLI
```

### 4. Post performance analysis (ARCH persona)

**Scenario**: Analyze which posts perform best.

```
User: "إيه الـ posts اللي شغالة أكتر؟"

Agent workflow:
1. linkedin_list_drafts(status="published")  → list of post URNs
2. linkedin_get_post_stats(urn) × N
3. Rank by likes + comments
4. Report top performers + content patterns
```

### 5. Cross-platform synergy (PROPOSAL persona)

**Scenario**: Post about a completed Upwork project on LinkedIn.

```
User: "انشر على LinkedIn إني خلصت مشروع على Upwork"

Agent workflow:
1. upwork_list_contracts(status="active")  → recent projects
2. Generate LinkedIn post from project details
3. linkedin_create_draft(text="...", kind="text")
4. User reviews + approves
5. linkedin_publish_draft(draft_id)
```

## Content Guidelines

### Effective LinkedIn posts

- **Hook in first 3 lines** — LinkedIn truncates after ~210 chars
- **Use line breaks** — white space improves readability
- **End with a question or CTA** — drives engagement
- **Add 3-5 hashtags** — but place them at the end, not in the body
- **Best times**: Tue-Thu, 8-10am (local time)
- **Avoid**: links in body (LinkedIn suppresses reach); put link in comments

### Brand voice

The `octopus-linkedin` server supports brand-voice memory. Train it by:
1. Publishing 5-10 posts in your natural voice
2. The LLM layer learns your tone, vocabulary, rhythm
3. Future drafts match your style automatically

## Security

- **Token storage**: `site-packages/token.json` (local only, never committed)
- **`.gitignore`**: blocks `token.json`, `*.token`, `*.secret`, `credentials.json`
- **No credentials in code**: plugin reads token from file/env, never hardcoded
- **Token expiry**: ~60 days; re-run `octopus-linkedin authorize` to refresh
- **Governed publishing**: no content goes live without explicit approval

## CLI Commands

```bash
# Profile
aizee linkedin profile

# Direct post
aizee linkedin post "Hello, world!" --visibility PUBLIC

# Draft workflow
aizee linkedin draft "A post to review later"
aizee linkedin drafts --status approved
aizee linkedin approve drft_abc123 --note "lgtm"
aizee linkedin schedule drft_abc123 2026-07-02T09:00:00Z
aizee linkedin publish drft_abc123

# Analytics
aizee linkedin stats urn:li:share:123
```

## Related Skills

- `social-media-marketing` — LinkedIn is ONE channel within this broader skill; use it for cross-channel strategy, calendars, and measurement across X/Instagram/YouTube/TikTok/Facebook.
- `cv-writer` — LinkedIn profile optimization + CV/resume writing
- `proposal-writer` — Cross-platform content generation (Upwork + LinkedIn)
- `freelance-platforms` — Upwork, Fiverr, Freelancer integration

## Cross-Channel Notes

- LinkedIn is a single distribution channel. For X (Twitter) and YouTube, draft natively per platform voice and reuse the approved LinkedIn message as the seed — do not cross-post verbatim.
- Analytics: alongside `linkedin_get_post_stats`, pull `social_analytics` (from the `social-media-marketing` skill) for unified cross-platform reach/engagement reporting.
