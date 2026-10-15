---
name: radix
description: Canonical Radix & Positional Numeral Notation Registry and Transcoding Engine. Map 43 known radices (Base 1 to 360), perform arbitrary base conversions, encode/decode HUMMBL Base120 PIN-CODE-RESY coordinates, and identify candidate notation formats.
version: 0.1.0
execution-mode: advisory
argument-hint: "<command> [args...]"
category: cognitive
status: candidate
---
# Radix & Positional Numeral Notation Registry

A canonical mathematical, computational, and governance radix registry mapping 43 distinct radices and positional notations (Base 1 through Base 360), with native transcoding and first-class support for HUMMBL Base120 (PIN-CODE-RESY coordinates).

Governed by: `scripts/radix.py` (stdlib-only, Python 3.11+, zero external dependencies).

## Usage

```bash
[radix] list                               # List all 43 registered radices
[radix] list --category binary_to_text     # Filter by category
[radix] info base120                       # Inspect metadata, divisors, totient, and alphabet
[radix] convert 255 --from dec --to hex    # Transcode decimal 255 to hex (ff)
[radix] convert 255 --from dec --to b120   # Transcode decimal 255 to Base120 (P3.P16)
[radix] convert 11111111 --from bin --to dna # Transcode binary to DNA Base-4 (TTTT)
[radix] convert 703 --from dec --to bijective_base26 # Spreadsheet column (AAA)
[radix] b120 12345                         # Encode decimal 12345 to Base120 (SY3.SY6)
[radix] b120 SY3.SY6                       # Decode Base120 coordinates to decimal 12345
[radix] identify P1.CO5                    # Heuristically detect radix and decode value
```

## Categories Mapped (43 Radices)

1. **Standard Positional**: Unary (1), Binary (2), Ternary (3), Quaternary (4), Quinary (5), Senary (6), Septenary (7), Octal (8), Nonary (9), Decimal (10), Undecimal (11), Duodecimal/Dozenal (12), Tetradecimal (14), Hexadecimal (16), Vigesimal (20), Tetravigesimal (24), Base26 (26), Trigesimal (30), Base36 (36), Sexagesimal (60), Base94 (94), Base256 (256).
2. **Binary-to-Text & Data Encoding**: DNA Base-4 (`ACGT`), RFC 4648 Base32, Base32 Hex, Crockford Base32, z-base-32, Geohash Base32, RFC 9285 Base45, Bitcoin Base58, Flickr Base58, Ripple Base58, Base62, RFC 4648 Base64, URL-Safe Base64, Adobe Ascii85, RFC 1924 IPv6 Base85, ZeroMQ Z85, basE91.
3. **Bijective Numeral Systems**: Bijective Base-26 (Spreadsheet column notation `1->A`, `26->Z`, `27->AA`, `702->ZZ`; zero-less positional mapping).
4. **Non-Standard & Signed**: Balanced Ternary (`{-1, 0, +1}` mapped to `{T, 0, 1}`, Setun computer architecture).
5. **Geometric / Astronomical**: Base 360 ($360 = 2^3 \cdot 3^2 \cdot 5$, 24 divisors, circular rotational degree space).
6. **HUMMBL Governed Radix**: Base120 ($5! = 120 = 2^3 \cdot 3 \cdot 5$, 16 divisors, full PIN-CODE-RESY coordinate mapping + 120-symbol deterministic alphabet).

## The HUMMBL Base120 Coordinate Basis

Base120 functions as the mathematical radix for HUMMBL intelligence and agent reasoning. It organizes 120 discrete operator positions into 6 transformations (20 operators each):

$$\mathbf{PIN-CODE-RESY} = 6 \text{ Families} \times 20 \text{ Operators} = 120 \text{ Positions}$$

| Prefix | Family | Focus | Operator Range | Radix Range |
|:---:|:---:|:---:|:---:|:---:|
| **P** | Perspective | Point of view, framing, assumptions | P1 – P20 | 0 – 19 |
| **IN** | Inversion | Counterfactuals, edge cases, premortems | IN1 – IN20 | 20 – 39 |
| **CO** | Composition | Integration, synthesis, combining parts | CO1 – CO20 | 40 – 59 |
| **DE** | Decomposition | Analysis, orthogonal factor isolation | DE1 – DE20 | 60 – 79 |
| **RE** | Recursion | Self-reference, loops, compounding | RE1 – RE20 | 80 – 99 |
| **SY** | Systems | Macro constraints, emergent behavior | SY1 – SY20 | 100 – 119 |

### Multi-Digit Positional Coordinates

Any integer $N \ge 0$ is uniquely expressed in positional Base120 notation as dot-delimited operator coordinates:
$$N = \sum_{k=0}^{M} d_k \cdot 120^k \quad \text{where } d_k \in [0, 119]$$

* Decimal `0` $\to$ `P1`
* Decimal `44` $\to$ `CO5`
* Decimal `120` $\to$ `P2.P1` ($1 \cdot 120^1 + 0 \cdot 120^0$)
* Decimal `255` $\to$ `P3.P16` ($2 \cdot 120^1 + 15 \cdot 120^0$)
* Decimal `12345` $\to$ `SY3.SY6` ($102 \cdot 120^1 + 105 \cdot 120^0$)

## Execution Mechanics

This skill invokes `scripts/radix.py` via Python:

```bash
python scripts/radix.py $ARGUMENTS
```

All operations are stdlib-only, non-mutating (advisory), and execute in under 10ms.
