---
name: wycheproof
type: domain
description: >
  Wycheproof provides test vectors for validating cryptographic implementations.
  Use when testing crypto code for known attacks and edge cases.
---

# Wycheproof

Wycheproof is an extensive collection of test vectors designed to verify the correctness of cryptographic implementations and test against known attacks. Originally developed by Google, it is now a community-managed project where contributors can add test vectors for specific cryptographic constructions.

## Background

### Key Concepts

| Concept | Description |
|---------|-------------|
| Test vector | Input/output pair for validating crypto implementation correctness |
| Test group | Collection of test vectors sharing attributes (key size, IV size, curve) |
| Result flag | Indicates if test should pass (valid), fail (invalid), or is acceptable |
| Edge case testing | Testing for known vulnerabilities and attack patterns |

### Why This Matters

Cryptographic implementations are notoriously difficult to get right. Even small bugs can:
- Expose private keys
- Allow signature forgery
- Enable message decryption
- Create consensus problems when different implementations accept/reject the same inputs

Wycheproof has found vulnerabilities in major libraries including OpenJDK's SHA1withDSA, Bouncy Castle's ECDHC, and the elliptic npm package.

## When to Use

**Apply Wycheproof when:**
- Testing cryptographic implementations (AES-GCM, ECDSA, ECDH, RSA, etc.)
- Validating that crypto code handles edge cases correctly
- Verifying implementations against known attack vectors
- Setting up CI/CD for cryptographic libraries
- Auditing third-party crypto code for correctness

**Consider alternatives when:**
- Testing for timing side-channels (use constant-time testing tools instead)
- Finding new unknown bugs (use fuzzing instead)
- Testing custom/experimental cryptographic algorithms (Wycheproof only covers established algorithms)

## Quick Reference

| Scenario | Recommended Approach | Notes |
|----------|---------------------|-------|
| AES-GCM implementation | Use `aes_gcm_test.json` | 316 test vectors across 44 test groups |
| ECDSA verification | Use `ecdsa_*_test.json` for specific curves | Tests signature malleability, DER encoding |
| ECDH key exchange | Use `ecdh_*_test.json` | Tests invalid curve attacks |
| RSA signatures | Use `rsa_*_test.json` | Tests padding oracle attacks |
| ChaCha20-Poly1305 | Use `chacha20_poly1305_test.json` | Tests AEAD implementation |

## Testing Workflow

```
Phase 1: Setup                 Phase 2: Parse Test Vectors
┌─────────────────┐          ┌─────────────────┐
│ Add Wycheproof  │    →     │ Load JSON file  │
│ as submodule    │          │ Filter by params│
└─────────────────┘          └─────────────────┘
         ↓                            ↓
Phase 4: CI Integration        Phase 3: Write Harness
┌─────────────────┐          ┌─────────────────┐
│ Auto-update     │    ←     │ Test valid &    │
│ test vectors    │          │ invalid cases   │
└─────────────────┘          └─────────────────┘
```

## Repository Structure

The Wycheproof repository is organized as follows:

```text
┣ 📜 README.md       : Project overview
┣ 📂 doc             : Documentation
┣ 📂 java            : Java JCE interface testing harness
┣ 📂 javascript      : JavaScript testing harness
┣ 📂 schemas         : Test vector schemas
┣ 📂 testvectors     : Test vectors
┗ 📂 testvectors_v1  : Updated test vectors (more detailed)
```

The essential folders are `testvectors` and `testvectors_v1`. While both contain similar files, `testvectors_v1` includes more detailed information and is recommended for new integrations.

## Supported Algorithms

Wycheproof provides test vectors for a wide range of cryptographic algorithms:

| Category | Algorithms |
|----------|------------|
| **Symmetric Encryption** | AES-GCM, AES-EAX, ChaCha20-Poly1305 |
| **Signatures** | ECDSA, EdDSA, RSA-PSS, RSA-PKCS1 |
| **Key Exchange** | ECDH, X25519, X448 |
| **Hashing** | HMAC, HKDF |
| **Curves** | secp256k1, secp256r1, secp384r1, secp521r1, ed25519, ed448 |

## Reference material

**[references/implementation.md](references/implementation.md)** — test file structure and the implementation guide

**[references/vulnerabilities.md](references/vulnerabilities.md)** — vulnerability classes detected, a case study, and advanced usage

## Related Skills

### Tool Skills

| Skill | Primary Use in Wycheproof Testing |
|-------|-----------------------------------|
| **pytest** | Python testing framework for parameterized tests |
| **mocha** | JavaScript testing framework for test generation |
| **constant-time-testing** | Complement Wycheproof with timing side-channel testing |
| **cryptofuzz** | Fuzz-based crypto testing to find additional bugs |

### Technique Skills

| Skill | When to Apply |
|-------|---------------|
| **coverage-analysis** | Ensure test vectors cover all code paths in crypto implementation |
| **property-based-testing** | Test mathematical properties (e.g., encrypt/decrypt round-trip) |
| **fuzz-harness-writing** | Create harnesses for crypto parsers (complements Wycheproof) |

### Related Domain Skills

| Skill | Relationship |
|-------|--------------|
| **crypto-testing** | Wycheproof is a key tool in comprehensive crypto testing methodology |
| **fuzzing** | Use fuzzing to find bugs Wycheproof doesn't cover (new edge cases) |

## Skill Dependency Map

```
                    ┌─────────────────────┐
                    │    wycheproof       │
                    │   (this skill)      │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  pytest/mocha   │ │ constant-time   │ │   cryptofuzz    │
│ (test framework)│ │   testing       │ │   (fuzzing)     │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │   Technique Skills       │
              │ coverage, harness, PBT   │
              └──────────────────────────┘
```

## Resources

### Official Repository

**[Wycheproof GitHub Repository](https://github.com/C2SP/wycheproof)**

The official repository contains:
- All test vectors in `testvectors/` and `testvectors_v1/`
- JSON schemas in `schemas/`
- Reference implementations in Java and JavaScript
- Documentation in `doc/`

### Real-World Examples

**[pycryptodome](https://pypi.org/project/pycryptodome/)**

The pycryptodome library integrates Wycheproof test vectors in their test suite, demonstrating best practices for Python crypto implementations.

### Community Resources

- [C2SP Community](https://c2sp.org/) - Cryptographic specifications and standards community maintaining Wycheproof
- Wycheproof issues tracker - Report bugs in test vectors or suggest new constructions

## Summary

Wycheproof is an essential tool for validating cryptographic implementations against known attack vectors and edge cases. By integrating Wycheproof test vectors into your testing workflow:

1. Catch subtle encoding and validation bugs
2. Prevent signature malleability issues
3. Ensure consistent behavior across implementations
4. Benefit from community-contributed test vectors
5. Protect against known cryptographic vulnerabilities

The investment in writing a reusable testing harness pays dividends through continuous validation as new test vectors are added to the Wycheproof repository.
