---
name: aiox-wave-gate
description: >
  Executa o gate sistêmico ao final de cada wave de saneamento.
  Revisão transversal por @architect e @qa antes de iniciar a próxima wave.
  Usar quando uma wave de dívida técnica for concluída.
---

# AIOX Wave Gate — Gate Sistêmico por Wave

## Quando esta skill é acionada

- Ao final de cada wave de saneamento de dívida técnica
- Quando todas as stories de uma wave estiverem com status Done
- Antes de iniciar a próxima wave

## Avaliação do @architect

| Dimensão | Pergunta |
|----------|---------|
| Aderência | Arquitetura real está alinhada à arquitetura-alvo? |
| Dependências | Quais dependências foram alteradas? |
| Dívida resolvida | Quais débitos foram completamente resolvidos? |
| Dívida parcial | Quais débitos foram parcialmente resolvidos? |
| Novos débitos | Quais débitos legados foram descobertos durante a wave? |
| Dívida introduzida | Houve introdução de nova dívida? |
| Riscos residuais | Quais riscos permanecem após esta wave? |
| Replanejamento | A próxima wave precisa ser ajustada? |

## Avaliação do @qa

| Dimensão | Verificação |
|----------|------------|
| Regressão | Testes de regressão entre módulos |
| Segurança | Scan de vulnerabilidades |
| Integridade | Consistência de dados |
| Integração | Contratos entre módulos |
| Performance | Benchmarks comparativos |
| Observabilidade | Logs, métricas, alertas |
| Testes | Cobertura e suite completa |
| Build | Compilação limpa |
| Confiabilidade | Testes de stress e edge cases |
| Compatibilidade | Backward compatibility |
| Metas da wave | Cumprimento dos objetivos declarados |

## Veredito

- **APPROVED:** Próxima wave liberada
- **CONCERNS:** Próxima wave liberada com ressalvas documentadas
- **BLOCKED:** Correções necessárias antes de prosseguir

## Definition of Healthy

Sistema saudável quando:
- Sem vulnerabilidades críticas conhecidas
- Sem falhas críticas de integridade de dados
- Sem débitos HIGH sem owner e prazo
- Nenhuma nova dívida sem registro
- Lint, typecheck, testes e build passam
- Fluxos críticos com testes
- Migrations reversíveis e testadas
- Erros relevantes observáveis
- Sem regressões conhecidas
- Arquitetura real alinhada à arquitetura-alvo
- Backlog e ledger reconciliados
- Gate sistêmico da wave passou

## Condições de interrupção

- Veredito BLOCKED → não iniciar próxima wave
- Débito HIGH sem owner → não considerar wave concluída
- Regressão crítica → rollback e reavaliação

## Referências

- Protocolo: `.claude/rules/aiox-project-operating-protocol.md`
- Brownfield workflow: `.aiox-core/development/workflows/brownfield-discovery.yaml`
- Ledger: `docs/technical-debt/ledger.md`
