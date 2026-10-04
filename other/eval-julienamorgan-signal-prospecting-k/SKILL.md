---
name: eval
description: >
  Test harness for the Signal Prospecting Kit v4.1. Runs deterministic checks and
  rubric-based grading against all 6 skills including tool connections,
  multi-batch flow, LinkedIn outreach, channel selection, self-improvement
  loop, enrichment tiers, bridge/CTA variation, variation planning,
  and fallback tool detection. Triggers: /eval, /eval all,
  /eval {skill-name}, /eval simulate.
  Does NOT require WebSearch — validates structure, rules, and simulated output.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
---

# /eval — Signal Prospecting Kit v4.1 Test Harness

You are a testing agent. You evaluate the Signal Prospecting Kit by reading
each SKILL.md, checking against deterministic rules, simulating scenarios,
and scoring output quality. Strict, specific, every failure gets a fix.

---

## Running Evals

**`/eval all`** — Full test suite.
**`/eval structure`** — File structure and frontmatter only.
**`/eval start`** — Orchestrator tests.
**`/eval profile`** — Market research tests.
**`/eval signal-scout`** — Signal discovery tests.
**`/eval prospect`** — Company + contact + enrichment tests.
**`/eval outreach`** — Email + LinkedIn + batch variation tests.
**`/eval push`** — Export + deliverability + learnings tests.
**`/eval simulate`** — Full simulated output grading only.

Default: run all.

---

## Test Suite 1: Structure

### 1.1 Directory Layout

```
Check exists (inside .claude/skills/):
  ✓ .claude/skills/start/SKILL.md
  ✓ .claude/skills/profile/SKILL.md
  ✓ .claude/skills/signal-scout/SKILL.md
  ✓ .claude/skills/prospect/SKILL.md
  ✓ .claude/skills/outreach/SKILL.md
  ✓ .claude/skills/push/SKILL.md
  ✓ README.md (at repo root)

Must NOT exist in distributed kit:
  ✗ eval/ (dev only)
  ✗ gtm/ (created at runtime)
  ✗ install.sh (no longer needed)
```

### 1.2 Frontmatter Validity

For each SKILL.md:
```
  ✓ Valid YAML frontmatter (--- delimiters)
  ✓ 'name' field matches directory name
  ✓ 'description' mentions: triggers, reads, writes, standalone
  ✓ 'allowed-tools' is non-empty list
  ✓ All listed tools exist in Claude Code
  ✓ WebSearch/WebFetch for skills that research
  ✓ Write/Edit for skills that create files
```

### 1.3 No Leaked Secrets

Grep all files except eval/:
```
Must NOT match:
  ✗ /[A-Z_]*(KEY|TOKEN|SECRET)\s*[:=]/ (actual API keys)
  ✗ /Users/ (absolute paths)
  ✗ Deepline, deeplineagent, Exa API, Apify, ScrapeCreators
  ✗ Julien-specific references in SKILL.md files
  ✗ Tool names in outreach OUTPUT (Clay, Instantly, HeyReach)
    — allowed only in "don't mention these" rules

Note: API key REFERENCES are fine (e.g., "$APOLLO_API_KEY",
"API Keys Available section"). Actual key VALUES are not.
```

### 1.4 README Quality

```
  ✓ Install: clone + cd + claude (3 lines)
  ✓ Quick start shows all 6 stages
  ✓ Mentions all 6 skills by name
  ✓ Mentions approval gates + auto-continue
  ✓ Mentions LinkedIn outreach as a channel option
  ✓ Mentions tool connections (Clay, Apollo, Hunter, Instantly)
  ✓ Mentions the learning loop + multi-batch progression
  ✓ Has CTA to climategrowthadvisors.com
  ✓ Under 1200 words
  ✓ No broken markdown links
```

### 1.5 Cross-Skill Consistency

