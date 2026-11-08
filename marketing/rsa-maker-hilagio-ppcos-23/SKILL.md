---
name: rsa-maker
description: Create Google Ads Responsive Search Ads from offer angles and brand context, outputting a CSV ready for Editor import. Use to create, build, or generate RSAs from angles.
argument-hint: "[--new]"
---

# RSA Maker Skill

Generate Google Ads Responsive Search Ads from offer angles and brand context, outputting CSV files ready for import into Google Ads Editor.

## Command Format

```
/rsa-maker [--new]
```

**Examples:**
- `/rsa-maker` - Interactive mode, asks existing or new campaign
- `/rsa-maker --new` - Skip to manual name entry

---

## Process

### Step 1: Prerequisites Check

Check required context files:

| File | Required | If Missing |
|------|----------|------------|
| `context/offer-angles.md` | Yes | Prompt: "Run `/offer-maker angles` first" |
| `context/brand.md` | Yes | Prompt: "Run `/ads-context [URL]` first" |

**If both missing, stop and show:**

```markdown
## Prerequisites Missing

To create quality RSAs, the following context is required:

| File | Status | Action |
|------|--------|--------|
| context/offer-angles.md | Missing | Run `/offer-maker angles` first |
| context/brand.md | Missing | Run `/ads-context [URL]` first |
```

**If one exists, show which is missing and the action to take.**

---

### Step 2: Campaign/Ad Group Selection

**Question:** "Is this for an existing campaign/ad group or a new one?"

Use AskUserQuestion tool:
- **Option 1:** "Existing campaign/ad group" - Select from account data
- **Option 2:** "New campaign/ad group" - Enter names manually

**If existing (`--new` flag NOT provided):**
1. Read `context/google-ads/data/campaigns.csv` → extract unique `campaign.name` values
2. Read `context/google-ads/data/ads.csv` → extract unique `ad_group.name` values
3. Present campaign options via AskUserQuestion (max 4 options + Other)
4. If more than 4 campaigns, show top 4 by impressions and allow "Other" for manual entry
5. After campaign selection, show ad groups for that campaign

**If new (or `--new` flag):**
1. Ask: "Enter the exact campaign name:"
2. Ask: "Enter the exact ad group name:"

---

### Step 2.5: Peer Context Pull (Mode 2 — Enrichment, no gate)

Before composition, read fresh peer audit reports and extract findings that should bias the headlines, descriptions, and CTAs you generate. **This is purely read + extract. No gate, no warn-and-abort, no hard-block.** If a peer report is missing or stale, skip that row silently — generation continues either way. The maker's *output quality* is what improves; peer findings flow into the generated asset.

**2.5.1 Walk the 10-peer freshness table.**

For each peer, check that the report file exists and is fresh per the window below. **Freshness rule:** the report header date is canonical. Read the first 30 lines of each peer file and locate the header date (typically `**Generated:** YYYY-MM-DD` or similar). If the file's mtime is older than the header date, surface a warning in the user-facing output (the file may have been edited but the header wasn't refreshed — treat the header as the source of truth, but flag the discrepancy). If the header date is within the fresh window, the peer is FRESH. Otherwise STALE — skip silently.

| Peer skill | Report file | Fresh window | Highest-leverage signal for RSAs |
|---|---|---|---|
| `/quality-score-auditor` | `context/analysis/quality-score-audit.md` | ≤ 7 days | Ad Relevance, Expected CTR per AG |
| `/search-term-auditor` | `context/analysis/search-term-audit.md` | ≤ 7 days | Top converting n-grams to mirror in headlines |
| `/keyword-auditor` | `context/analysis/keyword-audit.md` | ≤ 7 days | Per-AG keyword themes for headline pinning |
| `/budget-auditor` | `context/analysis/budget-audit.md` | ≤ 7 days | Which AGs are budget-limited (lower priority) |
| `/bidding-auditor` | `context/analysis/bidding-audit.md` | ≤ 7 days | Smart-bidding context |
| `/competitive-analyst` | `context/analysis/competitive-audit.md` | ≤ 14 days | Differentiation angles vs competitors |
| `/lp-auditor` | `context/analysis/lp-audit.md` | ≤ 14 days | Message-match alignment to LP H1/offer |
| `/offer-auditor` | `context/analysis/offer-audit.md` | ≤ 30 days | Offer angles to lead with |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days | Informational warning if dirty |
| `/strategy-specialist` | `context/analysis/strategy-audit.md` | ≤ 30 days | Posture/break-even informs CTA urgency |

