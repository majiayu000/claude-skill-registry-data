---
name: evo-suricata-custom-exfil
description: Generates and validates Suricata 7.0 rules for detecting data exfiltration hidden in HTTP telemetry traffic, using sticky buffers, exact URI matching, header inspection, and PCRE body pattern matching.
---

# evo-suricata-custom-exfil

## Description
Generates Suricata 7.0 rules for detecting data exfiltration hidden in HTTP telemetry traffic.
Handles all five detection conditions with proper sticky buffer syntax, URL-decode transforms,
parameter boundary awareness, and PCRE anchoring to minimize false positives and false negatives.

## Domain Knowledge

### Suricata 7.0 Rule Structure
- Header: `alert http any any -> any any` — use `alert http` to leverage Application Layer
  Protocol Identification (ALPI); avoids port-dependent matching.
- Use `any any -> any any` when both source and destination may be internal (e.g., 10.x to 10.x).
- Options in parentheses, semicolon-delimited.
- Must include `sid`, `rev`, and ideally `flow:established,to_server`.

### Sticky Buffers (Suricata 7.0)
Sticky buffers are **context switches**: once declared, all subsequent `content`, `pcre`, `bsize`,
`depth`, `offset`, `distance`, `within` keywords apply to that buffer until a new sticky buffer
is declared. This is the modern 7.0 approach — legacy trailing modifiers like `http_method` are
deprecated.

- `http.method;` — matches HTTP verb (POST, GET, etc.)
- `http.uri;` — normalized URI including query string and leading `/`
- `http.uri.raw;` — unnormalized URI as on the wire
- `http.header;` — all request headers concatenated, CRLF-separated
- `http.request_header;` — individual header, name and value joined by `|3a 20|` (`: `)
- `http.request_body;` — HTTP request body (POST/PUT/PATCH payload)

### Critical Rules & Edge Cases

1. **Sticky buffer ordering**: Buffer keyword BEFORE content match.
   Correct: `http.method; content:"POST";`
   Wrong: `content:"POST"; http.method;`

2. **Exact URI matching**: `http.uri` includes query string. Use `startswith; endswith;`
   to prevent substring matches (e.g., `/telemetry/v2/report/extra`).

3. **Header matching options**:
   - `http.header;` with `content:"X-TLM-Mode"; content:"exfil";` — works but risks
     cross-header false positives.
   - `http.request_header;` with `content:"X-TLM-Mode|3a 20|exfil";` — isolates a single
     header, more precise. The `|3a 20|` is the colon-space separator Suricata normalizes.

4. **`http.request_body` is NOT URL-decoded by default**. If the POST body uses
   `application/x-www-form-urlencoded`, characters like `=` become `%3D` and `+` replaces
   spaces. The `url_decode` transform must be applied after the sticky buffer declaration
   to decode before matching. However, if the body is raw/JSON/binary, `url_decode` is
   harmless (it only transforms `%HH` sequences and `+`).

5. **PCRE relative flag `R`**: When `pcre` follows a `content` match within the same sticky
   buffer, the `R` flag makes the PCRE start matching from the byte after the content match.
   This is essential for validating the *value* after a parameter name like `blob=`.

6. **Parameter boundary awareness**: To ensure `blob=` is a top-level parameter (not a
   substring like `xblob=`), use a separate `pcre` without `R` to check `(?:^|&)blob=`.

7. **Hex value exact length**: For `sig=` with exactly 64 hex chars, use
   `pcre:"/^[0-9a-fA-F]{64}(?:[^0-9a-fA-F]|$)/R"` — the lookahead ensures no 65th hex char.

8. **Base64 charset**: `[A-Za-z0-9+/=]`. In PCRE inside Suricata rules, forward slash must
   be escaped: `[A-Za-z0-9+\\/=]`.

9. **`-k none` for PCAP testing**: Disables checksum validation. PCAPs from tcpdump often
   have invalid checksums due to TCP Offload Engines; without this flag, packets are dropped.

10. **`flow:established,to_server`**: Ensures TCP handshake completed and traffic flows
    client→server. Mandatory for production rules to prevent spoofed-IP false positives.

### Multiple Approaches for Robustness
The skill generates multiple rule variants and tests them against training PCAPs to find the
best-performing rule. This handles edge cases where:
- The body may or may not be URL-encoded
- Header casing may vary
- Parameters may appear in any order in the body

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-suricata-custom-exfil/scripts')
from generate_rule import write_rules_file, test_rule_with_suricata, auto_select_best_rule

# Auto-select best rule variant by testing against training PCAPs
best_rule = auto_select_best_rule()

# Or manually generate and write rule
rule = write_rules_file('/root/local.rules')

# Test against pcaps
pos_count, _ = test_rule_with_suricata('/root/pcaps/train_pos.pcap')
neg_count, _ = test_rule_with_suricata('/root/pcaps/train_neg.pcap', log_dir='/tmp/suri-neg')
```

## Files
- `scripts/generate_rule.py` - Rule generation, variant testing, and validation utilities