```
  ✓ All skills reference ./gtm/ path
  ✓ Consistent file names: company.md, icp.md, voice.md,
    signals.md, prospects.md, learnings.md
  ✓ Routing chain: start → profile → signal-scout →
    prospect → outreach → push
  ✓ Auto-continue after each stage (no manual /command needed)
  ✓ Approval gates at: profile, signal-scout, prospect, outreach
  ✓ All skills show "what was loaded" before working
  ✓ All skills work standalone (graceful degradation)

Anti-signal data flow:
  ✓ /start collects lost deals in Q2 (optional)
  ✓ /start saves Lost Deal Anti-Signals to icp.md
  ✓ /signal-scout reads lost deals from icp.md
  ✓ /signal-scout generates anti-signal list + competitor list
  ✓ /signal-scout saves anti-signals to signals.md
  ✓ /prospect reads anti-signals from signals.md
  ✓ /prospect applies anti-signal penalties in scoring
  ✓ /prospect shows Flagged + Dropped sections with anti-signal reasons
  ✓ Flow works if lost deals are empty (theoretical anti-signals used)

Tool-agnostic enrichment flow:
  ✓ /start asks about email enrichment conversationally (no hardcoded tools)
  ✓ /start does NOT recommend specific software unprompted
  ✓ /prospect uses whatever tools are connected, no preference hierarchy
  ✓ /prospect pattern-guesses emails when no enrichment tools available
  ✓ /prospect marks contacts "LinkedIn only" when no email found
  ✓ /outreach writes LinkedIn-only for contacts without email
  ✓ /push shows email status breakdown (verified / pattern-guess / LinkedIn only)
  ✓ /push does NOT hardcode recommendations for specific tools

Orchestrator resilience:
  ✓ All 6 skills have "Handling Questions and Tangents" sections
  ✓ Users can ask "what tool should I use?" and get researched answer
  ✓ Users can skip ahead (skills ask for what they need inline)
  ✓ Users can go off-topic and resume with "continue"
  ✓ Approval gates handle rejection with re-research, not just deletion
  ✓ /start returning mode updates icp.md when new tools detected
  ✓ /prospect handles mid-session tool changes and ICP changes
  ✓ /outreach handles mid-flow tool connection (re-enriches LinkedIn-only)
  ✓ /signal-scout standalone creates minimal icp.md for downstream
  ✓ /prospect standalone generates signals inline if signals.md missing
  ✓ /push adapts format menu and deliverability to user's actual stack
```

---

## Test Suite 2: /start

### 2.1 First-Run Onboarding

```
  ✓ Shows empty state scan with all 6 context files
  ✓ Empty state includes plain-english descriptions for jargon terms
    (ICP Profile → "your ideal customer", Signal Types → "events that
    suggest someone needs your product")
  ✓ Q1 uses "email sending tool" not "sequencer"
  ✓ Asks exactly 2 compound questions
  ✓ Q1 covers: domain, ICP, stack, do-not-contact
  ✓ Q1 does NOT ask about API keys (auto-detected in Step 3)
  ✓ Q2 covers: cold emails that got replies + deals won + deals LOST
  ✓ Q2 does NOT say "paste a writing sample" (old version)
  ✓ Lost deals marked as optional but valuable
  ✓ Accepts partial answers gracefully
  ✓ Researches company domain via WebSearch/WebFetch
```

### 2.2 Tool Detection (CRITICAL — must not be skipped)

```
  ✓ Step is marked CRITICAL, DO NOT SKIP in SKILL.md
  ✓ Runs silent detection (Bash for env vars, MCP tool check)
  ✓ NEVER displays or logs API key values
  ✓ Notes tools user mentioned in stack answer
  ✓ Asks about email enrichment conversationally if none detected
  ✓ Does NOT recommend specific software unprompted
  ✓ If user asks "what tool?", researches and gives honest answer
  ✓ Handles "I don't have one" gracefully (pattern-guess + LinkedIn)
  ✓ Shows TOOLS output block (connected / mentioned / no enrichment)
  ✓ Saves to Connected Tools section in icp.md
  ✓ Does NOT gate anything on tool connections
  ✓ Foundation Built includes "Email enrichment: {tool or pattern-guess}"
```

### 2.2b No-outbound fallback

```
  ✓ If user has no cold emails and no deals, skill proceeds gracefully
  ✓ Voice.md built from website copy and LinkedIn instead
  ✓ Voice.md includes note "Built from website copy — provide example anytime"
  ✓ Signals built from market research (theoretical) instead of won deals
```

### 2.3 Files Created

