---
name: post-quantum-lord
description: Lord skill for post-quantum cryptography migration — ML-DSA (FIPS 204), ML-KEM (FIPS 203), SLH-DSA (FIPS 205), hybrid schemes, and PQC readiness.
triggers:
  - post quantum lord
  - post quantum
  - ml-dsa
  - ml-kem
  - kyber
  - dilithium
  - quantum safe
  - crypto migration
  - cryptography
  - تشفير كمي
personas:
  - SEC
  - ARCH
  - API
  - DEV
  - DEVOPS
tech_stack:
  - go-1-27
  - rust-1-98
  - python-3-14
lord: true

---

# Post-Quantum Cryptography Lord

[OBJ] Migrate systems to post-quantum cryptography (PQC) using NIST-standardized algorithms (FIPS 203/204/205) and hybrid schemes.

## Problem

Quantum computers will break RSA, ECDSA, and ECDH. NIST standardized PQC algorithms (Aug 2024): ML-KEM (Kyber, FIPS 203), ML-DSA (Dilithium, FIPS 204), SLH-DSA (SPHINCS+, FIPS 205). Go 1.27, Rust, OpenSSL 3.5+ now ship PQC primitives. Migration is a multi-year effort — start now with hybrid schemes.

## Rules

1. [REQ] **Know the NIST PQC standards:**
   - **ML-KEM** (FIPS 203) — Key Encapsulation Mechanism (replaces ECDH for key exchange)
   - **ML-DSA** (FIPS 204) — Digital Signature Algorithm (replaces RSA/ECDSA)
   - **SLH-DSA** (FIPS 205) — Hash-based signatures (slow but conservative, fallback)
2. [REQ] **Use hybrid schemes during migration.** Combine classical (X25519/Ed25519) + PQC (ML-KEM-768/ML-DSA-65) for transition period. `X25519Kyber768Draft00` for TLS, `Ed25519+ML-DSA-65` for signatures.
3. [REQ] **Use `crypto/mldsa` in Go 1.27+** for ML-DSA signatures: `mldsa.GenerateKey()`, `mldsa.Sign()`, `mldsa.Verify()`. Prefer over hand-rolled PQC.
4. [REQ] **Use OpenSSL 3.5+** for PQC in C/C++/Python: `EVP_PKEY_CTX_new_from_name(NULL, "ML-KEM-768", NULL)`.
5. [REQ] **TLS 1.3 + PQC hybrid.** Use `SSL_CTX_set1_groups_list` with `X25519Kyber768Draft00` (or `MLKEM768`) for post-quantum TLS. Supported in OpenSSL 3.5+, BoringSSL, AWS s2n.
6. [REQ] **Larger key/signature sizes.** ML-DSA-65: pk=1952B, sig=3293B (vs Ed25519: pk=32B, sig=64B). Plan storage, bandwidth, database schema changes.
7. [REQ] **Crypto-agility.** Abstract crypto behind interfaces so algorithms can be swapped without code changes. `KeyAlgorithm` enum, `SignatureScheme` enum.
8. [REQ] **Inventory crypto assets.** Identify all RSA, ECDSA, ECDH usage: TLS certs, JWT signing, code signing, SSH, VPN, database encryption, backups.
9. [REQ] **Prioritize by exposure.** Long-lived secrets (TLS certs, code signing) first — these are harvest-now-decrypt-later targets. Short-lived tokens last.
10. [REQ] **Test PQC interop.** Use `OQS OpenSSL` provider or `PQC-Net` test vectors. Verify cross-implementation compatibility.
11. [REQ] **HSM support.** Verify HSMs support PQC algorithms before migration. Most HSMs (YubiHSM, Thales, Utimaco) added ML-DSA/ML-KEM in 2025-2026 firmware.
12. [PROHIBIT] Never roll your own PQC implementation — use stdlib (Go `crypto/mldsa`), OpenSSL, liboqs, or BoringSSL.
13. [PROHIBIT] Never use pure PQC without hybrid during transition — classical fallback needed for crypto-agility.
14. [PROHIBIT] Never assume PQC is quantum-resistant forever — monitor for cryptanalysis breakthroughs.

## Migration Timeline

- **2024-2026**: NIST standards published, libraries add support (Go 1.27, OpenSSL 3.5, Rust pqc crate)
- **2026-2028**: Hybrid adoption for long-lived secrets (TLS certs, code signing)
- **2028-2030**: Pure PQC for new systems, deprecate classical for long-lived
- **2030+**: Quantum computers reach cryptographically relevant scale — classical broken

## Commands

- Go: `go get crypto/mldsa` (stdlib in 1.27+)
- Rust: `cargo add pqc` or `cargo add oqs`
- Python: `pip install liboqs-python` or use `cryptography` 45+ (OpenSSL 3.5 backend)
- OpenSSL: `openssl genpkey -algorithm ML-KEM-768`

## References

- https://csrc.nist.gov/projects/post-quantum-cryptography
- https://pkg.go.dev/crypto/mldsa
- https://openquantumsafe.org/
- https://datatracker.ietf.org/wg/pquip/documents/
