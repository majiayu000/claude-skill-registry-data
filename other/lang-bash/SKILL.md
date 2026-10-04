---
name: "lang-bash"
description: "Fornece padrões de engenharia de software em Bash/Shell Scripting. Cobre execução estrita e segura (set -euo pipefail), manipulação defensiva de variáveis e aspas, funções modulares, verificação de dependências, manipulação de arquivos/redirecionamento, além de integração com ShellCheck e boas práticas de portabilidade."
---

# Habilidade de IA: Engenharia de Bash (Bash & Shell Scripting Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista em **Bash e Shell Scripting**, com foco em scripts seguros, previsíveis, portáveis e com tratamento estrito de erros para automação de sistemas, rotinas de CI/CD e administração de servidores Linux/Unix.

---

## 🧭 Diretrizes de Desenvolvimento em Bash

Ao atuar nesta skill, aplique rigorosamente os seguintes padrões:

### 1. Modo Estrito e Segurança de Execução
- **Configuração Inicial Estrita**: Todo script Bash deve iniciar definindo o modo estrito:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  IFS=$'\n\t'
  ```
  - `set -e`: Interrompe a execução imediatamente se qualquer comando retornar status diferente de zero (falha).
  - `set -u`: Trata o uso de variáveis não declaradas/não inicializadas como erro.
  - `set -o pipefail`: Garante que pipelines (`cmd1 | cmd2`) retornem o código de erro do primeiro comando a falhar no pipeline, e não apenas o último.
  - `IFS=$'\n\t'`: Previne *word splitting* indesejado baseado em espaços em branco.

### 2. Manipulação Defensiva de Variáveis e Aspas
- **Aspas em Variáveis**: Sempre envolva o uso de variáveis entre aspas duplas: `"$var"` ou `"${var}"`. Isso evita vazamentos por *word splitting* ou expansão de *globbing*.
- **Uso de Chaves**: Prefira a sintaxe `${var}` para clareza e desambiguação sintática.
- **Valores Padrão**: Use a expansão de parâmetros para tratar variáveis opcionais de forma defensiva:
  ```bash
  LOG_LEVEL="${LOG_LEVEL:-INFO}"
  PORT="${1:-8080}"
  ```

### 3. Funções Modulares e Escopo Local
- **Variáveis Locais**: Declare TODAS as variáveis internas de funções com a palavra-chave `local`.
- **Valores de Retorno**: Funções Bash retornam um código de status numérico (`return 0` para sucesso, `return 1-255` para erros). Para "retornar" dados, imprima no `stdout` e capture com substituição de comando: `result=$(my_function)`.
- **Separar Logs da Saída Útil**: Envie mensagens de log e diagnósticos para o `stderr` (`>&2`) para não poluir a saída principal capturada pelo caller.

### 4. Gestão de Recursos e Limpeza com `trap`
- **Garantia de Cleanup**: Utilize `trap` para capturar sinais de término (`EXIT`, `INT`, `TERM`) e garanta a remoção de arquivos temporários, liberação de locks ou restauração do estado do sistema.

### 5. Portabilidade e Verificação de Dependências
- **Shebang Portável**: Use `#!/usr/bin/env bash` em vez de caminhos fixos como `#!/bin/bash`.
- **Validar Binários Externos**: Antes de invocar utilitários como `jq`, `curl`, ou `docker`, verifique a existência deles no `PATH`:
  ```bash
  command -v jq >/dev/null 2>&1 || { echo "Erro: 'jq' é necessário mas não está instalado." >&2; exit 1; }
  ```
- **Conformidade com ShellCheck**: Escreva código limpo de acordo com as regras de análise estática do ShellCheck.

---

## 🧰 Padrões de Código Recomendados

### Template de Script Profissional e Robusto com Cleanup e Option Parsing

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Configurações e Globais
readonly SCRIPT_NAME="$(basename "$0")"
readonly TMP_DIR="$(mktemp -d -t "${SCRIPT_NAME}.XXXXXX")"

