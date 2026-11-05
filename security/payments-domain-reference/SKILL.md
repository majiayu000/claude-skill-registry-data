---
name: payments-domain-reference
description: >
  Payments-domain theory as implemented in THIS repo. Load when you hit unfamiliar
  payments jargon, need to reason about message/crypto correctness, OR are ADDING or
  extending a field table, dialect/MessageFormat, simulator decision rule, or HSM host
  command (extension-point maps included): ISO 8583 (MTI,
  bitmaps, DEs, LLVAR/LLLVAR, dialects/MessageFormats), EMV (BER-TLV, DOL,
  ARQC/ARPC, MDK/UDK/session keys, AIP/TVR/TSI), PIN security (ISO 9564 PIN blocks,
  PVV, CVV/CVV2), DUKPT (BDK/IPEK/KSN), HSM concepts (LMK, key tokens, payShield
  host commands — 15 implemented, e.g. NC/A0/KQ/G0), scheme flows (authorization vs clearing
  vs reversal vs network management, VISA Base I, CyberSource /pts/v2). Keywords:
  MTI, bitmap, data element, DE 55, TLV, cryptogram, ARQC, PIN block, KSN, LMK,
  key check value, KCV, STAN, RRN, Base I, STIP, retail MAC, track 2.
---

# Payments Domain Reference (as implemented in PayProbe)

Ground rules for reading this file:

- Every concept points at the PayProbe file that implements it. Paths are
  repo-root-relative. This is the theory *this codebase* embodies — not a textbook.
- PayProbe is a **testing platform**: it simulates hosts, schemes, and HSMs. Nothing
  here handles real card data or production keys.
- Facts date-stamped 2026-07-03 unless noted. Re-verify with the commands in
  "Provenance and maintenance" before trusting volatile details.

**When NOT to use this skill:**

| You want to… | Use instead |
|---|---|
| Start/stop/operate simulators, run scenarios or load tests | `payprobe-run-and-operate` |
| Debug a wire-level failure (framing mismatch, hung socket, bad decode) | `payprobe-debugging-playbook` |
| Understand why the architecture is shaped this way | `payprobe-architecture-contract` |
| Find configuration knobs for these subsystems | `payprobe-config-and-flags` |

---

## 1. ISO 8583 — the card-transaction wire format

ISO 8583 is the message standard card networks and bank switches speak: one message =
**MTI** (message type indicator) + one or two **bitmaps** + a sequence of numbered
**data elements** (DEs, also called "fields", numbered 2–128).

### 1.1 MTI — four digits, each positional

`decode_mti()` in `packages/scenario-service/models/iso8583_analyzer.py` (tables
`_MTI_VERSION`, `_MTI_CLASS`, `_MTI_FUNCTION`, `_MTI_ORIGIN` around line 419) decodes:

| Digit | Meaning | Values implemented |
|---|---|---|
| 1st — version | which edition of the standard | `0` = ISO 8583:1987, `1` = :1993, `2` = :2003, `8` national, `9` private |
| 2nd — class | what kind of transaction | 1 authorization, 2 financial, 3 file actions, 4 reversal/chargeback, 5 reconciliation, 6 administrative, 7 fee collection, 8 network management |
| 3rd — function | request/response/advice | 0 request, 1 request response, 2 advice, 3 advice response, 4 notification, 8/9 (n)ack |
| 4th — origin | who originated it | acquirer/issuer/other |

So `0200` = 1987 financial request, `0210` its response; `1100` = 1993 authorization
request. **0xxx vs 1xxx is the edition digit** — the 1993 dialect uses 1xxx
MTIs (`1100 1200 1220 1420 1500 1804`, see `_ISO8583_MTIS_1993` in
`packages/scenario-service/models/message_format.py`). The portal step editor's MTI
menu follows the selected dialect's edition (0xxx ↔ 1xxx).

### 1.2 Bitmaps — which DEs are present

- **Primary bitmap**: 64 bits; bit *n* set ⇒ DE *n* present.
- **Bit 1 set** ⇒ a **secondary bitmap** follows, covering DEs 65–128.

Implemented **once** since ADR-0011 (2026-09-24) in the shared leaf package, so the worker still never imports scenario-service code:

