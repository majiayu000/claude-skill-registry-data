---
name: prove-it
description: Verify that work actually shipped and actually works in production before telling the user it does. Checks uncommitted/unpushed code, every CI job, whether the live deployment is the current commit, whether real pages serve real content, whether API endpoints behave, whether logging and persistence are genuinely wired, and whether analytics events actually arrive. Use this skill before any claim that something is "done", "shipped", "deployed", "live", "fixed" or "working"; when the user asks "is it live?", "did that deploy?", "is it actually working?", "are you sure?"; after pushing anything; and whenever a previous claim of success turned out to be false. Trigger it even when you are confident — confidence is exactly when this gets skipped and exactly when it burns the user.
---

# Prove It

A checklist for turning "I think it works" into "here is the evidence it works."

Every rule below exists because it was violated in a real session and cost the user real money.

## The one rule

**A claim without a command output behind it is a guess.** If you are about to type
"deployed", "live", "working", "fixed", or "done", you must have run something in
this turn whose output proves it. Not last turn. Not from memory. This turn.

## When to use

- Before saying anything shipped, deployed, or works
- Right after `git push`
- When the user asks "is it live?" / "is it working?" / "are you sure?"
- When a previous success claim turned out to be wrong — run the whole thing again
- Before a status report of any kind

## Run the script first

