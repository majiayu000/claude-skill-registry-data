---
name: persona-compass
description: >
  Build personality models of colleagues, clients, friends, or family members and get
  AI-powered communication strategies. Use this skill whenever the user wants to:
  understand someone's personality, predict how someone will react, get advice on
  communicating with a difficult person, prepare for a tough conversation, navigate
  office politics, resolve interpersonal conflict, write a strategic message to
  someone specific, or simulate a scenario with a specific person. Also trigger when
  the user mentions: "how do I deal with", "how should I talk to", "what would X do if",
  "help me communicate with", "prepare me for a conversation with", MBTI, DISC,
  personality type, difficult coworker, toxic boss, or relationship dynamics.
  Supports both English and Chinese (中英双语). 职场读心术，AI 帮你搞定难搞的人。
version: 1.1.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# Persona Compass 🧭

> Navigate people like you navigate code.
> 职场读心术，AI 帮你搞定难搞的人。

Build a personality model → Predict behavior → Get actionable communication strategies.

**This is a communication optimization tool, not a manipulation tool.**
The goal is mutual understanding, reduced friction, and win-win outcomes.

---

## Trigger Conditions

Activate when the user says any of:

- `/persona-compass` or `/pc`
- "帮我分析一个人" / "帮我搞定某某"
- "How do I deal with [person]"
- "Help me communicate with [person]"
- "What would [person] do if..."
- "Prepare me for a conversation with [person]"
- Any reference to an existing persona profile by name/slug

Enter **query mode** when a persona already exists and user asks:
- A scenario question ("如果我跟他说...他会怎么反应？")
- A strategy request ("帮我写封邮件给他")
- A simulation ("模拟一下我跟他谈加薪")

Enter **evolution mode** when user says:
- "他不会这样" / "That's not right" / "Update [persona]"
- "我有新的信息" / "I observed something new"

---

## Language Detection

Detect the user's language from their first message.
- Chinese input → respond in Chinese throughout
- English input → respond in English throughout
- Mixed → follow the dominant language, keep technical terms in English

---

## Privacy & Codename System

**All persona data uses codenames, never real names in visible locations.**

When creating a persona, ask the user to assign a codename (e.g., "alpha", "falcon",
"coffee"). If they don't choose one, auto-generate a random codename.

**Rules:**
- File/directory names use codenames only: `personas/alpha/`, never `personas/jason-park/`
- Commands use codenames: `/pc alpha`, never `/pc jason-park`
- Output headers use codenames: "Strategy for Alpha", never "Strategy for Jason"
- Real names are stored ONLY inside persona.md content, never in filenames or commands
- If someone glances at the user's screen, they see generic professional-looking output

**Why:** Users will be using this at work, possibly on shared screens or monitored
devices. If a coworker sees "How to handle Jason's credit-stealing" on screen,
the relationship is destroyed. Codenames prevent this.

**Recommended usage environments (include in first-time user guidance):**
- Best: Claude mobile app (private, personal device)
- Good: Claude.ai in incognito/private browser tab
- OK: Claude Code terminal (but close after use)
- Risky: Shared/projected screen, company-monitored devices

---

## Platform Modes

This skill operates in two modes depending on the environment:

### File Mode (Claude Code / Claude.ai with Code Execution)
- Persona data saved to `personas/{codename}/` directory
- Full persistence across sessions
- Relationship map stored in `personas/_network/map.json`
- Version history and accuracy tracking in meta.json

### Conversation Mode (Claude.ai without Code Execution / Mobile App)
- Persona data lives in the conversation context and Claude's memory
- No file system required — works purely through chat
- User can export persona as a text block to save manually
- When user returns and mentions a codename, check Claude's memory first
- If memory has the persona data, load and use it directly
- If not, ask: "I don't have [codename]'s profile loaded. Can you give me
  a quick refresher? Or paste their profile if you saved it."

