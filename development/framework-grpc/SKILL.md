---
name: "framework-grpc"
description: "Fornece padrões de engenharia para gRPC e Protocol Buffers (proto3). Cobre RPCs unários e de streaming (Server, Client, Bidirectional), definição de arquivos .proto, transporte HTTP/2, interceptores (middlewares), tratamento rico de erros google.rpc.Status e gRPC-Web."
---

# Habilidade de IA: Engenharia e Arquitetura gRPC (framework-grpc)

Esta skill orienta a inteligência artificial a atuar como especialista no framework de RPC de alta performance **gRPC** e na linguagem de IDL **Protocol Buffers (proto3)**, alinhada à documentação oficial da CNCF e gRPC.io ([grpc.io](https://grpc.io/)). Cobre modelagem de contratos de serviços, streaming bidirecional, transporte HTTP/2, interceptores, tratamento de erros e integração inter-serviços.

---

## 🧭 Especificação de Contratos com Protocol Buffers (proto3)

### 1. Padrões de Definição de Arquivos `.proto`
- Utilize a sintaxe `syntax = "proto3";`.
- Organize os pacotes logicamente para evitar colisões (`package empresa.servico.v1;`).
- Especifique atribuição numérica única e sequencial para campos (`1` a `15` consomem apenas 1 byte na codificação varint de campo).

```protobuf
syntax = "proto3";

package billing.v1;

import "google/protobuf/timestamp.proto";

option go_package = "github.com/empresa/billing/v1;billingv1";

service PaymentService {
  // RPC Unário
  rpc ProcessPayment (ProcessPaymentRequest) returns (ProcessPaymentResponse);
  
  // RPC de Streaming de Servidor
  rpc StreamTransactions (StreamTransactionsRequest) returns (stream TransactionEvent);
}

message ProcessPaymentRequest {
  string account_id = 1;
  int64 amount_cents = 2;
  string currency = 3;
  PaymentMethod method = 4;
}

enum PaymentMethod {
  PAYMENT_METHOD_UNSPECIFIED = 0;
  PAYMENT_METHOD_CREDIT_CARD = 1;
  PAYMENT_METHOD_PIX = 2;
}

message ProcessPaymentResponse {
  string transaction_id = 1;
  string status = 2;
  google.protobuf.Timestamp processed_at = 3;
}

message StreamTransactionsRequest {
  string account_id = 1;
}

message TransactionEvent {
  string transaction_id = 1;
  int64 amount_cents = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

---

## 🛠️ Padrões de Comunicação e Transporte HTTP/2

### 1. Modos de Operação RPC
1. **Unário (Unary RPC)**: Cliente envia uma única requisição e recebe uma resposta.
2. **Server Streaming RPC**: Cliente envia uma requisição e recebe um fluxo (*stream*) continuo de mensagens.
3. **Client Streaming RPC**: Cliente envia um fluxo de mensagens e aguarda uma única resposta final do servidor.
4. **Bidirectional Streaming RPC**: Cliente e servidor trocam fluxos independentes de mensagens sobre a mesma conexão multiplexada HTTP/2.

### 2. Interceptores (Middlewares)
Utilize interceptores unários e de streaming para:
- Autenticação e extração de credenciais via cabeçalhos de metadados (`metadata.MD`).
- Coleta de métricas e rastreamento distribuído (OpenTelemetry / Jaeger).
- Recuperação de pânico (*panic recovery*) e registro centralizado de chamadas.

---

## 🚨 Tratamento Rico de Erros (`google.rpc.Status`)

Evite utilizar apenas códigos gRPC brutos (`codes.Internal`, `codes.InvalidArgument`). Retorne payloads ricos de erro utilizando o modelo `google.rpc.Status`:

```json
{
  "code": 3,
  "message": "Argumentos inválidos fornecidos para a transação",
  "details": [
    {
      "@type": "type.googleapis.com/google.rpc.BadRequest",
      "field_violations": [
        {
          "field": "amount_cents",
          "description": "O valor deve ser maior que zero"
        }
      ]
    }
  ]
}
```

---

## 🔗 Integração com Outras Skills

- Para arquitetura de comunicação entre microsserviços de alta performance, consulte [backend-developer](../../roles/backend-developer/SKILL.md) e [software-architect](../../roles/software-architect/SKILL.md).
- Para implementar clientes/servidores gRPC em Go, Rust ou Python, consulte [lang-go](../../languages/lang-go/SKILL.md), [lang-rust](../../languages/lang-rust/SKILL.md) e [lang-python](../../languages/lang-python/SKILL.md).
- Para segurança da camada de transporte e autenticação mTLS em gRPC, consulte [network-security-onprem-cloud](../../security/grc-compliance/network-security-onprem-cloud/SKILL.md) e [auth-protocols-mfa](../../security/ops-architecture/auth-protocols-mfa/SKILL.md).
