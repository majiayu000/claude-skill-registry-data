---
name: prospect
description: >
  Finds companies matching the ICP that are showing buying signals right now,
  then finds contacts at the best ones. Builds a scored prospect list for
  outreach. Triggers: /prospect, "find companies", "build a list", "find
  prospects". Reads: ./gtm/icp.md, ./gtm/signals.md, ./gtm/company.md.
  Writes: ./gtm/prospects.md. Standalone: yes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - WebSearch
  - WebFetch
---

# /prospect — Company + Contact Discovery

You find companies that match the user's ICP and are showing buying signals
right now, then find the right contacts at those companies. You build a
scored, researched prospect list ready for outreach.

---

## Process

### Step 1: Load Context

Read:
- `./gtm/icp.md` — who to target, disqualifiers, buyer situation,
  do-not-contact list, API keys available, lost deal anti-signals
- `./gtm/signals.md` — what buying signals to look for (with search queries),
  anti-signals to disqualify against, signal reliability hierarchy,
  competitor list
- `./gtm/company.md` — to avoid targeting competitors or the user's own company
- `./gtm/prospects.md` — to avoid duplicates if previous runs exist

If signals.md doesn't exist, you can still proceed:
1. Ask: "What signals indicate someone needs your product right now?"
2. If they give you signals, use those to search.
3. If they're unsure, generate 3-5 obvious signal types from icp.md
   (or from what you know about their product) and confirm before
   searching. Example: "I'll look for companies that are [hiring
   for X], [posting about Y problem], or [recently raised funding].
   Sound right?"
4. Suggest running /signal-scout for a more thorough signal analysis,
   but don't block on it.

**Load Anti-Signals from signals.md.** The Anti-Signals section contains
disqualification patterns — characteristics of companies that look like
prospects but never close. Check EVERY company found against this list
before adding to results. A company matching 2+ anti-signals gets
dropped regardless of how strong their buying signals look.

**Load Signal Reliability Hierarchy.** When a company shows multiple
signal types, weight them according to the hierarchy in signals.md.
Job listings and behavioral signals outweigh transactional signals
like funding rounds.

**Load Competitor List from signals.md.** Companies identified as
competitors during /signal-scout are automatically excluded.

**Load the Do Not Contact list from icp.md.** This includes existing
customers, companies already contacted, and competitors. Every company
found must be checked against this list before being added to results.

**Load Connected Tools from icp.md.** Check what enrichment tools,
CRM connections, and outreach tools are available. Use whatever
the user has — do not prefer one tool over another.

**FALLBACK — If Connected Tools section is empty or missing in icp.md,
detect tools yourself before proceeding.** This covers cases where
/start was skipped or tool detection didn't run:
1. Check for MCP tools: look for any available tools starting with
   `mcp__` that handle contacts, enrichment, or company data
2. Check env vars with Bash: `env | grep -i '_API_KEY\|_TOKEN' |
   sed 's/=.*/=set/' 2>/dev/null`
3. Use whatever you find. Update icp.md Connected Tools section.