```
company.md sections:
  ✓ Domain, Product, Positioning, Claimed Customers,
    Differentiators, Stage, Researched

icp.md sections:
  ✓ What We Sell, Target Buyer, Buyer's Situation,
    Scoring Criteria, Pain Indicators
  ✓ Stack (CRM, email sending tool, LinkedIn, email finder)
  ✓ Connected Tools (tool name, status, what it enables)
  ✓ Do Not Contact (existing customers, past contacts)
  ✓ Won Deal Patterns (from Q2 deal examples):
    - Per deal: Buyer, Trigger, Closer, Signal
    - Patterns section (what deals have in common)
  ✓ Lost Deal Anti-Signals (from Q2 lost deal examples):
    - Per loss: Buyer, Why didn't buy, Anti-signal
    - Anti-Fit Patterns section (what losses have in common)
    - Section empty if user skipped lost deals (not an error)

voice.md sections:
  ✓ Name (from sign-off)
  ✓ Extracted From, Tone, Patterns
  ✓ Signature Moves (from reply-getting emails)
  ✓ What Got Replies (what specifically worked)
  ✓ Avoid

company.md vs icp.md no overlap:
  ✓ company.md: Product, Claimed Customers (from THEIR site)
  ✓ icp.md: What We Sell, Target Buyer (USER's words)
```

### 2.4 Returning Mode

```
  ✓ Shows batch history with reply rates per batch
  ✓ Shows overall cumulative stats
  ✓ Shows top pattern + what to avoid from learnings
  ✓ Flags unlogged results ("N prospects sent, no results logged")
  ✓ Priority 1: Offer structured result logging if unlogged sends exist
  ✓ Priority 2: Route to incomplete pipeline step
  ✓ Priority 3: Offer next batch if all batches complete
  ✓ Re-detects tools silently, reports new connections
```

### 2.5 Auto-Continue + Anti-Patterns

```
  ✓ Auto-continues to /profile after foundation built
  ✓ Does NOT show "→ /profile" as a manual command
  ✓ Never presents skills as a menu
  ✓ Never gates output on missing files
  ✓ Never asks more than 2 questions
```

---

## Test Suite 3: /profile

```
  ✓ Reads company.md and icp.md
  ✓ Standalone if company.md missing
  ✓ 5-8 direct competitors researched
  ✓ 3-5 adjacent competitors researched
  ✓ White space analysis (what nobody else claims)
  ✓ Saturated claims (3+ competitors)
  ✓ ICP refinements proposed (buyer situation, positioning, disqualifiers)
  ✓ APPROVAL GATE before updating icp.md
  ✓ Auto-continues to /signal-scout after approval
```

---

## Test Suite 4: /signal-scout

### 4.1 Signal Categories

```
All categories + proven tier:
  ✓ Proven signals (from won deals in icp.md) — shown FIRST
  ✓ Transactional (funding, M&A, hires, expansion — standard)
  ✓ Behavioral (buyer posting about problems, asking for recs,
    commenting on content, engaging with competitors) — highest value
  ✓ Negative (churned off vendor, employee turnover, declining
    metrics, Glassdoor reviews, spam database) — strongest triggers
  ✓ Organizational (reorg, IC→manager, downsized adjacent team)
  ✓ Competitive/Market (competitor raised, category crowded)
  ✓ Proxy (conferences, evaluating related tools)
  ✓ Buyer's Customer Signals (what's happening to THEIR customers)
  ✓ Social Signals (Reddit, X/Twitter, LinkedIn)
  ✓ Anti-Signals (disqualification patterns — shown in presentation)

  ✓ Explicit instruction: "Go deeper than 'company is hiring'"
  ✓ Behavioral + negative prioritized over transactional

Won deal integration:
  ✓ Checks icp.md for Won Deal Patterns section
  ✓ Extracts signals from real deals
  ✓ Labels proven vs theoretical signals
  ✓ Proven signals go to highest tier

Lost deal integration:
  ✓ Checks icp.md for Lost Deal Anti-Signals section
  ✓ Extracts anti-signals from lost deals
  ✓ Supplements with research-based anti-signals
  ✓ Anti-signals saved to signals.md for /prospect to use
  ✓ Competitor list built and saved to signals.md

Signal reliability hierarchy:
  ✓ Explicit ranking: job listings > proven > behavioral >
    negative > compliance > tech stack > website > transactional
  ✓ Saved to signals.md for /prospect scoring
  ✓ Website signals flagged as unreliable for back-office tools

Signal interpretation rules:
  ✓ Seller vs buyer distinction documented
  ✓ Source context matters (product page vs careers vs blog)
  ✓ Tech stack positive vs inverse correlation
  ✓ n=1 signal flagging requirement
  ✓ CRM confirmation bias warning (catalyst notes, MEDDPICC, etc.)
```

### 4.2 Social Signals

```
  ✓ Reddit: thread types + site:reddit.com queries
  ✓ X/Twitter: post types + site:twitter.com queries
  ✓ LinkedIn: engagement mining + site:linkedin.com/posts queries
  ✓ All use site: operators (no API keys)
  ✓ Explains why social = high-intent
```

### 4.3 Output + Flow

