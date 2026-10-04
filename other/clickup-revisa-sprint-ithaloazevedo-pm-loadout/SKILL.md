---
name: clickup-revisa-sprint
description: |
  Gera o relatório de Sprint (rito de Revisão, com insumo para a Retrospectiva) para as squads que já trabalham por sprints nativas do ClickUp (workspace Vertical Tech) — PAM e Backoffice.
  Varre a Sprint ativa de um squad, separa concluído de não-concluído, calcula taxa de entrega e sintetiza um relatório narrativo — o principal artefato de dados e valor para stakeholders a cada ciclo.
  Ignora tarefas operacionais, bugs sem relação com a sprint e qualquer squad ainda no fluxo antigo Backlog→Execução (Jogos). Executado pelo agente agente-delivery. Feito para rodar sob demanda no rito de Revisão, ou agendado ao fim de cada sprint.
  Comandos: /clickup-revisa-sprint run [squad], /clickup-revisa-sprint dry-run, /clickup-revisa-sprint help
invocation: user
inputs: squad e sprint ativa no ClickUp
outputs: relatório narrativo de entregue vs. planejado
side_effects: propose
context: references de clickup-spec (config e método), sprint ativa do squad
completion: relatório entregue com taxa de entrega e itens não concluídos identificados
---

**Autor:** Ithalo Mendes <ithalo.mendes@verticalloto.com>

# ClickUp Revisa Sprint — Revisão e Retrospectiva

> **Renomeada em 2026-09-10** de `clickup-rollup` para `clickup-revisa-sprint` — o nome antigo vinha da mecânica
> técnica (consolidar/"rollup" comentários), não do rito que a skill serve. O nome novo diz o que ela faz e
> quando: gera a revisão da sprint.

> **Redesenhada em 2026-09-10.** Esta skill existia para consolidar updates em comentários nos **Objetivos**
> do ClickUp — nível removido do processo (ver `knowledge/domains/processo.md` e
> `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`). Sem
> Objetivo, não há mais card para ancorar um roll-up de portfólio. A skill foi redirecionada para o nível que
> resta e que o time realmente vive agora: a **Sprint**. Duas responsabilidades do design antigo não têm mais
> um lar natural e foram **descontinuadas nesta versão** (não substituídas): a reconciliação do Portfólio de
> Projetos (dependia da seção 🗂️ no card de Objetivo) e a consolidação do Plano de Medição (dependia do mesmo
> card). Se o Plano de Medição (handoff PM → Dados sobre eventos de instrumentação) continuar sendo valioso,
> ele precisa de um novo lar — proponha isso ao usuário em vez de tentar recriar sozinho.

Gera, ao fim de cada sprint (rito de **Revisão**), o relatório que mostra **o que foi entregue vs. planejado**
para o squad — o principal artefato de dados e valor para stakeholders que o modelo de sprints introduziu.
Também dá insumo objetivo para a **Retrospectiva** (tempo em cada status, itens que voltaram para a sprint
seguinte).

> **Quem executa:** o agente [agente-delivery](../../agents/agente-delivery.md).
> **Relação com `clickup-spec`:** a `clickup-spec` *cria/estrutura* itens e move do Backlog para a Sprint; a
> `clickup-revisa-sprint` *sintetiza o que aconteceu* numa sprint. As duas compartilham config e método.

## Escopo

