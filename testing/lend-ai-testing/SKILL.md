---
name: lend-ai-testing
description: >
  GATE OBLIGATORIO pre-commit/pre-PR — tests unitarios, CI, cobertura.
  NADA se sube sin tests en verde. Trigger: Siempre antes de cada commit
  o PR, o al escribir tests/configurar CI/revisar calidad.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
---

# Skill: lend-ai-testing

GATE OBLIGATORIO. No se comitea nada sin tests en verde.

## Trigger (ejecutar SIEMPRE antes de commit/PR)

- **Terminaste código → corré tests antes de commit**
- Vas a configurar o modificar el CI
- Querés medir cobertura o mejorarla
- Un test existente falla

## Regla de ORO

**Nunca hagas commit sin testear antes.** Es GATE obligatorio.
Si el orquestador te llama para commit, lo primero es verificar tests.

## Workflow LEND (obligatorio, no opcional)

1. DETECTAR
   ├── Stack del proyecto: ¿pytest, vitest, go test, nose?
   ├── ¿Ya existe suite de tests? → correrla completa
   └── ¿No hay tests? → avisar al orquestador: "no hay tests, hay que crearlos"

2. EJECUTAR (automático, sin menú)
   ├── Correr suite existente completa
   ├── pytest → `python -m pytest` / vitest → `npx vitest run`
   └── Revisar que TODO pase en verde

3. SI FALLA
   ├── Diagnosticar causa raíz
   ├── Fixear o avisar al orquestador
   └── NO seguir hasta que esté en verde

4. SI NO HAY TESTS
   ├── Crear tests mínimos para el cambio actual
   ├── Unit tests para funciones nuevas
   ├── Integration tests si cruza módulos
   └── Verificar que pasan

5. VERIFICAR (antes de devolver control)
   ├── ✅ Suite completa en verde
   ├── ✅ Cobertura aceptable (mínimo 80% en líneas nuevas)
   └── ✅ Resultado: "Tests OK, podés comitear"
