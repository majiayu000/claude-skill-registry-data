---
name: ctf-methodology
description: >
  CTF challenge triage and time management — identify the category and intended technique from the
  handout artifacts in the first 10 minutes, budget points vs. time, and know when to park a
  challenge. Load at the start of any CTF/jeopardy challenge, when handed an unknown file, URL, or
  "nc host port" with no context. Signals: flag{...} / CTF{...} format, challenge tarball, pwn/
  web/crypto/rev/forensics/misc categories, "nc ", Docker handout, points value.
domain: ctf
type: methodology
stability: learning
modes: [pentest, bugbounty]
severity: info
tools: [file, binwalk, exiftool, checksec, strings]
schema_version: 1
---

# CTF methodology: triage and time budgeting

## When it applies
You're working jeopardy-style CTF challenges (authorized by definition — the organizer hands you the
targets). This skill is the entry point: it classifies the challenge, picks the category playbook
(`ctf-web`, `ctf-pwn`, `ctf-crypto`, `ctf-rev`, `ctf-forensics`), and keeps you from sinking three
hours into a 100-point guessy challenge.

## Why it works
CTF challenges are *designed* puzzles with an intended path, and the handout almost always telegraphs
it: the category, the files provided, the service type, the description's wordplay. Reading those
signals first converts "stare at an unknown blob" into a 2-minute routing decision, and a point/time
budget converts sunk-cost grinding into deliberate moves.

## Method
1. **Read the handout like a spec, not a flavor text.** Category, title, and description are hints:
   puns name the technique ("relationships" → RSA common modulus, "padding" → padding oracle),
   an unusual port or protocol *is* the challenge. Note the flag format (`flag{`, `CTF{`) so you
   can grep for it later.
2. **Inventory the artifacts (2 minutes).** For each provided file:
   ```
   file <f> ; exiftool <f> ; strings -n 6 <f> | head -50 ; checksec --file=<bin>
   ```
   Archive/disk image → `ctf-forensics`. ELF/PE/APK with a flag-check → `ctf-rev`. ELF + `nc` +
   libc → `ctf-pwn`. `.py`/`.sage` with math → `ctf-crypto`. URL only → `ctf-web`.
3. **Fingerprint the service.** `nc` banner grab; for HTTP, `curl -sS -D- <url>` and read headers,
   cookies, comments, and linked assets — server header (Flask/PHP/Express) narrows the bug class
   immediately (`recon-techstack-fingerprinting`).
4. **Classify difficulty honestly.** Provided source + small binary + common category = intended
   easy; read the source for the bug before touching tools. No source + large binary + kernel/heap/
   custom crypto = intended hard; expect the full chain and budget accordingly.
5. **Budget by points and momentum.** A working heuristic: cap exploration at ~15–20 minutes per
   untried idea, and re-evaluate a challenge when you've spent more time than its points justify
   relative to what remains open. Points are worth the same everywhere — three quick 100s beat one
   stalled 400.
6. **Move on deliberately, not silently.** Park a challenge when: you've enumerated the obvious
   surface twice with no new information, every hypothesis needs information the challenge doesn't
   provide (guessy), or a teammate/other challenge offers better points-per-hour. Write down the
   state (what you tried, what's ruled out, next idea) so re-entry is cheap — solves often come
   from a fresh look or a later organizer hint.
7. **Watch for released hints and solve counts.** Organizers drop hints when a challenge stalls
   event-wide; a high solve count means the intended path is simple and you're overthinking —
   go back to the description and the most obvious reading.

## Gotchas
- **The category label lies occasionally** — "web" challenges that end in SSTI-to-RCE, "crypto"
  that's really encoding, "misc" that's actually forensics. Re-classify as evidence appears instead
  of forcing the labeled playbook.
- **Warmup/100-point challenges never require deep tooling.** If you're writing a heap exploit for
  a warmup, you missed something — look for the joke, the encoding, the default creds.
- **Guessy challenges** (stego with no cover text, obscure cipher with no key hint) burn unlimited
  time. Timebox hard and return after everything tractable is done.
- **Dynamic/shared instances** — other players can leave artifacts in shared services (uploaded
  shells, changed passwords); a freshly spawned instance is worth the restart.
- **Don't skip the flag format grep** — `strings`, pcap searches, and memory dumps often yield the
  flag directly to `grep -a 'flag{'` before any "real" solve.

## Verify success
Every open challenge has: a category assignment, a loaded playbook, a written list of tried/ruled-
out ideas, and an explicit keep/park decision — no challenge is being worked by vibes. Scoreboard
confirms submitted flags.

## References
Routes into `ctf-web`, `ctf-pwn`, `ctf-crypto`, `ctf-rev`, `ctf-forensics`; technique depth in the
domain skills they chain to (`web-testing-checklist`, `exploit-pwn-chain`, `crypto-rsa-attacks`,
`reverse-eng-binary-triage`, `defense-dfir-triage`).
