---
name: docx-cmr-generator
description: Gera documentos Word (.docx) a partir de Markdown no padrão CMR Advogados. Use quando precisar converter peças jurídicas de Markdown para DOCX com formatação correta (fontes, margens, espaçamentos).
---

# CMR DOCX Generator

Converte documentos Markdown para Word (.docx) seguindo o padrão de formatação CMR Advogados.

## Localização

A ferramenta está em `skills/docx-cmr-generator/`:

```
skills/docx-cmr-generator/
├── doc_builder.py       # Conversor MD → DOCX
├── style_extractor.py   # Extrator de DNA de templates
├── cmr_styles.json      # Configuração de estilos
├── requirements.txt     # Dependências
└── .venv/               # Ambiente virtual
```

## Como Usar

### Ativação do ambiente

```bash
cd skills/docx-cmr-generator
source .venv/bin/activate
```

### Converter Markdown para DOCX

```bash
python doc_builder.py <entrada.md> [saida.docx]
```

**Exemplo:**
```bash
python doc_builder.py ../CONTESTACAO.md ../CONTESTACAO.docx
```

### Extrair DNA de template existente

```bash
python style_extractor.py <template.docx> [estilos.json]
```

### Gerar consenso de múltiplos documentos

```bash
python style_extractor.py --consensus ./pasta/ [consenso.json]
```

## Mapeamento Markdown → Estilo

| Markdown | Estilo |
|----------|--------|
| `# Texto` | Endereçamento |
| `## CONTESTAÇÃO` | Title_Peca (centralizado) |
| `## I. Título` | Chapter_Heading |
| `### A. Subtítulo` | Subcapitulo |
| `1. Parágrafo` | Paragraph_Numbered (recuo 4cm) |
| `> Citação` | Citation (10pt, itálico, recuo 4cm) |
| `a) Item` | Item_Lista |
| `**Nome** + OAB` | Assinatura |
| `---` | Page break |

## Especificações de Formatação CMR

### Fontes
| Elemento | Fonte | Tamanho |
|----------|-------|---------|
| Cabeçalho | Verdana | 26pt |
| Subtítulo | Verdana | 12pt |
| Corpo | Century Gothic | 12pt |
| Citações | Century Gothic | 10pt italic |
| Rodapé | Century Gothic | 6pt |

### Página (A4)
- **Margens**: Superior/Inferior 2.5cm, Esquerda 3cm, Direita 2cm
- **Recuo 1ª linha**: 4cm (parágrafos numerados)
- **Espaçamento**: 1.5 linhas (corpo), 1.0 linha (citações)

### Header/Footer
- **Header**: "C. M. RODRIGUES / Advogados" (direita, Verdana)
- **Footer**: Endereço do escritório (direita, Century Gothic 6pt)

## Configuração (cmr_styles.json)

O arquivo `cmr_styles.json` define todo o DNA de formatação:

```json
{
  "page_setup": { "margins_twips": {...} },
  "header": { "line1": {...}, "line2": {...} },
  "footer": { "lines": [...] },
  "styles_map": {
    "Normal": { "font_name": "Century Gothic", ... },
    "Citation": { "font_size_pt": 10, "italics": true, ... }
  }
}
```

## Conversão de Unidades

| Medida | Twips |
|--------|-------|
| 1 cm | 567 |
| 4 cm (recuo) | 2268 |
| 3 cm (margem esq) | 1701 |
| 2.5 cm (margem sup/inf) | 1417 |
| 2 cm (margem dir) | 1133 |
