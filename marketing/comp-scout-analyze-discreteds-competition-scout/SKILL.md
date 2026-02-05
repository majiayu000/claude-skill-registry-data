---
name: comp-scout-analyze
description: Generate strategic analysis for competition entries and auto-persist to GitHub issue. Identifies winning tone, themes, and angles based on sponsor type and brand voice.
---

# Competition Strategy Analyzer

Generate strategic analysis for "25 words or less" competition entries and **automatically add to GitHub issue**.

## Execution Modes

| Mode | Behavior |
|------|----------|
| **Interactive** (default) | Ask clarifying questions about brand voice, tone preferences |
| **Unattended** | Use defaults based on sponsor category, no prompts |

The `comp-scout-daily` workflow always invokes this skill in **unattended mode**.

### Interactive Mode

When run interactively, this skill may ask:
- "What tone would you prefer? (sincere/humorous/mix)"
- "Any specific themes you want to emphasize?"
- "Should we focus on any particular angle?"

### Unattended Mode

When invoked with `--unattended` or by `comp-scout-daily`:
- Uses sponsor category to determine default tone
- Generates standard set of 5 angle ideas
- No user prompts - runs end-to-end automatically

## What This Skill Does

1. Analyzes the competition's brand, sponsor type, and prompt
2. Determines winning tone and approach
3. Generates angle ideas and themes
4. **Auto-persists strategy as comment on the competition's GitHub issue**

**No manual "please save to issue" step required.**

## Input

Competition data (from GitHub issue or `comp-scout-scrape`):
- url, title, brand
- prize_summary, prize_value
- prompt, word_limit
- closing_date
- **issue_number** (for auto-persist)

Optional flags:
- `--unattended` - Skip all interactive prompts, use defaults

## Workflow

### Step 1: Identify Sponsor Category

Classify the brand/sponsor into one of these categories:

| Category | Examples | Indicators |
|----------|----------|------------|
| **Wellness/luxury** | Spas, skincare, premium travel, health retreats | Premium language, self-care themes, aspirational imagery |
| **Tech/gaming** | Electronics, gaming, apps, software | Features, specs, community, innovation |
| **Food/beverage** | Grocery, restaurants, drinks, snacks | Sensory language, recipes, family moments, occasions |
| **Travel** | Airlines, hotels, destinations, experiences | Adventure, discovery, escape, bucket-list |
| **Retail/general** | Department stores, homewares, fashion | Lifestyle, value, everyday convenience |
| **Rural/agricultural** | Farm supplies, outdoor equipment, regional brands | Practical language, weather, land, hard work |

### Step 2: Determine Winning Tone

Based on sponsor category, identify the likely winning tone:

| Sponsor Type | Likely Winning Tone |
|--------------|---------------------|
| Wellness/luxury | Sincere, aspirational, emotional honesty. Judges want to feel you genuinely need/deserve this. |
| Tech/gaming | Knowledgeable enthusiasm, self-aware humour. Show you understand the product without being a fanboy. |
| Food/beverage | Relatable moments, sensory details. Specific tastes, smells, family traditions. |
| Travel | Discovery, bucket-list energy, specific memories. What makes this destination special to YOU? |
| Retail/general | Personality, memorability, genuine need. Stand out from generic "I'd love to win" entries. |
| Rural/agricultural | Practical, financially savvy, honest about habits. Down-to-earth authenticity wins. |

### Step 3: Assess Brand Voice

Analyze how the brand communicates:

**Questions to answer:**
- Is the brand formal or casual?
- Do they use humour or stay serious?
- What values do they emphasize? (family, adventure, quality, value, sustainability)
- What language patterns appear in their marketing?
- Who is their target audience?

**Output example:**
> "Casual and friendly, emphasizes family moments and everyday joy. Uses warm, approachable language. Target audience is parents/families."

### Step 4: Analyze the Prompt

Break down what the prompt is really asking:

**Questions to answer:**
- What's the surface-level question?
- What's the emotional response they're hoping for?
- What generic answers will judges see hundreds of times?
- What would make an entry memorable?

**Example:**
> Prompt: "Tell us in 25 words or less why you love our coffee"
>
> Surface: Why do you like coffee?
> Real ask: What specific, personal moment makes our coffee special?
> Generic answers: "I love the taste", "It wakes me up", "Best coffee ever"
> Memorable: Specific sensory detail, unexpected moment, personal ritual

### Step 5: Generate Angle Ideas

Create 3-5 distinct approaches, each with:
- Different emotional hook
- Different arc structure (sincere, comedic, self-deprecating, list-pivot)
- Brief description of the strategy

**Format:**
```
1. **Sincere - The morning ritual**
   Focus on a specific moment when the product is part of your routine.
   Arc: Honest admission → Sensory detail → Warm landing

2. **Self-deprecating - The confession**
   Admit to a relatable "flaw" that the product addresses.
   Arc: Confession → Constraint → Resolution

3. **Comedic - The unexpected angle**
   Find an unusual perspective that subverts expectations.
   Arc: Setup → Pivot → Callback

4. **Sensory - The specific detail**
   Zero in on one vivid sensory moment.
   Arc: Scene-setting → Sensory detail → Emotional resonance

5. **List-pivot - The credentials**
   Quick list establishing context, then pivot to the real point.
   Arc: List → Gap → Aspiration
```

### Step 6: Identify What to Avoid

Common pitfalls for this type of competition:

**Always avoid:**
- Generic superlatives ("amazing", "best ever", "fantastic")
- Begging or desperation ("please pick me", "I really need this")
- Lies or fabricated stories
- Clichés the judges will see hundreds of times
- Empty enthusiasm without specificity

