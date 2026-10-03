---
name: ad-environment-constraints
description: >
  Real-world Active Directory environment constraints that silently break attacks when
  ignored: NTLM disabled (Kerberos fallback), AES-only KDCs (RC4 blocked by GPO), LDAP
  signing and channel binding requiring LDAPS on 636, Kerberos clock skew (KRB_AP_ERR_SKEW),
  SPNs that must be FQDNs never short names or IPs (the misleading invalidCredentials),
  Protected Users / LAPS / gMSA / MachineAccountQuota, LDAP 1000-object paging, and VPN
  latency. Use this whenever a bind, TGT request, LDAP query, or SMB negotiation fails in a
  way that looks like bad credentials but is really hardening, or before running any AD
  tooling against a domain you have not fingerprinted. Standard-tooling knowledge (netexec,
  impacket, certipy, bloodyAD, kerbrute), no vendor-specific engine.
---

# AD Environment Constraints

Code and commands that work in a lab break in a hardened domain, and the failure almost
never says what it is. A Kerberos SPN mismatch surfaces as `invalidCredentials`. NTLM
being disabled surfaces as a logon failure. AES-only KDCs reject your RC4 request with an
etype error you have to know to read. This skill is the checklist of those constraints and
how to survive each one with standard tooling.

**Detect the posture before you authenticate.** Every constraint below is detectable up
front: probe whether NTLM answers, whether the KDC accepts RC4, whether LDAP signing is
required, whether LDAPS is listening. Fingerprint first, then choose your auth path to
match. Fixing an auth path reactively after each failure is slower and noisier than
reading the environment once and picking the right transport from the start.

---

## 1. Authentication protocol: NTLM may be disabled

NTLM can be turned off org-wide or on specific DCs by GPO. Any auth path that assumes
NTLM must fall back to Kerberos.

- impacket: add `-k` (use Kerberos) and `-no-pass` when you have a ccache/TGT.
- netexec: `-k` / `--kerberos`.
- certipy: `-k` / add `--dc-host <fqdn>` so it targets the KDC by name.

```bash
# NTLM path
nxc smb dc01.corp.local -u user -p pass
# Kerberos path (NTLM disabled): request a TGT, export ccache, reuse it
getTGT.py corp.local/user:pass -dc-ip <dc_ip>
export KRB5CCNAME=user.ccache
nxc smb dc01.corp.local -u user -k --use-kcache
```

**Reading the signal, not guessing it.** A healthy NTLM-enabled DC answers an NTLM bind
with a *bogus* password with exactly `invalidCredentials` / logon-denied, and that proves
NTLM is alive (the DC reached credential verification and rejected the password). Do not
infer "NTLM disabled" from a failed bind with a wrong password. NTLM is actually disabled
only when you see the SSP collapse markers (`STATUS_NTLM_BLOCKED`, unsupported-function),
or when a bind fails as logon-denied *while a valid Kerberos TGT for the same identity
succeeds concurrently*. Only then is "wrong password" ruled out as the cause.

If a tool only supports pass-the-hash (NTLM hash), treat that as an explicit limitation in
an NTLM-disabled environment: it will not work, and no flag fixes it.

---

## 2. AES-only KDCs: RC4 blocked by GPO

Domains migrating off legacy crypto enforce AES-128/AES-256 and reject RC4 (arcfour-hmac).

- Do not force `-cipher rc4` or an explicit `etype 23`. A request that only offers RC4
  fails with `KDC_ERR_ETYPE_NOTSUPP` on an AES-only KDC.
- Let tools negotiate. impacket and netexec negotiate supported etypes by default.
- For roasting, offering RC4 *first* is fine where the KDC still allows it (RC4 hashes
  crack faster); on an AES-only KDC the request simply falls back to AES automatically.
- On AES-only KDCs with a non-standard salt, AES key derivation needs the salt from an
  ETYPE-INFO2 pre-auth probe. Standard clients do this as part of the AS exchange; if you
  hand-roll key derivation you must probe the salt first or the key is wrong.

