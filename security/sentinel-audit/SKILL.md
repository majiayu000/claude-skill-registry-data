---
name: sentinel-audit
description: Audit securite smart contracts SENTINEL
user-invocable: true
---

Utilise l'agent security-auditor pour :

1. Scanner tous les fichiers .sol du projet
2. Verifier : reentrancy, access control, signatures, overflow, front-running
3. Produire AUDIT_REPORT.md avec findings High+ uniquement

$ARGUMENTS
