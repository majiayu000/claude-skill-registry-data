---
name: cx-macro-audit
description: Use to audit canned responses, macros, templates and saved replies for staleness, contradictions, overuse and gaps. Trigger for "audit our macros", "are our canned responses up to date", "which templates do agents actually use", macro sprawl, template cleanup, conflicting saved replies, or before migrating macros to a new helpdesk.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Auditing macros and templates

Macros are the highest-leverage content in a support operation and the least
maintained. One stale macro sends a wrong answer hundreds of times before anyone
notices — and because it is consistent, it does not look like an error. It looks like
policy.

That is the reason this audit matters more than its unglamorous framing suggests: **a
wrong macro is the most efficient way an organisation has of being uniformly wrong**,
and it is invisible to per-agent QA, which sees consistent behaviour and passes it.

## Start from usage, not from the list

Most macro libraries have hundreds of entries and a small number that do nearly all the
work. Pull usage counts first and the audit prioritises itself.

Expect roughly:

- **A short head** — a handful of macros covering most sends. **Audit these first and
  most carefully.** An error here has already reached thousands of customers.
- **A long tail of near-zero usage** — candidates for deletion, and worth checking for
  duplicates of the head.
- **A dead middle** — created for a campaign or a situation that has passed.

If your helpdesk does not record macro usage, detect it by matching distinctive phrases
from macro bodies against sent messages. Report the match rate so the reader knows how
complete the usage picture is.

## What to check on the head

**1. Factual currency.** Every claim — fee, timeline, eligibility, process step, link —
verified against current policy. Check the last-edited date against the last policy
change on that topic; a macro older than the policy it describes is the finding.

**2. Contradictions between macros.** Two macros answering the same question
differently is worse than either being wrong alone, because which answer a customer
gets depends on which agent they reach. Group macros by topic and compare. This is the
check that most often finds something serious and is almost never run.

**3. Dead links and stale references.** Links to retired pages, removed features,
deprecated forms, or an old brand name.

**4. Placeholders that leak.** Unfilled variables reaching customers as `{{first_name}}`
or, worse, a placeholder that silently renders as blank mid-sentence. Search sent
messages for template syntax and for the tell-tale double spaces and orphaned commas a
blank substitution leaves.

**5. Tone and reading level** against the team's documented standard, and whether the
macro still sounds like the current brand. Macros calcify a voice from years ago.

**6. Compliance content.** Required disclosures present and current, and no macro
making a commitment or giving regulated advice it should not.

**7. Localisation currency.** Where macros are translated, check the translations were
updated when the source changed. A source macro edited and its translations left behind
is extremely common and means non-English markets are running the old policy.

## Usage pattern findings

The way macros are used is as informative as their content:

- **A macro used far more than the volume of its topic** suggests it is being applied to
  situations it does not fit — agents reaching for the nearest thing.
- **Heavy editing before send**, where you can detect it, means the macro is close but
  wrong. That is a rewrite candidate with the correction already written by the agents.
- **A high-volume contact driver with no macro** is the clearest gap. Cross-reference
  the contact-driver ranking against macro coverage; the uncovered high-volume drivers
  are the highest-value additions.
- **Macros used almost exclusively by one agent** are personal shortcuts. Either promote
  them or accept that the library is not the real source of answers.
- **Macros sent as a first response and followed by a repeat contact** are candidates
  for being unhelpful. Link macro usage to repeat-contact rate where you can; a macro
  with a materially higher repeat rate than the topic average is not resolving anything.

## Deletion is the point

An oversized library is itself the problem: agents cannot find the right macro, so they
improvise or reuse the nearest, and consistency collapses. A library that has doubled
in size has usually got worse.

Recommend deletion aggressively for the tail, but:

- **Check for seasonal use** before deleting something unused for months.
- **Deletion is often irreversible** in helpdesk configuration, and it may break
  automations, triggers or workflows that reference the macro. Check references first,
  export the current definitions before changing anything, and treat bulk deletion as a
  reviewed change with a plan rather than a cleanup task.
- **Prefer deactivating to deleting** where the platform supports it.

## Traps

- **Macro text is not what the customer received.** Agents edit before sending, and
  variables substitute. Audit the macro *and* a sample of sent messages that used it.
- **Personal or team-scoped macros** may not appear in an admin list. Ask.
- **Automation-sent templates** — triggers, autoresponders, satisfaction emails — are
  usually a separate object type and are audited even less often. Include them; they
  send at higher volume than any human-used macro.
- **Do not judge a macro purely on tone.** A blunt, correct, well-used macro beats a
  warm one that misstates a fee.

## Present results to the user

1. **Usage distribution** — how concentrated the library is, and the coverage of your
   usage data.
2. **Findings on the high-usage head**, worst first, with an estimate of how many
   customers each error has already reached. That estimate is what gets these fixed.
3. **Contradictions**, grouped by topic.
4. **Gaps** — high-volume drivers with no macro.
5. **Localisation drift** — translations older than their source.
6. **Deletion candidates**, with reference checks and a note on reversibility.
7. **Rewrite candidates**, prioritised by usage × severity, with the agent edits as
   evidence where available.
