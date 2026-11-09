---
name: til
description: Capture a "today I learned" note from the current session into the user's own learning folder, shaped so it can become a blog post later. Use when the user says "TIL", "note this down", or "I want to blog about this". Writes one markdown file outside this library and outside any public repo. Never publishes.
argument-hint: "[what you learned, or empty to take it from this session]"
disable-model-invocation: true
---

# TIL

Input: what the user typed after the invocation. If it is empty, take the lesson from the current session: the most recent thing that surprised the user, cost real time, or changed how they work. If there are several candidates, list up to three in one line each and ask which one.

## Where it goes

The learning folder belongs to the user. This skill has no default path.

1. A path in the message wins.
2. Otherwise use the `TIL_DIR` environment variable (`echo "$TIL_DIR"`).
3. Otherwise ask once. Tell the user they can set `TIL_DIR` in their own shell profile so it is not asked again. Do not edit their profile.

Refuse a path inside this library's checkout or inside a git repo with a public remote. TIL notes are personal until the user decides to publish one.

File: `<TIL_DIR>/YYYY-MM-DD-<kebab-slug>.md`, today's date, slug from the title in five words or fewer. Template: [til-note.md](../../../templates/til-note.md).

## Steps

1. Pin the lesson to one sentence: "X works like Y, because Z." If you cannot, ask the user one question.
2. Check for a duplicate: `grep -ril "<two or three key terms>" "$TIL_DIR"`. If a note covers the same thing, add a dated `## Update YYYY-MM-DD` section to it instead of a new file.
3. Gather evidence from the session: the failing command or error, the code before and after, and the public source that explains it (official docs, a public issue, upstream library docs). No source found means the note says so under Sources.
4. Write the file from the template in the `plain-voice` style.
5. Add one line to `<TIL_DIR>/README.md`, newest first, creating it if needed: `- YYYY-MM-DD [<title>](<file>) <tags>`.
6. Reply with the file path and the one-sentence lesson. Nothing else.

## Keep it publishable

The note may become a public post, so write it public-safe from the start:

- No colleague names, customer names, internal links, private issue numbers, chat quotes, metrics, unreleased features or credentials. Describe them generically ("a reviewer pointed out", "an internal tool").
- Code samples are minimal reproductions, not pasted private code.
- If something in the lesson cannot be made generic, keep it out and say so in the reply.

## Hand-offs, suggested only

- A gotcha that cost more than 15 minutes may also be a rule worth keeping. Say "This could be a local rule too, run `learn-from-fixes` when the fix merges." Do not edit any shared library from this skill.
- Turning a note into a post is a separate request. When asked, draft it from the note in the `plain-voice` style and leave publishing to the user.

## Boundaries

- Writes only inside the learning folder. Never posts, publishes, commits or pushes.
- Never stores secrets or tokens in a note.
