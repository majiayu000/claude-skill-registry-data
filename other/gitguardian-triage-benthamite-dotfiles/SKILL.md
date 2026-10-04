---
name: gitguardian-triage
description: Triage and remediate GitGuardian secret incidents. Use for gitguardian/GG triage, secret audit, rotating leaked secrets, processing incidents, or clearing the GitGuardian dashboard.
user-invocable: true
model: opus
---

# GitGuardian triage and remediation

Triage the requested GitGuardian incidents and, when authorized, remediate real
credentials and update their incident status. An audit or classification request
is read-only. A request to rotate named credentials or close a named incident
set supplies authorization for those actions; do not ask for it again. Do not
infer provider rotation, incident closure, or deletion from a read-only audit.

Before handling credentials, read the local secrets context and service-access
routing. Use the personal, Tlön and Epoch 1Password brokers according to those
instructions. Treat matches, replacement keys, provider
responses, and consumer files as sensitive. Keep values out of tool arguments,
process command lines, logs, chat, and screenshots.

## 1. Enumerate and establish the incident set

Use the committed redacting wrapper; it obtains the GitGuardian token internally
and prints a fixed metadata schema:

```bash
"$HOME/My Drive/dotfiles/bin/gitguardian-incidents" list-open
"$HOME/My Drive/dotfiles/bin/gitguardian-incidents" list-closed
"$HOME/My Drive/dotfiles/bin/gitguardian-incidents" get "$id"
```

The wrapper owns the credential locator; use its configured account rather
than duplicating a personal credential-store path in this skill. Check
availability through the wrapper, never by printing the entry. Provision missing access only
when needed, using the secret-handling workflow.

`list-open` includes `TRIGGERED` and `ASSIGNED`; `list-closed` includes
`RESOLVED` and `IGNORED`. Listings deliberately omit occurrence topology.
Targeted `get` returns current detail and every paginated occurrence with
source, SHA, filepath, match positions, and lifecycle evidence, but no match
values. These are the wrapper's only commands; it does not perform mutations.

For a named subset, process only that subset. For a full workspace request,
retain one redacted record per incident and reconcile the enumerated count
against completed, unchanged, and blocked records. Zero open incidents does
not establish that historical credentials are invalid.

## 2. Match exact occurrences

When a repository security audit supplied fingerprints, join each finding to
a targeted occurrence using source, full commit SHA, filepath, and match
position. Retain both incident ID and occurrence ID. A detector, path, or
incident status alone does not establish a match.

A standalone GitGuardian triage does not require a pre-existing audit report.
Start its redacted record from the exact incident and occurrence IDs, source,
SHA, path, and match coordinates. Keep unresolved mappings explicit.

Fetch raw matches only when redacted metadata cannot answer the question.
Create a mode-0700 temporary directory outside sync roots, use a restrictive
umask before writing, and keep secret-bearing files mode 0600. Resolve the exact
occurrence's source content at its recorded revision; never apply historical
coordinates to HEAD. Inspect all named match components required by the detector,
not only `matches[0]`.

Check the API's coordinate semantics for the source type before extraction.
Do not assume offsets are whole-file byte positions: Unicode, diff occurrences,
and pre/post-line locations can change the interpretation. A deleted match may
require the pre-patch image rather than `commit:path`. Validate the extracted
component against the recorded detector/position evidence without printing it.
If the exact source or coordinate interpretation cannot be established, retain
an unresolved mapping rather than probing or rotating a possibly different key.
Obtain missing commits only through an already authorized repository path;
do not clone unrequested repositories or follow API-supplied download URLs.

## 3. Classify using evidence

Use these dispositions, recording the evidence for each:

- **False positive:** content that was never a credential. Candidate examples
  include bibliography titles/DOIs, timestamps or IDs in data, prose, and code
  that references a credential variable without containing its value. Inspect
  the matched context; a detector name or file extension is not enough.
- **Test credential:** a confirmed non-production fixture with no access to a
  deployed service. Strings such as `admin`, `letmein`, or `password123` in
  a compose file can be real credentials and do not establish this disposition.
