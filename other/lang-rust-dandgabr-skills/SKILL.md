---
name: "lang-rust"
description: "Fornece padrões de engenharia de software em Rust baseados na documentação oficial (doc.rust-lang.org), na tradução brasileira 'A Linguagem de Programação Rust' (rust-br.github.io/rust-book-pt-br), em 'The Rust Programming Language 3rd Edition' (Klabnik, Nichols, Krycho) e em 'Programming Rust 2nd Edition' (Blandy, Orendorff, Tindall), cobrindo Ownership, Borrowing, Lifetimes, Structs, Enums e Pattern Matching exaustivo, Módulos e Crates, Coleções (Vec/String/HashMap), tratamento de erros (Result/Option/thiserror), Genéricos e Traits, Closures e Iterators zero-cost, Smart Pointers (Box/Rc/Arc/RefCell/Mutex), Concorrência (threads, channels, Send/Sync), Async (Tokio), Testes (cargo test), Cargo Workspaces e Profiles, Unsafe Rust/Nomicon e FFI."
---

# Habilidade de IA: Engenharia de Rust (Rust Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem **Rust**, seguindo rigorosamente as diretrizes da documentação oficial ([rust-lang.org/pt-BR/learn](https://www.rust-lang.org/pt-BR/learn)) — *O Livro* (A Linguagem de Programação Rust, com [tradução pt-BR](https://rust-br.github.io/rust-book-pt-br/title-page.html)), *Rust by Example*, *Rustlings*, *The Cargo Book*, *The Rustonomicon* e a *Referência* — sempre via `rustup doc` para consulta offline. O objetivo é criar código seguro contra corridas de dados (*data races*), livre de vazamentos de memória (sem Garbage Collector), concorrente e de extrema performance.

> 📖 **Referência canônica**: consulte [references/rust-book-guide.md](references/rust-book-guide.md) para o guia consolidado dos capítulos do Livro (conceitos comuns, ownership/borrowing/slices, structs, enums e match, módulos, coleções, erros, genéricos/traits/lifetimes, testes, closures/iterators, Cargo/workspaces, smart pointers, concorrência, padrões avançados e keywords).
> 📖 **Referência avançada**: consulte [references/programming-rust-advanced-guide.md](references/programming-rust-advanced-guide.md) para temas profundos (layout de memória/size/align, traits e generics avançados, unsafe/raw pointers/unions/unsafe traits, atomics e memory orderings, macros `macro_rules!` com fragment specifiers, Pin/Unpin e internals de Futures, FFI com `repr(C)` e panic safety).

---

## 🧭 Diretrizes Gerais de Desenvolvimento em Rust

Ao atuar nesta skill, aplique rigorosamente os fundamentos de segurança de memória e concorrência destemida (*fearless concurrency*):

### 1. Sistema de Posse (Ownership), Empréstimo (Borrowing) e Lifetimes
- **Posse Única (Ownership)**: Cada valor em Rust tem um único proprietário por vez. Quando o proprietário sai de escopo, o valor é desalocado automaticamente via trait `Drop` (RAII).
- **Movimentação (Move Semantics)**: Atribuições de tipos não-Copy (ex.: `String`) transferem a posse e invalidam a origem ("use of moved value"). Tipos `Copy` (inteiros, floats, bool, char) copiam implicitamente; cópia profunda é explícita com `.clone()`.
- **Regras de Empréstimo (Borrowing)**:
  - Pode-se ter qualquer número de referências imutáveis (`&T`) **OU** exatamente uma referência mutável (`&mut T`) em um determinado escopo, mas nunca ambas simultaneamente.
  - Referências devem ser sempre válidas (prevenção de ponteiros pendentes / *dangling pointers*).
- **Slices (`&str`, `&[T]`)**: Prefira views sem posse em assinaturas de API — `fn first_word(s: &str) -> &str` em vez de `&String`, aproveitando deref coercion.
- **Tempo de Vida (Lifetimes)**:
  - Utilize anotações explícitas de tempo de vida (`'a`) em estruturas e funções apenas quando o compilador não puder elidir as regras de tempo de vida (Lifetime Elision Rules).
  - Em estruturas que guardam referências, garanta que a struct não sobreviva ao dado emprestado (`struct Livro<'a> { titulo: &'a str }`).