```
  ✓ Presentation: Proven / High-Intent / Moderate / Customer / Social
    + Anti-Signals + Signal Reliability Hierarchy
  ✓ Each signal: type, real example, why it matters, working query
  ✓ Anti-signals shown with ✗ prefix and disqualification reason
  ✓ Signal reliability hierarchy shown (1-8 ranking)
  ✓ Validates findability via WebSearch
  ✓ APPROVAL GATE
  ✓ Saves signals.md with: company + social search queries,
    anti-signals section, competitor list, reliability hierarchy
  ✓ Auto-continues to /prospect after approval
  ✓ Single-company mode when user names a company
```

---

## Test Suite 5: /prospect

### 5.1 Search Channels

```
  ✓ Channel 1: Behavioral + Negative signals (HIGHEST priority)
    - LinkedIn posts, G2/Glassdoor reviews, churn events, turnover
  ✓ Channel 2: Social community mining (Reddit, X, LinkedIn threads)
  ✓ Channel 3: Company event signals (org changes, funding, hires)
  ✓ Channel 4: Proxy + content signals (conferences, blog, eval)
  ✓ Explicit: "Don't default to job boards"
  ✓ Channel reliability: Reddit > LinkedIn > X
  ✓ Guidance to skip X if thin results
  ✓ Captures SPECIFIC behavioral events, not generic "hiring SDRs"

Channel ordering (NEW v4.2 — hard rule):
  ✓ Skill mandates ≥2 Channel 1 searches BEFORE Channel 3/4
  ✓ Skill mandates ≥2 Channel 2 searches BEFORE Channel 3/4
  ✓ Explicit execution checklist in the skill
  ✓ Thin Channel 1/2 results must be noted, not hidden
```

### 5.2 Filtering + Anti-Signal Disqualification

```
  ✓ Checks Do Not Contact list from icp.md
  ✓ Within-run dedup across channels (merge same company)
  ✓ Cross-run dedup against prospects.md
  ✓ Excludes user's company + competitors from signals.md
  ✓ Checks disqualifier list from icp.md

Anti-signal checks (NEW):
  ✓ Loads anti-signals from signals.md
  ✓ Checks every company against anti-signal list
  ✓ 2+ anti-signal matches = auto-drop (moved to Dropped)
  ✓ 1 anti-signal match = -3 penalty + flag in output
  ✓ Competitor list from signals.md auto-excluded

Competitor vs buyer interpretation (NEW):
  ✓ Website signals checked: does company SELL or NEED the product?
  ✓ Product/features page = seller signal (competitor, not buyer)
  ✓ Careers/jobs page = buyer signal (high intent)
  ✓ Failed interpretation = -4 penalty or drop
  ✓ Flagged section in output for companies with single anti-signal
```

### 5.3 Scoring

```
  ✓ Fit Score: title +2, industry +2, size +2, not disqualified +1
  ✓ Behavioral signals: +4 (buyer posted about problem, asked for recs,
    churned off competitor, asking in community)
  ✓ Standard signals: high-30d +3, high-90d +2, moderate +1
  ✓ Bonuses: multiple signals +1, social-sourced +2, customer signal +1,
    job listing signal +1
  ✓ Combined max: ~18 with multiple behavioral signals
  ✓ Thresholds: Top 10+, Worth a Look 6-9, Dropped below 6
  ✓ Behavioral scores highest because buyer is actively thinking about problem

Anti-signal penalties (NEW):
  ✓ Single anti-signal match: -3 (flagged in output)
  ✓ Two+ anti-signal matches: auto-drop
  ✓ Competitor list match: auto-drop
  ✓ Failed seller-vs-buyer interpretation: -4
  ✓ Signal reliability weighting documented (job listings > website)
```

### 5.4 Contact + Email Enrichment

```
  ✓ One contact per company
  ✓ Title-case names, drop 1-char or initials
  ✓ LinkedIn URL captured

Tool-agnostic enrichment:
  ✓ Uses whatever enrichment tools are connected (no preference)
  ✓ Does NOT hardcode tool preferences or tiers
  ✓ API calls use environment variables, NEVER hardcoded
  ✓ Falls back gracefully per company if a tool fails

Pattern-guess fallback (when no enrichment tools):
  ✓ Checks for publicly available emails first
  ✓ Detects company email pattern from known employee emails
  ✓ Applies pattern to contact name (first.last@domain etc.)
  ✓ Marks pattern-guess emails as "pattern-guess — verify before sending"
  ✓ If no pattern detectable, marks as "LinkedIn only"
  ✓ NEVER leaves a prospect in a dead end — always has a next step

Email status in prospects.md:
  ✓ Verified email (from tool or public source)
  ✓ Pattern-guess email (with verification note)
  ✓ "LinkedIn only" (connection request instead)
  ✓ Email source column tracks where email came from

Fallback tool detection:
  ✓ If Connected Tools empty/missing in icp.md, /prospect detects
    tools independently (MCP check + env var check)
  ✓ Mid-session tool changes handled (re-detect and switch)
  ✓ ICP changes mid-flow handled (update and re-search)
  ✓ Loaded context display shows enrichment method being used
```

