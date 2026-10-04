---
name: qa-bug-filer
section: pipeline
description: "Deduplicates issues.jsonl and files Azure DevOps Bug work items with annotated screenshots attached"
model: sonnet
notes: "Sonnet only for bug-description prose. Dedup, API calls, and attachment upload run on Haiku-tier mechanical steps."
---

# qa-bug-filer

## Overview

Reads `issues.jsonl` files produced by audit skills, deduplicates them, creates Azure DevOps Bug work items via REST API, and attaches annotated screenshots to each filed bug.

---

## Your Role

You are the bug filer. Your responsibilities:

- **Never file duplicate bugs** for the same defect. One Bug work item per unique `(issueType + url + viewport + browser)` combination, per run.
- **Respect dry-run mode.** If `dry_run = true` in `argus/customize.toml`, print what would be filed but do not create anything in ADO.
- **Attach evidence.** Every filed bug should have a screenshot — annotated if available, clean otherwise.

---

## On Activation

🚨 **CRITICAL — DO NOT REGENERATE THE BUG-FILING SCRIPT.**

A **permanent, audited** script lives at `{project-root}/scripts/file-bugs.cjs`. It is the single source of truth for bug filing. It already handles:
- Reading all `.jsonl` issues from the run directory
- Deduplicating by `issueType + route + viewportClass + browser`
- Severity sorting; **files ALL issues by default (no cap)** — set `max_bugs`/`QA_MAX_BUGS` to a positive integer only if you want a spam cap
- Writing the HTML body to **BOTH** `Microsoft.VSTS.TCM.ReproSteps` AND `System.Description`
  (Critical — ADO's Bug template displays ReproSteps; only setting Description leaves the ticket looking empty.)
- Attaching the annotated screenshot (or clean screenshot fallback) via the ADO attachments REST API
- Writing the result log to `.tmp/<run-id>/bugs-filed.jsonl`

**The orchestrator MUST NOT generate its own copy of this script.** Each new audit must call the permanent script directly. Re-generating it has historically dropped the ReproSteps field and broken ticket bodies (Bug filed in run-006).

### The ONE step to file bugs

```powershell
node "{project-root}/scripts/file-bugs.cjs" "<run-id>"
```

Or in bash:
```bash
node "{project-root}/scripts/file-bugs.cjs" "<run-id>"
```

Stream the output. The script prints `✓ #<bugId>` per filed bug with `body:both-fields` and `attach:<status>` markers so you can verify in real time that both fields and attachments are populated.

### What if the run has no issues?

The permanent script handles the empty case gracefully — it prints `Collected 0 issues` and exits 0 without making any ADO calls.

### What about dry-run mode?

The permanent script always files real bugs when invoked. To prevent filing, do not invoke it. The argus orchestrator's Step 8 already checks `dryRun` in `customize.toml` BEFORE calling this skill — if `dryRun = true`, the orchestrator skips bug filing entirely.

### Step 4 — Attach Screenshots (MANDATORY)

For each successfully filed bug, attach the screenshot. This is a **two-step ADO REST API operation**:

#### 4a — Upload the file as an attachment

```
POST https://dev.azure.com/{org}/{project}/_apis/wit/attachments?fileName={filename}&api-version=7.1
Content-Type: application/octet-stream
Authorization: Basic base64(":<PAT>")
Body: <raw PNG bytes>
```

Response contains `{ id, url }`. The `url` is the attachment GUID URL — save it.

#### 4b — Link the attachment to the bug

```
PATCH https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{bugId}?api-version=7.1
Content-Type: application/json-patch+json
Body: [
  {
    "op": "add",
    "path": "/relations/-",
    "value": {
      "rel": "AttachedFile",
      "url": "<url from step 4a>",
      "attributes": { "comment": "Annotated screenshot" }
    }
  }
]
```

#### Priority order for which file to upload

1. If `annotatedScreenshotPath` is set and the file exists → upload it.
2. Else if `screenshotPath` is set and the file exists → upload the clean screenshot.
3. If neither → log a warning, continue (do not fail the bug filing).

#### Required Node.js example (the runtime `.cjs` MUST include this — not optional)

```js
const fs = require('fs');
const https = require('https');

async function attachScreenshot(orgUrlPath, projectName, bugId, pat, filePath, comment = 'Annotated screenshot') {
  if (!filePath || !fs.existsSync(filePath)) {
    console.log(`    ⚠ no screenshot to attach for bug #${bugId}`);
    return null;
  }
  const fileName = require('path').basename(filePath);
  const fileBuf  = fs.readFileSync(filePath);
  const auth     = Buffer.from(`:${pat}`).toString('base64');

  // 4a — upload bytes
  const uploadRes = await new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'dev.azure.com',
      path: `/${orgUrlPath}/${projectName}/_apis/wit/attachments?fileName=${encodeURIComponent(fileName)}&api-version=7.1`,
      method: 'POST',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/octet-stream',
        'Content-Length': fileBuf.length
      }
    }, res => {
      let data = ''; res.on('data', c => data += c);
      res.on('end', () => { try { resolve({ status: res.statusCode, body: JSON.parse(data) }); } catch(e) { resolve({ status: res.statusCode, body: data }); } });
    });
    req.on('error', reject);
    req.write(fileBuf); req.end();
  });

  if (uploadRes.status !== 200 && uploadRes.status !== 201) {
    console.log(`    ✗ attachment upload failed (HTTP ${uploadRes.status})`);
    return null;
  }
  const attachmentUrl = uploadRes.body.url;

  // 4b — link to the bug
  const patchBody = JSON.stringify([{
    op: 'add',
    path: '/relations/-',
    value: { rel: 'AttachedFile', url: attachmentUrl, attributes: { comment } }
  }]);
  const linkRes = await new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'dev.azure.com',
      path: `/${orgUrlPath}/${projectName}/_apis/wit/workitems/${bugId}?api-version=7.1`,
      method: 'PATCH',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/json-patch+json',
        'Content-Length': Buffer.byteLength(patchBody)
      }
    }, res => {
      let data = ''; res.on('data', c => data += c);
      res.on('end', () => resolve({ status: res.statusCode }));
    });
    req.on('error', reject);
    req.write(patchBody); req.end();
  });

  if (linkRes.status === 200) {
    console.log(`    ✓ attached ${fileName} to bug #${bugId}`);
  } else {
    console.log(`    ✗ link-to-bug failed (HTTP ${linkRes.status})`);
  }
  return attachmentUrl;
}
```

Call this for every filed bug. **A runtime `.cjs` that omits this function is incomplete — do not skip it.**

### Step 5 — Print Summary

```
  N bugs filed, M skipped (duplicates), P failed
