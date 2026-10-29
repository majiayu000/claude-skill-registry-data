---
name: password-attacks
description: Use when cracking password hashes or auditing password strength
  on an authorized engagement. Covers hash identification, hashcat 6.2.6 and
  John the Ripper 1.9.0-jumbo-1 workflows, wordlist strategy, rule-based
  mutation, mask and hybrid attacks, and interpreting results for the report.
  Use when you recovered hashes from a database dump, a SAM file, /etc/shadow,
  or an application backup, or when the client asked for a password audit.
version: 1.0.0
domain: auth
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [auth-attacks]
tools:
  - name: hashcat
    version: 6.2.6
  - name: John the Ripper
    version: 1.9.0-jumbo
  - name: Python
    version: "3.12"
---

Password attacks turn recovered hashes back into plaintext to prove what an
attacker could do with a stolen database. This skill covers identifying the
hash type, running efficient cracking campaigns with hashcat and John the
Ripper, building wordlist and rule strategies, and using mask attacks for
known patterns. Only crack hashes you are authorized to handle, keep them
on encrypted storage, and delete them when the engagement ends.

## Quick Workflow

1. Collect hashes into a clean file, one per line, with usernames split
   out when present.
2. Identify the hash type with hashid and manual inspection before
   choosing a mode.
3. Run a fast dictionary attack with rules first; it wins most often.
4. Follow with targeted masks for known password policies.
5. Use hybrid attacks (wordlist plus mask) for common suffix patterns.
6. Finish with full brute force only for short or weak hash types.
7. Track cracked pairs, restore sessions, and stop when the agreed time
   or budget is spent.
8. Report statistics (cracked count, time, weakest patterns), never the
   full plaintext list beyond what the client agreed to receive.

## 1. Hash identification

Never guess the mode. Identify first, because the wrong mode wastes the
whole run.

```bash
# Install hashid from source repos if missing, then identify
hashid -m '$2y$12$KIXxQG8HcVXJxKjKZQZQZuXxQG8HcVXJxKjKZQZQZu'

# Manual checks that matter
head -5 /tmp/hashes.txt
awk -F: '{print length($NF)}' /tmp/hashes.txt | sort | uniq -c
# 32 hex chars  -> MD5 (-m 0) or NTLM (-m 1000)
# 40 hex chars  -> SHA1 (-m 100)
# 60 chars $2y$ -> bcrypt (-m 3200)
# $6$...        -> sha512crypt (-m 1800)
# $y$...        -> yescrypt: check your hashcat build with
#                  hashcat --help | grep -i yescrypt; if the mode is missing,
#                  use John the Ripper which handles yescrypt natively.
```

# Normalize shadow entries: cut keeps the full $id$salt$hash field intact
cut -d: -f2 /tmp/shadow.txt > /tmp/hashes_clean.txt

# Quick benchmark to pick a sane workload for your GPU
hashcat -b -m 1000
```

## 2. hashcat workflows

Dictionary with rules is the highest value first step.

```bash
# Straight dictionary with best64 rules
hashcat -m 1000 -a 0 /tmp/ntlm.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule

# Bigger rule sets for a second pass
hashcat -m 1000 -a 0 /tmp/ntlm.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/d3ad0ne.rule

# Show cracked results
hashcat -m 1000 /tmp/ntlm.txt --show

# Save and restore long sessions
hashcat -m 1800 -a 0 /tmp/shadow_hashes.txt rockyou.txt \
  --session=clientA --restore
hashcat --session=clientA --restore
```

Rule strategy: start with `best64.rule`, then `d3ad0ne.rule`, then a
custom rule file with the client's observed patterns (company name plus
digits, keyboard walks, season plus year). Write custom rules in a plain
text file, one rule per line, and test them on a tiny hash set first.

```bash
# Custom rules example (/tmp/custom.rule)
# append 2024-2026, capitalize first letter, leetspeak basic
$2 $0 $2 $4
$2 $0 $2 $5
$2 $0 $2 $6
c
sa@
```

## 3. Mask attacks

Use masks when the password policy is known (for example 8 characters,
uppercase first, digits last).

```bash
# ?l lower, ?u upper, ?d digit, ?s special, ?a all
# Policy: 1 upper + 7 lower (?u?l?l?l?l?l?l?l)
hashcat -m 1000 -a 3 /tmp/ntlm.txt ?u?l?l?l?l?l?l?l

# Incremental: grow the mask from 4 to 8 characters
hashcat -m 1000 -a 3 /tmp/ntlm.txt ?a?a?a?a --increment --increment-min=4

