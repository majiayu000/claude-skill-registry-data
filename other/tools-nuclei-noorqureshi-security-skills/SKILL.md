---
name: tools-nuclei
description: >
  Operate nuclei for template-based vulnerability scanning at scale — severity/tag selection, bulk
  targets, rate limiting, proxying, JSON output, and safe custom templates. Load when you have live
  hosts from recon and need known-CVE/misconfig/exposure sweeps, or when scanner hits need
  validation. Signals: nuclei, -severity critical,high, nuclei-templates, -tags cve, "9000+
  templates", httpx | nuclei pipelines.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty, defense]
severity: info
mitre: [T1595.002]
tools: [nuclei, httpx, subfinder]
schema_version: 1
---

# nuclei vulnerability scanning

## When it applies
Recon has produced live in-scope hosts (`automation-recon-pipeline`) and you want fast coverage of
*known* issues — CVEs, exposed panels, misconfigurations — before spending manual time. Also the
right tool for re-checking a fixed finding across all hosts. For writing a template that codifies
your own finding, load `automation-nuclei-templates` (that skill is the deep guide; the essentials
are below).

## Why it works
nuclei runs declarative YAML templates (9000+ community templates, HTTP/DNS/TCP/SSL/file protocols)
against many targets in parallel with matchers on the response. You trade stealth for breadth: it's
fast and consistent, and loud.

## Method
1. **Install/update:** `apt install nuclei` (Kali) or
   `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest`; always
   `nuclei -update-templates` first.
2. **Scope the run — never full-template blindly:**
   ```bash
   nuclei -u https://target.com -severity critical,high        # single host, high signal
   nuclei -u https://target.com -tags cve,exposure             # by tag
   nuclei -l urls.txt -severity critical,high -o results.txt   # bulk targets
   nuclei -u https://target.com -t http/cves/2024/             # one template dir after fingerprinting
   ```
3. **Pipe from recon** (the standard pipeline):
   `subfinder -d target.com -silent | httpx -silent | nuclei -severity critical,high -o report.txt`
4. **Be a good citizen** (and stay under WAF/IDS thresholds):
   `-rate-limit 10 -bulk-size 5` to slow down; `-proxy http://127.0.0.1:8080` to route through Burp
   for visibility; `-exclude-tags dos,fuzz` to skip destructive/noisy checks; `-new-templates` for
   only-recently-added templates on a re-visit.
5. **Capture machine-readable output** for triage: `-json -o results.json`.
6. **Custom template essentials** (full guide: `automation-nuclei-templates`): `id` in
   `vendor-product-vulnerability` form; `info` with honest severity/tags; `http:` block with
   `{{BaseURL}}` paths; combine matchers with `condition: and` and match a signal *unique* to the
   vuln (a computed reflection like `49` from `{{7*7}}`, a specific error string) — never a bare
   200; add an `extractor` that pulls the proof. Validate with `-validate`, then against a
   known-vulnerable and a known-good host.

## Gotchas
- **A nuclei hit is a candidate, not a finding** — templates false-positive on version banners and
  lookalike strings. Manually reproduce every hit (`reporting-triage-validation`) before it goes in
  notes/findings; this is the #1 way automated scanning burns reporter credibility.
- **Full-template runs are loud and slow** — fingerprint first (`recon-techstack-fingerprinting`),
  then run only relevant tags/dirs.
- **Rate limiting cuts both ways** — too fast gets you WAF-banned (and can breach bug-bounty RoE on
  request rates); too slow on a big scope never finishes. Tune `-rate-limit`/`-bulk-size` to the RoE.
- **Windows naming collision** — the `httpx` command on Windows may resolve to the Python httpx
  library's CLI, not ProjectDiscovery's httpx; verify with `httpx -version` before piping.
- **Keep templates read-only** — anything that writes state or can DoS doesn't belong in a mass scan.

## Verify success
Each nuclei hit either reproduces manually with a concrete impact (and gets a findings entry) or is
recorded as a false positive with the reason. The scan config (severity/tags/rate) is logged so the
run is reproducible.

## References
ProjectDiscovery docs; nuclei-templates repo. Writing templates: `automation-nuclei-templates`.
Pipeline context: `automation-recon-pipeline`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