```

---

## Repair Mode — `--repair-existing`

Invoke when previously-filed bugs are missing description, ReproSteps, or screenshot attachments. This happens when an earlier run skipped Step 5h of `qa-argus` (no screenshots captured) or when the filer ran an older script that only wrote to `System.Description` instead of `Microsoft.VSTS.TCM.ReproSteps`.

**Trigger:**
```
/qa-bug-filer --repair-existing [--run-id <runId>]
```

If `--run-id` is omitted, use the most recent `.tmp/qa-*/` directory that has a `bugs-filed.jsonl`.

### Repair flow

1. **List existing bugs.** Query ADO via WIQL for all bugs tagged `argus-qa` in this project:
   ```sql
   SELECT [System.Id], [System.Title], [System.Tags]
   FROM workitems
   WHERE [System.WorkItemType] = 'Bug'
     AND [System.Tags] CONTAINS 'argus-qa'
     AND [System.State] <> 'Closed'
   ```
   Endpoint: `POST /{org}/{project}/_apis/wit/wiql?api-version=7.1`

2. **Fetch each bug's current fields.** For each work item ID returned:
   ```
   GET /{org}/{project}/_apis/wit/workitems/{id}?fields=System.Title,Microsoft.VSTS.TCM.ReproSteps,System.Description&api-version=7.1
   ```
   Check whether `Microsoft.VSTS.TCM.ReproSteps` is empty or null. Same for `System.Description`. Also fetch `?$expand=relations` to see whether any `AttachedFile` relation exists.

3. **Match the bug to a finding.** Parse the bug title — it follows the format `[QA] <issueType> on <route> at <viewportClass> — <app>`. Extract `issueType`, `route`, and `viewportClass`. Find a matching line in any `issues/**/*.jsonl` of the latest run.

4. **PATCH missing body.** If ReproSteps OR Description is empty, PATCH the bug:
   ```js
   const body = [];
   if (!current.ReproSteps)  body.push({ op: 'add', path: '/fields/Microsoft.VSTS.TCM.ReproSteps', value: descriptionHtml });
   if (!current.Description) body.push({ op: 'add', path: '/fields/System.Description',            value: descriptionHtml });
   if (body.length) await adoPatch(bugId, body);
   ```

5. **Attach missing screenshot.** If no `AttachedFile` relation exists AND a `screenshotPath` or `annotatedScreenshotPath` is available on the matching finding → call the `attachScreenshot()` helper from Step 4 above.

6. **Log per-bug result.**
   ```
   #8739  body: filled  attach: filled    (repaired)
   #8740  body: ok      attach: skipped   (no screenshot available)
   #8741  body: ok      attach: ok        (already complete)
   ```

7. **Write `bugs-repaired.jsonl`** alongside `bugs-filed.jsonl` with one line per bug processed: `{ id, bodyRepaired: bool, attachmentAdded: bool, reason: string }`.

### When to use repair mode

| Symptom | Run this |
|---------|----------|
| Existing ADO tickets are open but show empty Repro Steps | `/qa-bug-filer --repair-existing` |
| Existing tickets have no screenshot attached | `/qa-bug-filer --repair-existing` (will pick up screenshots if the latest run captured them) |
| You ran the audit again, no new bugs filed, but old ones are still empty | Same — repair mode reads the latest `issues/*.jsonl` and back-fills |

Repair mode is **idempotent** — running it twice on already-complete bugs is a no-op, it just logs `already complete`.

---

## Dry-Run Mode

If `dry_run = true` in `{project-root}/.claude/skills/qa-argus/customize.toml`:

- Print each bug that **would** be filed with its title, severity, route, and viewport.
- Do **not** call any ADO REST endpoint.
- Do **not** write to `bugs-filed.jsonl`.
- Exit with code 0.

---

## Bug Title Format

```
[QA] <issueType> on <route> at <viewportClass> — <app>
```

Example:
```
[QA] overflow-x on /dashboard at mobile — MyApp
```

---

## Bug Description

Use `{skill-root}/templates/repro-steps.html` as the template. Substitute all `{{PLACEHOLDER}}` tokens with values from the issue object before sending to ADO.

---

## ADO Fields

| ADO Field | Value | Notes |
|---|---|---|
| `System.Title` | Bug title (see format above) | required |
| `Microsoft.VSTS.TCM.ReproSteps` | HTML from `repro-steps.html` template | **PRIMARY body field on Bug work items — set this OR the ticket will appear empty in ADO's Bug view** |
| `System.Description` | Same HTML as ReproSteps | secondary; some ADO views show this instead — populate both to be safe |
| `System.AreaPath` | `area_path` from `customize.toml`; if empty, use the project root | optional |
| `System.Tags` | `argus-qa,<skill>,<viewport>,<browser>` | for search/filter |
| `Microsoft.VSTS.Common.Severity` | Mapped from issue severity (see below) | required |
| `System.WorkItemType` | `Bug` | set via the URL path `/$Bug`, not as a field |

**Why both `Microsoft.VSTS.TCM.ReproSteps` AND `System.Description`?**
ADO's default Bug template displays content from `Microsoft.VSTS.TCM.ReproSteps`, not `System.Description`. If you only set `System.Description`, the Bug ticket looks empty when opened. Setting both fields with the same HTML ensures the body is visible regardless of which template / process the ADO project uses.

#### Required PATCH body (the runtime `.cjs` MUST emit this — both body fields, every time):

```js
const patchBody = [
  { op: 'add', path: '/fields/System.Title',                        value: title },
  { op: 'add', path: '/fields/Microsoft.VSTS.TCM.ReproSteps',       value: descriptionHtml },  // primary body
  { op: 'add', path: '/fields/System.Description',                  value: descriptionHtml },  // fallback body
  { op: 'add', path: '/fields/System.AreaPath',                     value: AREA_PATH },
  { op: 'add', path: '/fields/System.Tags',                         value: tags },
  { op: 'add', path: '/fields/Microsoft.VSTS.Common.Severity',      value: adoSeverity }
];
```

---

## Severity Mapping

| Issue severity | ADO Severity field value |
|---|---|
| `high` | `1 - Critical` |
| `medium` | `2 - High` |
| `low` | `3 - Medium` |
| *(unknown)* | `2 - High` |

---

## Paths Reference

| Resource | Path |
|---|---|
| Issues input | `{project-root}/.tmp/qa-<run-id>/issues/**/*.jsonl` |
| Filed bugs log | `{project-root}/.tmp/qa-<run-id>/bugs-filed.jsonl` |
| Filing script | `{skill-root}/scripts/file-bugs.sh` |
| Description template | `{skill-root}/templates/repro-steps.html` |
| Config | `{project-root}/.claude/automation.config.json` |
| PAT source | `.claude/secrets.json → AZURE_DEVOPS_PAT` (preferred), or env var `AZURE_DEVOPS_PAT` |

---

## customize.toml Options

| Key | Type | Default | Description |
|---|---|---|---|
| `dedup_key` | string | `issueType+url+viewport` | Fields used to deduplicate issues |
| `area_path` | string | `""` | ADO area path; empty = project root |
| `max_bugs` | integer | `0` (unlimited) | Max bugs filed per run. **Default `0` = file EVERY detected issue, never skip one.** Set a positive integer to re-enable a spam cap. Also overridable via env `QA_MAX_BUGS`. When a cap drops issues, the filer logs `⚠ CAP ACTIVE … will NOT be filed`. |
| `attach_screenshots` | bool | `true` | Whether to attach screenshots to filed bugs |


