---
name: "lang-c"
description: "Fornece padrões de engenharia de software em C moderno baseados na norma internacional ISO/IEC 9899 (com foco em C23 - ISO/IEC 9899:2024, C17, C11 e C99) e nas referências oficiais de en.cppreference.com/w/c, cobrindo palavras-chave (nullptr, bool, constexpr), atributos ([[nodiscard]], [[deprecated]]), matemática segura (<stdckdint.h>), operações de bits (<stdbit.h>), depuração de memória e CMake."
---

# Habilidade de IA: Engenharia de C Moderno (ISO/IEC 9899 & cppreference Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem **C moderno**, baseando-se estritamente na norma internacional oficial **ISO/IEC 9899** (publicada pelo ISO JTC1/SC22/WG14 em [iso-9899.info](https://www.iso-9899.info/wiki/The_Standard)) e na documentação oficial de referência do C em [en.cppreference.com/w/c](https://en.cppreference.com/w/c). O foco principal é a versão mais recente **C23 (ISO/IEC 9899:2024)**, mantendo suporte às revisões C17, C11 e C99 para a construção de sistemas de baixo nível de alta performance, seguros e isentos de Comportamentos Indefinidos (*Undefined Behavior - UB*).

---

## 🧭 Especificações da Linguagem C (en.cppreference.com/w/c)

Ao desenvolver em C, consulte a especificação e as tabelas formais dos cabeçalhos da Biblioteca Padrão no `cppreference`:

### 1. ISO/IEC 9899:2024 (C23 - Padrão Mais Recente)
- **Novas Palavras-Chave Nativas**:
  - `nullptr`: Tipo estrito `nullptr_t` para ponteiros nulos, substituindo a ambiguidade numérica do `NULL`.
  - `bool`, `true`, `false`: Tipos booleanos nativos (sem dependência de `<stdbool.h>`).
  - `constexpr`: Avaliação de constantes imutáveis no tempo de compilação.
  - `auto`: Inferência automática de tipos na declaração de variáveis.
  - `typeof` e `typeof_unqual`: Operadores de inspeção de tipo em tempo de compilação.
  - `static_assert`, `alignas`, `alignof`, `thread_local`: Palavras-chave simplificadas (sem prefixo `_`).
- **Sintaxe Unificada de Atributos (`[[attribute]]`)**:
  - `[[nodiscard]]`: Alerta se o valor retornado por uma função for ignorado.
  - `[[maybe_unused]]`: Suprime avisos para variáveis ou parâmetros intencionalmente não utilizados.
  - `[[deprecated("motivo")]]`: Sinaliza funções ou tipos obsoletos.
  - `[[likely]]` / `[[unlikely]]`: Pistas de otimização para previsão de desvio (*branch prediction*).
  - `[[fallthrough]]`: Declaração explícita de queda intencional em instruções `switch`.
  - `[[noreturn]]`: Indica que a função nunca retorna (ex: `exit`, `abort`).
- **Novos Cabeçalhos e Funções de Segurança da Libc**:
  - **`<stdckdint.h>`**: Operações aritméticas inteiras com checagem de estouro (*checked integer arithmetic*): `ckd_add`, `ckd_sub`, `ckd_mul`.
  - **`<stdbit.h>`**: Manipulação de bits padronizada: `stdc_count_ones`, `stdc_leading_zeros`, `stdc_trailing_zeros`, `stdc_has_single_bit`, `stdc_bit_ceil`.
  - `memset_explicit`: Sanitização de memória confidencial (senhas, chaves) imune a otimizações de eliminação do compilador.
  - `memalignment`: Verificação de alinhamento em bytes de ponteiros.
  - `strdup` e `strndup`: Alocação e duplicação dinâmica de strings padronizada na libc.
  - `unreachable()`: Macro de otimização para caminhos de código inalcançáveis (`<stddef.h>`).
- **Pré-processador e E/S Modernos**:
  - `#embed`: Inclusão direta de recursos binários em dados no tempo de compilação.
  - `#elifdef` e `#elifndef`, macros `__has_include` e `__VA_OPT__`.
  - Formato de inteiros binários `%b` e `%B` em `printf`/`scanf` e literais `0b1010`.
  - Inicialização nula com chaves vazias: `struct Buffer buf = {};`.

### 2. ISO/IEC 9899:2018 (C17) & 9899:2011 (C11)
- **`<threads.h>` (C11)**: Gestão de threads nativas (`thrd_create`, `thrd_join`), exclusão mútua (`mtx_t`, `mtx_lock`, `mtx_unlock`) e variáveis de condição (`cnd_t`).
- **`<stdatomic.h>` (C11)**: Tipos e operações atômicas sem lock (`atomic_int`, `atomic_store`, `atomic_load`, `atomic_compare_exchange_strong`).
- **`_Generic`**: Seleção genérica de expressões baseada em tipos para macros polimórficas.
- **C17**: Correções técnicas e esclarecimentos de ambiguidades da norma C11 sem adição de novas características sintáticas.

### 3. ISO/IEC 9899:1999 (C99)
- Comentários de linha `//`, inicializadores nomeados (`.field = val`), literais compostos, `inline`, qualificador `restrict`, inteiros de largura fixa em `<stdint.h>` e tipos complexos `<complex.h>`.

---

## 🛠️ Diretrizes de Engenharia e Prevenção de Defeitos

