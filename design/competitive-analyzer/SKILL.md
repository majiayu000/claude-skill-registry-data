---
name: Competitive Analyzer
description: Analyzes how multiple platforms handle UX problems for classified/IL4+ environments, identifying gaps and differentiation opportunities.
version: 1.0.0
author: Mattermost Design Team
tags: [competitive-analysis, ux-research, doD-compliance, security-analysis, platform-comparison]
---

# Competitive Analyzer

## Overview

The Competitive Analyzer is a senior UX research skill that performs systematic comparative analysis of how enterprise collaboration platforms handle specific feature areas and UX problems, with explicit focus on gaps in classified/IL4+ (DoD IL5) environments. This skill synthesizes findings into actionable patterns for Mattermost differentiation.

## When to Use

- Analyzing a new feature area where competitive precedent exists (e.g., "How do other platforms handle secure group messaging?" or "How do competitors prevent cross-channel data spillage?")
- Identifying UX patterns that have strong user mental model precedent to preserve
- Understanding where ALL platforms fail for DoD environments (these are differentiation opportunities)
- Building a competitive positioning narrative for a specific capability
- Early-stage design discovery before writing PRDs
- Evaluating whether to adopt a competitor pattern or innovate

## When NOT to Use

- When you need a complete market analysis across all possible features (this skill compares specific platforms, not whole markets)
- For evaluating vendor solutions for procurement (not a procurement tool)
- When you need to understand competitor business models or go-to-market strategy
- For compliance gap analysis without UX context (use Threat Modeler skill instead)
- When analyzing user research data from Mattermost users (use interview-synthesizer instead)

## System Prompt

```
You are a senior UX researcher specializing in enterprise security platforms and classified communication environments.

Your analysis methodology:
1. For each platform in the list, examine how they handle the specified feature area
2. Document their UX approach using this framework:
   - Paradigm: What conceptual model governs the interaction?
   - Key interactions: What are the primary user actions?
   - Information architecture: How is the feature surfaced and organized?
   - Affordances: What signals guide user behavior?
   - Error states: How do they handle misuse?

3. Assess strengths using these dimensions:
   - Established mental models: Do users already know this pattern from other apps?
   - Usability evidence: Is there public evidence this works well? (reviews, adoption, awards)
   - Learnability: Can new users understand it quickly?
   - Consistency: Does it align with platform norms?

4. Identify failures specific to DoD IL5 / classified environments:
   - Security gaps: Where could a user accidentally expose classified information?
   - Compliance gaps: Which DoD/NIST controls are not addressed by the UI?
   - Operational gaps: What assumptions break down under mil-ops tempo?
   - Insider threat enablement: What could a malicious insider exploit?
   - Classification/handling marking requirements: Are classification levels visible and reinforced at every interaction point?

5. Document patterns from each platform:
   - Which patterns are leverage-worthy (users expect them)
   - Which patterns must be avoided or adapted for classified environments
   - Which patterns are present in ALL platforms (indicating a gap vs. innovation opportunity)

6. Synthesize findings:
   - List 3-5 patterns Mattermost should leverage (cognitive continuity)
   - List 2-3 patterns Mattermost must avoid or adapt
   - Identify 1-2 areas where ALL platforms fail (this is where Mattermost differentiates)
   - For each differentiation opportunity, suggest a UX principle that guides the solution

Your analysis should be specific, evidence-based, and pragmatic. Avoid generic statements like "Slack is better at UX."
Ground observations in concrete interactions and user mental models.
```

## Input Schema

```json
{
  "feature_area": {
    "type": "string",
    "description": "Specific UX problem area to analyze (e.g., 'preventing accidental cross-channel messaging', 'managing classification levels on messages', 'handling mobile offline sync in low-bandwidth environments')",
    "minLength": 20,
    "maxLength": 300
  },
  "platforms": {
    "type": "array",
    "items": {
      "type": "string",
      "enum": ["Slack", "Microsoft Teams", "Google Chat", "Symphony", "Element", "Wire", "Rocket.Chat", "Zulip", "Nextcloud Talk"]
    },
    "description": "List of platforms to analyze. Defaults to ['Slack', 'Microsoft Teams', 'Google Chat', 'Symphony', 'Element']",
    "minItems": 2,
    "maxItems": 6,
    "default": ["Slack", "Microsoft Teams", "Google Chat", "Symphony", "Element"]
  },
  "environment_context": {
    "type": "string",
    "description": "DoD classification level, user population, operational tempo (e.g., 'IL5 classified, Air Force tactical operations, high-stress time-critical decisions', or 'IL4 contractor collaboration, distributed teams, asynchronous')",
    "minLength": 20,
    "maxLength": 500
  },
  "depth": {
    "type": "string",
    "enum": ["shallow", "standard", "deep"],
    "description": "Analysis depth. shallow=2-3 sentences per platform; standard=paragraph per platform; deep=detailed with user flows and screenshots if possible",
    "default": "standard"
  },
  "focus_security_posture": {
    "type": "boolean",
    "description": "If true, emphasize security and compliance gaps over general UX strengths",
    "default": true
  },
  "required": ["feature_area", "environment_context"]
}
```

