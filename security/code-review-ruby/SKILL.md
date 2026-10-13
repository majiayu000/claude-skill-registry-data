---
name: code-review-ruby
description: >
  Security review of Ruby code — dangerous sinks and Rails pitfalls. Load when reviewing a Ruby/Rails
  codebase/PR, on .rb source in scope, or "review this Rails app". Signals: Gemfile, config/routes.rb,
  ActiveRecord, ERB, YAML.load, send/constantize.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-94, CWE-89, CWE-502, CWE-915, CWE-78]
tools: [brakeman, semgrep, bundler-audit, ripgrep]
schema_version: 1
---

# Ruby / Rails source review

## When it applies
Reviewing Ruby source, usually Rails. Rails is safe by default in many places, so the bugs cluster
in dynamic dispatch, mass assignment gaps, raw SQL, and unsafe deserialization/rendering.

## Why it works
Ruby's metaprogramming (`send`, `constantize`, `eval`) turns strings into method/class/code
references, and Rails helpers have unsafe escape hatches (`.html_safe`, `where("...#{x}...")`,
`render inline:`). Tracing params to these is the whole game — and Brakeman automates the first pass.

## Sinks & patterns (grep, then trace to user input)
- **Code exec**: `eval`, `instance_eval`, `class_eval`, backticks/`system`/`%x`/`exec`/`open("|…")`.
- **Dynamic dispatch**: `send`/`public_send`/`__send__` with a param method name; `constantize`/
  `safe_constantize` on input (arbitrary class instantiation).
- **SQLi**: string interpolation in `where("name = '#{x}'")`, `find_by_sql`, `order(params[:sort])`,
  `pluck`/`group` with input.
- **Mass assignment**: missing/loose Strong Parameters (`params.permit!`, `permit(*keys)`).
- **Deserialization**: `YAML.load`(vs `safe_load`), `Marshal.load`, `Oj` in compat mode on input.
- **XSS/SSRF/render**: `.html_safe`/`raw` on user data, `render inline:`/`render text:` with input,
  `open`/`Net::HTTP` on user URLs, `send_file`/`params[:path]` traversal.

## Framework specifics
- **Rails**: `permit`/`require` correctness, `skip_before_action :verify_authenticity_token` (CSRF),
  `redirect_to params[...]` (open redirect), route globbing exposing actions, secrets in
  `credentials`/ENV, default `protect_from_forgery` disabled on APIs.

## Method
1. Run `brakeman` and `bundler-audit`; triage the warnings (Brakeman is high-signal for Rails).
2. `rg 'send\(|constantize|eval|where\(".*#\{|html_safe|YAML.load|render.*inline'` → trace to params.
3. Check every controller's strong-params and `before_action` auth coverage.
4. Confirm exploitable findings with `web-sqli`, `web-deserialization`, `web-ssrf`, `web-idor`.

## Gotchas
- `send` to a fixed symbol is fine; the bug is `send(params[:action])`.
- `YAML.safe_load` is safe; plain `YAML.load` on input is RCE-capable.
- Brakeman false positives exist — always confirm the param actually reaches the sink.

## References
Brakeman docs; Rails Security Guide; OWASP Ruby on Rails cheat sheet.