### 5.5 Approval + Flow

```
  ✓ APPROVAL GATE after company list
  ✓ APPROVAL GATE after contact list
  ✓ Auto-continues to /outreach after final approval
  ✓ Handles user-provided lists
  ✓ Handles "not enough results"
  ✓ Handles social-sourced unknown-company prospects
```

---

## Test Suite 6: /outreach

### 6.1 Channel Selection

```
  ✓ Asks channel before writing: email / LinkedIn / both
  ✓ Accepts inline: "/outreach email", "/outreach linkedin", "/outreach both"
  ✓ Defaults to "both" if unspecified
  ✓ Description triggers include LinkedIn terms
```

### 6.2 Cold Email Framework

```
  ✓ 4 paragraphs + CTA, under 120 words
  ✓ Subject: lowercase, 2-4 words
  ✓ 5 opener types: observation, signal, question, buyer, social
  ✓ Social-sourced: references topic, NOT "I saw your post"
  ✓ Rotation across batch
```

### 6.3 Bridge Variation (NEW)

```
  ✓ 7 bridge angles documented:
    methodology, scale, accuracy, API, price, workflow, skip
  ✓ "Use 4+ different angles per 10 emails" rule
  ✓ "No single angle more than 3 times" rule
  ✓ "If you catch yourself writing the same sentence" warning
```

### 6.4 CTA Variation (NEW)

```
  ✓ 7+ CTA options documented
  ✓ "No CTA more than 3 times" rule
  ✓ CTA-opener pairing guidance
  ✓ "No CTA" option for senior execs
```

### 6.5 LinkedIn Framework (NEW)

```
  ✓ Under 300 characters (with COUNT instruction)
  ✓ 4 opener patterns: signal curiosity, market observation,
    buyer-world, mutual context
  ✓ 3+ non-obvious signals
  ✓ No pitch, no "I build...", no em dashes
  ✓ Never names a social platform as signal source (no "r/subreddit",
    no "on Twitter") — reference the TOPIC, not WHERE discussed
  ✓ Rotation across batch
  ✓ NOT a compressed version of the email
  ✓ When both channels: completely different signals (not just
    different framing of same signal)
  ✓ Handles "LinkedIn only" prospects (no email available)
```

### 6.6 Variation Plan (NEW — v4.1)

```
  ✓ Variation plan table created BEFORE writing any email
  ✓ Plan assigns: opener, bridge, CTA, client reference per prospect
  ✓ Batches of 5+: no type used more than 3x, 4+ bridge angles at 8+
  ✓ Batches under 5: each prospect gets different angles (relaxed caps)
  ✓ No two adjacent emails share same opener+bridge combo
  ✓ No client reference/case study used more than 3x
```

### 6.7 Output Format (v4.1)

```
  ✓ Every email has a subject line (lowercase, 2-4 words)
  ✓ Every email shows metadata: Signal | Opener | Bridge | CTA
  ✓ Word count shown for emails, char count for LinkedIn
```

### 6.7.5 Pre-Send Validator (NEW — v4.2)

```
Skill has a Step 4.5 "Pre-Send Validator — HARD CHECKS" block that
enumerates the hard fails the model must check before presenting:

Per email:
  ✓ Subject ≤4 words (with explicit failure example)
  ✓ Body <120 words
  ✓ Zero em dashes (grep the text for —)
  ✓ No banned vocabulary
  ✓ No hedging / exclamation / "I help" / tool names
  ✓ Company-name removal test

Per LinkedIn:
  ✓ <300 chars
  ✓ Zero em dashes
  ✓ NO product name (own product cannot appear in LinkedIn text)
  ✓ 3+ non-obvious signals
  ✓ Different signal than paired email
  ✓ No shared client ref with paired email

Per batch:
  ✓ Hard caps enforced (3x opener/bridge/CTA/ref)
  ✓ 4+ bridge angles at N=8+
  ✓ No adjacent opener+bridge duplicate
  ✓ LinkedIn independence test

Skill mandates: "Do not present a batch with known failures."
```

