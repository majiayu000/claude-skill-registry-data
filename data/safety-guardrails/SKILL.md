---
name: safety-guardrails
description: LLM safety guardrails and content moderation
sasmp_version: "1.3.0"
bonded_agent: 08-prompt-security-agent
bond_type: PRIMARY_BOND
---

# Safety Guardrails Skill

**Bonded to:** `prompt-security-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:safety-guardrails")
```

---

## Parameter Schema

```yaml
parameters:
  safety_level:
    type: enum
    values: [permissive, standard, strict, maximum]
    default: standard

  content_filters:
    type: array
    values: [harmful, hate, violence, adult, pii]
    default: [harmful, hate, violence]

  output_validation:
    type: boolean
    default: true
```

---

## Guardrail Types

| Guardrail | Purpose | Implementation |
|-----------|---------|----------------|
| Input filtering | Block harmful requests | Pattern matching |
| Output filtering | Prevent harmful outputs | Content analysis |
| Topic boundaries | Stay on-topic | Scope enforcement |
| Format validation | Ensure safe formats | Schema checking |

---

## Content Filtering

### Categories

```yaml
content_categories:
  harmful:
    - dangerous_activities
    - illegal_actions
    - self_harm

  hate_speech:
    - discrimination
    - slurs
    - targeted_harassment

  violence:
    - graphic_violence
    - threats
    - weapons_instructions

  pii:
    - personal_data
    - financial_info
    - credentials
```

### Filter Implementation

```markdown
## Content Guidelines

NEVER generate content that:
1. Provides instructions for harmful activities
2. Contains hate speech or discrimination
3. Describes graphic violence
4. Exposes personal information
5. Bypasses safety measures

If a request violates these guidelines:
1. Decline politely
2. Explain which guideline applies
3. Offer a safe alternative if possible
```

---

## Output Validation

```yaml
validation_rules:
  format_check:
    - valid_json_if_requested
    - no_executable_code_in_text
    - no_embedded_commands

  content_check:
    - no_pii_exposure
    - no_harmful_instructions
    - appropriate_for_audience

  consistency_check:
    - matches_role_constraints
    - within_topic_boundaries
```

---

## Safe Response Patterns

### Declining Harmful Requests

```markdown
I can't help with that request because [reason].

Here's what I can help with instead:
- [Alternative 1]
- [Alternative 2]

Would any of these work for you?
```

### Handling Edge Cases

```markdown
I notice this request is [description of concern].

To ensure I'm being helpful in the right way:
1. Could you clarify [specific aspect]?
2. Here's a safe approach to [related task]:
   [Safe alternative]
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Over-blocking | Too strict | Tune sensitivity |
| Under-blocking | Too permissive | Add patterns |
| False positives | Ambiguous content | Context-aware rules |
| Inconsistent | Rule conflicts | Prioritize rules |

---

## References

See: Anthropic Constitutional AI, OpenAI Moderation API
