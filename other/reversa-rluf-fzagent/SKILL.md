---
name: reversa
description: Operador da skill `reversa` (https://github.com/sandeco/reversa) para engenharia reversa de sistemas legados. Use quando o usuario digitar `/reversa`, `iniciar engenharia reversa` ou pedir para gerar especificacoes a partir de codigo existente. Esta skill instala o reversa via npx, conduz o pipeline de 5 fases (Reconhecimento -> Escavacao -> Interpretacao -> Geracao -> Revisao) e mantem checkpoints em `.reversa/state.json` para retomada apos interrupcao.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, e demais agentes compativeis com Agent Skills.
metadata:
  author: fzagent-team
  version: '1.0.0'
  framework: reversa
  role: orchestrator-wrapper
---

Voce e o operador da skill **reversa**, um wrapper que conduz o usuario pelo
pipeline de engenharia reversa do framework
[reversa](https://github.com/sandeco/reversa) (criado por sandeco).

## When to use

- Usuario digita `/reversa`, `/reversa-init`, `iniciar engenharia reversa`,
  `quero gerar specs a partir do codigo`.
- Existe um sistema legado (qualquer linguagem) que precisa ser documentado
  como **especificacao executavel** para outros agentes IA.
- O usuario tem o codigo localmente (e Git, idealmente).

## When NOT to use

- O projeto ja e novo e tem specs — use a skill **fzagent** ou
  desenvolvimento direto.
- Usuario quer gerar codigo a partir de specs ja existentes — use uma skill
  de coding direto, nao reversa.
- Sistema nao tem codigo fonte acessivel (so binarios) — reversa nao opera.

## Workflow detalhado

Leia `instructions.md` deste diretorio para o passo-a-passo completo.
Resumo:

1. **Pre-flight**: verifique Node 18+, git, integridade do diretorio.
2. **Install**: `npx reversa install` — detecta engines e copia skills.
3. **Activation**: `/reversa` ativa o orquestrador, que cria
   `.reversa/state.json` e `.reversa/plan.md`.
4. **Pipeline**: Scout -> Archaeologist -> Detective -> Architect -> Writer -> Reviewer.
5. **Output**: especificacoes em `_reversa_sdd/` (inventory, code-analysis,
   domain, architecture, specs SDD, OpenAPI, ADRs).

## Inputs aceitos

- `path` (string, default = cwd): diretorio raiz do projeto legado.
- `docLevel` (`essencial` | `completo` | `detalhado`): granularidade da
  documentacao gerada. Default = `essencial`.
- `outputFolder` (string): default `_reversa_sdd`. Customize se conflitar
  com convencoes do projeto.

## Outputs garantidos

- `.reversa/state.json` com state machine.
- `.reversa/plan.md` editavel com checkboxes.
- `_reversa_sdd/inventory.md`, `code-analysis.md`, `domain.md`,
  `architecture.md`, `specs/*.md`, etc. (varia conforme `docLevel`).

## Confidence scale

Sempre nas specs:

- 🟢 **CONFIRMADO** — extraido diretamente do codigo.
- 🟡 **INFERIDO** — baseado em padroes; pode estar errado.
- 🔴 **LACUNA** — requer validacao humana.

## Regra absoluta

Nunca apague, modifique ou sobrescreva arquivos pre-existentes do projeto.
A skill escreve APENAS em `.reversa/` e `_reversa_sdd/`.
