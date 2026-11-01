---
name: afinz-pptx-campanha
description: 'Cria e edita decks .pptx de campanha comercial, parceria de marca (bandeira/parceiro,
  ex. Visa) ou ativação sazonal (Copa do Mundo, Black Friday, Dia das Mães etc.) usando
  o template de campanha da Afinz — que tem 12 layouts a mais que o template institucional
  padrão, incluindo uma capa temática (`capa copa`). Skill irmã de `afinz-pptx` (paleta/fonte/regras
  de marca) e `pptx` (mecânica de slides): use as três juntas. Acione sempre que o
  usuário pedir deck/apresentação/pptx de campanha, parceria com bandeira, ativação
  sazonal, ou mencionar um layout de campanha (capa temática, timeline, depoimento,
  portfólio de fotos, gráfico + texto).'
license: Distribuição pública autorizada pela Afinz em 2026-10-30; direitos de marca
  e de terceiros preservados.
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
  license: Distribuição pública autorizada pela Afinz em 2026-10-30; direitos de marca
    e de terceiros preservados.
---

# Afinz PPTX Campanha — template de campanha/parceria/sazonal

Complementa a skill `afinz-pptx` (que cuida de paleta, fonte e regras de marca) com o
**template de campanha** — extraído de um deck real (parceria Visa, tema Copa do
Mundo, ago/2026). Existe como skill separada porque o arquivo de template é grande
demais pra empacotar junto com o template institucional dentro do limite de uma skill
instalável (30MB por skill) — instale as duas.

## Quando usar esta skill em vez de só `afinz-pptx`

| Cenário | Template |
|---|---|
| Deck institucional, relatório, growth/KPIs | `afinz-pptx` sozinha (`afinz_template_institucional.pptx`) |
| Deck de campanha comercial, parceria de marca (bandeira/varejo) ou ativação sazonal | Esta skill (`afinz_exemplo_campanha_visa_copa.pptx`) + `afinz-pptx` pra cor/fonte |

## O template

`assets/afinz_exemplo_campanha_visa_copa.pptx` (16:9, 13.33"×7.5") é uma versão enxuta
do deck original: mantém o slide master completo e os **34 layouts** (incluindo os 22
que já existem em `afinz_template_institucional.pptx` — é o mesmo master estendido —
e mais 12, dos quais só `capa copa` é específico de marca; os outros 11 são layouts
default do PowerPoint, evite usá-los), mas só 6 dos 48 slides originais foram mantidos
como exemplo de preenchimento real (um por layout efetivamente usado no deck fonte,
escolhido pelo de menor peso de mídia). Os outros 42 slides e a mídia não referenciada
por eles foram removidos com o `clean.py` da skill `pptx` — isso é o que permitiu o
arquivo caber no limite de tamanho.

Leia **`references/campanha_layouts.md`** antes de montar qualquer slide — ele lista
os 34 layouts, quais têm exemplo real neste arquivo (e o nome do slide XML
correspondente: `slide2.xml`, `slide3.xml`, `slide7.xml`, `slide12.xml`, `slide19.xml`,
`slide38.xml`), e evita ter que rodar `thumbnail.py` (a conversão via LibreOffice desse
arquivo pode ser lenta em sandboxes com limite curto de comando — teste com um recorte
pequeno primeiro se precisar do render visual).

## Workflow

1. Confirme com o usuário: é campanha com parceiro (co-branding) ou ativação sazonal
   própria da Afinz? Isso muda a Regra do parceiro abaixo.
2. Leia `references/campanha_layouts.md` e escolha o layout certo pelo nome.
3. Duplique o slide de exemplo mais próximo (workflow da skill `pptx`):
   ```bash
   python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" \
     assets/afinz_exemplo_campanha_visa_copa.pptx
   python scripts/add_slide.py unpacked/ slide7.xml --after slide7.xml
   ```
4. Edite o conteúdo do slide duplicado (ver regras de "Template slots ≠ source items"
   na skill `pptx`).
5. Aplique a marca com o script de acento (ver Regra do parceiro/tema abaixo).
6. QA visual antes de entregar (converter em imagem e inspecionar).

## Regra do parceiro / bandeira — não adota a cor de marca do parceiro

Confirmado no deck real analisado: a Visa entra só como **logo**, nunca com cor
própria — a paleta do deck inteiro continua 100% Afinz (ciano `#00C6CC` PF / verde-neon
`#D3FF00` PJ). Trate isso como regra para qualquer parceiro/bandeira futuro: o
co-branding é o logotipo lado a lado com o da Afinz, não a paleta de cores dele.

## Regra do tema sazonal — um acento a mais, nunca substituição

O que muda numa campanha sazonal (Copa do Mundo, Black Friday etc.) é **um acento
temático a mais** por cima da paleta padrão — nunca a paleta inteira. No deck da Copa
do Mundo esse acento é um **dourado** (`#C8A94A`, `#FFC107`, tom escuro `#7A5C00`),
associado a troféu/prêmio, usado com moderação (números, ícones, blocos de destaque —
nunca fundo ou texto longo).

**Mais importante que a cor: a fotografia.** Renderizando slides reais desse deck, o
que mais carrega o tema é o banco de imagens (fotos de torcedores, cores da bandeira do
Brasil) — não o hex de shape. Ao adaptar este template pra outro tema sazonal, troque
primeiro as fotos por um banco alinhado ao tema; a paleta de marca (ciano/verde-neon)
segue dona do fundo, texto e blocos de destaque.

Ao rodar o script de marca, preserve o acento temático em vez de deixá-lo ser remapeado
pro azul/verde dominante:

```bash
python scripts/apply_afinz_brand.py deck.pptx --audience institucional --extra-accent C8A94A,FFC107
```

(Script idêntico ao de `afinz-pptx`, incluído aqui também para esta skill funcionar
sozinha. `--audience` também aceita `pf` / `pj`.)

## Dependências

- Skill `afinz-pptx` — paleta, fonte, logo e regras gerais de marca (ler
  `brand_spec.md` dela antes de montar qualquer slide).
- Skill `pptx` — mecânica de slides, thumbnail, `add_slide.py`, `clean.py`, QA visual.
- `python-pptx`, LibreOffice + Poppler (QA visual) — mesmas dependências da `pptx`.
