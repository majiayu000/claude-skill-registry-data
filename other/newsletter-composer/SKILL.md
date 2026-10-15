---
name: newsletter-composer
description: "Composes recurring newsletters (internal team or company updates, customer newsletters, community digests) from the items of the period: collects and filters the news, ranks it for the readers, writes a consistent issue with a lead story, short items, dates, and calls to action, applies the organization's brand and format rules, and produces a subject line and preview text. Use when the user wants to write, assemble, or schedule a weekly or monthly newsletter, team update, digest, or bulletin, or wants to turn a pile of updates into one readable issue."
---

# Newsletter Composer

You turn a period's worth of updates into one newsletter issue that people actually open and read. You decide what makes the cut, put the most relevant item first, keep every item short, and keep the format consistent from issue to issue. The facts come from the user, uploaded material, or connected tools and sources; you never fill a slow week with invented news.

## Set up the newsletter once

The first time, establish the newsletter's profile and reuse it for every issue. If the user has a previous issue, read the profile from it.

| Setting | Question | Example |
|---|---|---|
| **Readers** | Who gets it, and what do they care about? | All employees; engineering team; customers on the Pro plan |
| **Purpose** | Why does it exist? | Keep a distributed team aligned; drive feature adoption |
| **Cadence and period** | Weekly, biweekly, monthly; which dates does an issue cover? | Weekly, Monday to Friday |
| **Length** | Minutes to read, or number of items | 3-minute read; 1 lead + 5 short items |
| **Fixed sections** | Which sections appear every time, in what order? | Lead story, Shipped, People, Dates, Kudos |
| **Voice and brand** | Brand guidelines, tone, words to avoid, language(s) | Friendly, informal du-form in German edition |
| **Channel** | Email, intranet page, chat post, PDF | Email with intranet archive link |
| **Sign-off** | Who sends it, how it ends | "— The People Team" |

Write the profile down as a short block at the top of your first answer, so the user can save it (as a prompt, a file, or in the scheduled task's instructions) and reuse it.

## Step 1 — Collect the items

Gather candidate items for the period from:

| Source | Examples |
|---|---|
| Material the user provides | Notes, bullet lists, forwarded announcements, documents |
| Connected tools and sources | Release notes, tracker updates, wiki or intranet changes, team chat channels, calendar of upcoming events, CRM or support highlights |
| Recurring inputs | Standing sections such as new joiners, anniversaries, or upcoming dates, if the user supplies them |

List every candidate with its source and date. Drop anything outside the period unless it is an upcoming date.

## Step 2 — Select and rank

Score each candidate quickly:

| Criterion | Question |
|---|---|
| **Relevance** | Does it affect most readers, or only a few? |
| **Actionability** | Do readers need to do, decide, or attend something? |
| **Novelty** | Is it new to them, or already announced elsewhere? |
| **Timeliness** | Does it lose value if it waits until the next issue? |

Then:

- **Pick one lead story:** the item with the most relevance and actionability. If nothing qualifies, lead with the most useful short item, not with filler.
- **Fit the length budget.** Cut, merge, or move items to "More links" rather than exceeding the agreed length.
- **Keep sections consistent.** If a fixed section has nothing this period, either drop it for this issue or write one honest line ("No new releases this week — the next one lands on 14 May."). Ask the user which they prefer, then keep doing it that way.
- Show the user the cut list (what you left out and why) in one compact line per item.

## Step 3 — Write the issue

Use this structure, adapted to the fixed sections in the profile:

```
Subject: [specific, ≤ 50 characters, names the lead story]
Preview text: [≤ 90 characters that add to the subject, not repeat it]

# [Newsletter name] — [period or issue number]

[1–2 sentence intro: the one thing to know this week]

## [Lead story headline: what happened and why it matters]
[60–120 words: what, why it matters for the reader, what to do]
→ [Call to action with link or contact]

## [Section name]
- **[Item headline]** — [1–2 sentences]. [Link]
- ...

## Dates
| When | What | Where / how to join |
|---|---|---|

## [Optional: Kudos / People / Tip of the week]

[Sign-off]
```

Writing rules:

- **Headlines say what happened**, not just the topic: "Expense tool switches to the new form on 1 June" beats "Expense tool update".
- **Lead with the reader's impact.** "You can now…" or "From Monday you need to…" before background.
- **One idea per item, two sentences at most.** Link out for detail.
- **Every call to action is specific:** what, by when, and where.
- **Dates and numbers are exact**, with time zones for events across sites.
- **Names and credit are accurate.** Only name people who appear in the source material.
- Write in the newsletter's language(s). For bilingual editions, produce both versions with the same structure.

## Step 4 — Check before sending

| Check | Pass when |
|---|---|
| Period | Every news item falls inside the period; dates are in the future for "Dates" |
| Facts | Every item traces back to a source; no invented figures or quotes |
| Length | Within the agreed budget |
| Links and CTAs | Each one has a target or a clear `[Link required]` placeholder |
| Consistency | Same section order, naming, and sign-off as previous issues |
| Brand and tone | Matches the profile and any brand guidelines in use |
| Sensitive content | No confidential, personal, or unreleased information for this audience |

## Running on a schedule

Newsletters suit scheduled tasks well: for example, a task every Friday at 10:00 that drafts next week's issue from the connected sources. When you run without a person watching:

- Do not ask questions. Use the profile from the task instructions or the last issue, and list any open points at the top of the draft under **"Needs your input"**.
- Produce a **draft for review**, never a sent newsletter, unless the task's instructions and tools explicitly provide for sending.
- Use the run's date to determine the period (for a weekly issue, the seven days before the run).
- If there are too few items to make an issue, write a short note saying so, with the items you did find, instead of padding.

## Combining with other skills

- **Brand Voice Framework** (or the organization's brand guidelines) sets tone and wording rules. Apply them over your defaults.
- **Match My Writing Style** makes the intro and sign-off sound like the sender.
- **Activity Roundup** is useful for collecting the raw items across tools before Step 2.
- **Product Update Communicator** is the better fit when the issue is a single product release announcement.

## Ground rules

- Never invent news, numbers, quotes, people, or events. Use `[Input required]` and list open points at the top.
- Respect the audience boundary: internal details never go into external editions.
- Don't include personal data (birthdays, health, family news) unless the user confirms it is approved for the newsletter.
- Mark what comes from where in the review draft: `[From your notes]`, `[Via connected tool]`, `[My suggestion]`, and `[Input required]`. Remove the markers in the final version once the user approves.
