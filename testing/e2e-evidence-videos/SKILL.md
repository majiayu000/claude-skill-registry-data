---
name: e2e-evidence-videos
description: Record captioned evidence videos of Playwright BDD e2e scenarios (353.e2e-bdd-playwright) for a Jira ticket. Runs each scenario alone with video on, against deployed SQA or a local production build of an open MFE PR, then burns in captions (ticket, the bug, live Gherkin steps, "The bug / Fixed" notes with freeze frames, PASSED/FAILED card with the error) and optionally attaches the passing videos to Jira. Use when asked to "record the e2e tests", "make videos of the e2e tests", "rerun the e2e with video", "add captions to the e2e videos", "evidence videos for NGS-XXXX", "attach the test videos to the ticket", or invokes /e2e-evidence-videos.
---

# E2E evidence videos

Turns e2e scenarios into short MP4s a PO or QA can watch without context: what the bug was, what
the test did, and whether the fix held. Built on the NGS-4202 / NGS-4271 run of 2026-10-27.

Scripts live in `<skill-dir>/scripts/`. Work in a scratch dir, e.g. `WORK=/tmp/ngs-videos`.
Never commit anything this skill creates; the temporary Playwright config is removed on exit.

## Where old videos are (check before re-running)

- `353/playwright.config.ts` keeps video only on failure (`chromium-scheduler`: `on-first-retry`),
  and Playwright wipes `test-results/` on every run. A passing run leaves no video.
- `353/allure-results/*-attachment.webm` holds older failure videos; map one to its test with
  `grep -l <uuid> allure-results/*-result.json`.
- `.mp4` files named in old sessions are usually Jira bug-report attachments, not test runs.

## 1. Find the scenarios

Scenarios from an open e2e PR exist only on that PR's branch. Check it out first, or the run fails
with errors like `Unknown AGUI proposal fixture` (the runner prints the branch it ran on). Ask before
switching if the tree is dirty or someone else may be using the checkout.

```bash
cd ~/git.work/353.e2e-bdd-playwright
git status -sb | head -1                             # on the e2e PR branch? clean?
grep -rln "NGS-XXXX" src/tests/features            # feature files tagged @spec:NGS-XXXX / @NGS-XXXX
npx bddgen                                           # refresh .features-gen
grep -nE "^\s*test\(" .features-gen/all/<feature path>.feature.spec.js   # line per scenario
```

Each run target is `<id>=.features-gen/all/<path>.feature.spec.js:<line>`. Ids like `4202-1`.

## 2. Pick the code under test

- **Fix merged and deployed to SQA:** use no override and skip to step 3.
- **Fix in an open PR:** production-build the PR branch and serve it locally:

```bash
<skill-dir>/scripts/build-local-mfe.sh ~/git.work/307.ehr-scheduler-website-react <pr-branch>
cd ~/git.work/353.e2e-bdd-playwright
(nohup npm run mfe:serve -- ../307.ehr-scheduler-website-react/build > /tmp/mfe-serve.log 2>&1 &)
cp <skill-dir>/scripts/probe-mfe.mjs .probe-mfe.mjs
node .probe-mfe.mjs https://sqa-e2e.sqa.raintreeinc.com https://local.raintreeinc.com:3004/ehr-scheduler
rm .probe-mfe.mjs                                    # must print MOUNTED: true
export MFE_EHR_SCHEDULER_URL=https://local.raintreeinc.com:3004/ehr-scheduler
```

`build-local-mfe.sh` refuses a dirty tree. It builds with only the SQA block of `.env`, then
restores `.env` and the original branch. A PR branch rebased on main also carries earlier merged
fixes, so one build can cover several tickets.

## 3. Record

```bash
setsid nohup <skill-dir>/scripts/run-scenarios.sh $WORK \
  4202-1=.features-gen/all/src/tests/features/scheduler/appointment/reschedule-provider-location.feature.spec.js:19 \
  4202-2=.features-gen/all/src/tests/features/scheduler/appointment/reschedule-provider-location.feature.spec.js:26 \
  > $WORK/run.log 2>&1 &
grep -E "START|END|✓|✘|ALL_DONE" $WORK/run.log     # poll; a scenario takes ~2-4 min
```

One scenario per Playwright run is deliberate. With a local MFE only the first scenario of a run
sets up reliably; later ones fail in Background with an empty location list.

For each failure, read the failing step: `jq '.[] | select(.error) | .title, .error' $WORK/<id>.steps.json`.
- **Background step, empty location list (`filter-location-multi-select-item` timeout):** harness
  flake. Re-run that id alone.
- **Failure before the code under test (e.g. the live assistant replies differently):** run the
  same id once with `MFE_EHR_SCHEDULER_URL` unset, as a control. If deployed code fails at the same
  step, it is the environment, not the fix. Say so in `why_failed`.

## 4. Caption

```bash
cp <skill-dir>/scripts/notes.example.py $WORK/notes.py    # edit: one entry per id
python3 <skill-dir>/scripts/caption.py $WORK <id>          # -> $WORK/out/<file>
```

Write the notes from the ticket's description and the feature's comments. Each note names the bug
at the step where it used to happen: "The bug: X stayed clickable here and booked the old slot.
Fixed: it is disabled." Check one frame before rendering all of them:
`ffmpeg -v error -ss <sec> -i $WORK/out/<file> -frames:v 1 /tmp/check.png`.

Layout (1280x1050): top band = ticket, scenario, bug; video 1280x720; bottom band = last 3
steps (▶ running, ✓, ✗), a red "Failed here" line, and yellow notes. Each note freezes the frame
4 s. The last frame holds 8 s under a PASSED or FAILED card. The video timeline is anchored on the
teardown of the `context` fixture, which is when Playwright stops recording.

## 5. Deliver

- Copy the files where the user asks (e.g. `/mnt/d/tmp`).
- Attach to Jira **only when asked**, and normally only the passing videos:
  `<skill-dir>/scripts/attach-jira.sh NGS-XXXX $WORK/out/<file>.mp4 ...`
- If a video ran on a local build of an open PR, tell the user. The ticket alone will not show it.

## 6. Clean up

```bash
for p in $(pgrep -f "[s]erve-local-mfe"); do kill $p; done
cd ~/git.work/353.e2e-bdd-playwright && git status --short   # no playwright.video.local.config.ts
cd ~/git.work/307.ehr-scheduler-website-react && git status --short && git branch --show-current
```

## Gotchas

- `pkill -f <pattern>` run inside a bash tool call matches its own command line and kills the
  shell (exit 143). Use `pgrep -f "[p]attern"` and `kill` the PIDs.
- `--project` takes several values: a spec path after it is read as a project name. The runner
  puts the path first.
- Run with `ENV=sqa AWS_PROFILE=rt-devops-assuresoft` (global setup reads AWS AppConfig).
  `USER_ROLE=FRONT_OFFICE` matches earlier runs. On SQA the scheduler UI logs in as AUTOMATION;
  a blocked FRONT_OFFICE account (`provider15@...`) only prints warnings.
- A development build does not mount in the deployed host (React `getOwner` mismatch). Always
  build with `--env env=prod`.
- Live-assistant scenarios depend on SQA's AI replies and can fail for reasons outside the fix.
  `@agui-proxy` scenarios with a mocked fixture are deterministic.
- Playwright's default video is 800x450. The runner sets 1280x720 so the UI text stays readable.
