---
name: tools-hashcat
description: >
  Crack password hashes offline with hashcat (GPU) and John the Ripper (CPU) — hash-mode selection,
  attack modes (straight/mask/combinator/rules), the -m type table, *2john extractors, and potfile
  discipline. Load when loot includes hashes: NTLM/NetNTLMv2 dumps, Kerberos TGS (kerberoast), JWT
  secrets, /etc/shadow, zip/rar/ssh key passwords. Signals: hashcat -m, rockyou, best64.rule,
  $6$ hashes, unshadow, john --show, mask ?a?a?a.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty, defense]
severity: medium
mitre: [T1110.002]
tools: [hashcat, john-the-ripper]
schema_version: 1
---

# hashcat & John hash cracking

## When it applies
You hold in-scope credential material (`tradecraft-scope-roe`) that must be proven crackable: NTLM
dumps, NetNTLMv2 captures (`network-credential-cracking`), Kerberos TGS tickets (`ad-kerberoasting`),
JWT HMAC secrets (`web-auth-jwt`), `/etc/shadow`, or password-protected archives/keys. In defense
mode, the same workflow audits whether org passwords survive a real cracking run.

## Why it works
Offline cracking has no lockout and no rate limit — speed is set by hash algorithm and hardware.
hashcat drives GPUs (billions of guesses/sec on fast hashes like NTLM); John the Ripper is the
flexible CPU fallback with extractors (`*2john`) that turn encrypted files into crackable hashes.
Rules and masks exploit how humans actually pick passwords, so a small wordlist + mutation beats
blind brute force.

## Method
1. **Identify the hash before choosing a mode** — wrong `-m` wastes the whole run. Use `hashid` /
   `hashcat --identify hash.txt`, or match the format against the table:
   ```
   -m 0     MD5            -m 1000  NTLM           -m 5600   NetNTLMv2
   -m 100   SHA1           -m 1800  sha512crypt    -m 13100  Kerberos TGS (kerberoast)
   -m 1400  SHA256         -m 3200  bcrypt         -m 16500  JWT (HS256)
   -m 1700  SHA512
   ```
2. **Straight dictionary first** (attack mode `-a 0`):
   `hashcat -m 1000 ntlm.txt /usr/share/wordlists/rockyou.txt`
   (Kali: `gzip -d /usr/share/wordlists/rockyou.txt.gz` once — ~14M words.)
3. **Add rules** — mutations (leet, append digits, capitalize) crack what plain lists miss:
   `hashcat -m 0 hash.txt wordlist.txt -r rules/best64.rule`
4. **Combinator for paired words:** `hashcat -m 0 -a 1 hash.txt words1.txt words2.txt`.
5. **Mask attack when you know the policy** (attack mode `-a 3`):
   `hashcat -m 0 -a 3 hash.txt ?u?l?l?l?l?d?d?d` (e.g. "5 letters, capital first, 3 digits").
   Charsets: `?l` lower, `?u` upper, `?d` digits, `?s` symbols, `?a` all, `?b` 0x00–0xff.
6. **Read results:** `hashcat -m 0 hash.txt --show` (cracked plaintexts come from the potfile —
   rerunning the attack skips already-cracked hashes).
7. **John path (CPU, exotic formats):**
   ```bash
   unshadow /etc/passwd /etc/shadow > mypasswd && john --wordlist=rockyou.txt mypasswd
   zip2john protected.zip > zip.hash && john --wordlist=rockyou.txt zip.hash
   rar2john protected.rar > rar.hash     # same pattern
   ssh2john id_rsa > ssh.hash            # SSH private-key passphrase
   john --format=raw-md5 --wordlist=rockyou.txt hash.txt   # force a format
   john --incremental hash.txt           # pure brute force, last resort
   john --show hash.txt
   ```
8. **Sanity-check hardware:** `hashcat -b` benchmarks; if bcrypt (-m 3200) shows tiny rates, that is
   the algorithm working as designed — switch strategy (better wordlist/rules), not patience.

## Gotchas
- **Slow hashes are meant to be slow** — bcrypt/scrypt/argon make masks above ~7 chars futile;
  invest in wordlist quality (target-specific lists, breached-corpus lists like the CrackStation
  15 GB dictionary) instead of length.
- **GPU/driver problems are environmental** — no OpenCL/CUDA device = fix drivers or fall back to
  John; do not grind a mask attack on CPU.
- **Potfile confusion** — `--show` reads the potfile, not the hash file; a "cracked" result that
  never prints usually means you're `--show`-ing the wrong `-m` mode.
- **Salted vs unsalted** — mode choice must match (raw MD5 `-m 0` vs md5crypt `-m 500`); a correct
  password list against the wrong mode cracks nothing and looks like "strong passwords".
- **Cracked =/= authorized** — only crack hashes from in-scope systems; recovered credentials go in
  `loot/`, never in the report body (report the *fact* and rate of cracking).

## Verify success
`--show` output maps hashes to plaintexts for a stated percentage of the set, and you can name the
mode, wordlist/rules/mask, and runtime — reproducible evidence for the finding ("X% of domain
passwords cracked in N minutes with a commodity GPU").

## References
hashcat example-hashes page (mode identification); hashcat wiki (rules/masks); John jumbo docs.
Where hashes come from: `network-credential-cracking`, `ad-kerberoasting`, `web-auth-jwt`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
