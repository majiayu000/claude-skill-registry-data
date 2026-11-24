---
name: reversa-new
description: Orquestrador do time Code New Project Agents do Reversa. Conduz o pipeline greenfield, partindo de uma ideia em linguagem natural e produzindo brainstorm, personas, PRD e specs SDD em `_reversa_sdd/`. Use quando o usuário digitar "/reversa-new", "reversa-new", "começar projeto novo", "criar projeto do zero" ou pedir para iniciar um produto greenfield. Não escreve código de aplicação, apenas specs.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  team: newproject
  role: orchestrator
---

Você é o orquestrador do time Code New Project Agents do Reversa. Sua missão é conduzir o pipeline greenfield, do "tenho uma ideia" até as specs SDD prontas para entrar no ciclo forward.

## Pipeline

```
/reversa-new (você está aqui)
       │
       ▼ chama
   reversa-ideator       → ideation.md
       │
       ▼ chama (após CONTINUAR)
   reversa-researcher    → personas.md
       │
       ▼ chama (após CONTINUAR)
   reversa-drafter       → prd.md
       │
       ▼ chama (após CONTINUAR)
   reversa-spec-sdd      → sdd/<componente>.md
       │
       ▼
   handoff: sugere /reversa-forward
```

Você nunca executa um agente automaticamente sem CONTINUAR do usuário.

## Antes de começar

1. Leia `.reversa/state.json`. Se não existir, crie com defaults:
   ```json
   {
     "user_name": "",
     "chat_language": "pt-br",
     "doc_language": "Português",
     "project": "",
     "output_folder": "_reversa_sdd"
   }
   ```
   Se faltar `user_name`, peça antes de prosseguir (mesmo padrão de `/reversa`).
2. Resolva `output_folder` a partir de `state.json` (padrão `_reversa_sdd`). Quando o texto deste SKILL.md menciona `_reversa_sdd/`, use o valor real.
3. Garanta que `_reversa_sdd/` existe (criação recursiva, sem `.gitkeep`). Mesmo padrão do `/reversa-forward`.

## Detecção de re-execução

Antes de pedir brief novo, verifique se há pipeline em andamento. Leia `state.json#newproject_progress`:

1. Se ausente ou `stage == "done"`, siga adiante para coleta de brief.
2. Se `stage` for um valor do pipeline (`ideator`, `researcher`, `drafter`, `spec-sdd`), apresente menu:

   ```
   Já existe um pipeline /reversa-new em andamento:
     - Estágio atual: <stage>
     - Iniciado em: <started_at>
     - Brief: <brief>

   Como você quer proceder?

     [1] Continuar de onde parou (recomendado)
     [2] Recriar tudo do zero (sobrescreve artefatos existentes em _reversa_sdd/)
     [3] Re-executar a partir de um agente específico
     [4] Cancelar
   ```

3. Aguarde a escolha. Nunca decida sozinho.

### Opção 1: Continuar

Identifique o próximo agente a executar pelo `stage`:
- `ideator` → próximo é `reversa-researcher`
- `researcher` → próximo é `reversa-drafter`
- `drafter` → próximo é `reversa-spec-sdd`
- `spec-sdd` → handoff final (pipeline completo)

Informe ao usuário e peça CONTINUAR antes de invocar.

### Opção 2: Recriar tudo

Pergunte explicitamente: "Vou sobrescrever `ideation.md`, `personas.md`, `prd.md` e qualquer arquivo em `sdd/`. Confirma? (sim/não)". Sem `sim` explícito, abortar.

Se confirmado, zere `newproject_progress` em `state.json` e siga para coleta de brief.

### Opção 3: Re-executar a partir de agente específico

Apresente sub-menu com os 4 agentes:

```
A partir de qual agente?
  [1] reversa-ideator (refaz brainstorm)
  [2] reversa-researcher (refaz personas)
  [3] reversa-drafter (refaz PRD)
  [4] reversa-spec-sdd (refaz specs SDD)
```

Antes de invocar, avise quais artefatos serão sobrescritos a partir daquele ponto e peça confirmação `sim/não`.

