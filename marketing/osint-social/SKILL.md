---
name: osint-social
description: Social media reconnaissance skill — platform enumeration, Google dork patterns, cross-platform identity resolution, public data collection without scraping, and digital footprint analysis.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, social-media, identity-resolution, google-dorks, digital-footprint, linkedin, twitter, facebook]
    triggers: [social-media, social, digital-footprint, identity-resolution, google-dork, find-profile, social-recon]
    related_skills: [osint-person, osint-facial, osint-recon]
---

# OSINT Social Media Reconnaissance

Social media intelligence from public sources — platform enumeration, Google dorking, cross-platform identity resolution, and digital footprint analysis using only publicly available information and respecting platform terms of service.

## Prerequisites

### Required Tools
- **Web browser** (Firefox DevTools MCP)
- **Terminal** with curl/jq
- **No MCP servers required** for manual public-data techniques

### Recommended (but optional) Tools
- **Sherlock**: https://github.com/sherlock-project/sherlock (username search across 400+ sites)
- **Holehe**: https://github.com/megadose/holehe (email registration check across 100+ platforms)
- **WhatsMyName**: https://whatsmyname.app (web-based username check)
- **Google Alerts**: https://www.google.com/alerts (monitor names/brands)
- **Namechk**: https://namechk.com (username availability checker)
- **Social Bearing**: https://socialbearing.com (Twitter analytics, free tier)
- **PhantomBuster**: https://phantombuster.com (ethical automation, paid)
- **Google Dork Cheat Sheet**: See below

## Public Social Media Sources

### Major Platforms
| Platform | Public Info Available | Typical Use Case |
|----------|----------------------|------------------|
| LinkedIn | Profile, job history, education, skills, connections (partial) | Professional recon |
| Facebook | Name, profile pic, public posts, pages, groups, photos | Personal recon |
| Twitter/X | Bio, posts, follows, followers, media, lists | Real-time activity monitoring |
| Instagram | Bio, photos, followers (public accounts) | Visual recon, location patterns |
| TikTok | Bio, public videos | Youth demographic recon |
| Reddit | Post/comment history, subreddit participation | Interests, opinions |
| GitHub | Repos, contributions, profile, organizations | Technical skills |
| YouTube | Channel, videos, comments, playlists | Content interests |
| Pinterest | Boards, pins, interests | Lifestyle, design, planning |
| Medium | Articles, responses, publications | Professional writing |
| Substack | Newsletters, subscriber counts | Thought leadership |
| Strava | Exercise routes, heat maps | Location inference |
| Meetup | Groups, events, RSVPs | Professional/personal network |
| Goodreads | Books read, reviews | Reading preferences |
| Quora | Answers, questions, topics | Knowledge areas |
| Wikipedia | Edit history, talk page participation | Specialized knowledge |
| Stack Overflow | Answers, reputation, badges | Technical expertise |
| Foursquare | Venue tips, check-ins (historical) | Location patterns |
| Eventbrite | Events hosted/attended | Professional networking |

## Google Dork Patterns

### Basic Google Operators
```text
"exact phrase"        → Exact match search
site:example.com      → Limit to specific site
-inurl:spam           → Exclude URLs containing "spam"
intitle:"profile"     → Pages with "profile" in title
inurl:about           → URLs containing "about"
filetype:pdf          → Specific file types
link:example.com      → Pages linking to example.com
related:example.com   → Similar sites
cache:example.com     → Google cached version (historical)
```

### Social Media Specific Dorks

