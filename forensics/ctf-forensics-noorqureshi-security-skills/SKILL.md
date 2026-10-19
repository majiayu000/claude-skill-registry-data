---
name: ctf-forensics
description: >
  CTF forensics playbook — quick wins on pcaps, memory dumps, disk images, and stego files:
  binwalk carving, Wireshark object export, Volatility's five commands that solve most memory
  challenges, steghide/zsteg/exiftool stego battery. Load when the handout is a capture, image, or
  dump file. Signals: "forensics"/"stego" category, .pcap/.pcapng, .mem/.raw/.vmem, .dd/.img/.E01,
  a lone .png/.jpg/.wav, "incident", "suspicious traffic".
domain: ctf
type: technique
stability: learning
modes: [pentest, defense]
severity: medium
cwe: []
tools: [wireshark, tshark, binwalk, foremost, volatility3, exiftool, steghide, zsteg, strings, bulk_extractor]
schema_version: 1
---

# CTF forensics and stego

## When it applies
The handout is an artifact to investigate: a packet capture, memory dump, disk image, or an
innocent-looking media file. This skill is the CTF quick-win battery — the 80% of challenges that
fall to standard tooling run in the right order. For real-IR depth (timelines, root cause,
attacker methodology) defer to `defense-dfir-triage`, `defense-malware-triage`,
`defense-log-analysis`; here the only objective is finding the flag in the haystack.

## Why it works
CTF forensics artifacts are constructed, not organic: the flag was placed by an author using a
standard technique (appended data, an HTTP download, a deleted file, an LSB embedding), and each
technique has a canonical tool. Running the *standard battery in order* surfaces the planted
artifact faster than clever hypotheses, because the author used the same tools you have.

## Method
1. **Universal first pass (every file, 2 minutes).**
   ```
   file <f>; exiftool <f>; strings -n 8 <f> | grep -iE 'flag|pass|key|{' ; binwalk <f>
   ```
   `file` lying about the type (wrong extension/magic) is itself a classic stage one. Metadata
   (exiftool) hides flags in comment/author/GPS fields. `binwalk -eM` extracts embedded archives
   recursively — appended zip-after-image is the most common stage one of all.
2. **pcap (.pcap/.pcapng).**
   - Open in Wireshark; check *Protocol Hierarchy* and *Conversations* first — the odd protocol
     or the one giant stream is the lead.
   - Export objects: *File → Export Objects → HTTP/SMB/TFTP* — downloaded files (exfil zips,
     images) come out whole.
   - Follow TCP streams; flag-in-cleartext-chat is common. `tshark -r cap.pcap -Y 'http' -T fields
     -e http.request.uri` for quick scripting.
   - Exfil channels: DNS (long encoded subdomains — decode base32/64/hex of the labels), ICMP
     payload bytes, TLS where a `keys.log`/RSA key is provided (set the key log in preferences).
   - USB pcaps: `usb.capdata` keystroke/mouse reconstruction (map HID codes back to characters).
3. **Memory dumps (.mem/.raw/.vmem) — Volatility 3, the five that solve most:**
   ```
   vol -f dump.mem windows.info            # profile/OS
   vol -f dump.mem windows.pslist          # the odd process (notepad, mspaint, truecrypt)
   vol -f dump.mem windows.cmdline         # commands with passwords/flags as args
   vol -f dump.mem windows.filescan | grep -iE 'flag|secret|\.zip|\.png'
   vol -f dump.mem windows.dumpfiles --physaddr <addr>   # carve the file out
   ```
   Then per the story: `hashdump` (crack the SAM), `malfind`, clipboard/notepad plugins, browser
   history plugins. And the cheap shot first: `strings dump.mem | grep flag{`.
4. **Disk images (.dd/.img/.E01).** Mount or autopsy-free carve:
   - `fls -r <img>` / `icat` (Sleuth Kit) — list and read files; **deleted files** (`fls -rd`)
     are where flags hide; recover by inode with `icat`.
   - `foremost -i <img> -o out/` or `photorec` — carve by signature when the filesystem is
     damaged or the challenge is raw.
   - `bulk_extractor <img>` — one-shot sweep of URLs, emails, credit cards, keys; grep its output.
   - Check slack/unallocated space and alternate partitions (`mmls` shows the layout; a hidden
     second partition is a classic).
5. **Stego battery (images/audio) — run all, not one.**
   - PNG: `zsteg -a img.png` (LSB and friends, automatic); `pngcheck -v` for odd chunks.
   - JPEG: `steghide extract -sf img.jpg` (try empty passphrase first, then challenge title /
     description words); `stegseek` for fast passphrase cracks; `outguess`; check DCT with
     `stegoveritas` which runs the whole battery at once.
   - Any image: inspect the planes visually (StegSolve-style: bit-plane views reveal QR codes and
     text), compare against an original if the challenge gives one (diff = the payload).
   - Audio: open in Audacity — spectrogram view shows drawn text/QR; morse in the waveform;
     reversed audio; DTMF tones (decode with a dial-tone decoder).
   - Whitespace/zero-width text in provided .txt files; `snow` for whitespace stego.
6. **Chain the stages.** CTF forensics is layered: binwalk gives a password-protected zip → the
   password is in pcap stream 7 → the zip has a QR image → zsteg on the QR. When a stage yields a
   password/key, apply it to every locked artifact you already hold.

## Gotchas
- **Wrong file magic is stage one, not a broken download** — fix the header (`file` says data but
  binwalk sees a zip at offset 0x100 → carve from there).
- **`binwalk -e` without `-M`** misses nested archives — always recurse; also watch for
  false-positive signatures at huge offsets.
- **Volatility profile mismatches fail silently** — if `pslist` looks empty/garbage, the image is
  a different OS build or it's a Linux dump (needs a custom profile / `linux.*` plugins).
- **Steghide passphrases come from the challenge text** — title, description, lyrics of the
  linked song. Try them before brute-forcing.
- **Encrypted volumes (VeraCrypt) in disk images** — the password is elsewhere in the challenge
  (memory dump, deleted note); don't brute a VeraCrypt container, hunt the hint.
- **Corrupted-by-author files** (QR with wrong alignment patterns, PNG with bad CRC) — repair
  tools (`pcrt`, online QR fixers) beat redrawing by hand.

## Verify success
A flag in the event format extracted from the artifact, with a reproducible extraction path (the
exact tool chain and parameters) written down — other players' flags differ, so "found a string"
must survive re-running the battery from the original handout file.

## References
Volatility 3 docs; Sleuth Kit (`fls`/`icat`/`mmls`); Wireshark object export; stegoveritas,
zsteg, stegseek. IR-grade methodology: `defense-dfir-triage`, `defense-malware-triage`.
Triage via `ctf-methodology`.
