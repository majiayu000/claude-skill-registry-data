---
name: "lang-cpp"
description: "Fornece padrões de engenharia de software em C++ moderno baseados na norma internacional ISO/IEC 14882 (com foco em C++23 - ISO/IEC 14882:2024, C++20, C++17 e C++14) e na documentação do en.cppreference.com, cobrindo RAII, Smart Pointers, Concepts, Modules, Coroutines, std::expected, std::print, Ranges, CMake e C++ Core Guidelines."
---

# Habilidade de IA: Engenharia de C++ Moderno (ISO/IEC 14882 Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem **C++ moderno**, baseando-se estritamente na norma internacional oficial **ISO/IEC 14882** e nas referências técnicas do [en.cppreference.com](https://en.cppreference.com/). O foco engloba a revisão mais recente **C++23 (ISO/IEC 14882:2024)**, **C++20 (ISO/IEC 14882:2020)**, C++17, C++14 e C++11, garantindo o cumprimento dos princípios de *Zero-Cost Abstractions*, gestão segura de recursos via **RAII**, concorrência destemida e alinhamento com as **C++ Core Guidelines**.

---

## 🧭 Evolução dos Padrões ISO/IEC 14882 e Recursos C++ Modernos

Ao projetar software em C++, utilize as ferramentas e abstrações mais recentes suportadas pelo compilador do projeto:

### 1. ISO/IEC 14882:2024 (C++23 - Padrão Mais Recente)
- **Tratamento de Erro Monádico (`std::expected`)**: Substituto eficiente para exceções e código de erro tradicional (`std::expected<T, E>`), fornecendo encadeamento com `.and_then()`, `.transform()` e `.or_else()`.
- **Formatador e Impressão Nativa (`std::print` / `std::println`)**: Impressão direta e tipada para streams sem a sobrecarga de `std::cout` (`#include <print>`).
- **Novos Contêineres de Desempenho (`std::flat_map` / `std::flat_set`)**: Adaptadores de contêiner baseados em vetores contíguos de memória com excelente localidade de cache.
- **Geradores e Corrotinas (`std::generator`)**: Criação simplificada de iteradores e sequências lazily-evaluated baseados em corrotinas (`co_yield`).
- **Deducing `this` (Explicit Object Parameters)**: Simplificação de métodos de classe, recursão de lambdas e padrão CRTP.
- **Utilitários Adicionais**: Inversão de bytes nativa (`std::byteswap`), extensões de `std::span` e atributo `[[assume(expr)]]`.

### 2. ISO/IEC 14882:2020 (C++20)
- **Conceitos e Restrições (`concepts` e `requires`)**: Validação de metaprogramação no tempo de compilação com mensagens de erro legíveis (`template <std::integral T>`).
- **Módulos do C++ (`module`, `import`, `export`)**: Substituição do modelo tradicional de headers (`#include`) por módulos compilados com isolamento de escopo e tempos de build drasticamente reduzidos.
- **Ranges e Pipelines (`std::ranges`)**: Composição de algoritmos de forma funcional utilizando o operador pipe `|` (`views::filter`, `views::transform`).
- **Corrotinas Nativas**: Suporte a funções suspensíveis com `co_await`, `co_yield` e `co_return`.
- **Operador Espaçonave (`<=>` / Three-Way Comparison)**: Geração automática de todos os operadores de comparação (`auto operator<=>const = default;`).
- **Formatação de Texto (`std::format`)**: Interpolação de strings rápida e segura inspirada na sintaxe do Python.
- **Concorrência e Threads**: `std::jthread` (thread com RAII e auto-join) e tokens de cancelamento (`std::stop_token`).

### 3. ISO/IEC 14882:2017 (C++17) & 14882:2014 (C++14)
- **C++17**: Tipos utilitários de valor (`std::optional`, `std::variant`, `std::any`), visualização sem alocação (`std::string_view`), Structured Bindings (`auto [x, y] = point;`), suporte a arquivos (`std::filesystem`), `if` com inicializador local e algoritmos paralelos (`std::execution::par`).
- **C++14**: `std::make_unique`, lambdas genéricas (`auto x`), `std::shared_lock` e `constexpr` relaxado.

### 4. ISO/IEC 14882:2011 (C++11 - A Base do C++ Moderno)
- Semântica de Movimento (*Move Semantics*) com rvalue references (`std::move`, `std::forward`).
- Smart Pointers para RAII: `std::unique_ptr` (posse exclusiva), `std::shared_ptr` e `std::weak_ptr`.
- Concorrência nativa: `<thread>`, `<mutex>`, `<atomic>`, `<future>`.

---

## 🛠️ Diretrizes de Engenharia e C++ Core Guidelines

### 1. RAII (Resource Acquisition Is Initialization)
- **Zero Vazamentos Manuais**: Nunca invoque `new` ou `delete` explicitamente. Encapsule a gestão de recursos (memória, sockets, arquivos, mutexes) em objetos RAII (`std::unique_ptr`, `std::lock_guard`, `std::fstream`).
- **Regra dos Zero, Três ou Cinco (Rule of Zero/3/5)**: Se uma classe precisa gerenciar recursos explicitamente, defina ou delete os 5 métodos especiais (destrutor, construtor de cópia, atribuição por cópia, construtor de movimento, atribuição por movimento). Prefira a *Rule of Zero* delegando a gestão para smart pointers e contêineres padrão.

