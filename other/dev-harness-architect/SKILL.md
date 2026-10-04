---
name: dev-harness-architect
description: >
  Audita, diagnostica ou desenha o harness de desenvolvimento de um projeto —
  guias e sensores que governam um agente de codificação (Claude Code,
  Copilot, Codex, Cursor). Stack-agnóstico: funciona em Python, Swift/iOS,
  Kotlin/Android, Node/TS, Go, Rust. Use quando o usuário quiser saber "o que
  meu harness tem/falta", por que uma regra não está sendo aplicada, ou
  precisar desenhar um harness do zero num projeto novo.
license: MIT
metadata:
  author: exported-from-uimaker-adk
  version: "1.0"
---

# Skill — Dev Harness Architect

Harness de desenvolvimento é tudo que envolve o agente de codificação além do
próprio modelo: instruções, configuração e sensores que aumentam a qualidade e
a segurança do que ele produz. Este skill audita, diagnostica e desenha essa
camada — não o runtime de agentes do produto (se houver um), só o harness que
governa quem escreve o código.

Antes de qualquer ação, leia [`reference/harness-model.md`](reference/harness-model.md)
se ainda não tiver o modelo carregado nesta sessão — ele tem o quadrante
completo guias×sensores e a tabela de adaptação por stack.

## Modelo em uma tabela

| Eixo | Inferencial (linguagem natural) | Computacional (mecânico) |
|---|---|---|
| **Guia** (feedforward — o que o agente sabe antes de agir) | Arquivo raiz (`CLAUDE.md`/`AGENTS.md`), regras de arquitetura, skills, prompts situacionais | Config de linter/formatter/type-checker, manifest de dependências, config de editor |
| **Sensor** (feedback — o que verifica o que foi produzido) | Skill de code-review, segundo agente avaliador, revisão humana | Pre-commit hooks, CI em tiers, fitness functions (testes estruturais), guardrails de runtime (hook PreToolUse, gateway de filesystem) |

**Regra de prioridade:** sempre que uma regra puder ser verificada
deterministicamente, prefira o sensor computacional. Reserve sensores
inferenciais para julgamentos semânticos que código não captura (isso é raro
de precisar mudar — quando um sensor inferencial falha repetidamente no mesmo
padrão, ele deveria ter virado sensor computacional).

## Modo 1 — Auditoria de um harness existente

Objetivo: descobrir o que já está implementado e onde estão os buracos.

1. Procure guias inferenciais: arquivo raiz do agente (`CLAUDE.md`, `AGENTS.md`,
   `.github/copilot-instructions.md`, `.cursor/rules/`), diretórios de skills
   (`.claude/skills/`, `.github/skills/`), prompts situacionais
   (`.github/prompts/*.prompt.md`, `.claude/commands/`).
2. Procure guias computacionais: config de editor (`.vscode/settings.json`,
   `.editorconfig`), config de linter/formatter/types (varia por stack — veja
   a tabela de adaptação), manifest de dependências com versões fixas.
3. Procure sensores rápidos: `.pre-commit-config.yaml`, hooks git nativos
   (`.git/hooks/`), Husky (`.husky/`), fastlane lanes de lint.
4. Procure sensores de CI: `.github/workflows/*.yml`, `.gitlab-ci.yml`,
   Bitrise/Xcode Cloud config. Identifique os "tiers" (lint/types → testes+cobertura
   → segurança → arquitetura) — se não há tiers, o CI provavelmente roda tudo
   num job só e falha lento.
5. Procure sensores estruturais/fitness functions: testes que verificam regras
   de arquitetura em vez de comportamento (nomes como `test_architecture`,
   `ArchitectureTests`, `DependencyRuleTest`, config de `dependency-cruiser`,
   regras custom de Detekt/SwiftLint).
6. Procure guardrails de runtime: um gateway único de escrita em filesystem
   (equivalente a `PathGuard`), uma allowlist de comandos de shell, hooks
   `PreToolUse` do Claude Code ou equivalente do Copilot.
7. Reporte em formato de tabela (guia/sensor × presente/ausente × arquivo) e
   proponha os 2-3 buracos de maior risco primeiro — normalmente: (a) nenhum
   gateway de escrita/shell, (b) nenhuma fitness function para regras já
   documentadas em prosa, (c) CI sem tier de segurança.

