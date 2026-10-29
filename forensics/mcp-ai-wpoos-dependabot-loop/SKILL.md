---
type: Skill
name: mcp-ai-wpoos-dependabot-loop
description: "Operational guide for the NV oOS Dependabot alert triage-and-remediation loop: querying open alerts via gh api, separating stale from genuinely vulnerable lockfile entries (default-branch forensics), deciding between safe in-major override bumps, scoped overrides, or deferred major migrations (npm pack signature diffing), regenerating the 13-lockfile tree, rebuilding the tracked JS bundles that lockfile movement stales, dismissing alerts with the right reason, GitHub issue housekeeping, and triaging the known CI failure modes. Use when asked to fix dependabot alerts, close out dependabot issues, bump vulnerable npm packages, or resume a dependabot session."
license: Proprietary. See LICENSE.txt
metadata:
  plugin: mcp-ai-wpoos
  plugin-version: "1.2.10"
  plugin-version-tested: "1.2.10"
  last-updated: "2026-10-23"
---

# NV oOS Dependabot Loop — Alert Triage, Safe Bumps & Dismissal

Playbook for the recurring Dependabot sweep in this repo, distilled from the
executed 2026-09-30 run (PR #6817: js-yaml + webpack-dev-middleware bumps;
alerts 803/804, 898, 901, 922–976 triaged; issues #6647/#6818). It covers the
full loop: discovery → forensics → fix decision → lockfile regen → bundle
rebuild → dismissal → issue housekeeping → CI triage. The workflow implements Dependabot's own
dismissal semantics (`fix_started` vs `tolerable_risk`) adapted to this repo's
alpha-working → main merge flow.

## When to use this skill

- The user asks to "fix the dependabot alerts", "close out dependabot issues",
  "bump vulnerable npm packages", or resumes a previous dependabot sweep.
- You see a PR/CI run titled like `Bump <pkg> to patched versions`.
- A `security/dependabot` dashboard link is pasted with an alert list or CI log.

## Step 0 — Orientation (before touching anything)

1. **Check existing work first** (multi-agent rule from `AGENTS.md`): `git branch -a`
   for `dependabot/*` branches and `gh issue list --search dependabot` for
   tracking issues. The 2026-09-11 sweep used `dependabot/npm-safe-bumps` and
   `dependabot/safe-bumps-batch`; do not duplicate scopes they already fixed
   (sharp, nodemailer, joi, postcss-selector-parser).
2. **Alerts are computed against the DEFAULT branch (`main`), not
   `alpha-working`.** Fixes committed to `alpha-working` (the active v1.1.x
   line) do not clear an alert until they merge to `main`. Never dismiss an
   alert as "fixed" without verifying `main`'s lockfiles (Step 2).
3. Branch from `origin/alpha-working` (not `main`) for all new work; PR base is
   `alpha-working` (Step 5).

## Step 1 — Alert discovery

Aggregate the open alerts by package + manifest (dedupes the ~10 undici GHSA
variants that each hit 4 manifests):

```sh
gh api repos/nvdigitalsolutions/mcp-ai-wpoos/dependabot/alerts --paginate --jq '
  [.[] | select(.state == "open")]
  | group_by(.security_vulnerability.package.name + "|" + .dependency.manifest_path)
  | map({package: .[0].security_vulnerability.package.name,
         ecosystem: .[0].security_vulnerability.package.ecosystem,
         manifest: .[0].dependency.manifest_path,
         patched: .[0].security_vulnerability.first_patched_version.identifier,
         count: length, alerts: map(.number)})
  | sort_by(.manifest + .package)'
```

For one alert's advisory details: `gh api .../dependabot/alerts/{n}` and read
`security_vulnerability.vulnerable_version_range`,
`security_vulnerability.first_patched_version.identifier`, and
`security_advisory.description` (the description names the affected code path —
e.g. GHSA-866g-f22w-33x8 names `createJsonResponseHandler`).

**Multi-line advisory gotcha (the 2026-10-03 undici family):** the alert's
top-level `security_vulnerability` exposes only ONE vulnerable range, but recent
advisories declare several — one per supported major line, each with its own
patch. Read the full `security_advisory.vulnerabilities[]` array, not just the
top-level field. The undici family published 2026-09-29 patches three lines at
once: `6.x → 6.28.1`, `7.x → 7.29.1`, `8.x → 8.10.2`. The Step 1 aggregate
dedupes by the single-range `first_patched_version`, so a manifest whose top
copy is patched can still hide a vulnerable copy on another major line — always
check every copy against every range (a three-line range checker is in the
2026-10-03 triage below).

## Step 2 — Staleness forensics (which alerts are real?)

Dependabot's state machine only auto-transitions alerts to `fixed` when the
default branch is clean, and re-scans lag pushes. So verify versions yourself.

**A. Scan the local lockfiles** (21 npm trees as of 2026-10-03 — root + 20
addons, each with its own `package-lock.json`; the set grows, so `find_path` for
`**/package-lock.json` first):

```sh
node -e "const fs=require('fs'); const files=['package-lock.json','addons/pro/package-lock.json','addons/pro/assets/spa/package-lock.json','addons/pro/assets/spa-v2/package-lock.json','addons/chat-spa/package-lock.json','addons/cloud-worker/package-lock.json','addons/cloudways-dashboard/package-lock.json','addons/saas-controller/package-lock.json','addons/toolkit-shell/package-lock.json','addons/docs-hub/package-lock.json','addons/media-studio/package-lock.json','addons/media-worker/package-lock.json','addons/canvas-toolkit/package-lock.json','addons/comic-reader/package-lock.json','addons/document-editor/package-lock.json','addons/funiq-bridge/package-lock.json','addons/librechat/package-lock.json','addons/page-agent/package-lock.json','addons/schedule-anything-spa/package-lock.json','addons/tenant-router/package-lock.json','addons/mcp-wordpress-gateway/package-lock.json']; const names=['js-yaml','undici','webpack-dev-middleware','body-parser','qs','@ai-sdk/provider-utils']; for(const f of files){ if(!fs.existsSync(f)) continue; const l=JSON.parse(fs.readFileSync(f,'utf8')); const pk=l.packages||{}; for(const p in pk){ const n=p.split('node_modules/').pop(); if(names.includes(n)) console.log(f,'|',p,'|',pk[p].version); } }"
```

Multi-line range checker (flags any copy inside any undici advisory range; adapt
the thresholds per package):

```sh
node -e "const fs=require('fs'); const files=['addons/media-worker/package-lock.json']; const vuln=(v)=>{ if(/^6\./.test(v)) return v<'6.28.1'; if(/^7\./.test(v)) return v<'7.29.1'; if(/^8\./.test(v)) return v<'8.10.2'; return false; }; for(const f of files){ const pk=JSON.parse(fs.readFileSync(f,'utf8')).packages||{}; for(const p in pk){ if(p.endsWith('node_modules/undici') && vuln(pk[p].version)) console.log('VULNERABLE', f, p, pk[p].version); } }"
```

Print the **full path** (not just the name) — multiple copies of the same
package can coexist (e.g. `node_modules/webpack-dev-middleware@6.1.3` for
react-cosmos next to `node_modules/webpack-dev-server/node_modules/webpack-dev-middleware@8.0.3`),
and only some copies may sit in the vulnerable range.

**B. Verify the DEFAULT branch state** for any alert you plan to dismiss as
stale. The contents API truncates files >1 MB (silently! — JSON.parse then
fails with "Unexpected end of JSON input"), so fetch with the raw media type:

```sh
gh api "repos/nvdigitalsolutions/mcp-ai-wpoos/contents/addons/pro/package-lock.json?ref=main" -H "Accept: application/vnd.github.raw" > /tmp/check.json
```

**C. Classify** each alert group:
- **Stale** — patched version already present in the relevant lockfile(s)
  (default branch or the branch carrying the fix). No code change; these
  auto-dismiss after the fix reaches `main` (or dismiss manually, Step 8).
- **Genuinely vulnerable** — a copy inside `vulnerable_version_range` exists.
  Proceed to Step 3–4.
- **Stale-graph false positive** — the alert fired against an outdated
  dependency-graph snapshot even though the CURRENT default-branch lockfile is
  already patched. Seen 2026-10-03: 7 media-worker undici alerts fired
  2026-10-02 against `main`'s already-clean lockfile (7.29.1/6.28.1 patched by
  PR #6806, in `main` since the v1.1.92 squash merge of 2026-10-01 — before the
  alerts were created). Verify `main` directly (Step 2B) before assuming an
  alert is real; if the manifest is clean on `main`, dismiss as `inaccurate`
  with the evidence in the comment. Don't expect a re-scan to clear these until
  the next push to `main`.

