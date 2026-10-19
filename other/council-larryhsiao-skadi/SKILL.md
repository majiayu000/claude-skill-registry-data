---
name: council
description: Use when the user runs /council [ticket-id]. Convenes a planning council on an issue tracker ticket. Erestor (subagent) drafts a plan, posts it as a ticket comment, and waits for the human's verdict. Each subsequent invocation refines the plan from the human's reply. Read-only agency — never writes code, opens PRs, or acts on the repo.
purpose: Convenes a planning council on a tracker ticket and refines the plan through the human's replies.
user_invocable: true
stage: plan
---

# Council

Convenes a planning council on a tracker ticket. A subagent — Erestor, chief counsellor of Imladris — drafts a plan from the ticket's text. The plan is posted as a comment. The human — Elrond — renders verdict through further comments. Each `/council TICKET-ID` turns the wheel another round.

## Ethos

- **Elrond decides.** The human holds every verdict. The Council never acts in their name.
- **Erestor counsels.** He reads, he drafts, he asks when he must. He does not approve, reject, or act.
- **The thread is the record.** Every plan, every question, every verdict is a comment on the ticket. No side channels.

## Argument parsing

`/council [ticket-id]`

- `ticket-id`: the tracker's ticket identifier (e.g. `YT-123`). If omitted, ask the user via AskUserQuestion.

## Tracker routing

Two trackers are wired today:

| Tracker | Fetch hook | Comment hook |
|---|---|---|
| YouTrack | `~/.claude/hooks/council-youtrack-fetch.sh` | `~/.claude/hooks/council-youtrack-comment.sh` |
| Jira | `~/.claude/hooks/council-jira-fetch.sh` | `~/.claude/hooks/council-jira-comment.sh` |

**Hybrid dispatch rule.** Resolve the tracker for a given `/council [tracker:]TICKET-ID` invocation in this order:

1. **Explicit override.** If the argument carries a tracker prefix — `youtrack:MET-1`, `yt:MET-1`, `jira:PSG-4264` — that wins. Strip the prefix and use the remainder as the ticket ID. Accept `youtrack` or `yt`; accept `jira`. Case-insensitive.
2. **Per-project memory.** Read `tracker_routing.md` from the project memory directory. The file maps a project key prefix to a tracker:

   ```markdown
   ---
   name: Tracker Routing
   description: Project-key prefix to tracker mapping for /council, /celebrimbor, and /mandos.
   type: reference
   ---

   - MET → youtrack
   - PSG → jira
   ```

   Match the prefix of the ticket ID (`MET-1` → prefix `MET`) against the table; if found, use the named tracker.
3. **Ask.** No prefix override, no memory mapping — ask the user via AskUserQuestion which tracker to use, then offer to save the mapping to memory for next time.

Once the tracker is chosen, all subsequent steps use that backend's hooks. The ticket-ID prefix itself is just a project shortName; do not hardcode any list of valid prefixes.

**Jira read-only rule.** When smoke-testing or otherwise running the council in a non-production capacity, treat Jira tickets as read-only — do not post comments. The Jira comment hook accepts `COUNCIL_DRY_RUN=1` in env to print the would-be ADF payload instead of posting. Use that for shape verification.

---

## Working-directory contract

Erestor's working directory comes from a per-project memory file `repo_routing.md`, **not** from the user's current shell pwd. Resolution order:

1. **Memory mapping.** Read `repo_routing.md` from the project memory directory.
   - **Single-repo (default).** Look up `<tracker>:<project>` (e.g. `youtrack:MET`). If found, that's the **source repo path**. If the value is `(no repo)`, tell Erestor explicitly that this ticket has no codebase context — he drafts from ticket text alone, and the worktree step below is skipped.
   - **Multi-repo (sub-keyed).** A project whose tickets span several repos declares **sub-keyed** entries instead — a line whose key carries a third segment, `<tracker>:<project>:<tag>` (e.g. `jira:PSG:APP`, `jira:PSG:WEB`). To detect the case, scan `repo_routing.md` for any line keyed with the `<tracker>:<project>:` prefix; when one or more exist, this project is multi-repo and the bare key is *not* used. Derive the **tag** from the ticket summary: scan its leading bracket tags `[…]` for the first that matches a declared sub-key (case-insensitive), then look up `<tracker>:<project>:<tag>` for the source repo path (`(no repo)` honoured as above). A summary bearing **no matching sub-key tag** has no repo for this ticket — treat it as `(no repo)` (Erestor drafts from ticket text, worktree skipped) and say so plainly. Tags that are not sub-keys — region or flavour markers like `[NA]`, `[JP]` — are ignored for routing; only the declared layer tags steer the tree.
