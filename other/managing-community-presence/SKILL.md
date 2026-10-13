---
name: managing-community-presence
version: "2.0.0"
description: >
  Manages FlashFusion's community intelligence and audience engagement using
  HubSpot (MCP connected), Notion (MCP connected), and LinkedIn (manual
  surface — no MCP). Common Room is NOT connected; this skill works without
  it and flags its absence explicitly. Surfaces who is engaging with
  FlashFusion content, identifies high-intent community members, and guides
  community-building decisions for the newsletter audience and LinkedIn
  following. Activates when the user mentions: community, audience engagement,
  who's engaging with my content, community building, newsletter audience,
  community intelligence, GTM community, who should I reach out to from my
  audience, Common Room (will surface NOT_CONNECTED status), LinkedIn
  engagement signals, warm prospect identification, or any request to
  understand or act on who is engaging with FlashFusion.
allowed-tools: Read Write Bash
---

# Community Presence Manager

Community signal → pipeline routing, wired through HubSpot (MCP ✅) and
Notion (MCP ✅). LinkedIn is a manual surface — pull signals by hand, route
decisions through connected tools. Common Room is not connected; see
DEPENDENCY_DECLARATION for the manual fallback path.

---

## DEPENDENCY_DECLARATION

| Tool | Status | Operational Path | Notes |
|------|--------|-----------------|-------|
| HubSpot | MCP ✅ CONNECTED | Create / update contacts, log activity notes, pipeline stage changes | Primary CRM path |
| Notion | MCP ✅ CONNECTED | Log community intel, update engagement tracker | FlashFusion HQ root: `cda29e98-3f08-4c83-8cfe-4c1e560836ee` |
| LinkedIn | MANUAL SURFACE | Open browser, pull engagement signals by hand, paste here | No MCP / API available |
| Common Room | ❌ NOT_CONNECTED | — | Manual URL: https://app.commonroom.io — log in manually; see Section 5 for what to pull |

**Hard rule:** No step in this skill calls Common Room via MCP. If the user references Common Room data, treat it as a manual paste and route it through HubSpot and Notion steps below.

---

## FAIL_IF

- **FAIL_IF** you query Common Room via MCP — it is not connected; any data returned would be fabricated.
- **FAIL_IF** you present engagement signal data as "from Common Room" without the user confirming they pulled it manually from https://app.commonroom.io.
- **FAIL_IF** you infer LinkedIn engagement signals from memory or training data — signals must be explicitly provided in this session.
- **FAIL_IF** you create or update a HubSpot contact without user confirmation — all write operations require explicit approval per connector permissions.
- **FAIL_IF** you embed any API key, HubSpot secret, or OAuth token in any output — all HubSpot writes go through the connected MCP only.
- **FAIL_IF** you batch-create HubSpot contacts without per-contact confirmation.

**"Just do it" override:** if the user provides explicit signals in the conversation and says to proceed, skip clarification and label all assumptions inline.

---

## Evals

**Should trigger:**
1. "Who's been engaging most with my LinkedIn posts this month?"
2. "I want to do a community check before I start my next outreach cycle"
3. "Pull community signals — who looks like a warm prospect?"
4. "Common Room — what's it showing?" (will surface NOT_CONNECTED status and offer manual path)
5. "Who should I reach out to from my newsletter audience?"

**Should NOT trigger:**
1. "Help me write a LinkedIn post" → use generating-social-posts
2. "Find new prospects for FlashFusion" → use managing-ff-pipeline
3. "Write my next newsletter edition" → use producing-ai-newsletter

---

## Section 1: LinkedIn Signal Pull (Manual — 10 minutes)

LinkedIn has no MCP. Pull signals by hand, then paste them into this session to continue.

**What to open:**
- LinkedIn → Notifications → filter by "reacted to your post" and "commented on your post"
- Your 2–3 most recent posts → open each, check who commented (comments > likes for intent)
- LinkedIn → your profile → Recent activity → who followed you this week

**Signal tier weights:**

| Signal | Weight |
|--------|--------|
| Commented on a post | High |
| Shared your post | High |
| Sent a direct message | High |
| Reacted to 3+ posts in a week | Medium |
| Reacted once | Low — monitor |
| Followed your profile | Low — monitor |