### Input Example

```json
{
  "feature_area": "How do platforms prevent users from accidentally sending classified messages to unclassified channels or users without proper clearance?",
  "platforms": ["Slack", "Microsoft Teams", "Symphony", "Element"],
  "environment_context": "IL5 special access program environment, fighter pilots and mission planners using mobile devices in tactical operations center, high stress decision-making, asynchronous deconfliction required",
  "depth": "standard",
  "focus_security_posture": true
}
```

## Output Schema

```json
{
  "feature_area": "string (echoed from input)",
  "analysis_timestamp": "ISO 8601 datetime",
  "platform_analyses": [
    {
      "platform": "string (platform name)",
      "paradigm": "string (conceptual model)",
      "key_interactions": [
        {
          "interaction": "string (e.g., 'composing a message')",
          "description": "string (how the platform handles this interaction)"
        }
      ],
      "strengths": [
        {
          "strength": "string",
          "evidence": {
            "source": "string (URL, doc title, or vendor reference; use '[REQUIRES VENDOR DOCUMENTATION]' if unverifiable — never fabricate a source)",
            "as_of": "string (ISO 8601 publication or access date; omit only if the source is undated)",
            "confidence": "string (verified | reported | inferred)"
          }
        }
      ],
      "failures_for_il5": [
        {
          "failure": "string (what breaks)",
          "type": "security_gap | compliance_gap | operational_gap | insider_threat",
          "description": "string (why it's a problem in DoD context)",
          "severity": "P1 | P2 | P3 (P1 = mission-critical exposure)"
        }
      ],
      "patterns_worth_adopting": [
        "string (specific, copyable pattern)"
      ],
      "patterns_to_avoid": [
        "string (specific pattern)"
      ]
    }
  ],
  "synthesis": {
    "patterns_to_leverage": [
      {
        "pattern": "string",
        "rationale": "string (why users expect this)",
        "platforms_with_precedent": ["string"],
        "mattermost_implementation_hint": "string"
      }
    ],
    "patterns_to_avoid_or_adapt": [
      {
        "pattern": "string",
        "reason": "string (why it breaks for classified environments)",
        "suggested_adaptation": "string"
      }
    ],
    "all_platforms_fail_at": [
      {
        "gap": "string (the unmet need)",
        "why_it_matters": "string (operational consequence)",
        "differentiation_principle": "string (how Mattermost should think about solving this)",
        "investigation_needed": "string (what research or design work is needed)"
      }
    ]
  },
  "recommendations": {
    "next_research_steps": ["string"],
    "features_to_prototype": ["string"],
    "design_system_implications": ["string"]
  }
}
```

### Output Example

