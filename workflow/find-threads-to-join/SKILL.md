---
name: find-threads-to-join
description: Get a short ranked list of LinkedIn or X posts worth commenting on today, from the people you track, with two ready-to-paste comments for each in your voice and a separate list of who moved jobs. Use when you say "/find-threads-to-join", "posts to comment on", "engagement digest", "what should I reply to", or ask for a fresh batch of posts to engage with.
---

# Find posts worth replying to

Turn a raw feed of posts from the people the user tracks into a short, ranked digest: the few posts where a
comment from the user adds something real, two comment drafts for each, and a separate list of people moves
worth knowing about. The user may run this several times a day, so each batch must be high-signal and skip
anything already shown.

## Set up once

Ask the user for anything you can't find, then save the answers in a config file in the project (for example
`engage/config.md`) so later runs need no questions:

- **Where posts come from.** One of: a scraper or automation tool's export (PhantomBuster, Apify and similar,
  through its MCP server or API), a CSV or JSON export, an RSS feed, a list of profile URLs to read in a browser,
  or URLs the user pastes. Note how to get the newest *successful* run.
- **Who is tracked.** The lists of people (by track: for example customers, investors, partners, peers) and any
  outbound state (invite sent, accepted, connection degree).
- **The user's topics.** The 5 to 10 subjects where the user can credibly add something. This drives the gate.
- **The target market** for people moves (industry, region, company size, roles).
- **Relationship sources,** if connected: a CRM, an email outreach tool, a notes or memory tool. All optional.
- **The user's voice.** A voice profile for `write-like-me`, plus any comment-specific rules the user has.
- **Where the digest goes.** Slack or another chat tool if connected; otherwise a local Markdown or HTML file.
- **The seen-posts store,** for example `engage/seen_posts.json`. Create it empty.

## Pipeline

Run these steps in order. Do not skip.

### 1. Fetch new posts

1. **Pick the newest successful run** of the source. Scrapers often have a newer run that failed or came back
   short; don't use it. If every recent run failed, tell the user the source is failing and stop. Don't send an
   empty digest. Don't start a long scrape mid-digest; if the user wants fresh data, start it in the background
   and pick it up on a later run.
2. **Pull the rows.** Large results go to a file; don't read the whole blob into context.
3. **Process them** (write a small script if the project has none):
   - Keep every row where a tracked person **authored or engaged** (reacted, commented, reposted, replied).
   - Group by post, so one post engaged with by several tracked people becomes one record listing all of them.
   - Record each post's `strongest_engagement`: authored > commented > replied > reposted > reacted.
   - Drop posts already in the seen-posts store.
   - Keep the last 2 days by default (allow the user to ask for more).

If nothing new is left, say "No new posts since last run" and stop. Send nothing.

**Why reactions and reposts count:** if someone the user tracks likes, comments on or reshares a post, that post
is almost certainly in the user's conversation. Several tracked people on one post is a strong signal.

### 2. Resolve who everyone is

Exports often carry only handles. Build one dossier per author and per engager, from every source you have, in
parallel:

- **Tracked lists and outbound state:** name, title, company, connection degree, invite status and dates.
- **CRM:** the record, last note date, owner, context from notes.
- **Email outreach tool:** campaign, reply status, last reply date. A person who replied well two weeks ago and is
  now engaging with a post in the user's field is the warmest moment there is.
- **Notes or memory:** prior conversations, in-person meetings, anything the others miss.

```
{
  identity: {name, headline, company, connection_degree},
  outbound: {track, invite_status, invite_age_days, accepted},
  crm: {record_id, last_note_date, owner, note_excerpts},
  outreach: {campaign, last_reply_at, category, status},
  notes: [<excerpts>],
  is_known: bool   // true if any relationship source returned anything
}
```

Cache the lists for the whole run. Normalise profile URLs the same way everywhere (lowercase, no trailing slash,
no query string). Never make up a name from a handle. If every source is empty, say the person is unknown.

### 3. Rank into two tiers

#### Tier 1: worth a comment

**The bridge gate (a hard filter, applied before warmth).** A post passes only if both are true:

1. **The author makes a point** the user can build on. A claim, an observation, a story with a point, a
   structural take, or news the post argues about. Not a milestone, welcome, award or thank-you.
2. **The user can credibly add something,** because the post sits on one of the user's topics.

**Drop without exception, however warm the person:**
- Welcomes, appointments, promotions, "thrilled to share I've started a new role".
- Awards and recognitions. Birthdays, anniversaries, milestone thanks.
- Job posts and hiring announcements.
- Daily market recaps with nothing to add beyond chiming in.
- News reshares where the author doesn't argue anything.
- Motivational or philosophical posts, personal or political content off the user's topics.
- Course certificates, graduations, generic career advice.
- Real substance where the user has nothing distinctive to add.

**Warmth alone never passes the gate.** The user's comment has to sharpen what the author already said. If the
user would have to invent the substance, the post is wrong. Skip it.

**Then score warmth:**
- **5:** accepted a connection in the last 14 days, or a positive CRM or outreach signal in the last 14 days.
- **4:** invite pending 7 to 21 days.
- **3:** already connected, more than 14 days ago.
- **2:** in a tracked list, invite not yet sent.
- **1:** known only from CRM or notes.
- **0:** unknown.

