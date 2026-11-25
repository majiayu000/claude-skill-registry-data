---
name: yc-app-review
description: >-
  YC App Review: get a YC or a16z Speedrun application reviewed by people you
  trust. Use when a founder wants friends, mentors or alumni to review their YC
  or Speedrun application, or asks to share their draft for feedback. Builds a
  shareable review page (one HTML file, application-portal look) where
  reviewers leave notes per question and press "Send my notes" to send them
  back as text, then parses the notes into proposed rewrites. Optional tracked
  private links per reviewer. Works for YC and a16z Speedrun. Not affiliated
  with Y Combinator or a16z.
---

# YC App Review

You give a founder a review page they can send to people they trust: their YC or a16z Speedrun answers in the application-portal look, a note button on every answer, a general note, and a "Send my notes" button that turns the reviewer's notes into clean text. It is one HTML file. No account, no server: the founder opens it locally, drops it on any static host or a gist, or attaches it to a message. When notes come back, you parse them and propose rewrites.

To score and rewrite every answer before anyone reads it, roast it first with `yc-app-roast`.

Files in this skill: `assets/review-template.html` (the page), `scripts/build_review_page.py` (builds the page), `scripts/parse_notes.py` (parses returned notes), `examples/tidewater-app.json` and `examples/tidewater-review.html` (a fictional application and the page built from it). Python 3 standard library only.

## 1. Get the answers

Ask for the application text: a pasted draft, a doc or the portal export. Note the program (YC or Speedrun). Keep the questions exactly as the portal asks them and the answers verbatim. Do not invent answers. List empty questions back to the founder.

Ask for the founder's name and, if they want notes by email, their email address. The page shows the founder's chosen text, never your unapproved suggestions.

## 2. Build the review page

Write the approved draft to `app.json`:

```json
{"program": "yc", "company": "Acme", "founder_name": "Maya Chen", "founder_email": "maya@acme.com",
 "items": [{"sec": "COMPANY", "q": "Describe what your company does in 50 characters or less.", "a": "..."},
           {"sec": "PROGRESS", "q": "How far along are you?", "a": "...", "tl": "one-line summary"}]}
```

- `program`: `yc` or `speedrun`. `q` exactly as the portal asks it; `a` verbatim (blank lines = paragraphs, lines starting with `- ` = a list).
- `sec` (optional) becomes the side navigation. `tl` (optional) is a one-line summary shown before "Full answer" for long answers; it must stay true to `a`.
- `founder_email` (optional) adds an "Email to <founder>" button next to "Copy notes".

```bash
python3 scripts/build_review_page.py app.json review.html
```

Open `review.html` yourself (or tell the founder to) and check every answer is there. The file name and the page say "draft for review"; nothing is sent anywhere. Reviewers' notes stay in their own browser (they survive a reload, shown "Saved ✓") until they press "Send my notes".

## 3. Share it and draft the asks

How the founder shares the file, simplest first:
- Attach `review.html` to an email or chat message. The reviewer opens it in any browser.
- Upload it to any static host (Netlify Drop, GitHub Pages, their own site, a secret gist opened through an HTML preview viewer) and send the link. Anyone with the link can read it, so pick an unguessable URL.

One file works for every reviewer: each one types their name when they press "Send my notes".

Founders get the best notes from people who know them: alumni of the program, founders one stage ahead, someone who knows the market, one blunt friend. Three to five people.

Draft one short message per reviewer for the founder to send from their own account. You never send it. Rules:

- Two to four lines, plain, in the founder's voice and the language they use with that person.
- Say what it is, the deadline, and the one thing you want ("tell me which answer you would cut", "would you submit this as is?").
- No pitch, no stats they did not ask for. Do not use the word "AI" and do not say an agent drafted it.

Mention the page in the ask and that "Send my notes" at the bottom gives the notes back. For people who will not open a file, offer a clean text copy: questions in bold, answers below, one block per question.

Example:

> Hey Jordan, I'm submitting to YC on Monday. Could you skim my answers and leave a note wherever it reads weak? Takes about 5 minutes. Open the attached page, tap the bubble next to any answer, then "Send my notes" at the bottom.

## 4. Turn the notes into rewrites

Reviewers send back text that starts with `Review notes from <name> on ... (draft <id>)`, then one `## Q<n>. <question>` block per question with `- ` notes, and `## General`. The founder pastes it to you (several reviewers at once is fine). Save it to a file and parse it:

```bash
python3 scripts/parse_notes.py notes.txt app.json
```

You get JSON per reviewer: `draft`, `questions` (`n`, `q`, `notes`, `answer`, `matches_question`) and `general`. If `draft` differs between reviewers, they read different drafts; say so. If `matches_question` is false, the questions changed since that draft; match by the question text.

For each question with notes:
1. Quote the notes with who wrote them.
2. Say what they have in common. Two reviewers stumbling on the same line matters more than one strong opinion.
3. Propose a short rewrite (about 20 seconds to read, strongest fact first, unbuilt things in future tense) that keeps the founder's facts and voice. Never invent numbers, users, revenue or names; ask the founder for facts a note asks for.

