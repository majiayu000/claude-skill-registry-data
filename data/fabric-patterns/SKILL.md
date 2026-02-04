---
name: fabric-patterns
description: Applies Fabric AI prompt patterns for summarization, analysis, extraction, code review, and content creation. Use when asked to summarize content, analyze documents, extract insights, review code, create documentation, or transform text. Patterns are in data/patterns/.
---

# Fabric Patterns

Apply specialized prompt patterns from the Fabric framework for consistent, high-quality AI outputs.

## When This Skill Activates

- Summarizing documents, videos, meetings, papers, git diffs
- Analyzing code, threats, claims, logs, prose
- Extracting insights, ideas, entities, wisdom
- Creating PRDs, user stories, commit messages, documentation
- Improving writing, code, or prompts

## How to Use Patterns

1. Identify the relevant pattern from categories below
2. Read the pattern: `data/patterns/{pattern_name}/system.md`
3. Follow its IDENTITY, STEPS, and OUTPUT INSTRUCTIONS sections

## Pattern Categories

### Summarize
| Pattern | Use |
|---------|-----|
| `summarize` | General summary with key points |
| `summarize_paper` | Academic papers |
| `summarize_meeting` | Meeting notes → action items |
| `summarize_git_diff` | Code changes |
| `create_micro_summary` | Ultra-concise |

### Analyze
| Pattern | Use |
|---------|-----|
| `analyze_claims` | Truth-rate claims with evidence |
| `analyze_prose` | Writing quality evaluation |
| `analyze_logs` | Server log analysis |
| `analyze_threat_report` | Security threats |
| `review_code` | Code review feedback |

### Extract
| Pattern | Use |
|---------|-----|
| `extract_wisdom` | Key insights from content |
| `extract_ideas` | Main ideas as bullets |
| `extract_recommendations` | Actionable recommendations |
| `extract_references` | Citations and sources |

### Create
| Pattern | Use |
|---------|-----|
| `create_prd` | Product Requirements Document |
| `create_user_story` | Technical user stories |
| `write_pull-request` | PR descriptions |
| `create_git_diff_commit` | Commit messages |
| `create_design_document` | System design docs |

### Improve
| Pattern | Use |
|---------|-----|
| `improve_writing` | Grammar and clarity |
| `improve_prompt` | Enhance AI prompts |
| `improve_academic_writing` | Academic tone |

## Full Pattern List

See all 232 patterns: `ls data/patterns/`

Read pattern details: `cat data/patterns/{name}/system.md`

## Example

User: "Summarize this research paper"

1. Read `data/patterns/summarize_paper/system.md`
2. Apply its methodology to the paper
3. Output per the pattern's format instructions
