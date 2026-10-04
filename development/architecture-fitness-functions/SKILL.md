---
name: architecture-fitness-functions
description: >
  Converte uma regra de arquitetura documentada em prosa (arquivo raiz do
  agente, ADR, code review recorrente) num teste automatizado e
  determinístico — uma fitness function. Stack-agnóstico: exemplos para
  Python/pytest, Swift/XCTest, Kotlin/Konsist, Node/dependency-cruiser. Use
  quando uma regra de arquitetura for violada mais de uma vez apesar de estar
  documentada, ou ao desenhar o sensor computacional de um harness novo.
license: MIT
metadata:
  author: exported-from-uimaker-adk
  version: "1.0"
---

# Skill — Architecture Fitness Functions

Uma **fitness function** (Ford/Parsons/Kua, *Building Evolutionary
Architectures*) é um teste automatizado que verifica uma propriedade
arquitetural — não comportamento de negócio. É o sensor computacional que
substitui "confiar que o agente/dev leu a regra e lembrou dela".

## Quando promover uma regra para fitness function

Use o sinal do `dev-harness-architect`: se uma regra documentada em prosa
(arquivo raiz do agente) é violada **duas vezes** por revisão manual ou
review de agente, ela deveria ter virado teste desde a primeira vez. Regra
prática: se a violação pode ser detectada por um grep, um parse de AST, ou
uma checagem de grafo de dependências — é candidata imediata, não espere a
segunda violação.

## As 5 famílias de regras mais comuns

1. **Direção de dependência entre camadas** — ex. "domínio não importa
   camada de apresentação". Detector: parse de imports/`import`s do arquivo,
   comparar contra uma lista de camadas proibidas.
2. **Gateway único para uma operação perigosa** — ex. "toda escrita em disco
   passa por um módulo único", "toda chamada de rede passa por um client
   único". Detector: grep pela API nativa (`open(...)`, `FileManager`,
   `URLSession`, `File(...)`) fora do módulo permitido.
3. **Padrão proibido** — ex. "sem `print()` fora da camada de CLI", "sem
   `try!`/força-desembrulho fora de testes", "sem captura ampla de exceção".
   Detector: grep/regex linha a linha, com allowlist de diretórios.
4. **Sem segredo literal** — ex. `token = "..."`. Detector: regex sobre
   atribuições que parecem credencial.
5. **Contrato de saída obrigatório** — ex. "todo agente novo tem um teste de
   schema". Detector: verificar que para cada arquivo novo em `agents/`
   existe um arquivo correspondente em `tests/` que importa o schema.

## Estrutura comum (independente de stack)

Toda fitness function segue a mesma forma:

```
Regra → Detector (varre arquivos, coleta violações) → Assert (lista vazia) → Mensagem (arquivo:linha + trecho)
```

A mensagem de falha deve apontar exatamente onde e sugerir a correção — o
agente que vai ler essa falha não tem contexto da conversa que gerou a
regra.

## Exemplo — Python / pytest (`ast` + regex)

```python
"""Architecture fitness sensors — enforce root-guide rules at test time."""
import ast
import re
from pathlib import Path

SRC = Path(__file__).parent.parent.parent / "src" / "mypkg"
OUTER_LAYERS = {"cli", "api"}


def _imports(filepath: Path) -> list[str]:
    tree = ast.parse(filepath.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def test_domain_does_not_import_outer_layers() -> None:
    violations = []
    for py_file in (SRC / "domain").rglob("*.py"):
        for imp in _imports(py_file):
            if any(f"mypkg.{layer}" in imp for layer in OUTER_LAYERS):
                violations.append(f"{py_file}: imports {imp}")
    assert not violations, "domain/ must not depend on outer layers:\n" + "\n".join(violations)


_SECRET = re.compile(r'(api_key|token|password|secret)\s*=\s*"[^"]{6,}"', re.IGNORECASE)


def test_no_hardcoded_secrets() -> None:
    violations = []
    for py_file in SRC.parent.parent.rglob("*.py"):
        if ".venv" in py_file.parts:
            continue
        for i, line in enumerate(py_file.read_text(encoding="utf-8").splitlines(), 1):
            if _SECRET.search(line):
                violations.append(f"{py_file}:{i}: [REDACTED]")
    assert not violations, "Hardcoded secrets detected:\n" + "\n".join(violations)
```

