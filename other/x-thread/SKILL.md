---
name: x-thread
description: >-
  Build an X thread: the first post that sells the whole thing, one idea per
  post, cut to fit X's weighted character count, and a last post that people
  act on. Use when the user says "thread", "write a thread", "turn this into a
  thread", "tweetstorm", or has a list-shaped or step-shaped idea that would
  be cramped in one post.
---

# x-thread

A thread is a list that people read one post at a time, and most of them stop
after the first. So a thread is really one post with a sequel. Build it that
way round.

One tool lives in this folder and it runs:

```bash
python3 thread.py draft.txt              # cut it, count every post, lint it
python3 thread.py draft.txt --number     # add 1/7, 2/7 ... (counted in the length)
python3 thread.py draft.txt --pack       # merge short paragraphs into one post
```

Posts break at your own `---` lines first, then at paragraphs, then at
sentences. A sentence longer than a whole post is the only thing that gets
split between words, and it is flagged when it happens.

## Thread, long post, or single post

Decide this before writing anything, and say which one and why:

| the idea | format |
| --- | --- |
| one claim | a single post. `/x-post` |
| one argument that needs room, no natural steps | a long post, if the user has Premium |
| steps, a list, a sequence, a story with beats | a thread |

The most common way a thread fails is being one claim cut into eight pieces.
If that is what the user has, say so and hand it to `/x-post`.

## Structure

5 to 12 posts. Under 3 is a post. Past about 15, fewer people finish it than
read post 2.

```
1        THE HOOK      stands completely alone. The payoff, promised
                       specifically. Formula from ../x-post/hooks.json,
                       usually #16 Thread Promise, #2 Number Reveal or #5 The List.
2        THE STAKE     why the reader should care, or the proof you are
                       the one to say it. The second most-read post.
3..N     ONE IDEA EACH a line of claim, a line or two of why. Short.
N+1      THE RECAP     the whole thread as a list, so a screenshot of it works.
LAST     THE ASK       one: follow, a keyword, the link. One.
```

## Rules

- **Post 1 is 80% of the result.** Score it with
  `python3 ../x-post/hookscore.py --hook "..."` before writing the rest.
- **No "A thread 🧵" as the hook.** X shows it is a thread. Spend the line on
  the payoff. `thread.py` flags it.
- **Every post has to survive being seen alone.** Posts from the middle of a
  thread turn up on their own in people's timelines.
- **Numbering is optional.** It helps a list and costs 5 to 7 characters a
  post. `--number` counts it for you.
- **Links go last.** A link in post 2 is an exit before the payoff.
- **The recap is the post people screenshot.** Make it standalone.
- **Humanize every post.** Run the draft through `/x-human` before cutting it.
  Thread boilerplate ("if you found this thread helpful, follow me...") is in
  the lexicon for a reason.

## Output

The thread from `thread.py`, each post copy-ready with its count, then the
lints and what you did about each. Then:

```
THREAD READY  ·  8 posts
hook:     #16 Thread Promise (score 78 STRONG)
checks:   all posts fit · no mid-sentence breaks · link in the last post only
humanizer: 11 artefacts stripped across 8 posts

Reply "yes" to log it, or tell me which post to change.
```

Nothing is posted by this skill. The user posts post 1, then replies to it
with post 2, and so on, or pastes them into X's composer with the + button.
On "yes", log post 1 to `~/.claude/x/log.md` with the formula.
