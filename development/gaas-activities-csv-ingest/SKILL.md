---
name: gaas-activities-csv-ingest
description: Simular, revisar e importar CSV de Dinâmica BI para activities do GaaS
  Afinz usando o motor do Atualizador Inteligente, com diferenças por campo, atualização
  parcial e auditoria. Use para novos disparos ou métricas tardias; não para SFMC
  ou rentabilização.
metadata:
  version: 1.0.0
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Ingestão de dados
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Ingestão de activities por CSV

Use o mesmo motor do app, `src/utils/intelligentUpdateEngine.ts`, e os payloads financeiros de `src/services/intelligentUpdateService.ts`. Nunca implemente outro parser em Python ou adivinhe campos do CSV. A implementação executável e os testes ficam no repositório GaaS, não duplicados nesta skill.

## Preparar o ambiente

Localize um checkout que contenha `scripts/activities-csv.mjs`; confira a raiz Git, revisão e alterações locais. A pasta antiga `calendar-estrategico` pode estar numa branch arquivada. Leia AGENTS.md aplicável e `docs/reference/activities-csv-ingest.md` no checkout. Dependências: Node 24.11.1 e dependências do package-lock do projeto.

Até a integração ao main, a implementação validada está em `C:\Users\Pablo Prado\.codex\.chatgpt-projects\g-p-697787e7e13c81918cb4ed0d0c811d6b\activities-ingest`, branch `codex/activities-csv-skill-20261026`. Confira sua existência e estado antes de executar; não substitua pela pasta arquivada.

Confirme via conector Supabase o projeto **GaaS Framework Afinz**, `mipiwxadnpwtcgfcedym`. Inspecione schema, triggers, RLS e `bulk_update_activities_from_json` atuais. O schema de referência tem 54 colunas, mas o schema vivo prevalece. Preserve todas as colunas sem origem observada ou regra governada; cobertura completa não significa preencher tudo.

Leia os contratos atuais do vault: `08-Engenharia/Importador-Segmentacao-Aquisicao-2026-10.md`, `02-Entidades-Dados/activities.md`, `03-Dimensoes/Canais.md` e decisões específicas das jornadas do lote. Snapshots antigos não definem tarifas vigentes. Uma decisão humana para a jornada exata vence inferência por nome.

## Simular

Obtenha snapshot **somente leitura** de activities via Supabase MCP, paginado e ordenado por UUID. Salve o resultado JSON localmente sem imprimir a base inteira no chat. Confira contagem e estabilidade da leitura: quantidade, max(updated_at) e hashes devem permanecer estáveis; repita se houver mudanças durante a paginação. Não use credenciais secretas ou altere RLS para exportar.

Execute no checkout:

```powershell
node scripts/activities-csv.mjs --csv 'CAMINHO.csv' --snapshot 'activities-snapshot.json' --out 'outputs/activities-audit/current'
node scripts/activities-source-audit.mjs 'CAMINHO.csv' 'outputs/activities-audit/current/source-audit.json'
```

O primeiro comando gera `summary.json`, `simulation.json` e `plan.json`; o segundo lista rejeições por linha física e totais dos blocos. Preserve os arquivos originais. Informe o hash do CSV, intervalo, contagens e limitações. Não chame candidatos sem correspondência de novas execuções confirmadas.

Trate nulo como desconhecido, preserve zero explícito, não copie resultados entre jornadas nem escolha silenciosamente entre vários UUIDs. Métricas reduzidas, renomeações, dimensões sugeridas e inserções ficam em revisão. Mantenha atualizações tardias de histórico visíveis, mesmo quando o objetivo principal for importar datas recentes.

Confirmação de 26/10/2026: ANC / Aprovados_nao_convertidos usa Meio_de_Funil e
Subgrupos=N/A (sem subgrupo). Não oferecer Diario ou janelas de carrinho para ANC,
mesmo que apareçam em históricos contaminados. Em WhatsApp, `_resposta_optout_pontual`
é a resposta ao clique em “Não tenho interesse agora”; é reutilizada entre jornadas.
Não usar o histórico global da mesma activity para inferir seu público ou atribuir
causalidade a propostas/cartões. Consulte a nota canônica do vault
`04-Operacao/WhatsApp-Respostas-de-Opt-out.md`, incluindo as melhorias propostas.

## Aplicar um lote autorizado

A simulação é somente leitura. Para escrever, verifique a autorização vigente do usuário e o escopo exato. Não peça autorização novamente se o usuário já aprovou aquele plano e aquela seleção. Nesta primeira entrega do projeto, a carga depende da aprovação final do lote.

Prepare um JSON de seleção que contenha o `planId` exibido e as chaves exatas aprovadas:

```json
{"planId":"HASH_DO_PLANO","keys":["CHAVE_EXATA"],"reviewedKeys":["CHAVE_EXATA_REVISADA"]}
```

`reviewedKeys` registra revisão efetiva dos casos sinalizados; não preencha automaticamente com todos os candidatos. Candidatos bloqueados não podem ser aprovados pelo executor: resolva a causa e regenere o plano.

```powershell
node scripts/activities-csv.mjs --prepare-apply --plan 'plan.json' --selection 'selection.json' --sql 'approved-batch.sql'
```

Esse comando **prepara**, não executa. Leia o SQL e confira plano/seleção, projeto, triggers e compatibilidade do schema vivo. Execute o SQL aprovado usando `supabase_execute_sql` no projeto confirmado. Não remova guardas de concorrência, bloqueios ou assertivas para forçar uma carga. A transação usa o RPC financeiro existente, IDs determinísticos para inserções, comparação da linha anterior e auditoria before/after em gaas_update_runs/gaas_update_candidates. Erro reverte o lote inteiro; não siga com metade dele.

Gravações podem acionar vínculos automáticos de templates e auditorias do próprio banco. Preserve e reporte esses efeitos; os testes locais não certificam integrações desses triggers em produção.

## Verificar e recuperar

Salve o recibo retornado pelo SQL e obtenha novo snapshot. Confira os registros e os totais no Supabase; depois:

```powershell
node scripts/activities-csv.mjs --verify --plan 'plan.json' --snapshot 'after.json' --receipt 'receipt.json'
```

Reexecutar o mesmo SQL contra as linhas ainda iguais ao recibo deve não gerar alterações adicionais. Se uma linha aplicada mudou depois, o executor bloqueia a repetição; regenere a simulação. Reprocessar o CSV deve reconhecer os UUIDs persistidos.

Não execute rollback cego. Para desfazer, prepare uma correção inversa a partir do recibo, protegida por comparação com o after atual; examine efeitos sobre templates e auditorias relacionadas. Inserções que receberam atualizações posteriores exigem revisão própria.

## Validação de alterações no motor

```powershell
npm test -- src/utils/intelligentUpdateEngine.test.ts src/components/admin/IntelligentFrameworkUpdate.test.ts src/services/intelligentUpdateService.test.ts src/utils/intelligentImportRouting.test.ts
node --test scripts/test-activities-plan-sql.mjs
npm run typecheck:release
npm run build
```

Os testes SQL precisam de `schema.json` e `db-functions.json` exportados pela auditoria, contendo as funções públicas efetivamente inspecionadas. Nunca confunda o resultado local com aplicação em produção.

