---
name: web-sync
description: Port recent OpenAlgo web commits (github.com/marketcalls/openalgo) to OpenAlgo Desktop. Use when asked to catch up with the web, sync or port web changes, review what changed upstream since a date or commit, carry a web fix or feature (broker, frontend page, /api/v1 endpoint, service, WebSocket protocol) into the desktop, or re-record a golden fixture after the web changed a wire format.
---

# Porting web commits to the desktop

The web defines the contract; the desktop follows it. Anything that works
against the web must keep working against the desktop unchanged, so a web
change to a wire format, a page or a broker is desktop work. The web checkout
next to this repo (`/Users/openalgo/openalgo-desktop/openalgo`) is read-only
reference: never pull, edit, check out, stash or commit there. If it is
stale, read upstream through `gh` instead.

## 1. List the commits

From GitHub (always current):

```bash
gh api "repos/marketcalls/openalgo/commits?since=2026-10-01T00:00:00Z&per_page=100" --paginate \
  --jq '.[] | [.sha[0:9], .commit.author.date[0:10], (.commit.message | split("\n")[0])] | @tsv'
gh api "repos/marketcalls/openalgo/commits/<sha>" --jq '.files[] | [.status, .filename] | @tsv'
gh pr list -R marketcalls/openalgo --state merged --search "merged:>=2026-10-01" --limit 100
gh pr view <number> -R marketcalls/openalgo --json title,body,files,mergeCommit
```

Or from the read-only checkout (a read-only `git log` / `git show` is fine;
nothing that writes):

```bash
git -C /Users/openalgo/openalgo-desktop/openalgo log --since=2026-10-01 --oneline --no-merges
git -C /Users/openalgo/openalgo-desktop/openalgo show --stat <sha>
```

Start from the last web commit already ported: search this repo's history for
the web PR numbers (`git log --grep 'openalgo#'`).

## 2. Classify each commit

Write the list down first, one line per web commit or PR, with its class and
the decision. Skipped commits are listed explicitly with the reason, so the
next sync does not re-read them.

| Web path | Desktop destination | How |
| --- | --- | --- |
| `broker/<name>/**` | `src-tauri/src/brokers/<name>/` (or the family config under `brokers/families/{noren,xts}`) | port the behaviour to Rust with the `broker-integration` skill; payload changes get a new recorded fixture under `src-tauri/tests/fixtures/brokers/<name>/` |
| `frontend/src/**` | `src/**` at the same relative path | port by diff (below); keep the file as close to the web original as the desktop allows |
| `restx_api/*.py`, `restx_api/schemas.py` | `src-tauri/src/server/api_v1/*.rs`, `src-tauri/src/services/schemas.rs` | request validation and error shapes, field for field |
| `services/*.py` | `src-tauri/src/services/*.rs` | response dicts, envelopes, number types, date formats |
| `websocket_proxy/**` | `src-tauri/src/feed/**` (8765 server), `src-tauri/src/websocket/` (broker side) | protocol frames and acks; `tests/it/feed_conformance.rs` |
| `sandbox/**` | `src-tauri/src/sandbox/**` | engine behaviour; `tests/it/sandbox_web_scenarios.rs` |
| `events/**` | `src-tauri/src/events/**` | topics and payloads |
| `mcp/**` | `src-tauri/src/mcp/**` | tool names, descriptions and schemas are pinned by `tests/it/mcp_contract.rs` |
| `test/test_*.py`, `test/risk/vectors.json` | Rust tests (below) | port the cases |
| `docs/api/**`, `docs/prompt/**` | nothing to copy; they are the contract source | re-read when the change touches a wire format |
| `pyproject.toml`, `uv.lock`, `requirements*.txt` | skip | Python dependencies |
| the Agent (`blueprints/agent*`, `services/agent*`, `frontend/src/{pages,components,lib}/agent/**`, `frontend/src/api/agent.ts`, `frontend/src/components/trading/AgentPanel*`, `frontend/src/lib/trading/chartContract.ts`, the Assistant entry in `RightRail.tsx`) | skip | not in this version (maintainer, 2026-10-12) |
| Flow (`/flow`, `flow/**`, `frontend/src/**/flow*`) | skip | out of scope |
| Python Strategy Host (`/python`, `blueprints/python_strategy.py`, the Telegram bot's `/stoppython`) | skip | not in this version (maintainer, 2026-10-12) |
| pandas backtesters (Portfolio Backtester, SIP Backtester, Portfolio Analyzer) | skip | out of scope |
| `.github/**`, Docker, install scripts, `upgrade/**` | skip (read for intent only) | web deployment |
| `frontend/dist` auto-build commits (`github-actions[bot]`) | skip | build output |

A commit that spans classes is split: port each part to its destination, and
skip the parts that are out of scope by name.

## 3. Frontend by diff

```bash
WEB=/Users/openalgo/openalgo-desktop/openalgo
gh api "repos/marketcalls/openalgo/commits/<sha>" -H "Accept: application/vnd.github.diff" > /tmp/web-<sha>.diff
# or: git -C "$WEB" show <sha> -- frontend/src > /tmp/web-<sha>.diff
sed 's#frontend/src/#src/#g' /tmp/web-<sha>.diff > /tmp/desktop-<sha>.diff
git apply --3way --check /tmp/desktop-<sha>.diff && git apply --3way /tmp/desktop-<sha>.diff
```

Conflicts are the desktop's intentional differences (for example
`src/lib/desktop.ts` hooks, server-built OAuth URLs, port defaults). Keep the
desktop difference and take the web change around it. Compare a whole file
with `diff "$WEB/frontend/src/<path>" src/<path>` before and after; the gap
must not grow. A page added on the web is a route in the frontend router, the
same path served by the Rust SPA fallback (`server/spa.rs`), and the
navigation entry, in one change. Vitest tests carried over with the page live
next to it, as on the web. Run `npx tsc -b`, `npx vitest run`, and
`npx biome ci ./src`.