```text
# LinkedIn
site:linkedin.com/in "Jane Smith" "Portland"
site:linkedin.com/in "Software Engineer" "Jane"
site:linkedin.com/company "Acme Corp" employees
site:linkedin.com/company "Acme Corp" about
site:linkedin.com/pub "Jane Smith" "Portland"

# Facebook
site:facebook.com "Jane Smith" "Portland"
site:facebook.com intitle:"Jane Smith"
site:facebook.com/people "Jane" "Portland" "OR"
site:facebook.com/public/"Jane-Smith"

# Twitter / X
site:twitter.com "Jane Smith" Portland
site:x.com "Jane Smith" Oregon
site:twitter.com intitle:"Jane Smith"

# Instagram
site:instagram.com "jane.smith"
site:instagram.com/p/ "Jane Smith"           # Photo captions

# Reddit
site:reddit.com "Jane Smith"
site:reddit.com/user/"Jane Smith"
site:reddit.com "Smith" subreddit:Portland

# GitHub
site:github.com "Jane Smith"
site:github.com/ "jane-smith" inurl:README
site:github.com/ "email: jane@example.com"   # Look for exposed emails

# YouTube
site:youtube.com "Jane Smith" inurl:channel
site:youtube.com "Jane Smith" inurl:about
site:youtube.com/watch "Jane Smith" intitle:"comment"  # Comments

# Medium
site:medium.com "Jane Smith"
site:medium.com/@jane.smith

# General presence
site:about.me "Jane Smith" Portland
site:linktr.ee "Jane Smith"
site:behance.net "Jane Smith"
site:dribbble.com "Jane Smith"
site:pinterest.com "Jane Smith"
site:goodreads.com "Jane Smith"
site:gravatar.com "Jane Smith"
site:keybase.io "Jane Smith"
site:angel.co "Jane Smith"                   # AngelList
site:crunchbase.com "Jane Smith"             # Startup profiles
site:zoominfo.com "Jane Smith"               # Professional profiles
site:spokeo.com "Jane Smith"                 # Public records aggregator
```

### Advanced Dork Patterns

```text
# Find email addresses
"Jane Smith" "@" "gmail.com" OR "@" "yahoo.com" OR "@" "outlook.com"
"Jane Smith" email
site:linkedin.com/in "Jane" email

# Find resumes (often contain detailed personal info)
intitle:resume "Jane Smith" Portland filetype:pdf
intitle:cv "Jane Smith" filetype:docx
"Jane Smith" resume "Software Engineer" Portland

# Find documents with personal info
"Jane Smith" phone filetype:pdf
"Jane Smith" address filetype:pdf
"Jane Smith" "SSN" - DO NOT USE — illegal search pattern
"Jane Smith" "DOB" filetype:xlsx

# Breach/corpus mentions
"Jane Smith" "haveibeenpwned"
"Jane Smith" "password" filetype:txt           # Potential breach remnants

# Personal websites
"Jane Smith" "my website" OR "personal website"
"Jane Smith" "wix.com" OR "squarespace.com" OR "wordpress.com"

# News mentions
"Jane Smith" "ABC Corp" site:nytimes.com
"Jane Smith" "ABC Corp" site:wsj.com
"Jane Smith" "ABC Corp" site:bloomberg.com
"Jane Smith" "award" OR "promoted" OR "hired"
```

## Step-by-Step Workflows

### 1. Identity Resolution — Name → Profiles

```python
# Discovery workflow
name = "Jane Smith"
location = "Portland, OR"
employer = "Acme Corp"  # If known

# Phase 1: Google reconnaissance
google_queries = [
    f'"{name}" "{location}"',
    f'"{name}" linkedin',
    f'"{name}" "{employer}"',
    f'"{name}" github',
    f'"{name}" twitter',
    f'"{name}" facebook',
]

# Phase 2: Platform-specific searches
platforms = {
    "linkedin": f"site:linkedin.com/in \"{name}\" \"{location}\"",
    "facebook": f"site:facebook.com \"{name}\" \"{location}\"",
    "twitter": f"site:twitter.com \"{name}\" \"{location}\"",
    "github": f"site:github.com \"{name}\" \"{employer}\"",
}
```

### 2. Username → Cross-Platform Mapping