### 6.8 Batch Tests

```
  ✓ Opener test: all different across batch
  ✓ Bridge test: same sentence in 4+ = fail
  ✓ CTA test: same CTA in 4+ = fail
  ✓ Proof point test: same stat in 4+ = fail
  ✓ Reference test: same client ref in 4+ = fail (NEW v4.1)
  ✓ Template test: two prospects comparing = no template visible
  ✓ Cross-channel test: LinkedIn ≠ compressed email
```

### 6.9 Banned Vocabulary

```
  ✓ Full list: leverage, synergy, optimize, AI-powered, seamless,
    robust, unlock, empower, cutting-edge, revolutionary, transform,
    game-changer, furthermore, moreover, additionally, pivotal,
    crucial, testament, landscape, nestled, groundbreaking, renowned
  ✓ Tool names in output: Clay, Claude Code, Instantly, HeyReach
  ✓ Hedging: "I think", "maybe", "potentially"
  ✓ No exclamation points, no "I help", no em dashes
```

### 6.10 Humanizer Pass

```
  ✓ Structural: em dashes, rule of three, same structure, same length
  ✓ Vocabulary: banned list, copula avoidance, -ing analyses,
    vague attributions, promotional, filler
  ✓ Voice: match voice.md, vary across batch, anti-AI final pass
  ✓ NOT mentioned to user
```

### 6.11 Self-Improvement Loop

```
learnings.md tracking — 7 dimensions per send:
  ✓ Channel (email / linkedin / both)
  ✓ Signal type (proven / high-intent / moderate / social)
  ✓ Opener type
  ✓ Bridge angle
  ✓ CTA type
  ✓ Reply (yes / no / pending)
  ✓ Notes

Adaptation rules:
  ✓ Signal type with 2+ replies → promote to high-confidence
  ✓ Signal type with 0/5+ → deprioritize
  ✓ Opener type with replies → use more (still rotate)
  ✓ 3+ same opener type no replies → try others
  ✓ Bridge angle tracking + adjustment
  ✓ CTA tracking + adjustment
  ✓ Channel comparison (email vs LinkedIn rates)

Progressive refinement:
  ✓ Batch 1: baseline
  ✓ Batch 2-3: weight toward winners
  ✓ Batch 4+: pattern recommendations shown to user

Shows LEARNINGS APPLIED summary before writing:
  ✓ Batches sent, reply rates per channel
  ✓ Best signal/opener/bridge/CTA
  ✓ Adjustments being made
```

### 6.12 Presentation + Flow

```
  ✓ Email-only format with signal + opener + bridge metadata
  ✓ LinkedIn-only format with char count + pattern
  ✓ Both-channel format: side by side per prospect
  ✓ APPROVAL GATE with fix/cut/approve options
  ✓ Auto-continues to /push after approval
```

---

## Test Suite 7: /push

### 7.1 Direct Push (Connected Tools)

```
  ✓ Checks Connected Tools from icp.md before offering file export
  ✓ Instantly API: creates campaign + adds leads directly
    - Uses $INSTANTLY_API_KEY (NEVER hardcoded)
    - Shows confirmation with campaign name
  ✓ Clay MCP: pushes contacts to Clay table
    - Uses track-event or add-contact-data-points
  ✓ Falls back to file export if no direct push tools
  ✓ Always offers file export as alternative even when tools connected
```

### 7.2 Export Formats

```
Email formats:
  ✓ Plain text (.txt)
  ✓ CSV (Instantly, Apollo, Smartlead)
  ✓ Outreach/Salesloft format
  ✓ HubSpot sequences format

LinkedIn formats:
  ✓ Copy-paste .txt (all messages with char counts)
  ✓ CSV for LinkedIn tools (HeyReach, Dripify)
  ✓ "Both email + LinkedIn" export option

  ✓ Auto-detects format from stack/tools in icp.md
  ✓ Falls back to asking if unknown
  ✓ Exports to ./gtm/export/
```

### 7.3 Email Status Handling

```
  ✓ Shows email status breakdown (verified / pattern-guess / LinkedIn only)
  ✓ Pattern-guess emails flagged "verify before sending"
  ✓ Offers to verify with connected tool (generic, no hardcoded preference)
  ✓ If no enrichment tools, suggests user connect one (no specific rec)
  ✓ Does NOT hardcode recommendations for specific tools
  ✓ LinkedIn-only contacts get connection requests (not a dead end)
```

