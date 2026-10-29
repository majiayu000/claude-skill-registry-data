---
name: john
description: "Crack hashes offline on CPU with John the Ripper: wordlist, rules, single and incremental modes, sessions and the pot file. Use when a hash dump must be turned into plaintext and no GPU is available, or when a hash format only John understands is in play. Not for online guessing against a service (use hydra) and not for GPU-accelerated mask attacks (use hashcat)."
---

# John the Ripper

John is an offline cracker: it reads a hash file, generates candidates, and writes every match to a pot file. It never touches the target, so it is invisible to the victim and limited only by local CPU time.

This host runs **jumbo**: `/opt/john/jumbo/john` reports `1.9.0-jumbo-1+bleeding-5184bc0b8c`, AVX2 with OpenMP, and `/usr/local/bin/john` is a wrapper that execs it so the config and rule files resolve. Formats include `NT`, `netntlmv2`, `krb5tgs`, `Raw-MD5`, `bcrypt` and `sha512crypt`; check with `--list=formats` rather than assuming. The distro's core build is still at `/usr/sbin/john` — it loses on PATH order, and it should stay unused.

`hashcat` v6.2.6 is also installed and works on this host through the pocl CPU backend (`hashcat -b -m 0` ≈ 44 MH/s MD5). John is the better choice for format coverage and rule quality; hashcat is the better choice for masks and raw throughput on a large wordlist.

## When to use

| Goal | Mode | Hash shape |
| --- | --- | --- |
| Linux `/etc/shadow` ($1$, $5$, $6$) | `--format=crypt --wordlist` | `user:$6$salt$hash` |
| Legacy LM (Windows pre-Vista, some caches) | `--format=LM --wordlist` | 32 hex chars |
| Quick win from usernames and GECOS fields | `--single` | full passwd-format file |
| Dictionary plus mangling | `--wordlist --rules` | any supported format |
| Exhaustive short passwords | `--incremental=MODE` | any supported format |
| Resume an interrupted run | `--restore` / `--session` | any |
| Show what is already cracked | `--show` | same file and format |

Use hashcat when the hash type is unsupported here and a GPU exists. Use hydra when the password has to be guessed against a live service.

## Prerequisites

- `john` on PATH (`/usr/sbin/john`). `john --version` is **not** a valid option in this build; version appears in the banner or `--test`.
- Wordlists: `/opt/wordlists/rockyou.txt` (14M lines), `pass-top1m.txt`, `users-top.txt`.
- A hash file in `user:hash` form. John also accepts bare hashes and full passwd/shadow lines.
- Patience: 2 CPU cores, no GPU. Benchmarks below are from this host.

## Core invocations