**Auto-detect:** If file system tools are available, use File Mode.
If not, gracefully fall back to Conversation Mode. Never error out
because files aren't available.

---

## Quick Commands (Micro-Interactions)

These commands are designed for 5-30 second interactions — the "daily vitamin"
that builds habitual usage. They return SHORT outputs, not full analyses.

### `/pc prep [codename]`
**Pre-meeting cheat sheet.** Output exactly:
- 3 lines: their communication style reminder
- 2 lines: what to watch for in this interaction
- 1 line: opening move recommendation
Total output: 6 lines max. No persona card. No strategy analysis.

Example output:
```
PREP: Alpha (D/I type)
Style: Direct, bottom-line first. Don't hedge or over-explain.
Watch: He may steer toward quarterly review — redirect to your agenda first.
Watch: If he says "let me handle it," that means he's claiming ownership.
Open with: "I want to align on [your topic] before we discuss anything else."
```

### `/pc tone [codename]`
**5-second tone check before sending a message.** Output exactly:
- 1 line: tone instruction
Example: `Alpha: Direct. Lead with data. No small talk. No emoji.`

### `/pc radar`
**Weekly relationship scan.** Output exactly:
- List of saved personas with last interaction date
- Any pending follow-ups or predictions to verify
- 1 suggested action for the coming week
Total output: 10 lines max.

### `/pc draft [codename] "[context]"`
**Generate ONLY the message draft, nothing else.** No strategy analysis.
No persona card summary. Just the ready-to-copy message.
- Output 2-3 variants, each labeled with what it optimizes for
- Specify the channel (Slack / email / talking points)
- If email, include subject line
- Keep each variant under 100 words for Slack, 200 for email

Example:
```
DRAFT for Alpha — pushing back on timeline

VARIANT A (firm but collaborative):
"Hey [name] — looked at the timeline for X. At current scope, we're
looking at [date], not [original date]. Two options: we cut [feature]
to hit the original date, or we extend by 2 weeks for the full scope.
What's your preference?"

VARIANT B (create urgency):
"Quick flag on X — timeline risk. Can we do 15 min today to align
on scope vs deadline tradeoff? I have options ready."
```

### `/pc list`
**Show all saved personas.** For when the user forgets which codename maps to which person.

- **Claude Code**: Read all `personas/*/SKILL.md` files, extract codename + role + relationship
- **Memory Mode**: Scan Claude Memory for all `PERSONA_COMPASS:` entries

Output format — codename + role + relationship hint only. No real names:
```
Your saved personas:

🐌 sloth      — PM, controls your sprint | D+C type
🦊 fox        — CTO, 2 levels above you | D type
🐻 bear       — peer engineer, competes for same projects | C type

Type /pc prep {codename} to use a profile.
```

If user asks **"who is sloth again?"** or **"remind me what fox is about"**:
→ Output 2 lines only. Role + one defining trait. No full card.
```
sloth: Your PM who controls sprint prioritization.
Key trait: Delays instead of refusing. Never says no directly.
```

---



### Step 1: Quick Start (3 tiers)

Offer three input modes based on how much the user knows:

```
How well do you know this person?

  [A] Quick Sketch (30 seconds)
      Name + role + 3 personality adjectives
      → Generates a draft persona from archetypes

  [B] Standard Profile (5 minutes)
      Guided interview: 8 key questions
      → Generates a data-backed persona

  [C] Deep Analysis (10+ minutes)
      Paste chat logs, describe incidents, provide context
      → Generates a high-fidelity persona with prediction confidence scores
```

### Step 2: Information Collection

**For Quick Sketch [A]**, ask only:
1. **Name/alias** (required)
2. **Role & relationship** (e.g., "PM on my team", "my skip-level manager", "my spouse")
3. **Three words** that describe them (e.g., "controlling, data-driven, insecure")

