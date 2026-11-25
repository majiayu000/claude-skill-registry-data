---
name: x-growth-playbook
description: X Growth Playbook. Analyse a person's own X (Twitter) posts and tell them what to post next, with the numbers behind every claim. Compares quote posts vs originals, links vs no links, short vs long, time of day in their timezone, media vs text and the topics they name, reports medians with n, then writes a 10-step plan and the next 7 posts in their voice. Use when the user says "analyse my X posts", "what works on my Twitter", "how do I grow on X", "what should I post next on X", "audit my X account", or shares an X data archive, X API export or a list of their posts. Runs on the user's computer.
---

# X Growth Playbook

Method by Federico De Ponte.

Turn a person's own X posts into a short, honest account of what works for them, then a plan and the next 7 posts. The reader is usually a founder building in public, not an analyst. Plain words, short sentences.

The plan comes only from the user's own numbers. Federico's run in `references/worked-example.md` shows the shape of a good answer. His numbers are not targets and not benchmarks: never tell a user that something works because it worked for him.

## Step 1: Get the posts

Ask which of these the user has, in this order, and use the first one available:

1. **X API keys.** If they have a bearer token, run the fetcher. The token goes in the environment, never in the chat or the command line arguments. X may bill API reads on their developer plan: say so and get a yes first.
   ```bash
   X_BEARER_TOKEN=... python3 scripts/fetch_x_posts.py <their username> --out posts.json
   ```
   This gives impressions for up to 3,200 recent posts and their current follower count.
2. **The X data archive.** On X: Settings, Your account, Download an archive of your data. X emails a link, usually within a day or two. Use the zip or the unzipped folder. The archive has likes but no impressions per post, so the analysis measures reactions, not reach. Say this up front.
3. **Pasted posts or screenshots.** Ask for every post they can get, not only the good ones: date and time, text, impressions (views), likes, replies, reposts, and whether it was a quote, a reply or had an image or video. Write them into a CSV with a header row `date,text,impressions,likes,replies,reposts,kind,media` and use that. Read numbers off screenshots exactly; if a number is unreadable, leave the cell empty. Never fill gaps with guesses.

Then tell them once, before running anything: "The analysis runs on your computer. Your posts are not uploaded anywhere." (The API fetch reads from X; nothing else leaves the machine.)

Also ask two things the file does not hold:

- **Their timezone**, or their audience's if most of it lives elsewhere. Time of day is reported in that timezone.
- **Follower counts** at the start and end of any stretch they want to talk about. Follower history is not in any of these files.

## Step 2: Pick the topic names

Read the user's posts and pick 2 to 4 names they mention often enough to test: a tool, a company, a person, a product, a theme word. Each needs at least 5 top-level posts that mention it. Show the user the list and the matching pattern, and let them change it. Example: `--topic "Claude=claude|opus"`.

## Step 3: Run the report

```bash
python3 scripts/x_growth_report.py <input> --tz <Area/City> --topic "Name=pattern" [--topic ...] --out <folder>
```

- Needs Python 3.9 or newer, nothing else. The report script makes no network calls.
- Input: the fetcher's JSON, the archive zip or folder (or its `data/tweets.js`), or the CSV.
- Writes `report.md` and `report.json`. Read `report.md` fully before writing anything, starting with "Notes from reading the file": pass every note on to the user.

What the script computes, on original and quote posts only (replies are reported apart, reposts are dropped):

| Breakdown | Groups |
|---|---|
| Kind | quote posts vs original posts |
| Links | with an external link vs without one (media and quoted-post links do not count) |
| Length | under 140, 140 to 280, over 280 characters, counted the way X counts them |
| Time of day | 00:00-05:59, 06:00-11:59, 12:00-16:59, 17:00-23:59 in the given timezone |
| Media | image or video vs text only |
| Topics | mentions the name vs does not |

Plus: median for replies, the top 10 and bottom 5 posts, the most replied-to posts, the busiest 7 days and posts per week. Every number is a median per post, with its n and a flag when the group is small.

## Step 4: Read it

Write the findings in this order, one screen long:

1. **What is in the file.** Number of posts, date range, how many were replies, the metric used (impressions, or likes for an archive).
2. **The comparisons.** Each one as "A: median X (n = a) vs B: median Y (n = b)". Biggest gaps first.
3. **The single posts that carried the account.** From the top 10 and most-replied lists: what the top 3 have in common, in the user's own words. Mark these as single posts (n = 1): stories, not results.
4. **What did not matter.** Comparisons where the two medians are close. These are useful: they tell the user what to stop worrying about.
5. **Activity.** Busy weeks against their medians, and follower counts if the user gave them.
6. **What this file cannot tell you** (see below).

### Rules for every finding

- **State the n.** Every claim carries the number of posts behind it. A finding without an n is not allowed.
- **Small groups.** Under 5 posts: "too few posts to conclude anything (n = 3)", and move on. 5 to 9: a hint, not a result. The script flags both. Use its flags, do not soften them.
- **Medians, not totals.** One viral post can carry a total. Use the medians the script prints and do not do arithmetic by eye. If a group's best post is many times its median, say the median is the honest number.
- **Together, not because.** Groups overlap: quote posts may also be the ones that name a popular tool. Say "posts with X did better", never "X makes posts do better". Where two findings may be the same posts, say so.
- **Nothing from outside the file.** No "best time to post on X", no algorithm claims, no industry engagement rates, no generic tips. If a sentence would be true for any account, delete it.
- **Report, do not flatter.** If the file shows nothing clear, the finding is "nothing clear".

### What the file cannot tell you

Always say, in plain words:

- Who saw a post and why: impressions do not show where the views came from.
- Follower growth per post: none of these files hold it.
- With an archive: reach. Likes only measure reactions.
- Anything the script listed under "Notes from reading the file".

## Step 5: The 10-step plan

Write exactly 10 steps. Each step:

- one line saying what to do, in plain words;
- the finding behind it, with its numbers and n, copied from `report.md`;
- its strength: "result" (both groups 10 or more), "hint" (5 to 9) or "single post" (from the top-posts lists).

Order them by strength, then by size of the gap. Use the comparisons first, then the single posts, then activity. If the file supports fewer than 10 steps, write fewer and say why. Never pad the list with steps the file does not support. A "stop doing" step is valid when the data shows it (for example links in the post body doing worse).

## Step 6: The next 7 posts

Draft the next 7 posts in the user's voice:

- **Learn the voice from their own posts.** Read their top 10 and 10 typical posts. Copy their casing, line breaks, length, punctuation, emoji use and how they open a post. If they write in lowercase, so do you.
- **Each post applies one or more steps.** Label it, for example "applies steps 1 and 4".
- **Give each a day and a time** in their timezone, inside their best time bucket when it is a result or a hint.
- **No invented facts.** Use only things the user said or posted. Where a post needs a number, a name or an event you do not have, write a bracketed placeholder like `[your number]` and list what you need from them.
- **For quote posts,** say what kind of post to quote and why, and leave the target for them to pick.

## Step 7: Deliver

Give the findings, the plan and the 7 posts in the chat, and save them as `PLAYBOOK.md` next to `report.md`. Include the line "Method by Federico De Ponte." and the reminder that the analysis ran locally. Point to `report.md` for the full tables. Offer to rerun in a few weeks on the new posts to see whether the plan held.
