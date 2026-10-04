---
name: "framework-graphql"
description: "Fornece padrões de engenharia e design de APIs baseados na especificação oficial GraphQL (GraphQL Foundation). Cobre Schema Definition Language (SDL), tipos de operação (Query, Mutation, Subscription), resolvedores, DataLoader para prevenção de N+1, formato de resposta e erros, introspecção, diretivas, Relay Cursor Connections e segurança de queries."
---

# Habilidade de IA: Engenharia e Arquitetura de APIs GraphQL (framework-graphql)

Esta skill orienta a inteligência artificial a atuar como especialista em design, arquitetura e implementação de **APIs GraphQL**, alinhada rigorosamente às especificações oficiais da GraphQL Foundation ([spec.graphql.org](https://spec.graphql.org/)). Cobre modelagem de esquemas usando GraphQL SDL (Schema Definition Language), construção de operações executáveis (Queries, Mutations e Subscriptions), arquitetura de resolvedores, mitigação do problema N+1 com DataLoader, paginação padrão Relay, formato estrito de resposta e tratamento de erros, e boas práticas de segurança e otimização.

---

## 🧭 Sistema de Tipos e Linguagem de Definição de Esquema (GraphQL SDL)

### 1. Tipos Escalares e Wrappers de Nulo/Lista
- **Escalares Nativos**: `Int`, `Float`, `String`, `Boolean`, `ID`.
- **Escalares Customizados**: Defina escalares explícitos para validação de dados específicos (ex: `DateTime`, `JSON`, `EmailAddress`).
- **Modificadores de Tipo (Non-Null e List)**:
  - `[User]`: Lista nula de usuários nulos.
  - `[User!]`: Lista nula de usuários não-nulos.
  - `[User!]!`: Lista não-nula de usuários não-nulos (padrão mais recomendado para coleções).

### 2. Definição Declarativa do Esquema (SDL)

```graphql
"""
Representa a conta de um usuário no sistema.
"""
type User implements Node {
  id: ID!
  name: String!
  email: String!
  role: UserRole!
  orders(first: Int = 10, after: String): OrderConnection!
  createdAt: DateTime!
}

"""
Padrão de Interface Node para identificação única global (padrão Relay).
"""
interface Node {
  id: ID!
}

enum UserRole {
  ADMIN
  CUSTOMER
  GUEST
}

"""
Entrada de dados para criação de novo usuário.
"""
input CreateUserInput {
  name: String!
  email: String!
  role: UserRole = CUSTOMER
}

type CreateUserPayload {
  user: User
  userErrors: [UserError!]!
}

type UserError {
  field: [String!]!
  message: String!
}

"""
Diretivas nativas e customizadas para alterar comportamentos de execução e validação.
"""
directive @auth(requires: UserRole = ADMIN) on FIELD_DEFINITION | OBJECT
```

---

## 🛠️ Definição de Operações Executáveis (Queries, Mutations & Subscriptions)

### 1. Queries, Fragmentos e Aliases
Utilize variáveis explícitas, fragmentos reutilizáveis e aliases para evitar colisões e otimizar payloads no lado do cliente:

```graphql
query GetUserProfileWithOrders($userId: ID!, $orderLimit: Int!) {
  user(id: $userId) {
    ...BasicUserFields
    recentOrders: orders(first: $orderLimit) {
      edges {
        node {
          id
          totalAmount
          status
        }
      }
    }
  }
}

fragment BasicUserFields on User {
  id
  name
  email
  role
}
```

### 2. Mutations e Design de Payload de Resposta
Adote o padrão **Mutation Ingest Input / Payload Output**:
- As mutations devem aceitar um único parâmetro de entrada (`input: CreateUserInput!`).
- Retorne um payload contendo a entidade criada/modificada e uma coleção declarativa de erros de domínio (`userErrors`).

```graphql
mutation CreateNewCustomer($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
      email
    }
    userErrors {
      field
      message
    }
  }
}
```

### 3. Subscriptions (Comunicação em Tempo Real)
Implemente assinaturas reativas sobre WebSocket/Server-Sent Events (SSE) para atualização de eventos no cliente:

```graphql
subscription OnOrderStatusUpdated($orderId: ID!) {
  orderStatusUpdated(orderId: $orderId) {
    id
    status
    updatedAt
  }
}
```

---

## ⚡ Arquitetura de Resolvedores e Resolução de N+1 (DataLoader)

### 1. Modelo de Execution & Resolver Tree
Cada campo no GraphQL possui um resolvedor (*resolver*). Os resolvedores recebem quatro argumentos padrão: `(parent/root, args, context, info)`.

### 2. Prevenção do Problema N+1 com DataLoader
Evite disparar múltiplas consultas SQL/HTTP para coleções associadas agrupando e armazenando requisições em lote (*batching and caching*) no ciclo de vida por requisição HTTP.

```typescript
import DataLoader from 'dataloader';

// Resolver delegando a busca para DataLoader no contexto por requisição
export const resolvers = {
  User: {
    orders: (parent, args, context) => {
      return context.loaders.ordersByUserId.load(parent.id);
    },
  },
};

// Instanciação do DataLoader no context da requisição
export function createLoaders(dbConnection) {
  return {
    ordersByUserId: new DataLoader(async (userIds: readonly string[]) => {
      const orders = await dbConnection.findOrdersByUserIds(userIds);
      // Mapeia os resultados garantindo a mesma ordem das chaves solicitadas
      return userIds.map(id => orders.filter(order => order.userId === id));
    }),
  };
}
```

---

## 📑 Paginação Padrão (Relay Cursor Connections Specification)

Sempre que retornar listas extensas de dados, utilize a especificação **Relay Cursor Connections** para suportar paginação infinita e eficiente baseada em cursores bidirecionais:

```graphql
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  cursor: String!
  node: Order!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## 🚨 Formato de Resposta e Tratamento Estrito de Erros (GraphQL Spec)

A especificação GraphQL determina um formato de resposta JSON estrito composto por `data`, `errors` e `extensions`:

```json
{
  "data": {
    "user": null
  },
  "errors": [
    {
      "message": "Acesso negado para visualização deste recurso",
      "locations": [
        {
          "line": 3,
          "column": 5
        }
      ],
      "path": ["user"],
      "extensions": {
        "code": "FORBIDDEN",
        "timestamp": "2026-08-07T14:30:00Z"
      }
    }
  ],
  "extensions": {
    "tracing": {
      "version": 1,
      "duration": 4500000
    }
  }
}
```

- **Propagação de Erros Nulos (*Error Bubbling*)**: Se um erro ocorrer em um campo declarado como Não-Nulo (`!`), o erro propaga para o ancestral anulável mais próximo. Defina os campos com segurança para evitar que pequenas falhas anulem toda a árvore da resposta `data`.

---

## 🔒 Segurança, Proteção de Introspecção e Limitação de Taxa

1. **Limitação de Profundidade (Query Depth Limiting)**:
   - Limite a profundidade máxima aninhada das consultas (ex: máximo de 5 a 7 níveis) para evitar ataques de DoS com queries recursivas circulares.
2. **Cálculo de Complexidade de Query (Cost Analysis / Query Complexity)**:
   - Atribua um custo por campo ou coleção e recuse a execução caso o custo exceda o limite máximo permitido por requisição.
3. **Desativação de Introspecção em Produção**:
   - Desative as consultas de introspecção (`__schema`, `__type`) em ambientes de produção para ocultar detalhes da estrutura do modelo interno do atacante.
4. **Persisted Queries (Automatic Persisted Queries - APQ)**:
   - Permita apenas a execução de hashes SHA-256 pré-aprovados de queries em produção para reduzir largura de banda e bloquear requisições arbitrárias.

---

## 🔗 Integração com Outras Skills

- Para projetar a arquitetura completa de backend e integração com banco de dados, consulte [backend-developer](../../roles/backend-developer/SKILL.md) e [software-architect](../../roles/software-architect/SKILL.md).
- Para integração de clientes GraphQL no Frontend com React ou Vue, consulte [framework-react](../framework-react/SKILL.md) e [framework-vue](../framework-vue/SKILL.md).
- Para auditoria de segurança em APIs GraphQL segundo a OWASP API Security Top 10, consulte [pentester-owasp-api-security-2023](../../security/appsec/pentester-owasp-api-security-2023/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
- Para comparar ou integrar com outros estilos de API, consulte [framework-rest-api](../framework-rest-api/SKILL.md), [framework-grpc](../framework-grpc/SKILL.md) e [framework-soap](../framework-soap/SKILL.md).
- Para implementação segura em TypeScript ou Python, consulte [lang-typescript](../../languages/lang-typescript/SKILL.md) e [lang-python](../../languages/lang-python/SKILL.md).
