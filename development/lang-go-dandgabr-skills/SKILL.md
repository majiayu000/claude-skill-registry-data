---
name: "lang-go"
description: "Fornece padrões de engenharia de software em Go (Golang) baseados na documentação oficial (go.dev/doc), Effective Go, Go Memory Model e boas práticas de concorrência (goroutines, channels, context), tratamento de erros, genéricos, módulos e testes."
---

# Habilidade de IA: Engenharia de Go (Go Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem **Go (Golang)**, seguindo estritamente as diretrizes da documentação oficial ([go.dev/doc](https://go.dev/doc/)), o guia **Effective Go** e o modelo de memória de Go. O objetivo é criar código idiomático, concorrente, de alta performance, fácil manutenção e fortemente testado.

---

## 🧭 Diretrizes Gerais de Desenvolvimento em Go

Ao atuar nesta skill, aplique rigorosamente os seguintes princípios idiomáticos da linguagem:

### 1. Estilo, Nomenclatura e Formatação (Effective Go)
- **`gofmt` Obrigatório**: Todo o código Go deve ser formatado utilizando a ferramenta oficial `gofmt` ou `goimports`.
- **Nomenclatura Simples e Curta**:
  - Variáveis locais devem ter nomes curtos e diretos (ex: `i` para índice, `r` para io.Reader, `err` para erro).
  - Use `MixedCaps` ou `camelCase` (nunca `snake_case`). Primeira letra maiúscula exporta o identificador para fora do pacote; minúscula mantém o acesso privado.
- **Interfaces Pequenas e Componíveis**: Prefira interfaces enxutas com um ou dois métodos (`io.Reader`, `io.Writer`, `fmt.Stringer`). A implementação é implícita (Duck Typing estático).
- **Sem Getters Ruidosos**: Não prefixe métodos com `Get`. O getter para o campo `user` deve ser nomeado apenas `User()`.

### 2. Tratamento Idiomático de Erros
- **Erros como Valores Explícitos**: Trate erros explicitamente imediatamente após a chamada (`if err != nil`). Nunca ignore erros com o identificador nulo `_` sem motivo documentado.
- **Encadeamento e Inspeção de Erros (Go 1.13+)**:
  - Envolva contexto aos erros usando `fmt.Errorf("falha ao processar ordem %d: %w", orderID, err)`.
  - Inspecione a cadeia de causa com `errors.Is(err, ErrNotFound)` e extraia tipos com `errors.As(err, &customErr)`.
- **Uso Restrito de `panic` e `recover`**: Reserve `panic` apenas para erros irrecuperáveis na inicialização da aplicação. Em bibliotecas e código de produção, retorne `error`.

### 3. Concorrência e Modelo de Memória
- **"Do not communicate by sharing memory; instead, share memory by communicating."**:
  - Prefira o uso de canais (`channels`) e `goroutines` para passar dados e coordenar tarefas entre processos.
- **Gerenciamento de Ciclo de Vida com `context.Context`**:
  - Passe `ctx context.Context` como primeiro parâmetro em chamadas de I/O, banco de dados ou RPCs para controlar timeouts e propagação de cancelamentos.
- **Sincronização Primitiva**:
  - Use `sync.WaitGroup` para aguardar a conclusão de grupos de goroutines.
  - Proteja o acesso concorrente a estruturas compartilhadas usando `sync.Mutex` ou `sync.RWMutex`.
- **Prevenção de Data Races**: Sempre valide a concorrência executando testes com a flag `-race` (`go test -race`).

### 4. Genéricos (Go 1.18+)
- Use parâmetros de tipo (`[T any]`, `[T comparable]`) quando a lógica for genérica para estruturas de dados (filas, pilhas, árvores) ou algoritmos utilitários.
- Não substitua interfaces orientadas a comportamento por genéricos desnecessários.

---

## 🛠️ Estrutura de Projeto e Ecossistema Go

### 1. Organização de Repositório (Standard Go Project Layout)
- **Go Modules (`go.mod`)**: Toda aplicação ou biblioteca deve utilizar módulos nativos.
- **Estrutura de Diretórios Recomendada**:
  - `cmd/`: Binários e pontos de entrada (`main.go`).
  - `internal/`: Código privado da aplicação que não deve ser importado por outros projetos.
  - `pkg/`: Código público de utilidade reutilizável por terceiros.
  - `api/`: Definições de contratos OpenAPIs, esquemas gRPC/Protobuf.

