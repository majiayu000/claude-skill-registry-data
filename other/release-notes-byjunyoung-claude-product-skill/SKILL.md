---
name: release-notes
description: Turns an engineering release notice into notes the people who run the product can act on — per feature, the change as a sentence, a recording of the real screen, where it is, who it reaches and what they have to do — written to the spec or a file, then a short reply on the notice saved as a draft. Triggers - "/pm:release-notes", "write the release notes", "turn this release notice into notes for operations", "릴리즈 노트 써줘", "배포 공지 정리해줘", "배포 전 안내 써줘".
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page, mcp__claude_ai_Notion__notion-query-data-sources, mcp__claude_ai_Notion__notion-create-file-upload, mcp__claude_ai_Slack__slack_read_thread, mcp__claude_ai_Slack__slack_read_channel, mcp__claude_ai_Slack__slack_search_public_and_private, mcp__claude_ai_Slack__slack_read_user_profile, mcp__claude_ai_Slack__slack_send_message_draft, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__find, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__gif_creator
---

# release-notes — a release notice, in the words of the people who run the product

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

Engineering's release notice names tickets and short titles. The people who run the product — operations, support, whoever answers the customer — cannot tell from it what changes on their screens, whom it reaches, or whether a customer has to hear about it first. The planning side wrote the spec and drew the screens, so it is the side that can say. For each feature in the notice this skill writes the change as a sentence, a recording of the real screen, where on screen it is, what changes, who it reaches, and what the readers have to do. The notes go where `release.notes.target` says; the notice's thread gets a short reply linking to them, saved as a draft.

The readers are on a phone as often as at a desk. The reply alone should tell them what changes; the notes are there for when they want to see the screen.

## Config

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml
```

Where `release.notes.target` is `notion`, run it again with `--authored release.notes.section,release.actions`. The section heading and the three action labels are written into somebody else's page, and a floor value in another language would put words there that the team never chose. **Exit 3 stops the run** with the message naming the line to add. Do not interview for the value, and do not proceed on the default. A markdown target writes only into your own folder, so it runs on the floor.

The tickets come from `task.mirror.type`'s adapter — or `task.record.type`'s, where the mirror is `none`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.mirror.type} --role mirror
```

Chat goes through `sources.chat_type`'s adapter (`--kind sources --role chat`); Slack ships. **Exit 3 or 4 means no usable adapter** — stop and say it in the person's words ("this tool isn't supported yet; `/pm:setup` can add it from what's connected here"), never the exit code. Where `sources.chat_type` is `none`, the notice is pasted in and the reply is printed for the person to post.

## Input

A link to the release notice. "The latest <product> release" works where `release.channel` is set: read that channel newest-first and take the most recent notice for that product. If two could be meant, ask.

## Flow

1. **Read the notice** — the notice and its replies so far. Pull the release date and time, the product and version, and one line per feature. A line with no ticket behind it is a candidate for internal work. Work out the deadline: `release.lead_time_hours` before the release.
2. **Read the material** — for each feature, the ticket, then the spec, then the design.
   - Ticket: through the adapter. The scenario, the requirements (`task.contract.sections.requirements`), the QA checklist (`task.contract.sections.qa`), and the links to the spec and the design. A ticket the notice does not link is found under the release's milestone or version in the tracker. Where the notice names a child ticket, read its parent too.
   - Spec: the feature or policy entry — its latest revision, where there are several.
   - Design: menu and button names exactly as they appear on screen.
3. **Write each entry** — *An entry*, below.
4. **Record the screens** — *Recordings*. Show each recording in the conversation and confirm it is this release's screen.
5. **Notes: preview → go → write** — *Where the notes go*. Read the result back from the source afterwards.
6. **Reply: preview → go → draft** — *The reply*. It needs the notes' link, so it comes after 5. Saved as a draft on the notice's thread, never sent.
7. **After it goes out** — when the person says it was sent, read the thread again for the sentences that actually went. Wording they changed is where the next draft starts.

The notes and the reply each get their own go, and each preview carries the full text, not just the part that changed.

## An entry

One entry per feature line in the notice:

```
### N. <the change, as a sentence>          e.g. Turn online ordering on and off per location
(recording)
- Where: <menu path>                         e.g. Ordering > Locations
- What changes: two sentences at most
- Who: one line                              e.g. every location that takes online orders
- To do: <one of release.actions> — the reason in one sentence
```

- The title is the change from the reader's side, not the feature's name — the way public changelogs such as GitHub's, Vercel's and Intercom's write theirs. No parent-ticket titles, no ticket numbers.
- What changes: from the scenario and the QA checklist, only what the reader meets on screen. The detailed rules stay with the screen and the ticket.
- To do is one of `release.actions`, in this order, and never left blank:
  1. A customer meets it — something they did is blocked, or works differently, or gives a different result — so someone has to tell them before they find out. Judge it from the customer's side, not the readers'. Where `release.customers_operate` is true, a screen the spec gives to an internal role may still be run by a customer's own staff — it counts here.
  2. No customer is caught out, but the readers get something new, or something they need to know to answer a question. A blocking change on a screen only your own staff use drops here.
  3. Nothing reaches them.