2. **Ask and save.** If no entry, prompt the user via AskUserQuestion with options:
   - *"Current cwd"* — capture `git rev-parse --show-toplevel` (or the cwd if not a repo) and save.
   - *"A specific path"* — let the user type one (the AskUserQuestion "Other" affordance).
   - *"No repo"* — save `(no repo)` for this project.

   Save the chosen value to `repo_routing.md` under the `<tracker>:<project>` key, then proceed.
3. **Wrap the source in a worktree.** Erestor does **not** read the source repo directly — the human may be editing files there, and a concurrent Read against unsaved edits would mislead the draft. Instead, acquire an isolated detached-HEAD workspace via the shared helper:

   ```bash
   ~/.claude/hooks/skadi-worktree.sh acquire <source-repo>
   ```

   The helper prints the workspace path on stdout. It tries `git worktree add --detach` first (fast — shares the object store); on failure it falls back to a temp clone under `$TMPDIR`. Either way, the workspace pins to the source repo's HEAD at acquire time and lives under `$TMPDIR/skadi-…`. Hold the path; this — not the source repo — is what Erestor sees.

   When the source value is `(no repo)`, skip this step.
4. **Use the workspace path** as Erestor's working directory and pass it in his prompt. He may Read / Grep / Glob / `git log` there. He must not modify anything.

This decouples *where you happen to be* from *which repo this ticket concerns*, and the worktree wrap decouples *what Erestor reads* from *whatever the human happens to be editing right now*. To change the binding for a project, edit `repo_routing.md`. To re-prompt, delete the project's line.

## Workflow

### 0. Resolve the tracker

Apply the **Hybrid dispatch rule** from "Tracker routing" above to choose between YouTrack and Jira. The remainder of these steps refer to `<fetch-hook>` and `<comment-hook>` — substitute the chosen tracker's pair from the routing table.

**YouTrack credentials.** One Vaultwarden item named `youtrack`: URI = server URL, password = permanent token. Hooks resolve via `secret.sh youtrack uri` / `secret.sh youtrack`. Env fallback: `$YOUTRACK_URL` / `$YOUTRACK_TOKEN`. Token comes from `<YOUTRACK_URL>/users/me?tab=account-security`.

**Jira credentials.** One Vaultwarden item named `jira`: URI = `https://<your>.atlassian.net`, username = your email, password = an API token. Hooks resolve via `secret.sh jira uri` / `secret.sh jira username` / `secret.sh jira password JIRA_API_TOKEN`. Env fallback: `$JIRA_BASE_URL` / `$JIRA_EMAIL` / `$JIRA_API_TOKEN`. Token comes from `https://id.atlassian.com/manage-profile/security/api-tokens`.

If any credential cannot be resolved, the hook prints `{"error":"jira credentials missing"}` (or YouTrack equivalent) — surface it and stop.

### Rendering the plan: Henneth mirror and diagram/wireframe embed

Before every post or edit of a plan comment — draft or redraft, either
tracker — run this pipeline on Erestor's returned body (`$EREST_OR_BODY`).
It is invoked from four call sites: the YouTrack modify-only path's
`draft_plan`/`await_start` and `redraft_plan` branches below, and the Jira
path's step 6 first-turn-create and redraft-edit branches. It does **not**
run on `[PEDO]`/`[PARLEY]` — the plan body is unchanged in both cases, so
there is nothing fresh to mirror or scan.

**1. Render the Henneth mirror.** Write Erestor's full returned body to
Henneth so it can be read locally:

```bash
printf '%s' "$EREST_OR_BODY" | python3 ~/.claude/hooks/council-plan-html.py render-plan <TICKET-ID> ~/.skadi/henneth/plan-<TICKET-ID>.html
```

This always runs, on every draft and redraft — independent of whether a
diagram/wireframe block is present and independent of tracker-post success.

**2. Detect a diagram or wireframe.** Scan the same body for a fenced block:

```bash
DETECT_OUT=$(printf '%s' "$EREST_OR_BODY" | python3 ~/.claude/hooks/council-plan-html.py detect)
DETECT_STATUS=$?
```

If `$DETECT_STATUS` is `1` (no block found — `$DETECT_OUT` is `NONE`), skip
straight to posting/editing the comment with `$EREST_OR_BODY` unchanged; none
of the remaining sub-steps run. If `$DETECT_STATUS` is `0`, the first line of
`$DETECT_OUT` is `FOUND tag=<diagram|wireframe>` and the rest is the raw
block body — extract both and continue:

```bash
DIAGRAM_TAG=$(printf '%s' "$DETECT_OUT" | head -1 | sed 's/FOUND tag=//')
DIAGRAM_BODY=$(printf '%s' "$DETECT_OUT" | tail -n +2)
```

**3. Render and screenshot the block.** Write the block alone to a scratch
HTML file, then screenshot it — reusing the same pipeline `/celebrimbor
--skeleton` uses for its diagram PNG (`skills/celebrimbor/SKILL.md:152`):

