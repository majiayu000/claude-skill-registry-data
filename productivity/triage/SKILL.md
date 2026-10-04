---
name: triage
description: Especialista em triagem e causa raiz (RCA) de bugs. Use quando o usuário reportar "erro", "bug" ou "falha" para isolar o problema e localizar arquivos prováveis.
---

## Workflow

1. **Isolamento**: Recebe stack traces e localiza arquivos/linhas prováveis.
2. **Diagnóstico**: Gera RCA (Root Cause Analysis) com hipóteses e formaliza utilizando o template `memorys/templates/bug.md`.
3. **Action**: Aciona `feature-flow` (tipo `fix`) enviando o artefato de bug gerado para iniciar a correção.
