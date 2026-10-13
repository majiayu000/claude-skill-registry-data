---
name: network-credential-cracking
description: >
  Crack hashes and handshakes captured during an engagement — identify the format, pick the right
  hashcat/john mode, and run wordlist + rules. Load when you've recovered a hash, ticket, or
  handshake and need the plaintext. Signals: bcrypt $2b$/PBKDF2/sha512crypt $6$, NTLM/NetNTLMv2,
  Kerberos $krb5tgs$/$krb5asrep$, WPA2 .22000, a leaked DB hash column, "what hashcat mode".
domain: network
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
mitre: [T1110.002, T1003]
cwe: [CWE-916, CWE-521]
tools: [hashcat, john, hashid, haiti]
schema_version: 1
---

# Credential & hash cracking

## When it applies
You've captured something crackable — an application DB hash, a Windows NTLM/NetNTLMv2 hash, a
Kerberos ticket (`ad-kerberoasting`), or a WPA2 handshake — and the plaintext unlocks the next step
(login, lateral movement, privesc). This is the offline counterpart to `network-password-spraying`.

## Why it works
Most stored credentials are one-way hashes, but users pick guessable passwords and many hash schemes
are fast to compute. Given the format, you brute the hash offline against a wordlist (optionally
mutated by rules) at millions/billions of guesses per second — no lockout, no network.

## Method
1. **Identify the format first — this is the whole game.** `hashid`/`haiti` on the sample, and look
   at the shape: `$2b$` = bcrypt, `$6$` = sha512crypt, `$argon2` = Argon2, `pbkdf2:sha256:...` =
   Werkzeug PBKDF2, `$krb5tgs$` = Kerberoast, `$krb5asrep$` = AS-REP. A wrong mode wastes hours.
2. **Map to the mode:**

   | Hash | hashcat `-m` |
   |------|:---:|
   | MD5 / SHA1 / SHA-256 (raw) | 0 / 100 / 1400 |
   | bcrypt (`$2*$`) | 3200 |
   | sha512crypt (`$6$`) | 1800 |
   | NTLM | 1000 |
   | NetNTLMv2 (responder capture) | 5600 |
   | Kerberoast TGS-REP | 13100 |
   | AS-REP roast | 18200 |
   | Werkzeug PBKDF2-SHA256 | 10900 |
   | WPA/WPA2 (hcxtools `.22000`) | 22000 |

3. **Extract a hash from a protected file** when the "hash" is a locked artifact, then crack that:
   `ssh2john id_rsa`, `zip2john f.zip`, `rar2john f.rar`, `keepass2john db.kdbx`,
   `office2john doc.docx`, `pdf2john f.pdf`, `pfx2john cert.pfx` → feed the output to john/hashcat.
   An encrypted SSH key, Office doc, KeePass DB, or ZIP found on a target is often the fastest win.
4. **Run wordlist + rules:** `hashcat -m <mode> hashes.txt rockyou.txt -r rules/best64.rule` (start
   with `best64`, escalate to `OneRuleToRuleThemAll`). Add target-specific words (company, seasons,
   app names) to the wordlist — context beats a bigger dictionary. Build one with `cewl <url> -m5`
   (words from the site), `crunch` (patterns), or `username-anarchy` (name → username permutations).
5. **Mask/brute** only when the keyspace is small or a pattern is known:
   `hashcat -m <mode> hashes.txt -a 3 '?u?l?l?l?l?d?d!'`.
6. **Reuse and pivot** — a cracked password is worth spraying elsewhere (`network-password-spraying`)
   and checking for reuse across accounts/services.

## Gotchas
- **Slow hashes (bcrypt/Argon2/sha512crypt)** — a good rule + targeted wordlist beats raw brute;
  don't waste days masking a bcrypt.
- **Format ambiguity** — a 32-hex could be raw MD5 or NTLM; try the likely context (Windows → NTLM).
- **Kerberoast/AS-REP** must be captured in hashcat's exact `$krb5*$` format — use Impacket/Rubeus
  output verbatim.
- **WPA2** is `-m 22000` now (the old `-m 2500 .hccapx` is deprecated) — convert with `hcxpcapngtool`.
- **Handle cracked creds like live secrets** — keep them in the git-ignored `engagements/` tree; the
  report shows *that* a weak password existed, not a wall of plaintext.

## Verify success
A recovered plaintext that authenticates against the intended service, or that demonstrably matches
the captured hash — the concrete lead for the next step.

## References
hashcat mode reference & rule sets; John the Ripper; `hcxtools`; MITRE ATT&CK T1110.002.
Online counterpart: `network-password-spraying`.
