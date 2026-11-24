---
name: lakona-define-rpc-contract
description: Define or update Lakona Shared RPC service contracts, notification contracts, DTOs, and stable numeric IDs. Use when adding an RPC API, changing request or reply shapes, adding server-to-client callbacks, assigning service, method, or notification IDs, fixing contract generator diagnostics, or validating Unity and serializer compatibility.
---

# Define a Lakona RPC Contract

Define the wire contract in the project's Shared assembly without leaking server implementation details into it. Treat published numeric IDs and serialized member order as compatibility commitments.

## Workflow

1. Read the repository instructions, root documentation, and instructions governing Shared, Server, and client code before editing.
2. Locate the Shared project, its serializer, target frameworks, language version, existing RPC contracts, ID registries, and generated-code configuration.
3. Search all existing service, method, and notification IDs before choosing a value. Identify the project's naming and domain-file conventions.
4. Establish the API semantics from the request and repository evidence:
   - operation name and owning service
   - request and reply data
   - business failure representation
   - whether a server-to-client notification contract is required
5. Read [references/contract-shapes.md](references/contract-shapes.md) before assigning IDs or defining DTO fields.
6. Add or update the named ID constants, service interface, notification interface when needed, and serializer-compatible DTOs in Shared.
7. Keep each RPC method to exactly one request DTO parameter. Preserve the required `ValueTask` or `ValueTask<T>` return shape.
8. Prefer `void` notification methods with one DTO parameter for new contracts, following project conventions. Preserve valid existing signatures and connect the notification contract to its service explicitly; see the supported shapes in the reference.
9. Update an existing contract in place. Do not leave duplicate interfaces, parallel ID registries, handwritten generated output, or compatibility aliases without an explicit requirement.
10. Build the actual Shared and server application projects so analyzers and source generators execute. Build the affected client when its generated API or serializer compatibility changes, then run focused contract or integration tests.

## Compatibility Rules

- Treat service, method, and notification IDs as wire-level API. Never renumber a published member or reuse its ID for a different meaning.
- Use a positive service ID for business services. Service ID `0` belongs to Lakona's internal control protocol.
- Follow the repository's serializer and Unity compatibility line. Do not introduce syntax or BCL APIs unsupported by the Shared project's Unity/C# target.
- Preserve serialized member order. Append compatible fields according to the serializer's versioning rules; do not silently reorder or repurpose existing fields.
- Represent expected business outcomes in reply DTOs. Reserve framework RPC status for transport, dispatch, serialization, and other framework failures.

## Ownership Boundaries

- Shared owns public RPC interfaces, notification interfaces, DTOs, and stable IDs.
- Server.Hotfix owns implementations. Use the `lakona-implement-service` Skill after the contract is defined.
- Do not expose `GameSessionKey`, `RpcSession`, actor references, dependency-injection types, transport types, callbacks as stored state, or server-only runtime types through Shared DTOs.
- Do not implement behavior, invent product rules, run client generation scripts that the project does not own, or edit compiler-generated files as part of this Skill.
- Prefer the project's established API grouping and naming. Ask for a product decision when semantics cannot be inferred safely.

## Validation

Apply the validation steps to affected contracts, reusing existing coverage and
adding tests only where meaningful coverage is missing. For non-behavioral,
low-impact edits, use relevant static checks. A test command may also satisfy
the build when it covers the same graph and configuration. Once relevant checks
and required stage gates pass, stop unless new changes, failures, or a concrete
unresolved risk justify more verification. Report any unverified outcomes.

For contract changes, cover the following build targets directly or through
test/build commands that cover their dependency graph and configuration:

1. Build the discovered Shared project.
2. Build the discovered Server.App or equivalent server host project.
3. Build the affected client when its generated API or serializer compatibility changes.
4. Run focused tests for ID stability, serialization, generated client shape, or RPC behavior when the repository provides them.
5. Inspect diagnostics for duplicate IDs, invalid method shape, serializer ordering, unsupported target APIs, and generator failures.

Report the IDs and contract files changed, compatibility assumptions, commands run, and any behavior that still requires a decision. A successful build proves structural compatibility, not that an untested API has correct product semantics.
