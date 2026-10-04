---
name: kelly-jobhunt
description: Run a Busabase-backed job-search outreach desk with a bundled Hono App-in-Skill deployable to AirApp. Use when the user invokes $kelly-jobhunt or /kelly-jobhunt, wants to turn a resume into a structured profile and a typeset PDF, wants to find target companies and their contact addresses instead of applying through a job board, wants one tailored application email drafted per company, or wants to review and approve each send. Four subcommands - setup, profile, research, send - plus the desk itself. One company receives exactly one email; mailbox credentials live in the Busabase Vault and never reach browser code.
metadata:
  category: comms
  tags:
    - risk:gated-write
    - surface:busabase
    - surface:smtp
  busabase:
    template: true
    folderSlug: kelly-jobhunt
    resources:
      - profile
      - companies
      - leads
    risk: gated-write

---

# Kelly JobHunt

Replace board-and-pray applications with a short, inspectable loop: find the
companies worth writing to, find one address that will actually be read, write
one email per company, and let the human approve each send.

## Subcommands

The desk shows state and takes decisions. Everything it cannot do itself is one
of four subcommands, and **the desk always names the next one on screen** — the
operator never has to remember which is which.

| Invocation | What you do |
| --- | --- |
| `/kelly-jobhunt setup` | Create or adopt the Busabase Folder and three Bases, then read them back |
| `/kelly-jobhunt profile` | Take the user's resume or raw notes, extract a structured profile, ask which job channels to search, and build a typeset PDF resume |
| `/kelly-jobhunt research` | Find target companies and their contact addresses, draft one email each, import them |
| `/kelly-jobhunt send` | Put the user's own SMTP credentials in the Busabase Vault, rehearse the transport, then send what they approved |
| `/kelly-jobhunt` (no argument) | Open the desk and report where things stand |

Run them in that order the first time. Afterwards `research` is the one that
repeats. `setup` is optional in the sense that the desk provisions lazily on
first use, but running it first turns "why is this empty" into one command with
an answer.

The first app run has two separate gates before that command loop begins:

1. connect Busabase and explicitly select the target Space when the account has
   more than one;
2. initialize schema v4 resources, then show product onboarding v1 with
   `/kelly-jobhunt profile` as the primary path. The user may skip it and enter
   the desk; target role, truthful highlights, and sender address remain visible
   readiness requirements for later operations. A generated resume file is
   optional and must not block the desk.

Persist completed onboarding as `onboarding-version` on the profile record. An
explicit skip dismisses the prompt for the current open app session without
writing placeholder profile data or browser storage. Until version 1 is
materialized or the prompt is skipped, read only the Profile Base; do not load
the Companies or Leads queues. After a skip, the desk may load, but `research`
and `send` still stop on their own missing profile requirements. A deployed
AirApp submits a completed onboarding update as a ChangeRequest and stays on the
waiting state until that CR is merged. OAuth success alone never marks product
onboarding complete.

## Mandatory Dependencies