**Category-specific pitfalls:**

| Category | Avoid |
|----------|-------|
| Wellness/luxury | Sounding entitled, over-the-top drama |
| Tech/gaming | Being too technical, gatekeeping |
| Food/beverage | Generic taste descriptions, "yummy" |
| Travel | Bucket-list clichés, generic wanderlust |
| Retail/general | "I want free stuff" energy |
| Rural/agricultural | City-slicker posturing, romanticism |

### Step 7: Auto-Persist to GitHub Issue

Add strategy as a comment on the competition's issue:

```bash
gh issue comment $ISSUE_NUMBER -R "$TARGET_REPO" --body "$(cat <<'EOF'
## Strategy Analysis

**Sponsor Category:** {sponsor_category}
**Brand Voice:** {brand_voice}
**Recommended Tone:** {recommended_tone}

### Approach
{approach}

### Themes to Use
{themes_list}

### Angle Ideas
{angle_ideas_list}

### Avoid
{avoid_list}

---
*Generated: {date}*
EOF
)"
```

### Step 8: Report Completion

```
✅ Strategy analysis complete and saved to issue #42!

**Summary:**
- Sponsor Category: Food/beverage
- Recommended Tone: Relatable with sensory details
- Generated 5 angle ideas

(In interactive mode: "Ready to compose entries?")
```

## Output Format

```yaml
strategy:
  competition_url: "https://..."
  issue_number: 42
  brand: "Example Brand"
  brand_voice: "Casual and friendly, emphasizes family moments"
  sponsor_category: "food/beverage"
  recommended_tone: "Relatable with sensory details, warm and specific"
  approach: |
    Focus on a specific moment when the product is part of your life.
    Avoid generic taste descriptions - instead, anchor to a memory,
    ritual, or unexpected moment. The best entries will make judges
    nod in recognition.
  themes_to_use:
    - "Family traditions"
    - "Sensory memories"
    - "Everyday rituals"
    - "Unexpected moments"
  words_to_consider:
    - "ritual"
    - "moment"
    - "discover"
    - "finally"
  angle_ideas:
    - "Sincere: The Sunday morning ritual that wouldn't be complete without it"
    - "Self-deprecating: Confessing to hiding the good stuff from the family"
    - "Sensory: The specific smell that triggers childhood memories"
    - "Comedic: The unexpected place/time you've enjoyed the product"
    - "List-pivot: All the things you've tried, but this is the one that stuck"
  avoid:
    - "I love [brand]"
    - "Best [product] ever"
    - "Please pick me"
    - "My family would love this"
    - "Delicious" / "Yummy" / "Amazing"
```

## Example Session

```
User: Analyze issue #42 for strategy

Claude: I'll analyze this competition and save the strategy to the issue.

[Reads issue #42 details]

Competition: Win a Year's Supply of Coffee (Nespresso)
Prompt: "Complete this sentence in 25 words or less: My morning coffee..."

## Strategy Analysis: Nespresso Competition

**Sponsor Category:** Food/beverage (premium)

**Brand Voice:** Sophisticated but accessible. Nespresso positions itself as
everyday luxury - not pretentious, but elevated. George Clooney campaigns
suggest self-aware humour is welcome.

**Recommended Tone:** Sensory and specific, with room for subtle wit.
The "morning coffee" framing invites ritual/routine angles.

**What they're really asking:** What specific, personal moment makes your
morning coffee ritual special?

**Themes to use:**
- Morning rituals and routines
- Sensory details (aroma, warmth, first sip)
- The pause before chaos begins
- Small luxuries

**Angle ideas:**

1. **The Pause** - Focus on the quiet moment before the day begins
2. **Sensory Detail** - Zero in on one specific sensation
3. **Self-Deprecating** - Admit to needing it more than you'd like
4. **The Ritual** - Describe the specific routine
5. **Unexpected Angle** - Subvert the "morning" framing

**Avoid:**
- "I need coffee to function" (overdone)
- "Best coffee ever" (generic)
- "I'm not a morning person" (cliché)

[Runs: gh issue comment 42 --body "..."]

✅ Strategy saved to issue #42!
```

**Note:** When run in unattended mode (via comp-scout-daily), do NOT ask "Ready to compose entries?" - the workflow will automatically invoke compose next.

## Unattended Mode Details

When running in unattended mode (e.g., via `comp-scout-daily`), the skill:

1. **Skips all user prompts** - No tone preference questions
2. **Uses default tone mapping** - Based on sponsor category (see Step 2)
3. **Generates standard angles** - Always produces 5 angle ideas
4. **Auto-persists immediately** - No confirmation needed

### Default Tone Mapping (Unattended)

| Sponsor Category | Default Tone |
|------------------|--------------|
| Wellness/luxury | Sincere, aspirational |
| Tech/gaming | Knowledgeable, self-aware humor |
| Food/beverage | Relatable, sensory |
| Travel | Discovery, bucket-list |
| Retail/general | Personality, memorable |
| Rural/agricultural | Practical, honest |

### Invocation by comp-scout-daily

The daily workflow invokes this skill as:

```
For each new competition issue:
  1. Read issue details
  2. Run comp-scout-analyze with --unattended
  3. Strategy is auto-persisted as comment
  4. Proceed to comp-scout-compose
```

## Integration

This skill:
- Reads competition data from GitHub issues
- Auto-saves strategy as comment
- Outputs strategy for `comp-scout-compose` to use
- Can be invoked by `comp-scout-daily` in unattended mode
