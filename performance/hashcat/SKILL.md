---
name: hashcat
description: "Crack hashes offline with hashcat: choose the right -m mode, run dictionary, rule, mask and hybrid attacks, and manage the potfile. Use when NetNTLM, Kerberos or application hashes have been captured and need cracking before being reported as uncracked. Not for on-host credential dumping (use netexec) and not for protocol capture (use responder)."
---

# hashcat

hashcat is the reference GPU cracker: one binary, one mode number per hash format, five useful attack modes, and a potfile that makes repeated runs cheap. On this host it is `/usr/bin/hashcat` version 6.2.6 on a 2 vCPU cloud instance: no GPU, but a working pocl CPU backend, so it does crack — at CPU speed. Read the throughput note under Prerequisites before promising anyone a crack time.

## When to use

| Goal | Mode | Command shape |
| --- | --- | --- |
| Crack captured NetNTLMv2 | `-a 0 -m 5600` | `hashcat -m 5600 cap.txt /opt/wordlists/rockyou.txt` |
| Crack NTLM (SAM/NTDS) | `-m 1000` | `hashcat -m 1000 ntlm.txt /opt/wordlists/rockyou.txt` |
| Crack NetNTLMv1 | `-m 5500` | `hashcat -m 5500 cap.txt /opt/wordlists/rockyou.txt` |
| Crack Kerberoast (etype 23) | `-m 13100` | `hashcat -m 13100 tsp.txt /opt/wordlists/rockyou.txt` |
| Crack AS-REP roast (etype 23) | `-m 18200` | `hashcat -m 18200 asrep.txt /opt/wordlists/rockyou.txt` |
| Crack pre-auth AS-REQ capture | `-m 7500` | `hashcat -m 7500 cap.txt /opt/wordlists/rockyou.txt` |
| Apply mangling rules | `-a 0 -r` | `-r /usr/share/hashcat/rules/best64.rule` |
| Known suffix/prefix pattern | `-a 6` / `-a 7` | `-a 6 words.txt '?d?d?d?d'` |
| Pure exhaustion of a pattern | `-a 3` | `-a 3 '?u?l?l?l?l?d?d' -i` |
| Re-show what is already cracked | `--show` | `hashcat -m 5600 cap.txt --show` |

hashcat is offline only. It never contacts a target, so it produces no victim telemetry; the risk is on your side (potfile plaintext, CPU time, disk).

## Prerequisites

- A working compute backend. On this host the pocl CPU device is installed and usable: `hashcat -I` lists `OpenCL 3.0 PoCL` with device `cpu-haswell-DO-Regular` (~2.9 GB, 512 MB per allocation). If a host shows `ATTENTION! No OpenCL, Metal, HIP or CUDA installation found.`, install the loader — it is a host change, not a hashcat flag:

```sh
apt-get install -y ocl-icd-libopencl1 pocl-opencl-icd
hashcat -I                                      # must list a pocl CPU device
```

  Without a backend hashcat still prints help, modes and example hashes, but cannot crack.
- Wordlists at `/opt/wordlists`: `rockyou.txt` (14,344,391 lines), `pass-top1m.txt` (1,000,000), `pass-1050.txt`.
- Rule files ship in `/usr/share/hashcat/rules`: `best64.rule`, `d3ad0ne.rule`, `dive.rule`, `rockyou-30000.rule`, `leetspeak.rule`, `T0XlC.rule`, `combinator.rule`.
- Hash text exactly as captured. Captured files with `user::...` prefixes need `--username`; Responder and impacket both write prefixes.

**Expected throughput on this host.** Two vCPU (`DO-Regular`), no GPU, pocl CPU backend. Measured: `hashcat -b -m 0` reports **44,011 kH/s (≈44 MH/s) MD5** on one CPU device. Treat published GPU tables as 50-200x optimistic for everything else:

| Work | Expected order | Why |
| --- | --- | --- |
| `-m 1000` NTLM, `-m 3000` LM | hundreds of kH/s, low MH/s at best | single MD4 pass, CPU-bound |
| `-m 5600` NetNTLMv2 | tens of kH/s | HMAC-MD5 per candidate |
| `-m 7500/13100/18200` Kerberos | tens of kH/s | etype 23 is RC4-HMAC |
| `-m 1800` sha512crypt | low single-digit kH/s | 5000 iterations by design |
| `-m 3200` bcrypt, `-m 13400` KeePass | hundreds of H/s or less | deliberately slow KDFs |

