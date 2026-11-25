---
name: linkedin-year-audit
description: LinkedIn Year Audit. Analyse a person's own LinkedIn analytics export (the AggregateAnalytics .xlsx file from LinkedIn creator analytics) and report what worked, with the numbers behind every claim. Use when the user says "analyse my LinkedIn analytics export", "what worked on my LinkedIn this year", "audit my LinkedIn", "review my LinkedIn posts or numbers", "which of my posts performed best", or shares an AggregateAnalytics xlsx file. Runs fully on the user's computer.
---

# LinkedIn Year Audit

Method by Federico De Ponte.

Turn a LinkedIn analytics export into a short, honest account of what worked: totals, growth, how concentrated the results are, which themes travel and which get reactions. The reader is usually a founder or solopreneur, not an analyst. Write in plain words and short sentences.

## Step 1: Get the file

If the user has not shared the export yet, tell them how to get it in these two sentences:

> On a computer, open LinkedIn, go to Analytics, then Content, set the date range to the past 365 days and click Export. LinkedIn downloads a file named `AggregateAnalytics_<your name>_<dates>.xlsx`: tell me where it is saved.

Then tell them once, before running anything: "Everything runs on your computer. Your file is not uploaded anywhere."

If they say it is in Downloads, look for `AggregateAnalytics_*.xlsx` there and confirm the file name with them before using it.

## Step 2: Run the script

```bash
python3 scripts/linkedin_year_audit.py "<path to export.xlsx>" --out "<output folder>"
```

- Needs Python 3 and `openpyxl`. If it is missing: `python3 -m pip install openpyxl`.
- Writes `report.md` (readable) and `report.json` (same numbers, plus post ids and links). Default output folder: `linkedin-year-audit-output` next to the export.
- The script makes no network calls. Do not paste the user's file or numbers into any online tool.
- Read `report.md` fully before writing anything. Read the "Notes from reading the file" section first if it exists: it lists missing sheets, guessed date formats and other caveats that must be passed on to the user.

What the export contains, and what the script does with it:

| Sheet | Content | Used for |
|---|---|---|
| DISCOVERY | total impressions, members reached | totals |
| ENGAGEMENT | daily impressions and engagements | monthly table |
| TOP POSTS | two tables, at most 50 posts each: by engagements, by impressions (link, date, one number) | everything about posts |
| FOLLOWERS | followers on the end date, daily new followers | follower growth |
| DEMOGRAPHICS (two sheets) | audience percentages | not used |

There is no post text in the export. The script recovers a "hook" from each post link, which keeps only the first few words of the post, lowercased and without punctuation. Treat hooks as clues, not as the post.

## Step 3: Label themes

Give every post in the report exactly one theme, judged from its hook only:

- **personal story**: something that happened to the author (first person, an event, a person they met)
- **bold claim / comparison**: an opinion, a prediction, a provocative statement, X versus Y
- **milestone**: a number or result reached (revenue, signed deals, followers, stats)
- **launch / announcement**: launching, introducing, joining, leaving, a deadline
- **list**: a list of things, tools, companies, lessons
- **other / unclear**: anything else, and every hook too short or vague to judge

Rules:

- When a hook could fit two themes, or is one or two words, use "other / unclear". Do not guess from what the product or person might be.
- Show the user the labels in a compact table and ask them to correct any they know to be wrong. They know their posts, the file does not. If they do not want to check, continue and say the labels are your reading of cut-off hooks.
- Save the labels as a JSON file mapping post id (from `report.json`) to theme, then run the script again with `--themes <file>`. This adds a themes table with n, impressions, medians, and how many posts of each theme sit in the top 10 of each ranking. Use these computed numbers. Do not do the arithmetic by eye.

## Step 4: Interpret

Write the findings in this order. Keep it to one page.

1. **The year in numbers.** Impressions, members reached, followers at the start and now, the multiple. Monthly trend in one or two sentences. Never compare a partial month with a full one.
2. **Concentration.** What share of all impressions came from the listed top posts, the top 10 and the top 1. Say what that means in plain words (for example how much of the year rests on a handful of posts).
3. **Themes that travel versus themes that get reactions.** "Travel" = impressions. "Reactions" = engagements and engagement rate. Report each theme with its n. These are often different themes: say so when they are.
4. **Mismatches.** Posts with many reactions but modest reach, and posts with reach but few reactions. Look for what the posts in each group have in common. If nothing obvious, say that.
5. **Timing, last.** Publish month, then weekday. Weekday is almost never readable from this file: a handful of posts per day and only winners. Check it last and expect to write "nothing to conclude".
6. **What this file cannot tell you.** Always include this (see below).
7. **Do more / stop.** Two short lists in plain words (see below).

### Rules for every finding

- **State the n.** Every claim carries the number of posts behind it: "personal stories (n = 14) brought ...". A finding without an n is not allowed.
- **Small buckets.** With fewer than 5 posts in a bucket, write "too few posts to conclude anything (n = 3)" and move on. The script marks these. With 5 to 10, call it a hint, not a result. One outlier post can carry a whole bucket: check the median as well as the total, and say when the total depends on one post.
- **Only winners are in the file.** A theme being common among top posts does not prove it works better: it may simply be what the user posts most. Say this when it applies.
- **Nothing from outside the file.** No benchmarks, no "good engagement rate is X", no best time to post, no algorithm claims, no generic LinkedIn tips. If a sentence would be true for any account, delete it.
- **Report, do not flatter.** No hype words. If the file shows nothing clear, the finding is "nothing clear".
- **Hooks are cut off.** Quote hooks as they appear in the report or as the user corrects them. Never complete a hook or describe what a post "was about" beyond the words shown.

### What the export cannot tell you

Always tell the user, in plain words:

- No flops: only the top posts are listed (at most 50 per ranking), so the file cannot show what failed or how many posts were published.
- No text, format or time of day: only the first words from the link.
- No breakdown of engagement into likes, comments and reposts.
- Whatever the script noted while reading the file.

Then offer the deeper pass once: "If you paste or share your full post list with numbers (every post with its text, date, impressions and reactions), I can also show what flopped and how often each theme works, not just its best cases." If they provide it, repeat steps 3 and 4 on the full list: compare each theme's share of all posts with its share of the top posts, report the bottom posts, and keep the same rules on n. Keep that data local too.

### Do more / stop

End with two short lists, each item tied to a finding and its n:

- **Do more:** only things the file supports with at least 5 posts.
- **Stop:** only things the file supports. The export hides weak posts, so a real stop list is usually not possible without the full post list. Say that plainly instead of inventing one. Valid stop items from the export alone are things like "stop choosing the posting day based on this data".

If the two goals pull apart (one theme brings reach, another brings reactions), say so and let the user choose: do not pick for them.

## Step 5: Deliver

Give the findings in the chat, and save them as `FINDINGS.md` next to `report.md`. Include the line "Method by Federico De Ponte." and the reminder that the analysis ran locally. Point to `report.md` for the full tables.