`scripts/verify.sh` (in this skill's folder) runs every layer a script can run, the
same way every time, on any site and any host. Run it before you write a word of status.

```bash
# project has a .prove-it file (see below): no arguments needed
bash <this-skill>/scripts/verify.sh

# ad hoc, any URL
bash <this-skill>/scripts/verify.sh https://example.com/pricing/ \
  --expect "text only the new build has" --reject "text that should be gone" \
  --version-url https://example.com/version.json --wait 600 \
  --endpoint https://example.com/api/lead --endpoint-status 400
```

| Exit | Meaning | What you may say |
|------|---------|------------------|
| 0 | every declared layer passed | "it works" — listing what was checked |
| 1 | something FAILED | lead with the failure |
| 2 | nothing failed, something is UNVERIFIED | "X is verified, Y is not" — never "it works" |
| 64 | unknown flag or bad config line | nothing was checked; fix the command |

- Every layer ends as PASS, FAIL, UNVERIFIED or N/A. A layer is only N/A when someone
  **declares** it (`--na ci`, or `na ci <reason>` in `.prove-it`). "This site has no CI"
  is a decision a person makes, never something the script assumes.
- Matching is literal, against the raw source. Give the string the way it appears in
  the HTML (`&amp;`, not `&`). Status code and body always come from the same request.
- `--wait 600` keeps polling until the live commit is HEAD and CI has finished. Use it
  right after a push instead of guessing when the deploy is done.
- Layers 6 and 7 live in systems no generic script can see. Do them by hand, or give
  the project its own check (below) so they run every time too.

### `.prove-it` — one file per project, so nobody has to remember the strings

Commit it at the repo root. One directive per line; comments go on their own line.

```
version https://example.com/version.json
wait    600

page https://example.com/
  expect Book a call
  reject Lorem ipsum
page https://example.com/pricing/
  expect $49/mo

# an empty payload should be rejected: proves the route and its validation are live
# without creating a junk record
endpoint https://example.com/api/lead
  status 400
  expect "error"

na    analytics  brochure site, no events
check storage    node scripts/read-back-test-record.js
```

`check <name> <command>` runs from the config's folder. Exit 0 means proven, and the
last five lines of output are printed as the evidence. Name it `storage` or `analytics`
to satisfy layer 6 or 7; any other name is an extra project check. A check must be
read-only or clean up after itself — and verify the cleanup.

## The seven layers

Check them in order. A failure at any layer invalidates every claim above it.

### 1. Code state

```bash
git status --porcelain                      # empty = clean
git fetch -q origin
git rev-parse HEAD && git rev-parse origin/main   # must match
```

**Trap:** a clean tree does not mean pushed. Compare the hashes. Work sitting
unpushed for days looks identical to work that shipped.

### 2. CI — every job, not the summary

```bash
gh run list --commit "$(git rev-parse HEAD)"   # runs for THIS commit, every workflow
gh run view <id>                               # per-job breakdown
gh run view <id> --log-failed
```

**Trap:** "the build passed" usually means one job passed. A run with a green
`verify` and a red `audit` reports as failure overall, and a red-forever CI gets
ignored by everyone — which silently disables whatever regression guard it held.
Check when CI last passed, not just whether it exists.

**Trap:** the newest run in the list is not necessarily *your* run. Right after a push
it is still the previous commit's, and a green one reads as "passed". Always filter by
commit SHA. Not on GitHub? Same rule on any CI: find the pipeline for this exact
commit, then open every job.

### 3. Deployment — match the commit, never the word "Active"

Get the live deployment's **commit hash** and compare it to HEAD.

**Trap:** deployment lists show queued and building rows too. "Active" on the
first row can be the *previous* deployment while the new one builds. Testing
during that window tests the old code and produces a confident wrong answer.

When a platform has no reliable status field, poll the deployed artifact itself
for something only the new build contains — a new response field, new copy, a new
asset. That is the only trustworthy signal.

**Make that signal permanent, on any host:** have the build write its commit into a
file that ships with the site. Copy `scripts/stamp-version.sh` from this skill into the
project and call it from the build command, pointed at the folder that gets published:

```bash
bash scripts/stamp-version.sh public      # writes public/version.json {"commit":"<sha>"}
```

It reads whichever variable the platform provides, then falls back to `git rev-parse HEAD`:

| Host | Commit variable |
|------|-----------------|
| Cloudflare Pages / Workers Builds | `CF_PAGES_COMMIT_SHA` / `WORKERS_CI_COMMIT_SHA` |
| Vercel | `VERCEL_GIT_COMMIT_SHA` |
| Netlify | `COMMIT_REF` |
| Render / Railway | `RENDER_GIT_COMMIT` / `RAILWAY_GIT_COMMIT_SHA` |
| AWS Amplify | `AWS_COMMIT_ID` |
| GitHub Actions / GitLab CI | `GITHUB_SHA` / `CI_COMMIT_SHA` |
| No build step (WordPress, rsync, FTP) | deploy script runs `git rev-parse HEAD > version.txt` |

Then `verify.sh --version-url <site>/version.json --wait 600` polls until the live
commit is HEAD, and fails if it never gets there. Page checks only mean something
after that passes. The SHA may appear anywhere in that URL's body or headers.

**Trap:** read the host's *real* build command before wiring the stamp. A host that
builds with `npx next build` (or any direct tool call) never fires npm `prebuild` /
`postbuild` hooks, so a stamp placed there works locally and in CI and silently never
ships. Either put it in the host's build command, or call it from something the build
tool itself always loads (e.g. the framework config, on the production-build phase).
Then prove it: build with the host's exact command and check the file is in the output.

### 4. Pages — assert on content, never on 200

```bash
curl -s -L -H "Cache-Control: no-cache" "$URL?cb=$RANDOM" | grep -c "<distinctive string>"
```

For every public route, assert:
- a string that only appears when the page rendered correctly
- the *absence* of a string that means the wrong thing rendered
- canonical/og/sitemap URLs point at a domain that actually resolves (`host <domain>`)
- referenced assets return 200, not just that the tag exists

**Traps:**
- 200 proves a server answered, not that the right page came back
- A CDN can serve the old build for minutes. Cache-bust every check.
- On static sites with client-side variants, the HTML is the *build-time* variant.
  Verify the served HTML matches what real traffic lands on, not what you assume.
- In a script, never pipe a page into `grep -q` with `pipefail` on
  (`echo "$BODY" | grep -q X`). On pages past ~64KB grep exits at the first match, the
  writer dies of SIGPIPE, and the check reports the opposite of the truth: "missing"
  for text that is there, "gone" for text that is not. Save the body to a file and use
  `grep -qF -- "$X" file` — which also stops `.`, `?` and `(` being read as regex.

### 5. Endpoints — prove the destination, not the handshake

Call the endpoint and assert on the response body.

**Trap — the one that destroys leads:** a vendor returning 200 does not mean the
record exists. Webhooks, queues and Measurement Protocol endpoints all accept and
discard. Always verify at the **destination system** that the row/contact/event
actually landed. If the endpoint claims success, go look for the thing it claims
to have created.

Prefer a request that proves the path without creating junk — an invalid payload
that exercises validation and logging, or an upsert of an existing test record.
Clean up anything you do create, and verify the cleanup.

### 6. Logging and persistence — write, then read back

Do not trust that a store is wired because the code references it.

1. Trigger a real write
2. Read it back out of the store
3. Show the retrieved record

**Traps:**
- A binding declared in code does nothing until it is attached to the deployment,
  and bindings usually apply only to *new* deployments.
- Many CLIs default to a **local emulator**, reporting an empty remote store.
  `wrangler kv key list` needs `--remote`; Stripe's CLI reads test mode unless told
  `--live`. Check the equivalent flag for any tool before concluding "nothing is there."
- List operations are often eventually consistent. Confirm a delete with a direct
  read, not a list.
- Ephemeral logs are not logs. If the platform does not retain them, say so and
  build durable storage instead of pointing at a live tail.

### 7. Analytics and events

Query the destination for the event, in a window that covers the action. (The examples
below are GA4's; every analytics tool has the same four traps under other names.)

**Traps:**
- Standard reports lag 24–48h. Use realtime to confirm something just fired.
- Custom parameters are invisible in reports until registered as custom dimensions.
- A single wrong character in a measurement/property ID makes every event vanish
  with a success response. Diff the configured ID against the real one character
  by character.
- Path dimensions frequently strip query strings, collapsing distinct pages into
  one row. Use the query-string variant before concluding anything about traffic.

## Searching for things you claim are absent

Before saying "there are no references" / "nothing matches" / "it's all gone":

```bash
git grep -n "<pattern>" -- .        # tracked files, whole repo
grep -rn "<pattern>" . --exclude-dir=node_modules --exclude-dir=.git
```

**Trap:** a grep scoped to a few directories and extensions will happily report
zero while the string sits in `.env.example`, a README, a workflow file or a
config. Search the whole repo, then narrow. "None" is a strong claim; earn it.

## Before saying "I can't"

Try the underlying API first.

A missing MCP tool or CLI subcommand is not proof the capability is absent. The
platform's REST API usually exposes it, and credentials are often already on disk
(the platform CLI's own config file, `gh auth token`, env vars). One attempt costs
a few seconds; a wrong "I can't" costs the user hours and they will find out you
were wrong.

When mutating shared config through a raw API, send only the sub-object you intend
to change, then re-read and confirm the neighbouring settings survived.

## Reporting

Report per layer, with the evidence inline:

```
Code      clean, HEAD <sha7> == origin/main
CI        green for <sha7> (<job> ✓, <job> ✓) — run <id>
Deploy    live commit <sha7> matches HEAD
Pages     <route> → <new thing> present, <old thing> absent
Endpoint  POST <route> → <status> <body>
Storage   record <id> written and read back
Events    <event_name> seen in realtime
```

Anything unverified is listed as **unverified**, never omitted and never softened
into sounding checked. If you could not check something, say which layer and why.

State failures first and plainly. A status report that buries a red layer under
green ones is worse than no report.

## Honesty rules

- Never present a conclusion drawn from inference as one drawn from data. Say
  which it is.
- If you previously claimed something worked and it did not, lead with the
  correction, name the specific mistake, and do not pad it with what went right.
- Scope your claims to what you measured. "One lead was lost" and "leads are being
  lost" are different claims requiring different evidence.
- A tool that silently returns success is the most dangerous thing in any stack.
  When a system reports success, ask what would look identical if it had failed —
  then go check that.