(`/account-auditor` is not part of the table — RSAs are about ad-group themes, not naming conventions. If `context/analysis/account-audit.md` is fresh and contains AG-level findings that look material, you may include it ad-hoc.)

**2.5.2 For each FRESH peer, extract findings relevant to the selected campaign/ad group and quote them into a peer-context buffer.**

Build an in-memory buffer keyed by peer skill. For each fresh peer, scan the report for the selected ad-group name (and selected campaign name, as fallback). Extract:

| Peer | What to extract |
|------|----------------|
| QS auditor | Handoff Queue rows (Ad Relevance, Expected CTR) for the target AG. Note `dominant_issue`, `recommended_action`, `class` (BRANDED/COMPETITOR/PROBLEM/SOLUTION). |
| Search-term auditor | Top converting n-grams for the target AG (from the n-gram module). 3-7 phrases the user actually searches and converts on. |
| Keyword auditor | Per-AG keyword theme — the dominant intent cluster + top-volume keywords for this AG. |
| Budget auditor | Is this AG's campaign budget-limited? (Yes/No flag — informs how aggressively to lean on USP vs price-anchor language.) |
| Bidding auditor | Smart-bidding strategy + learning state for this campaign (informs whether the AG is in a stable optimization regime or still volatile). |
| Competitive analyst | Differentiation angles vs top competitors for this campaign's keyword set. |
| LP auditor | Message-match findings for the target Final URL — the LP's H1, primary offer phrasing, and any flagged mismatches. |
| Offer auditor | Strongest offer angle (guarantee, value prop, urgency, trust) per offer-audit's recommendations for this campaign/AG. |
| Tracking specialist | Module M (Measurement) status — clean or dirty? |
| Strategy specialist | Account posture (growth/maintain/efficiency) and break-even constraints — informs CTA urgency. |

