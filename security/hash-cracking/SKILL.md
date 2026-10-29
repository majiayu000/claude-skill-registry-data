---
name: hash-cracking
description: Use when you need to recover plaintexts from password hashes on
  an authorized engagement, such as cracking NTLM hashes from a domain dump,
  testing password strength after extracting hashes in scope, or solving CTF
  crypto challenges. Covers hash identification, choosing between hashcat
  6.2.6 and John the Ripper 1.9.0-jumbo, the cost-ordered attack ladder
  (wordlist, rules, masks, brute force), Kerberos and NetNTLM specifics,
  potfile and session management, and knowing when to stop. Use when you
  hold hashes you are authorized to crack, or when password-attacks gave you
  a dump and now you need the plaintexts.
version: 1.0.0
domain: crypto
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [crypto-fundamentals, password-attacks]
tools:
  - name: hashcat
    version: 6.2.6
  - name: John the Ripper
    version: 1.9.0-jumbo
  - name: Python
    version: "3.12"
---

Hash cracking is guessing: you hash candidate passwords and compare
against the target hash until one matches. The skill is not in the
guessing but in the ordering, spending cheap guesses first, using the
right mode for the hash type, and stopping when the economics turn bad.
This skill is the operator's advanced workflow for hashcat and John the
Ripper on authorized engagements: dumps from in-scope systems, CTF
challenges, and password audits you were hired to run. It builds on the
identification basics in crypto-fundamentals and pairs with
password-attacks for getting the hashes in the first place. All cracking
targets hashes you have written permission to crack.

## Quick Workflow

1. Identify the hash type precisely: algorithm, salt format, and
   iteration count, before choosing a tool mode.
2. Normalize the input file: one hash per line, `user:hash` format where
   supported, no duplicates.
3. Crack in cost order: wordlist, wordlist plus rules, masks, then
   brute force, stopping when returns diminish.
4. Tune for the hardware: benchmark first, set workloads that fit the
   engagement window.
5. Manage sessions and potfiles so cracked hashes persist and reruns
   skip solved work.
6. Handle special formats (NTLM, Kerberos, NetNTLMv2, bcrypt) with
   their specific modes and considerations.
7. Report cracked credentials with the method that cracked each one,
   and purge the plaintexts per the engagement rules.

## 1. Identify the hash type

Wrong mode means zero cracks and wasted hours. Identify from structure:

```bash
# Length and alphabet triage
head -5 hashes.txt | awk '{print length, $0}'

# Common fingerprints:
# 32 hex chars      -> MD5 (0) or NTLM (1000); context decides
# 40 hex chars      -> SHA-1 (100)
# 64 hex chars      -> SHA-256 (1400) or raw SHA-256 crypt is $5$
# $2b$/$2y$ prefix  -> bcrypt (3200)
# $6$ prefix        -> sha512crypt (1800)
# $krb5tgs$...      -> Kerberos TGS-REP (13100)
# $krb5asrep$...    -> Kerberos AS-REP (18200)
# netntlmv2 format  -> NetNTLMv2 (5600)

# hashid for automated identification
hashid -m '$2b$12$KIXxQG8b2aV8KxQ8b2aV8KO'
```

```bash
# hashcat help lists every mode number
hashcat --help | grep -i -E 'ntlm|bcrypt|sha512crypt' | head
```

When in doubt between MD5 and NTLM (both 32 hex), test both modes on a
small sample; the wrong one cracks nothing and the right one often
cracks fast. Context is the tiebreaker: Windows SAM or NTDS output is
NTLM, web application dumps are usually MD5 or bcrypt.

## 2. The cost-ordered attack ladder

Always climb in this order. Each step costs roughly ten times the
previous one.