```bash
printf '%s' "$DIAGRAM_BODY" | python3 ~/.claude/hooks/council-plan-html.py render-diagram <TICKET-ID> "$TMPDIR/diagram-<TICKET-ID>.html"
npx -y playwright screenshot "$TMPDIR/diagram-<TICKET-ID>.html" "$TMPDIR/diagram-<TICKET-ID>.png"
```

If either command fails (non-zero exit), stop the diagram pipeline here: log
the failure so it can be named in the round's report (see the report-format
addition in *Report and release* below), and post/edit the comment with
`$EREST_OR_BODY` **unchanged** (the fenced block posts as raw ASCII, exactly
as council would with no preview pipeline at all) — do not attempt the
attach/embed sub-steps below.

**4. Attach, then embed — per tracker.** Still within the same conditional
(a diagram/wireframe block was found and screenshotted successfully), do
this **before** the tracker's post/edit call:

- **YouTrack:**

  ```bash
  ~/.claude/hooks/youtrack-attach.sh <TICKET-ID> "$TMPDIR/diagram-<TICKET-ID>.png"
  ```

  On success, replace the fenced block in the body before posting/editing:

  ```bash
  printf '![Plan diagram](diagram-<TICKET-ID>.png)' > "$TMPDIR/img-ref.txt"
  EREST_OR_BODY=$(printf '%s' "$EREST_OR_BODY" | python3 ~/.claude/hooks/council-plan-html.py replace "$TMPDIR/img-ref.txt")
  ```

  On failure, leave `$EREST_OR_BODY` unchanged (raw ASCII posts) and note the
  failure for the round's report.

- **Jira:**

  ```bash
  ATTACH_OUT=$(~/.claude/hooks/jira-attach.sh <ISSUE-KEY> "$TMPDIR/diagram-<TICKET-ID>.png")
  ```

  On success, `$ATTACH_OUT` is `attached: name=... id=<ATTACHMENT-ID> url=...`
  — extract `<ATTACHMENT-ID>` and replace the fenced block with the sentinel:

  ```bash
  JIRA_ATTACHMENT_ID=$(printf '%s' "$ATTACH_OUT" | sed -n 's/.*id=\([^ ]*\).*/\1/p')
  printf '[[PLAN-PREVIEW]]' > "$TMPDIR/sentinel.txt"
  EREST_OR_BODY=$(printf '%s' "$EREST_OR_BODY" | python3 ~/.claude/hooks/council-plan-html.py replace "$TMPDIR/sentinel.txt")
  ```

  `JIRA_ATTACHMENT_ID` must reach `council-jira-comment.sh` or
  `jira-comment-edit.sh` on the **same command** that invokes the hook for
  this round (both hooks read it from the environment) — prefix that
  invocation with `JIRA_ATTACHMENT_ID="$JIRA_ATTACHMENT_ID"` rather than
  exporting it as a standing variable here; a later code block is a separate
  invocation, and a standing export would not survive into it. On attach
  failure, leave `$EREST_OR_BODY` unchanged, do not set `JIRA_ATTACHMENT_ID`,
  and note the failure for the round's report.

### YouTrack modify-only path (skeleton-stage pipeline)

When the resolved tracker is **YouTrack**, council maintains a single living
`[PLAN]` comment instead of appended `[COUNSEL vN]` versions, and follows this
path instead of steps 1–7 below. (The Jira path below also maintains a single
living plan comment, edited in place — it keeps its own thread parser and a
visible `[COUNSEL vN]` marker, but the plan body is no longer re-appended each
round.)

1. **Fetch + decide.** Run the fetch hook, pipe to the decider:

   ```bash
   ~/.claude/hooks/council-youtrack-fetch.sh <TICKET-ID> > /tmp/thread.json
   action_line=$(~/.claude/hooks/skeleton-rung.py < /tmp/thread.json)
   ```

   Parse `action=` and `plan_id=` from `action_line`.

