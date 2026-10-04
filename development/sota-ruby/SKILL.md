---
name: sota-ruby
description: >-
  State-of-the-art Ruby engineering rules (supported Ruby releases) that Claude
  applies when writing or auditing Ruby. Covers modern idioms (frozen string literals,
  pattern matching, Data/Struct, RBS/Sorbet/Steep typing), security (SQL injection via
  ActiveRecord/Sequel, ERB/XSS escaping, mass assignment, CSRF, Marshal/YAML
  deserialization, command injection, ReDoS), framework-neutral web hardening
  (Rails/Sinatra/Hanami as neutral examples), supply chain and tooling (Bundler lockfile
  and checksums, bundler-audit, RuboCop/StandardRB, Brakeman, RSpec/Minitest, CI gates),
  and concurrency/performance (GVL, threads vs fibers vs Ractors, background-job
  idempotency, YJIT/ZJIT, GC and memory, N+1 queries). Trigger keywords: Ruby, gem,
  Gemfile, bundler, Rails, Sinatra, Hanami, Rack, ERB, ActiveRecord, Sequel, RSpec,
  minitest, RuboCop, Sorbet, RBS, Sidekiq, YJIT, Ractor, rake, ruby-lang. Use for BOTH
  building Ruby services/gems/CLIs and reviewing or auditing Ruby codebases.
---

# SOTA Ruby (2026)

