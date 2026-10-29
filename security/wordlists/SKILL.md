---
name: wordlists
description: "Pick the right list from /opt/wordlists (symlinked SecLists plus rockyou) for fuzzing, spraying and subdomain work, and add new lists without breaking the symlink farm. Use before any ffuf, gobuster, feroxbuster, hydra, hashcat or nuclei run; Not for payload authoring (use PayloadsAllTheThings) or hash cracking technique (use hashcat)."
---

# Wordlists

`/opt/wordlists` is a thin, stable naming layer over `/opt/repos/SecLists`. Seven of the eight entries are symlinks; only `rockyou.txt` is a real file. The point is that commands can say `/opt/wordlists/dir-medium.txt` and keep working when SecLists is updated underneath, and that the choice of list becomes a decision you make once instead of a path you retype.

## When to use

| Job | List | Why |
| --- | --- | --- |
| Directory and file discovery, default | `dir-medium.txt` | 220k DirBuster entries, ~1.9 MB, finishes in minutes |
| Directory discovery, last pass | `dir-big.txt` | 1.27M entries, 7x the requests, use only after medium is clean |
| Real-world paths, API and dotfiles | `web-common.txt` | 4.7k curated paths, very low noise |
| Password spraying or a quick crack | `pass-1050.txt` | 10k most common, smallest useful set |
| Crack with a broad common base | `pass-top1m.txt` | 1M Pwdb entries, 8.8 MB |
| Full offline crack | `rockyou.txt` | 14.3M entries, 140 MB, the reference list |
| Username spraying | `users-top.txt` | 17 default/administrative names, fast to test |
| Subdomain brute force | `subs-20k.txt` | 20k names, sized for a DNS resolver, not a /16 |

Rule of thumb: smallest list that can plausibly contain the answer, one wave at a time, and log which wave hit.

## Prerequisites

- `ls -l /opt/wordlists` shows the arrow for each symlink; a missing target means SecLists was moved or not cloned.
- Consumers on this host: `/opt/tools/{ffuf,gobuster,feroxbuster,httpx,nuclei}`, `~/.local/bin/dirsearch`, `/usr/bin/hydra`, `/usr/bin/hashcat`. `/opt/tools` is only on PATH in a login shell.
- Raw material: `/opt/repos/SecLists` (Discovery, Passwords, Usernames, Fuzzing, Payloads, Web-Shells) and `/opt/repos/PayloadsAllTheThings` (XSS, SQLi, SSRF, JWT, command injection, ...).
- Disk: the farm is 140 MB, almost all of it rockyou. Do not copy lists into engagement directories.

## Core invocations

```sh
# 1. the farm itself: seven arrows, one real file
ls -l /opt/wordlists
readlink -f /opt/wordlists/dir-medium.txt   # resolves to the SecLists path

# 2. size and line count of every list, following symlinks
for f in /opt/wordlists/*.txt; do printf '%-20s %8s lines\n' "$(basename "$f")" "$(wc -l < "$f")"; done

# 3. directory fuzzing, medium wave
ffuf -u https://target.example/FUZZ -w /opt/wordlists/dir-medium.txt -ic -mc all -fc 404

# 4. extension sweep on the same paths
ffuf -u https://target.example/FUZZ.php -w /opt/wordlists/web-common.txt -ic -mc 200,301,302,403

# 5. subdomain brute force against a known resolver
ffuf -u https://FUZZ.target.example -w /opt/wordlists/subs-20k.txt -ic -mc all -fs 0

# 6. gobuster equivalent when ffuf output is too noisy
gobuster dir -u https://target.example -w /opt/wordlists/dir-medium.txt -t 20 --no-error

# 7. spray usernames before passwords
hydra -L /opt/wordlists/users-top.txt -p 'Spring2026!' ssh://10.0.0.5 -t 2

# 8. password spray with the small list
hydra -l svc-backup -P /opt/wordlists/pass-1050.txt smb://10.0.0.5 -t 1

# 9. crack a fast hash: common first, rockyou second
hashcat -m 0 -a 0 hashes.txt /opt/wordlists/pass-top1m.txt
hashcat -m 0 -a 0 hashes.txt /opt/wordlists/rockyou.txt --rules-file /usr/share/hashcat/rules/best64.rule

# 10. strip DirBuster header comments before a tool that does not ignore them
grep -v '^#' /opt/wordlists/dir-medium.txt > /tmp/dir-medium.clean

# 11. work a subset first, so a bad run costs minutes instead of hours
head -n 5000 /opt/wordlists/dir-big.txt > /tmp/dir-big.head
ffuf -u https://target.example/FUZZ -w /tmp/dir-big.head -ic

# 12. find the original in SecLists when a list is missing here
find /opt/repos/SecLists -name 'subdomains-top1million-*' | head
```

Adding a list without breaking the farm:

```sh
# 13. new symlink into SecLists (absolute target, same naming style)
ln -s /opt/repos/SecLists/Discovery/Web-Content/raft-medium-directories.txt \
      /opt/wordlists/dir-raft.txt
ls -l /opt/wordlists/dir-raft.txt          # arrow must resolve

# 14. a list with no upstream home stays a real file, never a fake symlink
install -m 644 /tmp/custom.txt /opt/wordlists/custom.txt

# 15. refresh the upstream instead of replacing the links
git -C /opt/repos/SecLists pull --ff-only
```

