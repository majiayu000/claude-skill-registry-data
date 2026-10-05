---
name: referral-program
description: 'Referral program design - referrer / referee incentive structure, viral mechanics, fraud and abuse controls, attribution, and channel placement. Use when: referral program, refer a friend, viral loop design, K-factor, advocacy referrals, partner referrals, customer referral incentives, referral attribution, viral coefficient.'
---

# Referral Program (RIPPLE Framework)

Design a referral program with a real viral mechanic - not a "refer a friend" button buried in settings. RIPPLE forces explicit design of who refers, why they refer, what the receiver gets, where the program lives, and how it's measured against a viral coefficient.

## Core Principle

**Referral programs fail because they optimize for the *sender's* reward and ignore the *receiver's* trust.** A high-K loop requires both. RIPPLE designs both sides of the exchange and instruments the loop end-to-end.

## The RIPPLE Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **R** | Reward Architecture | What does the referrer get, what does the referee get, and when? |
| **I** | Invite Mechanic | How is the invite sent, and how low-friction is the share? |
| **P** | Placement | Where in the product / journey does the ask appear? |
| **P** | Proof | What social proof and trust signals accompany the invite? |
| **L** | Loop Math | What's the viral coefficient target, and which lever moves it? |
| **E** | Evaluate & Defend | How is fraud, cannibalization, and incremental lift measured? |

## Reward Architecture

The most common failure mode is **single-sided** rewards.

| Type | Pattern | Best For |
|------|---------|----------|
| **Double-sided** | Both referrer and referee get reward | Most consumer / SMB programs |
| **Single-sided (referrer)** | Only referrer rewarded | Pure-advocacy programs (low conversion lift) |
| **Single-sided (referee)** | Only referee rewarded | When referrer reward feels mercenary (e.g., enterprise) |
| **Tiered** | Reward escalates with N successful referrals | Power-user motivation |

Reward type considerations:

| Reward | Pros | Cons |
|--------|------|------|
| **Cash / credit** | Simple, easy attribution | Attracts abuse, low brand lift |
| **Product credit** | Reinforces product use | Less appealing if not active user |
| **Account upgrade** | Aligns with retention | Limited liability cap |
| **Cause donation** | High-trust, brand-aligned | Smaller activation lift |
| **Exclusive access** | Status-driven, low cost | Niche appeal |

## Invite Mechanic

Friction is the silent killer of K-factor:

| Lever | High-Friction | Low-Friction |
|-------|---------------|--------------|
| **Channel** | Email-only | Email + SMS + share link + native share sheet |
| **Personalization** | Generic copy | Pre-filled referrer name + custom note field |
| **Tracking** | Manual code | Auto-attributed unique link |
| **Recipient onboarding** | Standard signup | Landing page with referrer context |

## Placement

Placement determines who sees the ask and when.

| Placement | When It Works |
|-----------|---------------|
| **Post-aha moment** | After the first clear value event - referrer is intrinsically motivated |
| **Account / settings page** | Permanent home, low discoverability |
| **Email lifecycle** | Anniversary, milestone, or NPS positive |
| **In-app banner** | High visibility; must be dismissible |
| **CSM / sales triggered** | B2B; manual but high quality |

## Loop Math

| Metric | Definition | Target |
|--------|------------|--------|
| **Referral rate** | % of eligible customers who refer at least once in window | 5-15% strong |
| **Invites per referrer** | Average invites sent by active referrer | 3-8 strong |
| **Conversion rate** | % of invitees who become customers | 5-25% varies by motion |
| **K-factor** | Referral rate × Invites × Conversion | > 1.0 = self-sustaining loop |
| **Cycle time** | Days from invite to converted referee | Shorter = faster compounding |

## Fraud & Cannibalization Controls

| Risk | Control |
|------|---------|
| **Self-referral** | Device / IP / payment-instrument matching |
| **Fake account farms** | Rate limits + manual review thresholds |
| **Reward abuse** | Cap rewards per referrer per window |
| **Cannibalization** | Match referrer-influenced cohort against organic; measure incrementality |
| **Channel arbitrage** | Block paid-media referrers if program is meant for organic |

## Output

Save to `outputs/referral-program-[motion]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Reward Design** | Sender + receiver rewards, tier escalation, liability cap |
| **Invite Spec** | Channels, copy, personalization, tracking |
| **Placement Map** | Where the ask appears across product / lifecycle |
| **Loop Math Model** | K-factor projection with sensitivity analysis |
| **Fraud Controls** | Detection rules and reward holds |
| **Attribution Spec** | Tracking schema, incrementality test design |
| **KPIs Dashboard** | Referral rate, invites/referrer, conversion, K-factor, fraud rate |

## Process

1. **Pick reward architecture** with sender + receiver explicit
2. **Strip friction** from the invite mechanic; benchmark every step
3. **Place the ask** at intrinsic-motivation moments (post-aha is gold)
4. **Add proof** - testimonials, "X people have invited friends," referrer endorsement
5. **Model the loop math** with sensitivities; identify the binding constraint
6. **Instrument fraud and incrementality** before launching, not after

## Tips

1. **K-factor < 1 is fine** if it lowers blended CAC; don't only chase virality
2. **Reward at successful action**, not invite, to align with revenue
3. **Run a holdout** to prove incrementality - most teams skip this
4. **Refresh rewards** quarterly; novelty drives participation
5. **B2B referrals** often work better as advocacy plays than cash bounties

## Pairs With

- **customer-advocacy** - Top advocates are the highest-K referrers
- **community-catalyst** - Communities amplify referral loops
- **loyalty-lifecycle** - Tiered status integrates with referral milestones
- **demand-engine** - Channel mix that promotes the program