```bash
# Step 1: straight wordlist (fast hashes: minutes; slow: hours)
hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# Step 2: wordlist plus rules (mutations: leetspeak, appends, case)
hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule

# Heavier rule sets when best64 stalls
hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/d3ad0ne.rule

# Step 3: mask attack (known structure, e.g. 8-char lowercase + 2 digits)
hashcat -m 1000 -a 3 hashes.txt '?l?l?l?l?l?l?l?l?d?d'

# Step 4: full brute force (last resort, only for fast hashes)
hashcat -m 1000 -a 3 hashes.txt '?a?a?a?a?a?a?a?a'
```

John the Ripper equivalents:

```bash
# Wordlist mode
john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT hashes.txt

# Rules (John's wordlist rules are strong)
john --wordlist=/usr/share/wordlists/rockyou.txt --rules --format=NT hashes.txt

# Incremental (brute force) mode
john --incremental --format=NT hashes.txt

# Show cracked passwords
john --show --format=NT hashes.txt
```

Move up the ladder only when the current step exhausts. Do not start
with brute force on bcrypt; the math says you will retire first.

## 3. Benchmark and tune

```bash
# Benchmark the exact mode on your hardware before committing hours
hashcat -m 1000 -b
hashcat -m 3200 -b   # bcrypt: expect thousands, not billions

# Typical speeds (single modern GPU, rough):
# NTLM:    tens of GH/s  -> full keyspace attacks are feasible
# MD5:     tens of GH/s  -> same
# bcrypt:  tens of kH/s  -> wordlist only, be selective
# sha512crypt: hundreds of kH/s -> wordlist plus light rules
```

Tune for the engagement window:

```bash
# Limit runtime: --runtime=3600 stops after one hour
hashcat -m 1000 -a 0 hashes.txt rockyou.txt --runtime=3600

# Restore interrupted sessions instead of restarting
hashcat --session=clientA --restore
# (hashcat auto-saves; --restore resumes the named session)

# Distribute across GPUs
hashcat -m 1000 -a 0 hashes.txt rockyou.txt -D 1,2 --force
```

Estimate before brute force: keyspace divided by speed equals seconds.
If the answer exceeds the engagement, do not start; report the math.

```bash
# Keyspace estimate: 8 chars of ?a (95) = 95^8
python3 -c "print(95**8 / 50e9 / 3600, 'hours at 50 GH/s')"
```

## 4. Potfile and session hygiene

```bash
# Cracked hashes live in the potfile; reuse across runs automatically
# Disable potfile only for clean benchmarking
hashcat -m 1000 -a 0 hashes.txt rockyou.txt --potfile-disable

# Show only newly cracked in this run
hashcat -m 1000 hashes.txt --show

# Merge and deduplicate hash lists before starting
sort -u hashes_raw.txt > hashes.txt
wc -l hashes.txt
```

Keep one potfile per engagement, never mix client data. At engagement
end, follow the rules of engagement on data destruction: cracked
plaintexts are sensitive, and the report should describe the method
and count, not republish every password.

## 5. Special formats

NTLM (mode 1000) is the workhorse of Windows engagements:

```bash
# NTDS dump format: user:rid:lm:ntlm:::
# Extract the NTLM field for hashcat
cut -d: -f4 ntds.txt > ntlm.txt
hashcat -m 1000 -a 0 ntlm.txt rockyou.txt -r rules/best64.rule

# Keep user:hash mapping for reporting
hashcat -m 1000 --username -a 0 ntds_users.txt rockyou.txt
```

Kerberos tickets from in-scope captures:

```bash
# TGS-REP roast (mode 13100), AS-REP roast (mode 18200)
hashcat -m 13100 -a 0 tgs.txt rockyou.txt
hashcat -m 18200 -a 0 asrep.txt rockyou.txt
```

NetNTLMv2 from responder captures (only on authorized tests):

```bash
# Mode 5600, hash format: user::domain:challenge:response...
hashcat -m 5600 -a 0 netntlmv2.txt rockyou.txt
```

Slow hashes (bcrypt 3200, sha512crypt 1800, PBKDF2): wordlist only,
small curated lists, and consider targeted masks from password policy
hints. A policy requiring 12 characters with symbols means masks, not
rockyou.