Before designing, creating, or changing the app:

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete local `content/kelly-jobhunt-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, API, ChangeRequest, review, merge, and Vault behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.
4. Read `references/jobhunt-schema.md` before changing any Base, field slug, status value, or Vault key.
5. Read `references/research-playbook.md` before running `/kelly-jobhunt research` for the first time — it is the working method behind the boundaries stated here.

If a required skill is unavailable, continue safe local app work but stop before
the unavailable Busabase or deployment operation and report the missing
dependency. Never replace Busabase persistence with local JSON, browser storage,
SQLite, or a file-backed provider.

## Product Boundary

- **One company, one email.** A company row is the unit of outreach. Extra
  addresses stay in the pool as fallbacks for a bounce; they are never a reason
  to mail the same company twice. Sending three near-identical letters to `hr@`,
  `jobs@`, and a department head reads as harassment and gets the whole domain
  filtered.
- **The human approves every send.** The app records a verdict; it never sends
  on its own initiative and never batch-sends without an explicit click.
- **Every address carries its source.** Record the exact page each address came
  from. An address with no source is a guess, and a guess is not allowed —
  write `未找到邮箱` instead and let the desk disable the send button.
- **No secret ever reaches the browser.** SMTP host, user, and app password live
  in the Busabase Vault, written by `scripts/configure_smtp.mjs` and read only
  by `scripts/send_emails.mjs`. Browser code has no mail transport, never calls
  `vault.get`, and never displays a credential value — only whether one exists.
  Not even a masked one: a mask still leaks the length, and it lands in whatever
  log captured the run.
- **Never ask the user to paste a password into chat.** Take it through the
  script's `--pass` flag or the `SMTP_PASS` environment variable.
- **Only ever approve this app's own ChangeRequests.** A Space's open-CR list is
  shared by every app in it. Filter to the three JobHunt Base IDs from
  the generated template sidecars under `content/` — and, when approving one company, to that Record ID —
  before reviewing or merging anything. Merging the whole list because it was
  what the query returned is how an unrelated app's pending write gets approved
  by someone who never read it.

## `/kelly-jobhunt setup`

Goal: the Busabase side exists and has been read back, before anyone types a
resume into it.

```bash
node scripts/setup.mjs           # dry run: what exists, what is missing
node scripts/setup.mjs --apply   # create what is missing, then verify
```

Confirm the Space first — with several, `BUSABASE_SPACE_ID` must be explicit;
picking one silently is how an app lands in the wrong workspace. Then run it.
Nobody copies a Node or Base ID anywhere: every script resolves them from the
Folder by slug, and the script prints the IDs only so a human can recognise them
in the Busabase UI.

Re-running is safe. Provisioning inspects first and proposes only what is
absent, so a second run reports 已就绪 and creates nothing. If a Space
administrator has to approve the structure ChangeRequest, the script says which
one is pending rather than hanging.

## `/kelly-jobhunt profile`

Goal: turn whatever the user has into a profile the other commands can rely
on, plus a resume PDF worth attaching.

1. **Take their material as it comes.** A PDF, a Word file, a LinkedIn export, a
   few paragraphs pasted into chat — all fine. Read it; do not make them fill a
   form first.
2. **Extract, do not invent.** Fill `name`, `target-role`, `locations`,
   `industries`, `highlights`, and `resume-source`. `highlights` is the two or
   three sentences the emails will quote, so it must be concrete: "把跨部门审批
   链路从 3.4 天压到 9 小时" beats "负责用户增长". If the material is vague, ask
   for one specific number rather than writing something generic.
3. **Ask which channels to search**, and offer a sensible default rather than an
   open question. If the user writes in Simplified Chinese, they are most likely
   job-hunting in mainland China — propose BOSS 直聘 / 拉勾 / 猎聘 / 脉脉 plus
   company career pages, and ask them to confirm or edit. Traditional Chinese →
   104 / 1111 / CakeResume. English → LinkedIn / Indeed / Wellfound / company
   career pages. Always let them add their own. Store the answer in
   `job-boards`; `research` reads it.
4. **Write the profile** and set `onboarding-version: 1` in the same approved
   change once target role, truthful highlights, and sender address are ready.
   When the user wants a PDF attachment, build the resume:
   ```bash
   node scripts/build_resume.mjs           # dry run: writes an HTML preview
   node scripts/build_resume.mjs --apply   # renders resume/<name>.pdf
   ```
   Resume generation is optional; research and sending can proceed without a
   `resume-file`. The dry run exists so the user can look at the layout before committing.
   Layout is HTML + CSS printed by headless Chrome; edit the template in
   `scripts/build_resume.mjs` if they want a different look. Rendering is
   `scripts/render_pdf.mjs`: it tries every browser on the machine — including
   the Chromium that Playwright installs into its cache — then the Playwright
   library, and only then gives up. Giving up prints each attempt with its exit
   code and stderr, because "Chrome 挂了" without a reason is not a diagnosis;
   the HTML preview survives either way, so manual 打印 → 存为 PDF is always the
   fallback. Do not report a missing PDF without pasting that list.
5. Never put a claim in the PDF that was not in their material. Degrees, titles,
   dates, and numbers must survive a reference check.

## `/kelly-jobhunt research`

Goal: a queue of companies worth writing to, each with a real address and a
letter that could only have been written for it.

**Use whatever actually works to find them** — the channels in `job-boards`,
search engines, company career pages, public job aggregators, browser
automation. Depth beats politeness about method here. Three rules do hold:

- **record the source URL for every company and every address** — that is what
  makes the result checkable, and it is the only defence against a hallucinated
  address;
- **do not buy, sell, or import purchased contact lists;**
- **do not use someone's credentials, or bypass a paywall or anti-bot control,
  to reach data you are not entitled to.**

For each address record its role and where it came from, and grade confidence:

- `high` — printed on the company's own careers or contact page;
- `medium` — from a job posting or an aggregator that names the company;
- `low` — an individual's public profile, or a general-purpose inbox.

**Record `evidenceType` and `evidenceDate` on every company.** A score says how
well a company fits; it cannot say whether the role is still open, and the desk
sorts on the second question first — `official-site` above `aggregator` above
`business-match`, score only breaking ties. `evidenceDate` is the day the
evidence was captured, not the day of the import. Leave the type blank when you
genuinely do not know: blank renders amber as 未标注 alongside anything older
than 30 days, and both correctly mean "check before sending". Labelling an
aggregator find as `official-site` to clear that badge puts a possibly-dead role
at the top of the queue, which is the failure the field exists to prevent.

Draft `email-subject` and `email-body` at import time so the queue is reviewable
immediately. Tailor the opening paragraph to that company's specific evidence —
a real posting line, a real product direction — and keep the rest consistent
with `highlights`. Plain text, no HTML, no tracking pixel.

`references/research-playbook.md` has the full method: where addresses actually
come from and how to grade them, what separates a usable match reason from
filler, how to calibrate `matchScore` so the sort keeps meaning something, and
the six ways this step usually goes wrong.

Then import:

```bash
node scripts/import_leads.mjs findings.json           # dry run
node scripts/import_leads.mjs findings.json --apply
```

The import is idempotent: it skips any company key that already exists and any
`company + address` pair already recorded, so widening a search never resets an
approved or sent row. Re-run it freely.

Aim for twenty to thirty companies per round. A longer list does not get read
carefully, and a list that is not read carefully is just slower board-and-pray.

## `/kelly-jobhunt send`

Goal: the user's own mailbox sends the letters they approved.

1. Get the SMTP settings for **their** mailbox — the letters must come from
   their own address, not a shared one. For QQ/163/Gmail this means an app
   password or authorization code, not the account password. Point them at their
   mail provider's settings page; do not walk them through disabling security.
   Only the password is ever required. `SMTP_HOST`, `SMTP_PORT`, and `SMTP_USER`
   are derived from the sender address for the mailboxes people actually use
   (QQ/Foxmail, 163, 126, yeah, Sina, Aliyun, Gmail, Outlook), so a QQ sender
   needs nothing but their 授权码. An explicitly configured value always wins
   over a derived one. Nothing is derived for a company domain — its MX is not
   its submission host.
2. Store it. One command, on Cloud and self-hosted alike:
   ```bash
   node scripts/configure_smtp.mjs --host smtp.qq.com --port 465 --user me@qq.com --pass <授权码> --apply
   # or, to keep it out of shell history:
   SMTP_PASS=xxx node scripts/configure_smtp.mjs --host smtp.qq.com --user me@qq.com --apply
   ```
   This writes four Vault items and records only their **reference names** on
   the profile. Two things about that write are load-bearing, both because the
   Vault API is a **full-document PUT** rather than an upsert:
   - the script reads the existing set and merges — never send a partial set;
   - it writes back **only the personal scope**, and **keeps each item's `id`**.
     On Cloud a read masks every secret to `""` and a blank secret means "keep
     the stored value", matched by id. Strip the ids and that write blanks every
     secret in the scope the script did not set itself. Echo back Space-scoped
     items and the write is refused, because Cloud takes the target scope from
     the items.

   The user can equally add the items in the web app's Vault under a Space or
   API-key scope, with **runtime** ticked. Either way no session restart is
   needed — see step 3.
3. Understand where a value can come from, because the dry run names it:
   - **self-hosted** serves `/api/v1/vault` with real values;
   - **Cloud** serves the same route with every secret masked to `""` — it can
     only tell you an item exists — and serves `/api/v1/vault/runtime` with the
     values of items marked `access.runtime`. That is the same set Cloud injects
     into a task's environment at startup, so reading it over HTTP just removes
     the requirement to have restarted since the item was saved.

   Which routes answer is the only reliable way to tell the two apart. Never
   infer it from the base URL, and never tell the user the Vault is missing —
   that sentence was wrong even when the route 404'd.
4. Send what was approved:
   ```bash
   node scripts/send_emails.mjs           # dry run: prints sender, attachment, and the exact list
   node scripts/send_emails.mjs --apply
   ```
   The dry run reports each of the four settings as 就绪 or 缺失 with where it
   came from (环境变量注入 / Vault / Vault 运行时 / 由发件地址推导) and never
   prints a value. Read
   that list before guessing at a cause: "缺 SMTP_PASS" and "什么都没配" need
   different answers. A failed send leaves the row `queued` so another address
   from the pool can be tried. Report failures per company; never silently drop
   one.
5. **Rehearse with `--test-to` before the first real send**, so SMTP auth, the
   attachment, and the letter itself are proven against an inbox the user owns:
   ```bash
   node scripts/send_emails.mjs --test-to me@qq.com --apply
   ```
   It sends one queued letter — `--test-limit` for more — to that address with a
   `[测试]` subject prefix, and **writes nothing to Busabase**: no contact row is
   touched and every company stays `queued`, because no company was actually
   contacted. Never rehearse by editing contact rows to a test address. That is
   what the first live run did, and it overwrote 25 researched addresses to
   prove one SMTP connection worked.

## Operating Loop

- **Research** — `/kelly-jobhunt research` collects companies and addresses with
  their sources and drafts one letter each.
- **Plan** — the desk sorts by match score and gives each row a stable `#n`, so
  a conversation can say "改第 3 条" unambiguously.
