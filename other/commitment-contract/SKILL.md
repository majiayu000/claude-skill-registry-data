---
name: commitment-contract
description: Design and test PromiseTwin contract state transitions, criteria and evidence binding. Use when implementing commitment schemas, fulfillment decisions or migrations.
---
# commitment-contract

Consult docs/03-DATA-CONTRACTS.md. Write pure deterministic functions for transitions, proof binding, expiry, actor authorization and version checking. Build table-driven tests including Done != Fulfilled, missing proof, wrong customer, stale proof, duplicate event and unauthorized acknowledgement. Verify all required criteria satisfied before fulfillment.

Do not auto-deploy, publish, create public links or change external permissions. Return concise evidence and next action.