2. **Branch on the action:**
   - `draft_plan` **or** `await_start` — summon Erestor (worktree per the
     Working-directory contract); he drafts the plan body. `await_start` means the
     thread bears no `[MELLON]` summons, but reaching `/council` directly **is** the
     summons (the invocation is consent), so it drafts exactly as `draft_plan` does.
     Erestor still returns his `[COUNSEL vN]` envelope; strip that envelope and wrap
     his body as the `[PLAN]` comment. **Create** the comment with the marker,
     watermark, and body:

     ```
     [PLAN] — awaiting [FORTH]
     <!-- consumed: <newest-human-created-or-0> -->

     <Erestor's plan>
     ```

     Before posting, run the Henneth-mirror and diagram/wireframe pipeline
     (*Rendering the plan* above) on Erestor's returned body — it may swap
     the fenced block for an attached image. Then post the (possibly
     diagram-swapped) body as `<Erestor's plan>` via
     `~/.claude/hooks/council-youtrack-comment.sh <TICKET-ID>`.
   - `redraft_plan` — Elrond has posted `[ENVINYA]`/`[ALTER]`, directing a change.
     Summon Erestor with the thread (including the alter instruction); he redrafts.
     Before editing, run the same Henneth-mirror and diagram/wireframe pipeline
     (*Rendering the plan* above) on Erestor's returned body. **Edit the same
     comment** in place via
     `~/.claude/hooks/youtrack-comment-edit.sh <TICKET-ID> <plan_id>`, with the
     watermark advanced to the newest human comment's `created`. An in-place edit
     fires no thread notification, so **append a `[VINYA]` notice** afterwards via
     `~/.claude/hooks/council-youtrack-comment.sh <TICKET-ID>` (see *The `[VINYA]`
     change notice* below), so Elrond sees the plan was renewed.
   - `answer_plan` — Elrond has asked a question (`[CEIST]`/`[ASK]`, or bare prose),
     not directed a change. Summon Erestor in **answer mode** (see step 5): give him
     the standing `[PLAN]` body, the thread, and the question; he returns a `[PEDO]`
     body that answers without redrafting. **Append** it as a new comment via
     `~/.claude/hooks/council-youtrack-comment.sh <TICKET-ID>`. Then **edit the
     `[PLAN]` comment** via `~/.claude/hooks/youtrack-comment-edit.sh <TICKET-ID>
     <plan_id>`, advancing only its watermark to the newest human comment's
     `created` (body otherwise unchanged) — this consumes the question so the next
     ride stays quiet. The plan body is never rewritten; only `[ENVINYA]`/`[ALTER]`
     does that.
   - `draft_skeleton` — `[FORTH]` has just approved the plan; the skeleton rung
     itself belongs to celebrimbor, so council does **not** draft it. But this is
     YouTrack's approval moment: **run *The `[ENWINA]` divergence notice* below**,
     then report "awaiting (plan approved; skeleton is celebrimbor's)" — naming
     whether an `[ENWINA]` notice was posted — and stop.
   - `await_plan` / `redraft_skeleton` / `answer_skeleton` / `forge` / `done` —
     **no-op**. Council's job is the plan rung only; later rungs belong to celebrimbor.
     Report "awaiting" and stop. (`await_start` is handled by the draft clause above —
     a direct invocation is consent.)

3. **Watermark rule.** Whenever council writes the `[PLAN]` comment, set
   `<!-- consumed: N -->` to the `created` of the newest human comment in the
   thread (0 if none). This is what makes the loop quiet between instructions.

### 1. Fetch the ticket and its comment thread

Invoke the chosen tracker's fetch script with just the ticket ID — credentials are resolved inside:

```bash
<fetch-hook> <TICKET-ID>
```

(The script pulls every credential via the secret helper; do not echo or log them.)

The script prints a single JSON object:

```json
{
  "summary": "...",
  "description": "...",
  "comments": [
    { "author": "...", "login": "...", "text": "...", "created": 1700000000000 },
    ...
  ]
}
```

If the script prints `{"error": "..."}`, tell the user the error and stop.

> **The steps below apply to the Jira path only.** The YouTrack path is handled by
> the modify-only section above and does not reach here. The Jira path keeps the
> thread parser and the `[COUNSEL vN]` marker, but maintains a **single living plan
> comment edited in place** (step 6): the first turn creates `[COUNSEL v1]`; each
> `[ENVINYA]` redraft edits that same comment (version bumped) and appends a
> `[VINYA]` change notice. Only `[PEDO]` answers and `[PARLEY]` are still appended.

### 2. Parse the thread

Walk the `comments` array (already oldest-first). Determine:

- **Latest plan version.** The highest `N` where a comment's first line matches `[COUNSEL vN]` or its alias `[PLAN vN]` (case-insensitive). If no plan exists yet, the next version is `1`.
- **Plan comment id.** The `id` of that highest-version plan comment (from the fetch hook's `id` field). This is the comment step 6 edits in place on a redraft. If no plan exists yet, there is no id — step 6 creates the comment instead.
- **Bot identity.** Two modes:
  - **Service-account mode** (e.g. YouTrack with a dedicated `claude` user): a comment is the bot's iff `login == "<bot-login>"`.
  - **Shared-identity mode** (e.g. Jira where the bot posts as Elrond): no login distinction exists; a comment is the bot's iff its first line carries `[COUNSEL v…]` / `[PLAN v…]` (alias), `[PARLEY]` / `[AGENT-ASK]` (alias), `[PEDO]` / `[ANSWER]` (alias), `[VINYA]` / `[RENEWED]` (alias — the in-place-edit notice), `[ENWINA]` / `[STALE]` (alias — the description-drift notice), `[DOOM]` / `[VERDICT]` (alias — Mandos's faithfulness verdict, loop-neutral), `[GWAITH]` / `[FORGED]` / `[SHIPPED]` (Celebrimbor's mark), `[SKELETON]` (Celebrimbor's opt-in skeleton rung), or `[METTA]` (Aulë's close-on-merge). `hooks/jira-skeleton-rung.py` applies this same list.

  Detect mode by inspecting the comment thread: if any login carries the configured bot value (today: `claude`), use service-account mode; otherwise use shared-identity mode.

- **Bot's last word.** The most recent comment classified as the bot's under the chosen mode. If no bot comment exists yet, this is the first turn.
- **Fresh counsel.** Any comments after the bot's last word that are *not* the bot's under the chosen mode. These are Elrond's counsel. If none exist, the thread has not moved since the bot last spoke.
- **Verdict.** Scan the fresh counsel for any of these tokens (case-insensitive, anywhere in the body): `[FORTH]` or its alias `[APPROVE]` (yes); `[NAY]` or its alias `[REJECT]` (no); `[NAMARIE]` or its alias `[FAREWELL]` (adjourn without verdict).

### 3. Handle thread state

The order of these checks matters — skeleton beats verdict beats quiet (no fresh counsel) beats first-turn beats alter beats answer.

0. **Skeleton standing (Jira).** If the thread bears a bot `[SKELETON]`, the plan rung is closed and every later human word — `[FORTH]`, `[ENVINYA]`, a question — belongs to the skeleton, which is `/celebrimbor --skeleton`'s to answer. Council posts nothing (a `[PEDO]` here would read as the bot's last word and swallow the skeleton question). Tell the user "awaiting — the skeleton is celebrimbor's" and stop. This mirrors the YouTrack path's `draft_skeleton` no-op.

1. **Verdict present.** Scan all fresh counsel for the three verdict tokens (and their aliases). Token precedence — *not* chronological order — picks the winner: `[FORTH]`/`[APPROVE]` beats `[NAY]`/`[REJECT]` beats `[NAMARIE]`/`[FAREWELL]`. So if Elrond posts `[NAY]` and later posts `[FORTH]`, the parser adjourns as approved (FORTH wins regardless of when it appeared); same if the order is reversed. Effect:
   - `[FORTH]`/`[APPROVE]` → adjourn with approval on `[COUNSEL vN]`. **Before stopping, run *The `[ENWINA]` divergence notice* below** — on approval the plan is settled, so this is the one moment to flag a description that has fallen behind it.
   - `[NAY]`/`[REJECT]` → adjourn without approval.
   - `[NAMARIE]`/`[FAREWELL]` → adjourn without verdict (farewell — for out-of-band resolution).
   
   Tell the user which adjournment fired and on which counsel version (and, for `[FORTH]`, whether an `[ENWINA]` notice was posted). Post nothing further. Stop.

2. **No fresh counsel and a plan already exists.** The bot has spoken last and Elrond has not replied. Do not draft, do not post — there is no new ground to chew on, and a re-issue would only clutter the thread. Tell the user: "Awaiting Elrond's reply on `[COUNSEL vN]` (or the latest `[PARLEY]`). No fresh counsel since `<timestamp>`." Stop. **This makes the skill loop-safe** — repeated invocations between Elrond's replies are no-ops.

3. **First turn (no plan yet).** Skip to step 4 to draft `[COUNSEL v1]`. The ticket itself is the counsel; no prior bot word is required. A plan must exist before a question can be answered, so a bare question on a planless ticket drafts v1 rather than answering.

4. **Fresh counsel bearing `[ENVINYA]`/`[ALTER]`.** Elrond has directed a change. Fall through to the turn-limit check, then summon Erestor to redraft `[COUNSEL vN+1]`.

5. **Fresh counsel without verdict and without `[ENVINYA]`** — a `[CEIST]`/`[ASK]`, or bare prose. Elrond has asked, not directed. Summon Erestor in **answer mode** (step 5): he returns a `[PEDO]` body that answers the question without redrafting. Post it via the comment hook. Do **not** increment the counsel version, and skip the turn-limit check entirely — an answer is not a counsel and does not count toward the five-counsel limit. The bot's `[PEDO]` becomes its last word, so the next invocation finds no fresh counsel and stays quiet. Stop.

### 4. Check turn limit

The limit is on `[COUNSEL vN]` count, not invocation count — `[PARLEY]` posts do not count. If the next plan would be `[COUNSEL v6]` (i.e. five counsels already posted without verdict), do not draft. Post a single `[PARLEY]` comment via the comment script with this body:

```
[PARLEY] The council has turned five times without a verdict. This thread has outgrown what a comment can resolve. Take it offline — a conversation, a design doc, or a fresh ticket narrowed to one open question.
```

Then stop.

### 5. Summon Erestor

Acquire the isolated workspace per the **Working-directory contract** above (step 3 of the contract). The workspace path is what Erestor sees as his working directory; the source repo is untouched. If the contract's source value is `(no repo)`, skip the acquire and tell Erestor he has no codebase context.

