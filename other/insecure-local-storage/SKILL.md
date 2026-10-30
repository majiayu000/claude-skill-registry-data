---
name: insecure-local-storage
description: Detects sensitive data written to unprotected local files, preference stores,
  or SQLite. Use when writing code that stores sensitive data (credentials,
  tokens, PII) to local files, platform preference stores (NSUserDefaults,
  SharedPreferences, UserDefaults), SQLite databases, or localStorage without
  encryption at rest.
---

# Insecure Local Data Storage (A02:2025)

## What this checks

Detects sensitive data written to unprotected local storage. Cleartext storage lets any
process with file-system access, or a device backup restore, harvest credentials and
tokens without authentication.

## Vulnerable patterns

- Credentials or tokens written to a plain file (JSON, INI, dotfile) without encryption
- Sensitive values written to an unencrypted platform preference store such as Android `SharedPreferences`, iOS `UserDefaults`, or Windows registry
- Long-lived auth token placed in browser `localStorage` or `sessionStorage` where any script on the origin can read it
- SQLite or other embedded database storing credentials with no at-rest encryption
- Temp files containing secrets written to a world-readable directory with default permissions and not deleted on completion

## Fix immediately

Flag the vulnerable code and explain the risk. Translate the principles below to the
audited file's platform and language — use that platform's documented secure-storage
API (keychain, EncryptedSharedPreferences, DPAPI, HttpOnly cookie, etc.).

For each finding, establish these properties:

1. **Sensitive values go to platform-managed secure storage, not a plain file or
   pref store.** OS keychain, Android `EncryptedSharedPreferences`, Windows DPAPI
   or Credential Manager, Linux secret service. These encrypt at rest and scope
   access to the owning process.
2. **Web clients do not store long-lived credentials in `localStorage` or
   `sessionStorage`.** These are readable by any script on the origin — one XSS
   and the token is gone. Use a Secure, HttpOnly, SameSite cookie for session
   tokens, or a short-lived in-memory token refreshed from the server.
3. **If secure storage is unavailable, data is encrypted with a key that also
   lives in secure storage** — not hardcoded, not in the same file, not derived
   from device-static values. Symmetric encryption with a keychain-held key is
   the baseline.
4. **Temp files for sensitive data are avoided**, or created with restrictive
   user-only permissions, written to a user-only directory, and deleted in a
   finally/cleanup block — never left in a world-writable directory with default
   permissions.

## Verification

- [ ] No credentials, tokens, or PII written to plain files or standard preference stores
- [ ] Platform secure storage API used (keyring, Keychain, EncryptedSharedPreferences, DPAPI, or equivalent for the platform)
- [ ] Temp files with sensitive data use secure deletion or are avoided entirely

## References

- CWE-312 ([Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html))
- CWE-922 ([Insecure Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/922.html))
- [OWASP A02:2025 Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [OWASP Mobile M9:2024 Insecure Data Storage](https://owasp.org/www-project-mobile-top-10/)