### 2. Modelagem de Dados Idiomática (Structs, Enums e Pattern Matching)
- **Structs + `impl`**: campos privados por padrão (expostos com `pub`), métodos com `&self`/`&mut self`/`self` e construtores como associated functions (`::new`). Documente com `///`.
- **Enums com dados**: Modele estados e mensagens como `enum` com payloads (`enum Shape { Circle(f64), Square { side: f64 } }`) — equivalente a discriminated unions.
- **`match` exaustivo**: O compilador exige cobertura total de casos; use guards (`x if x > 5`), bindings `@`, or-patterns `|` e destructuring. Para um caso único, prefira `if let` / `let else`.
- **Preferência por `Option<T>`**: A ausência de valor é sempre explícita — nunca existirá `null`/`NullPointerException`; `.unwrap_or`, `.map`, `.and_then`, `.ok_or(err)` compõem com segurança.
- **Newtypes**: `struct Meters(f64);` para type-safety em unidades e invariáveis de domínio.

### 3. Tratamento Idiomático de Erros (`Result` e `Option`)
- **Sem Exceções em Tempo de Execução**: Rust não utiliza exceções. Erros recuperáveis devem ser representados pelo tipo enum `Result<T, E>` (`Ok`/`Err`) e valores opcionais por `Option<T>`; falhas de invariante de programador usam `panic!`.
- **Operador de Propagação `?`**: Prefira propagar erros usando o operador `?` em vez de chamadas repetitivas de `match` ou `.unwrap()`.
- **Proibição de `.unwrap()` em Produção**: Evite `.unwrap()` e `.expect()` em código de produção, exceto em testes unitários ou invariantes matematicamente comprovadas.
- **Panics como Vetor de DoS**: Prefira métodos não-panicking — `.get(i)` em vez de `v[i]`, `checked_add`/`saturating_add` em vez de operadores aritméticos em inputs não confiáveis.
- **Tratamento Encadeado de Erros**: Utilize crates consolidadas como `thiserror` (para definir erros de bibliotecas) e `anyhow` (para tratamento flexível de erros em aplicações binárias, com `.context()`).

### 4. Abstração Zero-Cost, Traits e Genéricos
- **Polimorfismo Baseado em Traits**: Defina comportamentos compartilhados utilizando `trait` (com default methods). Prefira dispatch estático (*monomorphization*) usando `impl Trait` ou genéricos `<T: Trait>` com bounds em `where`.
- **Dynamic Dispatch (`dyn Trait`)**: Use `Box<dyn Trait>` apenas quando for estritamente necessário alocar tipos heterogêneos em tempo de execução (dynamic dispatch via vtable).
- **Closures e Iterators (Cap. 13)**: Preferir o estilo funcional zero-cost — `iter().filter().map().sum()` compila para loop nativo. Compreender os traits de captura de closure: `Fn` (borrow), `FnMut` (mutable borrow), `FnOnce` (consume); use `move` ao transferir dados para threads/tasks.
- **Derivações Automáticas**: Utilize atributos decoradores como `#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]` em structs e enums sempre que apropriado.

### 5. Organização de Projetos (Módulos, Crates e Cargo)
- **Estrutura**: Package → crates (lib/binário) → módulos (`mod`/`pub`/`use`/`super::`/`crate::`). Idioma padrão: **library crate com a lógica + binary crate fino** (`main.rs` mínimo).
- **Cargo.toml**: declare edition (2015/2018/2021), dependências (com features) e **profiles** (`[profile.release] opt-level = 3`); use `cargo check` para iteração rápida, `cargo test` para todos os níveis de teste (unit, integration em `tests/`, doc-tests).
- **Workspace**: monorepos com múltiplos crates compartilhando `Cargo.lock`/`target` (Cargo Workspaces).
- **Qualidade de Código e Formatação**:
  - **`rustfmt`**: Formatação estrita oficial do código (`cargo fmt`).
  - **`clippy`**: Linter oficial para capturar antipadrões e otimizações (`cargo clippy -- -D warnings`).
- **Segurança de Dependências**: Execute `cargo audit` periodicamente para verificar vulnerabilidades conhecidas em crates de terceiros.

### 6. Concorrência e Programação Assíncrona (`Async/Await`)
- **Segurança Concorrente Estática**: Tipos que podem ser transferidos entre threads com segurança implementam o marker trait `Send`. Tipos que podem ser acessados concorrentemente via referências imutáveis implementam `Sync`.
- **Sincronização Primitiva**: Use `Arc<T>` (Atomic Reference Counting) para compartilhamento de posse entre threads e `Mutex<T>` ou `RwLock<T>` para mutabilidade interior concorrente.
- **Ecossistema Assíncrono (`Future`)**:
  - Utilize o padrão `async/await` com um runtime assíncrono consolidado como **Tokio** ou `async-std`.
  - Evite bloqueios síncronos de I/O em tarefas assíncronas (use `tokio::task::spawn_blocking` quando necessário).

