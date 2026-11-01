---
name: sfmc-jornadas-pacote
description: Lê pacotes do SFMC Package Manager (ZIP de jornadas exportado pelo Pablo),
  extrai cada mensagem de WhatsApp, SMS, e-mail e push com texto, parâmetros, link,
  af_sub e o caminho dentro da jornada, liga cada mensagem aos disparos reais da tabela
  `activities` no Supabase pelo Activity Name e ranqueia qual template trouxe melhor
  resultado (conversão = cartões / base acionável, com CAC, cobertura e confiança).
  Também desenha a jornada (raio-x). Use quando o usuário mandar um .zip de pacote/jornadas
  do SFMC, pedir pra "ler as mensagens das jornadas", "qual template converteu melhor",
  "ranking de templates", "ligar mensagem ao disparo", ou analisar réguas de carrinho,
  repescagem (NGD), upgrade (ANC), topo. Também CARREGA o pacote na Fila de reconciliação
  do GaaS (Comunicações) e anota cada proposta, quando o Pablo pedir "carrega esse
  pack na fila", "sobe o pacote pro GaaS" ou mandar um ZIP pra virar sugestão de template
  ID. NÃO cria nem publica jornada no SFMC; NÃO é a skill de governança de template_id
  (`gaas-governanca-comunicacoes`) nem de copy (`afinz-copy-aquisicao`).
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - SFMC
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# SFMC · Jornadas do pacote (mensagens, disparos e ranking de templates)

Funciona igual no Claude Code e no Codex. Extração e ranking são Python puro (só biblioteca padrão)
e dependem de uma consulta SQL no Supabase do GaaS (`mipiwxadnpwtcgfcedym`, tabela `activities`).
A carga na Fila usa Node 24 + o parser do repo (ver seção própria).

## Quando usar

- O Pablo mandou um ZIP do **Package Manager** (Plataforma → Package Manager → Pacote → Download).
- Ele quer saber **o que cada disparo falou** e **qual template rendeu mais**.
- Ele quer o desenho de uma jornada ou checar problemas de montagem.

## Fluxo padrão (ranking de templates)

## Régua completa e ordem de ativação

Quando o usuário pedir a régua completa ou a sequência de uma safra, buscar todos os canais (WhatsApp, SMS, e-mail e push) no mesmo contexto de BU × parceiro × segmento × safra. Apresentar pela ordem de toque/ativação, separando essa posição do Activity Name e do Template ID. Ler [regras da sequência multicanal](references/regua-completa-ordem-ativacao.md) antes de totalizar ou sugerir o próximo toque.

## Passos do ranking

1. **Extrair as mensagens**

   ```bash
   python .claude/skills/sfmc-jornadas-pacote/scripts/extract_messages.py "<pacote.zip>" [<outro.zip>] --out <pasta_saida>
   ```

   Gera `messages.json`, `messages.csv` (abre no Excel) e `results_query.sql`.

2. **Buscar resultados reais**: rodar o `results_query.sql` no Supabase (MCP do Supabase no
   Claude; no Codex, o conector/psql disponível) e salvar o retorno como `results.json`
   (lista de objetos) ou CSV. A consulta agrega `activities` por activity_name × jornada.

3. **Ranquear**

   ```bash
   python .claude/skills/sfmc-jornadas-pacote/scripts/rank_templates.py \
     --messages <pasta_saida>/messages.json --results <pasta_saida>/results.json \
     --out <pasta_saida> --filtro-jornada 21D --filtro-caminho "api serasa"
   ```

   Gera `ranking.md` e `ranking.csv`. Opções úteis:
   - `--filtro-jornada` / `--filtro-caminho`: recorte por régua e por público (ramo da decisão).
   - `--min-base` (padrão 300): abaixo disso fica fora do ranking.
   - `--maturacao-dias` (padrão 10): disparo recente recebe ⏳.
   - `--somar-outras-jornadas`: soma o mesmo activity_name usado em jornadas que não vieram no
     pacote (ex.: a mesma atividade em MAIO26 e JUL26). **Só use depois de confirmar que o
     conteúdo é o mesmo**; o padrão é não somar e listar essas jornadas no fim do relatório.