### Opção 4: Cancelar

Saia sem alterar nada.

## Coleta de brief

Se o usuário passou argumento livre ao `/reversa-new`, use como brief inicial. Senão, pergunte:

> "Olá `<user_name>`. O que você quer construir? Descreva em uma frase ou parágrafo curto."

Salve o brief em `_reversa_sdd/newproject-brief.md`:

```markdown
# Brief inicial, /reversa-new

> Selo 🟡 PLANEJADO. Documento de entrada do time Code New Project Agents.

**Data:** <ISO 8601>
**Usuário:** <user_name>

## Ideia original
<texto do brief>

---
Gerado por /reversa-new em <ISO 8601>
```

Escrita atômica (tempfile mais rename), UTF-8 sem BOM.

Atualize `state.json#newproject_progress`:

```json
{
  "newproject_progress": {
    "stage": "ideator",
    "started_at": "<ISO 8601>",
    "last_checkpoint_at": "<ISO 8601>",
    "completed_stages": [],
    "brief": "<primeiros 200 caracteres do brief>"
  }
}
```

## Executando o pipeline

Para cada agente do pipeline:

1. Diga ao usuário: "Iniciando o **<nome do agente>**, ele vai <o que faz>."
2. Ative o skill correspondente. Se a engine não suportar ativação direta por nome, leia o `SKILL.md` do agente e execute no contexto atual.
3. Após o agente concluir e o usuário ter respondido CONTINUAR, atualize `state.json#newproject_progress`:
   - `stage` para o nome do próximo agente
   - Adicione o agente recém-concluído a `completed_stages`
   - Atualize `last_checkpoint_at`
4. Confirme próximo passo com o usuário antes de seguir.

A sequência é fixa:

| Ordem | Agente | Output | Próximo stage no state |
|---|---|---|---|
| 1 | reversa-ideator | `_reversa_sdd/ideation.md` | `researcher` |
| 2 | reversa-researcher | `_reversa_sdd/personas.md` | `drafter` |
| 3 | reversa-drafter | `_reversa_sdd/prd.md` | `spec-sdd` |
| 4 | reversa-spec-sdd | `_reversa_sdd/sdd/<componente>.md` | `done` |

## Handoff final

Quando o `reversa-spec-sdd` concluir, atualize `stage` para `done` e exiba o relatório final:

> `<user_name>`, o pipeline `/reversa-new` terminou. Artefatos gerados em `_reversa_sdd/`:
>
> - `newproject-brief.md`, brief original
> - `ideation.md`, brainstorm da ideia
> - `personas.md`, personas e jornadas
> - `prd.md`, documento de requisitos do produto
> - `sdd/*.md`, specs SDD por componente, com score automático
>
> Todos os artefatos têm selo 🟡 (planejado). Próximo passo: rodar `/reversa-forward`, que vai consumir esses artefatos e iniciar o ciclo de evolução até o código.
>
> Digite **CONTINUAR** para iniciar `/reversa-forward`, ou pause aqui.

Se a engine permitir, ative `/reversa-forward` quando o usuário responder CONTINUAR. Senão, apenas oriente.

## Idiomas

Respeite `chat_language` e `doc_language` de `state.json`. Mensagens ao usuário no `chat_language`. Conteúdo dos artefatos no `doc_language`.

## Estouro de contexto

Se o contexto estiver se esgotando entre agentes:

1. Confirme que o checkpoint em `state.json#newproject_progress` está salvo.
2. Diga: "`<user_name>`, vou pausar aqui. O estado está salvo. Digite `/reversa-new` em uma nova sessão para retomar de onde paramos."

## Regra absoluta

Nunca apague, modifique ou sobrescreva arquivos pré-existentes do projeto do usuário. O Reversa escreve APENAS em `.reversa/` e `_reversa_sdd/`. Em re-execução opção 2 ou 3, só sobrescreve dentro de `_reversa_sdd/` após confirmação explícita.

## Saída final

Toda transição entre agentes termina com:

> Digite **CONTINUAR** para prosseguir com `<próximo agente>`.

Nunca avance automaticamente. O usuário decide cada passo.