- Entries taking the first action come first in the notes.
- A bug fix needs no spec or design — write it from the ticket and the chat thread it links.
- Internal work — a package manager change, a refactor — gets no entry.
- A product opening for the first time gets a short block at the top: who, from when, where, and what the readers now do themselves.
- Voice: `release.notes.voice`. Before the release the entries speak of what will change; after it, of what changed.

## Recordings

One recording per entry, of the real screen, `release.capture.seconds` long, no sound.

- Tool: Claude in Chrome's GIF recorder — start recording, operate (click through `find` refs), stop, then export with `download: true`, `showWatermark: false`, `showActionLabels: false`, `showProgressBar: false`, `showClickIndicators: true`. Collect the files under `release.capture.dir`.
- Environment: before the release, the build being released (a staging or development server); after it, production. A staging server can show what production does not — a menu still in development, test data. Name it in the preview.
- **Change no data.** Before recording, install a guard in the page that blocks every `fetch` and XHR request that is not a GET. Open a confirmation dialog and cancel it; leave an edit screen through its own exit. After recording, check that the guard blocked nothing.
- Open test accounts and test locations only. A real person's name or email, or a test post's title, caught on screen → use another screen, or name it in the preview.
- The person logs in themselves. To show the login screen, make the page's session check answer as signed out, then go to the login route.
- A feature that cannot be run safely — a screen that opens only after a state change, an input that saves the moment it is typed, a device that is not a browser — gets a still from the design file instead. A browser capture comes at 1×; where a still is soft, scale the region to 2× in the page (`transform: scale(2)`) and capture that.

## Where the notes go

`markdown` — one file per release at `<release.notes.dir>/<slug(product)>/<date>-<slug(release)>.md`, the recordings in a folder beside it, linked relatively.

`notion` — one row per release in the table under the `release.notes.section` heading of the product's spec page (`prd`), matched by the heading's text with any leading number ignored.

- Read the table's schema before writing. Fill the title (the release, e.g. "Ordering 2.4.0"), the release date, and the relation to the spec's feature and policy entries — their latest revisions. Add no properties.
- A spec with no such section gets one, with the schema the section has in `prd.notion.template`, behind its own preview and go, and one line in the spec's change log. Where `prd.notion.template` is `null`, stop and name it. Insert the section after the end of the neighbouring block; do not rewrite an existing block's opening to splice it in — a large callout rewritten that way has jumped to the top of the page.
- Recordings: for each file, get an upload address from the file-upload tool, send the file with `curl -F "file=@x.gif;type=image/gif"`, and place it in the body as `<image source="file-upload://<id>"></image>`. Never through the clipboard.
- Afterwards, read the row back: the number of recordings, and any broken characters. Where the spec page was touched, the order of its sections too.

## The reply

A reply on the notice's thread, in the name of the person running this, and short. Find an earlier reply of this kind by the same person in that channel and follow its shape; with none, this one:

```
[<product> release notes] <audience mentions>

What changes in this <product> release.

<the first of release.actions>
• <screen>: what the customer will meet, and from when

• <screen>: <one line>
• <screen>: <one line> <the mention of the group that uses it>
<a line the readers truly need first — how to sign in, say>

The details, with screen recordings: <link to the notes>

cc. <release.cc> <the notice's author>
```

- The reply has to stand on its own. Readers who never open the notes should still know what changes and why — a reply of this length was what the first readers asked for.
- Features that take the first of `release.actions` go first, in a block of their own under that label, each saying what the customer will meet and from when. These are the ones the readers have to pass on, and a label at the end of an ordinary line gets missed — the first readers asked for them to stand out. With none, the block is left out.
- Every other feature is one line. The to-do and its conditions stay in the notes.
- Tag from `release.audience` by who uses each feature, not every group every time.
- Whatever the notice's author said they would share themselves — an address after the release, say — is not announced early.
- Mentions are written in the chat tool's mention syntax, taken from the config — never typed as display names. A person addressed by title gets the title from their chat profile, not from how others address them.
- Saved with the chat tool's draft call on the notice's thread. Sending is the person's.

## Notes for the person only

A separate block in each preview, only what applies:

- Missing links: a spec or design the notice or the ticket did not link, found directly.
- Material in conflict: where the ticket, spec, design and running screen disagree, and which was followed.
- Unchecked behaviour: a ticket in the release whose QA has not passed.
- Changes outside the notice: something that reaches users, found while reading. Ask whether it goes in.
- Recording environment: what looks different from production because it is a staging server.
- An action that was a close call, and why it went where it did.

## Checks before each preview

- Entries: each has a title, a recording, where, what changes, who, and to do — and to do is one of the three.
- Words: none of `release.forbidden_terms` in the notes or the reply, and no ticket numbers, abbreviations, or internal role and plan names the readers do not use. A menu or button name exactly as the screen shows it is the exception.
- Customers first: every entry taking the first action sits in the reply's top block, and nowhere else in the reply.
- Mentions: the reply tags at least one group from `release.audience` where any is set, and ends with `release.cc`.
- Time: past the deadline, the top of the preview says "past the deadline (release HH:MM, now HH:MM)"; already released, "after the release — decide whether to post this as notes after the fact"; inside `release.quiet_hours`, "the mentions will notify people now".

## Before the first run

- The release notice's template should cc whoever writes these notes, or notices get missed. Where it does not, say so once in the notes for the person.
- Check once per product that the readers can open the notes — a spec page shared only with the planning side is a link they cannot follow.
