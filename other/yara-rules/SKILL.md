---
name: yara-rules
description: Use when you need to write, test, or tune YARA rules for
  malware detection and hunting. Covers rule anatomy, string types and
  modifiers, condition logic, the pe/elf/math/hash/dotnet modules, testing
  against clean and malicious corpora, measuring false positives, atom
  quality for performance, and YARA-X differences. Use when static triage
  finds a new family, when you need hunt rules for an incident, or when an
  existing rule fires too much or too little.
version: 1.0.0
domain: malware
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [static-triage]
tools:
  - name: YARA
    version: 4.5.5
  - name: YARA-X
    version: 1.7.1
  - name: Python
    version: "3.12"
---

YARA rules describe malware families as sets of strings plus a boolean
condition, and they are the shared language of malware detection: analysts
write them, sandboxes run them, and threat intel feeds distribute them. A
good rule fires on every sample of the family and nothing else; a bad rule
fires on your operating system. This skill covers writing rules from real
triage findings, choosing string types and modifiers, using modules for
structural conditions, testing against clean and dirty corpora, tuning
performance, and the YARA-X migration path. Scope: write and test rules
against samples and corpora you are authorized to handle. Test every rule
against a clean corpus before deploying it anywhere that blocks or alerts.

## Quick Workflow

1. Pick 5 to 10 unique strings from static triage of confirmed family
   samples (avoid common library strings).
2. Write the rule with meta, strings, and condition sections.
3. Compile-check it with `yara` against one known sample.
4. Test against your malicious corpus: it should fire on all family samples.
5. Test against your clean corpus (OS files, common apps): it must fire on
   none.
6. Check performance: scan time and atom quality on a large directory.
7. Tune strings and conditions until coverage is high and false positives
   are zero.
8. Version, document, and commit the rule with its test results.

## 1. Rule anatomy

Every rule has three sections. Meta is documentation, strings are the
patterns, condition is the logic.

```yara
rule Trojan_Example_Family_A
{
    meta:
        description = "Detects Example family dropper variant A"
        author = "lab"
        date = "2026-10-23"
        reference = "case-2026-1042"
        hash = "abc123..."  // sample the rule was built from

    strings:
        $mz = "MZ"                                   // sanity anchor
        $s1 = "XxTeaEncryptedPayload" ascii wide
        $s2 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" ascii
        $s3 = { 55 8B EC 83 EC 20 53 56 57 }          // hex: function prologue pattern
        $re1 = /https?:\/\/[a-z0-9.-]+\/gate\.php/ ascii

    condition:
        $mz at 0 and filesize < 5MB and 3 of ($s*)
}
```

Rules live in `.yar` files, one family per file is a good default, with an
index file that includes them all for scanning.

```bash
# Compile check: yara parses before scanning
yara /opt/rules/malware/trojan_example.yar sample.bin && echo COMPILED_OK

# Scan with string match details for tuning
yara -s /opt/rules/malware/trojan_example.yar sample.bin
```

## 2. Choosing strings

String selection is the whole craft. Good strings are unique to the family,
present in all its variants, and unlikely in benign software.

```yara
    strings:
        // Prefer: custom protocol markers, ransom note phrases, unique mutexes
        $a1 = "B0T_C2_v3.2" ascii wide
        $a2 = "SOFTWARE\\Classes\\ExamplePersistence" ascii
        // Avoid: standard library errors, common API names alone
        // Avoid: short strings (< 6 chars) unless combined with others

        // Modifiers that widen or narrow matching
        $b1 = "config" nocase ascii wide          // case-insensitive, both encodings
        $b2 = "payload" xor(0x01-0xff)            // try all single-byte XOR keys
        $b3 = { E8 ?? ?? ?? ?? 85 C0 74 ?? }      // hex with wildcards

    condition:
        // Thresholds beat "all of them": families mutate
        4 of ($a*) or (2 of ($a*) and 1 of ($b*))
```

Test each candidate string against your clean corpus individually before
combining; one bad string poisons the rule. Prefer longer strings (12+
characters) and strings from the malware's unique logic (C2 protocol,
encryption constants, custom error messages) over generic Windows API names.

## 3. Modules for structural conditions

Modules let the condition inspect file structure, not just byte patterns.
The `pe` module is the workhorse for Windows malware.

```yara
import "pe"
import "math"

rule Packed_Example_Loader
{
    meta:
        description = "Example loader: high-entropy text section plus C2 marker"

    strings:
        $c2 = "gate.php?id=" ascii

    condition:
        pe.number_of_sections == 3 and
        math.entropy(pe.sections[0].raw_data_offset, pe.sections[0].raw_data_size) > 7.5 and
        $c2 and
        pe.imports("kernel32.dll", "VirtualAlloc")
}
```

Other modules worth knowing: `elf` (ELF headers and sections), `hash`
(md5/sha256 of regions, for allow/deny lists), `dotnet` (.NET metadata),
`magic` (libmagic file type, useful to scope rules to PEs only). Check
module availability in your build with `yara --module-data pe -v` style
probes or the docs, since distro builds vary.

## 4. Testing against corpora