### 7. Unsafe Rust e FFI
- **Encapsulamento Estrito de `unsafe`**: Isole blocos `unsafe` dentro de abstrações e funções públicas totalmente seguras (*safe wrappers*).
- **Invariantes de Segurança**: Documente detalhadamente as precondições e invariantes de segurança (`// SAFETY: ...`) em cada bloco `unsafe`.
- **FFI (Foreign Function Interface)**: Utilize `extern "C"` e C-compatible tipos (`c_char`, `c_int`) para interoperabilidade segura com C/C++.

## 🚀 Rust Moderno (Edition 2024 / TRPL 3ª ed.)

O Livro, em sua 3ª edição (Rust 1.85+), reflete os idiomas da **edition 2024** — declarada com `edition = "2024"` no `Cargo.toml`. Destaques:

- **Async como capítulo canônico**: a 3ª ed. traz um novo Capítulo 17 (Fundamentals of Asynchronous Programming) cobrindo `async`/`await` junto com os traits `Future` e `Stream` — deixou de ser apêndice "avançado".
- **`let else`**: para padrões refutáveis, `let Some(x) = value else { return; };` trata o caso de não-correspondência com um bloco de saída (divergência) em vez de propagar `Option` (TRPL, Cap. 19). Erros de padrões não-exaustivos em `let` sugerem migar para `let else`.
- **Trait objects de `Future`**: `dyn Future<Output = ()>` não é `Unpin` — o compilador indicará `Box::pin` quando for necessário fixar futuros heterogêneos coletados em `Box<dyn Future>` (TRPL, Cap. 17, Pin/Unpin).
- **`Box<dyn Error>` como tipo de erro padrão**: retorno `Result<T, Box<dyn Error>>` em `main` e em testes aceita qualquer tipo de erro via `?` — o padrão idiomático da 3ª ed. para aplicações antes de migrar para `anyhow`.

```rust
use std::error::Error;
use std::fs::File;

fn main() -> Result<(), Box<dyn Error>> {
    let greeting_file = File::open("greeting.txt")?;
    Ok(())
}
```

- **`anyhow` em aplicações**: para binários, `anyhow::Result` + `?` + `.context(...)` fornece relatório de causa raiz com backtrace (Programming Rust, Cap. 7); para bibliotecas, mantenha `thiserror`.
- **Genéricos sobre arrays via const bounds**: `[T; N]` com `N` constante permite APIs genéricas sobre tamanho de array (Programming Rust, Cap. 5 e Cap. 10).
- **Closures async**: o corpo de `async fn` compila para um bloco `async move` que retém os parâmetros por posse — prefira `async move` ao transferir capturas para tasks (TRPL, Cap. 17).
- **Miri para unsafe**: a 3ª ed. introduz o uso de `cargo +nightly miri` como verificador dinâmico de undefined behavior em código `unsafe` (Cap. 20).
- **Compatibilidade garantida**: edições são retrocompatíveis — código de editions anteriores continua compilando com a `edition` correta no `Cargo.toml` (Apêndice E).

---

## 🛠️ Ferramentas e Gerenciamento de Projetos (Cargo & Toolchain)

- **Configuração de Dependências (`Cargo.toml`)**:
  - Defina dependências, recursos opcionais (*features*) e perfis de compilação.
  - Utilize `cargo check` durante o desenvolvimento para compilações rápidas sem geração de código de máquina.
- **Qualidade de Código e Formatação**:
  - **`rustfmt`**: Formatação estrita oficial do código (`cargo fmt`).
  - **`clippy`**: Linter oficial para capturar antipadrões e otimizações (`cargo clippy -- -D warnings`).
- **Segurança de Dependências**: Execute `cargo audit` periodicamente para verificar vulnerabilidades conhecidas em crates de terceiros.

---

## 🧰 Padrões de Código Recomendados

