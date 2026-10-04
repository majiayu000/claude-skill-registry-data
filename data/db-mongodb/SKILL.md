---
name: "db-mongodb"
description: "Fornece padrões de administração e engenharia para MongoDB baseados na documentação oficial em português (mongodb.com/pt-br/docs). Cobre modelagem de documentos (Embedding vs Referencing), motor WiredTiger, Read/Write Concern, índices (Compound, Multikey, Text, TTL, 2dsphere), Aggregation Framework e Sharded Clusters."
---

# Habilidade de IA: Engenharia e Administração de MongoDB (db-mongodb)

Esta skill orienta a inteligência artificial a atuar como especialista no banco de dados Orientado a Documentos **MongoDB**, fundamentada na documentação oficial ([mongodb.com/pt-br/docs](https://www.mongodb.com/pt-br/docs/)). Cobre estratégias avançadas de modelagem de esquemas, motor de armazenamento WiredTiger, garantias de consistência (Write/Read Concern), otimização com índices, Aggregation Framework, Replica Sets e Sharded Clusters.

---

## 🧭 Modelagem de Dados Orientada a Documentos

No MongoDB, a modelagem é orientada pelos padrões de acesso da aplicação (consultas de leitura e gravação juntas), em vez da normalização estrita:

### 1. Incorporação (*Embedding*) vs. Referência (*Referencing*)
- **Embutir (Desnormalização - Preferencial)**:
  - Utilize quando houver relacionamentos 1:1 ou 1:N (onde N é limitado e pequeno, ex: endereços de um cliente).
  - Garante atomacidade de gravação e leituras de alto desempenho em uma única operação de E/S.
- **Referenciar (Normalização)**:
  - Utilize quando houver relacionamentos 1:N (onde N é ilimitado ou muito grande, ex: logs de auditoria) ou N:M.
  - Evita o limite máximo de tamanho de documento do BSON (16 MB).

### 2. Padrões de Projeto de Esquema (*Schema Design Patterns*)
- **Subset Pattern**: Guarda apenas os N dados mais recentes ou acessados no documento principal e o restante em uma coleção separada.
- **Bucket Pattern**: Agrupa dados de séries temporais (*time-series*) ou métricas de IoT por janelas de tempo (ex: 1 hora) para reduzir número de documentos e otimizar índices.
- **Outlier Pattern**: Trata documentos excepcionalmente grandes separadamente sem penalizar a maioria dos documentos padrão.

---

## 🛠️ Indexação Avançada e Otimização de Consultas

### 1. Tipos de Índices no MongoDB
- **Composto (*Compound Index*)**: Siga a regra ESR (**Equality, Sort, Range**):
  - 1º: Campos de igualdade exata (`$eq`).
  - 2º: Campos usados na ordenação (`sort()`).
  - 3º: Campos de intervalo (`$gte`, `$lte`, `$in`).
- **Multikey Index**: Criado automaticamente ao indexar campos contendo arrays.
- **TTL Index**: Apaga documentos automaticamente após um tempo especificado:
  ```javascript
  db.sessions.createIndex({ "createdAt": 1 }, { expireAfterSeconds: 3600 });
  ```
- **Geoespacial (`2dsphere`)**: Para consultas de proximidade (`$near`, `$geoWithin`).

### 2. Análise com `explain()`
Execute sempre a explicação com modo `executionStats` para diagnosticar varredura de coleção (*COLLSCAN*):
```javascript
db.orders.explain("executionStats").find({
  status: "COMPLETED",
  createdAt: { $gte: ISODate("2026-01-01") }
});
```

---

## 🔍 Aggregation Framework Nativo

Utilize pipelines de agregação para transformações complexas de dados de forma nativa e paralela:

```javascript
db.orders.aggregate([
  // 1. Filtragem inicial usando índice
  { $match: { status: "COMPLETED", orderDate: { $gte: ISODate("2026-01-01") } } },
  
  // 2. Junção com a coleção de clientes
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer_details"
    }
  },
  
  // 3. Desfazer o array gerado pelo lookup
  { $unwind: "$customer_details" },
  
  // 4. Agrupamento e cálculo de métricas
  {
    $group: {
      _id: "$customer_details.segment",
      totalRevenue: { $sum: "$totalAmount" },
      averageOrderValue: { $avg: "$totalAmount" },
      totalOrders: { $count: {} }
    }
  },
  
  // 5. Ordenação do resultado
  { $sort: { totalRevenue: -1 } }
]);
```

---

## ⚙️ Concorrência, Consistência e Alta Disponibilidade

### 1. Consistência e Garantias de Durabilidade
- **Write Concern**: Controla a confirmação da escrita pelo cluster:
  - `w: "majority"`: Garante que a escrita foi persistida no journal da maioria dos nós do Replica Set (previne *rollback* no failover).
- **Read Concern**:
  - `rc: "majority"`: Retorna apenas dados confirmados pela maioria dos nós.
  - `rc: "linearizable"`: Garante leitura estritamente em tempo real (evita leituras obsoletas).

### 2. Arquitetura de Produção
- **Replica Sets**: Mínimo de 3 nós votantes (1 Primário e 2 Secundários) para automatizar a eleição e o failover sem indisponibilidade.
- **Sharded Cluster**: Para escalabilidade horizontal em múltiplos terabytes de dados. Escolha a **Shard Key** com atenção para evitar *jumbo chunks* ou pontos quentes (*hotspots*) de gravação.

---

## 🔒 Hardening e Conformidade de Segurança (OWASP ASVS & CIS MongoDB Benchmark)

- **Autenticação Obrigatória e TLS**:
  - Habilite autenticação de controle de acesso (`security.authorization: enabled`).
  - Exija conexões cifradas TLS 1.3/1.2 (`net.tls.mode: requireTLS`).
- **Autenticação Interna do Cluster**: Utilize certificados X.509 ou chave de arquivo (*keyFile*) para comunicação entre nós de Replica Set ou Shards.
- **Criptografia no Nível de Campo (CSFLE - Client-Side Field Level Encryption)**: Cifre dados sensíveis (PII, números de cartão) no cliente usando chaves KMS antes da transmissão para o banco.
- **Validação de Esquema (`$jsonSchema`)**: Aplique Schema Validation na coleção para evitar injeção de operador NoSQL (`$where`, `$gt: ""`).

---

## 🔗 Integração com Outras Skills

- Para integrar MongoDB em APIs Node.js/TypeScript ou Python, consulte [backend-developer](../../roles/backend-developer/SKILL.md), [lang-typescript](../../languages/lang-typescript/SKILL.md) e [lang-python](../../languages/lang-python/SKILL.md).
- Para diretrizes gerais de administração de bancos de dados NoSQL e SQL, consulte [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- Para validação de segurança e conformidade de dados (V8/V14), consulte [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md), [cis-controls](../../security/grc-compliance/cis-controls/SKILL.md) e [security-privacy](../../security/grc-compliance/security-privacy/SKILL.md).
