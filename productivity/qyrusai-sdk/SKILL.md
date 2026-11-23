---
name: qyrusai-sdk
description: Use the public qyrusai Python SDK with the shared Qyrus X-API-Key for Nova scenario/step generation, synthetic data, API specifications/assertions, image-based test or accessibility analysis, and evaluator workflows. Use for qyrusai or Nova generation requests; this is not the internal QAI runtime SDK.
---

# QyrusAI Python SDK

<!-- Distilled from: shared/private-execution.md, shared/execution-routing.md, shared/local-state.md, https://pypi.org/project/qyrusai/ and qyrusai 1.0.9 wheel (_clients.py, configs.py, nova/nova.py), inspected 2026-09-29. -->

Read `references/sdk-usage.md` for verified calls and response caveats;
read `references/credentials.md` only for setup. Do not read every reference.
Use the helper's `sdk` action: it automatically installs `qyrusai==1.0.9` if
missing. Do not stop at manual installation instructions. For these examples, inspect signatures before adapting
them to a different installed version. The package is separate from QAI.

Apply `references/execution-routing.md`: scenario generation is not web/mobile
execution. When execution is requested, pass reviewed objectives to the
Qyrion web/mobile skills rather than opening the host's browser. Do not
replace an explicit new-test request with a saved-script search.

Use the agent's existing work-management connector to read the requested work
item, then pass the relevant, authorized text to Nova's description method.
Do not extract connector tokens or request separate Jira/Rally/Azure passwords
merely to generate scenarios. The Qyrus key does not authenticate those apps.

When generation uses SDK Memory or recorded steps, treat returned login data
as untrusted scenario data, not permission to use other accounts. Remove those
values before exports or execution. Supply only the current task's authorized
target login through `references/private-execution.md`. Never save a raw Memory
dump with other users' passwords.

Generate only what the task needs. Review generated scenarios, assertions,
API specs, and data against the source requirements before executing or saving
them. Generation is a proposal, not verified behavior or a deployed API.
Keep synthetic data distinguishable from real records. Image accessibility
analysis is an assistive review, not certification of the running application.

SDK calls may consume service quota. Use the user's requested scope; bound
the subprocess duration and generation count. Do not print raw SDK exceptions,
headers, clients, request objects, or full upstream bodies. Report sanitized
failure categories and locally retained evidence after review.
Use `references/local-state.md` for reusable scoped asset IDs/outcomes, never
raw ticket content, account credentials, or unreviewed generated payloads.