4. **Responder ao Pablo**: tabela curta por canal e por público, com o vencedor, a margem e a
   ressalva de amostra. Mostrar o texto da mensagem vencedora (bloco de código, quebras
   preservadas). Não despejar o ranking.md inteiro.

## Carregar o pacote na Fila do GaaS (você no lugar do botão "Importar pacote SFMC")

Quando o Pablo manda o ZIP e quer as sugestões de template ID na tela de Comunicações.
Usa o MESMO parser do botão (`src/modules/sfmc-package/parsePackage.ts` do repo), então o
resultado é idêntico ao import manual. Grava em nome dele (`uploaded_by`) com
`staged_via = 'agent:claude'` (ou `agent:codex`) para a Auditoria saber quem subiu.

Pré-requisitos (uma vez só):
- Node 24+ e um checkout do GaaS com `node_modules` (o script acha sozinho em
  `calendar-estrategico/` ou `calendar-estrategico/.codex-worktrees/*`; ou passe `--repo`).
- `calendar-estrategico/.env.agent` (fora do git, já excluído) preenchido pelo Pablo:
  `SUPABASE_URL=https://mipiwxadnpwtcgfcedym.supabase.co`, `SUPABASE_SERVICE_ROLE_KEY=...`,
  `GAAS_ON_BEHALF_USER_ID=187810b7-9f30-4a0d-ba85-721aa000107b` (Pablo). Nunca leia, imprima ou
  peça a chave no chat; se o arquivo faltar, peça para ele criar.

Passos:

```bash
S=.claude/skills/sfmc-jornadas-pacote/scripts/fila_agente.mts
node $S carregar "<pacote.zip>" --escopo B2C --saida <pasta>     # parse + stage + cruzamento + rascunho de notas
#   --simular: só parseia (sem credencial), útil pra conferir contagens antes
# revise <pasta>/notas.json: ajuste o texto, troque "info" por "hipotese"/"pergunta" quando for o caso
node $S anotar <pasta>/notas.json                                 # grava "Análise do Claude" em cada proposta
node $S cruzar <import_id> --saida <pasta>                        # refaz o cruzamento quando activities atualizar
node $S sugerir <pasta>/cruzamento.json --saida <pasta>           # ID para peças SEM ID (topo CRM por regra; senão ID único de activities)
node $S propor <pasta>/propostas.json                             # grava ID proposto; status vira "Com pendências"
```

O que acontece no banco (migration `20261008013347_sfmc_agent_staging`, só `service_role`):
- `stage_sfmc_package_as_agent` faz as mesmas validações do botão; o gatilho existente cria as
  propostas (`governance-v2.1`: af_sub3 observado vira ID proposto).
- `sfmc_agent_cross(import_id)` devolve, por peça governada: utm, catálogo (status, tem peça),
  execuções na mesma jornada e em outras, datas, template_id já gravado e colunas
  BU/Segmento/Oferta/Promocional/Canal de `activities`.
- `propose_templates_as_agent` (migration `20261008020946_sfmc_agent_propose`) preenche o ID só em proposta
  ainda não revisada, sempre como 'review', soma razões/conflitos e registra evento `agent_proposed`.
- `annotate_proposals_as_agent` só grava evento `agent_note` (erro/hipotese/pergunta/info).
  Não muda status, ID proposto nem `activities`. Aprovar e Enviar é sempre do Pablo, na tela.

