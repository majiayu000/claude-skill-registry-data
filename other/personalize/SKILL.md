---
name: personalize
description: Customize this workspace to your role, company, and tools - quick (3 min) or deep (10 min)
argument-hint: "[quick | deep]"
---

# Personalize Your Workspace

You help the user customize the AI PM Workspace template to their specific role, company, and tools. Two tiers:

- **Quick start** (default, target 3 min): name, role, one free-text paragraph. Fills `CLAUDE.md` identity. Ships working skills immediately.
- **Deep personalization** (target 10 min): full flow with MCP detection, initiatives/projects setup, and people profiles. Suggested after the user has completed the first `/guide` module or sees a first win with the shipped skills.

## Mode selection

Check `$ARGUMENTS`:
- `quick` (or no argument): quick start
- `deep`: deep personalization

If the user invokes without arguments on a repo that already has filled identity (i.e., `CLAUDE.md` no longer contains `[YOUR NAME]`), ask once: "You already ran quick personalize. Run deep personalization now?"

---

## Quick start (target 3 minutes)

### Phase 1: One AskUserQuestion (3 questions)

```
Welcome. Two minutes and you're running.
```

**Questions:**

1. **Role**: "What's your role?"
   - Options: "Product Manager", "Senior / Group PM", "Head of Product", "Designer", "Other role (free text)"

2. **Team interactions**: "Who do you typically communicate with?" (multiSelect)
   - Options: "Engineering", "Design", "Leadership", "Customers / External"

3. **Note-taking language**: "What language do you write notes in?"
   - Options: "English only", "Mixed (English work + another language for personal notes)"

### Phase 2: One free-text prompt

```
Now the specifics - in one short answer, tell me:

1. Your full name
2. Your company (name, and what it does in one sentence)
3. Your focus area (part of the product you own, e.g., "Payments", "Developer Tools", "Core Platform")

That's it. Example: "Jordan Kim. Stripe, payments infrastructure. I own the subscription billing area."
```

Parse the answer into: name, company, company description, focus area.

**If "Mixed" was chosen in Phase 1**, also ask: "Which language for personal notes? (e.g., German, Spanish, French)"

### Phase 3: Apply

Update `CLAUDE.md`:
- `[YOUR NAME]` -> user's name
- `[YOUR ROLE]` -> from Phase 1 question 1
- `[YOUR COMPANY]` -> from Phase 2 parse
- `[YOUR PRODUCT AREAS]` -> from Phase 2 parse
- Company context section -> populated from Phase 2 description (one paragraph)
- Communication tone guidance -> keep only audience types selected in Phase 1 question 2
- Language section -> update if "Mixed" was selected

Add a note in the `CLAUDE.md` skill dispatch area that `/personalize --deep` is available for richer setup.

Initialize `Dashboard/Weekly P-Tasks.md` with the current week header (if empty).

### Phase 4: Summary

Structure the summary so `/guide` is the headline recommendation (with a short explanation), direct skills come next as alternatives, and `/personalize --deep` is mentioned last as an optional richer setup.

```
Workspace personalized (quick).

Filled CLAUDE.md identity:
- Name: [name]
- Role: [role]
- Company: [company]
- Focus: [focus area]

Recommended first step:

  /guide

An 8-module interactive learning path through the shipped skills, adapted to your role. It walks you through daily skills (/today, /meeting, /decision), weekly planning, and the craft skills (epics, user journeys, competitive research, opportunity-solution trees) using the sample data in samples/. About 5 minutes per module, you can stop and resume anytime with /guide next.

Or jump straight into a skill:

1. /today                       plan your day
2. /meeting                     process a meeting transcript
3. /decision                    document a product decision
4. /weekly-plan                 weekly priorities (best Monday/Friday)
5. /communicate                 draft a Slack, email, or async update
6. /create-epic                 turn an idea into an epic draft
7. /opportunity-solution-tree   structure discovery with Teresa Torres' OST
8. /competitive-research        sourced competitive matrix on a topic

For a richer setup (MCP detection, initiatives, people profiles):

  /personalize --deep
```

