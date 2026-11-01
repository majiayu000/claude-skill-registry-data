---
name: afinz-pptx
description: Cria apresentações PowerPoint (.pptx) com a identidade visual oficial
  da Afinz — paleta de cores, tipografia, logo e grafismos do guia de marca institucional.
  Use sempre que o usuário pedir slides, deck, apresentação ou .pptx no contexto Afinz,
  incluindo relatórios de growth/performance (CAC, safra, campanhas, KPIs), relatórios
  de gastos/resultados de mídia paga por período, comunicação institucional/interna,
  planos de mídia paga por frente (Aquisição, Branding, Rentabilização, Seguros, Plurix),
  e decks de campanha comercial ou parceria de marca. Aplica verde D3FF00 para PJ
  e azul 00C6CC para PF, fundo escuro como assinatura, fonte Lembra com fallback Calibri.
metadata:
  version: 1.0.0
  origin: cowork
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Apresentações
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

---
name: "afinz-pptx"
description: "Cria apresentações PowerPoint (.pptx) com a identidade visual oficial da Afinz — paleta de cores, tipografia, logo e grafismos do guia de marca institucional. Use sempre que o usuário pedir slides, deck, apresentação ou .pptx no contexto Afinz, incluindo relatórios de growth/performance (CAC, safra, campanhas, KPIs), relatórios de gastos/resultados de mídia paga por período, comunicação institucional/interna, planos de mídia paga por frente (Aquisição, Branding, Rentabilização, Seguros, Plurix), e decks de campanha comercial ou parceria de marca. Aplica verde D3FF00 para PJ e azul 00C6CC para PF, fundo escuro como assinatura, fonte Lembra com fallback Calibri."
---

# Afinz PPTX — Apresentações com a marca Afinz

Cria decks `.pptx` fiéis ao guia de marca institucional da Afinz. Esta skill é uma
camada de marca **sobre** a skill `pptx` genérica: a skill `pptx` continua responsável
pela mecânica (criar/editar/QA de slides); esta aqui impõe cores, fontes, logo e regras
da marca.

## Regra zero — sempre pergunte o público

A marca Afinz usa **cores diferentes por audiência**. Antes de gerar qualquer slide,
confirme com o usuário:

> Esse deck é para público **PF** (pessoa física), **PJ** (lojista/empresa) ou **Institucional** (ambos)?