Load the Erestor prompt from `<skill-dir>/erestor.md` (read the file contents). Dispatch a subagent via the Agent tool, `subagent_type: general-purpose`, `model: opus`, passing:

- The Erestor prompt as the *system/instruction* portion of the Agent call's `prompt`.
- A tail block containing:
  - The ticket `summary` and `description`.
  - The full comment thread (all `[COUNSEL v…]`, `[PARLEY]`, and human comments in order, with author names).
  - The workspace path resolved above. If `(no repo)` was the contract's verdict, state that plainly so Erestor knows not to attempt reads.
  - The instruction, by mode:
    - **Draft mode** (first turn, or a `[ENVINYA]`/`[ALTER]` redraft): "You are drafting `[COUNSEL v{NEXT}]`. Your working directory is the named workspace (or none, if so stated) — an isolated detached snapshot of the repo; you may read it with no writes, to verify assumptions before drafting. If a clarifying question is more honest than a guess, reply with a single `[PARLEY]` instead."
    - **Answer mode** (`answer_plan`, or a Jira question without `[ENVINYA]`): "You are in answer mode. Elrond has asked a question of the standing plan, quoted below; answer it with a single `[PEDO]` body and do not redraft. The same read rules apply. If the question cannot be honestly answered from what you have, reply with a single `[PARLEY]` instead." Quote the standing `[COUNSEL vN]`/`[PLAN]` body and the question.

Erestor returns a single markdown body whose first line begins with `[COUNSEL v{NEXT}]`, `[PARLEY]`, or — in answer mode — `[PEDO]`. If he returns anything else, treat it as a drafting failure and stop — do not post. **Even on drafting failure, release the workspace** (see step 7) so it does not accumulate under `$TMPDIR`.

### 6. Post the comment

The Jira path keeps **one living plan comment, edited in place**. Branch on what
Erestor returned and whether a plan already exists (the *plan comment id* from
step 2):

- **`[PEDO]` answer** or **`[PARLEY]`** — these are appends, never edits. Pipe the
  body to the comment hook as a new comment:

  ```bash
  printf '%s' "$EREST_OR_BODY" | ~/.claude/hooks/council-jira-comment.sh <ISSUE-KEY>
  ```

- **`[COUNSEL v{NEXT}]` on the first turn** (no plan comment id from step 2) —
  create the living plan comment. Before creating it, run the Henneth-mirror
  and diagram/wireframe pipeline (*Rendering the plan* above) on
  `$EREST_OR_BODY` — it may swap the fenced block for an attachment embed
  and, on Jira, set `JIRA_ATTACHMENT_ID` (thread it inline on the hook call
  below, which reads it from the environment):

  ```bash
  JIRA_ATTACHMENT_ID="$JIRA_ATTACHMENT_ID" printf '%s' "$EREST_OR_BODY" | ~/.claude/hooks/council-jira-comment.sh <ISSUE-KEY>
  ```

- **`[COUNSEL v{NEXT}]` on a redraft** (a plan comment id exists) — **edit that
  comment in place**, then append a `[VINYA]` change notice. Before editing,
  run the same Henneth-mirror and diagram/wireframe pipeline (*Rendering the
  plan* above) on `$EREST_OR_BODY`:

  ```bash
  JIRA_ATTACHMENT_ID="$JIRA_ATTACHMENT_ID" printf '%s' "$EREST_OR_BODY" | ~/.claude/hooks/jira-comment-edit.sh <ISSUE-KEY> <plan-comment-id>
  printf '%s' "$VINYA_BODY"     | ~/.claude/hooks/council-jira-comment.sh <ISSUE-KEY>
  ```

  Compose `$VINYA_BODY` per *The `[VINYA]` change notice* below. The edit must
  land before the notice; if the edit hook exits non-zero, surface the error and
  stop — do **not** post the notice (it would point at an unchanged plan).