Rascunho de notas (regras em `fila_agente.mts`, revisar antes de anotar):
template_id já gravado diferente (pergunta, nunca sobrescrever) · ID fora do catálogo ·
catálogo sem peça · sem disparo · rodou só em outra jornada · af_sub1 x Segmento ·
c (copa/vibe) x Oferta/Promocional · af_sub2 x sufixo do ID · prefixo bb_/b2c_ x BU ·
activity sem taxonomia (único "erro" automático) · alertas do parser.

Depois de carregar, responda ao Pablo com: quantas propostas entraram, quantas prontas,
conflitos, IDs fora do catálogo e o que ficou sem disparo. Lembre que a fila mostra só o que
disparou no período do calendário (botão "Mostrar fora do período" para o resto).

**Cobertura:** um pacote só traz as jornadas que foram colocadas nele, de UMA BU do SFMC.
Para cobrir um mês inteiro, compare as jornadas do pack com `activities` do mês (consulta em
`references/anatomia-pacote.md`, seção Cobertura) e peça os packs que faltam (Plurix é outra BU;
carrinho diário e topo CRM costumam ficar de fora). E-mail do Plurix é dinâmico (AMPscript):
o texto e o af_sub vêm da DE de briefing, não do pacote. Os demais e-mails trazem o af_sub3 no HTML. O ID de e-mail/SMS de topo CRM sai da regra
em `references/logicas-crm.md` (D = ordem do disparo, disp4 repete D02, bsp só B2C, parceiros crm).

## Raio-x de jornada (quando ele pedir o desenho ou uma auditoria)

```bash
python .claude/skills/sfmc-jornadas-pacote/scripts/xray.py "<pacote.zip>" > raiox.md
```

Mostra entrada (DE + filtro), decisões, splits, esperas, mensagens, Update Contact, meta e
saída de cada jornada.

## Regras de leitura (não negociáveis)

1. **Compare dentro do mesmo público.** Ramos diferentes da decisão são populações diferentes.
   No carrinho, `api serasa` (eCred) e `institucional` têm escala e semântica distintas:
   em Serasa as propostas passam da base (lead externo pré-qualificado, ver vault
   `Dimensao-Canonica-de-Parceiro`). Rode o ranking separado por `--filtro-caminho`.
2. **Métrica principal = cartões / base acionável** (função-objetivo tática do `CLAUDE.md`).
   CAC entra como restrição, não como critério de ordenação. Recalcule das contagens; nunca
   faça média de colunas de taxa.
3. **Confiança vem da base, não da conversão**: alta ≥ 5.000, média ≥ 1.000, baixa ≥ 300,
   insuficiente abaixo disso. Conversão zero com base grande é resultado válido.
4. **Imaturo não é perdedor.** Disparo com menos de ~10 dias, ou linha sem cartão preenchido,
   fica sinalizado, não ranqueado contra os maduros.
5. **Ligação mensagem ↔ disparo é pelo Activity Name** (`activities."Activity name / Taxonomia"`,
   com `btrim`) e pela jornada normalizada (`JOR_AQS_` = `JOR_AQUISICAO_`, espaço no fim
   ignorado). Mensagem sem linha em `activities` vai para "sem resultado ligado". Não invente
   ligação por semelhança de nome.
6. **Respostas de opt-out** (`..._resposta_optout_...`) são a mesma atividade em várias jornadas:
   ficam fora do ranking por padrão.
7. **Inconsistência ≠ erro.** Boa parte do que parece errado é lógica da operação que ainda não
   está documentada (ver `references/logicas-crm.md`). Classifique em três baldes:
   **erro confirmado** (evidência de impacto, ex.: parâmetro trocado no texto),
   **hipótese a confirmar** (Test Send / log) e **lógica a perguntar**. Pergunte ao Pablo
   antes de chamar de bug e registre a resposta em `references/logicas-crm.md`.
