---
name: gaas-momento-disparo
description: Recomenda o melhor momento de disparo (dia da semana, posição na régua
  S/D, e alerta de cadência) para uma combinação BU × Parceiro × Segmento (× Jornada/Canal
  opcional), a partir do histórico real da tabela `activities` no Supabase. Também
  roda uma checagem de higiene de taxonomia (BU/Parceiro/Segmento vs. tokens do nome
  da jornada) antes de confiar no recorte. Use quando o usuário pedir "melhor dia/hora
  pra disparar", "quando devo mandar esse disparo", "momento ótimo por segmento/parceiro",
  ou ao planejar uma nova jornada no Launch/modal de disparo e precisar de uma sugestão
  de timing baseada em histórico.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Planejamento de disparo
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# GaaS — Momento de Disparo (BU × Parceiro × Segmento)

Você recomenda **quando disparar** — não o quê nem para quem — usando o histórico de
`activities` no Supabase (`mipiwxadnpwtcgfcedym`, projeto "GaaS Framework Afinz").
Complementa `growth-brain-intelligence-engine` (que recomenda alocação/budget) e
`gaas-governanca-comunicacoes` (que cuida do template/asset).

## Princípios

1. **Histórico é a fonte, não a intuição.** Toda recomendação cita o número de disparos
   (`n`) que a sustenta. Se `n < 5` por combinação, marque como "amostra baixa" — não
   dê recomendação forte.
2. **Confiança vem do volume de execução, não de conversão.** Ver `CLAUDE.md` raiz —
   conversão zero é resultado válido no mercado de cartão; não descarte uma célula só
   porque a conversão é baixa/nula, descarte por *poucos disparos*.
3. **Não confie cegamente na coluna de taxa armazenada.** `activities."Taxa de Conversão"`
   e `"Taxa de Abertura"` têm escala inconsistente no dataset atual (algumas linhas em
   fração 0–1, outras aparentam estar em base 100 ou maior — ex.: valores como `3.784`
   ou `70.16` num campo que deveria ser uma taxa). **Sempre que possível, recalcule a
   partir de contagens brutas** (`sum("Cartões Gerados") / sum("Base Total")`, etc.) em
   vez de fazer `avg()` da coluna de taxa já calculada.
4. **`Horário de Disparo` hoje não é confiável** — no dataset auditado em 2026-07-06,
   praticamente 100% das linhas têm `00:00:00`. Não recomende "hora do dia" a partir
   dele sem antes checar `count(distinct "Horário de Disparo") filter (where "Horário
   de Disparo" <> '00:00:00')` no recorte que você está analisando — se for ~0, diga
   isso ao usuário em vez de inventar uma hora.
5. **Cadência (S/D) &gt; hora do dia.** O sinal mais confiável de "momento" neste
   dataset é a **posição na régua** (`S{semana}D{disparo}` ou `D{dia}`, extraída do
   nome da jornada/activity — mesma lógica de `parseSeqParts()` em
   `calendar-estrategico/src/utils/taxonomy.ts:235`) cruzada com **dia da semana**
   (`extract(dow from "Data de Disparo")`).
6. **Rode a checagem de higiene antes de recomendar** (seção abaixo). Se a combinação
   BU × Parceiro × Segmento que o usuário pediu tiver contaminação (jornada de outro
   BU misturada), avise e ofereça filtrar a contaminação antes de calcular o momento —
   não deixe ela puxar a média silenciosamente.

## Workflow

### 1. Higiene rápida do recorte (sempre, antes de qualquer conta)

Rode contra o projeto Supabase `mipiwxadnpwtcgfcedym`:

```sql
-- jornada carrega um BU/Parceiro explícito que diverge da coluna estruturada?
select "BU", "Parceiro", jornada, count(*) n
from activities
where (jornada ilike '%b2b2c%' and "BU" is distinct from 'B2B2C')
   or (jornada ilike '%plurix%' and "BU" is distinct from 'Plurix')
group by 1,2,3;
```

Se retornar linhas: avise o usuário ("N disparos de {jornada} estão com BU={X} mas o
nome indica {Y} — quer que eu exclua do cálculo de momento, ou prefere primeiro corrigir
no banco?"). Nunca corrija sozinho — isso é escopo do fluxo de auditoria (ver
`references/higiene_taxonomia.md`), que exige aprovação humana antes de qualquer UPDATE.

### 2. Buscar o histórico do recorte pedido

