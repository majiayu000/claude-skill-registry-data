---
name: tray-imagens-produtos
description: >
  API de Imagens de Produtos e Variações da Tray. Utilize quando o
  desenvolvedor precisar fazer upload, atualizar ou remover imagens de produtos
  e variações. Inclui formatos aceitos, método de envio e posicionamento de imagens.
---

# API de Imagens de Produtos e Variações — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-imagens-de-produtos-e-variacoes

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| POST | `/products/:id/images` | Cadastro e atualização de imagem do produto |
| POST | `/variants/:id/images` | Cadastro e atualização de imagem da variação |
| POST | `/images/remove` | Remoção de imagens |

**Autenticação:** `?access_token={token}`

## Envio de Imagens

As imagens podem ser enviadas de duas formas:

### Via URL

```json
{
  "ProductImage": {
    "image_url": "https://exemplo.com/imagem.jpg"
  }
}
```

### Via Base64

```json
{
  "ProductImage": {
    "image_base64": "data:image/jpeg;base64,/9j/4AAQSk..."
  }
}
```

## Campos

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `image_url` | string | URL pública da imagem |
| `image_base64` | string | Imagem codificada em Base64 |
| `position` | number | Posição/ordem da imagem (1 = principal) |

## Thumbnails Gerados

Após o upload, a Tray gera automaticamente thumbnails em 3 tamanhos:

| Tamanho | Uso |
|:--|:--|
| 30px | Miniatura/ícone |
| 90px | Lista de produtos |
| 180px | Exibição média |

Cada thumbnail é disponibilizado em HTTP e HTTPS.

## Remoção de Imagens

Para remover imagens, envie um POST para `/images/remove` com o ID da imagem.

## Boas Práticas

1. **Faça upload sequencialmente** — evite paralelismo excessivo para não exceder o rate limit
2. **Use URLs quando possível** — evita o overhead de Base64 (33% maior)
3. **Defina a posição** — a imagem de posição 1 é a imagem principal do produto
4. **Formatos aceitos** — JPG, PNG, GIF

## Como Usar no Claude Code

### Exemplos de Prompt

- "faz upload das imagens para o produto 123 a partir de URLs"
- "define a imagem principal do produto e mais 3 imagens secundárias"
- "como envio imagens de variações separadas do produto?"
- "remove a imagem ID 55 do produto"

### O que o Claude faz

1. Gera o código de upload via URL ou Base64 conforme o caso
2. Define o campo `position` (1 = principal, 2, 3... para as demais)
3. Diferencia o endpoint de produto (`/products/:id/images`) do de variação (`/variants/:id/images`)
4. Explica os thumbnails gerados automaticamente (30px, 90px, 180px)

### O que você recebe

- Código de upload com wrapper `{"ProductImage": {...}}` correto
- Lógica de posicionamento para múltiplas imagens
- Exemplos separados para produto e variação
- Código de remoção via `/images/remove`

### Pré-requisitos

- Produto ou variação já cadastrado com ID disponível
- URLs das imagens públicas e acessíveis (para envio via URL)
- `access_token` configurado
