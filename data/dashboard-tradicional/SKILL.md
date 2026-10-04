---
name: dashboard-tradicional
description: >
  Sobe/verifica/derruba o dashboard local "Geral/Turnover/Funil de Aquisição"
  da Tradicional.bet.br (origem: Jonatas Souza; mantido pelo PM +
  Orquestrador desde 02/09/2026) — funil de cadastro (flags de estado), funil
  de recorrência de depósito (FTD → 2º/3º/.../7º+ depósito), funil de
  aquisição/jornada de cadastro granular por eventos em dwh.player_events
  (catálogo versionado em dwh.registration_steps, ranking de etapas com mais
  perdas, sinais de atrito, tempo entre passos), GGR/NGR, tráfego pago,
  taxonomia de frente por btag. Roda local na máquina do usuário (Flask + Chart.js), autenticado com o
  token IAM pessoal do usuário no trad_prd — sem senha compartilhada. Use
  quando o usuário pedir "abre o dashboard", "sobe o backoffice", "quero ver o
  funil em tempo real", "onde a gente está perdendo gente no cadastro", ou
  perguntar por métricas que esse dashboard já cobre antes de reconstruir a
  análise via query-trad/agente-dados do zero.
---

# Dashboard Geral/Turnover/Funil de Aquisição — Tradicional.bet.br

App local (Flask + SQLite de cache) em `tools/dashboard-tradicional/` (dentro
deste repositório), recorte do dashboard pessoal de Jonatas Souza. **Antes de
reconstruir uma
análise de funil/retenção/tráfego via SQL manual (`query-trad`/`agente-dados`),
confira se esse dashboard já cobre a pergunta** — ele tem rotas prontas para:

- `/api/funil_cadastro` — funil macro por flags de estado (pré-cadastro →
  telefone → e-mail → cadastro → verificado/KYC → depositante), com filtro por
  frente/btag/afiliado. Histórico completo, aba **Geral**.
- `/api/funil_aquisicao` — **atenção ao nome**: apesar do nome da rota, isto é
  retenção de depósito (FTD → 2º, 3º... 7º+ depósito), exibido na aba Geral sob
  o título "Funil de Recorrência de Depósito". Não confundir com a aba
  **Funil de Aquisição** abaixo — são conceitos diferentes que só coincidem no
  nome da rota por histórico do código.
- `/api/funil_jornada`, `/api/funil_jornada_diario`, `/api/funil_atrito`,
  `/api/funil_tempo_passos` — aba **Funil de Aquisição**: jornada granular de
  cadastro por eventos em `dwh.player_events`, com catálogo de passos
  versionado em `dwh.registration_steps`. Cobre: funil com todas as etapas,
  ranking de etapas com mais perdas, evolução por dia (tabela), sinais de
  atrito (reenvio de código, troca de telefone/e-mail, câmera negada) e tempo
  mediana/p90 entre passos consecutivos.
  **Só existe dado a partir de 27/08/2026** (26/08 é dia quebrado), e os
  últimos ~3 dias são provisórios — ingestão tardia ainda faz o número subir.
  As respostas trazem `avisos[]` com essas ressalvas; o dashboard as exibe
  acima do funil.

  ⚠️ **Corrigido em 02/09/2026** — antes disso a aba divergia **4x** do
  `/api/funil_cadastro` (1.700 contas contra 336 entidades no mesmo dia).
  Três defeitos: (1) usava `registration_completed` como conclusão, mas esse
  evento é disparado pela **revalidação de liveness no login** — 96% vinham de
  conta antiga reentrando; (2) filtrava por `player_events.created`, que é data
  de **ingestão**, não de ocorrência; (3) não separava a coorte de cadastro
  novo da de revalidação. Hoje o marco é `account_created` e a aba fecha
  **97,5–99,0%** com `public.entities`. Detalhes e evidências em
  `knowledge/decisions/2026-09-01-funil-eventos-usa-account-created-e-data-de-ocorrencia.md`.

  ⚠️ **A instrumentação do meio do funil é incompleta, e isso não é fricção.**
  Em 29/08 foram 946 contas criadas, mas só 509 `email.submitted`, 267
  `consent.submitted` e 219 `kyc.provider_handoff_completed` — não se cria
  conta sem passar por esses gates, logo eles não emitem evento para todo
  mundo. Cada etapa vem com `cobertura_pct` e `instrumentacao_parcial`, e a
  conversão (`pct_da_etapa_anterior`) só é calculada entre marcos confiáveis —
  nos demais vem `null` de propósito. **Não preencha esse `null` com conta
  própria.** A cadeia que fecha hoje é `signup_started` → `phone.submitted` →
  `account_created`: ~21–23% de quem começa cria conta, e a perda real está no
  passo do telefone (~3.000 pessoas/dia).
