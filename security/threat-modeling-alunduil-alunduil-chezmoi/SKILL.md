---
name: threat-modeling
description: Audit, write, or revise a threat model using STRIDE. Use when asked what could go wrong with a system, to threat-model or security-review a design, to enumerate threats against a component or data flow, or to check an existing threat model for coverage gaps or stale mitigation claims. Walks a data flow diagram element by element, pins the threat table as the output artifact, and makes every row cite the code that makes its claim true.
---

# Threat modeling

References:

- <https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats> — STRIDE categories.
- <https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started> — the SDL process.
- <https://learn.microsoft.com/en-us/archive/blogs/larryosterman/threat-modeling-again-what-does-stride-have-to-do-with-threat-modeling> — STRIDE-per-element.
- <https://learn.microsoft.com/en-us/archive/blogs/larryosterman/threat-modeling-again-stride-mitigations> — mitigation classes.

A threat model answers what an attacker can do to a design, before the
design ships. STRIDE is the categorisation that turns that open
question into a finite checklist: for a given design the threats are
static, so walking every element against the categories that apply to
it terminates.

Work from the design. Engineers know their own system better than they
know what an attacker wants from it, and the element walk reaches the
same threats without that guess.

## Input

The model is a data flow diagram with trust boundaries drawn. Its
element list is the enumeration checklist and its element names are the
threat table's row keys, so the diagram has to exist first — invoke the
`dfd` skill when it doesn't.

## Categories

| Category | Violates | Is |
| --- | --- | --- |
| **S**poofing | Authenticity | Using another party's identity — credentials, a signature, an address |
| **T**ampering | Integrity | Malicious modification of data, at rest or in transit |
| **R**epudiation | Non-repudiation | Denying an action the system cannot prove happened |
| **I**nformation disclosure | Confidentiality | Exposure of data to someone not granted access to it |
| **D**enial of service | Availability | Denying service to valid users |
| **E**levation of privilege | Authorisation | An unprivileged party gaining privileged access |

## Element types

Which categories a DFD element is subject to. Enumerate these and stop:

| Element type | Categories |
| --- | --- |
| External entity | S, R |
| Process | S, T, R, I, D, E |
| Data store | T, R, I, D |
| Data flow | T, I, D |

An external entity can be a person: impersonate one and they can deny
having acted, while the rest lies outside the system's reach. Stores
and flows are passive, holding no privilege to elevate. A store
carries repudiation because logs live in stores: flooding one is how a
repudiation attack succeeds, and one is usually the mitigation.

## Mitigations

Where to start per category:

| Category | Mitigation classes |
| --- | --- |
| Spoofing | Authentication — credentials, Kerberos, PKI, IPsec, code signing. Where the caller can bypass the client and call directly, validate the payload server-side instead |
| Tampering | Digital signatures, message authentication codes, access control on the file or key, validation of what is read back |
| Repudiation | Secure logs and audit records, paired with strong authentication |
| Information disclosure | Encryption in transit and at rest, access control |
| Denial of service | Access control against deletion, filter rules, disk and CPU quotas, high-availability design |
| Elevation of privilege | Input validation first, then access control and permission checks |

Validation added as a tampering mitigation can itself deny service —
rejecting corrupt input has to leave the component running.

## Rules

Coverage:

- Analyse every element in the DFD. One held out of scope records why,
  in the same table.
- Every element × category pair from *Element types* gets a row,
  including the pairs that turn out to be nothing. A missing row is
  indistinguishable from an oversight.
- Two threats in one category against one element take two rows.

Fields:

- **Element** names match the DFD exactly. They are the join between
  the two documents.
- **Threat** on a dismissed pair carries the reason — the record that
  the category got considered.
- **Priority** is High, Medium, or Low against what the system's owner
  would actually stop to fix, not absolute severity. A dismissed pair
  carries none.
- **Mitigation** is the concrete mechanism, chosen from the class in
  *Mitigations*. `Mitigated` requires one.
- **Status** is `Not Started` (default), `Needs Investigation`,
  `Not Applicable`, or `Mitigated`. `Needs Investigation` names who or
  what resolves it.
- **Evidence** locates the claim in the system: for `Mitigated`, where
  the mechanism lives; for `Not Applicable`, what makes it
  inapplicable. Cite a path and a symbol — line numbers rot on the next
  edit. A row claiming either status with the cell empty is
  `Needs Investigation` instead.

Currency:

- The model matches the DFD. Adding, removing, or renaming an element
  revisits its rows in the same change.
- Moving or deleting cited code revisits every row citing it.

## Output

One table per DFD level, rows in the diagram's element order:

| Element | Category | Threat | Priority | Mitigation | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0 Decrypt secret | Spoofing | Another local process impersonates the caller and requests decryption | High | Socket peer credential check | Mitigated | `src/ipc.rs`, `verify_peer_uid` |
| 1.0 Decrypt secret | Tampering | In-proc call — modifying the flow needs code already running at the caller's privilege | — | — | Not Applicable | `src/decrypt.rs`, `decrypt_in_place` |
| age identity | Information Disclosure | Identity file readable by any process running as the user | High | — | Not Started | — |

## Location

`docs/explanation/threat-model-<system>.md`, linking to the DFD file it
walks. A threat model explains a system, so it is a Diátaxis
explanation and the `diataxis` skill owns the surrounding prose. It
stays a separate document from the DFD: the diagram answers how the
system works, the model answers what can go wrong with it.

## Procedure

Model:

1. Read the DFD, or draw one with the `dfd` skill. Confirm trust
   boundaries are drawn — a flow crossing one is where the threats
   concentrate.
2. Reconcile the diagram against the code before trusting it as a
   checklist. List the system's entry points, persisted state, and
   outbound calls, and map each to an element. One that maps to nothing
   is a missing element, and a missing element is a whole column of
   threats nobody enumerated — send it back to `dfd`.
3. Take each element in diagram order. For each category *Element
   types* gives it, ask what an attacker positioned outside the nearest
   trust boundary could do.
4. Fill the row's fields per *Rules*, reading the code for each claim.
   The diagram says what to ask about; only the code says what is true.

Check:

1. Walk *Rules* against the result, coverage first.
2. Reconcile the element column against the DFD in both directions.
3. Open every citation and confirm it says what the row claims. One
   that no longer resolves, or no longer shows the mechanism, reopens
   the row as `Needs Investigation`.
