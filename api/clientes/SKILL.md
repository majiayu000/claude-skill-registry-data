---
name: tray-clientes
description: >
  API de Clientes da Tray. Utilize quando o desenvolvedor precisar
  gerenciar dados de clientes da loja: listagem, consulta, cadastro, atualização
  e exclusão. Inclui campos de pessoa física (CPF) e jurídica (CNPJ), validações
  brasileiras e gestão de newsletter.
---

# API de Clientes — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-clientes

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/customers` | Listagem de clientes com paginação e filtros |
| GET | `/customers/:id` | Consultar dados do cliente por ID |
| POST | `/customers` | Cadastrar novo cliente |
| PUT | `/customers/:id` | Atualizar dados do cliente |
| DELETE | `/customers/:id` | Excluir cliente |

**Autenticação:** `?access_token={token}`

## Campos do Cliente

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `name` | string | Nome completo |
| `email` | string | E-mail (obrigatório, único) |
| `cpf` | string | CPF (pessoa física) |
| `cnpj` | string | CNPJ (pessoa jurídica) |
| `rg` | string | RG |
| `phone` | string | Telefone fixo |
| `cellphone` | string | Celular |
| `birth_date` | date | Data de nascimento (YYYY-MM-DD) |
| `gender` | string | Gênero |
| `company_name` | string | Razão social (PJ) |
| `newsletter` | number | 0=não inscrito, 1=inscrito na newsletter |
| `created_at` | datetime | Data de cadastro |

## Validações Brasileiras

- **CPF**: deve ser um CPF válido (11 dígitos, algoritmo de verificação)
- **CNPJ**: deve ser um CNPJ válido (14 dígitos, algoritmo de verificação)

## Corpo da Requisição (POST/PUT)

```json
{
  "Customer": {
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "cpf": "12345678901",
    "phone": "1133334444",
    "cellphone": "11999998888",
    "newsletter": 1
  }
}
```

## Paginação

`limit` (máximo 50, padrão 30), `page`.

## Recursos Relacionados

- **Endereços**: gerenciados via API separada — consulte o skill `tray-enderecos-cliente`
- **Perfis**: gerenciados via API separada — consulte o skill `tray-perfis-cliente`

## Boas Práticas

1. **E-mail único** — o e-mail é identificador único do cliente na plataforma
2. **Valide CPF/CNPJ** — antes de enviar, valide localmente para evitar erros 400
3. **Newsletter opt-in** — respeite a LGPD, envie `newsletter: 1` apenas com consentimento
4. **Webhook** — configure o webhook `customer` para receber notificações de alterações

## Como Usar no Claude Code

### Exemplos de Prompt

- "cadastra um novo cliente pessoa física com CPF e telefone"
- "busca o cliente pelo e-mail joao@exemplo.com"
- "lista todos os clientes inscritos na newsletter"
- "implementa a sincronização de clientes do meu ERP para a Tray"

### O que o Claude faz

1. Gera o código de criação com wrapper `Customer` e validação de CPF/CNPJ
2. Usa filtros de listagem (`email`, `cpf`, `newsletter`) para buscas específicas
3. Inclui tratamento de erro para e-mail duplicado (cliente já existente)
4. Sugere o fluxo completo: cliente → endereço → perfil quando necessário

### O que você recebe

- Código de criação com wrapper `{"Customer": {...}}` e campos obrigatórios
- Validação local de CPF/CNPJ antes da chamada à API
- Código de busca por e-mail ou CPF via filtros de listagem
- Orientação sobre campos LGPD (`newsletter`)

### Pré-requisitos

- `access_token` configurado
- E-mail único por cliente