## 6. Building better wordlists

The default rockyou cracks the easy half. Targeted lists crack the
rest:

```bash
# Company-specific mutations: combine names, years, seasons
cat company_words.txt | while read w; do
  echo "$w"; echo "${w}2024"; echo "${w}2025"; echo "${w}!"
done > targeted.txt

# CeWL-style spidering is for web passwords; for audits use HR data:
# department names, office locations, product names (all authorized)

# Merge and deduplicate
cat rockyou.txt targeted.txt | sort -u > combined.txt

# John can generate candidates from cracked patterns
john --wordlist=combined.txt --rules --stdout | head -5
```

Rules beat bigger wordlists: `best64` and `d3ad0ne` encode the
mutations humans actually use (append year, capitalize first, leet
substitutions). Custom rule files for the client's language and
keyboard layout outperform generic ones.

## 7. Knowing when to stop

Stop conditions, in order of importance:

1. The engagement window ends. Cracking does not justify missing the
   report deadline.
2. The remaining hashes are slow types (bcrypt cost 12+) and the
   wordlist plus rules are exhausted. Further effort has near-zero
   expected return.
3. You have cracked enough to prove the point. For a password audit,
   30 percent cracked with method notes beats 35 percent with no
   report.
4. The math says no: brute force estimate exceeds available time by
   orders of magnitude.

Report format per hash type: total hashes, cracked count, method that
cracked each batch, and the policy failures the cracks demonstrate
(no complexity, reused passwords, seasonal patterns).

## Edge cases

- Hashcat reports "no devices found". Install the right OpenCL or
  CUDA runtime, or fall back to CPU with `--force` (slow but works).
- The hash file has salts in a nonstandard layout. Write a small
  Python normalizer to the exact `hash:salt` format the mode
  expects; one malformed line can abort the whole run.
- John guesses the wrong format. Force it with `--format=` and
  verify with `--show` on a known test hash first.
- Cracks show as hex blobs, not passwords. The password contained
  non-UTF8 bytes; decode with `--hex-charset` awareness or inspect
  the potfile raw.
- Duplicate effort across runs. Always `--restore` sessions and keep
  the potfile; hashcat skips already-cracked hashes automatically.
- The client used pepper (secret salt). Cracking is infeasible
  without it; document the control as effective and move on.

## Escalation

- Wordlist plus rules stalls on fast hashes: build targeted masks
  from the password policy (length, character classes) and from
  cracked samples (common prefixes in this organization).
- One GPU is too slow: split the keyspace across machines with
  `--keyspace` and `--skip`/`--limit` ranges, or rent cloud GPUs
  within the engagement budget and with client approval.
- The hash type is exotic with no hashcat mode: check John's jumbo
  formats (it covers hundreds), then write a custom cracker only if
  the hash count justifies the development time.
- You need the plaintext but cracking is hopeless: pivot. Password
  reuse from other cracked sets, default credentials, and password
  reset flows often beat cryptography.

## Detection and defender view

Defenders detect cracking indirectly: they see the hash dump leaving
(the real incident), not the cracking itself, which happens offline.
The durable defenses are slow, salted hashes (bcrypt, scrypt, Argon2
with appropriate cost), unique salts per user, pepper for high-value
systems, and breach monitoring for dumped hashes. Password policies
should enforce length over complexity and check new passwords against
known-breach lists. For the audit report, every cracked password maps
to a policy gap; the fix list is policy and hashing upgrades, not
longer blocklists.

## Key references

- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): fast
  hashes for passwords (MD5, SHA-1).
- CWE-916 (Use of Password Hash With Insufficient Computational
  Effort).
- CWE-759 (Use of a One-Way Hash without a Salt).
- CWE-798 (Use of Hard-coded Credentials): when the dump reveals
  defaults.
- hashcat wiki and example hashes: https://hashcat.net/wiki/
- John the Ripper documentation: https://www.openwall.com/john/doc/
- OWASP Password Storage Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
