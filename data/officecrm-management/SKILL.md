---
name: office:crm-management
description: Manage contacts, companies, deals, and relationships. Use when adding contacts, logging interactions, or working with CRM data to prevent duplicates and maintain data quality.
---

# Office Admin CRM Management

## When to Use This Skill

Use this skill ANY time you:
- Add contacts from emails or conversations
- Create or update deals
- Log interactions with people
- Search for existing contacts or companies
- Work with relationships between contacts
- Backfill CRM data from email history
- Need to check if a contact already exists

## User CRM Preferences

Load user preferences from `~/.claude/office-admin-config.json`:

```json
{
  "crm": {
    "contactTypes": "professional" | "personal" | "mixed",
    "detailLevel": "minimal" | "standard" | "detailed",
    "autoLogInteractions": true | false,
    "trackRelationships": true | false
  }
}
```

Adapt your CRM workflow to match these preferences.

## Core Principles

### 1. Always Check Before Adding
**NEVER add a contact or company without checking if they already exist first.**

```bash
# WRONG - adds without checking
mcp__pagen__add_contact(name="John Doe", email="john@example.com")

# RIGHT - check first
mcp__pagen__find_contacts(query="john@example.com")
# Only add if not found
```

### 2. Associate Contacts with Companies
When you know someone's company, ALWAYS link them:

```bash
# Add company first (if needed)
mcp__pagen__add_company(
  name="Acme Corp",
  domain="acme.com",
  industry="Technology"
)

# Then add contact with company association
mcp__pagen__add_contact(
  name="John Doe",
  email="john@example.com",
  company_name="Acme Corp",
  phone="+1-555-0100"
)
```

### 3. Log Meaningful Interactions
After ANY significant email exchange, meeting, or conversation, log it (if user has `autoLogInteractions` enabled):

```bash
mcp__pagen__log_contact_interaction(
  contact_id="abc-123",
  note="Discussed Q4 partnership. They're interested in our AI tool. Follow up after Thanksgiving.",
  interaction_date="2025-11-22"
)
```

Adjust detail level based on user's `detailLevel` preference:
- **Minimal**: Just key facts
- **Standard**: Context about interaction
- **Detailed**: Thorough notes with quotes, decisions, next steps

## Available CRM Tools

### Core Tools
- `mcp__pagen__add_company(name, domain, industry, notes)` - Add new company
- `mcp__pagen__add_contact(name, email, company_name, phone, notes)` - Add new contact
- `mcp__pagen__update_contact(id, name, email, phone, notes)` - Update existing contact
- `mcp__pagen__create_deal(title, company_name, amount, stage, contact_name, initial_note, expected_close_date, currency)` - Create business opportunity
- `mcp__pagen__update_deal(id, title, stage, amount, expected_close_date)` - Update deal status

### Search & Query Tools
- `mcp__pagen__query_crm(entity_type, query, filters, limit)` - Universal search (contact/company/deal/relationship)
- `mcp__pagen__find_contacts(query, company_id, limit)` - Search contacts by name/email
- `mcp__pagen__find_companies(query, limit)` - Search companies by name/domain

### Relationship & Interaction Tools
- `mcp__pagen__log_contact_interaction(contact_id, note, interaction_date)` - Log interactions
- `mcp__pagen__link_contacts(contact_id_1, contact_id_2, relationship_type, context)` - Connect contacts
- `mcp__pagen__find_contact_relationships(contact_id, relationship_type)` - View relationships
- `mcp__pagen__add_deal_note(deal_id, content)` - Add notes to deals

## Deal Stages

Use these standard stages for deals:
- **prospecting** - Initial conversations, exploring possibilities
- **qualification** - Determining if it's a real opportunity with potential
- **proposal** - Active proposal or pitch in progress
- **negotiation** - Terms being discussed, getting close
- **closed_won** - Deal completed successfully
- **closed_lost** - Deal didn't happen (still valuable to track why)

## Workflow: Adding Contact from Email

When processing an email with a new person:

```bash
# 1. Check if contact exists
mcp__pagen__find_contacts(query="person@example.com")

# 2. If not found, extract info from email:
#    - Full name
#    - Email address
#    - Company (if mentioned)
#    - Phone (if in signature)
#    - Context about them (adapt detail level to user's preference)

# 3. Check if company exists (if applicable)
mcp__pagen__find_companies(query="Example Corp")

# 4. Add company if needed
mcp__pagen__add_company(
  name="Example Corp",
  domain="example.com",
  industry="Technology",
  notes="[Context based on user's detailLevel preference]"
)

# 5. Add contact with company association
mcp__pagen__add_contact(
  name="Jane Smith",
  email="jane@example.com",
  company_name="Example Corp",
  phone="+1-555-0200",
  notes="[Context based on user's detailLevel preference]"
)

# 6. Log the interaction (if autoLogInteractions enabled)
mcp__pagen__log_contact_interaction(
  contact_id="<returned_id>",
  note="[Detail based on user's detailLevel preference]",
  interaction_date="2025-11-22"
)

# 7. Track relationships (if trackRelationships enabled)
# If they mention knowing someone else in your CRM:
mcp__pagen__link_contacts(
  contact_id_1="<jane_id>",
  contact_id_2="<bob_id>",
  relationship_type="colleague",
  context="Jane mentioned working with Bob at previous company"
)
```

## Workflow: Creating a Deal

When you identify a business opportunity:

