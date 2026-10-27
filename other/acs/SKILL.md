---
description: >
  Manage AI Content Strategy recommendations via Drush CLI.
  Generate, curate, and export content strategy recommendations
  powered by AI analysis of your existing site content.
trigger: when user asks to generate content strategy, manage recommendations, work with content ideas, or export content plans
---

# AI Content Strategy

You are managing AI-powered content strategy recommendations.
The module analyzes existing site content, navigation, and sitemap
to generate actionable content recommendations organized by category.

## Preamble — Auto-discover Current State

```bash
# Check AI provider health
drush acs:health

# List configured categories
drush acs:category:list

# Check last generation status
drush acs:report:status

# Get site structure for context
drush acs:sitemap
```

## Commands Reference

### Generation

| Command | Alias | Purpose |
|---|---|---|
| `acs:generate` | `acs-g` | Generate recommendations (`--category` to filter) |
| `acs:generate:more` | `acs-gm` | Generate 5 more ideas for a card |
| `acs:generate:add` | `acs-ga` | Add more cards to a category |
| `acs:health` | `acs-h` | Check AI provider configuration |

### Reports & Reading

| Command | Alias | Purpose |
|---|---|---|
| `acs:report` | `acs-r` | Full report (`--category`, `--priority`) |
| `acs:report:card` | `acs-rc` | View single card with all ideas |
| `acs:report:status` | `acs-rs` | Last-run timestamp, pages analyzed |
| `acs:sitemap` | `acs-s` | Site structure and content types |

### Card Management

| Command | Alias | Purpose |
|---|---|---|
| `acs:card:edit` | `acs-ce` | Edit card title/description (`--dry-run`) |
| `acs:card:delete` | `acs-cd` | Delete recommendation card (`--dry-run`) |

### Idea Management

| Command | Alias | Purpose |
|---|---|---|
| `acs:idea:edit` | `acs-ie` | Edit idea text (`--dry-run`) |
| `acs:idea:implement` | `acs-ii` | Mark implemented (`--link`, `--undo`, `--dry-run`) |
| `acs:idea:delete` | `acs-id` | Delete content idea (`--dry-run`) |

### Categories

| Command | Alias | Purpose |
|---|---|---|
| `acs:category:list` | `acs-catl` | List all with status/weight |
| `acs:category:get` | `acs-catg` | Full category detail |
| `acs:category:create` | `acs-catc` | Create category (`--dry-run`) |
| `acs:category:update` | `acs-catu` | Update category (`--dry-run`) |
| `acs:category:delete` | `acs-catd` | Delete category (`--dry-run`) |

### Settings & Export

| Command | Alias | Purpose |
|---|---|---|
| `acs:settings:get` | `acs-sg` | View global settings |
| `acs:settings:set` | `acs-ss` | Update system prompt (`--dry-run`) |
| `acs:export` | `acs-e` | Export (`--format=yaml/json/csv`, `--file`) |

### Setup

| Command | Alias | Purpose |
|---|---|---|
| `acs:setup-ai` | `acs-sa` | Install AI skill files (`--host`, `--check`) |

## Workflow Examples

### Generate fresh recommendations
```bash
drush acs:health
drush acs:generate -l https://example.com
drush acs:report
```

### Curate and implement
```bash
drush acs:report --priority=high
drush acs:idea:implement content_gaps CARD-UUID IDEA-UUID --link=https://example.com/new-page
drush acs:export --format=json
```

### Manage categories
```bash
drush acs:category:list
drush acs:category:create seasonal_content "Seasonal Content" \
  --instructions="Identify seasonal and timely content opportunities"
drush acs:category:update trust_signals --weight=5
```

## Key Concepts

- **Categories** are config entities (content_gaps, authority_topics,
  expertise_demonstrations, trust_signals, etc.)
- **Cards** are recommendations within a category, each with a title,
  description, priority (high/medium/low), and content ideas
- **Ideas** are specific content suggestions within a card, with
  implementation status and optional links
- Recommendations are stored in key-value store, not as nodes
- Generation requires a configured AI provider (via drupal/ai module)
- All state-changing commands support `--dry-run`
- All output is structured YAML with success/message/data envelope
