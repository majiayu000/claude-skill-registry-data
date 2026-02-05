---
name: weekly-snippets
description: Interactive weekly snippets builder for gathering and drafting Friday-Thursday accomplishment summaries. Use when creating weekly snippets, status updates, or accomplishment tracking. Covers context-file creation, source-by-source gathering (Weekly Notes, GitHub PRs/issues, Meeting Notes), section ordering (Ships, Risks, Blockers, Ideas, Collaborations, Shoutouts), business-impact-first writing, and link formatting rules.
---

# Weekly Snippets Builder

Reusable workflow for creating Friday–Thursday accomplishment summaries with proper formatting, business impact focus, and structured gathering process.

## Core Principles

- **Interactive process**: Ask for confirmation at each data-gathering step
- **Append-only context file**: Build incrementally without editing prior sections
- **Business impact first**: Lead Ships bullets with organizational value, not just technical details
- **Strict date range**: Friday–Thursday only; filter out work from other periods
- **Link format**: Always use `[repo#number](URL)` inline format, never footnotes

## Related Skills

**Use `brain-operating-system` skill** for:
- Directory structure and naming conventions (`Daily Projects/`, `Snippets/`, `Weekly Notes/`)
- Append-only workflow patterns and when to archive
- Wikilink format and file organization rules

**Use `github-interaction` skill** for:
- Fetching PRs, issues, and discussions with proper filters
- Comment and review retrieval using MCP tools
- Date-range queries and pagination handling

**Use `voice-and-tone` skill** for:
- Ships bullets (business impact first, metrics framing)
- Collaborations style (natural integration of @mentions, how you collaborated)
- Crediting patterns and showing human impact

## Workflow Overview

1. Create context file in `Daily Projects/YYYY-MM-DD/snippets-context-YYYY-MM-DD-to-YYYY-MM-DD.txt`
2. Reference 2-3 recent snippets for formatting/tone
3. Confirm Friday–Thursday date range
4. Gather sources with user approval:
   - Weekly Notes → Meeting Notes
   - GitHub PRs/issues (authored + reviewed)
   - Project updates from Daily Projects
5. Build section candidates (Ships → Risks → Blockers → Ideas → Collaborations → Shoutouts)
6. Draft final snippets Markdown

## Date Range Rules

**Strict Friday–Thursday enforcement**:
- All work must fall within the specified week
- Use GitHub date filters: `created:YYYY-MM-DD..YYYY-MM-DD`
- Only include meetings with dates in range
- Filter Weekly Notes to target week only

## Context File Management

**Location**: `Daily Projects/YYYY-MM-DD/snippets-context-YYYY-MM-DD-to-YYYY-MM-DD.txt`

**Append-only**: Add each source's findings to the end. Each entry includes source type, summary, and user clarifications.

## Source Gathering (With Confirmation Gates)

### 1. Weekly Notes
- Ask: "Should I pull Weekly Notes for this period?"
- If yes: Summarize goals, todos, linked meetings, progress logs
- Show list of linked meeting notes
- Append summary to context file
- **Wait for confirmation** before continuing

### 2. Meeting Notes
- Ask for each meeting: "Want to pull details from this meeting?"
- **Read first 100 lines maximum** (newest entries first)
- Extract: transcript/summary links (dated within window)
- Classify collaboration type:
  - Pairing on implementation (coding together)
  - Pairing on design/concepts (planning together)
  - Review/feedback (one builds, other reviews)
  - Strategic planning (leadership/direction)
- For breakthroughs: **identify who figured out what solution**
- Present candidate takeaways
- Append to context file
- **Wait for confirmation** before next meeting

### 3. GitHub Contributions

**Use GitHub MCP tools** for all PR/issue comment data (standard API will fail).

**Traditional Search**:
- Ask: "Pull PRs you authored/merged in date range?"
- **Filter to merged/closed PRs only** for Ships (open/draft → Ideas)
- Ask: "Pull issues/discussions where you contributed?"
- **Filter to closed/completed issues** for Ships
- Show candidates with links
- Append to context file
- **Wait for confirmation**

**Copilot-Authored Work**:
- Ask: "Review PRs where you were requested as reviewer?" (check for Copilot-authored)
- Ask: "Check issues/PRs assigned to you?" (check for Copilot-authored)
- Fetch comments/reviews to show your involvement
- Present collaboration candidates
- Append to context file
- **Wait for confirmation**

### 4. Project Updates
- Ask: "Check Daily Projects and Projects folders for recent notes?"
- Scan modified files in date range
- Present relevant project work not captured elsewhere
- Append to context file
- **Wait for confirmation**

## Section Building (Step Through Each)

**Before starting**: Check 2-3 recent `Snippets/*.md` files for current formatting/tone preferences.

**Process each section in order**: Ships → Risks → Blockers → Ideas → Collaborations → Shoutouts

For each section:
1. Use context file to suggest candidates
2. Present as concise bullets (one line each) with inline links `[repo#number](URL)`
3. Ask user to confirm, edit, discard
4. **Explicitly ask**: "Any others to add to this section?"
5. Repeat until user says no
6. Move to next section

### Ships Section Rules

**Every bullet MUST**:
- Lead with business impact (why it matters to GitHub/users/teams), then technical work
- **Only include completed work** (merged PRs, closed issues, published content)
- Include inline link where applicable

**Example**:
- ✅ "Reduced PSQ queue from 650k to 60k entries, giving analysts manageable work and boosting morale after layoffs—designed systematic cleanup with conservative retention [spamurai-next#5894](https://github.com/...)"
- ❌ "Cleaned up PSQ queue [spamurai-next#5894](https://github.com/...)"

### Collaborations Section Rules

- Integrate person names naturally (`@username`), describe collaboration type (pairing, review, planning)
- Verify attribution for technical solutions
- No bold prefixes like "@person:"

**Example**:
- ✅ "Paired with @yoodan on kafka consumer monitoring concepts for hamzo, exploring signal detection patterns"
- ❌ "@yoodan: worked on monitoring for hamzo"

### Shoutouts Section Rules

- Include celebratory emojis (🎉🚀💪🤖🔧), focus on recognizing others
- Verify attribution for breakthroughs, connect to specific accomplishments

## Final Output Format

```markdown
## Ships
- [business impact first, technical details second] [link if applicable]

## Risks

## Blockers

## Ideas
- [open/draft PRs, explorations, experiments] [link]

## Collaborations
- [How you collaborated with @person on what] [link if applicable]

## Shoutouts
- 🎉 [Recognition for @person's contribution] [link if applicable]
```

**All sections use bullet lists**. No bold/italic formatting. Start bullets directly with content.

## Link Formatting

**Required format**: `[repo#number](URL)`

**Examples**:
- `[hamzo#4133](https://github.com/github/hamzo/pull/4133)`
- `[platform-health#8524](https://github.com/github/platform-health/pull/8524)`

**Never** use footnotes or plain text URLs.

## Collaboration Rules

- Must include someone other than @jonmagic or @copilot
- Talk about HOW you collaborated, not just what was accomplished
- Verify collaboration type from meeting notes when possible

## Final Steps

1. Assemble all confirmed sections into final Markdown
2. Ask user to review and approve
3. Once approved, save to `Snippets/YYYY-MM-DD-to-YYYY-MM-DD.md`
