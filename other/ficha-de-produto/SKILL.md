---
name: ficha-de-produto
description: Modelo de ficha de produto com campos obrigatórios e regra de dados desconhecidos.
---

# Skill: ficha-de-produto

Uma ficha por produto (e por variação, quando os dados diferirem).

## Campos obrigatórios
- **SKU interno** e **identificador global** (EAN/GTIN, se houver)
- **Nome padronizado**: Marca + Tipo + Modelo + Atributo-chave
- **Categoria** e **subcategoria**
- **Marca**, **fabricante/fornecedor**
- **Variações** (tamanho, cor, voltagem...) com SKU por variação
- **Dimensões e peso** do produto e da embalagem (unidade explícita)
- **Material/composição**
- **O que vem na caixa**
- **Garantia** (prazo e quem dá)
- **Certificações ou registros exigidos** (se aplicável)
- **Custo**, **preço atual**, **estoque** (se fornecidos)
- **Imagens necessárias** (lista e status)
- **Observações**

## Regra de ouro
Dado ausente = `A CONFIRMAR`. Nunca estime medida, composição, garantia ou certificação.
