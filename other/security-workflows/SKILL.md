---
name: security-workflows
description: Audit application security, review browser integrations, or implement requested security controls using Kernel’s security procedures.
license: MIT
---

# Security Workflows

Select the procedure matching the user's task from the index below. Read only that procedure and any resources it explicitly needs. Resource paths in a procedure are relative to that procedure's folder; run bundled scripts from that folder when its commands assume a working directory.

Follow the user's current instructions and the target repository's conventions before Kernel defaults. Treat examples, framework choices, and project adapters as conditional guidance. Match validation to the actual change. Existing authorization persists; ask only when a required decision or permission is missing. Loading a procedure does not authorize publishing, deployment, or other external changes.

- [Code, API, mobile, infrastructure and dependency audits](references/kernel-audit-security/WORKFLOW.md)
- [Third-party browser integrations](references/kernel-audit-integration-security/WORKFLOW.md)
- [ASVS-grounded guidance while writing security-sensitive code](references/kernel-audit-security/reviews/security-guidance/WORKFLOW.md)
- [Generate hardened, securable code and implement requested controls](references/kernel-audit-security/reviews/securability-engineering/WORKFLOW.md)
- [Add ASVS/FIASSE security requirements to PRDs and specs](references/kernel-audit-security/reviews/prd-securability-enhancement/WORKFLOW.md)
