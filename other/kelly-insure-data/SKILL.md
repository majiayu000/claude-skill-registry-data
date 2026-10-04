---
name: kelly-insure-data
description: Insurance-industry App-in-Skill for read-only data governance, backed by an operator-provisioned Busabase workspace (one Drive node for the file drive plus four Bases for QA pairs, featured information, insurer notices, and user feedback) and trusted export/restore/PDF-text-backfill scripts. Use when the user invokes $kelly-insure-data or /kelly-insure-data, wants an insurance data workspace with UI, needs to review insurance files, metadata completeness, QA pairs, featured information, insurer notices, or user feedback, wants to back up or restore a Kelly Insure Data Busabase workspace from local PDFs, or wants Busabase Drive/Base data surfaced for data quality review and ongoing data governance.
metadata:
  category: industry-intel
  tags:
    - risk:read-only
    - industry:insurance
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-insure-data
    resources:
      - featured
      - notices
      - qa
      - feedback
    risk: read-only

---

# Kelly Insure Data

## Overview

Kelly Insure Data is a Busabase Cloud App-in-Skill. Its canonical product surface is the AirApp in Busabase, not a separate local-data product. The same Hono source supports an explicitly requested local preview with OAuth connection bootstrap. Use this skill as Kelly's insurance data-entry and data-governance cockpit: it reads one Busabase Drive node for the file drive, one Base for insurance QA pairs, two Bases for featured information and insurer notices, and one Base for user feedback — surfacing metadata completeness, missing fields, and review status before data becomes trusted insurance knowledge.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, give the user the clickable AirApp URL. Start localhost only when local preview/debugging is explicitly requested; it uses the same Busabase resources and never offers another data provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-insure-data-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Architectural note: an operator-provisioned workspace, not an app-owned one

Every Base and the Drive node here belong to an existing production
insurance dataset — they are not a Folder+Bases tree this AirApp creates or
owns the way most other Kelly App-in-Skills do. There is nothing for a
read-only reader to safely auto-create in someone else's canonical dataset,
so:

- `content/kelly-insure-data-app/app/js/config.js` declares the Drive node and the four Bases (by slug)
  for lookup only; page size is the reader's own concern, not a per-Base
  declaration, so each Base is read to exhaustion. It does **not** go through
  `resource-provisioning.js`'s create-if-missing/ownership-metadata flow used
  by every other converted skill in this batch — that flow is the wrong model
  for "connect to an existing external workspace."
- `content/kelly-insure-data-app/app/js/providers/busabase-provider.js` resolves the Drive node and
  each Base by slug (via `content/kelly-insure-data-app/app/js/insure-client.js`, a raw-fetch client —
  see below) and degrades a missing resource to a `snapshot.warnings` entry,
  exactly like the retired `lib/data-provider/busabase-provider.ts` did. It
  never shows an "Initialize workspace" setup screen and never creates a
  Folder, Drive, Base, or record.
- An operator provisions and repairs the Drive node and Bases out-of-band
  with the trusted scripts in the skill-root `scripts/` directory
  (`export_busabase_snapshot.mjs`, `restore_busabase_snapshot.mjs`,
  `backfill_pdf_metadata.mjs`), documented below.

## Architectural note: Drive/Asset reads bypass busabase-sdk