Rode em CI como um tier próprio (`pytest tests/structural/ -x -q`), separado
dos testes de comportamento — falha rápida e não depende de fixtures pesadas.

## Exemplo — Swift/iOS (regra de gateway único, sem dependências)

Swift não tem um `ast` acessível em stdlib de forma trivial para scripts
soltos; a abordagem mais barata é regex linha a linha, rodando como um
script Python (independente do projeto ser Swift — o script só *lê* arquivos
`.swift`) ou como custom rule do SwiftLint.

**Opção A — script Python que varre `.swift` (funciona sem SwiftLint):**

```python
import re
import sys
from pathlib import Path

SRC = Path("Sources")
FORBIDDEN = re.compile(r"\bURLSession\.shared\b")
ALLOWLIST_DIR = "Networking"

violations = []
for swift_file in SRC.rglob("*.swift"):
    if ALLOWLIST_DIR in swift_file.parts:
        continue
    for i, line in enumerate(swift_file.read_text(encoding="utf-8").splitlines(), 1):
        if FORBIDDEN.search(line):
            violations.append(f"{swift_file}:{i}: {line.strip()[:80]}")

if violations:
    print("URLSession.shared usado fora de Networking/:")
    print("\n".join(violations))
    sys.exit(1)
```

**Opção B — SwiftLint custom rule** (`.swiftlint.yml`), se o projeto já usa
SwiftLint:

```yaml
custom_rules:
  no_direct_urlsession:
    included: ".*\\.swift"
    excluded: ".*/Networking/.*"
    regex: "URLSession\\.shared"
    message: "Use o client de rede único em Networking/, não URLSession.shared direto."
    severity: error
```

Para regra de direção de dependência (ex. "Domain não importa UIKit/SwiftUI"),
o mesmo script Python funciona: procure `import UIKit`/`import SwiftUI` dentro
de `Sources/Domain/`.

## Exemplo — Kotlin/Android (Konsist)

[Konsist](https://github.com/LemonAppDev/konsist) é uma lib de teste de
arquitetura nativa em Kotlin, roda junto do JUnit:

```kotlin
class ArchitectureTest {
    @Test
    fun `domain does not depend on outer layers`() {
        Konsist.scopeFromProject()
            .packages("..domain..")
            .assertFalse {
                it.imports.any { imp ->
                    imp.name.contains("..ui..") || imp.name.contains("..data..")
                }
            }
    }

    @Test
    fun `no direct File access outside storage package`() {
        Konsist.scopeFromProject()
            .files
            .filterNot { it.packagee?.name?.contains("..storage..") == true }
            .assertFalse { file -> file.text.contains("java.io.File(") }
    }
}
```

Sem Konsist, a mesma ideia funciona com uma regra custom do Detekt (arquivo
`detekt-rules/` + config em `detekt.yml`), mais verboso mas sem dependência
extra de teste.

## Exemplo — Node/TypeScript (dependency-cruiser)

Para direção de dependência entre camadas, `dependency-cruiser` já resolve
sem escrever regex:

```json
{
  "forbidden": [
    {
      "name": "domain-no-outer-layers",
      "severity": "error",
      "from": { "path": "^src/domain" },
      "to": { "path": "^src/(cli|api)" }
    }
  ]
}
```

```bash
npx depcruise src --config .dependency-cruiser.json
```

Para padrões proibidos (sem `console.log` fora de `cli/`, sem segredo
literal), `eslint` com uma regra custom ou um script de regex — mesma forma
dos exemplos acima.

## Checklist ao escrever uma fitness function nova

- [ ] A regra já existe em prosa no arquivo raiz do agente? Se não, adicione
      lá também — o teste sozinho não ensina o agente a evitar a violação
      antes de tentar; ele só pega depois.
- [ ] O detector tem um teste negativo (fixture que viola a regra de
      propósito) para provar que o sensor de fato dispara?
- [ ] A mensagem de falha diz o arquivo, a linha e a correção esperada?
- [ ] O teste roda em segundos, não minutos — senão vai para o tier de CI
      certo (não pre-commit) em vez de ficar esquecido/desabilitado.
- [ ] Existe um allowlist explícito de exceções (diretório onde a regra não
      se aplica), em vez de exceções implícitas via `# noqa`/`// nolint`
      espalhadas pelo código?
