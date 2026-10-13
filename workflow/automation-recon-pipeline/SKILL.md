---
name: automation-recon-pipeline
description: >
  Chain recon tools into a repeatable, resumable pipeline for continuous bug-bounty coverage.
  Load on "automate recon", "recon pipeline", monitoring many programs, or scaling subdomain→
  live→scan. Signals: wildcard scope at scale, wanting scheduled/continuous discovery.
domain: automation
type: technique
stability: learning
modes: [bugbounty]
severity: info
mitre: [T1595]
tools: [subfinder, dnsx, httpx, naabu, nuclei, notify, anew]
schema_version: 1
---

# Recon automation pipeline

## When it applies
You track one or more wildcard programs and want discovery to run repeatably (and on a
schedule), surfacing only *new* assets/findings instead of re-reviewing everything.

## Why it works
Recon is a directed flow: roots → subdomains → resolve → live → ports → nuclei. Wiring the
ProjectDiscovery tools together (each reads/writes lines) makes it composable, and diffing
against last run (`anew`) turns it into continuous monitoring that alerts on change.

## Method
1. **Pipeline (each stage feeds the next):**
   ```
   subfinder -dL roots.txt -all -silent \
     | dnsx -silent -a -resp-only \
     | httpx -silent -sc -title -tech-detect \
     | tee live.txt \
     | nuclei -silent -severity low,medium,high,critical
   ```
2. **Diff for "only new"**: pipe each stage through `anew subs.txt` / `anew live.txt` so reruns
   emit only newly-seen lines — the basis of continuous monitoring.
3. **Notify**: pipe results to `notify` (Slack/Discord/Telegram) so new hosts/findings alert you.
4. **Schedule** with cron/systemd-timer/GitHub Actions; persist state files per program so runs resume.
5. **Keep templates current**: `nuclei -update-templates` before each run.

## Gotchas
- Stay in scope: feed only in-scope roots, filter out-of-scope hosts before scanning.
- Respect rate limits (`-rl`, `-c`) and program automation rules — don't hammer.
- De-dupe wildcard DNS (`dnsx` wildcard filtering) or you'll alert on noise forever.

## Verify success
A rerun surfaces only newly-appeared assets/findings and notifies you — hands-off continuous coverage.

## References
ProjectDiscovery pipeline docs; TomNomNom `anew`; nuclei templates.