| Codec | File | Notes |
|---|---|---|
| The codec | `packages/payprobe_common/iso8583/codec.py` (`pack`, `unpack`, `resolve_encoding`, `encode_bitmap` / `decode_bitmap`, `field_options`) | Bytes in, bytes out, under a wire profile (see 1.5). `fields.py` holds the dictionaries (`ISO8583_1987`, `ISO8583_1993`, `VISA_BASE_I`), `validate.py` the dialect validator, `tlv.py` the EMV BER-TLV helpers, `portable.py` the ASCII paste for code steps. |
| Worker wire entry point | `packages/worker/adapters/tcp/iso8583.py` | Re-export plus the legacy `str` helpers `iso_pack` / `iso_unpack` (ASCII profile; `iso_unpack` strips all whitespace, so it is not used on the wire). |
| Inspector/analyzer | `packages/scenario-service/models/iso8583_analyzer.py` (`analyze_message`, `build_message`, `diff_messages`) | The analysis layer (rows, per-field messages, interpretations, TLV trees) over the shared codec; `iso_pack` / `iso_pack_bytes` kept as thin wrappers. |

### 1.3 Field classes and length types

Field **type classes** (one rule set, `charset_error` in
`packages/payprobe_common/iso8583/validate.py`, used by the responder's
`iso_validate` and the analyzer's `validate_field`): `n` digits, `a` alphabetic,
`an` alphanumeric, `ans`/`anp`/`p`/`s` printable ASCII, `b` binary (hex, whole
bytes), `z` track-2 (digits plus `=`/`D` separators). Lengths are in **logical
units** whatever the wire profile: digits/characters, hex characters for `b`.

**Length types** — a fixed length, or a length indicator whose wire form follows the profile's `length` axis (ASCII digits, packed BCD, 1–2 binary bytes, or EBCDIC digits):

| len_type | Prefix width (digits) | Example |
|---|---|---|
| `fixed` | none | DE 4 amount, 12 digits |
| `llvar` | 2 | DE 2 PAN, up to 19 |
| `lllvar` | 3 | DE 55 ICC data, up to 999 |
| `llllvar` | 4 | supported by both codecs |
| `lllllvar` | 5 | supported by both codecs |

All five are handled by the one codec (`LEN_PREFIX` in
`packages/payprobe_common/iso8583/codec.py`).

### 1.4 Dialects = MessageFormats (the format registry)

A "dialect" is a concrete DE table + MTI list + presence matrix. In PayProbe that is a
**MessageFormat**: model in `packages/scenario-service/models/message_format.py`,
persistence in `packages/scenario-service/api/format_store.py` (builtin seeds live in
code; user formats are file-backed and may override a builtin id). Builtins
(`BUILTIN_FORMATS`), all cloneable; `definition.encoding` is the wire profile the
bound simulator and the packing steps use (ADR-0011):

| id | What it is |
|---|---|
| `iso8583-1987` | The 50-DE 1987 directory (`payprobe_common.iso8583.ISO8583_1987`), `encoding: ascii` |
| `iso8583-binary` | The same 1987 table under the representative `binary` profile (binary bitmap, BCD numerics + MTI, raw binary fields, BCD length indicators). A profile, not a scheme spec; clone and adjust axes / per-field overrides to match a host |
| `iso8583-1993` | 1993 changes: DE 22 → 12-char POS Data Code, DE 39 → 3-char Action Code, DE 56 message reason |
| `visa-base1` | DE table for the bundled VISA Base I simulator (1987 core + VISA-touched DEs 43/44/48/54/60/62/63/90/95; DE 62/63 opaque) |
| `iso20022-pacs008` | ISO 20022 `pacs.008.001.08` (XML, not 8583) |

Simulators can **bind a MessageFormat** for inbound validation (warn/reject), and
tcp_iso8583 send_message steps carry a dialect picker whose fields override the
default table.

### 1.5 Encodings — the wire profile (ADR-0011, built 2026-09-24)

One profile drives the wire, the Inspector and the code-step defaults. It is a
name (`"ascii"`, the default and the historical behaviour; `"binary"`) or an axis
dict overriding the ASCII profile:

| Axis | Values | Governs |
|---|---|---|
| `bitmap` | `hex` \| `binary` \| `ebcdic` | 16 hex chars, 8 raw bytes, or hex chars in EBCDIC |
| `numeric` | `ascii` \| `bcd` \| `ebcdic` | `n` fields, and the MTI unless `mti` says otherwise |
| `text` | `ascii` \| `ebcdic` | `a` / `an` / `ans` / `z` fields (EBCDIC = cp037) |
| `binary` | `hex` \| `raw` | `b` fields as hex text or raw bytes |
| `length` | `ascii` \| `bcd` \| `binary` \| `ebcdic` | the LL / LLL indicators |
| `mti` | `ascii` \| `bcd` \| `ebcdic` | optional; defaults to `bcd` when `numeric` is `bcd` |

A field spec may carry its own `encoding` override for `numeric` / `text` /
`binary` / `length`, plus `pad` (`left` default, `right`), `pad_nibble` (`0` /
`F`) for odd BCD digit counts, and `separator` (`D` default) for a BCD-packed
track-2 field (a `z` field is BCD only when *its own* override says so).

Where the profile comes from on the live path (`wire_encoding_from_config`):
the config's top-level `encoding` wins (that is where the orchestrator injects a
bound Message Format's `definition.encoding`, flag `PAYPROBE_ISO8583_FORMAT_ENCODING`,
default on); otherwise the legacy `framing.encoding` text codec is folded
(`ascii`/`utf-8`/`latin-1` → ascii profile, `cp037`/`ebcdic` → `text: ebcdic`);
an unknown value or a disagreeing pair is refused before anything binds.
`framing.length_encoding` (`binary` | `ascii` | `bcd`) is the *frame* length
prefix and is separate from the body profile. Proof that a binary host
interoperates over a live socket: `packages/worker/tests/test_iso8583_binary_wire.py`.
Unknown-DE decodes stop with `truncated: true` + `error`; a structurally broken
message raises `Iso8583DecodeError`.

