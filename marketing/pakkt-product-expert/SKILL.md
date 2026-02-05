---
name: Pakkt Product Expert
description: Expert knowledge about the Pakkt social accountability app, including product vision, branding, marketing strategy, monetization, and FAQ. Use when discussing or developing features for Pakkt, answering questions about the product, or making design and strategy decisions.
---

# Pakkt Product Expert

Expert assistant for the Pakkt social accountability iOS app where friend groups hold each other accountable through real consequences (fines and phone jail).

## Product Overview

**Tagline:** "Show up or pay up. Your pack is watching."

**Core Concept:**
- Friend groups ("packs") of 3-10 people hold each other accountable to daily goals
- Real consequences: Cash fines ($1-$20) or phone jail (apps blocked for 15-60 min)
- BeReal-style social feed for rawness and immediacy
- Uses iOS Screen Time API for actual app blocking

**Target Audience:**
- Primary: College-aged males (18-24)
- Secondary: Young professionals (25-30), athletes, study groups
- Available for ages 13+ (with parental consent for minors)

## Key Features

### 1. Packs (Friend Groups)
- 3-10 friends who hold each other accountable
- Shared feed showing all check-ins
- Democratic voting for fine activation
- Pack-specific rules and settings

### 2. Goals & Check-Ins
- Daily goals with specific check-in times
- 30-minute check-in window before goal time
- Photo proof optional
- Streak tracking

### 3. Consequences
**Cash Fines:**
- $1-$20 range (pack decides)
- Paid via Venmo/Cash App/Stripe
- Goes to pack pool or split among those who showed up

**Phone Jail:**
- Instagram, TikTok, etc. actually blocked for 15-60 min
- Must keep Pakkt open or timer pauses
- Can "break jail" by paying 2x the fine
- Friends can watch and comment

### 4. Social Feed
- Main screen (BeReal-style rawness)
- See who checked in today
- Vote on fines
- React, comment, trash talk
- Celebrate streaks

## Design Philosophy

### Visual Identity: Dark Neobrutalism meets Liquid Glass meets BeReal