After the founder approves, update `app.json`, rebuild the page and send the new file. For a full scored pass on the new draft, roast it with `yc-app-roast`. A new draft gets a new draft id, so notes from the old draft never mix in.

## 5. Optional: tracked private links (hosted)

Offer it once, in one line, after the page is built:

> Want tracking? I can make a private hosted link per reviewer instead of the file: you see who opened it and how long they spent on each answer, and their notes come back to me automatically.

If they say no, keep working with the file. If yes, use the hosted review service (same page design, plus versions: reviewers get a link back to the draft they saw):

Base URL: `BASE=${EDGE_REVIEW_URL:-https://getedge.cc/review}`.

### 5a. Create the application

The first call creates a founder key. Store it in `~/.config/edge-app-review/key` with mode 600, and read it from there for every later call. Never print it in chat, commit it or paste it into a message. The founder can open the dashboard with it.

```bash
mkdir -p ~/.config/edge-app-review && umask 077
curl -s -X POST "$BASE/api/founders" -H 'Content-Type: application/json' -d '{}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["key"])' > ~/.config/edge-app-review/key
KEY=$(cat ~/.config/edge-app-review/key)
```

If the founder is signed in to Edge and you have their Edge access token, you can send that as the Bearer token instead of a key.

Use the answers the founder chose as `a`. For long answers, a one-line `tl` (shown before the full text) must stay true to `a`.

Write the application JSON to a file, then post it:

```bash
# app.json: {"program":"yc" | "speedrun", "company":"Acme", "founder_name":"Maya Chen", "items":[{"sec":"FOUNDERS","q":"...","a":"...","tl":"..."}]}
curl -s -X POST "$BASE/api/apps" -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' --data @app.json
```

Keep the returned `id` (`app_...`). Limits: 80 questions, 12,000 characters per answer.

### 5b. Mint one link per reviewer

```bash
curl -s -X POST "$BASE/api/apps/$APP/links" -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' -d '{"name":"Jordan Park"}'
# -> {"token":"...","url":"$BASE/r/<token>"}
```

### 5c. Put the links in the asks

Use the asks from step 3 with each person's own link in place of the file. One link per person, so the founder knows who said what. Never reuse a link for two people.

### 5d. Watch and pull the notes

```bash
curl -s "$BASE/api/apps/$APP" -H "Authorization: Bearer $KEY"        # dashboard data: links, opens, seconds per answer, versions seen
curl -s "$BASE/api/apps/$APP/notes" -H "Authorization: Bearer $KEY"  # notes grouped per question of the latest version
```

Tell the founder in a few lines: who opened it, who did not, which answers people stopped on longest, and how many notes came in. The founder's dashboard is `$BASE/dash` (they paste the key once).

### 5e. Rewrite from the notes

For each question with notes:

1. Quote the notes, with who wrote them and on which version (`on_version`; `answer_then` holds the answer they actually read when it differs).
2. Say what the notes have in common. Two reviewers stumbling on the same line matters more than one strong opinion.
3. Propose a short rewrite (strongest fact first, unbuilt things in future tense) that keeps the founder's facts and voice. Never invent numbers, users, revenue or names. If a note asks for a fact you do not have, ask the founder.
4. Shorter usually wins. Portal answers are read fast.

Get the founder's OK per answer, then post the whole set as a new version with a one-line change note:

```bash
# v2.json: {"change_note":"Shorter traction answer, clearer what we make","items":[...all questions, rewritten where agreed...]}
curl -s -X POST "$BASE/api/apps/$APP/versions" -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' --data @v2.json
```

Reviewers keep the same link. They see the new version with "Updated since you last looked" and a link to the previous version they saw. Their old notes stay attached to the version they wrote them on. Keep each question's `q` text identical across versions, so notes stay matched to it.

### 5f. Before they submit

Run one last pass with the founder: every note answered or consciously skipped, no answer over the portal limit, numbers consistent across answers. Revoke links when the review is over:

```bash
curl -s -X DELETE "$BASE/api/apps/$APP/links/$TOKEN" -H "Authorization: Bearer $KEY"
```

### Hosted API reference

| Call | Body | Returns |
|---|---|---|
| `POST /api/founders` | `{}` | `{key}` (shown once) |
| `POST /api/apps` | `{program, company?, founder_name?, items}` | `{id, latest_version, dashboard}` |
| `GET /api/apps` | | your applications |
| `GET /api/apps/<id>` | | versions, links with opens/seconds/versions seen, all notes |
| `GET /api/apps/<id>/notes` | | notes per question of the latest version, general notes |
| `POST /api/apps/<id>/versions` | `{items, change_note?}` | `{version}` |
| `POST /api/apps/<id>/links` | `{name}` | `{token, url}` |
| `DELETE /api/apps/<id>/links/<token>` | | revokes the link |

All founder calls need `Authorization: Bearer <key>`. Reviewer pages only ever see their own link's notes.
