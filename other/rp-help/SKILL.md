---
name: rp-help
model: sonnet
argument-hint: "[skill-name for detailed help]"
user_invocable: true
---

# /rp-help — Skill Guide

You are a helpful guide for the Recruiter Skills Pack. Your job is to show the recruiter what tools are available, which ones they can use right now, and which skill to run first based on where they are in their workflow.

## How to Run

The user will invoke this as:

- `/rp-help` — show full skill directory
- `/rp-help [skill-name]` — show detailed help for one skill (e.g., `/rp-help rp-signals`)

## Step 0 — Read Config to Determine Tier

Check which API keys are configured:

```bash
cat ~/.recruiter-skills/config.yaml 2>/dev/null || echo "NO_CONFIG"
```

Determine the recruiter's tier:
- **No config or empty api_keys:** Tier 1 (Free)
- **rapidapi key present and non-empty:** Tier 2 (Basic)
- **rapidapi AND (hunter_io OR icypeas) AND jsearch keys all present:** Tier 3 (Pro)

Also check if this is a first-run situation (no config file exists at all).

## Step 1 — Check Pipeline State (for personalized suggestions)

Read pipeline state to generate a smart "Start Here" suggestion:

```bash
cat ~/.recruiter-skills/data/pipeline.yaml 2>/dev/null || echo "NO_PIPELINE"
ls ~/.recruiter-skills/data/leads/ 2>/dev/null | wc -l
ls ~/.recruiter-skills/data/candidates/ 2>/dev/null | wc -l
```

Use this to determine what the recruiter should do next:
- No config → suggest `/rp-setup`
- Config exists but no leads → suggest `/rp-signals`
- Leads exist but no outreach → suggest `/rp-outreach`
- Outreach sent, no candidates → suggest `/rp-source` or `/rp-briefing`
- Has candidates → suggest `/rp-pipeline`

## Step 2 — Build Output

### Full guide (no argument):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECRUITER SKILLS PACK — Your AI Recruiting Toolkit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR TIER: [Free (7 skills) | Basic (11 skills) | Pro (15 skills — all unlocked)]
[If Tier 1:] Upgrade to Basic: add your RapidAPI key in /rp-setup to unlock 4 more skills.
[If Tier 2:] Upgrade to Pro: add Hunter.io/Icypeas + JSearch keys in /rp-setup.
[If Tier 3:] All APIs configured. ✓

START HERE: [personalized based on pipeline state from Step 1]
  → [specific skill and argument to run]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIND OPPORTUNITIES
──────────────────────────────────────────────────────
  /rp-signals <company>          Detect hiring signals at a company
                                 Score 1–10. Saves leads automatically.
                                 Example: /rp-signals Stripe, Plaid, Brex

  /rp-find-jobs <role>           Search live job boards for open roles    [RapidAPI]
                                 Example: /rp-find-jobs "DevOps engineer Austin"

  /rp-briefing                   Daily market intelligence briefing
                                 New postings + market news + pipeline snapshot
                                 Example: /rp-briefing

RESEARCH & ENRICH
──────────────────────────────────────────────────────
  /rp-research <company>         Deep company intelligence brief
                                 Funding, hiring patterns, key people, outreach angle
                                 Example: /rp-research Datadog --deep

  /rp-find-dm <company>          Find the decision maker to contact       [RapidAPI]
                                 Example: /rp-find-dm Snowflake

  /rp-enrich <name> at <co>      Find email address for a contact         [Hunter/Icypeas]
                                 Example: /rp-enrich "Sarah Chen" at Figma

  /rp-market-map <role>          Map the competitive landscape for a role
                                 Example: /rp-market-map "Head of Security SaaS"

OUTREACH
──────────────────────────────────────────────────────
  /rp-outreach <company>         Draft cold outreach to hiring manager
                                 3-email sequence. Grounded in signal data.
                                 Example: /rp-outreach Acme Corp

  /rp-candidate-msg <name>       Draft personalized candidate message
                                 Example: /rp-candidate-msg "Alex Torres"

EVALUATE CANDIDATES
──────────────────────────────────────────────────────
  /rp-source <role>              Find matching candidates on LinkedIn      [RapidAPI]
                                 Example: /rp-source "Staff Engineer Python remote"

  /rp-score <candidate>          Score candidate-job fit (9 dimensions)
                                 Example: /rp-score jane-smith

  /rp-resume-screen              Screen resume against a job description
                                 Example: /rp-resume-screen resume.pdf against jd.txt

  /rp-verify <candidate>         Verify candidate claims + red flags       [RapidAPI]
                                 Example: /rp-verify "Michael Brown"

  /rp-interview-prep <name>      Generate identity verification questions  [RapidAPI]
                                 Example: /rp-interview-prep "Chris Park"

REVERSE RECRUITER
──────────────────────────────────────────────────────
  /rp-reverse <candidate>        Find best jobs for a candidate +          [RapidAPI]
                                 draft outreach to those companies
                                 Example: /rp-reverse "Dana Lee"

MANAGE
──────────────────────────────────────────────────────
  /rp-pipeline                   View and update your active pipeline
                                 Example: /rp-pipeline
                                 Example: /rp-pipeline update "Acme Corp" replied

  /rp-setup                      Configure API keys and preferences
                                 Run this first if you haven't already

  /rp-help [skill]               This guide. Pass a skill name for details.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API KEYS NEEDED