**Email enrichment path (determined by what's connected):**
- **Connected enrichment tools:** Use whatever MCP tools or API keys
  are available to find emails. If multiple tools are connected, try
  the one that returns the richest data first.
- **No enrichment tools:** Find contacts via WebSearch, then:
  1. Check for publicly available emails (company website, LinkedIn)
  2. Detect the company's email pattern from any known employee emails
     (first.last@domain, flast@domain, firstl@domain)
  3. Pattern-guess the email using the detected format
  4. If no pattern detected, mark as "LinkedIn only" — outreach will
     default to LinkedIn connection request for this contact

**Every prospect should end up with one of:**
- A verified email (from enrichment tool or public source)
- A pattern-guessed email (marked as "pattern-guess — verify before sending")
- "LinkedIn only" (no email found — LinkedIn connection request instead)

**Never leave a prospect in a dead end.** If you can't find an email,
the prospect still gets LinkedIn outreach. No "needs enrichment"
without a clear next step.

Show what you loaded:

```
  Loaded: ICP ({buyer type}), {N} signal types,
  {N} anti-signals active, {N} competitors excluded,
  {N} existing prospects (dedup check active),
  {N} companies on do-not-contact list.
  Email enrichment: {tool name(s) or "web research + pattern-guess"}
  Fallback channel: LinkedIn connection requests
  Searching for companies showing buying signals.
```

### Step 2: Find Companies

Use ALL search queries from signals.md — both company signals and social
signals — to find companies and people RIGHT NOW.

**IMPORTANT: Don't default to job boards.** Job postings ("hiring VP
Sales", "hiring SDRs") are the weakest signals because every sales
tool surfaces them. Prioritize behavioral and negative signals — what
people are SAYING and what's going WRONG. These are harder to find
but produce dramatically better prospects.

**CHANNEL ORDERING — HARD RULE:**
You MUST run at least 2 searches from Channel 1 (behavioral/negative)
AND at least 2 searches from Channel 2 (social community mining)
BEFORE running any Channel 3 (company events) or Channel 4 (proxy)
queries. This is not a preference — it is a required execution order.

The reason: the model's default instinct is to reach for news/hire
signals because they return cleaner results. That's exactly the
failure mode this ordering prevents. If Channels 1 and 2 come back
thin, note it explicitly in the output ("social signals sparse —
leaning on transactional") but still run them first.

Track your queries as you go. Before you write any prospect into
the list, verify:
- [ ] ≥2 Channel 1 (behavioral/negative) queries executed
- [ ] ≥2 Channel 2 (social community) queries executed
- [ ] Then, and only then, Channel 3/4 queries

**Channel 1: Behavioral + Negative Signals (highest priority)**
Search for the buyer DOING or SAYING something that reveals pain:

LinkedIn activity searches:
- `site:linkedin.com/posts "{buyer title}" "{problem keyword}"`
  e.g., `"VP Sales" "outbound not working"` or `"Head of Revenue"
  "pipeline challenges"`
- `site:linkedin.com/posts "{buyer title}" "{competitor}" switching
  OR alternative OR replacing`
- `site:linkedin.com/posts "{buyer title}" "looking for" OR
  "anyone recommend" "{product category}"`

G2/review searches:
- `site:g2.com "{competitor}" review negative OR disappointed OR
  switching OR expensive`
- `"{competitor}" churned OR cancelled OR replaced OR "switched to"`

Glassdoor/employee sentiment:
- `site:glassdoor.com "{company}" "sales" OR "SDR" poor tools OR
  bad leads OR no process`
- Look for patterns: SDR turnover, mentions of bad data/tools

Negative event searches:
- `"{company}" layoffs OR restructuring sales team 2026`
- `"{company}" "reply rates" OR "pipeline" declining OR struggling`
- `"{company}" "agency" OR "vendor" churn OR switch OR replace`

What to extract:
- **The person posting/reviewing** = potential buyer
- **The company mentioned** = company with the pain
- **The specific complaint** = use this in the outreach opener

**Channel 2: Social Community Mining**
Find people actively discussing the problem in communities:

Reddit:
- `site:reddit.com "{problem keyword}" OR "{product category}"`
- `site:reddit.com "{competitor}" alternative OR review OR vs`
- `site:reddit.com "{industry}" "looking for" OR "anyone use"`
- Read promising threads via WebFetch — extract company names,
  pain points, identifiable users

X/Twitter:
- `site:twitter.com "{problem keyword}" recommend OR "looking for"`
- `site:twitter.com "{competitor}" frustrated OR switching`
- Less reliable than Reddit via WebSearch. Try it, but don't
  depend on it.

LinkedIn post engagement:
- `site:linkedin.com/posts "{topic}" OR "{pain point}"`
- Commenters are self-identified interested parties (warmest leads)
- Post authors are potential referral sources

**Channel 3: Company Event Signals**
These are standard but still useful — just don't ONLY search here:

Organizational changes:
- `"{company}" new "VP Sales" OR "CRO" OR "Head of Revenue" hired
  OR joined OR appointed 2026`
- `"{company}" "RevOps" OR "Revenue Operations" first hire`
- `"{company}" reorganized OR restructured sales`

Financial events:
- Funding rounds, revenue milestones, M&A
- But go DEEPER: `"{company}" post-funding sales hiring scaling`

Competitive pressure:
- `"{company}" competitor raised OR launched OR expanded`
- `"{industry}" new entrant OR disruption 2026`

**Channel 4: Proxy + Content Signals**
Indirect indicators that someone is thinking about the problem:

- `"{buyer title}" "{conference}" OR "{event}" speaking OR attending`
- `"{company}" blog "sales process" OR "pipeline" OR "outbound"`
- `"{company}" evaluated OR piloting "{related tool}"`
- Companies whose competitors recently scaled their sales teams

**For each company found, capture the SPECIFIC signal:**
Don't just note "hiring VP Sales." Note "VP Sales posted on LinkedIn
Mar 3 about pipeline being 40% below target and asking for tool
recommendations." The specificity is what makes the outreach work.

**For each company found (from any channel):**
1. Verify they match ICP (industry, size, buyer title exists)
2. Check they're not on the disqualifier list from icp.md
3. **Anti-signal check** — Run through the anti-signal list from
   signals.md. A company matching 2+ anti-signals gets dropped
   immediately, even if their buying signals look strong. Log the
   reason in the Dropped section. Single anti-signal = flag but
   don't auto-drop (note it in the presentation).
4. **Competitor vs buyer check** — If you found the company because
   they mention your product category on their website, verify
   they're a BUYER not a COMPETITOR. Check: does their website
   describe this as something they SELL or something they NEED?
   Product/features pages = seller signal. Careers/jobs pages =
   buyer signal. This is the #1 false-positive source in
   signal-based prospecting.
5. **Dedup within this run** — if the same company appeared in Reddit
   AND news AND LinkedIn, merge into one entry. Note all signal sources.
   Multiple channels = stronger signal (bonus in scoring).
6. Check they're not already in prospects.md (cross-run dedup)
7. Check they're not the user's own company or on the competitor list
   from signals.md
8. Note which signals they're showing, when, and from which channel.
   **Tag each signal with its reliability tier** from signals.md
   (job listing > behavioral > negative > tech stack > website > transactional)

**Target: 15-25 unique companies per search run.** Quality over quantity.

**Channel reliability notes:**
- Reddit (`site:reddit.com`) — most reliable social search. Rich threads
  with identifiable companies and pain points.
- LinkedIn (`site:linkedin.com/posts`) — hit or miss via WebSearch. Works
  best for recent, high-engagement posts. May return limited results.
- X/Twitter (`site:twitter.com`) — least reliable via WebSearch. Google
  often returns poor results for Twitter. Try it, but don't depend on
  it as a primary source. If results are thin, skip and spend the time
  on Reddit and LinkedIn instead.

### Step 3: Score and Rank

Score each company on two axes:

**Fit Score (does this company match ICP?)**
- Buyer title exists at this company: +2
- Industry match: +2
- Company size/stage match: +2
- Not a disqualifier: +1 (0 if disqualified)

**Signal Score (is the timing right?)**

Behavioral signals (buyer doing/saying something):
- Buyer posted about the problem on LinkedIn: +4
- Negative G2/Glassdoor review about current solution: +3
- Churned off a competitor or agency: +4
- Employee turnover in relevant department: +3
- Buyer asking for recommendations in community: +4

Standard signals (company events):
- High-intent signal in last 30 days: +3
- High-intent signal in last 90 days: +2
- Moderate signal in last 30 days: +1

Bonuses:
- Multiple signals from different categories: +1
- Social-sourced (Reddit/X/LinkedIn thread): +2
- Buyer's customer signal detected: +1
- Job listing signal (highest reliability): +1
- Signal structurally matches a won-deal trigger pattern: +2
  (e.g., if won deal triggered by "board risk mandate" and prospect
  just announced portfolio risk review, score as proven-adjacent)

**Anti-Signal Penalties (subtract from score):**
- Single anti-signal match: -3 (flag in output)
- Two+ anti-signal matches: auto-drop (moved to Dropped section)
- Company appears on competitor list: auto-drop
- Website signal is seller-not-buyer (failed interpretation check): -4

**Behavioral signals score highest** because the person is actively
thinking about the problem. "VP Sales posted about pipeline struggles"
is worth more than "company raised Series B" because the first shows
awareness, the second just shows budget.

**Signal reliability weighting:** When scoring, weight signals by
their reliability tier. A job-listing signal (+3 for high-intent in
last 30 days) is more trustworthy than a website-content signal
(same +3) because job listings indicate active budget. If a company's
only signal is website content, note the reliability concern.

A job posting alone (hiring SDRs, VP Sales) scores as a standard
signal (+2 or +3). A job posting PLUS a behavioral signal (the new
VP posted about needing better tools) scores as behavioral (+4)
plus standard (+2) = much higher.

**Combined Score = Fit + Signal.** Rank by combined score.

Fit max = 7 (title +2, industry +2, size +2, not disqualified +1).
Signal max = 11+ (behavioral +4, standard +3, bonuses +4).
Realistic top score for a strong prospect: 14-18.

**Show the raw score, not a fraction.** Don't write "14/16" or
"14/18" — just write "Score: 14". The scale isn't fixed because
signal bonuses stack.

**Thresholds:**
- Top prospects: 10+
- Worth a look: 6-9
- Dropped: below 6

### Step 4: Present Companies for Approval

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PROSPECT LIST: {N} companies found
  Searched: {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TOP PROSPECTS (score 10+)
  ─────────────────────────────────────────────

  ① {Company Name} — {domain} — Score: {X}
     Fit: {industry, size, buyer title exists}
     Signal: {SPECIFIC behavioral event — not "hiring SDRs"
       but "VP Sales posted Mar 3 about pipeline being 40%
       below target" or "3-star G2 review of Clay from their
       SDR manager citing 'no signal layer'"}
     Source: {LinkedIn post / G2 review / Reddit thread /
       Glassdoor / news / job board}
     Why now: {one sentence connecting signal to buying urgency}

  ② {Company Name} — {domain} — Score: {X}
     Fit: {details}
     Signal: {SPECIFIC behavioral event + date}
     Source: {where found}
     Why now: {one sentence}

  ...

  WORTH A LOOK (score 6-9)
  ─────────────────────────────────────────────

  {lower-scored companies, same format}

  FLAGGED (single anti-signal — proceed with caution)
  ─────────────────────────────────────────────

  {Company Name} — {domain} — Score: {X} (includes -3 penalty)
     Anti-signal: {which anti-signal matched}
     Buying signal: {what positive signal they showed}
     Risk: {why they might not close}

  DROPPED (disqualified)
  ─────────────────────────────────────────────

  {company}: {why dropped}
  {If anti-signal:} Anti-signals: {matched 2+ anti-signals}
  {If competitor:} Competitor: {sells same product category}
  {If interpretation fail:} Seller, not buyer: {website describes
    them selling the product, not needing it}

  ──────────────────────────────────────────────

  Which companies should I find contacts for?
  (Say "all top" or name specific ones.)
```

### ✋ APPROVAL GATE

Wait for user to select companies. They may:
- Say "all top" → research contacts for all top-scored
- Name specific companies → research only those
- Remove some → note why (update disqualifiers if pattern)
- Add companies they know → research those too

### Step 5: Find Contacts + Emails

For each approved company, find the right contact AND their email.

**Target titles** (from icp.md buyer profile):
- Primary: {the decision-maker title from ICP}
- Secondary: {one level up or adjacent title}

---

**FINDING CONTACTS (same for all users):**

Search for the right person at each company:
- WebSearch: `"{company name}" "{target title}" site:linkedin.com`
- WebSearch: `"{company name}" team OR leadership OR about`
- Company website team/about page via WebFetch

If an enrichment MCP tool is connected that can find contacts
(check Connected Tools in icp.md), use it. Follow the tool's
actual parameter schema — do not invent parameters. If the tool
is async (returns a task ID), capture it and continue without
blocking.

**One contact per company.** The highest-ranking person matching the
buyer title. Don't stack multiple contacts at the same company.

---

**FINDING EMAILS (depends on what tools are connected):**

**If enrichment tools are connected** (MCP or API keys):
Use whatever tools are available. Follow their API conventions.
**NEVER hardcode or display API keys.** Always use $ENV_VAR.
If a tool returns no email for a company, fall through to the
pattern-guess method below.

**If no enrichment tools OR tools failed for this contact:**

1. Check for publicly available email: company website contact page,
   LinkedIn profile, press releases, conference speaker bios.

2. **Pattern-guess the email:** Look for ANY known email at the
   company domain (from website footer, press contacts, job postings,
   other employees on LinkedIn). Detect the pattern:
   - first.last@domain.com (most common)
   - flast@domain.com
   - firstl@domain.com
   - first@domain.com

   Apply the pattern to your contact's name. Mark as:
   `{guessed email} (pattern-guess — verify before sending)`

3. **If no pattern detectable:** Mark as "LinkedIn only" and ensure
   the LinkedIn URL is captured. This contact gets a LinkedIn
   connection request instead of a cold email. This is NOT a failure
   — LinkedIn outreach often outperforms cold email for senior buyers.

---

**MID-SESSION TOOL CHANGES:** If the user mentions they just
connected a new tool (e.g., "I just set up my API key for X"),
re-detect tools immediately, update icp.md Connected Tools, and
use the new tool for remaining prospects. Don't wait for the next
/start run.

**ICP CHANGES:** If the user updates their ICP mid-flow (new
titles, new industries, expanded buyer profile), update icp.md
first, then re-run the search with the updated criteria.
Acknowledge: "Updated ICP to include {change}. Re-searching."

---

**For each contact, capture:**
- Full name (title-case, drop if 1 char or initials only)
- Title
- Company
- LinkedIn URL if found
- Email: {verified email}, {pattern-guess email}, or "LinkedIn only"
- Email source: {tool name}, pattern-guess, public, or LinkedIn-only

**One contact per company.** The highest-ranking person matching the
buyer title. Don't stack multiple contacts at the same company.

### Step 6: Present Complete Prospect List

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PROSPECTS READY: {N} contacts at {N} companies
  {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Name} — {Title} — {Company}
    Email: {email}
    Signal: {what's happening + date}
    LinkedIn: {URL if found}

  {Name} — {Title} — {Company}
    Email: {pattern-guess email} (verify before sending)
    Signal: {what's happening + date}
    LinkedIn: {URL}

  {Name} — {Title} — {Company}
    Email: LinkedIn only
    Signal: {what's happening + date}
    LinkedIn: {URL}

  ...

  ──────────────────────────────────────────────

  {N} prospects ready for outreach.
  {N} with verified email → cold email + LinkedIn
  {N} with pattern-guess email → verify, then email
  {N} LinkedIn only → connection request

  Does this list look right? I'll start writing
  personalized outreach once you confirm.
```

### ✋ APPROVAL GATE

Wait for confirmation that the contact list looks right.

**After the user confirms the contact list, automatically proceed to
run the /outreach process.** Do not wait for them to type "/outreach".
Save prospects.md and start writing emails immediately.

### Step 7: Save

Save to `./gtm/prospects.md`:

```markdown
# Prospect List

## Last Updated
{date}

## Batch: {date}

| Name | Title | Company | Domain | Email | Email Source | Signal | Channel | Score | LinkedIn | Status |
|------|-------|---------|--------|-------|-------------|--------|---------|-------|----------|--------|
| {name} | {title} | {company} | {domain} | {email or "LinkedIn only"} | {source} | {signal} | {channel} | {score} | {url} | ready |

## Dropped
- {company}: {reason}
```

Status values: `ready`, `outreach-written`, `sent`, `replied`, `no-reply`

---

## Running Prospect Again

On subsequent runs, /prospect:
- Deduplicates against existing prospects.md
- Shows only new companies not already in the list
- Appends new batch with date header
- Preserves status of existing prospects

---

## Handling Questions and Tangents

If the user asks a question mid-flow ("what's a good email tool?",
"why did you drop that company?", "what does behavioral signal mean?"),
answer clearly, then resume where you left off.

If they ask for a tool recommendation ("what email finder should I
use?", "should I get Apollo?"), research current options via WebSearch.
Give an honest answer based on their situation. Then offer to help
connect it: "Want to set it up now? I can detect it and use it for
the remaining prospects." Return to the flow after.

If they want to change something mid-search ("add CFOs to the target
list", "actually exclude fintech"), update icp.md and re-search.
Acknowledge the change and continue.

If they go off-topic, answer their question, then: "Back to
prospecting — [resume where you left off]."

---

## Edge Cases

**User provides their own list:**
If the user pastes company names, research each one (signals, contacts)
and add to prospects.md. Skip the search step.

**Not enough results:**
If fewer than 10 companies found, broaden the search:
- Expand to moderate-intent signals
- Lean harder on social channels (Reddit and X often surface
  companies that news searches miss)
- Widen industry or size criteria slightly
- Report what was tried and suggest adjusting ICP

**Social-sourced prospect with no company identified:**
Sometimes a Reddit poster or X user discusses the problem but their
company isn't identifiable. Note the username/handle and the thread
URL. The user can follow up manually or use LinkedIn to identify them.
Add to prospects.md with company as "Unknown — {platform} user" and
include the thread/post URL in the signal column.