A resposta define a cor dominante. Se o usuário já deixou claro no pedido (ex: "deck para
lojistas" = PJ; "campanha de cartão pra clientes" = PF), confirme em uma linha e siga.

## Workflow

```
Afinz Deck Progress:
- [ ] 1. Confirmei o público (PF / PJ / Institucional)
- [ ] 2. Li brand_spec.md e carreguei a paleta + regras
- [ ] 3. Defini o conteúdo dos slides (dados/insights já em mãos)
- [ ] 4. Escolhi o template-base certo e gerei o deck a partir dele
- [ ] 5. Apliquei cores/fontes via scripts/apply_afinz_brand.py
- [ ] 6. Rodei QA visual (converti em imagem e inspecionei) — feedback loop
- [ ] 7. Salvei no folder do usuário e apresentei
```

**Passo 4 — sempre comece do template-base certo.** Não gere do zero.

Para deck institucional, relatório, growth/KPIs ou **plano de mídias**: use
`assets/afinz_template_institucional.pptx` (16:9, 13.33"×7.5", 22 layouts nomeados,
slide master e logo oficial já embutidos).

Para deck de **campanha comercial, parceria de marca ou ativação sazonal**: use a skill irmã
**`afinz-pptx-campanha`**, que tem 12 layouts a mais, incluindo a capa temática. Invoque as
duas juntas.

Use o workflow de edição da skill `pptx`: unpack → manipular slides → editar conteúdo → pack.

**Passo 5 — aplique a marca de forma determinística.** Rode:

```bash
python scripts/apply_afinz_brand.py deck.pptx --audience pf   # ou pj | institucional
```

O script força as cores hex exatas e a fonte correta. Não confie em "aplicar a cor na mão".

**Campanha sazonal ou com parceiro?** Adicione `--extra-accent` com o hex do acento temático,
ou o script vai remapeá-lo para o azul/verde dominante.

## Especificação da marca

Paleta, tipografia e regras de uso em **[brand_spec.md](brand_spec.md)**. Resumo operacional:

| | PF | PJ | Institucional |
|---|---|---|---|
| Cor dominante | Azul `#00C6CC` | Verde `#D3FF00` | Azul + Verde equilibrados |
| Acento | Verde como apoio | Azul como apoio | Vermelho `#E74742` pontual |

**Constantes:**

- Preto `#000000` e branco `#FFFFFF` são a base. **Fundo escuro é a assinatura visual** — use
  em capa, divisórias e slide final.
- Headings em **caixa-baixa** por padrão. Se o usuário pedir sentence case, aplique em todos.
- Fonte: **Lembra** (oficial) com fallback **Calibri**. Assuma Calibri como fonte real gravada
  no arquivo. Nunca use Arial.
- Logo: `assets/afinz_logo.png`. Nunca distorça, recolora ou gire.
- **Só as cinco cores da marca.** O script remapeia cinza para preto e qualquer cor fora da
  paleta para o acento dominante — um card cinza-claro vira um bloco preto.

## Estilo dos slides

- **Estrutura sanduíche**: capa preta com neon → conteúdo em fundo claro → fechamento preto.
- **Verde/azul são acentos**, não fundo de texto longo. Use para números grandes, barras,
  ícones e blocos de destaque.
- Uma cor domina (60-70%), a outra apoia.
- Stat callouts grandes para números-âncora em fundo preto.

## Geometria do template institucional

- Slide 13,333" × 7,5". Layout `Slide de Tabela`: header cinza claro de 0 a 1,89", corpo
  branco abaixo. Placeholders: título idx 16, subtítulo idx 17, tabela idx 12 (remova).
- Área útil: esquerda 0,74" · direita 12,59" · topo 2,12" · base 6,86".
- **Bandas de rodapé: no máximo até 6,75" de altura e 10,6" de largura.** O logo ocupa o canto
  inferior direito a partir de 11,67".
- Rodapé de fonte a 7,02". Linha de tabela 0,30" a 0,40". Separador: retângulo de 0,012".
- Layouts mais usados: `Capa` · `Slide respiro / Título` (divisórias) · `Slide de Tabela`
  (workhorse) · `Fechamento`.

## QA (obrigatório)

Use o processo da skill `pptx` (converter em imagem e inspecionar). Além disso, verifique:

- [ ] Cor dominante bate com o público?
- [ ] Nenhuma cor default do Office sobrou?
- [ ] Logo presente, sem distorção?
- [ ] Contraste OK?
- [ ] Nenhuma banda passando de 6,75" ou colidindo com o logo?

---

# Plano de Mídias — arquitetura de referência

Seção específica para o deck de plano de mídia paga da Afinz. Referência aprovada:
`Plano_de_Midias_Afinz_Vibe_Ago26.pptx`, 14 slides.

## Fontes de dados

**Planilha do plano** (`Plano_de_Midias_Afinz_Vibe_v*.xlsx`). Localize por padrão, nunca por
nome fixo. Liste as abas antes de assumir quantas são — o arquivo cresce por versão.

| Aba | O que dá ao deck |
|---|---|
| `00_Resumo_Estrategico` | Frentes, objetivo, KPI herói, regras |
| `01_Plano_de_Midias` | Verba total e por frente, campanhas, evento, destino, território de mensagem, status |
| `02_Audiencias_e_Grupos` | Grupos com origem, modo de segmentação, exclusões, direito de uso |
| `03_Mensuracao_e_QA` | Mensuração, testes, checklist de publicação |
| `04_Roteiro_PPT` | Roteiro proposto — ponto de partida, nunca especificação |
| `05_Projecao_KPIs` | Cenários por campanha, fatores, baselines |
| `06_Plano_de_Criativos` | Briefing por grupo, conceitos, variações, formatos, refresh |

**Supabase `GaaS Framework Afinz`** (project id `mipiwxadnpwtcgfcedym`):
`paid_media_metrics` (histórico real de Meta e Google — origem de CPM, CTR, CPC e custo por
evento) · `event_map` (mapa governado de eventos, origem da escada) · `copa_visa_daily`.

**Vault Obsidian** (`docs/AFINZ_GAAS_ONTOLOGY.md`): taxonomia de segmentos, etapas de
aquisição, arquitetura de audiências por frente.

## Os 14 slides

Divisórias no layout `Slide respiro / Título` fazem o deck respirar e são o que permite
explicar falando.

| # | Slide | Pergunta que responde |
|---|---|---|
| 1 | Capa | Qual plano, qual período |
| 2 | **Divisória: Estratégia mídia paga** | — |
| 3 | Objetivo e divisão de investimento por frente ativa | O que cada frente entrega e quanto custa |
| 4 | Peças e KVs | O que vamos dizer e quanto precisa ser produzido |
| 5 | **Divisória: Estrutura de campanhas** | — |
| 6 | Aquisição | Como a frente está montada |
| 7 | Branding | idem |
| 8 | Rentabilização | idem |
| 9 | Seguros | idem |
| 10 | **Divisória: Projeções e acompanhamento** | — |
| 11 | Projeção por campanha | Quanto esperamos e de onde vem o número |
| 12 | Acompanhamento e decisão por métrica | O que medimos e o que decidimos quando |
| 13 | O que fica fora deste ciclo | O que está parado e o que destrava |
| 14 | Próximos passos | O que acontece depois da reunião |

**Criativo (slide 4) vem antes do detalhe das frentes.** O deck estabelece o que será dito
antes de detalhar onde será veiculado. Decisão validada, serve a reuniões com marketing na
sala. **Não existe apêndice** no deck aprovado.

## Anatomia do slide de frente (6 a 9)

Cinco blocos fixos, sempre na mesma ordem. A repetição é intencional: cada dono de área lê um
slide só.

**A · Faixa de topo** — retângulo preto, largura total, 0,58" de altura. Cinco pares
rótulo/valor: Verba mensal · Verba diária · Canais · KPI principal · Última etapa medida.
Rótulo ciano 7,5pt, valor branco 10,5pt negrito.

**B · Colunas de plataforma** — duas colunas de 4,01", a 0,58" e 5,12". Logo da plataforma em
PNG (~0,45"), card branco com contorno preto contendo nome da campanha e verba mensal.

**C · Lista de conjuntos** — uma linha por grupo: `➔ nome · verba · status`. Status é caixa
colorida com texto, nunca bolinha. Verde pronto, ciano piloto, vermelho bloqueado ou
aguardando. Se a planilha não define verba por conjunto, divida a da campanha igualmente e
declare no rodapé.

**D · Coluna de segmentação** — retângulo preto à direita a partir de ~9,7", largura ~3,3".
Título "Segmentação" em verde, um bloco por audiência: nome em ciano, descrição em prosa de
2 a 3 linhas em branco 8,8pt. **Aqui mora o detalhe que não cabe na tabela** — quem é a
pessoa, o que já fez, o que a exclui. É o bloco que diferencia o deck de uma planilha
exportada. Padrão herdado de deck de agência.

**E · Faixa de KVs** — cards numerados, largura útil até 8,70" para não invadir a coluna de
segmentação. Cada card: barra colorida à esquerda com "KV n", nome do conceito entre aspas,
quem recebe em ciano, selo "Novo" ou "Avaliar acervo", chips brancos com os quatro formatos.

**F · Nota de rodapé** — uma linha, 8,5pt, com fonte ou ressalva.

## Cores por frente

| Frente | Tratamento |
|---|---|
| Aquisição | Ciano preenchido |
| Rentabilização | Ciano vazado |
| Branding / Brandformance | Verde preenchido |
| Seguros | Verde vazado |
| Plurix e standby | Preto |

Cheio e vazado agrupam por família: azul é a jornada do cartão, verde é marca e cross-sell.
**Vermelho nunca identifica frente** — só alerta e bloqueio. A cor se repete em cinco lugares:
chip do slide 3, faixa do slide da frente, barra da projeção, marcador do slide 4 e resumo.

## Modelo de decisão — Messy Middle, não funil

O deck usa o ciclo do estudo *Decoding Decisions* (Google e The Behavioural Architects, 2020):
**Exposição** envolve tudo, **Gatilhos** disparam, o laço **Exploração ↔ Avaliação** é onde a
decisão acontece, depois **Compra** e **Experiência**, que realimenta o laço.

| Posição | Frente |
|---|---|
| Exposição | Branding — lookalike e display contextual |
| Gatilhos | Serasa, aprovados e negados do CRM |
| Exploração | Branding — search de intenção e display em cupom e cashback |
| Avaliação | Brandformance — audiência exata levando à landing |
| Compra | Aquisição — Meta App e Display |
| Experiência | Rentabilização e Seguros |

**Ressalva obrigatória:** o estudo descreve categorias de escolha aberta. Cartão de crédito tem
uma camada acima do ciclo — elegibilidade. Por isso o plano opera em lista própria: não é
limitação de alcance, é a aplicação da recomendação do estudo de encurtar a distância entre
gatilho e compra.

**Brandformance ≠ Branding.** Brandformance é tráfego para audiência qualificada, medido por
visita à landing. Branding é reconhecimento, medido por lembrança estimada.

## Criativo — KV, desdobre e peça

Três níveis, nunca confundir:
- **KV** — a ideia visual original. Trabalho de criação. Serve o **território de mensagem**,
  não o grupo de anúncio.
- **Desdobre** — o mesmo KV em outro formato. Execução.
- **Peça** — o arquivo final que entra na plataforma, direcionado ao grupo.

**Territórios (gatilhos):** Solicitar cartão · Retomar pedido · Avaliar · Lembrar · Usar ·
Proteger. Grupos do mesmo território dividem o KV e mudam só copy e destino. Se cada grupo
tivesse KV próprio, a produção dobraria para dizer as mesmas seis coisas.

**Formatos:** Meta 4:5 (1080×1350) · Meta 9:16 (1080×1920) · Display 1:1 (1200×1200) ·
Display 1,91:1 (1200×628). Vídeo só no Meta.

**Regra do número de desdobres** — formatos por canal × tipos de peça:
Meta e Display sem vídeo → 4 · Meta e Display com vídeo → 6 · só Meta com vídeo → 4.
**Escreva a regra no slide**, senão 4 e 6 parecem arbitrários.

**Search não gera KV visual** — são títulos e descrições. Diga se é revisão de copy existente
ou criação do zero.

**Com a criação, fale em KV estático e vídeo, não em desdobre.** Eles produzem conceito e
vídeo; desdobre é adaptação.

## Regras de conteúdo que não se negociam

**Três categorias de dado.** Todo número é *realizado*, *projetado* ou *pendente*, e o slide
diz qual. Projeção leva selo próprio. "Pendente" nunca vira estimativa.

**Baseline própria antes de benchmark externo.** Confira CPM e CTR contra `paid_media_metrics`.
Se bater, diga no slide que bate — é o que dá credibilidade. Se o benchmark externo divergir
do dado próprio, use o próprio.

**Não comparar CPA de plataforma com CAC de CRM.** CRM ativa base já adquirida, mídia paga
compra alcance novo.

**Não somar unidades heterogêneas.** Arquivo de Meta, asset de Display responsivo, asset
textual de Search e asset group de PMax são quatro moedas. Não existe "total de peças".

**Verba é mensal; ritmo é diário.** A tabela mostra verba mensal e verba diária (mensal ÷ 31).
Se a janela não cobre o mês, confirme com o usuário — não assuma.

**Nenhum nome próprio.** Responsabilidade é sempre área.
**"Regras", nunca "guardrail".**

## Processo específico do plano de mídias

1. Localizar o arquivo mais recente, listar as abas, ler todas.
2. Consultar `paid_media_metrics` e `event_map` no Supabase.
3. **Verificação de integridade antes de escrever qualquer slide:** contagem real de campanhas
   e grupos incluindo buracos de numeração · soma das verbas contra o total · IDs cruzados
   entre abas (quando divergirem use o **nome operacional**) · grupos simultaneamente com
   direito de uso aprovado e status pronto. Reporte os achados antes de continuar.
4. **Produzir um contra-roteiro** — diagnóstico da narrativa, o que cortar, o que falta, a tese
   em uma frase. Submeter. O roteiro da aba `04` é ponto de partida, não destino.
5. Seguir do passo 5 do workflow geral.

**Se o usuário já editou uma versão, edite o arquivo dele — não regenere.** Ele adiciona logos,
divisórias e correções de texto que se perdem numa regeração. Para editar com python-pptx,
identifique shapes por posição e remova com `sh._element.getparent().remove(sh._element)`.

## Erros que já custaram retrabalho

- Apontar para o arquivo errado por usar nome fixo em vez de padrão.
- Tratar o roteiro da planilha como especificação e não produzir contra-roteiro.
- Transformar todo slide em tabela porque a fonte é planilha. Varie: diagrama, cards, escada,
  faixa de status.
- Somar arquivos de Meta com assets de Display.
- Quebrar uma frente em várias linhas por causa de uma coluna de situação — se a coluna sair,
  a quebra perde o motivo.
- Bandas de largura total colidindo com o logo.
- Cinza claro em card, que o script de marca transforma em preto.
- Inventar prazos e fases que a planilha não tem sem marcar como proposta.

---

# Relatório de Resultados — arquitetura alternativa (financeiro, tom de fechamento)

Segunda arquitetura de referência, para um caso de uso diferente do plano de mídias: **prestar
contas de investimento e resultado de um período fechado** (trimestre, mês) a um público
diretor/executivo. Referência aprovada: `Relatorio_Gastos_Trimestral_Midia_Paga_Mai-Jul26.pptx`,
7 slides, período maio–julho de 2026.

## Quando usar esta arquitetura em vez da do Plano de Mídias

| Situação | Arquitetura |
|---|---|
| Planejar o próximo ciclo, apresentar estratégia, briefar criação | Plano de Mídias (14 slides) |
| Prestar contas de um período fechado — quanto foi gasto, o que voltou | Relatório de Resultados (esta seção) |
| Público é diretor/liderança que só quer saber "quanto custou e o que trouxe" | Relatório de Resultados |
| Público é o time de marketing que vai executar | Plano de Mídias |

## A virada de tom que definiu esta arquitetura

A primeira tentativa (v2) abriu com um número-herói de alerta: "metade da verba do trimestre não
tem leitura de retorno". O usuário rejeitou — não porque estivesse errado, mas porque **não é
isso que se leva pra diretoria**: "não queremos passar isso pro diretor, ele só quer saber mais
de financeiro e o que é feito com a verba". A virada foi trocar diagnóstico por prestação de
contas: tabela limpa, sem alarme, sem explicar lacuna de medição no corpo do slide. A ressalva de
qualidade de dado que for necessária vai em **nota de rodapé factual**, nunca em bloco de texto
que soe como pedido de desculpas.

**Regra derivada: para público de diretoria, o corpo do slide é fato financeiro. Incerteza e
diagnóstico de causa vivem no rodapé ou nas notas do apresentador — nunca competem com o número
principal pela atenção de quem só tem 30 segundos.**

## Os 7 slides

| # | Slide | Conteúdo |
|---|---|---|
| 1 | Capa | "Mídia paga · Relatório de gastos trimestral", subtítulo com o período |
| 2 | Visão de investimento total | Tabela: frente × objetivo × mês a mês × total × % da verba, com linha de total no rodapé |
| 3 a 6 | Um slide por frente | Tabela mês a mês: custo, impressões, CPM, cliques, CPC, resultado principal da frente, custo por resultado — mais linha de trimestre |
| 7 | A verba do próximo ciclo | Tabela: frente × o que muda × verba do mês anterior × verba do próximo ciclo |

Sem divisórias, sem apêndice, sem slide de "o que aprendemos" — é prestação de contas, não
storytelling. O texto de abertura de cada slide de frente é uma frase de objetivo, não uma tese.

## Arquitetura da tabela por frente (slides 3 a 6)

Colunas fixas em toda frente: **Mês · Custo · Impressões · CPM · Cliques · CPC**. Depois entram
as colunas específicas do resultado da frente — **isso muda por objetivo, não é genérico**:

| Frente | Colunas de resultado |
|---|---|
| Aquisição (instalação → início de proposta) | Instalações · Custo por instalação · Inícios de proposta · Custo por início de proposta |
| Rentabilização (objetivo é o próprio clique, não há evento além dele) | CTR — não force uma coluna de "resultado" que não existe; o clique já é o resultado |
| Seguros (lead) | Leads · Custo por lead |
| Plurix (instalação, mas sem canal de medição confirmado) | Instalações · Custo por instalação — **ou "(sem leitura)" se o dado não estiver confirmado, ver seção abaixo** |

Toda linha termina em **Trimestre**, com os totais e (quando fizer sentido) a média ponderada de
CPM/CPC — não a soma.

**Formatação obrigatória:** todo valor monetário leva `R$` — custo, CPM, CPC, custo por
resultado. Impressões, cliques e contagens de resultado (instalações, leads) não levam prefixo.
Percentuais levam `%`. Foi um retrabalho real: a primeira versão só tinha `R$` na linha de custo
e não nas outras colunas monetárias.

## Regra inegociável: nunca rotular um número sem confirmar a fonte

Esta é a lição mais cara desta arquitetura. Na v3, o slide de Plurix trazia "980 instalações" em
maio, puxado da coluna `conversions` de `paid_media_metrics`. Ao ser questionado de onde vinha
esse número, a investigação direto no Meta Ads (via MCP, `ads_get_ad_entities` no nível de
campanha) mostrou que o campo `results`/`conversions` da campanha **retorna "Not available"
para o indicador de instalação em todos os três meses do trimestre, inclusive maio** — ou seja,
o 980 nunca foi confirmado como instalação. Nenhum dos campos testados (`app_install`,
`mobile_app_install`, `omni_app_install`, `landing_page_view`, `lead`, `post_engagement`) batia
com o número. E o app do Plurix (+amigo) nunca foi cadastrado no AppsFlyer
(`appsflyer_governed_apps` só tem o app Afinz/Sorocred).

**Decisão tomada:** remover o número da tabela e usar `(sem leitura)` nas três colunas de
resultado de Plurix, mesmo tendo um valor numérico disponível no banco. Um número sem fonte
confirmada é pior que nenhum número — ele parece dado e não é.

**Rotina obrigatória antes de rotular qualquer coluna de "resultado" com o nome de um evento**
(instalação, lead, início de proposta etc.):

1. O nome da coluna em `paid_media_metrics` não é a verdade — é o nome que o pipeline deu. Puxe
   o resultado **direto da plataforma** (Meta Ads MCP, `ads_get_ad_entities` com `results` e
   `cost_per_result` no nível de campanha) e confira se o indicador bate com o que você vai
   escrever no slide.
2. Se a plataforma responder "Not available" para o indicador esperado, **o número da tabela não
   pode levar esse rótulo** — vire "(sem leitura)" ou remova a coluna.
3. Para eventos de app, confira `appsflyer_governed_apps` no Supabase: se o app não está lá, não
   existe MMP conectado e a reconciliação nem é possível.
4. Documente a causa raiz encontrada — não escreva simplesmente "sem leitura" sem saber por quê;
   isso é o que separa um relatório confiável de um que só parece confiável.

## Risco de pipeline: dias inteiros podem faltar sem aviso

Ao comparar o gasto total do Meta (via MCP) com a soma de `paid_media_metrics`, apareceu uma
divergência de ~4,7% no trimestre — não de uma frente, **de todas ao mesmo tempo**. Causa: quatro
datas de calendário (28/06, 24/07, 25/07, 26/07) tinham só 2 ou 3 campanhas registradas em vez
das 5 esperadas — um buraco de sincronização, não erro de campanha.

**Antes de fechar qualquer relatório de período, rode esta checagem:**

```sql
with cal as (select generate_series('<inicio>'::date,'<fim>'::date,'1 day') d)
select c.d from cal c
left join paid_media_metrics p on p.date = c.d and p.campaign ilike '%<frente>%'
where p.date is null
```

Se aparecerem datas, compare o gasto real dessas datas direto no Meta Ads (MCP) antes de decidir
se corrige o relatório ou registra a pendência. **Decisão do usuário nesta ocorrência: não
recalcular o deck já pronto em cima da hora — registrar a pendência e corrigir no próximo
fechamento.** Isso é uma escolha válida sob prazo, mas precisa ser uma escolha consciente, não um
buraco que ninguém viu. Detalhe completo: `Falha-Sincronizacao-Meta-Supabase-4Dias-Ago26.md` no
vault Obsidian.

## Exemplo de referência

`Relatorio_Gastos_Trimestral_Midia_Paga_Mai-Jul26.pptx`, na raiz do repositório do projeto —
versão final aprovada pelo usuário, com edições manuais de texto por cima da versão gerada. Ao
construir um relatório novo com esta arquitetura, comece lendo esse arquivo com a skill `pptx`
para herdar a geometria exata de tabela, espaçamento de linha e formatação de rodapé — não
reconstrua do zero.

## Dependências

- Skill `pptx` (mecânica + QA) — esta complementa, não substitui.
- `python-pptx`, LibreOffice e Poppler para QA visual.
- MCP do Meta Ads para confirmar indicadores de resultado antes de rotular qualquer coluna.
- Supabase `GaaS Framework Afinz` (`mipiwxadnpwtcgfcedym`), tabela `paid_media_metrics`, para os
  números de custo/impressão/clique, sempre com a checagem de dias faltantes acima.

