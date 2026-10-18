---
name: x-profile
description: >-
  Score an X profile out of 100 against a 12-part rubric and rewrite the parts
  that lose points - bio, pinned post, display name, header, link. Use when the
  user says "optimize my profile", "fix my X bio", "score my Twitter profile",
  "what should I pin", "rewrite my bio", or pastes their profile and asks how
  it reads.
---

# x-profile

Nobody reads your profile on purpose. They land on it from a reply or a post
they liked, give it about four seconds, and either follow or leave. Those four
seconds are the bio's first line, the pinned post, and the last two things you
posted. Everything here is in service of that visit.

## Input

Ask the user to paste: display name, username, bio, website, what is pinned
(paste its text), and their last ten posts, or a screenshot of the top of the
profile plus the first screen of posts. Do not log into X on their behalf and
do not ask for a password.

## Score it

Read `rubric.json` in this folder. Twelve items, 100 points, each with what
full marks looks like. Score every item, show the table, give the total. Be
honest: most profiles land in the 40s on the first pass, and a generous score
is useless.

```
PROFILE SCORE  46/100

  bio_open           4/14   job titles, no reader, no outcome
  pinned_post        0/14   nothing pinned
  topic_consistency  6/12   4 of last 10 posts on-topic
  reply_presence     8/10   replies most days
  bio_proof          0/8    no number, nothing checkable
  header             2/8    default grey
  ...
```

## Then rewrite, in this order

Fix in descending order of points lost. The user has to paste each of these
in by hand, so give them in the order that pays most first.

**1. The bio's first line (160 characters for the whole bio).** Who you help
and what changes, in words the reader would use. Three options. Then one line
of proof. Then, if there is room, what you post about. Not a title stack, not
"passionate about", not three hashtags.

**2. The pinned post.** The single most-read post on the account, because it
is the first one every visitor sees. Either the user's best-performing post
that still holds up, or a "start here" post written for a stranger: who you
are, what you post, and the one thing to read first. Draft it through
`/x-post` if it needs writing.

**3. Topic consistency.** If the last ten posts wander, say so plainly. A
profile rewrite cannot fix this; the next two weeks of posts can, and
`/x-plan` is where that happens.

**4. Header (1500x500).** One line of positioning or proof and nothing
important in the bottom-left, where the profile photo sits over it. Write the
line; say what goes where.

**5. Display name, photo, link.** Real name plus one word if it helps. A face
that reads at 40px in a reply thread, because that is the size most people
will ever see it. A link to the one page that matches the bio's promise.

## Output

Score table, then the rewrites as copy-ready blocks in fix-first order, each
through `/x-human`. Re-score at the end and show the delta honestly: if the
rewrite gets to 81, say 81, and say what the remaining points need (usually a
pinned post that has actually performed, and weeks of on-topic posting,
neither of which a rewrite can create).

Nothing is saved to X by this skill. The user pastes each section in.
