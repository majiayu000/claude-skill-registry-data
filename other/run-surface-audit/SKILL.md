---
name: run-surface-audit
description: >
  Internal /ace:run step — Audit a run's public summary page before it is shared.
user-invocable: false
---

# Run-surface audit — what an outsider actually gets

**Run workspace:** when the dispatch carries a `run_workspace:` block, its values replace the `.env` ones this skill names — `ACE_HQ_DOMAIN` → `run_workspace.hq_domain`, `${ACE_WEB_WORKSPACE}` → the run's `workspace:` from `run_state.yaml` (pass `--workspace`) — and a partner workspace never falls back to `.env`. Contract: [`skills/_run-workspace.md`](../_run-workspace.md).

The **run-summary page is ACE's canonical shareable output** and, since
2026-08-13, the first thing an external partner ever sees of a run. It is
served by ace-web from `run_state.yaml` live in Drive, at:

```
${ACE_WEB_BASE_URL}/opps/${ACE_WEB_WORKSPACE}/<opp-slug>/runs/<run-id>/summary
```

Defaults: `ACE_WEB_BASE_URL=https://labs.connect.dimagi.com/ace`,
`ACE_WEB_WORKSPACE=dimagi-team`. It is un-authed — the URL is the secret —
which is exactly why what it shows an anonymous visitor has to be right.

## Inputs

Pipeline-only: audits one run's public run-summary page; the run is the object (§ Process).

## Why this skill exists, and what it replaces

**It supersedes `run-summary-qa`.** That skill drove
`scripts/check-summary-links.py`, which asked one question — *does this URL
resolve?* — and answered it well. On 2026-08-14, `spark-facilitator/20260813-2126`
went out with **twelve** defects and the checker printed
`12 links · 0 BROKEN`, exit 0. Eleven of the twelve were not link reachability.
A day was spent finding them by hand, by eye.

Those twelve are now this capability's regression corpus
(`test/lib/run-surface-audit.test.ts`, one `describe` each). The old checker's
rules — the `PRIVATE-DELIVERABLE` class, `MEMBER-GATED`, relative-URL
resolution, per-reviewer membership read-backs — are ported intact into
`lib/run-surface-audit.ts` and still enforced.

**The governing rule: a check that cannot see the thing it checks is worse than
no check.** The single most expensive failure of that day was an agent
"verifying" open questions by counting a payload key named `questions` when the
field is `items` — it reported 0 forever and nearly sent someone to fix a
working feature. So this auditor declares every section and key it reads up
front, and an unknown section, a vanished section, or a populated section
missing the key it reads all **block**. It never reports a silent zero.

## When to run

- **Before sharing the run-summary link with anyone** — that is the whole
  trigger. A stakeholder email, a Slack message, a gate.
- At the end of an `/ace:run`, when the orchestrator surfaces the URL.
- After editing `run_state.yaml` products that feed the summary.
- After an ace-web deploy that touched `apps/opps/summary.py` or the summary
  page components.

## Process

### 1. Gather the inputs that turn "unverified" into "verified"

All are blocking when absent, deliberately — see § Unverified blocks.

```
# The run's own record of what it produced.
resolve_opp_path(slug) → opp_root_id
drive_list_folder(runs_id) → the run folder
drive_read_file(<run_state.yaml file id>, writeToPath="/tmp/<run>-run_state.yaml")

# The run FOLDER's contents. Not the same input, and not redundant:
# `/ace:qa-deep` deliberately writes NOTHING into run_state.yaml (so a
# later `/ace:run` resume is unaffected), so the two deep-QA verdict
# FILES are the only record that the deep gate ran. run_state cannot
# answer it, at all.
drive_list_folder(<run folder id>)                 # → 5-ocs, 6-qa-and-training, …
drive_list_folder(<5-ocs folder id>)
drive_list_folder(<6-qa-and-training folder id>)
# Write the run-relative paths as a JSON array to /tmp/<run>-files.json, e.g.
#   ["run_state.yaml", "decisions.yaml",
#    "5-ocs/ocs-chatbot-eval_verdict-deep.yaml",
#    "6-qa-and-training/app-ux-eval_verdict-deep.yaml"]
```