### 1. Prevenção Estrita de Comportamento Indefinido (Undefined Behavior - UB)
- **Gestão de Memória Segura**:
  - Sempre zere ou inicialize memória alocada dinamicamente (`malloc`/`calloc`).
  - Atribua `nullptr` (C23) ou `NULL` a ponteiros imediatamente após liberá-los com `free()`.
  - Em alocações contendo dados de senhas ou chaves, utilize `memset_explicit()` antes do `free()`.
- **Estouro de Inteiros**: Evite estouro de inteiros sinalizados utilizando as funções checked de `<stdckdint.h>` (C23) ou verificações prévias de limites.
- **Evitar VLAs (Variable Length Arrays)**: Prefira alocação dinâmica em heap ou tamanhos fixos para evitar estouro de pilha (*stack overflow*).

### 2. Análise Estática e Sanitizers
- Compilação com avisos estritos ativados: `-Wall -Wextra -Wpedantic -Wconversion -Wshadow -std=c23`.
- Execução com Sanitizers durante os testes: `-fsanitize=address,undefined,leak`.

---

## 🧰 Padrões de Código C23 Recomendados (cppreference style)

### 1. Aritmética Inteira Segura e Atributos (`<stdckdint.h>` & C23)
```c
#include <stdio.h>
#include <stdckdint.h>

[[nodiscard]] bool safe_multiply_and_add(int a, int b, int c, int *result) {
    int temp = 0;
    
    // Multiplicação com checagem de estouro em C23
    if (ckd_mul(&temp, a, b)) {
        return false; // Estouro detectado
    }
    
    // Adição com checagem de estouro em C23
    if (ckd_add(result, temp, c)) {
        return false; // Estouro detectado
    }
    
    return true;
}

int main(void) {
    int val = 0;
    if (safe_multiply_and_add(100000, 200000, 50, &val)) {
        printf("[+] Resultado seguro: %d\n", val);
    } else {
        printf("[-] Erro: Estouro de inteiro prevenido!\n");
    }
    return 0;
}
```

### 2. Manipulação de Bits Nativa C23 (`<stdbit.h>`)
```c
#include <stdio.h>
#include <stdbit.h>
#include <stdint.h>

int main(void) {
    uint32_t mask = 0b00111010;
    
    // Funções padronizadas de contagem de bits em C23 (stdbit.h)
    unsigned int ones = stdc_count_ones(mask);
    bool is_power_of_two = stdc_has_single_bit(mask);

    printf("[+] Número de bits 1: %u\n", ones);
    printf("[+] É potência de dois? %s\n", is_power_of_two ? "sim" : "não");

    return 0;
}
```

### 3. Uso do `nullptr`, Atributos e Limpeza Segura de Memória (`memset_explicit`)
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char username[32];
    char secret_token[64];
} UserAccountSecure;

void wipe_sensitive_data(UserAccountSecure *account) {
    if (account == nullptr) {
        return;
    }
    
    // memset_explicit garante que o compilador não otimizará a exclusão
    memset_explicit(account->secret_token, 0, sizeof(account->secret_token));
}

int main(void) {
    // Inicialização vazia C23
    UserAccountSecure user = {};
    snprintf(user.username, sizeof(user.username), "alice");
    snprintf(user.secret_token, sizeof(user.secret_token), "secret_12345");

    printf("[+] Usuário ativado: %s\n", user.username);

    wipe_sensitive_data(&user);
    return 0;
}
```

---

## ⚙️ Configuração de Build System Moderno (CMakeLists.txt C23)

```cmake
cmake_minimum_required(VERSION 3.25)
project(c23_modern_project C)

# Define o padrão C23 (ISO/IEC 9899:2024)
set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_executable(app_main src/main.c)

# Bateria estrita de avisos do compilador
if (MSVC)
    target_compile_options(app_main PRIVATE /W4 /WX)
else()
    target_compile_options(app_main PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror)
endif()
```

---

## 🔒 Questões de Segurança e Práticas Seguras

- **Buffer Overflows (CWE-121 / CWE-122)**: Nunca use funções inseguras como `strcpy`, `strcat`, `gets` ou `sprintf`. Substitua-as por equivalentes seguras como `strncpy`, `strncat`, `snprintf` ou funções de strings dinâmicas.
- **Estouros de Inteiro (CWE-190)**: Valide operações aritméticas antes da execução se o resultado for usado para alocação de memória (ex: `malloc(width * height)`). Use checagens seguras (ou `<stdckdint.h>` em C23).
- **Use-After-Free & Double Free (CWE-416 / CWE-415)**: Sempre anule ponteiros imediatamente após liberá-los (`free(ptr); ptr = NULL;`) para mitigar ponteiros órfãos.
- **Strings de Formatação (CWE-134)**: Nunca passe entradas do usuário diretamente como o formato de funções de impressão (use `printf("%s", input)` em vez de `printf(input)`).

## 🔗 Integração com Outras Skills

- Para compilar componentes em C++23 e interoperabilidade com C, consulte [lang-cpp](../lang-cpp/SKILL.md).
- Para realizar testes unitários seguros de funções em C utilizando o framework Criterion, consulte [framework-criterion](../../framework/framework-criterion/SKILL.md).
- Para auditoria de vulnerabilidades de estouro de buffer, format strings e ponteiros em código C, consulte [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