- **Low risk:** a documented, accepted risk after checking ownership, exposure,
  and actual use. Age, an archive directory, an apparently unused OAuth app, or
  an old Slack note does not prove a credential is dead. Meeting passwords may
  be reused for recurring meetings. Do not ignore those incidents on age alone.
- **Real credential:** investigate current validity, ownership, and consumers;
  rotate or revoke when authorized and necessary.
- **Unknown:** unresolved ownership, validity, source mapping, or consumer
  evidence. Leave an open incident open pending that evidence. When inspecting
  historical closed incidents, report the uncertainty without reopening them
  unless that change is authorized.

Record credential identity, validity, consumer coverage, and incident lifecycle
separately; a real credential can still have unknown validity or incomplete
consumer coverage.

Google Drive client-internal keys are a special ownership case when exact
context identifies Drive.app or File Provider internals, such as anonymous
feedback/survey annotations. They may belong to Google and be non-user-rotatable;
do not generalize that conclusion to arbitrary Google API keys.

GitGuardian's `validity == invalid` is recorded validity, not a fresh provider
probe. It can reflect a customer override; establish its provenance before
attributing it to GitGuardian's checker. `secret_revoked == true` records a
resolver's disposition.
`RESOLVED` and `IGNORED` are workflow states. Preserve the exact
`ignore_reason` when reviewing history, including `invalid` if returned by
the API. Do not turn any of these fields alone into proof of provider revocation.

## 4. Establish ownership and validity

Check ownership before sending a credential to a provider. Notes such as
"<name>'s key", `owner:`, or a setup transcript helping another person are
evidence of possible third-party ownership. Do not test or revoke a
collaborator's credential without authority. Record a contact-owner disposition;
use `personalize` for an authorized draft, and send it only when sending is
explicitly authorized.

Consult current official provider documentation for the credential type's
authentication check. Prefer a read-only endpoint and return only a fixed
classification/status, not raw responses. For example, OpenAI documents
`GET /v1/models`; do not rely on the undocumented `/v1/me` endpoint or an
assumed `email` response. A restricted key may lack permission to list models,
so even a documented endpoint must fit the key's granted permissions.

Read the credential internally from its protected source; do not interpolate it
into curl headers or URLs on the process command line. Providers with token
paths or query parameters need an HTTP client that builds the request in memory,
suppresses credential-bearing exception text, and refuses cross-origin redirects.

Interpret the provider's authentication result, not just the HTTP status:
permission denial, disabled API, wrong project, rate limits, quota exhaustion,
network errors, and malformed requests do not prove revocation. In particular,
a generic 403 is not evidence that a key is invalid. Record inconclusive probes
as such. If no suitable probe exists, preserve the evidence boundary.

## 5. Find and update consumers

Map the service to its credential sources and all active consumers. Literal
search alone misses named fields inside multi-field 1Password items and
indirection through environment variables, auth-source, 1Password, or Keychain.

Check these relevant locations without dumping their contents:

1. Local environment/config assignments, including `.zshenv-secrets`.
2. 1Password items for the service, comparing the actual named field consumed
   by code, not only the primary credential field.
3. Source references to matching item titles or `op://` paths, including
   `auth-source-extras-op-get`, `auth-source-search`, and child-process readers.
4. Direct occurrences in active code/config, excluding archives and transcripts
   from the live-consumer list.
5. `op://` references and runtime broker injection, plus `gh`'s Keychain
   credential where GitHub consumers use it.

Use protected pattern files or in-memory comparisons; output only matching
locations and field names. Avoid broad vault decryption when service metadata
can narrow the search. For Epoch credentials, use the approved 1Password broker
rather than routing them through ambient environment values.
Use the active credential-store configuration and record unreadable entries or
failed searches as coverage gaps; an unsuccessful search does not prove absence.

Before replacing a value, compare the live consumer with the old credential.
Do not overwrite a newer unrelated key. Update only the matching field and
preserve other fields; a match in a subkey must not replace the entry's first
line or all occurrences blindly.

After rotation, repeat the relevant searches for the old value and test the
actual consumer's credential-loading route. Historical transcripts are evidence
of the leak, not consumers to replace with a new live secret.

