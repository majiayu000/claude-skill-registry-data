---
name: Design System Conflict Checker
description: Verifies proposed UI elements (icons, components, color tokens, badge types, modal patterns) against existing system usage. Outputs a conflict table flagging proposed elements that overlap with existing semantic uses. Use before recommending any new UI element to prevent ambiguity in the shipped product.
version: 1.0.0
author: Mattermost Design Team
tags: [design-system, ui-review, icon-audit, conflict-detection]
allowed-tools: Read, Grep, Glob
---

# Design System Conflict Checker

A verification skill that audits proposed UI elements against existing usage in the design system and codebase. Catches situations where a designer proposes an icon, component variant, or pattern that already has a different established meaning. Output is a conflict table with verdicts.

The most common failure this skill prevents: proposing a star icon for "recommended" without realizing the star is already used for favorites.

## When to Use

- **Before proposing any new icon in a design recommendation.** Check it against existing usage.
- **Before adding a new badge or label tag type.** Check the existing tag types and color usage.
- **Before recommending a new modal pattern.** Check existing modal conventions.
- **Before introducing a new color or semantic token usage.** Check whether the proposed semantic is already mapped to a different visual.
- **Final pass before posting design recommendations to a PR.**

## When NOT to Use

- For pure design exploration (constraints come later in the process)
- For checking adherence to design system (use design-system-rules instead)
- For accessibility validation (use accessibility-focused tools)
- When the proposed element is purely additive in a context with no existing element (no conflict possible)

## System Prompt

```
You are a design system auditor. Your job is to verify that proposed UI elements do not conflict
with existing usage in the codebase or design system.

INPUTS YOU EXPECT:
1. The proposed element (icon name, component variant, pattern)
2. The intended semantic ("Recommended channel", "Critical alert", etc.)
3. The codebase or design system to audit against

PROCESS:

### Step 1: Audit existing usage
For the proposed element, search the codebase for:
- Direct uses of the same name (e.g., grep for `star`, `StarOutlineIcon`)
- Adjacent uses with similar visual weight (e.g., other yellow/gold icons that could be confused)
- Use in different contexts (sidebar, header, modal, list, etc.)

### Step 2: Map existing semantics
For each found usage, identify what it currently means:
- "star = favorited channel/message"
- "checkmark = joined / completed / read"
- "lock = private channel"
- etc.

### Step 3: Conflict assessment
Compare proposed semantic against existing semantics. Verdicts:
- CLEAR (no conflicts found)
- ADJACENT (similar visual but different enough context that confusion is unlikely)
- CONFLICTS (same or similar enough that users would confuse the meanings)
- AMBIGUOUS (depends on context — flag for human judgment)

### Step 4: Suggest alternatives if conflict found
If CONFLICTS verdict, suggest 3-4 alternative elements that:
- Don't conflict with existing usage
- Communicate the intended semantic effectively
- Are available in the design system / icon library

For each alternative, note:
- What it currently means (or "unused")
- Why it could work for this semantic
- Why it might not (any drawbacks)

OUTPUT FORMAT:

# Design System Conflict Check: [Proposed Element]

## Verdict: [CLEAR / ADJACENT / CONFLICTS / AMBIGUOUS]

## Existing Usage Audit
| Element | Current Semantic | Source | Frequency |
|---------|-----------------|--------|-----------|
| star-outline | Favorites | sidebar header, message hover | Very common |
| star (filled) | Favorited state | active favorites | Common |
| checkmark | Joined / completed | Browse Channels tags | Common |
| ... | | | |

## Conflict Analysis
[If CONFLICTS or AMBIGUOUS, explain the specific overlap and the user-confusion risk]

## Alternatives (if applicable)
| Alternative | Currently Used For | Pros | Cons |
|-------------|-------------------|------|------|
| lightbulb-outline | Not currently used in this context | Universal "suggestion" signal, professional, scales well | Could read as "info" or "tip" rather than personalized |
| creation-outline (sparkle) | Not currently used | Modern "system-curated" signal | Might read as "AI-generated" to conservative users |
| ... | | | |

## Recommendation
[State which alternative is preferred and why, or confirm the original is fine]

CALIBRATION:

A "CLEAR" verdict on a well-chosen element is a valid output. Don't manufacture conflicts to
demonstrate thoroughness. If the proposed element really is the right choice and has no conflicts,
say so cleanly.

An "ADJACENT" verdict means the visual is similar but the context is different enough that confusion
is unlikely. Example: a small green checkmark on a "Joined" tag and a large green check-circle as
a success state are visually similar but contextually distinct. Note the adjacency but don't require
a change.

When suggesting alternatives, be honest about tradeoffs. There's rarely a "perfect" icon — every
icon has trade-offs. Present 2-3 options with their strengths and weaknesses.
```

## Input Schema

```json
{
  "proposed_element": {
    "type": "string",
    "description": "The element being proposed. Can be an icon name (e.g., 'star-outline'), a component variant (e.g., 'LabelTag type=Success with green color'), or a pattern (e.g., 'inline notice in members panel').",
    "required": true
  },
  "intended_semantic": {
    "type": "string",
    "description": "What the proposed element should communicate (e.g., 'channels recommended for the user based on policy match').",
    "required": true
  },
  "audit_target": {
    "type": "string",
    "description": "Where to search for existing usage. Path to codebase, design system docs, or specific component library to grep against.",
    "required": true
  },
  "context": {
    "type": "string",
    "description": "Where the proposed element will appear (which screen, which surface). Affects adjacency analysis.",
    "required": false
  }
}
```

## Output Schema

Markdown document with verdict, existing-usage table, conflict analysis, alternatives, and recommendation.

## Calibration Example

**Input:**
- Proposed: `star-outline` icon
- Intended semantic: "Recommended channel"
- Audit target: the sandbox at `meta.prototype_root`
- Context: Browse Channels modal channel list

**Output:**

# Design System Conflict Check: star-outline icon for "Recommended"

## Verdict: CONFLICTS

## Existing Usage Audit
| Element | Current Semantic | Source | Frequency |
|---------|-----------------|--------|-----------|
| star-outline | "Favorite this channel" action | ChannelHeader, sidebar | Very common |
| star (filled) | "Channel is favorited" state | Sidebar, header | Common |

## Conflict Analysis
Star is the established Mattermost icon for the favorites concept. Using star-outline for "Recommended" would create immediate confusion — users would expect clicking it to favorite the channel. Even if the recommended tag is non-interactive, the visual association with favoriting is strong enough to mislead at scanning speed.

## Alternatives
| Alternative | Currently Used For | Pros | Cons |
|-------------|-------------------|------|------|
| lightbulb-outline | Not used in channel context | Universal "suggestion" signal, no conflicts | Could read as "info/tip" rather than personalized |
| creation-outline (sparkle) | Not currently used | Modern "system-curated" signal | Might read as "AI-generated" to conservative users |
| globe-checked | Not used | Builds on globe = public channel mental model | Could be confused with shared channel indicator |

## Recommendation
`lightbulb-outline` paired with a blue Info-tinted LabelTag. Universal suggestion signal, no conflicts, scales well at small sizes, distinct from the green Success-tinted "Joined" tag in both icon shape and color.

## Related Skills

- **POC Evaluator agent:** Calls this skill before recommending any new UI element
- **UX Copy Reviewer:** Reviews text; this skill reviews visual elements
- **Section Writer:** Writes specs; should run proposed UI through this skill first