The create/append hook prints `posted: id=<comment-id> created=<epoch-ms> url=<full-ticket-url>`;
the edit hook prints `edited: id=<comment-id> url=<issue-url>`. On failure either
prints `{"error":"...","response":"..."}` (the `response` field carries the
server's actual error body). If a script exits non-zero, tell the user the error
and stop.

#### The `[VINYA]` change notice

This notice serves **both trackers** — the Jira step 6 redraft branch above and
the YouTrack modify-only `redraft_plan` branch. A redraft edits the plan comment
silently — Jira and YouTrack fire no thread notification on an in-place edit, so
Elrond would never learn the plan moved. After the edit, council appends one
short `[VINYA]` (Quenya *renewed*, kin to Elrond's `[ENVINYA]` *renew it*)
comment via the tracker's plain comment hook (`council-jira-comment.sh` /
`council-youtrack-comment.sh`), recognized as the bot's word so the next ride
reads it as no fresh counsel. Point at the plan with the marker that tracker
uses — Jira's versioned `[COUNSEL vN]`, YouTrack's bare `[PLAN]`:

```
# Jira (versioned marker):
[VINYA] The plan is renewed to v{NEXT} — see the [COUNSEL v{NEXT}] comment above.

# YouTrack (single living [PLAN]):
[VINYA] The plan is renewed — see the [PLAN] comment above.
```

The notice is composed by the skill body, not Erestor. It is the only append a
redraft makes; the plan body itself is never re-appended. (The first-turn create
needs no notice — a new comment already notifies.)

#### The `[ENWINA]` divergence notice

This notice serves **both trackers** — the Jira verdict branch (§3, check 1, on
`[FORTH]`) and the YouTrack modify-only `draft_skeleton` branch (the moment
`[FORTH]` advances the plan rung). Council posts it **at most once per ticket**:
when the accepted plan has outgrown the ticket's own description, it flags the
drift so Elrond can renew the description. It **never rewrites the description** —
council counsels through comments; the human's words are the human's to change.

Run it only at approval, in this order:

1. **Idempotency guard.** Scan the thread already fetched for any prior bot
   comment whose first line is `[ENWINA]` / `[STALE]`. If one exists, do nothing
   — the drift was flagged already. Stop here.
2. **Compare.** Read the approved plan body — Jira's latest `[COUNSEL vN]`,
   YouTrack's `[PLAN]` — against the ticket `description` (both from the fetch
   hook). Judge **material divergence**: at least one of
   - the plan **adds** scope the description never states,
   - the description states scope the plan **drops** (its *Not covered*, or a
     silent omission),
   - the plan's approach **contradicts** what the description says will be done.

   *Not* divergence: added implementation detail, rewording, or elaboration
   consistent with the description. When in doubt, do **not** post — a false flag
   clutters the thread, and a description left as-is is recoverable.
3. **Post — if and only if diverged.** Compose the notice naming each drift
   point in one line; do **not** draft replacement description text. Post it via
   the tracker's plain comment hook (`council-jira-comment.sh` /
   `council-youtrack-comment.sh <TICKET-ID>`), recognized as the bot's word so
   the next ride reads it as no fresh counsel:

   ```
   # Jira (versioned plan marker):
   [ENWINA] The approved [COUNSEL vN] has moved past the ticket description —
   the description is now stale and should be updated to match. What drifted:
   - <one line per divergence point>
   The plan on this thread is the source of truth for the forge.
   ```

   ```
   # YouTrack (single living [PLAN]):
   [ENWINA] The approved [PLAN] has moved past the ticket description —
   the description is now stale and should be updated to match. What drifted:
   - <one line per divergence point>
   The plan on this thread is the source of truth for the forge.
   ```

   The leading `[ENWINA]` token is identical on both trackers — only the *inner*
   reference to the plan comment differs (`[COUNSEL vN]` vs `[PLAN]`). The notice
   is composed by the skill body, not Erestor, and is loop-neutral — it counts
   toward no turn limit and redrafts nothing.

### 7. Report and release

Tell the user, in one short block:

- The ticket ID.
- What council did this round — `[COUNSEL vN]` created, `[COUNSEL vN]` edited in place (with the `[VINYA]` notice appended), `[PARLEY]`, or `[PEDO]`.
- The ticket URL printed on the success line in step 6.
- Whether a diagram/wireframe was found this round, and if so, whether it
  rendered and attached successfully or fell back to raw ASCII (name which
  tool failed, if any — screenshot or attach).

Do not reproduce Erestor's draft in the response — it lives on the ticket now.

Then release the isolated workspace, if one was acquired in step 5:

```bash
~/.claude/hooks/skadi-worktree.sh release <workspace-path>
```

The helper handles both worktree and temp-clone modes silently. Release on the success path *and* on the drafting-failure path (the workspace is ephemeral; nothing of value lives in it after Erestor returns). If Erestor never ran — verdict adjournment, loop-safe quiet, turn-limit `[PARLEY]` — no workspace was acquired, so nothing to release.

---

## Comment grammar

Fourteen tokens carry state. Everything else is counsel.

