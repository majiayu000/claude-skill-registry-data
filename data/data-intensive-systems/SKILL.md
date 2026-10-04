---
name: data-intensive-systems
description: Especialista em Sistemas Data-Intensive (Reliabilidade, Escalabilidade e Manutenibilidade) baseado em Designing Data-Intensive Applications 2nd Edition (Martin Kleppmann & Chris Riccomini). Cobre modelos de dados e linguagens de consulta, storage engines (LSM-Tree, B-Tree, column stores), encoding e evolução de schemas, replicação, particionamento/sharding, transações ACID e isolamento (snapshot isolation, serializabilidade SSI), consistência e consenso (Raft, consenso linearizável), processamento batch e stream (log-structured, CDC, exatamente-once), filosofia de sistemas stream e ética de dados.
---

# Habilidade de IA: Sistemas Data-Intensive (Data-Intensive Applications)

Esta skill orienta a inteligência artificial a projetar, avaliar e operar sistemas cujo desafio principal é **quantidade, complexidade e velocidade de dados** (não intensivos em CPU), baseada na obra *Designing Data-Intensive Applications, 2nd Edition* (Martin Kleppmann & Chris Riccomini, O'Reilly 2026).

---

## 🏛️ 1. Fundações: Confiabilidade, Escalabilidade, Manutenibilidade

- **Trade-offs em data systems** (cap. 1): toda escolha — SQL vs NoSQL, consistência vs latência, batch vs stream — é um trade-off; o motor de decisão são os **requisitos não-funcionais** (SLOs de latência, throughput, disponibilidade).
- **Confiabilidade**: tolerar falhas de hardware, software e humanas com testes de caos, degradação graciosa e recuperação verificada.
- **Escalabilidade**: descreva carga com parâmetros (RPS, hit ratio, cardinalidade) e avalie como crescer 10× afeta cada camada; desempenho via percentis (p50/p99) e throughput em regime.
- **Manutenibilidade**: opere pela simplicidade (abstrações que escondem complexidade acidental), evolvibilidade e transparência operacional.

---

## 🗃️ 2. Modelos de Dados, Storage e Encoding

### Modelos e linguagens de consulta
- **Relacional vs Documento vs Grafo**: documentos refletem estruturas locais (um-para-muitos) com schema flexível; relacional normaliza e suporta joins/otimizador forte; grafos (Cypher/SPARQL) naturalizam navegação recursiva e muitos-para-muitos.
- Escolha pelo **formato dos dados do domínio e padrão de acesso**, não por modismo.

### Storage engines
- **LSM-Tree (log-structured)**: writes sequenciais rápidos, compressão alta; paga com compactions, amplificação de escrita e variação de latência (stalls de compaction).
- **B-Tree**: leituras previsíveis, transações fortes maduras; paga amplificação de escrita em páginas aleatórias e write-ahead log.
- **Índices secundários, clustering, column-oriented**: column stores comprimem e chrupam analíticas (vectorized execution); row stores otimizam OLTP por linha.
- **Hash vs range partitions** no disco; bloom filters para evitar lookups vazios em LSM.

### Encoding e evolução de schemas
- **Esquemas de codificação**: JSON/XML legíveis mas volumosos; binários (Protocol Buffers, Avro, Thrift) compactos e tipados.
- **Evolução (rolling upgrades)**: compatibilidade *backward* (leitor novo lê dado velho) e *forward* (leitor velho lê dado novo) — regule com `optional`/campos numerados (Avro: writer/reader schema; schema registry).
- **Dataflow maduras**: via banco (o dado sobrevive ao código), REST/RPC (contratos versionados), event streaming (eventos imutáveis com schema versionado).

---

## 🔁 3. Replicação e Particionamento

### Replicação
| Estratégia | Descrição | Trade-off central |
| :--- | :--- | :--- |
| **Single-leader** | Escritas no líder; réplicas seguem o log | Simples; lag e failover com perda possível |
| **Multi-leader** | Vários líderes aceitam escritas | Multi-DC writing; conflitos que precisam resolução (LWW/CRDT/hook) |
| **Leaderless (Dynamo-style)** | Cliente escreve em quorum | Alta disponibilidade; quorum `W+R>N`, read repair, anti-entropy |

- Semânticas de garantias: read-your-writes, monotonic reads, consistent prefix reads — implementáveis via sticky sessions/version tokens.
- **Detecção de falhas** (timeouts) e **consenso de failover** (evitar split brain com epoch/fencing tokens).

### Particionamento (sharding)
- **Por chave (hash) vs por faixa (range)**: hash distribui carga uniformes mas mata range queries; range preserva queries mas cria hotspots.
- **Skew e hotspots**: mitiguve com salting, particionamento composto (ex: (user_id, timestamp)) e shards de gravidade dinâmica.
- **Rebalancing**: strategy fixa de hash mod é ruim; use Consistent Hashing ou partições fixas (mais que nós) migração barata.
- **Consultas cross-shard**: scatter/gather custoso; desenhe schemas com "transactional locality" (dados juntos no shard do agregado) e secondary indexes globais (document-based vs term-based).
- **Rebalancing e consistência**: mova dados com protocolo "dual-write + backfill + cutover", evitando leituras sujas durante migração.

---

## 🛡️ 4. Transações e Isolamento

- **Níveis de isolamento e anomalias**: dirty reads, lost updates, write skew, phantom reads — cada nível (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) nega um conjunto de anomalias.
- **Snapshot Isolation (MVCC)**: leituras de snapshot consistente sem bloquear escritores; implementações: PostgreSQL, Oracle; perene em distributed DBs (Spanner, FoundationDB).
- **Serializable Snapshot Isolation (SSI)**: detección de conflitos rw/ww + rethrows — serializabilidade com performance de SI.
- **Transações distribuídas**: 2PC bloqueante; alternativas semi-assíncronas: Percolator, Spanner (TrueTime + 2PC), Calvin (determinístico pré-ordenado).
- **Guia prático**: se o requisito não exige multi-objeto atômico em breve escala, considere transação de objeto único + logging assíncrono; se exige, plano de capitulação (saga/compensação) para limites do isolamento.

---

## 🌐 5. Consistência e Consenso

- **Linearizabilidade**: máximo de consistência (registrar behaves como um único nó); custa latência e disponibilidade sob partição (CAP).
- **Ordem causal e happens-before**: causal consistency mais barata que linearizável; sequencer de causalidade (version vectors, Lamport clocks).
- **Consenso (Raft/Paxos/Zab)**: unanimidade sobre um valor com liderança eleita e log replicado; base de metadados (etcd/ZooKeeper) e locking/fencing.
- **Fencing tokens**: cada lease/lock emite token monotônico; serviços de storage rejeitam tokens antigos para matar zombie writes.
- **Sem consenso?** Use "o suficiente" para o caso: read-your-writes em sessão, causal API, sessions sticky, ou CRDTs para dados colaborativos offline.

---

## 🔬 6. Processamento Batch e Stream

### Batch (cap. 11)
- **Modelo MapReduce / dataflow engine (Spark, Flink batch, Beam)**: particionar → map → shuffle → reduce; falhas tratadas por retry de tarefa com saída determinística.
- **Joins**: reduce-side (grande × grande), map-side (broadcast), hash partition joins.
- **Materialized views / batch em datasets** (Dataflow + HDFS/S3) alimenta_feed de ML, indexes e outputs de BI com reprocessamento incremental (checkpoints).

### Stream (cap. 12–13)
- **Log-structured message broker (Kafka/Amazon Kinesis)**: log append-only particionado, replay seguro, offsets em vez de acks destrutivos.
- **Linguagens de streaming**: processamento de eventos (Flink/Dthree) — janelas (event-time vs processing-time), watermarks para atraso, exatamente-once via checkpoints (chandy-lamport) e transações 2PC de sink.
- **CDC (Change Data Capture) e Databases Internals**: banco como fonte de eventos — Debootstrap (Debezium), log-based extraction sem thrashing no banco.
- **Deriving state from streams**: compacted topics (Kafka Streams, changelog topics), "unbundled database" — stream processor + storage especializado por visão.
- **Filosofia stream (cap. 13)**: unificar batch e stream (Lambda vs Kappa), desenhe fluxo primeiro, derive visões; camadas de exatamente-once (idempotência + transações) e ordem por chave.

---

## ⚖️ 7. Ética, Impacto e Filosofia de Projeto (cap. 14)

- Privacidade por design (PII minimizada),svg beveillamento de consentimento, derivada de dados (inference risks), equidade algorítmica e autorização determinata.
- Data systems são produtos sócio-técnicos: documente lineage e fontes, promova transparência e capacidade de correção (GDPR art. 16–17, LGPD arts. VIII/18).

---

## 🧭 8. Protocolo de Decisão para Arquitetura de Dados

1. **Liste抒 requisitos não-funcionais** (SLO de leitura/escrita, volume/days, SLA de disponibilidade) antes de escolher o storage.
2. **Modele o domínio** (relacional/documento/grafão) pelo padrão de acesso (OLTP vs analítica vs relacionamento).
3. **Defina o contrato de consistência** por caso de uso (linearizável vs causal vs eventual) e escolha a arquitetura de replicação que o suporte ao menor custo.
4. **Dimensione particionamento** com headroom (chave de shard por throughput futuro), evitando hotspots conhecidos.
5. **Especifique evolução** (compatibilidade de schemas, política de rolling upgrade, schema registry).
6. **Escolha os ferramentais** integrados, não monoculturas: log de eventos como espinha, streams para visões incrementais, batch para reprocessamentos.
7. **Valide com failure modes**: timeouts, partição, lag de réplica, GC pause — teste cada um com leukemia de caos e verifique invariantes (quórum, fencing, idempotência).

---

## 🔗 Integração com Outras Skills

- [system-design-scalability](../../engineering-practices/system-design-scalability/SKILL.md): CAP/PACELC, sharding e caching à larga escala (visão sistêmica).
- [latency-engineering](../../engineering-practices/latency-engineering/SKILL.md): custo de latência de consenso, réplicas e janela de consistência.
- [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md) e [db-postgresql](../db-postgresql/SKILL.md): operação real de storage engines e transações.
- [realtime-streaming-event-driven](../realtime-streaming-event-driven/SKILL.md): Kafka, Flink, Pinot e OLAP em tempo real.
- [data-mesh-governance](../data-mesh-governance/SKILL.md): governança federada e data products na malha corporativa.