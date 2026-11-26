---
name: portable-source-assertions
description: "Fix Python AST source-identity assertions that break across interpreter versions while keeping the exact semantic check. Keeps a source review separate from an actual fixture run."
---

# Zügelchischte (portable-source-assertions)

Use when unchanged Python controller source passes AST-hash checks locally but fails them on another pinned interpreter. Keep the repair limited to the demonstrated representation difference; this skill does not authorize a rerun, deployment or native workload.

## Establish the falsifier

1. Preserve the failed run, raw assertion values, interpreter identities, source hashes, selected test names, exit statuses and cleanup receipts. A failed fixture remains incomplete until separately resolved; it does not refute the underlying algorithm.
2. Compare the actual tested source bytes with the frozen source. If they differ, investigate source selection or mutation before considering formatter changes.
3. Inspect the exact versions' `ast.dump` implementation or retained primary documentation. Parse the source once and compare both formatters on the **same AST object**. This isolates serialization from parser/schema differences.
4. Require the explanation to reproduce the actual failure hash. Comparing two dumps that merely look similar is insufficient. Record every protected node's old and proposed digest, not just the first failing node.

If the same-source witness fails, or AST fields/values changed, stop the formatter-only repair. Do not silently normalize away a genuine source or parser difference.

## Use an explicit format

For the demonstrated Python 3.12/3.14 case, retain fields and omit only location attributes:

```python
import ast
import sys

def full_field_ast_dump(node):
    if sys.version_info >= (3, 13):
        return ast.dump(
            node, annotate_fields=True, include_attributes=False,
            show_empty=True,
        )
    return ast.dump(node, annotate_fields=True, include_attributes=False)
```

Python 3.14's default omitted empty fields; the retained Python 3.12 formatter included them. Explicit full-field dumps matched for all sixteen protected nodes in the incident below. This is a bound compatibility convention, not a universal canonical AST format across future Python releases. Recheck interpreter/schema changes separately.

Hash the UTF-8 dump with the existing digest algorithm. Keep one expected digest per node. Do not accept both old and new hashes, discard fields, skip nodes, remove assertions or catch comparison failures as success.

## Make an additive repair

- Preserve the original frozen package and failed evidence. Create a new revision; keep production controller files unchanged when only the assertion format is defective.
- Update the serializer and every affected expected digest from the bound witness. In this incident, all sixteen per-node equality checks (seven lifecycle and nine observer nodes), all twenty-four test names and every assertion remained present.
- Retain an exact reverse diff and source hashes. Check that reversing the test-only edit recovers the original test source; compare assertion bodies and selected names. Where authorized, a deliberate semantic mutation should still fail. Do not claim that check ran when it did not.
- Regenerate the complete package manifest and archive, then read every member back by SHA, size and mode. An unchanged production code manifest does not imply an unchanged package: test/fixture bytes also need binding.
- Rebind consumers and transport wrappers to the new package, manifest and fresh once-only namespace. Preserve parent-wait, process-group cleanup, lock, deadline, transfer and raw-evidence requirements. Keep any missing review or grant explicitly closed.

## Close the right evidence gate

A source-only repair receipt reports its exact files, derivation, preserved assertions and checks actually performed. It must say whether production modules were imported and whether a suite ran.

An independent source review admits only the inspected revision. A later authorized run must bind that revision and retain actual test names/counts, raw logs, parent/child exit status, source readback and cleanup. Never turn a source diagnosis, local formatting comparison or prepared grant template into an actual Linux pass. Preserve the original failure even after a later success.