2026-09-30 example: `undici` (31 alerts), gateway `body-parser`/`qs` were
stale on `alpha-working` but still vulnerable on `main` (`undici@8.10.0`,
`body-parser@1.20.3`, `qs@6.13.0`) — the fixes were already committed to
alpha-working v1.1.89 and only needed the merge. `js-yaml@5.2.x` and
`webpack-dev-middleware@8.0.3` were genuinely vulnerable everywhere.

## Step 3 — Registry checks before any bump

- Confirm the patched version exists: `npm view <pkg> versions --json`.
- Find who depends on it and which ranges they declare:

```sh
node -e "const l=JSON.parse(require('fs').readFileSync('package-lock.json','utf8')); const pk=l.packages||{}; for(const p in pk){ const d=pk[p].dependencies; if(d && d['<pkg>']) console.log(p,'->',d['<pkg>']); }"
```

This tells you whether the override is moving an in-major patch (safe) or
crossing a major for some consumer (e.g. `@langchain/classic` genuinely
requires `js-yaml@^5.2.2`; eslint declares `^4.1.0` but had already been forced
onto 5.x by the prior override).

## Step 4 — Fix decision tree

### A. In-major override bump (the common case)

When the vulnerable copy is already on a major line and the patched version is
a patch bump, raise the existing `overrides` value in each affected
`package.json` (e.g. `"js-yaml": ">=4.3.0"` → `">=5.4.1"`) and regenerate the
lockfiles (Step 6). No dependency ranges change; only the override.

