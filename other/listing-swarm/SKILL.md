---
name: listing-swarm
description: Submit your AI product to 70+ AI directories. Agent automates form filling, captcha solving (BYOK 2captcha), and email verification (BYOK IMAP). Save 10+ hours of manual submissions. User provides their own API keys - no credentials stored in skill.
version: 1.0.3
author: LinkSwarm
website: https://linkswarm.ai/skill/
security: BYOK
metadata:
  openclaw:
    requires:
      env:
        - CAPTCHA_API_KEY
        - CAPTCHA_SERVICE
        - IMAP_USER
        - IMAP_PASSWORD
        - IMAP_HOST
      bins:
        - node
    primaryEnv: CAPTCHA_API_KEY
    user-invocable: true
    disable-model-invocation: true
---

# Listing Swarm 🐝

**A Clawdbot skill to list your AI product on 70+ AI directories.**

Your agent does the submissions. You bring your captcha API key. Human assists when stuck.

---

## 🔒 Security Model: BYOK (Bring Your Own Key)

> **This skill contains ZERO credentials.** All API keys and passwords are provided by YOU at runtime via environment variables. Nothing is stored, logged, or transmitted to LinkSwarm.

| What | Security |
|------|----------|
| Captcha API | ✅ Your key, your account, your billing |
| Email/IMAP | ✅ Your credentials, optional, never stored |
| Data flow | ✅ Your product info → directory forms (that's it) |
| Source code | ✅ Fully readable, no obfuscation |

**See [SECURITY.md](SECURITY.md) for complete security documentation.**

---

## What It Does

Automates submitting your AI tool to directories like:
- There's An AI For That
- Futurepedia  
- OpenTools
- TopAI.tools
- AI Tool Guru
- 65+ more

## Setup

### 1. Get Your Own Captcha Solver API Key (Required)

⚠️ **You must get your own API key.** The skill does not include one.

1. Go to [2Captcha.com](https://2captcha.com) (recommended)
2. Create an account
3. Add funds (~$3 covers 1000 captchas, enough for all 70 directories)
4. Copy your API key from the dashboard

Then add to your environment:
```bash
export CAPTCHA_API_KEY="your-own-2captcha-key"
export CAPTCHA_SERVICE="2captcha"
```

Alternative services (same process):
- [Anti-Captcha](https://anti-captcha.com)
- [CapSolver](https://capsolver.com)

**No API key?** The agent will flag each captcha for you to solve manually.

### 2. Email Access for Auto-Verification (Optional)

Most directories send verification emails. Your agent can handle these automatically if you provide IMAP access.

**Recommended:** Create a dedicated email for submissions:
```
yourproduct.listings@gmail.com
```

**For Gmail:**
1. Create the email account (or use existing)
2. Enable 2-Factor Auth: Google Account → Security → 2-Step Verification
3. Create App Password: Google Account → Security → App passwords → Generate
4. Copy the 16-character password

Set environment variables:
```bash
export IMAP_USER="yourproduct.listings@gmail.com"
export IMAP_PASSWORD="xxxx xxxx xxxx xxxx"  # app password, not your real password
export IMAP_HOST="imap.gmail.com"
```

**No email access?** Agent will flag you: "Check your email for verification link from Futurepedia"

### 3. Your Product Info

Create a product config the agent can reference:
```json
{
  "name": "Your Product Name",
  "url": "https://yourproduct.ai",
  "tagline": "One line description (60 chars)",
  "description": "Full description for directory listings...",
  "category": "AI Writing Tool",
  "pricing": "Freemium",
  "logo_url": "https://yourproduct.ai/logo.png",
  "screenshot_url": "https://yourproduct.ai/screenshot.png",
  "email": "hello@yourproduct.ai"
}
```

## Usage

Tell your Clawdbot agent:

> "Use the listing-swarm skill to submit my product to AI directories. My product info is in product.json. My 2captcha key is in the environment."

The agent will:
1. Load the directory list
2. Visit each directory's submit page
3. Fill out the form with your product info
4. Solve captchas using your API key
5. Flag you if it gets stuck (needs login, payment, etc.)
6. Track what's submitted

## Human-in-the-Loop

When the agent hits something it can't handle:
- "Hey, this directory needs you to create an account first"
- "This one requires payment for listing"
- "Captcha failed 3 times, can you solve this one?"

You solve it, tell the agent to continue.

## Directory List

Full list in `directories.json`. Includes:
- Directory name and URL
- Submit page URL
- Domain rating
- Monthly traffic
- Free vs paid listing
- Notes on submission process

## Tracking

Submissions tracked in `submissions.json`:
```json
{
  "directory": "Futurepedia",
  "status": "submitted",
  "submitted_at": "2026-02-09",
  "listing_url": null,
  "notes": "Pending review"
}
```

## Files

```
listing-swarm/
├── SKILL.md           # This file
├── directories.json   # 70+ AI directories with submit URLs
├── submissions.json   # Track your submissions
└── captcha.js         # Captcha solver integration
```

## Tips

- **Start with free directories** - Many accept free submissions
- **Have screenshots ready** - Most require at least one
- **Consistent branding** - Use same name/tagline everywhere
- **Check emails** - Many send verification links

## Why This Exists

Getting listed on AI directories is tedious. 70+ sites, each with different forms. Your agent can do the grunt work while you handle the few things that need a human.

Part of [LinkSwarm](https://linkswarm.ai) - the AI visibility network.