**Squads cobertas hoje:** PAM (Sprint Folder "Sprints", `90118303225`) e Backoffice (Sprint Folder "Pasta do
sprint", `90118303239`) — as duas já migradas para sprints. **Squad Jogos não entra** — ainda está no fluxo
antigo Backlog→Execução, sem Sprint Folder; não há sprint para relatar.

**Entra:** todas as tasks da lista de Sprint ativa do squad.

**NÃO entra:**
- Itens do board de Execução legado (`901114029785` PAM, `901114029783` Backoffice) — não fazem parte da
  sprint atual, mesmo que ainda ativos.
- Itens ainda no Backlog (fora da sprint) — não fizeram parte do compromisso do ciclo.

## Comandos

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `run` | `/clickup-revisa-sprint run [PAM/Backoffice]` | Varre a Sprint ativa do squad e gera o relatório. Sem squad especificado, pergunte qual. |
| `run` **+ notas** | `/clickup-revisa-sprint run [squad]` + notas da reunião | Igual ao `run`, mas você fornece as **notas da Revisão/Retrospectiva** (o que foi decidido, motivo de itens não concluídos, aprendizados). A skill cruza o progresso do ClickUp com suas notas e escreve o relatório na sua voz. **Modo recomendado.** |
| `dry-run` | `/clickup-revisa-sprint dry-run [squad]` | Gera e **apresenta** o relatório sem postar em lugar nenhum. Use para revisar antes. |
| `help` | `/clickup-revisa-sprint help` | Explica escopo, cálculo e formato. |

## Verificação de Conector (obrigatória)

Antes de rodar, verifique silenciosamente se o conector do ClickUp está ativo (ex: `clickup_get_list` com o
ID da Sprint ativa em [../clickup-spec/references/clickup-config.md](../clickup-spec/references/clickup-config.md)).
Se não estiver disponível, interrompa e oriente a conectar o ClickUp (Configurações → Integrações → ClickUp).

## O que o relatório mede

1. **Planejado vs. concluído**: total de itens na Sprint ativa vs. itens em status `done`/`closed` (`pronto`,
   `fechado`, `cancelado` — ver os status exatos por squad em `clickup-config.md`). Taxa de entrega em %.
2. **Entregue**: lista dos itens concluídos, com link.
3. **Não concluído**: lista dos itens que não fecharam, com o motivo quando disponível (comentários, status
   `bloqueada`, ou a nota da reunião) — esses migram para a próxima sprint pela automação nativa do ClickUp
   (Sprint Automations), não é a skill que move.
4. **Itens travados** (opcional, útil antes da Daily, não só na Revisão): via
   `clickup_get_bulk_tasks_time_in_status`, sinalize itens parados há muito tempo no mesmo status.

## Modo com notas (briefing da Revisão/Retrospectiva) — recomendado

O fluxo ideal: você coleta os pontos na reunião de Revisão/Retrospectiva e **roda a skill passando essas
notas**. O relatório final junta duas camadas:

- **Camada factual** (do ClickUp): o que de fato foi concluído/não concluído na sprint — a skill detecta sozinha.
- **Camada humana** (das suas notas): o motivo de itens não concluídos, decisões tomadas na retro, aprendizados do ciclo.

**Como passar as notas:** rode `/clickup-revisa-sprint run [squad]` e cole as notas. Ex.:
> *"PAM: o item de KYC não fechou porque esbarrou num bloqueio de infra, resolve segunda. A validação facial saiu antes do previsto. Aprendizado da retro: revisão técnica está demorando demais, vamos tentar revisar em par."*

**Como a skill usa:**
1. Cruza cada trecho da nota com o item correspondente (por nome). Não identificou com segurança → **pergunta**, não chuta.
2. O motivo de não-conclusão vem da nota quando houver; sem nota, usa o que está nos comentários/status do ClickUp, ou marca **"motivo não registrado"** — nunca invente.

Sem notas, a skill roda no **modo automático** (só ClickUp) — só os fatos, sem interpretação de motivo.

## Onde o relatório vai

Não há mais um card de Objetivo para ancorar o relatório. Ofereça, nesta ordem, e **confirme com o usuário**
qual destino usar (pode ser mais de um):

1. **Comentário em cada item concluído/não concluído** — reconhece o trabalho individualmente, mas fragmenta o relatório.
2. **Mensagem no canal de Chat do ClickUp do squad** (`clickup_send_chat_message`, se um canal existir — confirme com `clickup_get_chat_channels`) — visível para o squad e stakeholders que acompanham o canal, sem precisar de um card artificial.
3. **Só na conversa** (o padrão mais simples e seguro) — a skill entrega o relatório pronto para você colar onde fizer sentido (Slack, e-mail, ou ler na reunião de Revisão). Sempre disponível, mesmo se as opções 1 e 2 não forem usadas.

**Nunca crie uma task nova só para servir de "card de sprint"** — isso recriaria a estrutura que a skill não
usa mais sem necessidade real. Se o usuário quiser um lugar persistente e não houver Chat channel disponível,
sinalize a lacuna e pergunte como ele prefere resolver (não decida sozinho).

## Processo (passo a passo)

1. **Confirmar o squad e a Sprint ativa** — resolver a lista de Sprint pelo squad (ver `clickup-config.md`). Squad Jogos → informe que ainda não há sprint, encerre.
2. **Listar os itens da Sprint ativa**: `clickup_filter_tasks` na lista de Sprint.
3. **Classificar**: concluído (status `done`/`closed`) vs. não concluído. Calcular a taxa de entrega.
4. **Para não concluídos**: buscar motivo em comentários recentes (`clickup_get_task_comments`) ou usar a nota da reunião, se fornecida.
5. **Opcional — itens travados**: `clickup_get_bulk_tasks_time_in_status` para sinalizar o que está parado há muito tempo no mesmo status, útil como insumo de Retrospectiva.
6. **Sintetizar** o relatório (formato abaixo), fundindo o progresso do ClickUp com as notas da reunião (se houver).
7. **Confirmar o destino** com o usuário (ver "Onde o relatório vai") e postar/entregar conforme escolhido.
8. **Reportar** ao final: taxa de entrega, quantos itens concluídos/não concluídos, onde o relatório foi entregue.

## Tom e formato do relatório

Narrativo, não um dump de status — é o relatório que o PM levaria para a reunião de Revisão.

**Tom (voz do Ithalo):**
- Fale como gente, para gente: "a gente", "entregamos" — direto e caloroso, sem jargão de processo.
- **Comece pelo resultado**, não pela lista de tarefas. Quantidade concluída é dado de apoio, não abertura.
- Para não concluídos, seja direto sobre o motivo — transparência honesta, sem enfeitar.
- Curto: o suficiente para caber numa leitura de 1 minuto antes da reunião.

**Estrutura:**

```markdown
**Sprint [N] ([datas]) — [squad] — Revisão**

{Abertura: taxa de entrega e 1 frase sobre o resultado geral.}

Entregue:
- [nome do item] → [link]

Não concluído:
- [nome do item] — [motivo] → migra para a próxima sprint

{Fecho: 1 frase de contexto para a Retrospectiva, se houver sinal relevante (ex.: gargalo recorrente).}
```

## Modo de confirmação

- **Interativo**: apresente o relatório e confirme o destino (comentário / Chat / só conversa) antes de postar em qualquer lugar do ClickUp. Não pergunte item a item — uma confirmação cobre o relatório inteiro.
- **Agendado/autônomo**: gerar o relatório é automático; **postar em qualquer lugar do ClickUp continua exigindo confirmação** — se rodar sem uma pessoa disponível para confirmar, entregue o relatório pronto e aguarde a próxima interação para postar.

## Agendamento

Diferente do design antigo (rotina diária), esta skill acompanha a **cadência da sprint** — 2 semanas por
squad, intercaladas. Rode sob demanda no rito de Revisão, ou agende via a skill `schedule` para disparar a
cada 2 semanas, alinhado à data de fim da Sprint ativa de cada squad (datas exatas em `clickup-config.md`,
squads migram em datas diferentes — não use uma cadência única para as duas).

> ⚠️ **Conector em execução headless:** rotinas agendadas rodam fora da sessão interativa e o conector ClickUp
> autenticado via Codex.ai pode **não** estar presente. Se o run agendado falhar na verificação de conector,
> trate o agendamento como um lembrete para executar `/clickup-revisa-sprint run [squad]` manualmente.

## Guardrails

- **Só a Sprint ativa das squads migradas (PAM, Backoffice).** Nunca gere relatório para o board de Execução legado nem para a squad Jogos (sem sprint ainda).
- **Não invente motivo de não-conclusão.** Sem nota nem comentário no ClickUp → "motivo não registrado".
- **Não muda status nem campos** das tarefas — esta skill só **lê** e **relata**. A cascata de itens não concluídos para a próxima sprint é automação nativa do ClickUp (Sprint Automations), não desta skill. Mudanças de status são da `clickup-spec`/`agente-delivery` sob confirmação.
- **Não cria tasks nem listas novas** para servir de ancoragem do relatório.
- **Português, primeira pessoa, voz do PM** — humanizado, resultado antes de lista de tarefas (ver "Tom e formato").
- **Plano de Medição descontinuado nesta versão** — se precisar dessa funcionalidade de volta, é uma decisão de onde ela mora agora (por épico? num Doc?), não algo para reinventar sozinho.

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| [../clickup-spec/references/clickup-config.md](../clickup-spec/references/clickup-config.md) | IDs de space, folders, listas (Backlog + Sprint), custom fields, status |
| [../clickup-spec/references/clickup-method.md](../clickup-spec/references/clickup-method.md) | Método, sprints (ritos, cadência) e modelos de comentário narrativo |
| [../../agents/agente-delivery.md](../../agents/agente-delivery.md) | Agente executor |
