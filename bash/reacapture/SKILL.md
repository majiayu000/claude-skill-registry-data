---
name: reaCapture
description: Analyze what a platform's client does from live runs in the account's own browser (AdsPower first). Every browser action records a raw HAR of the session, the installed rea-agents CLI reads it and its scripts offline, and the findings go through SubQ matrices to make design decisions for log-cli's Facebook client. Use to resume the REA work, run a capture, read rea's Evidence, or turn findings into a matrix.
---

# reaCapture

The point of this work: use REA on real captures of our own Facebook client
to find out what the create page actually does, then score design changes
with SubQ so the client gets as efficient as it can. The work is based on
live runs. log-cli already knows much of the flow
(`docs/listingPublish/`, `src/facebook/marketplace/publish/machine.ts`). The
captures test that knowledge and find what it misses.

Why a HAR plus scripts, read offline: `docs/rea/matrix/` and
`docs/rea/spec.md`.

## Hard boundaries

1. **Captures are raw (rule 19).** The HAR keeps every cookie, header,
   token and body. Nothing is stripped, because the analysis needs it. It
   stays on the owner's development machine in the run folder
   (`~/.logCli/publish/<run>/<browser>`) and is never committed.
2. **Captures come from every browser action (rule 19)**: inspect, flow,
   host, warm-up, `facebookConnect`, `facebookScan`, `facebookStatus`, each
   `facebookWatch` check and `log facebook publish` (dry run unless `--live`,
   rule 8). There is no flag to skip it. Those runs follow the launch rules
   as they are (rule 35): headed, proxy in country, self-check, waking hours.
3. **REA reads files, never the window.** No CDP, no attach. The rea
   commands that need a live target (`inspect-web-page`,
   `analyze-web-bundle`, `observe-web-*`, `export-web-scripts`) aren't
   used on the account's browser.
4. **Listen, don't replay.** A capture never sends a request of its own.

## Environment

- `rea --version` prints `6.7.0` (`npm install --global rea-agents@6.7.0`).
  Frida's postinstall is skipped. The HAR and script commands don't need it.
- SubQ: `SUBQ_API_KEY` in the environment, `POST https://api.subq.ai/v1/systemone`,
  model `subq-snap-preview`, 1-16 questions per call. Pattern:
  `docs/rea/matrix/runMatrix.mjs`.
- Code: `src/rea/capture/` (`exportScripts`, `settleCapture`,
  `captureFromHar`), `src/cli/capture/`, and the `record_har_*`
  arguments in `python/session/publishSession.py`.

## The loop

### 1. Capture (live)

Any action records one. Through the MCP, `mcp__log__facebookConnect` /
`facebookScan` / `facebookPublish` do the same.

```bash
log facebook connect --account <a> --noPrompt   # the login, step by step
log facebook scan --account <a>
log facebook publish <listingId>                # dry run; the HAR records the whole session
```

Where: `~/.logCli/runs/<action>/<time>_<account>/<browser>/` (`adsPower`, `camoufox`, or `firefox` for runs before 2026-10-20) (`LOG_RUNS_DIR`
moves it; a watch has `check<N>/` per check), and publish's
`~/.logCli/publish/<run>/<browser>/`. The command's last lines name the folder.

Per action: the Python writes each log line, timed, to `steps.jsonl` (what
the run did: page reached, email typed, submitted, code typed...). After the
run, `settleRunCapture` cuts `session.har` by those times into
`steps/NN_<action>.har` (each request goes to the step it started in; quiet
steps are left out), runs `rea inspect-web-network-capture` on each one
(`steps/NN_<action>.rea.json`), and lists them in run order in
`steps/index.json`. Read a step's rea output to see exactly what Facebook
did for that one action, e.g. which GraphQL operations the login submit
fired.

The run folder gets `<browser>/session.har` (raw), `<browser>/scripts/scriptN.js`,
`<browser>/scriptsManifest.json` and `<browser>/reaNetwork.json`, and the exit
notes print
`Capture: N requests, M scripts, raw HAR kept. REA ...`.

### 2. Read with rea (offline)

`log facebook publish` runs these itself. To re-run on any HAR:

```bash
log capture har <path> --out <dir>      # --noRea to only write the files
rea inspect-web-network-capture <absolute>/session.har har --format json
```

Never `rea analyze-javascript-application` on a run's whole `scripts/`: it
timed out after 10 minutes on 50 MB of bundles (2026-10-19). Facebook's code
is read per request instead (step 2b).

