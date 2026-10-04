---
name: go-testing
description: >
  Testing en Go con la biblioteca estándar y Bubbletea — tests unitarios,
  table-driven tests, mocking y cobertura.
  Trigger: Cuando escribís tests en Go, usás teatest, o agregás cobertura.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: go-testing

Testing en Go. Table-driven, parallel, sin magia.

## Trigger

- Escribiste una función en Go y necesitás testearla
- Querés agregar cobertura a un paquete
- Usás Bubbletea y necesitás testear el modelo
- Un test existente falla y hay que debuggearlo

## Workflow LEND

1. ANALIZAR
   ├── Paquete: ¿funciones puras, I/O, Bubbletea model?
   ├── Tipo: unitario (funciones) o integración (handler, DB)
   ├── Dependencias: ¿interfaces para mockear?
   └── Cobertura actual: go test -cover

2. OFRECER (Menú del Senior)
   ├── A) Test unitario — table-driven test para funciones puras
   ├── B) Test con mock — interfaces + stub para dependencias externas
   └── C) Bubbletea test — teatest para modelos TUI

3. ELEGIR → confirmación

4. HACER
   ├── Archivo: *_test.go, misma carpeta que el código
   ├── Table-driven: []struct{name, input, expected} + t.Run
   ├── t.Parallel() en tests independientes
   ├── Cobertura: go test -cover -coverprofile=coverage.out
   ├── Bubbletea: teatest.NewTestModel + teatest.WaitFor
   └── Assert: testing package, sin librerías externas de assert

5. VERIFICAR
   ├── go test ./... pasa sin errores
   ├── Cobertura > 70% en paquetes críticos
   └── Los tests paralelos no compiten por recursos compartidos