**Paste format for this session:**
```
Name: [Full Name]
Title / Company: [Title at Company]
Signals: [e.g., "commented on workflow post + reacted to 3 others this week"]
LinkedIn URL: [url]
Already in HubSpot: [yes / no / unsure]
ICP fit: [yes / no / unsure — MSP, SaaS, tech team, content creator]
```

Paste one or multiple entries. The workflow below consumes them.

---

## Section 2: Routing Signals Through HubSpot (MCP ✅)

Once signals are pasted, route each person through one of four HubSpot actions.

### Decision tree

```
Signal received →
  ├─ Person already in HubSpot?
  │     Yes → update activity note with signal detail and date
  │     No  → ICP fit? (MSP, SaaS, tech team, content creator)
  │               Yes → create contact + tag COMMUNITY_SOURCE, stage = PROSPECT
  │               No  → skip, or tag WATCH_LIST if borderline
  ├─ Peer, collaborator, or adjacent creator?
  │     → create contact + tag PARTNER_POTENTIAL
  └─ Newsletter reader showing ICP signals?
       → update contact with NEWSLETTER_ENGAGED tag; note specific content engaged
```

### HubSpot operations (via MCP — confirm before executing)

**Search before creating** — always check for duplicates by name or LinkedIn URL first.

**Create a new contact:**
- Required: first name, last name, LinkedIn URL (in "LinkedIn Bio URL" field)
- Source: "Community" (not "Inbound" or "Outbound")
- Stage: PROSPECT (ICP fit) or WATCH_LIST (monitor)
- Optional: company, job title

**Update activity note on existing contact:**
```
[DATE] Community signal — LinkedIn
Signal type: [commented / shared / reacted / DM]
Specific content engaged: [post title or topic]
Signal weight: High / Medium / Low
Action taken: [followed back / messaged / added to pipeline sequence / none]
```

---

## Section 3: Logging Community Intel to Notion (MCP ✅)

Signals that don't produce a HubSpot action (non-ICP contacts, audience trends, strategy notes) go to Notion.

**Target:** FlashFusion HQ root → Community Intelligence log
Parent page root: `cda29e98-3f08-4c83-8cfe-4c1e560836ee` — navigate from here to the correct sub-page.

**Log entry format:**
```
## [DATE] Community Pulse

### LinkedIn Signals This Week
- [Name] ([Title, Company]): [Signal] → [Action taken or "none — monitor"]
- [Name]: [Signal] → [Action]

### Trends Observed
- [Recurring topic in comments]
- [Type of post driving highest engagement]

### Newsletter (manual pull from Substack)
- Open rate: [%] | Click rate: [%]
- Top-performing issue: [topic]

### Community Threshold Check
Active subscribers: [number]
Status: [ ] Pre-threshold  [ ] Approaching 1k  [ ] Ready for dedicated platform
Recommendation: [distributed strategy / beginning to evaluate / ready to act]
```

---

## Section 4: Engagement Response Patterns

Response is proportional to signal weight. Community trust is the asset — every engaged reader who becomes a sales target without a genuine relationship is a trust withdrawal.

| Engagement level | Response |
|-----------------|---------|
| 1–2 low signals | No action — add to watch list if ICP fit |
| 3–5 mixed signals | Follow on LinkedIn if not already; no message yet |
| 6–10 signals, ICP fit | Direct LinkedIn message — curiosity opener, not a pitch |
| 10+ signals, ICP fit | Add to HubSpot as warm PROSPECT; reference specific content in opener |
| Any level, peer / collaborator | Outreach for partnership or guest content conversation |

**DM opener template (not a sales message):**
> "I've noticed you've been reading the FlashFusion content — what are you working on right now?"

The opener exists to start a conversation, not to convert. Conversion comes later if fit is real.

---

## Section 5: Common Room Manual Path (When Browser Session Open)

Common Room is not connected via MCP. If you have a live browser session at https://app.commonroom.io, pull these signals manually and paste them into this conversation:

**What to pull from Common Room:**
1. Activity feed → members with 3+ signals in the last 7 days
2. Member list → sort by engagement score descending → top 10
3. For each: name, platform, signal type, count, LinkedIn URL if available

**Paste format:**
```
Name: [Full Name]
Platform: [LinkedIn / Newsletter / other]
Signals: [e.g., "3 newsletter opens, 2 LinkedIn interactions"]
LinkedIn URL: [if available]
```

Route these through Section 2 (HubSpot) and Section 3 (Notion) exactly as you would LinkedIn signals.

**When Common Room connects via MCP:** replace Sections 1 and 5 with a live query step, remove this manual bridge.

---

## Section 6: Community Building Strategy

FlashFusion's community is currently distributed — newsletter subscribers, LinkedIn followers. Current strategy: newsletter as anchor, LinkedIn as discovery surface, individuals treated as individuals rather than an audience.

**Threshold to evaluate a dedicated community platform (Slack / Discord / Circle):**
- Newsletter list exceeds 1,000 active subscribers
- Consistent inbound conversation volume that benefits from group discussion rather than 1-on-1 answers
- A defined audience segment (e.g., MSP technicians learning AI) with sufficient density to sustain peer interaction

**Do not** create a community platform before the audience density exists. A Slack or Discord with 12 members creates maintenance burden and signals low traction to anyone who joins.

Track the threshold check in Notion monthly (Section 3 log entry).

---

## Self-Verification Checklist

**Weekly:**
- [ ] LinkedIn signals pulled manually and pasted into session — **FAIL** if you skip this and infer signals from memory
- [ ] High-signal ICP-fit contacts added or updated in HubSpot via MCP — **FAIL** if HubSpot is bypassed for contacts that warrant action
- [ ] Community intel logged to Notion — **FAIL** if this step is skipped for three consecutive weeks
- [ ] Warm contacts messaged within 48 hours of signal before they cool

**Monthly:**
- [ ] Newsletter engagement trends reviewed (open rate, click rate) — manual pull from Substack
- [ ] Community threshold check documented in Notion with current subscriber count
- [ ] Common Room manual pull completed if a browser session is available

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

**CLAIMS**
- [GENERATED] Outreach referencing specific content the contact engaged with converts at higher rates than cold openers — documented principle in community-led GTM; FlashFusion-specific numbers are not yet measured.
- [GENERATED] Newsletter engagement (clicks > opens) is a stronger intent proxy than LinkedIn follows alone, because clicks require deliberate action while opens can be triggered by email clients automatically.

**COUNTEREXAMPLE**
- LinkedIn engagement can be skewed by algorithmic amplification — a post that went wide will attract commenters with no ICP fit. Weight comments on niche-topic posts (workflow breakdowns, MSP AI content) more heavily than comments on high-reach general posts.
- Common Room open signals from the newsletter are unreliable due to auto-open behavior in email clients. Weight click and comment signals more heavily than opens in Common Room data.

**CONTRADICTIONS**
- "Move high-engagement members to pipeline" conflicts with community relationship integrity. Resolve by moving to pipeline only when ICP fit is explicit AND a genuine interaction already exists. Converting every engaged reader to a sales target destroys the engagement signal source that makes this workflow valuable.

---

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- **No Substack MCP.** Newsletter engagement data (open rate, click rate, per-issue opens) must be pulled manually from Substack's dashboard. There is no live path for newsletter analytics in this skill.
- **Common Room not connected.** All Common Room steps are manual bridges. When Common Room connects via MCP, Sections 1 and 5 should be rewritten to replace manual pulls with live queries.
- **LinkedIn API not available.** Engagement signals require a manual pull every time this workflow runs. If LinkedIn surfaces an MCP integration, update Section 1 to automate signal ingestion.
- **HubSpot write operations require per-contact confirmation** per connector permissions. Do not batch-create without user approval for each record.
- **SELF-REVIEW:** Verified no Common Room MCP calls present. All HubSpot and Notion operations route through connected MCPs. LinkedIn steps are explicitly manual. DEPENDENCY_DECLARATION and FAIL_IF blocks added. Version bumped to 2.0.0 (major — gate logic and tool dependencies changed from original).