```bash
# Kerberoast: RC4 preferred where allowed, auto-falls back to AES on an AES-only KDC
GetUserSPNs.py corp.local/user:pass -dc-ip <dc_ip> -request -outputfile hashes.kerberoast
```

---

## 3. LDAP signing, channel binding, and LDAPS

Hardened DCs require signed LDAP or channel-bound LDAPS. Plain LDAP on 389 gets rejected
after the bind with `strongerAuthRequired` / `LDAP_STRONG_AUTH_REQUIRED`.

- Prefer **LDAPS on 636**. It satisfies both signing and channel binding in one move.
- Certipy, bloodyAD and any LDAP-writing tool need `-scheme ldaps` (or the equivalent) when
  channel binding is enforced; a plain LDAP write is refused.
- If only plain LDAP 389 is available and the server demands signing, the client must sign
  the connection (SASL sign/seal). A tool with no signing support cannot talk to that DC;
  that is a hard limitation, document it.

```bash
certipy find -u user@corp.local -p pass -dc-ip <dc_ip> -scheme ldaps
bloodyAD --host dc01.corp.local -d corp.local -u user -p pass --secure get object <target>
```

**Legacy environments without LDAPS.** Not every domain has a cert on the DC. Where 636 is
closed, LDAP 389 is your only channel and it is plaintext; signing is often on to
compensate. Distinguish a *transport* failure (636 closed → connection refused / TLS
handshake error → retry on 389) from a *policy* failure (bind succeeds, then
`strongerAuthRequired` → signing/channel-binding issue, a different fix). A tool that tries
LDAPS and falls back to plain LDAP handles the first case; the second needs signing, not a
port change.

---

## 4. Clock skew: Kerberos requires ≤5 minutes

Kerberos rejects tickets outside a five-minute window with `KRB_AP_ERR_SKEW`. Sync to the
DC before any Kerberos operation.

```bash
sudo ntpdate <dc_ip>            # or rdate -n <dc_ip>
# netexec auto-retries after clock correction on skew errors
```

If a TGT request that should work fails with a skew error, it is your clock, not your
credentials.

---

## 5. Kerberos SPNs: always FQDN, never short name or IP

This is the most misleading failure in AD. A service ticket requested for `ldap/dc01`
(short) or `cifs/10.0.0.1` (IP) does not match the server's canonical SPN, which is the
FQDN. The KDC cannot find the SPN, or the server rejects the AP-REQ, and the client
receives `invalidCredentials` / logon-denied **with no visible Kerberos error**. It looks
exactly like a bad password when the credentials are perfectly valid.

Symptoms of an SPN mismatch (not a credential problem):

- Unauthenticated posture probes pass; the TGT mints without error.
- The LDAP/SMB/RDP/WinRM/MSSQL bind over Kerberos fails as logon-denied.
- No underlying `KRB_AP_ERR_*` in the exception chain.

**Fix:** always target Kerberos by FQDN. Promote short hostnames to FQDN, keep already-formed
FQDNs (including cross-forest suffixes), and if all you have is an IP you must resolve the
real FQDN first; there is no synthetic FQDN that works.

```bash
# WRONG: Kerberos against a short name or IP
nxc smb DC01 -u user -k
nxc smb 10.0.0.1 -u user -k

# RIGHT: full FQDN so the SPN matches
nxc smb dc01.corp.local -u user -k
```

Add the DC to `/etc/hosts` as `<ip> dc01.corp.local dc01` so name resolution never hands a
tool a short label or an IP where an FQDN is required. Do not assume libraries canonicalize
the name via DNS; most do not.

---

## 6. Domain context: authentication domain vs target domain

Confusing these is a top source of cross-domain failure. Keep three things distinct:

| Term | Meaning |
|---|---|
| auth domain | the domain the credential belongs to (where the user lives) |
| target domain | the domain being enumerated or attacked |
| target DC / PDC | the DC of the target domain |

