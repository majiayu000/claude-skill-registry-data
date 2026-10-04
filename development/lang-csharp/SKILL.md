---
name: lang-csharp
description: Fornece padrões de engenharia de software em C# moderno (C# 12/13/14, .NET 8/10 LTS) baseados na documentação oficial (learn.microsoft.com/en-us/dotnet/csharp) e na obra C# 2026 Enterprise Mastery (Victor Mihailov). Cobre records e primary constructors, pattern matching, Span<T>/memory-efficient code, async/await e Task, LINQ e collections, SOLID pragmático, DDD tático, performance (GC, allocation tracing, pooling), observabilidade e padrões modernos de API cloud-native com Minimal APIs.
---

# Habilidade de IA: Engenharia de Software em C# (.NET Moderno)

Esta skill orienta a inteligência artificial a escrever código C# moderno, idiomático e performático, baseada na documentação oficial Microsoft (learn.microsoft.com/dotnet/csharp, C# 14 / .NET 10 LTS) e na obra *C# 2026 Enterprise Mastery* (Victor Mihailov).

---

## 🧭 1. C# Moderno (C# 9 → C# 14)

- **Records** (`record class` / `record struct`): imutabilidade com semântica de valor paraequality, DTOs e Value Objects; mutação não destrutiva via `with`.
- **Primary constructors** (C# 12): réduz ceremony em classes e structs que não precisam de lógica extra de construção.
- **Collection expressions** (C# 12): `[1, 2, ..other, 9]` — sintaxe unificada para inicialização com spread.
- **Pattern matching completo**: type patterns, property patterns, list patterns (C# 11), relational/logical (`and`, `or`, `not`) em `switch` expressions exaustivas — preferência sobre cadeias `if/else`.
- **`field` backed properties** (C# 14): valide no `set` sem declarar campo explícito — `set => field = value ?? throw new ArgumentNullException(nameof(value));`.
- **Extension members** (C# 14): blocos `extension` adicionam **extension properties** e membros estáticos (incluindo operadores), além de extension methods clássicos.
- **Null-conditional assignment** (C# 14): `customer?.Order = GetCurrentOrder();` substitui null-check básico antes de atribuir.
- **Span<T> first-class** (C# 14): conversões implícitas entre `Span<T>`, `ReadOnlySpan<T>` e `T[]` — generics e receivers de extension mais naturais; `params` aceita `ReadOnlySpan<T>` (C# 13) evitando allocation de array.
- **`System.Threading.Lock`** (C# 13): `lock` statement gera `EnterScope()`/`Dispose` — mais rápido e `TypeSafe` que `Monitor` sobre object.
- **Required members** (C# 11), **file-local types** (C# 11), **file-scoped namespaces** (C# 10) e **global usings** (C# 10): organização e expressividade.

---

## 🏛️ 2. SOLID Pragmático e Domain Modeling

- **SRP com coesão de razão de mudança**: "uma razão para mudar, não um método"; extraia sub-passos quando um método mistura níveis de abstração.
- **OCP/DIP com composição**: programe para abstrações; injete dependências (DI nativo em .NET) em vez de new dentro de classes de domínio.
- **LSP/ISP**: interfaces pequenas e coesas; evite interfaces "god" que forçam implementações vazio (violam LSP).
- **DDD tático**: Aggregates com invariantes protegidos, Value Objects imutáveis (records), Domain Events para efeitos colaterais; agregados pequenos com fronteiras claras (regra de ouro: agregado referencia outros por ID, não por navegação direta).
- **GoF no runtime**: muitos padrões são built-in — Builder (object initializers + required), Strategy (delegates/lambdas), Iterator (`IEnumerable`), Observer (`IObservable`/events), Decorator/Proxy (DIN + middleware); **não implemente o que o runtime dá**.
- **Código que perdura**: nomes reveladores de intenção, métodos em um nível de abstração, guard clauses cedo, classes fechadas para modificação mas abertas para extensão.

---

## ⚡ 3. Performance (GC, Span, Async, AOT)

### 3.1 Gerenciamento de memória e GC
- **Generational GC**: objetos de vida curta temporários são baratos (Gen0); evite LOH (Large Object Heap) para buffers >= 85 KB — use `ArrayPool<T>.Shared`/`MemoryPool<T>` para buffers grandes reutilizáveis.
- **Alocação e profiling**: `dotnet-counters monitor --counters System.Runtime` para GC em produção; `dotnet-trace collect --profile gc-verbose` para trace de alocações de 30 s; `dotnet-gcdump collect` para heap snapshot e análise dos tipos mais alocados.
- **Struct vs class**: structs pequenos e imutáveis evitam indireção e GC, mas cuidado com copy de structs grandes (passe por `in`/`ref readonly`).
- **Pooling e stackalloc**: `stackalloc` em operações de buffer de vida curta (até ~1 KB), `Span<T>` para slices sem alocação, `string.Create` para strings construídas.

### 3.2 Span e código memory-efficient
- Passe `ReadOnlySpan<T>`/`Span<T>` em hot paths (parsing, slicing) em vez de arrays/String; evite `.ToString()`/`.ToArray()` intermediários.
- `Utf8JsonReader`/`Utf8JsonWriter` para JSON de alta performance sem materializar `string`.
- **AVX10.2, devirtualização de métodos e improved inline** chegam pelo runtime .NET 10 — projete camadas de abstração estáveis para permitir o JIT otimizar.

### 3.3 Async/await correto
- `async all the way` — nunca `.Result`/`.Wait()` (deadlock + thread starvation); `ConfigureAwait(false)` em bibliotecas de infraestrutura.
- **`ValueTask<T>`** para paths frequentemente síncronos (evita alocação de Task); Task quando sempre assíncrono.
- `IAsyncEnumerable<T>` + `await foreach` para streams assíncronos; `CancellationToken` propagado em toda cadeia async.
- Evite `async void` (somente handlers de evento); captura de contexto leve em hot loops.

### 3.4 Native AOT e cloud-native
- **NativeAOT** para startup < 100 ms e footprint mínimo (APIs serverless/containers); desabilitar reflexão dinâmica não-compatível.
- JSON: `System.Text.Json` com source generators (`JsonSerializerContext`) — sem reflexão, compatível com AOT e mais rápido.
- Minimal APIs para endpoints leves; analise tamanho de imagem (`dotnet publish /p:PublishAot=true`).

---

## 🏗️ 4. Padrões de Aplicação Enterprise (.NET 10)

- **Cloud-Native APIs**: ASP.NET Core 10 (Minimal APIs, OpenAPI integrado, `WebSocketStream`), idioms de versionamento e Idempotency-Key em mutações.
- **Observabilidade**: OpenTelemetry nativo (traces/metrics/logs), `ILogger` estruturado (sem Sensitive Data), ActivitySource para correlação distribuída.
- **Entity Framework Core 10**: LINQ melhorado, named query filters múltiplos, Cosmos DB melhorado — veja EF Core pitfalls em [jpa-hibernate-performance](../../databases/jpa-hibernate-performance/SKILL.md) N+1 equivalents (lazy loading + projection).
- **Segurança**: Data Protection API, autenticação/authorização com passkeys (Identity .NET 10), PQC (ML-DSA) disponível nas libs criptográficas do .NET 10.
- **Resiliência**: Microsoft.Extensions.Resilience/Polly v8 (circuit breaker, timeout, retry com backoff) em chamadas outbound.

---

## 🧪 5. Protocolo de Implementação e Revisão (C#)

1. **Modele o domínio** com records + primary constructors; valide invariantes no constructor/property (`field` keyword).
2. **Defina a estratégia de concorrência** (`async/await` para I/O, `System.Threading.Lock` para exclusão, `Channel<T>` para pipelines produtor-consumidor).
3. **Perf-first no hot path**: spans, pooling, source-generated JSON; meça com BenchmarkDotNet antes de aceitar otimização.
4. **Instrumente**: `dotnet-counters`, `dotnet-trace`, `dotnet-gcdump`, JFR-like com EventCounters — veja exemplo no livro (trace de 30 s, heap dump, análise de tipos mais alocados).
5. **Testes**: xUnit/NUnit com MTP (`dotnet test` .NET 10), WebApplicationFactory para endpoints; cobertura de invariantes de domínio.
6. **Documente** API com XML comments e OpenAPI; versioning explícito.

---

## 🔗 Integração com Outras Skills

- [backend-developer](../../roles/backend-developer/SKILL.md): integração de serviços e contratos REST/gRPC.
- [framework-rest-api](../../framework/framework-rest-api/SKILL.md): design de APIs HTTP idiomático para ASP.NET Core.
- [latency-engineering](../../engineering-practices/latency-engineering/SKILL.md): eliminação de work no hot path e tail latency.
- [code-optimizer](../../roles/code-optimizer/SKILL.md): o agente de otimização orquestra esta skill em refatorações C#.
- [lang-java](../lang-java/SKILL.md): paralelo direto de concorrência (Loom vs async/await) e JVM vs CLR.