### 7.4 Deliverability

```
  ✓ SPF/DKIM/DMARC mentioned
  ✓ Warmup guidance
  ✓ 50/day per mailbox limit
  ✓ Spread across days
```

### 7.5 Structured Result Logging

```
  ✓ Shows sent prospect list with numbers for easy marking
  ✓ Accepts flexible input ("1 and 4 replied", "nobody replied",
    "got a reply from {name}", etc.)
  ✓ Marks unmarked prospects as no-reply after user reports
  ✓ Asks for details on what they said (optional, helps learning)
```

### 7.6 Post-Send Feedback

```
learnings.md format captures:
  ✓ Summary: emails sent, replies, LinkedIn sent, accepts, rates
  ✓ Per reply: channel, signal type, opener, bridge, CTA, notes
  ✓ Per no-reply: same dimensions tracked
  ✓ Patterns section: signal, opener, bridge, CTA, channel, title
  ✓ Cumulative stats updated across all batches
  ✓ Best/worst performing combinations identified

Shows LEARNING UPDATE after logging:
  ✓ Reply rate this batch + cumulative
  ✓ WHAT'S WORKING section (winning patterns with rates)
  ✓ WHAT'S NOT section (anti-patterns to deprioritize)
  ✓ BATCH PROGRESSION (trend across all batches)
```

### 7.7 Next Batch Flow

```
  ✓ After logging results, offers "go" to start next batch
  ✓ Auto-continues to /prospect (dedupes against existing)
  ✓ /prospect uses updated learnings for signal prioritization
  ✓ /outreach uses updated learnings for pattern weighting
  ✓ The loop: send → log → learn → find → write → send
```

---

## Test Suite 8: Simulated Output Grading

### 8.1 Mock Scenario

```
Company: BNBCalc (bnbcalc.com)
ICP: DSCR lenders, 50-500 emp, VP/Director level
Voice: Casual-professional, direct. Name: Julien.
Stack: HubSpot, Instantly, Apollo, LinkedIn manual
Connected Tools: Apollo API (email enrichment), Instantly API (direct push)

Won deals:
- Lima One: VP Lending, triggered by 40% projection miss,
  closed on 5-deal comparison (8% vs 35% variance)
- Visio: Dir Credit Risk, triggered by board risk mandate,
  closed on 2-week API pilot

Lost deals:
- PropTech startup: Head of Product, didn't buy because they
  built their own model. Anti-signal: company had "rental analytics"
  on their product page (competitor, not buyer)
- Consumer fintech: VP Ops, no B2B lending vertical.
  Anti-signal: consumer mortgage company, not DSCR lender

Target: Wade Susini, Chief Lender, Dominion Financial
Signals:
- News: #3 Scotsman, 82% headcount growth, wholesale launch
- LinkedIn: Partner posting about DSCR defaults (Mar 2026)
- Reddit: r/realestateinvesting thread on STR income projections

Channel: Both (email + LinkedIn)
```

### 8.2 Cold Email Rubric (/100)

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Word count | 10 | Under 120 = full. 121-130 = half. Over 130 = 0. |
| Personalization | 20 | Names Dominion's product AND their borrower's situation. Remove-company-name test fails. |
| Signal integration | 15 | Weaves signal naturally as timing. Not listed as fact. |
| Voice match | 15 | Matches casual-professional. No banned words. No em dashes. |
| Bridge quality | 15 | Uses a SPECIFIC angle (not generic). Different from other emails in batch. |
| CTA quality | 10 | Specific, varies from other emails. Matches opener energy. |
| Structure | 10 | Subject lowercase. 3-4 paragraphs. Sign-off matches voice. |
| Social awareness | 5 | If social-sourced: topic reference, not "I saw your post." |

### 8.3 LinkedIn Rubric (/100) (NEW)

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Character count | 20 | Under 300 = full. 301-320 = half. Over 320 = 0. |
| Signal specificity | 25 | 3+ signals, non-obvious, researched. Not "hiring" or "growing." |
| No pitch | 20 | Zero self-promotion. No product name. No "I build/run." |
| Tone | 15 | Curious peer, not vendor. Reads like someone in the same industry. |
| Differentiation | 10 | NOT a compressed version of the email. Different conversation. |
| Format | 10 | Correct structure. No em dashes. Ends with question/curiosity. |

### 8.4 Batch Variation Rubric (/100) (EXPANDED)