- **Action** — the operator reviews, edits, picks an address, and approves;
  `status: queued` plus `sent-to` and `approved-at` are written. The trusted
  sender then sends and writes `status: sent` plus `sent-at`.
- **Retrospective** — out of scope. Reply detection, reply-rate attribution, and
  follow-up sequencing belong to a Pro variant. Do not add a reply column, a
  funnel chart, or a scheduler here.

## App Artifact

- Keep the complete canonical project under `<skill-root>/content/kelly-jobhunt-app/` and provide a
  working `pnpm --dir <skill-root>/app dev` command.
- Follow the UI and product contract from `$kelly-app-skill-creator`; delegate
  the runtime, SDK, security, validation, and deployment contract to
  `$busabase-app-creator`.
- Read and write every persistent value through `busabase-sdk`. The browser
  writes exactly two things: profile fields, and a company's approval verdict
  plus its edited draft.
- Transport pagination is owned by the provider, not declared per Base. Follow
  `nextCursor` to exhaustion — `research` routinely produces more than one page
  of contact addresses, and a desk that stops at one page silently hides them.
- Writes auto-merge only on a standalone loopback preview. A deployed AirApp
  submits each write as a ChangeRequest for review.
- A standalone OAuth connection verifies accessible Spaces before reading app
  resources. One Space is selected automatically; multiple Spaces require an
  explicit in-app choice that is validated and attached to every proxied SDK
  request.
