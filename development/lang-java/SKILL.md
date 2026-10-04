---
name: lang-java
description: Fornece padrões de engenharia de software em Java moderno (Java 17/21/25 LTS) baseados na documentação oficial (docs.oracle.com/en/java), Java Concurrency in Practice (Goetz) e boas práticas de JVM. Cobre lambdas/Streams, Records e sealed classes, Virtual Threads (Project Loom), concorrência segura (Executor framework, immutability, happens-before, CompletableFuture), Collections, Pattern Matching, JCTools/Agrona e tuning de JVM (G1/ZGC, JIT).
---

# Habilidade de IA: Engenharia de Software em Java (Java Moderno e Concorrência)

Esta skill orienta a inteligência artificial a escrever código Java moderno, idiomático e thread-safe, baseada na documentação oficial Java (JDK 21/25 LTS — docs.oracle.com/en/java) e na obra *Java Concurrency in Practice* (Brian Goetz et al., Addison-Wesley).

---

## 🧭 1. Java Moderno (Linguagem)

- **Records**: use para dados imutáveis (Value Objects, DTOs). Componha com `record` patterns para deconstrução segura.
- **Sealed classes/interfaces**: modele hierarquias fechadas (ADTs) combinadas com pattern matching em `switch` exaustivo.
- **Text blocks e switch expressions**: prefira `switch` como expressão (arrows, exaustividade compilada) a cadeias de if/else.
- **Optional**: tipo de retorno de consultas eventualmente vazias; **nunca** para campos ou parâmetros (anti-padrão).
- **Streams**: expressam pipelines sobre coleções; cuidado em hot paths (alocação de lambdas/boxes); use loops tradicionais onde o profiler apontar gargalo.
- **Var e generics**: `var` para tipo óbvio local; escreva generics com PECS (`extends`/`super` wildcards corretos) e bounded types.
- **Imutabilidade por padrão**: `final` em campos, classes fecháveis, coleções imutáveis (`List.of`, `Map.copyOf`). Imutáveis são thread-safe gratuitos.

---

## 🔀 2. Concorrência Segura (Java Concurrency in Practice)

### 2.1 Estado compartilhado e visibilidade
- **Regra de ouro**: sempre que mais de um thread acessa um mesmo estado mutável, **todas** as vias de acesso devem usar o mesmo lock.
- **Volatile**: garante visibilidade e ordenação (happens-before), não atomicidade composta. Use para flags de parada e publicação segura; nunca para `count++`.
- **Happens-before**: monitor locks, `volatile`, `Thread.start/join`, `Executor.submit`, `CompletableFuture` estabelecem happens-before; sem ele, reordenações do JIT tornam dados publicados inconsistências (stale data, reordering).
- **Escape analysis e publicação**: publique objetos imutáveis livremente (safe publication); objetos mutáveis exigem synchronization, `final` fields ou fences.
- **Thread confinement**: stack confinement (locais), `ThreadLocal` — zero sincronização quando o estado não cruza threads.

### 2.2 Composição de objetos thread-safe
- **Delegação**: componha segurança a partir de classes thread-safe (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `AtomicLong`, `BlockingQueue`).
- **Invariantes multi-variáveis** (ex: `lower <= upper`): exigem **um único lock** que cubra todos os campos do invariante; delegar por variável quebra o invariante.
- **Client-side locking frágil**: só se o "cliente" souber qual lock a classe usa; prefira extensão por composição.
- **Immutability como estratégia**: objetos imutáveis podem ser compartilhados sem lock (regra happens-before do campo `final`).

### 2.3 Building blocks (java.util.concurrent)
- **Executor framework**: nunca crie `Thread` cru em produção — desacople submissão de execução com `ExecutorService` (thread pools nomeados, `ManagedThreadFactory` em containers).
- **BlockingQueues** (`ArrayBlockingQueue`, `LinkedBlockingQueue`, `SynchronousQueue`): produtor/consumidor com backpressure natural.
- **Sincronizadores**: `CountDownLatch` (aguardar N eventos), `Semaphore` (limitar acesso), `CyclicBarrier` (pontos de sincronização), `Phaser` (fases).
- **ConcurrentHashMap**: não sincronize manualmente o mapa; use `compute`, `computeIfAbsent`, `putIfAbsent` para atomicidade por chave.
- **CompletableFuture**: composição assíncrona não-bloqueante (`thenApply/thenCompose/thenCombine`, `orTimeout`); evite `get()` sem timeout.

