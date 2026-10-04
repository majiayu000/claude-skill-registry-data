---
name: guard
description: Monitora conformidade arquitetural e automatiza ADRs (Technical Decisions). Use quando o usuário pedir para "criar ADR", "validar arquitetura" ou "checar padrões".
---

## 🏛 ADR Automator

- Formaliza decisões técnicas em `docs/adr/NNN-titulo.md`.
- Status: Proposed -> Accepted -> Deprecated.

## 🛡 Consistency Checker

- Analisa grafos de importação para evitar vazamento de infraestrutura no domínio.
- Valida conformidade com Clean/Onion Architecture.