## Flags that matter

| Flag | Applies to | Effect |
| --- | --- | --- |
| `-w <file>[:KEYWORD]` | ffuf, gobuster | list plus optional placeholder name |
| `-ic` | ffuf | ignore `#` comment lines (DirBuster headers) |
| `-mc` / `-fc` | ffuf | match / filter status codes |
| `-fs` / `-fl` / `-fw` | ffuf | filter by size, lines, words: kills wildcard responses |
| `-t <n>` | ffuf, gobuster | threads; ffuf defaults to 40, gobuster to 10, both are loud |
| `-L` / `-P` / `-C` | hydra | user list / password list / `user:pass` list |
| `-t` | hydra | parallel tasks per target; keep at 1-2 for sprays |
| `-m <mode>` / `-a 0` | hashcat | hash type and straight dictionary attack |
| `--rules-file` | hashcat | mutate each candidate; multiplies candidates |
| `--no-error` | gobuster | suppress connection noise on large lists |

## Workflow

1. **Confirm the farm.** `ls -l /opt/wordlists` and resolve one path with `readlink -f`. A red arrow means everything below is wasted time.
2. **Size the job.** Estimate requests = lines x threads x accept rate. A 220k list at 40 threads takes minutes; 1.27M is a different decision.
3. **One wave at a time.** `web-common` -> `dir-medium` -> `dir-big`, recording hits and 401/403 responses separately; a 403 is a finding, not a miss.
4. **Filter the wildcard first.** On `ffuf`, run a random path and note its size, then `-fs <size>`.
5. **Credentials before cracking.** `users-top.txt` plus `pass-1050.txt` finds the default account far more often than rockyou finds a real password.
6. **Crack in tiers.** top1m, then rockyou, then rules. Stop when the hash rate says the next tier costs more than the value.
7. **Record the list.** Every hit is only reproducible with the exact filename, since the symlinks move with SecLists.

## OPSEC and telemetry

- Request volume is the signal: `dir-big.txt` against one host is a 1.27M-request spike in the target's logs and WAF. Rate limit before you are rate limited.
- Default `User-Agent` values from ffuf and gobuster are trivially blocked and fingerprinted; set one you have authorization to use.
- Hydra sprays lock accounts. `-t 1` and the short list exist for that reason.
- Wordlists themselves leak intent: never copy `pass-top1m.txt` into a target-owned share or a git repository.
- SecLists is a public repository; the fact that you pulled it says nothing about the target, but paths you add to `/opt/wordlists` may.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `wc -l` returns "No such file or directory" | dangling symlink, SecLists moved | `readlink -f` the link, re-clone SecLists, recreate the link |
| ffuf reports hits on every path | wildcard response (catch-all 200) | filter by size/lines/words from a random-path probe |
| ffuf hits on `#` lines | DirBuster header comments are 13 of the 220,559 lines | add `-ic`, or `grep -v '^#'` first |
| `pass-1050.txt` looks wrong-sized | it is the 10k list (10,001 lines), not 1,050 | treat the name as a label, check `wc -l` |
| hashcat rejects the wordlist | list is fine; the mode or file encoding is not | confirm `-m`, and that the file is plain text (rockyou here is extracted UTF-8) |
| hydra stops after the first success | default stops per host | that is correct for a spray; use `-f` deliberately, not by accident |
| `ffuf: command not found` | `/opt/tools` only on login PATH | absolute path or `source /etc/profile.d/10-redteam.sh` |
| Newly added symlink points nowhere | target path typo, or a relative link from the wrong cwd | always `ln -s /absolute/target /opt/wordlists/name.txt` |
| `ln: failed to create symbolic link` | a file already exists at that name | pick a new name; never overwrite a farm entry |

## Verification

```sh
ls -l /opt/wordlists
# 7 arrows (dir-big, dir-medium, pass-1050, pass-top1m, subs-20k, users-top,
# web-common) and one regular file, rockyou.txt

wc -l /opt/wordlists/dir-medium.txt    # 220559
wc -l /opt/wordlists/pass-top1m.txt    # 1000000
stat -Lc '%s %n' /opt/wordlists/rockyou.txt   # 139921497 .../rockyou.txt
readlink -f /opt/wordlists/web-common.txt     # /opt/repos/SecLists/Discovery/Web-Content/common.txt
```

Byte sizes: dir-medium 1,979,956; dir-big 14,802,784; web-common 38,536; subs-20k 135,562; users-top 112; pass-1050 73,026; pass-top1m 8,755,171. No list uses CRLF.

## Related skills

- [ffuf](../ffuf/SKILL.md) and [httpx](../httpx/SKILL.md) for the raw HTTP loops these lists feed
- [hydra](../hydra/SKILL.md) for spray mechanics and lockout avoidance
- [hashcat](../hashcat/SKILL.md) for mode selection and rules
- [segfault-cli](../segfault-cli/SKILL.md) for `resolv`, which turns a name list into addresses
- [redteam-toolchain](../redteam-toolchain/SKILL.md) for how the farm is built and repaired