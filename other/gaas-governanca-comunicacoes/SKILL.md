---
name: gaas-governanca-comunicacoes
description: Lê a planilha de governança de links/templates do CRM (GOVERNANÇA_LINKS_E_TEMPLATES,
  CSV ';' latin-1), cruza os ID TEMPLATE (af_sub3) com os ACTIVITY NAME e com o Supabase
  (activities + communication_templates), valida a taxonomia (detecta activity_name
  copiado entre apps e divergência de marca) e — após aprovação — pré-cria os templates
  como 'draft' (sem asset) e vincula activities.template_id. Use quando o usuário
  pedir para importar/interpretar a planilha de governança de templates, cruzar template_id
  com activity_name, ou preparar a fila de cadastro de comunicações para só subir
  o asset.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Comunicações
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# GaaS — Governança de Comunicações (template_id × activity_name)

Você prepara o terreno da aba **Comunicações**: interpreta a planilha de governança,
cruza com o histórico (`activities`) e o catálogo (`communication_templates`), e deixa
cada peça pronta para o operador **só adicionar o asset** (HTML/imagem).

## Princípios (não-negociáveis)

1. **Dry-run primeiro, gravação só com aprovação.** O `analyze` NÃO grava nada.
   Mostre o relatório ao usuário e **espere o OK** antes de rodar `apply`.
2. **Linhas suspeitas NÃO são importadas por padrão.** A inteligência de taxonomia
   sinaliza; quem decide é o usuário (ver `references/taxonomia_marcas.md`).
3. **Preservar a caixa exata de template_id e af_sub3.** Não normalizar silenciosamente. Antes de aplicar, conferir o contrato atual do banco; se uma constraint divergir, registrar o conflito e não alterar a identidade para contorná-la.
4. **Só metadados, sem link agora.** Não cria `attribution_links` nem gera links.
5. **Pré-cria templates como `draft` sem asset.** O asset é adicionado depois, no app.

## Workflow

1. **Analisar (dry-run):**
   ```powershell
   & "C:\Users\Pablo Prado\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .claude\skills\gaas-governanca-comunicacoes\scripts\governance_templates.py analyze "CAMINHO\DO\GOVERNANCA.csv"
   ```
   Gera `outputs/governance_report_<ts>.json` e imprime o resumo por status.

2. **Ler o relatório e apresentar ao usuário** — contagem por status e, em especial,
   a lista de **suspeitos** com o motivo de cada um. Status possíveis:
   - `ok` — activity_name existe e taxonomia consistente → será vinculado.
   - `planejado_sem_activity` — template sem activity_name ainda → cria draft, sem vínculo.
   - `activity_nao_encontrada` — activity_name não existe em `activities` → cria draft, sem vínculo.
   - `suspeito` — activity_name copiado entre apps OU marca divergente → **não importa** sem decisão.

3. **Esperar a decisão do usuário.** Não rode `apply` antes de o usuário aprovar.

4. **Aplicar (grava no banco):**
   ```powershell
   & "C:\...\python.exe" .claude\skills\gaas-governanca-comunicacoes\scripts\governance_templates.py apply "outputs\governance_report_<ts>.json"
   ```
   - Faz upsert dos templates `draft` (com metadados: app, campanha, semana/af_sub2,
     segmento/af_sub1, nome, códigos, activity_names planejados).
   - Vincula `activities.template_id` apenas nas linhas `ok`.
   - **Não** importa `suspeito` (use `--include-suspeito` só se o usuário mandar).

5. **Reportar** quantos templates draft entraram e quantas activities foram vinculadas.

## O que NÃO fazer

- Não rode `apply` sem mostrar o relatório e obter aprovação.
- Não tente "adivinhar/corrigir" o activity_name certo — apenas sinalize (decisão do operador).
- Não crie attribution_links nem gere links AppsFlyer (fora de escopo agora).
- Não sobrescreva templates já existentes (o apply pula `template_ja_existe`).

## Conexão Supabase

Os scripts usam a REST API com a publishable key fornecida por SUPABASE_ANON_KEY (projeto
`mipiwxadnpwtcgfcedym` — "GaaS Framework Afinz"). Para sobrescrever, use
`--supabase-url` / `--supabase-key` ou as env `SUPABASE_URL` / `SUPABASE_ANON_KEY`.

## Governança multifonte e links AppsFlyer

Para reconciliar SFMC, links, catálogo e cobertura de assets, ler [governanca-multifonte.md](references/governanca-multifonte.md). O modo de planilha acima não cria links; o modo multifonte pode preparar propostas de links, sempre sem aplicar vínculos fracos. Preservar a caixa exata de template_id/af_sub3 em ambos. O antigo nome gaas-communication-governance é um alias desta capacidade.

## Configuração após instalação

Defina SUPABASE_URL e SUPABASE_ANON_KEY no ambiente (ou use as opções de linha de comando existentes). O pacote público não contém valores de chave. Acesso autenticado pode ser exigido pelas políticas atuais do banco; não contorne RLS.