Practical consequence: `rockyou.txt` against `-m 5600` is a coffee break, not a minute. Against bcrypt it is not feasible here at all; scope those to a rented GPU or accept a targeted mask. Measure with `hashcat -b -m <mode>` rather than trusting these numbers.

## Core invocations

```sh
# 1. What hardware hashcat can see (the first command on any new box)
hashcat -I

# 2. Benchmark one mode to get a real local number instead of guessing
hashcat -b -m 1000

# 3. Straight dictionary attack on captured NetNTLMv2
hashcat -m 5600 cap.txt /opt/wordlists/rockyou.txt --username

# 4. Dictionary plus best64 mangling (cheap, usually the best first try)
hashcat -m 5600 cap.txt /opt/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --username

# 5. Kerberoast and AS-REP material
hashcat -m 13100 kerberoast.txt /opt/wordlists/pass-top1m.txt
hashcat -m 18200 asrep.txt /opt/wordlists/rockyou.txt -r /usr/share/hashcat/rules/leetspeak.rule

# 6. Hybrid: wordlist plus four digits (season suffixes)
hashcat -m 1000 ntlm.txt -a 6 /opt/wordlists/pass-top1m.txt '?d?d?d?d'

# 7. Hybrid the other way: two digits in front of the word
hashcat -m 1000 ntlm.txt -a 7 '?d?d' /opt/wordlists/pass-top1m.txt

# 8. Mask attack with increment, letters first then digits
hashcat -m 1000 -a 3 ntlm.txt '?u?l?l?l?l?l?d?d' -i --increment-min 5 --increment-max 8

# 9. Custom charset for company-style passwords
hashcat -m 1000 -a 3 ntlm.txt -1 '?u?l' -2 '?d?s' '?1?1?1?1?2?2?2?2'

# 10. Report and re-check without re-running the attack
hashcat -m 5600 cap.txt --show --username
hashcat -m 5600 cap.txt --left --username

# 11. Per-engagement potfile so results stay separable
hashcat -m 5600 cap.txt /opt/wordlists/pass-top1m.txt --potfile-path /tmp/eng1.potfile --username

# 12. Optimised kernels plus high workload, on a host that actually has a backend
hashcat -m 1000 ntlm.txt /opt/wordlists/rockyou.txt -O -w 3

# 13. Preview candidates before spending CPU on them
hashcat --stdout -a 3 '?u?l?l?l?d?d' | head
hashcat --stdout -r /usr/share/hashcat/rules/best64.rule -a 0 password

# 14. Identify what a mystery hash is, before choosing -m
hashcat --identify mystery.hash

# 15. Long run with a session name and a hard stop
hashcat -m 13100 kerberoast.txt /opt/wordlists/pass-top1m.txt --session eng1 --runtime 3600 -o cracked.txt
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-m` | hash mode | wrong mode = instant `Exhausted` with no cracks |
| `-a` | attack mode 0/1/3/6/7 | 0 straight, 3 mask, 6 wordlist+mask, 7 mask+wordlist |
| `-r` | rule file applied to each word | `best64.rule` first, `rockyou-30000.rule` if time allows |
| `-j` / `-k` | single rule left / right | right-hand rule applies to the right wordlist in `-a 1` |
| `-1`..`-4` | custom charsets `?1`..`?4` | define before the mask |
| `-i` | mask increment | pair with `--increment-min` / `--increment-max` |
| `-O` | optimised kernels | help says it `limits password length`; drop it for long plains |
| `-w` | workload profile 1-4 | 4 is `Nightmare`, makes the box unresponsive |
| `-s` / `-l` | skip / limit candidates | for parallel workers or resuming |
| `--show` / `--left` | print cracked / uncracked from potfile | does not run an attack |
| `--potfile-path` | alternate potfile | essential per engagement |
| `--username` | treat a leading `user:` as a username | needed when a capture is `user:hash` |
| `-o` | write plains to a file | easier to hand off than the potfile |
| `--remove` | delete hashes as they crack | mutates the input file, keep a copy |
| `--identify` | guess the algorithm | works without a backend |
| `--example-hashes` | print example hash and settings for a mode | works without a backend |
| `--force` | ignore warnings | needed when pocl reports an unusable device |
| `--runtime`, `--session`, `--restore` | bound and resume work | `~/.hashcat/sessions/` holds the restore file |

## Workflow

