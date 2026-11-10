---
name: unroll
description: Fetch an X/Twitter thread or reply chain as clean Markdown. Use whenever the user shares an x.com or twitter.com status link and wants to read, summarize, discuss, translate, or save the thread, e.g. "read this thread", "what does this thread say", "summarize this", "save this thread", "прочитай тред", "о чём тред", "перескажи", "сохрани тред". Prefer it over web fetching, since x.com pages need login and return little to a fetcher.
compatibility: Requires Python 3.8+ (standard library only) and network access to api.fxtwitter.com
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/unroll.py *)
metadata:
  version: "0.6.0"
---

# unroll

Fetches an X/Twitter thread as Markdown (to stdout or a file) using the public FxTwitter API
(`https://api.fxtwitter.com/2/thread/<id>`). No X account, API key, or browser automation needed.

## Steps

1. Take the tweet URL (or bare status ID) from the user's message or the skill arguments.
   Any tweet of the thread works: first, middle, or last.
2. Pick the mode from what the user wants:
   - **Read** (read, summarize, explain, translate, answer questions about the thread):
     pass `-o -`. The Markdown goes to stdout and no file is created. Work with that text.
   - **Save** (save, export, archive, "to a file"): pass `-o <path.md>` if the user named a
     path, otherwise omit `-o`; the script writes `<author>-<first-tweet-id>.md` into the
     current working directory.
3. Run the bundled script. `scripts/unroll.py` is relative to this skill's directory
   (the folder containing this SKILL.md); build the absolute path from it:

   ```bash
   python3 <skill-dir>/scripts/unroll.py "<url>" -o -          # read
   python3 <skill-dir>/scripts/unroll.py "<url>" [-o <path.md>] # save
   ```

   Requires Python 3.8+. In save mode it prints `✓ N tweets → <file>` to stderr.
4. Read mode: answer what the user asked, based on the thread text. Save mode: tell the user
   the file path and tweet count; don't paste the whole file into the chat unless asked.

## Output format

- YAML frontmatter: `author`, `name`, `date`, `source`, `tweets`
- `# Title` from the first line of the first tweet, then author and date
- Each tweet's text, separated by `---`
- Photos as `![](url)`, videos and GIFs as a thumbnail linking to the mp4
- Quoted tweets as a `>` blockquote with a source link; quote chains are followed and nested
  (`> >`), up to 8 levels
- X Articles (long posts) as their title and lead, with a link

The output covers the reply chain around the linked tweet: the author's self-replies, plus
other people's tweets the author was answering. When more than one person posts in it, each
tweet starts with a bold `@handle` and the frontmatter lists `participants`. The
auto-added `@user` prefixes of replies are stripped. Other replies under the post (side
branches) are not included.

## Errors

- `Failed to fetch thread <id>: ...`: the tweet is deleted, protected, or the ID is wrong.
  Report the message as is; do not retry in a loop.
- Network or 5xx errors: FxTwitter may be down. Say so; there is no fallback source.
- Rate limit is 1000 requests/minute per IP, one request per thread.