### 1. Manipulação Idiomática de Erros com `Result` e `thiserror`
```rust
use std::fs::File;
use std::io::{self, Read};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("falha de E/S ao ler o arquivo de configuração")]
    Io(#[from] io::Error),
    #[error("formato de configuração inválido: {0}")]
    InvalidFormat(String),
}

pub fn read_config(path: &str) -> Result<String, ConfigError> {
    let mut file = File::open(path)?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    
    if content.is_empty() {
        return Err(ConfigError::InvalidFormat("arquivo vazio".into()));
    }
    
    Ok(content)
}
```

### 2. Concorrência Assíncrona com Tokio e Canais
```rust
use tokio::sync::mpsc;
use tokio::task;

#[derive(Debug)]
pub struct WorkItem {
    pub id: u64,
    pub payload: String,
}

pub async fn run_pipeline(items: Vec<WorkItem>) {
    let (tx, mut rx) = mpsc::channel::<String>(32);

    for item in items {
        let tx_clone = tx.clone();
        task::spawn(async move {
            let result = format!("Processado item {}: {}", item.id, item.payload);
            let _ = tx_clone.send(result).await;
        });
    }

    drop(tx); // Fecha o transmissor original para permitir que o receptor termine quando as tasks concluírem

    while let Some(message) = rx.recv().await {
        println!("[+] Recebido: {}", message);
    }
}
```

### 3. Padrão Builder com Validação Estática
```rust
#[derive(Debug)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
}

pub struct ServerConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
}

impl ServerConfigBuilder {
    pub fn new() -> Self {
        Self { host: None, port: None }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn build(self) -> Result<ServerConfig, &'static str> {
        let host = self.host.ok_or("host é obrigatório")?;
        let port = self.port.unwrap_or(8080);
        Ok(ServerConfig { host, port })
    }
}
```

---

## 🔒 Questões de Segurança e Práticas Seguras

- **Blocos Unsafe e Comportamento Indefinido**: Isole blocos `unsafe` ao estrito necessário (deref de raw pointers, FFI, mutação de estáticos, acesso a fields de union). Certifique-se de que as premissas de segurança de memória exigidas pelo Rust sejam respeitadas, evitando desalinhamentos de dados ou referências nulas. Documente com `// SAFETY: ...`.
- **Ciclos de Referência vazam memória mesmo em Rust**: `Rc<RefCell<T>>` com ciclo destrói as garantias de liberação — use `Weak<T>` (com `upgrade() -> Option<Rc<T>>`) no lado não-dono do ciclo.
- **Mutabilidade Interior**: `RefCell<T>` viola regras de borrowing em **runtime** (panic em `borrow_mut` duplicado) — restrinja a single-thread e a superfícies pequenas; entre threads use `Mutex<T>`/`RwLock<T>` e evite deadlock (lock em ordem fixa, solte o guard cedo).
- **Data Races em Unsafe**: Embora o compilador do Rust garanta a thread-safety do código seguro, o uso incorreto de `Send`/`Sync` e ponteiros crus em blocos `unsafe` pode introduzir condições de corrida complexas.
- **Panics como Vetor de DoS**: Operações aritméticas estritas ou acessos a índices de vetores podem causar `panic!` em runtime se falharem. Use métodos seguros como `.get()` ou `.checked_add()` para evitar interrupções de serviço repentinas.
- **Strings UTF-8**: Nunca indexe `String` por byte (pode cortar caractere multibyte/travar) — itere com `chars()`/`bytes()` ou use slices em fronteiras válidas de caracteres.
- **Overflow aritmético**: em release o overflow faz wrap silencioso — valide entradas antes de operar; para contadores/protocolos use Checked/Saturating APIs.

## 🔗 Integração com Outras Skills

- Para aplicação de análise estática e revisão de segurança em código Rust, consulte [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
- Para integrar acesso a banco de dados com tipos verificados em tempo de compilação em Rust (`sqlx`, `diesel`, `tokio-postgres`, `mongodb`), consulte [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md), [db-postgresql](../../databases/db-postgresql/SKILL.md), [db-sqlite](../../databases/db-sqlite/SKILL.md), [db-mariadb](../../databases/db-mariadb/SKILL.md) e [db-mongodb](../../databases/db-mongodb/SKILL.md).
- Para desenvolvimento de ferramentas ofensivas, agentes de segurança ou parsers de alta performance em Rust, consulte [pentest-scripter-python-bash-go](../../security/appsec/pentest-scripter-python-bash-go/SKILL.md).
- Para modelar a arquitetura e comunicação entre componentes de software usando Rust, consulte [software-architect](../../roles/software-architect/SKILL.md).
