---
name: handover-test-continuity
description: Run a complete Handover MCP continuity test across separate authenticated people or service agents. Use when asked to test an agent handoff end to end, qualify a Handover integration, verify multi-file round-trip, exercise revision-anchored review and correction, or test denied, read-only, stale-revision, and revoked-credential paths.
license: MIT
compatibility: Requires Handover MCP and at least two distinct authenticated identities with access to one test workspace. The handover-sh CLI may be used for setup or read-back, but MCP is required for the complete review workflow.
metadata:
  author: 44-pixels
  version: "1.0.0"
---

# Test Handover continuity

Prove that work survives a change of identity, host, review state, and revision.
Do not report a continuity pass merely because the endpoint responded or a
create call succeeded.

## Distinguish the test layers

Report each layer separately:

1. **Connectivity:** the host can reach Handover and list or call tools.
2. **Workflow completion:** one authenticated actor publishes and reads back
   an immutable multi-file revision.
3. **Continuity:** another authenticated actor reviews exact evidence, a later
   revision corrects it, and a fresh successor continues without the original
   chat.

Use `handover-verify` instead when the user only needs a read-only connection
or identity check.

## Preconditions

Require:

- Principal A with read and write access;
- Principal B with read and annotation access;
- Principal C with read and write access, which may be Principal A;
- Principal D outside the workspace for the denied test;
- a dedicated test workspace or an explicit integration-test label; and
- permission to create harmless test data and revoke a test credential.

Grant each principal only the smallest role and workspace scope required for
its checkpoint. The test must not use owner access where a member, reviewer,
reader, or denied principal is the behavior under evaluation.

Use a unique marker such as:

```text
e2e-mcp-handoff-YYYYMMDD-HHMMSS
```

Never request, display, log, or publish credentials. Do not put hidden
reasoning or unrelated personal data in artifacts.

If the required identities or permissions are unavailable, run only the
provable subset and mark every skipped checkpoint. Do not widen access merely
to make a test pass.

## 1. Verify the publisher

As Principal A:

1. call `handover.whoami`;
2. record the server-resolved principal, organization, workspace, role, and
   scopes;
3. stop if any boundary is unexpected; and
4. call `handover.search` for the unique marker before creating.

Authorship comes from the accepted credential, never from a name supplied in
the prompt.

## 2. Publish and read back the source package

Call `handover.create` with:

- a brief containing objective, current state, decisions, one open question,
  and one open next step;
- `context.md` containing the marker and continuation state;
- `query.sql` containing executable analysis; and
- `evidence.json` containing the marker, claim, source, and pending
  verification state.

Keep the record restricted to the test workspace.

Save every returned handover, revision, artifact, comment, and principal ID.
Never invent IDs.

Then:

1. call `handover.get` for the returned handover;
2. call `handover.read_artifact` for all three artifacts;
3. verify names, media types, marker, full content, and `truncated: false`; and
4. verify Principal A is the revision author.

A create response without exact artifact read-back fails workflow completion.

## 3. Review exact evidence independently

In a separate authenticated session, Principal B:

1. calls `handover.whoami` and proves its principal ID differs from Principal
   A;
2. searches for the unique marker;
3. calls `handover.get` with the initial revision ID;
4. reads `query.sql` and `evidence.json`;
5. creates an artifact annotation with `handover.annotate`;
6. anchors it to the initial revision, SQL artifact, exact selected text,
   surrounding context, and offsets calculated from the returned source;
7. mentions or assigns an authorized resolver when appropriate; and
8. confirms the finding is open with `handover.annotations`.

Mentions and assignments do not grant access. Do not comment on a summary when
the underlying artifact is available.

## 4. Publish a correction safely

Principal C:

1. calls `handover.whoami`;
2. retrieves the current revision;
3. calls `handover.continue` with that revision as `expectedRevisionId`;
4. publishes corrected `query.sql` and `evidence.json`;
5. updates the brief and next steps; and
6. records the new revision ID.

The correction must be a later immutable revision. The initial reviewed
revision must remain inspectable.

## 5. Verify and resolve

Principal B retrieves the correcting revision and reads both corrected
artifacts. Only after verifying the evidence, call `handover.update_comment`
with:

- the original comment ID;
- `status: "resolved"`; and
- `resolvedRevisionId` set to the correcting revision.

Call `handover.annotations` again. Require the annotation to remain anchored
to the initial artifact and revision while its resolution names the correcting
revision.

## 6. Prove successor continuity

Give a fresh authorized session only the marker or canonical handover link,
not the original chat.

The successor must:

1. verify its identity;
2. find and retrieve the current handover;
3. inspect annotations;
4. read the corrected source artifacts;
5. state the objective, current revision, corrected decision, and next action;
   and
6. continue only when new work is actually performed.

The stated continuation must agree with the canonical artifacts and brief.

## 7. Run the required negative paths

Run and record each result:

- **Denied identity:** Principal D must not discover or retrieve the protected
  record.
- **Read-only identity:** protected reads succeed, while annotation and
  continuation writes are refused.
- **Stale revision:** a continuation using the initial revision after the
  correction exists must return a conflict and require rereading.
- **Revoked credential:** after an owner revokes a dedicated test credential,
  the next protected read must fail without returning or logging the
  credential.

Do not substitute a broader credential when a negative path fails.

## Pass criteria

Pass only when all applicable checks are evidenced:

- publisher and reviewer have distinct server-resolved identities;
- search before create prevented duplicates;
- Markdown, SQL, and JSON round-trip intact;
- the reviewer retrieved the exact initial revision;
- the finding is anchored to exact initial evidence;
- the correction is a later immutable revision;
- resolution links to the correcting revision;
- a fresh successor recovered the objective, decision, and next action;
- denied and read-only boundaries held;
- stale continuation was rejected;
- revoked credentials stopped authorizing reads; and
- no credential appeared in artifacts, output, or logs.

If any required checkpoint was skipped, return **incomplete**, not pass.

## Report

Return:

- overall result: pass, fail, or incomplete;
- connectivity, workflow completion, and continuity results separately;
- principal types and IDs, without credentials;
- workspace and access boundary;
- handover and revision IDs;
- artifact round-trip result;
- annotation and resolution result;
- successor recovery result;
- every negative-path result;
- skipped checks and why;
- first failed checkpoint and safe remediation; and
- cleanup or archival action.

For exact sample payloads and offsets, use the
[production-schema procedure](https://handover.sh/examples/end-to-end-mcp-handoff-workflow.md?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_test_continuity)
and the
[rendered rationale](https://handover.sh/guides/end-to-end-mcp-agent-handoff?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_test_continuity).
