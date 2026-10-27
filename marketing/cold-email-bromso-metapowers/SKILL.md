---
name: cold-email
description: Create cold outbound email campaigns — ICP and targeting, a three-to-five email sequence with personalization, subject lines and compliance notes. Use when the user wants to reach prospects who have never heard of them and book meetings by email. Not for emails to existing subscribers or users; see /marketing:email-sequence.
argument-hint: "[project] [--skip-checks]"
---

# Cold Email

Design cold outbound email campaigns for "$ARGUMENTS". Create personalized email templates, follow-up sequences, and targeting criteria.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.metapowers/marketing/<project>/skip-log.md`: `- <ISO timestamp> — <skill name> skipped prerequisite check for <artifact file> — reason: <reason or "none given">`.

## Prerequisites

Read `.metapowers/marketing/<project>/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "<project>". Run `/marketing:customer-research <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/<project>/00-strategy.md` for audience and value proposition
   - Read `${CLAUDE_PLUGIN_ROOT}/shared/campaign-plan-template.md` for structure

2. **Define targeting criteria:**
   - Ideal customer profile (ICP) for outbound
   - Company firmographics: size, industry, tech stack, growth signals
   - Contact persona: title, department, seniority
   - Intent signals: hiring, funding, tech changes, content engagement

3. **Design email sequence:**
   - 3-5 email sequence with timing (typically days 1, 3, 7, 14)
   - Each email: different angle or value prop
   - Personalization strategy: what's personalized per recipient?
   - Follow-up logic: when to stop, when to escalate

4. **Write email templates:**
   - For each email: subject line (2-3 variants), body, CTA
   - Keep emails short (under 150 words)
   - Lead with relevance, not pitch
   - Include specific personalization placeholders
   - Compliance: include opt-out, identify sender, no deceptive subjects

5. **Write the artifact** — append to `.metapowers/marketing/<project>/03-convert.md` under a `## Cold Email` section. Create the file with a `# Convert — <project>` heading if it does not exist; if a `## Cold Email` section already exists, replace only that section. The section contains:
   - **ICP & Targeting** — who to target and why
   - **Sequence Design** — timing and logic
   - **Email Templates** — full copy for each email
   - **Personalization Guide** — what to customize per recipient
   - **Compliance Notes** — CAN-SPAM, GDPR requirements

## Output

Cold email strategy appended to `.metapowers/marketing/<project>/03-convert.md`. Present the full email sequence for review.
