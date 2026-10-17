---
name: verify
description: Verify a claim before stating it, and verify a test before trusting it, in OpenAlgo Desktop. Use before asserting that a security control holds (redaction, CSRF, broker state check, API key, webhook secret), that a pattern is safe, that a bug is fixed, that a leak is gone, or that a test guards a fix; when reporting audit or scanner findings (cargo deny, cargo audit, npm audit, gitleaks, trivy, CodeQL, leak_grep); when a grep "found nothing"; when a clippy, test or scanner count looks clean; and before telling anyone something is or is not a vulnerability.
---

# Verify before claiming

High-severity findings come from executing something. Wrong claims come from
reading something and reasoning about it. The rules are cheap; skipping them
produces a confident, wrong answer that a maintainer then acts on.

## Rule 1: execute the control, never read it

A redaction function, a CSRF check, a route guard, an account binding, a
regex: each is code. Run it on a realistic value and look at the output.

The desktop's redaction is Rust, in four places, each with different
coverage:

| Code | What it removes | What it does not |
| --- | --- | --- |
| `brokers::common::redact::url_safe` / `url_safe_error` | userinfo, query and fragment of every `scheme://` URL in a text | a token in a URL *path*, a token not in a URL at all |
| `brokers::common::redact::{http, ws, redact}` | the URL from a `reqwest` error, socket errors reduced to their kind | anything the adapter formats itself |
| `db::sqlite::logs::redact` | the keys `apikey`, `api_key`, `password`, `totp`, `auth_code`, `request_token` at the top level of a logged request body | the same keys nested deeper, any other key name |
| `services::error_log::sanitize_url` | sensitive query values (`SENSITIVE_QUERY_NAMES`) and the fragment of a client-reported URL | the path |

Whether a given log line leaks depends on data you have not read yet: the
real parameter name, whether the token rides in the path, whether a body is
nested. So do not judge it; drive it.

**How to execute it here.** The functions are pure, so a throwaway unit test
is the fastest probe. Put it in the module's own test block, run it, read the
output, then delete it (or keep it if it guards something):

```rust
#[test]
fn probe_url_safe() {
    for s in [
        "GET wss://ws.example/feed?api_key=SENTINEL1&access_token=SENTINEL2 failed",
        "error sending request for url (https://api.example/v1/SENTINEL3/orders)",
        "https://user:SENTINEL4@host/x",
    ] {
        println!("{} => {}", s, url_safe(s));
    }
}
```

```bash
cd src-tauri && CARGO_TARGET_DIR=/Users/openalgo/openalgo-desktop/openalgo-desktop/src-tauri/target \
  cargo test --locked --lib probe_url_safe -- --nocapture
```

Expect the second line to survive: `url_safe` keeps the path (its own test,
`queries_and_userinfo_are_dropped`, pins `http://h/p` through unchanged), so
a token in a URL path is not redacted by it. That is the kind of answer
reading the function will not give you with confidence; the probe's output
is the evidence.

Mind the shared target directory before probing: a `--lib` test build from a
new worktree path compiles a fresh copy of this crate (several GB). On a
nearly full disk, or while other agents hold the build lock, run the probe
in the worktree that already built, or ask.

**For a whole path** (an adapter's login failure, a feed's reconnect), drive
it with sentinel credentials, capture the tracing output at TRACE, and scan
what was written. The harness pattern is
`src-tauri/tests/it/brokers_direct_batch_b/secrets.rs` (`capture()`,
`logs_clean()`, which also asserts the capture is not empty). For output you
captured yourself, or a test data directory's databases:

```bash
cargo test --locked --test it <name> -- --nocapture 2>&1 > run.log
python3 .claude/skills/verify/leak_scan.py run.log
python3 .claude/skills/verify/leak_scan.py --marker MYSENTINEL <test-data-dir>/logs.db <test-data-dir>/openalgo.db
```

`leak_scan.py` flags the sentinel (default `SENTINEL`, `SEKRET`), a
sensitive query parameter with a real value (`apikey=`, `access_token=`,
`token=`, `jKey=`, `susertoken=`, `code=`, `Value1=`, ...; redaction
placeholders such as `<redacted>` and `%5Bredacted%5D` pass), `user:pass@`
in a URL, `Authorization: Bearer <value>`, and a JWT with a real-looking
signature (fixture JWTs ending in `.sig` pass). SQLite files are opened
read-only and every text cell is scanned. It exits 1 on a leak and 2 when
nothing was scanned: an empty capture proves nothing, so it refuses to
report clean. Hits are printed masked. Never point it at the trader's real
data folder.

## Rule 2: break the code to validate the test

A test that passes proves nothing until you have seen it fail. Revert the
fix, or neuter the exact guard it depends on, run the test, watch it go red,
restore, watch it go green.

