---
name: review-feedback
description: |
  Process reviewer feedback from the docs-factory review site: fetch open review
  threads, locate each in this checkout, edit the docs or blog source, set
  approved pages to `status: ready`, turn accepted content requests into planned
  nav slots or tracked compatibility journeys, open a PR, and reply on each thread. Use when the user asks to
  process, address, or work through review comments, feedback, approvals, or
  content requests, for one page, a project, or everything.
argument-hint: 'Optional scope: a page slug, a project (unitycatalog, delta), docs, blogs, or model'
---

# Process review feedback

Review comments, approvals, and content requests live in the review site's
database, not in git. The `review-feedback` MCP server (`list_feedback`,
`get_thread`, `reply_to_thread`, `review_status`, `list_content_requests`,
`complete_content_request`) reads them and maps each onto this checkout. Without
MCP, the same operations are `just feedback list | show <id> | reply <id> --body
… | status | requests | complete-request <id> --planned <backlog-id>`.

The release rule ([ADR-0002](../../../docs/decisions/ADR-0002-git-ready-is-release.md)):
an approval in the review app is the signal to set `status: ready`, and that
merged to main is the release. `private` content is reviewed but never released.

If a tool says there's no token or the token is invalid, stop and ask the user to
run `just feedback login --url <review site>` in a terminal. Don't try to work
around auth.

## 1. Fetch

Call `list_feedback` with the user's scope (`slug`, `project`, or `area`). The
default `state: open` returns threads still waiting on a change. Threads you or
another agent already answered show as `awaiting-reviewer` and are skipped, so
rerunning this skill is safe.

Also call `review_status` (default `awaiting-ready`) for approved pages still at
`draft`, and `list_content_requests` (default `accepted`) for requested content
to add to the backlog.

Summarize what you found per page before editing anything, and confirm the plan
with the user when there are more than a handful of threads or any are ambiguous.

## 2. Locate and decide

For each thread, `get_thread` gives the conversation plus a location:

- `quote` / `code-line`: the exact lines. A note "only the start of the quote
  matched" means the end line is a guess.
- `moved`: the passage was found away from where the comment was written. The
  note says how: the quote now sits under another heading, or the lines were
  followed from the authored commit through the diff or by the lines that
  survived a move. Read around the lines before editing, and check that they
  are still the passage the reviewer meant.
- `section`: the comment's heading section. The quoted text has since changed, so
  find the passage by meaning.
- `file`, or "not in this checkout": the anchor is gone. Read the page and the
  thread, and decide whether it still applies. A note "were deleted since" means
  the passage was removed after the comment; the thread may already be answered.
- `review app: …`: where the review server's re-anchoring placed the thread on
  the latest registered version: moved (and the heading it was written under),
  reworded (and the text it reads now), or quote gone with the heading kept. It
  is what the reviewer sees in the app, so say where it went when you reply.
- `file changed since comment`: line numbers may be stale. Read around them. The
  `changed since comment in N commits` line names those commits; `git show` one
  when you need to know why the passage changed.
- anchor `the whole page`: a page-level thread about the page as a whole (its
  scope, structure, or angle). It maps to the file; read the page end to end.
- anchor `model element <id>` / `model view <id>` / `model the model as a
  whole`: a thread on the estate model from the review app's Model section. It
  maps to the element's or view's declaration in `architecture/model/`. Make the
  change with the `update-architecture` skill (it proposes the `.likec4` patch
  for approval) and regenerate with `just arch-model`. A declaration under
  `deployment/generated/` comes from Trestle: change the environment's
  `env.toml` and run `just env-render` instead.

A thread may carry a **suggestion**: the reviewer's exact wording for the
anchored passage, shown as a `diff` block (`-` original, `+` replacement; no `+`
side means delete the passage). Treat it as the preferred change:

- With a `source match`, replace that source text with the replacement.
- Without one, the passage has inline markup (emphasis, links, code spans) or
  moved. Apply the new wording and keep the source's formatting.