### 1.6 Where ISO 8583 lives (map)

| Concern | Location |
|---|---|
| Wire codec (worker) | `packages/worker/adapters/tcp/iso8583.py` |
| Initiator transport (client) | `packages/worker/adapters/tcp/adapter.py` (`TcpAdapter`) |
| Responder/simulator (server) | `packages/worker/adapters/tcp/responder.py` (`TcpResponder`) |
| Protocol strategy (iso8583 vs header_echo) | `packages/worker/adapters/tcp/protocols.py` |
| Analyzer + validation + TLV + MTI decode | `packages/scenario-service/models/iso8583_analyzer.py` |
| Field tables (1987/1993/VISA) | `packages/scenario-service/models/iso_catalog.py` |
| Format registry (model/store) | `packages/scenario-service/models/message_format.py`, `packages/scenario-service/api/format_store.py` |
| Inspector HTTP endpoints | `packages/scenario-service/api/main.py` — `POST /iso8583/analyze` (~line 1199), `/iso8583/build`, `/iso8583/diff`, `/iso8583/tlv/build` |
| MCP tools | `packages/mcp-server/mcp_server/tools.py` — `iso8583_analyze`, `iso8583_build`, `iso8583_diff`, `iso8583_tlv_build` |
| Tests | `packages/worker/tests/test_iso8583_protocol.py`, `packages/scenario-service/tests/test_iso8583_analyzer.py`, `packages/scenario-service/tests/test_formats.py` |

---

## 2. EMV — chip-card data and cryptograms

EMV is the chip-card standard. On the 8583 wire, EMV data rides inside **DE 55** as
BER-TLV.

### 2.1 TLV / BER-TLV

Tag-Length-Value encoding; a **constructed** tag's value is itself a TLV sequence
(nested). `parse_tlv()` / `build_tlv()` in
`packages/scenario-service/models/iso8583_analyzer.py` parse/encode nested trees;
the analyzer auto-parses TLV-carrying DEs (DE 55 among them — see the "TLV DEs" set
near the bottom of that file). A broad EMV tag dictionary (names for 5A, 82, 95, 9B,
9F26, 9F38 …) lives in `packages/scenario-service/models/emv_catalog.py`.

### 2.2 DOL — Data Object List

A DOL (PDOL/CDOL1/CDOL2/TDOL) is a list of **tag + length pairs with no values**: the
card tells the terminal "send me these objects, in this order, at these lengths". The
terminal concatenates the values in DOL order (padded/truncated per entry) — that
value stream is what the card MACs to make a cryptogram. Implemented as runnable
code-tool snippets in `emv_catalog.py`: `_DOL_PARSE` (parse a DOL), `_DOL_BUILD`
(assemble the value stream from `{tag: hex}`), plus `_TRACK2`, `_SERVICE_CODE`,
`_AIP`, `_TVR`, `_LUHN`, `_TRACK_GEN`.

### 2.3 Application cryptograms — ARQC / ARPC and the key chain

The issuer key chain, exactly as `packages/worker/engine/crypto_tools.py` implements
it (real DES/3DES, not stubs):

1. **MDK** (issuer Master Derivation Key) + PAN + PAN sequence number →
   **UDK / ICC Master Key**: `emv_icc_mk(mdk_hex, pan, psn)` → `{"udk": …}`.
2. UDK + **ATC** (Application Transaction Counter) → **session key**
   (EMV Common Session Key, CVN-18 style): `emv_session_key(mk_hex, atc_hex)`.