**Sort by:** warmth, then number of tracked engagers, then reach, then recency. For each kept post, write a
one-line `why_it_matters`: the topic angle plus the warmth context.

#### Tier 2: people moves (intel)

A separate list of who moved where inside the target market. Used for the user's own outreach, not for public
comments. No drafts.

- **Keep:** someone moving into a relevant role (leadership, head of a function, founding team) at a company in
  the target market. Keep it even with no warmth signal; the move itself is the news.
- **Drop:** moves outside the market, milestones with no change of role or company, hiring posts, awards.

Shape per item: name, role, company, segment, warmth, engagement, post URL. Render as one-liners at the bottom.

#### Calibration

In a typical batch of 200 posts, expect about 3 to 7 to pass Tier 1 and 5 to 15 people moves. Feeds lean heavily
ceremonial. If you're shipping 8 or more Tier 1 posts, the gate isn't being applied. If you're shipping none,
look harder in the long tail for real substance. Record the user's corrections in the config file so the gate
gets sharper.

### 4. Gather context for the comments

For each kept post, search in parallel (3 to 6 searches per post) about the *topic*, not the person:

- The user's earlier takes on this topic (posts, notes, memory).
- Patterns or proof points in the user's notes or knowledge files that map to the post.
- Earlier phrasings that nail the same point.

Track which notes or files informed each comment, so the user can check the source.

### 5. Draft two comments per post

Use `write-like-me` for every draft, with the user's voice profile. Read any comment-specific rules the user
keeps before drafting; they override the general voice.

Give it: the full post, the author's dossier, the engager list and what it means, the context from step 4, and
this instruction: two distinct, paste-ready comments, peer-exchange posture, give something real.

**Rules for public comments (the most-broken ones):**

- **Be helpful, not heroic.** A comment is a public thought given to the author and the thread. The thought is
  the credibility. No case-study or experience references: strip "a client I work with...", "two of the larger
  firms I track...", "the teams I see...", "we've shipped...", "in our experience...". They read as promotion in
  public even when discreet. If the draft loses its punch without them, the thought wasn't strong enough; rework
  it until the substance carries.
- **Don't look down on peers.** Don't pronounce what an industry "should" do, what "the next moat" is, or what
  "most companies" get wrong. Speak from inside the problem.
- **Name the structural reason, don't prescribe.** "The process was built around the form, so rebuilding for
  judgement is an operating-model change" says why it's hard. "They should rebuild the operating model" lectures.
- **No closing question** ("curious what you're seeing"). Add value, stop.
- **No "worth X-ing"** ("worth noting", "worth sitting with").
- **No made-up closing punchline** ("Different equilibrium two years out"). Stop when the body lands, or land on a
  concrete image.

Example rewrite:
- Weak: "One insurer I track cut claim intake from 4 hours to zero in 3 weeks. That's the shift the author means."
- Better: "The lever isn't in the pricing math. It's in claim operations. Cut intake time and the same team
  handles double the volume. The premium math eases without touching premiums."

**The two angles must differ** in argument and opening move:
- **A, agree and extend:** the core claim is right; add a specific mechanism or second step that sharpens it.
- **B, reframe:** name the second-order effect the post missed, the failure mode in what it celebrates, or the
  contradiction the data implies.

Length: 2 to 5 sentences each. If the user's tracked person only engaged (didn't author), the comment still goes
on the original post. Let the engager shape what's worth saying; don't mention them.

### 6. Send the digest

Build one payload:

```json
{
  "header": "Posts worth replying to: <date time, user's time zone>, N posts",
  "items": [
    {
      "rank": 1,
      "author_name": "...",
      "author_headline": "role, company",
      "post_url": "...",
      "post_excerpt": "first ~200 chars, one line",
      "why_it_matters": "topic angle + warmth",
      "engagement": "120 likes, 14 comments, 2d ago, authored | engaged by: <names>",
      "relationship": "track, invite state, CRM notes, last touch",
      "comment_a": "...",
      "comment_b": "...",
      "sources": ["note or file names"]
    }
  ],
  "intel_items": [ { "name": "...", "role": "...", "company": "...", "segment": "...", "warmth": "...", "engagement": "...", "post_url": "..." } ]
}
```

- **Chat tool connected (Slack or similar):** post the ranked links, context and intel to the channel the user
  chose. Keep the comment drafts out of the channel; put them in your reply to the user so they can copy them.
- **No chat tool:** write the digest to a local Markdown or HTML file (with drafts) and give the user the path.

Never post a comment on the user's behalf. They paste it themselves.

### 7. Mark as seen

Only after the digest was delivered successfully, add every included post URL to the seen-posts store so the
next run skips them.

### 8. Report

One short message:
- N posts sent to <where>, plus N people moves.
- Authors, names only.
- What was dropped, with a one-line reason when it isn't obvious ("dropped 3: 2 reshares, 1 motivational post
  off-topic").
- The comment drafts.

Keep ranking and drafting tight. The user runs this often, so speed matters.
