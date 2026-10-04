---
name: "framework-criterion"
description: "Atua como Especialista em testes unitários para a linguagem C utilizando Criterion, cobrindo macros Test, cr_assert/cr_expect, ciclos de vida (.init/.fini), teste de sinais/crashes, captura de stdout/stderr e integração com CMake."
---

# Habilidade de IA: Especialista em Testes com Criterion em C (Criterion Specialist)

Esta skill orienta a inteligência artificial a agir como **Engenheiro de QA e Desenvolvimento de Software em C especializado no framework Criterion**. O objetivo é guiar a criação de suítes de testes unitários modernos, seguros e concisos em C (C99, C11, C17, C23), cobrindo asserções de memória, teste de sinais/sistemas, redirecionamento de entrada/saída padrão e integração com pipelines CMake/Meson.

---

## 🧭 Princípios e Arquitetura do Criterion

Ao utilizar o Criterion em projetos de código C:
- **Sintaxe Limpa e Declarativa**: Utilize a macro `Test(suite_name, test_name)` para definir suítes e testes sem necessidade de escrever funções `main()` ou registrar testes manualmente.
- **Asserções e Expectativas**:
  - `cr_assert_*`: Interrompe imediatamente a execução do teste atual se a condição for falsa.
  - `cr_expect_*`: Marca a falha no relatório final, mas permite que o teste continue sendo executado.
- **Isolamento por Processos (Process Isolation)**: O Criterion executa cada teste em um processo isolado separado via `fork()`. Crashes (como `SIGSEGV` por ponteiro nulo) em um teste não interrompem a suíte completa.
- **Redirecionamento de I/O Nativo**: Teste saídas para `stdout` e `stderr` capturando descritores de arquivo nativamente.

---

## 🛠️ Diretrizes Práticas de Engenharia e Padrões de Código

### 1. Testes Unitários de Funções C (`cr_assert_eq`, `cr_assert_str_eq`)
- Utilize macros de comparação tipadas para mensagens de erro detalhadas.

```c
#include <criterion/criterion.h>
#include <criterion/new/assert.h>
#include "calculator.h"

Test(calculator_suite, test_add_positive_numbers) {
    int result = add(15, 25);
    cr_assert_eq(result, 40, "Esperado 40, mas obteve %d", result);
}

Test(calculator_suite, test_string_formatting) {
    char *formatted = format_currency(100.50);
    cr_assert_str_eq(formatted, "$100.50", "String formatada incorreta: %s", formatted);
    free(formatted); // Limpeza de memória
}
```

### 2. Configuração de Ciclo de Vida (`.init` e `.fini`)
- Defina funções de setup (`.init`) e teardown (`.fini`) diretamente nos parâmetros adicionais da macro `Test`.

```c
#include <criterion/criterion.h>
#include <stdio.h>
#include "database_driver.h"

static DBConnection *db_conn = NULL;

void setup_db(void) {
    db_conn = db_connect("sqlite::memory:");
    db_create_tables(db_conn);
}

void teardown_db(void) {
    if (db_conn) {
        db_disconnect(db_conn);
        db_conn = NULL;
    }
}

Test(database_suite, test_insert_record, .init = setup_db, .fini = teardown_db) {
    cr_assert_not_null(db_conn, "Conexão com o banco de dados deve estar ativa.");
    int status = db_insert(db_conn, "users", "Alice");
    cr_assert_eq(status, DB_SUCCESS, "Falha ao inserir registro.");
}
```

### 3. Teste de Sinais, Crashes e Timeouts (`.signal` e `.timeout`)
- Garanta que funções defensivas em C tratem ponteiros nulos ou disparem `SIGSEGV`/`SIGABRT` quando apropriado.

```c
#include <criterion/criterion.h>
#include <signal.h>
#include "utils.h"

// Teste espera que a função dispare Segmentation Fault se receber ponteiro nulo
Test(safety_suite, test_null_pointer_crash, .signal = SIGSEGV) {
    process_buffer(NULL, 100);
}

// Teste é cancelado se demorar mais de 1.5 segundos
Test(performance_suite, test_infinite_loop_prevention, .timeout = 1.5) {
    compute_complex_hash("payload");
}
```

### 4. Teste de Saída Padrão (`stdout` / `stderr`)
- Redirecione e valide dados impressos com `printf`.

```c
#include <criterion/criterion.h>
#include <criterion/redirect.h>
#include <stdio.h>

void setup_redirects(void) {
    cr_redirect_stdout();
    cr_redirect_stderr();
}

Test(cli_suite, test_print_welcome_message, .init = setup_redirects) {
    puts("Bem-vindo ao Sistema!");
    cr_assert_stdout_eq_str("Bem-vindo ao Sistema!\n");
}
```

---

## ⚙️ Integração com Build System (CMakeLists.txt)

```cmake
cmake_minimum_required(VERSION 3.14)
project(c_project_tests C)

set(CMAKE_C_STANDARD 11)

find_package(PkgConfig REQUIRED)
pkg_check_modules(CRITERION REQUIRED criterion)

add_executable(run_tests 
    tests/test_main.c 
    src/calculator.c
)

target_include_directories(run_tests PRIVATE src/ ${CRITERION_INCLUDE_DIRS})
target_link_libraries(run_tests PRIVATE ${CRITERION_LIBRARIES})

enable_testing()
add_test(NAME criterion_tests COMMAND run_tests)
```

---

## 🔗 Integração com Outras Skills

- [lang-c](../../languages/lang-c/SKILL.md): Garante conformidade de padrões C (C11/C17), prevenção de comportamentos indefinidos (UB) e gestão de memória.
- [qa-engineer](../../roles/qa-engineer/SKILL.md): Orienta o desenho de suítes de testes unitários para software embarcado e sistemas de baixo nível.
- [framework-testing](../framework-testing/SKILL.md): Fornece os conceitos teóricos de TDD e pirâmide de testes.