---

## Deep personalization (target 10 minutes)

### Phase 1: Identity deep dive (free text)

Prompt:
```
Tell me more:

1. Your full name
2. Your role and seniority (e.g., "Senior PM, 5 years at current company")
3. Your company - name, one-sentence description, target customers
4. Your focus area - what part of the product you own, key features or surfaces
5. Your main users - who actually uses your product day-to-day
```

### Phase 2: MCP detection (no user questions)

Check which MCP servers are available in the current Claude Code environment by reading the tool list:

- **GitHub MCP** (`mcp__github__*` tools present) -> note as available
- **Any documentation MCP** (`mcp__*-docs__*` tools) -> note as available
- **Notion / Linear / Jira** -> note if present
- Any other MCPs -> list them

Present:

```
MCP servers I can see:
- Connected: GitHub MCP, [other detected MCPs]
- Missing but potentially useful: [suggestions]

Want to set up any missing ones now? (Optional - you can skip and add later)
```

If the user wants to set one up, provide the `claude mcp add ...` command and ask them to restart Claude Code.

### Phase 3: Initiatives / projects

Ask:
```
List 1-3 active initiatives or projects you're currently driving.

For each: name, one-sentence description, rough status (discovery / in-development / validation / shipped).

Example:
- Subscription billing migration - moving legacy customers to new billing stack - in development
- Developer onboarding v2 - rework the first-run experience for new API users - discovery
```

For each initiative, create `Initiatives/[slug].md` (create the folder if missing) using `templates/initiative-template.md` if present, otherwise this minimal structure:

```markdown
---
tags: Initiative
status: [discovery | in-development | validation | shipped]
updated: YYYY-MM-DD
---

# [Initiative Name]

**One-line**: [Description]

## Status
[Current status, last updated]

## Why this matters
[Problem / opportunity, target outcome]

## Open questions
-

## Decisions made
-

## Open risks
-

## Related notes
-
```

### Phase 4: People profiles

Ask:
```
List 3-5 key people you work with regularly. For each: name, role, and how they prefer to communicate (brief/detailed, technical/strategic).
```

Write `Dashboard/people-profiles.md`:

```markdown
---
tags: Dashboard
updated: YYYY-MM-DD
---

# People Profiles

Communication preferences and working styles of key stakeholders.

## [Name]
- **Role**: [Role]
- **Communication style**: [brief description]
- **Preferred channel**: [Slack / email / async]
- **Tags**: #[FirstName]
```

### Phase 5: Apply all + summary

Update `CLAUDE.md` with:
- Full identity fields
- Company description and target users
- MCP section reflecting what was detected / configured
- Any initiative references in the skill dispatch table

Then:

```
Deep personalization complete.

Filled:
- CLAUDE.md (identity, company, MCP section)
[if initiatives] - Initiatives: N working files in Initiatives/
[if people] - People profiles: N profiles in Dashboard/people-profiles.md
[if mixed lang] - Language rules: [language] for personal, English for work

Recommended first step:

  /guide

An 8-module interactive learning path through the shipped skills, adapted to your role. Walks you through daily, weekly, and craft skills using the sample data in samples/. ~5 min per module, resume anytime with /guide next.

Or jump straight into a skill:

1. /today                       plan today
2. /meeting                     process a meeting
3. /decision                    document a decision
4. /create-epic                 draft an epic from an idea
5. /opportunity-solution-tree   structure discovery with an OST

Run /personalize --deep again anytime to refresh or add more context.
```

---

## Notes

- Quick start must feel fast. If the user gives brief answers, don't push for more.
- Deep mode should feel thorough but never bureaucratic. Skip any section the user pushes back on.
- Never ask about tools the user didn't bring up.
- Never create Todoist config - this template is Todoist-free. If the user mentions wanting Todoist sync, point them to `docs/todoist-sync.md` (optional extension, not shipped by default).
- If `Initiatives/` or `Dashboard/people-profiles.md` already exist and have content, append rather than overwrite.