## Modo 2 — Diagnóstico: "por que essa regra não está sendo seguida"

Siga este checklist na ordem — pare no primeiro "não":

1. **A regra está documentada?**
   `grep -r "<palavra-chave>" <arquivo-raiz-do-agente> <diretório-de-skills>`
   Se não → falta um **guia inferencial**. Adicione a regra no arquivo raiz,
   com um exemplo correto e um incorreto. Seja específico: "nunca use
   `URLSession` fora de `Networking/`" é melhor que "use boas práticas de rede".

2. **A regra tem um sensor que a verifica?**
   Procure em pre-commit, CI, testes estruturais.
   Se não → falta um **sensor**. Veja o skill `architecture-fitness-functions`
   para converter a regra num teste determinístico.

3. **O sensor está rodando de fato?**
   Rode os comandos de verificação localmente (lint, types, testes
   estruturais). Um sensor que existe no repo mas não está no CI nem no
   pre-commit é decorativo.

4. **O sensor é forte o suficiente?**
   Se um sensor inferencial (skill de review, segundo agente) falha
   repetidamente no mesmo tipo de erro → converta para sensor computacional
   (teste ou grep determinístico no CI).

## Modo 3 — Desenhar um harness do zero

Para um projeto novo (qualquer stack):

1. Rode o Modo 1 primeiro — mesmo em projeto novo pode haver config de editor
   ou CI já herdada de um template.
2. Escolha o arquivo raiz único: se o projeto vai ser trabalhado por mais de
   um agente de codificação (Claude Code + Copilot, por exemplo), crie um
   arquivo raiz fino (`CLAUDE.md`) que só aponta para uma única fonte de
   verdade (`AGENTS.md` ou equivalente) — nunca duplique regras em dois
   lugares, porque eles divergem silenciosamente. Modelo em
   [`reference/harness-model.md`](reference/harness-model.md#hierarquia-de-instrucoes).
3. Use a tabela de adaptação por stack para escolher as ferramentas
   computacionais (linter, type-checker, test runner, coverage, security
   scan).
4. Defina os tiers de CI: Tier 1 lint+types (segundos), Tier 2 testes+cobertura
   (minutos), Tier 3 security scan (dependências + secrets), Tier 4
   arquitetura/fitness functions. Sensores lentos vão para CI; só os rápidos
   (<5s) vão para pre-commit/hook local.
5. Se o projeto vai usar mudança em fases (proposta → implementação, ex.
   OpenSpec), use o skill `install-dev-harness` para materializar os hooks de
   gate de fase.
6. Escreva pelo menos uma fitness function desde o commit inicial para a
   regra de arquitetura mais importante do projeto (normalmente: direção de
   dependência entre camadas, ou um gateway único para uma operação
   perigosa — escrita em disco, rede, shell).

## Sinais de saúde do harness

| Sinal observado | Diagnóstico | Ação |
|---|---|---|
| Sensor nunca dispara | Cobertura de teste do sensor é fraca, ou o código realmente nunca viola a regra | Adicione um teste negativo (fixture que viola a regra de propósito) para confirmar que o sensor funciona |
| Guia é ignorado repetidamente pelo agente | Guia inferencial não é suficiente para essa regra | Converta para sensor computacional |
| PRs sempre reprovam no mesmo tipo de erro | Falta sensor rápido (pre-commit) — o erro só é pego tarde, no CI ou na revisão humana | Adicione o check em pre-commit/hook local |
| Agente repete o mesmo erro em sessões diferentes | Guia inferencial ausente ou fraco (não estava no arquivo raiz) | Adicione o guia com exemplo concreto |
| Sensores lentos bloqueando o desenvolvedor local | Sensor pesado demais para pre-commit | Mova para CI, deixe só os sensores <5s localmente |

## Saída esperada

Ao final de uma auditoria ou desenho, produza:
- Uma tabela guias×sensores do estado atual (ou do estado alvo, no Modo 3).
- Lista priorizada de buracos, cada um com o guia/sensor concreto a
  adicionar e o arquivo onde vive.
- Se aplicável, aponte para `install-dev-harness` (esqueleto de fase) e
  `architecture-fitness-functions` (converter regra em teste).
