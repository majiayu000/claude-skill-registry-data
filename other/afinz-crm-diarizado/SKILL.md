---
name: afinz-crm-diarizado
description: Generate or update the AFINZ CRM acquisition daily Excel report from
  Supabase `activities` and `b2c_daily_metrics`, including Copa 2026 diarized blocks,
  B2C/Plurix/Dia/Bem Barato funnel mapping, cart abandonment, realized B2C columns,
  and an Auditoria sheet with mapped-block and journey/taxonomy diagnostics. Use when
  the user asks for Excel diarizado, aquisição CRM, Copa 2026, AFINZ CRM Supabase
  analysis, campaign journey mapping, or updates after new Supabase dispatch/B2C result
  data.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Relatórios
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# AFINZ CRM Diarizado

Use this skill to generate the AFINZ CRM acquisition workbook from Supabase and validate that campaign rows land in the correct business blocks.

## Quick Start

Run the bundled generator from the repo root:

```powershell
& "C:\Users\Pablo Prado\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .claude\skills\afinz-crm-diarizado\scripts\generate_aquisicao_crm_excel.py --output outputs\aquisicao_crm_copa2026_atualizado.xlsx --write-raw-json outputs\aquisicao_crm_copa2026_raw.json
```

Use a timestamped output when the workbook may be open in Excel or Google Drive sync may lock it:

```powershell
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
& "C:\Users\Pablo Prado\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .claude\skills\afinz-crm-diarizado\scripts\generate_aquisicao_crm_excel.py --output "outputs\aquisicao_crm_copa2026_$ts.xlsx" --write-raw-json "outputs\aquisicao_crm_copa2026_raw_$ts.json"
```

Default period is `2026-04-13` through `2026-05-21`. Override with `--start YYYY-MM-DD --end YYYY-MM-DD`.

## Workflow

1. Fetch raw rows from Supabase `activities` using the script defaults or env overrides `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
2. Generate the workbook with two sheets:
   - `Aquisição CRM`: diarized report with sections `B2C`, `PLURIX`, `DIA`, `BEM BARATO`, plus realized B2C daily columns from `b2c_daily_metrics`.
   - `Auditoria`: source counts, mapped-block summary, unmapped detail, and journey/taxonomy map.
3. Validate with openpyxl after generation:
   - Workbook opens.
   - Expected sheets exist.
   - `Aquisição CRM` has freeze panes `C3`.
   - Dates stay inside the requested period.
   - Formula strings contain no `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, or `#N/A`.
   - `Auditoria` has `Fora do escopo: Seguros/Rentabilizacao` as the only expected unmapped reason for the current Copa report.
4. Report the output path and the key audit counts to the user.

## Realized B2C Columns

Fill `DADOS REALIZADOS B2C` as total B2C plus Serasa/API split, keyed by `data`:
- `Propostas` = total proposals, i.e. B2C APP + Serasa/API.
- `Cartões Emitidos` = total emissions/cards, i.e. B2C APP + Serasa/API.
- `Propostas Serasa` = API/Serasa proposals.
- `Cartões Serasa` = API/Serasa emissions.

Preferred future source is Supabase `b2c_daily_metrics` with explicit `tipo = total` rows and rows containing `serasa`. Until the table has complete Serasa proposals, use `--b2c-realized-json` with `propostas_total`, `emissoes_total`, `propostas_serasa`, and `emissoes_serasa`. Legacy override files with `propostas_app`/`emissoes_app` are accepted only as an input convenience and are summed with Serasa before writing the workbook.

Write these values only on the first B2C row for each date, so days with multiple CRM campaign/channel rows do not duplicate realized totals.

## Mapping Rules

For exact business mapping, read `references/mapping.md` before changing any block logic.

Core B2C rules:
- `Base_Proprietaria + Aquisicao` -> `TOPO DE FUNIL B2C`.
- `Negados + Meio_de_Funil` -> `REPESCAGEM B2C`.
- `Aprovados_nao_convertidos + Meio_de_Funil` -> `UPGRADE B2C`.
- `Leads_Parceiros` or `Serasa + Base_Proprietaria + Meio_de_Funil` -> `LEADS PARCEIROS B2C`.
- `Abandonados` -> `CARRINHO ABANDONADO B2C`.

Core Plurix rules:
- `CRM + Aquisicao` -> `TOPO DE FUNIL PLURIX`.
- `Negados + Meio_de_Funil` -> `REPESCAGEM PLURIX`.
- `Aprovados_nao_convertidos + Meio_de_Funil` -> `UPGRADE PLURIX`.
- `Recencia de Compra` -> `RECENCIA PLURIX`.
- `Abandonados` -> `CARRINHO ABANDONADO PLURIX`.

## Auditoria

The auditor is not only an exception log. It must help explain where data went.

Keep these sections:
- Global source/mapped/unmapped counts.
- `Resumo dos blocos mapeados`.
- Unmapped detail by `Motivo`, `BU`, `Parceiro`, `Segmento`, `Etapa`, `Canal`.
- `Mapa de jornadas e taxonomias por destino`.

Read `references/auditoria.md` before changing audit columns or validation expectations.

## Safe Changes

- Use the script in `scripts/` as the source of truth for generation.
- Patch the skill copy and, if needed, sync the project-level script intentionally.
- Never silently put unknown acquisition rows into a report block; map deliberately or leave them visible in `Auditoria`.
- Treat `Seguros/Rentabilizacao` as outside this acquisition report.

## Configuração após instalação

Defina SUPABASE_URL e SUPABASE_ANON_KEY no ambiente (ou use as opções de linha de comando existentes). O pacote público não contém valores de chave. Acesso autenticado pode ser exigido pelas políticas atuais do banco; não contorne RLS.