```bash
# 1. Ensure contact and company exist (see above)

# 2. Create the deal
mcp__pagen__create_deal(
  title="AI Consulting Project - Example Corp",
  company_name="Example Corp",
  contact_name="Jane Smith",
  stage="prospecting",
  amount=50000,  # in cents
  currency="USD",
  expected_close_date="2026-03-01",
  initial_note="[Detail based on user's detailLevel preference]"
)

# 3. Log updates as deal progresses
mcp__pagen__add_deal_note(
  deal_id="<deal_id>",
  content="[Detail based on user's detailLevel preference]"
)

# 4. Update deal stage when it changes
mcp__pagen__update_deal(
  id="<deal_id>",
  stage="proposal",
  amount=75000  # updated after scope discussion
)
```

## What Counts as a "Deal"?

Track these as deals:
- ✅ Consulting or advisory opportunities
- ✅ Speaking engagements with compensation
- ✅ Book publishing opportunities
- ✅ Partnership or collaboration opportunities
- ✅ Investment opportunities
- ✅ Real estate transactions
- ✅ Major purchases or sales
- ✅ Sponsorships (being a sponsor or receiving sponsorship)

Don't track as deals:
- ❌ Social lunches with no business angle
- ❌ Informational coffee chats
- ❌ Personal favors or introductions
- ❌ Newsletter subscriptions
- ❌ Generic networking

## Email Backfill Best Practices

When backfilling CRM from email history:

1. **Work in time-bounded batches** - Process 1-2 months at a time
2. **Start with SENT emails** - You're usually the initiator, so sent emails have better signal
3. **Then do INBOX** - Catch incoming opportunities you might have missed
4. **Skip noise** - Ignore newsletters, receipts, automated emails
5. **Focus on humans** - Only add real people they interact with
6. **Log context** - Include what was discussed, not just "sent email"
7. **Check for dupes** - Always search before adding
8. **Respect detailLevel** - Match note detail to user's preference

## Contact Types and Filtering

Based on user's `contactTypes` setting:

**Professional:**
- Focus on work relationships
- Track company associations carefully
- Emphasize business context in notes
- Create deals for opportunities

**Personal:**
- Focus on personal relationships
- Company associations optional
- Emphasize personal context (how you met, shared interests)
- Deals less common

**Mixed:**
- Handle both types
- Clearly distinguish in notes which category
- Be flexible with detail level
- Track both business and personal context

## Common Mistakes to Avoid

### ❌ Adding without checking
```bash
# This creates duplicates!
mcp__pagen__add_contact(name="Bob Jones", email="bob@test.com")
mcp__pagen__add_contact(name="Bob Jones", email="bob@test.com")
```

### ❌ Not associating with company
```bash
# Missing valuable context
mcp__pagen__add_contact(
  name="Jane Smith",
  email="jane@bigcorp.com"
  # Should include company_name="BigCorp"!
)
```

### ❌ Wrong level of detail
```bash
# User has detailLevel: "minimal" but you write:
mcp__pagen__log_contact_interaction(
  contact_id="abc",
  note="Had extensive discussion about their company's AI strategy including their plans for Q1 implementation of LLM-based customer support, concerns about hallucinations, budget constraints around $50k, and follow-up scheduled for next Tuesday at 2pm to review proposal draft..."
)

# Should be:
mcp__pagen__log_contact_interaction(
  contact_id="abc",
  note="Discussed AI strategy. Follow up Tue 2pm with proposal."
)
```

### ❌ Not tracking deals
```bash
# Someone asks about consulting work - this is a deal!
# Don't just log it as an interaction
# Create a deal to track the opportunity
```

### ❌ Over-logging when autoLogInteractions is false
```bash
# If user disabled auto-logging, only log:
# - Significant milestones
# - Explicit user request
# - Deal-related interactions
```

## Data Quality Guidelines

### Good Contact Notes (based on detailLevel)

**Minimal:**
- How you met
- Their role or what they do
- One-line context

**Standard:**
- How you met
- What they're interested in
- Current conversation or project
- Key personal detail (timezone, etc.)

**Detailed:**
- Comprehensive background
- Detailed conversation history
- Personal preferences and patterns
- Relationship mapping
- Next steps and follow-ups

### Good Company Notes

Include (scaled to detailLevel):
- Industry or sector
- Company size if relevant
- What they do
- Context about the relationship

### Good Interaction Notes

Include (scaled to detailLevel):
- What was discussed
- Outcomes or decisions
- Next steps or follow-ups
- Date of interaction

## Integration with Email Skill

When email-management skill identifies a new contact:
1. Automatically trigger CRM workflow
2. Check for existing contact
3. Add if new (respecting CRM preferences)
4. Log interaction if enabled
5. Return to email workflow

## Summary Checklist

Before adding to CRM, ask yourself:

- ☐ Did I check user's CRM preferences from config?
- ☐ Did I search to see if this contact already exists?
- ☐ Did I search to see if their company already exists?
- ☐ Did I include company association if I know it?
- ☐ Did I match the user's preferred detail level?
- ☐ Is autoLogInteractions enabled? Should I log this?
- ☐ Is this a deal I should be tracking?
- ☐ Should I track relationships to other contacts?
- ☐ Did I include phone number if available?

**Remember**: The CRM is only valuable if the data is clean and contextual. Quality over quantity, always.

## Success Criteria

You're managing CRM well when:
- No duplicate contacts are created
- Contact notes match user's preferred detail level
- Interactions are logged appropriately (not too much, not too little)
- Deals are tracked consistently
- Relationships are mapped when user has that enabled
- Integration with email workflow is seamless
