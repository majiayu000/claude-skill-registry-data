---
name: gherkin-standards
description: "Buenas practicas, convenciones y ejemplos de escritura Gherkin para BDD. Incluye formato de archivo de test case, nomenclatura y matriz de cobertura."
---

# Gherkin Standards Skill

Estandares para disenio de casos de prueba en formato Gherkin (BDD).

## Formato de Archivo de Test Case

```markdown
# TC-{nn}: {Titulo descriptivo}

**Historia de Usuario**: HU-{nn}
**Criterios cubiertos**: CA-{nn}.{x}, CA-{nn}.{y}
**Tipo**: {Happy Path | Negativo | Borde | E2E}
**Prioridad**: {Alta | Media | Baja}
**Precondiciones**: {Estado inicial requerido}
**URL**: {URL de la aplicacion}
**Datos de prueba**: {datos especificos a utilizar}

## Escenario Gherkin

` ` `gherkin
Feature: {Nombre de la funcionalidad}

  Scenario: {Descripcion del escenario}
    Given {precondicion o estado inicial}
    When {accion del usuario}
    And {accion complementaria}
    Then {resultado esperado verificable}
    And {validacion adicional}
` ` `

## Pasos Detallados

| # | Keyword | Descripcion | Datos | Resultado Esperado |
|---|---------|-------------|-------|-------------------|
| 1 | Given | {descripcion} | {datos} | {resultado} |
| 2 | When | {descripcion} | {datos} | {resultado} |
| 3 | Then | {descripcion} | {datos} | {resultado} |
```

## Nomenclatura de Archivos
- Formato: `TC-{nn}-{descripcion-kebab-case}.md`
- Numeracion global consecutiva: TC-01, TC-02, TC-03...
- Ejemplos: `TC-01-busqueda-exitosa-id-valida.md`, `TC-02-busqueda-sin-datos-requeridos.md`

## Adaptacion por Modo de Prueba

### Modo `positivos`
- Solo escenarios Happy Path
- Tipo: `Happy Path`
- 1 test case por criterio de aceptacion positivo
- Given con precondiciones validas, When con datos correctos, Then valida exitos

### Modo `negativos`
- Solo escenarios de error
- Tipo: `Negativo`
- 1 test case por criterio de error
- When con datos invalidos, Then valida mensajes de error

### Modo `borde`
- Solo escenarios de valores limite
- Tipo: `Borde`
- Test cases para minimo, maximo, longitud maxima, vacio, caracteres especiales

### Modo `e2e`
- UN unico test case que cubre el flujo completo
- Tipo: `E2E`
- Recorre autenticacion -> navegacion -> operacion principal -> resultado final
- Maximo 2 test cases E2E

## Matriz de Cobertura

```markdown
## Matriz de Cobertura

| Criterio | Test Case | Tipo |
|----------|-----------|------|
| CA-01.1 | TC-01 | Happy Path |
| CA-01.2 | TC-02 | Negativo |
```

## Constraints
- SOLO crear test cases basados en user-stories.md
- Generar unicamente el tipo que corresponda al testMode
- NO mezclar tipos
- Datos de prueba ESPECIFICOS y concretos
- Resultados esperados VERIFICABLES visualmente
- Un archivo MD por test case
- Registrar testMode en cada test case