8. Nunca publicar, ativar ou alterar nada no SFMC a partir desta skill.
9. **Ocorrência e ramificação são a unidade de leitura.** Preserve jornada + versão + activity_key e todos os caminhos que chegam à atividade. Em cada caminho, conserve atividade de decisão, outcome (chave e rótulo), condição, atividade de referência de engajamento e esperas/janelas Einstein. Não reduza caminhos diferentes a um único momento ou ao primeiro ramo encontrado.
10. **Reuso de peça é permitido.** Mesmo asset, HTML ou Template ID em atividades/posições diferentes não é erro nem duplicidade de ocorrência. Separe identidade do conteúdo, Template ID observado no link, ID proposto/aprovado e posição operacional da atividade. Um disp4 pode reutilizar a peça D02; preservar ambos. Conteúdo igual não autoriza colapsar nós nem transferir métricas entre públicos. Só apontar incompatibilidade quando existir evidência além do reuso.
11. **Desenho com rastreabilidade.** Cada nó de comunicação mostra preview, nome da peça, Template ID observado e Activity Name completo em área própria (quebra de linha; nunca usar só o ID como referência). Decisões mantêm Sim/Não/Restante e a atividade cujo engajamento avaliam. Saída, atualização de contato e espera não são comunicações. Registrar ausências do pack em vez de completar com suposições.

Para desenho, extração enriquecida ou análise de reuso, leia [ramificações e ocorrências](references/ramificacoes-e-ocorrencias.md).


## O que vem em cada mensagem (`messages.json`)

`jornada`, `jornada_versao`, `de_entrada`, `filtro_entrada`, `caminho` (rótulos de decisão/split
até a mensagem), `esperas_antes`, `activity_name`, `canal`, `template_meta` (nome do template
aprovado na Meta), `asset_nome`, `parametros` (o que preenche `${1}`, `${2}`…), `texto`,
`rodape`, `cta1`, `cta2`, `banner`, `banner_url` (imagem do cabeçalho), `link`, `c`, `af_sub1`, `af_sub2`, `af_sub3`,
`sms_remetente`, `alertas`.

Alertas automáticos: campo de personalização fora da DE de entrada, nome da atividade com canal
diferente do canal real, atividade sem nome de taxonomia, WhatsApp com link sem `af_sub3`.
Lembre da regra 7 antes de tratar um alerta como erro.

## Limites conhecidos

- Só o e-mail do Plurix é dinâmico (AMPscript): texto e af_sub vêm da DE de briefing. Os e-mails de
  B2C, BB e Dia são HTML normal e o af_sub3 sai do link no corpo do asset (parser 1.1.0, igual no
  Python e no GaaS). SMS também: o link rastreado está no texto do asset.
- O pacote mostra a **versão exportada** da jornada. Versões anteriores podem ter usado outro
  template com o mesmo Activity Name.
- Resultados dependem da ingestão em `activities`: linhas recentes podem estar sem safra e sem
  resultado (visto em set/2026 para jornadas `JOR_AQS_`).

## Arquivos

- `scripts/extract_messages.py`: extrai mensagens e gera a consulta de resultados.
- `scripts/rank_templates.py`: liga resultados e ranqueia.
- `scripts/xray.py`: desenho/auditoria das jornadas.
- `scripts/pkg_common.py`: leitura do pacote (usado pelos outros).
- `scripts/fila_agente.mts`: carrega o pacote na Fila do GaaS, cruza com activities e anota (Node 24).
- `references/anatomia-pacote.md`: estrutura do ZIP e de cada tipo de atividade.
- `references/logicas-crm.md`: lógicas da operação já confirmadas e as que estão em aberto.

Vault relacionado: `04-Operacao/AppsFlyer-Tracking-CRM.md`, `04-Operacao/Formatacao-WhatsApp-Variaveis-e-Espacamento.md`,
`02-Entidades-Dados/Dicionario-de-Produtos/Pode-Dizer-Nao-Pode-Dizer.md`, `01-Conceitos/Carrinho-Abandonado.md`,
`01-Conceitos/Repescagem.md`, `01-Conceitos/Upgrade.md`.
