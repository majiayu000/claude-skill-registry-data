---
name: reach-warm-path-check
description: Checks each account for a warm path from your own connections export, inbox and notes, with who you already know there, how well you know them in your own words and a verdict per account. Use for "run reach-warm-path-check", "warm path check", "who do I know at this company", "check my connections", "warm before cold", "can someone introduce me", "do I know anyone there", "use my LinkedIn export", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Warm Path Check

## When To Use
You are about to write cold to a company where a former colleague works, and you do not know it. Run this on every account before any cold message. It answers: do I already know someone here, or someone who does, and is that a better way in?

## When Not To Use
If you have no accounts chosen yet, run Target Account List first; this check works account by account. It does not find new people at the organisation: for publicly named roles you do not know, use Contact Shortlist.

## Inputs
- Your account list, with the organisations you kept.
- Your own connections file from the data export LinkedIn lets every member request (LinkedIn Help, "Download your account data"), pasted or uploaded. You download it yourself.
- Optional: the Gmail connector, used to search and read your own past threads by organisation name. It never drafts or sends.
- Your own notes on former colleagues, clients and people you met.
If you have none of this, I start from the account names and what you remember, and mark every row "from memory, to check".

## Approach
Warm before cold, from your own data: the fastest research is finding out you already know someone. I match your accounts against your own records and make a first guess at how well you know each person from real exchange; you correct every guess, because a message count says little about a relationship. Nothing is fetched from LinkedIn and nothing there is automated; you bring the export. The failure it prevents is the cold pitch to a director whose colleague you worked beside for three years.

## Workflow
1. Ask at most three questions: which accounts to check, what you can share (export, inbox search, notes), and whether former employees of an account count as a path for you.
2. Match by organisation: people in your records who work at each account now, and people who used to. Show where each match came from (export row, thread, your notes).
3. Make a first closeness guess from real exchange only: several exchanges, a few, one, none. It is a guess about contact, not a view of the person.
4. You correct it in plain words: "I could call them tomorrow", "we know each other, not deeply", "connected, but I barely know them", "I would not recognise them". Your words replace my guess.
5. Keep at most three names per account, so one organisation does not fill your week. Closeness says how well you know someone, never how useful they are.
6. Give a verdict per account, for you to confirm: ask for an introduction (someone you know well is there or knows the person), write directly (you know the person a little), or cold with a trigger (no path found).
7. Write "no path found" as a fact, not a flaw. It tells you this account needs a real trigger before any message.

## Output Format
```markdown
# Warm Path Check
Accounts checked: [number] | Sources used: [connections export / inbox search / your notes] | Date: [date]
## Paths per account
| Account | Who you know (there now or formerly) | Found in | How well you know them (your words) | Verdict (you confirm) |
|---|---|---|---|---|
| [organisation] | [name, or "no path found"] | [export / thread on date / notes] | [your words] | [ask for an introduction / write directly / cold with a trigger] |
## To check from memory
- [name or account you think you know someone at, with nothing in the records]
## Not used
- [matches set aside, and why: namesake, left long ago, you would rather not ask]
## Decision
[Your name] confirms the verdict for each account and decides who to ask for an introduction first, by [date].
```

## Done When
- Every account has a row, "no path found" included.
- Every closeness line is in your words and confirmed by you.
- Each match shows where it came from.
- No account has more than three names.

## Quality Bar
- Your own data only: your export, your inbox, your notes. Nothing is looked up on LinkedIn.
- Inbox search reads who and when; message text is not copied into the check.
- Closeness describes how well you know someone. It is never a rating of the person.
- An introduction is asked for, never assumed: the person you know decides whether to make it.
- Warm before cold, from your own data; you choose who to ask and you write to them yourself.

## Next
Run reach-company-fact-list (Company Fact List) to collect sourced facts about the first account you will work.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