Expert-level rules for producing and auditing production Ruby. Baseline language
line: **Ruby 3.4+**; Ruby 4.0 was released 2025-12-25 and is in normal
maintenance (latest stable — verify at the branches page). Per the [official branches page](https://www.ruby-lang.org/en/downloads/branches/):
4.0 and 3.4 are in normal maintenance; 3.3 is security-maintenance only
(expected EOL 2027-03); 3.2 and older are EOL (3.2 since 2026-04-01) — running
them is itself a finding. Feature notes: `Data.define` and `Regexp.timeout`
from 3.2, `it` block parameter and chilled-string warnings from 3.4,
`Ractor::Port` and experimental ZJIT from 4.0 — noted where relevant. Every
rules file ends with an audit checklist of grep/lint patterns.

## Purpose

Two consumers, one source of truth:

- **BUILD mode** — generating new Ruby code: follow the rules as defaults, not
  suggestions. Deviate only with an explicit comment justifying it.
- **AUDIT mode** — reviewing existing Ruby code: hunt violations using the
  audit checklists, classify by severity, report in the finding format below.

## BUILD mode

1. Before writing code, read the rules files relevant to the task (see index).
   A web endpoint touching the DB and a background job needs `02`, `03`, `05`.
2. Apply the **top-10 non-negotiables** (below) unconditionally.
3. Establish context first: `.ruby-version`, `Gemfile`/`Gemfile.lock`, RuboCop
   or StandardRB config, framework and test runner in use. Match the project's
   floor (no `it` block param on a 3.3 project).
4. New projects: pin the Ruby version (`.ruby-version`), commit
   `Gemfile.lock`, add RuboCop **or** StandardRB, `bundler-audit`, and the
   test suite to CI from day one (see `rules/04`). Rails apps add Brakeman.
5. Security posture is non-optional even when unrequested: parameterized SQL,
   argv-form process spawning, `YAML.safe_load` semantics, `SecureRandom`,
   escaped output (see `rules/02`, `rules/03`).
6. Write tests alongside the code (RSpec or Minitest — match the project).
   Anything with threads or jobs gets an idempotency/concurrency test.
7. When code must violate a rule for a legitimate reason, leave a
   `# NOTE(sota):` comment explaining the trade-off so auditors don't flag it.

## AUDIT mode

Work through each relevant rules file's audit checklist against the target
repo. Run the listed grep/lint commands; confirm each hit manually before
reporting (greps are recall-oriented, expect false positives). Useful
mechanical sweeps: `bundle exec rubocop`, `bundler-audit check --update`,
`brakeman -q` (Rails), plus the per-file greps.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **CRITICAL** | Exploitable now, or data loss | SQL built with `#{}` interpolation, `Marshal.load`/`YAML.unsafe_load` on external data, command injection via backticks with user input, `html_safe` on user input |
| **HIGH** | Exploitable with preconditions, or production-breaking | Missing CSRF protection on state-changing routes, `permit!`, `^`/`$` anchors in validation regexes, `rand` for tokens, `Timeout.timeout` around DB work, EOL Ruby in production |
| **MEDIUM** | Correctness/maintenance hazard, latent bug | N+1 on a hot path, non-idempotent retried jobs, no `Gemfile.lock` in an app, mutable shared state across threads without a lock, `rescue Exception` |
| **LOW** | Deviation from SOTA, friction | Missing frozen-string-literal comments, `Struct` where `Data` fits, stringly-typed booleans, unpinned dev tooling |
| **INFO** | Worth knowing, no action forced | YJIT not enabled, typing (RBS/Sorbet) absent, newer-Ruby features available after a floor bump |

### Finding format

```
file:line | rule violated (rules/NN §section) | severity | effort | fix
```

Severity: Critical / High / Medium / Low / Info. Effort: trivial / small /
medium / large. Borderline severities state the deciding assumption;
unconfirmed findings are marked "needs verification", never asserted. Group
findings by severity, CRITICAL first; end with counts per severity, the three
highest-leverage fixes, and which checklists were run.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-language-idioms.md` | Choosing/verifying the Ruby version baseline; frozen string literals; pattern matching; `Data` vs `Struct`; exception design; **`nil` over a sentinel, and `to_i` silently returning `0` for garbage**; typing with RBS/Sorbet/Steep; general idioms and pitfalls |
| `rules/02-security.md` | Any input crossing a trust boundary: SQL injection (ActiveRecord/Sequel), command injection (`system`/backticks/`Open3`), deserialization (`Marshal`, YAML/Psych), XML parser options (XXE/entity expansion in Nokogiri, REXML), ReDoS and regex anchors, `eval`/`send`/`constantize`, secrets and randomness, **the encrypted-credentials key** (`config/master.key`, `RAILS_MASTER_KEY`) kept out of git, path traversal; **escape hatches into raw memory**: Fiddle, the `ffi` gem and C extensions |
| `rules/03-web-hardening.md` | Building or auditing anything web-facing: XSS/ERB escaping, mass assignment and strong params, CSRF (incl. HEAD→GET verb confusion and routes that widen verbs or actions), sessions and app-set cookie flags, security headers, debug mode left on in production, outbound TLS verification, open redirects, SSRF, file uploads and `render file:`, **mounted admin apps** (`Sidekiq::Web`) without authentication — framework-neutral |
| `rules/04-supply-chain-tooling.md` | Bundler and Gemfile.lock discipline, lockfile checksums, **choosing an alternative index or mirror** (gem.coop, `mirror.<url>`, `disable_checksum_validation`), bundler-audit, RuboCop/StandardRB, Brakeman, RSpec/Minitest mechanics, CI gates, gem authoring/publishing |
| `rules/05-concurrency-performance.md` | Threads, fibers, Ractors, and the GVL; resetting request-scoped thread-local state; background-job idempotency; YJIT/ZJIT; GC and memory (allocator, RSS); N+1 detection; profiling workflow |

## Top-10 non-negotiables

1. **Supported Ruby only** — 3.4+ in production (3.3 accepted short-term with
   an upgrade plan; ≤3.2 is a finding). Pin it in `.ruby-version` and CI.
   (`rules/01`)
2. **SQL only via parameterized queries** — hash conditions or `?`/named
   placeholders in ActiveRecord/Sequel; string-interpolated SQL is CRITICAL,
   no exceptions for "internal" values. (`rules/02`)
3. **Never `Marshal.load`, `YAML.unsafe_load`, or `eval`-family on data you
   don't fully control**; `YAML.load` is safe-by-default only on Psych 4+
   (Ruby 3.1+) — verify the runtime. (`rules/02`)
4. **Processes spawn with argv lists** (`system("cmd", arg)`,
   `Open3.capture2`), never a shell string containing external input; no
   `Kernel#open`/`URI.open` on user-supplied names (a `|cmd` name is RCE on
   ≤ 3.4; on 4.0 it is still an arbitrary file read). (`rules/02`)
5. **All HTML output escaped by default**; every `raw`/`html_safe` is
   reviewed; non-Rails ERB configured to auto-escape. (`rules/03`)
6. **Mass assignment goes through an attribute allowlist** (strong params /
   `params.expect`; explicit attribute lists elsewhere); `permit!` is HIGH.
   (`rules/03`)
7. **CSRF protection on every cookie-authenticated state-changing endpoint**;
   `\A`/`\z` (never `^`/`$`) to anchor validation regexes. (`rules/02`, `rules/03`)
8. **`Gemfile.lock` committed and CI installs frozen** (`BUNDLE_FROZEN=true`);
   `bundler-audit` gates CI; git-sourced gems pinned to a SHA. (`rules/04`)
9. **`SecureRandom` (never `rand`/`Random`) for anything security-relevant**;
   constant-time comparison for secrets. (`rules/02`)
10. **Background jobs are idempotent and enqueue after commit** — at-least-once
    delivery and retries are the contract; jobs take IDs, not objects.
    (`rules/05`)
