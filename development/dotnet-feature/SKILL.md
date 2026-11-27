---
name: dotnet-feature
description: "Implement a high-quality .NET/C# feature slice with minimal complexity, domain rules, tests, and verifiable build outputs."
---

# Implement focused .NET feature
1. Locate the nearest existing use case, endpoint, tests, DTOs and architecture policy; preserve conventions.
2. Convert acceptance criteria to behavior-focused tests before or alongside changes.
3. Design only needed request/response types, domain changes, validator, use-case handler and transport mapping; separate public models into files.
4. Keep core invariants together, `CancellationToken` end-to-end, no sync I/O, stable error semantics and explicit authorization/tenancy.
5. Prefer direct EF Core only if existing architecture allows; don't introduce generic repository or handler frameworks gratuitously.
6. Consider concurrency, duplicate requests, transaction scope and side effects; choose Outbox only for the actual dual-write problem.
7. Implement the smallest cohesive diff; add error cases and meaningful observability without logging sensitive input.
8. Run targeted tests, full relevant build/tests, format verification; disclose any check impossible to execute.
9. Report changed files, architecture conformity, run outputs, risk/rollout and follow-up debt only if needed.
