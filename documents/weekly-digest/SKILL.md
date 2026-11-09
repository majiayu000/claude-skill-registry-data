---
name: weekly-digest
description: Weekly engineering digest built from a config the user provides. Releases and changes in the user's area, incidents, AI news from chosen channels, next moves on work the user owns, and openings to contribute. Every item is one line with a link. Use when the user says "weekly digest", "what did I miss this week", or "Friday digest". Read-only; writes one markdown file where the user says.
argument-hint: "<path to digest config>"
disable-model-invocation: true
---

# Weekly digest

Config: the path the user gave. Template: [digest-config.md](../../../templates/digest-config.md).

One file per week that keeps the user ahead of what shipped, what changed in their area, what broke, and what is new in AI. Works with any harness that can read markdown and call read tools for a forge, a chat tool and the web.

## Config: the user provides it

This skill has no defaults for people, channels, repositories or paths. The user provides them, either as a config file path or in the message. If a field is missing, ask once. Never guess a channel, a repository or a goal. Keep the filled config in a private place the user controls, not in a public repository.

## Rule one: one line per item, with a link

- Every item in every section is one line with a link to its source: chat message permalink, issue, pull request, RFC, release post or doc.
- No sub-bullets, no multi-line fields, no paragraphs under an item.
- If something needs more (a draft reply, a diff, a code example), put it in the Drafts appendix and reference it from the line as `(draft D1)`.
- No link, no item.

## Tools

Use whatever the harness offers for: forge reads (pull requests, issues, releases, commits), chat reads (channel history, threads, search), and web fetch for public pages. If a source cannot be reached, write one line `Could not check: <source>, <error>` in that section. Never fill a gap from memory.

## Sections

1. **New in the product and its dependencies.** Release posts and changelogs in the window, items for the user's area first. Merged changes tagged as features in the configured repositories. Line: `- <feature, about 15 words> ([link](url))`. Max 8.
2. **Changes in the user's area.** Announcements, deprecations, new lint rules, migrations from the configured channels, plus merged changes touching shared code in the configured paths. Line: `- [Area] [major|minor] <change>; action: <few words or none> ([link](url))`. Major means it breaks existing code or changes a shared pattern. Max 8.
3. **Incidents.** Incident announcements in the window touching the configured areas, any incident touching the user's own recent merged work flagged. Line: `- <severity> <title>, <area>, <status>[, touches your code] ([link](url))`. If none: `- No incidents found in <range> (checked: <sources>)`.
4. **AI news.** From the configured channels, threads with real discussion. Group under: tooling, competitor moves, worth reading. Line: `- <summary>, <source> ([post](permalink))`. Max 5 per group. Summarise; quote no more than 15 words from anyone.
5. **Moves on owned work (max 5).** From sections 1 to 4, next steps on `owned_work` that show ownership. Line: `- <move>, <S|M|L> ([link](url)) (draft Dn)`.
6. **Openings to contribute (max 5).** Calls for help, open RFCs, unowned priority issues, working groups, incident follow-ups needing an owner. Rank by value against `goals`, at most two M or L items checked against `time_budget`. Read last week's digest so repeats say what changed. If nothing qualifies: `- No new openings found (searched: <sources>)`.

## File format

```markdown
# Weekly digest YYYY-Www (DD Mon to DD Mon YYYY)

Generated <date> <time> <timezone>. Sources checked: <list>. Could not check: <list or none>.

## Top 3 this week
- <one line> ([link](url))

## 1. New in the product
## 2. Changes in your area
## 3. Incidents
## 4. AI news
## 5. Moves on owned work
## 6. Openings to contribute

## Drafts (draft, user sends)
### D1: <short title>
<chat reply, issue comment, proposal outline or diff>
```

If the file for the week exists, replace it (rerun). Do not append a duplicate.

## Writing

- One line per item with a link. This overrides everything else.
- Conclusion first. Plain English, short sentences. No em dashes (see the `plain-voice` skill).
- Absolute dates in the configured timezone.
- Facts in sections 1 to 4. Recommendations only in 5 and 6.
- No labels or guesses about people's motives.

## Boundaries

- Read-only everywhere except `output_path`. Never post, comment, react, approve, assign, volunteer on the user's behalf, send email or accept a meeting. Drafts only.
- No credentials, tokens, customer data or restricted security findings in the file. For a security incident write only "security incident, details restricted" and the public link if one exists.
- Do not commit or push unless the user says so.

## Scheduling

This skill does not schedule itself. To run it weekly, the user sets up their own scheduler or reminder with the invocation and the config path. The skill only runs when invoked by name, so the agent never starts it on its own.