### 2. Frameworks e Bibliotecas Consolidadas
- **APIs Web e Roteadores**: `net/http` nativo (com as melhorias do Go 1.22+), `chi`, `gin`, `echo`, `fiber`.
- **Bancos de Dados e ORM**: `database/sql`, `pgx`, `sqlx`, `gorm`, `ent`, `sqlc`.
- **CLIs e Automação**: `cobra`, `viper`.
- **Comunicação RPC**: `gRPC` e `protocol buffers`.

---

## 🧰 Padrões de Código Recomendados

### 1. Handler HTTP Idiomático com Contexto e JSON (Go 1.22+)
```go
package user

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strconv"
)

type UserService interface {
	FindByID(ctx context.Context, id int64) (*User, error)
}

type Handler struct {
	service UserService
}

func NewHandler(s UserService) *Handler {
	return &Handler{service: s}
}

func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		http.Error(w, "ID inválido", http.StatusBadRequest)
		return
	}

	user, err := h.service.FindByID(r.Context(), id)
	if err != nil {
		if errors.Is(err, ErrNotFound) {
			http.Error(w, "Usuário não encontrado", http.StatusNotFound)
			return
		}
		http.Error(w, "Erro interno de processamento", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(user)
}
```

### 2. Worker Pool Concorrente com Canais e WaitGroup
```go
package worker

import (
	"context"
	"fmt"
	"sync"
)

type Job struct {
	ID   int
	Data string
}

func ProcessJobs(ctx context.Context, jobs []Job, numWorkers int) {
	jobChan := make(chan Job, len(jobs))
	var wg sync.WaitGroup

	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for {
				select {
				case <-ctx.Done():
					fmt.Printf("Worker %d interrompido pelo contexto\n", workerID)
					return
				case job, ok := <-jobChan:
					if !ok {
						return
					}
					fmt.Printf("Worker %d processando job %d: %s\n", workerID, job.ID, job.Data)
				}
			}
		}(i)
	}

	for _, j := range jobs {
		jobChan <- j
	}
	close(jobChan)

	wg.Wait()
}
```

### 3. Teste Orientado a Tabelas (Table-Driven Testing)
```go
package calc_test

import (
	"testing"
	"myproject/calc"
)

func TestDivide(t *testing.T) {
	tests := []struct {
		name        string
		a, b        float64
		want        float64
		wantErr     bool
	}{
		{name: "divisão exata", a: 10, b: 2, want: 5, wantErr: false},
		{name: "divisão por zero", a: 10, b: 0, want: 0, wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := calc.Divide(tt.a, tt.b)
			if (err != nil) != tt.wantErr {
				t.Fatalf("Divide(%f, %f) erro inesperado = %v, wantErr %v", tt.a, tt.b, err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("Divide(%f, %f) = %f, esperava %f", tt.a, tt.b, got, tt.want)
			}
		})
	}
}
```

---

## 🔒 Questões de Segurança e Práticas Seguras

- **Goroutine Leaks e Race Conditions**: Utilize sempre o detector de race conditions do Go (`go test -race`) durante o ciclo de testes. Certifique-se de que todas as goroutines possuem uma condição clara de término para evitar vazamentos de memória.
- **Manipulação Insegura (`unsafe` Package)**: Minimize o uso do pacote `unsafe`. Casts arbitrários de memória contornam a segurança de tipos do Go e podem levar a corrupções de memória inesperadas.
- **Geração de Segredos**: Nunca use `math/rand` para gerar tokens, senhas ou identificadores de sessão. Sempre utilize `crypto/rand` para geração de valores criptograficamente seguros.
- **Injeção de Comando em Processos**: Ao usar `os/exec`, evite passar strings concatenadas diretamente a shells como `sh` ou `bash`. Forneça argumentos como fatias separadas (`[]string`).

## 🔗 Integração com Outras Skills

- Para construir ferramentas de automação, varredura ou scripts de testes de invasão em Go, consulte [pentest-scripter-python-bash-go](../../security/appsec/pentest-scripter-python-bash-go/SKILL.md).
- Para integrar chamadas concorrentes e transacionais em bancos de dados em Go (`database/sql`, `pgx`, `gorm`, `sqlc`), consulte [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md), [db-postgresql](../../databases/db-postgresql/SKILL.md), [db-mariadb](../../databases/db-mariadb/SKILL.md), [db-sqlite](../../databases/db-sqlite/SKILL.md) e [db-mongodb](../../databases/db-mongodb/SKILL.md).
- Para aplicar análise estática de código e segurança em serviços web em Go, consulte [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
- Para projetar arquiteturas de microsserviços escaláveis em Go, consulte [software-architect](../../roles/software-architect/SKILL.md).