```json
{
  "feature_area": "How do platforms prevent users from accidentally sending classified messages to unclassified channels or users without proper clearance?",
  "analysis_timestamp": "2026-03-10T14:32:00Z",
  "platform_analyses": [
    {
      "platform": "Slack",
      "paradigm": "Flat channel model with optional data-loss-prevention (DLP) plugins. No native concept of classification levels; security is enforced administratively through channel membership and retention policies.",
      "key_interactions": [
        {
          "interaction": "composing a message",
          "description": "User types in a message composer, selects a channel from a dropdown or recent list, hits Send. No pre-send verification of channel context, classification level, or recipient clearance."
        },
        {
          "interaction": "channel switching",
          "description": "User clicks on channel name or scrolls a sidebar list. No visual distinction of classification level or handling marking. All channels appear equal."
        }
      ],
      "strengths": [
        {
          "strength": "Simple, low-cognitive-load composition flow",
          "evidence": {
            "source": "Slack Engineering Blog — composition UX benchmarks",
            "as_of": "2025-11",
            "confidence": "reported"
          }
        },
        {
          "strength": "Familiar mental model from email",
          "evidence": {
            "source": "[REQUIRES VENDOR DOCUMENTATION]",
            "confidence": "inferred"
          }
        }
      ],
      "failures_for_il5": [
        {
          "failure": "No classification level indicator on messages or channels",
          "type": "security_gap",
          "description": "User cannot verify they are in a classified channel before hitting Send. Visual affordance is missing. In tactical operations with high cognitive load, users will make mistakes.",
          "severity": "P1"
        },
        {
          "failure": "Channel membership is opaque",
          "type": "security_gap",
          "description": "User cannot easily verify that all intended recipients have required clearance without leaving the compose flow. No pre-send verification available.",
          "severity": "P1"
        },
        {
          "failure": "Message deletion/classification downgrade is not available",
          "type": "compliance_gap",
          "description": "Slack does not support post-send classification adjustment or secure deletion with audit trail. DoD requires ability to mark messages as 'sent in error' and remove them.",
          "severity": "P2"
        },
        {
          "failure": "Mobile UI removes classification affordances further",
          "type": "operational_gap",
          "description": "On mobile, channel context is even more difficult to perceive. Tactical users in field will have even higher error rate.",
          "severity": "P1"
        }
      ],
      "patterns_worth_adopting": [
        "Quick channel/DM selection via searchable dropdown",
        "Familiar message composer paradigm (textarea + Send button)",
        "Read receipts and presence indicators for synchronous coordination"
      ],
      "patterns_to_avoid": [
        "Assumption that channel membership implies sender awareness of classification level",
        "Post-send actions (delete, edit) that do not generate audit trail",
        "Mobile UI that reduces visual classification cues"
      ]
    },
    {
      "platform": "Microsoft Teams",
      "paradigm": "Hierarchical org structure (Teams > Channels > Threads). Classification levels can be assigned to Teams via sensitivity labels. Does not extend labels to individual messages.",
      "key_interactions": [
        {
          "interaction": "composing a message",
          "description": "User types in message composer. Sensitivity label (if team-level) is shown, but user cannot verify recipient clearance or change label at message level."
        },
        {
          "interaction": "channel/team switching",
          "description": "User clicks on Team or Channel from navigation. Sensitivity label badge may appear on Team name, but not consistently surfaced."
        }
      ],
      "strengths": [
        {
          "strength": "Team-level sensitivity labels provide org-context awareness",
          "evidence": {
            "source": "Microsoft Purview Information Protection documentation — sensitivity labels for Teams",
            "as_of": "2025-09",
            "confidence": "verified"
          }
        },
        {
          "strength": "Integration with Microsoft Entra ID (formerly Azure AD) clearance/group membership",
          "evidence": {
            "source": "Microsoft Entra ID — Teams membership governance documentation",
            "as_of": "2025-09",
            "confidence": "verified"
          }
        }
      ],
      "failures_for_il5": [
        {
          "failure": "Sensitivity labels are team-level only, not message-level",
          "type": "compliance_gap",
          "description": "A single team may contain both classified and unclassified conversations. User cannot tag an individual message as classified if the Team label is lower.",
          "severity": "P1"
        },
        {
          "failure": "User can forward/share messages to unlabeled teams without friction",
          "type": "security_gap",
          "description": "No warning or restriction when sharing a message from a labeled team to an unlabeled team. User error is easy.",
          "severity": "P1"
        },
        {
          "failure": "Threads can span classification levels",
          "type": "security_gap",
          "description": "A thread in a classified Team can contain both classified and unclassified messages, but the UI does not warn or enforce separation.",
          "severity": "P2"
        },
        {
          "failure": "Mobile UI does not consistently show Team sensitivity labels",
          "type": "operational_gap",
          "description": "Teams mobile app sometimes suppresses sensitivity label badges, increasing misuse risk on field devices.",
          "severity": "P2"
        }
      ],
      "patterns_worth_adopting": [
        "Hierarchical org structure (organization > team > channel > thread) is intuitive for large DoD orgs",
        "Sensitivity labels with visual badges (color, icon) as affordances",
        "Microsoft Entra ID (formerly Azure AD) integration for membership verification without user action"
      ],
      "patterns_to_avoid": [
        "Assuming team-level labels are sufficient for mixed-classification conversations",
        "Allowing cross-team message sharing without explicit security gate",
        "Suppressing security labels on mobile UI for brevity"
      ]
    }
  ],
  "synthesis": {
    "patterns_to_leverage": [
      {
        "pattern": "Searchable channel/team selector in composition flow",
        "rationale": "Users expect to find conversations by name, similar to email recipient selection. This is low-cognitive-load.",
        "platforms_with_precedent": ["Slack", "Teams", "Google Chat"],
        "mattermost_implementation_hint": "Include recent channels, favorites, and search in a typeahead. Do NOT require full channel navigation to compose."
      },
      {
        "pattern": "Visual classification badges on channel names and in sidebar",
        "rationale": "Users need constant, persistent visual cue of classification level. Badges (color, icon) are faster to scan than text.",
        "platforms_with_precedent": ["Teams (sensitivity labels)"],
        "mattermost_implementation_hint": "Show classification badge next to channel name everywhere it appears: sidebar, channel header, message composer dropdown, @mentions."
      },
      {
        "pattern": "Pre-send verification flow for high-sensitivity messages",
        "rationale": "Users making time-critical decisions cannot be expected to triple-check context. A confirmation dialog is necessary.",
        "platforms_with_precedent": ["None (this is a gap)"],
        "mattermost_implementation_hint": "Consider a modal that says 'You are about to send to [CLASSIFIED] channel. Recipients: [names + clearance levels]. This message is [classification]. Confirm Send?'"
      }
    ],
    "patterns_to_avoid_or_adapt": [
      {
        "pattern": "Flat channel model without hierarchical context",
        "reason": "In a DoD org with 100+ channels, flat navigation is cognitively overwhelming and increases error risk. Users need to see team context.",
        "suggested_adaptation": "Implement hierarchical channels (Team > Channel > Topic) with clear visual indentation and grouping."
      },
      {
        "pattern": "Silent message sharing across classification boundaries",
        "reason": "Allows accidental spillage without user awareness. DoD requires explicit confirmation.",
        "suggested_adaptation": "Block or warn when a message is about to be shared to a lower-classified channel. Show the user the classification delta."
      },
      {
        "pattern": "Sensitivity labels only at team/channel level",
        "reason": "Conversations in a team can span multiple classification levels (e.g., planning an operation vs. reporting results). One label is insufficient.",
        "suggested_adaptation": "Support message-level classification markers in addition to channel-level. A user can say 'this message is SECRET' even in a normal-classification channel."
      }
    ],
    "all_platforms_fail_at": [
      {
        "gap": "Verification of clearance levels at send time",
        "why_it_matters": "User cannot confirm that all recipients of a message have required clearance. This is the single biggest accidental spillage vector in DoD environments.",
        "differentiation_principle": "Mattermost must make recipient clearance visible and verified before Send is enabled. This is non-negotiable for IL5.",
        "investigation_needed": "Research how DoD organizations currently verify clearance levels in personnel databases. Can we integrate with CAC/Active Directory to surface clearance info in real time?"
      },
      {
        "gap": "Audit trail for classification decisions and changes",
        "why_it_matters": "When a message is marked as 'sent in error' or classification is adjusted post-send, DoD needs to know who made the decision, when, and why.",
        "differentiation_principle": "Every classification-related action (message marked classified, downgraded, deleted, forwarded) must be logged with user, timestamp, and reason.",
        "investigation_needed": "Work with DISA to understand audit trail requirements for IL5. What events must be logged? How long must logs be retained? How are they accessed during investigations?"
      },
      {
        "gap": "Mobile-first classification management",
        "why_it_matters": "All competitive platforms suppress classification affordances on mobile for UI simplicity. But DoD tactical users are primarily mobile-based. They need the same guarantees on a phone.",
        "differentiation_principle": "Mattermost must assume mobile is the primary interface for field users. Classification cues must be AS VISIBLE on mobile as on desktop, not less.",
        "investigation_needed": "Design and user test mobile flows with actual tactical users. What is the minimum set of classification info needed on a 4.5-inch screen? Can we use haptics, sounds, or status bar indicators?"
      }
    ]
  },
  "recommendations": {
    "next_research_steps": [
      "Interview 5-10 DoD mission planners about current message mishaps in classified operations (identify root causes)",
      "Analyze clearance management workflows in existing DoD systems (could Mattermost integrate?)",
      "Review NIST 800-53 AC-3 (Access Control) to understand formal policy requirements for access verification",
      "Audit Teams and Slack DLP configurations in DoD contractors to understand workarounds users have built"
    ],
    "features_to_prototype": [
      "Pre-send verification modal showing recipient clearance levels",
      "Message-level classification marker (independent of channel label)",
      "Classification audit trail display in message history",
      "Mobile-optimized classification affordances (larger badges, confirmation dialogs, status bar indicator)"
    ],
    "design_system_implications": [
      "Add classification badge component to design system (icon + color + text, responsive)",
      "Define confirmation dialog pattern for security-critical actions",
      "Create mobile-specific guidance: classification affordances MUST be same size/prominence on mobile as desktop"
    ]
  }
}
```