### 2. Tratamento Seguro de Erros e Imutabilidade
- **`const` por Padrão**: Marque variáveis, referências e métodos membros como `const` sempre que o valor não sofrer mutação.
- **`constexpr` e `consteval`**: Mova o máximo de computação possível para o tempo de compilação.
- **`noexcept`**: Marque funções que garantidamente não lançam exceções (especialmente construtores de movimento e operadores de movimentação).

---

## 🧰 Padrões de Código Recomendados

### 1. C++23: Tratamento de Erros Monádico com `std::expected` e Impressão Nativa (`std::print`)
```cpp
#include <print>
#include <expected>
#include <string_view>

enum class MathError {
    DivisionByZero,
    NegativeLogarithm
};

constexpr std::expected<double, MathError> divide(double a, double b) noexcept {
    if (b == 0.0) {
        return std::unexpected(MathError::DivisionByZero);
    }
    return a / b;
}

int main() {
    auto result = divide(10.0, 2.0)
        .transform([](double val) { return val * 100.0; });

    if (result.has_value()) {
        std::println("[+] Sucesso! Resultado calculado: {:.2f}", result.value());
    } else {
        std::println(stderr, "[-] Erro no cálculo matemático.");
    }
    return 0;
}
```

### 2. C++20: Conceitos, Ranges e Operador Espaçonave (`<=>`)
```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <concepts>
#include <compare>

// Definição de conceito em C++20
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

struct Item {
    std::string name;
    double price;

    // Operador de comparação espaçonave C++20
    auto operator<=>(const Item&) const = default;
};

template <Numeric T>
T calculate_sum(const std::vector<T>& values) {
    T sum = 0;
    for (const auto& v : values) {
        sum += v;
    }
    return sum;
}

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Filtro e transformação com C++20 Ranges
    auto even_squares = numbers 
        | std::views::filter([](int n) { return n % 2 == 0; })
        | std::views::transform([](int n) { return n * n; });

    std::cout << "[+] Quadrados pares: ";
    for (int val : even_squares) {
        std::cout << val << " ";
    }
    std::cout << "\n";
    return 0;
}
```

### 3. Gestão Segura de Recursos com Smart Pointers (`std::unique_ptr`)
```cpp
#include <memory>
#include <string>
#include <iostream>

class DatabaseConnection {
public:
    explicit DatabaseConnection(std::string conn_str) 
        : connection_string_(std::move(conn_str)) {
        std::cout << "[+] Conexão aberta: " << connection_string_ << "\n";
    }

    ~DatabaseConnection() {
        std::cout << "[-] Conexão fechada automaticamente por RAII.\n";
    }

    void execute_query(std::string_view query) const {
        std::cout << "    Executando: " << query << "\n";
    }

private:
    std::string connection_string_;
};

int main() {
    // Alocação segura sem chamar 'new'
    auto db = std::make_unique<DatabaseConnection>("Server=localhost;Port=5432;");
    db->execute_query("SELECT * FROM users;");
    
    // Conexão desalocada automaticamente no término do escopo
    return 0;
}
```

---

## ⚙️ Configuração de Build System Moderno (CMakeLists.txt C++23)

```cmake
cmake_minimum_required(VERSION 3.26)
project(cpp23_modern_project CXX)

# Impoe o padrão C++23 (ISO/IEC 14882:2024)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(app_main src/main.cpp)

# Bateria estrita de compilação e flags de segurança
if (MSVC)
    target_compile_options(app_main PRIVATE /W4 /WX /permissive-)
else()
    target_compile_options(app_main PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror)
endif()
```

---

## 🔒 Questões de Segurança e Práticas Seguras

- **Gerenciamento de Recursos (RAII)**: Evite gerenciamento manual com `new` e `delete`. Use Smart Pointers (`std::unique_ptr`, `std::shared_ptr`) para mitigar Use-After-Free e Memory Leaks.
- **Object Slicing e Type Confusion**: Tenha cuidado ao converter ponteiros de classes base para classes derivadas. Use `dynamic_cast` para realizar checagens em tempo de execução de forma segura.
- **Sobrecarga de Operadores e Construtores de Cópia**: Evite vazamento de recursos na atribuição de objetos implementando corretamente o construtor de cópia e operador de atribuição (Rule of Three/Five/Zero).
- **Injeção em Métodos Virtuais (vtable hijacking)**: Impeça heranças não intencionais declarando classes ou métodos como `final` para reduzir a superfície de ataque de desvio de fluxo.

## 🔗 Integração com Outras Skills

- Para desenvolvimento e interoperabilidade direta com código C (C23/C17), consulte [lang-c](../lang-c/SKILL.md).
- Para realizar testes unitários em código C++ utilizando frameworks modernos, consulte [framework-testing](../../framework/framework-testing/SKILL.md) e [framework-criterion](../../framework/framework-criterion/SKILL.md).
- Para auditoria de vulnerabilidades de segurança de memória, Use-After-Free, buffer overflows e segurança de código C++, consulte [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