- `/api/geral_completo`, `/api/geral_diario` — KPIs financeiros (GGR/NGR,
  depósitos, saques).
- `/api/apostas`, `/api/apostas_diario`, `/api/loteria_diario` — volume de
  apostas e recorte de loteria.
- `/api/filtros` — valores disponíveis para os seletores; `/api/prewarm`
  aquece o cache.

**Tráfego/frente não é rota, é filtro.** A taxonomia de frente (`App`,
`Tráfego`, `Mídias`, `Resultado Fácil`, `Afiliados`, `Orgânico` — classificação
por prefixo de `btag`, ver `FRENTE_CASE` em `geral_app.py`) entra como
parâmetro nas rotas acima: `?frente=`, `?btag=`, `?afiliado=`. Versões
anteriores desta skill listavam `/api/trafego_pago`, `/api/funil_trafego` e
`/api/trafego_diario` — **essas rotas não existem no app** (verificado em
02/09/2026); a lista completa e real sai de
`grep -nE "@app\.route\(['\"]" geral_app.py` (atenção: o código mistura aspas
simples e duplas, então grep só com `"` perde rotas).

## Subir o app

```bash
cd tools/dashboard-tradicional   # a partir da raiz do pm-loadout
source .venv/bin/activate   # criar com `python3 -m venv .venv && pip install -r requirements.txt` na primeira vez
python3 geral_app.py
```

Acesse em `http://localhost:5051`.

## Autenticação (sem senha compartilhada)

O app gera um **token IAM da AWS** automaticamente a cada ~10min (perfil
`trad-prd-ithalo_mendes`, usuário `ithalo_mendes`) — mesma identidade usada
no acesso pessoal ao `trad_prd` via `psql`/alias `trad-prd`. Não precisa
pedir credencial nova a ninguém. Pré-requisitos: AWS CLI configurado com
esse profile e `~/global-bundle.pem` baixado (ver manual de acesso pessoal
ao banco, ou `tools/dashboard-tradicional/README.md`).

## Verificar se já está rodando / derrubar

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5051/   # 200 = já está de pé
lsof -ti :5051 | xargs kill                                        # derruba, se precisar
```

## Governança e como mexer no código

Desde 02/09/2026 o app é mantido pelo PM + Orquestrador (não só pelo Jonatas):
pode editar direto. O `tools/` **não está no git** — faça backup do arquivo
antes de alterar.

Ao mexer nas rotas da jornada, respeite os invariantes que a correção de
02/09 estabeleceu (o bloco de comentário no topo de
`# ── FUNIL DE AQUISIÇÃO` em `geral_app.py` é a fonte completa):

- Filtre por `player_event_type_id`, **nunca** por `detail` — só o primeiro é
  indexado; a mesma agregação de 3 dias leva 14,7s por `detail` e 2,3s por
  type_id, numa tabela de 362M linhas / 207 GB.
- Recorte por data de **ocorrência** (`OCC_DATE_SQL`), com o prefiltro por
  `created` esticando **para frente** (o evento chega depois de ocorrer).
- Mantenha o filtro de coorte (`JORNADA_COORTE_SQL`), senão a revalidação de
  login volta a inflar o funil.
- As quatro rotas compartilham `_jornada_base_sql`. Não recrie o CTE numa
  rota só — foi assim que elas divergiram entre si na primeira vez.
- **Suba a versão da chave de cache** (`jornada3|` → `jornada4|`...) sempre que
  mudar a semântica: dias passados **nunca expiram** no cache, então sem isso a
  correção passa despercebida no histórico.
- `cache_purge()` existe porque chave com bucket de tempo no nome nunca colide
  com `INSERT OR REPLACE`. O `cache.db` já chegou a 1,4 GB por causa disso.

## Quando usar isto vs. `query-trad`/`agente-dados`

- **Pergunta padrão já coberta pelas rotas acima** (funil, retenção, GGR/NGR
  diário, tráfego pago por frente) → suba/abra o dashboard, é mais rápido e
  já está validado pelo time.
- **Pergunta nova, cruzamento ad-hoc, hipótese específica, ou algo fora do
  escopo das rotas** (ex.: KYC por fila/rejeição, PIX com falha, sessões
  antes do FTD) → use `query-trad`/`agente-dados` para SQL exploratório.
- Achados de uma investigação ad-hoc que viram métrica recorrente devem virar
  uma rota nova neste app, não ficar reimplementados em SQL solto a cada
  sessão. Avise o Jonatas quando mexer — o dashboard nasceu dele e ele
  continua usando.