- `reaNetwork.json` → `normalized_result.records[]`, one per request:
  method, URL, status, mime, timings, and the request body. On Facebook
  the operation is in the body of `POST /api/graphql/`
  (`fb_api_req_friendly_name`, `doc_id`, `variables`). rea blanks the
  values of the auth headers and cookies it knows in its own output. The
  HAR still has them. Keep the `evidence_id`.

### 2b. The Facebook client docs (per request, rule 25)

```bash
log capture docs          # run it live (Monitor), every stage prints
```

1. Every run under `~/.logCli` is split by its `steps.jsonl`; each request
   to Facebook is named (GraphQL by `fb_api_req_friendly_name`, or by
   `doc_id` through Facebook's `_facebookRelayOperation` modules; other
   POSTs by path) with its step, status, duration and time after our step.
2. Facebook's bundles are parsed into a syntax tree (TypeScript's compiler,
   `src/rea/facebookClient/helpers/indexModules.ts`): every
   `__d("Name", [deps], factory)` module.
3. Each GraphQL request's slice (`<Name>.graphql`, its doc_id module, and the
   modules that import it) goes to `rea analyze-javascript-application`:
   about 4 s each, cached by sha256 in `~/.logCli/rea/facebookClient/`.
4. `docs/platforms/facebook/<domain>/<Name>.md` gets the facts block, redacted
   before it is written (`src/privacy/redact`: secrets, emails, phones, IPs,
   ids, names, usernames and message text become `<slackToken>`, `<email>`,
   `<userId:1>`, `<messageText>` and the like; the raw run stays in
   `~/.logCli/runs/`). The three
   reasoning sections are written by hand from the facts and rea (open the
   Evidence with `inspect_analysis_view`). lefthook's pre-push refuses a
   push while any is unwritten, unread by rea, or older than a run.
5. Every other platform with a browser path (Reddit) is documented the same
   way under `docs/platforms/<platform>/`, its calls named by GraphQL
   operation or path and its code found in its own bundles.

What the recording, the docs build and the docs gate must do is in
[docs/specs/runsAndRea.md](../../docs/specs/runsAndRea.md).

### 3. Findings

Every run writes a first pass itself: `<browser>/findings.md` in the run
folder, one section per step with Facebook's GraphQL operations by name
(`x-fb-friendly-name`), pages loaded, uploads, failed requests and the
step's rea `evidence_id` (`summarizeStep`). Names and counts only. Read it
first; e.g. `useUFACSubmitActionMutation` is a checkpoint answer being sent,
`useMarketplaceComposerAttributesQuery` the category being set.

What rea does per run (`settleInBackground`, its own hidden process):
- the whole `session.har` only when it is 32 MB or less (rea's
  `maximum_capture_bytes`); bigger ones are read per step only;
- the scripts are saved, never read whole: `--docs` reads them per request;
- `settle.json` says when it finished and what it read.

For a decision, write `docs/rea/findings/<runId>.md` by hand: the operations the
create page fired, in order, with timing; the fields each one submits;
what the page's scripts read from the browser; and every gap against
`src/facebook/marketplace/publish/machine.ts` and `docs/listingPublish/formFill.md`.
Each line names its rea `evidence_id`. Session values aren't copied into
this file. It holds names, orders and counts.

### 4. SubQ matrix

Copy `docs/rea/matrix/runMatrix.mjs` into `docs/rea/<question>/` and
give it the findings as state, design options as `options.json`, criteria
(efficiency: requests, time, failure points, fit with the gate) as
`criteria.json`, and the claims the findings support or refute as
`claims.json`. Run two repeats per pass, as before, and keep
`subqResults.json`.

### 5. Decide

The winning option becomes a change to the client, plus a failing
fixture test first (`python/fixtures/createItem.html` or a new fixture).
Record the decision and its evidence ids in the `log.md` entry.

## Every action's run feeds the request docs

Every action (inspect, flow, host, warm-up, publish) records the session's
`session.har` with Facebook's bundles in it, and `log capture docs`
reads code slices from all of them: a run that isn't settled yet (a host still
open) has its bundles taken from its `session.har` and kept as `scripts/`
(`scriptsFromHar`). The recorder reads each body first, before any header round
trip, keeps scripts and documents up to 16 MB (other bodies 2 MB), and writes
`_bodyError` on a response whose body it couldn't keep; the build says how many
were lost. A request whose slice no run has is read the next time a run loads
its bundle.