- Keep deterministic Demo data explicit and non-persistent. Demo may mirror the
  same three-resource shape but must never become the backend, send mail, read
  the Vault, or claim a successful Busabase connection.

## Core Resources

Three application-owned Bases under one Folder, plus four Vault items. Field
slugs, status values, and Vault keys are fixed by `references/jobhunt-schema.md`.

| Resource | Purpose |
| --- | --- |
| `kelly-jobhunt-profile` | One row. Identity, target role, channels, resume source text, resume file name, sender address, onboarding version, and the SMTP Vault reference names. |
| `kelly-jobhunt-companies` | One row per company: match evidence, drafted email, outreach status, the address actually used. |
| `kelly-jobhunt-leads` | Several rows per company: candidate addresses with role, source URL, and confidence. |
| Vault `SMTP_*` | Host, port, user, app password. Values readable only by the trusted sender — from a self-hosted Vault, from Cloud's `/api/v1/vault/runtime`, or from the environment. |

`company-key` is a plain text foreign key, not a Busabase relation field. Two
mutually referencing Bases cannot be created in one ChangeRequest, and the
browser's lazy-provisioning flow cannot perform that two-phase creation.

## Screens

Two screens plus Help & Settings, routed by hash:

- `#/profile` — the profile form, including which channels to search and whether
  SMTP is configured (readiness only, never a value).
- `#/all`, `#/to-send`, `#/sent` — one list of companies with a detail pane;
  `#/<view>/<id>` selects a row.
- `#/settings/<tab>` — guide, resources, connection.

The sidebar shows brand, then what the human must do now, then **the next
subcommand to run**, then navigation, then Help & Settings.

## Stop Conditions

Stop and report rather than proceeding when: the profile is incomplete; a
company has no address; a send would go to a guessed address; the Vault has no
SMTP credentials; or an import would overwrite a company already approved or
sent.
