---
name: read-thread
description: "Read a Bluesky conversation as a whole: every reply, who wrote it, and which post it answers. Use it when what you do next depends on the rest of the conversation."
---

A reply's record carries its thread's root at `reply.root.uri`; a top-level
post is its own root. Read from the root:

    query(nsid="app.bsky.feed.getPostThread",
          params={"uri": <root uri>, "depth": 10, "parentHeight": 0},
          select='def w(d): (.post | "\("  " * d)@\(.author.handle) [\(.uri | split("/") | last)]: \(.record.text | gsub("\n"; " "))"), (if (.replies // []) == [] and (.post.replyCount // 0) > 0 then "\("  " * (d + 1))… \(.post.replyCount) more below, read from \(.post.uri)" else (.replies[]? | w(d + 1)) end); .thread | w(0)')

Each line is one post with its author and rkey, indented under the post it
answers. Media-only posts show empty text; get_record one when its media
matters.

The service returns at most 10 levels below the post you pass. A line
starting with "…" marks replies it left out; read again from the URI it names
to continue down that branch. Responses over 30k characters are trimmed: pass
the post you're joining with parentHeight 10 to read just its branch.