## Usage Example

### Scenario: Analyzing secure messaging patterns for IL5 tactical operations

```
Feature Area: "How can Mattermost prevent accidental classified message spillage when a user is composing under time pressure in a tactical operations environment?"

Platforms: ["Slack", "Teams", "Element"]

Environment: "IL5 special access program, tactical operations centers, fighter pilots and planners using mobile under 30-second decision windows, asynchronous deconfliction required post-action"

[Skill analyzes each platform's approach to message composition, classification marking, and recipient verification. Output identifies that:
- Slack has low cognitive load but zero classification guardrails
- Teams has team-level labels but allows cross-team spillage
- Element (Matrix) has no classification concept
- All three fail at verifying clearance levels at send time
- Differentiation opportunity: pre-send verification + mobile classification affordances]

Recommendation: Prototype a pre-send modal that shows:
1. Channel classification level (large, colored badge)
2. List of recipients with clearance levels (green = sufficient, red = insufficient)
3. Message classification being sent (with ability to upgrade if needed)
4. Large "Confirm Send" button (not small)
```

## Validation Rules

1. **Feature area specificity**: Input must be a specific UX problem, not a general product category (good: "preventing accidental @channel in critical channels"; bad: "how platforms do notifications")
2. **Platform selection**: At least 2 platforms, no more than 6. Include at least one defense-focused platform (Symphony, Element) if analyzing classified environments.
3. **Environment context**: Must include classification level (IL2-IL5 or equivalent), user population (role/tempo), and operational context (sync/async, mobile/desktop, time-critical?).
4. **Failure analysis rigor**: Each failure must include a concrete UI element or flow, not vague statements like "security is weak."
5. **Differentiation clarity**: All-platforms-fail section must identify where Mattermost can credibly be BETTER, not just different. Back up with research needs if claiming a gap.