```bash
# ── SHERLOCK ── Username search across 400+ social networks ──
# Install: pip install sherlock-project
# GitHub: https://github.com/sherlock-project/sherlock

# Basic usage
sherlock jane.smith123

# Check multiple usernames at once
sherlock jane.smith123 jsmith jane_smith

# Save results to JSON
sherlock jane.smith123 --output /tmp/sherlock_results.json

# Save to CSV for spreadsheet analysis
sherlock jane.smith123 --csv

# Save to Excel
sherlock jane.smith123 --xlsx

# Print only found accounts (clean output)
sherlock jane.smith123 --print-found

# Increase timeout for slow sites (default 60s)
sherlock jane.smith123 --timeout 30

# Use Tor proxy (requires tor to be running)
sherlock jane.smith123 --tor

# Check a single specific site by name
sherlock jane.smith123 --site instagram

# Bypass NSFW site filtering (checks adult platforms too)
sherlock jane.smith123 --nsfw

# Username variation engine — replaces {?} with _ - .
sherlock jane{?}smith     # Checks: jane_smith, jane-smith, jane.smith

# Check from a list of usernames in a file
sherlock --folderoutput /tmp/sherlock/ $(cat usernames.txt)

# Real-world example: find all accounts for a target
sherlock yourusername --print-found --output /tmp/paulie_accounts.json

# Method 2: WhatIsMyName (web)
# navigate_page to: https://whatsmyname.app/
# Enter username → returns matches across 300+ platforms

# Method 3: Manual search
for platform in "github.com" "twitter.com" "instagram.com" "reddit.com" "medium.com" "keybase.io"; do
  echo "Searching $platform/jane.smith123..."
  curl -sI "https://www.$platform/jane.smith123" | head -1
done
```

**Username Variations to Try:**
```
jane.smith
janesmith
jane_smith
jane-smith
j.smith
janesmith123
jane.smith.portland
jane.smith.90210
jane.smith.acme
jsmith
jane_s
itsjanesmith
iamjanesmith
jane_the_smith
ms.jane.smith
```

### 3. Email → Cross-Platform Registration Check (Holehe)

Holehe checks if an email address is registered on 100+ platforms **without sending a password reset email or alerting the target**. It works by exploiting subtle differences in how registration/login pages respond to existing vs. non-existent accounts — the same technique used by federal investigators.

**Install:** `pip install holehe`
**GitHub:** https://github.com/megadose/holehe

```bash
# Basic usage — check email across all platforms
holehe target@email.com

# Show only platforms where the email IS registered (clean output)
holehe target@email.com --only-used

# Disable password recovery attempts (faster, less detectable)
holehe target@email.com -NP

# CSV output for record-keeping
holehe target@email.com -C

# Increase timeout for slow sites (default: 10s)
holehe target@email.com -T 15

# Check multiple emails at once
holehe target1@email.com target2@email.com --only-used

# Real-world example: confirm a target's email usage
holehe the operator@gmail.com --only-used -NP
```

**What Holehe reveals:**
- Which social platforms the email is tied to (Facebook, Twitter, Instagram, LinkedIn)
- Which professional/creative platforms (GitHub, Medium, Adobe, Spotify)
- Which utilities/services (Amazon, PayPal, Discord, Telegram)
- Dating apps, forums, and industry-specific platforms

**Detection evasion:**
- `-NP` flag skips actual password recovery flows — reduces footprint
- No email is ever sent to the target
- Results come from analyzing HTTP response differences, not from triggered notifications
- The tool is silent — the target has no way to know you checked

**Cross-reference with Sherlock:**
```
Email (Holehe) → platforms registered → reveals associated usernames
Username (Sherlock) → cross-platform accounts → confirms identity
```

### 4. LinkedIn Profile Reconnaissance

```python
# LinkedIn public profile analysis
# Requires Firefox DevTools MCP

# Step 1: Search Google for the profile
# Step 2: Open LinkedIn profile (may need to be logged in)
# Step 3: Extract public info

linkedin_profile_data = {
    "name": "Jane Smith",
    "headline": "Software Engineer at Acme Corp",
    "location": "Portland, Oregon Area",
    "about": "Full-stack engineer...",  # "About" section
    "experience": [
        {"company": "Acme Corp", "title": "Senior Engineer", "dates": "2020-Present"},
        {"company": "TechCo", "title": "Developer", "dates": "2015-2020"},
    ],
    "education": [
        {"school": "Oregon State University", "degree": "BS CS", "years": "2010-2014"}
    ],
    "skills": ["Python", "JavaScript", "AWS", "Kubernetes"],
    "recommendations": 5,          # Number (counts of recommendations)
    "connections_count": 500,      # May not be visible
    "recent_activity": ["Posted about X...", "Commented on Y..."],  # If public
}
```