```sh
# 1. Confirm the build and the available options (no --version flag here)
john 2>&1 | head -5

# 2. Benchmark what this CPU can actually do before choosing an attack
john --test=3

# 3. Wordlist attack against md5crypt
john --format=md5crypt --wordlist=/opt/wordlists/rockyou.txt hashes.txt

# 4. Same, with mangling rules (this build applies 50 rules per word)
john --format=md5crypt --wordlist=/opt/wordlists/rockyou.txt --rules hashes.txt

# 5. Generic crypt(3): libc shadow hashes when the format is ambiguous
john --format=crypt --wordlist=/opt/wordlists/rockyou.txt shadow.txt

# 6. Legacy LM hashes
john --format=LM --wordlist=/opt/wordlists/rockyou.txt lm.txt

# 7. Single mode against an exported passwd file: tries login, GECOS and home dir
john --single passwd.txt

# 8. Incremental (brute force) limited to digits; modes come from john.conf
john --format=md5crypt --incremental=Digits hashes.txt

# 9. Target one account only, useful when a hash file holds many users
john --format=crypt --users=alice --wordlist=/opt/wordlists/rockyou.txt shadow.txt

# 10. Named session, left running in a background terminal, resumed later
john --session=eng01 --format=md5crypt --wordlist=/opt/wordlists/rockyou.txt hashes.txt
john --restore=eng01

# 11. Split the work across both cores without a GPU
john --format=md5crypt --fork=2 --wordlist=/opt/wordlists/rockyou.txt hashes.txt

# 12. Preview what rules would generate before wasting CPU time
john --wordlist=/opt/wordlists/users-top.txt --rules --stdout | head -40

# 13. Show every crack already recorded in the pot file
john --show --format=md5crypt hashes.txt

# 14. Only attack salts that cover many hashes (fastest first)
john --format=md5crypt --salts=5 --wordlist=/opt/wordlists/rockyou.txt hashes.txt

# 15. Filter a shared dump down to accounts with a real shell
john --format=crypt --shells=/bin/bash shadow.txt
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `--format=NAME` | force hash type | must be a compiled format; wrong name fails immediately |
| `--wordlist=FILE` | dictionary source | `--stdin` also works |
| `--rules` | mangling rules from `[List.Rules:Wordlist]` | 50 candidates per word in this build |
| `--single` | login/GECOS-derived candidates | needs passwd-format input, bare hashes give nothing |
| `--incremental[=MODE]` | brute force | modes in `/etc/john/john.conf`: ASCII, Alnum, Alpha, Digits, Lower, Upper, LowerNum, UpperNum, LM_ASCII |
| `--external=MODE` | custom filter/generator | defined in john.conf |
| `--stdout[=LENGTH]` | print candidates only | zero-risk way to test a rule set |
| `--show` | list cracked entries from the pot | requires the same `--format` |
| `--status[=NAME]` | progress of a running session | fails when no session exists |
| `--session=NAME` / `--restore[=NAME]` | name and resume | state in `~/.john/john.rec` |
| `--fork=N` | N processes | use 2 here |
| `--node=MIN-MAX/TOTAL` | split keyspace across machines | combine with `--fork` |
| `--users=` / `--groups=` / `--shells=` / `--salts=` | select targets | `-` prefix excludes |
| `--save-memory=LEVEL` | trade speed for RAM | levels 1-3 |

## Workflow

1. **Identify the hash type from its prefix**, not from the source: `$1$` md5crypt, `$2a$/$2b$/$2y$` bcrypt, `$6$` sha512crypt, 32 hex LM.
2. **Check the format exists**: `john --list=formats | tr ',' '\n' | grep -i nt`. Jumbo covers NTLM, NetNTLMv1/v2, Kerberos TGS/AS-REP and the usual web hashes.
3. **Normalise the file** to `user:hash`, one per line. Strip comments and blank lines.
4. **Run `--single` first** on passwd-format dumps; it is instant and sometimes free.
5. **Then wordlist + rules** with the biggest realistic list. Stop early if the engagement only needs a foothold.
6. **Then incremental** for short passwords, with an explicit mode and a length cap.
7. **Record results** with `--show`; hand plaintext back into the credential graph.
8. **Clean up**: the pot file is plaintext at rest.

## OPSEC and telemetry

- No network traffic and no target telemetry: cracking happens on your host. The only upstream artefacts are how you obtained the hashes (SAM read, DCSync, `/etc/shadow` read).
- `~/.john/john.pot` stores `hash:plaintext` in mode 0600. Delete it after the engagement; treat it as a credential store.
- `~/.john/john.log` and `john.rec` record session names, files and rates. They are evidence of intent.
- Measured on this host with jumbo (`john --test=2`): NT 33,250 kH/s, Raw-MD5 27,702 kH/s, bcrypt 849 c/s, sha512crypt 785 c/s. NTLM and MD5-era dumps fall quickly against rockyou; bcrypt and sha512crypt need targeted wordlists and rules, not brute force.
- Long runs consume both cores; do not run them while a scan needs the box.
- Rules that append years or `!` produce correct-looking candidates but also huge volumes against rate-limited services - irrelevant offline, relevant if you then spray online.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unknown ciphertext format name requested` | typo, or a format jumbo was built without | `john --list=formats | tr ',' '\n' | grep -i <name>`; names are case-insensitive but must match the list |
| `fopen: /usr/local/bin/john.conf` | the binary was invoked through a symlink, so it looked for its config beside the link | use the wrapper at `/usr/local/bin/john`, or set `JOHN=/opt/john/jumbo` |
| `No password hashes loaded` | wrong file shape or wrong `--format` | keep `user:hash`; retry without `--format` to see what John detects |
| `fopen: /root/.john/john.rec: No such file or directory` | `--status` with no session | only valid while a session runs |
| Run finishes with `0g` and no error | hash already in the pot, or wordlist exhausted | `--show`; check the pot; try `--rules` or a bigger list |
| `Warning: detected hash type X, but the string is also recognized as Y` | ambiguous hash | force the intended `--format` |
| Very slow, low c/s | bcrypt or sha512crypt cost | switch strategy: rules on a small targeted list, or move to a GPU host |
| `--single` finds nothing in seconds | bare hashes have no GECOS data | feed a real passwd-format file |
| Incremental ignores expected lengths | `MaxLen` reduced for the hash type | set an explicit mode and keep passwords short |

## Verification

```sh
john 2>&1 | head -2                    # expect: John the Ripper password cracker, version 1.9.0
john --test=1 | head -8                # expect: Benchmarking: descrypt ... DONE
# end-to-end sanity check with a throwaway hash ($1$ below is openssl passwd -1 -salt abcd test)
printf 'alice:$1$abcd$T2SbKcrpFB8biuNpvb0F4.\n' > /tmp/h.txt
printf 'test\n' > /tmp/w.txt
john --format=md5crypt --wordlist=/tmp/w.txt /tmp/h.txt    # expect: test (alice) and 1g
john --show --format=md5crypt /tmp/h.txt                    # expect: alice:test / 1 password hash cracked, 0 left
ls -l ~/.john/john.pot                                      # expect: -rw------- with hash:plaintext lines
```

## Related skills

- [hashcat](../hashcat/SKILL.md) for mask attacks and raw throughput
- [hydra](../hydra/SKILL.md) for online guessing when no hash is available
- [netexec](../netexec/SKILL.md) for obtaining the hashes in the first place
- [metasploit](../metasploit/SKILL.md) whose `creds` table carries a JtR format column
- [toolchain-router](../toolchain-router/SKILL.md) to choose between John and hashcat