Simulate 5 outreach pieces (email + LinkedIn each) and grade the SET:

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Opener variety | 20 | All 5 emails use different openers. All 5 LinkedIn use different patterns. |
| Bridge variety | 20 | 4+ different bridge angles across 5 emails. No sentence repeated. |
| CTA variety | 15 | 3+ different CTAs. No CTA used more than twice. |
| Proof point variety | 10 | Same stat max 2 times. Different proof angles used. |
| LinkedIn independence | 15 | Each LinkedIn message is a different conversation from its paired email. |
| Voice consistency | 20 | All 10 pieces sound like the same person despite structural variety. |

### 8.5 Self-Improvement Rubric (/100) (NEW)

Simulate: Batch 1 sent (5 emails, 5 LinkedIn). Got 2 email replies
(signal leads with accuracy bridge), 1 LinkedIn accept (market observation).
Grade how Batch 2 adapts.

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Logging completeness | 25 | All 7 dimensions captured per send. Patterns section filled. |
| Signal adjustment | 20 | Winning signal types weighted higher in Batch 2. |
| Opener adjustment | 20 | Signal lead used more often (but still rotated). |
| Bridge adjustment | 15 | Accuracy bridge used more (but capped at 3). Losing angles reduced. |
| Learning summary shown | 10 | LEARNINGS APPLIED block shown before Batch 2 with rates + adjustments. |
| Not over-fitted | 10 | Still rotates. Doesn't abandon all non-winning patterns after 1 batch. |

**All rubric thresholds:**
- 85+ = Ship it
- 70-84 = Minor fixes
- 50-69 = Rewrite needed
- Below 50 = Skill revision needed

---

## Reporting

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  SIGNAL OUTBOUND KIT v4 — EVAL REPORT
  {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  STRUCTURE                    {pass}/{total}
  ├── Directory layout         {✓/✗}
  ├── Frontmatter              {✓/✗}
  ├── No leaked secrets        {✓/✗}
  ├── README quality           {✓/✗}
  └── Cross-skill consistency  {✓/✗}

  /start                       {pass}/{total}
  ├── Onboarding questions     {✓/✗}
  ├── Tool detection           {✓/✗}
  ├── Files created            {✓/✗}
  ├── Returning mode           {✓/✗}
  └── Auto-continue            {✓/✗}

  /profile                     {pass}/{total}

  /signal-scout                {pass}/{total}
  ├── Signal categories        {✓/✗}
  ├── Social signals           {✓/✗}
  ├── Won deal integration     {✓/✗}
  ├── Lost deal anti-signals   {✓/✗}
  ├── Signal reliability       {✓/✗}
  └── Interpretation rules     {✓/✗}

  /prospect                    {pass}/{total}
  ├── Search channels          {✓/✗}
  ├── Filtering + anti-signals {✓/✗}
  ├── Scoring + penalties      {✓/✗}
  ├── Email enrichment         {✓/✗}
  └── Approval + flow          {✓/✗}

  /outreach                    {pass}/{total}
  ├── Channel selection        {✓/✗}
  ├── Email framework          {✓/✗}
  ├── Bridge variation         {✓/✗}
  ├── CTA variation            {✓/✗}
  ├── LinkedIn framework       {✓/✗}
  ├── Batch tests              {✓/✗}
  ├── Banned vocabulary        {✓/✗}
  ├── Humanizer                {✓/✗}
  ├── Self-improvement loop    {✓/✗}
  └── Presentation + flow      {✓/✗}

  /push                        {pass}/{total}
  ├── Direct push (tools)      {✓/✗}
  ├── Email export formats     {✓/✗}
  ├── LinkedIn export formats  {✓/✗}
  ├── Missing email handling   {✓/✗}
  ├── Deliverability           {✓/✗}
  ├── Structured result log    {✓/✗}
  ├── Post-send feedback       {✓/✗}
  └── Next batch flow          {✓/✗}

  SIMULATED OUTPUT
  ├── Cold email               {score}/100
  ├── LinkedIn                 {score}/100
  ├── Batch variation          {score}/100
  └── Self-improvement         {score}/100

  ──────────────────────────────────────────────

  OVERALL: {passed}/{total} deterministic
  + {avg}/100 simulated output

  {SHIP IT | FIXES NEEDED | REWRITE}

  ──────────────────────────────────────────────

  FAILURES:

  [{suite}.{test}] {what failed}
    Expected: {what should happen}
    Found: {what was found}
    File: {path}:{line}
    Fix: {specific actionable fix}
```

---

## Adding New Tests

Every manual fix = a new test case. The eval grows with the kit.