```bash
git diff > /tmp/fix.patch           # or note the one line you will neuter
# edit the guard (e.g. make catalog::configured_account return None)
cargo test --locked --lib every_way_to_create_a_broker_session -- --nocapture   # must FAIL
git checkout -- src-tauri/src/brokers/catalog.rs                                 # restore
cargo test --locked --lib every_way_to_create_a_broker_session                   # must PASS
```

Ways a test passes for the wrong reason, all possible here:

- **Tautological assertion.** The test re-implements the predicate inline
  instead of calling the function under test, so it tests `<`.
- **Vacuous pass.** The assertion holds whether or not the fix is present: a
  log capture that captured nothing (hence `logs_clean` asserts non-empty), a
  test against the wrong broker id in `family_harness`, a `#[tokio::test]`
  that returns before the awaited path runs, an `isolated!` test whose child
  ran zero tests (hence `run_isolated` checks for `1 passed`).
- **Racing a timer.** An assertion made before a debounce, a backoff or a
  reconnect fires holds by timing. Use the injected clock (`ManualClock`) or
  wait on the condition (`broker_session_e2e::until`), not a sleep.
- **A test that fails one run in five is a bug**, and almost always a race
  (every flaky test here so far was). Run a suspect test 10 to 30 times
  before calling it fixed:
  `for i in $(seq 1 20); do cargo test --locked --test it <name> -q || break; done`.
- **Wrong target.** When neutering a guard, change the exact line. A blind
  replace hits the first match, which may be a different guard, and then the
  red run proves nothing.

## Rule 3: grep for the sink, not the variable name

A grep that returns nothing is evidence about your pattern, not about the
code. Searching for `access_token` inside `tracing::` macros cannot see a
secret that rides inside something else that is logged:

- a URL assembled with the token in the query or the path, logged with `{}`;
- a `reqwest::Error` or `tungstenite::Error` logged with `{}` (their
  `Display` repeats the URL; hence `common::redact::http` / `ws`);
- a request or response body logged in full (`{:?}` of a payload struct);
- a `format!("{:?}", credentials)` of a struct without a redacted `Debug`;
- a value that reaches the trader-facing message (`client_message`).

Before concluding a class is clear, ask what the leak would look like if the
secret were never named in the log statement, and search for that. The same
holds for `leak_grep.py` (fd-audit): zero `conn-across-await` suspects means
the pattern did not match, not that no connection waits on the network. Its
`--self-test` shows each check can fire at all.

## Rule 4: baseline before and after

A count without its prior value is meaningless. Capture it on the base,
apply the change, capture again.

```bash
cd src-tauri
cargo clippy --all-targets --locked -- -D warnings 2>&1 | grep -c '^error'      # on the change
git stash push -m verify-baseline && cargo clippy --all-targets --locked -- -D warnings 2>&1 | grep -c '^error'; git stash pop
```

(The stash is shared across worktrees; prefer comparing against a clean
worktree of the base commit, see the `parallel-work` skill.)

Traps specific to this repo:

- **The shared target directory.** Every worktree builds into
  `/Users/openalgo/openalgo-desktop/openalgo-desktop/src-tauri/target`. A
  test that runs `target/debug/openalgo-desktop` may run another checkout's
  build (`tests/it/mcp_subcommand.rs` guards against it). A green run of a
  binary you did not just build is not your code's result.
- **Ignored tests.** `soak` and other long tests are `#[ignore]`; a run that
  did not pass `--ignored` did not run them. Check the summary line for the
  count you expected.
- **Test filters that match nothing** print `0 passed` and exit 0. Read the
  count.
- **`cargo test --lib` vs `--test it`.** Unit tests (`src/**`) and the one
  integration crate (`tests/it/main.rs`) are separate binaries; a new file in
  `tests/it/` that is not declared with `mod` in `main.rs` never runs.

## Rule 5: distinguish "already safe" from "fixed"

Reporting a safe site as fixed inflates the work and teaches the reader that
the report cannot be trusted. Of N reported sites, say which leaked, fix
those, and name the rest as false positives with the reason. Scanners here
produce known false positives: `cargo deny` duplicate-version warnings (not
vulnerabilities), CodeQL hard-coded-value alerts in `#[cfg(test)]` modules,
gitleaks on fixture placeholders (allowlisted in `.github/gitleaks.toml`),
`leak_grep.py` suspects that are test doubles or swept caches (triaged in the
fd-audit skill).

## Rule 6: an unrun check is not a pass

If a tool is not installed (`cargo audit` and `trivy` are not on this Mac by
default), timed out, or was blocked on the shared target's build lock, say so
and treat the area as unverified. A command that printed nothing because it
never compiled is not a clean result.

## When you are wrong

Correct it in one plain sentence with the evidence, and carry on. A wrong
claim quietly dropped is worse than one corrected, because someone may
already have acted on it.
