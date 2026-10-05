---
name: cx-tag-taxonomy-hygiene
description: Use to clean up sprawling helpdesk tags, categories and custom fields so reporting built on them means something. Trigger for "our tags are a mess", "consolidate our ticket categories", "why don't our tag reports add up", duplicate or near-duplicate tags, tags nobody uses, agents tagging inconsistently, or before building reporting on top of tags.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Tag and category hygiene

Tag sprawl is the normal end state of any helpdesk more than a year old. Free-text
tagging, several people with admin rights, campaign tags nobody removed, and three
spellings of the same concept.

The reason to fix it is not tidiness. It is that **every report built on tags inherits
their inconsistency**, usually without saying so, and the resulting numbers are quietly
wrong in ways nobody can see from the chart.

## Measure the damage first

Before proposing anything, quantify:

- **Tag count versus meaningfully-used tag count** — how many are applied more than a
  handful of times. The gap is usually enormous and is the argument for doing the work.
- **Tags per conversation.** A rising average means agents are hedging because they
  cannot find the right one.
- **Untagged share.** If a third of conversations carry no tag, tag-based reporting
  describes a self-selected two-thirds. This single number often invalidates a report
  someone is already using.
- **The near-duplicate clusters**: case variants, singular/plural, hyphen/underscore,
  abbreviations, translations, misspellings, and `payment_issue` next to `payment-issues`
  next to `Payments`.
- **Concurrent-lifetime overlap.** Two tags that were both actively applied in the same
  period are genuine duplicates. Two where one stopped when the other started are a
  rename, and merging them without noticing creates a false step change in every
  historical series.

## Decide what tags are for

Most sprawl comes from one taxonomy trying to do several jobs at once. Separate them,
because they have different owners, lifespans and rules:

- **What the contact was about** — the contact driver. Should be a controlled,
  mutually exclusive list, and it is what most reporting actually wants.
- **What happened to it** — escalated, refunded, bug-linked. Workflow state.
- **Attributes** — VIP, vulnerable customer, regulated, language.
- **Temporary markers** — a campaign, an incident, an experiment. **These need an expiry
  date at creation**, and their absence is the largest single source of sprawl.

Trying to encode all four in one flat tag list is why the list is unmanageable.

A contact-driver taxonomy in particular has its own design problems — deriving
categories that name a removable cause rather than a topic, and keeping the "Other"
rate honest — which are a bigger question than tag hygiene. Hygiene is about making the
mechanism reliable; taxonomy design is about making the categories worth reporting.

## Rules that keep it clean

- **Controlled list, not free text**, for anything used in reporting. Free-text tags are
  a reporting dead end from the first day.
- **One naming convention**, mechanically enforced: case, separator, singular or plural.
  Pick and apply.
- **Mutually exclusive within a dimension.** A conversation should carry exactly one
  contact driver. Multiple drivers means the reporting cannot sum, and every percentage
  built on it is over 100 or arbitrarily attributed.
- **Every tag has an owner and a definition.** A tag whose meaning is folklore will be
  applied inconsistently within a month, and the definition needs to be visible where
  agents tag, not in a document.
- **Expiry dates on temporary tags**, enforced by review.
- **A creation gate.** If anyone can create a tag from the ticket view, the list grows
  without bound. If nobody can, agents will use the nearest wrong tag. The workable
  middle is a request path with a fast turnaround plus a visible "suggest a tag"
  channel — and treat frequent requests as evidence the taxonomy has a gap.

## Consolidating without breaking history

This is the part that goes wrong.

**Merging tags rewrites history.** After merging `payment-issue` into `payments`, last
quarter's report of `payments` changes. Anyone comparing to a previously published
figure will find a discrepancy and lose confidence in the reporting.

So:

- **Map, do not just merge.** Keep a documented mapping from old tags to new, with the
  date it took effect.
- **Prefer a reporting-layer mapping to a destructive retag** where you can. It is
  reversible; a bulk retag usually is not.
- **If you do retag, treat it as a reviewed mutation** — a plan reviewed before it runs,
  a bounded batch size, an audit record per change, and the ability to resume. Bulk
  tag operations across a helpdesk are rarely reversible and frequently trigger
  automations and triggers as a side effect. Check what fires before running anything.
- **Announce the change**, with the date and the mapping, and mark it on dashboards.
- **Do not retag historical conversations to match a new taxonomy** unless you have a
  strong reason. Historical tags record what someone thought at the time, which is
  itself information — and a retro-fitted taxonomy makes a trend look like it always
  existed.

## Improving tagging behaviour

Tag quality is mostly a design problem, not a compliance problem:

- **Fewer options tagged correctly beat more options tagged badly.**
- **Put the definition where the agent tags**, not in a wiki.
- **Do not make tagging a QA criterion** without checking the tag list is usable first.
  Penalising agents for a broken taxonomy produces tagging that is compliant and
  meaningless.
- **Automate what can be automated** — channel, language, and attributes derivable from
  the record should never be typed by a human.
- **Audit agreement periodically**: have two people tag the same conversations
  independently and measure how often they match. Low agreement means the categories
  overlap, and that is a taxonomy fix, not a training fix.

## Present results to the user

1. **The damage** — tag count vs used count, tags per conversation, untagged share,
   duplicate clusters. Lead with the untagged share, because it bounds every existing
   report.
2. **The four dimensions**, and which of them the current list is conflating.
3. **A proposed consolidated list**, with definitions and owners.
4. **The mapping** from current tags to proposed, flagging renames versus true
   duplicates by their concurrent-lifetime overlap.
5. **The impact on existing reports** — which series change and by how much.
6. **The migration plan**, stating what is reversible and what is not, and what
   automations the change would trigger.
7. **Governance** — creation gate, expiry policy, review cadence, and who owns it.