## Related Skills

- **PRD Generator**: Takes competitive analysis and synthesizes into a product requirements document with specific feature set
- **Threat Modeler**: Takes this competitive analysis and identifies which patterns create UI-layer security risks for Mattermost
- **Solution Scorer**: Uses competitive insights to evaluate multiple solution approaches against DoD criteria
- **interview-synthesizer**: Combines competitive analysis with user research data to build design recommendations

## Design Principles

1. **Security cannot be an afterthought**: In DoD environments, every competitive pattern must be evaluated for security/compliance implications, not just usability.
2. **Mobile is not a stretch goal**: Field users are primarily mobile-based. If a pattern breaks on mobile, it fails for DoD.
3. **Copy leaders, innovate at gaps**: Use proven patterns where they exist (users understand them). Innovate only where all leaders fail.
4. **Clearance verification is mandatory**: Any messaging feature that does not verify recipient clearance before send is unacceptable for IL4+.
5. **Audit trails are non-negotiable**: Classification decisions, message changes, and failures must be logged for DoD compliance investigations.

## Troubleshooting

**Problem**: "The output is too generic and could apply to any product."
**Solution**: Ensure environment_context includes specific operational constraints (e.g., "30-second decision windows in tactical air control"). Re-run with focus_security_posture=true.

**Problem**: "I don't know enough about a specific platform's security features."
**Solution**: This skill analyzes publicly available information. For proprietary details (e.g., Teams' exact DLP implementation), note [REQUIRES VENDOR DOCUMENTATION] in the output and escalate to Research team.

**Problem**: "The differentiation opportunities feel obvious."
**Solution**: You may have selected platforms that are too similar. Try comparing Slack + Element + a bespoke military system to identify contrasting paradigms.

---

**Last Updated**: 2026-03-10
**Skill Owner**: Mattermost Design Research Team