# Custom charset for a known pattern (company prefix + 4 digits)
hashcat -m 1000 -a 3 /tmp/ntlm.txt -1 '?d' 'Acme?1?1?1?1'
```

Keep masks tight: every extra `?a` position multiplies the keyspace by 95.
Estimate the runtime with `--keyspace` style dry math or a short benchmark
before committing hours.

## 4. Hybrid attacks

Combine a wordlist with a mask for the most common real pattern: a word
plus a digit suffix.

```bash
# Wordlist base + up to 4 digits appended
hashcat -m 1000 -a 6 /tmp/ntlm.txt rockyou.txt ?d?d?d?d

# Mask prefix + wordlist appended (year-first policies)
hashcat -m 1000 -a 7 /tmp/ntlm.txt ?d?d?d?d rockyou.txt
```

Hybrid attacks beat pure brute force for human passwords and cost far
less GPU time than full masks.

## 5. John the Ripper workflows

John is strong for slow Unix hashes and for its wordlist modes.

```bash
# Auto-detect format from a shadow-style file
john --wordlist=/usr/share/wordlists/rockyou.txt /tmp/shadow.txt

# Force a format when detection is unsure
john --format=sha512crypt --wordlist=rockyou.txt /tmp/shadow.txt

# Show cracked passwords
john --show /tmp/shadow.txt

# Incremental mode for a targeted charset and length
john --incremental=digits --max-length=6 /tmp/pins.txt

# Custom rules in john.conf style, or use --rules with wordlist mode
john --wordlist=rockyou.txt --rules /tmp/shadow.txt
```

Use John for `sha512crypt`, `bcrypt`, and `yescrypt` when hashcat lacks
the mode on your build, and use hashcat for fast hashes (NTLM, MD5) where
GPU speed matters most.

## 6. Wordlist strategy

Build the list in layers, cheapest wins first.

```bash
# Layer 1: small targeted list (company, product, city names + seasons)
cat /tmp/targeted.txt | head

# Layer 2: rockyou.txt (14M, the classic baseline)
wc -l /usr/share/wordlists/rockyou.txt

# Layer 3: large collections (SecLists, CrackStation) with rules

# Generate a targeted list from client keywords with simple mutations
python3 - <<'EOF'
base = ["acme", "spring", "summer", "qwerty"]
years = ["2023", "2024", "2025", "2026"]
out = set()
for b in base:
    out.add(b)
    out.add(b.capitalize())
    for y in years:
        out.add(b + y)
        out.add(b.capitalize() + y)
        out.add(b + "@" + y[-2:])
print("\n".join(sorted(out)))
EOF
```

Deduplicate and sort large lists before use (`sort -u`), and never feed
crack output wordlists back into the same engagement without the client's
permission to retain derived data.

## Edge cases

- Hash file mixes formats. Split by length and prefix into separate files
  and crack each with its own mode.
- Salted hashes need the salt in hashcat's expected format
  (`hash:salt` for many modes); check `--help` for the exact layout.
- bcrypt/yescrypt are slow by design. Dictionary plus rules only, tiny
  targeted lists, and set expectations: full brute force is infeasible.
- The GPU runs out of memory on huge rule sets. Reduce with `-O`
  (optimized kernels) and smaller wordlists, or move slow hashes to CPU
  with John.
- Hashcat reports "no hashes loaded". The file has whitespace, BOM, or
  Windows line endings; clean with `dos2unix` or `tr -d '\r'`.
- Cracked count stalls. Check `--status` for temperature throttling and
  verify the mask keyspace math before extending the run.

## Escalation

- Dictionary plus rules fails: build a custom wordlist from the client's
  website text (cewl-style scraping of public pages only, in scope).
- Masks are too slow: narrow with policy intelligence from the
  registration page (minimum length, required classes).
- One hash type resists: convert formats (for example NTLM to
  NetNTLMv2 handling differs) and confirm the mode with a known
  password/hash pair you generate yourself.
- Time budget is nearly spent: prioritize administrator and service
  accounts, crack those first, and report partial statistics honestly.

## Detection and defender view

Defenders do not see offline cracking at all, which is why hash theft is
so serious; they see the theft (unusual database exports, SAM access,
backup downloads). The defense is making hashes hard to crack: strong
adaptive hashing (bcrypt cost 12+, Argon2id, scrypt), unique salts,
peppering secrets in an HSM or vault, and password policies that block
the top breached passwords. Monitor for mass hash disclosure and rotate
all credentials after any suspected dump.

## Key references

- MITRE ATT&CK T1110.002 (Brute Force: Password Cracking).
- MITRE ATT&CK T1003.002 (OS Credential Dumping: Security Account
  Manager) and T1003.008 (/etc/passwd and /etc/shadow): where hashes
  come from.
- CWE-916 (Use of Password Hash With Insufficient Computational Effort).
- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): MD5/SHA1
  for passwords.
- CWE-256 (Plaintext Storage of a Password).
- hashcat 6.2.6 docs: https://hashcat.net/wiki/
- John the Ripper docs: https://www.openwall.com/john/doc/
