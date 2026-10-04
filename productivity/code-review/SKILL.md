---
name: code-review
description: Revisão holística pré-commit (estilo PR Review). Valida o diff contra as 3 memórias vivas (guidelines, architecture, business), a spec da task e os padrões Clean Code. Executada obrigatoriamente pelo Tech Lead antes de liberar para Ops.
---

# Skill: Code Review (PR-Style Pre-Commit Gate)

**Objetivo:** Atuar como gate de qualidade pré-commit, simulando uma revisão de PR humana. O Tech Lead executa esta skill após a aprovação funcional do QA (e Security, quando aplicável) e antes de liberar para o Ops fechar o ciclo.

## Workflow de Execução

### 1. Coleta de Contexto
- Ler a task/spec ativa em `docs/todo/<NNN-nome-kebab>/tasks.md` para entender o que foi especificado.
- Ler as 3 memórias do projeto:
  - `memorys/guidelines.md` — padrões técnicos, convenções, restrições de implementação.
  - `memorys/architecture.md` — decisões arquiteturais, NFRs, stack definida.
  - `memorys/business.md` — regras de negócio, requisitos funcionais, glossário de domínio.

### 2. Diff Analysis
- Analisar as mudanças não commitadas (`git diff`) ou o diff da branch atual.
- Mapear quais arquivos foram alterados e qual o escopo da mudança.

### 3. Checklist de Validação Cruzada
Para cada item do diff, validar:

#### 3a. Spec Compliance (Task ↔ Código)
- Todos os itens da task/spec foram implementados?
- Algum critério de aceite (DoD) ficou sem cobertura?
- Há código que extrapola o escopo da task (scope creep)?

#### 3b. Guidelines Compliance (memorys/guidelines.md ↔ Código)
- Convenções de naming, estrutura de arquivos e padrões Clean Code respeitados?
- Restrições técnicas documentadas foram seguidas?
- Antipadrões registrados foram evitados?

#### 3c. Architecture Compliance (memorys/architecture.md ↔ Código)
- O código respeita as decisões arquiteturais registradas (stack, patterns, camadas)?
- NFRs documentados foram considerados (performance, escalabilidade)?
- Novas dependências ou integrações estão alinhadas com o ecossistema definido?

#### 3d. Business Compliance (memorys/business.md ↔ Código)
- Regras de negócio implementadas estão de acordo com o documentado?
- Glossário de domínio está sendo respeitado (naming de entidades, variáveis de negócio)?
- Permissões e fluxos de acesso seguem o modelo definido?

#### 3e. Higiene de Código (Clean Code)
- Código morto ou importações não utilizadas.
- Variáveis não semânticas ou nomenclaturas confusas.
- Funções excessivamente grandes (Complexidade Ciclomática alta).
- Duplicação desnecessária.

### 4. Relatório de Review
Gerar relatório estruturado com o seguinte formato:

```
## 📝 Code Review Report — Task [NNN]

**Revisor:** 👑 Tech Lead
**Data:** YYYY-MM-DD
**Veredito:** ✅ APPROVED | 🔁 CHANGES REQUESTED

### Spec Compliance
- [✅|❌] [Item da spec] — [observação]

### Guidelines Compliance
- [✅|⚠️] [Regra] — [observação]

### Architecture Compliance
- [✅|⚠️] [Decisão] — [observação]

### Business Compliance
- [✅|⚠️] [Regra de negócio] — [observação]

### Higiene de Código
- [Arquivo:Linha] — [sugestão]

### Veredito Final
[Explicação concisa da decisão]
```

### 5. Ação Pós-Review
- **✅ APPROVED**: Liberar para o Ops fechar o ciclo (changelog + versão + commit).
- **🔁 CHANGES REQUESTED**: Devolver ao Developer com o relatório. O Developer corrige e re-submete ao Tech Lead (loop iterativo, sem re-passar pelo QA a menos que mudanças substanciais).

## Restrições
- **Não duplicar** validação funcional (é responsabilidade do QA) nem auditoria de segurança (é responsabilidade do Security).
- **Foco na conformidade**: o review valida se o que foi feito está de acordo com o que foi especificado e documentado nas memórias.
- Manter o tom configurado em `memorys/guidelines.md` (seção Personalidade e Tom de Voz).