The desktop runs a newer Biome than the web (2.5 against the web's 2.3), which
sorts export lists and formats `it.each` calls differently, so about 26 files
under `src/components/ui` and the tests differ from the web in formatting
only. After applying a web diff to such a file, run `npx biome check --write`
on it; don't hand-revert the formatting to match the web.

## 4. API and services: parity plus golden fixtures

1. Read the web change in `restx_api/` (validation), `services/` (the
   response dict) and the docs under `docs/api/`.
2. Change the Rust handler and service to match field for field: key names,
   status strings, flat versus `{status, data}`, `message` as a string
   (business error) or an object (validation error), HTTP codes, number
   types, date and timestamp formats.
3. If the wire format changed, the golden fixture must change too (section
   6), and `tests/it/api_v1_contract.rs` replays it: errors compared exactly,
   successes by status and shape (`api_v1_support::same_shape`).
4. A web defect is not copied: `tests/fixtures/web/INDEX.md` lists the
   observed ones and `DIVERGENT` in `api_v1_contract.rs` asserts the
   desktop's corrected behaviour. Add to both if the new commit records one.

## 5. Port the web's tests

For each `test/test_*.py` the commit adds or changes, port its cases (same
inputs, same expected outputs, same edge cases) as Rust tests:

- pure logic (a mapper, a calculator, a parser): a unit test beside the code
  (`#[cfg(test)] mod tests` or the module's `tests.rs`);
- an endpoint or a flow: `src-tauri/tests/it/<area>_<topic>.rs`, declared in
  `tests/it/main.rs`; harnesses in `api_v1_support`, `webui_support`,
  `sandbox_support`, `feed_support`, `mcp_support`;
- risk vectors: the web's `test/risk/vectors.json` is the contract for the
  Rust risk core; copy it over `tests/fixtures/risk/vectors.json` and keep
  every vector passing (`cargo test --locked --lib risk`);
- a test that only speaks HTTP to `/api/v1` can be pointed at a desktop test
  server unchanged.

Name the source in the test's doc comment (`/// Web test/test_x.py::test_y`).
A ported test must fail without the ported change (`verify` skill, rule 2).

## 6. Golden fixtures

Fixtures recorded from a live web instance are the first authority
(`tests/fixtures/web/README.md`): REST pairs in
`tests/fixtures/web/rest/<endpoint>/<case>.json`, WebSocket transcripts in
`tests/fixtures/web/websocket/*.jsonl`, indexed in `INDEX.md` and
`rest_index.json`. When the web changes a wire format, re-record the
affected cases with the scripts in `tests/fixtures/web/capture/` (they read
the key from `OA_APIKEY` and talk to the web instance on `127.0.0.1:5000`).

Recording calls the maintainer's live web instance, so it is done only by the
maintainer or with the maintainer's explicit go-ahead for that session, and
only in analyzer mode for anything that places orders. Then:

- replace every API key, account id and email with `<APIKEY>`, `<USER_ID>`,
  `<EMAIL>` before the file is staged;
- run `gitleaks git --no-banner -c .github/gitleaks.toml --log-opts="origin/master..HEAD" .`
  and `python3 .claude/skills/verify/leak_scan.py --shapes-only <fixture>`;
- update `INDEX.md` with the date and the reason.

Broker payload fixtures (`src-tauri/tests/fixtures/brokers/<broker>/`)
follow the same placeholder rule.

## 7. Commits

One commit per web PR (or per direct web commit), referencing it:

```
fix(api): match web optionchain strike rounding (openalgo#1234)

Port of marketcalls/openalgo#1234 (<web sha>): <what changed and why>.
Fixture tests/fixtures/web/rest/optionchain/basic.json re-recorded.
```

The type follows the change (`feat:`, `fix:`, `test:`, ...). A sync that
skips commits ends with one `docs:` or `chore:` commit, or a note in the
merge description, listing each skipped web commit with its reason. Run the
full gates before pushing (see the `parallel-work` skill).