──────────────────────────────────────────────────────
  [RapidAPI]       Fresh LinkedIn Profile Data + JSearch — $50/mo
                   Unlocks: /rp-source, /rp-find-dm, /rp-find-jobs,
                            /rp-verify, /rp-interview-prep, /rp-reverse
                   Sign up: rapidapi.com

  [Hunter/Icypeas] Email finding — $44–59/mo
                   Unlocks: /rp-enrich
                   hunter.io or icypeas.com

  Configure keys: /rp-setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display rules:**
- Skills that require an API key the recruiter does NOT have: show `[RapidAPI]` or `[Hunter/Icypeas]` tag inline. Do not hide or gray out — show them so they know what they're missing.
- Skills they DO have: show normally, no tag.
- If Tier 1 (no RapidAPI): add a line after the API keys section: "7 of 15 skills work free right now."
- If no config at all: replace START HERE with: "→ Run /rp-setup first to configure your preferences and API keys."

### Detailed help for a specific skill (argument provided):

When the user passes a skill name, provide focused help for just that skill.

Look up the skill name (strip `rp-` prefix if provided, or match with it). Provide:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/[skill-name] — [skill title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT IT DOES
[2–3 sentences describing what the skill does and when to use it]

API REQUIRED: [None — works free | RapidAPI | Hunter.io or Icypeas]
[If API required and not configured:] Status: NOT CONFIGURED — run /rp-setup to add your key.
[If configured or free:] Status: READY

USAGE
  /[skill-name] [argument syntax]

EXAMPLES
  /[skill-name] [example 1]
  /[skill-name] [example 2]

OUTPUT
[What the skill produces — files saved, what's displayed]

WORKFLOW POSITION
[Where this skill fits in the workflow and what to run before/after]
  Before: [skill] → [skill]
  After:  [skill] → [skill]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use this reference for each skill's details:

**rp-signals:** Scans a company for hiring signals across three tiers (direct hiring, growth, leadership change). Scores 1–10. Saves leads to `~/.recruiter-skills/data/leads/`. No API required. Before: none. After: rp-research, rp-outreach.

**rp-research:** Deep company intelligence brief covering funding, hiring patterns, key people, tech stack, culture, and recommended outreach angle. No API required. Saves to `~/.recruiter-skills/data/research/`. Before: rp-signals. After: rp-outreach, rp-find-dm.

**rp-outreach:** Drafts a 3-email cold outreach sequence to a hiring manager, grounded in real signal data. No API required. Saves drafts to `~/.recruiter-skills/data/outreach/`. Before: rp-research, rp-signals. After: rp-pipeline update.

**rp-candidate-msg:** Drafts a personalized outreach message to a specific candidate. No API required. Before: rp-source or existing candidate file. After: rp-pipeline update.

**rp-resume-screen:** Screens a resume against a job description. 6-second scan, evidence audit, objections, positioning fixes. No API required. Saves to candidates/. Before: any. After: rp-score.

**rp-market-map:** Maps competitors and talent landscape for a role. Shows where to find candidates and who the companies are competing with. No API required. Before: any. After: rp-source.

**rp-score:** Scores a candidate against a job on 9 dimensions (skills match, scope, trajectory, etc.). No API required. Saves score to candidate YAML. Before: rp-resume-screen. After: rp-candidate-msg or submit.

**rp-source:** Searches LinkedIn for candidates matching a role description. Requires RapidAPI. Returns list of profiles with LinkedIn URLs. Saves to candidates/. Before: rp-market-map. After: rp-score, rp-resume-screen.

**rp-find-dm:** Finds the hiring manager or decision maker to contact at a company. Requires RapidAPI. Returns name, title, LinkedIn URL. Saves to lead contacts. Before: rp-research. After: rp-outreach, rp-enrich.

**rp-enrich:** Finds verified email address for a specific person at a company. Requires Hunter.io or Icypeas API key. Before: rp-find-dm. After: rp-outreach.

**rp-verify:** Verifies a candidate's resume claims, digital footprint, and flags red flags. Requires RapidAPI. Before: rp-resume-screen. After: submit or rp-interview-prep.

**rp-interview-prep:** Generates identity verification questions tailored to a candidate's specific background to detect fraud. Requires RapidAPI. Before: rp-verify. After: submit.

**rp-find-jobs:** Searches live job boards (LinkedIn, Indeed) for open roles matching a query. Requires RapidAPI (JSearch). Saves matching roles as leads. Before: none. After: rp-signals, rp-research.

**rp-reverse:** Takes a candidate profile and finds the best-matched open jobs, then drafts outreach to those hiring managers. Requires RapidAPI. Before: rp-source or existing candidate. After: rp-outreach.

**rp-pipeline:** Tracks all active leads, candidates, and outreach across the funnel. No API required. Before: any. After: any.

**rp-briefing:** Daily intelligence briefing. Searches for new postings and market news, summarizes pipeline, lists today's actions. No API required for core function. Before: any. After: any action from the TODAY'S ACTIONS list.

**rp-setup:** First-run wizard. Collects recruiter profile, ICP, and API keys. Creates config.yaml. No API required to run but guides through adding them. Before: none (run first). After: everything.

**rp-help:** This guide. Before: none. After: any skill.

If the user provides an unrecognized skill name, say: "No skill named '[name]' in the Recruiter Skills Pack. Run /rp-help to see all available skills."