**What LinkedIn Reveals (Public without login):**
```
- Full name (may show "Jane S." if privacy settings)
- Headline (current role)
- Location (city/metro area)
- Industry
- Number of connections (500+, 3rd+)
- Recent profile activity
- Profile photo (may be public)
- Featured posts (if public)

**What LinkedIn Reveals (Logged In, Not Connected):**
- More detailed experience timeline
- Education details
- Skills (partial)
- Recommendations count
- About section
- Recent activity feed

**What LinkedIn Reveals (1st Connection):**
- Full profile (except private sections)
- Mutual connections
- Contact info (if shared)
- All skills and endorsements
```

### 5. Twitter/X Profile Reconnaissance

```bash
# Public Twitter data collection (no auth needed for basic)
# Step 1: Navigate to profile
# Step 2: Extract bio, header, pinned tweet
# Step 3: Review recent public tweets

# Advanced: Search tweets by user
curl -s "https://api.twitter.com/2/tweets/search/recent?\
query=from:janesmith\
&max_results=10" | jq .

# Tweet analysis patterns:
# - Location data from tweet metadata
# - Retweet patterns (affiliations)
# - Reply threads (connections)
# - Liked tweets (interests, may not be public)
# - Lists (categorization by user or others)
# - Follows/Followers (network mapping)
```

### 6. Facebook Reconnaissance

```
Facebook public information (varies by privacy settings):
- Name and profile picture (may be public)
- Cover photo (often public)
- Public posts (varies by user)
- About section (selected fields)
- Friends list (user-dependent)
- Liked Pages (may reveal interests)
- Groups (public group memberships)
- Reviews written (public)
- Events attended (public events)
```

**Facebook Search Techniques:**
```text
# Facebook graph search (limited as of 2024)
https://www.facebook.com/search/people/?q=jane%20smith%20portland
https://www.facebook.com/search/posts/?q=jane%20smith
https://www.facebook.com/public/jane-smith

# Facebook's directory page
https://www.facebook.com/directory/people/
```

### 7. GitHub Reconnaissance

```
GitHub public information:
- Profile: Name, bio, location, website, company, orgs
- Repositories: Code, README, issues, PRs
- Contributions: Calendar graph, activity history
- Gists: Code snippets
- Comments: On issues, PRs, commits
- Organizations: Affiliations
- Sponsors: If enabled
- GPG keys: Email addresses

Search patterns:
# Find email in commits
git log --format="%an <%ae>" | sort -u

# Find personal info in repos
# Search code for: API keys, configs, passwords
site:github.com "jane.smith" password
site:github.com "jane.smith" API_KEY
site:github.com "jane.smith" aws_secret_access_key
```

### 8. Digital Footprint Compilation

```markdown
## Digital Footprint: Jane Smith

### Professional Platforms
- [x] LinkedIn: linkedin.com/in/janesmith (500+ connections, active)
- [x] GitHub: github.com/janesmith (150 contributions last year)
- [ ] Medium: Not found
- [x] Stack Overflow: stackoverflow.com/users/12345 (2k reputation, 45 answers)

### Social Platforms
- [x] Twitter/X: @janesmith (2,500 tweets, 1,200 followers)
- [x] Facebook: facebook.com/jane.smith (limited privacy settings)
- [x] Instagram: @jane.smith.pdx (private account — bio only)
- [ ] TikTok: Not found
- [ ] Reddit: Not found with this name/username

### Content Platforms
- [x] YouTube: youtube.com/@janesmith (12 videos, 500 subs)
- [ ] Pinterest: Not found
- [ ] Substack: Not found
- [x] Goodreads: goodreads.com/janesmith (150 books)

### Other
- [x] Keybase: keybase.io/janesmith (verified social proofs)
- [x] About.me: about.me/janesmith
- [x] AngelList: angel.co/u/janesmith

### Breach / Security
- [x] HaveIBeenPwned: Email jane.smith@email.com found in 3 breaches
- [x] DeHashed: 2 records found (name + email)
- [ ] Dark web: Not searched (see osint-threat for methodology)

### Footprint Score: HIGH (13+ platforms, active on multiple)
```