1. **Identify the format.** `hashcat --identify`, then `--example-hashes -m <n>` and compare the structure (field count, separators). A Responder SMB capture is `user::DOMAIN:challenge:response:blob` and is mode 5600.
2. **Check the backend once.** `hashcat -I`. If it prints the ATTENTION block, stop: install `ocl-icd-libopencl1` or use another host. Do not tune flags against a backend that does not exist.
3. **Clean the input.** Strip blank lines and duplicates; keep an untouched copy. Use `--username` instead of editing captures when possible.
4. **Straight dictionary first.** `rockyou.txt` or `pass-top1m.txt`. `--show` afterwards to see the yield before spending more.
5. **Add rules.** `best64.rule`, then `d3ad0ne.rule` or `rockyou-30000.rule`. Preview cost with `--stdout | wc -l`.
6. **Then masks.** Company patterns (`?u?l?l?l?l?l?d?d`, season + year) beat full exhaustion. Use `-i` to grow length instead of guessing one width.
7. **Record results per engagement.** `--potfile-path` and `-o` keep engagements separable; `--show` output is the report evidence.
8. **Escalate format coverage to john** if hashcat has no mode for the hash, and note that this host's `john` is core 1.9.0 (`/usr/sbin/john`), which rejects `--list=formats` and non-core formats such as `raw-md5`. Verify support before relying on it; otherwise bring the hash to a host with john jumbo.

## OPSEC and telemetry

- Cracking is offline: no packets, no target logs. The exposure is local - the potfile and `-o` output are plaintext credentials sitting in `~/.hashcat/` or `/tmp`.
- On a shared cloud box, sustained `-w 4` will starve your other tooling and can trip provider CPU-credit alarms. Use `-w 1` or `nice -n 19`.
- Wordlist contents and rule names can reveal engagement context. Keep `--potfile-path` inside the engagement directory, not the default.
- `--remove` rewrites your capture file; lose the original and you cannot re-verify whether a hash was crackable.
- A cracked password is often reused. Re-test it only against in-scope systems, with the lockout policy in hand.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `ATTENTION! No OpenCL, Metal, HIP or CUDA installation found.` | no OpenCL loader | install `ocl-icd-libopencl1` and `pocl-opencl-icd`; this host already has them |
| Exits immediately after `Started:` with no work | same missing backend | confirm with `hashcat -I` |
| `Token length exception` | wrong `-m`, or hash truncated by copy/paste | re-capture, compare with `--example-hashes` |
| `Separator unmatched` | hash line has a username prefix or trailing junk | add `--username`, clean the line |
| `Exhausted` in seconds with no crack | mode mismatch (e.g. 5600 run as 1000) | `--identify`, then correct `-m` |
| `--show` prints nothing although a crack was reported | different potfile path | pass the same `--potfile-path` used during the run |
| `Hashfile ... token length exception` only for some lines | mixed formats in one file | split by mode, run separately |
| Optimised kernel rejects the plain | `-O` caps password length | drop `-O` for that run |
| `Device #1: Not enough memory` / `skipping` | pocl CPU device under-provisioned | `--force`, lower `-n`/`-u`, smaller segment `-c` |
| Cracks nothing on a hash known to be crackable | wordlist encoding or `$HEX[]` plains | add `--hex-wordlist` or normalise the wordlist |

## Verification

```sh
hashcat --version                                  # v6.2.6
hashcat -I | head -3                               # backend list, or the ATTENTION block
hashcat --example-hashes -m 5600 | grep -E 'Name|Example.Hash'   # mode semantics, no backend needed
hashcat --identify /tmp/one.hash                   # expected mode for a captured line
```

`--version`, `-I`, `--example-hashes`, `--identify` and `--show` all work without a compute backend, which is what makes them usable as a health check on this host. `--show` against an empty file answers `hashfile is empty or corrupt.`, so give it a real capture. A real crack additionally requires `hashcat -I` to name at least one device.

## Related skills

- [john](../john/SKILL.md) for formats hashcat has no mode for; verify this host's core 1.9.0 build first
- [responder](../responder/SKILL.md) for the NetNTLMv2 captures this tool consumes
- [kerbrute](../kerbrute/SKILL.md) for validating the usernames behind cracked passwords
- [netexec](../netexec/SKILL.md) to test recovered credentials in scope
- [redteam-toolchain](../redteam-toolchain/SKILL.md) for what this host does and does not have installed