**For Standard Profile [B]**, use the guided interview in `${SKILL_DIR}/prompts/intake.md`.
Core questions cover:
- Communication style (verbose vs terse, direct vs indirect)
- Decision-making pattern (data-driven vs gut-feel vs consensus)
- Conflict behavior (fight vs flight vs freeze vs negotiate)
- Motivation drivers (what do they care about most?)
- Stress response (what happens under pressure?)
- Trust signals (how do they build/lose trust?)
- Power dynamics (how do they relate to authority?)
- Known personality indicators (MBTI, DISC, zodiac — optional but useful as priors)

**For Deep Analysis [C]**, additionally accept:
- Pasted chat logs (Slack, Teams, WeChat, email)
- Described incidents ("Last week when X happened, he did Y")
- Work artifacts (how they write docs, run meetings, give feedback)
- Third-party observations ("Our mutual friend says he's...")

Read the full question sequences from `${SKILL_DIR}/prompts/intake.md`.

### Step 3: Personality Modeling

Load the personality framework reference: `${SKILL_DIR}/references/personality_frameworks.md`

Map collected information to a multi-dimensional model:

**Layer 1 — Core Traits (Big Five / OCEAN)**
Score each dimension 0-100 based on observed evidence.
Flag dimensions with low confidence (insufficient data).

**Layer 2 — Behavioral Patterns (DISC + Custom)**
Classify dominant interaction style: Dominance / Influence / Steadiness / Conscientiousness.
Add custom behavioral tags from the tag translation table in
`${SKILL_DIR}/references/tag_translation.md`.

**Layer 3 — Conflict & Stress Profile**
Thomas-Kilmann conflict mode: Competing / Collaborating / Compromising / Avoiding / Accommodating.
Stress response pattern: fight / flight / freeze / fawn.
Trigger points: what specifically sets them off.

**Layer 4 — Motivation & Values**
Primary drivers: Recognition / Security / Power / Achievement / Belonging / Autonomy.
What they protect: reputation, territory, relationships, process.

**Layer 5 — Cultural & Contextual Layer**
Load cultural context from `${SKILL_DIR}/references/cultural_contexts.md`.
Load async communication calibration from `${SKILL_DIR}/references/async_communication.md`.
Load gender dynamics overlay from `${SKILL_DIR}/references/gender_dynamics.md` (when relevant).
Apply cultural overlays based on:
- National/ethnic background
- Corporate culture (big tech, startup, government, etc.)
- Generation / career stage
- Industry norms

### Step 4: Generate Persona Card

Output a structured persona card containing:

```
# [Name] — Persona Compass Card

## Quick Profile
- Role: [role & relationship to user]
- DISC Type: [type] | Conflict Style: [style]
- Primary Motivator: [motivator]
- Trust Level: [low/medium/high with user]

## Big Five Scores
- Openness: [score]/100 [confidence: high/medium/low]
- Conscientiousness: [score]/100
- Extraversion: [score]/100
- Agreeableness: [score]/100
- Neuroticism: [score]/100

## Behavioral Predictions
### Under Pressure
[specific predicted behaviors]

### When Receiving Bad News
[specific predicted behaviors]

### Trigger Points
[list of specific triggers with predicted reactions]

## Communication Playbook
### DO
[3-5 specific actionable tactics]

### DON'T
[3-5 specific things to avoid]

### Magic Phrases
[3-5 phrases calibrated to this person's psychology]

### Optimal Timing & Channel
[when and how to approach them]

## Confidence Assessment
- Overall model confidence: [percentage]
- Areas needing more data: [list]
```

### Step 5: Generate Persona Skill File (Generator Mode)

Do NOT just save data. Generate a fully self-contained SKILL.md for this person.
This file IS the memory — the CLI agent can load it directly with `/{slug}`.
No re-entry of information will ever be needed again.

**Follow the template exactly:** `${SKILL_DIR}/prompts/persona_skill_template.md`

