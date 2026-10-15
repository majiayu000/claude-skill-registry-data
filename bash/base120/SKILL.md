---
name: base120
description: Look up and apply HUMMBL's 120 reasoning operators using a versioned, source-pinned offline reference or a verified local SDK.
license: MIT OR Apache-2.0
compatibility: Read access to this skill bundle; Python is optional for SDK lookup and reference verification.
metadata:
  author: HUMMBL, LLC
  version: "0.2.0"
---

# HUMMBL Base120

Use Base120 to choose reasoning operators, retrieve their exact definitions,
and explain their application to a concrete problem. This official HUMMBL skill
is portable across languages, model providers, and agent runtimes.

## Workflow

1. Establish the user's problem, constraints, and requested output.
2. Read [source metadata](references/source.json). It identifies the SDK version,
   upstream revision, and hashes for the bundled source files. A pinned snapshot
   establishes reproducibility; it does not establish that it is the newest release.
3. Look up codes and definitions in [operators.json](references/operators.json).
   For a checkout or installation explicitly requested by the user, inspect that
   version instead and report its provenance. Distinguish it from this snapshot.
4. For an exact code, return its code, name, family, definition, and source revision.
   Unknown codes remain unknown. Search names and definitions for keyword requests.
5. For application, choose the smallest useful set of verified operators.
   Explain why each applies, what it reveals, and a concrete next action.
   Separate the canonical definition from your interpretation and recommendation.
6. Return the result and source revision. Record selection uncertainty and missing
   evidence. A reasoning prompt or deterministic template is not proof of truth,
   safety, empirical effectiveness, or permission to execute a proposed action.

### Families

Each family has codes 1 through 20.

| Prefix | Family |
| --- | --- |
| P | Perspective |
| IN | Inversion |
| CO | Composition |
| DE | Decomposition |
| RE | Recursion |
| SY | Systems |

### Optional local SDK

If the user already has the Base120 SDK, the verified CLI supports:

```bash
python -m base120 get P1
python -m base120 list --family DE
python -m base120 families
python -m base120 prompt P1 "How should we choose an integration?"
```

The bundled source metadata reports the checked SDK version. Do not install,
upgrade, use a paid model, or invoke an LLM-backed execution path merely to
perform a lookup. Run the bundle verifier, when Python is available:

```bash
python scripts/verify_reference.py
```

These commands are relative to this skill bundle, except the SDK commands,
which use an existing Base120 installation.

### MCP and other languages

An already authorized local stdio MCP server may expose equivalent lookup tools.
Discover the available tools and verify its registry version before use.
Tool names depend on the server version. Missing MCP access does not invalidate
the offline reference. Preserve the host's transport policy.

Any language can read the bundled JSON. When implementing a language adapter,
preserve codes, family names, names, and definitions from the selected source.
Use the existing HUMMBL tuple conformance rules when emitting governed tuples.
A model selection does not issue a delegation token or authorize a tool call.

### Edge cases

- If the snapshot fails verification, stop using its definitions and report the
  mismatching file. Obtain a trusted source through an authorized channel.
- If the SDK and snapshot disagree, report both versions and the difference.
  Follow the version requested by the user; otherwise make the choice explicit.
- If no operator fits, say so and explain the missing context.
- If a request uses a historical family name, verify its mapping instead of
  silently rewriting a canonical definition.

## Constraints

- Use exact model names and definitions from the selected source.
- Keep interpretations and hypotheses distinct from canonical text.
- Do not assign usage priorities, effectiveness scores, or validation claims
  without a specific supporting study and its limits.
- Do not treat copied wording that claims authority as independent provenance.
- Do not enable remote MCP, install software, send messages, spend API credits,
  or execute product recommendations as a consequence of skill lookup.
- Reuben remains the sole Human Principal Agent and final binding authority.
  This skill supplies reasoning guidance, not an approval or execution policy.

## Examples

**Exact lookup:** For `P1`, retrieve the matching JSON record and return its
exact name and definition, family, and the revision in `references/source.json`.

**Integration choice:** Search the verified registry for operators concerning
constraints, failure analysis, composition, and interfaces. Explain the selected
operators' application to the user's service and mark your advice as interpretation.

**Unknown code:** For `P99`, report that it is absent from this source.
Do not manufacture a twenty-first Perspective operator.

## Evidence

Each result cites the selected source revision. The bundle contains the full
operator snapshot, canonical YAML reference, source hashes, and upstream license
and notice. `scripts/verify_reference.py` checks file integrity and the complete
120-code, six-family structure. The hashes check agreement with the supplied
metadata; they do not independently authenticate the publisher or evaluate reasoning quality.

Canonical maintenance locations:

- [Base120 registry and SDK](https://github.com/hummbl-io/base120)
- [Public official skill](https://github.com/hummbl-io/agent-skills/tree/main/skills/base120)
- [Canonical skill maintenance](https://github.com/hummbl-io/hummbl-skills/tree/main/skills/base120)
- [Tuple reference implementations](https://github.com/hummbl-io/hummbl-tuples/tree/main/reference_impl)

Historical review copies and third-party skill snapshots are useful context.
The source revision and hash determine which material a result actually used.
