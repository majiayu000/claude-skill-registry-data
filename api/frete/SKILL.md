---
name: tray-frete
description: >
  API de Frete da Tray. Utilize quando o desenvolvedor precisar calcular
  valores de frete e consultar métodos de envio disponíveis. Inclui cálculo de frete
  por CEP com peso e dimensões, listagem de formas de envio configuradas na loja,
  e integração com gateways de frete como Frete-X API para cotação automática.
---

# API de Frete — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-integracao-de-frete

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/shippings/cotation/` | Calcular frete para um ou mais produtos por CEP |
| GET | `/shippings/` | Listar formas de envio disponíveis na loja |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Parâmetros do Cálculo de Frete (`/shippings/cotation/`)

| Parâmetro | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `zipcode` | string | Sim | CEP de destino (apenas números, ex: "04001001") |
| `products[n][product_id]` | number | Sim | ID do produto (índice n começa em 0) |
| `products[n][price]` | decimal | Sim | Preço do produto |
| `products[n][quantity]` | number | Sim | Quantidade do produto |

> A rota aceita múltiplos produtos na mesma requisição usando índices `products[0]`, `products[1]`, etc.

## Exemplo de Requisição — Cálculo de Frete

```
GET /shippings/cotation/?access_token={token}&zipcode=04001001&products[0][product_id]=123&products[0][price]=58.90&products[0][quantity]=2
```

## Exemplo de Resposta — Cálculo de Frete

```json
{
  "Shipping": [
    {
      "id": "1",
      "name": "PAC",
      "price": "25.90",
      "delivery_time": "8",
      "delivery_time_text": "8 dias úteis"
    },
    {
      "id": "2",
      "name": "SEDEX",
      "price": "45.50",
      "delivery_time": "3",
      "delivery_time_text": "3 dias úteis"
    }
  ]
}
```

## Campos da Resposta de Frete

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `id` | number | ID do método de envio |
| `name` | string | Nome do método (ex: "PAC", "SEDEX", "Transportadora") |
| `price` | decimal | Valor do frete em reais |
| `delivery_time` | number | Prazo de entrega em dias úteis |
| `delivery_time_text` | string | Texto formatado do prazo de entrega |

## Exemplo de Resposta — Listar Métodos de Envio

```json
{
  "ShippingMethods": [
    {
      "ShippingMethod": {
        "id": "1",
        "name": "PAC",
        "active": "1"
      }
    },
    {
      "ShippingMethod": {
        "id": "2",
        "name": "SEDEX",
        "active": "1"
      }
    },
    {
      "ShippingMethod": {
        "id": "3",
        "name": "Retirada na Loja",
        "active": "1"
      }
    }
  ]
}
```

## Integração com Gateway de Frete (Frete-X API)

A Tray suporta integração com gateways de frete como o Frete-X API para cotação automática com múltiplas transportadoras.

### Funcionamento

1. A loja configura o gateway de frete no painel administrativo
2. Ao calcular o frete via API, a Tray consulta automaticamente o gateway configurado
3. O gateway retorna as opções de transportadoras com preços e prazos
4. A resposta é consolidada no formato padrão da API de Frete

### Configuração

A configuração do gateway de frete é feita no painel administrativo da Tray ou via API de Configuração de Frete (consulte o skill `tray-configuracao-frete`).

## Boas Práticas

1. **CEP apenas números** — envie o CEP sem pontos ou traços (ex: "01304001")
2. **Peso em gramas** — informe o peso sempre em gramas; 1 kg = 1000 g
3. **Dimensões mínimas** — os Correios possuem dimensões mínimas (16x11x2 cm); considere isso na requisição
4. **Cache de resultados** — o cálculo de frete pode ser lento por depender de APIs externas; considere cachear resultados por CEP + peso + dimensões
5. **Tratamento de erros** — nem sempre todos os métodos retornam resultado; trate o cenário de frete indisponível para determinada região
6. **Frete grátis** — produtos com `free_shipping: 1` podem retornar frete zerado dependendo da configuração da loja
7. **Recursos relacionados** — consulte o skill `tray-configuracao-frete` (`/shippings/method/gateway`, `/shippings/method/zipcode_table`) para gerenciar métodos de envio e tabelas de CEP

## Como Usar no Claude Code

### Exemplos de Prompt

- "calcula o frete para o CEP 01310100 para 2 unidades do produto 123"
- "lista os métodos de envio disponíveis na loja"
- "implementa o cálculo de frete com cache por CEP para evitar chamadas repetidas"
- "calcula o frete para um carrinho com 3 produtos diferentes"

### O que o Claude faz

1. Gera o código de requisição para `GET /shippings/cotation/` com os parâmetros indexados
2. Monta os índices `products[0]`, `products[1]`... para múltiplos produtos
3. Implementa cache de resultados por CEP + produtos quando solicitado
4. Trata o cenário de frete indisponível para determinada região

### O que você recebe

- Código de cálculo de frete com CEP e produtos indexados corretamente
- Tratamento da resposta com nome, preço e prazo de cada método
- Implementação de cache para otimizar chamadas repetidas
- Código de listagem de métodos via `GET /shippings/`

### Pré-requisitos

- `access_token` configurado
- `product_id` e `price` dos produtos disponíveis
- CEP de destino