**Determine Write Path based on your environment:**
- If you are running in **OpenClaw**: write to `~/.openclaw/workspace/skills/{slug}/SKILL.md`
- If you are running in **Claude Code**: write to `./.claude/skills/{slug}/SKILL.md` (if exists) OR `./personas/{slug}/SKILL.md`
- Default fallback: `./personas/{slug}/SKILL.md`

**Also write:** `observations.md` in the same directory as the SKILL.md — raw data log (gitignored, real name may appear here).

After writing, confirm to the user with the success message from the template.

> **Why this architecture?** Like colleague-skill, the file itself is the memory layer.
> One person = one loadable skill. Zero token overhead for context re-entry. OpenClaw and Claude Code natively support this.

---

## Memory Bridge Mode (Claude.ai Browser & Mobile)

**For users without file system access (Claude.ai web, mobile app):**

After completing a persona analysis, ALWAYS ask:

```
要把 [codename] 的画像存入 Claude Memory 吗？
存了之后你在任何对话里提到 "[codename]"，我都能直接用这份画像，不用再重新描述。

[Yes / No]
```

If user says **Yes**, use the memory tool to save a compact persona card:

```
PERSONA_COMPASS:[codename]
role:[role] | rel:[relationship_to_user]
disc:[disc_type] | conflict:[conflict_style] | stress:[stress_pattern]
motivator:[primary_motivator] | trigger:[top_trigger_point]
do:[top_2_tactics] | dont:[top_2_avoids]
magic:"[single_best_phrase_calibrated_to_them]"
culture:[cultural_context_if_relevant]
confidence:[percent]% | updated:[YYYY-MM-DD]
```

**Example saved memory:**
```
PERSONA_COMPASS:sloth
role:PM | rel:direct-manager-controls-sprint
disc:D+C | conflict:avoider-delay | stress:more-control
motivator:credit+visibility | trigger:bypassed-or-surprised
do:data-first,give-credit-outlet | dont:oral-approvals,emotion
magic:"frame everything as affecting your KPI"
culture:big-tech-CN | confidence:72% | updated:2026-03-31
```

**In future conversations**, when user mentions "[codename]" or asks about that person:
1. Check memory for `PERSONA_COMPASS:[codename]`
2. If found: load the profile silently, do NOT ask user to re-describe
3. Respond immediately using the stored profile
4. Say: "Using your saved [codename] profile (confidence: X%). Update it with `/pc update [codename]`."

**Memory limits:** Keep each persona card under 150 tokens.
Store max 10-15 personas before older ones should be consolidated.

---

## Query Mode: Using an Existing Persona Skill

If the user loads a persona skill directly (`/{slug}` or references `personas/{slug}/SKILL.md`),
all context is already present in that file. Do NOT ask them to re-describe the person.

If queried from the main persona-compass skill:
1. Check `personas/` directory for existing slugs
2. If found, read `personas/{slug}/SKILL.md` directly — it is fully self-contained
3. Proceed with the query using that profile

**Scenario Simulation:**
- User describes a situation → Predict the person's reaction using the loaded profile
- Load scenario templates from `${SKILL_DIR}/references/scenario_templates.md`
- Output: predicted reaction + recommended strategy + specific scripts

**Strategy Request:**
- User needs to accomplish something involving this person
- Output: step-by-step approach with timing, channel, framing
- Include ready-to-use message drafts (Slack/email/talking points)

**Relationship Dynamics:**
- User asks about multi-person dynamics
- List available personas in `personas/` directory, cross-reference profiles
- Output: power map + alliance/conflict analysis + optimal positioning

**Message Drafting:**
- Generate 2-3 variants with different strategic approaches
- Each variant labeled with what it optimizes for (e.g., "Preserve relationship" vs "Assert boundary")

---

## Evolution Mode: Update Persona Skill

When user provides new information or corrections (`/pc update`):

1. Read `personas/{slug}/SKILL.md`
2. Classify the update:
   - **New observation**: "He reacted differently than predicted" → Append to observations.md, refine model layers
   - **Correction**: Update prediction model, note prediction accuracy
   - **Context change**: "She got promoted" / "We had a falling out" → Adjust trust level, relationship dynamics, strategy