3. Session key + DOL data stream → **ARQC** (Authorization Request Cryptogram —
   the card proving itself to the issuer): `arqc()` = retail MAC over the data.
4. ARQC + ARC (auth response code) → **ARPC** (issuer proving itself back to the
   card): `arpc()`, methods 1 and 2.

The **retail MAC** is ISO 9797-1 MAC algorithm 3 with method-2 padding
(`retail_mac()` in the same file). The portal palette group "EMV Crypto (HSM)"
(`packages/scenario-service/models/emv_crypto_catalog.py`) chains these as drag-in
steps: Derive ICC MK → Derive Session Key → Generate/Verify ARQC → Generate/Verify
ARPC. The VISA simulator verifies inbound ARQCs issuer-style and answers with
an ARPC (§6.1).

**On the wire (ADR-0013).** Two things ride on the bytes codec of ADR-0011:

- *Message authentication*: a `mac` block (Message Format `definition.mac`, or
  the same keys on a connection / simulator config, which wins) puts a retail
  MAC or truncated AES-CMAC (8 or 4 bytes; DE 64 / 128 are 64-bit fields) over
  **every wire byte before the MAC field**, so the same message MACs differently
  under ASCII and binary. Contract in `payprobe_common/iso8583/mac.py`
  (`pack_with_mac`, `verify_mac`), algorithms bound in
  `worker/adapters/tcp/iso8583.py` (`MAC_ALGORITHMS`). The adapter reports
  `mac_verified` / `mac_error`; the responder treats a bad or missing MAC as a
  dialect violation (`on_failure`: `warn` records, `reject` answers DE 39 `30`).
- *EMV awareness*: `tag_map(de55)` (`payprobe_common/iso8583/tlv.py`) gives the
  `{tag: hex}` view that decoded messages expose as `emv`, that responder rules
  match with `when.emv`, and that the VISA simulator uses to verify tag `9F26`
  over the message's own tags (CVN 10/18 order by default) with a given session
  key or one derived from an MDK (`emv_icc_mk` → `emv_session_key`), returning
  tag `91` (ARPC method 1 || ARC) when configured.

### 2.4 AIP / TVR / TSI

- **AIP** (tag 82, 2 bytes): what the *card* supports (SDA/DDA/CDA, cardholder
  verification, etc.) — decoder snippet `_AIP` in `emv_catalog.py`.