### 2.4 Task execution e pools
- **Tamanho do pool**: CPU-bound ≈ `Runtime.availableProcessors()`; IO-bound ≈ `cores × (1 + wait/compute)`. Prefira filas limitadas (`ArrayBlockingQueue`) + política de saturação (`CallerRunsPolicy` para degenerar graciosamente, ou rejeição com backpressure).
- **Executores da plataforma vs `newVirtualThreadPerTaskExecutor`**: I/O-intensivo com milhões de tarefas → Virtual Threads; CPU-intensivo → pool fixo de Platform Threads.
- **Encontre o paralelismo explorável** (Lei de Amdahl): adicionar threads além dos núcleos de CPU não acelera cargas CPU-bound; adiciona contaminação de cache e trocas de contexto.

### 2.5 Cancellation, shutdown e liveness
- **Cooperação**: implemente cancelamento via interruption (`Thread.interrupt`, checks periódicos de `isInterrupted`) ou flag `volatile` de cancelamento.
- **Time-outs em todas as blocking calls**; nunca `Thread.stop`/`suspend` (deprecadas/destrutivas).
- **Deadlock** (lock-ordering cycles): ordene aquisição de locks globalmente; alternativas com `tryLock` timeout (recuperação sem deadlock).
- **Starvation e livelock**: evite prioridades de thread; fairness (`new ReentrantLock(true)`) só onde estritamente necessário.
- **Shutdown gracioso**: `shutdown()` + `awaitTermination` + "shutdown hooks" para estados persistentes.

### 2.6 Competição e performance
- **Reduza contenção**: escopo do lock curto, lock striping/concurrent collections, copy-on-write para read-heavy, atômicos (CAS) em contadores leves (`LongAdder` em alta contenção).
- **Nonblocking algorithms** (CAS/lock-free): `AtomicReference`/`AtomicStampedReference` (ABA com versionamento); prefira bibliotecas maduras (JCTools, Agrona) a lock-free caseiro.
- **False sharing**: pad fields compartilhados entre threads em cache lines distintas (`@Contended`/jdk.internal.vm.annotation ou padding manual).

---

## 🧵 3. Virtual Threads (Project Loom, JDK 21+)

Baseado na documentação oficial (docs.oracle.com/en/java/javase/21/core/virtual-threads.html, JEP 444):

- **O que são**: instâncias de `java.lang.Thread` implementadas pelo runtime Java (não pelo SO), mapeando milhões de threads virtuais em poucos *carrier threads* de plataforma. Bloqueio de I/O suspende (unmount) a thread virtual, liberando o carrier.
- **Fornecem escala (throughput), não velocidade (latência)**: não executam código mais rápido que platform threads; existem para ampliar concorrência em servidores thread-per-request.
- **Quando usar**: altíssimo throughput concorrente com tarefas majoritariamente bloqueadas em I/O (HTTP, JDBC); **não** para tarefas CPU-intensivas ou longas.
- **Escreva código síncrono simples com I/O bloqueante**: o estilo thread-per-request com APIs bloqueantes é o que mais se beneficia; evite misturar código bloqueante síncrono com frameworks assíncronos (Callbacks/CompletableFuture encadeado não se beneficia).
- **Nunca faça pool de virtual threads**: crie um executor por tarefa com `Executors.newVirtualThreadPerTaskExecutor()` (leve, fechável com try-with-resources). O número de threads virtuais deve igualar o número de tarefas concorrentes, como "strings para nomes".
- **Use `Semaphore` para limitar concorrência** (ex: serviço externo que aceita 10 chamadas simultâneas) em vez de pool de threads — filas de threads bloqueadas são equivalentes a filas de tarefas. Pools de conexão de banco já funcionam como semáforo.
- **Pinning**: uma thread virtual **não desmonta do carrier** quando bloqueia dentro de bloco/método `synchronized` ou método `native`/FFM. Pinning frequente e longo prejudica a escalabilidade.
  - Detecção: evento JFR `jdk.VirtualThreadPinned` (default > 20 ms) ou `-Djdk.tracePinnedThreads=full|short`.
  - Correção: troque `synchronized` por `ReentrantLock` (`lock.lock(); try { ... } finally { lock.unlock(); }`) nos pontos longos; preserve `synchronized` em operações curtas/infrequentes.
- **ThreadLocal**: cuidado com caches de objetos caros em `ThreadLocal` (ex: `SimpleDateFormat`) — com milhões de threads virtuais cada tarefa instancia um objeto novo (o oposto do efeito desejado). Prefira objetos imutáveis compartilhados (`DateTimeFormatter`) ou Scoped Values.
- **Observabilidade**: dumps com `jcmd <pid> Thread.dump_to_file -format=json <file>`; eventos JFR `jdk.VirtualThreadStart/End/Pinned/SubmitFailed`.

