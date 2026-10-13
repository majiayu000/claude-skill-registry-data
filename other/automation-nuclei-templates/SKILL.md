---
name: automation-nuclei-templates
description: >
  Write custom nuclei templates to codify a finding into a repeatable, mass-scannable check.
  Load on "write a nuclei template", turning a manual bug into automation, checking a CVE across
  many hosts, or regression-scanning. Signals: a reproducible request→match, YAML templates, nuclei.
domain: automation
type: technique
stability: learning
modes: [bugbounty, defense]
severity: info
tools: [nuclei]
schema_version: 1
---

# Custom nuclei templates

## When it applies
You confirmed a bug (or a CVE pattern) and want to (a) find every other affected host and
(b) keep a regression check. A nuclei template turns "one request + one match condition" into
a scalable, shareable detector.

## Why it works
nuclei runs declarative YAML: send request(s), assert matchers on the response. If your finding
is expressible as request→observable signal, it's a template — and then it scans thousands of
hosts consistently, no manual repetition.

## Method
1. **Capture the minimal repro**: the exact request and the unambiguous signal that proves the
   bug (status, a body string, a header, a reflected marker, response time).
2. **Write the template**: `id`, `info` (name/severity/tags), then `http:` with `method`,
   `path` (use `{{BaseURL}}`), any `payloads`, and `matchers` (`word`/`status`/`regex`/`dsl`).
   Use `matchers-condition: and` to avoid false positives; add an `extractor` to pull the proof.
3. **Reduce false positives**: match a signal unique to the vuln (a computed reflection, a
   specific error), not a generic 200; test against a known-good and known-bad host.
4. **Validate**: `nuclei -t mytemplate.yaml -u https://known-vuln` (should hit) and against a
   safe host (should not). Lint with `-validate`.
5. **Scale/share**: run across your live-hosts list; contribute non-sensitive templates upstream.

## Gotchas
- Overbroad matchers = noisy, untrusted results; require a signal that only the vuln produces.
- Interpolate `{{BaseURL}}`/variables correctly; hardcoded hosts don't scale.
- Destructive checks (writes/DoS) don't belong in a mass template — keep them read-only.

## Verify success
The template fires only on genuinely-affected hosts (true on the known-vuln, quiet on the
known-good) and extracts a clear proof.

## References
nuclei templating guide; nuclei-templates repo (examples); PDTM docs.