## Common Pitfalls

### Privacy Settings
- **PITFALL**: Privacy settings change constantly; what was public yesterday may not be today.
- **SOLUTION**: Collect and cache data promptly. Note date of collection.
- **WORKAROUND**: Check Google cached versions for historical content.

### Fake / Impersonation Accounts
- **PITFALL**: Multiple accounts for the same name — at least some are impersonators or spam.
- **SOLUTION**: Verify identity cross-referencing photo, bio details, follower overlaps.
- **WORKAROUND**: LinkedIn verified profiles, Twitter blue check, GitHub verified email.

### Platform API Changes
- **PITFALL**: Platforms frequently change API access (Twitter/X drastically reduced free API).
- **SOLUTION**: Prefer web-based manual methods over API-dependent automation.
- **WORKAROUND**: Firefox DevTools MCP for extracting visible web data.

### Regional Platform Preferences
- **PITFALL**: Subject may use platforms dominant outside the US (VK, WeChat, Telegram).
- **SOLUTION**: Consider subject's geographic/cultural context.
- **WORKAROUND**: In Russia → search VK; China → WeChat/Weibo; Japan → LINE.

### Deleted / Abandoned Accounts
- **PITFALL**: Old profiles may still exist but be abandoned, giving a misleading impression.
- **SOLUTION**: Check last activity date on each platform.
- **WORKAROUND**: Archived content may persist (Internet Archive, Google Cache).

## Legal & Ethical Notes

> **⚠️ WARNING**: Social media OSINT is heavily regulated:
> - **No Automated Scraping**: LinkedIn, Facebook, Instagram, Twitter/X prohibit automated data collection in their ToS
> - **No Impersonation**: Creating fake profiles to gather intel is fraud and illegal in many states
> - **No Deception**: Do not connect with targets under false pretenses
> - **No Private Data**: Do not attempt to access private/restricted content
> - **Stalking Laws**: Monitoring someone's social media activity for harassment is illegal
> - **DPPA**: Location data from Strava/FourSquare may reveal home addresses
> - **Photo Rights**: Do not use profile photos without permission
> - **GDPR/ePrivacy**: EU subjects have enhanced protections
> - **UK Investigatory Powers Act**: Broader surveillance restrictions

### Permissible Methodology
- Use Google and search engines to find public profiles
- View only what is accessible without logging in (or with your own logged-in account viewing public content)
- Use Google cached pages for historical content
- Use Internet Archive (Wayback Machine) for historical website content
- Document everything with timestamps and URLs

### What NOT to Do
- ❌ Do not create fake accounts to friend/follow targets
- ❌ Do not use automated tools that scrape platforms
- ❌ Do not access private/restricted content
- ❌ Do not harvest contact information for spam
- ❌ Do not share screenshots of private interactions
- ❌ Do not use information for harassment, stalking, or doxxing

## Cross-References

- `security/osint-recon` — Full OSINT investigation pipeline
- `security/osint-person` — Detailed person investigation with enrichment
- `security/osint-facial` — Facial recognition matching across social platform photos
- `security/osint-threat` — Breach data analysis for exposed credentials
- `security/osint-redteam` — Social engineering vector identification from social data
- `software-development/web-scraping-scrapling` — If you need legitimate scraping with proper headers/respect
- `software-development/systematic-debugging` — Systematic approach to identity resolution problems

## Verification Checklist

- [ ] Google search performed with name + location + employer
- [ ] LinkedIn profile found and analyzed (public view)
- [ ] Google dork patterns executed for each major platform
- [ ] Username search across 10+ platforms
- [ ] GitHub profile checked for email/info exposure
- [ ] Twitter/X profile reviewed for connections and activity
- [ ] Facebook public profile reviewed
- [ ] Digital footprint score assigned
- [ ] Breach databases checked (HIBP, DeHashed)
- [ ] Privacy settings respected — no private content accessed
- [ ] All findings dated with source URLs
- [ ] Legal constraints documented
- [ ] Verification note: Social media data alone is insufficient for identity confirmation
