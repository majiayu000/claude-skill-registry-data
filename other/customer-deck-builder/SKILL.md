---
name: customer-deck-builder
description: Build tailored customer-facing sales or customer success decks from approved account context and generate the presentation with Gamma through Zapier MCP.
---

# Customer Deck Builder

Use this skill when a GTM team needs a customer-facing deck for discovery, QBR, renewal, expansion, executive briefing, onboarding, or follow-up.

## Workflow

1. Gather the minimum context:
   - company name, domain, or account ID
   - call type
   - meeting goal
   - attendee roles
   - specific topics, questions, or risks
2. Resolve the account from approved CRM or account-data sources.
3. Pull only the approved fields needed for the deck:
   - account plan and renewal context
   - usage summary
   - active users or builder roles
   - top apps and workflows
   - feature adoption
   - relevant customer notes or meeting context
4. Choose the right deck shape:
   - discovery or first meeting
   - QBR or business review
   - renewal
   - expansion or upsell
   - executive briefing
   - onboarding kickoff
   - follow-up or check-in
5. Build the narrative before writing slides:
   - what the customer is doing today
   - what value they are already getting
   - what risks, gaps, or opportunities are visible
   - which use cases fit their stack, role, or goal
   - what next step should come out of the meeting
6. Write slide-by-slide markdown for Gamma.
7. Generate the deck through Zapier MCP using Gamma actions.
8. Return the Gamma URL, deck summary, and review notes.

## Deck Structures

### Discovery Or First Meeting

Goal: establish credibility, show useful context, and frame relevant automation opportunities.

Suggested slides:

1. Cover
2. Agenda
3. What we know about the customer
4. AI automation opportunity
5. Where to start
6. Relevant use cases
7. Customer proof
8. Next steps

### QBR Or Business Review

Goal: show value delivered, identify optimization opportunities, and align on next steps.

Suggested slides:

1. Cover
2. Agenda
3. Customer and Zapier team
4. Account health overview
5. Usage trend or task-limit utilization
6. Feature adoption
7. Top workflows and apps
8. Opportunities
9. Progress and next steps

### Renewal

Goal: recap value, show trajectory, and connect the renewal conversation to measurable outcomes.

Suggested slides:

1. Cover
2. Agenda
3. Year in automation
4. Usage trend
5. Current-period usage
6. Automation stack
7. Relevant product updates
8. Plan fit
9. Expansion opportunities
10. Next steps

### Expansion Or Executive Briefing

Goal: show current value, identify where more teams or workflows can benefit, and keep the conversation outcome-focused.

Suggested slides:

1. Cover
2. Current impact
3. Who is building
4. What is working
5. New use cases
6. Product updates
7. Proof points
8. Next steps

## Gamma Generation Pattern

Prepare the deck content as markdown:

```markdown
# Zapier + [Company Name] - [Call Type]
*Prepared for [Company Name] | [Date]*

---

## Agenda
1. Context
2. Current impact
3. Opportunities
4. Next steps

---

## [Slide Title]
[Concise slide content]
```

Then use Zapier MCP to run the Gamma create-generation action with:

- format: presentation
- card dimensions: 16x9
- tone: professional
- audience: business executive
- text amount: concise

Poll the Gamma generation status action until the presentation URL is available.

## Content Guidelines

- Lead with the customer outcome, not the data source.
- Use concrete numbers only when the source supports them.
- Make every slide useful in three seconds.
- Clean up technical app names before putting them on slides.
- Group workflow logic tools separately from external apps.
- Use plain language for task usage, feature adoption, renewal timing, and expansion opportunities.
- Flag any claims, product roadmap mentions, or customer references that need approval.

## Zapier MCP And SDK Role

- Use Zapier MCP to read approved CRM, account, usage, meeting, and document context.
- Use Zapier MCP to call Gamma generation and status actions.
- Use Zapier SDK when the workflow becomes repeatable: deck request intake, data snapshot logging, approval routing, and handoff tracking.

## Guardrails

- Do not include raw SQL, internal table names, private notes, emails, or internal IDs in customer-facing slides.
- Do not use unapproved customer names, quotes, logos, or metrics.
- Do not share a generated deck externally until a human has reviewed the content.
- Do not write back to CRM, create customer messages, or publish assets without approval.