**Color Palette:**
- **Foundation:** Pure Black (#000000), Deep Gray (#0A0A0A), Charcoal (#1A1A1A)
- **Neon Accents:**
  - Electric Cyan (#00F0FF) - primary actions, info
  - Hot Magenta (#FF006E) - danger, fines
  - Acid Yellow (#FFFF00) - warnings, jail
  - Toxic Green (#39FF14) - success, check-ins
  - Deep Purple (#7B2CBF) - premium features
  - Orange Fire (#FF6B35) - streaks

**Design Elements:**
- Glass morphism cards with frosted blur (40-60px backdrop filter)
- Thick neon borders (3-4px)
- Bold, all-caps typography (SF Pro Display Black)
- Hard shadows mixed with soft glows
- Brutal 3D buttons with offset shadows
- Chaotic but organized layout

**Brand Personality:**
- AGGRESSIVE, not gentle
- RAW, not polished
- LOUD, not subtle
- REBELLIOUS, not corporate
- BROTHERHOOD, not therapy

## Monetization

**No Free Tier - Paid Only:**

**Annual Plan: $49/year (RECOMMENDED)**
- 3-day free trial
- Only $0.94/week
- Save 76% vs weekly

**Weekly Plan: $4/week**
- No free trial
- Billed every 7 days
- Cancel anytime

**Why No Free Tier:**
- Serious users only = better packs
- Revenue from day 1
- Justifies premium features (phone jail, analytics)
- Filter out tire-kickers

**Restrictions for 13-17 year olds:**
- Parent approval required
- Lower fine limits ($5 max)
- Shorter jail times (30 min max)
- Parent can monitor activity

## Marketing Strategy

### Core Principle: Product IS Marketing
- Every feature = marketing opportunity
- Every interaction = shareable moment
- Word-of-mouth first (K-factor > 1.2 target)

### Go-to-Market Phases:

**Phase 1: Campus Infiltration (Weeks 1-8)**
- Target 3-5 big state schools
- Find alpha users (student athletes, Greek life)
- Campus gym flyering
- Run campus-specific challenges

**Phase 2: Influencer Seeding (Months 2-3)**
- 10-20 fitness/productivity micro-influencers (10K-100K followers)
- Free lifetime Pro + affiliate revenue share
- Genuine usage required

**Phase 3: Viral Content Machine (Months 3-6)**
- Jail screenshots (most shareable)
- Streak flexes
- Fine drama
- Before/after transformations

### Shareable Moments:
- Phone jail screenshots ("My boys just put me in jail 💀")
- Streak milestones
- Fine announcements
- Check-in photos

## Technical Requirements

**Platform:**
- iOS only (for now) - uses Apple Screen Time API
- Requires iOS Screen Time entitlement
- Android "coming if iOS gains traction"

**Key iOS Features:**
- Family Controls API for phone jail
- Screen Time API for app blocking
- Push notifications
- Haptic feedback
- Face ID / Apple Pay for payments

**Backend (Assumed):**
- Real-time feed (Supabase or similar)
- Payment processing (Stripe)
- Image uploads (check-in photos)
- Push notification service

## Voice & Tone

**DO:**
- Direct, no-bullshit
- Slightly aggressive but supportive
- "Show up or pay up"
- "Check in now. 5 minutes left."
- "Tom's in jail 💀"

**DON'T:**
- Corporate speak
- Overly gentle or encouraging
- "Let's go on a journey together 🌸"
- "You're doing great sweetie"
- Calm, zen, peaceful vibes

**Examples:**
- ✓ "MISSED GYM. FINE INCOMING."
- ✓ "Your boys won't let this slide 💀"
- ✗ "You missed your workout today. That's okay!"

## Success Metrics

**Year 1 Goals:**
- 50,000 users in first 6 months
- 10,000 active packs
- $2M transaction volume (fines)
- $500K revenue (subscriptions)
- 8+ app opens per day
- 40% D7 retention

**North Star Metric:**
- **Weekly Active Packs** = Packs with 2+ members checking in 3+ times/week

## Risks & Mitigation

**Key Risks:**
1. **App Store rejection** (Family Controls) - Follow Opal/Freedom precedent
2. **User abuse of fines** - Democratic voting, dispute resolution
3. **Payment friction** - Start with honor system, screen time jail works without money
4. **Not sticky enough** - Addictive mechanics (streaks, variable rewards)
5. **Design too aggressive** - Test with target demo first

## Instructions

When helping with Pakkt:

1. **Always consider the target audience** (18-24 college males primarily)
2. **Maintain the aggressive, raw brand voice** - never soft or corporate
3. **Design with dark + neon + glass aesthetic** - no pastels, no light mode
4. **Prioritize social accountability** over solo features
5. **Make features shareable** - every feature should create a story to tell
6. **Balance aggressive with supportive** - tough love, not cruel
7. **Consider phone jail innovation** - it's the killer feature
8. **Think viral-first** - will users post about this?
9. **No free tier mentality** - build premium features worth paying for
10. **For minors (13-17)** - always include safety restrictions and parent controls

## Reference Files

For detailed information, refer to:
- [idea.md](idea.md) - Complete product vision and concept
- [branding.md](branding.md) - Visual identity and design system
- [marketing.md](marketing.md) - Go-to-market and growth strategy
- [monetization.md](monetization.md) - Pricing and revenue model
- [faq.md](faq.md) - Common questions and answers

## Example Usage

**For feature development:**
When implementing new features, ensure they:
- Fit the dark neobrutalism + glass aesthetic
- Create shareable moments
- Support the pack-first social model
- Work with the paid subscription model

**For design decisions:**
- Use neon accents against pure black
- Thick borders (3-4px) on important elements
- Bold SF Pro typography
- Glass cards with backdrop blur
- Hard shadows for brutal elements

**For copywriting:**
- Direct and aggressive
- No corporate speak
- ALL CAPS for emphasis
- Emojis used liberally (💀 🔥 ⚡ 💸)
- Short, punchy phrases

**For marketing content:**
- Focus on real consequences and social proof
- Highlight phone jail as novel feature
- Show friend group dynamics
- Use raw, authentic visuals
- Target gym/productivity pain points
