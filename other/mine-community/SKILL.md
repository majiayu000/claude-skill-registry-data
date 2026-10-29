---
name: mine-community
description: Harvest a founder community (a subreddit, a forum, a newsletter archive) for what is actually working in app marketing, pricing, ASO and growth, then filter it honestly and file the few findings worth keeping. Drops milestone and promotional posts, keeps only claims that either converge with an unrelated source or contradict something the project already believes, and ranks the survivors against the app's real stage. Use when the user wants to learn from other founders, asks what is working for other people, says "mine r/<something>", "what are other indie devs doing", "find the best tips from this community", or pastes a community link and asks whether it is useful.
---

# Mine a community

Founder communities are full of people describing what worked for them. Most of
it is noise, some of it is advertising, and a little of it is the most useful
input available to someone running an app alone. This turns a community into a
few findings worth acting on, and throws the rest away.

This is not the research skill. Research answers a question you already have.
This reads a room and tells you which few things in it apply to you.

## The honesty rules

These exist because the failure mode here is confident nonsense, and it is
expensive: a founder spends a week on a tactic that never worked for anyone.

**Everything is a claim, not a measurement.** Nobody in a community posts
audited numbers. A revenue screenshot is a screenshot. Write "a dev reports",
never "it is proven that".

**Assume survivorship bias, and say so out loud.** A top posts listing from a
founder community is a sample of winners and self promoters. The people whose
identical tactic produced nothing do not post. Count the failures in your
sample and put the number in the output. If it is near zero, the sample cannot
tell you a tactic's success rate, only that the tactic sometimes works.

**Flag the posts that are themselves marketing.** A long tactical post that ends
with a link to the author's own tool is an advertisement with data attached. It
can still be useful. Say which ones they are.

**A claim earns its place by convergence or contradiction.** Keep a finding when
either:

- two unrelated sources reach it independently, especially when one of them is
  the project's own existing research, or
- it contradicts something the project currently believes, in which case say so
  plainly and do not resolve it by picking the newer source.

Everything else is interesting reading and does not go in the output.

**Never carry a number across from a different app's situation.** Someone's 20%
conversion at 50,000 followers says nothing about a conversion rate at 15 daily
users. Report the mechanism, not the multiplier.

## 1. Know the user's stage before reading anything

Findings are only rankable against a real situation. Read the project's rules
file, goals file and research folder, and write down in one line each:

- roughly how many people use the app now, and how many arrive a month
- which channels have already been tried, and what the project concluded
- what the project has already decided and closed

That last one matters most. A community will cheerfully recommend something the
user has already tried and rejected, and repeating it reads as not listening.
Standing decisions in the rules file are closed. Say when a finding touches one,
and do not reopen it.

## 2. Get the posts

Prefer whatever the user can give you with least effort. In order:

1. **The public feed, which costs the user nothing.** A forum that refuses its
   JSON API to scripts often still publishes a feed that answers them fine, so
   try the feed before asking a person to do anything. For Reddit, `/.json`
   answers a script 403 whatever user agent it sends, while the Atom feed answers
   200 and carries the full post body:

   ```
   https://www.reddit.com/r/<subreddit>/top/.rss?t=year
   ```

   Parse each `<entry>` for `title`, `content` (the body, as HTML), `author`,
   `published` and the entry link. Checked 2026-10-19.

   Two limits decide what you may conclude from it. A feed returns **at most 25
   entries**, so breadth comes from running several windows (`t=week`, `month`,
   `year`, `all`) and merging them, not from asking for a bigger page. And it
   carries **no score and no comment count**, so ranking is position within its
   window, and nothing you write can be weighted by votes. Say so in the output.

   It is rate limited hard enough that a handful of requests in a minute earns a
   429, so pace a few seconds between windows and back off when refused.

2. **The user saves the page**, when there is no feed, or when you need the
   scores. A signed in browser is served the JSON a script is refused, so give
   them the URL and ask them to save the file:

   ```
   https://www.reddit.com/r/<subreddit>/top/.json?t=year&limit=100
   ```

   Then parse `data.children[].data` for `title`, `selftext`, `score`,
   `num_comments` and `created_utc`.

3. **A web search**, when the community is indexed and you only want a sample.
   Weaker, since you get what is quoted elsewhere rather than what the community
   upvoted.

4. **The user pastes posts.** Fine, and often better, since they filter the
   obvious junk first.

Do not install a scraper, and do not send the user through an API approval queue
to read a forum. Reading a public feed is not that, and a few lines that fetch
one are worth leaving behind when the user wants the harvest to repeat. If the
easy routes fail, say so and ask for pastes.

Respect each community's terms. Read what is public, do not republish it
wholesale, and quote only what you cite.

## 3. Drop the noise before reading

In a founder community most posts are celebrations with no content: a revenue
screenshot and a sentence. They carry the community's mood, not its knowledge.

- Drop anything whose body is under roughly 1,000 characters. In one Reddit
  harvest this left 40 of 100 posts and lost nothing.
- Keep the long ones regardless of score. A detailed post at 90 points usually
  beats a celebration at 500.
- Read the titles of everything you dropped once, in a list. The pattern of what
  people celebrate is itself a finding, and it is free.

## 4. Read for mechanisms

For each surviving post, pull out only:

- **The mechanism**: what the person actually did, in enough detail to copy.
  "Ten image carousels a day, confession framing, the app never named in the
  post" is a mechanism. "Posted engaging content" is not.
- **The claimed result**, with its timeframe, quoted.
- **What it cost**: money, hours a week, and whether it needs a skill the user
  does not have.
- **Whether the post is selling something.**

Quote the exact words for anything that will be acted on. Paraphrase loses the
detail that makes a tactic reproducible.

## 5. Rank for this user, not in the abstract

Order the survivors by what the user can act on now:

1. Converges with the project's own research, and is cheap at the user's size.
2. Converges, but costs real money or a skill they do not have.
3. Contradicts something the project believes, and is worth sitting with.
4. Works only at a size the user is not at yet. Say when it becomes relevant.

Mark anything that touches a standing decision. Name the decision, say the
finding exists, and leave it closed.

## 6. Answer in chat

Short. Lead with the single most useful finding, not with the method.

```
<N> posts, <date range>. <M> had real content; the rest were milestone posts.
Caveat: <survivorship, and how many of the substantive posts are selling something>.

The finding worth the harvest: <one paragraph, with the quote>

Ranked for where you are:
1. <mechanism> <what it costs> <what it converges with>
2. ...

Confirms what you already decided: <one line each>
Contradiction worth sitting with: <one, or none>
Saved: <path>
```

## 7. File it

Write a dated doc in the project's research folder, following whatever naming
the project already uses. It must carry:

- the date, the source, the sample size and the date range of the posts
- the honesty caveats from the top of this skill, in the doc, not just in chat
- the quotes, since the next reader cannot re run the harvest
- which findings converge with which existing project docs, by filename
- the method, so the harvest can be repeated without rediscovering it

Then add the project's usual one line index entry wherever research docs are
indexed, with the headline finding in it rather than a description of the topic.

## What this skill will not do

- It will not turn a community into a strategy. It produces inputs to a decision
  the user makes.
- It will not rank a channel by how often it is mentioned. Popularity inside a
  community measures the community, not the channel.
- It will not recommend a tactic the project has already tried and rejected,
  however many people are recommending it this month.
