---
name: writing-rules
description: Extract and manage writing rules (style, structure, persona, publisher, custom) (project)
---

# Writing Rules Skill

## Overview

Unified system for extracting writing rules AND managing the extensible rule type registry. Handles both rule extraction operations and registry management operations.

**For usage examples and workflows, see `CLAUDE.md`.**

---

## Operations

### Extraction Operations

**style** - Extract style guidelines (voice, tone, word choice)
- Entry: `writing-rules-skill style --type <mode> --auto-discover`
- Modes: primary, technical-docs, blog, etc.
- Output: `rules/style/<descriptive-name>.md`

**structure** - Extract structure templates (document organization, section flow)
- Entry: `writing-rules-skill structure --type <mode> --auto-discover`
- Modes: tutorial, landing-page, api-reference, etc.
- Output: `rules/structure/<descriptive-name>.md`

**persona** - Extract target personas (audience roles, pain points, preferences)
- Entry: `writing-rules-skill persona --audience-type <type> --auto-discover`
- Types: technical, business, all, etc.
- Output: `rules/personas/<descriptive-name>.md`

**publisher** - Extract publisher profile (company identity, messaging, positioning)
- Entry: `writing-rules-skill publisher --auto-discover`
- Output: `rules/publisher/publisher-profile.md` (single file)

**[custom-type]** - Extract custom rule types (if configured in registry)
- Entry: `writing-rules-skill <custom-type> --type <mode> --auto-discover`
- Output: `rules/<custom-type>/<descriptive-name>.md`

### Update Operations (Feedback-Driven)

**style --update** - Update existing style rule based on recent feedback
- Entry: `writing-rules-skill style --type <type> --update`
- Requires: Existing style rule + recent tone/style feedback
- Output: Updated style rule with backup
- Subskill: `subskills/update-style.md`

**structure --update** - Update existing structure template based on recent feedback
- Entry: `writing-rules-skill structure --type <type> --update`
- Requires: Existing structure template + recent structure/organization feedback
- Output: Updated structure template with backup
- Subskill: `subskills/update-structure.md`

**persona --update** - Update existing persona based on recent feedback
- Entry: `writing-rules-skill persona --audience-type <type> --update`
- Requires: Existing persona + recent info/length/comprehension feedback
- Output: Updated persona with backup
- Subskill: `subskills/update-persona.md`

### Management Operations

**list** - List all rule types (built-in + custom) with extraction status
- Entry: `writing-rules-skill list`

**show** - Show details about a specific rule type
- Entry: `writing-rules-skill show <type>`

**add** - Add new custom rule type (interactive wizard with conflict detection)
- Entry: `writing-rules-skill add`

**validate** - Validate registry configuration and file system consistency
- Entry: `writing-rules-skill validate`

**generate-subskill** - Generate extraction subskill for custom type
- Entry: `writing-rules-skill generate-subskill <custom-type>`

**onboard** - Onboarding wizard for new teams
- Entry: `writing-rules-skill onboard`

---

## Technical Details

### Routing Logic

1. **Parse arguments** - Determine operation type and parameters
2. **Load context:**
   - Registry: Read `rules/rules-config.yaml`
   - Project context (if available)
   - Source content status
   - Existing rules
   - Feedback data (for update operations)
3. **Route to subskill:**
   - Management ops → `subskills/manage-<operation>.md`
   - Extraction ops → `subskills/extract-<type>.md`
   - Update ops (--update flag) → `subskills/update-<type>.md`
4. **Pass context** - Provide all necessary info to subskill

### Preview Mode (Iterative Extraction)

When invoked from extract-rules subskill:

**Pattern:** Analyze → Preview → Approve → Extract

1. **Analyze available content** - Group indexed documents by type, domain, date
2. **Preview sample documents** - Show 3-5 examples with coverage stats
3. **Get approval** - User can approve, refine (use different docs), or skip
4. **Execute extraction** - Run with --auto-discover on approved document set
5. **Review results** - Show extracted rule file and key characteristics

**Why preview?**
- Ensures right documents analyzed
- Shows coverage before expensive AI analysis
- Allows refinement if wrong documents selected

### Registry Configuration

**Location:** `rules/rules-config.yaml`

**Defines:**
- Which rule types are enabled (built-in + custom)
- What each type extracts and governs
- Directory locations for each type
- Extraction settings (discovery modes, sample size)

**Built-in types** (always available):
- style, structure, persona, publisher

**Custom types** (team-configurable):
- verticals, use-cases, channels, journey-stages, etc.

### Extraction Modes

**Incremental** (default - recommended):
- Compares with existing rules
- Creates new files only if distinct patterns found
- Safe, additive approach

**Overwrite** (nuclear option):
- Deletes existing rules in category
- Performs fresh analysis
- Use when rules are outdated

---

## Integration with Other Skills

**Called by:**
- **extract-rules subskill** - Routes extraction requests here with preview mode
- **check-onboarding subskill** - For extracting core rules (publisher, primary voice, personas)
- **feedback-skill patterns subskill** - Recommends update operations when patterns emerge
- Direct invocation for rule extraction or updates

**Delegates to:**
- **Extraction subskills** - Type-specific extraction logic in `subskills/extract-<type>.md`
- **Update subskills** - Feedback-driven updates in `subskills/update-<type>.md`
- **Management subskills** - Registry operations in `subskills/manage-<operation>.md`

**Works with:**
- **project-management-skill** - Rules are referenced in project.md
- **content-writing-skill** - Rules are applied during content creation
- **feedback-skill** - Provides feedback data to drive rule updates

---

## Key Principles

1. **Registry as source of truth** - All rule types defined in rules-config.yaml
2. **Extensibility** - Custom types via registry configuration
3. **Preview before extraction** - Always show sample documents for approval
4. **Incremental by default** - Don't overwrite existing rules unless explicitly requested
5. **Quality over quantity** - Need 3-5 documents minimum for reliable extraction
6. **Type-specific extraction** - Each type has specialized extraction logic
7. **Feedback-driven updates** - Use real user feedback to improve rules over time
8. **User control** - Always show diff preview and get approval before updating rules

---

For usage examples and workflows, see **`CLAUDE.md`**.
For registry configuration details, see `README.md` in this skill directory.