## 6. Rotate at the provider

Perform the authorized provider operation through the owning account's supported
CLI or available browser/session tools. Follow current provider documentation;
do not select a key solely by token scopes, a display name, or a brittle DOM
selector. Establish the exact key ID/owner and the mapping to the leaked value.

When the provider supports overlapping keys, create and securely store a
replacement, update and test consumers, then revoke the old key. When immediate
revocation is necessary or the provider's regeneration invalidates the old key
at once, account for the outage and verify the consumer after replacement.

Provider-specific details to preserve:

- **GitHub:** update both the matching store fields and the Keychain entry if
  unattended jobs authenticate through `gh` without environment tokens.
  Feed the new token on stdin to
  `env -u GH_TOKEN -u GITHUB_TOKEN gh auth login --with-token`. Verify an
  authenticated read with those variables unset, plus the ordinary consumer
  route. Do not print `gh auth token` or credential-helper passwords.
  Check the existing Git credential helper before changing it.
- **OpenAI/Anthropic:** identify the owning user, organization, project, and key
  ID in the current management surface. Legacy user credentials may require
  their creator. Update only these providers' consumers; GitHub Keychain
  refresh commands are not part of their rotation.
- **Google/Gemini:** use the owning authenticated project/account. Capture any
  `gcloud ... get-key-string` or key-creation output directly into protected
  storage; those commands may emit key material. Match key IDs internally,
  preserve appropriate API/application restrictions, and verify consumers.
  Do not probe an unrelated API merely to infer a project from an error.
- **Telegram:** use an available authenticated client and the official
  `@BotFather` flow for the identified bot. Request user-only login/2FA steps
  only if there is no agent path. Capture replacement tokens through protected
  storage, never by asking the user to paste them into chat.
- **Other services:** use their documented rotation flow and existing access
  tools; do not assume that a provider dashboard requires the user to do the
  whole operation manually.

Afterward, verify the replacement through the actual consumer and establish
that the old credential fails authentication or has authoritative revocation
evidence. If either check is inconclusive, leave the remediation incomplete.

## 7. Update GitGuardian when authorized

Respect authorization already supplied in the conversation for the incident
set and action. Read-only triage does not authorize `resolve` or `ignore`.
Do not ask the user to pre-approve a broad tool permission rule.

Use the current documented API for the exact incident:
`POST /v1/incidents/secrets/{id}/resolve` or
`POST /v1/incidents/secrets/{id}/ignore`. Check the current request schema and
allowed dispositions before sending. Set `secret_revoked: true` only when the
evidence supports that claim, and choose the exact justified ignore reason.

The committed wrapper is read-only. Use a narrowly scoped request helper for a
write, with the token loaded internally, privacy mode, timeouts, no redirect
following, and suppressed raw response/error bodies. Do not print raw curl
responses or put credentials in command arguments. Verify HTTP success and
re-fetch the targeted incident through `gitguardian-incidents get ID` to
confirm the intended lifecycle state and disposition. A zero curl exit code
alone does not prove success. For an ambiguous network result, re-fetch before
retrying so the same mutation is not sent blindly.

## 8. Contain leaks and finish

Removing a file from HEAD does not revoke a credential or remove its history.
Do not delete whole logs or notes just to stop GitGuardian re-flagging them.
When local redaction is authorized, remove only the secret-bearing content and
preserve the surrounding record. History cleanup is a separate operation;
follow `publish-dotfiles` if an explicitly requested public dotfiles
publication requires sanitizing unpublished commits.

Clean up the exact temporary files created for matches, replacements, headers,
and provider responses, following the local deletion policy. Track paths from
the time each file is created; cleanup must work for a read-only or zero-incident
run too. Do not claim secure erasure from `shred` on SSD/APFS or from moving a
file to Trash.

Report the reconciled incident counts and any blocked items: what evidence or
user-only access is missing, and why no available agent path can complete it.
Keep provider validity, consumer verification, and GitGuardian lifecycle status
distinct. Preserve a redacted audit record; never include credential values.