# Função de Limpeza (Executada automaticamente no EXIT)
cleanup() {
    local exit_code=$?
    if [[ -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
    exit "$exit_code"
}
trap cleanup EXIT INT TERM

# Funções de Logging (Direcionadas para stderr)
log_info() {
    printf '[INFO] %s\n' "$*" >&2
}

log_error() {
    printf '[ERROR] %s\n' "$*" >&2
}

usage() {
    cat <<EOF
Uso: ${SCRIPT_NAME} [OPÇÕES] -i <input_file>

Opções:
  -i, --input FILE    Caminho do arquivo de entrada (obrigatório)
  -o, --output FILE   Caminho do arquivo de saída (opcional)
  -h, --help          Exibe esta ajuda
EOF
}

# Parsing de Argumentos
parse_args() {
    local input_file=""
    local output_file=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -i|--input)
                input_file="${2:-}"
                shift 2
                ;;
            -o|--output)
                output_file="${2:-}"
                shift 2
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Opção desconhecida: $1"
                usage
                exit 1
                ;;
        esac
    done

    if [[ -z "$input_file" ]]; then
        log_error "O parâmetro --input é obrigatório."
        usage
        exit 1
    fi

    echo "$input_file" "$output_file"
}

# Função Principal
main() {
    local input_file=""
    local output_file=""

    read -r input_file output_file <<< "$(parse_args "$@")"

    if [[ ! -f "$input_file" ]]; then
        log_error "Arquivo de entrada não encontrado: $input_file"
        exit 1
    fi

    log_info "Processando o arquivo: $input_file"
    local temp_output="${TMP_DIR}/processed.txt"

    # Exemplo de processamento seguro linha a linha
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Processa apenas linhas não vazias e que não são comentários
        if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
            printf 'PROCESSED: %s\n' "$line" >> "$temp_output"
        fi
    done < "$input_file"

    if [[ -n "$output_file" ]]; then
        mv "$temp_output" "$output_file"
        log_info "Resultado salvo em: $output_file"
    else
        cat "$temp_output"
    fi
}

main "$@"
```

### Verificação de Dependências e Leitura Segura de Arquivos JSON

```bash
#!/usr/bin/env bash
set -euo pipefail

# Garante dependências antes da execução
check_dependencies() {
    local dep
    for dep in jq curl; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            printf '[ERROR] Dependência ausente: %s\n' "$dep" >&2
            return 1
        fi
    done
}

fetch_github_user() {
    local username="${1:-}"
    if [[ -z "$username" ]]; then
        printf '[ERROR] Usuário não informado.\n' >&2
        return 1
    fi

    local response
    response=$(curl -sSL "https://api.github.com/users/${username}")

    local name
    name=$(echo "$response" | jq -r '.name // "N/A"')

    printf 'User: %s | Name: %s\n' "$username" "$name"
}

main() {
    check_dependencies || exit 1
    fetch_github_user "octocat"
}

main "$@"
```

## 🔒 Questões de Segurança e Práticas Seguras

- **Injeção de Comando**: Evite expandir variáveis diretamente em comandos do sistema. Use aspas duplas sempre que possível (`"$var"` em vez de `$var`) para evitar divisão de palavras e globbing.
- **Definições Seguras de Inicialização**: Use sempre `set -euo pipefail` no início dos scripts para que o interpretador pare imediatamente em caso de erro, variáveis indefinidas ou falhas ocultas em pipelines.
- **Manipulação de Variável $PATH**: Evite executar binários relativos ou depender de um `$PATH` herdado não controlado. Defina um `$PATH` explícito no início de scripts SUID ou administrativos.
- **Arquivos Temporários**: Nunca crie arquivos temporários fixos (ex: `/tmp/temp.txt`). Use o comando `mktemp` para gerar nomes de arquivos temporários aleatórios e seguros.