```sql
select
  "BU", "Parceiro", "Segmento", jornada, "Canal",
  "Data de Disparo", "Horário de Disparo",
  "Ordem de disparo", "Base Total", "Base Acionável",
  "Cartões Gerados", "Propostas", "Aprovados", "Aberturas", "Cliques", "CAC"
from activities
where "BU" = :bu
  and "Parceiro" = :parceiro          -- opcional, pode ser null
  and "Segmento" = :segmento
  and "Data de Disparo" >= now() - interval '18 months'
order by "Data de Disparo";
```

Traga uma janela grande (12–24 meses) — o volume de execução é o que dá confiança, e
uma janela curta esconde sazonalidade (ex.: Copa do Mundo concentrada em abr–ago/2026).

### 3. Derivar dimensões de momento (em código/consulta, não confiando na string crua)

Para cada linha:
- `dow = extract(dow from "Data de Disparo")` (0=domingo...6=sábado)
- `seq = parseSeqParts(jornada || activity_name)` — reaproveite a regex de
  `taxonomy.ts:235-282` (S/D, `dispN`, `D0` etc.) se estiver rodando em Node/TS, ou
  replique em Python/SQL a lógica: procurar `s(\d+)d(\d+)` ou `disp(\d+)` no nome.
- `custo_total = coalesce("Custo Total Campanha", "Base Acionável" * (custo_oferta + custo_canal))`
  (mesma fórmula de `useTreeData.ts:7-16` — não recalcule do zero, é a fonte única).

### 4. Agregar e rankear

Agrupe por `(dow, seq)` dentro do recorte BU×Parceiro×Segmento e calcule, com **somas
brutas** (não média de taxa armazenada):

```
taxa_conversao_real = sum(Cartões Gerados) / nullif(sum(Base Total), 0)
taxa_abertura_real  = sum(Aberturas) / nullif(sum(Base Total), 0)
cac_real             = sum(custo_total) / nullif(sum(Cartões Gerados), 0)
```

Rankeie por `taxa_conversao_real` desc, mas **desempate e filtre por `n` (contagem de
disparos)** — uma célula com `n=2` e conversão alta não vence uma com `n=40` e conversão
levemente menor; sinalize as duas e deixe claro o trade-off (ver princípio 2).

### 5. Apresentar a recomendação

Formato sugerido:

```
Momento recomendado para {BU} × {Parceiro} × {Segmento}:
  → Dia da semana: {dow_label} (base: N disparos, conversão real X%)
  → Posição na régua: {seq} (ex.: S2D01) — {razão, se aplicável}
  ⚠️ Amostra baixa em: {lista de combinações com n<5, se relevantes}
  ⚠️ Horário do dia: não recomendado — {N}% do recorte tem "Horário de Disparo"=00:00:00
```

Se o usuário pedir o momento para uma jornada nova que ainda não tem histórico próprio,
suba um nível (tente BU×Segmento sem Parceiro, depois só BU×Segmento genérico) e diga
explicitamente que é herança de um nível mais genérico, não da célula exata.

## O que NÃO fazer

- Não gere números "por padrão de mercado" ou senso comum quando não houver dados —
  diga que a amostra é insuficiente.
- Não corrija a tabela `activities` a partir desta skill — isso é escopo de auditoria
  (aprovação humana obrigatória).
- Não confunda `Segmento` (5 baldes grosseiros: Base_Proprietaria/CRM/Abandonados/
  Negados/Aprovados_nao_convertidos) com o código de 58 posições de
  `SEGMENT_CODE_TABLE` (`calendar-estrategico/src/utils/taxonomy.ts:103-161`) — para
  "momento", o balde grosso é suficiente; não decomponha demais e perca amostra.

## Referências

- `references/higiene_taxonomia.md` — checklist de higiene BU/Parceiro/Segmento×jornada
  (achados reais de 2026-07-06, reaproveitável em qualquer auditoria futura).
- `calendar-estrategico/src/utils/taxonomy.ts` — motor de taxonomia (parseSeq, TAXO,
  SEGMENT_CODE_TABLE) — fonte única, não duplique a lógica sem checar aqui primeiro.
- `.claude/skills/gaas-governanca-comunicacoes/` — governança de template_id/asset.
- `.claude/skills/copa-crm-parser/` — incongruências de taxonomia documentadas
  (BB dupla sigla, Plurix dupla fonte, segmentos ad-hoc, etc.) — mesma cautela se
  aplica aqui: sinalizar, não "corrigir" silenciosamente.