`busabase-sdk` (the vendored package every other converted skill uses for
Bases/records reads) only wraps `/api/v1/nodes`, `/api/v1/bases`, and
`/api/v1/records`. It has no equivalent for the Drive/Asset REST surface
(`/api/v1/drives/*`, `/api/v1/assets/*`) this skill's file drive needs.
`content/kelly-insure-data-app/app/js/insure-client.js` is therefore a small browser module that talks
straight to the same-origin `/api/v1/*` proxy in `content/kelly-insure-data-app/server.js` with plain
`fetch` — a port of the read paths (`resolveDrive`, `resolveBase`,
`listDriveFiles`, `listRecords`) from the retired
`lib/data-provider/busabase-client.ts`, with two endpoint paths corrected
against a live `busabase@0.11.0` server during porting: records listing is
`GET /records` (not `/records/paged`, verified against busabase-sdk's own
`recordContract.list` route), and a Drive's file listing/metadata come from
`GET /nodes/{nodeId}` (not `/drives/{nodeId}` or `/drives/{nodeId}/files`,
both 404). See the header comment in `insure-client.js` for details.
`scripts/lib/busabase-client.mjs` is the same corrected client ported for
the trusted skill-root scripts, using the operator's own
`BUSABASE_BASE_URL` / `BUSABASE_API_KEY` / `BUSABASE_SPACE_ID` credentials
(never the AirApp's ambient OAuth session), since those scripts also need
the write/upload endpoints (`assets/upload-urls`, `assets/confirmations`,
node/drive/record ChangeRequests) that
`busabase-sdk` does not cover either.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Insure Data overview"></td>
    <td width="50%"><img src="assets/screenshots/files.webp" alt="Kelly Insure Data file drive"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Insurance governance cockpit with counts, data quality score, metadata coverage, and records requiring cleanup.</td>
    <td><strong>文件盘</strong><br>Busabase Drive-node file list with metadata completeness and missing-field diagnostics.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/qa.webp" alt="Kelly Insure Data QA base"></td>
    <td width="50%"><img src="assets/screenshots/news.webp" alt="Kelly Insure Data news base"></td>
  </tr>
  <tr>
    <td><strong>问答</strong><br>Canonical insurance QA records with source, review status, and answer-quality warnings.</td>
    <td><strong>资讯精选 / 保司通知</strong><br>Featured information and insurer notices combined, with carrier, dates, and source URLs.</td>
  </tr>
</table>

## Boundary

- The AirApp reads the Busabase Drive node and the four Bases only; it is
  entirely read-only and must NEVER create, update, or delete a Busabase
  node, Base, or record (`readOnly: true`, no `writeProcedures`).
- Never expose API keys, tokens, or cookies in UI state, logs, screenshots,
  or chat.
- Treat insurance data quality as high-stakes: the trusted scripts preserve
  source attribution, dates, jurisdiction, carrier/product names, and
  original wording where possible.
- If the user asks for data entry or cleanup, propose it as a reviewable
  change (a manifest edit plus `restore_busabase_snapshot.mjs --apply`, or a
  direct Busabase ChangeRequest the user reviews) — never silently mutate
  the canonical workspace.

## Busabase Resources

Declared in `content/kelly-insure-data-app/app/js/config.js` and the generated template sidecars under `content/`, resolved by
slug (IDs are never required):

- `drive` (`kelly-insure-data-files`): the file drive — insurance PDFs/docs with
  governance metadata (`policy_type`, `carrier`, `region`, `effective_date`,
  `status`, ...).
- `featured` (`kelly-insure-data-featured`) and `notices` (`kelly-insure-data-notices`,
  legacy alias `news`): combined in the `#/news` route, each item tagged
  `featured` or `notice`.
- `qa` (`kelly-insure-data-qa`): canonical insurance question/answer pairs.
- `feedback` (`kelly-insure-data-feedback`): user feedback records.
- `prompts` (`insurance-prompts`, 预置提示词): the preset prompt library read by
  the insure miniapp, **not** by this AirApp. It is not declared in
  `content/kelly-insure-data-app/app/js/config.js` and never appears in the snapshot, but it lives in the
  same workspace folder as the four Bases above, so an operator provisioning or
  repairing this workspace must keep it — with the field contract in
  `references/insure-data-schema.md`.

See `references/insure-data-schema.md` for the exact normalized snapshot
shape and `references/restore-manifest-schema.md` for the backup/restore
manifest shape.

## Views

- `#/overview`: counts, data quality score, metadata field coverage, and
  records needing governance.
- `#/files` ("文件盘"): Drive-node files with metadata fields and missing-field
  badges.
- `#/qa` ("问答"): QA Base records with question/answer, source, and
  completeness.
- `#/news` ("资讯精选 / 保司通知"): Featured Information and Insurer Notices
  combined, each tagged `featured` or `notice`.
- `#/feedback` ("用户反馈"): Feedback Base records with content, source,
  rating, and status.
- `#/settings`: sanitized Busabase target slugs and Base field schemas. Never
  exposes tokens.

## Backup / Restore / PDF Text Backfill

These are trusted skill-root Node scripts (own `scripts/lib/busabase-client.mjs`,
raw fetch, the operator's own `BUSABASE_BASE_URL`/`BUSABASE_API_KEY`/`BUSABASE_SPACE_ID`).
They read local PDF bytes from disk, which a browser AirApp cannot do.

```bash
cd skills/kelly-insure-data
npm run busabase:export -- --output content/kelly-insure-data-app/.data/busabase_restore_manifest.json
npm run busabase:restore -- --manifest content/kelly-insure-data-app/.data/busabase_restore_manifest.json --files-root /path/to/local/pdf-backup --dry-run
npm run busabase:backfill-pdf-text -- --drive-node-id <node-id> --files-root /path/to/local/pdf-backup --limit 5
```

- `busabase:export` writes a portable restore manifest (folder/Drive/Base
  shape, Drive file paths, sanitized asset metadata, Base records). It never
  embeds PDF bytes.
- `busabase:restore` previews restoration from that manifest plus a local PDF
  backup directory; add `--apply` only when the user explicitly asks to
  recreate a missing folder, Drive files, Bases, or records.
- `busabase:backfill-pdf-text` parses local PDFs and previews the Asset text
  slot write and generated governance metadata. Add `--apply` to write the
  text slot (`PUT /api/v1/assets/{assetId}/text`) and sanitized metadata
  (never `parsed_text`) back to Busabase. The old
  `busabase:backfill-pdf-metadata` command remains available as an alias.

## Demo Mode

- `?demo=1` (or `?demo=overview`) opens a deterministic offline dataset: 4
  files, 4 QA pairs, 3 news items (2 featured, 1 notice), and 2 feedback
  items with varying governance completeness.
- `?demo=files`, `?demo=qa`, `?demo=news`, `?demo=feedback`, `?demo=settings`
  select named scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads Busabase, tokens, or local production data.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-insure-data-app dev` only when local preview/debugging is explicitly
requested. UI language supports Chinese (primary) and English chrome with an
`Auto` default.

## Deployed AirApp node: `hk-insurance-workbench`

The workspace already contains a deployed AirApp node, `hk-insurance-workbench`
(港险资料库工作台), sitting at the space root beside the 港险公司资料库 folder. It
is **not** a deployment of this skill's `content/kelly-insure-data-app/` artifact — it is an older
hand-written five-file viewer (`package.json`, `server.js`, `index.html`,
`app.js`, `styles.css`) that predates the AirApp migration. Treat it as a second,
much smaller surface on the same dataset: a read-only tile row of record counts
per Base plus the five most recently updated records.

Runtime contract, and the reason this node was broken for months:

- Busabase starts an AirApp with `npm install` then literally `npm run dev`.
  A `package.json` with only a `start` script never boots — the runtime reports
  `Missing script: "dev"`. Busabase now rejects such a write
  (`AIRAPP_NOT_RUNNABLE`), but nodes created before that check can still be in
  this state.
- A bundler dev server (`vite`, `next`, `webpack`, …) cannot boot in this
  runtime at all, so renaming a Vite scaffold's script to `dev` is not a fix.
  Serve from a plain Node server.
- A running AirApp is proxied same-origin under
  `/api/airapp-preview/{nodeId}/`, so browser code reaches Busabase with an
  absolute `/api/v1/...` path, using the session of the user who clicked Run.
  There is no API-key handling and no bridge prefix in front of `/api/v1`.
- Reads use `GET /api/v1/records?baseId=…&limit=…` (cursor paging via
  `nextCursor`) or `GET /api/v1/records/page` (numbered pages). Record values
  live under `headCommit.payload`, keyed by field slug.
- The cloud engine is Nodepod, an in-browser Node runtime, and two habits that
  are fine under real Node kill the dev server there. This node hit both:
  `fileURLToPath(new URL(".", import.meta.url))` throws, because
  `import.meta.url` is not guaranteed to be a `file:` URL — read static files
  relative to cwd (`./index.html`) instead; and
  `listen(port, function () { this.address().port })` throws
  `this.address is not a function`, because the listen callback's `this` is not
  bound to the server — log a captured `port` variable instead. Both throw
  after `npm run dev` starts, so the symptom is `[dev server exited with code 1]`
  and a run stuck before "ready". Busabase's own `PURE_HTML_SERVER_JS` demo
  still uses the second shape, so it is not a safe template to copy verbatim.

Fixed in this node (version 0.3.2): the missing `dev` script; a request to a
non-existent `/__busabase_api__/api/v1/records/paged` prefix and route; reading
`headCommit.fields` instead of `headCommit.payload`; the two Nodepod crashes
above; and a hardcoded three-Base id list that had gone stale. Bases are now resolved by slug from
`GET /api/v1/bases`, and a slug that no longer resolves degrades to a `—` tile
plus a warning instead of failing the page.

Open question for the operator, deliberately left open: whether to keep this
node as a thin viewer or replace its contents with this skill's `content/kelly-insure-data-app/` artifact.
Keeping both means two divergent readers of one dataset; replacing means
uploading the full `content/kelly-insure-data-app/` tree, including the vendored SDK, into the node.

## File Contract

Read `references/insure-data-schema.md` before editing the app or
`content/kelly-insure-data-app/app/js/config.js`, and `references/restore-manifest-schema.md` before
changing the trusted export/restore scripts.

## Safety Defaults

- Never create, update, or delete a Busabase node, Base, or record from the
  AirApp. Only the trusted skill-root scripts write, and only with the
  operator's own credentials and an explicit `--apply`.
- Keep real tokens in environment variables only; never commit
  `config.local.json`-style files, local PDF backups, or anything under
  `content/kelly-insure-data-app/.data/`.
- A missing Drive node or Base degrades to a visible warning, never a
  blocked or broken view.