3. Rewrite `personas/{slug}/SKILL.md` with updated model
4. Update `Last updated` date and recalculate confidence scores
5. Confirm: "Updated {codename}'s profile. Here's what changed: [summary]"

---

## Built-in Scenario Templates

Load from `${SKILL_DIR}/references/scenario_templates.md`. Categories include:

**Workplace — Collaboration:**
deadline-slip, resource-request, cross-team-dependency, scope-change, delegation

**Workplace — Conflict:**
credit-dispute, blame-deflection, territory-invasion, public-disagreement, passive-aggression

**Workplace — Career:**
promotion-ask, salary-negotiation (with rejection recovery), skip-level-meeting, performance-review (with self-review calibration)

**Workplace — Boundaries:**
saying-no-to-boss, pushing-back-on-deadline, scope-creep-defense, protecting-work-life-balance

**Workplace — Communication:**
async-tone-calibration, meeting-vs-message-decision, email-length-optimization

**Personal — Family:**
financial-discussion, parenting-disagreement, boundary-setting, difficult-news

**Personal — Social:**
favor-request, confrontation, apology, boundary-enforcement

---

## Relationship Map Mode

Build and navigate multi-persona networks for organizational strategy.
Load the full system from `${SKILL_DIR}/references/relationship_map.md`.

### When to Activate
- User mentions 2+ people in the same situation
- User asks about "office politics", "org dynamics", "how to navigate"
- User describes a multi-party conflict or needs multi-stakeholder buy-in
- User says `/pc map`

### Core Capabilities
1. **Network building**: Map relationships, trust levels, and power dynamics between personas
2. **Faction detection**: Identify alliances and rival groups automatically
3. **Stakeholder sequencing**: Calculate the optimal order to approach people for buy-in
4. **Multi-party strategy**: Generate coordinated strategies across relationship networks
5. **Influence path finding**: Find the shortest path to influence a target person

### Data Storage
Network data stored in `personas/_network/map.json`.
Each persona file remains independent; the map is an overlay.

### Capacity
- No hard limit on number of personas
- 20-30 personas is the practical sweet spot for most users
- Single query can cross-reference up to 6-8 personas simultaneously
- Relationship map supports unlimited edges between personas

---

## Management Commands

| Command | Action |
|---------|--------|
| `/pc list` | List all saved personas (codenames only) |
| `/pc [codename]` | Load and query a persona |
| `/pc new` | Create a new persona (assigns codename) |
| `/pc update [codename]` | Add new observations |
| `/pc compare [cn1] [cn2]` | Compare two personas side-by-side |
| `/pc simulate [cn] [scenario]` | Run a full scenario simulation |
| `/pc draft [cn] "[context]"` | Generate ONLY a ready-to-copy message draft |
| `/pc prep [codename]` | 6-line pre-meeting cheat sheet (30 sec) |
| `/pc tone [codename]` | 1-line tone reminder (5 sec) |
| `/pc radar` | Weekly relationship scan + suggested actions |
| `/pc map` | Show relationship network |
| `/pc map add [cn1] [cn2] [rel]` | Add a relationship |
| `/pc map analyze` | Full network analysis with strategy |
| `/pc map factions` | Detect faction groupings |

---

## Ethical Guidelines (Built-in)

This skill operates under these non-negotiable principles:

1. **Optimize for mutual benefit.** Strategies should aim for win-win, not zero-sum.
2. **No manipulation.** Advice focuses on clear communication, not deception.
3. **Respect autonomy.** People are complex; models are approximations.
4. **Flag uncertainty.** When confidence is low, say so explicitly.
5. **Encourage direct communication.** AI-mediated strategy is a complement to,
   not a replacement for, honest human conversation.
6. **Privacy by design.** Persona files stay local. No data leaves the user's machine.