Quote the actual finding text into the buffer (don't just note "QS audit fresh" — pull the row). Example buffer entry:

```
QS auditor (FRESH, 2 days old):
  - Ad group "AI Slides — Exact" has 4 keywords with AR Below Avg.
  - dominant_issue: "headline does not contain keyword phrase"
  - recommended_action: "Tighten H1 anchoring via Method B (Static Anchoring) — pin the
    keyword 'AI presentation maker' to H1 across all RSAs."
  - class: SOLUTION

Search-term auditor (FRESH, 1 day old):
  - Top converting n-grams for AG "AI Slides — Exact":
    1. "ai presentation maker" (28 conv)
    2. "make slides with ai" (19 conv)
    3. "ai powerpoint generator" (12 conv)
    4. "create slides ai" (8 conv)
```

**2.5.3 Surface peer-report contradictions.**

After building the buffer, scan for cross-peer contradictions and quote both sides. **Do NOT auto-pick a winner.** Examples to watch for:

- LP auditor says LP H1 is "X" but offer auditor recommends leading offer angle "Y" (which doesn't appear on the LP).
- QS auditor's recommended `class` (e.g., BRANDED) conflicts with the user's Step 3 traffic temperature (e.g., they classified Cold).
- Search-term auditor's top n-gram differs from keyword auditor's dominant theme for the same AG.

If contradictions exist, surface them in the user-facing summary (Step 8) so the user picks which signal to align to. Quote both verbatim.

**2.5.4 Tracking-audit informational note.**

If `tracking-audit.md` is FRESH and Module M (Measurement) is dirty (any HIGH-severity findings, or the M-layer score is < 70), surface this one-liner once in the user-facing output (Step 8 summary header):

> "Note: tracking-audit shows M layer dirty — RSAs will be created but performance measurement is unreliable until tracking is fixed."

**Informational only. Does NOT block generation.**

**2.5.5 Header-vs-mtime warning.**

If any peer report's filesystem mtime is older than its header date, surface this in the Step 8 summary:

> "Warning: `{peer-report.md}` header date is {YYYY-MM-DD} but file mtime is older — header treated as canonical, but the report may have been edited inconsistently. Verify before relying on findings."

**2.5.6 No gate.**

If zero peer reports are fresh, generation still proceeds. The peer-context buffer is simply empty, and the Step 8 "Cross-skill context applied" section will say "No fresh peer audits available — RSAs composed from offer-angles.md and brand.md only." This is Mode 2 enrichment, not a Mode 1 gate.

---

### Step 3: Traffic Temperature Classification

Different traffic types need different angle emphasis. Check if the selected campaign matches the classification in `offer-angles.md`.

**3.1 Read existing classification:**

Parse `context/offer-angles.md` → Traffic Classification section:
- Campaign/Traffic name
- Awareness Stage
- Temperature (Cold/Warm/Hot)

**3.2 Decision logic:**

| Scenario | Action |
|----------|--------|
| Campaign name matches offer-angles classification | Use existing temperature, confirm with user |
| Campaign name differs OR new campaign | Ask user to classify traffic temperature |

**3.3 If classification needed, use AskUserQuestion:**

**Question:** "What type of traffic will this RSA serve?"

**Options:**

| Option | Description |
|--------|-------------|
| Brand Search (Hot) | People searching for your brand name |
| Competitor Search (Hot) | People searching for competitor names |
| Product/Service Search (Warm) | People searching for what you sell (e.g., "AI presentation maker") |
| Problem/Symptom Search (Cold) | People searching for their problem (e.g., "how to make slides faster") |
| Remarketing (Hot) | Previous visitors returning |

**3.4 Set angle priorities based on temperature:**

| Angle | Cold | Warm | Hot |
|-------|------|------|-----|
| Problem/Pain | **LEAD** (H2-H3) | Include (H8) | Light |
| Value Proposition | Include (H4) | **LEAD** (H2) | Include |
| USPs | Light | **LEAD** (H3, H6) | **LEAD** |
| Value Boosters | Skip | Include | **LEAD** |
| Social Proof | Light | Include (H4) | **LEAD** |
| Risk Removal | Skip | Include (H5) | **LEAD** |

**Priority meanings:**
- **LEAD** = Multiple headline slots (H2, H3, H6)
- **Include** = At least one headline slot
- **Light** = Optional, in descriptions only
- **Skip** = Don't emphasize

---

### Step 4: Gather Additional Inputs

Collect the following using AskUserQuestion:

1. **Final URL** (required):
   - Question: "What is the Final URL? (e.g., https://plusai.com/)"
   - Validate: Must start with `https://`

2. **Path 1** (optional):
   - Question: "Display URL path 1 (max 15 chars, leave blank to skip):"
   - Validate: Max 15 characters

3. **Path 2** (optional):
   - Question: "Display URL path 2 (max 15 chars, leave blank to skip):"
   - Validate: Max 15 characters

4. **Pinning** (optional):
   - Question: "Should specific headlines/descriptions be pinned to positions?"
   - Options:
     - "Yes - Pin key messages (Recommended)" - Claude selects up to 3 pins
     - "No - Let Google optimize all positions"

---

### Step 5: RSA Composition

Read `context/offer-angles.md` and `context/brand.md` to compose RSA assets. **Apply the peer-context buffer from Step 2.5 to bias the generated headlines, descriptions, and CTAs.**

**Reference files to read for this step:**
- `references/rsa-composition-sop.md` — Assembly framework, slot distribution, pinning rules
- `references/headline-angle-catalog.md` — Headline patterns by type (7 types with formulas + examples)
- `references/description-expansion-catalog.md` — Description patterns (single-angle + combined-angle)
- `references/headline-quality-checklist.md` — Validate headlines after composition
- `references/description-quality-checklist.md` — Validate descriptions after composition

**Use the traffic temperature from Step 3 to determine slot distribution.**

#### 5.0 Peer-Context Biasing Rules

The peer-context buffer from Step 2.5 changes *what* gets generated (not *whether*). Apply the rules below in order — each one points to the slots it influences and the precise effect on copy. Track which rules fired so the Step 8 summary can list them under "Cross-skill context applied."

| Trigger (peer finding) | Effect on generation |
|---|---|
| **Search-term auditor FRESH** with top n-grams for target AG | Mirror the top 3-5 n-grams verbatim (or near-verbatim, respecting 30-char limit) in headlines. Distribute across H2-H4 by search volume — top n-gram → H2, second → H3, third → H4. Do not stuff; one n-gram per headline max. |
| **Keyword auditor FRESH** with per-AG keyword theme | Use the dominant theme keyword as the H1 anchor (overrides default `{KeyWord:Default}` framing — write a static H1 containing the theme keyword for stable Static Anchoring). Use 1-2 secondary cluster keywords in H6 / H8. |
| **QS auditor FRESH + Ad Relevance Below Avg** for target AG | Prioritize tight keyword-mirroring in pinned headlines. Pin H1 to position 1 with the target AG's primary keyword phrase verbatim. Use Method B (Static Anchoring) — drop `{KeyWord:Default}` in favor of a hardcoded keyword headline. Avoid abstract benefit framing in H1-H3; benefits go to H4-H8. |
| **QS auditor FRESH + Expected CTR Below Avg** for target AG | Lead H2-H4 with strong benefit / value-prop language and clear CTAs. Front-load specificity (numbers, outcomes, time savings). Description D1 must combine value-prop + clear next-step CTA. Avoid passive / generic copy. |
| **QS auditor handoff class = BRANDED** for target AG | Branded low-QS is usually LP message-match — surface the BRANDED-class warning to the user (informational), and prioritize H1 = brand name + primary product, with descriptions mirroring the brand promise from `brand.md`. |
| **QS auditor handoff class = COMPETITOR** for target AG | AR Below Avg is structurally expected for COMPETITOR campaigns — don't force tight keyword-mirroring. Lead with differentiation USPs and offer strength (per offer-audit) rather than relevance methods. |
| **LP auditor FRESH + Message Match flagged** for target Final URL | Headlines and descriptions must align with the LP's H1 and primary offer copy. Quote the LP H1 into the buffer; H2 of the RSA should echo or paraphrase the LP H1 within 30 chars. D1 must include the LP's primary offer phrasing. If the LP H1 is materially different from offer-angles.md's value-prop, flag the contradiction (Step 2.5.3) and ask the user which to align to in Step 8. |
| **Offer auditor FRESH** with strongest offer angle | RSAs lead with the strongest offer angle per offer-audit's recommendations. If "guarantee" is strongest → H4 or H5 = risk-removal headline + D2 = guarantee + CTA. If "value-prop" is strongest → H2 = value-prop. If "urgency" is strongest → H7 (CTA) carries urgency phrasing + D3 = urgency + risk-removal. Override the temperature-based slot defaults where offer-audit's recommendation is stronger. |
| **Budget auditor FRESH + AG's campaign IS budget-limited** | Lower priority for this AG — keep RSAs simpler and tighter (fewer headlines, target 7 not 15). Lead with high-CTR / high-conversion-rate language to maximize value of each impression. Note in Step 8 summary: budget-limited campaign, RSAs designed for impression efficiency. |
| **Budget auditor FRESH + AG's campaign NOT budget-limited** | Standard priority — full 15 headlines, full 4 descriptions, broader angle coverage. |
| **Bidding auditor FRESH + smart bidding in LEARNING state** | RSAs should not introduce drastic copy variance during learning — use 1-2 dominant angles per RSA rather than 5+ competing angles. This stabilizes the bidding signal. Note in Step 8 summary. |
| **Bidding auditor FRESH + tCPA / tROAS strategy** | Lean into proof / value-prop language that aligns with the conversion goal — tCPA campaigns favor lead-gen / signup CTAs; tROAS campaigns favor revenue / value-driven CTAs. |
| **Competitive analyst FRESH** with differentiation angles | Use 1-2 differentiation angles in H3 / H6 (USP slots). Quote the differentiator verbatim where character limit allows. Avoid generic "best in class" framing — use the specific axis the competitive audit identified. |
| **Strategy specialist FRESH + posture = growth** | CTA tone = inviting, low-friction ("Start free trial", "See it in action"). |
| **Strategy specialist FRESH + posture = efficiency** or **break-even tight** | CTA tone = decisive, high-intent ("Get a quote", "Book a demo"). Lean on risk-removal in D2. |
| **Tracking specialist FRESH + M-layer dirty** | No effect on copy. Surface the informational note in Step 8 summary header (per Step 2.5.4). |

**Conflict resolution between peer rules:**
- When two rules target the same slot (e.g., search-term-auditor wants H2 = top n-gram, but offer-auditor wants H2 = value-prop), the closer-to-traffic peer wins: **search-term > keyword > QS > offer > LP > competitive > bidding > budget > strategy > tracking**. Note the conflict and the resolution in the Step 8 summary.
- When peer rules conflict with the temperature-based default slot distribution (Step 3.4), peer rules win — they are based on observed account data, not heuristics.
- When peer reports themselves contradict (e.g., LP H1 ≠ offer-audit's recommended angle), do NOT auto-pick. Surface both in Step 8 and ask the user.

**Track which rules fired** in a `peer_rules_fired` list — this drives the Step 8 "Cross-skill context applied" section. Each entry: `{rule_name, slot_affected, source_quote}`.

#### Slot Distribution by Temperature

**Cold Traffic (Problem/Symptom Search):**

| Slot | Angle | Source |
|------|-------|--------|
| H1 | Relevance Anchor | `{KeyWord:Default}` |
| H2 | Problem/Pain (LEAD) | offer-angles.md → Problem/Pain phrases |
| H3 | Problem/Pain (LEAD) | offer-angles.md → Problem/Pain phrases (2nd) |
| H4 | Value Proposition | offer-angles.md → Value Prop phrases |
| H5 | USP | offer-angles.md → USP phrases |
| H6 | Social Proof | offer-angles.md → Social Proof phrases |
| H7 | CTA | brand.md → Primary CTA |

**Warm Traffic (Product/Service Search) - DEFAULT:**

| Slot | Angle | Source |
|------|-------|--------|
| H1 | Relevance Anchor | `{KeyWord:Default}` |
| H2 | Value Proposition (LEAD) | offer-angles.md → Value Prop phrases |
| H3 | USP (LEAD) | offer-angles.md → USP phrases |
| H4 | Social Proof | offer-angles.md → Social Proof phrases |
| H5 | Risk Removal | offer-angles.md → Risk Removal phrases |
| H6 | USP (LEAD secondary) | offer-angles.md → USP phrases (2nd) |
| H7 | CTA | brand.md → Primary CTA |
| H8 | Problem/Pain (optional) | offer-angles.md → Problem/Pain phrases |

**Hot Traffic (Brand/Competitor/Remarketing):**

| Slot | Angle | Source |
|------|-------|--------|
| H1 | Relevance Anchor | `{KeyWord:Default}` |
| H2 | USP (LEAD) | offer-angles.md → USP phrases |
| H3 | Value Booster (LEAD) | offer-angles.md → Value Booster phrases |
| H4 | Social Proof (LEAD) | offer-angles.md → Social Proof phrases |
| H5 | Risk Removal (LEAD) | offer-angles.md → Risk Removal phrases |
| H6 | USP (LEAD secondary) | offer-angles.md → USP phrases (2nd) |
| H7 | CTA | brand.md → Primary CTA |
| H8 | Value Booster (optional) | offer-angles.md → Value Booster phrases (2nd) |

#### Headlines (7-8 total, max 30 chars each)

**Composition guidelines:**
- Each headline MUST be ≤30 characters
- Use exact phrases from offer-angles.md when possible
- Use patterns from `references/headline-angle-catalog.md` to write headlines for each angle type
- Adapt CTA from brand.md to fit character limit
- If a phrase exceeds 30 chars, truncate or rewrite concisely
- Include character count for verification
- Follow the slot distribution for the selected traffic temperature

**After composing all headlines, validate against `references/headline-quality-checklist.md`.** Fix any failures before proceeding to descriptions.

#### Descriptions (2-3 total, max 90 chars each)

| Slot | Pattern | Construction |
|------|---------|--------------|
| D1 | Problem + Solution | Combine pain point + value prop (from offer-angles.md) |
| D2 | Proof + CTA | Social proof + action (from offer-angles.md + brand.md) |
| D3 | (Optional) Offer + Risk Removal | Value booster + guarantee (from offer-angles.md) |

**Composition guidelines:**
- Each description MUST be ≤90 characters, target 75-90
- Use patterns from `references/description-expansion-catalog.md` (Section A for single-angle, Section B for combined-angle)
- D1: Lead with problem, follow with solution (Catalog → Pattern 1: Problem + Solution)
- D2: Lead with proof (numbers), end with CTA (Catalog → Pattern 2: Proof + Benefit)
- D3: Include bonus value + risk removal if content available (Catalog → Pattern 3: Benefit + Risk Removal)

**After composing all descriptions, validate against `references/description-quality-checklist.md`.** Fix any failures before generating CSV.
- Include character count for verification

---

### Step 6: Pinning Logic (if enabled)

Apply up to 3 pins total. Selection criteria:

| Asset | Pin to Position | Rationale |
|-------|-----------------|-----------|
| H1 (Relevance Anchor) | Position 1 | Ensures keyword visibility in first headline |
| D1 (Problem + Solution) | Position 1 | Strongest description appears first |
| H7 (CTA) | Position 3 | Ends with clear action |

**Position values for CSV:**
- `1`, `2`, `3` = Pinned to that position
- `-` = Unpinned (Google optimizes)
- Empty = Slot not used

**If pinning disabled:** All position columns get `-` for used slots, empty for unused.

---

### Step 7: Generate CSV

**Use the helper script to ensure proper CSV formatting.**

**7.1 Create JSON input file:**

Create a JSON file at `created/rsas/{timestamp}_input.json` with the RSA data:

```json
[
  {
    "campaign": "Campaign Name",
    "ad_group": "Ad Group Name",
    "headlines": [
      {"text": "Headline 1 text", "position": "1"},
      {"text": "Headline 2 text", "position": "-"},
      {"text": "Headline 3 text", "position": "-"},
      {"text": "Headline 4 text", "position": "-"},
      {"text": "Headline 5 text", "position": "-"},
      {"text": "Headline 6 text", "position": "-"},
      {"text": "Headline 7 text", "position": "3"},
      {"text": "Headline 8 text", "position": "-"}
    ],
    "descriptions": [
      {"text": "Description 1 text (max 90 chars)", "position": "1"},
      {"text": "Description 2 text (max 90 chars)", "position": "-"},
      {"text": "Description 3 text (max 90 chars)", "position": "-"}
    ],
    "path1": "url-path",
    "path2": "segment",
    "final_url": "https://example.com/"
  }
]
```

**For multiple RSAs (e.g., one per ad group), use an array with multiple objects.**

**7.2 Run the CSV generator script:**

```bash
python3 .claude/skills/rsa-maker/scripts/generate-csv.py created/rsas/{timestamp}_input.json created/rsas/{timestamp}_{campaign}.csv
```

The script will:
- Validate headlines (≤30 chars) and descriptions (≤90 chars)
- Ensure all 45 columns are correctly aligned
- Output warnings for any issues
- Generate a properly formatted CSV

**7.2.1 Remove the JSON file after generating the CSV.**

After generating the CSV, remove the JSON file.

**7.2.2 Write the peer-context sidecar.**

Alongside the CSV, write a sidecar markdown file at `created/rsas/{timestamp}_{campaign}.context.md` containing:

- The full Step 8 "Cross-skill context applied" section (peer status table, rules-fired bullets, contradictions surfaced).
- The headlines/descriptions tables with their `Peer-rule source` columns.
- The informational notes block (tracking-audit warning, header-vs-mtime warnings, etc.).

The CSV stays Google-Ads-Editor-clean (no extra metadata that would corrupt import). The sidecar is the durable record of which peer findings shaped the asset, parallel to how optimizers persist their dry-run rationale. If no peer audits were fresh, the sidecar still gets written and contains the "No fresh peer audits available" note — this confirms peer enrichment was attempted and produced an empty buffer.

**7.3 Position values:**

| Value | Meaning |
|-------|---------|
| `1` | Pin to position 1 |
| `2` | Pin to position 2 |
| `3` | Pin to position 3 |
| `-` | Unpinned (Google optimizes) |

**7.4 Filename format:**

- JSON input: `{YYYYMMDD_HHMMSS}_input.json`
- CSV output: `{YYYYMMDD_HHMMSS}_{campaign_name_sanitized}.csv`
- Sanitize: lowercase, replace spaces with `-`, remove special chars

---

### Step 8: Present Summary

After generating the CSV, present:

```markdown
## RSA Created

**Campaign:** {campaign_name}
**Ad Group:** {ad_group_name}
**Traffic Temperature:** {Cold/Warm/Hot} ({traffic_type})
**Output:** created/rsas/{filename}.csv

{informational_notes_block — surface tracking-audit M-layer warning here, header-vs-mtime
warnings, and any peer-report contradictions that need user resolution. Skip the block if
none apply.}

### Cross-skill context applied

Peer audits consulted (Step 2.5):

| Peer skill | Status | Effect on this RSA |
|---|---|---|
| /quality-score-auditor | {FRESH N days / STALE / MISSING} | {one-line effect or "no relevant findings" or "—"} |
| /search-term-auditor | {FRESH / STALE / MISSING} | {one-line effect} |
| /keyword-auditor | {FRESH / STALE / MISSING} | {one-line effect} |
| /budget-auditor | {FRESH / STALE / MISSING} | {one-line effect} |
| /bidding-auditor | {FRESH / STALE / MISSING} | {one-line effect} |
| /competitive-analyst | {FRESH / STALE / MISSING} | {one-line effect} |
| /lp-auditor | {FRESH / STALE / MISSING} | {one-line effect} |
| /offer-auditor | {FRESH / STALE / MISSING} | {one-line effect} |
| /tracking-specialist | {FRESH / STALE / MISSING} | {informational only — no copy effect} |
| /strategy-specialist | {FRESH / STALE / MISSING} | {one-line effect} |

**Specific rules fired** (from peer_rules_fired list — one bullet per slot influenced):

- Headlines 1–3 mirror the search-term-auditor's top n-grams: "{n-gram-1}", "{n-gram-2}", "{n-gram-3}".
- Headline 1 (pinned) addresses the QS-audit Ad Relevance Below Avg finding for ad group `{AG}` — Static Anchoring on keyword "{kw}".
- Description 1 leads with offer-audit's strongest angle: "{angle}" (e.g., guarantee / value-prop / urgency).
- Headlines 2 & 5 align with LP-auditor's Message Match finding — H2 echoes the LP H1: "{LP H1}".
- {…one bullet per rule that fired…}

**Contradictions surfaced** (if any — peer reports that disagreed; Claude did NOT auto-pick):

- LP-audit says LP H1 is "{X}", but offer-audit recommends leading angle "{Y}". Headlines currently align to {X}. Confirm the LP and the offer angle should match — or update one of them.
- {…etc…}

(Omit the contradictions sub-block if none.)

If zero peers were fresh: "No fresh peer audits available — RSAs composed from offer-angles.md and brand.md only. Run `/quality-score-auditor`, `/search-term-auditor`, `/keyword-auditor`, `/lp-auditor`, and `/offer-auditor` to enrich future RSA generation."

### Headlines ({count}/15)

| # | Headline | Chars | Pin | Peer-rule source |
|---|----------|-------|-----|------------------|
| 1 | {headline} | {X}/30 | {1/-} | {e.g. "ST-audit n-gram #1" or "—"} |
| 2 | {headline} | {X}/30 | {-} | {e.g. "QS-audit AR fix"} |
| ... | ... | ... | ... | ... |

### Descriptions ({count}/4)

| # | Description | Chars | Pin | Peer-rule source |
|---|-------------|-------|-----|------------------|
| 1 | {description} | {X}/90 | {1/-} | {e.g. "offer-audit guarantee angle"} |
| 2 | {description} | {X}/90 | {-} | {…} |
| ... | ... | ... | ... | ... |

### Import Instructions

1. Open **Google Ads Editor**
2. Go to **Account > Import > From file**
3. Select the CSV file: `created/rsas/{filename}.csv`
4. Review the imported ad
5. Post changes to your account
```

**Informational-notes block content** (assemble these conditionally and prepend to summary):

- If `tracking-audit.md` is FRESH and M layer is dirty:
  > "Note: tracking-audit shows M layer dirty — RSAs will be created but performance measurement is unreliable until tracking is fixed."
- For each peer report whose mtime is older than its header date:
  > "Warning: `{peer-report.md}` header date is {YYYY-MM-DD} but file mtime is older. Header treated as canonical, but verify the report wasn't edited inconsistently."
- If a contradiction exists between peer reports (LP-audit vs offer-audit, QS class vs user temperature, etc.):
  > "Contradiction: see 'Cross-skill context applied → Contradictions surfaced' below — review before importing."

---

## Error Handling

| Error | Message |
|-------|---------|
| Missing prerequisites | Show table with status and run commands |
| No campaigns.csv | "Run `/gads-context` first to pull account data, or use `--new` flag for manual entry" |
| Headline > 30 chars | Warning + auto-truncated version with note |
| Description > 90 chars | Warning + auto-truncated version with note |
| Invalid URL | "Final URL must start with https://" |
| Path > 15 chars | "Path must be 15 characters or less. Current: {X} chars" |

---

## Integration Points

### Uses (reads from):
- `context/offer-angles.md` - Source for headline phrases and slot distribution
- `context/brand.md` - Source for CTAs and brand voice
- `context/google-ads/data/campaigns.csv` - Campaign names for selection
- `context/google-ads/data/ads.csv` - Ad group names for selection

**Peer audit reports (Mode 2 enrichment, Step 2.5 — read-only, no gate):**
- `context/analysis/quality-score-audit.md` (≤7d) — Ad Relevance / Expected CTR per AG
- `context/analysis/search-term-audit.md` (≤7d) — Top converting n-grams per AG
- `context/analysis/keyword-audit.md` (≤7d) — Per-AG keyword themes
- `context/analysis/budget-audit.md` (≤7d) — Budget-limited AG flag
- `context/analysis/bidding-audit.md` (≤7d) — Smart-bidding strategy / learning state
- `context/analysis/competitive-audit.md` (≤14d) — Differentiation angles
- `context/analysis/lp-audit.md` (≤14d) — LP H1 / message-match
- `context/analysis/offer-audit.md` (≤30d) — Strongest offer angle
- `context/analysis/tracking-audit.md` (≤30d) — M-layer status (informational)
- `context/analysis/strategy-audit.md` (≤30d) — Posture / break-even

### Produces (writes to):
- `created/rsas/{timestamp}_{campaign}.csv` - Import-ready RSA file (Editor-clean)
- `created/rsas/{timestamp}_{campaign}.context.md` - Peer-context sidecar (which findings shaped which slots)

### Downstream:
- Google Ads Editor import
- Account upload via UI or API

---

## Output Location

All files are created relative to the **current working directory**:
- Output directory: `created/rsas/`
- Creates directory if it doesn't exist
- Each run creates a new timestamped file (never overwrites)
