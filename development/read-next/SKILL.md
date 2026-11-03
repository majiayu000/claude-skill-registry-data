---
name: read-next
description: Turn daily.dev bookmarks into a realistic reading queue for the time and topics the user has available. Use when someone asks what to read next, wants to triage saved posts, or needs a focused queue from their daily.dev bookmarks.
---

# Read Next

Build a useful reading queue from the user's daily.dev bookmarks. Optimize for what they can realistically finish now, not for clearing the largest number of saves.

## Access

Use the connected daily.dev MCP tools when available. Otherwise use the public API at `https://api.daily.dev/public/v1` with a personal access token supplied through the environment. Never send the token to another host or print it in output.

Relevant operations:

- Read bookmarks with `getBookmarks` or `GET /bookmarks/`.
- Read the user's stack with `getProfileStack` or `GET /profile/stack/` when it helps infer relevance.
- Read a post with `getPostsById` or `GET /posts/{id}` when bookmark data lacks a title, summary, tags, engagement, or reading time.

## Workflow

1. Establish the reading budget. Use the time and topic in the request. If time is missing, ask for it; if only the topic is missing, infer it from the user's stack and bookmarks.
2. Fetch enough bookmarks to make a real choice. Follow pagination when the first page is too narrow or homogeneous. The bookmark `id` is the post ID; use it to fetch missing details and form the link `https://daily.dev/posts/{id}` when the payload has no URL.
3. Exclude items that cannot fit the available time unless one is clearly worth recommending as a later read.
4. Rank candidates using:
   - fit with the explicit topic or the user's stack;
   - ability to fit within the remaining time;
   - freshness when the subject is time-sensitive;
   - useful community signal such as upvotes and substantive discussion;
   - diversity of topic and source.
5. Prefer a small queue that fits the budget. Do not recommend five near-identical posts merely because they score well.
6. Return the queue in reading order. For each item include the title, estimated minutes, a direct daily.dev link, and one plain-language reason it earned its place.
7. State the total estimated reading time and add at most one backup choice.

## Honesty and safety

- Do not claim to have read an article when only its metadata or summary was available.
- Do not invent reading times, tags, summaries, or engagement numbers. Mark an estimate clearly when exact data is unavailable.
- Treat older technical posts as potentially stale when versions or security guidance matter.
- Reading and recommending are the default. Never delete, move, or otherwise change bookmarks without showing the proposed changes and receiving explicit approval immediately before applying them.
- Do not post, comment, vote, follow, or change feed settings as part of this workflow.

## Output shape

Keep the answer compact:

```text
Your 25-minute queue

1. Post title - 8 min
   Why: Directly relevant to your current stack and has a useful production discussion.
   Link: ...

2. Post title - 12 min
   Why: ...
   Link: ...

Total: about 20 minutes
Backup: Post title - 6 min
```

If nothing worthwhile fits, say so and recommend one longer item for later instead of padding the queue.