Floor-raise variant (the 2026-10-01 fast-uri run, PR #6834): when the advisory's
vulnerable range is a *minor* inside the override's major (`>= 4.1.3, < 4.1.5`
vs the `>=4.1.4` floor), just raise the floor (`>=4.1.4` → `>=4.1.5`, resolving
4.2.1) — same lockfile-only diff, but run the npm-pack `index.d.ts` diff anyway
(it showed an additive optional `ipv6Zone` field only) and cite it in the PR.

Bounded-floor variant (the 2026-10-03 markdown-it run, PR #6868): when the
advisory's patched line is a minor bump but the **next major exists and is
undesired**, bound the override — `">=14.2.0"` → `">=14.3.1 <15"` across the
three trees (root, `addons/pro/assets/spa`, `addons/saas-controller`) so npm
stays on 14.x (an unbounded floor resolved to 15.0.2). Same discipline:
npm-pack diff the minor (14.3.0 → 14.3.1: internal rule/helper files + dist
bundles only, no `lib/index.mjs` delta), note the consumer is dev-only tooling
(`@wordpress/scripts` → `markdownlint-cli` → `markdown-it`, linkify off —
availability-only advisory, medium severity), and remember sibling-alert notes
(the 9 jsdom-nested undici alerts clear only when `alpha-working` merges to
`main`; media-worker undici alerts are stale-graph false positives).

### B. Scoped override (`@version` syntax) — do not force unrelated majors

A blanket override (`"webpack-dev-middleware": ">=8.3.0"`) applies to ALL
copies — it ripped react-cosmos-plugin-webpack's `webpack-dev-middleware@6.1.3`
up to 8.x. Scope it instead, matching the repo's existing `minimatch@^3` style:

```json
"webpack-dev-middleware@^8": ">=8.3.0"
```

Only use a plain key when the tree has a single copy (e.g.
`addons/pro/assets/spa`).

### C. Major / API-breaking bumps — prove it, then defer to an issue

When the patched version is a different major (or the fixed range excludes the
whole installed line), **verify API compatibility before overriding**:

1. `npm pack <pkg>@<old>` and `npm pack <pkg>@<new>` in a scratch dir; untar.
2. Grep the **consumers'** dist for what they call on the package
   (`grep -o "import_<pkg>[0-9]*\.[A-Za-z0-9_]*" .../dist/index.js | sort -u`),
   then diff those symbols' signatures between the two `index.d.ts`.
3. **Watch for sync → async changes specifically** — a function returning a
   value vs a Promise is the classic silent breaker.

Case study (the `@ai-sdk/provider-utils` alerts, left open): ui-utils 1.2.11
calls `safeParseJSON({text})` synchronously in the useChat stream parser and
react 1.2.12 calls `safeValidateTypes()` synchronously; both became
Promise-returning in provider-utils 3.x, so an override silently breaks chat
streaming. The entire 2.x line is vulnerable (no backport), so the only fix is
the `@ai-sdk/react` 1.x → 2.x migration — file a tracking issue instead
(Step 9). Never ship an override you have not verified against the consumer's
call sites.

Case study — a verified-safe cross-major bump that SHIPPED (the 2026-10-01
nodemailer run, PR #6833): the advisory's patched range (`>= 10.0.9`) excluded
the whole installed 9.x line, so this was a major migration in `addons/pro` +
`addons/media-worker`. It shipped because the proof was strong:

1. npm-pack diff showed the mailparser deep-import
   (`nodemailer/lib/addressparser`) still resolves through nodemailer 10's
exports map as a callable CJS export.
2. A/B-testing 9.1.1 vs 10.0.9 on quoted local-part / group / encoded-name /
   plain inputs was **byte-identical** (and 10.x preserves the quoted local
   part, which is the advisory's required behavior).
3. nodemailer 10 has zero runtime deps and requires Node ≥ 20 — the
   media-worker sidecar already runs `node:22-alpine`; CI passes
   `--ignore-engines` on the 18/20 matrix (EBADENGINE warnings only).

**Vendor-bundle gotcha specific to this repo:** nodemailer 10 ships **no
top-level `lib/`** — the `copy-dependencies.js` vendor copy spec had to switch
from copying `lib/` to copying `dist/`, and `assets/vendor/nodemailer` was
refreshed 8.0.5 → 10.0.9 with the old `lib/` removed so vulnerable code is
never distributed. When a major bump touches a package this repo vendors
(`copy-dependencies.js` + `assets/vendor/`), updating the copy spec + bundle is
part of the fix — a lockfile-only bump leaves the vulnerable vendored code in
the tree.

### D. Stale alerts — no code change

Document them in the PR/commit body and let Dependabot re-scan (or dismiss
with `fix_started` referencing the branch that already carries the fix).

## Step 5 — Branch, commit, PR conventions

- Branch: `dependabot/<packages>-safe-bumps` from `origin/alpha-working`;
  PR base `alpha-working`.
- Commit subject ≤ 50 chars, imperative, e.g.
  `Bump js-yaml and webpack-dev-middleware to patched versions`. Body lists the
  alert numbers + GHSA IDs resolved, and calls out what was left open and why.
- Create the PR with `gh pr create --base alpha-working --head <branch>` (the
  `create_pull_request` MCP tool may lack credentials — fall back to `gh`).
- **Do not merge unless told to.** Create the PR and stop; merge only when
  the user explicitly asks for the merge. Never self-merge off inferred
  intent.

## Step 6 — Lockfile regen & validation

For every `package.json` you changed (root + addons):

```sh
npm install --package-lock-only --ignore-scripts --no-audit --no-fund
```

- `addons/pro` **must** use `--legacy-peer-deps` (its lockfile is generated
  that way by the root `postinstall`).
- `--package-lock-only` avoids touching `node_modules`; `--ignore-scripts`
  avoids the root `postinstall` recursion.
- Expect benign churn: npm re-resolves transitive ranges against the current
  registry and syncs the lockfile's stale root `version` field. Accept it; the
  repo's own history has "regenerate lock file with full dependency tree"
  commits.
- Validate each tree: `npm ci --dry-run --ignore-scripts --no-audit --no-fund`
  must pass in all 13 directories before pushing.
- Verify the final state with the Step 2A scanner — every previously
  vulnerable copy must be at/above `first_patched_version`.

## Step 7 — Rebuild tracked JS bundles (lockfile movement stales them)

A lockfile-only bump leaves the repo's tracked build artifacts stale: the
bundles in git still embed the pre-bump dependency graph, so packaged ZIPs
ship old code. Proof case 2026-10-22 (PR #7182): #7175 + #7106 moved
`package-lock.json` after the 2026-10-09 rebuild (#6979);
`addons/pro/bin/generate-{word,pdf,excel}.bundle.js` were 13 days stale —
a fresh `npm run build:js:pro` diffed hundreds of dependency-internal
lines with zero source changes.

- **Detect:** `git status` shows modified bundles whose sources are clean,
  and `git log --oneline origin/alpha-working -- package-lock.json` is
  newer than `git log --oneline -1 -- <bundle>`. Marker-grep to prove it:
  `grep -c EXPANSION_MAX_DEPTH addons/pro/bin/generate-excel.bundle.js`
  (2 committed → 0 freshly built after the brace-expansion override moved).
- **Rebuild:** run the Full JS rebuild map in the `mcp-ai-wpoos-spa-ui`
  skill (it also carries the rebuild discipline: vendor never-commit gate,
  node_modules drift, standalone-addon `npm ci`, bad-merge recovery).
  Standalone addons with their own committed lockfiles (e.g. `chat-spa` →
  `@ai-sdk/react@1.2.12`) need `npm ci` inside the addon dir first —
  "Could not resolve <pkg>" means the addon's `node_modules` is missing,
  not the root's (no npm workspaces here).
- **Commit discipline:** stage only the rebuilt artifacts. Never commit
  `vendor/composer/*` regen (`vendor/` is tracked in production state;
  local composer output is dev-only dirt) and never foreign WIP in a
  shared worktree. Pre-commit gate:
  `git diff --cached --name-only | grep -E '^vendor/'` must be empty.

## Step 8 — Alert dismissal (close-out)

When asked to close out the dashboard, dismiss with honest reasons via
`gh api` (50 PATCH calls in a sh `for` loop is fine; rate limit is 5000/hr):

```sh
gh api -X PATCH "repos/nvdigitalsolutions/mcp-ai-wpoos/dependabot/alerts/$n" \
  -f state=dismissed \
  -f dismissed_reason=fix_started \
  -f dismissed_comment="Fix in PR #6817; applies once alpha-working merges to main." \
  --jq '"dismissed \(.number)"'
```

Reason mapping:

| Reason | Use when |
| --- | --- |
| `fix_started` | Fix exists in a PR or on `alpha-working`, awaiting merge to `main` |
| `tolerable_risk` | Accurate but accepted; a tracking issue documents the plan (e.g. the AI SDK migration → #6647) |
| `inaccurate` / `not_used` / `no_bandwidth` | Alert wrong / package unused / no capacity — rare in this repo |

Always put the PR number or issue number in `dismissed_comment`. Then verify:

```sh
gh api repos/nvdigitalsolutions/mcp-ai-wpoos/dependabot/alerts --paginate \
  --jq '[.[] | select(.state == "open")] | length' | \
  node -e "let t=0;process.stdin.on('data',c=>t+=parseInt(c)||0).on('end',()=>console.log('open:',t))"
```

**Caveat to state in the report:** dismissal is permanent, but `main` stays
vulnerable until alpha-working merges — call that out and recommend the merge.

## Step 9 — GitHub issue housekeeping

- **Search before filing**: `gh issue list --search dependabot` — the AI SDK
  migration already had issue #6647 before the sweep filed #6818; close the
  duplicate (`gh issue close <n> --reason duplicate`) and copy the analysis
  into the canonical issue as a comment.
- One canonical tracker per deferred major migration; the dismissal comment
  references it.
- Unrelated issues that merely *mention* a dependabot PR (e.g. #6366) are out
  of scope — leave them.

## Step 10 — CI triage (known failure modes)

- **`npm error EEXIST ... /home/runner/.npm/_cacache/tmp/<hex>`** — transient
  npm cache race on GitHub runners (npm/cli#7447), not a lockfile problem.
  Re-run the job: `gh run list --branch <b> --workflow "JavaScript Tests"` then
  `gh run watch <databaseId> --exit-status`. Note: the display number (e.g.
  #17610) is NOT the API id — `gh run watch 17610` 404s; use `databaseId`.
- **`npm warn EBADENGINE`** (webpack-dev-server@6, http-proxy-middleware@4,
  p-retry@8 want node ≥ 22 while the matrix runs 18/20) — warnings only, the
  job passes `--ignore-engines`. Pre-existing; a Node 22/24 matrix bump is a
  separate change.

## Gotchas (this repo, Windows git-bash)

- Default shell is `sh`: no `dir`, no `bc` (use `ls`, node arithmetic).
- `/tmp` written by sh resolves to git-bash's `/tmp`, but node.exe sees
  `F:\tmp` — use repo-relative paths for handoffs between the two. Best of all:
  pipe `gh api` raw output straight into `node -e` on stdin and skip temp files.
- Older `gh` versions have no `-o/--output` flag on `gh api` — redirecting with
  `-o /tmp/x.json` fails with "unknown shorthand flag"; use `| node` instead.
- GitHub contents API: >1 MB files need
  `-H "Accept: application/vnd.github.raw"` (see Step 2B).
- The root `package-lock.json` carries a stale `version` until regen — the
  diff will always include that sync line; do not hand-edit it out.
- `npm ci --dry-run` does not touch node_modules; it only proves
  `package.json`/lockfile consistency — the real install happens in CI.

## References

- PR #6931 — executed 2026-10-06 sweep: 14 packages bumped via **bounded
  in-major overrides** across 17 manifest trees (axios ≥1.20.0 <2, brace-expansion@^1
  ≥1.1.21 <2, source-map-js ≥1.2.2 <2, dompurify, proxy-addr ≥2.0.8 <3,
  compression ≥1.8.2 <2, joi, katex ^0.18.2, moment ≥2.31.0 <3, simple-git
  ≥4.0.1 <5 + @simple-git/argv-parser ≥2.0.1 <3, basic-ftp ≥6.2.1 <7,
  postcss-selector-parser@^7 ≥7.1.6 <8, webpack-dev-middleware ≥7.4.6 <8) —
  **138 of 166 open alerts**; every cross-version move npm-pack-diffed.
  **28 deferred in issue #6930** — postcss-selector-parser 6.x copies
  (6→7 flips whitespace defaults), sentry-pinned @opentelemetry/instrumentation-*
  (cross-minor 0.x), react-cosmos webpack-dev-middleware 6.1.3 (6→7 major),
  and 11 no-patch advisories (sprintf-js, braces, http-cache-semantics).
  Same-day dashboard close-out: 138 dismissed `fix_started` + 28
  `tolerable_risk` → 0 open alerts (main clears once alpha-working merges).
- PR #6817 — executed 2026-09-30 sweep (js-yaml + webpack-dev-middleware).
- PR #6850 — merged 2026-10-02: jsdom's undici 7.29.0 → 7.30.0 in 8 addons
  (fixes the 2026-09-29 undici advisory family on `alpha-working`; clears
  `main`'s alerts once alpha-working merges).
- PR #6806 — merged 2026-09-29: patched media-worker's undici to 7.29.1
  (the fix behind the stale-graph false positives dismissed 2026-10-03).
- 2026-10-03 triage sweep — 39 open alerts, all undici, all already patched on
  `alpha-working`: 32 dismissed `fix_started` (PR #6850 awaiting main merge)
  and 7 media-worker alerts dismissed `inaccurate` (stale graph). No lockfile
  changes required.
- Issue #6647 — AI SDK v1→v5 migration tracker (canonical for provider-utils).
- Advisories seen in this repo: GHSA-r3ph-w7gj-g6xm (js-yaml),
  GHSA-g84c-rxfj-3j2c (webpack-dev-middleware),
  GHSA-866g-f22w-33x8 (@ai-sdk/provider-utils), plus the undici/body-parser/qs
  families (GHSA-rfgv-xxqx-mfg5 and siblings). The 2026-09-29 undici family:
  GHSA-3xpg-4rpp-hhhm, GHSA-pmjh-fq2x-6v4x, GHSA-2gqq-gqf2-x968,
  GHSA-rx4f-c7p8-82vq, GHSA-rfgv-xxqx-mfg5, GHSA-r53p-7pc4-xj5r,
  GHSA-2jfj-6hjv-fm6j (plus GHSA-w293-vg96-wgc3 fixed earlier) — three patched
  lines: 6.28.1 / 7.29.1 / 8.10.2.
- npm/cli#7447 — the EEXIST cacache race behind the flaky CI job.
- `mcp-ai-wpoos-updates` skill §A5 — new-skill bookkeeping rules (counts in
  `AGENTS.md` §1, `.github/copilot-instructions.md`, `README.md`).