| Token (primary) | Accepted alias | Who writes it | Meaning |
|---|---|---|---|
| `[COUNSEL vN]` | `[PLAN vN]` | Erestor | A draft of the plan. N increments each round. The counsellor's counsel. |
| `[PARLEY]` | `[AGENT-ASK]` | Erestor | A single clarifying question — speech between sides to come to terms. |
| `[PEDO]` | `[ANSWER]` | Erestor / the smith | *Speak, and answer.* The reply to a `[CEIST]` (or bare question) — the plan stands untouched. Loop-neutral; uncounted toward the turn limit. |
| `[VINYA]` | `[RENEWED]` | Council | *Renewed.* The notice appended after the living plan comment is edited in place (a silent edit fires no thread notification). Points at the renewed `[COUNSEL vN]`/`[PLAN]` above; the plan body lives there, not here. Loop-neutral. |
| `[ENWINA]` | `[STALE]` | Council | *Old — of the elder days.* Posted once at approval when the accepted plan has outgrown the ticket description: the written account is stale and wants renewing. Names the drift; never rewrites the description — council flags, Elrond renews. Loop-neutral. |
| `[MELLON]` | `[FRIEND]` | Elrond | Summons. *Speak, friend, and enter* — enrolls a planless ticket in the skeleton-stage sweeps (`/glorfindel`, `/aule`); the decider yields `await_start` without it. Ignored by single-ticket `/council` (the invocation itself is consent). |
| `[CEIST]` | `[ASK]` | Elrond | *A question put to the council.* Draws a `[PEDO]` answer; the plan is untouched. Bare prose is read the same way — it answers, never redrafts. |
| `[ENVINYA]` | `[ALTER]` | Elrond | *Renew it.* The one human word that redrafts the standing plan or skeleton. Absent it, fresh prose only draws an answer. |
| `[FORTH]` | `[APPROVE]` | Elrond | The plan stands. *Forth, Eorlingas!* Council adjourns. |
| `[NAY]` | `[REJECT]` | Elrond | The plan is abandoned. Council adjourns. |
| `[NAMARIE]` | `[FAREWELL]` | Elrond | *Farewell.* Adjourn without verdict — when the thread closes for reasons other than approval or rejection (resolved out-of-band, ticket subsumed by another, etc.). |
| `[GWAITH]` | `[FORGED]`, `[SHIPPED]` | Celebrimbor | The Gwaith-i-Mírdain — the smith-guild of Eregion. The deed is wrought; PR/MR opened on the approved counsel. Body carries the URL and branch. Council itself never posts this; `/celebrimbor` does. |
| `[DOOM]` | `[VERDICT]` | Mandos | *The Doom.* A verdict on whether the deed matches the decree — Covered / Missing / Scope-crept against the ticket's goal. Loop-neutral; uncounted toward the turn limit, never redrafts or approves. Council never posts it; `/mandos post` does. |
| `[METTA]` | — | Aulë | *Quenya "the end."* Closed on merge — the ticket's `[GWAITH]` PR/MR has merged; State moved to the project's closed value. Terminal; the true no-op the decider calls `at_rest`. Loop-neutral; uncounted toward the turn limit. Council never posts it; `/aule` does. |

The English aliases (`[PLAN vN]`, `[AGENT-ASK]`, `[ANSWER]`, `[RENEWED]`, `[STALE]`, `[FRIEND]`, `[ASK]`, `[ALTER]`, `[APPROVE]`, `[REJECT]`, `[FAREWELL]`, `[FORGED]`, `[SHIPPED]`, `[VERDICT]`) are accepted equivalents, recognized everywhere their Tolkien primaries are. Use either form; the parser treats them identically. User-facing reports prefer the Tolkien token.

Human replies between these tokens are free-form prose — read as a question and answered with `[PEDO]`, never folded into a redraft. Only `[ENVINYA]`/`[ALTER]` redraws the plan.

## Rules

- Never act on Elrond's behalf. The skill only reads tickets and posts comments.
- The living plan comment is **edited in place** on a redraft (both trackers), followed by a `[VINYA]` notice; `[PEDO]` answers, `[PARLEY]`, and the first-turn plan creation are appends. No comment is ever deleted.
- **Loop-safe.** If no fresh counsel from Elrond has come since the bot's last word, post nothing. Repeated invocations between Elrond's replies must be silent no-ops. The thread, not the invocation count, is the source of truth.
- **Description drift is flagged, never fixed.** On approval, if the accepted plan has materially diverged from the ticket description, council posts one `[ENWINA]` notice naming the drift, then stops — it does not rewrite the description (Elrond's words are Elrond's to change). Once per ticket, guarded by the presence of a prior `[ENWINA]`; when in doubt whether the drift is material, post nothing.
- If the tracker hook reports a credential is missing, surface the error and stop — do not proceed.
- Turn limit is five counsels per ticket. On the sixth, post `[PARLEY]` asking to take the thread offline. (Only triggers when fresh counsel exists; otherwise the loop-safe rule keeps the thread quiet.)
- Case-insensitive matching of all fourteen tokens and their aliases.
- Two trackers are wired: YouTrack and Jira. The hybrid dispatch rule above chooses between them.
- **Jira tickets are real work.** Do not post test or diagnostic comments to Jira during smoke testing. Use `COUNCIL_DRY_RUN=1` env on the Jira comment **and edit** hooks (`council-jira-comment.sh`, `jira-comment-edit.sh`) for shape verification, and do write-path smoke tests against YouTrack (MET-1).
- Do not surface tracker tokens in logs, responses, or saved files.