---

## ⚡ 4. Tuning de JVM e Boas Práticas de Performance

- **GC**: G1 (padrão balanceado), ZGC/Shenandoah (latência de sub-ms com heap grande); dimensione `-Xms`/`-Xmx` iguais em produção; monitore pausas e frequência de full GC.
- **JIT**: métodos pequenos quentes são inlinados; evite megamorphic call sites (mantenha bimorphic), métodos frios grandes quebram inlining.
- **Medidas**: microbenchmarks com JMH (forks, warmup, blackhole); nunca `System.nanoTime` avulso; profilers async-profiler/flamegraphs para CPU e alocação.
- **Coleções**: escolha pelo perfil de acesso (`HashMap` vs `ConcurrentHashMap`, `ArrayDeque` em vez de `Stack`, `EnumMap` tipados); sized adequadamente (`initialCapacity`) evita rehash.
- **Strings e I/O**: `StringBuilder` em loops; buffers com size adequado; UTF-8 explícito.

---

## 🧪 5. Protocolo de Implementação e Revisão (Java)

1. **Modele o estado compartilhado**: identifique variáveis mutáveis compartilhadas e escolha a estratégia (imutável > confinement > concurrent collection > lock).
2. **Desacople tarefas com Executors**: defina política (pool size, fila, saturação, naming, context propagation) documentada.
3. **Prove a thread-safety**: invariante identificado + mecanismo que o protege + teste de estresse concorrente (ex: jcstress para algoritmos avançados).
4. **Prefira APIs de alto nível** (`java.util.concurrent`) a primitivas (`synchronized/wait/notify`) quebradas à mão.
5. **Instrumente e meça**: latência p99, GC, contention (jstack, JFR, jitwatch) antes/depois da mudança.
6. **Documente**: estados compartilhados com o lock/guard que os protege, razões de invariante e política de shutdown.

---

---

## 🧼 6. Java Distiller: Refatoração, Modernização e Código Idiomático (Java 21/25)

Inspirado nos princípios do *Java Distiller* da comunidade SouJava, aplique a simplificação rigorosa e a eliminação de complexidade acidental:

### 6.1 Transformações Canônicas de Modernização
1. **POJO / JavaBean para Record**:
   - Substitua classes de transporte de dados verbosas (getters, setters, equals, hashCode manuais) por `record`.
   - Utilize deconstrução com Record Patterns:
     ```java
     if (response instanceof SuccessResponse(var payload, var timestamp)) {
         process(payload);
     }
     ```
2. **Loops Imperativos para Stream Pipelines & Gatherers**:
   - Converta loops com acumuladores e mutação de listas para Streams declarativos:
     ```java
     // Antes: loop imperativo acumulador
     // Depois:
     var activeNames = users.stream()
         .filter(User::isActive)
         .map(User::name)
         .toList();
     ```
3. **Switch Expressions & Sealed Hierarchies**:
   - Elimine árvores de `instanceof` e casts manuais. Use `switch` exaustivo com type pattern matching:
     ```java
     return switch (event) {
         case OrderCreated e -> handleCreated(e);
         case OrderCancelled e -> handleCancelled(e);
     };
     ```
4. **Legado Date/Calendar para `java.time`**:
   - Elimine `java.util.Date`, `Calendar` e `SimpleDateFormat` (não thread-safe). Use `Instant`, `LocalDate`, `ZonedDateTime` e `DateTimeFormatter`.
5. **Eliminação de Código Prolixo ("Distill, don'''t decorate")**:
   - Remova abstrações intermediárias que apenas delegam chamadas sem agregar valor de domínio.
   - Preserve comportamento funcional idêntico com menos linhas e maior expressividade.

---

## 🔗 Integração com Outras Skills

- [jpa-hibernate-performance](../../databases/jpa-hibernate-performance/SKILL.md): persistência eficiente (N+1, batching, cache) em Java.
- [backend-developer](../../roles/backend-developer/SKILL.md): integração de serviços e APIs com contratos REST/gRPC.
- [latency-engineering](../../engineering-practices/latency-engineering/SKILL.md): sizing de thread pools com Little's Law e redução de lock contention.
- [lang-python](../lang-python/SKILL.md) e [python-performance-parallelism](../../engineering-practices/python-performance-parallelism/SKILL.md): equivalentes de concorrência em Python (GIL vs Loom).
- [code-optimizer](../../roles/code-optimizer/SKILL.md): o agente de otimização orquestra esta skill em refatorações Java.