A rule is not done until it has passed both corpora. Build and maintain them
as lab infrastructure.

```bash
# Directory layout
# /opt/corpus/malware/<family>/...   confirmed malicious samples
# /opt/corpus/clean/...              OS files, common applications

# Coverage: should fire on every sample of the target family
yara -r /opt/rules/index.yar /opt/corpus/malware/example_family/ | tee coverage.txt
wc -l coverage.txt   # compare against sample count

# False positives: must be ZERO on the clean corpus
yara -r /opt/rules/index.yar /opt/corpus/clean/ | tee fp.txt
wc -l fp.txt         # anything here is a rule bug, fix before deploying

# Per-rule stats across a big mixed directory
yara -r -c /opt/rules/index.yar /opt/corpus/mixed/ | sort -t: -k2 -rn | head -20
```

When a rule misses a variant, add strings from the missed sample rather than
loosening the condition; loosening is how false positives are born. When a
rule fires on clean files, identify the offending string with `yara -s`,
replace it with something more specific, and re-test both corpora.

## 5. Performance: atoms and scan speed

YARA extracts short byte sequences ("atoms") from your strings to pre-filter
files quickly. Rules with only regexes or short strings scan slowly.

```bash
# Time a full scan; investigate rules that dominate
time yara -r /opt/rules/index.yar /opt/corpus/mixed/ > /dev/null

# Find slow rules by testing individually on a large file
for r in /opt/rules/malware/*.yar; do
  printf '%s ' "$(basename $r)"
  /usr/bin/time -f '%es' yara "$r" /opt/corpus/mixed/big_sample.bin 2>&1 | tail -1
done | sort -k2 -rn | head -10
```

Performance rules of thumb: prefer literal strings over regexes, keep at
least one long literal (8+ bytes) per rule so atoms are strong, avoid
`xor`/`base64` modifiers on many strings at once, and put cheap structural
checks (filesize, `pe.` conditions) early in the condition so YARA can skip
fast. A hunt rule that takes 10x longer than the rest will get disabled by
whoever runs it, which is the same as not existing.

## 6. YARA-X notes

YARA-X is the Rust rewrite and the future of the project; classic YARA is in
maintenance mode. Most rules work unchanged, but know the differences.

```bash
# YARA-X CLI (yr) scans with the same rule files
yr scan /opt/rules/index.yar sample.bin

# Compile rules to a portable binary for distribution
yr compile /opt/rules/index.yar -o rules.yarc
yr scan rules.yarc sample.bin
```

Differences that bite: some obscure syntax and module fields changed, the
`--no-follow-symlinks` behavior differs on Windows, and compiled `.yarc`
files are the preferred distribution format. Keep rules in source `.yar`
form in version control and compile at deploy time. Test every migrated rule
against both corpora again after switching engines; do not assume parity.

## Edge cases

- Rule fires on packed samples of other families: your strings came from the
  packer stub, not the payload. Rebuild strings from the unpacked sample
  (packer-analysis first).
- Family uses string encryption: no plaintext strings exist. Pivot to hex
  patterns of the decryption routine, API import combinations, or structural
  `pe` conditions instead.
- `xor` modifier explodes scan time: restrict the key range or apply it to
  one anchor string, not ten.
- Rule must match in memory dumps too: add `wide` variants and consider that
  memory images contain fragments; loosen filesize conditions for memory
  scanning.
- Conflicting rule names across files: namespace with family prefixes
  (`Trojan_Example_...`) and keep one index that includes each file once.

## Escalation

- One rule cannot cover a polymorphic family: split into a loader rule and
  a payload rule, or write per-variant rules sharing a common include file
  of helper strings.
- Need to hunt across an enterprise: export the rule to your EDR/SIEM hunt
  capability or run it with Velociraptor's YARA artifact
  (velociraptor-basics) across endpoints.
- Strings are exhausted (fully encrypted payload): switch detection to
  behavior (dynamic-sandbox outputs) or to structural anomalies, and document
  why string-based detection is not viable for this family.
- False positive you cannot eliminate: convert the rule to hunt-only (never
  block) and document the known benign overlap.

## Detection and defender view

YARA rules are detection-as-code, and this skill is squarely on the defender
side: every rule you write should end up in a scanner, a hunt, or a feed
that protects someone. Operational hygiene matters as much as rule quality:
version-control rules, test on every change, track true/false positive rates
per rule, and retire rules for dead families so the set stays fast and
trusted. The misuse case is writing rules to fingerprint security products
or to test malware against detection before release; rules built from samples
you are not authorized to analyze, or built to aid evasion, are out of
scope.

## Key references

- MITRE ATT&CK T1027 (Obfuscated Files or Information): what good rules see
  through.
- MITRE ATT&CK T1036 (Masquerading): rules that key on structural lies.
- YARA documentation: https://yara.readthedocs.io
- YARA-X documentation: https://virustotal.github.io/yara-x/
- YARA-X stable announcement and migration notes: https://virustotal.github.io/yara-x/blog/yara-is-dead-long-live-yara-x/

## See also

- `malware-yara-writing`: Use it instead when the rule must be production-ready from triage findings, with naming, versioning, and deployment.