If you are preparing the page **for named people**, also get the membership
read-backs (`scripts/grant-review-access.ts --dry-run` for HQ + OCS;
`connect_list_org_members({ organization_slug })` for Connect — read-only;
never `connect_add_org_member`, which invites and emails anyone absent, ace#2986) and write them as `{"hq": {"a@b.c": true}, "ocs": {...}, "connect": {...}}`.

### 2. Run the audit

```bash
ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/audit-run-surface.ts" <opp-slug> <run-id> \
  --render \
  --run-state /tmp/<run>-run_state.yaml \
  --run-files /tmp/<run>-files.json \
  [--reviewer sophie@example.org ...] [--memberships /tmp/memberships.json] \
  [--doc-source /tmp/doc-sources.json] \
  [--workspace dimagi-team] [--base https://labs.connect.dimagi.com/ace] [--json]
```

`--render` launches headless Chromium in a **fresh anonymous context**. It is
where four of the twelve defects live and it is not optional for a share gate;
without it the audit blocks with `RENDER-UNVERIFIED`.

Exit 0 iff there are **no `broken` and no `misleading`** findings.

### 3. Fix, then re-run until it is clean

Every finding names its own fix. The common ones:

| Finding | What it means | Fix |
|---|---|---|
| `LINK-PRIVATE-DELIVERABLE` | an ACE-authored Google Doc that is shared with nobody — the recipient hits "You need access" | `drive_set_anyone_with_link` on the file id (`role: 'commenter'` when they should be able to leave feedback), then re-audit for `OK 200` |
| `LINK-BROKEN` | 404 / 5xx / DNS | fix the product URL or stop surfacing it. A **relative** link that 404s usually means a missing deployment path prefix — that is an ace-web serializer bug, not a data bug |
| `LINK-ACCESS-MISLABELLED` | the page says `public`, an outsider gets a gate | either share it or correct the tag. The page is telling the reader something untrue |
| `LINK-INTERSTITIAL` | a Drive **download** link answered `200` with a web page instead of the file's bytes — the reader gets Google's virus-scan or quota interstitial | share the file anyone-with-link **and** confirm by magic bytes, never by HTTP 200. Observed 2026-09-06 on two `.xml` forensics files that a status-only check had certified public (ace#1868 / ace#1831) |
| `LINK-UNTAGGED` | a link with no `access` tag | tag it in ace-web so the page can say why it cannot be opened. Untagged, it reads as broken rather than deliberate |
| `MISSING-ARTIFACT` | the run made it; the page does not link it | surface it in ace-web, or say on the page why it is withheld |
| `ASSISTANT-PUBLIC-URL-WITHHELD` | the page invites the reader to ask questions about the opportunity and the only link under that invitation is the **admin-only** OCS console, while the run's own anonymous chat URL is derivable from the payload the reader already has | either render the public chat link (`access: public`) beside the console link in ace-web `apps/opps/summary.py`, or change the copy so the page stops inviting. **Whether an un-authed reader should drive LLM spend on the per-opp bot is a product call this finding does not make** — it refuses to certify a page that promises what it does not deliver, and both remedies clear it. Self-retiring: any URL on OCS's `start/` route silences it (ace#1839) |
| `DEEP-QA-HIDDEN` | `/ace:qa-deep` ran and the page does not say what it found | surface the verdicts through ace-web `_read_deep_qa`. Phase 9 `llo-launch` refuses activation on a missing or stale deep verdict, so a silent page and a never-tested run read identically |
| `DEEP-QA-SCORE-WITHOUT-GATE` | a deep-QA score on the page with no gate beside it | carry `gate.disposition` and the Fail count, and lead with the gate. `spark-facilitator/20260828-0703` scored **8.03** against a **7.0** bar and its gate was **`iterate`** anyway — `--deep` needs zero Fails and two answers fabricated safety-adjacent procedure. A bare number reads as a pass |
| `DOC-LITERAL-MARKDOWN` | the reader is looking at raw `##` and `**` | republish via `drive_create_doc_from_markdown` (Drive **converts**) rather than uploading the `.md` as `text/plain` |
| `DOC-SCREENSHOTS-ABSENT` | a step-by-step guide published with zero images while the run captured screenshots | Render, **then embed**: `scripts/embed-doc-screenshots.ts` (`insertInlineImage` via `docs_batch_update`). The importer drops `![alt](drive:<id>)` outright, and sizes a real https src at its natural 1080x2400 — hence the second step |
| `CONF-SECRET-EXPOSED` | a secret-shaped value on the anonymous payload | stop serving it, or add it to `ACCEPTED_PUBLIC_SECRETS` **with the reasoning that makes it safe** — and mirror that in ace-web's `test_public_surface_contract.py` |
| `CONF-PRIVATE-REVIEW-LINKED` | a privately-captured reviewer's ledger, republished | ace-web `_read_feedback` must omit a non-public ledger for a non-member |
| `CONF-CLAIM-EVIDENCE-EXPOSED` | a claim's AUDIT record (`evidence` — Drive file ids, MCP atom signatures, ACE-internal read-path caveats) reached the anonymous summary | ace-web `_read_claims` must null `evidence` for a non-member. The counterpart-facing half is `says`; `evidence` is written for whoever may later have to re-derive the verdict, and it is the class `agent-turn-review` § F bans from counterpart comms (ace#2386, ace#2420) |
| `CLAIMS-DENOMINATOR-MISMATCH` | the claims section's tally does not match the claims rendered under it | ace-web `_read_claims` must count the rows it emits. `broken`, not `misleading`: the claim set IS the denominator, and a header reading "8/8 met" over seven rows restores exactly the silence the mechanism exists to remove (ace#2420) |
| `CONTRACT-*` | the auditor's assumptions about the payload are wrong | reconcile `lib/run-surface-audit.ts` against ace-web `apps/opps/summary.py`. **Do not relax one side** — both are frozen contracts |

A change that lives in ace-web code is live only after that PR deploys; a change
that is pure `run_state` data is live on the next fetch (the audit passes
`?force=1` to bypass the 60s summary cache).

### 4. Then run the judged half

`run-surface-audit-eval` grades what determinism cannot: whether an outsider
understands what they are looking at and what they are being asked to do.
QA gates eval — do not run eval on a surface that is still `NOT SAFE TO SHARE`.

## Unverified blocks — "we did not check" is not "it is fine"

Five checks refuse to certify without their inputs, and each one blocks exactly
as a broken link does:

| Blocking finding | Why it is not a warning |
|---|---|
| `COMPLETENESS-UNVERIFIED` | without `run_state.yaml` nothing compares the page against what the run PRODUCED. The PDD and the Work Order were absent from the page entirely and nothing noticed, because "absent" and "the run hasn't got there yet" look identical |
| `RENDER-UNVERIFIED` | four defects are invisible to a payload check. They shipped. Without it a same-origin **client-side** sign-in wall also stays invisible: it answers `200` at the requested URL and serves a JS shell, so the status line, the final URL and the raw body all read as open. The workbench link on `hh-poverty-targeting/20260828-0702` fetched as `200` with 443 bytes reading "ACE Web" and rendered as "Sign in with your Connect account to continue" (ace#1868) |
| `MEMBER-UNVERIFIED` / `REVIEWERS-UNDECLARED` | the probe is anonymous; anonymous reachability only proves a link works for SOMEBODY. A signed-in non-member gets a flat 404 — indistinguishable from "this run does not exist" — and reports it to us as a broken link (ace#913, ace#916, ace#1060) |
| `DOC-FIDELITY-UNVERIFIED` | nothing compared what was PUBLISHED against what was WRITTEN. One guide lost 44 screenshots and 224 words with every content check green |
| `DEEP-QA-UNVERIFIED` | without a run-FOLDER listing nothing can tell "the deep gate was never run" from "it ran, said `reject`, and the page hid it". `run_state.yaml` cannot answer this one — `/ace:qa-deep` writes no pointer into it by design — so `--run-state` does not substitute |

Treating any of these as fine **is** the bug. If you genuinely cannot get an
input this session, say so explicitly in the report — do not certify around it.

### `--doc-source` is a map you may supply PARTIALLY

`/tmp/doc-sources.json` maps each published doc url to the markdown it was
published from. Supply whatever you can recover; a partial map **narrows**
`DOC-FIDELITY-UNVERIFIED` to the documents still missing a source. It never
switches the check off — a url you leave out is unverified, and says so.

To stand the check down for a document that genuinely has **no** source
artifact, give that url an explicit `null`. That is a deliberate, per-url
claim; silence never means it.

```json
{
  "https://docs.google.com/document/d/<flw-guide>/edit": "# FLW guide\n...",
  "https://docs.google.com/document/d/<work-order>/edit": null
}
```

(Before ace#1687 a partial map made the finding vanish for every url absent
from it — one entry silenced five documents on a live run.)

**Where to GET the markdown (ace#1687 half 2).** The six documents composed
as markdown persist their exact source next to the published Doc as a sibling
`<name>.source.md` — a real `text/markdown` file, so `drive_read_file`
returns the bytes the Doc was built from. **Look for the file rather than
reasoning from a version:** its presence in the run folder is the fact, and
`drive_list_folder` already tells you.

| Published Doc | Source to read |
|---|---|
| `1-design/idea-to-pdd.md` | `1-design/idea-to-pdd.source.md` |
| `6-qa-and-training/training-{faq,flw-guide,llo-guide,quick-reference,onboarding-email}.md` | the matching `…​.source.md` |

Build the map by reading each `.source.md` and keying it on the published
doc's url. One document deliberately has no source and takes the explicit
`null` sentinel rather than a guess:

- **`1-design/pdd-to-work-order.gdoc`** — built by `docs_copy_template`
  (`drive.files.copy` + `replaceAllText`), Doc to Doc with **no markdown
  importer on the path**, so the content-dropping class this check guards
  cannot occur and no composed markdown exists. Its analogous preventer is
  the surviving-`{{` token scan in `skills/pdd-to-work-order` step 5.

**Check the companion's `mimeType`, not just its name (ace#2102).** A
`.source.md` that `drive_list_folder` reports as
`application/vnd.google-apps.document` is NOT a source — it is a second
rendered Doc wearing the source's filename, and comparing it to the published
Doc compares two outputs of the same importer and reports a green that means
nothing (the exact failure ace#1991 was filed for). Runs written before
ace#2102 can carry one, because find-or-create used to land correct
`text/markdown` bytes inside a pre-existing Doc and return success. Report
those as `UNVERIFIED` with the observed mimeType named, the same as an absent
source — never as a comparison. `drive_list_folder` already gives you the
mimeType in the same call that tells you the file is there, so this costs
nothing. A re-run of the producing skill now heals it (the mismatched file is
binned and replaced at the right type).

**On a run predating this fix the `.source.md` files simply are not there** —
the markdown was consumed at publish time and is unrecoverable. `UNVERIFIED`
is the correct and only honest result for those documents; do NOT reconstruct
a "source" by re-exporting the published Doc, which would compare the document
to itself and report a green that means nothing. An absent source file is also
not the `null` sentinel: `null` claims no source will ever exist, which is true
only for the two documents named above.

Registered in `lib/artifact-manifest.ts` (`sourcePersisted`, plus the
`.source.md` companion entries, all `required: false` so older runs do not
retroactively fail); enforced by
`test/lib/source-persisted-artifacts.test.ts`.

## Report

State, in this order:

1. The summary URL, and that it was probed **anonymously**.
2. Links probed, by class.
3. Findings by severity — **broken**, **misleading**, **improvement** — each
   with what a reviewer would experience, and the fix applied.
4. What was **not** verified and why (naming each `*-UNVERIFIED`).
5. `SAFE TO SHARE` only when there are zero broken and zero misleading. Never
   claim it while a `MEMBER-GATED` link is unresolved for the people you are
   about to send it to.

Severity language matters to the reader: **broken** = a reviewer hits a wall;
**misleading** = the page states something untrue; **improvement** = it would
confuse or underserve them. On 2026-08-14 the worst defects were *misleading*,
which is precisely why a checker that only knew reachable-vs-not certified them.

## What this cannot catch, and why

Say these out loud in the report rather than implying coverage.

- **The end-to-end write round-trip.** The audit proves both public write paths
  are live by sending a deliberately INVALID body and asserting the handler
  rejects it on validation (a 422 means the route exists, is wired, and is
  reachable anonymously). It does **not** post a real comment: there is no
  delete endpoint, writes land as feedback records in the opp's Drive folder,
  and **fabricated content must not go into a real opp**. The full round-trip —
  comment and decision edit persisted and read back — is covered hermetically in
  ace-web against a fake Drive (`apps/opps/tests/test_api.py`:
  `test_reaction_shows_up_on_the_next_summary_read`,
  `test_edit_shows_up_on_the_next_summary_read`).
- **Whether the CONTENT is any good.** Jargon, overstatement, an unclear ask —
  that is `run-surface-audit-eval`'s job, and it needs an LLM.
- **Whether a named reviewer's membership read-back is current.** The audit
  consumes the read-back; it does not perform it. A read-back from last week is
  a hypothesis.
- **Slides and Sheets rendering.** Google Slides has no plain-text export, so a
  training deck is judged by link reachability only.
- **Anything gated behind the member payload.** By construction — a member's
  view is a different document and a different test.

## MCP tools used

- `resolve_opp_path`, `drive_list_folder`, `drive_read_file` — to fetch the
  run's `run_state.yaml` (and any source markdown for `--doc-source`).
  `drive_list_folder` does double duty: it also produces the run-folder
  listing `--run-files` needs, which is a SEPARATE fact from `run_state`
  — the deep-QA verdicts leave no trace there.
- `drive_set_anyone_with_link` — to fix a `LINK-PRIVATE-DELIVERABLE`.

Everything else is read-only anonymous HTTP plus a headless browser
(`scripts/audit-run-surface.ts`, `scripts/audit-run-surface-render.ts`,
`lib/run-surface-audit.ts`).