- Code suggestions are dedented. Re-indent them to match the source lines.
- A suggestion that is `applied` or `dismissed` is settled. Read the replies for
  anything still open.

Apply a suggestion verbatim unless it would make the page wrong (a broken
command, a false claim, a convention violation). Then answer instead and leave
it open.

Read the whole thread; later replies often refine or retract the first comment.
Decide for each thread: change it, or answer without changing (the comment is
mistaken, already handled, or out of scope). Don't silently skip a thread.

## 3. Edit

Follow `AGENTS.md`:

- Docs code lives in the page's `snippets/`. Change the snippet, never inline code
  into `index.md`, and keep region markers around only what the reader sees.
- Set `status: ready` only on a page `review_status` lists as approved, and only
  once its open threads are answered (`next:` says so). Never set `ready` on an
  unapproved page or a `private` one, and never move a page off `ready` unless
  the user asks: that unpublishes it. Promoting a page makes its scripts gate
  CI and its compatibility claims render, so run `uv run docsnip compat --fix`
  and commit the tables it rewrites.
- For each accepted content request, add a `planned:` slot under the section its
  placement names (`A › B` is the section trail in `content/<project>/nav.yml`):
  a fresh backlog id from the project's documentation plan numbering, the
  request's title, and `request: <request id>`. Blog requests become an entry in
  `blogs/IDEAS.md` with `request: <id>`. Don't write the page itself.
- A thread on a planned slot (its anchor says `planned slot <id>`) is an
  instruction for writing that page, not an edit to make now. Leave it open
  and unanswered for `docs-write`, which reads it when the slot is filled.
- A `journey` request asks to track one more thing readers do, across the
  project's engines and clients. Journeys are estate-wide: first check
  `architecture/journeys/journeys/` for one that already covers the task on
  the same path, and reuse it. Otherwise add it to the area's file there with
  an `<area>.<task>` id, the request's title, a one-sentence `summary`, its
  `asset` and `path` (`architecture/journeys/paths.yml`), the spec
  obligations it exercises in `covers` when it exercises any
  (`architecture/journeys/obligations/`), and `request: <request id>`. Append the id to the `rows` of the table its placement names
  in `content/<project>/compatibility.yml`, and run `uv run docsnip compat
  --fix`. Its cells start unknown. Add `evidence` (to
  `architecture/journeys/evidence.yml`) only from a source you can cite, and
  leave claims to the scripts that prove them.
- Blog posts follow `blogs/CONVENTIONS.md`.

Then run `uv run docsnip check`, `cd site && node scripts/check-nav.mjs` if you
touched a `nav.yml`, and `uv run pytest content/<path>` for any page whose
snippets you changed.

## 4. Commit, push, PR

Work on a branch (`feedback/<scope>-<date>`), never `main`. Make one commit per
page or concern, following the repo's commit contract, and list the thread ids
addressed in the body. Push and open a PR whose description lists each thread
(page, one-line summary, what changed), each page set to `ready` (with its
approvers), and each planned slot or journey added (with its request id). CI warns on the PR
if a page went `ready` without an approval; treat that as a mistake to fix.

## 5. Reply

**Only after the PR exists**, call `reply_to_thread` once per handled thread:

- Changed: one or two sentences on what changed, plus the PR link. If the
  thread's suggestion is what you applied, set `suggestion_applied: true`
  (CLI: `--applied`) so it shows as applied.
- Not changed: why, briefly and respectfully, so the reviewer can push back.

For each content request whose planned slot or journey is in the PR, call
`complete_content_request` with its backlog id (a journey's id) and the PR
link. That needs a
token with the `requests:write` scope; if it's refused, list the request ids in
your report for the user instead.

Replies are posted as the token's owner and marked "via agent". Never resolve a
thread; the tools can't, and resolution is the reviewer's call once they've seen
the change. The same goes for dismissing a suggestion.

Finish with a short report: threads addressed, answered without change, and
skipped (with reasons); pages set to `ready`; planned slots added; plus the PR
link.