- Point `-d <target_domain>` at the target, not the auth domain.
- Cross-domain over a trust: the credential is from domain A, the target is domain B.
- Cross-domain Kerberos: use the full UPN `user@auth_domain.local` to disambiguate.
- Cross-domain Kerberoasting: `-target-domain <target_domain>` in impacket / netexec.
- BloodHound collection: point the collector at the *target* domain's DC.

In a single-domain lab these coincide, which is exactly why lab-tested commands break in a
multi-domain client.

---

## 7. Protected accounts and special objects

Do not assume a technique that works on a normal account works on every account.

- **Protected Users group**: no RC4, no NTLM, no unconstrained delegation. Delegation
  attacks and RC4 roasting simply do not apply to these members.
- **LAPS**: the local-admin password is a computer-object attribute (`ms-Mcs-AdmPwd` legacy
  / `msLAPS-Password`), readable over LDAP only by principals with the delegated right,
  not a normal credential path.
- **gMSA**: the password is a managed blob (`msDS-ManagedPassword`) retrievable over LDAP
  by authorized principals, not something you spray or crack.
- **AS-REP roasting**: only works against accounts with pre-auth disabled, so verify
  per-account (`DONT_REQUIRE_PREAUTH`), do not assume the whole domain is roastable.
- **MachineAccountQuota (MAQ)**: default 10. RBCD and shadow-credential attacks that create
  a machine account fail when MAQ is 0. Check it before you rely on creating one.

```bash
# LAPS read (authorized principal), gMSA read, MAQ check: all read-only LDAP
nxc ldap dc01.corp.local -u user -p pass -M laps
nxc ldap dc01.corp.local -u user -p pass --gmsa
nxc ldap dc01.corp.local -u user -p pass -M maq
```

---

## 8. LDAP paging: the silent truncation

The DC caps LDAP responses at **1000 objects per page** by default. A query that should
return 50,000 users returns 1,000 and does not warn you. Any query that can return more
than a page must use paged search.

- Standard tools (netexec, impacket, bloodyAD, BloodHound collectors) page automatically.
- If you write a raw LDAP query, use a paged control (`paged_size=1000`) and iterate every
  page. A single unpaged `search` over users/computers is a guaranteed silent truncation in
  any real domain.

A truncated collection produces a truncated attack graph, and you never see the path that
was in the objects you never fetched.

---

## 9. Network latency: do not tune timeouts to your lab

Developers test against a lab on the same subnet: sub-millisecond RTT. Most real
engagements run over a **VPN** at 100-400 ms RTT, sometimes over 500 ms. AD operations are
multi-round-trip, so cost scales with RTT.

| Operation | Round-trips | At 300 ms RTT |
|---|---|---|
| TCP + TLS handshake (LDAPS) | ~2-3 | ~0.6-0.9 s |
| NTLM/SPNEGO bind | ~3 + TLS | ~1.5-2 s |
| Kerberos AS-REQ / TGS-REQ | ~1 each | ~0.3 s each |
| DCSync / DRSUAPI | dozens | several s |

- Size timeouts to a latency budget (`worst-case RTT × round-trips + margin`), not to the
  lab baseline: ~5 s for connect, ~8-10 s for bind, more for heavy RPC, with a hard ceiling
  so a genuinely dead service still fails in reasonable time.
- A `TimeoutError` over VPN means "my budget ran out," not "the DC does not support this."
  Never conclude a constraint (disabled/required) from a timeout; that is a wrong-answer
  cached from a slow link.
- Before widening timeouts, confirm the slowness is the network and not a blocked local
  event loop. If connect measures milliseconds but the high-level operation takes seconds on
  a fast link, the problem is your code, not latency.

---

## Applying this checklist

Match the constraints to what you are doing:

- Anything that authenticates or opens a transport → §§ 1-7.
- Anything that queries many objects → § 8.
- Anything over a remote link → § 9.

Design for the hardest environment on every axis at once: AES-only, no LDAPS, NTLM
disabled, cross-domain, tens of thousands of objects, high latency. Tooling that survives
that also runs against a lab. The reverse is not true.