- **TVR** (tag 95, 5 bytes): what the *terminal* observed/failed during processing —
  decoder snippet `_TVR` (bit meanings incl. "Default TDOL used", "Issuer
  authentication failed").
- **TSI** (tag 9B): which processing steps were performed. Present in the tag
  dictionary; **no dedicated bit-decoder snippet exists** (only AIP and TVR have
  decoders).

Tests exercising the crypto chain: `packages/worker/tests/test_engine.py` (crypto
tools), `packages/worker/tests/test_visa_simulator.py` (ARQC verification path).

---

## 3. PIN security — PIN blocks, PVV, CVV

### 3.1 ISO 9564 PIN blocks — format 0 ONLY

An (ISO-0 / "format 0") PIN block XORs a PIN field (`0` + PIN length nibble + PIN,
padded with `F`) with a PAN field (`0000` + rightmost 12 PAN digits *excluding* the
check digit), then encrypts the 8-byte result under a PIN key.
Implemented in `packages/worker/engine/crypto_tools.py`: `_pin_field`, `_pan_field`,
`pin_block_encode`, `pin_block_decode`.

**Gap — be precise:** only **format 0** is implemented. ISO 9564 formats 1, 2, 3 are
NOT implemented, and format 4 (the AES PIN block) is absent entirely
(`docs/standards-gap-analysis.md`). The payShield simulator commands read the 2-digit
format codes off the wire but ignore them and process ISO-0.

### 3.2 PVV — Visa PIN Verification Value

A 4-digit value derived from PAN + PIN + PVKI under a PVK pair; the issuer stores the
PVV and re-derives it to verify a PIN without storing the PIN. `pvv()` in
`crypto_tools.py`; verified by the payShield `EC` command and by `VisaSimulator`'s
optional `verify_pvv` block. Test: `packages/worker/tests/test_dukpt_pvv.py`.

### 3.3 CVV / CVC / CVV2

Card verification value derived from PAN + expiry + service code under a CVK pair
(`cvv()` in `crypto_tools.py`). Same algorithm family covers magstripe CVV and CVV2
(different service-code/expiry ordering conventions at call sites). Used by payShield
`CW`/`CY` and `VisaSimulator` `verify_cvv2` (declines with VISA code `N7` on
mismatch).

---

## 4. DUKPT — Derived Unique Key Per Transaction (ANSI X9.24-1, TDES)

The terminal-key-management scheme: a terminal never stores a long-term PIN key.

- **BDK** — Base Derivation Key, held by the acquirer/HSM.
- **KSN** — Key Serial Number, 24 hex: 16-hex initial-key-id base + a **21-bit
  transaction counter** in the low bits (`_DUKPT_KSN_COUNTER_BITS`).
- **IPEK** — Initial PIN Encryption Key, injected into the terminal, derived from
  BDK + KSN: `dukpt_ipek(bdk_hex, ksn_hex)`.
- Per transaction, the terminal derives a fresh transaction key from IPEK + KSN
  counter, then XORs a **variant mask** to get the working key (`DUKPT_VARIANTS`:
  `pin`, `mac_req`, `mac_resp`, `data_req`). The host re-derives the identical key
  from BDK + KSN — the clear key never leaves an HSM.

All in `packages/worker/engine/crypto_tools.py` (from `_DUKPT_REG_MASK` through
`dukpt_pin_block`). Test: `packages/worker/tests/test_dukpt_pvv.py`.

**Load-test integration** — `packages/worker/engine/generators.py` provides per-
transaction template variables for high-volume runs:

| Variable | Yields |
|---|---|
| `${seq.ksn}` | a fresh DUKPT KSN per transaction (default base `3039505912345678`, 8-hex incrementing counter) |
| `${seq.ksn(<base16hex>)}` | same with a custom initial-key-id base |
| `${card.pan}` `.expiry` `.cvv` `.type`/`.brand` `.track2` `.seq` | fields of the card bound to the current transaction (rotates per transaction from the card pool) |

---

## 5. HSM concepts — and the payShield 10K simulator

An **HSM** (Hardware Security Module) is a tamper-resistant box that performs payment
crypto so clear keys never exist in host memory. The host sends short ASCII
**host commands**; every working key travels as a **key token** encrypted under the
HSM's **LMK** (Local Master Key).

### 5.1 The test LMK and key tokens

`packages/worker/adapters/hsm/lmk.py`: a key token is a one-char **scheme tag** +
hex ciphertext — `Z` single-length DES, `U` double-length TDES, `T` triple-length
TDES. The simulator wraps/unwraps with a single fixed **test LMK**
(`DEFAULT_LMK = 0123456789ABCDEFFEDCBA9876543210`, overridable per simulator).
Key-type **variants** (`KEYTYPE_VARIANT` in `packages/worker/adapters/hsm/lmk.py`)
give only PARTIAL key separation: type codes 000/001/002/008/302 (ZMK/ZPK/TPK/ZAK/BDK)
all map to variant 0 and are NOT separated from each other; only CVK (402 → variant 4)
and MK-AC (109 → variant 1) are variant-separated. A real payShield separates far more
strictly — don't infer production behavior from this simulator. Crypto fidelity is **hybrid**: tokens only round-trip inside
this simulator (they will not interoperate with a physical payShield), but KCVs,
CVV/PVV, PIN blocks and MACs are computed from the clear key, so values are
cryptographically correct and verifiable with independent tools.

### 5.2 Wire protocol

Length-prefixed frame: `header + command(2 chars) + data`; reply
`header + response_code + error_code + data`. The **response code is the command
with its second character incremented** (`A0→A1`, `NC→ND` — `response_code()` in
`commands.py`). The header is a host-chosen correlation id echoed verbatim — that is
what lets the client pipeline many in-flight commands (`HSMAdapter`,
`packages/worker/adapters/hsm/adapter.py`). Error codes: `00` OK, `01` verification
failed, `10` parity, `15` invalid data, `30` unknown command, `68` disabled.

### 5.3 Implemented host commands (`packages/worker/adapters/hsm/commands.py`)

| Cmd | Does |
|---|---|
| `NC` | Diagnostics — LMK check value + firmware string (default `0007-E000`) |
| `A0` | Generate key under LMK (optional export under a ZMK/TMK) |
| `BU` | Key check value (KCV) of an LMK-encrypted key |
| `CW` / `CY` | Generate / verify CVV/CVC |
| `CA` | Translate PIN block TPK → ZPK (ISO-0) |
| `EC` | Verify interchange PIN via PVV |
| `M6` / `M8` | Generate / verify retail MAC |
| `CC` | Translate PIN block ZPK → ZPK |
| `A6` | Import a key encrypted under a ZMK (re-wrap under LMK) |
| `K8` | Export a key under a KEK/ZMK (unwrap from LMK, re-encrypt under KEK) |
| `G0` | Translate a PIN block from BDK (3DES DUKPT) to ZPK encryption |
| `KQ` | ARQC verification and/or ARPC generation (static / Mastercard SKD) |
| `NO` | HSM status (mode 00: buffer/ethernet/sockets/firmware; mode 01: PCI-HSM flag) |

Full set as of 2026-07-06: **15 commands** (NC A0 A6 BU CA CC CW CY EC G0 K8 KQ M6 M8 NO)
— recount with the provenance grep before trusting this table.

Per-command scripted overrides and disabled-command sets are supported
(`HsmContext.overrides` / `disabled_commands`).

### 5.4 Where HSM things live

Simulator: `packages/worker/adapters/hsm/payshield.py` (`PayShieldSimulator`, a
`TcpResponder` subclass; default framing 2-byte big-endian length prefix, ASCII;
portal "payShield 10K" preset). Client: `packages/worker/adapters/hsm/adapter.py`
(action names like `generate_cvv`, `verify_pin`, `generate_mac`; connection pool +
pipelining). Docs: `docs/simulators/payshield-10k.md`,
`docs/simulators/payshield-hsm-reference.md`. MCP tools:
`start_payshield_simulator`, `hsm_command`, `run_hsm_example`
(`packages/mcp-server/mcp_server/tools.py`). Tests:
`packages/worker/tests/test_payshield_sim.py`, `test_payshield_e2e.py`,
`test_hsm_client.py`.

---

## 6. Scheme flows — authorization, clearing, reversal, network management

Four flow families you must keep apart (the MTI class digit encodes them):

- **Authorization** — "may this transaction proceed?" (010x auth-only, 020x
  financial request that also posts).
- **Reversal** — undo/void a prior authorization (040x request, 042x advice =
  "already done, informing you").
- **Clearing** — the money actually moves, usually batch/advice level (022x/052x
  here; full Base II batch formats are out of scope).
- **Network management** — session plumbing: sign-on, sign-off, echo test
  (080x, code in **DE 70**).

### 6.1 VISA Base I — `VisaSimulator` (`packages/worker/adapters/scheme/visa.py`)

Functional Base I simulator built on the public 1987 structure; **not** byte-exact
V.I.P./Base I member specs (DE 62/63 are opaque echo fields). A `TcpResponder`
subclass — same framing/codec, VISA-specific reply decision. Flows: `0100/0110`,
`0200/0210`, `0400/0410`, `0420/0430`, `0800/0810` (echoes DE 70), `0220/0230`,
`0520/0530`. Decision knobs: `stand_in` (STIP = the scheme answering on the
issuer's behalf; when false, auths decline `91` issuer-unavailable), `decline_over`
(DE 4 limit → `61`), `block_bins` (DE 2 prefix → `05`), `expiry_check` (DE 14 →
`54`). Opt-in real crypto verification blocks: `verify_cvv2` (decline `N7`),
`verify_pvv`, `verify_arqc` — each activates only when its key material is
configured, backed by `crypto_tools`. DE table: builtin format `visa-base1`.
Docs: `docs/simulators/visa-scheme.md`. Tests: `packages/worker/tests/test_visa_simulator.py`.

### 6.2 CyberSource REST — `CyberSourceSimulator` (`packages/worker/adapters/scheme/cybersource.py`)

The REST counterpart (gateway, not scheme wire): subclasses `HttpResponder`
(`packages/worker/adapters/http/responder.py` — first HTTP-based simulator base).
Functional model of the public CyberSource Payments REST contract, not byte-exact
processor codes. Flows:

| Flow | Route |
|---|---|
| Authorization (opt. auth+capture) | `POST /pts/v2/payments` |
| Capture | `POST /pts/v2/payments/{id}/captures` |
| Refund | `POST /pts/v2/payments/{id}/refunds`, `POST /pts/v2/captures/{id}/refunds` |
| Auth reversal | `POST /pts/v2/payments/{id}/reversals` |
| Void | `POST /pts/v2/{payments|captures|refunds}/{id}/voids` |
| Retrieve | `GET /pts/v2/payments/{id}` |

Status ladder: explicit `rules` win, then `block_bins` → DECLINED(DO_NOT_HONOR),
expiry → DECLINED(EXPIRED_CARD), `cvn_decline_values` → DECLINED(CVN_NOT_MATCH),
amount ≥ `decline_over` → DECLINED, ≥ `partial_over` → PARTIAL_AUTHORIZED, else
AUTHORIZED. `require_auth: true` returns 401 without a JWT/HTTP-Signature header.
Tests: `packages/worker/tests/test_cybersource_sim.py`.

---

## 7. Message-flow anatomy in PayProbe terms

- **Initiator** = the side that dials out and sends requests: `TcpAdapter`
  (`packages/worker/adapters/tcp/adapter.py`) — owns socket, background reader,
  request/response **correlation**, optional `sign_on` and `keepalive` (defaulting to
  the protocol's health probe: ISO 8583 ⇒ `0800` echo test; `header_echo` ⇒ its
  probe).
- **Responder** = the side that listens and answers: `TcpResponder`
  (`packages/worker/adapters/tcp/responder.py`) — rules-driven (first matching rule
  wins: match on MTI/DE conditions `eq/prefix/contains/gte…`, reply with
  `set/echo/generate/decline/delay/drop`), plus chaos/fault injection
  (`packages/worker/adapters/tcp/chaos.py`). Simulators (VISA, payShield) subclass it.
- **Framing** = how message boundaries are marked on a TCP stream. Config keys
  (adapter and responder share them): `length_prefix_bytes` (≥1), `length_encoding`
  (`binary` integer, or `ascii` zero-padded digits such as `0043`; added 2026-09-24,
  `packages/worker/adapters/tcp/framing.py` is the one encode/decode), `length_byte_order`
  (`big`/`little`, binary only), `length_includes_header`, `tpdu_bytes` (inbound TPDU
  header to strip), `encoding`. A framing mismatch between two ends is the classic "hangs
  forever / garbage decode" failure — see `payprobe-debugging-playbook`.
- **Protocol** = message content strategy on top of the transport
  (`packages/worker/adapters/tcp/protocols.py`): `iso8583` (correlate on STAN etc.)
  or `header_echo` (host echoes a leading header — HSM-style links).

---

## 8. Jargon glossary

| Term | One-line definition | Repo location |
|---|---|---|
| MTI | 4-digit message type: version/class/function/origin | `iso8583_analyzer.py` `decode_mti` |
| DE / field | numbered data element (2–128) in an 8583 message | `iso_catalog.py` field tables |
| Bitmap | 64-bit presence map; bit 1 ⇒ secondary bitmap for DE 65–128 | `worker/adapters/tcp/iso8583.py` |
| LLVAR/LLLVAR/… | variable-length field with 2/3/4/5-digit length prefix | both codecs (§1.3) |
| STAN | DE 11, System Trace Audit Number — request/response correlation | `protocols.py` iso8583 protocol |
| RRN | DE 37, Retrieval Reference Number | responder `generate: random_rrn` |
| DE 39 | response/action code (`00` approved, `05` do-not-honor, `91` issuer unavailable) | `iso8583_analyzer.py` response-code table |
| DE 55 | ICC (EMV) data as BER-TLV inside 8583 | `iso8583_analyzer.py` `parse_tlv` |
| DE 70 | network-management info code (echo/sign-on/sign-off) | `scheme/visa.py` 0800 handler |
| MessageFormat | a dialect: DE table + MTI list + presence matrix, registry-persisted | `models/message_format.py` |
| BER-TLV | nested tag-length-value encoding (EMV) | `iso8583_analyzer.py` |
| DOL (PDOL/CDOL/TDOL) | tag+length list the card wants values for, in order | `emv_catalog.py` `_DOL_PARSE/_DOL_BUILD` |
| MDK / UDK | issuer master derivation key / per-card ICC master key | `crypto_tools.py` `emv_icc_mk` |
| ATC | Application Transaction Counter — session-key diversifier | `crypto_tools.py` `emv_session_key` |
| ARQC / ARPC | card→issuer / issuer→card application cryptograms | `crypto_tools.py` `arqc`/`arpc` |
| AIP / TVR / TSI | card capabilities / terminal verification results / status info (tags 82/95/9B) | `emv_catalog.py` |
| Retail MAC | ISO 9797-1 alg 3, method-2 padding | `crypto_tools.py` `retail_mac` |
| MAC on DE 64 / 128 | coverage = all wire bytes before the MAC field; 8 or 4 bytes | `payprobe_common/iso8583/mac.py`; bound in `worker/adapters/tcp/iso8583.py` |
| EMV tag map | DE 55 as `{tag: hex}` for rules / responses / ARQC over message tags | `payprobe_common/iso8583/tlv.py` `tag_map`; `VisaSimulator._arqc_check` |
| PIN block (ISO-0) | PIN field XOR PAN field, encrypted under a PIN key | `crypto_tools.py` `pin_block_encode` |
| PVV / PVKI | Visa PIN verification value + key index | `crypto_tools.py` `pvv`; HSM `EC` |
| CVV/CVC/CVV2 | card verification value from PAN+expiry+service code under CVK | `crypto_tools.py` `cvv`; HSM `CW/CY` |
| DUKPT / BDK / IPEK / KSN | unique key per transaction; base key, initial key, key serial number | `crypto_tools.py` DUKPT section |
| HSM / LMK / key token / KCV | crypto appliance; its master key; wrapped working key; key check value | `worker/adapters/hsm/lmk.py` |
| ZMK/ZPK/TPK/TMK/CVK/PVK | zone master/zone PIN/terminal PIN/terminal master/CVV key/PIN-verification key types | `lmk.py` `KEYTYPE_VARIANT` |
| STIP | stand-in processing — scheme answers when issuer is down | `scheme/visa.py` `stand_in` |
| TPDU | transport-protocol header some hosts prepend before the 8583 body | `tcp/adapter.py` `tpdu_bytes` |
| Track 2 / service code | magstripe data: PAN `D` expiry + service code + discretionary | `emv_catalog.py` `_TRACK2` |
| Luhn | mod-10 PAN check digit | `emv_catalog.py` `_LUHN`; BIN→PAN generation in test-data manager |

---

## 9. What PayProbe does NOT implement — labeled gaps

Source: `docs/standards-gap-analysis.md` (written 2026-06-20), re-checked against
code 2026-07-03. Do not claim these capabilities in docs, tests, or positioning
(see `payprobe-external-positioning`).

| Gap | Status 2026-07-03 |
|---|---|
| Binary/BCD/EBCDIC **on the wire** | GAP. Worker TCP codec is ASCII-only. (Nuance: the Inspector/analyzer *has* gained binary/BCD/EBCDIC analyze+build profiles since the gap doc — §1.5 — but no live socket speaks them.) |
| ISO 9564 PIN block formats 1–3 | GAP — only format 0 (ISO-0) exists |
| ISO 9564 format 4 (AES PIN block) | GAP — absent |
| AES anywhere in EMV/keys (AES session keys, AES cryptograms) | GAP — DES/3DES only |
| TR-31 / ISO 20038 key blocks | GAP — no key-block wrap/unwrap |
| XSD validation for ISO 20022 | GAP — XML build/parse only, no schema validation, no version pinning |
| Published-edition ISO 8583 field dictionaries | GAP — tables are hand-maintained "1987-style"/"1993-style" |
| EMVCo L2/L3 conformance mapping | GAP — tooling models the flows, not tied to EMVCo test cases |
| Byte-exact VISA V.I.P. / Base II, exact processor response codes in CyberSource sim | GAP by design — functional fidelity only, documented in each simulator's docstring |
| Real scheme certification packs (VTS/ADVT, M-TIP) | GAP — pack machinery exists, content is generic |

---

## Provenance and maintenance

Authored 2026-07-03 against the live repo; every path/symbol above was verified by
reading the file cited. One-line re-verification commands (run from repo root):

```sh
# ISO 8583 codecs + length types + ASCII-only wire claim
grep -n "lllllvar" packages/worker/adapters/tcp/iso8583.py packages/scenario-service/models/iso8583_analyzer.py
head -20 packages/worker/adapters/tcp/iso8583.py            # still "ASCII"?
grep -n "resolve_encoding\|_BINARY_OPTS" packages/scenario-service/models/iso8583_analyzer.py

# Builtin formats and Inspector endpoints
grep -n "id=\"iso8583" packages/scenario-service/models/message_format.py
grep -n "/iso8583/" packages/scenario-service/api/main.py

# EMV crypto chain + DUKPT + PVV + PIN block
grep -n "def emv_icc_mk\|def emv_session_key\|def arqc\|def arpc\|def dukpt_ipek\|def pvv\|def pin_block_encode" packages/worker/engine/crypto_tools.py

# payShield commands
grep -n "@command(" packages/worker/adapters/hsm/commands.py

# Scheme simulators
grep -n "Supported message flows" -A 8 packages/worker/adapters/scheme/visa.py
grep -n "Supported flows" -A 10 packages/worker/adapters/scheme/cybersource.py

# Load-generator variables
sed -n 1,45p packages/worker/engine/generators.py

# Gaps doc still current?
sed -n 1,40p docs/standards-gap-analysis.md

# Run the suites touching everything above
cd packages && python -m pytest worker/tests scenario-service/tests -q
```

Volatile facts most likely to drift: the ASCII-only wire limitation (binary codec
work would land in `packages/worker/adapters/tcp/iso8583.py`), the builtin format
list, the payShield command set, and the gap table (§9) — re-check
`docs/standards-gap-analysis.md` dates before quoting it.
